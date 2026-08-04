"""Phase 03 tests for middleware, context, machine endpoints, and settings."""

from __future__ import annotations

import importlib
import json
import os
import sys
from xml.etree import ElementTree
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.http import JsonResponse
from django.test import RequestFactory, SimpleTestCase, TestCase, override_settings

from home.models import SiteSettings
from home.tests import create_test_home


@override_settings(
    TRUSTED_PROXY_CIDRS=("10.0.0.0/8", "192.0.2.0/24", "2001:db8:ffff::/48"),
)
class RealIPMiddlewareTests(SimpleTestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        try:
            middleware_module = importlib.import_module("mysite.middleware")
            self.middleware_class = middleware_module.RealIPMiddleware
        except (ImportError, AttributeError) as exc:  # pragma: no cover - RED guard
            self.fail(f"trusted RealIP middleware is unavailable: {exc}")

    def _resolved_ip(self, *, peer: str, forwarded: str = "", real_ip: str = "") -> str:
        def endpoint(request):
            return JsonResponse({"ip": request.META.get("REMOTE_ADDR", "")})

        request = self.factory.get(
            "/",
            REMOTE_ADDR=peer,
            HTTP_X_FORWARDED_FOR=forwarded,
            HTTP_X_REAL_IP=real_ip,
        )
        response = self.middleware_class(endpoint)(request)
        return json.loads(response.content)["ip"]

    def test_untrusted_peer_cannot_spoof_forwarded_headers(self) -> None:
        resolved = self._resolved_ip(
            peer="198.51.100.40",
            forwarded="203.0.113.9",
            real_ip="203.0.113.10",
        )
        self.assertEqual(resolved, "198.51.100.40")

    def test_trusted_proxy_chain_walks_from_right_and_prefers_forwarded_for(self) -> None:
        resolved = self._resolved_ip(
            peer="10.0.0.5",
            forwarded="198.51.100.7, 192.0.2.8",
            real_ip="203.0.113.99",
        )
        self.assertEqual(resolved, "198.51.100.7")

    def test_invalid_forwarded_chain_falls_back_to_trusted_real_ip_then_peer(self) -> None:
        real_ip = self._resolved_ip(
            peer="10.0.0.5",
            forwarded="not-an-ip",
            real_ip="203.0.113.25",
        )
        peer = self._resolved_ip(
            peer="10.0.0.5",
            forwarded="not-an-ip",
            real_ip="also-invalid",
        )
        self.assertEqual(real_ip, "203.0.113.25")
        self.assertEqual(peer, "10.0.0.5")


@override_settings(ALLOWED_HOSTS=["testserver", "target.example"])
class ContextProcessorPhase03Tests(TestCase):
    def setUp(self) -> None:
        cache.clear()
        self.home, self.site = create_test_home()
        self.biz = SiteSettings.objects.create(
            site=self.site,
            business_name="Target Appliance Service",
            main_nav_order="contact,unknown,contact,home",
            footer_company_order="blog,about",
        )

    def test_navigation_uses_editor_order_target_cache_keys_and_safe_normalization(self) -> None:
        response = self.client.get("/")

        self.assertEqual(
            [item["key"] for item in response.context["main_nav_items"]],
            ["contact", "home"],
        )
        self.assertEqual(
            [item["key"] for item in response.context["footer_company_links"]],
            ["blog", "about"],
        )
        self.assertIsNotNone(cache.get("inland:nav:services:en"))
        self.assertIsNone(cache.get("lowl:nav:services:en"))

    @override_settings(
        TRACKING_ENABLED=True,
        TRACKING_REQUIRE_CONSENT=True,
        TRACKING_STORAGE_KEY="inland_tracking_sid",
        TRACKING_COLLECTION_PATH="/api/track/collect/",
        BOOKING_DOMAIN="booking.target.example",
    )
    def test_tracking_context_documents_cookie_free_session_storage_contract(self) -> None:
        from mysite.context_processors import tracking_context

        request = RequestFactory().get("/")
        context = tracking_context(request)

        self.assertTrue(context["tracking_enabled"])
        self.assertTrue(context["tracking_consent_required"])
        self.assertEqual(context["tracking_storage"], "sessionStorage")
        self.assertEqual(context["tracking_storage_key"], "inland_tracking_sid")
        self.assertEqual(context["tracking_endpoint"], "/api/track/collect/")
        self.assertEqual(context["booking_domain"], "booking.target.example")
        self.assertNotIn("cookie", " ".join(context).lower())

    def test_navigation_localizes_static_paths_for_spanish_request(self) -> None:
        from mysite.context_processors import navigation_data

        request = RequestFactory().get("/es/")
        context = navigation_data(request)

        self.assertEqual(
            [item["url"] for item in context["main_nav_items"]],
            ["/es/contact/", "/es/"],
        )


SECURITY_MIDDLEWARE = [
    "mysite.middleware.RealIPMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "mysite.middleware.SEOHeadersMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]


@override_settings(MIDDLEWARE=SECURITY_MIDDLEWARE, ALLOWED_HOSTS=["testserver"])
class SecurityHeadersPhase03Tests(TestCase):
    def setUp(self) -> None:
        create_test_home()

    def test_csp_matches_target_fonts_scripts_images_and_has_no_broad_wildcards(self) -> None:
        response = self.client.get("/")
        csp = response["Content-Security-Policy"]
        directives = {
            item.strip().split(" ", 1)[0]: item.strip()
            for item in csp.split(";")
            if item.strip()
        }

        self.assertIn("https://fonts.googleapis.com", directives["style-src"])
        self.assertIn("https://fonts.gstatic.com", directives["font-src"])
        self.assertIn("https://cdn.jsdelivr.net", directives["script-src"])
        self.assertIn("https://res.cloudinary.com", directives["img-src"])
        self.assertIn("https://www.googletagmanager.com", directives["script-src"])
        self.assertIn("object-src 'none'", csp)
        self.assertEqual(directives["frame-ancestors"], "frame-ancestors 'self'")
        self.assertNotIn("unsafe-eval", csp)
        self.assertNotIn("api.fontshare.com", csp)
        self.assertNotIn("cdn.fontshare.com", csp)
        self.assertNotIn("google.co.*", csp)
        self.assertNotIn(" *", csp)

    def test_error_and_search_responses_are_noindex_while_public_pages_are_indexable(self) -> None:
        public = self.client.get("/")
        search = self.client.get("/search/")
        missing = self.client.get("/does-not-exist/")

        self.assertEqual(public["X-Robots-Tag"], "index, follow")
        self.assertEqual(search["X-Robots-Tag"], "noindex, follow")
        self.assertEqual(missing["X-Robots-Tag"], "noindex, nofollow")

    def test_authenticated_html_is_not_marked_public_cacheable(self) -> None:
        user = get_user_model().objects.create_superuser(
            username="cache-admin",
            email="cache-admin@example.com",
            password="test-password",
        )
        self.client.force_login(user)
        response = self.client.get("/")
        self.assertNotIn("public", response.get("Cache-Control", ""))


@override_settings(ALLOWED_HOSTS=["testserver", "target.example"])
class MachineEndpointPhase03Tests(TestCase):
    def setUp(self) -> None:
        self.home, self.site = create_test_home()
        SiteSettings.objects.create(
            site=self.site,
            business_name="Target Appliance Service",
            phone="+19515550100",
            email="hello@target.example",
            city="Corona",
            state="CA",
            zip_code="92879",
        )

    def test_health_is_get_only_and_never_cacheable(self) -> None:
        get_response = self.client.get("/health/")
        post_response = self.client.post("/health/")

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json(), {"status": "ok"})
        self.assertEqual(get_response["Cache-Control"], "no-store")
        self.assertEqual(post_response.status_code, 405)

    def test_robots_and_sitemap_derive_scheme_and_host_from_request(self) -> None:
        robots = self.client.get("/robots.txt", HTTP_HOST="target.example")
        sitemap = self.client.get("/sitemap.xml", HTTP_HOST="target.example")

        robots_text = robots.content.decode()
        sitemap_text = sitemap.content.decode()
        self.assertIn("Sitemap: http://target.example/sitemap.xml", robots_text)
        self.assertIn("Disallow: /api/", robots_text)
        self.assertIn("http://target.example/", sitemap_text)
        self.assertNotIn("lowl", (robots_text + sitemap_text).lower())
        ElementTree.fromstring(sitemap.content)

    def test_llms_endpoints_use_target_identity_and_absolute_request_urls(self) -> None:
        concise = self.client.get("/llms.txt", HTTP_HOST="target.example")
        full = self.client.get("/llms-full.txt", HTTP_HOST="target.example")

        self.assertEqual(concise.status_code, 200)
        self.assertEqual(full.status_code, 200)
        combined = concise.content.decode() + full.content.decode()
        self.assertIn("Target Appliance Service", combined)
        self.assertIn("http://target.example/", combined)
        self.assertNotIn("LOWL", combined)
        self.assertIn("max-age=3600", concise["Cache-Control"])

    def test_bing_verification_is_404_unconfigured_and_xml_when_validly_configured(self) -> None:
        disabled = self.client.get("/BingSiteAuth.xml")
        with override_settings(BING_SITE_AUTH_TOKEN="TARGETTOKEN1234567890"):
            enabled = self.client.get("/BingSiteAuth.xml")
        with override_settings(BING_SITE_AUTH_TOKEN="<invalid>"):
            invalid = self.client.get("/BingSiteAuth.xml")

        self.assertEqual(disabled.status_code, 404)
        self.assertEqual(invalid.status_code, 404)
        self.assertEqual(enabled.status_code, 200)
        self.assertIn("application/xml", enabled["Content-Type"])
        self.assertIn(b"TARGETTOKEN1234567890", enabled.content)
        self.assertNotIn(b"5261D594", enabled.content)

    def test_image_sitemap_is_valid_target_host_xml(self) -> None:
        response = self.client.get("/sitemap-images.xml", HTTP_HOST="target.example")
        self.assertEqual(response.status_code, 200)
        self.assertIn("application/xml", response["Content-Type"])
        ElementTree.fromstring(response.content)
        self.assertNotIn(b"lowl", response.content.lower())


class PlatformSettingsIdentityTests(SimpleTestCase):
    def test_integration_defaults_are_disabled_target_specific_and_registered(self) -> None:
        self.assertEqual(settings.WAGTAIL_SITE_NAME, "Inland Empire Appliance Repair")
        self.assertFalse(settings.TRACKING_ENABLED)
        self.assertFalse(settings.TRACKING_WEBHOOK_ENABLED)
        self.assertFalse(settings.VAPI_ENABLED)
        self.assertFalse(settings.VAPI_ALLOW_UNSIGNED)
        self.assertEqual(settings.BING_SITE_AUTH_TOKEN, "")
        self.assertEqual(settings.TRACKING_STORAGE_KEY, "inland_tracking_sid")
        self.assertIn("tracking.apps.TrackingConfig", settings.INSTALLED_APPS)
        self.assertIn(
            "mysite.context_processors.tracking_context",
            settings.TEMPLATES[0]["OPTIONS"]["context_processors"],
        )
        self.assertEqual(settings.MIDDLEWARE[0], "mysite.middleware.RealIPMiddleware")
        self.assertIn("mysite.middleware.SEOHeadersMiddleware", settings.MIDDLEWARE)
        self.assertLess(
            settings.MIDDLEWARE.index("mysite.middleware.SEOHeadersMiddleware"),
            settings.MIDDLEWARE.index(
                "django.contrib.sessions.middleware.SessionMiddleware"
            ),
        )
        identity_text = " ".join(
            (
                settings.WAGTAIL_SITE_NAME,
                settings.CACHES["default"]["LOCATION"],
                settings.TRACKING_STORAGE_KEY,
            )
        ).lower()
        self.assertNotIn("lowl", identity_text)

    def test_absolute_site_url_helper_uses_request_origin_and_rejects_external_paths(self) -> None:
        try:
            from mysite.site_utils import absolute_site_url
        except ModuleNotFoundError as exc:  # pragma: no cover - RED guard
            self.fail(f"structured-data URL helper is unavailable: {exc}")

        request = RequestFactory().get("/", HTTP_HOST="target.example")
        self.assertEqual(
            absolute_site_url(request, "/services/"),
            "http://target.example/services/",
        )
        self.assertEqual(absolute_site_url(request, "https://attacker.example/"), "")

    def test_production_proxy_scheme_headers_require_explicit_opt_in(self) -> None:
        env = {
            "SECRET_KEY": "phase03-test-secret-key-with-at-least-fifty-characters-12345",
            "DATABASE_URL": "sqlite:////tmp/inland-phase03-settings-test.sqlite3",
            "ALLOWED_HOSTS": "target.example",
            "RAILWAY_PUBLIC_DOMAIN": "target.example",
            "REDIS_URL": "",
        }
        module_name = "mysite.settings.production"
        previous = sys.modules.pop(module_name, None)
        try:
            with patch.dict(os.environ, env, clear=True):
                module = importlib.import_module(module_name)
            self.assertIsNone(module.SECURE_PROXY_SSL_HEADER)
        finally:
            sys.modules.pop(module_name, None)
            if previous is not None:
                sys.modules[module_name] = previous
