"""Management command to create supplemental SEO service pages (Issue #26).

Creates pages targeting "[brand] appliance repair [city]" keywords for
the top 5 most-searched appliance brands plus approved standalone services.

Run with: python manage.py create_brand_pages
"""

from __future__ import annotations

from typing import Any

from django.core.management.base import BaseCommand

from home.high_end_brand_seed_data import HIGH_END_BRAND_SERVICE_PAGES
from home.service_seed_data import (
    COMMERCIAL_SERVICE_PAGE,
    HIGH_END_SERVICE_PAGE,
    SEO_LANDING_SERVICE_SLUGS,
    apply_service_page_seed_data,
)
from services.models import ServicePage, ServiceRelatedService, ServicesIndexPage


BRAND_PAGES: list[dict[str, Any]] = [
    {
        "title": "Samsung Appliance Repair",
        "slug": "samsung-appliance-repair",
        "seo_title": "Samsung Appliance Repair — Same-Day Service, Certified Techs",
        "search_description": (
            "Expert Samsung appliance repair — refrigerators, washers, dryers, "
            "dishwashers & ranges. Same-day service, OEM Samsung parts, "
            "warranty included. Book today."
        ),
        "intro": (
            "Certified Samsung appliance repair for refrigerators, washers, "
            "dryers, dishwashers, and ranges — same-day service available"
        ),
        "short_description": "Factory-trained Samsung repair with OEM parts.",
        "hero_usp": (
            "Samsung-certified repair for all models — Family Hub fridges, "
            "FlexWash washers, smart ranges, and more."
        ),
        "body": (
            "<h2>Samsung Appliance Repair Specialists</h2>"
            "<p>Samsung appliances are packed with advanced technology — from "
            "Family Hub refrigerators with touchscreen displays to FlexWash "
            "washers with dual-drum systems. When these sophisticated "
            "appliances break down, you need a technician who understands "
            "Samsung's proprietary systems, error codes, and parts.</p>"
            "<p>Our technicians are factory-trained on Samsung's full "
            "appliance lineup and carry OEM Samsung parts on every truck. "
            "Whether your Samsung fridge is flashing error code 22E, your "
            "washer won't spin, or your dryer isn't heating, we diagnose "
            "and fix it the same day you call.</p>"
            "<h2>Samsung Appliances We Repair</h2>"
            "<p>We service the complete Samsung appliance range:</p>"
            "<ul>"
            "<li><strong>Refrigerators:</strong> French door, side-by-side, "
            "Family Hub, Bespoke, 4-Door Flex, bottom-freezer</li>"
            "<li><strong>Washers:</strong> front-load, top-load, FlexWash, "
            "smart washer models with Wi-Fi connectivity</li>"
            "<li><strong>Dryers:</strong> electric, gas, heat pump, "
            "FlexDry models</li>"
            "<li><strong>Dishwashers:</strong> built-in, StormWash, "
            "AutoRelease Door models</li>"
            "<li><strong>Ranges & Ovens:</strong> gas, electric, induction, "
            "slide-in, freestanding, double oven</li>"
            "</ul>"
            "<h2>Common Samsung Error Codes We Fix</h2>"
            "<p>Samsung appliances display specific error codes to help "
            "diagnose issues. Our technicians are trained to interpret and "
            "resolve all Samsung error codes quickly:</p>"
            "<ul>"
            "<li>Refrigerator codes: 22E, 41E, 84E, OF OF, PC ER</li>"
            "<li>Washer codes: UE, OE, LE, dE, nF, 4E</li>"
            "<li>Dryer codes: tS, tO, hE, dF, FE, bE</li>"
            "</ul>"
            "<h2>Why Choose Us for Samsung Repair</h2>"
            "<p>We carry a comprehensive inventory of genuine Samsung parts "
            "— compressors, control boards, door seals, drum bearings, "
            "heating elements, and sensors. Most Samsung repairs are "
            "completed in a single visit with OEM parts, ensuring your "
            "appliance performs like new and maintaining your manufacturer "
            "warranty compliance.</p>"
        ),
        "problems": [
            "Samsung refrigerator not cooling",
            "Samsung washer UE or unbalanced error",
            "Samsung dryer not heating",
            "Samsung dishwasher not draining",
            "Samsung oven not reaching temperature",
            "Samsung fridge ice maker not working",
            "Samsung washer leaking water",
            "Samsung error codes on display",
        ],
    },
    {
        "title": "LG Appliance Repair",
        "slug": "lg-appliance-repair",
        "seo_title": "LG Appliance Repair — Same-Day Service, OEM Parts",
        "search_description": (
            "Professional LG appliance repair — refrigerators, washers, dryers, "
            "dishwashers & ranges. Same-day service with OEM LG parts. "
            "Warranty included."
        ),
        "intro": (
            "Professional LG appliance repair for refrigerators, washers, "
            "dryers, and dishwashers — certified technicians, same-day service"
        ),
        "short_description": "Certified LG repair with genuine OEM parts.",
        "hero_usp": (
            "LG-trained technicians for InstaView fridges, TurboWash washers, "
            "ThinQ smart appliances, and all LG models."
        ),
        "body": (
            "<h2>LG Appliance Repair Experts</h2>"
            "<p>LG appliances feature Inverter Linear Compressor technology, "
            "ThinQ smart connectivity, and innovative designs like InstaView "
            "Door-in-Door refrigerators and TurboWash 360 washers. Our "
            "technicians are trained on LG's proprietary systems and "
            "carry genuine LG parts for same-day repairs.</p>"
            "<h2>LG Appliances We Repair</h2>"
            "<ul>"
            "<li><strong>Refrigerators:</strong> InstaView, French door, "
            "side-by-side, bottom-freezer, counter-depth</li>"
            "<li><strong>Washers:</strong> front-load, top-load, WashTower, "
            "TurboWash, TWINWash models</li>"
            "<li><strong>Dryers:</strong> gas, electric, heat pump, "
            "Dual Inverter models</li>"
            "<li><strong>Dishwashers:</strong> QuadWash, TrueSteam, "
            "built-in models</li>"
            "<li><strong>Ranges:</strong> gas, electric, InstaView, "
            "ProBake Convection, air fry models</li>"
            "</ul>"
            "<h2>Common LG Issues We Fix</h2>"
            "<p>LG appliances are reliable but common issues include "
            "Inverter Linear Compressor failures on refrigerators, drum "
            "bearing wear on washers, and control board malfunctions. "
            "Our trucks carry replacement compressors, bearings, motors, "
            "sensors, and boards for all current LG models.</p>"
            "<h2>OEM LG Parts, Same-Day Service</h2>"
            "<p>Using genuine LG parts ensures your appliance maintains "
            "its efficiency ratings and warranty coverage. We stock the "
            "most commonly needed LG parts on our trucks so most repairs "
            "are completed in a single visit — no waiting for parts "
            "to ship.</p>"
        ),
        "problems": [
            "LG refrigerator compressor failure",
            "LG washer OE or drain error",
            "LG dryer not heating properly",
            "LG dishwasher not cleaning dishes",
            "LG fridge not making ice",
            "LG washer excessive vibration",
            "LG oven igniter not working",
            "LG ThinQ connectivity issues",
        ],
    },
    {
        "title": "Whirlpool Appliance Repair",
        "slug": "whirlpool-appliance-repair",
        "seo_title": "Whirlpool Appliance Repair — Same-Day Fix, All Models",
        "search_description": (
            "Whirlpool appliance repair — refrigerators, washers, dryers & "
            "dishwashers. Same-day service with OEM Whirlpool parts. "
            "Certified technicians. Warranty included."
        ),
        "intro": (
            "Trusted Whirlpool appliance repair for all models — "
            "same-day service with factory-certified technicians"
        ),
        "short_description": "Expert Whirlpool repair — all models, same-day.",
        "hero_usp": (
            "Factory-trained on all Whirlpool models including smart "
            "appliances, French door refrigerators, and HE washers."
        ),
        "body": (
            "<h2>Whirlpool Appliance Repair You Can Trust</h2>"
            "<p>Whirlpool is one of the most common appliance brands in "
            "American homes, and our technicians work on Whirlpool appliances "
            "every day. From French door refrigerators and high-efficiency "
            "washers to smart ovens and quiet dishwashers, we know Whirlpool "
            "inside and out.</p>"
            "<h2>Whirlpool Appliances We Service</h2>"
            "<ul>"
            "<li><strong>Refrigerators:</strong> French door, side-by-side, "
            "top-freezer, bottom-freezer, counter-depth</li>"
            "<li><strong>Washers:</strong> front-load, top-load, "
            "high-efficiency, smart washer models</li>"
            "<li><strong>Dryers:</strong> gas, electric, with steam, "
            "moisture sensing models</li>"
            "<li><strong>Dishwashers:</strong> built-in, third-level rack, "
            "Sensor Cycle, FingerPrint Resistant</li>"
            "<li><strong>Ranges & Ovens:</strong> gas, electric, "
            "convection, double oven, smart models</li>"
            "</ul>"
            "<h2>Common Whirlpool Repairs</h2>"
            "<p>The most frequent Whirlpool issues we see include "
            "refrigerator ice maker failures, washer lid lock errors, "
            "dryer thermal fuse blowouts, and dishwasher drain pump "
            "replacements. We stock OEM parts for all of these common "
            "repairs on our trucks for immediate, same-day fixes.</p>"
            "<h2>Genuine Whirlpool Parts</h2>"
            "<p>We use authentic Whirlpool OEM parts for every repair, "
            "ensuring compatibility, performance, and warranty compliance. "
            "Our trucks carry control boards, compressors, pumps, motors, "
            "igniters, and sensors — the parts that Whirlpool appliances "
            "need most.</p>"
        ),
        "problems": [
            "Whirlpool refrigerator not cooling",
            "Whirlpool washer lid lock error",
            "Whirlpool dryer not heating",
            "Whirlpool dishwasher not draining",
            "Whirlpool ice maker not producing ice",
            "Whirlpool oven not igniting",
            "Whirlpool washer won't spin",
            "Whirlpool dryer squeaking noise",
        ],
    },
    {
        "title": "GE Appliance Repair",
        "slug": "ge-appliance-repair",
        "seo_title": "GE Appliance Repair — Same-Day Service, Certified Techs",
        "search_description": (
            "GE appliance repair — refrigerators, washers, dryers, dishwashers "
            "& ovens. Same-day service, OEM GE parts. Warranty included. "
            "Book today."
        ),
        "intro": (
            "Expert GE appliance repair covering all GE, GE Profile, "
            "and Cafe models — same-day service with OEM parts"
        ),
        "short_description": "Certified GE repair for all models and sub-brands.",
        "hero_usp": (
            "Trained on GE, GE Profile, and Cafe — smart appliances, "
            "French door refrigerators, and commercial-style ranges."
        ),
        "body": (
            "<h2>GE Appliance Repair Specialists</h2>"
            "<p>GE Appliances encompasses multiple product lines — GE, "
            "GE Profile, Cafe, Monogram, and Haier. Each line has unique "
            "technology and parts requirements. Our technicians are "
            "trained across all GE sub-brands and carry the specific "
            "OEM parts needed for your model.</p>"
            "<h2>GE Appliances We Service</h2>"
            "<ul>"
            "<li><strong>Refrigerators:</strong> French door, side-by-side, "
            "top-freezer, bottom-freezer, Profile, Cafe</li>"
            "<li><strong>Washers & Dryers:</strong> top-load, front-load, "
            "UltraFresh, Sapphire Blue, all-in-one combos</li>"
            "<li><strong>Dishwashers:</strong> built-in, portable, Profile, "
            "Cafe with CustomFit racks</li>"
            "<li><strong>Ranges & Ovens:</strong> gas, electric, induction, "
            "double oven, Cafe professional style</li>"
            "</ul>"
            "<h2>Common GE Repairs</h2>"
            "<p>Frequent GE issues include refrigerator motherboard "
            "failures, washer basket hub wear, oven igniter degradation, "
            "and dishwasher circulation pump failures. We carry "
            "replacement parts for all of these on our trucks.</p>"
            "<h2>All GE Sub-Brands Covered</h2>"
            "<p>Whether you own an entry-level GE appliance or a premium "
            "Cafe or Monogram unit, we have the training and parts to "
            "repair it. GE Profile and Cafe models often have unique "
            "features like hot water dispensers and built-in Keurig "
            "systems — our technicians are trained on all of these.</p>"
        ),
        "problems": [
            "GE refrigerator not cooling",
            "GE washer won't drain",
            "GE dryer not heating",
            "GE dishwasher not cleaning",
            "GE oven igniter not working",
            "GE Profile fridge leaking water",
            "GE washer making loud noise",
            "GE Cafe range error codes",
        ],
    },
    {
        "title": "Maytag Appliance Repair",
        "slug": "maytag-appliance-repair",
        "seo_title": "Maytag Appliance Repair — Same-Day Service, OEM Parts",
        "search_description": (
            "Maytag appliance repair — washers, dryers, refrigerators, "
            "dishwashers & ranges. Same-day service with genuine Maytag "
            "parts. Warranty included."
        ),
        "intro": (
            "Reliable Maytag appliance repair for washers, dryers, "
            "refrigerators, and dishwashers — same-day service guaranteed"
        ),
        "short_description": "Trusted Maytag repair with genuine OEM parts.",
        "hero_usp": (
            "Maytag-trained technicians for Pet Pro washers, "
            "commercial-grade dryers, and all Maytag models."
        ),
        "body": (
            "<h2>Maytag Appliance Repair Experts</h2>"
            "<p>Maytag appliances are built for durability, but even the "
            "toughest machines need repair eventually. Our technicians "
            "specialize in Maytag's heavy-duty components — commercial-grade "
            "motors, PowerWash agitators, and Extra Power dryers. We "
            "carry genuine Maytag parts and complete most repairs in a "
            "single visit.</p>"
            "<h2>Maytag Appliances We Repair</h2>"
            "<ul>"
            "<li><strong>Washers:</strong> top-load, front-load, Pet Pro, "
            "Commercial Technology models</li>"
            "<li><strong>Dryers:</strong> gas, electric, Extra Power, "
            "commercial-grade models</li>"
            "<li><strong>Refrigerators:</strong> French door, side-by-side, "
            "bottom-freezer, wide models</li>"
            "<li><strong>Dishwashers:</strong> built-in, Dual Power "
            "filtration, PowerBlast cycle</li>"
            "<li><strong>Ranges:</strong> gas, electric, True Convection, "
            "AquaLift self-clean models</li>"
            "</ul>"
            "<h2>Common Maytag Repairs</h2>"
            "<p>The most common Maytag repairs we handle include washer "
            "transmission failures, dryer drum roller replacements, "
            "refrigerator defrost system repairs, and dishwasher spray "
            "arm replacements. Maytag appliances often use the same "
            "platform as Whirlpool, so our extensive Whirlpool parts "
            "inventory covers many Maytag models as well.</p>"
            "<h2>Built to Last, Fixed to Last</h2>"
            "<p>We match Maytag's durability philosophy with our own: "
            "every repair uses OEM parts and is backed by a warranty on "
            "parts and labor. If the same issue returns, we come back "
            "and fix it free of charge.</p>"
        ),
        "problems": [
            "Maytag washer not spinning",
            "Maytag dryer not heating",
            "Maytag refrigerator not cooling",
            "Maytag dishwasher not cleaning",
            "Maytag washer leaking from bottom",
            "Maytag dryer making loud noise",
            "Maytag oven not reaching temperature",
            "Maytag washer error codes",
        ],
    },
]

SUPPLEMENTAL_SERVICE_PAGES: list[dict[str, Any]] = [
    COMMERCIAL_SERVICE_PAGE,
    HIGH_END_SERVICE_PAGE,
    *HIGH_END_BRAND_SERVICE_PAGES,
    *BRAND_PAGES,
]


def _sync_related_services(
    page: ServicePage,
    service_data: dict[str, Any],
) -> None:
    """Create declared related-service links for existing live English pages."""
    for related_slug in service_data.get("related", []):
        related_page = ServicePage.objects.filter(
            locale=page.locale,
            slug=related_slug,
        ).first()
        if related_page:
            ServiceRelatedService.objects.get_or_create(
                page=page,
                related_service=related_page,
            )


def _declared_related_count(page: ServicePage, service_data: dict[str, Any]) -> int:
    """Return how many declared related links already exist for this page."""
    related_slugs = set(service_data.get("related", []))
    if not related_slugs:
        return 0
    return ServiceRelatedService.objects.filter(
        page=page,
        related_service__slug__in=related_slugs,
    ).count()


class Command(BaseCommand):
    help = "Create supplemental SEO service pages (Issue #26)"

    def handle(self, *args: object, **options: object) -> None:
        try:
            index = ServicesIndexPage.objects.get(locale__language_code="en")
        except ServicesIndexPage.DoesNotExist:
            self.stdout.write(self.style.ERROR("ServicesIndexPage not found"))
            return

        created = 0
        updated = 0
        for service_data in SUPPLEMENTAL_SERVICE_PAGES:
            page = ServicePage.objects.filter(
                locale=index.locale,
                slug=service_data["slug"],
            ).first()
            if page and service_data["slug"] in SEO_LANDING_SERVICE_SLUGS:
                changed = apply_service_page_seed_data(page, service_data)
                before_related = _declared_related_count(page, service_data)
                _sync_related_services(page, service_data)
                after_related = _declared_related_count(page, service_data)
                if changed:
                    page.save()
                    page.save_revision().publish()
                    updated += 1
                    self.stdout.write(self.style.SUCCESS(f"  UPDATE {service_data['title']}"))
                elif after_related > before_related:
                    updated += 1
                    self.stdout.write(self.style.SUCCESS(f"  LINK {service_data['title']}"))
                else:
                    self.stdout.write(f"  OK {service_data['title']} — no changes needed")
                continue

            if page:
                self.stdout.write(
                    f"  '{service_data['slug']}' already exists — skipping"
                )
                continue

            page = ServicePage(
                title=service_data["title"],
                slug=service_data["slug"],
                intro=service_data["intro"],
            )
            apply_service_page_seed_data(page, service_data)
            index.add_child(instance=page)
            page.save_revision().publish()
            _sync_related_services(page, service_data)

            created += 1
            self.stdout.write(self.style.SUCCESS(f"  + {service_data['title']}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"\n{created} service page(s) created, {updated} updated."
            )
        )
