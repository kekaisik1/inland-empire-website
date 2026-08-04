"""
Management command to create Spanish translations of all English pages.

Run with: python manage.py setup_spanish_pages

Idempotent — safe to run multiple times. Skips pages that already have
Spanish translations. Does NOT modify English pages.
"""

from __future__ import annotations

import logging
from typing import Any

from django.core.management import call_command
from django.core.management.base import BaseCommand
from wagtail.models import Locale, Page

from blog.models import BlogIndexPage, BlogPage
from home.models import HomePage
from home.management.commands.populate_spanish_content import (
    SERVICE_CONTENT as FULL_SPANISH_SERVICE_CONTENT,
)
from home.management.commands.create_brand_pages import BRAND_PAGES
from home.management.commands.setup_pages import SERVICE_CONTENT as ENGLISH_CORE_SERVICES
from home.high_end_brand_seed_data import (
    HIGH_END_BRAND_SERVICE_PAGES,
    SPANISH_HIGH_END_BRAND_SERVICE_PAGES,
)
from home.service_seed_data import (
    COMMERCIAL_SERVICE_PAGE,
    HIGH_END_SERVICE_PAGE,
    SPANISH_COMMERCIAL_SERVICE_PAGE,
    SPANISH_HIGH_END_SERVICE_PAGE,
    SPANISH_PRIMARY_BRAND_SERVICE_PAGES,
    reconcile_service_page_seed_data,
)
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

SERVICE_TRANSLATIONS: dict[str, dict[str, Any]] = {
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
        "seo_title": "Reparación de Lavavajillas — Servicio el Mismo Día",
        "search_description": (
            "Reparación de lavavajillas el mismo día para problemas de limpieza, "
            "drenaje, fugas, puerta y ciclos. Diagnóstico claro y garantía incluida."
        ),
        "intro": "Servicio confiable de reparación de lavavajillas para hogares locales.",
        "short_description": (
            "Solucione problemas de limpieza, drenaje, fugas y puerta del lavavajillas."
        ),
        "hero_usp": "Reparación de lavavajillas el mismo día. Reparamos todas las marcas.",
        "body": (
            "<h2>Servicio confiable de reparación de lavavajillas</h2>"
            "<p>Cuando el lavavajillas no limpia, no drena, gotea o deja ciclos "
            "incompletos, Inland Empire Appliance Repair diagnostica la causa y "
            "explica sus opciones antes de comenzar el trabajo aprobado.</p>"
            "<h2>Lo que otros no pudieron reparar</h2>"
            "<p>Revisamos bombas, válvulas, sensores, brazos rociadores, sellos de "
            "puerta, controles, mangueras y conexiones de instalación para encontrar "
            "la falla real, no solo el síntoma visible.</p>"
            "<h2>Soporte profesional de instalación</h2>"
            "<p>Si la falla está relacionada con nivelación, drenaje, suministro de "
            "agua o una instalación reciente, el técnico lo documenta y le da una "
            "recomendación clara.</p>"
        ),
        "problems": [
            "Problemas comunes de lavavajillas",
            "Lavavajillas no drena",
            "Platos quedan sucios después del ciclo",
            "Fuga de agua debajo o frente a la puerta",
            "Lavavajillas no inicia o se detiene a mitad del ciclo",
            "Olores, residuos o agua estancada",
            "Ruido fuerte durante lavado o drenaje",
            "Problemas de instalación, nivelación o conexión de agua",
        ],
        "benefits": [
            (
                "Todas las marcas",
                "Diagnosticamos marcas principales y modelos comunes de lavavajillas residenciales.",
            ),
            (
                "Diagnóstico rápido",
                "Identificamos la causa probable antes de recomendar piezas o trabajo adicional.",
            ),
            (
                "Piezas disponibles",
                "Los camiones llevan piezas frecuentes para completar muchas reparaciones en una sola visita.",
            ),
            (
                "Trabajo limpio",
                "Protegemos el área de cocina y dejamos el espacio ordenado después del servicio.",
            ),
        ],
        "faq": [
            (
                "¿Cuánto cuesta reparar un lavavajillas?",
                "El costo depende de la falla y las piezas necesarias. Damos una cotización clara después del diagnóstico y antes de cualquier reparación aprobada.",
            ),
            (
                "¿Por qué mi lavavajillas no drena?",
                "Puede deberse a una bomba, filtro, manguera, triturador, válvula o problema de instalación. Un técnico revisa el recorrido de drenaje antes de reemplazar piezas.",
            ),
            (
                "¿Vale la pena reparar un lavavajillas?",
                "Si la unidad está en buen estado y la falla es de bomba, sello, válvula, sensor o control, reparar suele tener sentido. Le explicamos cuándo reemplazar conviene más.",
            ),
            (
                "¿Reparan problemas después de una instalación?",
                "Sí. Revisamos nivelación, suministro de agua, drenaje, anclaje y conexiones visibles para detectar problemas relacionados con instalación.",
            ),
        ],
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
    "garbage-disposal-repair": {
        "title": "Reparación de Trituradores de Basura",
        "seo_title": "Reparación de Trituradores de Basura — Servicio el Mismo Día",
        "search_description": (
            "Reparación de trituradores de basura el mismo día para atascos, fugas, "
            "motores con zumbidos y retornos de drenaje. Diagnóstico claro y garantía incluida."
        ),
        "intro": (
            "Reparación rápida de trituradores de basura atascados, con fugas, "
            "zumbidos o retornos de drenaje."
        ),
        "short_description": (
            "Reparamos trituradores atascados, con fugas, zumbidos o retornos de drenaje."
        ),
        "hero_usp": (
            "Ayuda el mismo día para cuchillas trabadas, fugas, obstrucciones y "
            "motores de triturador."
        ),
        "body": (
            "<h2>Reparación de Trituradores de Basura para Cocinas Activas</h2>"
            "<p>Un triturador que zumba, gotea, se atasca o regresa agua puede detener "
            "toda la cocina. Inland Empire Appliance Repair revisa el reinicio "
            "eléctrico, el montaje, los sellos, el volante y la conexión de drenaje, "
            "y explica si reparar o reemplazar es la mejor opción.</p>"
            "<h2>Atascos, Fugas, Olores y Retornos de Drenaje</h2>"
            "<p>Atendemos impulsores trabados, protectores de sobrecarga disparados, "
            "protectores contra salpicaduras desgastados, bridas flojas, entradas de "
            "lavavajillas con fugas y conexiones de drenaje del triturador.</p>"
            "<h2>Diagnóstico Claro de Electrodomésticos de Cocina</h2>"
            "<p>Su técnico entrega una cotización por adelantado. Las reparaciones "
            "aprobadas incluyen garantía en piezas y mano de obra.</p>"
        ),
        "problems": [
            "Triturador de basura zumba pero no gira",
            "Triturador atascado o trabado",
            "Agua goteando debajo del fregadero",
            "El triturador dispara el botón de reinicio",
            "Malos olores del triturador",
            "Lavavajillas regresa agua al fregadero",
            "Anillo de montaje o protector contra salpicaduras flojo",
            "Drenaje de cocina lento después de usar el triturador",
        ],
        "benefits": [
            (
                "Ayuda de Cocina el Mismo Día",
                "Hay citas disponibles rápidamente para fallas comunes del triturador y fugas bajo el fregadero.",
            ),
            (
                "Guía para Reparar o Reemplazar",
                "Explicamos si el triturador se puede reparar de forma segura o si conviene reemplazarlo.",
            ),
            (
                "Revisión de Conexiones de Drenaje",
                "Inspeccionamos el triturador, la entrada del lavavajillas, la brida y el drenaje en conjunto.",
            ),
            (
                "Garantía Incluida",
                "Las reparaciones aprobadas incluyen cobertura en piezas y mano de obra.",
            ),
        ],
        "faq": [
            (
                "¿Por qué mi triturador de basura zumba pero no gira?",
                "Normalmente está atascado, tiene el volante trabado o un motor fallando. Apáguelo y no siga intentando usarlo; un técnico puede diagnosticar la causa con seguridad.",
            ),
            (
                "¿Pueden reparar un triturador de basura con fugas?",
                "Sí. Revisamos la brida, el montaje, la entrada del lavavajillas, la salida de drenaje, los sellos y la carcasa.",
            ),
            (
                "¿Vale la pena reparar un triturador de basura?",
                "Si la unidad es reciente y el problema es un atasco, sello, reinicio o conexión, reparar suele tener sentido.",
            ),
            (
                "¿Reparan trituradores conectados a lavavajillas?",
                "Sí. Inspeccionamos las conexiones y el recorrido de drenaje cuando el lavavajillas regresa agua.",
            ),
        ],
    },
    "cooktop-repair": {
        "title": "Reparación de Cubiertas de Cocina",
        "seo_title": (
            "Reparación de Cubiertas de Cocina — Servicio de Gas, Eléctrico e Inducción"
        ),
        "search_description": (
            "Reparación de cubiertas de cocina de gas, eléctricas e inducción. "
            "Solucionamos quemadores que no encienden, no calientan parejo o no responden."
        ),
        "intro": (
            "Reparación de cubiertas de cocina de gas, eléctricas e inducción que "
            "no calientan, no encienden o no responden."
        ),
        "short_description": (
            "Reparamos problemas de quemadores en cubiertas de gas, eléctricas y de inducción."
        ),
        "hero_usp": (
            "Diagnóstico el mismo día para fallas de encendido, elementos, vidrio "
            "cerámico y controles."
        ),
        "body": (
            "<h2>Reparación de Cubiertas de Gas, Eléctricas e Inducción</h2>"
            "<p>Cuando un quemador no enciende, no calienta parejo o no responde a "
            "los controles, Inland Empire Appliance Repair realiza pruebas claras "
            "antes de reemplazar piezas.</p>"
            "<h2>Quemadores, Encendedores, Elementos y Controles</h2>"
            "<p>Revisamos chispa, puertos de quemador, elementos radiantes, "
            "interruptores, perillas, cableado y códigos de error de inducción.</p>"
            "<h2>Servicio Seguro para Electrodomésticos de Cocina</h2>"
            "<p>El técnico explica el diagnóstico, entrega una cotización detallada y "
            "respalda las reparaciones aprobadas con garantía.</p>"
        ),
        "problems": [
            "Quemador de gas no enciende",
            "Elemento eléctrico no calienta",
            "Código de error en cubierta de inducción",
            "Quemador calienta disparejo o se queda en alto",
            "Encendedor sigue haciendo clic",
            "Perilla o control no responde",
            "Zona de calor de vidrio cerámico falló",
            "La cubierta dispara el breaker",
        ],
        "benefits": [
            (
                "Gas, Eléctrico e Inducción",
                "Diagnosticamos tipos comunes de cubiertas y explicamos opciones seguras.",
            ),
            (
                "Pruebas de Control y Elementos",
                "Probamos encendedores, interruptores, elementos, controles y cableado visible.",
            ),
            (
                "Cotización Clara por Adelantado",
                "Usted aprueba la reparación después de conocer el diagnóstico y el precio.",
            ),
            (
                "Garantía Incluida",
                "Las reparaciones aprobadas incluyen garantía en piezas y mano de obra.",
            ),
        ],
        "faq": [
            (
                "¿Por qué mi cubierta de gas no enciende?",
                "Puede deberse a un puerto obstruido, encendedor sucio, módulo de chispa, conexión o flujo de gas. Probamos el sistema antes de reemplazar piezas.",
            ),
            (
                "¿Reparan cubiertas eléctricas de vidrio?",
                "Sí. Diagnosticamos elementos radiantes, interruptores, controles, cableado y energía.",
            ),
            (
                "¿Dan servicio a cubiertas de inducción?",
                "Sí. Diagnosticamos muchos códigos de error, problemas de control y fallas de calentamiento.",
            ),
            (
                "¿Se puede reparar una cubierta de vidrio agrietada?",
                "Una superficie agrietada normalmente requiere reemplazar el vidrio. Explicamos disponibilidad y costo antes de continuar.",
            ),
        ],
    },
    "ice-maker-repair": {
        "title": "Reparación de Máquinas de Hielo",
        "seo_title": (
            "Reparación de Máquinas de Hielo — Refrigeradores y Unidades Independientes"
        ),
        "search_description": (
            "Reparación de máquinas de hielo en refrigeradores y unidades independientes. "
            "Solucione falta de hielo, fugas, obstrucciones y líneas congeladas."
        ),
        "intro": (
            "Reparación de máquinas de hielo de refrigeradores y unidades independientes "
            "con fugas, obstrucciones o falta de producción."
        ),
        "short_description": (
            "Solucione problemas de máquinas de hielo sin producción, con fugas u obstruidas."
        ),
        "hero_usp": (
            "Diagnóstico el mismo día para válvulas, líneas congeladas, sensores, "
            "fugas y dispensadores."
        ),
        "body": (
            "<h2>Reparación de Máquinas de Hielo</h2>"
            "<p>Una máquina que deja de producir, gotea o hace cubos pequeños puede "
            "indicar problemas de agua, temperatura, válvula, sensor, filtro o control. "
            "Inland Empire Appliance Repair prepara un plan práctico de reparación.</p>"
            "<h2>Sin Hielo, Fugas y Líneas Congeladas</h2>"
            "<p>Inspeccionamos la válvula, línea de agua, filtro, molde, sensor, "
            "dispensador y temperatura del congelador para encontrar la causa real.</p>"
            "<h2>Servicio con Garantía</h2>"
            "<p>El técnico entrega una cotización antes de comenzar. Las reparaciones "
            "aprobadas incluyen cobertura de garantía.</p>"
        ),
        "problems": [
            "Máquina de hielo no produce hielo",
            "Cubos de hielo pequeños o huecos",
            "Máquina de hielo con fuga de agua",
            "Tubo de llenado o línea de agua congelada",
            "Dispensador de hielo no funciona",
            "Máquina de hielo se desborda",
            "Mal sabor u olor en el hielo",
            "Máquina de hielo independiente no da abasto",
        ],
        "benefits": [
            (
                "Refrigeradores y Unidades Independientes",
                "Diagnosticamos máquinas integradas y muchas unidades independientes.",
            ),
            (
                "Revisiones de Agua y Temperatura",
                "Inspeccionamos suministro, filtros, válvulas, sensores y temperatura.",
            ),
            (
                "Diagnóstico de Causa Raíz",
                "Si el problema proviene de una falla de enfriamiento, también la identificamos.",
            ),
            (
                "Garantía Incluida",
                "Las reparaciones aprobadas incluyen garantía en piezas y mano de obra.",
            ),
        ],
        "faq": [
            (
                "¿Por qué mi máquina de hielo dejó de producir hielo?",
                "Puede deberse a un tubo congelado, filtro obstruido, válvula, brazo de apagado, sensor o temperatura del congelador.",
            ),
            (
                "¿Pueden reparar una máquina de hielo que gotea?",
                "Sí. Revisamos la línea de agua, válvula, molde, drenaje y dispensador.",
            ),
            (
                "¿Reparan máquinas de hielo independientes?",
                "Diagnosticamos muchas unidades residenciales y comerciales ligeras cuando hay acceso y piezas.",
            ),
            (
                "¿Por qué mis cubos salen pequeños o huecos?",
                "Suele deberse a flujo de agua restringido, filtro obstruido, baja presión o una válvula fallando.",
            ),
        ],
    },
}


def _spanish_core_service_payload(slug: str) -> dict[str, Any]:
    meta = SERVICE_TRANSLATIONS[slug]
    if all(key in meta for key in ("body", "problems", "benefits", "faq")):
        return {**meta, "slug": slug}
    content = FULL_SPANISH_SERVICE_CONTENT[slug]
    title = meta["title"]
    return {
        **meta,
        "slug": slug,
        "seo_title": f"{title} | Inland Empire Appliance Repair",
        "search_description": (
            f"Información en español sobre {title.lower()} y cómo solicitar un diagnóstico."
        ),
        "body": content["body"],
        "problems": content["problems"],
        "benefits": [
            (item["title"], item["description"]) for item in content["benefits"]
        ],
        "faq": [
            (item["question"], item["answer"]) for item in content["faqs"]
        ],
    }


ENGLISH_SERVICE_PAYLOADS: dict[str, dict[str, Any]] = {
    data["slug"]: data
    for data in (
        *ENGLISH_CORE_SERVICES,
        COMMERCIAL_SERVICE_PAGE,
        HIGH_END_SERVICE_PAGE,
        *BRAND_PAGES,
        *HIGH_END_BRAND_SERVICE_PAGES,
    )
}

SPANISH_SERVICE_PAYLOADS: dict[str, dict[str, Any]] = {
    slug: _spanish_core_service_payload(slug) for slug in SERVICE_TRANSLATIONS
}
SPANISH_SERVICE_PAYLOADS.update(
    {
        COMMERCIAL_SERVICE_PAGE["slug"]: {
            **SPANISH_COMMERCIAL_SERVICE_PAGE,
            "slug": COMMERCIAL_SERVICE_PAGE["slug"],
        },
        HIGH_END_SERVICE_PAGE["slug"]: {
            **SPANISH_HIGH_END_SERVICE_PAGE,
            "slug": HIGH_END_SERVICE_PAGE["slug"],
        },
        **SPANISH_PRIMARY_BRAND_SERVICE_PAGES,
        **{
            data["slug"]: data for data in SPANISH_HIGH_END_BRAND_SERVICE_PAGES
        },
    }
)

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
        "body": (
            f"<h2>Reparación de electrodomésticos en {name}</h2>"
            "<p>Atendemos solicitudes de reparación para electrodomésticos del hogar. "
            "El servicio comienza con un diagnóstico del equipo y una explicación "
            "de los hallazgos antes de iniciar cualquier trabajo.</p>"
            "<h2>Qué esperar durante la visita</h2>"
            "<p>Comparta el tipo de electrodoméstico, el número de modelo y una "
            "descripción del problema. Confirmamos la disponibilidad y el alcance "
            "del servicio al programar la visita.</p>"
        ),
        "about_techs": (
            f"<p>Para una solicitud en {name}, el técnico revisa el equipo, explica "
            "el diagnóstico y presenta las opciones disponibles antes de que usted "
            "decida cómo continuar. Confirme la cobertura y el horario al reservar.</p>"
        ),
    }
    for name in _CITY_NAMES
}

HOME_TRANSLATIONS: dict[str, str] = {
    "title": "Inicio",
    "hero_title": "REPARACIÓN DE ELECTRODOMÉSTICOS EL MISMO DÍA",
    "hero_subtitle": (
        "Reparación profesional de refrigeradores, lavadoras, secadoras, "
        "lavavajillas y hornos en el Inland Empire."
    ),
    "commercial_title": "Reparación de Electrodomésticos Comercial y Residencial",
    "commercial_body": (
        "<p>Reparamos refrigeradores, congeladores, lavadoras, secadoras, "
        "lavavajillas, hornos y otros electrodomésticos residenciales y comerciales "
        "ligeros en el Inland Empire.</p><p>El servicio comienza con un diagnóstico "
        "en el lugar. Antes de iniciar el trabajo, el técnico explica el problema, "
        "las opciones disponibles y el precio para su aprobación.</p>"
    ),
    "services_heading": "¿Qué Electrodomésticos Reparamos?",
    "process_heading": "Cómo Reservar una Reparación",
    "process_subheading": (
        "Elija un servicio, confirme su área y programe una visita. Diagnosticamos "
        "el electrodoméstico antes de que usted apruebe la reparación."
    ),
    "pricing_heading": "¿Cuánto Cuesta la Reparación?",
    "pricing_note": (
        "El precio final depende del electrodoméstico, la falla y las piezas "
        "necesarias. El técnico confirma el precio antes de comenzar."
    ),
    "brands_heading": "¿Qué Marcas Reparamos?",
    "brands_subheading": (
        "Reparamos marcas comunes y premium. Seleccione una marca enlazada para ver "
        "detalles o llame para confirmar su modelo."
    ),
    "areas_heading": "Reparación de Electrodomésticos en el Inland Empire",
    "areas_subheading": (
        "Atendemos hogares y negocios en Corona, Riverside y comunidades cercanas. "
        "Ingrese su código postal para confirmar la cobertura."
    ),
    "testimonials_heading": "Lo Que Dicen Nuestros Clientes",
    "faq_heading": "Preguntas Frecuentes",
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
            # Regional landing pages are English editorial drafts. Do not expose
            # copied English content under /es/ before a Spanish version is approved.
            if isinstance(page, ServicePage) and page.is_regional_service_page:
                self.stdout.write(f'  SKIP  regional "{page.title}"')
                skipped_count += 1
                continue

            existing_translation = Page.objects.filter(
                translation_key=page.translation_key,
                locale=es_locale,
            ).first()
            if existing_translation:
                es_specific = existing_translation.specific
                if isinstance(page, HomePage) and isinstance(es_specific, HomePage):
                    if _apply_spanish_home_content(es_specific, page):
                        es_specific.save()
                        es_specific.save_revision().publish()
                elif isinstance(page, ServicePage) and isinstance(es_specific, ServicePage):
                    if _apply_spanish_service_content(es_specific, page):
                        es_specific.save()
                        es_specific.save_revision().publish()
                elif isinstance(page, CityPage) and isinstance(es_specific, CityPage):
                    if _apply_spanish_city_content(es_specific, page):
                        es_specific.save()
                        es_specific.save_revision().publish()
                self.stdout.write(f'  SKIP  "{page.title}"')
                skipped_count += 1
                continue

            try:
                es_page = page.copy_for_translation(es_locale)
                es_specific = es_page.specific
                _apply_translation(es_specific, page)
                es_specific.save()
                es_specific.save_revision().publish()

                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  +     "{es_specific.title}"'))

            except Exception as e:
                self.stderr.write(self.style.ERROR(f'  ERROR "{page.title}": {e}'))
                logger.exception("Failed to translate page %s", page.title)

        # Fix inline-panel foreign keys to point at Spanish pages
        service_map = _translation_map(ServicePage, es_locale)
        city_map = _translation_map(CityPage, es_locale)
        _fix_city_featured_services(service_map, es_locale)
        _fix_city_nearby_cities(city_map, es_locale)
        _fix_related_services(service_map, es_locale)

        # Blog payloads are maintained by their dedicated idempotent command.
        # Running it here prevents copied-English BlogPage translations from
        # surviving the canonical Spanish reconciliation path.
        call_command(
            "setup_spanish_blog_posts",
            stdout=self.stdout,
            stderr=self.stderr,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone! Created {created_count}, skipped {skipped_count}."
            )
        )


# ── Translation helpers ───────────────────────────────────────────────


def _apply_spanish_home_content(es_page: HomePage, en_page: HomePage) -> bool:
    """Repair blank/copied Home fields without overwriting editor-owned Spanish."""
    changed = False
    editorial_markers = (
        "Use this editable",
        "keep this process copy editable",
        "target-approved",
        "after claims are reviewed",
    )
    for field, spanish_value in HOME_TRANSLATIONS.items():
        current = str(getattr(es_page, field, "") or "")
        english = str(getattr(en_page, field, "") or "")
        should_repair = (
            not current
            or current == english
            or any(marker.lower() in current.lower() for marker in editorial_markers)
        )
        if should_repair and current != spanish_value:
            setattr(es_page, field, spanish_value)
            changed = True
    return changed


def _service_page_payload(page: ServicePage) -> dict[str, Any]:
    """Serialize one live ServicePage into canonical seed-data shapes."""

    payload: dict[str, Any] = {
        field: str(getattr(page, field, "") or "")
        for field in (
            "title",
            "seo_title",
            "search_description",
            "intro",
            "short_description",
            "hero_usp",
            "body",
        )
    }
    payload["problems"] = [str(block.value) for block in page.problems_we_fix]
    payload["benefits"] = [
        (str(block.value["title"]), str(block.value["description"]))
        for block in page.why_choose_us
    ]
    payload["faq"] = [
        (str(block.value["question"]), str(block.value["answer"]))
        for block in page.faq
    ]
    return payload


def _apply_spanish_service_content(
    es_page: ServicePage,
    en_page: ServicePage,
) -> bool:
    """Repair only empty, English-copied/generated, or sentinel service fields."""

    desired = SPANISH_SERVICE_PAYLOADS.get(en_page.slug)
    if desired is None:
        return False
    sources = [_service_page_payload(en_page)]
    seed_source = ENGLISH_SERVICE_PAYLOADS.get(en_page.slug)
    if seed_source is not None:
        sources.append(seed_source)
    return reconcile_service_page_seed_data(
        es_page,
        desired,
        replace_if_matches=tuple(sources),
    )


def _apply_spanish_city_content(es_page: CityPage, en_page: CityPage) -> bool:
    """Populate neutral Spanish city copy while preserving editor-authored Spanish."""

    desired = CITY_TRANSLATIONS.get(en_page.slug)
    if desired is None:
        return False
    changed = False
    for field, spanish_value in desired.items():
        current = str(getattr(es_page, field, "") or "")
        english = str(getattr(en_page, field, "") or "")
        if (not current or current == english) and current != spanish_value:
            setattr(es_page, field, spanish_value)
            changed = True
    return changed


def _apply_translation(es_page: Page, en_page: Page) -> None:
    """Set Spanish content on the translated page copy."""
    if isinstance(en_page, HomePage) and isinstance(es_page, HomePage):
        _apply_spanish_home_content(es_page, en_page)

    elif isinstance(en_page, ServicesIndexPage):
        es_page.title = "Servicios"
        es_page.hero_title = "Servicios de Reparación de Electrodomésticos"
        es_page.hero_subtitle = (
            "Reparación experta para todos los electrodomésticos principales. "
            "Servicio rápido, confiable y económico."
        )

    elif isinstance(en_page, ServicePage):
        _apply_spanish_service_content(es_page, en_page)

    elif isinstance(en_page, LocationsIndexPage):
        es_page.title = "Áreas de Servicio"
        es_page.intro = (
            "<p>Servimos con orgullo al Sur de California con "
            "reparación de electrodomésticos rápida y confiable.</p>"
        )

    elif isinstance(en_page, CityPage):
        _apply_spanish_city_content(es_page, en_page)

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


def _translation_map(page_type: type[Page], es_locale: Locale) -> dict[int, int]:
    """Return English page PK → Spanish translation PK for all existing pairs."""
    mapping: dict[int, int] = {}
    english_pages = page_type.objects.filter(locale__language_code="en")
    for english in english_pages:
        spanish = page_type.objects.filter(
            translation_key=english.translation_key,
            locale=es_locale,
        ).first()
        if spanish:
            mapping[english.pk] = spanish.pk
    return mapping


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
        seen_related_ids: set[int] = set()
        rows = ServiceRelatedService.objects.filter(page=svc).order_by("sort_order", "pk")
        for rs in rows:
            es_pk = service_map.get(rs.related_service_id, rs.related_service_id)
            if es_pk is None:
                continue
            if es_pk in seen_related_ids:
                rs.delete()
                continue
            seen_related_ids.add(es_pk)
            if es_pk != rs.related_service_id:
                rs.related_service_id = es_pk
                rs.save()
