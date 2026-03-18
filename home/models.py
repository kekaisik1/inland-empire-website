"""Home app models: HomePage and configurable SiteSettings."""

from __future__ import annotations

import logging

from django.db import models
from wagtail.admin.panels import FieldPanel, TabbedInterface, ObjectList
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.models import Page

logger = logging.getLogger(__name__)


class HomePage(Page):
    """The site's homepage — fetches live services for the landing page."""

    max_count = 1
    subpage_types = [
        "services.ServicesIndexPage",
        "locations.LocationsIndexPage",
        "pages.StaticPage",
        "blog.BlogIndexPage",
    ]

    def get_context(self, request: object) -> dict:
        """Add live services and FAQ items to the template context."""
        from django.utils.translation import gettext as _

        from services.models import ServicePage

        context = super().get_context(request)
        context["services"] = (
            ServicePage.objects.live()
            .filter(locale=self.locale)
            .only("id", "title", "slug", "url_path", "intro", "short_description")
        )
        # FAQ items for JSON-LD (matches the hardcoded FAQ in home_page.html)
        city = ""
        fee = "70"
        try:
            from wagtail.models import Site

            site = Site.find_for_request(request)
            biz = SiteSettings.for_site(site)
            city = biz.city or ""
            fee = str(biz.service_call_fee)
        except (SiteSettings.DoesNotExist, Site.DoesNotExist, AttributeError) as exc:
            logger.warning(
                "SiteSettings lookup failed in HomePage.get_context: %s", exc
            )

        area_answer = (
            _(
                "We serve %(city)s and the surrounding Inland Empire area,"
                " including Lake Elsinore, Murrieta, Temecula, Menifee, Corona,"
                " Riverside, Beaumont, Perris, Canyon Lake, and Norco. Our"
                " service area covers over 140 ZIP codes across Riverside County."
                " Enter your ZIP code in the booking form above to confirm"
                " same-day availability in your neighborhood."
            )
            % {"city": city}
            if city
            else _(
                "We serve the Inland Empire area, including Lake Elsinore,"
                " Murrieta, Temecula, Menifee, Corona, Riverside, Beaumont,"
                " Perris, Canyon Lake, and Norco. Our service area covers over"
                " 140 ZIP codes across Riverside County. Enter your ZIP code in"
                " the booking form above to confirm same-day availability in"
                " your neighborhood."
            )
        )

        # Review items for JSON-LD (matches hardcoded testimonials)
        context["review_items"] = [
            {
                "author": "Maria G.",
                "rating": 5,
                "text": _(
                    "Called in the morning and they were here by noon."
                    " Fixed my refrigerator on the spot."
                    " Very professional and fair pricing."
                ),
            },
            {
                "author": "James T.",
                "rating": 5,
                "text": _(
                    "Great experience with washer repair."
                    " The technician explained everything clearly"
                    " and the warranty gives peace of mind."
                ),
            },
            {
                "author": "David R.",
                "rating": 5,
                "text": _(
                    "They repaired our commercial dishwasher quickly."
                    " Reasonable rates and they waived the service call fee."
                    " Highly recommend!"
                ),
            },
        ]

        context["faq_items"] = [
            {
                "question": _("Do you service commercial appliances?"),
                "answer": _(
                    "Yes, we service both commercial and residential appliances"
                    " across Riverside County. Our technicians hold EPA 608"
                    " certification and are trained to work on industrial-grade"
                    " equipment — including walk-in coolers, commercial ice"
                    " machines, and restaurant-grade ovens — as well as standard"
                    " home appliances. We carry commercial-rated parts on our"
                    " trucks so most jobs are completed in a single visit."
                ),
            },
            {
                "question": _("Is there a warranty on repairs?"),
                "answer": _(
                    "Every repair includes a warranty on both parts and labor."
                    " If the same issue returns within the warranty period, we"
                    " come back and fix it at no additional charge — no questions"
                    " asked. We use OEM and manufacturer-approved replacement"
                    " parts, which means your appliance is restored to factory"
                    " performance standards. Ask your technician for specific"
                    " warranty terms for your repair."
                ),
            },
            {
                "question": _("What areas do you cover?"),
                "answer": area_answer,
            },
            {
                "question": _("How quickly can you get here?"),
                "answer": _(
                    "In most cases, we arrive the same day you book. Morning"
                    " bookings typically get an afternoon slot. We operate 7 days"
                    " a week, 8 AM to 8 PM, and evening and weekend appointments"
                    " are available at no extra charge. For urgent situations —"
                    " like a leaking washer or a refrigerator that stopped"
                    " cooling — let us know so we can prioritize your call."
                ),
            },
            {
                "question": _("How much does appliance repair cost?"),
                "answer": _(
                    "Our diagnostic service call is $%(fee)s, which is waived"
                    " when you approve the repair. Most residential appliance"
                    " repairs range from $150 to $400 depending on the appliance"
                    " type, the specific issue, and parts needed. We always"
                    " provide an itemized, upfront quote before starting any"
                    " work — no hidden fees, no surprise charges. You only pay"
                    " after the repair is complete and you are satisfied."
                )
                % {"fee": fee},
            },
            {
                "question": _("What appliance brands do you repair?"),
                "answer": _(
                    "We repair all major brands including Whirlpool, Samsung, LG,"
                    " GE, Maytag, Kenmore, Frigidaire, Bosch, KitchenAid,"
                    " Sub-Zero, Viking, Thermador, Amana, Electrolux, and Speed"
                    " Queen — plus dozens of other makes. Our technicians are"
                    " factory-trained and carry brand-specific OEM parts for"
                    " reliable, lasting repairs. If your brand is not listed,"
                    " give us a call — chances are we service it."
                ),
            },
            {
                "question": _("Do I need to be home during the repair?"),
                "answer": _(
                    "Yes, someone 18 or older should be present during the visit."
                    " The technician will need access to the appliance and may"
                    " need to ask questions about the issue. For commercial jobs,"
                    " a manager or authorized staff member should be available."
                    " We always call ahead before arrival so you can plan"
                    " accordingly."
                ),
            },
            {
                "question": _("What should I do before the technician arrives?"),
                "answer": _(
                    "Clear the area around the appliance so the technician can"
                    " access it easily. If possible, note the brand, model number"
                    " (usually on a sticker inside the door or on the back), and"
                    " a brief description of the problem. This helps us diagnose"
                    " the issue faster and ensures we have the right parts on"
                    " hand."
                ),
            },
        ]
        return context


@register_setting
class SiteSettings(BaseSiteSetting):
    """Configurable business info — editable from the Wagtail admin panel."""

    # Business identity
    business_name = models.CharField(
        max_length=255,
        default="LOWL Appliance Repair",
        help_text="Business name shown in header, footer, and SEO",
    )
    tagline = models.CharField(
        max_length=255,
        blank=True,
        default="Same-Day Appliance Repair",
        help_text="Short tagline shown in hero section",
    )

    # Contact info
    phone = models.CharField(
        max_length=20,
        blank=True,
        default="+19099752506",
        help_text="Primary phone number (with country code)",
    )
    phone_display = models.CharField(
        max_length=30,
        blank=True,
        default="(909) 975-2506",
        help_text="Phone number as displayed to users",
    )
    email = models.EmailField(blank=True, default="inlandrepair.ca@gmail.com")

    # Address
    address_line1 = models.CharField(
        max_length=255, blank=True, default="632 Shadybrook Ln"
    )
    address_line2 = models.CharField(max_length=255, blank=True, default="")
    city = models.CharField(max_length=100, blank=True, default="Corona")
    state = models.CharField(max_length=2, blank=True, default="CA")
    zip_code = models.CharField(max_length=10, blank=True, default="92879")

    # Booking
    booking_url = models.URLField(
        blank=True,
        default="https://lowl-booking-production.up.railway.app/",
        help_text="External booking system URL (UTM params will be appended automatically)",
    )
    booking_source = models.CharField(
        max_length=50,
        blank=True,
        default="lowl",
        help_text="Source parameter appended to booking URL (e.g. 'lowl', 'profix')",
    )

    # Business details
    business_hours = models.CharField(
        max_length=100,
        blank=True,
        default="8:00 AM - 8:00 PM",
        help_text="Operating hours displayed on the site",
    )
    opening_time = models.TimeField(
        default="08:00",
        help_text="Daily opening time for structured data (e.g. 08:00)",
    )
    closing_time = models.TimeField(
        default="20:00",
        help_text="Daily closing time for structured data (e.g. 20:00)",
    )
    warranty_text = models.CharField(
        max_length=100,
        blank=True,
        default="Warranty Included",
        help_text="Warranty label displayed on the site (e.g. 'Warranty Included', '90-Day Warranty')",
    )
    service_call_fee = models.PositiveIntegerField(
        default=70, help_text="Diagnostic/service call fee in dollars"
    )
    labor_rate_min = models.PositiveIntegerField(
        default=120, help_text="Minimum labor rate in dollars"
    )

    # SEO / Reviews
    google_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=4.9,
        help_text="Average Google review rating (e.g. 4.9)",
    )
    google_review_count = models.PositiveIntegerField(
        default=150,
        help_text="Total number of Google reviews",
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        default=33.668045,
        help_text="Business latitude for Google Maps (e.g. 33.668045)",
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        default=-117.327354,
        help_text="Business longitude for Google Maps (e.g. -117.327354)",
    )

    # Social profiles (feeds into Organization sameAs for Google Knowledge Panel)
    google_business_url = models.URLField(
        blank=True,
        help_text="Google Business Profile URL (e.g. https://g.co/kgs/...)",
    )
    yelp_url = models.URLField(
        blank=True,
        help_text="Yelp business page URL",
    )
    facebook_url = models.URLField(
        blank=True,
        help_text="Facebook business page URL",
    )

    # Analytics & tracking
    google_analytics_id = models.CharField(
        max_length=30,
        blank=True,
        help_text="Google Analytics 4 Measurement ID (e.g. G-XXXXXXXXXX)",
    )
    gtm_id = models.CharField(
        max_length=30, blank=True, help_text="Google Tag Manager ID (e.g. GTM-XXXXXXX)"
    )
    google_site_verification = models.CharField(
        max_length=100,
        blank=True,
        help_text="Google Search Console verification code (just the content value)",
    )
    bing_site_verification = models.CharField(
        max_length=100,
        blank=True,
        help_text="Bing Webmaster Tools verification code",
    )

    # Admin panels
    business_panels = [
        FieldPanel("business_name"),
        FieldPanel("tagline"),
        FieldPanel("business_hours"),
        FieldPanel("opening_time"),
        FieldPanel("closing_time"),
        FieldPanel("warranty_text"),
        FieldPanel("service_call_fee"),
        FieldPanel("labor_rate_min"),
    ]

    contact_panels = [
        FieldPanel("phone"),
        FieldPanel("phone_display"),
        FieldPanel("email"),
        FieldPanel("address_line1"),
        FieldPanel("address_line2"),
        FieldPanel("city"),
        FieldPanel("state"),
        FieldPanel("zip_code"),
    ]

    booking_panels = [
        FieldPanel("booking_url"),
        FieldPanel("booking_source"),
    ]

    seo_panels = [
        FieldPanel("google_rating"),
        FieldPanel("google_review_count"),
        FieldPanel("latitude"),
        FieldPanel("longitude"),
        FieldPanel("google_site_verification"),
        FieldPanel("bing_site_verification"),
        FieldPanel("google_business_url"),
        FieldPanel("yelp_url"),
        FieldPanel("facebook_url"),
    ]

    analytics_panels = [
        FieldPanel("google_analytics_id"),
        FieldPanel("gtm_id"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(business_panels, heading="Business"),
            ObjectList(contact_panels, heading="Contact"),
            ObjectList(booking_panels, heading="Booking"),
            ObjectList(seo_panels, heading="SEO"),
            ObjectList(analytics_panels, heading="Analytics"),
        ]
    )

    class Meta:
        verbose_name = "Site Settings"

    def __str__(self) -> str:
        return self.business_name

    @property
    def full_address(self) -> str:
        """Return formatted full address."""
        parts = [self.address_line1]
        if self.address_line2:
            parts.append(self.address_line2)
        parts.append(f"{self.city}, {self.state} {self.zip_code}")
        return ", ".join(parts)
