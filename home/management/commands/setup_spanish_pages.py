"""
Management command to create Spanish translations of all English pages.

Run with: python manage.py setup_spanish_pages

Idempotent — safe to run multiple times. Skips pages that already have
Spanish translations. Does NOT modify English pages.
"""

from __future__ import annotations

import logging
from typing import Any

from django.core.management.base import BaseCommand
from wagtail.models import Locale, Page

from blog.models import BlogIndexPage, BlogPage
from home.models import HomePage
from locations.models import (
    CityFeaturedService,
    CityNearbyCity,
    CityPage,
    LocationsIndexPage,
)
from pages.models import StaticPage
from services.models import ServicePage, ServiceRelatedService, ServicesIndexPage

logger = logging.getLogger(__name__)

# ── Translation data ──────────────────────────────────────────────────

SERVICE_TRANSLATIONS: dict[str, dict[str, str]] = {
    "refrigerator-repair": {
        "title": "Reparación de Refrigeradores",
        "intro": "Servicios profesionales de reparación de refrigeradores.",
        "short_description": "Solucione problemas de enfriamiento, fugas y ruidos extraños.",
        "hero_usp": "Reparación de refrigeradores el mismo día. Reparamos todas las marcas.",
    },
    "freezer-repair": {
        "title": "Reparación de Congeladores",
        "intro": "Servicios profesionales de reparación de congeladores.",
        "short_description": "Restaure la congelación adecuada y detenga la acumulación de hielo.",
        "hero_usp": "Reparación de congeladores el mismo día. Reparamos todas las marcas.",
    },
    "washer-repair": {
        "title": "Reparación de Lavadoras",
        "intro": "Servicios profesionales de reparación de lavadoras.",
        "short_description": "Solucione fugas, problemas de centrifugado y drenaje.",
        "hero_usp": "Reparación de lavadoras el mismo día. Reparamos todas las marcas.",
    },
    "dryer-repair": {
        "title": "Reparación de Secadoras",
        "intro": "Servicios profesionales de reparación de secadoras.",
        "short_description": "Restaure el calor y los ciclos de secado adecuados.",
        "hero_usp": "Reparación de secadoras el mismo día. Reparamos todas las marcas.",
    },
    "dishwasher-repair": {
        "title": "Reparación de Lavavajillas",
        "intro": "Servicios profesionales de reparación de lavavajillas.",
        "short_description": "Solucione problemas de limpieza, drenaje y puerta.",
        "hero_usp": "Reparación de lavavajillas el mismo día. Reparamos todas las marcas.",
    },
    "oven-repair": {
        "title": "Reparación de Hornos",
        "intro": "Servicios profesionales de reparación de hornos.",
        "short_description": "Restaure el calentamiento y control de temperatura adecuados.",
        "hero_usp": "Reparación de hornos el mismo día. Reparamos todas las marcas.",
    },
    "stove-repair": {
        "title": "Reparación de Estufas",
        "intro": "Servicios profesionales de reparación de estufas.",
        "short_description": "Solucione problemas de quemadores, encendido y resistencias.",
        "hero_usp": "Reparación de estufas el mismo día. Reparamos todas las marcas.",
    },
    "water-heater-repair": {
        "title": "Reparación de Calentadores de Agua",
        "intro": "Servicios profesionales de reparación de calentadores de agua.",
        "short_description": "Restaure el agua caliente y solucione fugas rápidamente.",
        "hero_usp": "Reparación de calentadores de agua el mismo día. Reparamos todas las marcas.",
    },
    "air-conditioning-repair-hvac": {
        "title": "Reparación de Aire Acondicionado (HVAC)",
        "intro": "Servicios profesionales de reparación de aire acondicionado.",
        "short_description": "Solucione problemas de enfriamiento y mejore la eficiencia.",
        "hero_usp": "Reparación de aire acondicionado el mismo día. Reparamos todas las marcas.",
    },
    "microwave-repair": {
        "title": "Reparación de Microondas",
        "intro": "Servicios profesionales de reparación de microondas.",
        "short_description": "Solucione problemas de calentamiento, plato giratorio y puerta.",
        "hero_usp": "Reparación de microondas el mismo día. Reparamos todas las marcas.",
    },
}

_CITY_NAMES = [
    "Corona",
    "Riverside",
    "Beaumont",
    "Perris",
    "Murrieta",
    "Temecula",
    "Canyon Lake",
    "Lake Elsinore",
    "Norco",
    "Menifee",
]

CITY_TRANSLATIONS: dict[str, dict[str, str]] = {
    f"appliance-repair-{name.lower().replace(' ', '-')}-ca": {
        "title": name,
        "intro": f"Reparación de electrodomésticos el mismo día en {name}, CA.",
        "hero_usp": f"Reparación profesional y rápida de electrodomésticos en {name}.",
    }
    for name in _CITY_NAMES
}


# ── Command ───────────────────────────────────────────────────────────


class Command(BaseCommand):
    help = "Create Spanish translations of all English pages (idempotent)"

    def handle(self, *args: Any, **options: Any) -> None:
        en_count = (
            Page.objects.filter(locale__language_code="en").exclude(depth__lt=2).count()
        )
        if en_count == 0:
            self.stderr.write(
                self.style.ERROR("No English pages found. Run setup_pages first.")
            )
            return

        es_locale, created = Locale.objects.get_or_create(language_code="es")
        if created:
            self.stdout.write(self.style.SUCCESS("Created Spanish locale"))
        else:
            self.stdout.write("Spanish locale already exists")

        # Track en_pk → es_pk for fixing inline-panel foreign keys later
        service_map: dict[int, int] = {}
        city_map: dict[int, int] = {}

        # Process every English page in tree order (parents before children)
        en_pages = (
            Page.objects.filter(locale__language_code="en")
            .exclude(depth__lt=2)
            .order_by("path")
            .specific()
        )

        created_count = 0
        skipped_count = 0

        for page in en_pages:
            if Page.objects.filter(
                translation_key=page.translation_key,
                locale=es_locale,
            ).exists():
                self.stdout.write(f'  SKIP  "{page.title}"')
                skipped_count += 1
                continue

            try:
                es_page = page.copy_for_translation(es_locale)
                es_specific = es_page.specific
                _apply_translation(es_specific, page)
                es_specific.save()
                es_specific.save_revision().publish()

                if isinstance(page, ServicePage):
                    service_map[page.pk] = es_specific.pk
                elif isinstance(page, CityPage):
                    city_map[page.pk] = es_specific.pk

                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  +     "{es_specific.title}"'))

            except Exception as e:
                self.stderr.write(self.style.ERROR(f'  ERROR "{page.title}": {e}'))
                logger.exception("Failed to translate page %s", page.title)

        # Fix inline-panel foreign keys to point at Spanish pages
        _fix_city_featured_services(service_map, es_locale)
        _fix_city_nearby_cities(city_map, es_locale)
        _fix_related_services(service_map, es_locale)

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone! Created {created_count}, skipped {skipped_count}."
            )
        )


# ── Translation helpers ───────────────────────────────────────────────


def _apply_translation(es_page: Page, en_page: Page) -> None:
    """Set Spanish content on the translated page copy."""
    if isinstance(en_page, HomePage):
        es_page.title = "Inicio"

    elif isinstance(en_page, ServicesIndexPage):
        es_page.title = "Servicios"
        es_page.hero_title = "Servicios de Reparación de Electrodomésticos"
        es_page.hero_subtitle = (
            "Reparación experta para todos los electrodomésticos principales. "
            "Servicio rápido, confiable y económico."
        )

    elif isinstance(en_page, ServicePage):
        t = SERVICE_TRANSLATIONS.get(en_page.slug, {})
        for field, value in t.items():
            setattr(es_page, field, value)

    elif isinstance(en_page, LocationsIndexPage):
        es_page.title = "Áreas de Servicio"
        es_page.intro = (
            "<p>Servimos con orgullo al Sur de California con "
            "reparación de electrodomésticos rápida y confiable.</p>"
        )

    elif isinstance(en_page, CityPage):
        t = CITY_TRANSLATIONS.get(en_page.slug, {})
        for field, value in t.items():
            setattr(es_page, field, value)

    elif isinstance(en_page, StaticPage):
        if en_page.slug == "about-us":
            es_page.title = "Sobre Nosotros"
            es_page.hero_title = "Sobre Nosotros"
            es_page.hero_subtitle = (
                "Sus expertos confiables en reparación de electrodomésticos."
            )
            es_page.body = (
                "<p>Nos especializamos en reparación de electrodomésticos "
                "residenciales y comerciales con enfoque en calidad, "
                "confiabilidad y satisfacción del cliente.</p>"
            )
            es_page.cta_title = "¿Listo para Comenzar?"
            es_page.cta_text = (
                "Reserve su servicio de reparación de electrodomésticos hoy."
            )
            es_page.cta_button_text = "Reservar Ahora"
        elif en_page.slug == "contact":
            es_page.title = "Contacto"
            es_page.hero_title = "Contáctenos"
            es_page.hero_subtitle = (
                "Estamos aquí para ayudarle con todas sus necesidades "
                "de reparación de electrodomésticos."
            )
            es_page.body = (
                "<p>¿Tiene preguntas? Complete el formulario a continuación "
                "o llámenos directamente.</p>"
            )
            es_page.cta_title = "¿Listo para Comenzar?"
            es_page.cta_text = (
                "Reserve su servicio de reparación de electrodomésticos hoy."
            )
            es_page.cta_button_text = "Reservar Ahora"

    elif isinstance(en_page, BlogIndexPage):
        es_page.title = "Blog"
        es_page.hero_title = "Nuestro Blog"
        es_page.hero_subtitle = (
            "Consejos, guías e información sobre el cuidado "
            "y reparación de electrodomésticos."
        )

    elif isinstance(en_page, BlogPage):
        # Blog posts need manual content translation in Wagtail admin
        pass


# ── Fix inline-panel foreign keys ─────────────────────────────────────


def _fix_city_featured_services(
    service_map: dict[int, int],
    es_locale: Locale,
) -> None:
    """Point CityFeaturedService FKs at Spanish service pages."""
    if not service_map:
        return
    for city in CityPage.objects.filter(locale=es_locale):
        for fs in CityFeaturedService.objects.filter(page=city):
            es_pk = service_map.get(fs.service_id)
            if es_pk:
                fs.service_id = es_pk
                fs.save()


def _fix_city_nearby_cities(
    city_map: dict[int, int],
    es_locale: Locale,
) -> None:
    """Point CityNearbyCity FKs at Spanish city pages."""
    if not city_map:
        return
    for city in CityPage.objects.filter(locale=es_locale):
        for nc in CityNearbyCity.objects.filter(page=city):
            es_pk = city_map.get(nc.nearby_city_id)
            if es_pk:
                nc.nearby_city_id = es_pk
                nc.save()


def _fix_related_services(
    service_map: dict[int, int],
    es_locale: Locale,
) -> None:
    """Point ServiceRelatedService FKs at Spanish service pages."""
    if not service_map:
        return
    for svc in ServicePage.objects.filter(locale=es_locale):
        for rs in ServiceRelatedService.objects.filter(page=svc):
            es_pk = service_map.get(rs.related_service_id)
            if es_pk:
                rs.related_service_id = es_pk
                rs.save()
