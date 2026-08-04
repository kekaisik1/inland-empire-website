"""Regression tests for Trello card #19 regional service pages."""

from __future__ import annotations

import hashlib
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase

from home.models import SiteSettings
from home.regional_service_seed_data import (
    REGIONAL_SERVICE_SPECS,
    SOURCE_PATH,
    regional_service_records,
    regional_source_sections,
)
from home.tests import create_test_home
from services.models import ServicePage, ServiceRelatedService, ServicesIndexPage


class RegionalServiceSourceTest(TestCase):
    def test_attached_source_builds_exactly_twenty_complete_unique_records(self) -> None:
        sections = regional_source_sections()
        records = regional_service_records()

        self.assertEqual(len(sections), 10)
        self.assertEqual(len(records), 20)
        self.assertEqual(len({record["slug"] for record in records}), 20)
        self.assertEqual(
            hashlib.sha256(SOURCE_PATH.read_bytes()).hexdigest(),
            "ff0190a77c39c0c3e5044f6b3f43cf978da543b4b0b8ad189a6d5bde752c536c",
        )
        self.assertTrue(all("[GEO]" not in record["body"] for record in records))
        self.assertTrue(all(record["body"].count("<h2>") >= 7 for record in records))
        freezer = next(
            record
            for record in records
            if record["slug"] == "freezer-repair-riverside-ca"
        )
        self.assertIn("<th>Freezer Type</th>", freezer["body"])
        self.assertIn("throughout Riverside, CA", freezer["body"])


class RegionalServicePagesCommandTest(TestCase):
    def setUp(self) -> None:
        cache.clear()
        self.home, self.site = create_test_home()
        SiteSettings.objects.create(
            site=self.site,
            business_name="Inland Empire Appliance Repair",
            phone="+155****4567",
            email="test@example.com",
        )
        self.services_index = ServicesIndexPage(title="Services", slug="services")
        self.home.add_child(instance=self.services_index)
        self.services_index.save_revision().publish()

        self.base_pages: dict[str, ServicePage] = {}
        for spec in REGIONAL_SERVICE_SPECS:
            page = ServicePage(
                title=spec["source_title"],
                slug=spec["base_slug"],
                intro=f"Professional {spec['source_title'].lower()}.",
                short_description=f"Same-day {spec['source_title'].lower()}.",
                problems_we_fix=[("problem", "Does not operate correctly")],
                why_choose_us=[
                    (
                        "benefit",
                        {
                            "title": "Local technicians",
                            "description": "Prompt local diagnostic service.",
                        },
                    )
                ],
                faq=[
                    (
                        "faq_item",
                        {
                            "question": "Do you offer same-day service?",
                            "answer": "Yes, when appointments are available.",
                        },
                    )
                ],
            )
            self.services_index.add_child(instance=page)
            page.save_revision().publish()
            self.base_pages[page.slug] = page

        ServiceRelatedService.objects.create(
            page=self.base_pages["freezer-repair"],
            related_service=self.base_pages["refrigerator-repair"],
            sort_order=0,
        )

    def test_command_creates_drafts_and_preserves_manual_publication_and_edits(
        self,
    ) -> None:
        first_output = StringIO()
        call_command("setup_regional_service_pages", stdout=first_output, verbosity=1)
        records = regional_service_records()
        regional_pages = ServicePage.objects.filter(is_regional_service_page=True)

        self.assertEqual(regional_pages.count(), 20)
        self.assertIn("20 drafts created", first_output.getvalue())
        self.assertEqual(
            set(regional_pages.values_list("slug", flat=True)),
            {record["slug"] for record in records},
        )

        for record in records:
            page = regional_pages.get(slug=record["slug"])
            self.assertFalse(page.live)
            self.assertTrue(page.has_unpublished_changes)
            self.assertEqual(page.revisions.count(), 1)
            self.assertEqual(page.title, record["title"])
            self.assertEqual(page.public_h1, record["title"])
            self.assertEqual(page.get_parent().specific.pk, self.services_index.pk)
            self.assertIn(record["area"], str(page.body))
            self.assertNotIn("[GEO]", str(page.body))

            response = self.client.get(f"/services/{record['slug']}/")
            self.assertEqual(response.status_code, 404)

        sitemap = self.client.get("/sitemap.xml").content.decode()
        for record in records:
            self.assertNotIn(
                f"http://testserver/services/{record['slug']}/",
                sitemap,
            )

        ac_page = regional_pages.get(slug="ac-repair-riverside-ca")
        admin_user = get_user_model().objects.create_superuser(
            username="regional-editor",
            email="regional-editor@example.com",
            password="test-password",
        )
        self.client.force_login(admin_user)
        edit_response = self.client.get(f"/admin/pages/{ac_page.pk}/edit/")
        self.assertEqual(edit_response.status_code, 200)
        self.assertContains(edit_response, ac_page.title)
        self.assertContains(edit_response, "Publish")
        self.client.logout()

        ac_page.get_latest_revision().publish()
        ac_page.refresh_from_db()
        self.assertTrue(ac_page.live)
        self.assertFalse(ac_page.has_unpublished_changes)

        ac_response = self.client.get(ac_page.url)
        self.assertEqual(ac_response.status_code, 200)
        self.assertEqual(
            ac_response.context["service_hero_slug"],
            "air-conditioning-repair-hvac",
        )
        self.assertIn(
            "service-hero-air-conditioning-repair-hvac",
            ac_response.context["static_service_hero_images"]["fallback"],
        )
        self.assertFalse(
            any(
                page.is_regional_service_page
                for page in ac_response.context["appliance_service_pages"]
            )
        )

        freezer_page = regional_pages.get(slug="freezer-repair-riverside-ca")
        self.assertEqual(freezer_page.related_services.count(), 1)
        self.assertEqual(
            freezer_page.related_services.first().related_service.slug,
            "refrigerator-repair",
        )

        services_response = self.client.get(self.services_index.url)
        self.assertFalse(
            any(
                page.is_regional_service_page
                for page in services_response.context["services"]
            )
        )
        home_response = self.client.get(self.home.url)
        self.assertFalse(
            any(
                page.is_regional_service_page
                for page in home_response.context["services"]
            )
        )
        self.assertFalse(
            any(
                page.is_regional_service_page
                for page in home_response.context["global_services"]
            )
        )

        sitemap = self.client.get("/sitemap.xml").content.decode()
        for record in records:
            regional_url = f"http://testserver/services/{record['slug']}/"
            if record["slug"] == ac_page.slug:
                self.assertIn(regional_url, sitemap)
            else:
                self.assertNotIn(regional_url, sitemap)

        ac_page.public_h1 = "Editor-approved Riverside AC Repair"
        ac_page.save_revision().publish()
        ac_page.refresh_from_db()

        revision_counts = {
            page.pk: page.revisions.count() for page in regional_pages
        }
        second_output = StringIO()
        call_command("setup_regional_service_pages", stdout=second_output, verbosity=1)

        self.assertEqual(
            ServicePage.objects.filter(is_regional_service_page=True).count(),
            20,
        )
        self.assertIn("20 existing preserved", second_output.getvalue())
        self.assertEqual(
            {
                page.pk: page.revisions.count()
                for page in ServicePage.objects.filter(is_regional_service_page=True)
            },
            revision_counts,
        )
        ac_page.refresh_from_db()
        self.assertTrue(ac_page.live)
        self.assertEqual(ac_page.public_h1, "Editor-approved Riverside AC Repair")
        self.assertEqual(
            ServicePage.objects.filter(
                is_regional_service_page=True,
                live=False,
            ).count(),
            19,
        )

        call_command("setup_spanish_pages", stdout=StringIO(), verbosity=0)
        self.assertFalse(
            ServicePage.objects.filter(
                is_regional_service_page=True,
                locale__language_code="es",
            ).exists()
        )


class CurrentLowlServiceCatalogParityTest(TestCase):
    """Keep the target's ordinary service catalog aligned with current LOWL logic."""

    expected_ordinary_slugs = {
        "refrigerator-repair",
        "freezer-repair",
        "washer-repair",
        "dryer-repair",
        "dishwasher-repair",
        "oven-repair",
        "stove-repair",
        "water-heater-repair",
        "air-conditioning-repair-hvac",
        "microwave-repair",
        "garbage-disposal-repair",
        "cooktop-repair",
        "ice-maker-repair",
    }

    def setUp(self) -> None:
        cache.clear()
        self.home, self.site = create_test_home()
        SiteSettings.objects.create(
            site=self.site,
            business_name="Inland Empire Appliance Repair",
            phone="+15555550199",
            email="test@example.com",
        )
        self.services_index = ServicesIndexPage(title="Services", slug="services")
        self.home.add_child(instance=self.services_index)
        self.services_index.save_revision().publish()
        first_page = ServicePage(
            title="Refrigerator Repair",
            slug="refrigerator-repair",
            intro="Professional refrigerator repair.",
        )
        self.services_index.add_child(instance=first_page)
        first_page.save_revision().publish()

    def test_update_command_creates_all_current_ordinary_services_with_spanish_pages(
        self,
    ) -> None:
        call_command("update_service_content", stdout=StringIO(), verbosity=0)

        ordinary_pages = ServicePage.objects.filter(
            locale__language_code="en",
            is_regional_service_page=False,
            slug__in=self.expected_ordinary_slugs,
        )
        self.assertEqual(
            set(ordinary_pages.values_list("slug", flat=True)),
            self.expected_ordinary_slugs,
        )

        for slug in (
            "garbage-disposal-repair",
            "cooktop-repair",
            "ice-maker-repair",
        ):
            page = ordinary_pages.get(slug=slug)
            self.assertTrue(page.live)
            self.assertIn("Inland Empire Appliance Repair", str(page.body))
            self.assertNotIn("LOWL Appliance Repair", str(page.body))
            response = self.client.get(page.url)
            self.assertEqual(response.status_code, 200)

        call_command("setup_spanish_pages", stdout=StringIO(), verbosity=0)
        spanish_pages = ServicePage.objects.filter(
            locale__language_code="es",
            slug__in={
                "garbage-disposal-repair",
                "cooktop-repair",
                "ice-maker-repair",
            },
        )
        self.assertEqual(spanish_pages.count(), 3)
        for page in spanish_pages:
            self.assertIn("Inland Empire Appliance Repair", str(page.body))
            self.assertNotIn("LOWL Appliance Repair", str(page.body))
