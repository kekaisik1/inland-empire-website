"""Failure-isolated server-side tracking utility."""

from __future__ import annotations

import logging
from typing import Any

from django.conf import settings
from django.db import DatabaseError
from django.http import HttpRequest
from django.utils import timezone

from .models import TrackEvent, TrackSession
from .views import ALLOWED_EVENTS, _sanitize_properties, _sanitize_url, _valid_uuid4

logger = logging.getLogger(__name__)


def track_server_event(
    request: HttpRequest,
    event_name: str,
    properties: dict[str, Any] | None = None,
) -> None:
    """Record an allowlisted event without ever breaking the caller."""
    if not getattr(settings, "TRACKING_ENABLED", False):
        return
    if request.headers.get("DNT") == "1" or request.headers.get("Sec-GPC") == "1":
        return
    if event_name not in ALLOWED_EVENTS:
        return
    session_id = _valid_uuid4(
        request.POST.get("tracking_session_id")
        or request.GET.get("tracking_session_id")
    )
    if session_id is None:
        return
    try:
        session = TrackSession.objects.filter(session_id=session_id).first()
        if session is None:
            return
        TrackEvent.objects.create(
            session=session,
            event_name=event_name,
            url=_sanitize_url(
                request.build_absolute_uri(),
                request,
                same_origin=True,
            ),
            properties=_sanitize_properties(event_name, properties or {}),
            created_at=timezone.now(),
        )
    except DatabaseError:
        logger.warning("Server-side tracking skipped because storage is unavailable")
