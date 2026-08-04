"""Shared seeded ServicePage content for Inland Empire Appliance Repair SEO landing pages."""

from __future__ import annotations

import json
from typing import Any

from home.high_end_brand_seed_data import (
    HIGH_END_BRAND_PAGE_SLUGS,
    high_end_brand_grid,
)


COMMERCIAL_SERVICE_PAGE: dict[str, Any] = {
    "title": "Commercial Appliance Repair",
    "slug": "commercial-appliance-repair",
    "seo_title": "Commercial Appliance Repair — Same-Day Service",
    "search_description": (
        "Commercial appliance repair for restaurants, offices, property managers, "
        "and laundry rooms. Same-day diagnostics, stocked parts, warranty included."
    ),
    "intro": (
        "Commercial appliance repair for restaurants, offices, property managers, "
        "and laundry rooms — same-day diagnostics with warranty-backed service"
    ),
    "short_description": (
        "Business-focused repair for refrigeration, cooking, dishwashing, ice, "
        "and laundry equipment."
    ),
    "hero_usp": (
        "Keep business moving with clear diagnostics, stocked parts, and "
        "warranty-backed repairs for commercial units."
    ),
    "body": (
        "<h2>Commercial Appliance Repair for Local Businesses</h2>"
        "<p>When equipment goes down at a restaurant kitchen, office, shared "
        "laundry room, or managed property, every hour can affect customers, "
        "tenants, and staff. Inland Empire Appliance Repair provides business-focused "
        "commercial appliance repair across the Inland Empire with clear "
        "diagnostics before work begins and same-day scheduling available for "
        "most repair requests.</p>"
        "<h2>Commercial Refrigeration, Ice, Cooking, and Laundry</h2>"
        "<p>Our existing service scope includes commercial refrigeration units, "
        "walk-in coolers and freezers, commercial ice machines, restaurant-grade "
        "ovens, dishwashers, washers, dryers, microwaves, and standard appliances "
        "used in office and property management settings. If a specialized unit "
        "needs a part or factory procedure outside our normal field scope, we will "
        "tell you during diagnosis instead of overpromising.</p>"
        "<h2>Downtime-Focused Diagnostics</h2>"
        "<p>Commercial repairs need practical answers fast: what failed, whether it "
        "can be repaired today, and what it will cost. Our technicians arrive with "
        "common OEM and manufacturer-approved parts, provide an itemized quote, "
        "and waive the diagnostic service call when you approve the repair.</p>"
        "<h2>Warranty-Backed Business Appliance Service</h2>"
        "<p>Every approved repair includes warranty coverage on parts and labor. "
        "From a commercial ice machine that cannot keep up to a walk-in cooler "
        "that is drifting warm, we focus on safe, durable repairs that help your "
        "business get back to normal.</p>"
    ),
    "problems": [
        "Walk-in cooler or freezer not holding temperature",
        "Commercial ice machine not making enough ice",
        "Restaurant oven or range not heating evenly",
        "Commercial dishwasher not cleaning or draining",
        "Commercial washer or dryer down",
        "Office refrigerator leaking or not cooling",
        "Property-management appliance turnover repairs",
        "Freezer frost buildup or temperature swings",
        "Microwave or warming equipment not heating",
        "Urgent diagnostics for business downtime",
    ],
    "benefits": [
        (
            "Minimize Business Downtime",
            "Same-day scheduling is available for most commercial repair requests, "
            "with practical diagnostics focused on getting operations moving again.",
        ),
        (
            "Commercial Refrigeration & Ice",
            "EPA 608 certified technicians diagnose walk-in coolers, freezers, "
            "refrigeration units, and commercial ice machines.",
        ),
        (
            "Clear Commercial Diagnostics",
            "You get an itemized quote before work begins, and the diagnostic service "
            "call is waived when you approve the repair.",
        ),
        (
            "Warranty-Backed Repairs",
            "Repairs use OEM or manufacturer-approved parts where available and include "
            "warranty coverage on parts and labor.",
        ),
    ],
    "faq": [
        (
            "Do you repair appliances for restaurants, offices, and property managers?",
            "Yes. Inland Empire Appliance Repair services both commercial and residential appliances across "
            "Riverside County, including restaurant kitchens, office break rooms, "
            "property-management units, and shared laundry rooms.",
        ),
        (
            "What commercial appliances can you diagnose?",
            "We diagnose commercial refrigeration, walk-in coolers and freezers, ice "
            "machines, dishwashers, ovens, ranges, microwaves, washers, dryers, and "
            "similar business appliances when parts and service access are available.",
        ),
        (
            "Can you help when downtime is urgent?",
            "Same-day scheduling is available for most repair requests. We focus on "
            "clear diagnostics, stocked common parts, and honest repair options so "
            "you can make a fast business decision.",
        ),
        (
            "Do commercial appliance repairs include a warranty?",
            "Yes. Approved repairs include warranty coverage on parts and labor. Your "
            "technician will explain the warranty terms that apply to the appliance, "
            "repair, and parts used.",
        ),
        (
            "How does pricing work for commercial appliance repair?",
            "The diagnostic service call is waived when you approve the repair. Before "
            "work begins, we provide an itemized quote based on the appliance, failure, "
            "and parts required.",
        ),
    ],
    "related": [
        "refrigerator-repair",
        "freezer-repair",
        "dishwasher-repair",
        "oven-repair",
        "washer-repair",
        "dryer-repair",
    ],
}


SPANISH_COMMERCIAL_SERVICE_PAGE: dict[str, Any] = {
    "title": "Reparación de Electrodomésticos Comerciales",
    "seo_title": "Reparación de Electrodomésticos Comerciales | Inland Empire Appliance Repair",
    "search_description": (
        "Reparación de electrodomésticos comerciales para restaurantes, oficinas, "
        "administradores de propiedades y lavanderías. Diagnóstico claro y garantía."
    ),
    "intro": (
        "Reparación de electrodomésticos comerciales para restaurantes, oficinas, "
        "administradores de propiedades y lavanderías, con diagnóstico claro y garantía"
    ),
    "short_description": (
        "Servicio comercial para refrigeración, cocción, lavado, hielo y lavandería."
    ),
    "hero_usp": (
        "Mantenga su negocio en marcha con diagnóstico claro, piezas disponibles "
        "y reparaciones comerciales con garantía."
    ),
    "body": (
        "<h2>Reparación comercial para negocios locales</h2>"
        "<p>Cuando un equipo falla en cocinas de restaurantes, oficinas, "
        "administradores de propiedades o lavanderías compartidas, cada hora "
        "puede afectar a clientes, "
        "inquilinos y personal. Inland Empire Appliance Repair ofrece reparación de "
        "electrodomésticos comerciales en el Inland Empire, con diagnóstico claro "
        "antes de empezar y citas el mismo día disponibles para la mayoría de las "
        "solicitudes.</p>"
        "<h2>Refrigeración, hielo, cocción y lavandería comercial</h2>"
        "<p>Nuestro alcance de servicio incluye unidades de refrigeración comercial, "
        "cámaras frigoríficas y congeladores, máquinas de hielo comerciales, hornos "
        "de restaurante, lavavajillas, lavadoras, secadoras, microondas y "
        "electrodomésticos usados en oficinas o propiedades administradas. Si una "
        "unidad especializada requiere una pieza o procedimiento fuera de nuestro "
        "alcance normal, se lo diremos durante el diagnóstico.</p>"
        "<h2>Diagnóstico pensado para reducir el tiempo fuera de servicio</h2>"
        "<p>Las reparaciones comerciales necesitan respuestas prácticas: qué falló, "
        "si se puede reparar hoy y cuánto costará. Nuestros técnicos llevan piezas "
        "OEM o aprobadas por fabricantes cuando están disponibles, entregan una "
        "cotización detallada y eliminan el costo de diagnóstico cuando usted "
        "aprueba la reparación.</p>"
        "<h2>Servicio comercial respaldado por garantía</h2>"
        "<p>Cada reparación aprobada incluye garantía en piezas y mano de obra. Desde "
        "una máquina de hielo comercial que no alcanza la demanda hasta una cámara "
        "frigorífica que pierde temperatura, nos enfocamos en reparaciones seguras "
        "y duraderas para que su negocio vuelva a operar.</p>"
    ),
    "problems": [
        "Cámara frigorífica o congelador que no mantiene temperatura",
        "Máquina de hielo comercial que no produce suficiente hielo",
        "Horno o estufa de restaurante que calienta de forma irregular",
        "Lavavajillas comercial que no limpia o no drena",
        "Lavadora o secadora comercial fuera de servicio",
        "Refrigerador de oficina con fuga o sin enfriar",
        "Reparaciones para rotación de unidades de propiedades administradas",
        "Escarcha o cambios de temperatura en congeladores",
        "Microondas o equipo de calentamiento que no calienta",
        "Diagnóstico urgente por tiempo fuera de servicio del negocio",
    ],
    "benefits": [
        (
            "Menos tiempo fuera de servicio",
            "Hay citas el mismo día disponibles para la mayoría de solicitudes "
            "comerciales, con diagnóstico práctico para reactivar la operación.",
        ),
        (
            "Refrigeración y hielo comercial",
            "Técnicos certificados EPA 608 diagnostican cámaras frigoríficas, "
            "congeladores, unidades de refrigeración y máquinas de hielo comerciales.",
        ),
        (
            "Diagnóstico comercial claro",
            "Recibe una cotización detallada antes de comenzar; el diagnóstico se "
            "elimina cuando aprueba la reparación.",
        ),
        (
            "Reparaciones con garantía",
            "Usamos piezas OEM o aprobadas por fabricantes cuando están disponibles, "
            "con garantía en piezas y mano de obra.",
        ),
    ],
    "faq": [
        (
            "¿Reparan equipos para restaurantes, oficinas y administradores de propiedades?",
            "Sí. Inland Empire Appliance Repair repara electrodomésticos comerciales y residenciales en "
            "Riverside County, incluyendo cocinas de restaurantes, áreas de descanso "
            "en oficinas, unidades administradas y lavanderías compartidas.",
        ),
        (
            "¿Qué electrodomésticos comerciales pueden diagnosticar?",
            "Diagnosticamos refrigeración comercial, cámaras frigoríficas y congeladores, "
            "máquinas de hielo, lavavajillas, hornos, estufas, microondas, lavadoras, "
            "secadoras y equipos similares cuando hay acceso de servicio y piezas.",
        ),
        (
            "¿Pueden ayudar cuando el tiempo fuera de servicio es urgente?",
            "Hay citas el mismo día disponibles para la mayoría de reparaciones. Nos "
            "enfocamos en diagnóstico claro, piezas comunes disponibles y opciones "
            "honestas para que pueda decidir rápido.",
        ),
        (
            "¿Las reparaciones comerciales incluyen garantía?",
            "Sí. Las reparaciones aprobadas incluyen garantía en piezas y mano de obra. "
            "El técnico le explicará los términos aplicables al equipo, la reparación "
            "y las piezas usadas.",
        ),
        (
            "¿Cómo funciona el precio de reparación comercial?",
            "El cargo de diagnóstico se elimina cuando aprueba la reparación. Antes de "
            "empezar, entregamos una cotización detallada según el equipo, la falla y "
            "las piezas necesarias.",
        ),
    ],
}


HIGH_END_SERVICE_PAGE: dict[str, Any] = {
    "title": "High End Appliance Repair",
    "slug": "high-end-appliance-repair",
    "seo_title": "High End Appliance Repair — Premium Brand Service",
    "search_description": (
        "High-end appliance repair for Bosch, KitchenAid, Sub-Zero, Thermador, "
        "Miele, Viking, Speed Queen, Fisher & Paykel, Monogram, and Wolf. Same-day diagnostics."
    ),
    "intro": (
        "High-end appliance repair for premium kitchens and laundry rooms — "
        "built-in refrigeration, pro-style ranges, premium dishwashers, "
        "luxury laundry, and specialized diagnostics"
    ),
    "short_description": (
        "Premium-brand diagnostics for built-in refrigeration, pro-style cooking, "
        "dishwashers, and luxury laundry."
    ),
    "hero_usp": (
        "Specialized diagnostics, OEM or manufacturer-approved parts where "
        "available, same-day scheduling, and warranty-backed repairs."
    ),
    "body": (
        "<h2>High-End Appliance Repair for Premium Homes</h2>"
        "<p>Premium appliances need careful diagnosis before parts are replaced. "
        "Inland Empire Appliance Repair services high-end appliance repair needs across "
        "the Inland Empire, including built-in refrigeration, "
        "pro-style ranges, premium dishwashers, luxury laundry, and specialty "
        "kitchen equipment. We use clear testing steps, explain the repair path, "
        "and avoid overpromising when a unit requires a factory procedure outside "
        "normal field service.</p>"
        "<section aria-labelledby=\"high-end-brand-grid-heading\" data-high-end-brand-grid>"
        "<h2 id=\"high-end-brand-grid-heading\">Premium Brand Repair Hub</h2>"
        "<p>Select a brand page for focused diagnostics, appliance details, "
        "and repair guidance. Each card now links to a live individual brand "
        "page instead of a placeholder.</p>"
        f"{high_end_brand_grid()}"
        "</section>"
        "<h2>Specialized Diagnostics Before Parts</h2>"
        "<p>High-end systems often combine electronic controls, sensors, cooling "
        "circuits, water systems, and cabinet-integrated installation details. "
        "Our technicians isolate the failed component first, then quote the "
        "repair with OEM or manufacturer-approved parts where available. Approved "
        "repairs include warranty coverage on parts and labor.</p>"
        "<h2>Same-Day Local Scheduling</h2>"
        "<p>Same-day scheduling is available for most high-end appliance repair "
        "requests. If a premium appliance needs a special-order part, we provide "
        "the next practical step clearly so you can plan around the repair.</p>"
    ),
    "problems": [
        "Built-in refrigerator not cooling or holding temperature",
        "Sub-Zero freezer or ice maker issue",
        "Pro-style range or oven not heating evenly",
        "Premium dishwasher not draining or cleaning",
        "Luxury washer or dryer error codes",
        "Thermador, Viking, or Miele cooking appliance diagnostics",
        "Bosch or KitchenAid dishwasher fault",
        "Fisher & Paykel DishDrawer problem",
        "Speed Queen washer or dryer performance issue",
        "High-end appliance control board or sensor fault",
    ],
    "benefits": [
        (
            "Premium Brand Focus",
            "Diagnostics for Bosch, KitchenAid, Sub-Zero, Thermador, Miele, Viking, Speed Queen, Fisher & Paykel, Monogram, and Wolf appliances.",
        ),
        (
            "Built-In & Pro-Style Experience",
            "Support for built-in refrigerators, pro-style ranges, premium dishwashers, and luxury laundry systems.",
        ),
        (
            "Clear Diagnostic Path",
            "We test before replacing parts and explain when a specialized unit needs a special-order component or factory procedure.",
        ),
        (
            "Warranty-Backed Repair",
            "Approved repairs use OEM or manufacturer-approved parts where available and include warranty coverage on parts and labor.",
        ),
    ],
    "faq": [
        (
            "Which high-end appliance brands do you service?",
            "This hub links to individual Bosch, KitchenAid, Sub-Zero, Thermador, Miele, Viking, Speed Queen, Fisher & Paykel, Monogram, and Wolf repair pages with brand-specific diagnostics and service details.",
        ),
        (
            "Do you repair built-in refrigerators and pro-style ranges?",
            "Yes. We diagnose built-in refrigeration, freezers, ice makers, pro-style ranges, wall ovens, cooktops, premium dishwashers, washers, and dryers when service access and parts are available.",
        ),
        (
            "Do high-end repairs use OEM parts?",
            "We use OEM or manufacturer-approved parts where available and explain any special-order timing before work proceeds.",
        ),
        (
            "Can I schedule high-end appliance repair the same day?",
            "Same-day local scheduling is available for most repair requests. If a premium appliance needs a specialized part, we will document the next practical step after diagnosis.",
        ),
        (
            "Is the repair covered by a warranty?",
            "Approved repairs include warranty coverage on parts and labor. Your technician will explain the warranty details for the appliance, repair, and parts used.",
        ),
    ],
    "related": [
        "refrigerator-repair",
        "freezer-repair",
        "dishwasher-repair",
        "oven-repair",
        "stove-repair",
        "washer-repair",
        "dryer-repair",
    ],
}


SPANISH_HIGH_END_SERVICE_PAGE: dict[str, Any] = {
    "title": "Reparación de Electrodomésticos de Alta Gama",
    "seo_title": "Reparación de Electrodomésticos de Alta Gama | Inland Empire Appliance Repair",
    "search_description": (
        "Reparación de electrodomésticos de alta gama para Bosch, KitchenAid, "
        "Sub-Zero, Thermador, Miele, Viking, Speed Queen, Fisher & Paykel, Monogram y Wolf."
    ),
    "intro": (
        "Reparación de electrodomésticos de alta gama para cocinas y lavanderías "
        "premium: refrigeración empotrada, rangos profesionales, lavavajillas "
        "premium y diagnóstico especializado"
    ),
    "short_description": (
        "Diagnóstico para marcas premium, refrigeración empotrada, cocción de alta gama y lavandería."
    ),
    "hero_usp": (
        "Diagnóstico especializado, piezas OEM o aprobadas por fabricantes cuando "
        "están disponibles, citas el mismo día y garantía."
    ),
    "body": (
        "<h2>Reparación de alta gama para hogares premium</h2>"
        "<p>Los electrodomésticos premium requieren diagnóstico cuidadoso antes de "
        "reemplazar piezas. Inland Empire Appliance Repair atiende necesidades de reparación "
        "de electrodomésticos de alta gama en el Inland Empire, "
        "incluyendo refrigeración empotrada, rangos profesionales, lavavajillas "
        "premium, lavandería de lujo y equipos especiales de cocina. Explicamos "
        "la ruta de reparación y evitamos prometer de más cuando una unidad necesita "
        "un procedimiento de fábrica fuera del servicio normal en campo.</p>"
        "<section aria-labelledby=\"high-end-brand-grid-heading\" data-high-end-brand-grid>"
        "<h2 id=\"high-end-brand-grid-heading\">Centro de marcas premium</h2>"
        "<p>Seleccione una página de marca para ver diagnóstico, detalles del "
        "equipo y guía de reparación. Cada tarjeta enlaza a una página individual "
        "activa en lugar de un marcador temporal.</p>"
        f"{high_end_brand_grid(spanish=True)}"
        "</section>"
        "<h2>Diagnóstico especializado antes de cambiar piezas</h2>"
        "<p>Los equipos de alta gama combinan controles electrónicos, sensores, "
        "circuitos de enfriamiento, sistemas de agua y detalles de instalación "
        "integrada. Primero aislamos la falla, luego cotizamos la reparación con "
        "piezas OEM o aprobadas por fabricantes cuando están disponibles. Las "
        "reparaciones aprobadas incluyen garantía en piezas y mano de obra.</p>"
        "<h2>Citas locales el mismo día</h2>"
        "<p>Hay citas el mismo día disponibles para la mayoría de solicitudes de "
        "reparación de alta gama. Si el electrodoméstico premium necesita una pieza "
        "especial, explicamos claramente el siguiente paso para que pueda planear.</p>"
    ),
    "problems": [
        "Refrigerador empotrado que no enfría o no mantiene temperatura",
        "Problema de congelador o fábrica de hielo Sub-Zero",
        "Rango profesional u horno que no calienta parejo",
        "Lavavajillas premium que no drena o no limpia",
        "Códigos de error en lavadora o secadora de lujo",
        "Diagnóstico de equipos Thermador, Viking o Miele",
        "Falla en lavavajillas Bosch o KitchenAid",
        "Problema de Fisher & Paykel DishDrawer",
        "Problema de rendimiento en lavadora o secadora Speed Queen",
        "Falla de control o sensor en electrodoméstico de alta gama",
    ],
    "benefits": [
        (
            "Enfoque en marcas premium",
            "Diagnóstico para Bosch, KitchenAid, Sub-Zero, Thermador, Miele, Viking, Speed Queen, Fisher & Paykel, Monogram y Wolf.",
        ),
        (
            "Experiencia con equipos empotrados",
            "Servicio para refrigeradores empotrados, rangos profesionales, lavavajillas premium y lavandería de lujo.",
        ),
        (
            "Ruta de diagnóstico clara",
            "Probamos antes de reemplazar piezas y explicamos si una unidad especializada necesita una pieza especial o procedimiento de fábrica.",
        ),
        (
            "Reparación con garantía",
            "Las reparaciones aprobadas usan piezas OEM o aprobadas por fabricantes cuando están disponibles e incluyen garantía.",
        ),
    ],
    "faq": [
        (
            "¿Qué marcas de alta gama cubren?",
            "Este hub enlaza a páginas individuales de reparación para Bosch, KitchenAid, Sub-Zero, Thermador, Miele, Viking, Speed Queen, Fisher & Paykel, Monogram y Wolf con diagnóstico y detalles de servicio por marca.",
        ),
        (
            "¿Reparan refrigeradores empotrados y rangos profesionales?",
            "Sí. Diagnosticamos refrigeración empotrada, congeladores, fábricas de hielo, rangos profesionales, hornos de pared, cubiertas, lavavajillas premium, lavadoras y secadoras cuando hay acceso y piezas disponibles.",
        ),
        (
            "¿Usan piezas OEM en reparaciones de alta gama?",
            "Usamos piezas OEM o aprobadas por fabricantes cuando están disponibles y explicamos cualquier tiempo de pedido especial antes de continuar.",
        ),
        (
            "¿Puedo agendar reparación de alta gama el mismo día?",
            "Hay citas locales el mismo día disponibles para la mayoría de reparaciones. Si una unidad premium necesita una pieza especializada, documentamos el siguiente paso después del diagnóstico.",
        ),
        (
            "¿La reparación tiene garantía?",
            "Las reparaciones aprobadas incluyen garantía en piezas y mano de obra. El técnico le explicará los detalles aplicables al equipo, la reparación y las piezas usadas.",
        ),
    ],
}


PRIMARY_BRAND_SERVICE_SLUGS: frozenset[str] = frozenset(
    {
        "ge-appliance-repair",
        "lg-appliance-repair",
        "samsung-appliance-repair",
        "maytag-appliance-repair",
        "whirlpool-appliance-repair",
    }
)

PRIMARY_BRAND_NAMES: dict[str, str] = {
    "ge-appliance-repair": "GE",
    "lg-appliance-repair": "LG",
    "samsung-appliance-repair": "Samsung",
    "maytag-appliance-repair": "Maytag",
    "whirlpool-appliance-repair": "Whirlpool",
}


def _spanish_primary_brand_service_page(slug: str, brand: str) -> dict[str, Any]:
    """Build neutral Spanish brand copy without affiliation or credential claims."""

    return {
        "title": f"Reparación de Electrodomésticos {brand}",
        "slug": slug,
        "seo_title": f"Reparación de Electrodomésticos {brand} | Inland Empire",
        "search_description": (
            f"Diagnóstico y reparación de electrodomésticos {brand}. "
            "Confirme la cobertura de su modelo y reciba una explicación antes del trabajo."
        ),
        "intro": (
            f"Diagnóstico y reparación para electrodomésticos {brand}, "
            "con alcance confirmado según el modelo y la pieza necesaria."
        ),
        "short_description": (
            f"Diagnóstico para refrigeradores, lavadoras, secadoras, cocción y "
            f"otros electrodomésticos {brand}."
        ),
        "hero_usp": (
            f"Evaluación clara para electrodomésticos {brand}; confirmamos el alcance "
            "del servicio antes de iniciar la reparación."
        ),
        "body": (
            f"<h2>Servicio para electrodomésticos {brand}</h2>"
            f"<p>Atendemos solicitudes de diagnóstico y reparación para equipos {brand}. "
            "La visita comienza con la revisión del síntoma, el número de modelo y el "
            "estado del electrodoméstico.</p>"
            "<h2>Tipos de equipos que podemos evaluar</h2>"
            f"<p>Según el modelo, podemos evaluar refrigeradores, lavadoras, secadoras, "
            f"lavavajillas y equipos de cocción {brand}. La disponibilidad de servicio "
            "y piezas se confirma antes de continuar.</p>"
            "<h2>Qué sucede después del diagnóstico</h2>"
            "<p>Explicamos la causa encontrada, las opciones disponibles y el alcance "
            "del trabajo. La reparación solo continúa después de su aprobación.</p>"
            "<h2>Información útil para reservar</h2>"
            f"<p>Tenga a mano el número de modelo de su equipo {brand} y una descripción "
            "del problema. Con esos datos podemos confirmar si el modelo está dentro "
            "del alcance y preparar la visita.</p>"
        ),
        "problems": [
            "El electrodoméstico no enciende",
            "La pantalla muestra un código de error",
            "El equipo no completa el ciclo",
            "Temperatura o calentamiento irregular",
            "Fuga de agua o drenaje deficiente",
            "Ruido o vibración fuera de lo normal",
        ],
        "benefits": [
            (
                "Diagnóstico antes de reparar",
                "Revisamos el síntoma y el modelo antes de proponer cualquier trabajo.",
            ),
            (
                "Explicación clara",
                "Recibe una explicación de los hallazgos y las opciones antes de decidir.",
            ),
            (
                "Alcance según el modelo",
                "Confirmamos la disponibilidad de servicio y piezas para su modelo específico.",
            ),
        ],
        "faq": [
            (
                f"¿Qué electrodomésticos {brand} pueden evaluar?",
                "El alcance puede incluir refrigeradores, lavadoras, secadoras, lavavajillas y equipos de cocción. Confirme su modelo al reservar.",
            ),
            (
                "¿Necesito el número de modelo?",
                "Sí. El número de modelo ayuda a confirmar el alcance del servicio y la disponibilidad de piezas antes de la visita.",
            ),
            (
                f"¿Atienden todos los modelos {brand}?",
                "La cobertura depende del tipo de equipo, el modelo, el acceso de servicio y las piezas disponibles. Lo confirmamos antes de continuar.",
            ),
            (
                "¿Cuándo conoceré las opciones de reparación?",
                "Después del diagnóstico explicamos la causa encontrada y las opciones disponibles para que usted decida cómo continuar.",
            ),
        ],
    }


SPANISH_PRIMARY_BRAND_SERVICE_PAGES: dict[str, dict[str, Any]] = {
    slug: _spanish_primary_brand_service_page(slug, brand)
    for slug, brand in PRIMARY_BRAND_NAMES.items()
}

SEO_LANDING_SERVICE_SLUGS: frozenset[str] = frozenset(
    {
        COMMERCIAL_SERVICE_PAGE["slug"],
        HIGH_END_SERVICE_PAGE["slug"],
        *PRIMARY_BRAND_SERVICE_SLUGS,
        *HIGH_END_BRAND_PAGE_SLUGS,
    }
)

FEATURED_SERVICE_HUB_SLUGS: tuple[str, str] = (
    COMMERCIAL_SERVICE_PAGE["slug"],
    HIGH_END_SERVICE_PAGE["slug"],
)


def streamfield_problem_data(problems: list[str]) -> str:
    """Return JSON for the ServicePage problems StreamField."""
    return json.dumps([{"type": "problem", "value": problem} for problem in problems])


def streamfield_benefit_data(benefits: list[tuple[str, str]]) -> str:
    """Return JSON for the ServicePage why_choose_us StreamField."""
    return json.dumps(
        [
            {"type": "benefit", "value": {"title": title, "description": description}}
            for title, description in benefits
        ]
    )


def streamfield_faq_data(faq: list[tuple[str, str]]) -> str:
    """Return JSON for the ServicePage FAQ StreamField."""
    return json.dumps(
        [
            {"type": "faq_item", "value": {"question": question, "answer": answer}}
            for question, answer in faq
        ]
    )


def _stream_equivalent(current: Any, desired_json: str) -> bool:
    """Compare StreamField data while ignoring Wagtail-generated block IDs."""
    raw_data = getattr(current, "raw_data", None)
    try:
        desired = json.loads(desired_json)
    except json.JSONDecodeError:
        return str(getattr(current, "raw_text", current) or "") == desired_json
    if raw_data is None:
        try:
            raw_data = json.loads(str(getattr(current, "raw_text", current) or ""))
        except (json.JSONDecodeError, TypeError):
            return False

    def strip_ids(items: Any) -> Any:
        if isinstance(items, list):
            return [strip_ids(item) for item in items]
        if isinstance(items, dict):
            return {key: strip_ids(value) for key, value in items.items() if key != "id"}
        return items

    try:
        current_data = list(raw_data) if not isinstance(raw_data, dict) else dict(raw_data)
    except TypeError:
        current_data = raw_data
    return strip_ids(current_data) == strip_ids(desired)


def _scalar_missing(current: Any) -> bool:
    """Return True when a scalar field has no editor-owned content yet."""
    return current is None or str(current) == ""


def _stream_missing(current: Any) -> bool:
    """Return True when a StreamField has no editor-owned blocks yet."""
    raw_data = getattr(current, "raw_data", None)
    if raw_data is not None:
        try:
            return len(raw_data) == 0
        except TypeError:
            return not raw_data
    raw_text = str(getattr(current, "raw_text", current) or "")
    if raw_text == "":
        return True
    try:
        return json.loads(raw_text) == []
    except (json.JSONDecodeError, TypeError):
        return False


EXACT_VERIFICATION_SENTINELS: dict[str, Any] = {
    "public_h1": "VERIFY CUSTOM H1",
    "photo_carousel_title": "VERIFY CUSTOM CAROUSEL",
    "intro": "VERIFY CUSTOM INTRO",
    "short_description": "VERIFY CUSTOM SHORT",
    "hero_usp": "VERIFY CUSTOM USP",
    "body": "<p>VERIFY CUSTOM BODY</p>",
    "problems": ["VERIFY CUSTOM PROBLEM"],
    "benefits": [("VERIFY CUSTOM BENEFIT", "VERIFY CUSTOM BENEFIT BODY")],
    "faq": [("VERIFY CUSTOM QUESTION", "VERIFY CUSTOM ANSWER")],
}


def repair_exact_verification_sentinels(page: Any, data: dict[str, Any]) -> bool:
    """Replace only the exact Phase 04 verification payload with seed values.

    These values came from a disposable-database negative control that was
    accidentally persisted as Wagtail revision 331. Exact whole-field matching
    keeps legitimate editor-authored content outside this bounded recovery.
    """

    changed = False
    scalar_replacements = {
        "public_h1": data.get("public_h1", ""),
        "photo_carousel_title": data.get("photo_carousel_title", ""),
        "intro": data.get("intro", ""),
        "short_description": data.get("short_description", ""),
        "hero_usp": data.get("hero_usp", ""),
        "body": data.get("body", ""),
    }
    for field, desired in scalar_replacements.items():
        sentinel = EXACT_VERIFICATION_SENTINELS[field]
        if str(getattr(page, field, "") or "") == str(sentinel):
            setattr(page, field, desired)
            changed = True

    stream_fields = (
        ("problems_we_fix", "problems", streamfield_problem_data),
        ("why_choose_us", "benefits", streamfield_benefit_data),
        ("faq", "faq", streamfield_faq_data),
    )
    for field, data_key, serializer in stream_fields:
        sentinel_json = serializer(EXACT_VERIFICATION_SENTINELS[data_key])
        desired_json = serializer(data.get(data_key, []))
        current = getattr(page, field)
        if _stream_equivalent(current, sentinel_json) and not _stream_equivalent(
            current, desired_json
        ):
            setattr(page, field, desired_json)
            changed = True
    return changed


def reconcile_service_page_seed_data(
    page: Any,
    desired: dict[str, Any],
    *,
    replace_if_matches: tuple[dict[str, Any], ...] = (),
) -> bool:
    """Apply desired content only to empty, copied/generated, or sentinel fields."""

    changed = False
    scalar_fields = (
        "title",
        "seo_title",
        "search_description",
        "intro",
        "short_description",
        "hero_usp",
        "body",
    )
    for field in scalar_fields:
        if field not in desired:
            continue
        current = getattr(page, field, None)
        generated_values = [source[field] for source in replace_if_matches if field in source]
        should_replace = (
            _scalar_missing(current)
            or any(str(current) == str(value) for value in generated_values)
            or str(current) == str(EXACT_VERIFICATION_SENTINELS.get(field, object()))
        )
        if should_replace and str(current) != str(desired[field]):
            setattr(page, field, desired[field])
            changed = True

    stream_fields = (
        ("problems_we_fix", "problems", streamfield_problem_data),
        ("why_choose_us", "benefits", streamfield_benefit_data),
        ("faq", "faq", streamfield_faq_data),
    )
    for field, data_key, serializer in stream_fields:
        if data_key not in desired:
            continue
        current = getattr(page, field)
        desired_json = serializer(desired[data_key])
        generated_json = [
            serializer(source[data_key])
            for source in replace_if_matches
            if data_key in source
        ]
        sentinel_json = serializer(EXACT_VERIFICATION_SENTINELS[data_key])
        should_replace = (
            _stream_missing(current)
            or any(_stream_equivalent(current, value) for value in generated_json)
            or _stream_equivalent(current, sentinel_json)
        )
        if should_replace and not _stream_equivalent(current, desired_json):
            setattr(page, field, desired_json)
            changed = True
    return changed


def apply_service_page_seed_data(page: Any, data: dict[str, Any]) -> bool:
    """Populate missing seeded ServicePage fields without overwriting editors."""
    changed = False
    for field in (
        "title",
        "seo_title",
        "search_description",
        "intro",
        "short_description",
        "hero_usp",
        "body",
    ):
        if field in data and _scalar_missing(getattr(page, field, None)):
            setattr(page, field, data[field])
            changed = True

    if "problems" in data:
        value = streamfield_problem_data(data["problems"])
        if _stream_missing(page.problems_we_fix) and not _stream_equivalent(page.problems_we_fix, value):
            page.problems_we_fix = value
            changed = True
    if "benefits" in data:
        value = streamfield_benefit_data(data["benefits"])
        if _stream_missing(page.why_choose_us) and not _stream_equivalent(page.why_choose_us, value):
            page.why_choose_us = value
            changed = True
    if "faq" in data:
        value = streamfield_faq_data(data["faq"])
        if _stream_missing(page.faq) and not _stream_equivalent(page.faq, value):
            page.faq = value
            changed = True
    return changed
