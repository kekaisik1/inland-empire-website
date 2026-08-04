"""Permission-gated Wagtail views for aggregate tracking data."""

from __future__ import annotations

import csv
from datetime import timedelta
from typing import Any
from urllib.parse import urlsplit

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from django.db.models import Avg, Count, Q
from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from django.views.generic import DetailView, TemplateView
from wagtail.admin.views.generic import WagtailAdminTemplateMixin

from .models import TrackEvent, TrackSession

SESSIONS_PER_PAGE = 25


class TrackingPermissionMixin(PermissionRequiredMixin):
    permission_required = "tracking.view_tracksession"

    def handle_no_permission(self) -> HttpResponse:
        if self.request.user.is_authenticated:
            raise PermissionDenied
        return super().handle_no_permission()


class DashboardView(
    TrackingPermissionMixin,
    WagtailAdminTemplateMixin,
    TemplateView,
):
    template_name = "tracking/dashboard.html"
    page_title = "Tracking Dashboard"
    header_icon = "view"

    def get_days(self) -> int:
        try:
            days = int(self.request.GET.get("days", 30))
        except (TypeError, ValueError):
            days = 30
        return days if days in (7, 30, 90) else 30

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        days = self.get_days()
        start = timezone.now() - timedelta(days=days)
        sessions = TrackSession.objects.filter(created_at__gte=start)
        total_sessions = sessions.count()
        converted = sessions.filter(is_converted=True).count()
        top_source = (
            sessions.exclude(utm_source="")
            .values("utm_source")
            .annotate(count=Count("id"))
            .order_by("-count", "utm_source")
            .first()
        )
        average_events = (
            sessions.annotate(event_count=Count("events"))
            .aggregate(value=Avg("event_count"))
            .get("value")
            or 0
        )
        context["summary"] = {
            "total_sessions": total_sessions,
            "conversion_rate": _percentage(converted, total_sessions),
            "top_source": top_source["utm_source"] if top_source else "Direct",
            "avg_events": round(average_events, 1),
        }

        events = TrackEvent.objects.filter(session__in=sessions)
        engaged = (
            events.filter(event_name__in=("scroll_depth", "time_on_page", "page_view"))
            .values("session_id")
            .distinct()
            .count()
        )
        intent = (
            events.filter(
                event_name__in=("zip_check", "cta_impression", "booking_form_submit")
            )
            .values("session_id")
            .distinct()
            .count()
        )
        clicked = (
            events.filter(event_name="booking_click")
            .values("session_id")
            .distinct()
            .count()
        )
        context["funnel"] = [
            ("Landing", total_sessions, 100 if total_sessions else 0),
            ("Engagement", engaged, _percentage(engaged, total_sessions)),
            ("Booking Intent", intent, _percentage(intent, total_sessions)),
            ("Booking Click", clicked, _percentage(clicked, total_sessions)),
            ("Booking Complete", converted, _percentage(converted, total_sessions)),
        ]

        try:
            requested_page = max(1, int(self.request.GET.get("page", 1)))
        except (TypeError, ValueError):
            requested_page = 1
        total_pages = max(1, (total_sessions + SESSIONS_PER_PAGE - 1) // SESSIONS_PER_PAGE)
        page_number = min(requested_page, total_pages)
        offset = (page_number - 1) * SESSIONS_PER_PAGE
        context["sessions"] = sessions.annotate(event_count=Count("events")).order_by(
            "-created_at"
        )[offset : offset + SESSIONS_PER_PAGE]
        context["page_num"] = page_number
        context["total_pages"] = total_pages
        context["page_range"] = range(1, total_pages + 1)

        sources = list(
            sessions.values("utm_source")
            .annotate(
                total=Count("id"),
                conversions=Count("id", filter=Q(is_converted=True)),
            )
            .order_by("-total", "utm_source")[:10]
        )
        for source in sources:
            source["rate"] = _percentage(source["conversions"], source["total"])
            source["utm_source"] = source["utm_source"] or "Direct"
        context["sources"] = sources

        landing_pages = list(
            sessions.values("landing_url")
            .annotate(
                total=Count("id"),
                conversions=Count("id", filter=Q(is_converted=True)),
            )
            .order_by("-total", "landing_url")[:10]
        )
        for landing in landing_pages:
            landing["rate"] = _percentage(landing["conversions"], landing["total"])
            landing["path"] = _url_path(landing["landing_url"])
        context["landing_pages"] = landing_pages
        context["days"] = days
        context["day_options"] = (7, 30, 90)
        return context


class SessionDetailView(
    TrackingPermissionMixin,
    WagtailAdminTemplateMixin,
    DetailView,
):
    template_name = "tracking/session_detail.html"
    model = TrackSession
    context_object_name = "session"
    page_title = "Session Detail"
    header_icon = "view"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["events"] = self.object.events.order_by("created_at")
        return context


def _csv_safe(value: object) -> str:
    text = str(value or "")
    return f"'{text}" if text.startswith(("=", "+", "-", "@")) else text


@permission_required("tracking.view_tracksession", raise_exception=True)
def export_csv(request: HttpRequest) -> HttpResponse:
    try:
        days = int(request.GET.get("days", 30))
    except (TypeError, ValueError):
        days = 30
    if days not in (7, 30, 90):
        days = 30
    start = timezone.now() - timedelta(days=days)
    sessions = (
        TrackSession.objects.filter(created_at__gte=start)
        .annotate(event_count=Count("events"))
        .order_by("-created_at")
    )
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="tracking-{days}d.csv"'
    writer = csv.writer(response)
    writer.writerow(
        (
            "Session",
            "Created",
            "Landing URL",
            "Source",
            "Medium",
            "Campaign",
            "Device",
            "Browser",
            "Events",
            "Converted",
        )
    )
    for session in sessions:
        writer.writerow(
            (
                str(session.session_id)[:8],
                session.created_at.isoformat(),
                _csv_safe(session.landing_url),
                _csv_safe(session.utm_source or "Direct"),
                _csv_safe(session.utm_medium),
                _csv_safe(session.utm_campaign),
                _csv_safe(session.device_type),
                _csv_safe(session.browser),
                session.event_count,
                "Yes" if session.is_converted else "No",
            )
        )
    return response


def _percentage(part: int, whole: int) -> float:
    return round(part / whole * 100, 1) if whole else 0


def _url_path(url: str) -> str:
    try:
        return urlsplit(url).path or "/"
    except ValueError:
        return "/"
