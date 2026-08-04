"""Create the 20 source-approved regional service landing pages as drafts."""

from __future__ import annotations

import copy

from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError

from home.regional_service_seed_data import regional_service_records
from services.models import ServicePage, ServiceRelatedService, ServicesIndexPage


class Command(BaseCommand):
    help = (
        "Create missing regional service pages for Lake Elsinore and Riverside "
        "as Wagtail drafts"
    )

    def handle(self, *args: object, **options: object) -> None:
        services_index = (
            ServicesIndexPage.objects.filter(locale__language_code="en").live().first()
        )
        if services_index is None:
            raise CommandError("A live English ServicesIndexPage is required")

        records = regional_service_records()
        required_base_slugs = {record["base_slug"] for record in records}
        base_pages = {
            page.slug: page
            for page in ServicePage.objects.filter(
                locale__language_code="en",
                is_regional_service_page=False,
                slug__in=required_base_slugs,
            )
        }
        missing = sorted(required_base_slugs - set(base_pages))
        if missing:
            raise CommandError(
                "Ordinary service pages must exist before regional pages: "
                + ", ".join(missing)
            )

        created = 0
        preserved = 0
        for record in records:
            base_page = base_pages[record["base_slug"]]
            page = ServicePage.objects.filter(
                locale__language_code="en", slug=record["slug"]
            ).first()
            if page is not None:
                if not page.is_regional_service_page:
                    raise CommandError(
                        f"Existing page with slug {record['slug']!r} is not marked "
                        "as a regional service page"
                    )
                # Once seeded, Wagtail owns the page. Preserve editorial changes and
                # publication state instead of restoring source content or publishing
                # a page that an editor intentionally left as a draft.
                preserved += 1
                continue

            page = ServicePage(
                title=record["title"],
                slug=record["slug"],
                live=False,
                has_unpublished_changes=True,
            )

            desired_values = {
                "title": record["title"],
                "slug": record["slug"],
                "public_h1": record["title"],
                "seo_title": (
                    f"{record['title']} | Inland Empire Appliance Repair"
                ),
                "search_description": (
                    f"Professional {record['title'].lower()}. Same-day diagnostics, "
                    "upfront pricing, and warranty-backed repairs from Inland Empire "
                    "Appliance Repair."
                )[:160],
                "intro": record["intro"],
                "short_description": (
                    f"Professional {base_page.title.lower()} throughout "
                    f"{record['area']}."
                )[:150],
                "hero_usp": (
                    f"Same-day {base_page.title.lower()} in {record['area']} with "
                    "upfront pricing and warranty-backed work."
                ),
                "body": record["body"],
                "featured_image_id": base_page.featured_image_id,
                "problems_we_fix": copy.deepcopy(
                    list(base_page.problems_we_fix.raw_data)
                ),
                "why_choose_us": copy.deepcopy(
                    list(base_page.why_choose_us.raw_data)
                ),
                "faq": copy.deepcopy(list(base_page.faq.raw_data)),
                "is_regional_service_page": True,
            }
            for field_name, value in desired_values.items():
                setattr(page, field_name, value)

            services_index.add_child(instance=page)
            page.save_revision()
            created += 1

            for relation in base_page.related_services.select_related(
                "related_service"
            ):
                ServiceRelatedService.objects.create(
                    page=page,
                    related_service=relation.related_service,
                    sort_order=relation.sort_order,
                )

        cache.delete("inland:nav:services:en")
        cache.delete("inland:nav:services:es")
        self.stdout.write(
            self.style.SUCCESS(
                f"Regional service pages ready: {created} drafts created, "
                f"{preserved} existing preserved, {len(records)} total."
            )
        )
