"""Contact submission and validated VAPI ZIP handlers."""

from __future__ import annotations

import hmac
import json
import logging
import os
import re
from typing import Any

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django_ratelimit.decorators import ratelimit

from .forms import ContactForm

logger = logging.getLogger(__name__)

UTM_KEYS = [
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_content",
    "utm_term",
    "gclid",
    "gad_source",
    "gad_campaignid",
]

ZIP_CACHE_KEY = "inland:vapi:zip-to-city"
ZIP_CACHE_TTL = 300
VAPI_MAX_BODY_SIZE = 32_768
_ZIP_RE = re.compile(r"^\d{5}$")


def _clean_attribution(value: object, max_length: int = 200) -> str:
    """Remove control characters and cap untrusted attribution values."""
    if not isinstance(value, str):
        return ""
    return "".join(char for char in value if char >= " " and char != "\x7f").strip()[
        :max_length
    ]


def _vapi_rate(_group: str, _request: HttpRequest) -> str:
    return str(getattr(settings, "VAPI_RATE", "30/m"))


@ratelimit(key="ip", rate="5/m", method="POST", block=True)
def contact_submit(request: HttpRequest) -> HttpResponse:
    """Process contact form submission with UTM attribution."""
    # Derive locale-aware contact page URL from the current request path
    contact_url = request.path.rsplit("submit/", 1)[0] or "/contact/"
    if request.method != "POST":
        return redirect(contact_url)

    form = ContactForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        phone = form.cleaned_data.get("phone", "")
        message_text = form.cleaned_data["message"]

        # Capture UTM attribution from hidden form fields
        utm_data = {
            key: cleaned
            for key in UTM_KEYS
            if (cleaned := _clean_attribution(request.POST.get(key, "")))
        }

        subject = f"Contact form: {name}"
        body = (
            f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message_text}"
        )

        if utm_data:
            body += "\n\n--- Attribution ---"
            for key, value in utm_data.items():
                body += f"\n{key}: {value}"

        try:
            # Send notification to business
            business_email = (
                getattr(settings, "CONTACT_EMAIL", "")
                or os.environ.get("CONTACT_EMAIL", "")
            )

            if business_email:
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=None,  # uses DEFAULT_FROM_EMAIL
                    recipient_list=[business_email],
                    fail_silently=False,
                )
            else:
                raise RuntimeError("Contact delivery is not configured")

            from tracking.utils import track_server_event

            track_server_event(
                request,
                "contact_email_sent",
                {"utm_source": utm_data.get("utm_source", "")},
            )

            messages.success(request, _("Thank you! We'll get back to you shortly."))
        except Exception:
            logger.exception("Failed to send contact form email")
            messages.error(
                request,
                _("We could not send your message right now. Please try again shortly."),
            )
    else:
        messages.error(request, _("Please correct the errors below and try again."))

    return redirect(contact_url)


def _build_zip_to_city_map() -> dict[str, str]:
    cached: dict[str, str] | None = cache.get(ZIP_CACHE_KEY)
    if cached is not None:
        return cached

    from locations.models import CityPage

    zip_map: dict[str, str] = {}
    cities = CityPage.objects.live().public().only("title", "zip_codes")
    for city in cities.iterator(chunk_size=200):
        for value in (city.zip_codes or "").split(","):
            zip_code = value.strip()
            if _ZIP_RE.fullmatch(zip_code):
                zip_map.setdefault(zip_code, city.title[:255])
    cache.set(ZIP_CACHE_KEY, zip_map, ZIP_CACHE_TTL)
    return zip_map


def _vapi_authorized(request: HttpRequest) -> tuple[bool, int]:
    expected = str(getattr(settings, "VAPI_SERVER_SECRET", ""))
    if not expected:
        if getattr(settings, "VAPI_ALLOW_UNSIGNED", False):
            return True, 200
        return False, 503
    provided = request.headers.get("X-Vapi-Secret", "")
    return hmac.compare_digest(provided, expected), 401


def _parse_arguments(value: object) -> dict[str, Any] | None:
    if isinstance(value, str):
        if len(value) > 2048:
            return None
        try:
            value = json.loads(value)
        except (json.JSONDecodeError, ValueError):
            return None
    return value if isinstance(value, dict) else None


def _extract_vapi_tool_call(payload: dict[str, Any]) -> tuple[str, str] | None:
    message = payload.get("message")
    if not isinstance(message, dict):
        return None

    tool_calls = message.get("toolCallList") or message.get("toolCalls")
    if isinstance(tool_calls, list):
        if len(tool_calls) != 1 or not isinstance(tool_calls[0], dict):
            return None
        tool_call = tool_calls[0]
        function = tool_call.get("function")
        if not isinstance(function, dict) or function.get("name") != "check_zip_code":
            return None
        arguments = _parse_arguments(
            function.get("arguments", tool_call.get("arguments"))
        )
        if arguments is None:
            return None
        call_id = _clean_attribution(tool_call.get("id", ""), 100)
        return call_id or "unknown", _clean_attribution(arguments.get("zip_code"), 10)

    function_call = message.get("functionCall")
    if isinstance(function_call, dict):
        name = function_call.get("name", "check_zip_code")
        if name != "check_zip_code":
            return None
        arguments = _parse_arguments(
            function_call.get("parameters", function_call.get("arguments"))
        )
        if arguments is None:
            return None
        call_id = _clean_attribution(function_call.get("id", ""), 100)
        return call_id or "unknown", _clean_attribution(arguments.get("zip_code"), 10)
    return None


def _vapi_result(tool_call_id: str, result: str) -> JsonResponse:
    return JsonResponse(
        {"results": [{"toolCallId": tool_call_id, "result": result}]}
    )


@csrf_exempt
@require_POST
@ratelimit(group="vapi-zip", key="ip", rate=_vapi_rate, method="POST", block=True)
def vapi_check_zip(request: HttpRequest) -> JsonResponse:
    """Check one ZIP against live target CityPages without external effects."""
    if not getattr(settings, "VAPI_ENABLED", False):
        return JsonResponse({"error": "Not found"}, status=404)
    if request.content_type != "application/json":
        return JsonResponse({"error": "Unsupported content type"}, status=415)
    if len(request.body) > VAPI_MAX_BODY_SIZE:
        return JsonResponse({"error": "Payload too large"}, status=413)
    authorized, failure_status = _vapi_authorized(request)
    if not authorized:
        message = "Unauthorized" if failure_status == 401 else "Endpoint unavailable"
        return JsonResponse({"error": message}, status=failure_status)
    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    if not isinstance(payload, dict):
        return JsonResponse({"error": "Invalid JSON object"}, status=400)
    extracted = _extract_vapi_tool_call(payload)
    if extracted is None:
        return JsonResponse({"error": "Invalid tool call"}, status=400)
    tool_call_id, zip_code = extracted
    if not zip_code:
        return _vapi_result(tool_call_id, "Please ask the caller for a five-digit ZIP code.")
    if not _ZIP_RE.fullmatch(zip_code):
        return _vapi_result(tool_call_id, "The ZIP code must contain exactly five digits.")

    city = _build_zip_to_city_map().get(zip_code)
    if city:
        result = (
            f"ZIP code {zip_code} is listed in the service area for {city}, California. "
            "A scheduler can confirm current availability."
        )
    else:
        result = (
            f"ZIP code {zip_code} is not currently listed in the configured service area. "
            "A scheduler can confirm whether an exception is available."
        )
    return _vapi_result(tool_call_id, result)
