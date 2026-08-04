"""
Management command to create SEO-optimized blog posts for Inland Empire Appliance Repair.

Creates 15 high-quality blog posts targeting real search queries homeowners use.
Posts are idempotent — existing slugs are skipped on re-run.

Usage:
    python manage.py populate_blog_posts              # Publish all immediately
    python manage.py populate_blog_posts --schedule   # Schedule future posts
    python manage.py populate_blog_posts --interval 4 # 4 days between scheduled posts
"""

from __future__ import annotations

import logging
from datetime import date, timedelta
from typing import Any

from django.core.management.base import BaseCommand
from django.utils import timezone

from blog.content_utils import stream_body
from blog.models import BlogIndexPage, BlogPage

logger = logging.getLogger(__name__)

# ── Helper ────────────────────────────────────────────────────────────────

H = "heading"
P = "paragraph"


def _body(blocks: list[tuple[str, str]]) -> str:
    """Convert (type, value) tuples to StreamField JSON."""

    return stream_body(blocks)


# ── Blog Post Data ────────────────────────────────────────────────────────

BLOG_POSTS: list[dict[str, Any]] = [
    # ─── Post 1: Refrigerator Not Cooling ─────────────────────────────
    {
        "title": "Why Is My Refrigerator Not Cooling? 7 Causes and Fixes",
        "slug": "refrigerator-not-cooling-causes-fixes",
        "seo_title": "Refrigerator Not Cooling? 7 Causes & Fixes",
        "search_description": (
            "Refrigerator not cooling? Discover the 7 most common causes "
            "and when to call a pro. Same-day repair in the Inland Empire."
        ),
        "intro": (
            "If your refrigerator stopped cooling, don't panic. Here are "
            "the 7 most common causes and what you can do about each one."
        ),
        "author_name": "Inland Empire Appliance Repair",
        "tags": ["refrigerator", "troubleshooting", "cooling"],
        "body": [
            (H, "Why Your Refrigerator Stopped Cooling"),
            (
                P,
                "<p>A refrigerator not cooling is one of the most common — and most "
                "urgent — appliance problems homeowners face. When your fridge stops "
                "keeping food cold, you have a limited window before groceries spoil. "
                "The good news? Many cooling issues have straightforward causes that a "
                "professional technician can diagnose and fix the same day.</p>"
                "<p>Here are the seven most common reasons your refrigerator isn't "
                "cooling properly, what you can check yourself, and when it's time "
                "to call for professional appliance repair.</p>",
            ),
            (H, "1. Dirty Condenser Coils"),
            (
                P,
                "<p>The condenser coils — usually located behind or underneath your "
                "fridge — release heat from the refrigerant. When they're caked with "
                "dust, pet hair, or grease, your refrigerator can't dissipate heat "
                "efficiently and the compressor works overtime without cooling properly.</p>"
                "<p><strong>What to check:</strong> Pull the fridge away from the wall and "
                "inspect the coils. If they're visibly dirty, vacuum them with a brush "
                "attachment. Clean condenser coils every 6–12 months to prevent this issue.</p>",
            ),
            (H, "2. Faulty Evaporator Fan Motor"),
            (
                P,
                "<p>The evaporator fan circulates cold air from the freezer into the "
                "refrigerator compartment. If this fan motor fails, the freezer may stay "
                "cold while the fridge section gets warm — a classic symptom that points "
                "directly to this part.</p>"
                "<p><strong>What to check:</strong> Open the freezer and listen for the fan. "
                "If it's silent or making grinding noises, the motor likely needs replacement. "
                "This is a common repair that a technician can complete in under an hour.</p>",
            ),
            (H, "3. Defrost System Failure"),
            (
                P,
                "<p>Modern frost-free refrigerators use a defrost heater, defrost timer "
                "(or control board), and defrost thermostat to prevent ice buildup on the "
                "evaporator coils. When any of these components fail, ice accumulates on "
                "the coils and blocks airflow, causing your fridge to stop cooling.</p>"
                "<p><strong>Signs of defrost failure:</strong> Frost or ice buildup visible "
                "inside the freezer, a fridge that cycles between cooling and warming, or "
                "water pooling under the crisper drawers.</p>",
            ),
            (H, "4. Broken Condenser Fan Motor"),
            (
                P,
                "<p>The condenser fan (near the compressor at the bottom/back of the fridge) "
                "pulls air across the condenser coils and compressor to cool them down. If "
                "this fan fails, the compressor overheats and the refrigerant can't cool "
                "properly, resulting in a warm refrigerator.</p>"
                "<p><strong>What to check:</strong> Listen for the condenser fan running when "
                "the compressor kicks on. If you don't hear it, or it's making scraping "
                "sounds, it needs professional attention.</p>",
            ),
            (H, "5. Thermostat or Temperature Control Issues"),
            (
                P,
                "<p>The temperature control thermostat directs voltage to the compressor, "
                "evaporator fan, and condenser fan. If it's malfunctioning, it may not "
                "signal these components to run, leaving your fridge warm. Similarly, a "
                "faulty temperature sensor can send incorrect readings to the control board.</p>"
                "<p><strong>Quick test:</strong> Try adjusting the thermostat from the lowest "
                "to the highest setting. You should hear a click. If there's no click at "
                "any setting, the thermostat may be defective.</p>",
            ),
            (H, "6. Refrigerant Leak"),
            (
                P,
                "<p>Refrigerant is the chemical that absorbs heat from inside your fridge "
                "and releases it outside. A leak in the sealed system means your "
                "refrigerator gradually loses its ability to cool. This is less common "
                "than other causes but requires professional repair — refrigerant "
                "handling is regulated and requires EPA certification.</p>"
                "<p><strong>Signs of a leak:</strong> An oily residue near the compressor, "
                "a hissing or gurgling sound, or a fridge that cools less and less over "
                "several days despite the compressor running.</p>",
            ),
            (H, "7. Compressor Failure"),
            (
                P,
                "<p>The compressor is the heart of your refrigerator's cooling system. When "
                "it fails, there's no refrigeration at all. Compressor issues often present "
                "as the fridge running but not cooling, the compressor clicking on and off "
                "repeatedly, or complete silence from the unit.</p>"
                "<p>Compressor replacement is a significant repair, but for high-end "
                "refrigerators (Sub-Zero, Viking, etc.), it's often more cost-effective "
                "than replacing the entire unit.</p>",
            ),
            (H, "When to Call a Professional"),
            (
                P,
                "<p>While cleaning condenser coils and checking thermostat settings are "
                "safe DIY tasks, most refrigerator cooling issues require professional "
                "diagnosis and repair. Electrical components, sealed refrigerant systems, "
                "and compressor work all need a trained technician with the right tools "
                "and parts.</p>"
                "<p>If your refrigerator isn't cooling in the Inland Empire area, our "
                "technicians carry the most common replacement parts on our trucks for "
                "same-day repair — including evaporator fans, defrost components, "
                "thermostats, and condenser fan motors.</p>",
            ),
            (H, "Frequently Asked Questions"),
            (
                P,
                "<p><strong>How long can food last in a fridge that stopped cooling?</strong><br>"
                "The USDA recommends discarding perishable food that has been above 40°F "
                "for more than 2 hours. Keep the fridge door closed to maintain cold air "
                "as long as possible while waiting for repair.</p>"
                "<p><strong>Why is my freezer cold but my fridge is warm?</strong><br>"
                "This almost always points to a failed evaporator fan motor or a blocked "
                "air vent between the freezer and fridge compartments. The fan that "
                "circulates cold air into the fridge has stopped working.</p>"
                "<p><strong>Is it worth repairing an old refrigerator?</strong><br>"
                "If your fridge is under 10 years old and the repair costs less than "
                "half the price of a new one, repair is usually the smarter financial "
                "choice. Refrigerators over 15 years old may be more expensive to run "
                "even after repair due to lower energy efficiency.</p>",
            ),
        ],
    },
    # ─── Post 2: Dryer Not Heating ────────────────────────────────────
    {
        "title": "Dryer Not Heating? Here's What to Check First",
        "slug": "dryer-not-heating-what-to-check",
        "seo_title": "Dryer Not Heating? What to Check First",
        "search_description": (
            "Dryer not heating? Learn the top causes for gas and electric "
            "dryers and when you need professional repair. Inland Empire service."
        ),
        "intro": (
            "A dryer that tumbles but won't heat is one of the most common "
            "laundry appliance problems. Here's what's likely going on."
        ),
        "author_name": "Inland Empire Appliance Repair",
        "tags": ["dryer", "troubleshooting", "heating"],
        "body": [
            (H, "Why Your Dryer Runs But Doesn't Heat"),
            (
                P,
                "<p>When your dryer tumbles clothes but they come out damp and cold, "
                "the problem is almost always a failed heating component — not the "
                "motor or drum. The specific cause depends on whether you have a gas "
                "or electric dryer, but both types share some common failure points.</p>"
                "<p>Before calling for repair, there are a few things you can check "
                "yourself that might solve the problem without a service call.</p>",
            ),
            (H, "Check These First (Both Gas and Electric)"),
            (
                P,
                "<p><strong>Lint filter and exhaust vent:</strong> A clogged lint filter "
                "or blocked dryer vent is the #1 cause of poor drying performance. Remove "
                "the lint screen and clean it thoroughly. Then check the exhaust vent "
                "outside your home — if air flow is weak when the dryer runs, the vent "
                "duct may be clogged. Restricted airflow causes the dryer to overheat "
                "and trip safety devices that shut off the heat.</p>"
                "<p><strong>Circuit breaker (electric dryers):</strong> Electric dryers "
                "use a double-pole 240V breaker. If one half trips, the dryer motor runs "
                "(120V) but the heating element doesn't get power (240V). Check your "
                "breaker panel — flip the dryer breaker fully off, then back on.</p>"
                "<p><strong>Gas supply (gas dryers):</strong> Make sure the gas valve "
                "behind the dryer is fully open. If you recently had gas work done or "
                "moved the dryer, the valve may have been partially closed.</p>",
            ),
            (H, "Common Electric Dryer Heating Problems"),
            (
                P,
                "<p><strong>Blown thermal fuse:</strong> The thermal fuse is a safety "
                "device that cuts power to the heating element if the dryer overheats. "
                "Once blown, it doesn't reset — it must be replaced. A blown thermal "
                "fuse is the most common cause of an electric dryer not heating and "
                "is typically caused by a clogged vent.</p>"
                "<p><strong>Failed heating element:</strong> The heating element is a "
                "coil of resistance wire that glows red-hot when electricity flows "
                "through it. Over time, the coil can break or burn out. Replacement "
                "is a straightforward repair for a technician.</p>"
                "<p><strong>Faulty cycling thermostat:</strong> The cycling thermostat "
                "regulates the dryer temperature by turning the heating element on and "
                "off. If it fails in the open position, the element never turns on.</p>",
            ),
            (H, "Common Gas Dryer Heating Problems"),
            (
                P,
                "<p><strong>Faulty igniter:</strong> Gas dryers use a glow-bar igniter "
                "that heats up to open the gas valve and ignite the burner. If the "
                "igniter cracks or weakens, it can glow without getting hot enough "
                "to open the gas valve. You'll hear the dryer attempt to ignite "
                "(a brief humming sound) then give up.</p>"
                "<p><strong>Worn gas valve solenoids:</strong> These electromagnetic "
                "valves open to allow gas flow to the burner. They can fail "
                "intermittently — the dryer heats for a while, then stops mid-cycle. "
                "This is a telltale sign of solenoid failure.</p>"
                "<p><strong>Flame sensor failure:</strong> The flame sensor detects "
                "whether the igniter is hot enough before opening the gas valve. "
                "If it fails, the valve never opens, even with a working igniter.</p>",
            ),
            (H, "How to Tell If It's the Vent or a Part"),
            (
                P,
                "<p>A simple test: disconnect the dryer exhaust vent from the back of "
                "the dryer and run a short cycle. If the dryer heats normally with "
                "the vent disconnected, the vent duct is restricted and needs "
                "cleaning. If the dryer still doesn't heat, a component has failed "
                "and you need professional repair.</p>"
                "<p>Never run the dryer for extended periods with the vent "
                "disconnected — it fills your laundry room with hot, humid air "
                "(and combustion gases for gas dryers).</p>",
            ),
            (H, "Frequently Asked Questions"),
            (
                P,
                "<p><strong>Can a clogged dryer vent cause a fire?</strong><br>"
                "Yes. The U.S. Fire Administration reports that clogged dryer vents "
                "cause approximately 2,900 home fires each year. Annual vent cleaning "
                "is strongly recommended.</p>"
                "<p><strong>How much does dryer heating repair cost?</strong><br>"
                "Thermal fuse and thermostat replacements are among the most affordable "
                "appliance repairs. Heating element replacement is moderate. Gas valve "
                "solenoid replacement is also very reasonable. Our diagnostic fee is "
                "waived when you approve the repair.</p>"
                "<p><strong>Should I repair a dryer that's 10+ years old?</strong><br>"
                "Dryers are mechanically simpler than most appliances and can last "
                "15–20 years. If the drum, motor, and cabinet are in good shape, "
                "replacing a heating component is almost always worth it, even "
                "on an older dryer.</p>",
            ),
        ],
    },
    # ─── Post 3: Dishwasher Not Draining ──────────────────────────────
    {
        "title": "Dishwasher Not Draining? 5 Common Causes and Solutions",
        "slug": "dishwasher-not-draining-causes-solutions",
        "seo_title": "Dishwasher Not Draining? 5 Causes & Fixes",
        "search_description": (
            "Dishwasher not draining? Learn the 5 most common causes — "
            "from clogged filters to pump failures — and how to fix them."
        ),
        "intro": (
            "Standing water in the bottom of your dishwasher? Here are the "
            "5 most common reasons and how to get it draining again."
        ),
        "author_name": "Inland Empire Appliance Repair",
        "tags": ["dishwasher", "troubleshooting", "drainage"],
        "body": [
            (H, "Why Is There Standing Water in My Dishwasher?"),
            (
                P,
                "<p>A small amount of water in the bottom of your dishwasher is "
                "normal — it keeps the pump seals lubricated. But if you open the "
                "door and find several inches of dirty water that won't drain, "
                "something is preventing water from exiting the machine.</p>"
                "<p>Dishwasher drainage problems range from simple clogs you can "
                "fix yourself to pump failures that need professional repair. "
                "Here are the five most common causes, from easiest to most complex.</p>",
            ),
            (H, "1. Clogged Filter or Food Trap"),
            (
                P,
                "<p>Most modern dishwashers have a removable filter at the bottom of "
                "the tub. When food debris, grease, and sediment clog this filter, "
                "water can't reach the drain pump. This is the most common cause "
                "of dishwasher drainage issues and the easiest to fix.</p>"
                "<p><strong>Fix it yourself:</strong> Remove the bottom rack, locate "
                "the filter (usually a twist-and-pull cylinder), and clean it under "
                "running water with a soft brush. Clean the filter monthly to prevent "
                "buildup. Also check for broken glass or debris in the filter well.</p>",
            ),
            (H, "2. Garbage Disposal Connection Blocked"),
            (
                P,
                "<p>If your dishwasher drains through the garbage disposal (most do), "
                "a clogged disposal or a new disposal with the drain knockout plug "
                "still in place will prevent the dishwasher from draining.</p>"
                "<p><strong>Fix it yourself:</strong> Run the garbage disposal for "
                "15–20 seconds to clear any food buildup. If you recently installed "
                "a new garbage disposal, make sure the dishwasher drain knockout "
                "plug was removed during installation.</p>",
            ),
            (H, "3. Kinked or Clogged Drain Hose"),
            (
                P,
                "<p>The flexible drain hose connects your dishwasher to the garbage "
                "disposal or sink drain. Over time, this hose can kink (especially "
                "if the dishwasher was pushed back too far) or develop internal "
                "clogs from grease and food buildup.</p>"
                "<p><strong>What to check:</strong> Pull the dishwasher out enough to "
                "see the drain hose. Straighten any kinks. If the hose is visibly "
                "clogged or corroded, it should be replaced — a quick job for a "
                "professional.</p>",
            ),
            (H, "4. Faulty Check Valve"),
            (
                P,
                "<p>The check valve prevents drained water from flowing back into "
                "the dishwasher. When it sticks closed, water can't drain out. When "
                "it sticks open, dirty water flows back in. Both scenarios leave "
                "standing water in the tub.</p>"
                "<p>Check valve replacement is an affordable repair that's best "
                "handled by a professional since it involves accessing the drain "
                "pump assembly.</p>",
            ),
            (H, "5. Failed Drain Pump"),
            (
                P,
                "<p>The drain pump uses an impeller to force water out of the "
                "dishwasher. If the pump motor burns out or the impeller breaks, "
                "the dishwasher fills and washes but can't drain. You may hear "
                "a humming sound (the motor trying to run) or complete silence "
                "during the drain cycle.</p>"
                "<p>Drain pump replacement is a common repair that a technician "
                "can typically complete in one visit with parts on the truck.</p>",
            ),
            (H, "Prevent Future Drainage Problems"),
            (
                P,
                "<p>Scrape food off dishes before loading (no pre-rinsing needed). "
                "Clean the filter monthly. Run the garbage disposal before starting "
                "the dishwasher. Use a dishwasher cleaner monthly to break down grease "
                "buildup in the drain path. These simple habits prevent most "
                "dishwasher drainage issues.</p>",
            ),
            (H, "Frequently Asked Questions"),
            (
                P,
                "<p><strong>Can I use Drano in my dishwasher?</strong><br>"
                "No. Chemical drain cleaners can damage dishwasher components including "
                "the pump seals, hoses, and stainless steel interior. Use a dishwasher-"
                "specific cleaner or a vinegar rinse instead.</p>"
                "<p><strong>Why does my dishwasher drain but leave some water?</strong><br>"
                "A small amount of water (about a cup) in the filter well is normal — "
                "it keeps the pump seals from drying out. If there's significantly "
                "more, the drain path may be partially clogged.</p>"
                "<p><strong>How much does dishwasher drain pump repair cost?</strong><br>"
                "Drain pump replacement is a mid-range repair — significantly less "
                "than buying a new dishwasher. Our diagnostic fee is waived when you "
                "approve the repair, and you get a full quote before we start.</p>",
            ),
        ],
    },
    # ─── Post 4: Appliance Repair Cost Guide ──────────────────────────
    {
        "title": "How Much Does Appliance Repair Cost? 2026 Price Guide",
        "slug": "appliance-repair-cost-guide",
        "seo_title": "Appliance Repair Cost Guide (2026 Prices)",
        "search_description": (
            "How much does appliance repair cost in 2026? Average prices for "
            "refrigerator, washer, dryer, dishwasher, and oven repair."
        ),
        "intro": (
            "Wondering how much appliance repair costs? Here's a transparent "
            "guide to average repair prices for every major appliance."
        ),
        "author_name": "Inland Empire Appliance Repair",
        "tags": ["appliance-repair", "pricing", "guide"],
        "body": [
            (H, "What Does Appliance Repair Cost in 2026?"),
            (
                P,
                "<p>One of the first questions homeowners ask when an appliance breaks "
                'down is "how much will this cost to fix?" The answer depends on the '
                "appliance type, the specific problem, and the parts needed. This "
                "guide breaks down average appliance repair costs so you know what "
                "to expect before calling for service.</p>"
                "<p>Keep in mind that most reputable repair companies waive the "
                "diagnostic fee when you approve the repair — so the service call "
                "cost is typically rolled into the total repair price.</p>",
            ),
            (H, "Refrigerator Repair Costs"),
            (
                P,
                "<p>Refrigerators are the most commonly repaired appliance. Average "
                "repair costs range from $150 to $500 depending on the issue:</p>"
                "<ul>"
                "<li><strong>Thermostat or temperature sensor:</strong> $100–$250</li>"
                "<li><strong>Evaporator fan motor:</strong> $150–$300</li>"
                "<li><strong>Defrost system components:</strong> $200–$400</li>"
                "<li><strong>Compressor replacement:</strong> $400–$800</li>"
                "<li><strong>Ice maker repair:</strong> $150–$350</li>"
                "</ul>"
                "<p>Premium brands (Sub-Zero, Viking, Thermador) typically cost more "
                "due to specialized parts, but repair is still far cheaper than "
                "replacing these high-end units.</p>",
            ),
            (H, "Washer and Dryer Repair Costs"),
            (
                P,
                "<p>Laundry appliance repairs are generally among the most affordable:</p>"
                "<ul>"
                "<li><strong>Dryer thermal fuse:</strong> $100–$200</li>"
                "<li><strong>Dryer heating element:</strong> $150–$300</li>"
                "<li><strong>Washer pump replacement:</strong> $150–$350</li>"
                "<li><strong>Washer bearing replacement:</strong> $200–$450</li>"
                "<li><strong>Washer control board:</strong> $200–$400</li>"
                "</ul>"
                "<p>Dryers are mechanically simpler than washers and tend to have "
                "lower repair costs overall.</p>",
            ),
            (H, "Dishwasher Repair Costs"),
            (
                P,
                "<p>Dishwasher repairs are typically mid-range:</p>"
                "<ul>"
                "<li><strong>Drain pump replacement:</strong> $150–$300</li>"
                "<li><strong>Water inlet valve:</strong> $100–$250</li>"
                "<li><strong>Door latch assembly:</strong> $100–$200</li>"
                "<li><strong>Wash motor:</strong> $200–$400</li>"
                "<li><strong>Control board:</strong> $200–$400</li>"
                "</ul>",
            ),
            (H, "Oven and Stove Repair Costs"),
            (
                P,
                "<p>Oven and stove repairs vary significantly based on fuel type:</p>"
                "<ul>"
                "<li><strong>Gas igniter replacement:</strong> $150–$300</li>"
                "<li><strong>Electric bake/broil element:</strong> $150–$300</li>"
                "<li><strong>Temperature sensor:</strong> $100–$250</li>"
                "<li><strong>Gas valve:</strong> $200–$400</li>"
                "<li><strong>Control board:</strong> $250–$500</li>"
                "</ul>",
            ),
            (H, "Factors That Affect Repair Cost"),
            (
                P,
                "<p><strong>Brand:</strong> Premium brands cost more due to specialized "
                "or proprietary parts. Standard brands (Whirlpool, GE, Samsung) have "
                "widely available, affordable parts.</p>"
                "<p><strong>Part availability:</strong> If a part is in stock on the "
                "service truck, there's no delay or extra trip charge. If a part must "
                "be ordered, there may be a follow-up visit.</p>"
                "<p><strong>Warranty status:</strong> If your appliance is still under "
                "manufacturer warranty, parts (and sometimes labor) may be covered. "
                "Check your warranty before scheduling service.</p>"
                "<p><strong>Complexity:</strong> Simple component swaps (thermostats, "
                "fuses, sensors) cost less than sealed system work (compressor, "
                "refrigerant) that requires specialized equipment.</p>",
            ),
            (H, "Frequently Asked Questions"),
            (
                P,
                "<p><strong>Is a service call fee separate from the repair cost?</strong><br>"
                "Most companies charge a diagnostic/service call fee to cover the "
                "technician's time and travel. At Inland Empire Appliance Repair, we waive this fee when you "
                "approve the repair — so you only pay for the repair itself.</p>"
                "<p><strong>How do I know if repair is worth it vs. buying new?</strong><br>"
                "The general rule: if the repair costs more than 50% of a new "
                "appliance's price, and the appliance is more than 75% through its "
                "expected lifespan, replacement may be the better value. We always "
                "give honest recommendations.</p>"
                "<p><strong>Do you charge more for weekends or emergencies?</strong><br>"
                "We don't charge weekend surcharges — same rate 7 days a week, "
                "8 AM to 8 PM.</p>",
            ),
        ],
    },
    # ─── Post 5: Repair vs Replace ────────────────────────────────────
    {
        "title": "Should You Repair or Replace Your Appliance? Expert Guide",
        "slug": "repair-or-replace-appliance-guide",
        "seo_title": "Repair or Replace Your Appliance? Expert Guide",
        "search_description": (
            "Should you repair or replace your broken appliance? Use our "
            "expert guide with the 50% rule to make the right decision."
        ),
        "intro": (
            "When an appliance breaks, the big question is: fix it or buy new? "
            "Here's a clear framework to make the right call every time."
        ),
        "author_name": "Inland Empire Appliance Repair",
        "tags": ["appliance-repair", "cost-savings", "tips"],
        "body": [
            (H, "The Repair vs. Replace Decision"),
            (
                P,
                "<p>When a major appliance breaks down, you face a decision that "
                "can save — or waste — hundreds of dollars. Repair the existing "
                "unit, or invest in a brand-new replacement? There's no universal "
                "answer, but there is a clear framework that helps you decide "
                "based on facts, not frustration.</p>",
            ),
            (H, "The 50% Rule"),
            (
                P,
                "<p>The most widely used guideline in the appliance industry: "
                "<strong>if the repair costs more than 50% of the price of a new "
                "equivalent appliance, replacement is usually the better value.</strong> "
                "This accounts for the remaining useful life of the appliance and "
                "the risk of additional failures in an aging unit.</p>"
                "<p>For example, if a new dishwasher costs $600 and the repair "
                "estimate is $200, repair makes financial sense. If the repair "
                "is $400, it's worth considering a new unit.</p>",
            ),
            (H, "Average Appliance Lifespans"),
            (
                P,
                "<p>Understanding how long appliances typically last helps frame "
                "the repair decision:</p>"
                "<ul>"
                "<li><strong>Refrigerator:</strong> 10–18 years</li>"
                "<li><strong>Washing machine:</strong> 10–14 years</li>"
                "<li><strong>Dryer:</strong> 13–20 years</li>"
                "<li><strong>Dishwasher:</strong> 9–13 years</li>"
                "<li><strong>Oven/range:</strong> 13–20 years</li>"
                "<li><strong>Microwave:</strong> 9–12 years</li>"
                "<li><strong>Water heater (tank):</strong> 8–12 years</li>"
                "<li><strong>Water heater (tankless):</strong> 15–20 years</li>"
                "</ul>"
                "<p>If your appliance is within the first half of its expected "
                "lifespan, repair is almost always the right call.</p>",
            ),
            (H, "When Repair Is the Clear Winner"),
            (
                P,
                "<p><strong>Simple component failures:</strong> Thermostats, fuses, "
                "fan motors, door switches, and heating elements are affordable "
                "repairs with years of remaining life afterward.</p>"
                "<p><strong>High-end appliances:</strong> A Sub-Zero refrigerator or "
                "Viking range costs thousands to replace. Even a $500–$800 repair "
                "is a fraction of replacement cost for premium brands.</p>"
                "<p><strong>Recent purchase:</strong> An appliance that's 1–5 years "
                "old with a failed component is absolutely worth repairing. Check "
                "if it's still under manufacturer warranty first.</p>",
            ),
            (H, "When Replacement Makes More Sense"),
            (
                P,
                "<p><strong>Frequent breakdowns:</strong> If the same appliance has "
                "needed multiple repairs in the past year, the cumulative cost and "
                "inconvenience tip the scales toward replacement.</p>"
                "<p><strong>Obsolete refrigerant:</strong> Refrigerators and AC units "
                "using R-22 (Freon) face increasingly expensive refrigerant costs as "
                "the supply shrinks. Switching to a modern R-410A or R-454B system "
                "may be more economical long-term.</p>"
                "<p><strong>Energy efficiency:</strong> Appliances from 2005 or earlier "
                "use significantly more energy than modern ENERGY STAR models. The "
                "annual energy savings on a new refrigerator or washer can offset "
                "the purchase price over time.</p>",
            ),
            (H, "Frequently Asked Questions"),
            (
                P,
                "<p><strong>Will a repair technician give an honest recommendation?</strong><br>"
                "A reputable company earns more from your trust and repeat business "
                "than from a single repair. We always tell you when replacement is "
                "the smarter investment, even though we'd make more money on a repair.</p>"
                "<p><strong>Should I repair a discontinued appliance?</strong><br>"
                "Discontinued doesn't mean unrepairable. Parts for most appliances "
                "remain available for 10+ years after the model is discontinued. "
                "If parts are available and the repair makes financial sense, go for it.</p>"
                "<p><strong>Does repairing an appliance void the warranty?</strong><br>"
                "No, as long as a qualified technician performs the repair. In fact, "
                "many manufacturer warranties cover repairs by authorized service "
                "providers. Always check your warranty terms first.</p>",
            ),
        ],
    },
    # ─── Post 6: How to Clean Dryer Vent ──────────────────────────────
    {
        "title": "How to Clean Your Dryer Vent: Step-by-Step Safety Guide",
        "slug": "how-to-clean-dryer-vent-guide",
        "seo_title": "How to Clean Your Dryer Vent (Safety Guide)",
        "search_description": (
            "Learn how to clean your dryer vent step by step. Prevent fires, "
            "reduce energy bills, and improve dryer performance."
        ),
        "intro": (
            "A clogged dryer vent is a fire hazard and energy waster. "
            "Here's how to clean it yourself and when to call a pro."
        ),
        "author_name": "Inland Empire Appliance Repair",
        "tags": ["dryer", "maintenance", "safety", "cleaning"],
        "body": [
            (H, "Why Dryer Vent Cleaning Matters"),
            (
                P,
                "<p>According to the U.S. Fire Administration, clothes dryers cause "
                "an estimated 2,900 home fires each year, and the leading cause is "
                "failure to clean the dryer vent. Beyond fire safety, a clogged "
                "vent makes your dryer work harder, uses more energy, takes longer "
                "to dry clothes, and shortens the dryer's lifespan.</p>"
                "<p>Cleaning your dryer vent annually is one of the most important "
                "home maintenance tasks. Here's how to do it safely.</p>",
            ),
            (H, "Signs Your Dryer Vent Needs Cleaning"),
            (
                P,
                "<p>Watch for these warning signs that your dryer vent is clogged:</p>"
                "<ul>"
                "<li>Clothes take more than one cycle to dry</li>"
                "<li>The dryer feels excessively hot to the touch during operation</li>"
                "<li>A burning smell when the dryer is running</li>"
                "<li>The laundry room feels more humid than usual</li>"
                "<li>Lint is visible around the dryer door seal</li>"
                "<li>The outside vent flap doesn't open when the dryer runs</li>"
                "<li>It's been more than a year since the last cleaning</li>"
                "</ul>",
            ),
            (H, "Step-by-Step Dryer Vent Cleaning"),
            (
                P,
                "<p><strong>Step 1: Disconnect the dryer.</strong> Unplug the dryer from "
                "the electrical outlet. For gas dryers, turn off the gas valve behind "
                "the dryer. Pull the dryer away from the wall to access the vent "
                "connection.</p>"
                "<p><strong>Step 2: Disconnect the vent duct.</strong> Loosen the clamp "
                "or tape securing the vent duct to the back of the dryer. Carefully "
                "pull the duct free.</p>"
                "<p><strong>Step 3: Clean from the inside.</strong> Use a dryer vent "
                "cleaning brush kit (available at hardware stores for about $20–$30). "
                "Insert the flexible brush into the vent opening on the back of the "
                "dryer and rotate to remove lint buildup.</p>"
                "<p><strong>Step 4: Clean the duct.</strong> Push the brush through "
                "the vent duct itself, working from both ends. For long vent runs, "
                "you may need an extended brush kit or a leaf blower to push lint out.</p>"
                "<p><strong>Step 5: Clean the exterior vent.</strong> Go outside and "
                "clear lint from the exterior vent opening. Make sure the flap moves "
                "freely.</p>"
                "<p><strong>Step 6: Reconnect and test.</strong> Reattach the vent duct, "
                "push the dryer back into position, restore power/gas, and run the "
                "dryer for 10–15 minutes on air only (no heat) to blow out any "
                "remaining loose lint.</p>",
            ),
            (H, "When to Call a Professional"),
            (
                P,
                "<p>DIY cleaning works well for short, straight vent runs. But call a "
                "professional for vent cleaning if your duct has multiple bends or "
                "elbows, runs through walls or ceilings, is longer than 15 feet, "
                "uses flexible vinyl or foil ducting (which should be replaced with "
                "rigid metal), or if you're unable to access both ends.</p>",
            ),
            (H, "Frequently Asked Questions"),
            (
                P,
                "<p><strong>How often should I clean my dryer vent?</strong><br>"
                "At minimum once per year. If you do heavy laundry (large family, "
                "pets), every 6 months is better. Clean the lint screen after every "
                "single load.</p>"
                "<p><strong>Can I use a leaf blower to clean my dryer vent?</strong><br>"
                "Yes — a leaf blower is effective for pushing lint out of the vent "
                "duct. Insert the blower nozzle into the vent opening behind the "
                "dryer, seal around it with a towel, and run the blower for 30 "
                "seconds. Have someone check the exterior vent for lint output.</p>"
                "<p><strong>Does a clean vent actually save energy?</strong><br>"
                "Yes. A clogged vent can increase drying time by 50% or more, "
                "which directly increases your electric or gas bill. Annual cleaning "
                "can save $25–$50 per year in energy costs.</p>",
            ),
        ],
    },
    # ─── Post 7: Appliance Maintenance Tips ───────────────────────────
    {
        "title": "10 Appliance Maintenance Tips That Save You Money",
        "slug": "appliance-maintenance-tips-save-money",
        "seo_title": "10 Appliance Maintenance Tips to Save Money",
        "search_description": (
            "Prevent costly appliance breakdowns with these 10 easy maintenance "
            "tips. Extend appliance life and save money on repairs."
        ),
        "intro": (
            "Simple maintenance habits can add years to your appliances "
            "and save hundreds on repairs. Here are 10 tips that matter most."
        ),
        "author_name": "Inland Empire Appliance Repair",
        "tags": ["maintenance", "tips", "cost-savings"],
        "body": [
            (H, "Preventive Maintenance Saves Hundreds"),
            (
                P,
                "<p>Most appliance breakdowns are preventable. The parts that fail "
                "most often — compressors overheating, drains clogging, pumps seizing "
                "— usually fail because of deferred maintenance, not manufacturing "
                "defects. Here are 10 maintenance habits that keep your appliances "
                "running longer and your repair bills low.</p>",
            ),
            (H, "1. Clean Refrigerator Condenser Coils Every 6 Months"),
            (
                P,
                "<p>Dusty condenser coils force the compressor to work harder, "
                "increasing energy use and shortening the compressor's life. Vacuum "
                "the coils (underneath or behind the fridge) twice a year. This "
                "single habit is the #1 way to extend your refrigerator's life.</p>",
            ),
            (H, "2. Clean Your Dryer Lint Screen After Every Load"),
            (
                P,
                "<p>Beyond the fire safety benefit, a clean lint screen improves "
                "airflow and drying efficiency. Also clean the dryer vent duct "
                "annually. A clogged vent is the leading cause of dryer heating "
                "failures and house fires.</p>",
            ),
            (H, "3. Run an Empty Dishwasher Cleaning Cycle Monthly"),
            (
                P,
                "<p>Place a cup of white vinegar on the top rack and run a hot "
                "cycle. This dissolves grease buildup in the spray arms, drain "
                "path, and interior. Also clean the dishwasher filter weekly — "
                "a clogged filter is the #1 cause of dishwashers not draining.</p>",
            ),
            (H, "4. Don't Overload Your Washing Machine"),
            (
                P,
                "<p>Overloading stresses the bearings, suspension springs, and "
                "drive belt. It also leads to poor cleaning and off-balance spin "
                "cycles that can damage the drum and frame. Leave enough room "
                "for clothes to move freely.</p>",
            ),
            (H, "5. Clean Washing Machine Door Seal Monthly"),
            (
                P,
                "<p>Front-load washers trap moisture in the rubber door gasket, "
                "breeding mold and mildew. Wipe the seal and glass after each "
                "use, and leave the door ajar between loads. Run a monthly "
                "cleaning cycle with a washing machine cleaner or bleach.</p>",
            ),
            (H, "6. Check Washing Machine Hoses Annually"),
            (
                P,
                "<p>Rubber washing machine hoses deteriorate and can burst, "
                "causing catastrophic water damage. Inspect them annually for "
                "bulges, cracks, or stiffness. Replace rubber hoses with braided "
                "stainless steel hoses every 5 years — they're more durable and "
                "resist bursting.</p>",
            ),
            (H, "7. Flush Your Water Heater Annually"),
            (
                P,
                "<p>Sediment builds up at the bottom of tank water heaters, "
                "reducing efficiency and accelerating corrosion. Annual flushing "
                "removes sediment and can extend your water heater's life by "
                "several years.</p>",
            ),
            (H, "8. Replace Oven Door Gaskets When Worn"),
            (
                P,
                "<p>The gasket around your oven door keeps heat inside. When it "
                "wears out, heat escapes, the oven works harder, and cooking "
                "times increase. If you feel heat escaping when your hand is "
                "near the closed oven door, the gasket needs replacing.</p>",
            ),
            (H, "9. Level Your Appliances"),
            (
                P,
                "<p>Washers, dryers, and refrigerators that aren't level vibrate "
                "more, wear parts unevenly, and can walk across the floor. Use "
                "a bubble level and adjust the leveling feet until the appliance "
                "is perfectly stable.</p>",
            ),
            (H, "10. Change AC and Range Hood Filters"),
            (
                P,
                "<p>Replace or clean HVAC air filters every 1–3 months. Dirty "
                "filters restrict airflow, increase energy use, and strain the "
                "blower motor. Range hood grease filters should be cleaned "
                "monthly in hot soapy water or the dishwasher.</p>",
            ),
            (H, "Frequently Asked Questions"),
            (
                P,
                "<p><strong>How much can maintenance save on repairs?</strong><br>"
                "Regular maintenance can reduce appliance repair costs by 30–50% "
                "over the lifetime of the appliance, mainly by preventing the most "
                "common failures (clogged coils, drains, and filters).</p>"
                "<p><strong>Should I get an annual appliance check-up?</strong><br>"
                "For HVAC systems, yes — annual professional service is strongly "
                "recommended. For other appliances, the DIY maintenance tips above "
                "are sufficient for most homeowners.</p>"
                "<p><strong>What's the best way to extend my appliance's life?</strong><br>"
                "Clean it regularly, don't overload it, and address small problems "
                "before they become big ones. A $150 repair today prevents a "
                "$1,500 replacement next year.</p>",
            ),
        ],
    },
    # ─── Post 8: Ice Maker Not Working ────────────────────────────────
    {
        "title": "Ice Maker Not Working? Complete Troubleshooting Guide",
        "slug": "ice-maker-not-working-troubleshooting",
        "seo_title": "Ice Maker Not Working? Troubleshooting Guide",
        "search_description": (
            "Ice maker not making ice? Troubleshoot common problems with our "
            "guide. Fix water supply, temperature, and mechanical issues."
        ),
        "intro": (
            "When your ice maker stops producing ice, it could be something "
            "simple or a failed component. Here's how to troubleshoot it."
        ),
        "author_name": "Inland Empire Appliance Repair",
        "tags": ["refrigerator", "ice-maker", "troubleshooting"],
        "body": [
            (H, "Why Your Ice Maker Stopped Making Ice"),
            (
                P,
                "<p>Ice maker problems are one of the most common refrigerator "
                "complaints. Before assuming the ice maker itself has failed, "
                "there are several external factors that can stop ice production — "
                "some of which you can fix yourself in minutes.</p>",
            ),
            (H, "Check the Simple Things First"),
            (
                P,
                "<p><strong>Is the ice maker turned on?</strong> This sounds obvious, "
                "but the on/off switch or arm can be accidentally bumped. Check that "
                "the wire arm is in the down position (on) or the switch is set to on.</p>"
                "<p><strong>Is the water supply connected?</strong> The ice maker needs "
                "a water line running from your home's plumbing to the back of the "
                "refrigerator. Check that the water valve behind the fridge is fully "
                "open and the supply line isn't kinked or disconnected.</p>"
                "<p><strong>Is the freezer cold enough?</strong> The ice maker requires "
                "the freezer to be at 0°F (−18°C) or below. If the freezer is too warm, "
                "the thermostat won't trigger the ice maker to cycle. Check the "
                "temperature setting.</p>"
                "<p><strong>Is the ice bin full?</strong> Most ice makers have a "
                "shutoff mechanism that stops production when the bin is full. If "
                "ice has clumped together, the sensor may read the bin as full. "
                "Break up clumps or empty and refill the bin.</p>",
            ),
            (H, "Common Ice Maker Component Failures"),
            (
                P,
                "<p><strong>Water inlet valve:</strong> This electrically controlled "
                "valve opens to fill the ice mold. If it fails or has low water "
                "pressure (below 20 psi), no water reaches the ice maker. A "
                "technician can test and replace this valve quickly.</p>"
                "<p><strong>Ice maker module:</strong> The ice maker module controls "
                "the cycle — filling, freezing, harvesting, and ejecting. If the "
                "module motor fails, the cycle stops. Module replacement restores "
                "full ice production.</p>"
                "<p><strong>Water filter:</strong> A clogged water filter restricts "
                "flow to the ice maker and water dispenser. Replace the filter every "
                "6 months. If you haven't changed it in over a year, this could be "
                "your problem.</p>"
                "<p><strong>Frozen water line:</strong> The small water line feeding "
                "the ice maker can freeze, especially if the freezer temperature is "
                "set too low. A technician can thaw the line and adjust the "
                "temperature to prevent recurrence.</p>",
            ),
            (H, "Frequently Asked Questions"),
            (
                P,
                "<p><strong>How long does it take for an ice maker to make ice?</strong><br>"
                "A healthy ice maker produces a batch of ice every 90 minutes to 2 "
                "hours. After installation or a reset, allow 24 hours for the first "
                "batch and discard the first 2–3 batches.</p>"
                "<p><strong>Why is my ice maker making small or hollow ice?</strong><br>"
                "Small, thin, or hollow ice cubes indicate low water flow — usually "
                "a clogged water filter, partially closed water valve, or low home "
                "water pressure.</p>"
                "<p><strong>Can I repair my ice maker myself?</strong><br>"
                "Resetting the ice maker, replacing the water filter, and checking "
                "the water supply are safe DIY tasks. Electrical components like the "
                "inlet valve and ice maker module require professional replacement.</p>",
            ),
        ],
    },
    # ─── Post 9: Washing Machine Shaking ──────────────────────────────
    {
        "title": "Why Is My Washing Machine Shaking and Vibrating?",
        "slug": "washing-machine-shaking-vibrating-causes",
        "seo_title": "Washing Machine Shaking? Causes & Fixes",
        "search_description": (
            "Washing machine shaking violently during spin? Learn the causes "
            "— from leveling to worn parts — and how to stop the vibration."
        ),
        "intro": (
            "A washing machine that shakes, walks, or vibrates during spin "
            "isn't just annoying — it can damage your floor and the machine."
        ),
        "author_name": "Inland Empire Appliance Repair",
        "tags": ["washer", "troubleshooting", "vibration"],
        "body": [
            (H, "What Causes a Washing Machine to Shake?"),
            (
                P,
                "<p>Some vibration during the spin cycle is normal — the drum "
                "spins at 800–1600 RPM depending on the model. But excessive "
                'shaking, banging, or a washer that "walks" across the floor '
                "indicates a problem that should be addressed before it causes "
                "real damage to the machine or your home.</p>",
            ),
            (H, "Start With the Basics: Leveling and Load Balance"),
            (
                P,
                "<p><strong>Level the machine:</strong> The #1 cause of washing "
                "machine vibration is simply not being level. Place a bubble level "
                "on top of the washer (front-to-back and side-to-side). Adjust the "
                "leveling feet until the washer is perfectly stable and doesn't "
                "rock when pushed.</p>"
                "<p><strong>Check the load:</strong> A single heavy item (like a "
                "comforter or jeans) without counterbalancing items creates an "
                "off-balance load. Add a few towels to balance heavy loads. Avoid "
                "washing a single large item alone.</p>"
                "<p><strong>Remove shipping bolts:</strong> New washing machines "
                "come with shipping bolts that lock the drum during transport. If "
                "these aren't removed during installation, the machine will vibrate "
                "violently. Check the back of the washer for large bolts securing "
                "the inner drum.</p>",
            ),
            (H, "Mechanical Causes of Excessive Shaking"),
            (
                P,
                "<p><strong>Worn shock absorbers or dampers (front-load):</strong> "
                "Front-load washers use shock absorbers to dampen drum movement "
                "during spin. When they wear out, the drum bounces excessively. "
                "This is a common repair on washers over 5 years old.</p>"
                "<p><strong>Broken suspension springs (top-load):</strong> Top-load "
                "washers use suspension springs to support the tub. A broken spring "
                "lets the tub hang unevenly, causing violent shaking during spin.</p>"
                "<p><strong>Worn drum bearings:</strong> Drum bearings allow the inner "
                "tub to spin smoothly. When they fail, you'll hear a loud rumbling "
                "or grinding noise along with increased vibration. Bearing replacement "
                "is a significant repair but is often worthwhile on newer machines.</p>"
                "<p><strong>Worn drive belt:</strong> A loose or worn drive belt can "
                "cause the drum to spin unevenly, creating vibration. Belt replacement "
                "is a quick, affordable repair.</p>",
            ),
            (H, "When to Call a Professional"),
            (
                P,
                "<p>If leveling the machine and balancing loads doesn't solve the "
                "problem, the vibration is likely mechanical — worn absorbers, "
                "springs, bearings, or a drum spider that's corroded. These repairs "
                "require disassembling the washer and are best handled by a "
                "professional technician with the right tools and parts.</p>",
            ),
            (H, "Frequently Asked Questions"),
            (
                P,
                "<p><strong>Can a shaking washer damage my floor?</strong><br>"
                "Yes. A violently shaking washer can crack tile floors, dent wood "
                "flooring, loosen plumbing connections, and even shift off the drain "
                "standpipe, causing water damage. Address the issue promptly.</p>"
                "<p><strong>Are anti-vibration pads worth it?</strong><br>"
                "Anti-vibration pads help reduce normal operational vibration and "
                "noise transfer to the floor. They're especially helpful on upper "
                "floors or over finished spaces. However, they won't fix a "
                "mechanical issue like worn shock absorbers.</p>"
                "<p><strong>How much does washing machine vibration repair cost?</strong><br>"
                "Shock absorber replacement is a moderate repair. Suspension spring "
                "and belt replacement are affordable. Bearing replacement is more "
                "involved but still costs far less than a new machine.</p>",
            ),
        ],
    },
    # ─── Post 10: Samsung Error Codes ─────────────────────────────────
    {
        "title": "Samsung Refrigerator Error Codes: What They Mean",
        "slug": "samsung-refrigerator-error-codes-explained",
        "seo_title": "Samsung Refrigerator Error Codes Explained",
        "search_description": (
            "Samsung refrigerator showing an error code? Learn what each code "
            "means and whether you need professional repair."
        ),
        "intro": (
            "Samsung refrigerators display error codes when they detect a "
            "problem. Here's what the most common codes mean."
        ),
        "author_name": "Inland Empire Appliance Repair",
        "tags": ["samsung", "refrigerator", "error-codes"],
        "body": [
            (H, "Understanding Samsung Refrigerator Error Codes"),
            (
                P,
                "<p>Samsung refrigerators use alphanumeric error codes to help "
                "technicians quickly diagnose problems. When you see an error "
                "code flashing on the display, your fridge is telling you exactly "
                "what's wrong — if you know how to read it.</p>"
                "<p>Here are the most common Samsung refrigerator error codes, "
                "what they indicate, and what action to take.</p>",
            ),
            (H, "Temperature Sensor Errors: 1E, 5E, 8E, 21E, 22E, 24E"),
            (
                P,
                "<p>These codes indicate a temperature sensor failure in various "
                'zones of the refrigerator. The number before "E" identifies '
                "which sensor:</p>"
                "<ul>"
                "<li><strong>1E / 5E:</strong> Fridge compartment sensor</li>"
                "<li><strong>8E:</strong> Ice maker sensor</li>"
                "<li><strong>21E:</strong> Freezer sensor</li>"
                "<li><strong>22E:</strong> Fridge room sensor (newer models)</li>"
                "<li><strong>24E:</strong> Freezer defrost sensor</li>"
                "</ul>"
                "<p><strong>Action:</strong> Temperature sensor replacement is a "
                "straightforward repair. The sensor itself is an affordable part — "
                "the key is correctly identifying which sensor has failed.</p>",
            ),
            (H, "Defrost Errors: 22E, 40E, PC ER"),
            (
                P,
                "<p><strong>22E / 40E:</strong> These indicate the defrost system "
                "is malfunctioning — the evaporator coils are icing over, blocking "
                "airflow. Common causes include a failed defrost heater, defrost "
                "thermostat, or control board issue.</p>"
                "<p><strong>PC ER:</strong> Communication error between the main "
                "control board and the display board. Power cycling (unplugging "
                "for 2 minutes) sometimes resolves this. If it persists, a control "
                "board replacement may be needed.</p>",
            ),
            (H, "Fan Errors: 21E, 41E, 83E, 85E"),
            (
                P,
                "<p>Fan error codes indicate that one of the refrigerator's fans "
                "has stopped working or is running outside normal parameters:</p>"
                "<ul>"
                "<li><strong>41E:</strong> Freezer fan error</li>"
                "<li><strong>83E / 85E:</strong> Ice maker fan (on models with "
                "an ice maker fan)</li>"
                "</ul>"
                "<p><strong>Action:</strong> Check if anything is blocking the fan. "
                "If the fan is visibly obstructed by ice buildup, a defrost issue "
                "is the root cause. If the fan motor has failed, replacement is "
                "needed.</p>",
            ),
            (H, "Ice Maker Errors: 8E, 14E, 39E, 40E"),
            (
                P,
                "<p>Ice maker-specific error codes point to problems with the "
                "ice making system:</p>"
                "<ul>"
                "<li><strong>8E:</strong> Ice maker sensor failure</li>"
                "<li><strong>14E:</strong> Ice maker function error</li>"
                "<li><strong>39E:</strong> Ice maker communication error</li>"
                "</ul>"
                "<p><strong>Action:</strong> Try resetting the ice maker first "
                "(press and hold the reset button for 10 seconds). If the error "
                "returns, the ice maker assembly or sensor needs professional "
                "diagnosis.</p>",
            ),
            (H, "How to Reset a Samsung Refrigerator"),
            (
                P,
                "<p>Before calling for service, try a power reset: unplug the "
                "refrigerator for 2–5 minutes, then plug it back in. This clears "
                "temporary errors caused by power fluctuations or software glitches. "
                "If the error code returns after resetting, the underlying "
                "component needs repair.</p>"
                "<p>On some Samsung models, you can also press and hold the "
                '"Power Freeze" and "Power Cool" buttons simultaneously for '
                "8 seconds to reset the display panel.</p>",
            ),
            (H, "Frequently Asked Questions"),
            (
                P,
                "<p><strong>Should I unplug my Samsung fridge when it shows an error?</strong><br>"
                "A brief unplug (2–5 minutes) is safe and clears temporary errors. "
                "But if the fridge isn't cooling, minimize how long it's off to "
                "protect your food. Call for same-day repair instead of repeated "
                "resets.</p>"
                "<p><strong>Are Samsung refrigerators reliable?</strong><br>"
                "Samsung makes well-featured refrigerators, but like all brands, "
                "they have common failure points (ice maker issues and temperature "
                "sensor failures being the most frequent). Most problems are "
                "repairable at a reasonable cost.</p>"
                "<p><strong>How much does Samsung refrigerator repair cost?</strong><br>"
                "Sensor replacements are affordable. Control board and ice maker "
                "assembly repairs are moderate. We service all Samsung models and "
                "carry common Samsung parts on our trucks.</p>",
            ),
        ],
    },
    # ─── Post 11: Oven Not Heating ────────────────────────────────────
    {
        "title": "Oven Not Heating? Gas vs. Electric Troubleshooting",
        "slug": "oven-not-heating-gas-electric-troubleshooting",
        "seo_title": "Oven Not Heating? Gas vs Electric Fixes",
        "search_description": (
            "Oven not heating up? Troubleshoot gas and electric oven problems. "
            "Common causes, DIY checks, and when to call a repair pro."
        ),
        "intro": (
            "An oven that won't heat disrupts your whole routine. The fix "
            "depends on whether you have gas or electric — here's how to tell."
        ),
        "author_name": "Inland Empire Appliance Repair",
        "tags": ["oven", "troubleshooting", "gas", "electric"],
        "body": [
            (H, "Gas Oven vs. Electric Oven: Different Problems, Different Fixes"),
            (
                P,
                "<p>When your oven won't heat, the troubleshooting approach "
                "depends entirely on whether you have a gas or electric model. "
                "Gas ovens use a burner and ignition system, while electric ovens "
                "rely on resistance heating elements. Here's what to check for "
                "each type.</p>",
            ),
            (H, "Gas Oven Not Heating"),
            (
                P,
                "<p><strong>Faulty igniter (most common):</strong> The igniter is a "
                "ceramic element that glows red-hot to open the gas safety valve "
                "and ignite the burner. Over time, igniters weaken — they may glow "
                "but not get hot enough to open the valve. You'll notice the oven "
                "taking forever to preheat, then eventually not heating at all. "
                "Igniter replacement is one of the most common and affordable oven "
                "repairs.</p>"
                "<p><strong>Gas safety valve:</strong> The safety valve opens when "
                "it receives enough heat from the igniter. If the valve itself "
                "fails (less common), gas can't reach the burner even with a "
                "working igniter.</p>"
                "<p><strong>Thermostat or temperature sensor:</strong> If the oven "
                "heats inconsistently (too hot, too cold, or fluctuating), the "
                "temperature sensor or thermostat may need replacement or "
                "calibration.</p>",
            ),
            (H, "Electric Oven Not Heating"),
            (
                P,
                "<p><strong>Burned-out bake element:</strong> The bake element is the "
                "coil at the bottom of the oven. When it fails, you may see visible "
                "damage — blistering, holes, or a break in the element. If the "
                "element doesn't glow red when the oven is set to bake, it needs "
                "replacement.</p>"
                "<p><strong>Failed broil element:</strong> The broil element at the "
                "top of the oven can also burn out. If baking works but broiling "
                "doesn't (or vice versa), the failed element is clear.</p>"
                "<p><strong>Faulty relay or control board:</strong> The control board "
                "sends power to the elements. If it fails, the elements don't "
                "receive electricity even though they're functional. Control board "
                "diagnosis requires a multimeter and professional expertise.</p>",
            ),
            (H, "Safety Warning for Gas Ovens"),
            (
                P,
                "<p>If you smell gas when the oven is off, <strong>do not try "
                "to light the oven manually or use any electrical switches.</strong> "
                "Open windows, leave the house, and call your gas company's "
                "emergency line. A persistent gas smell indicates a leak that "
                "requires immediate professional attention.</p>"
                "<p>A brief gas smell when a gas oven first ignites is normal — "
                "a small amount of gas releases before the igniter lights the "
                "burner. But if the smell lingers or is strong, shut off the gas "
                "supply and call for service.</p>",
            ),
            (H, "Frequently Asked Questions"),
            (
                P,
                "<p><strong>Why does my oven take so long to preheat?</strong><br>"
                "In gas ovens, a slow preheat almost always means a weakening "
                "igniter. In electric ovens, it could be a partially failed element "
                "or a calibration issue with the temperature sensor.</p>"
                "<p><strong>Can I replace an oven igniter myself?</strong><br>"
                "While technically possible, oven igniter replacement involves "
                "working near the gas line and safely reconnecting the igniter "
                "wiring. For safety, we recommend professional installation.</p>"
                "<p><strong>How long do oven heating elements last?</strong><br>"
                "Electric bake and broil elements typically last 5–15 years "
                "depending on usage. Gas igniters last 3–8 years on average.</p>",
            ),
        ],
    },
    # ─── Post 12: Washing Machine Mold ────────────────────────────────
    {
        "title": "How to Get Rid of Washing Machine Mold and Odors",
        "slug": "washing-machine-mold-odors-removal",
        "seo_title": "Washing Machine Mold & Odors: Removal Guide",
        "search_description": (
            "Smelly washing machine? Learn how to remove mold and odors from "
            "front-load and top-load washers with proven cleaning methods."
        ),
        "intro": (
            "Musty-smelling clothes after washing? Mold in your washing "
            "machine is the likely culprit. Here's how to fix it for good."
        ),
        "author_name": "Inland Empire Appliance Repair",
        "tags": ["washer", "maintenance", "cleaning", "mold"],
        "body": [
            (H, "Why Washing Machines Get Moldy"),
            (
                P,
                "<p>Washing machines are warm, damp environments — perfect for "
                "mold and mildew growth. Front-load washers are especially "
                "susceptible because their horizontal drum and airtight door "
                "seal trap moisture between cycles. But top-load washers can "
                "develop odors too, especially around the agitator and tub rim.</p>"
                "<p>The result: clothes come out of the wash smelling musty, "
                "and you may notice black spots on the rubber door gasket, "
                "a slimy residue inside the drum, or a sour smell when you "
                "open the machine.</p>",
            ),
            (H, "Step 1: Deep Clean the Door Gasket (Front-Load)"),
            (
                P,
                "<p>The rubber gasket around a front-load washer door is where "
                "mold hides most aggressively. Pull back the folds of the gasket "
                "and you'll likely find black mold, hair, and debris trapped "
                "inside.</p>"
                "<p><strong>How to clean it:</strong> Mix equal parts white vinegar "
                "and water in a spray bottle. Spray the gasket thoroughly, "
                "especially inside the folds. Let it sit for 10 minutes. Scrub "
                "with an old toothbrush, then wipe clean with a microfiber cloth. "
                "For stubborn black mold, use a paste of baking soda and water "
                "instead.</p>",
            ),
            (H, "Step 2: Run a Cleaning Cycle"),
            (
                P,
                "<p>Run the hottest cycle your washer offers (many models have "
                'a dedicated "Clean" or "Tub Clean" cycle). Add one of the '
                "following cleaning agents:</p>"
                "<ul>"
                "<li><strong>Option A:</strong> 2 cups of white vinegar directly "
                "in the drum</li>"
                "<li><strong>Option B:</strong> A commercial washing machine "
                "cleaner (Affresh, OxiClean, etc.)</li>"
                "<li><strong>Option C:</strong> 1/2 cup of bleach in the bleach "
                "dispenser (do NOT mix bleach with vinegar)</li>"
                "</ul>"
                "<p>Run the cycle empty — no clothes — on the hottest setting. "
                "This kills mold spores throughout the internal plumbing.</p>",
            ),
            (H, "Step 3: Prevent Mold From Coming Back"),
            (
                P,
                "<p>Killing existing mold is only half the battle. These habits "
                "prevent it from returning:</p>"
                "<ul>"
                "<li><strong>Leave the door ajar</strong> after every wash to let "
                "the drum air out</li>"
                "<li><strong>Wipe the gasket and door glass</strong> after each "
                "use to remove standing water</li>"
                "<li><strong>Remove wet clothes promptly</strong> — don't leave "
                "them sitting in the drum</li>"
                "<li><strong>Use HE detergent</strong> in HE machines — regular "
                "detergent creates excess suds that leave residue</li>"
                "<li><strong>Run a monthly cleaning cycle</strong> with vinegar "
                "or a washing machine cleaner</li>"
                "<li><strong>Don't overuse detergent</strong> — more soap doesn't "
                "mean cleaner clothes; excess detergent feeds mold</li>"
                "</ul>",
            ),
            (H, "Frequently Asked Questions"),
            (
                P,
                "<p><strong>Is washing machine mold dangerous?</strong><br>"
                "Mold exposure can trigger allergic reactions, respiratory "
                "irritation, and skin issues in sensitive individuals. Clothes "
                "washed in a moldy machine can carry mold spores, causing "
                "skin reactions when worn.</p>"
                "<p><strong>Can mold damage my washing machine?</strong><br>"
                "Persistent mold can deteriorate the rubber door gasket over "
                "time, eventually requiring gasket replacement. It can also "
                "clog drain paths and create persistent odor problems.</p>"
                "<p><strong>Why do front-load washers get more mold than top-load?</strong><br>"
                "Front-load washers use an airtight door seal that traps moisture "
                "inside the gasket folds. Top-load washers have better natural "
                "ventilation because heat rises and escapes through the top.</p>",
            ),
        ],
    },
    # ─── Post 13: Freezer Not Cold Enough ─────────────────────────────
    {
        "title": "Freezer Not Cold Enough? Common Causes and Fixes",
        "slug": "freezer-not-cold-enough-causes-fixes",
        "seo_title": "Freezer Not Cold Enough? Causes & Fixes",
        "search_description": (
            "Freezer not freezing properly? Discover common causes like "
            "dirty coils, door seals, and fan failures — plus when to call a pro."
        ),
        "intro": (
            "Soft ice cream and thawed food are signs your freezer isn't cold "
            "enough. Here are the most likely causes and what to do."
        ),
        "author_name": "Inland Empire Appliance Repair",
        "tags": ["freezer", "troubleshooting", "temperature"],
        "body": [
            (H, "Why Is My Freezer Not Freezing Properly?"),
            (
                P,
                "<p>A properly functioning freezer maintains a temperature of 0°F "
                "(−18°C). If your frozen food is soft, ice cream is mushy, or ice "
                "cubes are partially melted, your freezer isn't cold enough. This "
                "isn't just an inconvenience — food stored above 0°F loses quality "
                "faster and may not be safe for long-term storage.</p>",
            ),
            (H, "Check These Simple Things First"),
            (
                P,
                "<p><strong>Temperature setting:</strong> Verify the freezer is set "
                "to 0°F. Someone may have accidentally adjusted the dial or "
                "digital control.</p>"
                "<p><strong>Overpacking:</strong> An overstuffed freezer blocks "
                "airflow vents inside the compartment. Cold air needs to circulate "
                "freely. Leave some space between items and don't block the vents "
                "(usually at the back or top of the freezer).</p>"
                "<p><strong>Door seal:</strong> Close the freezer door on a dollar "
                "bill. If you can pull it out easily without resistance, the door "
                "gasket isn't sealing properly and warm air is leaking in. Gasket "
                "replacement is an affordable fix.</p>"
                "<p><strong>Door left ajar:</strong> Check that nothing is preventing "
                "the freezer door from closing completely. A protruding item, ice "
                "buildup on the gasket, or a warped shelf can keep the door from "
                "sealing.</p>",
            ),
            (H, "Component Failures That Cause Warm Freezers"),
            (
                P,
                "<p><strong>Dirty condenser coils:</strong> Dusty coils can't dissipate "
                "heat effectively, reducing the entire refrigerator's cooling capacity. "
                "The freezer suffers first because it requires the coldest temperatures. "
                "Vacuum the coils (usually underneath or behind the unit).</p>"
                "<p><strong>Evaporator fan failure:</strong> This fan circulates cold "
                "air throughout the freezer. If it fails, some areas of the freezer "
                "stay cold (near the coils) while others warm up. Listen for the fan "
                "when you open the freezer door — if it's silent, the motor likely "
                "needs replacement.</p>"
                "<p><strong>Defrost system failure:</strong> When the defrost heater, "
                "thermostat, or timer fails, ice builds up on the evaporator coils "
                "and blocks airflow. You may notice excessive frost inside the "
                "freezer. This is a common and repairable issue.</p>"
                "<p><strong>Sealed system leak:</strong> A slow refrigerant leak "
                "gradually reduces cooling capacity. The freezer may still cool "
                "but can't maintain 0°F. This requires professional diagnosis "
                "and repair.</p>",
            ),
            (H, "Frequently Asked Questions"),
            (
                P,
                "<p><strong>Is 10°F too warm for a freezer?</strong><br>"
                "Yes. The FDA recommends 0°F (−18°C) for safe long-term food "
                "storage. At 10°F, food quality degrades faster and bacterial "
                "growth isn't fully inhibited.</p>"
                "<p><strong>Can a full freezer cause temperature problems?</strong><br>"
                "Both extremes are problematic. An overpacked freezer blocks "
                "airflow. A nearly empty freezer loses cold air quickly when "
                "the door opens (frozen items act as thermal mass). Keep the "
                "freezer 75–85% full for optimal efficiency.</p>"
                "<p><strong>How do I check my freezer temperature accurately?</strong><br>"
                "Place a standalone freezer thermometer in the center of the "
                "freezer (not against a wall). Wait 24 hours for an accurate "
                "reading. Built-in temperature displays can be inaccurate.</p>",
            ),
        ],
    },
    # ─── Post 14: Dishwasher Not Cleaning ─────────────────────────────
    {
        "title": "Why Your Dishwasher Isn't Cleaning Dishes Properly",
        "slug": "dishwasher-not-cleaning-dishes-properly",
        "seo_title": "Dishwasher Not Cleaning? Causes & Solutions",
        "search_description": (
            "Dishes still dirty after the dishwasher? Learn why — from clogged "
            "spray arms to water temperature issues — and how to fix it."
        ),
        "intro": (
            "Dishes coming out cloudy, greasy, or with food still stuck on? "
            "Here are the most common reasons your dishwasher isn't cleaning."
        ),
        "author_name": "Inland Empire Appliance Repair",
        "tags": ["dishwasher", "troubleshooting", "cleaning"],
        "body": [
            (H, "Why Your Dishwasher Isn't Getting Dishes Clean"),
            (
                P,
                "<p>A dishwasher that runs a full cycle but leaves dishes dirty "
                "is frustrating. Before assuming the machine is broken, several "
                "common issues — from loading technique to water temperature — "
                "can prevent proper cleaning. Let's start with what you can fix "
                "yourself.</p>",
            ),
            (H, "User-Fixable Causes"),
            (
                P,
                "<p><strong>Overloading or poor loading:</strong> Dishes need space "
                "for water and detergent to reach every surface. Don't nest bowls "
                "together, block the spray arms, or overcrowd the racks. Face "
                "dirty surfaces toward the spray arms (typically the center).</p>"
                "<p><strong>Clogged spray arms:</strong> Remove the upper and lower "
                "spray arms and clean the small holes with a toothpick or thin "
                "wire. Food debris, mineral deposits, and broken glass can block "
                "the spray holes, dramatically reducing cleaning power.</p>"
                "<p><strong>Dirty filter:</strong> A clogged filter traps food "
                "debris that then recirculates onto your dishes. Remove and clean "
                "the filter under running water weekly for best performance.</p>"
                "<p><strong>Wrong detergent or too little detergent:</strong> Use "
                "fresh dishwasher detergent (pods or powder lose effectiveness "
                "when exposed to moisture). Make sure the dispenser opens during "
                "the wash cycle.</p>"
                "<p><strong>Water temperature too low:</strong> Your water heater "
                "should deliver water at 120°F (49°C) to the dishwasher. Run the "
                "kitchen faucet on hot until it's hot to the touch before starting "
                "the dishwasher — this ensures the first fill is hot, not lukewarm.</p>",
            ),
            (H, "Component Issues That Reduce Cleaning"),
            (
                P,
                "<p><strong>Failed wash motor:</strong> The wash motor powers the "
                "spray arms. If it's weak or failing, water pressure drops and "
                "dishes don't get clean. You may notice the wash cycle sounding "
                "quieter than usual.</p>"
                "<p><strong>Faulty water inlet valve:</strong> If the inlet valve "
                "doesn't open fully, the dishwasher doesn't get enough water for "
                "effective cleaning. Low water fill = poor cleaning.</p>"
                "<p><strong>Broken soap dispenser:</strong> If the dispenser doesn't "
                "pop open during the wash cycle, detergent sits in the door and "
                "never reaches the dishes. Check if the dispenser door opens and "
                "closes freely.</p>"
                "<p><strong>Worn spray arm bearings:</strong> If the spray arms don't "
                "spin freely, water distribution is uneven. Spin each arm by hand — "
                "they should rotate smoothly without wobbling.</p>",
            ),
            (H, "Frequently Asked Questions"),
            (
                P,
                "<p><strong>Should I pre-rinse dishes before loading?</strong><br>"
                "No — modern dishwashers and detergents are designed to work on "
                "food-soiled dishes. Scrape off large food pieces, but leave the "
                "rest. Pre-rinsing wastes water and can actually reduce cleaning "
                "because the detergent needs something to work on.</p>"
                "<p><strong>Why are my glasses coming out cloudy?</strong><br>"
                "Cloudy glasses are caused by hard water mineral deposits (etching). "
                "Use a rinse aid to prevent spotting, and check if your dishwasher "
                "has a water softener setting. If glasses are already etched, the "
                "damage is permanent.</p>"
                "<p><strong>How often should I clean my dishwasher?</strong><br>"
                "Clean the filter weekly. Run an empty cleaning cycle with vinegar "
                "or a dishwasher cleaner monthly. Inspect and clean spray arm holes "
                "every 3 months.</p>",
            ),
        ],
    },
    # ─── Post 15: No Hot Water ────────────────────────────────────────
    {
        "title": "No Hot Water? Water Heater Troubleshooting Guide",
        "slug": "no-hot-water-water-heater-troubleshooting",
        "seo_title": "No Hot Water? Water Heater Troubleshooting",
        "search_description": (
            "No hot water at home? Troubleshoot your gas or electric water "
            "heater with our guide. Common causes and when to call for repair."
        ),
        "intro": (
            "Woke up to a cold shower? Here's how to troubleshoot your gas "
            "or electric water heater and what the problem likely is."
        ),
        "author_name": "Inland Empire Appliance Repair",
        "tags": ["water-heater", "troubleshooting", "hot-water"],
        "body": [
            (H, "Why You Have No Hot Water"),
            (
                P,
                "<p>No hot water is a household emergency — it affects showers, "
                "dishes, laundry, and handwashing. The cause depends on whether "
                "you have a gas or electric water heater, and whether you have no "
                "hot water at all or just not enough. Here's how to troubleshoot "
                "both types.</p>",
            ),
            (H, "Gas Water Heater: No Hot Water"),
            (
                P,
                "<p><strong>Pilot light is out:</strong> If you have an older gas "
                "water heater with a standing pilot light, check if it's lit. Look "
                "through the small viewing window near the bottom of the tank. "
                "Follow the manufacturer's instructions on the tank to relight it. "
                "If it won't stay lit, the thermocouple likely needs replacement.</p>"
                "<p><strong>Faulty thermocouple:</strong> The thermocouple is a "
                "safety sensor that detects the pilot flame. If it fails, it shuts "
                "off the gas supply as a safety measure — even if the pilot is "
                "lit. This is one of the most common gas water heater repairs and "
                "is affordable to fix.</p>"
                "<p><strong>Gas valve failure:</strong> If the pilot lights but "
                "the main burner doesn't fire, the gas control valve may have "
                "failed. This controls both the thermostat function and the gas "
                "flow to the burner.</p>"
                "<p><strong>Sediment buildup:</strong> Over years, sediment "
                "accumulates at the bottom of the tank, insulating the water "
                "from the burner flame. This reduces heating efficiency and "
                "can cause rumbling or popping sounds. Annual flushing prevents "
                "this issue.</p>",
            ),
            (H, "Electric Water Heater: No Hot Water"),
            (
                P,
                "<p><strong>Tripped reset button:</strong> Electric water heaters "
                "have a high-temperature reset button (red button) on the upper "
                "thermostat. If it trips, the heater shuts off completely. Find "
                "the access panel on the tank, press the red button firmly, and "
                "listen for a click. If it trips again shortly after, there's an "
                "underlying electrical issue that needs professional diagnosis.</p>"
                "<p><strong>Tripped circuit breaker:</strong> Check your electrical "
                "panel. Electric water heaters use a dedicated 30-amp double-pole "
                "breaker. If it's tripped, flip it fully off then back on. If it "
                "trips again, do not keep resetting it — call an electrician or "
                "appliance technician.</p>"
                "<p><strong>Failed heating elements:</strong> Electric water heaters "
                "use two heating elements — upper and lower. If the upper element "
                "fails, you get no hot water at all. If the lower element fails, "
                "you get some hot water but it runs out quickly. Element replacement "
                "is a standard repair.</p>"
                "<p><strong>Faulty thermostat:</strong> Each heating element has its "
                "own thermostat. If a thermostat fails, its corresponding element "
                "doesn't turn on. Testing requires a multimeter and electrical "
                "knowledge — best left to a professional.</p>",
            ),
            (H, "Tankless Water Heater: No Hot Water"),
            (
                P,
                "<p><strong>Minimum flow rate not met:</strong> Tankless heaters "
                "require a minimum water flow rate to activate. If you're running "
                "a low-flow fixture, the heater may not fire. This is a design "
                "consideration, not a malfunction.</p>"
                "<p><strong>Scale buildup:</strong> Hard water causes mineral scale "
                "to build up inside the heat exchanger, reducing heating efficiency. "
                "Annual descaling with vinegar flush is essential for tankless "
                "heaters in hard water areas (which includes much of the Inland "
                "Empire).</p>"
                "<p><strong>Error codes:</strong> Tankless heaters display error "
                "codes for specific issues. Common codes relate to ignition "
                "failure, exhaust blockage, or sensor errors. Check your manual "
                "or call for professional diagnosis.</p>",
            ),
            (H, "Frequently Asked Questions"),
            (
                P,
                "<p><strong>How long should a water heater take to recover?</strong><br>"
                "Gas tank water heaters typically recover in 30–40 minutes. Electric "
                "tank heaters take 60–90 minutes. Tankless heaters provide continuous "
                "hot water with no recovery time. If recovery takes significantly "
                "longer than these ranges, a component is underperforming.</p>"
                "<p><strong>Why do I run out of hot water quickly?</strong><br>"
                "The most common causes are a failed lower heating element (electric), "
                "sediment buildup reducing tank capacity (gas or electric), a "
                "malfunctioning dip tube directing cold water to the hot outlet, "
                "or a tank that's too small for your household's demand.</p>"
                "<p><strong>Is a leaking water heater an emergency?</strong><br>"
                "A small drip from a valve fitting is not an emergency but should "
                "be repaired soon. A leak from the tank bottom indicates internal "
                "corrosion — turn off the water supply and gas/power, and call for "
                "service promptly to prevent water damage.</p>",
            ),
        ],
    },
]


class Command(BaseCommand):
    """Create SEO-optimized blog posts with optional scheduled publishing."""

    help = "Creates 15 SEO-optimized blog posts for Inland Empire Appliance Repair"

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument(
            "--schedule",
            action="store_true",
            help=(
                "Schedule posts for future publishing via go_live_at "
                "instead of publishing immediately. Requires "
                "'publish_scheduled' management command to run periodically."
            ),
        )
        parser.add_argument(
            "--interval",
            type=int,
            default=3,
            help="Days between scheduled posts (default: 3)",
        )
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete ALL existing blog posts before recreating them.",
        )

    def handle(self, *args: object, **options: Any) -> None:
        blog_index = BlogIndexPage.objects.live().first()
        if not blog_index:
            self.stderr.write(
                self.style.ERROR("BlogIndexPage not found. Run 'setup_pages' first.")
            )
            return

        # --reset: wipe all existing blog posts so they get recreated fresh
        if options.get("reset"):
            existing = BlogPage.objects.all()
            count = existing.count()
            if count:
                existing.delete()
                # Fix treebeard tree after bulk deletion
                from wagtail.models import Page

                Page.fix_tree()
                blog_index.refresh_from_db()
                self.stdout.write(
                    self.style.WARNING(f"  Reset: deleted {count} existing blog posts.")
                )

        schedule_mode: bool = options.get("schedule", False)
        interval_days: int = options.get("interval", 3)
        created = 0
        skipped = 0

        for i, post_data in enumerate(BLOG_POSTS):
            slug = post_data["slug"]

            if BlogPage.objects.filter(slug=slug).exists():
                self.stdout.write(f"  Exists, skipping: {post_data['title']}")
                skipped += 1
                continue

            # Stagger dates backward from today so posts appear in
            # chronological order on the blog listing
            days_ago = (len(BLOG_POSTS) - 1 - i) * interval_days
            post_date = date.today() - timedelta(days=days_ago)

            page = BlogPage(
                title=post_data["title"],
                slug=slug,
                seo_title=post_data["seo_title"],
                search_description=post_data["search_description"],
                intro=post_data["intro"],
                author_name=post_data.get("author_name", "Inland Empire Appliance Repair"),
                date=post_date,
                body=_body(post_data["body"]),
            )

            blog_index.add_child(instance=page)

            if schedule_mode and i >= 5:
                # First 5 posts publish immediately, rest are scheduled
                go_live = timezone.now() + timedelta(days=(i - 5) * interval_days)
                page.go_live_at = go_live
                page.live = False
                revision = page.save_revision()
                revision.approved_go_live_at = go_live
                revision.save()
                self.stdout.write(
                    f"  Scheduled: {post_data['title']} "
                    f"(go live: {go_live.strftime('%Y-%m-%d')})"
                )
            else:
                page.save_revision().publish()
                self.stdout.write(
                    self.style.SUCCESS(f"  Published: {post_data['title']}")
                )

            # Add tags after the page is saved
            for tag_name in post_data.get("tags", []):
                page.tags.add(tag_name)
            page.save()

            created += 1

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Done! Created {created} blog posts, skipped {skipped}."
            )
        )

        if schedule_mode:
            self.stdout.write(
                self.style.WARNING(
                    "\nScheduled posts require 'python manage.py publish_scheduled' "
                    "to run periodically (e.g., via Railway cron service)."
                )
            )
