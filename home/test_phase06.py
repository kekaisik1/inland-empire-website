"""Focused Phase 06 contracts for secondary public page families."""

from __future__ import annotations

import json
import re
from datetime import date
from io import BytesIO
from unittest.mock import patch

from django.core.files.base import ContentFile
from django.test import override_settings
from PIL import Image as PILImage
from wagtail.images import get_image_model
from wagtail.models import Locale
from wagtail.test.utils import WagtailPageTestCase

from blog.models import BlogIndexPage, BlogPage
from home.models import SiteSettings
from home.tests import create_test_home
from locations.models import CityPage, LocationsIndexPage
from pages.models import StaticPage
from services.models import ServicePage, ServicePhotoCarouselImage, ServicesIndexPage


def _jsonld_of_type(content: str, schema_type: str) -> list[dict[str, object]]:
    scripts = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>',
        content,
        re.DOTALL,
    )
    return [
        payload
        for script in scripts
        if isinstance((payload := json.loads(script)), dict)
        and payload.get("@type") == schema_type
    ]


class Phase06SecondaryPageRenderTests(WagtailPageTestCase):
    """Portable page-family behavior must use the inherited Inland shell."""

    def setUp(self) -> None:
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
            google_review_count=0,
        )

        self.services_index = ServicesIndexPage(
            title="Services",
            slug="services",
            hero_title="Repair services",
            hero_subtitle="Target-owned service choices.",
        )
        self.home.add_child(instance=self.services_index)
        self.services_index.save_revision().publish()

        self.service = self._service(
            "Refrigerator Repair",
            "refrigerator-repair",
            "Cooling diagnostics and repair.",
        )
        self.commercial = self._service(
            "Commercial Appliance Repair",
            "commercial-appliance-repair",
            "Business appliance diagnostics.",
        )
        self.high_end = self._service(
            "High End Appliance Repair",
            "high-end-appliance-repair",
            "Premium appliance diagnostics.",
        )
        self.brand = self._service(
            "Whirlpool Appliance Repair",
            "whirlpool-appliance-repair",
            "Whirlpool appliance diagnostics.",
        )

        self.locations_index = LocationsIndexPage(
            title="Service Areas",
            slug="service-areas",
            intro="Target service areas.",
        )
        self.home.add_child(instance=self.locations_index)
        self.locations_index.save_revision().publish()
        self.city = CityPage(
            title="Corona",
            slug="appliance-repair-corona-ca",
            intro="Appliance repair options in Corona.",
            public_h1="Corona Appliance Repair",
            zip_codes="92879, 92880",
            body="<h2>Local repair planning</h2><p>Service details for Corona homes.</p>",
        )
        self.locations_index.add_child(instance=self.city)
        self.city.save_revision().publish()

        self.blog_index = BlogIndexPage(
            title="Blog",
            slug="blog",
            hero_title="Repair notebook",
            hero_subtitle="Practical appliance care notes.",
        )
        self.home.add_child(instance=self.blog_index)
        self.blog_index.save_revision().publish()
        self.post = BlogPage(
            title="Refrigerator Care Guide",
            slug="refrigerator-care-guide",
            date=date(2026, 8, 2),
            intro="A practical refrigerator care guide.",
            author_name="Inland Service Desk",
            body=[
                ("heading", "Check the airflow"),
                ("paragraph", "<p>Keep vents clear and inspect the door seal.</p>"),
                ("heading", "Listen for changes"),
                ("paragraph", "<p>Document new sounds before scheduling service.</p>"),
                ("heading", "Prepare for a visit"),
                ("paragraph", "<p>Clear a safe path around the appliance.</p>"),
            ],
        )
        self.blog_index.add_child(instance=self.post)
        self.post.save_revision().publish()
        self.post.tags.add("refrigerator")
        self.related_post = BlogPage(
            title="Refrigerator Temperature Notes",
            slug="refrigerator-temperature-notes",
            date=date(2026, 8, 1),
            intro="How to record temperature changes.",
        )
        self.blog_index.add_child(instance=self.related_post)
        self.related_post.save_revision().publish()
        self.related_post.tags.add("refrigerator")

        self.contact = StaticPage(
            title="Contact",
            slug="contact",
            hero_title="Contact the service desk",
            hero_subtitle="Tell us what the appliance is doing.",
            body="<p>We will review your service request.</p>",
        )
        self.home.add_child(instance=self.contact)
        self.contact.save_revision().publish()

    def _service(self, title: str, slug: str, intro: str) -> ServicePage:
        page = ServicePage(
            title=title,
            slug=slug,
            intro=intro,
            short_description=intro,
        )
        self.services_index.add_child(instance=page)
        page.save_revision().publish()
        return page

    def _carousel_image(self, title: str, color: tuple[int, int, int], order: int) -> None:
        image_file = BytesIO()
        PILImage.new("RGB", (800, 600), color).save(image_file, format="PNG")
        image = get_image_model().objects.create(
            title=title,
            file=ContentFile(image_file.getvalue(), name=f"phase06-{order}.png"),
        )
        ServicePhotoCarouselImage.objects.create(
            page=self.service,
            image=image,
            sort_order=order,
        )

    def test_services_index_separates_featured_hubs_from_standard_cards(self) -> None:
        response = self.client.get(self.services_index.url)
        content = response.content.decode()

        self.assertEqual(
            [page.slug for page in response.context["featured_service_hubs"]],
            ["commercial-appliance-repair", "high-end-appliance-repair"],
        )
        standard = [page.slug for page in response.context["standard_services"]]
        self.assertIn("refrigerator-repair", standard)
        self.assertNotIn("whirlpool-appliance-repair", standard)
        self.assertIn('data-featured-service-hubs', content)
        self.assertIn('data-featured-service-hub="high-end-appliance-repair"', content)
        self.assertIn('data-standard-service-card="refrigerator-repair"', content)
        self.assertLess(
            content.index("data-featured-service-hubs"),
            content.index("data-standard-services-grid"),
        )
        self.assertIn("bg-background", content)
        self.assertNotIn("#1545ad", content.lower())

    def test_service_detail_uses_public_h1_responsive_hero_and_related_context(self) -> None:
        self.service.public_h1 = "Emergency Refrigerator Repair"
        self.service.seo_title = "Target Refrigerator SEO Title"
        self.service.search_description = "Target-owned refrigerator metadata."
        self.service.faq = [
            (
                "faq_item",
                {"question": "What should I note?", "answer": "Record the model and symptoms."},
            )
        ]
        self.service.save_revision().publish()

        response = self.client.get(self.service.url)
        content = response.content.decode()

        self.assertContains(response, "<title>Target Refrigerator SEO Title</title>", html=True)
        self.assertIn(">Emergency Refrigerator Repair</h1>", content)
        self.assertIn("service-hero-refrigerator-repair-768.webp", content)
        self.assertIn('data-service-brand-grid', content)
        self.assertIn('data-service-area-switcher', content)
        self.assertIn('data-service-blog-slider', content)
        self.assertEqual(response.context["review_items"], [])
        self.assertNotIn('data-service-review-card', content)
        self.assertGreater(len(response.context["brand_cards"]), 0)
        self.assertGreater(len(response.context["service_area_switcher_cities"]), 0)
        self.assertGreater(len(response.context["latest_blog_posts"]), 0)
        self.assertEqual(len(_jsonld_of_type(content, "Service")), 1)
        self.assertEqual(len(_jsonld_of_type(content, "FAQPage")), 1)

    def test_service_carousel_has_ordered_images_controls_keyboard_and_status_contract(self) -> None:
        self.service.photo_carousel_title = "Recent refrigerator repair photos"
        self.service.save_revision().publish()
        self._carousel_image("Compressor inspection", (20, 80, 140), 0)
        self._carousel_image("Door seal inspection", (140, 80, 20), 1)

        content = self.client.get(self.service.url).content.decode()

        self.assertIn('x-data="serviceCarousel"', content)
        self.assertIn('data-service-carousel-prev', content)
        self.assertIn('data-service-carousel-next', content)
        self.assertIn('data-service-carousel-status', content)
        self.assertIn('data-service-photo-carousel-track', content)
        self.assertIn('tabindex="0"', content)
        self.assertIn('@keydown="onKeydown"', content)
        self.assertIn('@pointerdown="pointerDown"', content)
        self.assertIn('@pointerup="pointerUp"', content)
        first = content.index('alt="Compressor inspection"')
        second = content.index('alt="Door seal inspection"')
        self.assertLess(first, second)

    def test_city_detail_uses_public_h1_static_picture_and_local_related_articles(self) -> None:
        response = self.client.get(self.city.url)
        content = response.content.decode()

        self.assertIn(">Corona Appliance Repair</h1>", content)
        self.assertIn(
            "images/service-areas/appliance-repair-corona-ca-hero-768.webp",
            content,
        )
        self.assertIn('data-city-service-body', content)
        self.assertIn('data-city-blog-slider', content)
        self.assertIn("Refrigerator Care Guide", content)
        self.assertNotIn("www.google.com/maps", content)
        self.assertEqual(response.context["static_city_hero_images"]["webp_768"], "images/service-areas/appliance-repair-corona-ca-hero-768.webp")
        self.assertGreater(len(response.context["latest_blog_posts"]), 0)
        self.assertEqual(len(_jsonld_of_type(content, "Service")), 1)
        self.assertEqual(len(_jsonld_of_type(content, "FAQPage")), 1)

    def test_city_hero_supporting_copy_uses_accessible_muted_text_contrast(self) -> None:
        self.city.hero_usp = "Target-owned supporting service-area copy."
        self.city.save_revision().publish()

        content = self.client.get(self.city.url).content.decode()

        self.assertNotIn("text-text-muted/60", content)
        self.assertIn(
            '<p class="text-text-muted mt-2 font-sans">Target-owned supporting service-area copy.</p>',
            content,
        )

    def test_blog_index_features_latest_post_with_reading_metadata_and_tags(self) -> None:
        content = self.client.get(self.blog_index.url).content.decode()

        self.assertIn('data-blog-featured-post', content)
        self.assertIn("Refrigerator Care Guide", content)
        self.assertIn("min read", content)
        self.assertIn("refrigerator", content)
        self.assertIn('data-blog-post-card', content)
        self.assertIn("bg-background", content)
        self.assertNotIn("#1545ad", content.lower())

    def test_blog_detail_renders_heading_anchors_toc_reading_time_and_related_posts(self) -> None:
        self.post.tags.add("refrigerator")
        self.post.save_revision().publish()
        self.related_post.tags.add("refrigerator")
        self.related_post.save_revision().publish()
        response = self.client.get(self.post.url)
        content = response.content.decode()

        self.assertIn('x-data="readingProgress"', content)
        self.assertIn('x-data="blogToc"', content)
        self.assertIn('data-blog-article', content)
        self.assertIn('id="check-the-airflow"', content)
        self.assertIn('href="#check-the-airflow"', content)
        self.assertIn("In This Article", content)
        self.assertIn("min read", content)
        self.assertIn("Inland Service Desk", content)
        self.assertIn("Refrigerator Temperature Notes", content)
        page_context = self.post.get_context(response.wsgi_request)
        related_ids = {post.pk for post in page_context["related_posts"]}
        recent_ids = {post.pk for post in page_context["recent_posts"]}
        self.assertTrue(related_ids.isdisjoint(recent_ids))
        self.assertEqual(len(_jsonld_of_type(content, "BlogPosting")), 1)

    def test_contact_form_exposes_locale_safe_action_validation_and_attribution_hook(self) -> None:
        content = self.client.get(self.contact.url).content.decode()

        self.assertIn('action="/contact/submit/"', content)
        self.assertIn('data-contact-form', content)
        self.assertIn('x-data="contactForm"', content)
        self.assertIn('maxlength="100"', content)
        self.assertIn('maxlength="20"', content)
        self.assertIn('maxlength="5000"', content)
        self.assertIn('aria-live="polite"', content)
        self.assertIn("js/utm.js", content)
        self.assertEqual(len(_jsonld_of_type(content, "ContactPage")), 1)

    @override_settings(SEARCH_RESULTS_PER_PAGE=1)
    def test_search_accepts_q_alias_paginates_and_emits_locale_aware_metadata(self) -> None:
        first = self.client.get("/search/?q=Repair&page=1")
        content = first.content.decode()

        self.assertEqual(first.status_code, 200)
        self.assertEqual(first.context["search_query"], "Repair")
        self.assertContains(first, "Showing results for")
        self.assertContains(first, "Next")
        self.assertIn('<meta name="robots" content="noindex, follow" />', content)
        self.assertIn('<link rel="canonical" href="http://testserver/search/" />', content)
        self.assertIn('hreflang="es"', content)
        self.assertIn('name="q"', content)
        self.assertNotIn('name="query"', content)

    def test_spanish_secondary_translation_keeps_equivalent_route_and_hreflang(self) -> None:
        es_locale, _ = Locale.objects.get_or_create(language_code="es")
        es_home = self.home.copy_for_translation(es_locale)
        es_home.save_revision().publish()
        es_index = self.services_index.copy_for_translation(es_locale).specific
        es_index.hero_title = "Servicios de reparación"
        es_index.save_revision().publish()
        es_service = self.service.copy_for_translation(es_locale).specific
        es_service.title = "Reparación de Refrigeradores"
        es_service.public_h1 = "Reparación de Refrigeradores en Corona"
        es_service.intro = "Diagnóstico de refrigeradores en Corona."
        es_service.save_revision().publish()

        response = self.client.get(es_service.get_url())
        content = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn('lang="es"', content)
        self.assertIn("Reparación de Refrigeradores en Corona", content)
        self.assertIn('<link rel="alternate" hreflang="en"', content)
        self.assertIn('<link rel="alternate" hreflang="es"', content)
        self.assertIn('<link rel="canonical" href="http://testserver/es/services/refrigerator-repair/"', content)
        self.assertIn('href="/es/contact/"', content)

    @patch("home.reviews.get_customer_review_items")
    def test_service_reviews_render_only_when_target_owned_evidence_is_supplied(self, reviews) -> None:
        reviews.return_value = [
            {
                "author": "Target Customer",
                "date": "Aug 2026",
                "date_published": "2026-08-01",
                "rating": 5,
                "source": "Target-owned source",
                "source_url": "https://reviews.inland.test/review/phase06",
                "text": "A target-owned service review fixture.",
            }
        ]

        content = self.client.get(self.service.url).content.decode()

        self.assertIn('data-service-review-card', content)
        self.assertIn('href="https://reviews.inland.test/review/phase06"', content)
        self.assertIn("Target Customer", content)
        self.assertIn("A target-owned service review fixture.", content)
