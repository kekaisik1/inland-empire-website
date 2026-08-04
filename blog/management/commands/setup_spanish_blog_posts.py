"""
Create Spanish translations of all English blog posts.

Run with: python manage.py setup_spanish_blog_posts

Idempotent — skips blog posts that already have Spanish translations.
Must run AFTER populate_blog_posts so English posts exist.
"""

from __future__ import annotations

import logging
from typing import Any

from django.core.management.base import BaseCommand
from wagtail.models import Locale

from blog.content_utils import normalized_stream_json, stream_body
from blog.models import BlogPage

logger = logging.getLogger(__name__)

H = "heading"
P = "paragraph"


def _body(blocks: list[tuple[str, str]]) -> str:
    """Convert (type, value) tuples to StreamField JSON."""

    return stream_body(blocks)


# ── Spanish translations for each blog post (keyed by English slug) ──

BLOG_TRANSLATIONS: dict[str, dict[str, Any]] = {
    # ── Post 1 ──
    "refrigerator-not-cooling-causes-fixes": {
        "title": "¿Por Qué Mi Refrigerador No Enfría? 7 Causas y Soluciones",
        "seo_title": "¿Refrigerador No Enfría? 7 Causas y Soluciones",
        "search_description": (
            "¿Su refrigerador no enfría? Descubra las 7 causas más comunes "
            "y cuándo llamar a un profesional. Reparación el mismo día en el Inland Empire."
        ),
        "intro": (
            "Si su refrigerador dejó de enfriar, no se alarme. Aquí están las "
            "7 causas más comunes y qué puede hacer con cada una."
        ),
        "body": [
            (H, "Por Qué Su Refrigerador Dejó de Enfriar"),
            (
                P,
                "<p>Un refrigerador que no enfría es uno de los problemas más comunes — y más urgentes — que enfrentan los propietarios. Cuando su refrigerador deja de mantener la comida fría, tiene un tiempo limitado antes de que los alimentos se echen a perder. La buena noticia es que muchos problemas de enfriamiento tienen causas directas que un técnico profesional puede diagnosticar y reparar el mismo día.</p><p>Aquí están las siete razones más comunes por las que su refrigerador no enfría correctamente, qué puede revisar usted mismo y cuándo es momento de llamar a un profesional.</p>",
            ),
            (H, "1. Serpentines del Condensador Sucios"),
            (
                P,
                "<p>Los serpentines del condensador — generalmente ubicados detrás o debajo de su refrigerador — liberan calor del refrigerante. Cuando están cubiertos de polvo, pelo de mascotas o grasa, su refrigerador no puede disipar el calor eficientemente y el compresor trabaja en exceso sin enfriar correctamente.</p><p><strong>Qué revisar:</strong> Aleje el refrigerador de la pared e inspeccione los serpentines. Si están visiblemente sucios, aspírelos con un accesorio de cepillo. Limpie los serpentines cada 6-12 meses para prevenir este problema.</p>",
            ),
            (H, "2. Motor del Ventilador Evaporador Defectuoso"),
            (
                P,
                "<p>El ventilador evaporador circula aire frío del congelador al compartimento del refrigerador. Si este motor falla, el congelador puede mantenerse frío mientras la sección del refrigerador se calienta — un síntoma clásico que apunta directamente a esta pieza.</p><p><strong>Qué revisar:</strong> Abra el congelador y escuche el ventilador. Si está en silencio o hace ruidos de trituración, el motor probablemente necesita reemplazo.</p>",
            ),
            (H, "3. Falla del Sistema de Descongelamiento"),
            (
                P,
                "<p>Los refrigeradores modernos sin escarcha usan un calentador de descongelamiento, temporizador (o tarjeta de control) y termostato de descongelamiento para prevenir la acumulación de hielo. Cuando alguno de estos componentes falla, el hielo se acumula en los serpentines y bloquea el flujo de aire.</p><p><strong>Señales de falla:</strong> Escarcha o hielo visible dentro del congelador, un refrigerador que alterna entre enfriar y calentar, o agua acumulada debajo de los cajones.</p>",
            ),
            (H, "4. Motor del Ventilador del Condensador Roto"),
            (
                P,
                "<p>El ventilador del condensador (cerca del compresor en la parte inferior/trasera) jala aire a través de los serpentines y el compresor para enfriarlos. Si este ventilador falla, el compresor se sobrecalienta y el refrigerante no puede enfriar correctamente.</p><p><strong>Qué revisar:</strong> Escuche si el ventilador del condensador funciona cuando el compresor se enciende. Si no lo escucha, necesita atención profesional.</p>",
            ),
            (H, "5. Problemas de Termostato o Control de Temperatura"),
            (
                P,
                "<p>El termostato de control de temperatura dirige voltaje al compresor, ventilador evaporador y ventilador del condensador. Si no funciona correctamente, puede no señalar a estos componentes que funcionen, dejando su refrigerador caliente.</p><p><strong>Prueba rápida:</strong> Intente ajustar el termostato del ajuste más bajo al más alto. Debería escuchar un clic. Si no hay clic en ningún ajuste, el termostato puede estar defectuoso.</p>",
            ),
            (H, "6. Fuga de Refrigerante"),
            (
                P,
                "<p>El refrigerante es el químico que absorbe calor de dentro de su refrigerador y lo libera afuera. Una fuga en el sistema sellado significa que su refrigerador pierde gradualmente su capacidad de enfriar. Esto requiere reparación profesional — el manejo de refrigerante está regulado y requiere certificación EPA.</p><p><strong>Señales de fuga:</strong> Residuo aceitoso cerca del compresor, sonido de silbido o burbujeo, o un refrigerador que enfría menos con el paso de los días.</p>",
            ),
            (H, "7. Falla del Compresor"),
            (
                P,
                "<p>El compresor es el corazón del sistema de enfriamiento de su refrigerador. Cuando falla, no hay refrigeración en absoluto. Los problemas del compresor se presentan como el refrigerador funcionando pero sin enfriar, el compresor encendiéndose y apagándose repetidamente, o silencio completo.</p><p>El reemplazo del compresor es una reparación significativa, pero para refrigeradores de gama alta (Sub-Zero, Viking, etc.), frecuentemente es más económico que reemplazar la unidad completa.</p>",
            ),
            (H, "Cuándo Llamar a un Profesional"),
            (
                P,
                "<p>Si ha revisado los serpentines del condensador y el termostato sin éxito, es momento de llamar a un técnico de reparación de electrodomésticos. Problemas como fallas del motor del ventilador evaporador, fallas del sistema de descongelamiento, fugas de refrigerante y problemas del compresor requieren herramientas profesionales y experiencia.</p>",
            ),
            (H, "Preguntas Frecuentes"),
            (
                P,
                "<p><strong>¿Cuánto cuesta reparar un refrigerador que no enfría?</strong> Los costos varían según la causa. Las reparaciones simples como limpieza de serpentines son mínimas. Los reemplazos de motor de ventilador y termostato cuestan moderadamente. Los reemplazos de compresor son los más costosos pero aún más económicos que un refrigerador nuevo.</p><p><strong>¿Vale la pena reparar un refrigerador viejo?</strong> Si tiene menos de 10-12 años y el costo de reparación es menos de la mitad del precio de uno nuevo, la reparación generalmente ofrece mejor valor.</p>",
            ),
        ],
    },
    # ── Post 2 ──
    "dryer-not-heating-what-to-check": {
        "title": "Secadora No Calienta: Qué Revisar Antes de Llamar al Técnico",
        "seo_title": "¿Secadora No Calienta? Qué Revisar y Cuándo Llamar",
        "search_description": (
            "¿Su secadora no calienta? Aprenda las causas más comunes y qué puede "
            "revisar usted mismo. Reparación el mismo día en el Inland Empire."
        ),
        "intro": (
            "Una secadora que funciona pero no calienta es frustrante. Estas son las "
            "causas más comunes y qué puede revisar antes de llamar a un técnico."
        ),
        "body": [
            (H, "¿Por Qué Su Secadora No Calienta?"),
            (
                P,
                "<p>Una secadora que gira pero no calienta es uno de los problemas más comunes que vemos. Su ropa sale húmeda después de un ciclo completo, los tiempos de secado se duplican o triplican. Las causas varían según si su secadora es de gas o eléctrica, pero muchas son reparables el mismo día.</p>",
            ),
            (H, "Revise el Conducto de Ventilación"),
            (
                P,
                "<p>La causa número uno de problemas de calentamiento en secadoras es un conducto de ventilación obstruido. La pelusa se acumula con el tiempo y restringe el flujo de aire, causando que la secadora se sobrecaliente y active el fusible térmico de seguridad. Desconecte la secadora, retire la manguera de ventilación y revise si hay bloqueos.</p>",
            ),
            (H, "Fusible Térmico Quemado"),
            (
                P,
                "<p>El fusible térmico es un dispositivo de seguridad que corta el calor cuando la secadora se sobrecalienta. Una vez que se quema, la secadora no calentará hasta que se reemplace. Es la reparación más común que realizamos en secadoras — rápida y económica.</p>",
            ),
            (H, "Elemento Calefactor o Encendedor"),
            (
                P,
                "<p>En secadoras eléctricas, el elemento calefactor puede quemarse con el tiempo. En secadoras de gas, el encendedor puede debilitarse y no encender el gas. Ambos requieren reemplazo profesional pero son reparaciones rutinarias que completamos el mismo día.</p>",
            ),
            (H, "Termostato de Ciclado"),
            (
                P,
                "<p>El termostato de ciclado regula la temperatura dentro de la secadora. Si falla, puede no permitir que el calentador se encienda. Este es un componente económico pero crítico.</p>",
            ),
            (H, "Problemas de Suministro de Gas"),
            (
                P,
                "<p>Para secadoras de gas, verifique que la válvula de gas esté abierta. Las bobinas de la válvula de gas pueden fallar intermitentemente — la secadora calienta al principio del ciclo pero pierde calor durante el secado. Este es un problema que requiere diagnóstico profesional.</p>",
            ),
            (H, "Cuándo Llamar a un Profesional"),
            (
                P,
                "<p>Si ha limpiado la ventilación y el problema persiste, es momento de llamar a un técnico. Nuestros técnicos diagnostican el problema exacto, proporcionan un presupuesto transparente y la mayoría de las reparaciones se completan en la misma visita.</p>",
            ),
            (H, "Preguntas Frecuentes"),
            (
                P,
                "<p><strong>¿Cuánto cuesta reparar una secadora que no calienta?</strong> Las reparaciones más comunes (fusible térmico, elemento calefactor) son económicas. La tarifa de diagnóstico se exime con la aprobación de la reparación.</p><p><strong>¿Puedo usar mi secadora si no calienta?</strong> Sí, pero la ropa no se secará correctamente. El tambor seguirá girando, lo cual no es peligroso, pero es ineficiente.</p>",
            ),
        ],
    },
    # ── Post 3 ──
    "dishwasher-not-draining-causes-solutions": {
        "title": "Lavavajillas No Drena: Causas y Soluciones",
        "seo_title": "¿Lavavajillas No Drena? Causas y Soluciones",
        "search_description": (
            "¿Su lavavajillas no drena el agua? Descubra las causas comunes y soluciones. "
            "Reparación profesional el mismo día en el Inland Empire."
        ),
        "intro": (
            "Un lavavajillas que no drena deja agua sucia estancada. Aquí están las "
            "causas más comunes y cómo solucionarlo."
        ),
        "body": [
            (H, "¿Por Qué Su Lavavajillas No Drena?"),
            (
                P,
                "<p>Abrir su lavavajillas después de un ciclo y encontrar agua estancada en el fondo es un problema común. Las causas van desde bloqueos simples hasta fallas de componentes. Muchos problemas de drenaje se pueden resolver rápidamente.</p>",
            ),
            (H, "Filtro Obstruido"),
            (
                P,
                "<p>La mayoría de los lavavajillas modernos tienen un filtro manual que necesita limpieza regular. Residuos de comida, grasa y partículas se acumulan y bloquean el drenaje. Retire el filtro (generalmente en el fondo del lavavajillas) y límpielo con agua caliente y jabón.</p>",
            ),
            (H, "Bomba de Drenaje Defectuosa"),
            (
                P,
                "<p>La bomba de drenaje expulsa el agua del lavavajillas. Si falla, el agua se queda estancada. Puede escuchar un zumbido cuando la bomba intenta funcionar sin éxito. El reemplazo de la bomba es una reparación profesional común.</p>",
            ),
            (H, "Manguera de Drenaje Obstruida o Torcida"),
            (
                P,
                "<p>La manguera de drenaje conecta su lavavajillas al triturador de basura o tubería de drenaje. Si está torcida, obstruida o mal instalada, el agua no puede salir. Revise debajo del fregadero para ver si la manguera tiene dobleces.</p>",
            ),
            (H, "Problema con el Triturador de Basura"),
            (
                P,
                "<p>Si su lavavajillas drena a través del triturador de basura, un tapón de instalación olvidado o un triturador obstruido puede causar respaldo de agua. Ejecute el triturador para limpiar cualquier bloqueo.</p>",
            ),
            (H, "Válvula de Entrada de Agua"),
            (
                P,
                "<p>Una válvula de entrada defectuosa puede permitir que agua continúe entrando después del ciclo, creando la apariencia de un problema de drenaje. Este componente requiere diagnóstico y reemplazo profesional.</p>",
            ),
            (H, "Cuándo Llamar a un Profesional"),
            (
                P,
                "<p>Si limpiar el filtro y revisar la manguera no resuelve el problema, llame a un técnico. Las fallas de bomba de drenaje y válvula de entrada requieren herramientas y experiencia profesional.</p>",
            ),
            (H, "Preguntas Frecuentes"),
            (
                P,
                "<p><strong>¿Es seguro usar un lavavajillas que no drena?</strong> No es recomendable. El agua estancada puede crear moho y malos olores. Además, el lavavajillas no limpiará correctamente si no puede drenar el agua sucia.</p><p><strong>¿Puedo arreglar la bomba de drenaje yo mismo?</strong> Es posible para alguien con experiencia, pero recomendamos un técnico profesional para asegurar una instalación correcta y segura.</p>",
            ),
        ],
    },
    # ── Post 4 ──
    "appliance-repair-cost-guide": {
        "title": "Guía de Costos de Reparación de Electrodomésticos (2026)",
        "seo_title": "Costos de Reparación de Electrodomésticos — Guía 2026",
        "search_description": (
            "¿Cuánto cuesta reparar un electrodoméstico? Guía completa de costos "
            "de reparación para refrigeradores, lavadoras, secadoras y más."
        ),
        "intro": (
            "Conozca los costos típicos de reparación de electrodomésticos para "
            "tomar decisiones informadas. Guía actualizada para 2026."
        ),
        "body": [
            (H, "¿Cuánto Cuesta Reparar un Electrodoméstico?"),
            (
                P,
                "<p>Conocer los costos típicos de reparación le ayuda a tomar decisiones informadas sobre si reparar o reemplazar un electrodoméstico. Los costos varían según el tipo de electrodoméstico, la gravedad del problema y las piezas necesarias. Aquí desglosamos los rangos de costos comunes.</p>",
            ),
            (H, "Costos de Reparación por Electrodoméstico"),
            (
                P,
                "<p><strong>Refrigerador:</strong> Las reparaciones comunes van desde limpieza de serpentines (mínimo) hasta reemplazo de compresor (lo más costoso). La mayoría de las reparaciones caen en un rango moderado que es significativamente menor que un refrigerador nuevo.</p><p><strong>Lavadora:</strong> Las reparaciones de bombas de drenaje, actuadores de tapa y válvulas de entrada de agua son las más comunes y generalmente económicas.</p><p><strong>Secadora:</strong> El fusible térmico, elemento calefactor y rodamientos de tambor son las reparaciones más frecuentes, todas con costos razonables.</p><p><strong>Lavavajillas:</strong> Bombas de drenaje, válvulas de entrada y brazos rociadores son reparaciones comunes a precios moderados.</p>",
            ),
            (H, "Factores que Afectan el Costo"),
            (
                P,
                "<p>Varios factores influyen en el costo final: la marca del electrodoméstico (las marcas premium requieren piezas más costosas), la edad del modelo, la disponibilidad de piezas y la complejidad de la reparación. Siempre proporcionamos un presupuesto transparente antes de comenzar cualquier trabajo.</p>",
            ),
            (H, "La Tarifa de Diagnóstico"),
            (
                P,
                "<p>Nuestra tarifa de diagnóstico cubre la visita del técnico, inspección completa del electrodoméstico y un presupuesto detallado. Si aprueba la reparación, la tarifa de diagnóstico se exime del costo total. Sin sorpresas, sin cargos ocultos.</p>",
            ),
            (H, "¿Reparar o Reemplazar?"),
            (
                P,
                "<p>La regla general: si la reparación cuesta más del 50% del precio de un electrodoméstico nuevo equivalente, considere el reemplazo. Si el electrodoméstico tiene menos de 10 años y la reparación es razonable, reparar casi siempre es mejor valor. Siempre le daremos una recomendación honesta.</p>",
            ),
            (H, "Preguntas Frecuentes"),
            (
                P,
                "<p><strong>¿Cobran por el presupuesto?</strong> La tarifa de diagnóstico cubre la visita e inspección. Si aprueba la reparación, esa tarifa se descuenta del total.</p><p><strong>¿Hay cargos adicionales por piezas?</strong> El presupuesto que proporcionamos incluye piezas y mano de obra. No hay sorpresas al final.</p>",
            ),
        ],
    },
    # ── Post 5 ──
    "repair-or-replace-appliance-guide": {
        "title": "¿Reparar o Reemplazar? Guía para Decidir sobre Su Electrodoméstico",
        "seo_title": "¿Reparar o Reemplazar Su Electrodoméstico? Guía Completa",
        "search_description": (
            "¿Debería reparar o reemplazar su electrodoméstico? Guía completa con "
            "factores clave, vida útil esperada y cuándo cada opción tiene sentido."
        ),
        "intro": (
            "¿Reparar o reemplazar? Conozca los factores clave para tomar la mejor "
            "decisión sobre su electrodoméstico averiado."
        ),
        "body": [
            (H, "¿Reparar o Reemplazar Su Electrodoméstico?"),
            (
                P,
                "<p>Cuando un electrodoméstico se avería, la primera pregunta es: ¿vale la pena repararlo? La respuesta depende de varios factores que analizaremos para ayudarle a tomar la mejor decisión financiera.</p>",
            ),
            (H, "La Regla del 50%"),
            (
                P,
                "<p>Si el costo de reparación supera el 50% del precio de un electrodoméstico nuevo equivalente, generalmente es mejor reemplazar. Pero esta regla tiene excepciones — los electrodomésticos de gama alta (Sub-Zero, Viking, Wolf) frecuentemente justifican reparaciones costosas porque el reemplazo es mucho más caro.</p>",
            ),
            (H, "Vida Útil Esperada"),
            (
                P,
                "<p><strong>Refrigeradores:</strong> 12-20 años. <strong>Lavadoras:</strong> 10-14 años. <strong>Secadoras:</strong> 13-15 años. <strong>Lavavajillas:</strong> 9-12 años. <strong>Hornos/Estufas:</strong> 15-20 años. Si su electrodoméstico está dentro de estos rangos, la reparación generalmente tiene sentido.</p>",
            ),
            (H, "Eficiencia Energética"),
            (
                P,
                "<p>Los electrodomésticos nuevos son significativamente más eficientes. Si su unidad tiene más de 15 años, un modelo nuevo puede ahorrarle suficiente en facturas de energía para justificar el reemplazo, incluso si la reparación es económica.</p>",
            ),
            (H, "Historial de Reparaciones"),
            (
                P,
                "<p>Si ha reparado el mismo electrodoméstico múltiples veces en los últimos dos años, eso indica un problema sistémico. En estos casos, reemplazar puede ser la mejor inversión a largo plazo.</p>",
            ),
            (H, "Nuestra Recomendación Honesta"),
            (
                P,
                "<p>Siempre le daremos una recomendación honesta. Si creemos que reemplazar es mejor opción, se lo diremos — nunca intentaremos venderle una reparación que no vale la pena. Su confianza es más valiosa que una venta.</p>",
            ),
            (H, "Preguntas Frecuentes"),
            (
                P,
                "<p><strong>¿Qué electrodomésticos vale más la pena reparar?</strong> Refrigeradores, estufas y hornos generalmente valen la pena por su larga vida útil y alto costo de reemplazo.</p><p><strong>¿Cuándo definitivamente debería reemplazar?</strong> Cuando la reparación cuesta más del 50% de uno nuevo, el electrodoméstico ya pasó su vida útil esperada, o ha tenido reparaciones repetidas del mismo problema.</p>",
            ),
        ],
    },
    # ── Post 6 ──
    "how-to-clean-dryer-vent-guide": {
        "title": "Cómo Limpiar el Conducto de la Secadora: Guía Paso a Paso",
        "seo_title": "Cómo Limpiar el Conducto de la Secadora — Guía Completa",
        "search_description": (
            "Aprenda a limpiar el conducto de ventilación de su secadora paso a paso. "
            "Prevenga incendios y mejore la eficiencia de secado."
        ),
        "intro": (
            "Un conducto de secadora obstruido es un riesgo de incendio. Aprenda a "
            "limpiarlo correctamente y con qué frecuencia hacerlo."
        ),
        "body": [
            (H, "Por Qué Limpiar el Conducto de la Secadora"),
            (
                P,
                "<p>Los conductos de secadora obstruidos causan miles de incendios domésticos cada año. Además de ser un riesgo de seguridad, un conducto sucio hace que su secadora trabaje más, use más energía y desgaste las piezas más rápido. Limpiar el conducto es uno de los mantenimientos más importantes del hogar.</p>",
            ),
            (H, "Señales de un Conducto Obstruido"),
            (
                P,
                "<p>La ropa tarda más de un ciclo en secarse, la secadora se siente caliente al tacto, hay un olor a quemado durante el funcionamiento, o la cubierta exterior de ventilación no abre cuando la secadora está funcionando. Si nota cualquiera de estas señales, limpie el conducto inmediatamente.</p>",
            ),
            (H, "Herramientas que Necesita"),
            (
                P,
                "<p>Kit de limpieza de conducto de secadora (varillas flexibles con cepillo), aspiradora con accesorio de manguera, destornillador para abrazaderas de manguera. Los kits de limpieza son económicos y se encuentran en cualquier ferretería.</p>",
            ),
            (H, "Guía Paso a Paso"),
            (
                P,
                "<p><strong>Paso 1:</strong> Desconecte la secadora de la electricidad (y cierre la válvula de gas si es de gas). <strong>Paso 2:</strong> Retire la manguera de ventilación de la parte trasera de la secadora. <strong>Paso 3:</strong> Use el kit de limpieza para cepillar el interior del conducto desde ambos extremos. <strong>Paso 4:</strong> Aspire toda la pelusa suelta. <strong>Paso 5:</strong> Reconecte la manguera y asegure las abrazaderas. <strong>Paso 6:</strong> Ejecute la secadora vacía en caliente por 15 minutos para expulsar pelusa restante.</p>",
            ),
            (H, "Con Qué Frecuencia Limpiar"),
            (
                P,
                "<p>Limpie el conducto al menos una vez al año. Si tiene mascotas, una familia grande o usa la secadora con frecuencia, cada 6 meses es mejor. Limpie el filtro de pelusa después de CADA carga.</p>",
            ),
            (H, "Cuándo Llamar a un Profesional"),
            (
                P,
                "<p>Si su conducto es largo, tiene múltiples curvas, pasa por el techo o no puede acceder a ambos extremos, llame a un profesional. También si sospecha daño en el conducto o si la secadora sigue sin calentar después de la limpieza.</p>",
            ),
        ],
    },
    # ── Post 7 ──
    "appliance-maintenance-tips-save-money": {
        "title": "10 Consejos de Mantenimiento de Electrodomésticos para Ahorrar Dinero",
        "seo_title": "10 Consejos de Mantenimiento de Electrodomésticos — Ahorre Dinero",
        "search_description": (
            "Mantenga sus electrodomésticos funcionando más tiempo con estos 10 consejos "
            "de mantenimiento preventivo. Ahorre dinero en reparaciones costosas."
        ),
        "intro": (
            "El mantenimiento preventivo extiende la vida útil de sus electrodomésticos "
            "y previene reparaciones costosas. Aquí están los 10 consejos más importantes."
        ),
        "body": [
            (H, "Mantenimiento Preventivo que Ahorra Dinero"),
            (
                P,
                "<p>La mayoría de las reparaciones costosas de electrodomésticos son prevenibles con mantenimiento básico. Dedicar unos minutos al mes puede ahorrarle cientos de dólares en reparaciones y extender la vida útil de sus electrodomésticos por años.</p>",
            ),
            (H, "1. Limpie los Serpentines del Refrigerador"),
            (
                P,
                "<p>Aspire los serpentines del condensador cada 6-12 meses. Los serpentines sucios hacen que el compresor trabaje más, aumentando el consumo de energía y reduciendo la vida útil del refrigerador.</p>",
            ),
            (H, "2. Limpie el Conducto de la Secadora"),
            (
                P,
                "<p>Limpie el conducto de ventilación al menos una vez al año y el filtro de pelusa después de cada carga. Un conducto obstruido es un riesgo de incendio y causa desgaste prematuro.</p>",
            ),
            (H, "3. Revise los Sellos de la Puerta del Refrigerador"),
            (
                P,
                "<p>Los sellos desgastados permiten que aire caliente entre, forzando al compresor a trabajar más. Pruebe con un billete — si se desliza fácilmente cuando la puerta está cerrada, los sellos necesitan reemplazo.</p>",
            ),
            (H, "4. Limpie el Filtro del Lavavajillas"),
            (
                P,
                "<p>Limpie el filtro del lavavajillas mensualmente. Los residuos acumulados reducen la eficiencia de limpieza y pueden obstruir la bomba de drenaje.</p>",
            ),
            (H, "5. No Sobrecargue la Lavadora"),
            (
                P,
                "<p>Sobrecargar la lavadora desgasta los rodamientos, la transmisión y el motor prematuramente. Llene al 75% de capacidad máxima para óptimo rendimiento y vida útil.</p>",
            ),
            (H, "6-10. Más Consejos Esenciales"),
            (
                P,
                "<p><strong>6. Nivele sus electrodomésticos</strong> — electrodomésticos desnivelados vibran excesivamente, desgastando componentes. <strong>7. Use la cantidad correcta de detergente</strong> — exceso de detergente causa residuos y problemas. <strong>8. Limpie la máquina de hielo</strong> — cada 6 meses para prevenir acumulación de minerales. <strong>9. Inspeccione mangueras de lavadora</strong> — reemplace mangueras de goma cada 5 años. <strong>10. Programe mantenimiento anual</strong> — una inspección profesional al año detecta problemas antes de que se vuelvan costosos.</p>",
            ),
            (H, "Preguntas Frecuentes"),
            (
                P,
                "<p><strong>¿Cuánto dinero puedo ahorrar con mantenimiento preventivo?</strong> El mantenimiento regular puede reducir sus costos de reparación hasta un 50% y extender la vida útil de sus electrodomésticos 3-5 años adicionales.</p>",
            ),
        ],
    },
    # ── Post 8 ──
    "ice-maker-not-working-troubleshooting": {
        "title": "Máquina de Hielo No Funciona: Guía de Solución de Problemas",
        "seo_title": "¿Máquina de Hielo No Funciona? Guía de Solución",
        "search_description": (
            "¿Su máquina de hielo no produce hielo? Descubra las causas comunes "
            "y soluciones paso a paso. Reparación profesional disponible."
        ),
        "intro": (
            "Si su máquina de hielo dejó de funcionar, estas son las causas más "
            "comunes y qué puede hacer para solucionarlo."
        ),
        "body": [
            (H, "¿Por Qué Su Máquina de Hielo No Funciona?"),
            (
                P,
                "<p>Los problemas de la máquina de hielo son una de las reparaciones más comunes de refrigeradores. Las causas van desde problemas simples que puede resolver usted mismo hasta fallas de componentes que requieren un técnico.</p>",
            ),
            (H, "Verifique el Suministro de Agua"),
            (
                P,
                "<p>La causa más simple: la línea de agua al refrigerador está cerrada o desconectada. Verifique la válvula de suministro detrás o debajo del refrigerador. También revise si la línea de agua está congelada o torcida.</p>",
            ),
            (H, "Filtro de Agua Obstruido"),
            (
                P,
                "<p>Un filtro de agua viejo restringe el flujo de agua a la máquina de hielo. Reemplace el filtro cada 6 meses según las recomendaciones del fabricante.</p>",
            ),
            (H, "Temperatura del Congelador"),
            (
                P,
                "<p>La máquina de hielo necesita que el congelador esté a -18°C (0°F) o menos. Si la temperatura es más alta, la producción de hielo se detiene. Verifique y ajuste la configuración de temperatura.</p>",
            ),
            (H, "Válvula de Entrada de Agua"),
            (
                P,
                "<p>La válvula de entrada de agua controla el flujo al refrigerador. Si falla, no llega agua a la máquina de hielo. Esta válvula requiere reemplazo profesional.</p>",
            ),
            (H, "Módulo de la Máquina de Hielo"),
            (
                P,
                "<p>Si el módulo de la máquina de hielo falla, no produce ni expulsa hielo correctamente. Nuestros técnicos pueden diagnosticar rápidamente si el módulo necesita reemplazo.</p>",
            ),
            (H, "Preguntas Frecuentes"),
            (
                P,
                "<p><strong>¿Cuánto tiempo tarda en hacer hielo después de encenderla?</strong> Una máquina de hielo nueva o recién encendida tarda 24 horas en comenzar a producir hielo normalmente. Los primeros 2-3 lotes deben descartarse.</p><p><strong>¿Cuánto hielo debe producir por día?</strong> La mayoría produce entre 3-5 kg de hielo por día en condiciones normales.</p>",
            ),
        ],
    },
    # ── Post 9 ──
    "washing-machine-shaking-vibrating-causes": {
        "title": "Lavadora Vibra o Tiembla Mucho: Causas y Soluciones",
        "seo_title": "¿Lavadora Vibra Mucho? Causas y Cómo Arreglarlo",
        "search_description": (
            "¿Su lavadora vibra o tiembla excesivamente? Conozca las causas "
            "más comunes y cómo solucionarlo. Guía completa."
        ),
        "intro": (
            "Una lavadora que vibra o se mueve durante el centrifugado puede dañar pisos "
            "y componentes internos. Aquí están las causas y soluciones."
        ),
        "body": [
            (H, "¿Por Qué Su Lavadora Vibra Tanto?"),
            (
                P,
                "<p>Vibración excesiva en la lavadora no solo es molesta — puede dañar pisos, paredes cercanas y los componentes internos de la máquina. Identificar la causa correcta es el primer paso para solucionarlo.</p>",
            ),
            (H, "Lavadora Desnivelada"),
            (
                P,
                "<p>La causa más común de vibración es una lavadora que no está nivelada. Todas las lavadoras tienen patas ajustables. Use un nivel de burbuja y ajuste las patas hasta que la máquina esté perfectamente nivelada en todas las direcciones.</p>",
            ),
            (H, "Carga Desbalanceada"),
            (
                P,
                "<p>Una carga con prendas pesadas en un solo lado causa desbalanceo durante el centrifugado. Distribuya la ropa uniformemente en el tambor. Evite lavar una sola toalla grande o sábana — agregue artículos adicionales para equilibrar la carga.</p>",
            ),
            (H, "Amortiguadores o Resortes Desgastados"),
            (
                P,
                "<p>Las lavadoras de carga frontal usan amortiguadores y las de carga superior usan resortes de suspensión para absorber la vibración. Cuando estos se desgastan, la vibración aumenta dramáticamente. Esta es una reparación profesional.</p>",
            ),
            (H, "Rodamientos de Tambor Desgastados"),
            (
                P,
                "<p>Los rodamientos permiten que el tambor gire suavemente. Cuando se desgastan, escuchará un ruido fuerte de rechinido o golpeteo durante el centrifugado. Si el tambor tiene juego cuando lo mueve manualmente, los rodamientos necesitan reemplazo.</p>",
            ),
            (H, "Tornillos de Transporte No Removidos"),
            (
                P,
                "<p>Las lavadoras nuevas vienen con tornillos de transporte que aseguran el tambor durante el envío. Si no se removieron durante la instalación, causan vibración severa. Revise el manual de su lavadora.</p>",
            ),
            (H, "Cuándo Llamar a un Profesional"),
            (
                P,
                "<p>Si nivelar la lavadora y equilibrar las cargas no resuelve el problema, probablemente necesita reemplazo de amortiguadores, resortes o rodamientos — reparaciones que requieren un técnico experimentado.</p>",
            ),
        ],
    },
    # ── Post 10 ──
    "samsung-refrigerator-error-codes-explained": {
        "title": "Códigos de Error de Refrigerador Samsung: Guía Completa",
        "seo_title": "Códigos de Error Samsung — Qué Significan y Qué Hacer",
        "search_description": (
            "Guía completa de códigos de error de refrigeradores Samsung. "
            "Aprenda qué significa cada código y cuándo llamar a un técnico."
        ),
        "intro": (
            "Los refrigeradores Samsung muestran códigos de error para diagnosticar "
            "problemas. Aquí explicamos los más comunes y qué hacer."
        ),
        "body": [
            (H, "Entendiendo los Códigos de Error Samsung"),
            (
                P,
                "<p>Los refrigeradores Samsung usan códigos alfanuméricos para indicar problemas específicos. Conocer estos códigos le ayuda a entender la urgencia del problema y comunicarse efectivamente con el técnico de reparación.</p>",
            ),
            (H, "Códigos Más Comunes"),
            (
                P,
                "<p><strong>22E / 22C:</strong> Problema del ventilador del congelador — el ventilador no está funcionando correctamente. <strong>41E / 41C:</strong> Error del ventilador del refrigerador. <strong>84E / 84C:</strong> Problema del descongelador — la resistencia de descongelamiento no funciona. <strong>OF OF / O FF:</strong> Modo demo activado — mantenga presionados los botones de temperatura por 5 segundos para desactivar.</p>",
            ),
            (H, "Códigos de Temperatura"),
            (
                P,
                "<p><strong>1E:</strong> Error del sensor de temperatura del congelador. <strong>5E:</strong> Error del sensor de temperatura del refrigerador. <strong>8E:</strong> Error del sensor de la máquina de hielo. Estos códigos generalmente requieren reemplazo del sensor — una reparación rápida y económica.</p>",
            ),
            (H, "Códigos de Comunicación"),
            (
                P,
                "<p><strong>PC ER:</strong> Error de comunicación entre tarjetas de control. Este es uno de los problemas más serios y generalmente requiere reemplazo de la tarjeta de control principal o de la tarjeta de visualización.</p>",
            ),
            (H, "Qué Hacer Cuando Ve un Código"),
            (
                P,
                "<p><strong>Paso 1:</strong> Anote el código exacto. <strong>Paso 2:</strong> Intente un reset — desconecte el refrigerador por 5 minutos y vuelva a conectar. <strong>Paso 3:</strong> Si el código persiste, llame a un técnico profesional. No ignore los códigos de error — indican problemas que generalmente empeoran con el tiempo.</p>",
            ),
            (H, "Preguntas Frecuentes"),
            (
                P,
                "<p><strong>¿Puedo resetear los códigos de error?</strong> Algunos códigos se borran con un ciclo de apagado/encendido. Pero si el problema subyacente no se resuelve, el código regresará.</p><p><strong>¿Es seguro usar mi refrigerador con un código de error?</strong> Depende del código. Errores de temperatura y ventilador significan que su comida puede no estar siendo enfriada correctamente. Es mejor actuar rápido.</p>",
            ),
        ],
    },
    # ── Post 11 ──
    "oven-not-heating-gas-electric-troubleshooting": {
        "title": "Horno No Calienta: Solución de Problemas Gas y Eléctrico",
        "seo_title": "¿Horno No Calienta? Diagnóstico Gas y Eléctrico",
        "search_description": (
            "¿Su horno no calienta? Guía de diagnóstico para hornos de gas y "
            "eléctricos. Causas comunes y cuándo llamar a un profesional."
        ),
        "intro": (
            "Un horno que no calienta interrumpe las comidas familiares. Aquí están "
            "las causas comunes para hornos de gas y eléctricos."
        ),
        "body": [
            (H, "¿Por Qué Su Horno No Calienta?"),
            (
                P,
                "<p>Un horno que no calienta o no alcanza la temperatura correcta tiene diferentes causas dependiendo de si es de gas o eléctrico. Ambos tipos comparten algunos problemas comunes, pero las causas específicas varían.</p>",
            ),
            (H, "Hornos de Gas: Causas Comunes"),
            (
                P,
                "<p><strong>Encendedor desgastado:</strong> El encendedor de gas se debilita con el tiempo. Si brilla pero no enciende el gas, necesita reemplazo — es la reparación más común de hornos de gas. <strong>Válvula de gas defectuosa:</strong> La válvula puede no abrir correctamente, impidiendo el flujo de gas. <strong>Suministro de gas:</strong> Verifique que la válvula de gas esté completamente abierta.</p>",
            ),
            (H, "Hornos Eléctricos: Causas Comunes"),
            (
                P,
                "<p><strong>Elemento calefactor quemado:</strong> Inspeccione visualmente — si tiene manchas, ampollas o rupturas, necesita reemplazo. <strong>Elemento de horneado vs asado:</strong> Si solo uno no funciona, es ese elemento específico. <strong>Tarjeta de control:</strong> Si ambos elementos fallan, la tarjeta de control puede ser la causa.</p>",
            ),
            (H, "Problemas Comunes (Gas y Eléctrico)"),
            (
                P,
                "<p><strong>Sensor de temperatura:</strong> Si el horno no alcanza o excede la temperatura configurada, el sensor de temperatura puede estar defectuoso. <strong>Termostato:</strong> Regula cuándo el horno enciende y apaga el calor. <strong>Tarjeta de control:</strong> Controla todo el horno — si falla, nada funciona correctamente.</p>",
            ),
            (H, "Cuándo Llamar a un Profesional"),
            (
                P,
                "<p>Las reparaciones de hornos de gas involucran gas natural — siempre llame a un profesional. Para hornos eléctricos, los elementos son reemplazables, pero la tarjeta de control y el sensor de temperatura requieren diagnóstico profesional.</p>",
            ),
            (H, "Preguntas Frecuentes"),
            (
                P,
                "<p><strong>¿Es peligroso un horno de gas que no enciende?</strong> Si huele a gas, salga de la casa inmediatamente y llame a la compañía de gas. Si no hay olor a gas, el problema probablemente es el encendedor, que es una reparación segura y común.</p>",
            ),
        ],
    },
    # ── Post 12 ──
    "washing-machine-mold-odors-removal": {
        "title": "Moho y Olores en la Lavadora: Cómo Eliminarlo",
        "seo_title": "Moho en la Lavadora — Cómo Eliminarlo y Prevenirlo",
        "search_description": (
            "¿Su lavadora huele mal o tiene moho? Aprenda a eliminar olores "
            "y moho paso a paso. Prevención y soluciones efectivas."
        ),
        "intro": (
            "El moho y los malos olores en la lavadora son problemas comunes, "
            "especialmente en lavadoras de carga frontal. Aquí cómo eliminarlo."
        ),
        "body": [
            (H, "¿Por Qué Su Lavadora Huele Mal?"),
            (
                P,
                "<p>El moho y los malos olores en lavadoras son causados por humedad atrapada, residuos de detergente y bacterias. Las lavadoras de carga frontal son especialmente susceptibles porque el sello de goma de la puerta atrapa humedad.</p>",
            ),
            (H, "Limpieza del Sello de la Puerta"),
            (
                P,
                "<p>El sello de goma alrededor de la puerta de las lavadoras de carga frontal es el principal culpable. Retire el sello suavemente, limpie con una mezcla de vinagre blanco y bicarbonato de sodio, y seque completamente. Revise si hay moho negro — si es extenso, el sello puede necesitar reemplazo.</p>",
            ),
            (H, "Ciclo de Limpieza"),
            (
                P,
                "<p>Ejecute un ciclo de limpieza con agua caliente y 2 tazas de vinagre blanco, seguido por otro ciclo con media taza de bicarbonato de sodio. Muchas lavadoras modernas tienen un ciclo de limpieza dedicado — úselo mensualmente.</p>",
            ),
            (H, "Limpie el Dispensador de Detergente"),
            (
                P,
                "<p>Retire el cajón del dispensador y límpielo a fondo. Los residuos de detergente y suavizante se acumulan y generan moho. Remoje en agua caliente con vinagre y cepille los residuos.</p>",
            ),
            (H, "Prevención de Olores"),
            (
                P,
                "<p><strong>Deje la puerta abierta</strong> después de cada lavado para permitir que se seque. <strong>Use la cantidad correcta de detergente</strong> — exceso crea residuos. <strong>Seque el sello</strong> después de cada uso. <strong>Use detergente HE</strong> en lavadoras de alta eficiencia.</p>",
            ),
            (H, "Cuándo Reemplazar el Sello"),
            (
                P,
                "<p>Si el moho está profundamente incrustado en el sello y no se elimina con limpieza, es hora de reemplazarlo. Nuestros técnicos pueden reemplazar el sello de la puerta rápidamente, eliminando la fuente del olor de raíz.</p>",
            ),
        ],
    },
    # ── Post 13 ──
    "freezer-not-cold-enough-causes-fixes": {
        "title": "Congelador No Enfría Suficiente: Causas y Soluciones",
        "seo_title": "¿Congelador No Enfría? Causas y Cómo Arreglarlo",
        "search_description": (
            "¿Su congelador no está suficientemente frío? Descubra las causas "
            "comunes y soluciones. Diagnóstico y reparación profesional."
        ),
        "intro": (
            "Un congelador que no mantiene la temperatura correcta puede arruinar "
            "comida congelada. Estas son las causas y cómo solucionarlo."
        ),
        "body": [
            (H, "¿Por Qué Su Congelador No Está Suficientemente Frío?"),
            (
                P,
                "<p>La temperatura ideal del congelador es -18°C (0°F). Si su congelador está más caliente, la comida no se congela correctamente y puede echarse a perder. Las causas van desde ajustes simples hasta fallas de componentes.</p>",
            ),
            (H, "Ajuste de Temperatura"),
            (
                P,
                "<p>Verifique que el control de temperatura esté en el ajuste correcto. Puede haberse movido accidentalmente. Configure a -18°C y espere 24 horas antes de evaluar.</p>",
            ),
            (H, "Puerta No Sella Correctamente"),
            (
                P,
                "<p>Un sello de puerta dañado o sucio permite que aire caliente entre, elevando la temperatura. Limpie el sello con agua tibia y jabón. Si está deformado o agrietado, necesita reemplazo.</p>",
            ),
            (H, "Serpentines del Condensador Sucios"),
            (
                P,
                "<p>Los serpentines sucios reducen la eficiencia de enfriamiento. Aspire los serpentines cada 6-12 meses, especialmente si tiene mascotas.</p>",
            ),
            (H, "Ventilador Evaporador"),
            (
                P,
                "<p>Si el ventilador evaporador no funciona, el aire frío no circula correctamente en el congelador. Puede escuchar que el motor intenta funcionar o no escuchar nada. Este requiere reemplazo profesional.</p>",
            ),
            (H, "Sistema de Descongelamiento"),
            (
                P,
                "<p>Una falla en el sistema de descongelamiento causa acumulación de hielo en los serpentines del evaporador, bloqueando el flujo de aire. Si ve escarcha excesiva dentro del congelador, este es probablemente el problema.</p>",
            ),
            (H, "Cuándo Llamar a un Profesional"),
            (
                P,
                "<p>Si ajustar la temperatura y limpiar los serpentines no resuelve el problema, contacte a un técnico. Los problemas de ventilador, sistema de descongelamiento y compresor requieren diagnóstico profesional.</p>",
            ),
        ],
    },
    # ── Post 14 ──
    "dishwasher-not-cleaning-dishes-properly": {
        "title": "Lavavajillas No Limpia Bien los Platos: Cómo Solucionarlo",
        "seo_title": "¿Lavavajillas No Limpia Bien? Causas y Soluciones",
        "search_description": (
            "¿Su lavavajillas no limpia los platos correctamente? Descubra "
            "las causas comunes y soluciones efectivas."
        ),
        "intro": (
            "Platos sucios después de un ciclo completo es frustrante. Estas son "
            "las causas más comunes y cómo mejorar el rendimiento de su lavavajillas."
        ),
        "body": [
            (H, "¿Por Qué Su Lavavajillas No Limpia Bien?"),
            (
                P,
                "<p>Si sus platos salen sucios, opacos o con residuos después de un ciclo completo, hay varias causas posibles — desde errores de carga hasta fallas mecánicas.</p>",
            ),
            (H, "Carga Incorrecta"),
            (
                P,
                "<p>La causa más común de limpieza deficiente es la carga incorrecta. No sobrecargar, asegurar que los platos no bloqueen los brazos rociadores y colocar los platos más sucios hacia el centro donde el agua tiene más presión.</p>",
            ),
            (H, "Brazos Rociadores Obstruidos"),
            (
                P,
                "<p>Los orificios de los brazos rociadores se obstruyen con depósitos de minerales y residuos de comida. Retire los brazos, limpie cada orificio con un palillo y enjuague con vinagre caliente.</p>",
            ),
            (H, "Filtro Sucio"),
            (
                P,
                "<p>Un filtro sucio recircula agua sucia sobre los platos. Limpie el filtro semanalmente — retírelo, enjuague bajo agua corriente y cepille los residuos acumulados.</p>",
            ),
            (H, "Temperatura del Agua"),
            (
                P,
                "<p>El lavavajillas necesita agua a 50-55°C (120-130°F) para limpiar efectivamente. Si la temperatura del calentador de agua de su hogar es demasiado baja, el lavavajillas no puede desinfectar correctamente.</p>",
            ),
            (H, "Bomba de Circulación"),
            (
                P,
                "<p>La bomba de circulación impulsa agua a través de los brazos rociadores. Si está debilitada o fallando, la presión de agua es insuficiente para limpiar. Esta es una reparación profesional.</p>",
            ),
            (H, "Cuándo Llamar a un Profesional"),
            (
                P,
                "<p>Si limpiar el filtro, los brazos rociadores y verificar la temperatura del agua no mejora la limpieza, probablemente hay un problema con la bomba de circulación, la válvula de entrada o el sensor de turbidez — todos requieren un técnico.</p>",
            ),
        ],
    },
    # ── Post 15 ──
    "no-hot-water-water-heater-troubleshooting": {
        "title": "Sin Agua Caliente: Diagnóstico del Calentador de Agua",
        "seo_title": "¿Sin Agua Caliente? Diagnóstico del Calentador",
        "search_description": (
            "¿No tiene agua caliente? Guía de diagnóstico para calentadores "
            "de agua de gas y eléctricos. Causas comunes y soluciones."
        ),
        "intro": (
            "Quedarse sin agua caliente es incómodo. Aquí están las causas más "
            "comunes y qué puede revisar antes de llamar a un técnico."
        ),
        "body": [
            (H, "¿Por Qué No Tiene Agua Caliente?"),
            (
                P,
                "<p>La falta de agua caliente puede ser causada por varios factores dependiendo del tipo de calentador (gas o eléctrico). Algunos problemas tienen soluciones simples, mientras que otros requieren reparación profesional.</p>",
            ),
            (H, "Calentadores de Gas: Causas Comunes"),
            (
                P,
                "<p><strong>Luz piloto apagada:</strong> Si la luz piloto se apagó, siga las instrucciones del fabricante para reencenderla. Si no se mantiene encendida, el termopar puede necesitar reemplazo. <strong>Termopar defectuoso:</strong> El termopar detecta si la luz piloto está encendida. Si falla, cierra el gas como medida de seguridad. <strong>Válvula de gas:</strong> Asegúrese de que esté en posición abierta.</p>",
            ),
            (H, "Calentadores Eléctricos: Causas Comunes"),
            (
                P,
                "<p><strong>Interruptor disparado:</strong> Revise el panel eléctrico — el interruptor del calentador puede haberse disparado. Resetéelo una vez. Si se dispara de nuevo, hay un problema eléctrico que necesita diagnóstico. <strong>Elementos calefactores:</strong> Los calentadores eléctricos tienen dos elementos. Si uno falla, tendrá agua tibia pero no caliente. Si ambos fallan, no hay calentamiento.</p>",
            ),
            (H, "Problemas Comunes (Ambos Tipos)"),
            (
                P,
                "<p><strong>Termostato:</strong> Si está configurado muy bajo o falla, el agua no se calienta suficiente. <strong>Acumulación de sedimentos:</strong> Los minerales se acumulan en el fondo del tanque, reduciendo eficiencia y capacidad. Drene el tanque anualmente. <strong>Tanque con fugas:</strong> Si el tanque tiene fugas, generalmente necesita reemplazo completo.</p>",
            ),
            (H, "Calentadores Sin Tanque"),
            (
                P,
                "<p>Los calentadores sin tanque pueden fallar por acumulación de minerales en el intercambiador de calor, problemas de flujo de gas o fallos del sensor de flujo. El mantenimiento anual con descalcificación previene la mayoría de los problemas.</p>",
            ),
            (H, "Cuándo Llamar a un Profesional"),
            (
                P,
                "<p>Los calentadores de agua involucran gas, electricidad de alto voltaje y agua caliente — una combinación que requiere experiencia profesional. Si el problema no es tan simple como una luz piloto o interruptor disparado, llame a un técnico certificado.</p>",
            ),
            (H, "Preguntas Frecuentes"),
            (
                P,
                "<p><strong>¿Cuánto dura un calentador de agua?</strong> Los calentadores con tanque duran 8-12 años. Los sin tanque pueden durar 15-20 años con mantenimiento adecuado.</p><p><strong>¿Es peligroso un calentador que gotea?</strong> Una fuga del tanque indica corrosión interna y el tanque puede fallar catastróficamente. Reemplace lo antes posible.</p>",
            ),
        ],
    },
}


class Command(BaseCommand):
    help = "Create or repair Spanish translations of all English blog posts"

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite existing Spanish blog content even when it no longer matches English.",
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

        force = bool(options.get("force"))
        en_posts = BlogPage.objects.filter(locale__language_code="en").order_by("path")
        created = 0
        updated = 0
        skipped = 0
        missed = 0

        for en_post in en_posts:
            translation = BLOG_TRANSLATIONS.get(en_post.slug)
            if not translation:
                self.stderr.write(
                    self.style.WARNING(
                        f'  MISS  No translation for slug="{en_post.slug}"'
                    )
                )
                missed += 1
                continue

            try:
                es_post = BlogPage.objects.filter(
                    translation_key=en_post.translation_key,
                    locale=es_locale,
                ).first()

                if es_post is None:
                    es_post = en_post.copy_for_translation(es_locale)
                    _apply_translation(es_post, en_post, translation)
                    created += 1
                    self.stdout.write(self.style.SUCCESS(f'  +     "{es_post.title}"'))
                    continue

                if _reconcile_translation(es_post, en_post, translation, force=force):
                    updated += 1
                    self.stdout.write(self.style.SUCCESS(f'  UPD   "{es_post.title}"'))
                else:
                    skipped += 1
                    self.stdout.write(f'  SKIP  "{es_post.title}"')

            except Exception as e:
                self.stderr.write(self.style.ERROR(f'  ERROR "{en_post.title}": {e}'))
                logger.exception("Failed to translate blog post %s", en_post.title)

        self.stdout.write(
            self.style.SUCCESS(
                "\nDone! "
                f"Created {created}, updated {updated}, skipped {skipped}, missed {missed}."
            )
        )


def _reconcile_translation(
    es_post: BlogPage,
    en_post: BlogPage,
    translation: dict[str, Any],
    *,
    force: bool,
) -> bool:
    """Repair copied/empty fields without overwriting editor-authored Spanish."""

    changed = False
    for field in ("title", "seo_title", "search_description", "intro"):
        current = str(getattr(es_post, field, "") or "")
        english = str(getattr(en_post, field, "") or "")
        desired = str(translation.get(field, "") or "")
        if (force or not current or current == english) and current != desired:
            setattr(es_post, field, desired)
            changed = True

    if not es_post.author_name and en_post.author_name:
        es_post.author_name = en_post.author_name
        changed = True

    normalized_body, body_was_normalized = normalized_stream_json(es_post.body)
    normalized_en_body, _ = normalized_stream_json(en_post.body)
    if "body" in translation and (
        force or normalized_body is None or normalized_body == normalized_en_body
    ):
        desired_body = _body(translation["body"])
        if normalized_body != desired_body:
            es_post.body = desired_body
            changed = True
    elif body_was_normalized and normalized_body is not None:
        es_post.body = normalized_body
        changed = True

    if changed:
        es_post.save()
        es_post.save_revision().publish()
    return changed


def _apply_translation(
    es_post: BlogPage,
    en_post: BlogPage,
    translation: dict[str, Any],
) -> None:
    """Apply static Spanish content while preserving Wagtail translation linkage."""

    es_post.title = translation["title"]
    es_post.seo_title = translation.get("seo_title", "")
    es_post.search_description = translation.get("search_description", "")
    es_post.intro = translation.get("intro", "")
    es_post.author_name = en_post.author_name

    if "body" in translation:
        es_post.body = _body(translation["body"])

    # Keep slugs aligned with English so existing /es/blog/<slug>/ URLs remain stable.
    es_post.slug = en_post.slug

    es_post.tags.set([tag.name for tag in en_post.tags.all()])
    es_post.save()
    es_post.save_revision().publish()
