"""
Populate Spanish service pages with full translated content.

Run with: python manage.py populate_spanish_content

Fills in body, problems_we_fix, why_choose_us, and faq fields that were
left empty during initial page creation. Idempotent — skips pages that
already have body content.
"""

from __future__ import annotations

import json
import logging
import uuid
from typing import Any

from django.core.management.base import BaseCommand
from wagtail.models import Locale

from services.models import ServicePage

logger = logging.getLogger(__name__)


def _uid() -> str:
    return str(uuid.uuid4())


def _problems(items: list[str]) -> str:
    return json.dumps([{"type": "problem", "value": v, "id": _uid()} for v in items])


def _benefits(items: list[dict[str, str]]) -> str:
    return json.dumps([{"type": "benefit", "value": v, "id": _uid()} for v in items])


def _faqs(items: list[dict[str, str]]) -> str:
    return json.dumps([{"type": "faq_item", "value": v, "id": _uid()} for v in items])


# ── Full Spanish content for each service ────────────────────────────

SERVICE_CONTENT: dict[str, dict[str, Any]] = {
    "refrigerator-repair": {
        "body": (
            "<h2>Reparación Experta de Refrigeradores de Confianza</h2>"
            "<p>Un refrigerador averiado significa comida echada a perder, dinero desperdiciado "
            "y una interrupción diaria. Nuestros técnicos certificados diagnostican y reparan "
            "problemas de refrigeradores en la primera visita — la mayoría de las reparaciones "
            "se completan el mismo día que llama. Reparamos todas las marcas principales "
            "incluyendo Samsung, LG, Whirlpool, GE, Maytag, KitchenAid, Sub-Zero y Frigidaire.</p>"
            "<h2>Problemas Comunes de Refrigeradores que Reparamos</h2>"
            "<p>Ya sea que su refrigerador no enfríe, tenga fugas de agua, haga ruidos extraños "
            "o funcione constantemente, lo hemos visto todo. Nuestros camiones están completamente "
            "equipados con piezas OEM para compresores, termostatos, ventiladores evaporadores, "
            "serpentines condensadores, calentadores de descongelamiento y placas de control — "
            "así podemos reparar la mayoría de los problemas en una sola visita sin pedir piezas.</p>"
            "<h2>Todos los Tipos de Refrigeradores</h2>"
            "<p>Reparamos refrigeradores de puerta francesa, side-by-side, congelador superior, "
            "congelador inferior, modelos empotrados y unidades comerciales. Cada tipo tiene "
            "problemas únicos y nuestros técnicos están capacitados en todos.</p>"
        ),
        "problems": [
            "Refrigerador no enfría o está caliente por dentro",
            "El congelador funciona pero el refrigerador está caliente",
            "La máquina de hielo no produce hielo",
            "Fuga de agua en el piso",
            "Ruidos extraños de zumbido o clic",
            "El refrigerador funciona constantemente",
            "Acumulación de escarcha dentro del refrigerador",
            "El dispensador de agua no funciona",
            "Fluctuaciones de temperatura",
            "La puerta del refrigerador no sella bien",
            "Los serpentines del condensador se congelan",
            "Panel de control no responde",
        ],
        "benefits": [
            {
                "title": "Reparación el Mismo Día",
                "description": "La mayoría de las reparaciones de refrigeradores se completan el mismo día que llama. Sin esperar piezas ni segundas visitas.",
            },
            {
                "title": "Todas las Marcas Principales",
                "description": "Capacitados de fábrica en Samsung, LG, Whirlpool, GE, Sub-Zero, Viking, KitchenAid y más.",
            },
            {
                "title": "Piezas OEM en Stock",
                "description": "Camiones completamente equipados con piezas genuinas del fabricante para compresores, termostatos y placas de control.",
            },
            {
                "title": "Garantía Incluida",
                "description": "Cada reparación de refrigerador respaldada por nuestra garantía integral de piezas y mano de obra.",
            },
        ],
        "faqs": [
            {
                "question": "¿Por qué mi refrigerador no enfría?",
                "answer": "Las causas más comunes son un serpentín condensador sucio, un motor de ventilador evaporador defectuoso, un termostato que no funciona correctamente o una fuga de refrigerante. Nuestro técnico diagnosticará el problema exacto y le proporcionará un presupuesto antes de comenzar cualquier trabajo.",
            },
            {
                "question": "¿Cuánto cuesta la reparación de un refrigerador?",
                "answer": "Los costos de reparación de refrigeradores varían según el problema. Nuestra tarifa de diagnóstico se exime con la aprobación de la reparación. Las reparaciones comunes como el reemplazo de termostato o motor de ventilador típicamente cuestan menos que comprar un refrigerador nuevo.",
            },
            {
                "question": "¿Vale la pena reparar un refrigerador viejo?",
                "answer": "Si su refrigerador tiene menos de 10-12 años y el costo de reparación es menos de la mitad del precio de uno nuevo, la reparación generalmente es mejor valor. Le daremos una recomendación honesta basada en el diagnóstico.",
            },
            {
                "question": "¿Cuánto tiempo toma la reparación de un refrigerador?",
                "answer": "La mayoría de las reparaciones de refrigeradores toman 1-2 horas. Llevamos piezas comunes en nuestros camiones, así que la mayoría de las reparaciones se completan en una sola visita. Los reemplazos complejos de compresor pueden tomar un poco más.",
            },
            {
                "question": "¿Reparan refrigeradores empotrados y Sub-Zero?",
                "answer": "Sí, reparamos todos los tipos de refrigeradores incluyendo empotrados, Sub-Zero, Viking y Thermador. Nuestros técnicos están capacitados de fábrica en marcas premium y llevan piezas especializadas.",
            },
            {
                "question": "Mi máquina de hielo dejó de funcionar. ¿Pueden repararla?",
                "answer": "Los problemas de máquinas de hielo son una de nuestras reparaciones más comunes. Ya sea que no produce hielo, hace cubos pequeños o huecos, o tiene fugas, diagnosticamos y reparamos la causa raíz — frecuentemente en menos de una hora.",
            },
        ],
    },
    "freezer-repair": {
        "body": (
            "<h2>Reparación Rápida y Confiable de Congeladores</h2>"
            "<p>Cuando su congelador deja de funcionar, cada hora cuenta. La comida descongelándose "
            "significa alimentos desperdiciados y riesgos potenciales para la salud. Nuestros técnicos "
            "certificados proporcionan reparación de congeladores el mismo día para todos los tipos — "
            "congeladores horizontales, verticales, de cajón y unidades comerciales. Llegamos con "
            "camiones completamente equipados para reparar la mayoría de los problemas en una sola visita.</p>"
            "<h2>¿Qué Causa los Problemas del Congelador?</h2>"
            "<p>Los problemas del congelador típicamente provienen de fallas del compresor, mal "
            "funcionamiento del termostato, fugas del sistema sellado, problemas del temporizador de "
            "descongelamiento o fallas del motor del ventilador evaporador. La acumulación de hielo "
            "a menudo indica un problema del sistema de descongelamiento, mientras que un congelador "
            "caliente generalmente apunta a un problema del compresor o refrigerante. Nuestros "
            "técnicos usan herramientas de diagnóstico profesionales para identificar la causa exacta.</p>"
        ),
        "problems": [
            "El congelador no congela o está muy caliente",
            "Acumulación excesiva de escarcha o hielo",
            "El congelador funciona pero no está suficientemente frío",
            "Agua acumulada en el fondo",
            "Sonidos inusuales de zumbido o clic",
            "El congelador funciona constantemente",
            "El sello de la puerta no cierra correctamente",
            "La temperatura del congelador fluctúa",
            "Escarcha en las paredes exteriores",
            "Comida descongelándose inesperadamente",
        ],
        "benefits": [
            {
                "title": "Servicio de Emergencia",
                "description": "Reparación de congeladores el mismo día para prevenir pérdida de alimentos. Entendemos la urgencia de un congelador averiado.",
            },
            {
                "title": "Todos los Tipos de Congeladores",
                "description": "Congeladores horizontales, verticales, de cajón, empotrados y unidades comerciales — los reparamos todos.",
            },
            {
                "title": "Precisión Diagnóstica",
                "description": "Herramientas profesionales para identificar problemas de compresor, termostato y sistema sellado en la primera visita.",
            },
            {
                "title": "Protección de Garantía",
                "description": "Todas las reparaciones de congeladores respaldadas por nuestra garantía de piezas y mano de obra para su tranquilidad.",
            },
        ],
        "faqs": [
            {
                "question": "¿Por qué mi congelador no congela?",
                "answer": "Las causas comunes incluyen un compresor defectuoso, bajo nivel de refrigerante, un termostato roto o un ventilador evaporador bloqueado. Nuestro técnico ejecutará diagnósticos y proporcionará un presupuesto transparente antes de comenzar cualquier reparación.",
            },
            {
                "question": "¿Qué causa la acumulación excesiva de escarcha?",
                "answer": "La acumulación de escarcha generalmente es causada por un temporizador de descongelamiento, calentador o termostato defectuoso. Un empaque de puerta dañado que deja entrar aire caliente también puede causar escarcha. Reparamos el sistema de descongelamiento para eliminar la acumulación de hielo.",
            },
            {
                "question": "¿Con qué frecuencia debe recibir mantenimiento un congelador?",
                "answer": "Los congeladores generalmente no necesitan mantenimiento regular, pero limpiar los serpentines del condensador cada 6-12 meses ayuda a la eficiencia. Si nota cambios de temperatura, ruidos inusuales o acumulación de escarcha, llame para un diagnóstico.",
            },
            {
                "question": "¿Pueden reparar un congelador comercial?",
                "answer": "Sí, reparamos congeladores y enfriadores comerciales. Nuestros técnicos llevan piezas para compresores comerciales, evaporadores y sistemas de control. Ofrecemos programación prioritaria para negocios.",
            },
            {
                "question": "¿Es más barato reparar o reemplazar un congelador?",
                "answer": "Si su congelador tiene menos de 10 años y el costo de reparación es menos del 50% del reemplazo, la reparación típicamente es mejor valor. Siempre proporcionamos una recomendación honesta después del diagnóstico.",
            },
        ],
    },
    "washer-repair": {
        "body": (
            "<h2>Reparación Profesional de Lavadoras</h2>"
            "<p>Una lavadora averiada interrumpe todo su hogar. Pilas de ropa sucia, viajes a la "
            "lavandería y el estrés de costos de reparación inesperados — lo entendemos. Nuestros "
            "técnicos certificados proporcionan reparación de lavadoras el mismo día para todas las "
            "marcas incluyendo Samsung, LG, Whirlpool, Maytag, GE, Kenmore, Bosch y Speed Queen.</p>"
            "<h2>Expertos en Carga Superior y Carga Frontal</h2>"
            "<p>Reparamos todos los tipos de lavadoras: modelos de carga superior con agitador, "
            "carga superior de alta eficiencia, lavadoras de carga frontal, unidades apilables y "
            "máquinas de lavandería comercial. Cada tipo tiene componentes únicos y patrones de "
            "falla — nuestros técnicos están capacitados en la mecánica específica de cada diseño.</p>"
            "<h2>Problemas Comunes de Lavadoras que Resolvemos</h2>"
            "<p>Desde una lavadora que no drena ni centrifuga hasta una que tiene fugas de agua por "
            "todos lados, lo hemos resuelto todo. Diagnosticamos rápidamente, llevamos piezas OEM y "
            "completamos la mayoría de las reparaciones en la misma visita.</p>"
        ),
        "problems": [
            "La lavadora no drena el agua",
            "La lavadora no centrifuga ni agita",
            "Fuga de agua de la lavadora en el piso",
            "Golpes fuertes o vibración durante el centrifugado",
            "Códigos de error en el panel de control",
            "La lavadora no enciende",
            "La ropa sigue mojada después del centrifugado",
            "La lavadora se llena de agua pero no lava",
            "Olor a quemado durante el funcionamiento",
            "La puerta o tapa no se bloquea",
            "La lavadora se desborda",
            "El dispensador de detergente no funciona",
        ],
        "benefits": [
            {
                "title": "Todos los Tipos de Lavadoras",
                "description": "Carga superior, carga frontal, apilables, alta eficiencia y comerciales — reparamos todo tipo de lavadora.",
            },
            {
                "title": "Servicio el Mismo Día",
                "description": "La mayoría de las reparaciones de lavadoras se completan el mismo día. No más viajes a la lavandería.",
            },
            {
                "title": "Piezas OEM",
                "description": "Piezas genuinas del fabricante para Samsung, LG, Whirlpool, Maytag, GE y todas las marcas principales.",
            },
            {
                "title": "Garantía Incluida",
                "description": "Cada reparación de lavadora respaldada por nuestra garantía integral de piezas y mano de obra.",
            },
        ],
        "faqs": [
            {
                "question": "¿Por qué mi lavadora no drena?",
                "answer": "Una lavadora que no drena generalmente es causada por una bomba de drenaje obstruida, manguera de drenaje bloqueada o interruptor de tapa defectuoso (carga superior) o pestillo de puerta (carga frontal). Nuestro técnico diagnosticará el problema y lo resolverá en la misma visita.",
            },
            {
                "question": "¿Por qué mi lavadora tiene fugas?",
                "answer": "Las fugas pueden provenir de un sello de puerta dañado (carga frontal), manguera de tina a bomba desgastada, conexiones sueltas o una tina agrietada. La ubicación de la fuga ayuda a identificar la causa — la identificaremos y repararemos en la misma visita.",
            },
            {
                "question": "¿Cuánto cuesta típicamente la reparación de una lavadora?",
                "answer": "Los costos de reparación de lavadoras dependen del problema y las piezas necesarias. Nuestra tarifa de diagnóstico se exime con la aprobación de la reparación. Las reparaciones comunes como bomba o correa son significativamente más baratas que comprar una máquina nueva.",
            },
            {
                "question": "Mi lavadora vibra violentamente durante el centrifugado. ¿Qué pasa?",
                "answer": "La vibración violenta generalmente es causada por amortiguadores desgastados (carga frontal) o varillas de suspensión (carga superior), una carga desbalanceada o rodamientos del tambor desgastados. Reemplazamos los componentes desgastados para restaurar un funcionamiento suave y silencioso.",
            },
            {
                "question": "¿Pueden reparar códigos de error en lavadoras Samsung/LG?",
                "answer": "Sí, estamos capacitados de fábrica en diagnóstico de códigos de error Samsung y LG. Códigos comunes como UE (desbalance), OE (error de drenaje) y DE (error de puerta) todos apuntan a componentes específicos que podemos reparar o reemplazar.",
            },
            {
                "question": "¿Vale la pena reparar una lavadora vieja?",
                "answer": "Si su lavadora tiene menos de 8-10 años y el costo de reparación es menos del 50% de una máquina nueva, la reparación generalmente es la opción inteligente. Le daremos una evaluación honesta después del diagnóstico.",
            },
        ],
    },
    "dryer-repair": {
        "body": (
            "<h2>Servicio Experto de Reparación de Secadoras</h2>"
            "<p>Cuando su secadora deja de calentar, tarda una eternidad en secar la ropa o no gira, "
            "necesita un servicio rápido y confiable. Nuestros técnicos certificados reparan secadoras "
            "de gas y eléctricas — todas las marcas, todos los modelos. La mayoría de las reparaciones "
            "se completan el mismo día con piezas de nuestros camiones completamente equipados.</p>"
            "<h2>Especialistas en Secadoras de Gas y Eléctricas</h2>"
            "<p>Las secadoras de gas y eléctricas tienen diferentes sistemas de calentamiento y "
            "requieren conocimiento especializado. Nuestros técnicos están capacitados en ambos tipos: "
            "ensambles de válvula de gas, sistemas de encendido y sensores de llama para secadoras de "
            "gas; elementos calefactores, fusibles térmicos y termostatos para modelos eléctricos. "
            "Manejamos todo de manera segura y eficiente.</p>"
            "<h2>No Ignore las Señales de Advertencia de la Secadora</h2>"
            "<p>Una secadora que necesita múltiples ciclos para secar, huele a quemado o hace ruidos "
            "inusuales está tratando de decirle algo. Estos problemas empeoran con el tiempo y pueden "
            "ser riesgos de incendio. Llame al primer síntoma para una reparación segura y económica.</p>"
        ),
        "problems": [
            "La secadora no calienta (gas o eléctrica)",
            "La secadora tarda demasiado en secar la ropa",
            "La secadora no enciende",
            "La secadora no gira o el tambor no rota",
            "Olor a quemado de la secadora",
            "La secadora se sobrecalienta",
            "La secadora hace ruidos de chirrido o rechinido",
            "La secadora se apaga a medio ciclo",
            "La ropa sigue húmeda después del ciclo completo",
            "El conducto de ventilación de la secadora obstruido",
            "El encendedor de la secadora de gas no brilla",
            "El temporizador o placa de control no funciona",
        ],
        "benefits": [
            {
                "title": "Gas y Eléctrica",
                "description": "Especializados en sistemas de válvula de gas y elementos calefactores eléctricos. Reparación segura y profesional.",
            },
            {
                "title": "Seguridad Contra Incendios",
                "description": "Inspeccionamos la acumulación de pelusa y conductos bloqueados — una causa principal de incendios de secadoras — durante cada servicio.",
            },
            {
                "title": "Rapidez",
                "description": "La mayoría de las reparaciones de secadoras se completan en 1-2 horas con piezas de nuestros camiones de servicio equipados.",
            },
            {
                "title": "Respaldado por Garantía",
                "description": "Todas las reparaciones de secadoras cubiertas por nuestra garantía tanto en piezas como en mano de obra.",
            },
        ],
        "faqs": [
            {
                "question": "¿Por qué mi secadora no calienta?",
                "answer": "Para secadoras eléctricas, las causas más comunes son un fusible térmico quemado, elemento calefactor defectuoso o termostato roto. Para secadoras de gas, generalmente es un encendedor defectuoso, solenoide de válvula de gas o sensor de llama. Diagnosticamos y reparamos ambos tipos.",
            },
            {
                "question": "¿Por qué mi secadora tarda tanto en secar?",
                "answer": "Los tiempos de secado largos típicamente son causados por un filtro de pelusa obstruido, conducto de ventilación bloqueado, sellos del tambor desgastados que dejan escapar el calor o un elemento calefactor defectuoso. Revisamos todos estos durante el diagnóstico y reparamos la causa raíz.",
            },
            {
                "question": "¿Un olor a quemado de mi secadora es peligroso?",
                "answer": "Sí — un olor a quemado puede indicar acumulación de pelusa cerca del elemento calefactor, una correa desgastada o un motor defectuoso. Apague la secadora inmediatamente y llame para servicio. Estos problemas pueden ser riesgos de incendio si no se atienden.",
            },
            {
                "question": "¿Cuánto cuesta la reparación de una secadora?",
                "answer": "Los costos de reparación de secadoras varían según el problema. Las reparaciones comunes como fusible térmico o elemento calefactor son muy accesibles. Nuestra tarifa de diagnóstico se exime cuando aprueba la reparación, y siempre recibirá un presupuesto antes de que comencemos.",
            },
            {
                "question": "¿Pueden reparar una secadora de gas que hace clic pero no enciende?",
                "answer": "Sí, esto típicamente es un encendedor defectuoso o solenoide de válvula de gas — ambas son piezas comunes que llevamos en nuestros camiones. Generalmente podemos reparar esto en menos de una hora.",
            },
            {
                "question": "¿Debo limpiar el conducto de ventilación de mi secadora?",
                "answer": "Sí, los conductos de ventilación de secadoras deben limpiarse anualmente. Los conductos obstruidos reducen la eficiencia, aumentan los costos de energía y son una causa principal de incendios domésticos. Podemos inspeccionar y asesorar durante cualquier servicio.",
            },
        ],
    },
    "dishwasher-repair": {
        "body": (
            "<h2>Servicio Confiable de Reparación de Lavavajillas</h2>"
            "<p>Un lavavajillas que no limpia, no drena o tiene fugas de agua es más que un "
            "inconveniente — puede dañar el piso y los gabinetes de su cocina. Nuestros técnicos "
            "certificados diagnostican y reparan todas las marcas y modelos de lavavajillas, "
            "típicamente el mismo día que llama.</p>"
            "<h2>Reparamos lo que Otros no Pueden</h2>"
            "<p>Desde reparaciones simples como un brazo rociador obstruido hasta problemas "
            "complejos como una placa de control defectuosa o reemplazo de motor de bomba, nuestros "
            "técnicos manejan todos los niveles de reparación de lavavajillas. Reparamos Bosch, "
            "Samsung, LG, Whirlpool, KitchenAid, GE, Maytag, Miele y todas las demás marcas principales.</p>"
            "<h2>Problemas Comunes de Lavavajillas</h2>"
            "<p>Platos que salen sucios, agua estancada en el fondo, la puerta que no cierra, "
            "códigos de error parpadeando o un lavavajillas que no arranca — estos son problemas que "
            "vemos y reparamos diariamente. Diagnosticamos rápidamente y llevamos las piezas necesarias.</p>"
        ),
        "problems": [
            "El lavavajillas no limpia los platos correctamente",
            "El lavavajillas no drena — agua estancada",
            "Fuga de agua del lavavajillas en el piso",
            "El lavavajillas no enciende",
            "El pestillo de la puerta no cierra o no bloquea",
            "El lavavajillas hace ruidos de rechinido o zumbido",
            "Los platos siguen mojados después del ciclo de secado",
            "Códigos de error en el panel de control",
            "El dispensador de detergente no abre",
            "El lavavajillas huele mal",
            "El agua no llena o llena lentamente",
            "Los brazos rociadores no giran",
        ],
        "benefits": [
            {
                "title": "Todas las Marcas",
                "description": "Capacitados de fábrica en Bosch, Samsung, LG, Whirlpool, KitchenAid, Miele y todas las marcas principales.",
            },
            {
                "title": "Diagnóstico Rápido",
                "description": "La mayoría de los problemas de lavavajillas se diagnostican en menos de 30 minutos con nuestras herramientas profesionales.",
            },
            {
                "title": "Piezas Disponibles",
                "description": "Bombas de drenaje, motores de lavado, válvulas de entrada y placas de control disponibles en nuestros camiones.",
            },
            {
                "title": "Trabajo Limpio",
                "description": "Protegemos el piso de su cocina y limpiamos completamente después de cada reparación.",
            },
        ],
        "faqs": [
            {
                "question": "¿Por qué mi lavavajillas no limpia bien?",
                "answer": "La limpieza deficiente generalmente es causada por brazos rociadores obstruidos, un motor de lavado defectuoso, baja temperatura del agua o un dispensador de detergente que no funciona correctamente. Revisamos todos los componentes y reparamos la causa raíz.",
            },
            {
                "question": "¿Por qué mi lavavajillas no drena?",
                "answer": "Un lavavajillas que no drena generalmente tiene una bomba de drenaje obstruida, manguera de drenaje bloqueada o válvula de retención defectuosa. Limpiamos obstrucciones y reemplazamos componentes fallidos para restaurar el drenaje adecuado.",
            },
            {
                "question": "¿Cuánto cuesta la reparación de un lavavajillas?",
                "answer": "Los costos de reparación de lavavajillas dependen del problema específico. Nuestra tarifa de diagnóstico se exime cuando aprueba la reparación. Las reparaciones comunes como bomba o válvula son mucho más baratas que comprar una unidad nueva.",
            },
            {
                "question": "Mi lavavajillas Bosch muestra un error E24. ¿Qué significa?",
                "answer": "El error E24 en lavavajillas Bosch indica un problema de drenaje. Típicamente es causado por una manguera de drenaje doblada, filtro obstruido o bomba de drenaje defectuosa. Diagnosticamos y reparamos códigos de error específicos de Bosch regularmente.",
            },
            {
                "question": "¿Vale la pena reparar un lavavajillas?",
                "answer": "Si su lavavajillas tiene menos de 7-10 años y el costo de reparación es menos de la mitad del precio de reemplazo, la reparación generalmente es mejor valor. Le daremos una recomendación honesta después del diagnóstico.",
            },
        ],
    },
    "oven-repair": {
        "body": (
            "<h2>Servicio Profesional de Reparación de Hornos</h2>"
            "<p>Cuando su horno no calienta correctamente, cocina desparejo o no enciende, la "
            "preparación de comidas se detiene por completo. Nuestros técnicos certificados reparan "
            "todos los tipos de hornos — gas, eléctricos, convección, dobles, de pared y rangos "
            "completos. La mayoría de las reparaciones se completan el mismo día con piezas de "
            "nuestros camiones de servicio.</p>"
            "<h2>Experiencia en Hornos de Gas y Eléctricos</h2>"
            "<p>Los hornos de gas y eléctricos requieren diferentes enfoques de diagnóstico. Para "
            "hornos de gas, solucionamos encendedores, válvulas de gas, válvulas de seguridad y "
            "termopares. Para hornos eléctricos, atendemos elementos calefactores (hornear y asar), "
            "sensores de temperatura, relés y placas de control. Nuestros técnicos están certificados "
            "en ambos tipos.</p>"
            "<h2>Reparación de Temperatura de Precisión</h2>"
            "<p>Un horno que funciona demasiado caliente, demasiado frío o fluctúa crea resultados "
            "de cocción inconsistentes. Calibramos sensores y termostatos para restaurar temperaturas "
            "precisas y consistentes para una cocción perfecta cada vez.</p>"
        ),
        "problems": [
            "El horno no calienta",
            "Temperatura del horno inexacta",
            "El encendedor del horno de gas no funciona",
            "Cocción despareja o puntos calientes",
            "El ciclo de autolimpieza no funciona",
            "La puerta del horno no cierra correctamente",
            "El elemento de asar no calienta",
            "El horno tarda demasiado en precalentar",
            "El panel de control o pantalla no funciona",
            "Olor a gas cuando el horno está encendido",
            "La luz del horno no enciende",
            "El ventilador de convección no funciona",
        ],
        "benefits": [
            {
                "title": "Gas y Eléctrico",
                "description": "Certificados en sistemas de ignición de gas y elementos calefactores eléctricos para reparaciones precisas y seguras.",
            },
            {
                "title": "Calibración de Temperatura",
                "description": "Calibramos sensores y termostatos para asegurar temperaturas de horno precisas y consistentes.",
            },
            {
                "title": "Marcas Premium",
                "description": "Capacitados en Viking, Wolf, Thermador, Sub-Zero y otras marcas premium de hornos.",
            },
            {
                "title": "Seguridad Primero",
                "description": "Las reparaciones de hornos de gas incluyen pruebas de seguridad contra fugas para proteger su hogar y familia.",
            },
        ],
        "faqs": [
            {
                "question": "¿Por qué mi horno de gas no enciende?",
                "answer": "La causa más común es un encendedor defectuoso — brilla pero no se calienta lo suficiente para abrir la válvula de gas. Otras causas incluyen una válvula de gas fallida, válvula de seguridad defectuosa o problema de cableado. Llevamos repuestos de encendedores en cada camión.",
            },
            {
                "question": "¿Por qué mi horno no alcanza la temperatura correcta?",
                "answer": "Las temperaturas inexactas generalmente apuntan a un sensor de temperatura defectuoso, elemento calefactor desgastado o un termostato que necesita calibración. Probamos y reemplazamos el componente específico para restaurar la precisión.",
            },
            {
                "question": "¿Es seguro usar un horno que huele a gas?",
                "answer": "No — si huele gas con el horno apagado, cierre el suministro de gas, ventile el área y llame para servicio inmediatamente. Si huele gas solo brevemente cuando el horno enciende por primera vez, eso generalmente es normal, pero hágalo revisar si le preocupa.",
            },
            {
                "question": "¿Pueden reparar un horno doble de pared?",
                "answer": "Sí, reparamos todas las configuraciones de hornos de pared incluyendo simples, dobles y combinaciones de horno/microondas. Reparamos hornos empotrados de todas las marcas principales.",
            },
            {
                "question": "¿Cuánto cuesta la reparación de un horno?",
                "answer": "Los costos de reparación de hornos dependen del problema. El reemplazo de encendedor es una de las reparaciones más accesibles. Nuestra tarifa de diagnóstico se exime con la aprobación de la reparación, y siempre recibirá un presupuesto antes de que comencemos.",
            },
        ],
    },
    "stove-repair": {
        "body": (
            "<h2>Reparación Experta de Estufas y Cooktops</h2>"
            "<p>Ya sea un quemador de gas que no enciende, un elemento eléctrico que no calienta o "
            "un cooktop de inducción mostrando códigos de error, nuestros técnicos lo reparan rápido. "
            "Reparamos todos los tipos de estufas y cooktops incluyendo rangos independientes, rangos "
            "deslizantes, cooktops de gas, cooktops eléctricos y unidades de inducción.</p>"
            "<h2>Especialistas en Estufas de Gas</h2>"
            "<p>Los problemas de estufas de gas frecuentemente involucran fallas de encendedor, "
            "puertos de quemador obstruidos, válvulas de gas defectuosas o problemas de termopar. "
            "Nuestros técnicos diagnostican de forma segura los problemas de flujo de gas, reemplazan "
            "encendedores y válvulas, limpian ensambles de quemadores y prueban fugas de gas después "
            "de cada reparación.</p>"
            "<h2>Cooktops Eléctricos y de Inducción</h2>"
            "<p>Las estufas eléctricas pueden tener elementos de bobina defectuosos, superficies "
            "cerámicas agrietadas, interruptores infinitos defectuosos o problemas de placa de control. "
            "Los cooktops de inducción requieren diagnóstico especializado para fallas de placa de "
            "potencia, errores de sensor y problemas de bobina. Manejamos todos los tipos.</p>"
        ),
        "problems": [
            "El quemador de gas no enciende",
            "El elemento eléctrico no calienta",
            "La llama del quemador es despareja o muy baja",
            "Sonido de clic pero no enciende",
            "Olor a gas cerca de la estufa",
            "Códigos de error del cooktop de inducción",
            "Superficie de cooktop cerámico agrietada",
            "El control de temperatura no funciona",
            "Perillas de quemadores rotas o sueltas",
            "La estufa produce chispas continuamente",
        ],
        "benefits": [
            {
                "title": "Todos los Tipos de Combustible",
                "description": "Gas, eléctrica, inducción y dual — reparamos todo tipo de estufa y cooktop.",
            },
            {
                "title": "Seguridad de Gas",
                "description": "Reparaciones de gas certificadas con pruebas de fugas después de cada servicio para la seguridad de su familia.",
            },
            {
                "title": "Cuidado de Superficies",
                "description": "Herramientas y técnicas especializadas para reparaciones de cooktops cerámicos y de vidrio sin daños.",
            },
            {
                "title": "Todas las Marcas",
                "description": "Desde rangos estándar GE/Whirlpool hasta cooktops premium Viking/Wolf — los reparamos todos.",
            },
        ],
        "faqs": [
            {
                "question": "¿Por qué mi quemador de gas no enciende?",
                "answer": "Las causas comunes incluyen un puerto de quemador obstruido (residuos de comida), un interruptor de encendido defectuoso, una tapa de quemador desalineada o un problema de suministro de gas. Limpiamos, ajustamos o reemplazamos componentes según sea necesario.",
            },
            {
                "question": "¿Por qué mi estufa hace clic pero no enciende?",
                "answer": "El clic continuo generalmente significa que el módulo de chispa del encendedor recibe energía pero el gas no llega al quemador. Esto puede ser un puerto obstruido, válvula de gas defectuosa o interruptor de encendido atascado. Diagnosticamos y reparamos en la misma visita.",
            },
            {
                "question": "¿Pueden reparar un cooktop de vidrio agrietado?",
                "answer": "Las superficies de cooktop de vidrio o cerámica agrietadas necesitan reemplazo en lugar de reparación. Podemos conseguir e instalar tapas de reemplazo para la mayoría de las marcas, o asesorar si el reemplazo completo es más económico.",
            },
            {
                "question": "¿Cuánto cuesta la reparación de una estufa?",
                "answer": "Los costos de reparación de estufas varían según el problema. Los reemplazos de encendedor e interruptores son reparaciones accesibles. Nuestra tarifa de diagnóstico se exime con la reparación, y siempre cotizamos antes de comenzar el trabajo.",
            },
            {
                "question": "¿Reparan cooktops de inducción?",
                "answer": "Sí, reparamos cooktops de inducción de Bosch, Samsung, GE y otras marcas. Los problemas comunes incluyen fallas de placa de potencia, errores de sensor y problemas de bobina.",
            },
        ],
    },
    "water-heater-repair": {
        "body": (
            "<h2>Reparación Rápida de Calentadores de Agua</h2>"
            "<p>¿Sin agua caliente? ¿Duchas tibias? ¿Un tanque con fugas? Proporcionamos reparación "
            "de calentadores de agua el mismo día para todos los tipos — calentadores de tanque "
            "convencionales (gas y eléctricos), calentadores de agua sin tanque y unidades híbridas "
            "con bomba de calor. Nuestros técnicos llegan con las piezas y herramientas para restaurar "
            "su agua caliente rápidamente.</p>"
            "<h2>Calentadores de Agua de Gas y Eléctricos</h2>"
            "<p>Los problemas de calentadores de agua de gas frecuentemente involucran fallas de la "
            "llama piloto, problemas de termopar, mal funcionamiento de válvulas de gas y acumulación "
            "de sedimento. Los modelos eléctricos comúnmente tienen elementos calefactores fallidos, "
            "botones de reinicio disparados, termostatos defectuosos o ánodos de varilla corroídos. "
            "Estamos certificados para reparar ambos tipos de forma segura.</p>"
            "<h2>Servicio de Calentadores sin Tanque</h2>"
            "<p>Los calentadores de agua sin tanque requieren conocimiento especializado. Reparamos "
            "todas las marcas principales incluyendo Rinnai, Navien, Noritz y Rheem. Problemas comunes "
            "incluyen fallas de ignición, acumulación de sarro y errores de sensor de flujo.</p>"
        ),
        "problems": [
            "Sin agua caliente en absoluto",
            "El agua no se calienta lo suficiente",
            "Fuga del calentador de agua por la parte inferior",
            "La llama piloto se apaga constantemente",
            "Ruidos extraños de estallidos o retumbar",
            "Agua caliente oxidada o descolorida",
            "El calentador de agua tarda demasiado en calentar",
            "Códigos de error del calentador sin tanque",
            "El agua caliente se acaba rápidamente",
            "Fuga de la válvula de alivio de temperatura y presión",
            "El calentador de agua dispara el interruptor",
        ],
        "benefits": [
            {
                "title": "Todos los Tipos",
                "description": "Calentadores de agua de tanque, sin tanque, gas, eléctricos e híbridos con bomba de calor — los reparamos todos.",
            },
            {
                "title": "Certificados en Seguridad",
                "description": "Trabajo en líneas de gas, pruebas de válvulas de presión y conexiones eléctricas manejadas por técnicos certificados.",
            },
            {
                "title": "Expertos en Sin Tanque",
                "description": "Servicio especializado para Rinnai, Navien, Noritz y otras marcas sin tanque.",
            },
            {
                "title": "Consejo Honesto",
                "description": "Le diremos cuándo la reparación tiene sentido y cuándo el reemplazo es mejor inversión.",
            },
        ],
        "faqs": [
            {
                "question": "¿Por qué no tengo agua caliente?",
                "answer": "Para calentadores de gas, verifique si la llama piloto está encendida. Las causas comunes incluyen un termopar defectuoso, problema de válvula de gas o interruptor de seguridad disparado. Para unidades eléctricas, generalmente es un elemento calefactor fallido o interruptor disparado.",
            },
            {
                "question": "¿Por qué mi calentador de agua tiene fugas?",
                "answer": "Las fugas de accesorios o válvulas generalmente se pueden reparar. Las fugas de la parte inferior del tanque indican corrosión interna y típicamente requieren reemplazo. Diagnosticaremos la fuente y le aconsejaremos el mejor curso de acción.",
            },
            {
                "question": "¿Cuánto debe durar un calentador de agua?",
                "answer": "Los calentadores de agua de tanque típicamente duran 8-12 años. Las unidades sin tanque duran 15-20 años con mantenimiento regular. El drenaje anual para eliminar sedimento puede extender la vida de cualquier calentador de agua significativamente.",
            },
            {
                "question": "Mi calentador sin tanque muestra un código de error. ¿Qué debo hacer?",
                "answer": "Los códigos de error varían según la marca. Los códigos comunes se relacionan con falla de ignición, problemas de sensor de flujo o sobrecalentamiento. No intente reiniciar repetidamente — llame para diagnóstico profesional para evitar daños mayores.",
            },
            {
                "question": "¿Cuánto cuesta la reparación de un calentador de agua?",
                "answer": "Los costos de reparación de calentadores de agua dependen del tipo y el problema. Los reemplazos de termopar y elementos son accesibles. Nuestra tarifa de diagnóstico se exime cuando aprueba la reparación.",
            },
        ],
    },
    "air-conditioning-repair-hvac": {
        "body": (
            "<h2>Reparación Experta de Aire Acondicionado</h2>"
            "<p>Cuando su aire acondicionado deja de enfriar en medio de una ola de calor, necesita "
            "un servicio rápido y confiable. Nuestros técnicos HVAC certificados proporcionan "
            "reparación de aire acondicionado el mismo día para sistemas residenciales y comerciales. "
            "Reparamos aires acondicionados centrales, mini-splits sin ductos, unidades de ventana y "
            "bombas de calor de todas las marcas principales.</p>"
            "<h2>Sistemas de Aire Central y Mini-Split</h2>"
            "<p>Los problemas de aire acondicionado central frecuentemente provienen de fugas de "
            "refrigerante, fallas del compresor, serpentines evaporadores sucios, capacitores defectuosos "
            "o problemas del termostato. Los sistemas mini-split pueden desarrollar fallas de placa "
            "inversora, problemas de refrigerante o problemas de drenaje. Estamos capacitados en ambos "
            "tipos de sistemas y llevamos las piezas para reparar la mayoría de los problemas en una visita.</p>"
            "<h2>La Eficiencia Energética Importa</h2>"
            "<p>Un sistema de aire acondicionado que no funciona eficientemente desperdicia energía y "
            "dinero. Restauramos la eficiencia máxima de su sistema mientras reparamos el problema "
            "inmediato, ahorrándole en facturas de energía a largo plazo.</p>"
        ),
        "problems": [
            "El AC no enfría o sopla aire caliente",
            "El AC no enciende",
            "Enfriamiento desparejo en diferentes habitaciones",
            "El AC hace ruidos fuertes o inusuales",
            "La unidad de AC tiene fuga de agua adentro",
            "El termostato no responde",
            "El AC se enciende y apaga rápidamente (ciclo corto)",
            "Serpentines evaporadores congelados",
            "Facturas de energía altas por el AC",
            "Mal olor de las ventilaciones del AC",
            "El compresor del AC no se activa",
            "El mini-split no calienta ni enfría",
        ],
        "benefits": [
            {
                "title": "Todos los Tipos de Sistemas",
                "description": "Aire central, mini-splits, unidades de ventana y bombas de calor — residencial y comercial.",
            },
            {
                "title": "Técnicos HVAC Certificados",
                "description": "Técnicos certificados por la EPA capacitados en manejo de refrigerante y diagnóstico HVAC.",
            },
            {
                "title": "Enfoque en Eficiencia",
                "description": "Restauramos la eficiencia máxima para reducir sus facturas de energía junto con reparar el problema inmediato.",
            },
            {
                "title": "Servicio de Emergencia",
                "description": "Reparación de AC el mismo día porque sabemos que la comodidad no puede esperar en calor extremo.",
            },
        ],
        "faqs": [
            {
                "question": "¿Por qué mi AC sopla aire caliente?",
                "answer": "Las causas comunes incluyen bajo refrigerante por una fuga, un filtro de aire sucio que restringe el flujo, un compresor defectuoso o un capacitor malo. Diagnosticamos la causa raíz y la reparamos — no solo el síntoma.",
            },
            {
                "question": "¿Con qué frecuencia debo dar mantenimiento a mi AC?",
                "answer": "El mantenimiento profesional del AC debe hacerse anualmente, idealmente en primavera antes de la temporada de enfriamiento. El mantenimiento regular previene averías, mejora la eficiencia y extiende la vida de su sistema.",
            },
            {
                "question": "¿Por qué mi AC tiene fugas de agua adentro?",
                "answer": "Las fugas interiores del AC generalmente son causadas por una línea de drenaje de condensado obstruida, un serpentín evaporador sucio o una bandeja de drenaje agrietada. Limpiamos obstrucciones y reparamos o reemplazamos componentes dañados.",
            },
            {
                "question": "¿Cuánto cuesta la reparación del AC?",
                "answer": "Los costos de reparación del AC varían ampliamente según el problema. El reemplazo de capacitor es accesible; el reemplazo de compresor es más complejo. Nuestra tarifa de diagnóstico se exime con la aprobación de la reparación, y siempre cotizamos antes de comenzar el trabajo.",
            },
            {
                "question": "¿Debo reparar o reemplazar mi unidad de AC?",
                "answer": "Si su AC tiene más de 15 años, usa refrigerante R-22 (que se está retirando), o necesita reemplazo de compresor, una unidad nueva puede ser más económica a largo plazo. Le daremos una recomendación honesta.",
            },
            {
                "question": "¿Reparan sistemas mini-split sin ductos?",
                "answer": "Sí, reparamos todas las marcas de mini-split sin ductos incluyendo Mitsubishi, Daikin, Fujitsu, LG y Samsung. Manejamos reparaciones de placa inversora, recarga de refrigerante y problemas de drenaje.",
            },
        ],
    },
    "microwave-repair": {
        "body": (
            "<h2>Reparación Profesional de Microondas</h2>"
            "<p>Mientras que los microondas de mostrador frecuentemente se reemplazan, las unidades "
            "empotradas, sobre-rango y de cajón son costosas de reemplazar y bien vale la pena "
            "repararlas. Nuestros técnicos reparan todos los tipos de microondas de todas las marcas "
            "principales — Samsung, LG, Whirlpool, GE, KitchenAid, Bosch y más.</p>"
            "<h2>Problemas Comunes de Microondas</h2>"
            "<p>Los microondas que no calientan, producen chispas, tienen un panel de control muerto "
            "o hacen ruidos inusuales típicamente tienen problemas con el magnetrón, diodo, interruptor "
            "de puerta, capacitor o placa de control. Todos estos son componentes que diagnosticamos "
            "y reemplazamos durante nuestras visitas de servicio.</p>"
            "<h2>Enfoque de Seguridad Primero</h2>"
            "<p>Los microondas contienen capacitores de alto voltaje que almacenan carga eléctrica "
            "peligrosa incluso desenchufados. Nunca intente reparar un microondas usted mismo. "
            "Nuestros técnicos están capacitados en procedimientos seguros de descarga y reparación "
            "de alto voltaje.</p>"
        ),
        "problems": [
            "El microondas no calienta la comida",
            "Chispas dentro del microondas",
            "El plato giratorio no gira",
            "El microondas no enciende",
            "La puerta no cierra o no traba correctamente",
            "Los botones del panel de control no responden",
            "El microondas funciona pero no calienta",
            "Sonidos inusuales de zumbido",
            "La luz interior no funciona",
            "El microondas se apaga a medio ciclo",
        ],
        "benefits": [
            {
                "title": "Todos los Tipos",
                "description": "Reparación de microondas empotrados, sobre-rango, de mostrador, de cajón y comerciales.",
            },
            {
                "title": "Seguridad de Alto Voltaje",
                "description": "Técnicos certificados capacitados en descarga segura de capacitores y reparación de alto voltaje.",
            },
            {
                "title": "Ahorro de Costos",
                "description": "Reparar microondas empotrados y sobre-rango cuesta una fracción del reemplazo — mantenemos su cocina intacta.",
            },
            {
                "title": "Todas las Marcas",
                "description": "Samsung, LG, GE, Whirlpool, KitchenAid, Bosch y todas las demás marcas principales de microondas.",
            },
        ],
        "faqs": [
            {
                "question": "¿Por qué mi microondas no calienta?",
                "answer": "La causa más común es un magnetrón fallido — el componente que genera la energía de microondas. Otras causas incluyen un diodo defectuoso, capacitor quemado o interruptor de puerta defectuoso. Diagnosticamos y reemplazamos el componente específico.",
            },
            {
                "question": "¿Vale la pena reparar un microondas?",
                "answer": "Para microondas de mostrador de menos de $200, el reemplazo frecuentemente tiene más sentido. Para unidades empotradas, sobre-rango o de cajón (que cuestan $500-$2000+), la reparación es casi siempre mejor valor.",
            },
            {
                "question": "¿Por qué mi microondas produce chispas?",
                "answer": "Las chispas pueden ser causadas por metal o aluminio adentro, una cubierta de guía de ondas dañada, un soporte de rejilla desgastado o pintura descascarándose dentro de la cavidad. Algunas causas son reparaciones simples; otras pueden necesitar reemplazo de componentes.",
            },
            {
                "question": "¿Cuánto cuesta la reparación de un microondas?",
                "answer": "Los costos de reparación de microondas dependen del problema y tipo. Las reparaciones de interruptor de puerta y plato giratorio son accesibles. El reemplazo de magnetrón cuesta más pero sigue siendo más barato que reemplazar una unidad empotrada. Siempre cotizamos antes de comenzar.",
            },
            {
                "question": "¿Pueden reparar un microondas sobre-rango en su lugar?",
                "answer": "Sí, en la mayoría de los casos reparamos microondas sobre-rango sin removerlos del soporte de pared. Solo para reparaciones internas mayores podría ser necesaria la remoción — y también nos encargamos de eso.",
            },
        ],
    },
}


class Command(BaseCommand):
    help = (
        "Populate Spanish service pages with full translated content (body, FAQ, etc.)"
    )

    def handle(self, *args: Any, **options: Any) -> None:
        try:
            es_locale = Locale.objects.get(language_code="es")
        except Locale.DoesNotExist:
            self.stderr.write(
                self.style.ERROR(
                    "Spanish locale not found. Run setup_spanish_pages first."
                )
            )
            return

        updated = 0
        skipped = 0

        for slug, content in SERVICE_CONTENT.items():
            page = ServicePage.objects.filter(locale=es_locale, slug=slug).first()
            if not page:
                self.stderr.write(
                    self.style.WARNING(f"  MISS  No Spanish page for slug={slug}")
                )
                continue

            # Skip if already populated
            if page.body and len(page.body) > 50:
                self.stdout.write(f"  SKIP  {page.title} (already has body content)")
                skipped += 1
                continue

            page.body = content["body"]
            page.problems_we_fix = _problems(content["problems"])
            page.why_choose_us = _benefits(content["benefits"])
            page.faq = _faqs(content["faqs"])

            page.save()
            page.save_revision().publish()
            updated += 1
            self.stdout.write(self.style.SUCCESS(f"  +     {page.title}"))

        self.stdout.write(
            self.style.SUCCESS(f"\nDone! Updated {updated}, skipped {skipped}.")
        )
