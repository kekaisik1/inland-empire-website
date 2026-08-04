"""Privacy-aware first-party tracking models."""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class TrackSession(models.Model):
    """A cookie-free browser session identified by a client UUID."""

    session_id = models.UUIDField(unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    landing_url = models.URLField(max_length=2000)
    referrer = models.URLField(max_length=2000, blank=True, default="")

    utm_source = models.CharField(max_length=100, blank=True, default="")
    utm_medium = models.CharField(max_length=100, blank=True, default="")
    utm_campaign = models.CharField(max_length=200, blank=True, default="")
    utm_content = models.CharField(max_length=200, blank=True, default="")
    utm_term = models.CharField(max_length=200, blank=True, default="")
    gclid = models.CharField(max_length=200, blank=True, default="")

    device_type = models.CharField(max_length=20, default="desktop")
    browser = models.CharField(max_length=100, blank=True, default="")
    os = models.CharField(max_length=100, blank=True, default="")
    screen_width = models.PositiveSmallIntegerField(null=True, blank=True)
    language = models.CharField(max_length=10, blank=True, default="")

    # The request address is subnet-reduced and keyed-hashed before persistence.
    ip_hash = models.CharField(max_length=64, blank=True, default="")

    is_converted = models.BooleanField(default=False)
    converted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"], name="track_session_created_idx"),
            models.Index(
                fields=["is_converted", "created_at"],
                name="track_session_conv_idx",
            ),
            models.Index(fields=["utm_source"], name="track_session_source_idx"),
        ]

    def clean(self) -> None:
        if self.is_converted and self.converted_at is None:
            raise ValidationError({"converted_at": "Converted sessions require a timestamp."})
        if not self.is_converted and self.converted_at is not None:
            raise ValidationError({"converted_at": "Unconverted sessions cannot have a timestamp."})

    def __str__(self) -> str:
        status = "converted" if self.is_converted else "active"
        return f"Session {str(self.session_id)[:8]}… ({status})"


class TrackEvent(models.Model):
    """A validated event in a first-party tracking session."""

    session = models.ForeignKey(
        TrackSession,
        on_delete=models.CASCADE,
        related_name="events",
    )
    event_name = models.CharField(max_length=50, db_index=True)
    url = models.URLField(max_length=2000, blank=True, default="")
    properties = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    server_created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(
                fields=["session", "created_at"],
                name="track_event_session_idx",
            ),
            models.Index(
                fields=["event_name", "created_at"],
                name="track_event_name_idx",
            ),
            models.Index(fields=["created_at"], name="track_event_created_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.event_name} @ {self.created_at:%H:%M:%S}"
