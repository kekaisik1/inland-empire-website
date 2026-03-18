"""Locations app models: LocationsIndexPage and CityPage."""

from __future__ import annotations

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page


class LocationsIndexPage(Page):
    """Landing page listing all service areas/cities."""

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro")]
    subpage_types = ["locations.CityPage"]

    def get_context(self, request: object) -> dict:
        """Fetch child cities and FAQ items for JSON-LD + template display."""
        from django.utils.translation import gettext as _

        context = super().get_context(request)
        context["cities"] = (
            CityPage.objects.child_of(self)
            .live()
            .order_by("title")
            .only("id", "title", "slug", "url_path", "intro", "state")
        )

        # FAQ items for JSON-LD FAQPage schema and template accordion
        context["faq_items"] = [
            {
                "question": _("What areas do you serve?"),
                "answer": _(
                    "We serve 10 cities across Riverside County and the"
                    " Inland Empire, including Lake Elsinore, Murrieta,"
                    " Temecula, Menifee, Corona, Riverside, Beaumont,"
                    " Perris, Canyon Lake, and Norco. Our service area"
                    " covers over 140 ZIP codes. Select a city above to"
                    " see the specific ZIP codes we cover in that area."
                ),
            },
            {
                "question": _("How do I know if you service my area?"),
                "answer": _(
                    "Enter your ZIP code on our booking page to instantly"
                    " confirm coverage. We service over 140 ZIP codes"
                    " across Riverside County. If your ZIP code is not"
                    " listed, call us directly — we are expanding"
                    " regularly and can often make arrangements for"
                    " nearby areas."
                ),
            },
            {
                "question": _("Do you charge extra for travel to distant locations?"),
                "answer": _(
                    "No. We charge the same flat-rate diagnostic fee and"
                    " repair rates across all service areas — no travel"
                    " fees, no mileage surcharges. Our technicians are"
                    " based locally in the Inland Empire, so driving"
                    " distances are short and we can reach most locations"
                    " within the hour."
                ),
            },
            {
                "question": _("Can I get same-day service in my city?"),
                "answer": _(
                    "Yes, we offer same-day service across all our service"
                    " areas. Our technicians are based throughout Riverside"
                    " County and operate 7 days a week, 8 AM to 8 PM. Book"
                    " before noon and a technician typically arrives that"
                    " same afternoon — no overtime or weekend surcharges."
                ),
            },
        ]
        return context


class CityPage(Page):
    """Individual city/service-area page."""

    intro = models.CharField(max_length=250)
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Featured image for OG/social sharing (1200x630 recommended)",
    )
    hero_usp = models.TextField(blank=True, verbose_name="Hero USP")
    body = RichTextField(blank=True)
    about_techs = RichTextField(blank=True, verbose_name="About Technicians")
    zip_codes = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated list of zip codes",
    )
    state = models.CharField(
        max_length=2, default="CA", verbose_name="State Abbreviation"
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("featured_image"),
        FieldPanel("hero_usp"),
        FieldPanel("body"),
        FieldPanel("about_techs"),
        FieldPanel("state"),
        FieldPanel("zip_codes"),
        MultiFieldPanel(
            [InlinePanel("featured_services", label="Featured Services")],
            heading="Services",
        ),
        MultiFieldPanel(
            [InlinePanel("nearby_cities", label="Nearby Cities")],
            heading="Nearby Locations",
        ),
    ]

    subpage_types: list[str] = []
    parent_page_types = ["locations.LocationsIndexPage"]

    class Meta:
        indexes = [models.Index(fields=["state"])]

    def get_context(self, request: object) -> dict:
        """Prefetch related data and build FAQ items for JSON-LD."""
        import logging

        from django.utils.translation import gettext as _

        context = super().get_context(request)
        context["nearby_cities_optimized"] = list(
            self.nearby_cities.select_related("nearby_city")
        )
        context["featured_services_optimized"] = list(
            self.featured_services.select_related("service")
        )

        city = self.title
        state = self.state or "CA"

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
                "SiteSettings lookup failed in CityPage.get_context"
            )

        # FAQ items — dynamic city name for local SEO keyword targeting
        context["faq_items"] = [
            {
                "question": _("How much does appliance repair cost in %(city)s?")
                % {"city": city},
                "answer": _(
                    "Our diagnostic service call is $%(fee)s, which is waived"
                    " when you approve the repair. We always provide an"
                    " itemized, upfront quote before starting any work — no"
                    " hidden fees or surprise charges. You pay only after the"
                    " repair is complete."
                )
                % {"fee": fee, "city": city},
            },
            {
                "question": _(
                    "What appliance brands do you repair in %(city)s, %(state)s?"
                )
                % {"city": city, "state": state},
                "answer": _(
                    "We repair all major brands including Whirlpool, Samsung,"
                    " LG, GE, Maytag, Kenmore, Frigidaire, Bosch, KitchenAid,"
                    " Sub-Zero, Viking, Thermador, Amana, Electrolux, and"
                    " Speed Queen. Our technicians carry brand-specific OEM"
                    " parts on every truck for fast, reliable repairs in"
                    " %(city)s."
                )
                % {"city": city},
            },
            {
                "question": _("Do you offer same-day appliance repair in %(city)s?")
                % {"city": city},
                "answer": _(
                    "Yes, we offer same-day service in %(city)s and surrounding"
                    " areas. Book before noon and a technician typically"
                    " arrives that afternoon. We operate 7 days a week,"
                    " 8 AM to 8 PM, with no overtime or weekend surcharges."
                    " Our trucks are fully stocked with OEM parts so most"
                    " repairs finish in a single visit."
                )
                % {"city": city},
            },
            {
                "question": _("Is there a warranty on repairs in %(city)s?")
                % {"city": city},
                "answer": _(
                    "Every repair in %(city)s includes a warranty on both"
                    " parts and labor. If the same issue returns within the"
                    " warranty period, we come back and fix it at no"
                    " additional charge — no questions asked. We use OEM"
                    " and manufacturer-approved parts to restore your"
                    " appliance to factory performance standards."
                )
                % {"city": city},
            },
        ]

        # Add ZIP code FAQ if ZIP codes are configured
        if self.zip_codes:
            context["faq_items"].append(
                {
                    "question": _("What ZIP codes do you service in %(city)s?")
                    % {"city": city},
                    "answer": _(
                        "We service the following ZIP codes in and around"
                        " %(city)s: %(zips)s. If your ZIP code is not listed,"
                        " call us — we are expanding our service area"
                        " regularly and can often make arrangements for"
                        " nearby neighborhoods."
                    )
                    % {"city": city, "zips": self.zip_codes},
                }
            )

        return context


class CityFeaturedService(Orderable):
    """Links a city to its featured services."""

    page = ParentalKey(CityPage, related_name="featured_services")
    service = models.ForeignKey(
        "services.ServicePage",
        on_delete=models.CASCADE,
        related_name="+",
    )
    panels = [FieldPanel("service")]


class CityNearbyCity(Orderable):
    """Links a city to nearby cities."""

    page = ParentalKey(CityPage, related_name="nearby_cities")
    nearby_city = models.ForeignKey(
        "locations.CityPage",
        on_delete=models.CASCADE,
        related_name="+",
    )
    panels = [FieldPanel("nearby_city")]
