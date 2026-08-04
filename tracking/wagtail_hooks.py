"""Wagtail hooks for the permission-gated tracking dashboard."""

from django.conf import settings
from django.urls import path, reverse
from wagtail import hooks
from wagtail.admin.menu import MenuItem

from . import admin_views


class TrackingMenuItem(MenuItem):
    def is_shown(self, request) -> bool:
        return bool(
            getattr(settings, "TRACKING_ADMIN_ENABLED", True)
            and request.user.has_perm("tracking.view_tracksession")
        )


@hooks.register("register_admin_urls")
def register_tracking_urls() -> list:
    return [
        path(
            "tracking/",
            admin_views.DashboardView.as_view(),
            name="tracking_dashboard",
        ),
        path(
            "tracking/session/<int:pk>/",
            admin_views.SessionDetailView.as_view(),
            name="tracking_session_detail",
        ),
        path(
            "tracking/export/",
            admin_views.export_csv,
            name="tracking_export_csv",
        ),
    ]


@hooks.register("register_admin_menu_item")
def register_tracking_menu() -> MenuItem:
    return TrackingMenuItem(
        "Tracking",
        reverse("tracking_dashboard"),
        icon_name="view",
        order=900,
    )
