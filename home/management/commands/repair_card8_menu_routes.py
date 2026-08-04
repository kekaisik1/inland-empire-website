"""Repair local data required for Inland Empire Appliance Repair Trello card #8 rendered menu QA."""

from __future__ import annotations

from typing import Any

from django.core.management.base import BaseCommand, CommandError
from wagtail.models import Site

from blog.models import BlogIndexPage
from home.management.commands.create_brand_pages import SUPPLEMENTAL_SERVICE_PAGES
from home.management.commands.setup_pages import SERVICE_CONTENT
from home.models import HomePage, SiteSettings
from home.service_seed_data import apply_service_page_seed_data
from locations.models import CityPage, LocationsIndexPage
from mysite.context_processors import (
    LEGACY_MAIN_NAV_DEFAULT_ORDER,
    MAIN_NAV_DEFAULT_ORDER,
    SHEET_BRAND_MENU_ROWS,
    SHEET_SERVICE_AREA_MENU_ROWS,
    SHEET_SERVICE_MENU_ROWS,
)
from pages.models import StaticPage
from services.models import ServicePage, ServicesIndexPage


STATIC_PAGE_SEEDS: tuple[dict[str, str], ...] = (
    {
        "title": "About Us",
        "slug": "about-us",
        "seo_title": "About Us — Certified Appliance Repair Technicians",
        "search_description": (
            "Learn about Inland Empire Appliance Repair's certified technicians, same-day "
            "service, and warranty-backed local appliance repairs."
        ),
        "hero_title": "About Us",
        "hero_subtitle": "Your trusted appliance repair experts.",
        "body": (
            "<p>Inland Empire Appliance Repair provides residential and commercial appliance "
            "repair with honest diagnostics, stocked service vehicles, and "
            "warranty-backed repairs across the Inland Empire.</p>"
        ),
    },
    {
        "title": "Contact",
        "slug": "contact",
        "seo_title": "Contact Us — Book Appliance Repair Today",
        "search_description": (
            "Contact Inland Empire Appliance Repair for same-day local appliance repair. "
            "Call, email, or book service online."
        ),
        "hero_title": "Contact Us",
        "hero_subtitle": "We're here to help with appliance repair questions and bookings.",
        "body": "<p>Have questions? Call us or book your appliance repair visit online.</p>",
    },
)


def _slug_from_path(path: str) -> str:
    return path.rstrip("/").rsplit("/", 1)[-1]


REQUIRED_SERVICE_SLUGS = {
    _slug_from_path(path)
    for _row, _label, path in (*SHEET_SERVICE_MENU_ROWS, *SHEET_BRAND_MENU_ROWS)
    if path
}
REQUIRED_CITY_ROWS = tuple(SHEET_SERVICE_AREA_MENU_ROWS)
SERVICE_SEEDS_BY_SLUG: dict[str, dict[str, Any]] = {
    seed["slug"]: seed
    for seed in (*SERVICE_CONTENT, *SUPPLEMENTAL_SERVICE_PAGES)
    if seed.get("slug") in REQUIRED_SERVICE_SLUGS
}


class Command(BaseCommand):
    help = "Repair legacy SiteSettings and missing local card #8 menu routes."

    def handle(self, *args: object, **options: object) -> None:
        site = Site.objects.filter(is_default_site=True).select_related("root_page").first()
        if site is None:
            raise CommandError("No default Wagtail Site found; run setup_pages first.")

        home_page = site.root_page.specific
        if not isinstance(home_page, HomePage):
            home_page = HomePage.objects.live().first()
        if home_page is None:
            raise CommandError("No HomePage found; run setup_pages first.")

        settings_count = SiteSettings.objects.filter(
            main_nav_order=LEGACY_MAIN_NAV_DEFAULT_ORDER
        ).update(main_nav_order=MAIN_NAV_DEFAULT_ORDER)

        services_index, services_index_created = self._ensure_services_index(home_page)
        service_created = self._ensure_service_pages(services_index)

        locations_index, locations_index_created = self._ensure_locations_index(home_page)
        city_created = self._ensure_city_pages(locations_index)

        blog_created = self._ensure_blog_index(home_page)
        static_created = self._ensure_static_pages(home_page)

        self.stdout.write(
            self.style.SUCCESS(
                "Card #8 repair complete: "
                f"settings_rows={settings_count}, "
                f"services_index_created={int(services_index_created)}, "
                f"service_pages_created={service_created}, "
                f"locations_index_created={int(locations_index_created)}, "
                f"city_pages_created={city_created}, "
                f"blog_index_created={int(blog_created)}, "
                f"static_pages_created={static_created}."
            )
        )

    def _ensure_services_index(self, home_page: HomePage) -> tuple[ServicesIndexPage, bool]:
        index = ServicesIndexPage.objects.child_of(home_page).filter(slug="services").first()
        if index is not None:
            return index, False

        index = ServicesIndexPage(
            title="Services",
            slug="services",
            hero_title="Appliance Repair Services",
            hero_subtitle="Expert repair for all major appliances. Fast, reliable, and affordable.",
        )
        home_page.add_child(instance=index)
        index.save_revision().publish()
        return index, True

    def _ensure_service_pages(self, services_index: ServicesIndexPage) -> int:
        created = 0
        for slug in sorted(REQUIRED_SERVICE_SLUGS):
            if ServicePage.objects.child_of(services_index).filter(slug=slug).exists():
                continue
            seed = SERVICE_SEEDS_BY_SLUG.get(slug)
            if seed is None:
                raise CommandError(f"No card #8 service seed data for {slug!r}")
            page = ServicePage(title=seed["title"], slug=slug, intro=seed["intro"])
            apply_service_page_seed_data(page, seed)
            services_index.add_child(instance=page)
            page.save_revision().publish()
            created += 1
        return created

    def _ensure_locations_index(self, home_page: HomePage) -> tuple[LocationsIndexPage, bool]:
        index = LocationsIndexPage.objects.child_of(home_page).filter(slug="service-areas").first()
        if index is not None:
            return index, False

        index = LocationsIndexPage(
            title="Service Areas",
            slug="service-areas",
            intro="<p>We proudly serve Southern California with fast, reliable appliance repair.</p>",
        )
        home_page.add_child(instance=index)
        index.save_revision().publish()
        return index, True

    def _ensure_city_pages(self, locations_index: LocationsIndexPage) -> int:
        created = 0
        for _row, label, path in REQUIRED_CITY_ROWS:
            slug = _slug_from_path(path)
            if CityPage.objects.child_of(locations_index).filter(slug=slug).exists():
                continue
            title = label.removeprefix("Appliance Repair in ").removesuffix(", CA")
            page = CityPage(
                title=title,
                slug=slug,
                intro=f"Same-day appliance repair in {title}, CA.",
                hero_usp=f"Fast, professional appliance repair in {title}.",
                state="CA",
            )
            locations_index.add_child(instance=page)
            page.save_revision().publish()
            created += 1
        return created

    def _ensure_blog_index(self, home_page: HomePage) -> bool:
        if BlogIndexPage.objects.child_of(home_page).filter(slug="blog").exists():
            return False
        page = BlogIndexPage(
            title="Blog",
            slug="blog",
            hero_title="Our Blog",
            hero_subtitle="Tips, guides, and insights about appliance care and repair.",
        )
        home_page.add_child(instance=page)
        page.save_revision().publish()
        return True

    def _ensure_static_pages(self, home_page: HomePage) -> int:
        created = 0
        for seed in STATIC_PAGE_SEEDS:
            if StaticPage.objects.child_of(home_page).filter(slug=seed["slug"]).exists():
                continue
            page = StaticPage(**seed)
            home_page.add_child(instance=page)
            page.save_revision().publish()
            created += 1
        return created
