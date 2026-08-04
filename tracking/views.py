"""Validated, privacy-aware tracking endpoints."""

from __future__ import annotations

import hashlib
import hmac
import ipaddress
import json
import logging
import re
import uuid
from datetime import datetime, timedelta, timezone as datetime_timezone
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from django.conf import settings
from django.db import DatabaseError, transaction
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django_ratelimit.decorators import ratelimit

from .models import TrackEvent, TrackSession

logger = logging.getLogger(__name__)

MAX_BODY_SIZE = 65_536
MAX_EVENTS_PER_BATCH = 50
TIMESTAMP_WINDOW = timedelta(minutes=30)

ALLOWED_EVENTS = frozenset(
    {
        "page_view",
        "scroll_depth",
        "time_on_page",
        "cta_impression",
        "outbound_click",
        "phone_click",
        "zip_modal_open",
        "zip_check",
        "booking_click",
        "booking_form_submit",
        "faq_expand",
        "nav_click",
        "contact_email_sent",
        "booking_completed",
    }
)

EVENT_PROPERTY_KEYS: dict[str, frozenset[str]] = {
    "page_view": frozenset({"title", "path"}),
    "scroll_depth": frozenset({"depth"}),
    "time_on_page": frozenset({"seconds"}),
    "cta_impression": frozenset({"cta"}),
    "outbound_click": frozenset({"target"}),
    "phone_click": frozenset({"location"}),
    "zip_modal_open": frozenset({"source"}),
    "zip_check": frozenset({"in_service_area"}),
    "booking_click": frozenset({"source"}),
    "booking_form_submit": frozenset({"service"}),
    "faq_expand": frozenset({"question"}),
    "nav_click": frozenset({"label"}),
    "contact_email_sent": frozenset({"utm_source"}),
    "booking_completed": frozenset({"booking_id", "service"}),
}

_MOBILE_RE = re.compile(r"Mobile|Android|iPhone|iPad|iPod", re.IGNORECASE)
_TABLET_RE = re.compile(r"iPad|Tablet|PlayBook|Silk", re.IGNORECASE)
_BROWSER_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"Edg(?:e|A|iOS)?/([\d.]+)"), "Edge"),
    (re.compile(r"OPR/([\d.]+)"), "Opera"),
    (re.compile(r"Chrome/([\d.]+)"), "Chrome"),
    (re.compile(r"Version/([\d.]+).*Safari/([\d.]+)"), "Safari"),
    (re.compile(r"Firefox/([\d.]+)"), "Firefox"),
)
_OS_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"Windows NT ([\d.]+)"), "Windows"),
    (re.compile(r"Mac OS X ([\d_.]+)"), "macOS"),
    (re.compile(r"Android ([\d.]+)"), "Android"),
    (re.compile(r"iPhone OS ([\d_]+)"), "iOS"),
    (re.compile(r"iPad.*OS ([\d_]+)"), "iPadOS"),
    (re.compile(r"Linux"), "Linux"),
)


def _collect_rate(_group: str, _request: HttpRequest) -> str:
    return str(getattr(settings, "TRACKING_COLLECT_RATE", "30/m"))


def _webhook_rate(_group: str, _request: HttpRequest) -> str:
    return str(getattr(settings, "TRACKING_WEBHOOK_RATE", "10/m"))


def _parse_ua(user_agent: str) -> tuple[str, str, str]:
    if not user_agent:
        return "desktop", "", ""
    if _TABLET_RE.search(user_agent):
        device = "tablet"
    elif _MOBILE_RE.search(user_agent):
        device = "mobile"
    else:
        device = "desktop"
    browser = next(
        (name for pattern, name in _BROWSER_PATTERNS if pattern.search(user_agent)),
        "",
    )
    os_name = next(
        (name for pattern, name in _OS_PATTERNS if pattern.search(user_agent)),
        "",
    )
    return device, browser, os_name


def _privacy_ip_hash(value: str) -> str:
    """Key-hash a reduced subnet, never the exact client address."""
    try:
        address = ipaddress.ip_address(value)
    except ValueError:
        return ""
    prefix = 24 if address.version == 4 else 48
    reduced = str(ipaddress.ip_network(f"{address}/{prefix}", strict=False).network_address)
    key = str(
        getattr(settings, "TRACKING_IP_HASH_KEY", "")
        or getattr(settings, "SECRET_KEY", "")
    )
    if not key:
        return ""
    return hmac.new(key.encode(), reduced.encode(), hashlib.sha256).hexdigest()


def _valid_uuid4(value: object) -> uuid.UUID | None:
    try:
        parsed = uuid.UUID(str(value))
    except (AttributeError, TypeError, ValueError):
        return None
    return parsed if parsed.version == 4 else None


def _safe_text(value: object, max_length: int) -> str:
    if not isinstance(value, (str, int, float)) or isinstance(value, bool):
        return ""
    text = "".join(char for char in str(value) if char >= " " and char != "\x7f")
    return text.strip()[:max_length]


def _safe_int(value: object) -> int | None:
    try:
        result = int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
    return result if 0 < result < 10_000 else None


def _sanitize_url(
    value: object,
    request: HttpRequest,
    *,
    same_origin: bool,
) -> str:
    if not isinstance(value, str) or not value or len(value) > 2000:
        return ""
    candidate = request.build_absolute_uri(value) if value.startswith("/") else value
    try:
        parsed = urlsplit(candidate)
    except ValueError:
        return ""
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return ""
    if parsed.username or parsed.password:
        return ""
    if same_origin and parsed.netloc.lower() != request.get_host().lower():
        return ""
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path or "/", "", ""))[:2000]


def _sanitize_properties(event_name: str, value: object) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    allowed = EVENT_PROPERTY_KEYS.get(event_name, frozenset())
    clean: dict[str, Any] = {}
    for key in allowed:
        item = value.get(key)
        if isinstance(item, bool):
            clean[key] = item
        elif isinstance(item, (int, float)) and not isinstance(item, bool):
            if -1_000_000 <= item <= 1_000_000:
                clean[key] = item
        else:
            text = _safe_text(item, 200)
            if text:
                clean[key] = text
    return clean


def _origin_allowed(request: HttpRequest) -> bool:
    if not getattr(settings, "TRACKING_REQUIRE_ORIGIN", True):
        return True
    origin = request.headers.get("Origin", "")
    if not origin or origin == "null":
        return False
    try:
        parsed = urlsplit(origin)
    except ValueError:
        return False
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return False
    normalized = f"{parsed.scheme}://{parsed.netloc}".rstrip("/")
    request_origin = f"{request.scheme}://{request.get_host()}".rstrip("/")
    configured = {
        str(item).rstrip("/")
        for item in getattr(settings, "TRACKING_ALLOWED_ORIGINS", ())
        if item
    }
    return normalized == request_origin or normalized in configured


def _is_privacy_opt_out(request: HttpRequest) -> bool:
    return request.headers.get("DNT") == "1" or request.headers.get("Sec-GPC") == "1"


def _json_body(request: HttpRequest) -> dict[str, Any] | None:
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
        return None
    return data if isinstance(data, dict) else None


@csrf_exempt
@require_POST
@ratelimit(group="tracking-collect", key="ip", rate=_collect_rate, method="POST", block=True)
def collect(request: HttpRequest) -> HttpResponse:
    """Collect a consented same-origin event batch without setting cookies."""
    if not getattr(settings, "TRACKING_ENABLED", False) or _is_privacy_opt_out(request):
        return HttpResponse(status=204)
    if request.content_type != "application/json":
        return JsonResponse({"error": "Unsupported content type"}, status=415)
    if len(request.body) > MAX_BODY_SIZE:
        return JsonResponse({"error": "Payload too large"}, status=413)
    if not _origin_allowed(request):
        return JsonResponse({"error": "Origin not allowed"}, status=403)

    data = _json_body(request)
    if data is None:
        return JsonResponse({"error": "Invalid JSON object"}, status=400)
    if getattr(settings, "TRACKING_REQUIRE_CONSENT", True) and data.get("consent") is not True:
        return HttpResponse(status=204)

    session_id = _valid_uuid4(data.get("session_id"))
    if session_id is None:
        return JsonResponse({"error": "Invalid session_id"}, status=400)
    events = data.get("events", [])
    if not isinstance(events, list) or len(events) > MAX_EVENTS_PER_BATCH:
        return JsonResponse({"error": "Invalid events"}, status=400)

    now = timezone.now()
    window_start = now - TIMESTAMP_WINDOW
    window_end = now + TIMESTAMP_WINDOW
    user_agent = request.headers.get("User-Agent", "")[:1000]
    device_type, browser, os_name = _parse_ua(user_agent)
    session_meta = data.get("session_meta")

    try:
        with transaction.atomic():
            if isinstance(session_meta, dict):
                landing_url = _sanitize_url(
                    session_meta.get("landing_url"),
                    request,
                    same_origin=True,
                )
                if not landing_url:
                    return JsonResponse({"error": "Invalid landing_url"}, status=400)
                session, _created = TrackSession.objects.get_or_create(
                    session_id=session_id,
                    defaults={
                        "landing_url": landing_url,
                        "referrer": _sanitize_url(
                            session_meta.get("referrer"),
                            request,
                            same_origin=False,
                        ),
                        "utm_source": _safe_text(session_meta.get("utm_source"), 100),
                        "utm_medium": _safe_text(session_meta.get("utm_medium"), 100),
                        "utm_campaign": _safe_text(session_meta.get("utm_campaign"), 200),
                        "utm_content": _safe_text(session_meta.get("utm_content"), 200),
                        "utm_term": _safe_text(session_meta.get("utm_term"), 200),
                        "gclid": _safe_text(session_meta.get("gclid"), 200),
                        "device_type": device_type,
                        "browser": browser,
                        "os": os_name,
                        "screen_width": _safe_int(session_meta.get("screen_width")),
                        "language": _safe_text(session_meta.get("language"), 10),
                        "ip_hash": _privacy_ip_hash(request.META.get("REMOTE_ADDR", "")),
                    },
                )
            else:
                session = TrackSession.objects.filter(session_id=session_id).first()
                if session is None:
                    return HttpResponse(status=202)

            event_objects: list[TrackEvent] = []
            for event in events:
                if not isinstance(event, dict):
                    continue
                event_name = _safe_text(event.get("name"), 50)
                if event_name not in ALLOWED_EVENTS:
                    continue
                timestamp = event.get("ts")
                if not isinstance(timestamp, (int, float)) or isinstance(timestamp, bool):
                    continue
                try:
                    event_time = datetime.fromtimestamp(
                        timestamp / 1000,
                        tz=datetime_timezone.utc,
                    )
                except (OSError, OverflowError, ValueError):
                    continue
                if not window_start <= event_time <= window_end:
                    continue
                event_url = _sanitize_url(
                    event.get("url"),
                    request,
                    same_origin=True,
                )
                event_objects.append(
                    TrackEvent(
                        session=session,
                        event_name=event_name,
                        url=event_url,
                        properties=_sanitize_properties(
                            event_name,
                            event.get("properties"),
                        ),
                        created_at=event_time,
                    )
                )
            if event_objects:
                TrackEvent.objects.bulk_create(event_objects)
            TrackSession.objects.filter(pk=session.pk).update(updated_at=now)
    except DatabaseError:
        logger.warning("Tracking collection skipped because storage is unavailable")

    return HttpResponse(status=202)


def _valid_signature(request: HttpRequest, secret: str) -> bool:
    signature = request.headers.get("X-Tracking-Signature", "")
    if signature.startswith("sha256="):
        signature = signature[7:]
    if len(signature) != 64:
        return False
    expected = hmac.new(secret.encode(), request.body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected)


@csrf_exempt
@require_POST
@ratelimit(group="tracking-webhook", key="ip", rate=_webhook_rate, method="POST", block=True)
def booking_complete(request: HttpRequest) -> HttpResponse:
    """Apply an idempotent HMAC-authenticated booking conversion."""
    if not getattr(settings, "TRACKING_WEBHOOK_ENABLED", False):
        return JsonResponse({"error": "Not found"}, status=404)
    if request.content_type != "application/json":
        return JsonResponse({"error": "Unsupported content type"}, status=415)
    if len(request.body) > MAX_BODY_SIZE:
        return JsonResponse({"error": "Payload too large"}, status=413)
    secret = str(getattr(settings, "TRACKING_SECRET", ""))
    if not secret:
        return JsonResponse({"error": "Webhook unavailable"}, status=503)
    if not _valid_signature(request, secret):
        return JsonResponse({"error": "Invalid signature"}, status=403)
    data = _json_body(request)
    if data is None:
        return JsonResponse({"error": "Invalid JSON object"}, status=400)
    session_id = _valid_uuid4(data.get("session_id"))
    if session_id is None:
        return JsonResponse({"error": "Invalid session_id"}, status=400)

    try:
        with transaction.atomic():
            session = (
                TrackSession.objects.select_for_update()
                .filter(session_id=session_id)
                .first()
            )
            if session is None:
                return JsonResponse({"error": "Session not found"}, status=404)
            if session.is_converted:
                return HttpResponse(status=200)
            now = timezone.now()
            session.is_converted = True
            session.converted_at = now
            session.save(update_fields=["is_converted", "converted_at", "updated_at"])
            TrackEvent.objects.create(
                session=session,
                event_name="booking_completed",
                properties=_sanitize_properties(
                    "booking_completed",
                    {
                        "booking_id": data.get("booking_id"),
                        "service": data.get("service"),
                    },
                ),
                created_at=now,
            )
    except DatabaseError:
        logger.warning("Tracking webhook skipped because storage is unavailable")
        return JsonResponse({"error": "Temporarily unavailable"}, status=503)
    return HttpResponse(status=200)
