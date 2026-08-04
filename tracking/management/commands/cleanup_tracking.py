"""Delete first-party tracking data according to configured retention."""

from __future__ import annotations

from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from tracking.models import TrackSession


class Command(BaseCommand):
    help = "Delete tracking sessions older than the configured retention windows."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report matching rows without deleting them.",
        )
        parser.add_argument("--unconverted-days", type=int)
        parser.add_argument("--converted-days", type=int)

    def handle(self, *args: object, **options: object) -> None:
        unconverted_days = options.get("unconverted_days") or getattr(
            settings,
            "TRACKING_RETENTION_DAYS",
            90,
        )
        converted_days = options.get("converted_days") or getattr(
            settings,
            "TRACKING_CONVERTED_RETENTION_DAYS",
            180,
        )
        if unconverted_days < 1 or converted_days < 1:
            raise CommandError("Retention days must be positive integers.")

        now = timezone.now()
        unconverted_cutoff = now - timedelta(days=unconverted_days)
        converted_cutoff = now - timedelta(days=converted_days)
        candidates = TrackSession.objects.filter(
            Q(is_converted=False, created_at__lt=unconverted_cutoff)
            | Q(
                is_converted=True,
                converted_at__lt=converted_cutoff,
            )
            | Q(
                is_converted=True,
                converted_at__isnull=True,
                created_at__lt=converted_cutoff,
            )
        )
        count = candidates.count()
        if options.get("dry_run"):
            self.stdout.write(
                f"Dry run: would delete {count} tracking sessions and their events."
            )
            return
        with transaction.atomic():
            candidates.delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {count} tracking sessions."))
