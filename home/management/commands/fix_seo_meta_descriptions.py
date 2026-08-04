"""Trim overly long meta descriptions (search_description) to ≤155 characters.

Targets pages identified in the SEO audit with descriptions >155 chars,
primarily service area pages, some service pages, and the About Us page.
Phone numbers are removed (already in structured data) and text is trimmed
to fit within Google's SERP display limit.
"""

from __future__ import annotations

from django.core.management.base import BaseCommand
from wagtail.models import Page


# Map of URL path → trimmed description (≤155 chars each)
TRIMMED_DESCRIPTIONS: dict[str, str] = {
    # Service pages
    "/services/refrigerator-repair/": (
        "Professional refrigerator repair — same-day service for all brands."
        " Fix cooling issues, leaks, ice makers & compressors. Warranty included."
    ),
    "/services/whirlpool-appliance-repair/": (
        "Whirlpool appliance repair — refrigerators, washers, dryers &"
        " dishwashers. Same-day service with OEM Whirlpool parts. Warranty included."
    ),
    # Service area pages — English
    "/service-areas/appliance-repair-corona-ca/": (
        "Same-day appliance repair in Corona, CA — South Corona, Dos Lagos"
        " & Sierra Del Oro. Refrigerator, washer & dryer repair. $70 diagnostic waived with repair."
    ),
    "/service-areas/appliance-repair-riverside-ca/": (
        "Same-day appliance repair in Riverside, CA — Mission Grove, Canyon"
        " Crest & Arlington. Refrigerator, washer & oven repair. Warranty included."
    ),
    "/service-areas/appliance-repair-beaumont-ca/": (
        "Same-day appliance repair in Beaumont, CA — Four Seasons, Fairway"
        " Canyon & Tournament Hills. Refrigerator & washer repair. Warranty included."
    ),
    "/service-areas/appliance-repair-perris-ca/": (
        "Same-day appliance repair in Perris, CA — May Ranch, Perris Valley"
        " & Good Hope. Refrigerator, washer & dryer repair. Warranty included."
    ),
    "/service-areas/appliance-repair-murrieta-ca/": (
        "Same-day appliance repair in Murrieta, CA — Greer Ranch, Los Alamos"
        " Hills & downtown. Refrigerator, washer & dryer repair. Warranty included."
    ),
    "/service-areas/appliance-repair-temecula-ca/": (
        "Same-day appliance repair in Temecula, CA — Redhawk, Wolf Creek"
        " & Old Town. Refrigerators, washers, dryers & dishwashers. Warranty included."
    ),
    "/service-areas/appliance-repair-canyon-lake-ca/": (
        "Same-day appliance repair in Canyon Lake, CA — serving the gated"
        " community and surrounding areas. Refrigerator, washer & dryer repair."
    ),
    "/service-areas/appliance-repair-lake-elsinore-ca/": (
        "Same-day appliance repair in Lake Elsinore, CA — Diamond Stadium,"
        " Lakepoint & Tuscany Hills. Refrigerator, washer & dryer repair. Warranty included."
    ),
    "/service-areas/appliance-repair-norco-ca/": (
        "Same-day appliance repair in Norco, CA — Horsetown USA."
        " Refrigerators, washers, dryers & dishwashers. $70 diagnostic waived with repair."
    ),
    "/service-areas/appliance-repair-menifee-ca/": (
        "Same-day appliance repair in Menifee, CA — Sun City, Audie Murphy"
        " Ranch & Heritage Lake. Washer, dryer & refrigerator repair. Warranty included."
    ),
    # About Us
    "/about-us/": (
        "Meet the Inland Empire Appliance Repair team — EPA 608 certified technicians"
        " serving the Inland Empire. Same-day service, warranty included."
    ),
    # Spanish service area pages (Wagtail stores these under /home-es/ tree path)
    "/home-es/service-areas/appliance-repair-corona-ca/": (
        "Reparación de electrodomésticos en Corona, CA. Todas las marcas,"
        " garantía incluida. $70 diagnóstico se descuenta con reparación."
    ),
    "/home-es/service-areas/appliance-repair-temecula-ca/": (
        "Reparación de electrodomésticos en Temecula, CA. Residencial y"
        " comercial. Garantía incluida. Diagnóstico $70 se descuenta."
    ),
    "/home-es/service-areas/appliance-repair-lake-elsinore-ca/": (
        "Reparación de electrodomésticos en Lake Elsinore, CA."
        " Refrigeradores, lavadoras, secadoras y hornos. Diagnóstico $70, gratis con reparación."
    ),
}


class Command(BaseCommand):
    help = "Trim meta descriptions exceeding 155 characters (SEO audit fix)."

    def add_arguments(self, parser: object) -> None:
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show changes without saving",
        )

    def handle(self, *args: object, **options: object) -> None:
        dry_run = options["dry_run"]
        updated = 0

        for url_path, new_desc in TRIMMED_DESCRIPTIONS.items():
            char_count = len(new_desc)
            if char_count > 155:
                self.stderr.write(
                    self.style.WARNING(
                        f"  WARNING: New description for {url_path} is"
                        f" {char_count} chars (should be ≤155)"
                    )
                )

            # Find page by URL path
            page = Page.objects.filter(url_path__endswith=url_path).first()
            if not page:
                # Try with /home prefix (Wagtail stores full tree paths)
                self.stderr.write(
                    self.style.WARNING(f"  Page not found for {url_path}")
                )
                continue

            specific = page.specific
            old_desc = specific.search_description or ""

            if old_desc == new_desc:
                self.stdout.write(f"  {url_path}: already correct")
                continue

            if dry_run:
                self.stdout.write(
                    f"  [DRY RUN] {url_path}:\n"
                    f"    OLD [{len(old_desc)}]: {old_desc[:80]}...\n"
                    f"    NEW [{char_count}]: {new_desc[:80]}..."
                )
            else:
                specific.search_description = new_desc
                specific.save_revision().publish()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  {url_path}: [{len(old_desc)}] → [{char_count}] chars"
                    )
                )
            updated += 1

        action = "would update" if dry_run else "updated"
        self.stdout.write(
            self.style.SUCCESS(f"\nDone: {action} {updated} meta descriptions.")
        )
