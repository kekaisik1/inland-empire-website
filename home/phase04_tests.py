"""Phase 04 CMS content, localization, review provenance, and asset contracts."""

from __future__ import annotations

import json
from io import StringIO

from django.contrib.staticfiles.finders import find
from django.core.management import call_command
from django.test import TestCase
from wagtail.models import Locale

from home.tests import create_test_home
from locations.models import CityPage, LocationsIndexPage
from services.models import ServicePage, ServiceRelatedService, ServicesIndexPage


class Phase04DataHelperContractTest(TestCase):
    """Source-derived Phase 04 helpers must be target-safe and asset-backed."""

    def test_brand_asset_map_includes_monogram_and_wolf_with_generated_provenance(self) -> None:
        from home.brand_assets import get_brand_cards

        cards = get_brand_cards()
        by_slug = {card["slug"]: card for card in cards}

        self.assertIn("monogram-appliance-repair", by_slug)
        self.assertIn("wolf-appliance-repair", by_slug)
        for slug in ("monogram-appliance-repair", "wolf-appliance-repair"):
            card = by_slug[slug]
            self.assertIn("generated", str(card["logo_source"]).lower())
            self.assertTrue(str(card["logo_static"]).endswith(".svg"))
            self.assertIsNotNone(find(str(card["logo_static"])))

    def test_review_manifest_withholds_source_reviews_from_target_public_claims(self) -> None:
        from home.reviews import get_customer_review_items, get_withheld_review_items

        self.assertEqual(get_customer_review_items(), [])
        withheld = get_withheld_review_items()
        self.assertGreaterEqual(len(withheld), 3)
        sample = withheld[0]
        self.assertEqual(sample["rating"], 5)
        self.assertIn(sample["source"], {"Google", "Yelp"})
        self.assertTrue(sample["source_url"].startswith("https://"))
        self.assertIn("LOWL", sample["withheld_reason"])
        self.assertIn("Inland Empire", sample["withheld_reason"])

    def test_homepage_context_does_not_republish_withheld_source_reviews(self) -> None:
        home, _site = create_test_home()

        context = home.get_context(None)

        self.assertEqual(context["review_items"], [])

    def test_homepage_template_does_not_render_withheld_source_reviews(self) -> None:
        home, _site = create_test_home()

        response = self.client.get(home.url)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Maria G.")
        self.assertNotContains(response, "Called in the morning")

    def test_city_static_asset_map_resolves_corona_responsive_variants(self) -> None:
        from locations.city_assets import get_static_city_hero_images

        images = get_static_city_hero_images("appliance-repair-corona-ca")
        self.assertIsNotNone(images)
        assert images is not None
        for key in ("fallback", "webp_480", "webp_768", "webp_1200", "og"):
            self.assertIsNotNone(find(images[key]), key)

    def test_blog_content_utils_normalize_draftail_unsafe_br_tags(self) -> None:
        from blog.content_utils import normalize_rich_text_html, stream_body

        self.assertEqual(normalize_rich_text_html("<p>A<br>B</p>"), "<p>A<br />B</p>")
        self.assertIn("<br />", stream_body([("paragraph", "Line<br>Break")]))

    def test_service_seed_data_is_target_safe_and_has_content_hubs(self) -> None:
        from home.service_seed_data import SEO_LANDING_SERVICE_SLUGS

        self.assertIn("commercial-appliance-repair", SEO_LANDING_SERVICE_SLUGS)
        self.assertIn("high-end-appliance-repair", SEO_LANDING_SERVICE_SLUGS)
        self.assertIn("monogram-appliance-repair", SEO_LANDING_SERVICE_SLUGS)
        self.assertIn("wolf-appliance-repair", SEO_LANDING_SERVICE_SLUGS)
        serialized = repr(SEO_LANDING_SERVICE_SLUGS).lower()
        self.assertNotIn("lowl appliance repair", serialized)
        self.assertNotIn("951) 620-9609", serialized)
        self.assertNotIn("409 n langstaff", serialized)


class Phase04ManagementCommandContractTest(TestCase):
    """Focused dry-run/idempotency contracts for Phase 04 command behavior."""

    def setUp(self) -> None:
        self.home, self.site = create_test_home()
        self.services_index = ServicesIndexPage(title="Services", slug="services")
        self.home.add_child(instance=self.services_index)
        self.services_index.save_revision().publish()

    def _add_seeded_service(self, slug: str) -> ServicePage:
        from home.management.commands.setup_pages import SERVICE_CONTENT
        from home.service_seed_data import apply_service_page_seed_data

        data = next(item for item in SERVICE_CONTENT if item["slug"] == slug)
        page = ServicePage(title=data["title"], slug=slug)
        self.assertTrue(apply_service_page_seed_data(page, data))
        self.services_index.add_child(instance=page)
        page.save_revision().publish()
        return page

    def test_add_brand_faqs_dry_run_previews_without_mutating_pages(self) -> None:
        page = ServicePage(
            title="Samsung Appliance Repair",
            slug="samsung-appliance-repair",
            intro="Samsung repair.",
        )
        self.services_index.add_child(instance=page)
        page.save_revision().publish()

        out = StringIO()
        call_command("add_brand_faqs", "--dry-run", stdout=out)

        page.refresh_from_db()
        self.assertIn("DRY RUN", out.getvalue())
        self.assertEqual(len(page.faq), 0)

    def test_add_brand_faqs_apply_then_rerun_preserves_existing_editor_faq(self) -> None:
        page = ServicePage(
            title="Samsung Appliance Repair",
            slug="samsung-appliance-repair",
            intro="Samsung repair.",
        )
        self.services_index.add_child(instance=page)
        page.save_revision().publish()

        call_command("add_brand_faqs", stdout=StringIO(), stderr=StringIO())
        page.refresh_from_db()
        first_count = len(page.faq)
        self.assertGreater(first_count, 0)

        out = StringIO()
        call_command("add_brand_faqs", stdout=out, stderr=StringIO())
        page.refresh_from_db()
        self.assertEqual(len(page.faq), first_count)
        self.assertIn("already has", out.getvalue())

    def test_setup_spanish_pages_creates_locale_and_second_run_skips_existing_translations(self) -> None:
        service = ServicePage(
            title="Refrigerator Repair",
            slug="refrigerator-repair",
            intro="Fix your refrigerator.",
        )
        self.services_index.add_child(instance=service)
        service.save_revision().publish()

        first_out = StringIO()
        call_command("setup_spanish_pages", stdout=first_out, stderr=StringIO())
        self.assertTrue(Locale.objects.filter(language_code="es").exists())
        es_count = ServicePage.objects.filter(locale__language_code="es").count()
        self.assertGreaterEqual(es_count, 1)

        second_out = StringIO()
        call_command("setup_spanish_pages", stdout=second_out, stderr=StringIO())
        self.assertEqual(ServicePage.objects.filter(locale__language_code="es").count(), es_count)
        self.assertIn("SKIP", second_out.getvalue())

    def test_populate_city_seo_preserves_english_and_spanish_editor_content(self) -> None:
        from locations.management.commands.populate_city_seo import CITY_DATA

        locations_index = LocationsIndexPage(
            title="Service Areas",
            slug="service-areas",
            intro="Service areas.",
        )
        self.home.add_child(instance=locations_index)
        locations_index.save_revision().publish()
        seed = CITY_DATA["Corona"]
        english = CityPage(
            title="Corona",
            slug="appliance-repair-corona-ca",
            intro=seed["intro"],
            hero_usp=seed["hero_usp"],
            body=seed["body"],
            about_techs=seed["about_techs"],
            zip_codes=seed["zip_codes"],
            seo_title=seed["seo_title"],
            search_description=seed["search_description"],
        )
        locations_index.add_child(instance=english)
        english.save_revision().publish()
        call_command("setup_spanish_pages", stdout=StringIO(), stderr=StringIO())
        spanish = CityPage.objects.get(
            translation_key=english.translation_key,
            locale__language_code="es",
        )

        custom = {
            "intro": "EDITOR CUSTOM CITY INTRO",
            "hero_usp": "EDITOR CUSTOM CITY USP",
            "body": "<p>EDITOR CUSTOM CITY BODY</p>",
            "about_techs": "<p>EDITOR CUSTOM CITY TECHS</p>",
            "zip_codes": "90001, 90002",
            "seo_title": "EDITOR CUSTOM CITY SEO",
            "search_description": "EDITOR CUSTOM CITY DESCRIPTION",
        }
        for page, prefix in ((english, "EN"), (spanish, "ES")):
            for field, value in custom.items():
                setattr(page, field, f"{prefix} {value}")
            page.save()
        revisions_before = {
            "en": english.revisions.count(),
            "es": spanish.revisions.count(),
        }

        call_command(
            "populate_city_seo",
            "--apply",
            "--city=Corona",
            stdout=StringIO(),
            stderr=StringIO(),
        )

        english.refresh_from_db()
        spanish.refresh_from_db()
        for page, prefix in ((english, "EN"), (spanish, "ES")):
            for field, value in custom.items():
                self.assertEqual(str(getattr(page, field)), f"{prefix} {value}")
        self.assertEqual(english.revisions.count(), revisions_before["en"])
        self.assertEqual(spanish.revisions.count(), revisions_before["es"])

    def test_populate_city_seo_backfills_missing_fields_once(self) -> None:
        from locations.management.commands.populate_city_seo import CITY_DATA

        locations_index = LocationsIndexPage(
            title="Service Areas",
            slug="service-areas",
            intro="Service areas.",
        )
        self.home.add_child(instance=locations_index)
        locations_index.save_revision().publish()
        city = CityPage(
            title="Riverside",
            slug="appliance-repair-riverside-ca",
            intro="temporary value cleared after tree insertion",
        )
        locations_index.add_child(instance=city)
        city.save_revision().publish()
        CityPage.objects.filter(pk=city.pk).update(intro="")
        city.refresh_from_db()
        revisions_before = city.revisions.count()

        call_command(
            "populate_city_seo",
            "--apply",
            "--city=Riverside",
            stdout=StringIO(),
            stderr=StringIO(),
        )
        city.refresh_from_db()
        seed = CITY_DATA["Riverside"]
        for field in (
            "intro",
            "hero_usp",
            "body",
            "about_techs",
            "zip_codes",
            "seo_title",
            "search_description",
        ):
            self.assertEqual(str(getattr(city, field)), seed[field])
        self.assertEqual(city.revisions.count(), revisions_before + 1)

        call_command(
            "populate_city_seo",
            "--apply",
            "--city=Riverside",
            stdout=StringIO(),
            stderr=StringIO(),
        )
        self.assertEqual(city.revisions.count(), revisions_before + 1)

    def test_setup_spanish_pages_creates_full_spanish_service_content(self) -> None:
        from home.management.commands.populate_spanish_content import (
            SERVICE_CONTENT as SPANISH_SERVICE_CONTENT,
        )

        english = self._add_seeded_service("refrigerator-repair")

        call_command("setup_spanish_pages", stdout=StringIO(), stderr=StringIO())

        spanish = ServicePage.objects.get(
            translation_key=english.translation_key,
            locale__language_code="es",
        )
        expected = SPANISH_SERVICE_CONTENT["refrigerator-repair"]
        self.assertEqual(str(spanish.body), expected["body"])
        self.assertEqual(
            [item["value"] for item in spanish.problems_we_fix.raw_data],
            expected["problems"],
        )
        self.assertEqual(
            [item["value"] for item in spanish.why_choose_us.raw_data],
            expected["benefits"],
        )
        self.assertEqual(
            [item["value"] for item in spanish.faq.raw_data],
            expected["faqs"],
        )
        self.assertNotEqual(str(spanish.body), str(english.body))
        revisions_before = spanish.revisions.count()
        call_command("setup_spanish_pages", stdout=StringIO(), stderr=StringIO())
        self.assertEqual(spanish.revisions.count(), revisions_before)

    def test_populate_spanish_content_repairs_only_missing_or_copied_english_fields(self) -> None:
        from home.management.commands.populate_spanish_content import (
            SERVICE_CONTENT as SPANISH_SERVICE_CONTENT,
        )

        english = self._add_seeded_service("freezer-repair")
        call_command("setup_spanish_pages", stdout=StringIO(), stderr=StringIO())
        spanish = ServicePage.objects.get(
            translation_key=english.translation_key,
            locale__language_code="es",
        )
        custom_benefits = json.dumps(
            [
                {
                    "type": "benefit",
                    "value": {
                        "title": "BENEFICIO EDITORIAL",
                        "description": "Contenido personalizado en español.",
                    },
                }
            ]
        )
        spanish.body = english.body
        spanish.problems_we_fix = json.dumps(list(english.problems_we_fix.raw_data))
        spanish.why_choose_us = custom_benefits
        spanish.faq = "[]"
        spanish.save()
        revisions_before = spanish.revisions.count()

        call_command("populate_spanish_content", stdout=StringIO(), stderr=StringIO())

        spanish.refresh_from_db()
        expected = SPANISH_SERVICE_CONTENT["freezer-repair"]
        self.assertEqual(str(spanish.body), expected["body"])
        self.assertEqual(
            [item["value"] for item in spanish.problems_we_fix.raw_data],
            expected["problems"],
        )
        self.assertEqual(
            spanish.why_choose_us.raw_data[0]["value"]["title"],
            "BENEFICIO EDITORIAL",
        )
        self.assertEqual(
            [item["value"] for item in spanish.faq.raw_data],
            expected["faqs"],
        )
        self.assertEqual(spanish.revisions.count(), revisions_before + 1)

        call_command("populate_spanish_content", stdout=StringIO(), stderr=StringIO())
        self.assertEqual(spanish.revisions.count(), revisions_before + 1)

    def test_setup_spanish_pages_repairs_stale_english_related_services(self) -> None:
        english_refrigerator = self._add_seeded_service("refrigerator-repair")
        english_freezer = self._add_seeded_service("freezer-repair")
        ServiceRelatedService.objects.create(
            page=english_refrigerator,
            related_service=english_freezer,
            sort_order=0,
        )
        call_command("setup_spanish_pages", stdout=StringIO(), stderr=StringIO())
        spanish_refrigerator = ServicePage.objects.get(
            translation_key=english_refrigerator.translation_key,
            locale__language_code="es",
        )
        spanish_freezer = ServicePage.objects.get(
            translation_key=english_freezer.translation_key,
            locale__language_code="es",
        )
        first_rows = list(spanish_refrigerator.related_services.order_by("sort_order", "pk"))
        self.assertEqual(
            [row.related_service_id for row in first_rows],
            [spanish_freezer.pk],
        )

        first_rows[0].related_service = english_freezer
        first_rows[0].save()
        ServiceRelatedService.objects.create(
            page=spanish_refrigerator,
            related_service=spanish_freezer,
            sort_order=1,
        )
        revisions_before = spanish_refrigerator.revisions.count()

        call_command("setup_spanish_pages", stdout=StringIO(), stderr=StringIO())

        repaired_rows = list(
            spanish_refrigerator.related_services.order_by("sort_order", "pk")
        )
        self.assertEqual(
            [row.related_service_id for row in repaired_rows],
            [spanish_freezer.pk],
        )
        self.assertEqual(
            repaired_rows[0].related_service.locale.language_code,
            "es",
        )
        self.assertIn("/es/", repaired_rows[0].related_service.get_url())
        self.assertEqual(spanish_refrigerator.revisions.count(), revisions_before)

        call_command("setup_spanish_pages", stdout=StringIO(), stderr=StringIO())
        self.assertEqual(spanish_refrigerator.related_services.count(), 1)
        self.assertEqual(spanish_refrigerator.revisions.count(), revisions_before)

    def test_update_service_content_populates_missing_fields_and_related_links(self) -> None:
        refrigerator = ServicePage(
            title="Refrigerator Repair",
            slug="refrigerator-repair",
            intro="Editor-entered intro must remain when optional fields are seeded.",
        )
        freezer = ServicePage(
            title="Freezer Repair",
            slug="freezer-repair",
            intro="Freezer intro must remain when optional fields are seeded.",
        )
        self.services_index.add_child(instance=refrigerator)
        refrigerator.save_revision().publish()
        self.services_index.add_child(instance=freezer)
        freezer.save_revision().publish()

        call_command("update_service_content", stdout=StringIO(), stderr=StringIO())

        refrigerator.refresh_from_db()
        self.assertEqual(
            refrigerator.intro,
            "Editor-entered intro must remain when optional fields are seeded.",
        )
        self.assertIn("Refrigerator Repair", refrigerator.seo_title)
        self.assertGreater(len(refrigerator.body), 0)
        self.assertGreater(len(refrigerator.problems_we_fix), 0)
        self.assertGreater(len(refrigerator.why_choose_us), 0)
        self.assertGreater(len(refrigerator.faq), 0)
        self.assertTrue(
            ServiceRelatedService.objects.filter(
                page=refrigerator,
                related_service=freezer,
            ).exists()
        )

    def test_update_service_content_preserves_editor_customized_seeded_fields_on_rerun(self) -> None:
        from home.management.commands.setup_pages import SERVICE_CONTENT

        seeded_by_slug = {service["slug"]: service for service in SERVICE_CONTENT}
        refrigerator_seed = seeded_by_slug["refrigerator-repair"]
        freezer_seed = seeded_by_slug["freezer-repair"]
        refrigerator = ServicePage(
            title=refrigerator_seed["title"],
            slug="refrigerator-repair",
            seo_title=refrigerator_seed["seo_title"],
            search_description=refrigerator_seed["search_description"],
            intro=refrigerator_seed["intro"],
            short_description=refrigerator_seed["short_description"],
            hero_usp=refrigerator_seed["hero_usp"],
            body=refrigerator_seed["body"],
            problems_we_fix=json.dumps(
                [
                    {"type": "problem", "value": problem}
                    for problem in refrigerator_seed["problems"]
                ]
            ),
            why_choose_us=json.dumps(
                [
                    {
                        "type": "benefit",
                        "value": {"title": title, "description": description},
                    }
                    for title, description in refrigerator_seed["benefits"]
                ]
            ),
            faq=json.dumps(
                [
                    {
                        "type": "faq_item",
                        "value": {"question": question, "answer": answer},
                    }
                    for question, answer in refrigerator_seed["faq"]
                ]
            ),
        )
        freezer = ServicePage(
            title=freezer_seed["title"],
            slug="freezer-repair",
            intro=freezer_seed["intro"],
        )
        self.services_index.add_child(instance=refrigerator)
        refrigerator.save_revision().publish()
        self.services_index.add_child(instance=freezer)
        freezer.save_revision().publish()
        revisions_before_customization = refrigerator.revisions.count()

        custom_problems = json.dumps(
            [{"type": "problem", "value": "EDITOR CUSTOM PROBLEM"}]
        )
        custom_benefits = json.dumps(
            [
                {
                    "type": "benefit",
                    "value": {
                        "title": "EDITOR CUSTOM BENEFIT",
                        "description": "EDITOR CUSTOM BENEFIT BODY",
                    },
                }
            ]
        )
        custom_faq = json.dumps(
            [
                {
                    "type": "faq_item",
                    "value": {
                        "question": "EDITOR CUSTOM QUESTION",
                        "answer": "EDITOR CUSTOM ANSWER",
                    },
                }
            ]
        )
        refrigerator.intro = "EDITOR CUSTOM INTRO"
        refrigerator.public_h1 = "EDITOR CUSTOM H1"
        refrigerator.photo_carousel_title = "EDITOR CUSTOM CAROUSEL"
        refrigerator.short_description = "EDITOR CUSTOM SHORT"
        refrigerator.hero_usp = "EDITOR CUSTOM USP"
        refrigerator.body = "<p>EDITOR CUSTOM BODY</p>"
        refrigerator.problems_we_fix = custom_problems
        refrigerator.why_choose_us = custom_benefits
        refrigerator.faq = custom_faq
        refrigerator.save()

        call_command("update_service_content", stdout=StringIO(), stderr=StringIO())

        refrigerator.refresh_from_db()
        self.assertEqual(refrigerator.intro, "EDITOR CUSTOM INTRO")
        self.assertEqual(refrigerator.public_h1, "EDITOR CUSTOM H1")
        self.assertEqual(refrigerator.photo_carousel_title, "EDITOR CUSTOM CAROUSEL")
        self.assertEqual(refrigerator.short_description, "EDITOR CUSTOM SHORT")
        self.assertEqual(refrigerator.hero_usp, "EDITOR CUSTOM USP")
        self.assertEqual(str(refrigerator.body), "<p>EDITOR CUSTOM BODY</p>")
        problems = list(getattr(refrigerator.problems_we_fix, "raw_data"))
        benefits = list(getattr(refrigerator.why_choose_us, "raw_data"))
        faq = list(getattr(refrigerator.faq, "raw_data"))
        self.assertEqual(problems[0]["value"], "EDITOR CUSTOM PROBLEM")
        self.assertEqual(
            benefits[0]["value"]["title"], "EDITOR CUSTOM BENEFIT"
        )
        self.assertEqual(faq[0]["value"]["question"], "EDITOR CUSTOM QUESTION")
        self.assertEqual(refrigerator.revisions.count(), revisions_before_customization)
