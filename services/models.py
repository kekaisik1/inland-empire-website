"""Services app models: ServicesIndexPage and ServicePage."""

from __future__ import annotations

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page

from home import reviews as customer_reviews
from home.brand_assets import BRAND_LOGOS, get_brand_cards
from services.service_assets import get_static_service_hero_images


FEATURED_SERVICE_HUB_SLUGS = (
    "commercial-appliance-repair",
    "high-end-appliance-repair",
)
BRAND_SERVICE_SLUGS = frozenset(str(brand["slug"]) for brand in BRAND_LOGOS)


class ServicesIndexPage(Page):
    """Landing page listing all repair services."""

    intro = RichTextField(blank=True)
    hero_title = models.CharField(
        max_length=255,
        blank=True,
        default="Appliance Repair Services",
        help_text="Main heading for the services page",
    )
    hero_subtitle = models.TextField(
        blank=True,
        default="Expert repair for all major appliances. Fast, reliable, and affordable service.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("hero_subtitle"),
        FieldPanel("intro"),
    ]

    subpage_types = ["services.ServicePage"]
    parent_page_types = ["home.HomePage"]

    def get_context(self, request: object) -> dict:
        """Fetch child services and FAQ items for JSON-LD + template display."""
        import logging

        from django.utils.translation import gettext as _

        context = super().get_context(request)
        services = list(
            ServicePage.objects.child_of(self)
            .live()
            .filter(is_regional_service_page=False)
            .only(
                "id",
                "title",
                "slug",
                "url_path",
                "intro",
                "short_description",
                "featured_image",
            )
        )
        context["services"] = services

        by_slug = {page.slug: page for page in services}
        context["featured_service_hubs"] = [
            by_slug[slug] for slug in FEATURED_SERVICE_HUB_SLUGS if slug in by_slug
        ]
        context["standard_services"] = [
            page
            for page in services
            if page.slug not in FEATURED_SERVICE_HUB_SLUGS
            and page.slug not in BRAND_SERVICE_SLUGS
        ]

        # Read live diagnostic fee from SiteSettings
        fee = "70"
        try:
            from home.models import SiteSettings
            from wagtail.models import Site

            site = Site.find_for_request(request)
            biz = SiteSettings.for_site(site)
            fee = str(biz.service_call_fee)
        except Exception:
            logging.getLogger(__name__).debug(
                "SiteSettings lookup failed in ServicesIndexPage.get_context"
            )

        # FAQ items for JSON-LD FAQPage schema and template accordion
        context["faq_items"] = [
            {
                "question": _("What appliances do you repair?"),
                "answer": _(
                    "We repair refrigerators, washers, dryers, dishwashers,"
                    " ovens, stoves, ranges, microwaves, freezers, ice makers,"
                    " garbage disposals, and more — both residential and"
                    " commercial units. Our technicians are EPA 608 certified"
                    " and trained on industrial-grade equipment like walk-in"
                    " coolers and commercial ice machines, in addition to"
                    " standard household appliances."
                ),
            },
            {
                "question": _("How much does appliance repair cost?"),
                "answer": _(
                    "Our diagnostic service call is $%(fee)s, which is waived"
                    " when you approve the repair. We always provide an"
                    " itemized, upfront quote before starting work — no hidden"
                    " fees or surprise charges. You pay only after the repair"
                    " is complete."
                )
                % {"fee": fee},
            },
            {
                "question": _("Do you offer same-day appliance repair?"),
                "answer": _(
                    "Yes, we offer same-day service for most repairs. Book"
                    " before noon and a technician typically arrives that"
                    " afternoon. We operate 7 days a week, 8 AM to 8 PM,"
                    " with no overtime or weekend surcharges. Our trucks are"
                    " fully stocked with OEM parts so most repairs finish in"
                    " a single visit."
                ),
            },
            {
                "question": _("What brands do you service?"),
                "answer": _(
                    "We repair all major brands including Whirlpool, Samsung,"
                    " LG, GE, Maytag, Kenmore, Frigidaire, Bosch, KitchenAid,"
                    " Sub-Zero, Viking, Thermador, Amana, Electrolux, and"
                    " Speed Queen — plus dozens of other makes. Our technicians"
                    " are factory-trained and carry brand-specific OEM parts"
                    " for reliable, lasting repairs."
                ),
            },
            {
                "question": _("Is there a warranty on appliance repairs?"),
                "answer": _(
                    "Yes, every repair includes a warranty on both parts and"
                    " labor. If the same issue returns within the warranty"
                    " period, we come back and fix it at no additional charge."
                    " We use OEM and manufacturer-approved parts, which means"
                    " your appliance is restored to factory performance"
                    " standards."
                ),
            },
        ]
        return context


class ServicePage(Page):
    """Individual service detail page (e.g., Refrigerator Repair)."""

    date = models.DateField("Post date", auto_now_add=True)
    intro = models.CharField(max_length=250)
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Featured image for OG/social sharing and hero display",
    )
    short_description = models.CharField(
        max_length=150,
        blank=True,
        help_text="Short description for service cards (1-2 lines)",
    )
    public_h1 = models.CharField(
        max_length=255,
        blank=True,
        help_text=(
            "Optional public H1/hero heading. Leave blank to use the Wagtail "
            "page title so navigation and menus keep using the page title."
        ),
    )
    photo_carousel_title = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional heading for the service photo carousel section.",
    )
    is_regional_service_page = models.BooleanField(
        default=False,
        help_text=(
            "Marks SEO service pages created for a specific city. Regional pages "
            "are published manually and intentionally excluded from service menus."
        ),
    )
    hero_usp = models.TextField(blank=True, verbose_name="Hero USP")
    body = RichTextField(blank=True, verbose_name="Main Content")

    problems_we_fix = StreamField(
        [("problem", blocks.CharBlock(form_classname="full title"))],
        use_json_field=True,
        blank=True,
    )

    why_choose_us = StreamField(
        [
            (
                "benefit",
                blocks.StructBlock(
                    [
                        ("title", blocks.CharBlock()),
                        ("description", blocks.TextBlock()),
                    ]
                ),
            ),
        ],
        use_json_field=True,
        blank=True,
        verbose_name="Why Choose Us",
    )

    faq = StreamField(
        [
            (
                "faq_item",
                blocks.StructBlock(
                    [
                        ("question", blocks.CharBlock()),
                        ("answer", blocks.TextBlock()),
                    ]
                ),
            ),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("featured_image"),
        FieldPanel("short_description"),
        FieldPanel("public_h1"),
        FieldPanel("photo_carousel_title"),
        FieldPanel("is_regional_service_page"),
        FieldPanel("hero_usp"),
        FieldPanel("body"),
        FieldPanel("problems_we_fix"),
        FieldPanel("why_choose_us"),
        FieldPanel("faq"),
        MultiFieldPanel(
            [InlinePanel("photo_carousel_images", label="Carousel image")],
            heading="Service Photo Carousel",
        ),
        MultiFieldPanel(
            [InlinePanel("related_services", label="Related Service")],
            heading="Related Services",
        ),
    ]

    parent_page_types = ["services.ServicesIndexPage"]

    class Meta:
        indexes = [models.Index(fields=["-date"])]

    def get_context(self, request: object) -> dict:
        """Add target-owned secondary-page relationships and sourced assets."""
        context = super().get_context(request)
        context["related_services_optimized"] = list(
            self.related_services.select_related("related_service")
        )
        brand_pages = ServicePage.objects.live().filter(
            locale=self.locale,
            slug__in=BRAND_SERVICE_SLUGS,
        )
        context["brand_cards"] = get_brand_cards(
            {page.slug: page for page in brand_pages}
        )
        service_hero_slug = str(self.slug)
        if self.is_regional_service_page:
            from home.regional_service_seed_data import get_regional_base_service_slug

            service_hero_slug = (
                get_regional_base_service_slug(service_hero_slug) or service_hero_slug
            )
        context["service_hero_slug"] = service_hero_slug
        context["static_service_hero_images"] = get_static_service_hero_images(service_hero_slug)
        context["review_items"] = customer_reviews.get_customer_review_items()

        from blog.models import BlogPage
        from locations.models import CityPage

        context["service_area_switcher_cities"] = list(
            CityPage.objects.live()
            .filter(locale=self.locale)
            .order_by("title")
            .only("id", "title", "slug", "url_path", "state")[:12]
        )
        context["latest_blog_posts"] = list(
            BlogPage.objects.live()
            .filter(locale=self.locale)
            .order_by("-date")
            .only("id", "title", "slug", "url_path", "date", "intro")[:6]
        )
        context["appliance_service_pages"] = list(
            ServicePage.objects.live()
            .filter(locale=self.locale, is_regional_service_page=False)
            .exclude(pk=self.pk)
            .exclude(slug__in=FEATURED_SERVICE_HUB_SLUGS)
            .exclude(slug__in=BRAND_SERVICE_SLUGS)
            .order_by("title")
            .only("id", "title", "slug", "url_path")[:12]
        )
        return context


class ServicePhotoCarouselImage(Orderable):
    """Ordered image-only carousel item for one service page."""

    page = ParentalKey(ServicePage, related_name="photo_carousel_images")
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        related_name="+",
    )

    panels = [FieldPanel("image")]


class ServiceRelatedService(Orderable):
    """Links to related services for internal linking."""

    page = ParentalKey(ServicePage, related_name="related_services")
    related_service = models.ForeignKey(
        "services.ServicePage",
        on_delete=models.CASCADE,
        related_name="+",
    )

    panels = [FieldPanel("related_service")]
