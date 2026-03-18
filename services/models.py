"""Services app models: ServicesIndexPage and ServicePage."""

from __future__ import annotations

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page


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
        context["services"] = (
            ServicePage.objects.child_of(self)
            .live()
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
        FieldPanel("hero_usp"),
        FieldPanel("body"),
        FieldPanel("problems_we_fix"),
        FieldPanel("why_choose_us"),
        FieldPanel("faq"),
        MultiFieldPanel(
            [InlinePanel("related_services", label="Related Service")],
            heading="Related Services",
        ),
    ]

    parent_page_types = ["services.ServicesIndexPage"]

    class Meta:
        indexes = [models.Index(fields=["-date"])]

    def get_context(self, request: object) -> dict:
        """Prefetch related services to avoid N+1 queries."""
        context = super().get_context(request)
        context["related_services_optimized"] = list(
            self.related_services.select_related("related_service")
        )
        return context


class ServiceRelatedService(Orderable):
    """Links to related services for internal linking."""

    page = ParentalKey(ServicePage, related_name="related_services")
    related_service = models.ForeignKey(
        "services.ServicePage",
        on_delete=models.CASCADE,
        related_name="+",
    )

    panels = [FieldPanel("related_service")]
