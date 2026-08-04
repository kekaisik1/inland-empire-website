"""Focused Phase 05 render contracts for the global shell and homepage."""

from __future__ import annotations

import json
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from django.core.cache import cache
from django.core.management import call_command
from django.test import RequestFactory, TestCase, override_settings
from django.utils import translation
from wagtail.models import Locale
from wagtail.test.utils import WagtailPageTestCase

from home.models import SiteSettings
from home.templatetags.seo_tags import jsonld_howto
from home.tests import create_test_home
from locations.models import CityPage, LocationsIndexPage
from pages.models import StaticPage
from services.models import ServicePage, ServicesIndexPage


class Phase05ShellHomeRenderTests(WagtailPageTestCase):
    """The Phase 02-04 contracts must be visible in the target-native UI."""

    def setUp(self) -> None:
        cache.clear()
        self.addCleanup(cache.clear)
        self.home, self.site = create_test_home()
        self.biz = SiteSettings.objects.create(
            site=self.site,
            business_name="Inland Test Appliance Repair",
            phone="+190****2506",
            email="hello@inland.test",
            city="Corona",
            state="CA",
            zip_code="92879",
            booking_url="https://booking.inland.test/schedule",
            booking_source="inland-test",
            main_nav_order="contact,services,service_areas,brands,home",
            footer_company_order="terms_of_service,about",
        )

        self.services_index = ServicesIndexPage(
            title="Services",
            slug="services",
            hero_title="Services",
        )
        self.home.add_child(instance=self.services_index)
        self.services_index.save_revision().publish()

        self.refrigerator = ServicePage(
            title="Refrigerator Repair",
            slug="refrigerator-repair",
            intro="Cooling repair.",
            short_description="Cooling issues and leaks.",
        )
        self.services_index.add_child(instance=self.refrigerator)
        self.refrigerator.save_revision().publish()

        self.whirlpool = ServicePage(
            title="Whirlpool Appliance Repair",
            slug="whirlpool-appliance-repair",
            intro="Whirlpool repair.",
            short_description="Whirlpool appliance service.",
        )
        self.services_index.add_child(instance=self.whirlpool)
        self.whirlpool.save_revision().publish()

        self.locations_index = LocationsIndexPage(
            title="Service Areas",
            slug="service-areas",
        )
        self.home.add_child(instance=self.locations_index)
        self.locations_index.save_revision().publish()
        self.city = CityPage(
            title="Corona",
            slug="appliance-repair-corona-ca",
            intro="Repair in Corona.",
            zip_codes="92879, 92880",
        )
        self.locations_index.add_child(instance=self.city)
        self.city.save_revision().publish()

    def test_shell_renders_editor_ordered_navigation_dropdowns_and_footer(self) -> None:
        response = self.client.get("/")
        content = response.content.decode()

        ordered_markers = [
            'data-nav-key="contact"',
            'data-nav-key="services"',
            'data-nav-key="service_areas"',
            'data-nav-key="brands"',
            'data-nav-key="home"',
        ]
        missing_markers = [marker for marker in ordered_markers if marker not in content]
        self.assertEqual(missing_markers, [], "ordered navigation markers are missing")
        positions = [content.index(marker) for marker in ordered_markers]
        self.assertEqual(positions, sorted(positions))
        self.assertIn('aria-controls="desktop-services-menu"', content)
        self.assertIn('aria-controls="desktop-areas-menu"', content)
        self.assertIn('aria-controls="desktop-brands-menu"', content)
        self.assertIn('data-nav-brand-link="whirlpool-appliance-repair"', content)

        terms = content.index('data-footer-link-key="terms_of_service"')
        about = content.index('data-footer-link-key="about"')
        self.assertLess(terms, about)

    def test_default_navigation_contract_keeps_all_keys_and_localizes_spanish(self) -> None:
        from mysite.context_processors import navigation_data

        self.biz.main_nav_order = ""
        self.biz.footer_company_order = ""
        self.biz.save()
        request = RequestFactory().get("/es/")
        request.META["HTTP_HOST"] = "testserver"

        with translation.override("es"):
            context = navigation_data(request)

        self.assertEqual(
            [item["key"] for item in context["main_nav_items"]],
            ["home", "services", "service_areas", "brands", "blog", "about", "contact"],
        )
        self.assertEqual(
            [item["url"] for item in context["main_nav_items"]],
            [
                "/es/",
                "/es/services/",
                "/es/service-areas/",
                "",
                "/es/blog/",
                "/es/about-us/",
                "/es/contact/",
            ],
        )
        labels = {item["key"]: item["label"] for item in context["main_nav_items"]}
        self.assertEqual(labels["services"], "Servicios")
        self.assertEqual(labels["service_areas"], "Áreas de Servicio")
        self.assertEqual(labels["brands"], "Marcas")

    def test_spanish_howto_schema_is_fully_localized(self) -> None:
        request = RequestFactory().get("/es/")
        request.META["HTTP_HOST"] = "testserver"

        with translation.override("es"):
            schema = jsonld_howto({"biz": self.biz, "request": request})

        payload = json.loads(schema.partition(">")[2].removesuffix("</script>"))
        serialized = json.dumps(payload, ensure_ascii=False)
        self.assertIn("Cómo reservar reparación", serialized)
        self.assertIn("Un técnico certificado llega", serialized)
        self.assertIn("Todas las reparaciones incluyen garantía", serialized)
        self.assertNotIn("A certified technician arrives", serialized)
        self.assertNotIn("We fix it on the spot", serialized)

    def test_homepage_uses_editable_fields_inside_the_dark_design(self) -> None:
        editable = {
            "hero_title": "PHASE05 EDITABLE HERO",
            "hero_subtitle": "PHASE05 EDITABLE HERO SUBTITLE",
            "commercial_title": "PHASE05 EDITABLE COMMERCIAL",
            "commercial_body": "<p>PHASE05 EDITABLE COMMERCIAL BODY</p>",
            "services_heading": "PHASE05 EDITABLE SERVICES",
            "process_heading": "PHASE05 EDITABLE PROCESS",
            "process_subheading": "PHASE05 EDITABLE PROCESS SUBTITLE",
            "pricing_heading": "PHASE05 EDITABLE PRICING",
            "pricing_note": "PHASE05 EDITABLE PRICING NOTE",
            "brands_heading": "PHASE05 EDITABLE BRANDS",
            "brands_subheading": "PHASE05 EDITABLE BRANDS SUBTITLE",
            "areas_heading": "PHASE05 EDITABLE AREAS",
            "areas_subheading": "PHASE05 EDITABLE AREAS SUBTITLE",
            "faq_heading": "PHASE05 EDITABLE FAQ",
        }
        for field, value in editable.items():
            setattr(self.home, field, value)
        self.home.save_revision().publish()

        content = self.client.get("/").content.decode()
        for value in editable.values():
            with self.subTest(value=value):
                expected = value.replace("<p>", "").replace("</p>", "")
                self.assertIn(expected, content)
        self.assertIn('class="stripe-bg"', content)
        self.assertIn('class="booking-widget"', content)
        self.assertIn("bg-background", content)
        self.assertNotIn("#1545ad", content.lower())
        self.assertNotIn("satoshi", content.lower())

    def test_homepage_defaults_never_render_editorial_workflow_copy(self) -> None:
        content = self.client.get("/").content.decode()

        for editorial_marker in (
            "Use this editable",
            "keep this process copy editable",
            "target-approved",
            "after claims are reviewed",
        ):
            with self.subTest(editorial_marker=editorial_marker):
                self.assertNotIn(editorial_marker, content)

    def test_homepage_renders_target_locality_as_the_hero_eyebrow(self) -> None:
        content = self.client.get("/").content.decode()

        self.assertIn('data-home-locality="inland-empire"', content)
        self.assertIn(">Inland Empire</p>", content)

    def test_booking_zip_field_has_a_programmatic_label(self) -> None:
        content = self.client.get("/").content.decode()

        self.assertIn('<label for="hero-zip"', content)

    def test_home_context_separates_core_services_and_builds_linked_brand_cards(self) -> None:
        response = self.client.get("/")

        service_slugs = [service.slug for service in response.context["services"]]
        self.assertIn("refrigerator-repair", service_slugs)
        self.assertNotIn("whirlpool-appliance-repair", service_slugs)
        brand_cards = {
            card["slug"]: card for card in response.context["brand_cards"]
        }
        self.assertEqual(
            brand_cards["whirlpool-appliance-repair"]["page"].pk,
            self.whirlpool.pk,
        )
        self.assertEqual(
            brand_cards["whirlpool-appliance-repair"]["logo_static"],
            "images/brand-logos/whirlpool.png",
        )

    def test_home_renders_brand_assets_and_only_approved_review_cards(self) -> None:
        self.home.brands_heading = "PHASE05 LINKED BRANDS"
        self.home.testimonials_heading = "PHASE05 APPROVED REVIEWS"
        self.home.save_revision().publish()
        approved = [
            {
                "author": "Target Customer",
                "date": "Jul 2026",
                "date_published": "2026-07-01",
                "rating": 5,
                "source": "Target-owned source",
                "source_url": "https://reviews.inland.test/review/1",
                "text": "A target-owned review fixture.",
            }
        ]

        with patch("home.models.get_customer_review_items", return_value=approved):
            content = self.client.get("/").content.decode()

        self.assertIn("PHASE05 LINKED BRANDS", content)
        self.assertIn("images/brand-logos/whirlpool.png", content)
        self.assertIn('data-brand-repair-link="whirlpool-appliance-repair"', content)
        self.assertIn("PHASE05 APPROVED REVIEWS", content)
        self.assertIn('data-review-card', content)
        self.assertIn('href="https://reviews.inland.test/review/1"', content)

    def test_hreflang_excludes_draft_translation_then_includes_live_translation(self) -> None:
        es_locale, _ = Locale.objects.get_or_create(language_code="es")
        es_home = self.home.copy_for_translation(es_locale)
        es_home.hero_title = "HÉROE EDITABLE EN ESPAÑOL"
        es_home.save_revision()

        draft_content = self.client.get("/").content.decode()
        self.assertNotIn('<link rel="alternate" hreflang="es"', draft_content)

        es_home.save_revision().publish()
        english_content = self.client.get("/").content.decode()
        self.assertIn('<link rel="alternate" hreflang="es"', english_content)

        spanish_response = self.client.get(es_home.get_url())
        self.assertEqual(spanish_response.status_code, 200)
        spanish_content = spanish_response.content.decode()
        self.assertIn('lang="es"', spanish_content)
        self.assertIn("HÉROE EDITABLE EN ESPAÑOL", spanish_content)
        self.assertIn("Servicios", spanish_content)

    def test_spanish_seed_repairs_a_copied_english_homepage(self) -> None:
        es_locale, _ = Locale.objects.get_or_create(language_code="es")
        es_home = self.home.copy_for_translation(es_locale)
        es_home.save_revision().publish()

        call_command("setup_spanish_pages", stdout=StringIO(), stderr=StringIO())

        es_home.refresh_from_db()
        self.assertIn("REPARACIÓN", es_home.hero_title)
        self.assertIn("Residencial", es_home.commercial_title)
        self.assertIn("Preguntas", es_home.faq_heading)
        self.assertNotEqual(es_home.process_subheading, self.home.process_subheading)

        spanish_content = self.client.get(es_home.get_url()).content.decode()
        for english_marker in (
            "Book a Repair",
            "Every truck is stocked",
            "Licensed & insured",
            "Licensed &amp; insured",
            "Fully stocked trucks",
            "OEM & commercial-grade",
            "OEM &amp; commercial-grade",
            "Flat-rate pricing",
            "Refrigerators, washers, dryers, ovens, dishwashers & more",
            "Don't see your brand?",
        ):
            with self.subTest(english_marker=english_marker):
                self.assertNotIn(english_marker, spanish_content)

    def test_setup_pages_repairs_missing_legal_footer_routes(self) -> None:
        self.assertFalse(StaticPage.objects.filter(slug="privacy-policy").exists())
        self.assertFalse(StaticPage.objects.filter(slug="terms-of-service").exists())

        call_command("setup_pages", stdout=StringIO(), stderr=StringIO())

        self.assertTrue(StaticPage.objects.filter(slug="privacy-policy", live=True).exists())
        self.assertTrue(StaticPage.objects.filter(slug="terms-of-service", live=True).exists())

    @override_settings(
        TRACKING_ENABLED=True,
        TRACKING_REQUIRE_CONSENT=True,
        TRACKING_STORAGE_KEY="inland_phase05_sid",
        TRACKING_COLLECTION_PATH="/api/track/collect/",
        BOOKING_DOMAIN="booking.inland.test",
    )
    def test_shell_includes_target_tracker_and_callrail_only_when_configured(self) -> None:
        self.biz.callrail_swap_url = "https://cdn.callrail.test/swap.js"
        self.biz.save()

        enabled = self.client.get("/").content.decode()
        self.assertIn("window.__INLAND_TRACK", enabled)
        self.assertIn('endpoint: "/api/track/collect/"', enabled)
        self.assertIn('storageKey: "inland_phase05_sid"', enabled)
        self.assertIn('consentRequired: true', enabled)
        self.assertIn("js/tracker.js", enabled)
        self.assertIn('src="https://cdn.callrail.test/swap.js"', enabled)
        self.assertNotIn("__LOWL_TRACK", enabled)

        with override_settings(TRACKING_ENABLED=False):
            disabled = self.client.get("/").content.decode()
        self.assertNotIn("window.__INLAND_TRACK", disabled)
        self.assertNotIn("js/tracker.js", disabled)

    def test_static_interaction_assets_use_target_owned_identifiers(self) -> None:
        static_js = Path(__file__).resolve().parents[1] / "mysite" / "static" / "js"
        tracker = static_js / "tracker.js"
        self.assertTrue(tracker.exists(), "Phase 05 target tracker.js is missing")
        combined = "\n".join(
            (static_js / name).read_text(encoding="utf-8")
            for name in ("utm.js", "tracker.js", "zip-check.js", "alpine-components.js")
        )
        forbidden = ("lowl_utm", "lowl_sid", "__LOWL_TRACK", "window.lowlTrack")
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(token, combined)
        self.assertIn("inland_utm", combined)
        self.assertIn("tracking_session_id", combined)

    def test_public_schema_helpers_have_no_source_identity_fallback(self) -> None:
        schema_source = (
            Path(__file__).resolve().parent / "templatetags" / "seo_tags.py"
        ).read_text()

        self.assertNotIn("LOWL Appliance Repair", schema_source)


@override_settings(DEBUG=False, ALLOWED_HOSTS=["testserver"])
class Phase05ErrorShellTests(TestCase):
    def setUp(self) -> None:
        cache.clear()
        self.addCleanup(cache.clear)
        self.home, self.site = create_test_home()
        SiteSettings.objects.create(site=self.site, business_name="Inland Error Shell")

    def test_404_inherits_global_shell_while_500_keeps_safe_dark_fallback(self) -> None:
        missing = self.client.get("/phase05-missing-page/")
        self.assertEqual(missing.status_code, 404)
        content = missing.content.decode()
        self.assertIn('aria-label="Main navigation"', content)
        self.assertIn('aria-label="Quick actions"', content)
        self.assertIn("bg-footer", content)

        fallback = (
            Path(__file__).resolve().parents[1] / "mysite" / "templates" / "500.html"
        ).read_text(encoding="utf-8")
        self.assertIn("#1A1B20", fallback)
        self.assertIn("#FFD504", fallback)
        self.assertNotIn("{% extends \"base.html\" %}", fallback)
