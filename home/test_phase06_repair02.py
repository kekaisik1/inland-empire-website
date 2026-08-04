"""Regression contracts for the final Phase 06 content/localization repair."""

from __future__ import annotations

import json
from datetime import date
from io import StringIO
from typing import Any

from django.core.management import call_command
from django.test import TestCase
from django.utils import translation
from django.utils.translation import gettext
from wagtail.models import Locale

from blog.models import BlogIndexPage, BlogPage
from home.tests import create_test_home
from locations.models import CityPage, LocationsIndexPage
from services.models import ServicePage, ServicesIndexPage


def _without_ids(value: Any) -> Any:
    if isinstance(value, list):
        return [_without_ids(item) for item in value]
    if isinstance(value, dict):
        return {
            key: _without_ids(item)
            for key, item in value.items()
            if key != "id"
        }
    return value


def _stream_data(value: Any) -> list[dict[str, Any]]:
    raw_data = getattr(value, "raw_data", None)
    if raw_data is not None:
        return _without_ids(list(raw_data))
    raw_text = str(getattr(value, "raw_text", value) or "[]")
    return _without_ids(json.loads(raw_text))


class Phase06Repair02ContentCommandTests(TestCase):
    """Content reconciliation must target generated/sentinel state, not editors."""

    def setUp(self) -> None:
        self.home, _site = create_test_home()
        self.services_index = ServicesIndexPage(title="Services", slug="services")
        self.home.add_child(instance=self.services_index)
        self.services_index.save_revision().publish()

    def _add_service(self, data: dict[str, Any]) -> ServicePage:
        from home.service_seed_data import apply_service_page_seed_data

        page = ServicePage(title=data["title"], slug=data["slug"], intro=data["intro"])
        apply_service_page_seed_data(page, data)
        self.services_index.add_child(instance=page)
        page.save_revision().publish()
        return page

    def test_update_service_content_repairs_only_exact_verification_sentinels(self) -> None:
        from home.management.commands.setup_pages import SERVICE_CONTENT

        seed = next(item for item in SERVICE_CONTENT if item["slug"] == "refrigerator-repair")
        page = self._add_service(seed)
        page.public_h1 = "VERIFY CUSTOM H1"
        page.photo_carousel_title = "EDITOR CUSTOM CAROUSEL"
        page.intro = "VERIFY CUSTOM INTRO"
        page.short_description = "EDITOR CUSTOM SHORT"
        page.hero_usp = "VERIFY CUSTOM USP"
        page.body = "<p>VERIFY CUSTOM BODY</p>"
        page.problems_we_fix = json.dumps(
            [{"type": "problem", "value": "VERIFY CUSTOM PROBLEM"}]
        )
        page.why_choose_us = json.dumps(
            [
                {
                    "type": "benefit",
                    "value": {
                        "title": "VERIFY CUSTOM BENEFIT",
                        "description": "VERIFY CUSTOM BENEFIT BODY",
                    },
                }
            ]
        )
        page.faq = json.dumps(
            [
                {
                    "type": "faq_item",
                    "value": {
                        "question": "VERIFY CUSTOM QUESTION",
                        "answer": "VERIFY CUSTOM ANSWER",
                    },
                }
            ]
        )
        page.save()
        revisions_before = page.revisions.count()

        call_command("update_service_content", stdout=StringIO(), stderr=StringIO())

        page.refresh_from_db()
        self.assertEqual(page.public_h1, "")
        self.assertEqual(page.photo_carousel_title, "EDITOR CUSTOM CAROUSEL")
        self.assertEqual(page.intro, seed["intro"])
        self.assertEqual(page.short_description, "EDITOR CUSTOM SHORT")
        self.assertEqual(page.hero_usp, seed["hero_usp"])
        self.assertEqual(str(page.body), seed["body"])
        self.assertEqual(
            [block["value"] for block in _stream_data(page.problems_we_fix)],
            seed["problems"],
        )
        self.assertEqual(
            [block["value"] for block in _stream_data(page.why_choose_us)],
            [
                {"title": title, "description": description}
                for title, description in seed["benefits"]
            ],
        )
        self.assertEqual(
            [block["value"] for block in _stream_data(page.faq)],
            [
                {"question": question, "answer": answer}
                for question, answer in seed["faq"]
            ],
        )
        self.assertEqual(page.revisions.count(), revisions_before + 1)

        call_command("update_service_content", stdout=StringIO(), stderr=StringIO())
        page.refresh_from_db()
        self.assertEqual(page.revisions.count(), revisions_before + 1)

    def test_spanish_core_repair_distinguishes_copied_sentinel_and_editor_fields(self) -> None:
        from home.management.commands.populate_spanish_content import SERVICE_CONTENT
        from home.management.commands.setup_pages import SERVICE_CONTENT as ENGLISH_SERVICES

        english_seed = next(
            item for item in ENGLISH_SERVICES if item["slug"] == "refrigerator-repair"
        )
        english = self._add_service(english_seed)
        call_command("setup_spanish_pages", stdout=StringIO(), stderr=StringIO())
        spanish = ServicePage.objects.get(
            translation_key=english.translation_key,
            locale__language_code="es",
        )
        spanish.title = english.title
        spanish.intro = english.intro
        spanish.short_description = "DESCRIPCIÓN EDITORIAL EN ESPAÑOL"
        spanish.hero_usp = "VERIFY CUSTOM USP"
        spanish.body = english.body
        spanish.problems_we_fix = json.dumps(list(english.problems_we_fix.raw_data))
        spanish.why_choose_us = json.dumps(
            [
                {
                    "type": "benefit",
                    "value": {
                        "title": "VERIFY CUSTOM BENEFIT",
                        "description": "VERIFY CUSTOM BENEFIT BODY",
                    },
                }
            ]
        )
        spanish.faq = json.dumps(list(english.faq.raw_data))
        spanish.save()
        revisions_before = spanish.revisions.count()

        call_command("setup_spanish_pages", stdout=StringIO(), stderr=StringIO())

        spanish.refresh_from_db()
        expected = SERVICE_CONTENT["refrigerator-repair"]
        self.assertEqual(spanish.title, "Reparación de Refrigeradores")
        self.assertEqual(spanish.intro, "Servicios profesionales de reparación de refrigeradores.")
        self.assertEqual(spanish.short_description, "DESCRIPCIÓN EDITORIAL EN ESPAÑOL")
        self.assertEqual(
            spanish.hero_usp,
            "Reparación de refrigeradores el mismo día. Reparamos todas las marcas.",
        )
        self.assertEqual(str(spanish.body), expected["body"])
        self.assertEqual(
            [block["value"] for block in _stream_data(spanish.problems_we_fix)],
            expected["problems"],
        )
        self.assertEqual(
            [block["value"] for block in _stream_data(spanish.why_choose_us)],
            expected["benefits"],
        )
        self.assertEqual(
            [block["value"] for block in _stream_data(spanish.faq)],
            expected["faqs"],
        )
        self.assertEqual(spanish.revisions.count(), revisions_before + 1)

    def test_spanish_supplemental_services_use_target_owned_payloads(self) -> None:
        from home.high_end_brand_seed_data import (
            HIGH_END_BRAND_SERVICE_PAGES,
            SPANISH_HIGH_END_BRAND_SERVICE_PAGES,
        )
        from home.management.commands.create_brand_pages import BRAND_PAGES
        from home.service_seed_data import (
            HIGH_END_SERVICE_PAGE,
            SPANISH_HIGH_END_SERVICE_PAGE,
        )

        english_pages = {
            data["slug"]: self._add_service(data)
            for data in (
                HIGH_END_SERVICE_PAGE,
                HIGH_END_BRAND_SERVICE_PAGES[0],
                BRAND_PAGES[0],
            )
        }

        call_command("setup_spanish_pages", stdout=StringIO(), stderr=StringIO())

        expected_by_slug = {
            HIGH_END_SERVICE_PAGE["slug"]: SPANISH_HIGH_END_SERVICE_PAGE,
            HIGH_END_BRAND_SERVICE_PAGES[0]["slug"]: SPANISH_HIGH_END_BRAND_SERVICE_PAGES[0],
        }
        for slug, expected in expected_by_slug.items():
            spanish = ServicePage.objects.get(
                translation_key=english_pages[slug].translation_key,
                locale__language_code="es",
            )
            for field in (
                "title",
                "seo_title",
                "search_description",
                "intro",
                "short_description",
                "hero_usp",
                "body",
            ):
                with self.subTest(slug=slug, field=field):
                    self.assertEqual(str(getattr(spanish, field)), str(expected[field]))
                    self.assertNotEqual(
                        str(getattr(spanish, field)),
                        str(getattr(english_pages[slug], field)),
                    )
            self.assertEqual(
                [block["value"] for block in _stream_data(spanish.problems_we_fix)],
                expected["problems"],
            )
            self.assertEqual(
                [block["value"] for block in _stream_data(spanish.why_choose_us)],
                [
                    {"title": title, "description": description}
                    for title, description in expected["benefits"]
                ],
            )
            self.assertEqual(
                [block["value"] for block in _stream_data(spanish.faq)],
                [
                    {"question": question, "answer": answer}
                    for question, answer in expected["faq"]
                ],
            )

        samsung = ServicePage.objects.get(
            translation_key=english_pages["samsung-appliance-repair"].translation_key,
            locale__language_code="es",
        )
        self.assertEqual(samsung.title, "Reparación de Electrodomésticos Samsung")
        for field in (
            "title",
            "seo_title",
            "search_description",
            "intro",
            "short_description",
            "hero_usp",
            "body",
        ):
            with self.subTest(slug=samsung.slug, field=field):
                self.assertTrue(str(getattr(samsung, field)).strip())
                self.assertNotEqual(
                    str(getattr(samsung, field)),
                    str(getattr(english_pages[samsung.slug], field)),
                )
        self.assertGreater(len(_stream_data(samsung.problems_we_fix)), 0)
        self.assertGreater(len(_stream_data(samsung.why_choose_us)), 0)
        self.assertGreater(len(_stream_data(samsung.faq)), 0)

    def test_spanish_city_body_and_service_explanation_are_seeded_once(self) -> None:
        locations_index = LocationsIndexPage(
            title="Service Areas",
            slug="service-areas",
            intro="Service areas.",
        )
        self.home.add_child(instance=locations_index)
        locations_index.save_revision().publish()
        english = CityPage(
            title="Corona",
            slug="appliance-repair-corona-ca",
            intro="English Corona intro",
            hero_usp="English Corona hero",
            body="<h2>English city body</h2><p>English city content.</p>",
            about_techs="<p>English technician claims.</p>",
        )
        locations_index.add_child(instance=english)
        english.save_revision().publish()

        call_command("setup_spanish_pages", stdout=StringIO(), stderr=StringIO())

        spanish = CityPage.objects.get(
            translation_key=english.translation_key,
            locale__language_code="es",
        )
        self.assertIn("Reparación de electrodomésticos en Corona", str(spanish.body))
        self.assertIn("diagnóstico", str(spanish.body).lower())
        self.assertIn("Corona", str(spanish.about_techs))
        self.assertNotEqual(str(spanish.body), str(english.body))
        self.assertNotEqual(str(spanish.about_techs), str(english.about_techs))
        revisions_before = spanish.revisions.count()

        call_command("setup_spanish_pages", stdout=StringIO(), stderr=StringIO())
        spanish.refresh_from_db()
        self.assertEqual(spanish.revisions.count(), revisions_before)

        spanish.body = "<p>CUERPO EDITORIAL EN ESPAÑOL</p>"
        spanish.about_techs = "<p>CONTENIDO EDITORIAL DEL SERVICIO</p>"
        spanish.save()
        call_command("setup_spanish_pages", stdout=StringIO(), stderr=StringIO())
        spanish.refresh_from_db()
        self.assertEqual(str(spanish.body), "<p>CUERPO EDITORIAL EN ESPAÑOL</p>")
        self.assertEqual(
            str(spanish.about_techs),
            "<p>CONTENIDO EDITORIAL DEL SERVICIO</p>",
        )

    def test_setup_spanish_pages_reconciles_real_blog_payload_idempotently(self) -> None:
        blog_index = BlogIndexPage(title="Blog", slug="blog")
        self.home.add_child(instance=blog_index)
        blog_index.save_revision().publish()
        english = BlogPage(
            title="Why Is My Refrigerator Not Cooling?",
            slug="refrigerator-not-cooling-causes-fixes",
            date=date(2026, 8, 4),
            intro="English refrigerator guide.",
            author_name="Inland Service Desk",
            body=[("heading", "English heading"), ("paragraph", "<p>English body.</p>")],
        )
        blog_index.add_child(instance=english)
        english.save_revision().publish()

        call_command("setup_spanish_pages", stdout=StringIO(), stderr=StringIO())

        spanish = BlogPage.objects.get(
            translation_key=english.translation_key,
            locale__language_code="es",
        )
        self.assertTrue(spanish.live)
        self.assertIn("Refrigerador", spanish.title)
        self.assertNotEqual(spanish.title, english.title)
        self.assertNotEqual(str(spanish.body), str(english.body))
        revisions_before = spanish.revisions.count()
        count_before = BlogPage.objects.filter(locale__language_code="es").count()

        call_command("setup_spanish_pages", stdout=StringIO(), stderr=StringIO())
        spanish.refresh_from_db()
        self.assertEqual(
            BlogPage.objects.filter(locale__language_code="es").count(),
            count_before,
        )
        self.assertEqual(spanish.revisions.count(), revisions_before)

    def test_spanish_blog_repair_preserves_editor_title_while_replacing_copied_body(self) -> None:
        blog_index = BlogIndexPage(title="Blog", slug="blog")
        self.home.add_child(instance=blog_index)
        blog_index.save_revision().publish()
        english = BlogPage(
            title="Why Is My Refrigerator Not Cooling?",
            slug="refrigerator-not-cooling-causes-fixes",
            date=date(2026, 8, 4),
            intro="English refrigerator guide.",
            body=[("heading", "English heading"), ("paragraph", "<p>English body.</p>")],
        )
        blog_index.add_child(instance=english)
        english.save_revision().publish()
        es_locale, _created = Locale.objects.get_or_create(language_code="es")
        es_home = self.home.copy_for_translation(es_locale)
        es_home.save_revision().publish()
        es_blog_index = blog_index.copy_for_translation(es_locale)
        es_blog_index.save_revision().publish()
        spanish = english.copy_for_translation(es_locale)
        spanish.title = "TÍTULO EDITORIAL EN ESPAÑOL"
        spanish.intro = english.intro
        spanish.body = json.dumps(list(english.body.raw_data))
        spanish.save()
        spanish.save_revision().publish()

        call_command("setup_spanish_pages", stdout=StringIO(), stderr=StringIO())

        spanish.refresh_from_db()
        self.assertEqual(spanish.title, "TÍTULO EDITORIAL EN ESPAÑOL")
        self.assertNotEqual(spanish.intro, english.intro)
        self.assertNotEqual(str(spanish.body), str(english.body))

    def test_about_content_fix_creates_no_revision_when_seed_is_current(self) -> None:
        from home.management.commands.seo_content_fixes import (
            ABOUT_BODY,
            ABOUT_HERO_SUBTITLE,
            ABOUT_SEARCH_DESCRIPTION,
        )
        from pages.models import StaticPage

        about = StaticPage(
            title="About Us",
            slug="about-us",
            body=ABOUT_BODY,
            hero_subtitle=ABOUT_HERO_SUBTITLE,
            search_description=ABOUT_SEARCH_DESCRIPTION,
        )
        self.home.add_child(instance=about)
        about.save_revision().publish()
        revisions_before = about.revisions.count()

        call_command("seo_content_fixes", stdout=StringIO(), stderr=StringIO())

        about.refresh_from_db()
        self.assertEqual(about.revisions.count(), revisions_before)

    def test_about_content_fix_preserves_nonseed_editor_content(self) -> None:
        from pages.models import StaticPage

        about = StaticPage(
            title="About Us",
            slug="about-us",
            body="<p>EDITOR AUTHORED ABOUT BODY</p>",
            hero_subtitle="EDITOR AUTHORED ABOUT SUBTITLE",
            search_description="EDITOR AUTHORED ABOUT DESCRIPTION",
        )
        self.home.add_child(instance=about)
        about.save_revision().publish()

        call_command("seo_content_fixes", stdout=StringIO(), stderr=StringIO())

        about.refresh_from_db()
        self.assertEqual(about.body, "<p>EDITOR AUTHORED ABOUT BODY</p>")
        self.assertEqual(about.hero_subtitle, "EDITOR AUTHORED ABOUT SUBTITLE")
        self.assertEqual(
            about.search_description,
            "EDITOR AUTHORED ABOUT DESCRIPTION",
        )


class Phase06Repair02CatalogTests(TestCase):
    """Representative Phase 06 UI strings must resolve through the compiled catalog."""

    def test_runtime_spanish_catalog_translates_repair_page_labels(self) -> None:
        expected = {
            "Repair work order": "Orden de trabajo de reparación",
            "Choose your city": "Elija su ciudad",
            "Repair notebook": "Cuaderno de reparaciones",
            "In This Article": "En este artículo",
            "Field note": "Nota de campo",
            "Service-area switcher": "Selector de área de servicio",
            (
                "Use a brand route for model-specific service information. "
                "Unlinked marks identify supported asset coverage only."
            ): (
                "Use una ruta de marca para consultar información específica del modelo. "
                "Las marcas sin enlace solo indican cobertura de recursos compatibles."
            ),
        }
        with translation.override("es"):
            actual = {message: gettext(message) for message in expected}
        self.assertEqual(actual, expected)
