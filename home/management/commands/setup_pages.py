"""
Management command to set up the complete page structure with SEO-optimized content.

Run with: python manage.py setup_pages
"""

from __future__ import annotations

import json
from typing import Any

from django.core.management.base import BaseCommand
from wagtail.models import Page, Site

from blog.models import BlogIndexPage
from home.models import HomePage
from locations.models import CityPage, LocationsIndexPage
from pages.models import StaticPage
from services.models import ServicePage, ServicesIndexPage


# ── Service Content Data ──────────────────────────────────────────────────

SERVICE_CONTENT: list[dict[str, Any]] = [
    {
        "title": "Refrigerator Repair",
        "slug": "refrigerator-repair",
        "seo_title": "Refrigerator Repair — Same-Day Service, All Brands",
        "search_description": (
            "Professional refrigerator repair — same-day service for all brands. "
            "Fix cooling issues, leaks, ice makers & compressors. "
            "Warranty included. Call now for a diagnostic."
        ),
        "intro": (
            "Expert refrigerator repair for all major brands — "
            "same-day service with warranty included"
        ),
        "short_description": "Fix cooling issues, leaks, ice makers, and strange noises.",
        "hero_usp": (
            "Same-day refrigerator repair for Samsung, LG, Whirlpool, "
            "GE, and all major brands."
        ),
        "body": (
            "<h2>Expert Refrigerator Repair You Can Trust</h2>"
            "<p>A malfunctioning refrigerator means spoiled food, wasted money, "
            "and daily disruption. Our certified technicians diagnose and repair "
            "refrigerator problems on the first visit — most repairs are completed "
            "the same day you call. We service all major brands including Samsung, "
            "LG, Whirlpool, GE, Maytag, KitchenAid, Sub-Zero, and Frigidaire.</p>"
            "<h2>Common Refrigerator Issues We Repair</h2>"
            "<p>Whether your fridge isn't cooling, is leaking water, making unusual "
            "noises, or running constantly, we've seen it all. Our trucks are fully "
            "stocked with OEM parts for compressors, thermostats, evaporator fans, "
            "condenser coils, defrost heaters, and control boards — so we can fix "
            "most problems in a single visit without ordering parts.</p>"
            "<h2>All Refrigerator Types</h2>"
            "<p>We repair all refrigerator types: French door, side-by-side, "
            "top-freezer, bottom-freezer, built-in, counter-depth, and commercial "
            "refrigeration units. Whether it's a residential kitchen fridge or a "
            "walk-in cooler for your restaurant, our technicians have the training "
            "and parts to get it running again.</p>"
            "<h2>Transparent Pricing, No Surprises</h2>"
            "<p>Our diagnostic service call fee is waived when you approve the "
            "repair. You'll receive a complete quote before any work begins — "
            "no hidden charges, no surprises. Every repair is backed by our "
            "parts and labor warranty for your peace of mind.</p>"
        ),
        "problems": [
            "Refrigerator not cooling or warm inside",
            "Freezer works but fridge is warm",
            "Ice maker not producing ice",
            "Water leaking on the floor",
            "Strange humming or clicking noises",
            "Refrigerator running constantly",
            "Frost buildup inside the fridge",
            "Water dispenser not working",
            "Temperature fluctuations",
            "Refrigerator door not sealing",
            "Condenser coils freezing up",
            "Control panel unresponsive",
        ],
        "benefits": [
            (
                "Same-Day Repair",
                "Most refrigerator repairs completed the same day you call. No waiting for parts or second visits.",
            ),
            (
                "All Major Brands",
                "Factory-trained on Samsung, LG, Whirlpool, GE, Sub-Zero, Viking, KitchenAid, and more.",
            ),
            (
                "OEM Parts In-Stock",
                "Fully stocked trucks with genuine manufacturer parts for compressors, thermostats, and control boards.",
            ),
            (
                "Warranty Included",
                "Every refrigerator repair backed by our comprehensive parts and labor warranty.",
            ),
        ],
        "faq": [
            (
                "Why is my refrigerator not cooling?",
                "The most common causes are a dirty condenser coil, a faulty evaporator fan motor, a malfunctioning thermostat, or a refrigerant leak. Our technician will diagnose the exact issue and provide a repair quote before starting any work.",
            ),
            (
                "How much does refrigerator repair cost?",
                "Refrigerator repair costs vary depending on the issue. Our diagnostic fee is waived with repair approval. Common fixes like thermostat replacement or fan motor repair typically cost less than buying a new fridge — and we always quote before starting.",
            ),
            (
                "Is it worth repairing an old refrigerator?",
                "If your refrigerator is under 10-12 years old and the repair cost is less than half the price of a new unit, repair is usually the better value. We'll give you an honest recommendation based on the diagnosis.",
            ),
            (
                "How long does refrigerator repair take?",
                "Most refrigerator repairs take 1-2 hours. We carry common parts on our trucks so the majority of repairs are completed in a single visit. Complex compressor replacements may take slightly longer.",
            ),
            (
                "Do you repair built-in and Sub-Zero refrigerators?",
                "Yes, we service all refrigerator types including built-in, Sub-Zero, Viking, and Thermador units. Our technicians are factory-trained on premium brands and carry specialized parts.",
            ),
            (
                "My ice maker stopped working. Can you fix it?",
                "Ice maker issues are one of our most common repairs. Whether it's not producing ice, making small or hollow cubes, or leaking, we diagnose and fix the root cause — often in under an hour.",
            ),
        ],
        "related": ["freezer-repair", "dishwasher-repair"],
    },
    {
        "title": "Freezer Repair",
        "slug": "freezer-repair",
        "seo_title": "Freezer Repair — Same-Day Service, All Brands",
        "search_description": (
            "Professional freezer repair — same-day service for all brands. "
            "Fix temperature issues, frost buildup & compressor problems. "
            "Warranty included."
        ),
        "intro": (
            "Professional freezer repair for standalone and built-in units — "
            "same-day service, all brands"
        ),
        "short_description": "Restore proper freezing and stop ice buildup.",
        "hero_usp": (
            "Same-day freezer repair — chest freezers, upright freezers, "
            "and commercial units."
        ),
        "body": (
            "<h2>Fast, Reliable Freezer Repair</h2>"
            "<p>When your freezer stops working, every hour counts. Thawing food "
            "means wasted groceries and potential health risks. Our certified "
            "technicians provide same-day freezer repair for all types — chest "
            "freezers, upright freezers, drawer freezers, and commercial walk-in "
            "units. We arrive with fully stocked trucks to fix most problems in "
            "a single visit.</p>"
            "<h2>What Causes Freezer Problems?</h2>"
            "<p>Freezer issues typically stem from compressor failure, thermostat "
            "malfunctions, sealed system leaks, defrost timer problems, or "
            "evaporator fan motor failures. Ice buildup often indicates a defrost "
            "system issue, while a warm freezer usually points to a compressor or "
            "refrigerant problem. Our technicians use professional diagnostic tools "
            "to pinpoint the exact cause.</p>"
            "<h2>Residential & Commercial Freezer Service</h2>"
            "<p>We repair residential freezers of all sizes as well as commercial "
            "freezer units for restaurants, grocery stores, and medical facilities. "
            "Our technicians are trained on all major brands including GE, "
            "Frigidaire, Whirlpool, Samsung, LG, and Sub-Zero. Every repair "
            "comes with a warranty on parts and labor.</p>"
        ),
        "problems": [
            "Freezer not freezing or too warm",
            "Excessive frost or ice buildup",
            "Freezer running but not cold enough",
            "Water pooling at the bottom",
            "Unusual buzzing or clicking sounds",
            "Freezer runs constantly",
            "Door seal not closing properly",
            "Freezer temperature fluctuating",
            "Frost on outside walls",
            "Food thawing unexpectedly",
        ],
        "benefits": [
            (
                "Emergency Service",
                "Same-day freezer repair to prevent food loss. We understand the urgency of a broken freezer.",
            ),
            (
                "All Freezer Types",
                "Chest freezers, upright, drawer, built-in, and commercial walk-in units — we repair them all.",
            ),
            (
                "Diagnostic Accuracy",
                "Professional tools to pinpoint compressor, thermostat, and sealed system issues on the first visit.",
            ),
            (
                "Warranty Protection",
                "All freezer repairs backed by our parts and labor warranty for lasting peace of mind.",
            ),
        ],
        "faq": [
            (
                "Why is my freezer not freezing?",
                "Common causes include a faulty compressor, low refrigerant, a broken thermostat, or a blocked evaporator fan. Our technician will run diagnostics and provide a transparent quote before starting any repair.",
            ),
            (
                "What causes excessive frost buildup?",
                "Frost buildup is usually caused by a malfunctioning defrost timer, heater, or thermostat. A damaged door gasket that lets warm air in can also cause frost. We repair the defrost system to eliminate ice buildup.",
            ),
            (
                "How often should a freezer be serviced?",
                "Freezers generally don't need regular servicing, but cleaning condenser coils every 6-12 months helps efficiency. If you notice temperature changes, unusual noises, or frost buildup, call for a diagnostic before the problem worsens.",
            ),
            (
                "Can you repair a commercial walk-in freezer?",
                "Yes, we service commercial walk-in freezers and coolers. Our technicians carry parts for commercial compressors, evaporators, and control systems. We offer priority scheduling for businesses.",
            ),
            (
                "Is it cheaper to repair or replace a freezer?",
                "If your freezer is under 10 years old and the repair costs less than 50% of replacement, repair is typically the better value. We always provide an honest recommendation after diagnosis.",
            ),
        ],
        "related": ["refrigerator-repair", "air-conditioning-repair-hvac"],
    },
    {
        "title": "Washer Repair",
        "slug": "washer-repair",
        "seo_title": "Washer Repair — Same-Day Service, All Brands",
        "search_description": (
            "Professional washer repair — same-day service for all brands. "
            "Fix leaks, spinning issues, drainage & error codes. "
            "Warranty included."
        ),
        "intro": (
            "Expert washing machine repair — fix leaks, spinning issues, "
            "and drainage problems same-day"
        ),
        "short_description": "Fix leaks, spinning issues, and drainage problems.",
        "hero_usp": (
            "Same-day washer repair for top-load, front-load, and commercial machines."
        ),
        "body": (
            "<h2>Professional Washing Machine Repair</h2>"
            "<p>A broken washing machine disrupts your entire household. "
            "Piles of dirty laundry, trips to the laundromat, and the stress "
            "of unexpected repair costs — we get it. Our certified technicians "
            "provide same-day washer repair for all brands including Samsung, "
            "LG, Whirlpool, Maytag, GE, Kenmore, Bosch, and Speed Queen.</p>"
            "<h2>Top-Load & Front-Load Expertise</h2>"
            "<p>We repair all washer types: top-load agitator models, high-efficiency "
            "top-load, front-load washers, stackable units, and commercial laundry "
            "machines. Each type has unique components and failure patterns — our "
            "technicians are trained on the specific mechanics of each design.</p>"
            "<h2>Common Washer Problems We Solve</h2>"
            "<p>From a washer that won't drain or spin to one that's leaking water "
            "all over your floor, we handle it all. Error codes, lid switch failures, "
            "control board issues, pump replacements, bearing repairs, and belt "
            "replacements are all within our expertise. We carry common washer "
            "parts on our trucks for first-visit fixes.</p>"
            "<h2>Built to Last</h2>"
            "<p>We use genuine OEM parts and professional-grade techniques to ensure "
            "your washer repair lasts. Every repair is backed by our warranty "
            "on parts and labor — if something goes wrong within the warranty "
            "period, we'll fix it at no additional cost.</p>"
        ),
        "problems": [
            "Washer won't drain water",
            "Washer not spinning or agitating",
            "Washer leaking water on the floor",
            "Loud banging or vibrating during spin",
            "Error codes on display panel",
            "Washer won't start or turn on",
            "Clothes still wet after spin cycle",
            "Washer fills with water but doesn't wash",
            "Burning smell during operation",
            "Door or lid won't lock",
            "Washer overflowing",
            "Detergent not dispensing",
        ],
        "benefits": [
            (
                "All Washer Types",
                "Top-load, front-load, stackable, HE, and commercial — we fix every kind of washing machine.",
            ),
            (
                "Same-Day Service",
                "Most washer repairs completed the same day. No more trips to the laundromat.",
            ),
            (
                "OEM Parts",
                "Genuine manufacturer parts for Samsung, LG, Whirlpool, Maytag, GE, and all major brands.",
            ),
            (
                "Warranty Included",
                "Every washer repair backed by our comprehensive parts and labor warranty.",
            ),
        ],
        "faq": [
            (
                "Why won't my washer drain?",
                "A washer that won't drain is usually caused by a clogged drain pump, blocked drain hose, or faulty lid switch (top-load) or door latch (front-load). Our technician will diagnose the issue and clear the blockage or replace the component.",
            ),
            (
                "Why is my washing machine leaking?",
                "Leaks can come from a damaged door boot seal (front-load), worn tub-to-pump hose, loose connections, or a cracked tub. The location of the leak helps identify the cause — we'll pinpoint and fix it on the spot.",
            ),
            (
                "How much does washer repair typically cost?",
                "Washer repair costs depend on the issue and parts needed. Our diagnostic fee is waived with repair approval. Common repairs like pump or belt replacement are significantly cheaper than buying a new machine.",
            ),
            (
                "My washer is shaking violently during spin. What's wrong?",
                "Violent shaking is usually caused by worn shock absorbers (front-load) or suspension rods (top-load), an unbalanced load, or worn drum bearings. We replace the worn components to restore smooth, quiet operation.",
            ),
            (
                "Can you fix error codes on Samsung/LG washers?",
                "Yes, we're factory-trained on Samsung and LG error code diagnostics. Common codes like UE (unbalanced), OE (drain error), and DE (door error) all point to specific components we can repair or replace.",
            ),
            (
                "Is it worth repairing an old washing machine?",
                "If your washer is under 8-10 years old and the repair costs less than 50% of a new machine, repair is usually the smart choice. We'll give you an honest assessment after diagnosis.",
            ),
        ],
        "related": ["dryer-repair", "dishwasher-repair"],
    },
    {
        "title": "Dryer Repair",
        "slug": "dryer-repair",
        "seo_title": "Dryer Repair — Same-Day Service, All Brands",
        "search_description": (
            "Professional dryer repair — same-day service for all brands. "
            "Fix no-heat, tumbling, and ventilation issues. "
            "Gas & electric dryers. Warranty included."
        ),
        "intro": (
            "Professional dryer repair for gas and electric units — "
            "restore heat and proper drying same-day"
        ),
        "short_description": "Restore heat and proper drying cycles.",
        "hero_usp": (
            "Same-day dryer repair — gas and electric, "
            "all brands, residential and commercial."
        ),
        "body": (
            "<h2>Expert Dryer Repair Service</h2>"
            "<p>When your dryer stops heating, takes forever to dry clothes, or "
            "won't tumble, you need fast, reliable service. Our certified "
            "technicians repair both gas and electric dryers — all brands, all "
            "models. Most repairs are completed the same day with parts from our "
            "fully stocked trucks.</p>"
            "<h2>Gas & Electric Dryer Specialists</h2>"
            "<p>Gas dryers and electric dryers have different heating systems "
            "and require specialized knowledge. Our technicians are trained on "
            "both types: gas valve assemblies, igniter systems, and flame sensors "
            "for gas dryers; heating elements, thermal fuses, and thermostats "
            "for electric models. We handle it all safely and efficiently.</p>"
            "<h2>Don't Ignore Dryer Warning Signs</h2>"
            "<p>A dryer that takes multiple cycles to dry, smells like burning, "
            "or gets excessively hot is not just inconvenient — it's a fire hazard. "
            "Lint buildup, blocked vents, and faulty thermostats are leading causes "
            "of dryer fires. We inspect and address these safety concerns during "
            "every repair visit.</p>"
            "<h2>All Brands, All Types</h2>"
            "<p>We service Samsung, LG, Whirlpool, Maytag, GE, Kenmore, Bosch, "
            "Speed Queen, and all other major brands. Whether it's a stackable "
            "unit, a ventless condenser dryer, or a commercial tumble dryer, "
            "our technicians have the expertise and parts.</p>"
        ),
        "problems": [
            "Dryer not heating (gas or electric)",
            "Dryer takes too long to dry clothes",
            "Dryer won't start or turn on",
            "Dryer not tumbling or drum not spinning",
            "Burning smell from dryer",
            "Dryer overheating or getting too hot",
            "Dryer making squeaking or grinding noises",
            "Dryer shuts off mid-cycle",
            "Clothes still damp after full cycle",
            "Dryer vent clogged or restricted",
            "Gas dryer igniter not glowing",
            "Timer or control board not working",
        ],
        "benefits": [
            (
                "Gas & Electric",
                "Specialized in both gas valve systems and electric heating elements. Safe, professional repair.",
            ),
            (
                "Fire Safety",
                "We inspect for lint buildup and blocked vents — a leading cause of dryer fires — during every service call.",
            ),
            (
                "Fast Turnaround",
                "Most dryer repairs completed in 1-2 hours with parts from our fully stocked service trucks.",
            ),
            (
                "Warranty Backed",
                "All dryer repairs covered by our warranty on both parts and labor.",
            ),
        ],
        "faq": [
            (
                "Why is my dryer not heating?",
                "For electric dryers, the most common causes are a blown thermal fuse, faulty heating element, or broken thermostat. For gas dryers, it's usually a faulty igniter, gas valve solenoid, or flame sensor. We diagnose and replace the specific component.",
            ),
            (
                "Why does my dryer take so long to dry?",
                "Long dry times are typically caused by a clogged lint filter, blocked vent duct, worn drum seals letting heat escape, or a failing heating element. We check all of these during diagnosis and fix the root cause.",
            ),
            (
                "Is a burning smell from my dryer dangerous?",
                "Yes — a burning smell can indicate lint buildup near the heating element, a worn belt, or a failing motor. Turn off the dryer immediately and call for service. These issues can be fire hazards if left unaddressed.",
            ),
            (
                "How much does dryer repair cost?",
                "Dryer repair costs vary by issue. Common repairs like thermal fuse or heating element replacement are very affordable. Our diagnostic fee is waived when you approve the repair, and you'll always get a quote before we start.",
            ),
            (
                "Can you fix a gas dryer that clicks but won't ignite?",
                "Yes, this is typically a faulty igniter or gas valve solenoid — both common parts we carry on our trucks. We can usually repair this in under an hour.",
            ),
            (
                "Should I clean my dryer vent?",
                "Yes, dryer vents should be cleaned annually. Clogged vents reduce efficiency, increase energy costs, and are a leading cause of house fires. We can inspect and advise during any service call.",
            ),
        ],
        "related": ["washer-repair", "oven-repair"],
    },
    {
        "title": "Dishwasher Repair",
        "slug": "dishwasher-repair",
        "seo_title": "Dishwasher Repair — Same-Day Service, All Brands",
        "search_description": (
            "Professional dishwasher repair — same-day service for all brands. "
            "Fix drainage, cleaning, door latch & leak issues. "
            "Warranty included."
        ),
        "intro": (
            "Professional dishwasher repair — fix drainage, cleaning, "
            "and leak issues same-day with warranty"
        ),
        "short_description": "Fix cleaning, draining, and door issues.",
        "hero_usp": (
            "Same-day dishwasher repair — built-in, portable, and commercial units."
        ),
        "body": (
            "<h2>Reliable Dishwasher Repair Service</h2>"
            "<p>A dishwasher that doesn't clean, won't drain, or leaks water "
            "is more than an inconvenience — it can damage your kitchen floor "
            "and cabinets. Our certified technicians diagnose and repair all "
            "dishwasher brands and models, typically on the same day you call.</p>"
            "<h2>We Fix What Others Can't</h2>"
            "<p>From simple fixes like a clogged spray arm to complex issues "
            "like a faulty control board or pump motor replacement, our "
            "technicians handle every level of dishwasher repair. We service "
            "Bosch, Samsung, LG, Whirlpool, KitchenAid, GE, Maytag, Miele, "
            "and all other major brands.</p>"
            "<h2>Common Dishwasher Problems</h2>"
            "<p>Dishes coming out dirty, standing water at the bottom, the "
            "door not latching, error codes flashing, or a dishwasher that "
            "won't start — these are all issues we solve daily. Most problems "
            "trace back to a faulty drain pump, wash motor, water inlet valve, "
            "or control module — all parts we carry on our trucks.</p>"
            "<h2>Professional Installation Support</h2>"
            "<p>Beyond repair, we can help with dishwasher installation, "
            "water line connections, and drain hookups. If your current dishwasher "
            "is beyond repair, we'll give you an honest recommendation and can "
            "help install your replacement unit.</p>"
        ),
        "problems": [
            "Dishwasher not cleaning dishes properly",
            "Dishwasher won't drain — standing water",
            "Dishwasher leaking water on the floor",
            "Dishwasher won't start or turn on",
            "Door latch not closing or locking",
            "Dishwasher making grinding or humming noises",
            "Dishes still wet after drying cycle",
            "Error codes on display panel",
            "Detergent dispenser not opening",
            "Dishwasher smells bad",
            "Water not filling or filling slowly",
            "Spray arms not spinning",
        ],
        "benefits": [
            (
                "All Brands",
                "Factory-trained on Bosch, Samsung, LG, Whirlpool, KitchenAid, Miele, and all major brands.",
            ),
            (
                "Quick Diagnosis",
                "Most dishwasher issues diagnosed in under 30 minutes with our professional tools.",
            ),
            (
                "Parts On Hand",
                "Drain pumps, wash motors, inlet valves, and control boards carried on our trucks.",
            ),
            (
                "Clean Work",
                "We protect your kitchen flooring and clean up completely after every repair.",
            ),
        ],
        "faq": [
            (
                "Why is my dishwasher not cleaning well?",
                "Poor cleaning is usually caused by clogged spray arms, a faulty wash motor, low water temperature, or a malfunctioning detergent dispenser. We check all components and fix the root cause.",
            ),
            (
                "Why won't my dishwasher drain?",
                "A dishwasher that won't drain usually has a clogged drain pump, blocked drain hose, or failed check valve. We clear blockages and replace failed components to restore proper drainage.",
            ),
            (
                "How much does dishwasher repair cost?",
                "Dishwasher repair costs depend on the specific issue. Our diagnostic fee is waived when you approve the repair. Common fixes like pump or valve replacement are much cheaper than buying a new unit.",
            ),
            (
                "My Bosch dishwasher shows an E24 error. What does it mean?",
                "The E24 error on Bosch dishwashers indicates a drain issue. It's typically caused by a kinked drain hose, clogged filter, or faulty drain pump. We diagnose and fix Bosch-specific error codes regularly.",
            ),
            (
                "Is it worth repairing a dishwasher?",
                "If your dishwasher is under 7-10 years old and the repair costs less than half the price of replacement, repair is usually the better value. We'll give you an honest recommendation after diagnosing the issue.",
            ),
        ],
        "related": ["refrigerator-repair", "washer-repair"],
    },
    {
        "title": "Oven Repair",
        "slug": "oven-repair",
        "seo_title": "Oven Repair — Same-Day Service, All Brands",
        "search_description": (
            "Professional oven repair — same-day service for gas & electric ovens. "
            "Fix heating, temperature & ignition issues. "
            "All brands. Warranty included."
        ),
        "intro": (
            "Expert oven repair for gas and electric models — "
            "restore proper heating and temperature control same-day"
        ),
        "short_description": "Restore proper heating and temperature control.",
        "hero_usp": (
            "Same-day oven repair — gas, electric, convection, wall ovens, and ranges."
        ),
        "body": (
            "<h2>Professional Oven Repair Service</h2>"
            "<p>When your oven isn't heating properly, cooks unevenly, or won't "
            "turn on at all, meal preparation grinds to a halt. Our certified "
            "technicians repair all oven types — gas, electric, convection, "
            "double ovens, wall ovens, and ranges. Most repairs are completed "
            "the same day with parts from our service trucks.</p>"
            "<h2>Gas & Electric Oven Expertise</h2>"
            "<p>Gas ovens and electric ovens require different diagnostic "
            "approaches. For gas ovens, we troubleshoot igniters, gas valves, "
            "safety valves, and thermocouples. For electric ovens, we address "
            "heating elements (bake and broil), temperature sensors, relays, "
            "and control boards. Our technicians are certified on both types.</p>"
            "<h2>Precision Temperature Repair</h2>"
            "<p>An oven that runs too hot, too cold, or fluctuates in temperature "
            "ruins your cooking results. We calibrate temperature sensors, replace "
            "faulty thermostats, and test heating elements to ensure your oven "
            "reaches and maintains the exact temperature you set — every time.</p>"
            "<h2>All Major Brands</h2>"
            "<p>We service GE, Whirlpool, Samsung, LG, KitchenAid, Frigidaire, "
            "Bosch, Viking, Wolf, Thermador, and all other major brands. "
            "From standard home ovens to premium built-in units, our technicians "
            "have the training and parts to handle any repair.</p>"
        ),
        "problems": [
            "Oven not heating up",
            "Oven temperature inaccurate",
            "Gas oven igniter not working",
            "Uneven cooking or hot spots",
            "Self-cleaning cycle not working",
            "Oven door won't close properly",
            "Broiler element not heating",
            "Oven takes too long to preheat",
            "Control panel or display not working",
            "Gas smell when oven is on",
            "Oven light not turning on",
            "Convection fan not running",
        ],
        "benefits": [
            (
                "Gas & Electric",
                "Certified on both gas ignition systems and electric heating elements for accurate, safe repairs.",
            ),
            (
                "Temperature Calibration",
                "We calibrate sensors and thermostats to ensure precise, consistent oven temperatures.",
            ),
            (
                "Premium Brands",
                "Trained on Viking, Wolf, Thermador, Sub-Zero, and other premium oven brands.",
            ),
            (
                "Safety First",
                "Gas oven repairs include safety leak testing to protect your home and family.",
            ),
        ],
        "faq": [
            (
                "Why won't my gas oven ignite?",
                "The most common cause is a faulty igniter — it glows but doesn't get hot enough to open the gas valve. Other causes include a failed gas valve, faulty safety valve, or wiring issue. We carry replacement igniters on our trucks.",
            ),
            (
                "Why is my oven not reaching the right temperature?",
                "Inaccurate temperatures usually point to a faulty temperature sensor, worn-out heating element, or a thermostat that needs calibration. We test and replace the specific component to restore accuracy.",
            ),
            (
                "Is it safe to use an oven that smells like gas?",
                "No — if you smell gas with the oven off, turn off the gas supply, ventilate the area, and call for service immediately. If you smell gas only briefly when the oven first ignites, that's usually normal for gas ovens.",
            ),
            (
                "Can you repair a double wall oven?",
                "Yes, we repair all wall oven configurations including single, double, and combination oven/microwave units. We service built-in ovens from all major brands.",
            ),
            (
                "How much does oven repair cost?",
                "Oven repair costs depend on the issue. Igniter replacement is one of the most affordable repairs. Our diagnostic fee is waived with repair approval, and you'll always receive a quote before we start work.",
            ),
        ],
        "related": ["stove-repair", "microwave-repair"],
    },
    {
        "title": "Stove Repair",
        "slug": "stove-repair",
        "seo_title": "Stove Repair — Same-Day Service, Gas & Electric",
        "search_description": (
            "Professional stove and cooktop repair — same-day service for "
            "gas & electric. Fix burners, ignition & heating elements. "
            "All brands."
        ),
        "intro": (
            "Professional stove and cooktop repair — "
            "fix burners, ignition, and heating elements same-day"
        ),
        "short_description": "Fix burners, ignition, and heating elements.",
        "hero_usp": (
            "Same-day stove repair — gas, electric, induction, and ceramic cooktops."
        ),
        "body": (
            "<h2>Expert Stove & Cooktop Repair</h2>"
            "<p>Whether it's a gas burner that won't light, an electric element "
            "that won't heat, or an induction cooktop showing error codes, "
            "our technicians fix it fast. We repair all stove and cooktop types "
            "including freestanding ranges, slide-in ranges, gas cooktops, "
            "electric cooktops, and induction units.</p>"
            "<h2>Gas Stove Specialists</h2>"
            "<p>Gas stove problems often involve igniter failures, clogged burner "
            "ports, faulty gas valves, or thermocouple issues. Our technicians "
            "safely diagnose gas flow problems, replace igniters and valves, "
            "clean burner assemblies, and test for gas leaks after every repair.</p>"
            "<h2>Electric & Induction Cooktops</h2>"
            "<p>Electric stoves can have failing coil elements, cracked ceramic "
            "surfaces, faulty infinite switches, or control board issues. Induction "
            "cooktops require specialized knowledge of magnetic field generators "
            "and power boards. We're trained on all three technologies.</p>"
            "<h2>All Brands Serviced</h2>"
            "<p>From GE and Whirlpool to Viking and Wolf, we service every major "
            "brand. Whether it's a basic apartment-style range or a professional "
            "6-burner gas cooktop, we have the expertise and parts to fix it.</p>"
        ),
        "problems": [
            "Gas burner won't ignite or light",
            "Electric element not heating",
            "Burner flame uneven or too low",
            "Clicking sound but no ignition",
            "Gas smell near the stove",
            "Induction cooktop error codes",
            "Cracked ceramic cooktop surface",
            "Temperature control not working",
            "Burner knobs broken or loose",
            "Stove sparking continuously",
        ],
        "benefits": [
            (
                "All Fuel Types",
                "Gas, electric, induction, and dual-fuel — we repair every type of stove and cooktop.",
            ),
            (
                "Gas Safety",
                "Certified gas repairs with leak testing after every service for your family's safety.",
            ),
            (
                "Surface Care",
                "Specialized tools and techniques for ceramic and glass cooktop repairs without damage.",
            ),
            (
                "All Brands",
                "From standard GE/Whirlpool ranges to premium Viking/Wolf cooktops — we fix them all.",
            ),
        ],
        "faq": [
            (
                "Why won't my gas burner light?",
                "Common causes include a clogged burner port (food debris), a faulty igniter switch, a misaligned burner cap, or a gas supply issue. We clean, adjust, or replace components as needed.",
            ),
            (
                "Why is my stove clicking but not igniting?",
                "Continuous clicking usually means the igniter spark module is receiving power but gas isn't reaching the burner. This can be a clogged port, faulty gas valve, or stuck igniter switch. We diagnose and fix the specific cause.",
            ),
            (
                "Can you fix a cracked glass cooktop?",
                "Cracked glass or ceramic cooktop surfaces need replacement rather than repair. We can source and install replacement tops for most brands, or advise if replacement is more cost-effective.",
            ),
            (
                "How much does stove repair cost?",
                "Stove repair costs vary by issue. Igniter and switch replacements are affordable fixes. Our diagnostic fee is waived with repair, and we always quote before starting work.",
            ),
            (
                "Do you repair induction cooktops?",
                "Yes, we repair induction cooktops from Bosch, Samsung, GE, and other brands. Common issues include power board failures, sensor errors, and coil problems.",
            ),
        ],
        "related": ["oven-repair", "microwave-repair"],
    },
    {
        "title": "Water Heater Repair",
        "slug": "water-heater-repair",
        "seo_title": "Water Heater Repair — Same-Day Service, Gas & Electric",
        "search_description": (
            "Professional water heater repair — same-day service for gas, "
            "electric & tankless units. Fix no hot water, leaks & pilot issues. "
            "Warranty included."
        ),
        "intro": (
            "Professional water heater repair — restore hot water fast "
            "with same-day gas and electric service"
        ),
        "short_description": "Restore hot water and fix leaks fast.",
        "hero_usp": (
            "Same-day water heater repair — tank, tankless, gas, and electric units."
        ),
        "body": (
            "<h2>Fast Water Heater Repair</h2>"
            "<p>No hot water? Lukewarm showers? A leaking tank? We provide "
            "same-day water heater repair for all types — conventional tank "
            "heaters (gas and electric), tankless water heaters, and hybrid "
            "heat pump units. Our technicians arrive with the parts and tools "
            "to restore your hot water quickly.</p>"
            "<h2>Gas & Electric Water Heaters</h2>"
            "<p>Gas water heater problems often involve pilot light failures, "
            "thermocouple issues, gas valve malfunctions, and sediment buildup. "
            "Electric models commonly have failed heating elements, tripped "
            "reset buttons, faulty thermostats, or corroded anode rods. We're "
            "certified to repair both types safely.</p>"
            "<h2>Tankless Water Heater Service</h2>"
            "<p>Tankless water heaters require specialized knowledge. We service "
            "all major brands including Rinnai, Navien, Noritz, Rheem, and "
            "Bosch. Common tankless issues include flow sensor problems, "
            "ignition failures, heat exchanger scaling, and error codes.</p>"
            "<h2>When to Repair vs. Replace</h2>"
            "<p>Tank water heaters typically last 8-12 years, while tankless "
            "units can last 15-20 years with proper maintenance. If your unit "
            "is leaking from the tank itself, replacement is usually necessary. "
            "For component failures (thermostats, elements, valves), repair is "
            "almost always the better value. We give honest recommendations.</p>"
        ),
        "problems": [
            "No hot water at all",
            "Water not getting hot enough",
            "Water heater leaking from the bottom",
            "Pilot light keeps going out",
            "Strange popping or rumbling noises",
            "Rusty or discolored hot water",
            "Water heater takes too long to heat",
            "Tankless water heater error codes",
            "Hot water runs out quickly",
            "Temperature and pressure relief valve leaking",
            "Water heater tripping breaker",
        ],
        "benefits": [
            (
                "All Types",
                "Tank, tankless, gas, electric, and hybrid heat pump water heaters — we repair them all.",
            ),
            (
                "Safety Certified",
                "Gas line work, pressure valve testing, and electrical connections handled by certified technicians.",
            ),
            (
                "Tankless Experts",
                "Specialized service for Rinnai, Navien, Noritz, and other tankless brands.",
            ),
            (
                "Honest Advice",
                "We'll tell you when repair makes sense and when replacement is the better investment.",
            ),
        ],
        "faq": [
            (
                "Why do I have no hot water?",
                "For gas heaters, check if the pilot light is on. Common causes include a faulty thermocouple, gas valve issue, or tripped safety switch. For electric units, it's usually a failed heating element or tripped reset button.",
            ),
            (
                "Why is my water heater leaking?",
                "Leaks from fittings or valves can usually be repaired. Leaks from the tank bottom indicate internal corrosion and typically require replacement. We'll diagnose the source and advise the best course of action.",
            ),
            (
                "How long should a water heater last?",
                "Tank water heaters typically last 8-12 years. Tankless units last 15-20 years with regular maintenance. Annual flushing to remove sediment can extend the life of any water heater significantly.",
            ),
            (
                "My tankless water heater shows an error code. What should I do?",
                "Error codes vary by brand. Common codes relate to ignition failure, flow sensor issues, or overheating. Don't try to reset repeatedly — call for professional diagnosis to avoid further damage.",
            ),
            (
                "How much does water heater repair cost?",
                "Water heater repair costs depend on the type and issue. Thermocouple and element replacements are affordable. Our diagnostic fee is waived when you approve the repair.",
            ),
        ],
        "related": ["air-conditioning-repair-hvac", "oven-repair"],
    },
    {
        "title": "AC Repair (HVAC)",
        "slug": "air-conditioning-repair-hvac",
        "seo_title": "AC Repair (HVAC) — Same-Day Service, All Brands",
        "search_description": (
            "Professional AC and HVAC repair — same-day service for central air, "
            "mini-splits & window units. Fix cooling, compressor & thermostat issues."
        ),
        "intro": (
            "Professional AC and HVAC repair — restore cooling fast "
            "with same-day service and warranty"
        ),
        "short_description": "Fix cooling problems and improve efficiency.",
        "hero_usp": (
            "Same-day AC repair — central air, mini-splits, "
            "and window units for home and business."
        ),
        "body": (
            "<h2>Expert Air Conditioning Repair</h2>"
            "<p>When your AC stops cooling in the middle of a heat wave, you need "
            "fast, reliable service. Our certified HVAC technicians provide "
            "same-day air conditioning repair for residential and commercial "
            "systems. We service central air conditioners, ductless mini-splits, "
            "window units, and heat pumps from all major brands.</p>"
            "<h2>Central Air & Mini-Split Systems</h2>"
            "<p>Central AC problems often stem from refrigerant leaks, compressor "
            "failures, dirty evaporator coils, faulty capacitors, or thermostat "
            "issues. Mini-split systems can develop inverter board failures, "
            "refrigerant issues, or drainage problems. We're trained on both "
            "system types and carry the parts to fix most issues in one visit.</p>"
            "<h2>Energy Efficiency Matters</h2>"
            "<p>An AC system that's not running efficiently wastes energy and "
            "money. Dirty coils, low refrigerant, and worn capacitors force your "
            "system to work harder, driving up electric bills. Our tune-up and "
            "repair service restores your system to peak efficiency, keeping "
            "you cool while saving on energy costs.</p>"
            "<h2>Brands We Service</h2>"
            "<p>We service Carrier, Lennox, Trane, Goodman, Rheem, Daikin, "
            "Mitsubishi, Fujitsu, LG, Samsung, and all other major HVAC brands. "
            "From a simple capacitor replacement to a full compressor swap, "
            "our technicians handle it all.</p>"
        ),
        "problems": [
            "AC not cooling or blowing warm air",
            "AC not turning on",
            "Uneven cooling in different rooms",
            "AC making loud or unusual noises",
            "AC unit leaking water inside",
            "Thermostat not responding",
            "AC short cycling (turning on/off rapidly)",
            "Frozen evaporator coils",
            "High energy bills from AC",
            "Bad odor from AC vents",
            "AC compressor not engaging",
            "Mini-split not heating or cooling",
        ],
        "benefits": [
            (
                "All System Types",
                "Central air, mini-splits, window units, and heat pumps — residential and commercial.",
            ),
            (
                "Certified HVAC Techs",
                "EPA-certified technicians trained on refrigerant handling and HVAC diagnostics.",
            ),
            (
                "Efficiency Focus",
                "We restore peak efficiency to lower your energy bills along with fixing the immediate issue.",
            ),
            (
                "Emergency Service",
                "Same-day AC repair because we know comfort can't wait in extreme heat.",
            ),
        ],
        "faq": [
            (
                "Why is my AC blowing warm air?",
                "Common causes include low refrigerant from a leak, a dirty air filter restricting airflow, a faulty compressor, or a bad capacitor. We diagnose the root cause and fix it — not just the symptom.",
            ),
            (
                "How often should I service my AC?",
                "Professional AC maintenance should be done annually, ideally in spring before the cooling season. Regular maintenance prevents breakdowns, improves efficiency, and extends the life of your system.",
            ),
            (
                "Why is my AC leaking water inside?",
                "Indoor AC leaks are usually caused by a clogged condensate drain line, a dirty evaporator coil, or a cracked drain pan. We clear blockages and repair or replace damaged components.",
            ),
            (
                "How much does AC repair cost?",
                "AC repair costs vary widely depending on the issue. Capacitor replacement is affordable; compressor replacement is more involved. Our diagnostic fee is waived with repair approval, and we always quote before starting.",
            ),
            (
                "Should I repair or replace my AC unit?",
                "If your AC is over 15 years old, uses R-22 refrigerant (being phased out), or needs a compressor replacement, a new unit may be more cost-effective long-term. We'll give you an honest recommendation.",
            ),
            (
                "Do you service ductless mini-split systems?",
                "Yes, we service all ductless mini-split brands including Mitsubishi, Daikin, Fujitsu, LG, and Samsung. We handle inverter board repairs, refrigerant recharging, and drainage issues.",
            ),
        ],
        "related": ["water-heater-repair", "freezer-repair"],
    },
    {
        "title": "Microwave Repair",
        "slug": "microwave-repair",
        "seo_title": "Microwave Repair — Same-Day Service, All Brands",
        "search_description": (
            "Professional microwave repair — same-day service for built-in, "
            "over-the-range & countertop. Fix heating, turntable & door issues."
        ),
        "intro": (
            "Expert microwave repair for built-in, over-the-range, "
            "and countertop units — same-day service"
        ),
        "short_description": "Fix heating issues, turntable, and door problems.",
        "hero_usp": (
            "Same-day microwave repair — countertop, over-the-range, "
            "built-in, and drawer models."
        ),
        "body": (
            "<h2>Professional Microwave Repair</h2>"
            "<p>While countertop microwaves are often replaced, built-in, "
            "over-the-range, and microwave drawer units are expensive to replace "
            "and well worth repairing. Our technicians fix all types of microwaves "
            "from all major brands — Samsung, LG, Whirlpool, GE, KitchenAid, "
            "Bosch, and more.</p>"
            "<h2>Common Microwave Issues</h2>"
            "<p>Microwaves that don't heat, spark inside, have a dead control panel, "
            "or make unusual noises typically have problems with the magnetron, "
            "diode, door switch, capacitor, or control board. These are all "
            "components we diagnose and replace during our service visits.</p>"
            "<h2>Safety-First Approach</h2>"
            "<p>Microwaves contain high-voltage capacitors that store dangerous "
            "electrical charge even when unplugged. Never attempt to repair a "
            "microwave yourself. Our technicians are trained in safe microwave "
            "repair procedures, including proper capacitor discharge and "
            "high-voltage component handling.</p>"
            "<h2>Built-In & Over-The-Range Units</h2>"
            "<p>Built-in and over-the-range microwaves are integrated into your "
            "kitchen design and cost significantly more than countertop models. "
            "Repairing these units is almost always more cost-effective than "
            "replacement, especially when the issue is a common component "
            "like a magnetron or door switch.</p>"
        ),
        "problems": [
            "Microwave not heating food",
            "Microwave sparking inside",
            "Turntable not spinning",
            "Microwave won't turn on",
            "Door won't close or latch properly",
            "Control panel buttons not responding",
            "Microwave runs but doesn't heat",
            "Unusual buzzing or humming sounds",
            "Light inside not working",
            "Microwave shuts off mid-cycle",
        ],
        "benefits": [
            (
                "All Types",
                "Built-in, over-the-range, countertop, drawer, and commercial microwave repair.",
            ),
            (
                "High-Voltage Safety",
                "Certified technicians trained in safe capacitor discharge and high-voltage repair.",
            ),
            (
                "Cost Savings",
                "Repairing built-in and OTR microwaves costs a fraction of replacement — we keep your kitchen intact.",
            ),
            (
                "All Brands",
                "Samsung, LG, GE, Whirlpool, KitchenAid, Bosch, and all other major microwave brands.",
            ),
        ],
        "faq": [
            (
                "Why is my microwave not heating?",
                "The most common cause is a failed magnetron — the component that generates microwave energy. Other causes include a faulty diode, burned-out capacitor, or defective door switch. We diagnose and replace the specific failed component.",
            ),
            (
                "Is it worth repairing a microwave?",
                "For countertop microwaves under $200, replacement often makes more sense. For built-in, over-the-range, or microwave drawer units (which cost $500-$2000+), repair is almost always the better value.",
            ),
            (
                "Why is my microwave sparking?",
                "Sparking can be caused by metal or foil inside, a damaged waveguide cover, a worn-out rack support, or paint peeling inside the cavity. Some causes are simple fixes; others may need component replacement.",
            ),
            (
                "How much does microwave repair cost?",
                "Microwave repair costs depend on the issue and type. Door switch and turntable repairs are affordable. Magnetron replacement costs more but is still cheaper than replacing a built-in unit. We always quote before starting.",
            ),
            (
                "Can you fix an over-the-range microwave in place?",
                "Yes, in most cases we repair over-the-range microwaves without removing them from the wall mount. Only for major internal repairs might removal be necessary — and we handle that too.",
            ),
        ],
        "related": ["oven-repair", "stove-repair"],
    },
]


class Command(BaseCommand):
    help = "Sets up the complete page structure with SEO-optimized content"

    def handle(self, *args: object, **options: object) -> None:
        self.stdout.write("Setting up website pages...\n")

        if HomePage.objects.exists():
            self.stdout.write(
                self.style.SUCCESS(
                    "HomePage already exists — skipping setup to preserve data."
                )
            )
            return

        self.stdout.write("No HomePage found. Creating initial page structure...")

        # Remove Wagtail's default Welcome page
        Page.objects.filter(depth__gt=1).delete()
        root_page = Page.objects.get(depth=1)
        Page.fix_tree()
        root_page.refresh_from_db()

        # Home Page
        home_page = HomePage(title="Home", slug="home")
        root_page.add_child(instance=home_page)
        home_page.save_revision().publish()

        Site.objects.all().delete()
        Site.objects.create(
            hostname="localhost",
            port=8000,
            site_name="LOWL Appliance Repair",
            root_page=home_page,
            is_default_site=True,
        )
        self.stdout.write(self.style.SUCCESS(" + Home Page"))

        # Services
        services_index = ServicesIndexPage(
            title="Services",
            slug="services",
            hero_title="Appliance Repair Services",
            hero_subtitle="Expert repair for all major appliances. Fast, reliable, and affordable.",
        )
        home_page.add_child(instance=services_index)
        services_index.save_revision().publish()

        service_pages: dict[str, ServicePage] = {}

        for svc_data in SERVICE_CONTENT:
            svc = ServicePage(
                title=svc_data["title"],
                slug=svc_data["slug"],
                seo_title=svc_data["seo_title"],
                search_description=svc_data["search_description"],
                intro=svc_data["intro"],
                short_description=svc_data["short_description"],
                hero_usp=svc_data["hero_usp"],
                body=svc_data["body"],
                problems_we_fix=json.dumps(
                    [{"type": "problem", "value": p} for p in svc_data["problems"]]
                ),
                why_choose_us=json.dumps(
                    [
                        {
                            "type": "benefit",
                            "value": {"title": title, "description": desc},
                        }
                        for title, desc in svc_data["benefits"]
                    ]
                ),
                faq=json.dumps(
                    [
                        {
                            "type": "faq_item",
                            "value": {"question": q, "answer": a},
                        }
                        for q, a in svc_data["faq"]
                    ]
                ),
            )
            services_index.add_child(instance=svc)
            svc.save_revision().publish()
            service_pages[svc_data["slug"]] = svc
            self.stdout.write(f"   + {svc_data['title']}")

        # Related service links
        from services.models import ServiceRelatedService

        for svc_data in SERVICE_CONTENT:
            page = service_pages[svc_data["slug"]]
            for related_slug in svc_data.get("related", []):
                related_page = service_pages.get(related_slug)
                if related_page:
                    ServiceRelatedService.objects.create(
                        page=page, related_service=related_page
                    )

        self.stdout.write(self.style.SUCCESS(" + Service relationships created"))

        # Locations
        locations_index = LocationsIndexPage(
            title="Service Areas",
            slug="service-areas",
            intro="<p>We proudly serve Southern California with fast, reliable appliance repair.</p>",
        )
        home_page.add_child(instance=locations_index)
        locations_index.save_revision().publish()

        cities_data = [
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

        city_pages = []
        for city_name in cities_data:
            slug = f"appliance-repair-{city_name.lower().replace(' ', '-')}-ca"
            city = CityPage(
                title=city_name,
                slug=slug,
                intro=f"Same-day appliance repair in {city_name}, CA.",
                hero_usp=f"Fast, professional appliance repair in {city_name}.",
                state="CA",
            )
            locations_index.add_child(instance=city)
            city.save_revision().publish()
            city_pages.append(city)
            self.stdout.write(f"   + {city_name}")

        # Link cities to services and neighbors
        from locations.models import CityFeaturedService, CityNearbyCity

        for city in city_pages:
            for svc in service_pages.values():
                CityFeaturedService.objects.create(page=city, service=svc)

        for i, city in enumerate(city_pages):
            for j in range(1, 4):
                neighbor_idx = (i + j) % len(city_pages)
                if neighbor_idx != i:
                    CityNearbyCity.objects.create(
                        page=city, nearby_city=city_pages[neighbor_idx]
                    )

        self.stdout.write(self.style.SUCCESS(" + City relationships created"))

        # Static pages
        about_page = StaticPage(
            title="About Us",
            slug="about-us",
            seo_title="About Us — Certified Appliance Repair Technicians",
            search_description=(
                "Learn about our certified appliance repair team. "
                "Years of experience, all major brands, same-day service, "
                "and warranty-backed repairs."
            ),
            hero_title="About Us",
            hero_subtitle="Your trusted appliance repair experts.",
            body=(
                "<p>We specialize in residential and commercial appliance repair "
                "with a focus on quality, reliability, and customer satisfaction. "
                "Our certified technicians are factory-trained on all major brands "
                "and arrive with fully stocked trucks for same-day repairs.</p>"
                "<p>Every repair is backed by our parts and labor warranty — "
                "if something goes wrong within the warranty period, we fix it "
                "at no additional cost. We believe in transparent pricing, "
                "honest diagnostics, and repairs that last.</p>"
            ),
        )
        home_page.add_child(instance=about_page)
        about_page.save_revision().publish()
        self.stdout.write(self.style.SUCCESS(" + About Us"))

        contact_page = StaticPage(
            title="Contact",
            slug="contact",
            seo_title="Contact Us — Book Appliance Repair Today",
            search_description=(
                "Contact our appliance repair team. Same-day service available. "
                "Call, email, or fill out our contact form for a fast response."
            ),
            hero_title="Contact Us",
            hero_subtitle="We're here to help with all your appliance repair needs.",
            body="<p>Have questions? Fill out the form below or call us directly.</p>",
        )
        home_page.add_child(instance=contact_page)
        contact_page.save_revision().publish()
        self.stdout.write(self.style.SUCCESS(" + Contact"))

        # Blog
        blog_index = BlogIndexPage(
            title="Blog",
            slug="blog",
            hero_title="Our Blog",
            hero_subtitle="Tips, guides, and insights about appliance care and repair.",
        )
        home_page.add_child(instance=blog_index)
        blog_index.save_revision().publish()
        self.stdout.write(self.style.SUCCESS(" + Blog"))

        self.stdout.write(self.style.SUCCESS("\nAll pages created successfully!"))
        self.stdout.write("Site: http://localhost:8000/")
        self.stdout.write("Admin: http://localhost:8000/admin/")
