"""Add FAQ items to brand service pages (Samsung, LG, Whirlpool, GE, Maytag).

These pages had zero FAQ items, missing out on FAQPage schema rich results
and long-tail keyword coverage. Each brand gets 5-6 brand-specific FAQs.
"""

from __future__ import annotations

import json

from django.core.management.base import BaseCommand

from services.models import ServicePage


BRAND_FAQS: dict[str, list[dict[str, str]]] = {
    "samsung-appliance-repair": [
        {
            "question": "How much does Samsung appliance repair cost?",
            "answer": (
                "Samsung repair costs vary by appliance and issue. Our"
                " diagnostic is $70, waived when you approve the repair."
                " Most Samsung repairs range from $150 to $400 depending"
                " on the part and labor involved."
            ),
        },
        {
            "question": "Do you use genuine Samsung parts?",
            "answer": (
                "Yes, we use OEM and manufacturer-approved Samsung parts"
                " whenever possible. Our trucks carry common Samsung"
                " replacement parts so most repairs are completed in a"
                " single visit."
            ),
        },
        {
            "question": "What Samsung error codes do you fix?",
            "answer": (
                "We diagnose and repair all Samsung error codes including"
                " refrigerator codes (22E, 5E, 8E), washer codes (UE, DC,"
                " LE), dryer codes (HE, tE, bE), and dishwasher codes."
                " Our technicians have Samsung-specific diagnostic tools."
            ),
        },
        {
            "question": "Can you fix Samsung smart home features?",
            "answer": (
                "Yes, we repair Samsung SmartThings-connected appliances"
                " including Wi-Fi connectivity issues, touchscreen"
                " problems, and smart diagnostic features. We also fix"
                " Family Hub refrigerator screens and software issues."
            ),
        },
        {
            "question": "How long does Samsung appliance repair take?",
            "answer": (
                "Most Samsung repairs are completed in one visit, typically"
                " 45 minutes to 2 hours depending on the issue. If a"
                " specialized part needs to be ordered, we schedule a"
                " follow-up visit as soon as the part arrives."
            ),
        },
    ],
    "lg-appliance-repair": [
        {
            "question": "How much does LG appliance repair cost?",
            "answer": (
                "LG repair costs depend on the appliance type and issue."
                " Our diagnostic fee is $70, waived with repair. Most LG"
                " repairs range from $150 to $400. We provide an upfront"
                " quote before starting any work."
            ),
        },
        {
            "question": "Do you repair LG linear compressor refrigerators?",
            "answer": (
                "Yes, we specialize in LG linear compressor repairs and"
                " replacements. These compressors are common in LG"
                " refrigerators and can fail over time. We carry"
                " replacement compressors and can complete most repairs"
                " the same day."
            ),
        },
        {
            "question": "Can you fix LG inverter direct drive washers?",
            "answer": (
                "Absolutely. We repair LG Inverter Direct Drive washers"
                " including motor issues, bearing failures, drum problems,"
                " and control board errors. Our technicians are trained on"
                " LG's direct drive technology."
            ),
        },
        {
            "question": "What LG error codes do you service?",
            "answer": (
                "We diagnose all LG error codes including washer codes"
                " (UE, OE, DE, LE), dryer codes (d80, d90, d95),"
                " refrigerator codes (Er IF, Er dH), and dishwasher"
                " codes. Each error is diagnosed on-site with professional"
                " tools."
            ),
        },
        {
            "question": "Do you use genuine LG parts?",
            "answer": (
                "Yes, we use OEM LG parts for all repairs. Our trucks are"
                " stocked with common LG replacement parts including"
                " compressors, motors, control boards, and door seals for"
                " fast, same-day service."
            ),
        },
    ],
    "whirlpool-appliance-repair": [
        {
            "question": "How much does Whirlpool appliance repair cost?",
            "answer": (
                "Whirlpool repair costs vary by appliance and issue. Our"
                " diagnostic is $70, waived with repair. Most Whirlpool"
                " repairs fall between $150 and $400. We give you an"
                " itemized quote before starting work."
            ),
        },
        {
            "question": "Do you repair Whirlpool Duet washers and dryers?",
            "answer": (
                "Yes, we service all Whirlpool Duet models including"
                " common issues like F21 drain errors, bearing failures,"
                " and control board problems. We carry Duet-specific"
                " parts on our trucks for same-day repair."
            ),
        },
        {
            "question": "Can you fix Whirlpool ice maker problems?",
            "answer": (
                "Absolutely. We repair all Whirlpool ice maker issues"
                " including no ice production, small or hollow cubes,"
                " water leaks, and jammed dispensers. Most ice maker"
                " repairs are completed in a single visit."
            ),
        },
        {
            "question": "Do you use genuine Whirlpool parts?",
            "answer": (
                "Yes, we use OEM Whirlpool parts for all repairs. As one"
                " of the most common brands in American homes, we keep a"
                " full stock of Whirlpool components on every truck for"
                " fast, reliable repairs."
            ),
        },
        {
            "question": "Do you repair Whirlpool commercial appliances?",
            "answer": (
                "Yes, our EPA 608 certified technicians service both"
                " residential and commercial Whirlpool units. This"
                " includes commercial-grade refrigeration, laundry"
                " equipment, and dishwashers used in restaurants and"
                " businesses."
            ),
        },
    ],
    "ge-appliance-repair": [
        {
            "question": "How much does GE appliance repair cost?",
            "answer": (
                "GE repair costs depend on the appliance and issue. Our"
                " diagnostic fee is $70, waived when you approve the"
                " repair. Most GE repairs range from $150 to $400"
                " including parts and labor."
            ),
        },
        {
            "question": "Do you repair GE Profile and Cafe series?",
            "answer": (
                "Yes, we service all GE product lines including GE"
                " Profile, GE Cafe, GE Monogram, and standard GE"
                " appliances. Our technicians are trained on the"
                " advanced features and electronics in premium GE"
                " models."
            ),
        },
        {
            "question": "Can you fix GE refrigerator water dispensers?",
            "answer": (
                "Absolutely. We repair GE water dispenser issues"
                " including low water pressure, leaks, no water flow,"
                " and temperature problems. We also service water filters"
                " and ice/water combo dispensers."
            ),
        },
        {
            "question": "Do you use genuine GE parts?",
            "answer": (
                "Yes, we use OEM GE Appliances parts for all repairs."
                " GE is one of the most popular brands in American homes,"
                " and we stock common GE replacement parts on every truck"
                " for same-day service."
            ),
        },
        {
            "question": "What GE appliance error codes do you fix?",
            "answer": (
                "We diagnose and repair all GE error codes including"
                " dishwasher codes (flood, pressure), oven codes (F2,"
                " F3, F7), and refrigerator temperature alerts. Our"
                " technicians use GE-specific diagnostic procedures."
            ),
        },
    ],
    "maytag-appliance-repair": [
        {
            "question": "How much does Maytag appliance repair cost?",
            "answer": (
                "Maytag repair costs vary depending on the appliance and"
                " issue. Our diagnostic is $70, waived with repair. Most"
                " Maytag repairs range from $150 to $400 including parts"
                " and labor. No surprise charges."
            ),
        },
        {
            "question": "Do you repair Maytag commercial-grade washers?",
            "answer": (
                "Yes, we service Maytag Commercial Technology washers and"
                " dryers, which are built for heavy-duty residential and"
                " commercial use. We repair motor issues, drum problems,"
                " control board failures, and agitator malfunctions."
            ),
        },
        {
            "question": "Are Maytag appliances worth repairing?",
            "answer": (
                "In most cases, yes. Maytag builds durable, long-lasting"
                " appliances. If your Maytag is less than 10 years old,"
                " repair is almost always more cost-effective than"
                " replacement. We provide honest advice on repair vs."
                " replace during our diagnostic visit."
            ),
        },
        {
            "question": "Do you use genuine Maytag parts?",
            "answer": (
                "Yes, we use OEM Maytag parts for all repairs. Since"
                " Maytag is part of the Whirlpool family, many parts are"
                " shared across brands, which means we carry them on our"
                " trucks for same-day repair."
            ),
        },
        {
            "question": "Can you fix Maytag Bravos washer issues?",
            "answer": (
                "Absolutely. We repair all Maytag Bravos washer problems"
                " including lid lock errors, spin cycle issues, drainage"
                " problems, and excessive vibration. We also service"
                " Maytag Centennial and Maxima models."
            ),
        },
    ],
}


class Command(BaseCommand):
    help = "Add FAQ items to brand service pages (Samsung, LG, Whirlpool, GE, Maytag)"

    def add_arguments(self, parser: object) -> None:
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show changes without saving",
        )

    def handle(self, *args: object, **options: object) -> None:
        dry_run = options["dry_run"]
        updated = 0

        for slug, faqs in BRAND_FAQS.items():
            page = (
                ServicePage.objects.live()
                .filter(slug=slug, locale__language_code="en")
                .first()
            )
            if not page:
                self.stderr.write(self.style.WARNING(f"  Page not found: {slug}"))
                continue

            existing_count = len(page.faq) if page.faq else 0
            if existing_count > 0:
                self.stdout.write(
                    f"  {page.title}: already has {existing_count} FAQs, skipping"
                )
                continue

            if dry_run:
                self.stdout.write(
                    f"  [DRY RUN] {page.title}: would add {len(faqs)} FAQs"
                )
                for faq in faqs:
                    self.stdout.write(f"    Q: {faq['question']}")
            else:
                # Build StreamField data
                faq_data = [
                    {
                        "type": "faq_item",
                        "value": {
                            "question": faq["question"],
                            "answer": faq["answer"],
                        },
                    }
                    for faq in faqs
                ]
                page.faq = json.dumps(faq_data)
                page.save_revision().publish()
                self.stdout.write(
                    self.style.SUCCESS(f"  {page.title}: added {len(faqs)} FAQ items")
                )
            updated += 1

        action = "would update" if dry_run else "updated"
        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone: {action} {updated} brand service pages with FAQs."
            )
        )
