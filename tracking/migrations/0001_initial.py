# Generated for the Inland Empire target-native tracking schema.

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies: list[tuple[str, str]] = []

    operations = [
        migrations.CreateModel(
            name="TrackSession",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("session_id", models.UUIDField(db_index=True, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("landing_url", models.URLField(max_length=2000)),
                ("referrer", models.URLField(blank=True, default="", max_length=2000)),
                ("utm_source", models.CharField(blank=True, default="", max_length=100)),
                ("utm_medium", models.CharField(blank=True, default="", max_length=100)),
                ("utm_campaign", models.CharField(blank=True, default="", max_length=200)),
                ("utm_content", models.CharField(blank=True, default="", max_length=200)),
                ("utm_term", models.CharField(blank=True, default="", max_length=200)),
                ("gclid", models.CharField(blank=True, default="", max_length=200)),
                ("device_type", models.CharField(default="desktop", max_length=20)),
                ("browser", models.CharField(blank=True, default="", max_length=100)),
                ("os", models.CharField(blank=True, default="", max_length=100)),
                ("screen_width", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("language", models.CharField(blank=True, default="", max_length=10)),
                ("ip_hash", models.CharField(blank=True, default="", max_length=64)),
                ("is_converted", models.BooleanField(default=False)),
                ("converted_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "ordering": ["-created_at"],
                "indexes": [
                    models.Index(fields=["created_at"], name="track_session_created_idx"),
                    models.Index(
                        fields=["is_converted", "created_at"],
                        name="track_session_conv_idx",
                    ),
                    models.Index(fields=["utm_source"], name="track_session_source_idx"),
                ],
            },
        ),
        migrations.CreateModel(
            name="TrackEvent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("event_name", models.CharField(db_index=True, max_length=50)),
                ("url", models.URLField(blank=True, default="", max_length=2000)),
                ("properties", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("server_created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events",
                        to="tracking.tracksession",
                    ),
                ),
            ],
            options={
                "ordering": ["created_at"],
                "indexes": [
                    models.Index(
                        fields=["session", "created_at"],
                        name="track_event_session_idx",
                    ),
                    models.Index(
                        fields=["event_name", "created_at"],
                        name="track_event_name_idx",
                    ),
                    models.Index(fields=["created_at"], name="track_event_created_idx"),
                ],
            },
        ),
    ]
