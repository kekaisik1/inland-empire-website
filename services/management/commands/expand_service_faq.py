"""Expand service page FAQ answers to 300-500 chars for featured snippet eligibility.

Usage:
    python manage.py expand_service_faq          # dry-run
    python manage.py expand_service_faq --apply  # applies changes
"""

from __future__ import annotations

import logging
from typing import Any

from django.core.management.base import BaseCommand, CommandParser

from services.models import ServicePage

logger = logging.getLogger(__name__)

# Minimum answer length in chars (target: 300-500 for featured snippets)
MIN_ANSWER_LENGTH = 280

# ---------------------------------------------------------------------------
# Expanded FAQ answers per service (English only — Spanish should be
# translated separately). Keyed by service slug → question → answer.
# ---------------------------------------------------------------------------

EXPANDED_FAQS: dict[str, dict[str, str]] = {
    "refrigerator-repair": {
        "Why is my refrigerator not cooling?": (
            "The most common causes are a dirty condenser coil, a faulty"
            " evaporator fan motor, a malfunctioning thermostat, or a"
            " refrigerant leak. A clogged or frosted-over evaporator coil can"
            " also block airflow between the freezer and fridge compartments."
            " Our technician will run a full diagnostic to pinpoint the exact"
            " cause and provide a repair quote before starting any work —"
            " the $70 diagnostic is waived when you approve the repair."
        ),
        "How much does refrigerator repair cost?": (
            "Most refrigerator repairs range from $150 to $400 depending on"
            " the specific issue and parts required. Common fixes like"
            " thermostat or fan motor replacement fall at the lower end, while"
            " compressor repairs or sealed-system work cost more. Our $70"
            " diagnostic fee is waived when you approve the repair, and you"
            " receive a complete itemized quote before any work begins — no"
            " hidden fees. Repair is almost always more cost-effective than"
            " replacement for units under 10-12 years old."
        ),
        "Is it worth repairing an old refrigerator?": (
            "As a general rule, if your refrigerator is under 10-12 years old"
            " and the repair cost is less than half the price of a new unit,"
            " repair is usually the smarter choice. Modern refrigerators have"
            " an average lifespan of 12-20 years depending on the brand and"
            " model. We will give you an honest assessment based on the"
            " diagnosis — including the appliance's age, the specific failure,"
            " and whether replacement parts are still available. We never"
            " push unnecessary repairs."
        ),
        "How long does refrigerator repair take?": (
            "Most refrigerator repairs take 1 to 2 hours from diagnosis to"
            " completion. Our trucks carry common parts — compressors,"
            " thermostats, evaporator fans, door seals, control boards, and"
            " defrost heaters — so the majority of repairs are completed in a"
            " single visit. Complex sealed-system work like compressor"
            " replacement may take up to 3 hours. We schedule same-day"
            " appointments 7 days a week so you are not stuck waiting."
        ),
        "Do you repair built-in and Sub-Zero refrigerators?": (
            "Yes, we service all refrigerator types including built-in units"
            " from Sub-Zero, Viking, Thermador, and other premium brands. Our"
            " technicians are factory-trained on these high-end models and"
            " carry specialized OEM parts. Built-in refrigerators require"
            " specific knowledge of integrated ventilation and panel mounting"
            " that our team handles routinely. Warranty included on all"
            " premium brand repairs."
        ),
        "My ice maker stopped working. Can you fix it?": (
            "Ice maker problems are one of our most common repair calls."
            " Whether your ice maker has stopped producing ice entirely, is"
            " making small or hollow cubes, leaking water, or producing ice"
            " with an off taste, we diagnose and fix the root cause — often"
            " in under an hour. Common issues include faulty water inlet"
            " valves, frozen fill tubes, defective ice maker modules, and"
            " temperature sensor failures. We carry parts for all major"
            " brands on our trucks."
        ),
    },
    "freezer-repair": {
        "Why is my freezer not freezing properly?": (
            "A freezer that isn't reaching proper temperature usually has a"
            " failed evaporator fan motor, a malfunctioning defrost system,"
            " dirty condenser coils, or a faulty thermostat. Ice buildup on"
            " the evaporator coils is another common culprit — it blocks"
            " airflow and prevents the freezer from cooling evenly. Our"
            " technician will run a full diagnostic to identify the exact"
            " issue and provide an upfront repair quote."
        ),
        "How much does freezer repair cost?": (
            "Freezer repairs typically range from $150 to $350 depending on"
            " the specific problem and parts required. Thermostat and fan"
            " motor replacements tend to be on the lower end, while"
            " compressor or sealed-system repairs cost more. Our $70"
            " diagnostic is waived when you approve the repair. You always"
            " receive an itemized quote before we start — no surprises."
            " Repair is usually more economical than replacing a chest or"
            " upright freezer that is less than 15 years old."
        ),
        "Is frost buildup inside my freezer a sign of a problem?": (
            "Excessive frost buildup is almost always a sign of a"
            " malfunctioning defrost system. Modern freezers have automatic"
            " defrost cycles controlled by a defrost timer, heater, and"
            " thermostat. When any of these components fail, ice accumulates"
            " on the evaporator coils and interior walls, reducing cooling"
            " efficiency and storage space. We diagnose which defrost"
            " component has failed and replace it with OEM parts — typically"
            " completed in one visit."
        ),
        "Should I repair or replace my old freezer?": (
            "Chest freezers and upright freezers can last 15-20 years with"
            " proper maintenance. If the repair cost is less than half the"
            " replacement price and the unit is under 15 years old, repair"
            " is usually the better value. We provide an honest assessment"
            " based on the age of your freezer, the specific failure, and"
            " parts availability. If replacement makes more sense, we will"
            " tell you — we do not push unnecessary repairs."
        ),
        "Do you repair commercial walk-in freezers?": (
            "Yes, our EPA 608 certified technicians service commercial"
            " walk-in freezers, reach-in freezers, and blast chillers. We"
            " understand that a failed commercial freezer means lost inventory"
            " and lost revenue, which is why we offer same-day service for"
            " commercial clients. We carry commercial-rated parts and have"
            " experience with major commercial brands. Warranty included on"
            " all commercial repairs."
        ),
    },
    "washer-repair": {
        "Why is my washer leaking water?": (
            "Washer leaks typically come from a worn door boot seal (on"
            " front-loaders), a cracked drain hose, a loose hose connection,"
            " or a faulty water inlet valve. Overloading the machine or using"
            " too much detergent can also cause overflow leaks. Our"
            " technician inspects all potential leak points, identifies the"
            " source, and fixes it on the spot with OEM parts. We carry"
            " door seals, hoses, inlet valves, and pump assemblies for all"
            " major brands on our trucks."
        ),
        "How much does washing machine repair cost?": (
            "Most washing machine repairs cost between $150 and $350"
            " depending on the issue and parts needed. Common repairs like"
            " lid switch replacement, drain pump repair, or inlet valve"
            " replacement fall at the lower end. Motor and transmission"
            " repairs for top-loaders or bearing replacements for"
            " front-loaders are at the higher end. Our $70 diagnostic fee"
            " is waived when you approve the repair, and you receive a"
            " detailed quote before work begins."
        ),
        "Why won't my washer spin or drain?": (
            "A washer that won't spin or drain usually has a failed lid"
            " switch (top-loaders), a broken door latch (front-loaders), a"
            " clogged drain pump, a worn drive belt, or a faulty motor"
            " coupling. Items like coins, hair clips, or small socks can"
            " also clog the drain pump. Our technician will diagnose the"
            " root cause and provide a quote. Most spin and drain issues"
            " are resolved in a single visit with parts we carry on our"
            " trucks."
        ),
        "My washer is making loud noises. What's wrong?": (
            "Loud banging, grinding, or squealing during the wash or spin"
            " cycle usually indicates worn drum bearings, a damaged drive"
            " belt, a failing motor coupling, loose drum baffles, or foreign"
            " objects caught between the drum and tub. Front-loaders with"
            " worn bearings often produce a rumbling sound that gets louder"
            " during the spin cycle. Our technicians diagnose the specific"
            " cause and repair it with OEM parts. Most noise-related"
            " repairs are completed the same day."
        ),
        "Is it worth repairing an old washing machine?": (
            "Top-loading washers typically last 12-14 years, while"
            " front-loaders last 10-13 years. If your washer is within"
            " that range and the repair cost is less than half the"
            " replacement price, repair usually makes financial sense. We"
            " give honest advice based on the specific diagnosis, your"
            " machine's age and condition, and parts availability. If"
            " replacement is the better option, we will tell you."
        ),
        "Do you repair all washer brands?": (
            "Yes, we repair all major washer brands including Whirlpool,"
            " Samsung, LG, GE, Maytag, Kenmore, Frigidaire, Bosch,"
            " Electrolux, and Speed Queen. Our technicians are"
            " factory-trained and carry brand-specific OEM parts on every"
            " truck. Whether you have a top-loader, front-loader, stackable,"
            " or commercial-grade unit, we have the training and parts to"
            " repair it. Warranty included on all repairs."
        ),
    },
    "dryer-repair": {
        "Why isn't my dryer heating?": (
            "A dryer that runs but doesn't produce heat usually has a burned-"
            "out heating element (electric dryers), a faulty gas igniter or"
            " gas valve solenoid (gas dryers), a broken thermal fuse, or a"
            " malfunctioning thermostat. A clogged lint trap or blocked vent"
            " duct can also cause the dryer to overheat and trip its thermal"
            " fuse as a safety measure. Our technician will diagnose the"
            " exact component that failed and replace it with OEM parts —"
            " typically in one visit."
        ),
        "How much does dryer repair cost?": (
            "Most dryer repairs cost between $150 and $350 depending on the"
            " issue and parts needed. Heating element, thermostat, and"
            " thermal fuse replacements are on the lower end, while motor"
            " replacements and gas valve repairs may cost more. Our $70"
            " diagnostic fee is waived when you approve the repair, and you"
            " receive an itemized quote before work starts. Dryer repair is"
            " almost always more affordable than buying a new unit."
        ),
        "Why is my dryer making a squealing or grinding noise?": (
            "Squealing typically means a worn drum belt or failing idler"
            " pulley. Grinding or rumbling sounds usually indicate worn drum"
            " support rollers, damaged drum glides, or a failing motor"
            " bearing. These are all common wear items that we carry on our"
            " trucks. Left unaddressed, worn rollers and bearings can damage"
            " the drum itself, so prompt repair saves money in the long run."
            " Most noise-related dryer repairs take 1-2 hours."
        ),
        "How often should I clean my dryer vent?": (
            "The U.S. Fire Administration recommends cleaning your dryer vent"
            " at least once a year — more often if you do heavy laundry loads"
            " or have a longer vent run. Clogged vents are a leading cause of"
            " house fires and also make your dryer work harder, increasing"
            " energy bills and accelerating component wear. Signs of a clogged"
            " vent include longer drying times, a hot dryer exterior, and a"
            " burning smell. If you notice these symptoms, call us"
            " immediately."
        ),
        "My dryer takes too long to dry clothes. What's the issue?": (
            "Extended drying times are usually caused by a restricted vent"
            " duct, a clogged lint screen, a failing heating element, worn"
            " drum seals that leak hot air, or a malfunctioning moisture"
            " sensor. Our technician checks all of these during the"
            " diagnostic. A simple vent cleaning sometimes solves the problem,"
            " but if a component has failed, we replace it with OEM parts on"
            " the spot. Restoring proper drying times also reduces your"
            " energy costs."
        ),
        "Do you repair gas and electric dryers?": (
            "Yes, we service both gas and electric dryers from all major"
            " brands. Gas dryers require specific knowledge of gas valve"
            " solenoids, igniters, and flame sensors — our technicians are"
            " trained and certified to work on gas appliances safely. Electric"
            " dryers have their own set of components including heating"
            " elements, high-limit thermostats, and thermal fuses. We carry"
            " parts for both types on every truck."
        ),
    },
    "dishwasher-repair": {
        "Why isn't my dishwasher cleaning properly?": (
            "Poor cleaning performance usually stems from clogged spray arms,"
            " a failing wash pump, a malfunctioning detergent dispenser, hard"
            " water mineral buildup, or a faulty water inlet valve that"
            " doesn't fill the tub with enough water. The water temperature"
            " may also be too low — dishwashers need 120°F water for optimal"
            " cleaning. Our technician will diagnose the specific cause and"
            " fix it with OEM parts. Most cleaning issues are resolved in a"
            " single visit."
        ),
        "How much does dishwasher repair cost?": (
            "Most dishwasher repairs range from $150 to $300 depending on"
            " the issue. Common fixes like pump replacements, door latch"
            " repairs, and spray arm cleaning fall at the lower end."
            " Control board or motor replacements are at the higher end."
            " Our $70 diagnostic fee is waived with repair approval, and"
            " you get a detailed quote before work begins. Repair is usually"
            " the better value for dishwashers under 8-10 years old."
        ),
        "My dishwasher won't drain. What should I do?": (
            "A dishwasher that won't drain usually has a clogged drain hose,"
            " a blocked garbage disposal connection, a failed drain pump, or"
            " a faulty check valve. Before calling for service, check that"
            " your garbage disposal isn't clogged and run it to clear the"
            " line. If the problem persists, our technician will diagnose"
            " and fix the exact cause. We carry drain pumps, hoses, and"
            " valves for all major brands on our trucks."
        ),
        "Why is my dishwasher leaking?": (
            "Dishwasher leaks most commonly come from a worn door gasket,"
            " a cracked or loose hose connection, a failing water inlet"
            " valve, or a damaged tub. Using too much detergent or the"
            " wrong type (non-HE in an HE machine) can also cause excess"
            " suds that leak through the door seal. Our technician pinpoints"
            " the leak source during diagnosis and repairs it on the spot."
            " Most dishwasher leak repairs are completed within an hour."
        ),
        "Should I repair or replace my dishwasher?": (
            "The average dishwasher lasts 8-12 years. If yours is within"
            " that range and the repair cost is less than half the price of a"
            " new unit, repair is typically the smarter financial choice."
            " Dishwashers are among the more affordable major appliances to"
            " replace, so for units over 10 years old with major component"
            " failures (motor, tub), replacement may make more sense. We"
            " provide honest recommendations based on your specific situation."
        ),
    },
    "oven-repair": {
        "Why is my oven not heating properly?": (
            "An oven that won't reach temperature or heats unevenly usually"
            " has a failed heating element (electric), a faulty igniter"
            " (gas), a malfunctioning temperature sensor, or a broken"
            " thermostat. A worn door gasket can also leak heat and prevent"
            " the oven from maintaining temperature. Our technician tests"
            " each component systematically to identify the exact failure"
            " and replaces it with OEM parts. Most oven heating issues are"
            " fixed in one visit."
        ),
        "How much does oven repair cost?": (
            "Most oven repairs cost between $150 and $400 depending on the"
            " issue and parts required. Igniter and heating element"
            " replacements are at the lower end, while control board or"
            " convection fan motor repairs cost more. Our $70 diagnostic"
            " fee is waived when you approve the repair. You receive a"
            " complete quote before any work begins. Oven repair is nearly"
            " always more cost-effective than replacing the entire unit,"
            " especially for built-in or double wall ovens."
        ),
        "Is it safe to use my oven if it smells like gas?": (
            "No — if you smell gas from your oven, turn it off immediately,"
            " do not use any electrical switches, open windows, and leave"
            " the house. Call your gas company's emergency line first. Once"
            " the gas company has confirmed the area is safe, call us for a"
            " diagnostic. Gas leaks can come from a faulty gas valve, a"
            " cracked gas line connection, or a worn safety valve. Our"
            " technicians are trained and certified to work on gas"
            " appliances safely."
        ),
        "My oven door won't close properly. Can you fix it?": (
            "A misaligned or loose oven door is usually caused by worn door"
            " hinges, a broken hinge spring, or a damaged door gasket."
            " Besides being inconvenient, a poorly sealing door leaks heat"
            " and wastes energy — it can also cause uneven cooking results."
            " We carry replacement hinges, springs, and gaskets for all major"
            " brands on our trucks. Most oven door repairs take under an"
            " hour and are immediately noticeable in cooking performance."
        ),
        "Do you repair gas and electric ovens?": (
            "Yes, we repair both gas and electric ovens from all major"
            " brands — freestanding, slide-in, wall ovens, double ovens,"
            " and commercial-grade units. Gas ovens require specific"
            " knowledge of igniters, gas valves, and safety systems, while"
            " electric ovens involve heating elements, relays, and"
            " temperature sensors. Our EPA-certified technicians are"
            " trained on both types and carry parts for same-day repair."
        ),
    },
    "stove-repair": {
        "Why won't my stove burner ignite?": (
            "A gas burner that clicks but won't light usually has a clogged"
            " burner port, a misaligned igniter electrode, a faulty spark"
            " module, or a defective gas valve. Food debris and grease"
            " buildup are the most common causes — sometimes a thorough"
            " cleaning resolves the issue. If cleaning doesn't help, our"
            " technician will diagnose the electrical or gas components and"
            " replace the faulty part with OEM replacements. Most burner"
            " ignition repairs are completed within an hour."
        ),
        "How much does stove repair cost?": (
            "Stove repairs typically range from $150 to $350 depending on"
            " the issue. Burner element replacements, igniter repairs, and"
            " switch replacements fall at the lower end. Glass cooktop"
            " replacements and control board repairs cost more. Our $70"
            " diagnostic fee is waived with repair approval. You receive a"
            " full quote before work begins — no surprises. Stove repair"
            " is almost always cheaper than replacing the entire unit."
        ),
        "My electric stove burner won't turn off. Is this dangerous?": (
            "Yes — a burner that stays on can be a fire hazard. The most"
            " likely cause is a faulty infinite switch (the knob control) or"
            " a shorted burner element. Unplug the stove or turn off the"
            " circuit breaker immediately and call for service. Do not"
            " attempt to fix electrical components yourself. Our technician"
            " will safely diagnose and replace the faulty switch or element"
            " with OEM parts. This is a repair we prioritize for same-day"
            " service."
        ),
        "Do you repair glass/ceramic cooktops?": (
            "Yes, we repair all types of cooktops including glass-ceramic"
            " (smooth-top), induction, gas, and electric coil models. Common"
            " glass cooktop issues include cracked surfaces, burnt-out"
            " radiant elements, faulty touch controls, and heating"
            " inconsistencies. We carry replacement elements and control"
            " components for major brands. Note that cracked glass tops"
            " require full panel replacement — we can source the correct"
            " panel for your model."
        ),
        "Can you repair induction cooktops?": (
            "Yes, we service induction cooktops from all major brands"
            " including Samsung, LG, Bosch, GE, and KitchenAid. Common"
            " induction issues include error codes, heating inconsistency,"
            " and failed induction coils. Induction technology requires"
            " specialized diagnostic equipment, which our technicians carry."
            " We use OEM parts for all induction repairs and include a"
            " warranty on parts and labor."
        ),
    },
    "water-heater-repair": {
        "Why is my water heater not producing hot water?": (
            "No hot water from a gas water heater usually means the pilot"
            " light is out, the thermocouple has failed, or the gas valve"
            " is defective. For electric water heaters, the most common"
            " causes are a failed heating element or a tripped reset button"
            " (high-limit switch). A faulty thermostat can also prevent"
            " proper heating on either type. Our technician will diagnose"
            " the exact cause and repair it on the spot with OEM parts."
        ),
        "How much does water heater repair cost?": (
            "Most water heater repairs range from $150 to $400 depending on"
            " the issue. Thermocouple, thermostat, and heating element"
            " replacements are at the lower end. Gas valve and anode rod"
            " replacements cost more. Our $70 diagnostic fee is waived when"
            " you approve the repair. You receive a complete quote before"
            " work begins. Repair is usually the right call for water"
            " heaters under 8-10 years old — replacement makes more sense"
            " for older units with major failures."
        ),
        "Is a leaking water heater an emergency?": (
            "A leaking water heater should be addressed promptly. While a"
            " slow drip from the pressure relief valve may be minor, active"
            " leaking from the tank bottom usually indicates internal"
            " corrosion and means replacement rather than repair. Water"
            " damage from a failed tank can be expensive. Turn off the water"
            " supply and the power (gas or electric) to the unit, and call"
            " us for a same-day assessment. We will tell you honestly"
            " whether repair or replacement is the right option."
        ),
        "How long do water heaters last?": (
            "Tank water heaters typically last 8-12 years, while tankless"
            " models can last 15-20 years with proper maintenance. The"
            " lifespan depends on water quality (hard water shortens it),"
            " maintenance (annual flushing helps), and usage patterns. If"
            " your water heater is approaching 10 years old and showing"
            " signs of trouble — rusty water, decreased hot water volume,"
            " strange noises — we can assess whether repair or replacement"
            " makes more sense for your situation."
        ),
        "Do you repair tankless water heaters?": (
            "Yes, we service both tank and tankless water heaters from all"
            " major brands including Rheem, A.O. Smith, Bradford White,"
            " Rinnai, Navien, and Noritz. Tankless units have specific"
            " maintenance needs including descaling and filter cleaning."
            " Common tankless issues include error codes, ignition failures,"
            " and mineral buildup in the heat exchanger. Our technicians"
            " carry the tools and parts for same-day tankless repair."
        ),
    },
    "air-conditioning-repair-hvac": {
        "Why isn't my AC cooling the house?": (
            "An AC that runs but doesn't cool usually has low refrigerant"
            " (from a leak), a dirty or frozen evaporator coil, a failing"
            " compressor, a blocked condenser unit, or a faulty thermostat."
            " A dirty air filter can also restrict airflow enough to reduce"
            " cooling performance significantly. Our technician will check"
            " refrigerant levels, inspect both coils, test the compressor,"
            " and diagnose the exact problem before providing a quote."
        ),
        "How much does AC repair cost?": (
            "AC repair costs range from $150 to $500 depending on the issue."
            " Capacitor and contactor replacements are at the lower end."
            " Refrigerant recharge, evaporator coil repair, and compressor"
            " replacement cost more. Our $70 diagnostic fee is waived when"
            " you approve the repair. You receive an itemized quote before"
            " work starts. For older units needing major repairs, we will"
            " advise honestly on whether repair or replacement is the"
            " better investment."
        ),
        "How often should I service my AC unit?": (
            "Professional AC maintenance should be done at least once a year,"
            " ideally in spring before the cooling season. Annual service"
            " includes cleaning the evaporator and condenser coils, checking"
            " refrigerant levels, inspecting electrical connections, and"
            " testing the thermostat. Homeowners should also replace the air"
            " filter every 1-3 months during heavy use. Regular maintenance"
            " extends the unit's lifespan, improves efficiency, and prevents"
            " costly emergency repairs during heat waves."
        ),
        "Why is my AC making strange noises?": (
            "Buzzing usually indicates a failing contactor or loose wiring."
            " Banging or clanking suggests a loose or broken component inside"
            " the compressor. Squealing may mean a worn fan belt or failing"
            " fan motor bearing. Hissing can signal a refrigerant leak. Any"
            " unusual noise warrants prompt inspection — small issues can"
            " become major failures quickly if left unaddressed. Our"
            " technicians diagnose and fix AC noise issues same-day with"
            " OEM replacement parts."
        ),
        "My AC is leaking water inside. What should I do?": (
            "Indoor water leaks from your AC typically mean a clogged"
            " condensate drain line, a cracked drain pan, or a frozen"
            " evaporator coil that's melting. Turn off the AC to prevent"
            " water damage and check if the air filter is dirty — a"
            " restricted filter can cause the coil to freeze. If the problem"
            " isn't a dirty filter, call us for a same-day diagnostic. We"
            " clear clogged drain lines and replace damaged components to"
            " stop the leak and prevent mold growth."
        ),
        "Do you service all AC brands and types?": (
            "Yes, we service central AC systems, mini-splits, heat pumps,"
            " and window units from all major brands including Carrier,"
            " Lennox, Trane, Goodman, Rheem, Daikin, Mitsubishi, and more."
            " Our technicians hold EPA 608 certification, which is required"
            " for handling refrigerants. We carry common HVAC parts"
            " — capacitors, contactors, fan motors, and thermostats —"
            " on every truck for same-day repair."
        ),
    },
    "microwave-repair": {
        "Why isn't my microwave heating food?": (
            "A microwave that runs but doesn't heat almost always has a"
            " failed magnetron — the component that generates microwaves."
            " Other causes include a burned-out high-voltage diode, a"
            " defective high-voltage capacitor, or a faulty door switch that"
            " doesn't engage properly. Our technician will safely test the"
            " high-voltage components and identify the exact failure."
            " Most microwave heating repairs are completed in one visit with"
            " OEM parts."
        ),
        "How much does microwave repair cost?": (
            "Microwave repairs typically cost between $100 and $250"
            " depending on the issue. Door switch and turntable motor"
            " replacements are at the lower end. Magnetron replacement is"
            " at the higher end. Our $70 diagnostic fee is waived with"
            " repair approval. For countertop microwaves under $200,"
            " replacement sometimes makes more financial sense than a major"
            " repair — we will give you an honest recommendation. Built-in"
            " and over-the-range microwaves are almost always worth"
            " repairing due to their higher replacement cost."
        ),
        "Is it safe to use a microwave with a cracked door?": (
            "No — do not use a microwave with a cracked or damaged door,"
            " door seal, or door latch. The door and its seals are critical"
            " safety components that contain microwave radiation. Even"
            " hairline cracks in the door glass or damage to the mesh screen"
            " can allow radiation leakage. Turn the microwave off and call"
            " for service. Our technicians can replace damaged doors, seals,"
            " and latch assemblies with OEM parts to restore safe"
            " operation."
        ),
        "My microwave turntable isn't spinning. Can you fix it?": (
            "A non-spinning turntable is usually caused by a worn turntable"
            " motor, a broken coupler (the three-pronged piece under the"
            " glass plate), or a misaligned guide roller ring. While the"
            " microwave will still heat food without a spinning turntable,"
            " it will heat unevenly. This is typically a quick, affordable"
            " repair. We carry turntable motors and couplers for all major"
            " brands and usually complete the fix in under 30 minutes."
        ),
        "Do you repair built-in and over-the-range microwaves?": (
            "Yes, we service all microwave types including built-in,"
            " over-the-range (OTR), countertop, and drawer-style models from"
            " all major brands. Built-in and OTR microwaves are more complex"
            " to service due to their installation — they require careful"
            " extraction and reinstallation. Our technicians are experienced"
            " with these installations and carry the necessary hardware."
            " Repair is almost always worthwhile for built-in units due to"
            " the high cost of replacement and installation."
        ),
    },
}


class Command(BaseCommand):
    help = "Expand thin FAQ answers on service pages to 300-500 chars."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Apply changes (default is dry-run).",
        )

    def handle(self, *args: object, **options: dict[str, Any]) -> None:
        apply = options["apply"]
        mode = "APPLYING" if apply else "DRY-RUN"

        self.stdout.write(f"\n{'=' * 60}")
        self.stdout.write(f"  Service FAQ Expansion — {mode}")
        self.stdout.write(f"{'=' * 60}\n")

        updated = 0
        en_pages = ServicePage.objects.live().filter(locale__language_code="en")

        for page in en_pages:
            slug = page.slug
            expanded = EXPANDED_FAQS.get(slug)
            if not expanded:
                self.stdout.write(
                    self.style.WARNING(f"  SKIP: No expanded FAQs for '{slug}'")
                )
                continue

            changes: list[str] = []
            new_faq_data = []
            changed = False

            for block in page.faq:
                question = str(block.value.get("question", ""))
                answer = str(block.value.get("answer", ""))

                if question in expanded:
                    new_answer = expanded[question]
                    if len(answer) < MIN_ANSWER_LENGTH and len(new_answer) > len(
                        answer
                    ):
                        changes.append(
                            f"    Q: {question[:50]}... "
                            f"({len(answer)} → {len(new_answer)} chars)"
                        )
                        new_faq_data.append(
                            {
                                "type": "faq_item",
                                "value": {"question": question, "answer": new_answer},
                            }
                        )
                        changed = True
                        continue

                new_faq_data.append(
                    {
                        "type": "faq_item",
                        "value": {"question": question, "answer": answer},
                    }
                )

            if not changed:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  OK: {page.title} — all answers already >= {MIN_ANSWER_LENGTH} chars"
                    )
                )
                continue

            self.stdout.write(f"\n  {page.title} ({len(changes)} answers expanded):")
            for change in changes:
                self.stdout.write(change)

            if apply:
                import json

                page.faq = json.dumps(new_faq_data)
                revision = page.save_revision()
                revision.publish()
                updated += 1
                self.stdout.write(self.style.SUCCESS("    ✓ Saved and published"))

        self.stdout.write(f"\n{'=' * 60}")
        if apply:
            self.stdout.write(self.style.SUCCESS(f"  Done — {updated} pages updated."))
        else:
            self.stdout.write("  Dry-run complete. Run with --apply to save changes.")
        self.stdout.write(f"{'=' * 60}\n")
