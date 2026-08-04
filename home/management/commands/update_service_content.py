"""
Management command to populate existing service pages with SEO-optimized content.

Fills in body, problems_we_fix, why_choose_us, faq, seo_title,
search_description, and related_services for all English service pages.

Run with: python manage.py update_service_content
"""

from __future__ import annotations

from typing import Any

from django.core.management.base import BaseCommand

from services.models import ServicePage, ServiceRelatedService, ServicesIndexPage

# Import the canonical content data from setup_pages
from home.management.commands.setup_pages import SERVICE_CONTENT
from home.service_seed_data import (
    apply_service_page_seed_data,
    repair_exact_verification_sentinels,
)


class Command(BaseCommand):
    help = "Populate missing service page SEO content without overwriting editor-customized fields"

    def handle(self, *args: object, **options: object) -> None:
        self.stdout.write("Updating service page content...\n")

        # Build a lookup by slug
        content_by_slug: dict[str, dict[str, Any]] = {
            s["slug"]: s for s in SERVICE_CONTENT
        }

        # Get all English service pages
        pages = ServicePage.objects.filter(
            locale__language_code="en",
            is_regional_service_page=False,
        ).select_related("locale")

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

            changed = apply_service_page_seed_data(page, data)
            changed = repair_exact_verification_sentinels(page, data) or changed

            if changed:
                page.save()
                page.save_revision().publish()
                updated += 1
                self.stdout.write(self.style.SUCCESS(f"  + {page.title}"))
            else:
                self.stdout.write(f"  OK {page.title} — no changes needed")
            page_by_slug[page.slug] = page

        services_index = (
            ServicesIndexPage.objects.filter(locale__language_code="en")
            .live()
            .first()
        )
        created_pages = 0
        if services_index is None:
            self.stdout.write(
                self.style.WARNING(
                    "Live English ServicesIndexPage not found; cannot create missing "
                    "ordinary service pages."
                )
            )
        else:
            for data in SERVICE_CONTENT:
                if data["slug"] in page_by_slug:
                    continue
                page = ServicePage(
                    title=data["title"],
                    slug=data["slug"],
                    intro=data["intro"],
                )
                apply_service_page_seed_data(page, data)
                services_index.add_child(instance=page)
                page.save_revision().publish()
                page_by_slug[page.slug] = page
                created_pages += 1
                self.stdout.write(self.style.SUCCESS(f"  + created {page.title}"))

        # Set up related service links
        related_created = 0
        for data in SERVICE_CONTENT:
            page = page_by_slug.get(data["slug"])
            if not page:
                continue

            for related_slug in data.get("related", []):
                related_page = page_by_slug.get(related_slug)
                if related_page:
                    _, created = ServiceRelatedService.objects.get_or_create(
                        page=page,
                        related_service=related_page,
                    )
                    if created:
                        related_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone! Updated {updated} service pages, "
                f"created {created_pages} missing service pages, "
                f"created {related_created} related service links."
            )
        )
