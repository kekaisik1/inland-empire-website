"""Seed data for card #7 high-end appliance brand landing pages."""

from __future__ import annotations

from typing import Any

HIGH_END_BRAND_PAGE_SLUGS: tuple[str, ...] = (
    "bosch-appliance-repair",
    "kitchenaid-appliance-repair",
    "sub-zero-appliance-repair",
    "thermador-appliance-repair",
    "miele-appliance-repair",
    "viking-appliance-repair",
    "speed-queen-appliance-repair",
    "fisher-paykel-appliance-repair",
    "monogram-appliance-repair",
    "wolf-appliance-repair",
)

_HIGH_END_BRAND_PAGE_SPECS: tuple[dict[str, Any], ...] = (
    {
        "brand": "Bosch",
        "title": "Bosch Appliance Repair",
        "slug": "bosch-appliance-repair",
        "spanish_title": "Reparación de Electrodomésticos Bosch",
        "seo_title": "Bosch Appliance Repair — Dishwasher & Oven Service",
        "spanish_seo_title": "Reparación de Electrodomésticos Bosch | Inland Empire Appliance Repair",
        "search_description": (
            "Bosch Appliance Repair for high-end appliance repair needs: "
            "dishwashers, refrigerators, ovens, ranges, and error diagnostics."
        ),
        "spanish_search_description": (
            "Reparación de Electrodomésticos Bosch para lavavajillas, "
            "refrigeradores, hornos, rangos y diagnóstico claro."
        ),
        "intro": (
            "Bosch appliance repair for quiet dishwashers, precision refrigerators, "
            "ovens, ranges, and error diagnostics"
        ),
        "spanish_intro": (
            "Reparación de electrodomésticos Bosch para lavavajillas silenciosos, "
            "refrigeradores precisos, hornos, rangos y diagnóstico de fallas"
        ),
        "short_description": "Bosch dishwasher, refrigerator, oven, and range diagnostics.",
        "spanish_short_description": (
            "Diagnóstico Bosch para lavavajillas, refrigeradores, hornos y rangos."
        ),
        "hero_usp": (
            "Careful Bosch diagnostics with same-day scheduling and "
            "warranty-backed repairs."
        ),
        "spanish_hero_usp": (
            "Diagnóstico Bosch cuidadoso, citas el mismo día y reparaciones con garantía."
        ),
        "sections": [
            (
                "Bosch Appliance Repair for Quiet, Precision Appliances",
                "Bosch kitchens often rely on quiet dishwashers, precise cooking, "
                "and integrated refrigeration. Inland Empire Appliance Repair diagnoses Bosch dishwashers, "
                "refrigerators, ovens, and ranges with model-specific testing before "
                "recommending parts.",
            ),
            (
                "Bosch Error Diagnostics Before Parts",
                "Panel codes, drain faults, heating issues, and cooling complaints can "
                "look similar from the outside. We run error diagnostics, inspect water "
                "and airflow paths, and explain the repair path clearly.",
            ),
            (
                "High-End Bosch Service Without Overpromising",
                "If a Bosch appliance needs a special-order component or a procedure "
                "outside normal field service, your technician documents the next step "
                "instead of making unsupported brand-affiliation claims.",
            ),
        ],
        "spanish_sections": [
            (
                "Servicio Bosch para equipos silenciosos y precisos",
                "Las cocinas Bosch suelen depender de lavavajillas silenciosos, "
                "refrigeradores precisos, hornos y rangos integrados. Inland Empire Appliance Repair diagnostica "
                "cada equipo con pruebas claras antes de recomendar piezas.",
            ),
            (
                "Diagnóstico de errores Bosch antes de cambiar piezas",
                "Códigos en pantalla, fallas de drenaje, problemas de calentamiento y "
                "quejas de enfriamiento pueden parecer iguales. Revisamos agua, aire y "
                "controles para explicar la ruta de reparación.",
            ),
            (
                "Servicio Bosch de alta gama con expectativas claras",
                "Si un equipo Bosch necesita una pieza especial o un procedimiento fuera "
                "del servicio normal en campo, lo explicamos sin hacer reclamos de "
                "respaldo directo del fabricante.",
            ),
        ],
        "problems": [
            "Bosch dishwasher not draining or showing an error code",
            "Bosch refrigerator not holding temperature",
            "Bosch oven or range not heating evenly",
            "Bosch dishwasher running loudly or leaving dishes wet",
            "Bosch control panel or sensor fault",
        ],
        "spanish_problems": [
            "Lavavajillas Bosch que no drena o muestra código de error",
            "Refrigerador Bosch que no mantiene temperatura",
            "Horno o rango Bosch que no calienta parejo",
            "Lavavajillas Bosch ruidoso o con platos mojados",
            "Falla de panel o sensor Bosch",
        ],
        "benefits": [
            (
                "Bosch-Focused Diagnostics",
                "Testing covers common Bosch dishwasher, refrigerator, oven, and range failure paths.",
            ),
            (
                "Quiet Appliance Care",
                "We check pumps, fans, seals, and controls that affect Bosch quiet-operation performance.",
            ),
            (
                "Clear Repair Options",
                "You receive an itemized quote and practical next steps before approving repair work.",
            ),
        ],
        "spanish_benefits": [
            (
                "Diagnóstico enfocado en Bosch",
                "Probamos fallas comunes en lavavajillas, refrigeradores, hornos y rangos Bosch.",
            ),
            (
                "Cuidado para equipos silenciosos",
                "Revisamos bombas, ventiladores, sellos y controles que afectan la operación silenciosa Bosch.",
            ),
            (
                "Opciones claras",
                "Recibe una cotización detallada y pasos prácticos antes de aprobar la reparación.",
            ),
        ],
        "faq": [
            (
                "Do you repair Bosch dishwashers?",
                "Yes. Bosch dishwasher drain, cleaning, drying, latch, and error-code issues are common service requests.",
            ),
            (
                "Can you diagnose Bosch refrigerators and ovens?",
                "Yes. We diagnose Bosch refrigerators, ovens, ranges, and related control or sensor faults when service access is available.",
            ),
            (
                "Will you claim Bosch brand affiliation?",
                "No. We avoid unsupported authorization claims and explain parts, warranty, and service scope clearly.",
            ),
        ],
        "spanish_faq": [
            (
                "¿Reparan lavavajillas Bosch?",
                "Sí. Atendemos drenaje, limpieza, secado, pestillos y códigos de error en lavavajillas Bosch.",
            ),
            (
                "¿Diagnostican refrigeradores y hornos Bosch?",
                "Sí. Diagnosticamos refrigeradores, hornos, rangos y fallas de sensores o controles Bosch cuando hay acceso de servicio.",
            ),
            (
                "¿Van a decir que son autorizados por Bosch?",
                "No. Evitamos reclamos no respaldados y explicamos piezas, garantía y alcance de servicio con claridad.",
            ),
        ],
        "related": [
            "high-end-appliance-repair",
            "dishwasher-repair",
            "refrigerator-repair",
            "oven-repair",
            "stove-repair",
        ],
    },
    {
        "brand": "KitchenAid",
        "title": "KitchenAid Appliance Repair",
        "slug": "kitchenaid-appliance-repair",
        "spanish_title": "Reparación de Electrodomésticos KitchenAid",
        "seo_title": "KitchenAid Appliance Repair — Built-In Kitchen Service",
        "spanish_seo_title": "Reparación de Electrodomésticos KitchenAid | Inland Empire Appliance Repair",
        "search_description": (
            "KitchenAid Appliance Repair for high-end appliance repair needs: "
            "built-in refrigerators, dishwashers, ranges, ovens, and kitchen suites."
        ),
        "spanish_search_description": (
            "Reparación de Electrodomésticos KitchenAid para refrigeradores "
            "empotrados, lavavajillas, rangos, hornos y suites de cocina."
        ),
        "intro": (
            "KitchenAid appliance repair for built-in refrigerators, dishwashers, "
            "ranges, ovens, and kitchen suites"
        ),
        "spanish_intro": (
            "Reparación de electrodomésticos KitchenAid para refrigeradores "
            "empotrados, lavavajillas, rangos, hornos y suites de cocina"
        ),
        "short_description": (
            "KitchenAid built-in refrigerator, dishwasher, range, and oven repair."
        ),
        "spanish_short_description": (
            "Servicio KitchenAid para refrigeradores empotrados, lavavajillas, rangos y hornos."
        ),
        "hero_usp": (
            "KitchenAid suite diagnostics with practical scheduling, clear quotes, "
            "and warranty-backed repair."
        ),
        "spanish_hero_usp": (
            "Diagnóstico KitchenAid con citas prácticas, cotización clara y reparación con garantía."
        ),
        "sections": [
            (
                "KitchenAid Appliance Repair for Premium Kitchen Suites",
                "KitchenAid kitchens often combine built-in refrigerators, wall ovens, "
                "ranges, dishwashers, and specialty cooking appliances. We diagnose "
                "the appliance in front of us and keep the repair scope clear.",
            ),
            (
                "Built-In Refrigerators, Ranges, and Dishwashers",
                "Cooling failures, range ignition problems, oven temperature swings, "
                "and dishwasher drain issues need different tests. Inland Empire Appliance Repair checks sensors, "
                "fans, valves, pumps, igniters, and controls before quoting repair.",
            ),
            (
                "Appliance-Service Scope for KitchenAid Mixers",
                "If your KitchenAid request involves a mixer or countertop appliance, "
                "we will confirm whether it fits our appliance-service scope before "
                "scheduling so expectations stay accurate.",
            ),
        ],
        "spanish_sections": [
            (
                "Servicio KitchenAid para suites de cocina premium",
                "Las cocinas KitchenAid combinan refrigeradores empotrados, hornos de "
                "pared, rangos, lavavajillas y equipos especiales. Diagnosticamos el "
                "equipo específico y mantenemos claro el alcance.",
            ),
            (
                "Refrigeradores empotrados, rangos y lavavajillas",
                "Fallas de enfriamiento, problemas de encendido en rangos, cambios de "
                "temperatura en hornos y drenaje de lavavajillas requieren pruebas "
                "distintas antes de cotizar.",
            ),
            (
                "Alcance de servicio para batidoras KitchenAid",
                "Si su solicitud incluye una batidora o equipo de encimera, confirmamos "
                "primero si entra en nuestro alcance de reparación de electrodomésticos.",
            ),
        ],
        "problems": [
            "KitchenAid built-in refrigerator not cooling",
            "KitchenAid dishwasher not draining or cleaning",
            "KitchenAid range burner or igniter issue",
            "KitchenAid oven temperature swings",
            "KitchenAid kitchen suite control fault",
        ],
        "spanish_problems": [
            "Refrigerador empotrado KitchenAid que no enfría",
            "Lavavajillas KitchenAid que no drena o no limpia",
            "Quemador o encendedor de rango KitchenAid con falla",
            "Horno KitchenAid con cambios de temperatura",
            "Falla de control en suite KitchenAid",
        ],
        "benefits": [
            (
                "Kitchen Suite Coverage",
                "Service covers KitchenAid refrigeration, cooking, and dishwashing appliances.",
            ),
            (
                "Built-In Care",
                "We account for cabinetry, airflow, water lines, and installation details around built-in appliances.",
            ),
            (
                "Scope Clarity",
                "Countertop or mixer requests are screened so you do not book the wrong service.",
            ),
        ],
        "spanish_benefits": [
            ("Cobertura de suite KitchenAid", "Servicio para refrigeración, cocción y lavavajillas KitchenAid."),
            ("Cuidado para equipos empotrados", "Consideramos gabinetes, flujo de aire, líneas de agua e instalación."),
            ("Alcance claro", "Revisamos solicitudes de encimera o batidoras antes de agendar el servicio incorrecto."),
        ],
        "faq": [
            ("Do you repair KitchenAid built-in refrigerators?", "Yes, when the unit has service access and parts are available."),
            ("Can you repair KitchenAid dishwashers and ranges?", "Yes. We diagnose dishwasher drain/cleaning issues and range or oven heating problems."),
            ("Do you service KitchenAid stand mixers?", "Only if the request fits our appliance-service scope; we confirm this before scheduling."),
        ],
        "spanish_faq": [
            ("¿Reparan refrigeradores empotrados KitchenAid?", "Sí, cuando la unidad tiene acceso de servicio y piezas disponibles."),
            ("¿Reparan lavavajillas y rangos KitchenAid?", "Sí. Diagnosticamos drenaje, limpieza, calentamiento y encendido."),
            ("¿Reparan batidoras KitchenAid?", "Solo si la solicitud entra en nuestro alcance de servicio; lo confirmamos antes de agendar."),
        ],
        "related": [
            "high-end-appliance-repair",
            "refrigerator-repair",
            "dishwasher-repair",
            "oven-repair",
            "stove-repair",
        ],
    },
    {
        "brand": "Sub-Zero",
        "title": "Sub-Zero Appliance Repair",
        "slug": "sub-zero-appliance-repair",
        "spanish_title": "Reparación de Electrodomésticos Sub-Zero",
        "seo_title": "Sub-Zero Appliance Repair — Built-In Refrigeration",
        "spanish_seo_title": "Reparación de Electrodomésticos Sub-Zero | Inland Empire Appliance Repair",
        "search_description": (
            "Sub-Zero Appliance Repair for high-end appliance repair needs: "
            "built-in refrigeration, wine storage, ice makers, and sealed system diagnostics."
        ),
        "spanish_search_description": (
            "Reparación de Electrodomésticos Sub-Zero para refrigeración empotrada, "
            "vinos, fábrica de hielo y diagnóstico de sistema sellado."
        ),
        "intro": (
            "Sub-Zero appliance repair for built-in refrigeration, wine storage, "
            "ice makers, and preservation urgency"
        ),
        "spanish_intro": (
            "Reparación de electrodomésticos Sub-Zero para refrigeración empotrada, "
            "vinos, fábrica de hielo y urgencias de conservación"
        ),
        "short_description": (
            "Sub-Zero built-in refrigerator, freezer, wine storage, and ice maker diagnostics."
        ),
        "spanish_short_description": (
            "Diagnóstico Sub-Zero para refrigerador empotrado, congelador, vinos y hielo."
        ),
        "hero_usp": (
            "Urgent Sub-Zero cooling diagnostics for preservation-focused refrigeration systems."
        ),
        "spanish_hero_usp": (
            "Diagnóstico urgente Sub-Zero para sistemas de refrigeración enfocados en conservación."
        ),
        "sections": [
            (
                "Sub-Zero Appliance Repair for Preservation Urgency",
                "When built-in refrigeration or wine storage loses temperature, food and "
                "collections can be at risk. Inland Empire Appliance Repair prioritizes clear Sub-Zero diagnostics "
                "for cooling, freezer, ice maker, and air-flow complaints.",
            ),
            (
                "Built-In Refrigeration and Wine Storage",
                "Sub-Zero systems depend on sensors, fans, sealed system components, "
                "door seals, condensers, and controls working together. We identify the "
                "failure path before recommending parts.",
            ),
            (
                "Sealed System Diagnostic Boundaries",
                "If a sealed system issue requires specialized equipment, parts, or "
                "factory procedure beyond normal field service, we explain that boundary "
                "and the practical next step.",
            ),
        ],
        "spanish_sections": [
            (
                "Servicio Sub-Zero cuando la conservación es urgente",
                "Si la refrigeración empotrada o el almacenamiento de vinos pierde "
                "temperatura, alimentos y colecciones pueden estar en riesgo. Inland Empire Appliance Repair "
                "prioriza diagnóstico claro para enfriamiento, hielo y flujo de aire.",
            ),
            (
                "Refrigeración empotrada y almacenamiento de vinos",
                "Los sistemas Sub-Zero dependen de sensores, ventiladores, componentes "
                "de sistema sellado, sellos, condensadores y controles trabajando juntos.",
            ),
            (
                "Límites de diagnóstico de sistema sellado",
                "Si un sistema sellado requiere equipo, piezas o procedimiento especial "
                "fuera del servicio normal, explicamos ese límite y el siguiente paso.",
            ),
        ],
        "problems": [
            "Sub-Zero built-in refrigerator warming up",
            "Sub-Zero freezer not holding temperature",
            "Sub-Zero wine storage temperature swing",
            "Sub-Zero ice maker or water issue",
            "Possible Sub-Zero sealed system fault",
        ],
        "spanish_problems": [
            "Refrigerador empotrado Sub-Zero que sube de temperatura",
            "Congelador Sub-Zero que no mantiene temperatura",
            "Cambio de temperatura en almacenamiento de vinos Sub-Zero",
            "Problema de agua o fábrica de hielo Sub-Zero",
            "Posible falla de sistema sellado Sub-Zero",
        ],
        "benefits": [
            ("Preservation Focus", "Cooling complaints are treated with urgency because food and wine storage can be time-sensitive."),
            ("Built-In Awareness", "We account for cabinetry, condenser access, airflow, and door sealing on integrated units."),
            ("Honest Sealed-System Scope", "We document when a specialized repair path is required."),
        ],
        "spanish_benefits": [
            ("Enfoque en conservación", "Atendemos quejas de enfriamiento con urgencia por alimentos y vinos."),
            ("Conciencia de equipos empotrados", "Consideramos gabinetes, condensador, flujo de aire y sellos."),
            ("Alcance honesto de sistema sellado", "Documentamos cuando se requiere una ruta de reparación especializada."),
        ],
        "faq": [
            ("Can you diagnose Sub-Zero built-in refrigerators?", "Yes. We diagnose cooling, freezer, fan, ice maker, control, and airflow issues when service access is available."),
            ("Do Sub-Zero cooling issues need urgent service?", "Often yes. Warm built-in refrigeration can threaten food or wine preservation, so prompt diagnosis matters."),
            ("Do you overpromise sealed system repairs?", "No. We explain clearly if the repair needs specialized sealed-system steps outside normal field scope."),
        ],
        "spanish_faq": [
            ("¿Diagnostican refrigeradores empotrados Sub-Zero?", "Sí. Revisamos enfriamiento, congelador, ventiladores, hielo, controles y flujo de aire cuando hay acceso."),
            ("¿Las fallas de enfriamiento Sub-Zero son urgentes?", "A menudo sí. La pérdida de temperatura puede afectar alimentos o vinos, así que el diagnóstico rápido importa."),
            ("¿Prometen de más con sistemas sellados?", "No. Explicamos si la reparación necesita pasos especializados fuera del alcance normal."),
        ],
        "related": ["high-end-appliance-repair", "refrigerator-repair", "freezer-repair"],
    },
    {
        "brand": "Thermador",
        "title": "Thermador Appliance Repair",
        "slug": "thermador-appliance-repair",
        "spanish_title": "Reparación de Electrodomésticos Thermador",
        "seo_title": "Thermador Appliance Repair — Pro-Style Kitchen Service",
        "spanish_seo_title": "Reparación de Electrodomésticos Thermador | Inland Empire Appliance Repair",
        "search_description": (
            "Thermador Appliance Repair for high-end appliance repair needs: "
            "pro-style ranges, wall ovens, dishwashers, and built-in refrigeration."
        ),
        "spanish_search_description": (
            "Reparación de Electrodomésticos Thermador para rangos profesionales, "
            "hornos de pared, lavavajillas y refrigeración empotrada."
        ),
        "intro": (
            "Thermador appliance repair for pro-style ranges, wall ovens, "
            "dishwashers, cooktops, and built-in refrigeration"
        ),
        "spanish_intro": (
            "Reparación de electrodomésticos Thermador para rangos profesionales, "
            "hornos de pared, lavavajillas, cubiertas y refrigeración empotrada"
        ),
        "short_description": (
            "Thermador ranges, wall ovens, dishwashers, cooktops, and built-in refrigeration."
        ),
        "spanish_short_description": (
            "Servicio Thermador para rangos, hornos de pared, lavavajillas y refrigeración."
        ),
        "hero_usp": (
            "Thermador diagnostics for pro-style cooking and integrated kitchen appliances."
        ),
        "spanish_hero_usp": (
            "Diagnóstico Thermador para cocción profesional y equipos integrados de cocina."
        ),
        "sections": [
            (
                "Thermador Appliance Repair for Pro-Style Kitchens",
                "Thermador cooking and refrigeration systems are often installed as "
                "part of a premium kitchen suite. We diagnose pro-style ranges, wall "
                "ovens, cooktops, dishwashers, and built-in refrigeration.",
            ),
            (
                "Ranges, Wall Ovens, and Dishwashers",
                "Ignition, temperature control, fan, drain, and wash problems need "
                "different test paths. Inland Empire Appliance Repair checks the specific Thermador appliance "
                "before quoting a repair.",
            ),
            (
                "Integrated Thermador Refrigeration",
                "For built-in refrigeration, we inspect airflow, sensors, door sealing, "
                "and cooling performance so the repair plan fits the installation.",
            ),
        ],
        "spanish_sections": [
            (
                "Servicio Thermador para cocinas de estilo profesional",
                "Los sistemas Thermador suelen formar parte de una suite premium. "
                "Diagnosticamos rangos profesionales, hornos de pared, cubiertas, "
                "lavavajillas y refrigeración empotrada.",
            ),
            (
                "Rangos, hornos de pared y lavavajillas",
                "Encendido, control de temperatura, ventiladores, drenaje y lavado "
                "requieren pruebas distintas antes de cotizar la reparación.",
            ),
            (
                "Refrigeración empotrada Thermador",
                "Revisamos flujo de aire, sensores, sellos de puerta y rendimiento de "
                "enfriamiento para que el plan se ajuste a la instalación.",
            ),
        ],
        "problems": [
            "Thermador pro-style range not igniting",
            "Thermador wall oven temperature problem",
            "Thermador dishwasher not draining",
            "Thermador cooktop burner issue",
            "Thermador built-in refrigerator not cooling",
        ],
        "spanish_problems": [
            "Rango profesional Thermador que no enciende",
            "Horno de pared Thermador con problema de temperatura",
            "Lavavajillas Thermador que no drena",
            "Quemador de cubierta Thermador con falla",
            "Refrigerador empotrado Thermador que no enfría",
        ],
        "benefits": [
            ("Pro-Style Cooking Focus", "Diagnostics cover ignition, burners, temperature sensors, fans, and controls."),
            ("Kitchen Suite Awareness", "Dishwashers and refrigeration are handled alongside Thermador cooking appliances."),
            ("Installation-Sensitive Repairs", "Built-in and pro-style appliances are checked with cabinet and airflow context in mind."),
        ],
        "spanish_benefits": [
            ("Enfoque en cocción profesional", "Revisamos encendido, quemadores, sensores de temperatura, ventiladores y controles."),
            ("Conciencia de suite de cocina", "Atendemos lavavajillas y refrigeración junto con equipos de cocción Thermador."),
            ("Reparaciones sensibles a la instalación", "Consideramos gabinetes y flujo de aire en equipos empotrados."),
        ],
        "faq": [
            ("Do you repair Thermador pro-style ranges?", "Yes. We diagnose burner, ignition, oven, fan, and temperature issues on Thermador cooking appliances."),
            ("Can you service Thermador dishwashers?", "Yes. Drain, wash, control, and water-fill issues are within normal dishwasher diagnostic scope."),
            ("Do you work on Thermador built-in refrigeration?", "Yes, when service access and parts availability make field diagnostics practical."),
        ],
        "spanish_faq": [
            ("¿Reparan rangos profesionales Thermador?", "Sí. Diagnosticamos quemadores, encendido, hornos, ventiladores y temperatura."),
            ("¿Atienden lavavajillas Thermador?", "Sí. Drenaje, lavado, controles y llenado de agua están dentro del diagnóstico normal."),
            ("¿Trabajan con refrigeración empotrada Thermador?", "Sí, cuando el acceso y la disponibilidad de piezas permiten diagnóstico en campo."),
        ],
        "related": [
            "high-end-appliance-repair",
            "stove-repair",
            "oven-repair",
            "dishwasher-repair",
            "refrigerator-repair",
        ],
    },
    {
        "brand": "Miele",
        "title": "Miele Appliance Repair",
        "slug": "miele-appliance-repair",
        "spanish_title": "Reparación de Electrodomésticos Miele",
        "seo_title": "Miele Appliance Repair — Premium Diagnostics",
        "spanish_seo_title": "Reparación de Electrodomésticos Miele | Inland Empire Appliance Repair",
        "search_description": (
            "Miele Appliance Repair for high-end appliance repair needs: "
            "dishwashers, laundry, ovens, cooktops, and premium diagnostics."
        ),
        "spanish_search_description": (
            "Reparación de Electrodomésticos Miele para lavavajillas, lavandería, "
            "hornos, cubiertas y diagnóstico premium."
        ),
        "intro": (
            "Miele appliance repair for dishwashers, laundry systems, ovens, "
            "cooktops, and premium diagnostics"
        ),
        "spanish_intro": (
            "Reparación de electrodomésticos Miele para lavavajillas, lavandería, "
            "hornos, cubiertas y diagnóstico premium"
        ),
        "short_description": "Miele dishwasher, laundry, oven, and cooktop diagnostics.",
        "spanish_short_description": "Diagnóstico Miele para lavavajillas, lavandería, hornos y cubiertas.",
        "hero_usp": (
            "Premium Miele diagnostics with careful testing before parts are replaced."
        ),
        "spanish_hero_usp": (
            "Diagnóstico premium Miele con pruebas cuidadosas antes de cambiar piezas."
        ),
        "sections": [
            (
                "Miele Appliance Repair for Premium Diagnostics",
                "Miele appliances reward careful testing. We diagnose premium Miele "
                "dishwashers, laundry systems, ovens, and cooktops before replacing "
                "parts so the repair targets the real fault.",
            ),
            (
                "Dishwashers, Laundry, and Cooking Appliances",
                "Common requests include dishwashers that will not drain or dry, laundry "
                "systems with error codes, ovens with temperature swings, and cooktops "
                "with control or heating faults.",
            ),
            (
                "Clear Scope for Premium Miele Service",
                "We explain whether a repair can be completed from stocked parts, needs "
                "a special-order component, or requires a specialized procedure outside "
                "normal field service.",
            ),
        ],
        "spanish_sections": [
            (
                "Servicio Miele con diagnóstico premium",
                "Los equipos Miele requieren pruebas cuidadosas. Diagnosticamos "
                "lavavajillas, lavandería, hornos y cubiertas Miele antes de cambiar "
                "piezas para apuntar a la falla real.",
            ),
            (
                "Lavavajillas, lavandería y cocción",
                "Atendemos lavavajillas que no drenan o no secan, lavandería con códigos "
                "de error, hornos con cambios de temperatura y cubiertas con fallas de "
                "calentamiento o control.",
            ),
            (
                "Alcance claro para servicio Miele premium",
                "Explicamos si la reparación se completa con piezas disponibles, requiere "
                "una pieza especial o necesita un procedimiento especializado.",
            ),
        ],
        "problems": [
            "Miele dishwasher not draining or drying",
            "Miele washer or dryer error code",
            "Miele oven temperature issue",
            "Miele cooktop not heating",
            "Miele control or sensor diagnostic request",
        ],
        "spanish_problems": [
            "Lavavajillas Miele que no drena o no seca",
            "Código de error en lavadora o secadora Miele",
            "Horno Miele con problema de temperatura",
            "Cubierta Miele que no calienta",
            "Solicitud de diagnóstico de control o sensor Miele",
        ],
        "benefits": [
            ("Premium Diagnostic Process", "We test components and controls before quoting Miele repairs."),
            ("Dishwasher & Laundry Coverage", "Service includes common Miele cleaning, drying, draining, and laundry performance issues."),
            ("No Fabricated Logo Claims", "Miele appears as a safe text fallback unless a verified logo asset is available."),
        ],
        "spanish_benefits": [
            ("Proceso de diagnóstico premium", "Probamos componentes y controles antes de cotizar reparaciones Miele."),
            ("Cobertura de lavavajillas y lavandería", "Incluye limpieza, secado, drenaje y rendimiento de lavandería Miele."),
            ("Sin reclamos de logo fabricados", "Miele se muestra como texto seguro si no hay logo verificado."),
        ],
        "faq": [
            ("Do you repair Miele dishwashers?", "Yes. We diagnose drain, wash, drying, latch, sensor, and control issues."),
            ("Can you service Miele laundry appliances?", "Yes, when the washer or dryer has service access and parts can be sourced."),
            ("Why is Miele shown as text in brand cards?", "No safe local logo asset is available in this project, so we use a non-fabricated text fallback."),
        ],
        "spanish_faq": [
            ("¿Reparan lavavajillas Miele?", "Sí. Diagnosticamos drenaje, lavado, secado, pestillos, sensores y controles."),
            ("¿Atienden lavandería Miele?", "Sí, cuando la lavadora o secadora tiene acceso de servicio y piezas disponibles."),
            ("¿Por qué Miele aparece como texto?", "No hay un logo local verificado en el proyecto, así que usamos texto seguro."),
        ],
        "related": [
            "high-end-appliance-repair",
            "dishwasher-repair",
            "washer-repair",
            "dryer-repair",
            "oven-repair",
        ],
    },
    {
        "brand": "Viking",
        "title": "Viking Appliance Repair",
        "slug": "viking-appliance-repair",
        "spanish_title": "Reparación de Electrodomésticos Viking",
        "seo_title": "Viking Appliance Repair — Professional-Style Service",
        "spanish_seo_title": "Reparación de Electrodomésticos Viking | Inland Empire Appliance Repair",
        "search_description": (
            "Viking Appliance Repair for high-end appliance repair needs: "
            "professional-style ranges, ovens, cooktops, and refrigeration."
        ),
        "spanish_search_description": (
            "Reparación de Electrodomésticos Viking para rangos estilo profesional, "
            "hornos, cubiertas y refrigeración."
        ),
        "intro": (
            "Viking appliance repair for professional-style ranges, ovens, cooktops, "
            "refrigeration, and premium kitchen performance"
        ),
        "spanish_intro": (
            "Reparación de electrodomésticos Viking para rangos estilo profesional, "
            "hornos, cubiertas, refrigeración y rendimiento premium"
        ),
        "short_description": "Viking professional-style ranges, ovens, cooktops, and refrigeration.",
        "spanish_short_description": "Servicio Viking para rangos estilo profesional, hornos, cubiertas y refrigeración.",
        "hero_usp": (
            "Professional-style Viking diagnostics for cooking and refrigeration appliances."
        ),
        "spanish_hero_usp": (
            "Diagnóstico Viking para equipos de cocción y refrigeración estilo profesional."
        ),
        "sections": [
            (
                "Viking Appliance Repair for Professional-Style Kitchens",
                "Viking appliances are often chosen for professional-style ranges, "
                "ovens, cooktops, and refrigeration. Inland Empire Appliance Repair diagnoses cooking, cooling, "
                "ignition, airflow, and control concerns with a practical repair plan.",
            ),
            (
                "Ranges, Ovens, and Refrigeration",
                "A Viking range that will not ignite needs different testing than a "
                "refrigerator that is warming or an oven that drifts from set point. "
                "We inspect the failed system first.",
            ),
            (
                "Premium Kitchen Service With Clear Limits",
                "We do not claim unsupported brand affiliation. If the Viking unit "
                "needs a special part or manufacturer procedure, we say so during diagnosis.",
            ),
        ],
        "spanish_sections": [
            (
                "Servicio Viking para cocinas estilo profesional",
                "Los equipos Viking se eligen por rangos estilo profesional, hornos, "
                "cubiertas y refrigeración. Diagnosticamos cocción, enfriamiento, "
                "encendido, flujo de aire y controles con un plan práctico.",
            ),
            (
                "Rangos, hornos y refrigeración",
                "Un rango Viking que no enciende requiere pruebas distintas a un "
                "refrigerador que se calienta o un horno que pierde temperatura.",
            ),
            (
                "Servicio premium con límites claros",
                "No hacemos reclamos de autorización no respaldados. Si la unidad "
                "necesita pieza o procedimiento especial, lo explicamos.",
            ),
        ],
        "problems": [
            "Viking professional-style range not igniting",
            "Viking oven not heating evenly",
            "Viking refrigerator not cooling",
            "Viking cooktop burner problem",
            "Viking control or sensor issue",
        ],
        "spanish_problems": [
            "Rango estilo profesional Viking que no enciende",
            "Horno Viking que no calienta parejo",
            "Refrigerador Viking que no enfría",
            "Quemador de cubierta Viking con problema",
            "Falla de control o sensor Viking",
        ],
        "benefits": [
            ("Professional-Style Cooking", "Diagnostics cover ignition, gas, electric, temperature, fan, and control concerns."),
            ("Refrigeration Support", "Viking cooling complaints are checked with airflow, seal, and temperature context."),
            ("Clear Limits", "We avoid unsupported authorization language and document specialized needs."),
        ],
        "spanish_benefits": [
            ("Cocción estilo profesional", "Revisamos encendido, gas, electricidad, temperatura, ventiladores y controles."),
            ("Soporte de refrigeración", "Revisamos enfriamiento Viking con contexto de flujo de aire, sellos y temperatura."),
            ("Límites claros", "Evitamos lenguaje de autorización no respaldado y documentamos necesidades especiales."),
        ],
        "faq": [
            ("Do you repair Viking ranges?", "Yes. We diagnose ignition, burner, oven, control, and temperature issues."),
            ("Can you service Viking refrigerators?", "Yes, when service access and parts availability allow field diagnostics."),
            ("Are you affiliated with Viking?", "We do not make unsupported affiliation claims; we provide practical diagnostic and repair options."),
        ],
        "spanish_faq": [
            ("¿Reparan rangos Viking?", "Sí. Diagnosticamos encendido, quemadores, hornos, controles y temperatura."),
            ("¿Atienden refrigeradores Viking?", "Sí, cuando el acceso y las piezas permiten diagnóstico en campo."),
            ("¿Son autorizados por Viking?", "No hacemos reclamos no respaldados de autorización; damos opciones prácticas."),
        ],
        "related": ["high-end-appliance-repair", "stove-repair", "oven-repair", "refrigerator-repair"],
    },
    {
        "brand": "Speed Queen",
        "title": "Speed Queen Appliance Repair",
        "slug": "speed-queen-appliance-repair",
        "spanish_title": "Reparación de Electrodomésticos Speed Queen",
        "seo_title": "Speed Queen Appliance Repair — Washer & Dryer Service",
        "spanish_seo_title": "Reparación de Electrodomésticos Speed Queen | Inland Empire Appliance Repair",
        "search_description": (
            "Speed Queen Appliance Repair for high-end appliance repair needs: "
            "washers, dryers, durable laundry systems, and laundromat overlap."
        ),
        "spanish_search_description": (
            "Reparación de Electrodomésticos Speed Queen para lavadoras, secadoras, "
            "sistemas duraderos y lavandería comercial cuando aplica."
        ),
        "intro": (
            "Speed Queen appliance repair for washers, dryers, durable laundry systems, "
            "and safe laundromat or commercial overlap"
        ),
        "spanish_intro": (
            "Reparación de electrodomésticos Speed Queen para lavadoras, secadoras, "
            "sistemas duraderos y lavandería comercial cuando aplica"
        ),
        "short_description": "Speed Queen washer, dryer, and durable laundry system diagnostics.",
        "spanish_short_description": "Diagnóstico Speed Queen para lavadoras, secadoras y sistemas duraderos.",
        "hero_usp": (
            "Durable Speed Queen laundry diagnostics for homes and appropriate "
            "commercial-overlap requests."
        ),
        "spanish_hero_usp": (
            "Diagnóstico Speed Queen para lavandería duradera en hogares y casos comerciales apropiados."
        ),
        "sections": [
            (
                "Speed Queen Appliance Repair for Durable Laundry",
                "Speed Queen is known for washers and dryers built for heavy use. Inland Empire Appliance Repair "
                "diagnoses home laundry systems and appropriate laundromat or commercial "
                "overlap requests when parts and service access are practical.",
            ),
            (
                "Washers and Dryers That Need Reliable Cycles",
                "Drain, spin, heating, airflow, timer, belt, and control issues can stop "
                "a laundry routine quickly. We identify the failed system before quoting repair.",
            ),
            (
                "Commercial-Overlap Scope Kept Safe",
                "Some Speed Queen requests involve laundromat-style equipment. We confirm "
                "service access and part availability before committing to field repair.",
            ),
        ],
        "spanish_sections": [
            (
                "Servicio Speed Queen para lavandería duradera",
                "Speed Queen es conocida por lavadoras y secadoras de uso intenso. Inland Empire Appliance Repair "
                "diagnostica sistemas de hogar y casos de lavandería comercial cuando el "
                "acceso y las piezas lo permiten.",
            ),
            (
                "Lavadoras y secadoras con ciclos confiables",
                "Drenaje, centrifugado, calor, flujo de aire, temporizadores, correas y "
                "controles pueden detener la rutina de lavandería rápidamente.",
            ),
            (
                "Alcance seguro para lavandería comercial",
                "Algunas solicitudes Speed Queen involucran equipos tipo laundromat. "
                "Confirmamos acceso y piezas antes de prometer reparación en campo.",
            ),
        ],
        "problems": [
            "Speed Queen washer not draining or spinning",
            "Speed Queen dryer not heating",
            "Speed Queen laundry system making noise",
            "Speed Queen timer or control issue",
            "Speed Queen laundromat-style service access question",
        ],
        "spanish_problems": [
            "Lavadora Speed Queen que no drena o centrifuga",
            "Secadora Speed Queen que no calienta",
            "Sistema Speed Queen con ruido",
            "Falla de temporizador o control Speed Queen",
            "Pregunta de acceso para equipo Speed Queen tipo lavandería comercial",
        ],
        "benefits": [
            ("Laundry-System Focus", "Washer and dryer diagnostics cover the failure points that interrupt laundry quickly."),
            ("Durability Mindset", "We quote repairs that fit the heavy-use nature of Speed Queen systems."),
            ("Safe Commercial Overlap", "Laundromat-style requests are screened for access and part availability first."),
        ],
        "spanish_benefits": [
            ("Enfoque en lavandería", "Diagnosticamos fallas de lavadoras y secadoras que interrumpen la rutina."),
            ("Mentalidad de durabilidad", "Cotizamos reparaciones acordes con equipos Speed Queen de uso intenso."),
            ("Alcance comercial seguro", "Casos tipo laundromat se revisan por acceso y piezas primero."),
        ],
        "faq": [
            ("Do you repair Speed Queen washers and dryers?", "Yes. We diagnose common drain, spin, heat, airflow, timer, and control issues."),
            ("Can you help with laundromat-style Speed Queen equipment?", "Sometimes. We confirm service access, parts, and scope before scheduling."),
            ("Do Speed Queen repairs include a warranty?", "Approved repairs include warranty coverage on parts and labor."),
        ],
        "spanish_faq": [
            ("¿Reparan lavadoras y secadoras Speed Queen?", "Sí. Diagnosticamos drenaje, centrifugado, calor, flujo de aire, temporizador y controles."),
            ("¿Pueden ayudar con equipo Speed Queen tipo laundromat?", "A veces. Confirmamos acceso, piezas y alcance antes de agendar."),
            ("¿Las reparaciones Speed Queen tienen garantía?", "Las reparaciones aprobadas incluyen garantía en piezas y mano de obra."),
        ],
        "related": [
            "high-end-appliance-repair",
            "washer-repair",
            "dryer-repair",
            "commercial-appliance-repair",
        ],
    },
    {
        "brand": "Fisher & Paykel",
        "title": "Fisher & Paykel Appliance Repair",
        "slug": "fisher-paykel-appliance-repair",
        "spanish_title": "Reparación de Electrodomésticos Fisher & Paykel",
        "seo_title": "Fisher & Paykel Appliance Repair — DishDrawer Service",
        "spanish_seo_title": "Reparación de Electrodomésticos Fisher & Paykel | Inland Empire Appliance Repair",
        "search_description": (
            "Fisher & Paykel Appliance Repair for high-end appliance repair needs: "
            "DishDrawer dishwashers, refrigerators, ranges, and integrated appliances."
        ),
        "spanish_search_description": (
            "Reparación de Electrodomésticos Fisher & Paykel para DishDrawer, "
            "refrigeradores, rangos y electrodomésticos integrados."
        ),
        "intro": (
            "Fisher & Paykel appliance repair for DishDrawer dishwashers, "
            "refrigerators, ranges, and premium integrated appliances"
        ),
        "spanish_intro": (
            "Reparación de electrodomésticos Fisher & Paykel para lavavajillas "
            "DishDrawer, refrigeradores, rangos y electrodomésticos integrados premium"
        ),
        "short_description": (
            "Fisher & Paykel DishDrawer, refrigerator, range, and integrated appliance diagnostics."
        ),
        "spanish_short_description": (
            "Diagnóstico Fisher & Paykel para DishDrawer, refrigeradores, rangos e integrados."
        ),
        "hero_usp": (
            "Fisher & Paykel diagnostics for DishDrawer dishwashers and integrated kitchen appliances."
        ),
        "spanish_hero_usp": (
            "Diagnóstico Fisher & Paykel para DishDrawer y electrodomésticos integrados de cocina."
        ),
        "sections": [
            (
                "Fisher & Paykel Appliance Repair for Integrated Kitchens",
                "Fisher & Paykel appliances often appear in premium integrated kitchens. "
                "Inland Empire Appliance Repair diagnoses DishDrawer dishwashers, refrigerators, ranges, and other "
                "integrated appliances with careful access and installation awareness.",
            ),
            (
                "DishDrawer Dishwashers, Refrigerators, and Ranges",
                "DishDrawer drain or fill issues, refrigerator cooling problems, and "
                "range heating complaints each need a different diagnostic path. We test "
                "the affected system before quoting repair.",
            ),
            (
                "Safe Text Fallback for Brand Cards",
                "No verified Fisher & Paykel logo asset is stored in this project, so "
                "the public brand cards use the exact brand name as text rather than a "
                "fabricated logo.",
            ),
        ],
        "spanish_sections": [
            (
                "Servicio Fisher & Paykel para cocinas integradas",
                "Los equipos Fisher & Paykel suelen estar en cocinas premium integradas. "
                "Diagnosticamos DishDrawer, refrigeradores, rangos y otros "
                "electrodomésticos integrados considerando acceso e instalación.",
            ),
            (
                "DishDrawer, refrigeradores y rangos",
                "Fallas de drenaje o llenado en DishDrawer, problemas de enfriamiento en "
                "refrigeradores y quejas de calentamiento en rangos requieren rutas de "
                "diagnóstico distintas.",
            ),
            (
                "Texto seguro para tarjetas de marca",
                "No hay logo Fisher & Paykel verificado en el proyecto, así que las "
                "tarjetas usan el nombre exacto como texto en lugar de un logo fabricado.",
            ),
        ],
        "problems": [
            "Fisher & Paykel DishDrawer not draining or filling",
            "Fisher & Paykel refrigerator not cooling",
            "Fisher & Paykel range not heating evenly",
            "Fisher & Paykel integrated appliance access issue",
            "Fisher & Paykel control or sensor fault",
        ],
        "spanish_problems": [
            "DishDrawer Fisher & Paykel que no drena o no llena",
            "Refrigerador Fisher & Paykel que no enfría",
            "Rango Fisher & Paykel que no calienta parejo",
            "Problema de acceso en electrodoméstico integrado Fisher & Paykel",
            "Falla de control o sensor Fisher & Paykel",
        ],
        "benefits": [
            ("DishDrawer Familiarity", "Diagnostics account for drawer-style dishwasher drain, fill, and latch behavior."),
            ("Integrated Appliance Care", "We consider cabinet fit, access, airflow, and water connections before repair."),
            ("No Fabricated Assets", "Brand cards use a safe text fallback when no sourced logo is available."),
        ],
        "spanish_benefits": [
            ("Conocimiento de DishDrawer", "El diagnóstico considera drenaje, llenado y pestillos de lavavajillas tipo cajón."),
            ("Cuidado para integrados", "Consideramos gabinetes, acceso, flujo de aire y conexiones de agua."),
            ("Sin activos fabricados", "Las tarjetas usan texto seguro si no hay logo verificado."),
        ],
        "faq": [
            ("Do you repair Fisher & Paykel DishDrawer dishwashers?", "Yes. We diagnose drain, fill, latch, wash, and control issues when service access is available."),
            ("Can you repair Fisher & Paykel refrigerators and ranges?", "Yes. We diagnose cooling, heating, sensor, and control complaints on serviceable units."),
            ("Why is Fisher & Paykel shown as text in brand cards?", "No safe local logo asset is available in this project, so the exact brand name is rendered as text."),
        ],
        "spanish_faq": [
            ("¿Reparan lavavajillas DishDrawer Fisher & Paykel?", "Sí. Diagnosticamos drenaje, llenado, pestillos, lavado y controles cuando hay acceso."),
            ("¿Reparan refrigeradores y rangos Fisher & Paykel?", "Sí. Diagnosticamos enfriamiento, calentamiento, sensores y controles en unidades reparables."),
            ("¿Por qué Fisher & Paykel aparece como texto?", "No hay logo local seguro en el proyecto, así que se muestra el nombre exacto."),
        ],
        "related": [
            "high-end-appliance-repair",
            "dishwasher-repair",
            "refrigerator-repair",
            "stove-repair",
        ],
    },
)

_CARD17_BRAND_PAGE_SPECS: tuple[dict[str, Any], ...] = (
    {
        "brand": "Monogram",
        "title": "Monogram Appliance Repair",
        "slug": "monogram-appliance-repair",
        "spanish_title": "Reparación de Electrodomésticos Monogram",
        "seo_title": "Monogram Appliance Repair — Premium Kitchen Service",
        "spanish_seo_title": "Reparación de Electrodomésticos Monogram | Inland Empire Appliance Repair",
        "search_description": "Monogram Appliance Repair for high-end appliance repair needs: built-in refrigeration, premium cooking, dishwashers, and kitchen diagnostics.",
        "spanish_search_description": "Reparación de Electrodomésticos Monogram para refrigeración empotrada, cocción premium, lavavajillas y diagnóstico de cocina.",
        "intro": "Monogram appliance repair for built-in refrigeration, premium cooking, dishwashers, and integrated kitchen diagnostics",
        "spanish_intro": "Reparación de electrodomésticos Monogram para refrigeración empotrada, cocción premium, lavavajillas y diagnóstico de cocina integrada",
        "short_description": "Monogram built-in refrigeration, premium cooking, dishwasher, and kitchen diagnostics.",
        "spanish_short_description": "Diagnóstico Monogram para refrigeración empotrada, cocción premium y lavavajillas.",
        "hero_usp": "Careful Monogram diagnostics for premium GE luxury line kitchen appliances.",
        "spanish_hero_usp": "Diagnóstico cuidadoso Monogram para equipos de cocina premium de la línea de lujo de GE.",
        "sections": [
            ("Monogram Appliance Repair for Premium Built-In Kitchens", "Monogram is GE Appliances' luxury line for premium kitchens. Inland Empire Appliance Repair diagnoses Monogram built-in refrigeration, premium cooking appliances, dishwashers, and integrated kitchen systems without claiming manufacturer authorization."),
            ("Built-In Refrigeration and Premium Cooking Diagnostics", "Cooling complaints, oven temperature drift, range ignition issues, dishwasher faults, and control problems each need a different test path. We inspect the affected Monogram appliance before quoting repair."),
            ("GE Luxury Line Scope Kept Clear", "Monogram appliances can share GE-family context, but a standalone Monogram request still receives brand-specific diagnostics and clear limits on parts, warranty, and field-service scope."),
        ],
        "spanish_sections": [
            ("Servicio Monogram para cocinas premium empotradas", "Monogram es la línea de lujo de GE Appliances para cocinas premium. Inland Empire Appliance Repair diagnostica refrigeración empotrada, cocción premium, lavavajillas y sistemas integrados sin reclamar autorización del fabricante."),
            ("Diagnóstico de refrigeración empotrada y cocción premium", "Fallas de enfriamiento, cambios de temperatura en hornos, encendido de rangos, problemas de lavavajillas y controles requieren pruebas distintas antes de cotizar reparación."),
            ("Alcance claro para la línea de lujo de GE", "Los equipos Monogram pueden compartir contexto de la familia GE, pero cada solicitud recibe diagnóstico específico y límites claros sobre piezas, garantía y alcance de servicio en campo."),
        ],
        "problems": ["Monogram built-in refrigerator not cooling", "Monogram freezer or ice maker issue", "Monogram range or cooktop ignition problem", "Monogram wall oven temperature drift", "Monogram dishwasher or control fault"],
        "spanish_problems": ["Refrigerador empotrado Monogram que no enfría", "Problema de congelador o fábrica de hielo Monogram", "Rango o cubierta Monogram con falla de encendido", "Horno de pared Monogram con cambio de temperatura", "Falla de lavavajillas o control Monogram"],
        "benefits": [("Built-In Kitchen Awareness", "Diagnostics account for cabinetry, airflow, water connections, and service access."), ("Premium Cooking Focus", "We test burners, igniters, temperature sensors, fans, and controls before quoting repair."), ("No Authorization Claims", "Monogram copy stays clear about service scope without implying official GE or Monogram affiliation.")],
        "spanish_benefits": [("Conciencia de cocina empotrada", "Consideramos gabinetes, flujo de aire, agua y acceso de servicio."), ("Enfoque en cocción premium", "Probamos quemadores, encendedores, sensores, ventiladores y controles."), ("Sin reclamos de autorización", "El contenido Monogram mantiene claro el alcance sin implicar afiliación oficial con GE o Monogram.")],
        "faq": [("Do you repair Monogram built-in refrigerators?", "Yes. We diagnose Monogram cooling, freezer, ice maker, airflow, and control issues when service access is available."), ("Can you work on Monogram ranges, ovens, and dishwashers?", "Yes. We diagnose premium cooking and dishwasher complaints with a clear repair quote before work begins."), ("Are you authorized by GE or Monogram?", "We do not make unsupported manufacturer-authorization claims; we explain practical service options and limits clearly.")],
        "spanish_faq": [("¿Reparan refrigeradores empotrados Monogram?", "Sí. Diagnosticamos enfriamiento, congelador, hielo, flujo de aire y controles cuando hay acceso."), ("¿Atienden rangos, hornos y lavavajillas Monogram?", "Sí. Diagnosticamos fallas de cocción premium y lavavajillas con cotización clara antes de empezar."), ("¿Son autorizados por GE o Monogram?", "No hacemos reclamos no respaldados de autorización del fabricante; explicamos opciones y límites de servicio.")],
        "related": ["high-end-appliance-repair", "refrigerator-repair", "freezer-repair", "oven-repair", "stove-repair", "dishwasher-repair"],
    },
    {
        "brand": "Wolf",
        "title": "Wolf Appliance Repair",
        "slug": "wolf-appliance-repair",
        "spanish_title": "Reparación de Electrodomésticos Wolf",
        "seo_title": "Wolf Appliance Repair — Ranges, Ovens & Cooktops",
        "spanish_seo_title": "Reparación de Electrodomésticos Wolf | Inland Empire Appliance Repair",
        "search_description": "Wolf Appliance Repair for high-end appliance repair needs: ranges, ovens, cooktops, burners, and temperature diagnostics.",
        "spanish_search_description": "Reparación de Electrodomésticos Wolf para rangos, hornos, cubiertas, quemadores y diagnóstico de temperatura.",
        "intro": "Wolf appliance repair for ranges, ovens, cooktops, burners, ignition, and temperature diagnostics",
        "spanish_intro": "Reparación de electrodomésticos Wolf para rangos, hornos, cubiertas, quemadores, encendido y diagnóstico de temperatura",
        "short_description": "Wolf range, oven, cooktop, burner, ignition, and temperature diagnostics.",
        "spanish_short_description": "Diagnóstico Wolf para rangos, hornos, cubiertas, quemadores y temperatura.",
        "hero_usp": "Wolf cooking-appliance diagnostics with clear scope and warranty-backed repair.",
        "spanish_hero_usp": "Diagnóstico Wolf para cocción con alcance claro y reparación con garantía.",
        "sections": [("Wolf Appliance Repair for High-End Cooking", "Wolf appliances are centered on high-end cooking performance. Inland Empire Appliance Repair diagnoses Wolf ranges, ovens, cooktops, burners, ignition systems, fans, and controls without implying official Sub-Zero/Wolf service status."), ("Ranges, Ovens, Cooktops, and Temperature Diagnostics", "A Wolf oven that drifts from set temperature needs a different path than a range burner that will not ignite or a cooktop control fault. We test the failed system before recommending parts."), ("Premium Cooking Scope With Honest Limits", "If a Wolf unit needs a special-order part or a procedure outside normal field service, your technician explains that boundary instead of making unsupported partnership or factory-service claims.")],
        "spanish_sections": [("Servicio Wolf para cocción de alta gama", "Los equipos Wolf se enfocan en rendimiento de cocción premium. Inland Empire Appliance Repair diagnostica rangos, hornos, cubiertas, quemadores, encendido, ventiladores y controles sin implicar servicio oficial de Sub-Zero/Wolf."), ("Rangos, hornos, cubiertas y diagnóstico de temperatura", "Un horno Wolf que pierde temperatura requiere una ruta distinta a un quemador que no enciende o una falla de control en cubierta. Probamos el sistema afectado antes de recomendar piezas."), ("Alcance premium con límites honestos", "Si una unidad Wolf requiere una pieza especial o procedimiento fuera del servicio normal, lo explicamos sin hacer reclamos de alianza o servicio de fábrica.")],
        "problems": ["Wolf range burner not igniting", "Wolf oven temperature diagnostics request", "Wolf cooktop control fault", "Wolf convection fan or heating issue", "Wolf appliance special-order part question"],
        "spanish_problems": ["Quemador de rango Wolf que no enciende", "Solicitud de diagnóstico de temperatura en horno Wolf", "Falla de control en cubierta Wolf", "Problema de ventilador de convección o calentamiento Wolf", "Pregunta de pieza especial para equipo Wolf"],
        "benefits": [("Cooking-Appliance Focus", "Diagnostics cover ranges, ovens, cooktops, burners, fans, sensors, and controls."), ("Temperature Testing", "We verify heating and temperature behavior before quoting Wolf cooking-appliance repairs."), ("Clear Brand Boundaries", "Copy and service notes avoid unsupported Sub-Zero/Wolf authorization or partnership claims.")],
        "spanish_benefits": [("Enfoque en cocción", "Diagnosticamos rangos, hornos, cubiertas, quemadores, ventiladores, sensores y controles."), ("Pruebas de temperatura", "Verificamos calentamiento y temperatura antes de cotizar reparaciones Wolf."), ("Límites claros de marca", "El contenido evita reclamos no respaldados de autorización o alianza con Sub-Zero/Wolf.")],
        "faq": [("Do you repair Wolf ranges and ovens?", "Yes. We diagnose burner, ignition, oven heating, fan, sensor, and control issues on serviceable Wolf cooking appliances."), ("Can you help with Wolf cooktop temperature problems?", "Yes. We test controls, elements or burners, sensors, and installation conditions before quoting repair."), ("Are you affiliated with Sub-Zero/Wolf?", "We do not make unsupported affiliation claims; we provide practical diagnostics and explain any special-order or referral limits.")],
        "spanish_faq": [("¿Reparan rangos y hornos Wolf?", "Sí. Diagnosticamos quemadores, encendido, calentamiento, ventiladores, sensores y controles en equipos reparables."), ("¿Ayudan con problemas de temperatura en cubiertas Wolf?", "Sí. Probamos controles, elementos o quemadores, sensores e instalación antes de cotizar."), ("¿Están afiliados con Sub-Zero/Wolf?", "No hacemos reclamos de afiliación no respaldados; damos diagnóstico práctico y explicamos límites.")],
        "related": ["high-end-appliance-repair", "stove-repair", "oven-repair"],
    },
)

_HIGH_END_BRAND_PAGE_SPECS = (*_HIGH_END_BRAND_PAGE_SPECS, *_CARD17_BRAND_PAGE_SPECS)


def _brand_body(spec: dict[str, Any], *, spanish: bool) -> str:
    """Build rich text body HTML for an English or Spanish brand page."""
    sections = spec["spanish_sections" if spanish else "sections"]
    prefix = "/es" if spanish else ""
    link_text = (
        "Volver al hub de Reparación de Electrodomésticos de Alta Gama"
        if spanish
        else "Back to High End Appliance Repair"
    )
    closing = (
        "para comparar todas las marcas premium que atendemos.</p>"
        if spanish
        else "to compare all premium brands we service.</p>"
    )
    sections_html = "".join(
        f"<h2>{heading}</h2><p>{paragraph}</p>" for heading, paragraph in sections
    )
    return (
        sections_html
        + f'<p><a href="{prefix}/services/high-end-appliance-repair/">{link_text}</a> '
        + closing
    )


def _brand_page_data(spec: dict[str, Any], *, spanish: bool = False) -> dict[str, Any]:
    """Convert a brand spec into ServicePage seed data."""
    if spanish:
        return {
            "title": spec["spanish_title"],
            "slug": spec["slug"],
            "seo_title": spec["spanish_seo_title"],
            "search_description": spec["spanish_search_description"],
            "intro": spec["spanish_intro"],
            "short_description": spec["spanish_short_description"],
            "hero_usp": spec["spanish_hero_usp"],
            "body": _brand_body(spec, spanish=True),
            "problems": spec["spanish_problems"],
            "benefits": spec["spanish_benefits"],
            "faq": spec["spanish_faq"],
        }

    return {
        "title": spec["title"],
        "slug": spec["slug"],
        "seo_title": spec["seo_title"],
        "search_description": spec["search_description"],
        "intro": spec["intro"],
        "short_description": spec["short_description"],
        "hero_usp": spec["hero_usp"],
        "body": _brand_body(spec, spanish=False),
        "problems": spec["problems"],
        "benefits": spec["benefits"],
        "faq": spec["faq"],
        "related": spec["related"],
    }


HIGH_END_BRAND_SERVICE_PAGES: list[dict[str, Any]] = [
    _brand_page_data(spec) for spec in _HIGH_END_BRAND_PAGE_SPECS
]

SPANISH_HIGH_END_BRAND_SERVICE_PAGES: list[dict[str, Any]] = [
    _brand_page_data(spec, spanish=True) for spec in _HIGH_END_BRAND_PAGE_SPECS
]


def high_end_brand_grid(*, spanish: bool = False) -> str:
    """Return linked High End hub brand cards for the requested brands."""
    prefix = "/es" if spanish else ""
    details = {
        "bosch-appliance-repair": (
            "Lavavajillas, refrigeradores, hornos y diagnóstico de errores."
            if spanish
            else "Dishwashers, refrigerators, ovens, ranges, and error diagnostics."
        ),
        "kitchenaid-appliance-repair": (
            "Refrigeradores empotrados, lavavajillas, rangos y hornos."
            if spanish
            else "Built-in refrigerators, dishwashers, ranges, ovens, and kitchen suites."
        ),
        "sub-zero-appliance-repair": (
            "Refrigeración empotrada, vinos, hielo y sistema sellado."
            if spanish
            else "Built-in refrigeration, wine storage, ice makers, and sealed systems."
        ),
        "thermador-appliance-repair": (
            "Rangos profesionales, hornos de pared, lavavajillas y refrigeración."
            if spanish
            else "Pro-style ranges, wall ovens, dishwashers, and built-in refrigeration."
        ),
        "miele-appliance-repair": (
            "Lavavajillas, lavandería, hornos y diagnóstico premium."
            if spanish
            else "Dishwashers, laundry, ovens, cooktops, and premium diagnostics."
        ),
        "viking-appliance-repair": (
            "Rangos estilo profesional, hornos, cubiertas y refrigeración."
            if spanish
            else "Professional-style ranges, ovens, cooktops, and refrigeration."
        ),
        "speed-queen-appliance-repair": (
            "Lavadoras, secadoras y lavandería comercial cuando aplica."
            if spanish
            else "Washers, dryers, durable laundry systems, and laundromat overlap."
        ),
        "fisher-paykel-appliance-repair": (
            "DishDrawer, refrigeradores, rangos y electrodomésticos integrados."
            if spanish
            else "DishDrawer dishwashers, refrigerators, ranges, and integrated appliances."
        ),
        "monogram-appliance-repair": (
            "Refrigeración empotrada, cocción premium y lavavajillas."
            if spanish
            else "Built-in refrigeration, premium cooking, dishwashers, and kitchen diagnostics."
        ),
        "wolf-appliance-repair": (
            "Rangos, hornos, cubiertas y diagnóstico de temperatura."
            if spanish
            else "Ranges, ovens, cooktops, burners, and temperature diagnostics."
        ),
    }
    cards = []
    for page in HIGH_END_BRAND_SERVICE_PAGES:
        brand = page["title"].replace(" Appliance Repair", "")
        slug = page["slug"]
        cards.append(
            f'<article role="listitem" data-high-end-brand-card="{slug}" '
            'class="rounded-card border border-gray-200 bg-white">'
            f'<a href="{prefix}/services/{slug}/" '
            'class="block min-h-[44px] p-4 text-gray-700 hover:text-primary">'
            f"<h3>{brand}</h3><p>{details[slug]}</p></a></article>"
        )
    return '<div class="grid gap-3 sm:grid-cols-2" role="list">' + "".join(cards) + "</div>"
