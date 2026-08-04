"""Home app models: HomePage and configurable SiteSettings."""

from __future__ import annotations

import logging
import re

from django.db import models
from wagtail.admin.panels import FieldPanel, HelpPanel, MultiFieldPanel, ObjectList, TabbedInterface
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import RichTextField
from wagtail.models import Page

from home.reviews import get_customer_review_items

logger = logging.getLogger(__name__)

MAIN_NAV_DEFAULT_ORDER = "home,services,service_areas,brands,blog,about,contact"
FOOTER_COMPANY_DEFAULT_ORDER = (
    "about,contact,blog,service_areas,privacy_policy,terms_of_service"
)


class HomePage(Page):
    """The site's homepage — fetches live services for the landing page."""

    hero_title = models.CharField(
        max_length=255,
        blank=True,
        default="Same-Day Appliance Repair",
        help_text="Main homepage H1. Leave blank to use the translated fallback.",
    )
    hero_subtitle = models.TextField(
        blank=True,
        default=(
            "Professional appliance repair for refrigerators, washers, dryers, "
            "dishwashers, and ovens. Same-day service with certified technicians "
            "and warranty on all repairs."
        ),
        help_text="Intro text shown under the homepage H1.",
    )
    commercial_title = models.CharField(
        max_length=255,
        blank=True,
        default="Commercial & Residential Appliance Repair",
    )
    commercial_body = RichTextField(
        blank=True,
        default=(
            "<p>We repair household and light-commercial refrigerators, freezers, "
            "washers, dryers, dishwashers, ovens, and related appliances across the "
            "Inland Empire.</p><p>Service begins with an on-site diagnosis. Before "
            "work starts, the technician explains the issue, available repair "
            "options, and the price for approval.</p>"
        ),
    )
    services_heading = models.CharField(
        max_length=255,
        blank=True,
        default="What Appliances Do We Repair?",
    )
    process_heading = models.CharField(
        max_length=255,
        blank=True,
        default="How to Book Appliance Repair",
    )
    process_subheading = models.TextField(
        blank=True,
        default=(
            "Choose a service, confirm your service area, and schedule a visit. "
            "We diagnose the appliance before you approve any repair."
        ),
    )
    pricing_heading = models.CharField(
        max_length=255,
        blank=True,
        default="How Much Does Appliance Repair Cost?",
    )
    pricing_note = models.TextField(
        blank=True,
        default=(
            "Your final price depends on the appliance, the fault, and required "
            "parts. The technician confirms the repair price before work begins."
        ),
    )
    brands_heading = models.CharField(
        max_length=255,
        blank=True,
        default="What Appliance Brands Do We Repair?",
    )
    brands_subheading = models.TextField(
        blank=True,
        default=(
            "We service common household and premium appliance brands. Select a "
            "linked brand for details, or call to confirm your model."
        ),
    )
    areas_heading = models.CharField(
        max_length=255,
        blank=True,
        default="Appliance Repair Across the Inland Empire",
    )
    areas_subheading = models.TextField(
        blank=True,
        default=(
            "Serving homes and businesses across Corona, Riverside, and surrounding "
            "Inland Empire communities. Enter your ZIP code to confirm coverage."
        ),
    )
    testimonials_heading = models.CharField(
        max_length=255,
        blank=True,
        default="What Our Customers Say",
    )
    faq_heading = models.CharField(
        max_length=255,
        blank=True,
        default="Frequently Asked Questions",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [FieldPanel("hero_title"), FieldPanel("hero_subtitle")],
            heading="Hero",
        ),
        MultiFieldPanel(
            [FieldPanel("commercial_title"), FieldPanel("commercial_body")],
            heading="Commercial & residential block",
        ),
        MultiFieldPanel(
            [
                FieldPanel("services_heading"),
                FieldPanel("process_heading"),
                FieldPanel("process_subheading"),
                FieldPanel("pricing_heading"),
                FieldPanel("pricing_note"),
                FieldPanel("brands_heading"),
                FieldPanel("brands_subheading"),
                FieldPanel("areas_heading"),
                FieldPanel("areas_subheading"),
                FieldPanel("testimonials_heading"),
                FieldPanel("faq_heading"),
            ],
            heading="Section headings",
        ),
    ]

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

        from home.brand_assets import get_brand_cards
        from home.service_seed_data import (
            FEATURED_SERVICE_HUB_SLUGS,
            SEO_LANDING_SERVICE_SLUGS,
        )
        from locations.models import CityPage
        from services.models import ServicePage

        context = super().get_context(request)
        service_pages = list(
            ServicePage.objects.live()
            .filter(locale=self.locale, is_regional_service_page=False)
            .order_by("path")
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
        service_pages_by_slug = {page.slug: page for page in service_pages}
        context["services"] = [
            page for page in service_pages if page.slug not in SEO_LANDING_SERVICE_SLUGS
        ]
        context["featured_services"] = [
            service_pages_by_slug[slug]
            for slug in FEATURED_SERVICE_HUB_SLUGS
            if slug in service_pages_by_slug
        ]
        context["brand_cards"] = get_brand_cards(service_pages_by_slug)
        context["cities"] = list(
            CityPage.objects.live()
            .filter(locale=self.locale)
            .order_by("title")
            .only("id", "title", "slug", "url_path", "state")
        )

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

        # Review items are sourced via the Phase 04 provenance gate; captured
        # source-business reviews are withheld until target-owned evidence exists.
        context["review_items"] = get_customer_review_items()

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
        default="Inland Empire Appliance Repair",
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
        default="",
        help_text="External booking system URL (UTM params will be appended automatically)",
    )
    booking_source = models.CharField(
        max_length=50,
        blank=True,
        default="inland",
        help_text="Source parameter appended to booking URL (e.g. 'inland', 'website')",
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
    callrail_swap_url = models.URLField(
        blank=True,
        default="",
        help_text=(
            "CallRail swap.js URL for Dynamic Number Insertion "
            "(configured per target account; leave blank when disabled)"
        ),
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

    # Navigation ordering
    main_nav_order = models.CharField(
        max_length=255,
        blank=True,
        default=MAIN_NAV_DEFAULT_ORDER,
        help_text=(
            "Comma-separated top navigation keys in display order. Allowed keys: "
            "home, services, service_areas, brands, blog, about, contact. "
            "Remove a key to hide it."
        ),
    )
    footer_company_order = models.CharField(
        max_length=255,
        blank=True,
        default=FOOTER_COMPANY_DEFAULT_ORDER,
        help_text=(
            "Comma-separated footer company link keys in display order. Allowed "
            "keys: about, contact, blog, service_areas, privacy_policy, "
            "terms_of_service. Remove a key to hide it."
        ),
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
        HelpPanel(
            content=(
                "<p>The display phone is formatted automatically from the "
                "stored phone number when these settings are saved.</p>"
            )
        ),
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
        FieldPanel("callrail_swap_url"),
    ]

    navigation_panels = [
        HelpPanel(
            content=(
                "<p>Edit comma-separated keys below to reorder or hide "
                "top navigation and footer links. Rendering behavior is added "
                "in later platform/UI phases.</p>"
            )
        ),
        FieldPanel("main_nav_order"),
        FieldPanel("footer_company_order"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(business_panels, heading="Business"),
            ObjectList(contact_panels, heading="Contact"),
            ObjectList(booking_panels, heading="Booking"),
            ObjectList(seo_panels, heading="SEO"),
            ObjectList(analytics_panels, heading="Analytics"),
            ObjectList(navigation_panels, heading="Navigation"),
        ]
    )

    class Meta:
        verbose_name = "Site Settings"

    def __str__(self) -> str:
        return self.business_name

    @staticmethod
    def _format_phone_for_display(phone: str) -> str:
        """Return a display phone from a stored phone value without source defaults."""
        digits = re.sub(r"\D", "", phone)
        if len(digits) == 11 and digits.startswith("1"):
            area, prefix, line = digits[1:4], digits[4:7], digits[7:11]
            return f"({area}) {prefix}-{line}"
        if len(digits) == 10:
            area, prefix, line = digits[0:3], digits[3:6], digits[6:10]
            return f"({area}) {prefix}-{line}"
        return phone.lstrip("+") if phone else ""

    def save(self, *args: object, **kwargs: object) -> None:
        """Keep editor-facing display phone synchronized with the stored phone."""
        if self.phone:
            self.phone_display = self._format_phone_for_display(self.phone)
        super().save(*args, **kwargs)

    @property
    def full_address(self) -> str:
        """Return formatted full address."""
        parts = [self.address_line1]
        if self.address_line2:
            parts.append(self.address_line2)
        parts.append(f"{self.city}, {self.state} {self.zip_code}")
        return ", ".join(parts)
