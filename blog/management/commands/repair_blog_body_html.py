"""Repair persisted blog StreamField HTML so Wagtail admin edit pages render."""

from __future__ import annotations

from typing import Any

from django.core.management.base import BaseCommand
from django.db import transaction

from blog.content_utils import normalized_stream_json
from blog.models import BlogPage


class Command(BaseCommand):
    help = "Normalize BlogPage StreamField rich-text HTML and publish repaired revisions."

    def handle(self, *args: Any, **options: Any) -> None:
        repaired = 0
        skipped = 0

        for page in BlogPage.objects.all().order_by("path"):
            normalized_body, changed = normalized_stream_json(page.body)
            if not changed or normalized_body is None:
                skipped += 1
                continue

            with transaction.atomic():
                page.body = normalized_body
                page.save()
                revision = page.save_revision()
                if page.live:
                    revision.publish()

            repaired += 1
            self.stdout.write(self.style.SUCCESS(f'  FIX   "{page.title}"'))

        self.stdout.write(
            self.style.SUCCESS(
                f"Done! Repaired {repaired} blog pages, skipped {skipped}."
            )
        )
