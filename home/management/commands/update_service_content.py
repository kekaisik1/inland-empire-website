"""
Management command to populate existing service pages with SEO-optimized content.

Fills in body, problems_we_fix, why_choose_us, faq, seo_title,
search_description, and related_services for all English service pages.

Run with: python manage.py update_service_content
"""

from __future__ import annotations

import json
from typing import Any

from django.core.management.base import BaseCommand

from services.models import ServicePage, ServiceRelatedService

# Import the canonical content data from setup_pages
from home.management.commands.setup_pages import SERVICE_CONTENT


class Command(BaseCommand):
    help = "Populate existing service pages with rich SEO content"

    def handle(self, *args: object, **options: object) -> None:
        self.stdout.write("Updating service page content...\n")

        # Build a lookup by slug
        content_by_slug: dict[str, dict[str, Any]] = {
            s["slug"]: s for s in SERVICE_CONTENT
        }

        # Get all English service pages
        pages = ServicePage.objects.filter(locale__language_code="en").select_related(
            "locale"
        )

        if not pages.exists():
            self.stdout.write(self.style.WARNING("No English service pages found."))
            return

        updated = 0
        page_by_slug: dict[str, ServicePage] = {}

        for page in pages:
            data = content_by_slug.get(page.slug)
            if not data:
                self.stdout.write(
                    self.style.WARNING(
                        f"  ? No content data for slug '{page.slug}' — skipping"
                    )
                )
                continue

            page.seo_title = data["seo_title"]
            page.search_description = data["search_description"]
            page.intro = data["intro"]
            page.short_description = data["short_description"]
            page.hero_usp = data["hero_usp"]
            page.body = data["body"]
            page.problems_we_fix = json.dumps(
                [{"type": "problem", "value": p} for p in data["problems"]]
            )
            page.why_choose_us = json.dumps(
                [
                    {"type": "benefit", "value": {"title": t, "description": d}}
                    for t, d in data["benefits"]
                ]
            )
            page.faq = json.dumps(
                [
                    {"type": "faq_item", "value": {"question": q, "answer": a}}
                    for q, a in data["faq"]
                ]
            )

            page.save()
            page.save_revision().publish()
            page_by_slug[page.slug] = page
            updated += 1
            self.stdout.write(self.style.SUCCESS(f"  + {page.title}"))

        # Set up related service links
        related_created = 0
        for data in SERVICE_CONTENT:
            page = page_by_slug.get(data["slug"])
            if not page:
                continue

            # Clear existing related services for this page
            ServiceRelatedService.objects.filter(page=page).delete()

            for related_slug in data.get("related", []):
                related_page = page_by_slug.get(related_slug)
                if related_page:
                    ServiceRelatedService.objects.create(
                        page=page, related_service=related_page
                    )
                    related_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone! Updated {updated} service pages, "
                f"created {related_created} related service links."
            )
        )
