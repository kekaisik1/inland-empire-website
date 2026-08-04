"""Management command to fix SEO audit v2 content issues.

Fixes CMS-stored content that cannot be changed via template edits:
- Issue #6:  Contact page meta description (thin/generic)
- Issue #9:  Service area pages unique meta descriptions
- Issue #12: Blog index H1 (hero_title) — "Our Blog" → keyword-rich
- Issue #14: About page H1 (hero_title) — "About Us" → branded
- Issue #15: Contact page H1 (hero_title) — "Contact Us" → branded
- Issue #18: Services index intro content (thin page)

Run with: python manage.py seo_audit_v2_fixes
"""

from __future__ import annotations

from django.core.management.base import BaseCommand


# ── Issue #9: Unique meta descriptions per service area ──────────────
CITY_META_DESCRIPTIONS: dict[str, str] = {
    "Lake Elsinore": (
        "Same-day appliance repair in Lake Elsinore, CA — serving Diamond"
        " Stadium, Lakepoint, and Tuscany Hills. Refrigerator, washer &"
        " dryer repair. $70 diagnostic waived with repair. Call {phone}."
    ),
    "Murrieta": (
        "Appliance repair in Murrieta, CA — serving Greer Ranch, Los Alamos"
        " Hills & historic downtown. Same-day refrigerator, washer & dryer"
        " repair. $70 diagnostic. Call {phone}."
    ),
    "Temecula": (
        "Appliance repair in Temecula, CA — serving Redhawk, Wolf Creek &"
        " Old Town. Same-day service for refrigerators, washers, dryers &"
        " dishwashers. $70 diagnostic. Call {phone}."
    ),
    "Corona": (
        "Appliance repair in Corona, CA — serving South Corona, Dos Lagos &"
        " Sierra Del Oro. Fast refrigerator, washer & dryer repair. $70"
        " diagnostic waived with repair. Call {phone}."
    ),
    "Riverside": (
        "Appliance repair in Riverside, CA — serving Mission Grove, Canyon"
        " Crest & Arlington. Same-day refrigerator, washer & oven repair."
        " $70 diagnostic waived with repair. Call {phone}."
    ),
    "Menifee": (
        "Appliance repair in Menifee, CA — serving Sun City, Audie Murphy"
        " Ranch & Heritage Lake. Same-day washer, dryer & refrigerator"
        " repair. $70 diagnostic. Call {phone}."
    ),
    "Beaumont": (
        "Appliance repair in Beaumont, CA — serving Four Seasons, Fairway"
        " Canyon & Tournament Hills. Same-day refrigerator & washer repair."
        " $70 diagnostic waived with repair. Call {phone}."
    ),
    "Perris": (
        "Appliance repair in Perris, CA — serving May Ranch, Perris Valley"
        " & Good Hope. Same-day refrigerator, washer & dryer repair. $70"
        " diagnostic waived with repair. Call {phone}."
    ),
    "Canyon Lake": (
        "Appliance repair in Canyon Lake, CA — serving the gated community"
        " and surrounding neighborhoods. Same-day refrigerator, washer &"
        " dryer repair. $70 diagnostic. Call {phone}."
    ),
    "Norco": (
        "Appliance repair in Norco, CA — Horsetown USA. Same-day service"
        " for refrigerators, washers, dryers & dishwashers. $70 diagnostic"
        " waived with repair. Call {phone}."
    ),
}


# ── Issue #18: Services index intro paragraph ────────────────────────
SERVICES_INTRO = (
    "<p>Inland Empire Appliance Repair provides certified, same-day repair for all"
    " major household and commercial appliances across the Inland Empire"
    " and Riverside County. Our EPA 608 certified technicians arrive in"
    " fully stocked trucks with OEM parts — so most repairs are completed"
    " in a single visit.</p>"
    "<p>We service all major brands including Whirlpool, Samsung, LG, GE,"
    " Maytag, Kenmore, Frigidaire, Bosch, KitchenAid, Sub-Zero, Viking,"
    " and Thermador. Whether your refrigerator stopped cooling, your washer"
    " won't drain, or your dryer isn't heating, our team diagnoses the"
    " issue on-site and provides an upfront, itemized quote before any"
    " work begins. Every repair includes a warranty on parts and labor,"
    " and our $70 diagnostic fee is waived when you approve the repair."
    " We operate 7 days a week, 8 AM to 8 PM — no overtime or weekend"
    " surcharges.</p>"
)


class Command(BaseCommand):
    help = "Fix SEO audit v2 content issues in CMS (meta descriptions, H1s, intro)"

    def handle(self, *args: object, **options: object) -> None:
        from wagtail.models import Site

        from home.models import SiteSettings

        # Fetch phone display from site settings
        site = Site.objects.get(is_default_site=True)
        settings = SiteSettings.for_site(site)
        phone = settings.phone_display

        self._fix_contact_meta(issue=6, phone=phone)
        self._fix_service_area_metas(issue=9, phone=phone)
        self._fix_blog_h1(issue=12)
        self._fix_about_h1(issue=14)
        self._fix_contact_h1(issue=15)
        self._fix_services_intro(issue=18)
        self.stdout.write(
            self.style.SUCCESS("\nAll SEO audit v2 content fixes applied.")
        )

    # ── Issue #6 ─────────────────────────────────────────────────────

    def _fix_contact_meta(self, issue: int, phone: str) -> None:
        """Replace generic contact page meta description."""
        from pages.models import StaticPage

        try:
            contact = StaticPage.objects.get(slug="contact", locale__language_code="en")
        except StaticPage.DoesNotExist:
            self.stdout.write(
                self.style.WARNING(f"  [#{issue}] Contact page not found")
            )
            return

        new_desc = (
            "Contact Inland Empire Appliance Repair in Lake Elsinore, CA."
            " Call {phone} for same-day service. Open 7 days,"
            " 8 AM\u20138 PM. $70 diagnostic, waived with repair."
        ).format(phone=phone)
        if contact.search_description == new_desc:
            self.stdout.write(f"  [#{issue}] Contact meta already up to date")
            return

        contact.search_description = new_desc
        contact.save_revision().publish()
        self.stdout.write(
            self.style.SUCCESS(f"  [#{issue}] Contact meta description updated")
        )

    # ── Issue #9 ─────────────────────────────────────────────────────

    def _fix_service_area_metas(self, issue: int, phone: str) -> None:
        """Replace templated meta descriptions on service area pages."""
        from locations.models import CityPage

        updated = 0
        for city in CityPage.objects.filter(locale__language_code="en"):
            raw_desc = CITY_META_DESCRIPTIONS.get(city.title)
            if not raw_desc:
                self.stdout.write(
                    self.style.WARNING(
                        f"  [#{issue}] No custom desc for '{city.title}'"
                    )
                )
                continue
            desc = raw_desc.format(phone=phone)
            if city.search_description == desc:
                continue
            city.search_description = desc
            city.save_revision().publish()
            updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"  [#{issue}] Updated {updated} service area meta descriptions"
            )
        )

    # ── Issue #12 ────────────────────────────────────────────────────

    def _fix_blog_h1(self, issue: int) -> None:
        """Change blog index H1 from 'Our Blog' to keyword-rich heading."""
        from blog.models import BlogIndexPage

        try:
            blog = BlogIndexPage.objects.get(locale__language_code="en")
        except BlogIndexPage.DoesNotExist:
            self.stdout.write(
                self.style.WARNING(f"  [#{issue}] BlogIndexPage not found")
            )
            return

        new_title = "Appliance Repair Tips & Guides"
        if blog.hero_title == new_title:
            self.stdout.write(f"  [#{issue}] Blog H1 already up to date")
            return

        blog.hero_title = new_title
        blog.save_revision().publish()
        self.stdout.write(self.style.SUCCESS(f"  [#{issue}] Blog index H1 updated"))

    # ── Issue #14 ────────────────────────────────────────────────────

    def _fix_about_h1(self, issue: int) -> None:
        """Change About page H1 from 'About Us' to branded heading."""
        from pages.models import StaticPage

        try:
            about = StaticPage.objects.get(slug="about-us", locale__language_code="en")
        except StaticPage.DoesNotExist:
            self.stdout.write(self.style.WARNING(f"  [#{issue}] About page not found"))
            return

        new_title = "About Inland Empire Appliance Repair"
        if about.hero_title == new_title:
            self.stdout.write(f"  [#{issue}] About H1 already up to date")
            return

        about.hero_title = new_title
        about.save_revision().publish()
        self.stdout.write(self.style.SUCCESS(f"  [#{issue}] About page H1 updated"))

    # ── Issue #15 ────────────────────────────────────────────────────

    def _fix_contact_h1(self, issue: int) -> None:
        """Change Contact page H1 from 'Contact Us' to branded heading."""
        from pages.models import StaticPage

        try:
            contact = StaticPage.objects.get(slug="contact", locale__language_code="en")
        except StaticPage.DoesNotExist:
            self.stdout.write(
                self.style.WARNING(f"  [#{issue}] Contact page not found")
            )
            return

        new_title = "Contact Inland Empire Appliance Repair"
        if contact.hero_title == new_title:
            self.stdout.write(f"  [#{issue}] Contact H1 already up to date")
            return

        contact.hero_title = new_title
        contact.save_revision().publish()
        self.stdout.write(self.style.SUCCESS(f"  [#{issue}] Contact page H1 updated"))

    # ── Issue #18 ────────────────────────────────────────────────────

    def _fix_services_intro(self, issue: int) -> None:
        """Add descriptive intro paragraph to services index page."""
        from services.models import ServicesIndexPage

        try:
            svc = ServicesIndexPage.objects.get(locale__language_code="en")
        except ServicesIndexPage.DoesNotExist:
            self.stdout.write(
                self.style.WARNING(f"  [#{issue}] ServicesIndexPage not found")
            )
            return

        if svc.intro and len(svc.intro) > 100:
            self.stdout.write(f"  [#{issue}] Services intro already has content")
            return

        svc.intro = SERVICES_INTRO
        svc.save_revision().publish()
        self.stdout.write(
            self.style.SUCCESS(f"  [#{issue}] Services index intro content added")
        )
