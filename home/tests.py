"""Tests for homepage, SiteSettings, SEO tags, and core functionality."""

from __future__ import annotations


from django.test import TestCase, override_settings
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from home.models import HomePage, SiteSettings


def create_test_home() -> tuple[HomePage, Site]:
    """Create a test HomePage and Site, removing Wagtail's default page."""
    root = Page.objects.get(depth=1)
    # Remove any existing child pages (Wagtail Welcome page)
    Page.objects.filter(depth__gt=1).delete()
    Page.fix_tree()
    root.refresh_from_db()

    home = HomePage(title="Home", slug="home")
    root.add_child(instance=home)
    home.save_revision().publish()

    Site.objects.all().delete()
    site = Site.objects.create(
        hostname="testserver",
        root_page=home,
        is_default_site=True,
    )
    return home, site


class HomePageModelTest(WagtailPageTestCase):
    """Test HomePage model behavior and page tree constraints."""

    def setUp(self) -> None:
        self.home, self.site = create_test_home()

    def test_home_page_renders_200(self) -> None:
        response = self.client.get(self.home.url)
        self.assertEqual(response.status_code, 200)

    def test_home_page_max_count(self) -> None:
        self.assertEqual(HomePage.max_count, 1)

    def test_home_page_context_contains_services(self) -> None:
        response = self.client.get(self.home.url)
        self.assertIn("services", response.context)

    def test_home_page_context_contains_faq_items(self) -> None:
        response = self.client.get(self.home.url)
        self.assertIn("faq_items", response.context)
        self.assertGreater(len(response.context["faq_items"]), 0)

    def test_home_page_context_contains_review_items(self) -> None:
        response = self.client.get(self.home.url)
        self.assertIn("review_items", response.context)
        self.assertEqual(len(response.context["review_items"]), 3)


class SiteSettingsTest(TestCase):
    """Test SiteSettings model and properties."""

    def setUp(self) -> None:
        self.home, self.site = create_test_home()
        self.settings = SiteSettings.objects.create(
            site=self.site,
            business_name="Test Biz",
            phone="+15551234567",
            phone_display="(555) 123-4567",
            email="test@example.com",
            address_line1="123 Main St",
            address_line2="",
            city="TestCity",
            state="CA",
            zip_code="90210",
            booking_url="https://booking.example.com",
            warranty_text="Warranty Included",
            service_call_fee=70,
            labor_rate_min=120,
        )

    def test_full_address_format(self) -> None:
        expected = "123 Main St, TestCity, CA 90210"
        self.assertEqual(self.settings.full_address, expected)

    def test_full_address_with_line2(self) -> None:
        self.settings.address_line2 = "Suite 100"
        self.settings.save()
        self.assertIn("Suite 100", self.settings.full_address)

    def test_str_returns_business_name(self) -> None:
        self.assertEqual(str(self.settings), "Test Biz")


class SeoTagsTest(TestCase):
    """Test custom SEO template tags."""

    def test_split_comma_filter(self) -> None:
        from home.templatetags.seo_tags import split_comma

        result = split_comma("90210, 90211, 90212")
        self.assertEqual(result, ["90210", "90211", "90212"])

    def test_split_comma_empty(self) -> None:
        from home.templatetags.seo_tags import split_comma

        self.assertEqual(split_comma(""), [])

    def test_split_comma_single(self) -> None:
        from home.templatetags.seo_tags import split_comma

        self.assertEqual(split_comma("90210"), ["90210"])


class SeoJsonLdTest(TestCase):
    """Test JSON-LD structured data output on rendered pages."""

    def setUp(self) -> None:
        self.home, self.site = create_test_home()
        self.biz = SiteSettings.objects.create(
            site=self.site,
            business_name="Test Biz",
            phone="+15551234567",
            email="test@example.com",
            city="TestCity",
            state="CA",
            zip_code="90210",
            google_rating=4.8,
            google_review_count=100,
            latitude=33.668,
            longitude=-117.327,
        )

    def test_homepage_contains_website_schema(self) -> None:
        response = self.client.get(self.home.url)
        content = response.content.decode()
        self.assertIn('"@type":"WebSite"', content)
        self.assertIn("SearchAction", content)

    def test_homepage_contains_local_business_schema(self) -> None:
        response = self.client.get(self.home.url)
        content = response.content.decode()
        self.assertIn("LocalBusiness", content)
        self.assertIn('"Test Biz"', content)

    def test_local_business_has_geo(self) -> None:
        response = self.client.get(self.home.url)
        content = response.content.decode()
        self.assertIn('"@type":"GeoCoordinates"', content)
        self.assertIn("33.668", content)

    def test_local_business_has_configurable_rating(self) -> None:
        response = self.client.get(self.home.url)
        content = response.content.decode()
        self.assertIn('"ratingValue":"4.8"', content)
        self.assertIn('"reviewCount":"100"', content)

    def test_homepage_contains_breadcrumbs(self) -> None:
        response = self.client.get(self.home.url)
        content = response.content.decode()
        self.assertIn('"@type":"BreadcrumbList"', content)

    def test_homepage_contains_faq_schema(self) -> None:
        response = self.client.get(self.home.url)
        content = response.content.decode()
        self.assertIn('"@type":"FAQPage"', content)

    def test_homepage_contains_organization_schema(self) -> None:
        response = self.client.get(self.home.url)
        content = response.content.decode()
        self.assertIn('"@type":"Organization"', content)
        self.assertIn("#organization", content)

    def test_homepage_contains_howto_schema(self) -> None:
        response = self.client.get(self.home.url)
        content = response.content.decode()
        self.assertIn('"@type":"HowTo"', content)
        self.assertIn('"@type":"HowToStep"', content)

    def test_meta_description_fallback(self) -> None:
        response = self.client.get(self.home.url)
        content = response.content.decode()
        # Should have a description meta tag even without search_description
        self.assertIn('<meta name="description"', content)

    def test_og_locale_format(self) -> None:
        response = self.client.get(self.home.url)
        content = response.content.decode()
        self.assertIn('content="en_US"', content)

    def test_favicon_links_present(self) -> None:
        response = self.client.get(self.home.url)
        content = response.content.decode()
        self.assertIn("favicon.ico", content)
        self.assertIn("apple-touch-icon", content)


class TranslationUrlTagTest(TestCase):
    """Test the translation_url template tag."""

    def test_returns_fallback_when_page_is_none(self) -> None:
        from home.templatetags.i18n_helpers import translation_url

        self.assertEqual(translation_url(None, "es", "/es/"), "/es/")
        self.assertEqual(translation_url(None, "en", "/"), "/")

    def test_returns_fallback_for_page_without_translation(self) -> None:
        from home.templatetags.i18n_helpers import translation_url

        home, _ = create_test_home()
        self.assertEqual(translation_url(home, "es", "/es/"), "/es/")

    def test_returns_translation_url_when_available(self) -> None:
        from home.templatetags.i18n_helpers import translation_url
        from wagtail.models import Locale

        home, _ = create_test_home()
        es_locale, _ = Locale.objects.get_or_create(language_code="es")
        es_home = home.copy_for_translation(es_locale)
        es_home.save_revision().publish()
        result = translation_url(home, "es", "/es/")
        self.assertEqual(result, es_home.get_url())


class HealthCheckTest(TestCase):
    """Test health check endpoint."""

    def test_health_check_returns_ok(self) -> None:
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})


class ContextProcessorTest(TestCase):
    """Test context processors: navigation_data and site_settings_context."""

    def setUp(self) -> None:
        self.home, self.site = create_test_home()
        self.biz = SiteSettings.objects.create(
            site=self.site,
            business_name="Test Biz",
            phone="+15551234567",
            city="TestCity",
            state="CA",
        )

    def test_navigation_data_in_response_context(self) -> None:
        response = self.client.get(self.home.url)
        self.assertIn("global_services", response.context)
        self.assertIn("global_cities", response.context)

    def test_navigation_data_is_list(self) -> None:
        response = self.client.get(self.home.url)
        self.assertIsInstance(response.context["global_services"], list)
        self.assertIsInstance(response.context["global_cities"], list)

    def test_site_settings_available_in_context(self) -> None:
        response = self.client.get(self.home.url)
        self.assertIn("biz", response.context)
        self.assertIn("booking_url", response.context)
        self.assertEqual(response.context["biz"].business_name, "Test Biz")

    def test_site_settings_recreated_when_deleted(self) -> None:
        """Wagtail's for_site() auto-creates SiteSettings if none exists.

        Deleting all SiteSettings and requesting a page should still provide
        a biz object (auto-created with model defaults), never None.
        """
        SiteSettings.objects.all().delete()
        response = self.client.get(self.home.url)
        biz = response.context["biz"]
        self.assertIsNotNone(biz)
        # Auto-created instance has the model field default
        self.assertEqual(biz.business_name, "LOWL Appliance Repair")

    @override_settings(
        CACHES={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
    )
    def test_navigation_data_is_cached(self) -> None:
        """Second request should use cached navigation data."""
        from django.core.cache import cache

        cache.clear()
        # First request populates cache
        self.client.get(self.home.url)
        # Cache keys should now exist
        cached = cache.get("lowl:nav:services:en")
        self.assertIsNotNone(cached)


class PaginationEdgeCaseTest(TestCase):
    """Test pagination edge cases in blog and search views."""

    def setUp(self) -> None:
        self.home, self.site = create_test_home()

    def test_blog_page_zero_returns_page_1(self) -> None:
        from blog.models import BlogIndexPage

        blog_index = BlogIndexPage(
            title="Blog", slug="blog", hero_title="Blog", hero_subtitle="Test"
        )
        self.home.add_child(instance=blog_index)
        blog_index.save_revision().publish()

        response = self.client.get(f"{blog_index.url}?page=0")
        self.assertEqual(response.status_code, 200)

    def test_blog_negative_page_returns_page_1(self) -> None:
        from blog.models import BlogIndexPage

        blog_index = BlogIndexPage(
            title="Blog", slug="blog", hero_title="Blog", hero_subtitle="Test"
        )
        self.home.add_child(instance=blog_index)
        blog_index.save_revision().publish()

        response = self.client.get(f"{blog_index.url}?page=-1")
        self.assertEqual(response.status_code, 200)

    def test_blog_non_numeric_page_returns_page_1(self) -> None:
        from blog.models import BlogIndexPage

        blog_index = BlogIndexPage(
            title="Blog", slug="blog", hero_title="Blog", hero_subtitle="Test"
        )
        self.home.add_child(instance=blog_index)
        blog_index.save_revision().publish()

        response = self.client.get(f"{blog_index.url}?page=abc")
        self.assertEqual(response.status_code, 200)

    def test_blog_huge_page_returns_last_page(self) -> None:
        from blog.models import BlogIndexPage

        blog_index = BlogIndexPage(
            title="Blog", slug="blog", hero_title="Blog", hero_subtitle="Test"
        )
        self.home.add_child(instance=blog_index)
        blog_index.save_revision().publish()

        response = self.client.get(f"{blog_index.url}?page=999999")
        self.assertEqual(response.status_code, 200)

    def test_search_negative_page_returns_200(self) -> None:
        response = self.client.get("/search/?query=test&page=-1")
        self.assertEqual(response.status_code, 200)

    def test_search_non_numeric_page_returns_200(self) -> None:
        response = self.client.get("/search/?query=test&page=abc")
        self.assertEqual(response.status_code, 200)

    def test_search_huge_page_returns_200(self) -> None:
        response = self.client.get("/search/?query=test&page=999999")
        self.assertEqual(response.status_code, 200)

    def test_search_empty_query_returns_200(self) -> None:
        response = self.client.get("/search/?query=")
        self.assertEqual(response.status_code, 200)


class RobotsAndSitemapTest(TestCase):
    """Test robots.txt and sitemap endpoints."""

    def setUp(self) -> None:
        create_test_home()

    def test_robots_txt_returns_200(self) -> None:
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/plain", response["Content-Type"])

    def test_robots_txt_blocks_ai_bots(self) -> None:
        response = self.client.get("/robots.txt")
        content = response.content.decode()
        self.assertIn("GPTBot", content)
        self.assertIn("ClaudeBot", content)

    def test_robots_txt_contains_sitemap(self) -> None:
        response = self.client.get("/robots.txt")
        content = response.content.decode()
        self.assertIn("Sitemap:", content)
        self.assertIn("sitemap.xml", content)

    def test_sitemap_returns_200(self) -> None:
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)

    def test_image_sitemap_returns_200(self) -> None:
        response = self.client.get("/sitemap-images.xml")
        self.assertEqual(response.status_code, 200)
        self.assertIn("application/xml", response["Content-Type"])


@override_settings(
    MIDDLEWARE=[
        "django.middleware.security.SecurityMiddleware",
        "django.middleware.gzip.GZipMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.locale.LocaleMiddleware",
        "django.middleware.common.CommonMiddleware",
        "mysite.middleware.SEOHeadersMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    ]
)
class MiddlewareSecurityHeadersTest(TestCase):
    """Test SEO and security headers from middleware (requires SEOHeadersMiddleware)."""

    def setUp(self) -> None:
        create_test_home()

    def test_permissions_policy_header(self) -> None:
        response = self.client.get("/")
        self.assertIn("Permissions-Policy", response)
        self.assertIn("camera=()", response["Permissions-Policy"])

    def test_csp_header_present(self) -> None:
        response = self.client.get("/")
        self.assertIn("Content-Security-Policy", response)

    def test_csp_no_unsafe_eval(self) -> None:
        """CSP should not contain unsafe-eval after the Alpine.js CSP build switch."""
        response = self.client.get("/")
        csp = response.get("Content-Security-Policy", "")
        self.assertNotIn("unsafe-eval", csp)

    def test_x_robots_tag_on_public_pages(self) -> None:
        response = self.client.get("/")
        self.assertIn("X-Robots-Tag", response)
        self.assertIn("index, follow", response["X-Robots-Tag"])

    def test_vary_accept_language(self) -> None:
        response = self.client.get("/")
        self.assertIn("Accept-Language", response.get("Vary", ""))

    def test_link_preconnect_header(self) -> None:
        response = self.client.get("/")
        self.assertIn("Link", response)
        self.assertIn("preconnect", response["Link"])


class ContactFormRateLimitTest(TestCase):
    """Test contact form rate limiting."""

    def setUp(self) -> None:
        create_test_home()

    def test_contact_get_redirects(self) -> None:
        """GET request to contact_submit should redirect."""
        response = self.client.get("/contact/submit/")
        self.assertEqual(response.status_code, 302)

    def test_contact_post_without_data_redirects(self) -> None:
        """POST without valid form data should redirect with error."""
        response = self.client.post("/contact/submit/", {})
        self.assertEqual(response.status_code, 302)


class JsonLdEscapingTest(TestCase):
    """Test JSON-LD output escapes dangerous characters to prevent XSS."""

    def test_jsonld_escapes_script_tags(self) -> None:
        from home.templatetags.seo_tags import _jsonld_script

        data = {"name": '</script><script>alert("xss")</script>'}
        result = _jsonld_script(data)
        self.assertNotIn("</script><script>", result)
        self.assertIn("\\u003C", result)
        self.assertIn("\\u003E", result)

    def test_jsonld_escapes_ampersand(self) -> None:
        from home.templatetags.seo_tags import _jsonld_script

        data = {"name": "A & B"}
        result = _jsonld_script(data)
        self.assertIn("\\u0026", result)
        self.assertNotIn("& ", result)

    def test_jsonld_preserves_valid_content(self) -> None:
        from home.templatetags.seo_tags import _jsonld_script

        data = {"@type": "LocalBusiness", "name": "Test Biz", "rating": "4.9"}
        result = _jsonld_script(data)
        self.assertIn("LocalBusiness", result)
        self.assertIn("Test Biz", result)
        self.assertIn('type="application/ld+json"', result)


class ContactFormEmailTest(TestCase):
    """Test contact form email sending and UTM capture."""

    def setUp(self) -> None:
        create_test_home()

    @override_settings(
        DEFAULT_FROM_EMAIL="noreply@test.com",
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    )
    def test_contact_form_sends_email(self) -> None:
        from django.core import mail

        import os

        with self.settings(DEFAULT_FROM_EMAIL="noreply@test.com"):
            os.environ["CONTACT_EMAIL"] = "biz@test.com"
            try:
                self.client.post(
                    "/contact/submit/",
                    {
                        "name": "Test User",
                        "email": "user@example.com",
                        "phone": "555-1234",
                        "message": "Need help with my fridge",
                    },
                )
                self.assertEqual(len(mail.outbox), 1)
                self.assertIn("Test User", mail.outbox[0].subject)
                self.assertIn("Need help with my fridge", mail.outbox[0].body)
                self.assertIn("user@example.com", mail.outbox[0].body)
            finally:
                os.environ.pop("CONTACT_EMAIL", None)

    @override_settings(
        DEFAULT_FROM_EMAIL="noreply@test.com",
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    )
    def test_contact_form_captures_utm_data(self) -> None:
        from django.core import mail

        import os

        os.environ["CONTACT_EMAIL"] = "biz@test.com"
        try:
            self.client.post(
                "/contact/submit/",
                {
                    "name": "Test User",
                    "email": "user@example.com",
                    "message": "Test",
                    "utm_source": "google",
                    "utm_campaign": "spring_promo",
                },
            )
            self.assertEqual(len(mail.outbox), 1)
            self.assertIn("utm_source: google", mail.outbox[0].body)
            self.assertIn("utm_campaign: spring_promo", mail.outbox[0].body)
        finally:
            os.environ.pop("CONTACT_EMAIL", None)

    def test_contact_form_invalid_data_redirects_with_302(self) -> None:
        response = self.client.post(
            "/contact/submit/",
            {"name": "", "email": "not-an-email", "message": ""},
        )
        self.assertEqual(response.status_code, 302)

    def test_contact_redirect_preserves_locale(self) -> None:
        """GET to /es/contact/submit/ should redirect to /es/contact/ not /contact/."""
        response = self.client.get("/es/contact/submit/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/es/contact/")
