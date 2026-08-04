"""Management command to fix SEO content issues from the audit.

- Issue #25: Expand About Us page from ~129 words to 500+ words
- Issue #33: Create Privacy Policy and Terms of Service pages

Run with: python manage.py seo_content_fixes
"""

from __future__ import annotations

from django.core.management.base import BaseCommand

from home.models import HomePage
from pages.models import StaticPage


# ── About Us expanded content (Issue #25) ─────────────────────────────

ABOUT_BODY = (
    "<h2>Our Story</h2>"
    "<p>Inland Empire Appliance Repair was founded in the heart of the Inland Empire "
    "with a simple mission: provide honest, same-day appliance repair that "
    "homeowners and business owners can trust. What started as a one-truck "
    "operation serving the Inland Empire has grown into a team of EPA 608 "
    "certified technicians covering over 140 ZIP codes across Riverside "
    "County — from Corona and Riverside to Temecula and Beaumont.</p>"
    "<h2>Our Team</h2>"
    "<p>Every Inland Empire Appliance Repair technician holds EPA Section 608 certification for safe "
    "refrigerant handling and is factory-trained on all major brands including "
    "Samsung, LG, Whirlpool, GE, Maytag, Sub-Zero, Viking, and Thermador. "
    "We invest in ongoing training so our team stays current with the latest "
    "appliance technology — from smart refrigerators with Wi-Fi diagnostics "
    "to high-efficiency heat-pump dryers.</p>"
    "<p>Our technicians arrive in fully stocked trucks carrying hundreds of "
    "OEM parts, so most repairs are completed in a single visit. No return "
    "trips, no waiting for parts to ship — just a fast, reliable fix.</p>"
    "<h2>How We Work</h2>"
    "<p>We believe appliance repair should be simple and stress-free. When "
    "you book with Inland Empire Appliance Repair, here is what to expect:</p>"
    "<ul>"
    "<li><strong>Transparent pricing:</strong> Our diagnostic service call "
    "fee is waived when you approve the repair. You receive an itemized, "
    "upfront quote before any work begins — no hidden fees, no surprise "
    "charges.</li>"
    "<li><strong>Same-day service:</strong> Book before noon and a "
    "technician typically arrives that afternoon. We operate 7 days a week, "
    "8 AM to 8 PM, with no overtime or weekend surcharges.</li>"
    "<li><strong>Warranty included:</strong> Every repair is backed by a "
    "warranty on both parts and labor. If the same issue returns within the "
    "warranty period, we come back and fix it at no additional charge.</li>"
    "<li><strong>Pay after the job:</strong> You only pay after the repair "
    "is complete and you are satisfied with the work.</li>"
    "</ul>"
    "<h2>What We Repair</h2>"
    "<p>We service all major household and commercial appliances:</p>"
    "<ul>"
    "<li>Refrigerators (French door, side-by-side, built-in, commercial walk-in coolers)</li>"
    "<li>Washers and dryers (top-load, front-load, stackable, gas and electric)</li>"
    "<li>Dishwashers</li>"
    "<li>Ovens, stoves, and ranges (gas and electric)</li>"
    "<li>Microwaves (built-in and countertop)</li>"
    "<li>Freezers (chest and upright)</li>"
    "<li>Ice makers</li>"
    "<li>Water heaters (tank and tankless)</li>"
    "</ul>"
    "<h2>Serving Our Community</h2>"
    "<p>As a locally owned business, we take pride in serving the Inland "
    "Empire communities we live in. From Lake Elsinore and Murrieta to "
    "Canyon Lake and Perris, we are your neighbors — and we treat every "
    "home like our own. We are committed to honest diagnostics, fair "
    "pricing, and repairs that last.</p>"
    "<p>Whether you need an emergency refrigerator repair, a routine dryer "
    "vent cleaning, or a second opinion on a quote from another company, "
    "Inland Empire Appliance Repair is here to help. Book online or call us today.</p>"
)

ABOUT_HERO_SUBTITLE = (
    "EPA-certified technicians. Same-day service across Riverside County. "
    "Warranty on every repair."
)

ABOUT_SEARCH_DESCRIPTION = (
    "Meet the Inland Empire Appliance Repair team — EPA 608 certified technicians "
    "serving the Inland Empire and 10+ Riverside County cities. "
    "Same-day service, OEM parts, warranty included on all repairs."
)

# Exact values emitted by setup_pages before the expanded About seed was added.
# They are deliberately narrow recovery markers: any other nonempty value is
# treated as editor-authored and preserved.
LEGACY_ABOUT_BODY = (
    "<p>We specialize in residential and commercial appliance repair "
    "with a focus on quality, reliability, and customer satisfaction. "
    "Our certified technicians are factory-trained on all major brands "
    "and arrive with fully stocked trucks for same-day repairs.</p>"
    "<p>Every repair is backed by our parts and labor warranty — "
    "if something goes wrong within the warranty period, we fix it "
    "at no additional cost. We believe in transparent pricing, "
    "honest diagnostics, and repairs that last.</p>"
)
LEGACY_ABOUT_HERO_SUBTITLE = "Your trusted appliance repair experts."
LEGACY_ABOUT_SEARCH_DESCRIPTION = (
    "Learn about our certified appliance repair team. "
    "Years of experience, all major brands, same-day service, "
    "and warranty-backed repairs."
)


# ── Privacy Policy content (Issue #33) ────────────────────────────────

PRIVACY_BODY = (
    "<h2>Information We Collect</h2>"
    "<p>When you use our website or book a service, we may collect the "
    "following information:</p>"
    "<ul>"
    "<li><strong>Contact information:</strong> name, email address, phone "
    "number, and mailing address that you provide through our contact form "
    "or booking system.</li>"
    "<li><strong>Service information:</strong> details about the appliance "
    "repair services you request, including appliance type, issue "
    "description, and preferred appointment times.</li>"
    "<li><strong>Usage data:</strong> information about how you interact "
    "with our website, including pages visited, time spent on pages, "
    "and referring URLs. This data is collected through Google Analytics "
    "and is used to improve our website experience.</li>"
    "<li><strong>Device information:</strong> browser type, operating "
    "system, and device type used to access our website.</li>"
    "</ul>"
    "<h2>How We Use Your Information</h2>"
    "<p>We use your personal information to:</p>"
    "<ul>"
    "<li>Schedule and provide appliance repair services</li>"
    "<li>Communicate with you about your service appointments</li>"
    "<li>Send appointment confirmations and reminders</li>"
    "<li>Respond to your questions and requests</li>"
    "<li>Improve our website and services</li>"
    "<li>Comply with legal obligations</li>"
    "</ul>"
    "<h2>Information Sharing</h2>"
    "<p>We do not sell, trade, or rent your personal information to third "
    "parties. We may share your information with:</p>"
    "<ul>"
    "<li><strong>Service providers:</strong> third-party tools we use to "
    "operate our business (e.g., scheduling software, payment processors, "
    "email services). These providers are bound by their own privacy "
    "policies and are prohibited from using your information for purposes "
    "other than providing services to us.</li>"
    "<li><strong>Legal compliance:</strong> when required by law, "
    "subpoena, or other legal process.</li>"
    "</ul>"
    "<h2>Your California Privacy Rights (CCPA)</h2>"
    "<p>If you are a California resident, you have the right to:</p>"
    "<ul>"
    "<li>Know what personal information we collect about you</li>"
    "<li>Request deletion of your personal information</li>"
    "<li>Opt out of the sale of your personal information (we do not sell "
    "personal information)</li>"
    "<li>Not be discriminated against for exercising your privacy rights</li>"
    "</ul>"
    "<p>To exercise these rights, contact us at the email or phone number "
    "listed on our Contact page.</p>"
    "<h2>Cookies and Tracking</h2>"
    "<p>Our website uses cookies and similar technologies for analytics "
    "(Google Analytics) and functionality. You can control cookie settings "
    "through your browser preferences. Disabling cookies may affect some "
    "website features.</p>"
    "<h2>Data Security</h2>"
    "<p>We implement appropriate technical and organizational measures to "
    "protect your personal information against unauthorized access, "
    "alteration, disclosure, or destruction. Our website uses HTTPS "
    "encryption for all data transmission.</p>"
    "<h2>Changes to This Policy</h2>"
    "<p>We may update this privacy policy from time to time. Any changes "
    "will be posted on this page with an updated effective date.</p>"
    "<h2>Contact Us</h2>"
    "<p>If you have questions about this privacy policy or our data "
    "practices, please contact us through our Contact page or call us "
    "directly.</p>"
)


# ── Terms of Service content (Issue #33) ──────────────────────────────

TERMS_BODY = (
    "<h2>Services</h2>"
    "<p>Inland Empire Appliance Repair provides residential and commercial appliance "
    "repair services in Riverside County, California and surrounding areas. "
    "Service availability depends on your location and technician "
    "scheduling. We operate 7 days a week, 8 AM to 8 PM.</p>"
    "<h2>Service Calls and Pricing</h2>"
    "<p>Our diagnostic service call fee is disclosed at the time of "
    "booking. This fee is waived when you approve the recommended repair. "
    "Before performing any repair work, our technician will provide an "
    "itemized quote for your approval. You are under no obligation to "
    "proceed with the repair — if you decline, only the diagnostic fee "
    "applies.</p>"
    "<p>Payment is due upon completion of the repair. We accept cash, "
    "credit cards, and debit cards.</p>"
    "<h2>Warranty</h2>"
    "<p>All repairs performed by Inland Empire Appliance Repair include a warranty "
    "on parts and labor. If the same issue recurs within the warranty "
    "period, we will return and repair it at no additional charge. The "
    "warranty covers the specific repair performed and does not extend to "
    "unrelated issues or pre-existing conditions not addressed during the "
    "original service.</p>"
    "<h2>Scheduling and Cancellations</h2>"
    "<p>We offer same-day and next-day appointments based on availability. "
    "If you need to cancel or reschedule, please contact us as soon as "
    "possible. We understand that schedules change and do not charge "
    "cancellation fees.</p>"
    "<h2>Customer Responsibilities</h2>"
    "<p>To ensure a smooth service experience, we ask that you:</p>"
    "<ul>"
    "<li>Provide accurate information about the appliance issue</li>"
    "<li>Ensure safe and reasonable access to the appliance</li>"
    "<li>Be present (or have an authorized adult present) during the "
    "service appointment</li>"
    "<li>Disclose any known safety hazards in the service area</li>"
    "</ul>"
    "<h2>Limitation of Liability</h2>"
    "<p>Inland Empire Appliance Repair is not liable for pre-existing damage, "
    "defects not related to the repair performed, damage caused by misuse "
    "or neglect after repair, or issues arising from unauthorized "
    "modifications to the appliance. Our total liability for any claim "
    "related to our services shall not exceed the amount paid for the "
    "specific repair in question.</p>"
    "<h2>Website Use</h2>"
    "<p>The content on this website is provided for informational purposes "
    "only. While we strive to keep information accurate and up to date, we "
    "make no warranties about the completeness, reliability, or accuracy "
    "of this information. Blog posts and repair guides are educational "
    "content and should not replace professional diagnosis.</p>"
    "<h2>Changes to These Terms</h2>"
    "<p>We reserve the right to update these terms at any time. Changes "
    "take effect when posted on this page.</p>"
    "<h2>Contact</h2>"
    "<p>For questions about these terms, please contact us through our "
    "Contact page or call us directly.</p>"
)


class Command(BaseCommand):
    help = "Fix SEO content issues: expand About page, create Privacy/Terms pages"

    def handle(self, *args: object, **options: object) -> None:
        self._expand_about_page()
        self._create_privacy_policy()
        self._create_terms_of_service()
        self.stdout.write(self.style.SUCCESS("\nAll SEO content fixes applied."))

    def _expand_about_page(self) -> None:
        """Issue #25: Expand About Us page from ~129 words to 600+ words."""
        try:
            about = StaticPage.objects.get(slug="about-us", locale__language_code="en")
        except StaticPage.DoesNotExist:
            self.stdout.write(
                self.style.WARNING("  About Us page not found — skipping")
            )
            return

        changed_fields: list[str] = []
        for field, legacy, desired in (
            ("body", LEGACY_ABOUT_BODY, ABOUT_BODY),
            (
                "hero_subtitle",
                LEGACY_ABOUT_HERO_SUBTITLE,
                ABOUT_HERO_SUBTITLE,
            ),
            (
                "search_description",
                LEGACY_ABOUT_SEARCH_DESCRIPTION,
                ABOUT_SEARCH_DESCRIPTION,
            ),
        ):
            current = str(getattr(about, field, "") or "")
            if current != desired and (not current or current == legacy):
                setattr(about, field, desired)
                changed_fields.append(field)

        if changed_fields:
            about.save_revision().publish()
            self.stdout.write(
                self.style.SUCCESS(
                    "  [#25] About Us seed updated: " + ", ".join(changed_fields)
                )
            )
        else:
            self.stdout.write("  [#25] About Us current/editor-authored — preserving")

    def _create_page_if_missing(
        self,
        slug: str,
        title: str,
        seo_title: str,
        search_description: str,
        hero_title: str,
        hero_subtitle: str,
        body: str,
        cta_title: str = "",
    ) -> bool:
        """Create a StaticPage under the homepage if it doesn't exist."""
        if StaticPage.objects.filter(slug=slug).exists():
            self.stdout.write(f"  '{slug}' already exists — skipping")
            return False

        try:
            home = HomePage.objects.first()
        except HomePage.DoesNotExist:
            self.stdout.write(self.style.WARNING("  HomePage not found — skipping"))
            return False

        if home is None:
            self.stdout.write(self.style.WARNING("  HomePage not found — skipping"))
            return False

        page = StaticPage(
            title=title,
            slug=slug,
            seo_title=seo_title,
            search_description=search_description,
            hero_title=hero_title,
            hero_subtitle=hero_subtitle,
            body=body,
            cta_title=cta_title or "Need Appliance Repair?",
            cta_text="Book same-day service with our certified technicians.",
            cta_button_text="Book Now",
        )
        home.add_child(instance=page)
        page.save_revision().publish()
        return True

    def _create_privacy_policy(self) -> None:
        """Issue #33: Create Privacy Policy page."""
        created = self._create_page_if_missing(
            slug="privacy-policy",
            title="Privacy Policy",
            seo_title="Privacy Policy | Inland Empire Appliance Repair",
            search_description=(
                "Inland Empire Appliance Repair privacy policy. Learn how we collect, "
                "use, and protect your personal information. CCPA compliant."
            ),
            hero_title="Privacy Policy",
            hero_subtitle="How we collect, use, and protect your information.",
            body=PRIVACY_BODY,
            cta_title="",
        )
        if created:
            self.stdout.write(self.style.SUCCESS("  [#33] Privacy Policy page created"))

    def _create_terms_of_service(self) -> None:
        """Issue #33: Create Terms of Service page."""
        created = self._create_page_if_missing(
            slug="terms-of-service",
            title="Terms of Service",
            seo_title="Terms of Service | Inland Empire Appliance Repair",
            search_description=(
                "Inland Empire Appliance Repair terms of service. Service call pricing, "
                "warranty terms, scheduling policies, and customer responsibilities."
            ),
            hero_title="Terms of Service",
            hero_subtitle="Terms and conditions for our appliance repair services.",
            body=TERMS_BODY,
            cta_title="",
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS("  [#33] Terms of Service page created")
            )
