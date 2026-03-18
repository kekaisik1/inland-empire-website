"""Populate city pages with unique SEO content, ZIP codes, and meta fields.

Usage:
    python manage.py populate_city_seo          # dry-run (shows changes)
    python manage.py populate_city_seo --apply  # applies changes
    python manage.py populate_city_seo --apply --city=Corona  # single city
"""

from __future__ import annotations

import logging
from typing import Any

from django.core.management.base import BaseCommand, CommandParser

from locations.models import CityPage

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# City data: unique content per city
# ---------------------------------------------------------------------------

CITY_DATA: dict[str, dict[str, Any]] = {
    "Lake Elsinore": {
        "zip_codes": "92530, 92531, 92532",
        "seo_title": "Appliance Repair in Lake Elsinore, CA — Same-Day Service",
        "search_description": (
            "Same-day appliance repair in Lake Elsinore, CA. Refrigerator, washer,"
            " dryer, dishwasher & oven repair. $70 diagnostic waived with repair."
            " Call (951) 620-9609."
        ),
        "intro": (
            "Certified same-day appliance repair for Lake Elsinore homes and"
            " businesses — warranty included, $70 diagnostic waived with repair."
        ),
        "hero_usp": (
            "EPA-certified technicians based locally in Lake Elsinore."
            " Fully stocked trucks. OEM parts. No overtime charges."
        ),
        "body": (
            "<h2>Trusted Appliance Repair in Lake Elsinore, CA</h2>"
            "<p>LOWL Appliance Repair is headquartered in Lake Elsinore, making"
            " this city our home base. When your refrigerator stops cooling on a"
            " hot summer afternoon or your washer springs a leak, our"
            " EPA-certified technicians can be at your door within hours — not"
            " days. We serve neighborhoods from Tuscany Hills and Canyon Estates"
            " to the lakefront communities along Railroad Canyon and Diamond"
            " Drive.</p>"
            "<h2>Why Lake Elsinore Residents Choose LOWL</h2>"
            "<p>As a locally owned company based right here on Langstaff Street,"
            " we understand the challenges Lake Elsinore homeowners face: hard"
            " water that wears out water heaters faster, summer heat that pushes"
            " refrigerators and AC units to their limits, and the daily demands"
            " of busy households. Our trucks carry OEM parts for Whirlpool,"
            " Samsung, LG, GE, and 15+ other brands, so most repairs are"
            " completed in a single visit.</p>"
            "<h2>Residential and Commercial Appliance Repair</h2>"
            "<p>From single-family homes near Rosetta Canyon to restaurants and"
            " businesses along Casino Drive and Railroad Canyon Road, we handle"
            " every appliance type: refrigerators, freezers, washers, dryers,"
            " dishwashers, ovens, stoves, microwaves, water heaters, and AC"
            " units. Commercial clients trust us for walk-in coolers, commercial"
            " ice machines, and restaurant-grade equipment — all serviced by the"
            " same certified technicians who work on residential appliances.</p>"
            "<h2>Transparent Pricing — No Surprises</h2>"
            "<p>Our $70 diagnostic service call is waived when you approve the"
            " repair. You receive an itemized quote before any work begins — no"
            " hidden fees, no surprise charges. Most residential repairs range"
            " from $150 to $400. Every repair includes a warranty on parts and"
            " labor. We operate 7 days a week, 8 AM to 8 PM, with no overtime"
            " or weekend surcharges.</p>"
        ),
        "about_techs": (
            "<p>Our Lake Elsinore technicians live in the community they serve."
            " Each one holds EPA 608 certification and is factory-trained across"
            " all major brands. With fully stocked trucks and years of hands-on"
            " experience in Riverside County, they arrive ready to diagnose and"
            " fix your appliance on the first visit. Every technician undergoes"
            " background checks and carries liability insurance for your peace"
            " of mind.</p>"
        ),
    },
    "Corona": {
        "zip_codes": "92877, 92878, 92879, 92880, 92881, 92882, 92883",
        "seo_title": "Appliance Repair in Corona, CA — Same-Day Service",
        "search_description": (
            "Same-day appliance repair in Corona, CA. Refrigerator, washer,"
            " dryer & oven repair for all brands. $70 diagnostic waived with"
            " repair. Call (951) 620-9609."
        ),
        "intro": (
            "Same-day appliance repair for Corona homes and businesses — all"
            " major brands, warranty included, $70 diagnostic waived with repair."
        ),
        "hero_usp": (
            "Certified technicians serving Corona and the 91 Corridor."
            " OEM parts on every truck. No overtime charges."
        ),
        "body": (
            "<h2>Professional Appliance Repair in Corona, CA</h2>"
            "<p>Corona is one of the largest cities in Riverside County, and its"
            " mix of established neighborhoods and newer developments keeps our"
            " technicians busy. Whether you live in South Corona near the"
            " Dos Lagos shopping center, the family-friendly streets of Eagle"
            " Glen, or the hillside homes of Sierra Del Oro, we provide"
            " same-day appliance repair with no overtime charges — even on"
            " weekends.</p>"
            "<h2>Common Appliance Issues in Corona</h2>"
            "<p>Corona's warm climate and hard municipal water create specific"
            " challenges for household appliances. Refrigerators and AC units"
            " work harder during triple-digit summers, which accelerates"
            " compressor and condenser wear. Hard water shortens the lifespan of"
            " water heaters, dishwashers, and washing machines by causing mineral"
            " buildup in valves and heating elements. Our technicians see these"
            " patterns daily and come prepared with the right parts.</p>"
            "<h2>All Brands, All Appliance Types</h2>"
            "<p>We repair refrigerators, freezers, washers, dryers, dishwashers,"
            " ovens, stoves, microwaves, water heaters, and AC units across all"
            " major brands — Whirlpool, Samsung, LG, GE, Maytag, Bosch,"
            " KitchenAid, Sub-Zero, Viking, and more. Our trucks carry OEM and"
            " manufacturer-approved parts for fast, reliable repairs. Most jobs"
            " are completed in a single visit.</p>"
            "<h2>Serving Corona's Commercial Businesses</h2>"
            "<p>From restaurants along Ontario Avenue and the Crossings"
            " to office parks near the 91/15 interchange, our"
            " EPA-certified team services commercial refrigeration, ice"
            " machines, and restaurant-grade equipment. Same-day scheduling"
            " means less downtime for your business. We understand that a broken"
            " walk-in cooler or commercial dishwasher costs you revenue every"
            " hour it's down.</p>"
        ),
        "about_techs": (
            "<p>Our Corona-area technicians are Riverside County residents with"
            " EPA 608 certification and factory training across all major"
            " appliance brands. They drive fully stocked trucks with common"
            " replacement parts — compressors, thermostats, control boards,"
            " heating elements, and pumps — so most repairs finish in one visit."
            " Every tech is background-checked, insured, and committed to"
            " transparent pricing with no surprise fees.</p>"
        ),
    },
    "Riverside": {
        "zip_codes": "92501, 92503, 92504, 92505, 92506, 92507, 92508, 92509",
        "seo_title": "Appliance Repair in Riverside, CA — Same-Day Service",
        "search_description": (
            "Same-day appliance repair in Riverside, CA. All major brands."
            " Refrigerator, washer, dryer, dishwasher & oven repair. $70"
            " diagnostic waived with repair. Call (951) 620-9609."
        ),
        "intro": (
            "Same-day appliance repair across Riverside — from downtown to"
            " Orangecrest, warranty included, $70 diagnostic waived with repair."
        ),
        "hero_usp": (
            "Certified technicians covering all Riverside ZIP codes."
            " Same-day service 7 days a week. No overtime charges."
        ),
        "body": (
            "<h2>Appliance Repair Across All of Riverside, CA</h2>"
            "<p>As the county seat and largest city in Riverside County,"
            " Riverside spans dozens of distinct neighborhoods — from the"
            " historic Mission Inn district and downtown core to the suburban"
            " developments of Orangecrest, Canyon Crest, and Alessandro Heights."
            " Wherever you are in Riverside, our technicians provide same-day"
            " appliance repair for residential and commercial properties.</p>"
            "<h2>Fast Response Times in Riverside</h2>"
            "<p>Our local base in the Inland Empire means shorter drive times to"
            " Riverside addresses. Morning bookings typically get an afternoon"
            " service window, and we operate 7 days a week from 8 AM to 8 PM"
            " with no overtime surcharges. Whether you're in the Galleria at"
            " Tyler area, the University neighborhood near UC Riverside, or the"
            " Arlanza community, we reach you the same day.</p>"
            "<h2>Riverside's Most Common Appliance Problems</h2>"
            "<p>Riverside's hot, dry summers push cooling appliances hard."
            " Refrigerator compressors, AC condensers, and freezer evaporator"
            " coils are among our most frequent repairs in this area. The"
            " region's mineral-rich water also takes a toll on dishwasher spray"
            " arms, washing machine inlet valves, and water heater anode rods."
            " Our trucks carry the parts to fix these common issues on the"
            " spot.</p>"
            "<h2>Residential and Commercial Coverage</h2>"
            "<p>From family homes in La Sierra and Woodcrest to restaurants on"
            " University Avenue and medical offices in the Magnolia Center area,"
            " we service every appliance type: refrigerators, freezers, washers,"
            " dryers, dishwashers, ovens, stoves, microwaves, water heaters,"
            " and commercial refrigeration. All brands, all types, all backed by"
            " our parts and labor warranty.</p>"
        ),
        "about_techs": (
            "<p>Our Riverside technicians are Inland Empire residents who know"
            " the city's neighborhoods and traffic patterns. Each holds EPA 608"
            " certification, carries factory training on all major brands, and"
            " drives a fully stocked truck with OEM parts. They provide upfront"
            " quotes before starting work and never charge overtime — even on"
            " evening or weekend calls.</p>"
        ),
    },
    "Murrieta": {
        "zip_codes": "92562, 92563, 92564",
        "seo_title": "Appliance Repair in Murrieta, CA — Same-Day Service",
        "search_description": (
            "Same-day appliance repair in Murrieta, CA. All major brands,"
            " warranty included. $70 diagnostic waived with repair."
            " Call (951) 620-9609."
        ),
        "intro": (
            "Certified same-day appliance repair in Murrieta — all major brands,"
            " OEM parts, warranty included, $70 diagnostic waived with repair."
        ),
        "hero_usp": (
            "Factory-trained technicians serving Murrieta and Southwest"
            " Riverside County. No overtime charges."
        ),
        "body": (
            "<h2>Reliable Appliance Repair in Murrieta, CA</h2>"
            "<p>Murrieta is one of the fastest-growing cities in Riverside"
            " County, and its newer housing developments mean appliances that"
            " are still within their serviceable lifespan — making repair the"
            " smart choice over replacement. From the master-planned communities"
            " of Bear Creek and Greer Ranch to the established neighborhoods"
            " near Murrieta Hot Springs Road, we provide same-day appliance"
            " repair with warranty on every job.</p>"
            "<h2>Why Murrieta Homeowners Call LOWL</h2>"
            "<p>Murrieta's family-oriented neighborhoods depend on working"
            " appliances. A broken washer with a family of five or a"
            " refrigerator outage in summer heat — these are urgent situations."
            " We respond the same day, arrive with OEM parts on the truck, and"
            " fix the problem in one visit. Our $70 diagnostic is waived when"
            " you approve the repair, and we never charge extra for evenings"
            " or weekends.</p>"
            "<h2>Full-Service Appliance Repair</h2>"
            "<p>We repair all major appliance types across every brand:"
            " refrigerators, freezers, washers, dryers, dishwashers, ovens,"
            " stoves, microwaves, water heaters, and AC units. Brands include"
            " Whirlpool, Samsung, LG, GE, Maytag, Frigidaire, Bosch,"
            " KitchenAid, Sub-Zero, and more. Our technicians are EPA 608"
            " certified and carry manufacturer-approved parts for lasting"
            " repairs.</p>"
            "<h2>Commercial Appliance Service in Murrieta</h2>"
            "<p>Murrieta's growing commercial corridor along Jefferson Avenue and"
            " the Town Square area relies on properly functioning equipment."
            " We service restaurants, cafes, and businesses with commercial"
            " refrigeration, ice machines, and industrial-grade kitchen"
            " equipment — all with the same warranty and transparent pricing we"
            " offer residential customers.</p>"
        ),
        "about_techs": (
            "<p>Murrieta-area technicians on our team are local Riverside County"
            " residents with EPA 608 certification and factory training on 15+"
            " appliance brands. They understand the specific appliance patterns"
            " in newer Southwest Riverside County homes and arrive with stocked"
            " trucks ready to complete most repairs in a single visit. All"
            " technicians are background-checked and fully insured.</p>"
        ),
    },
    "Temecula": {
        "zip_codes": "92589, 92590, 92591, 92592, 92593",
        "seo_title": "Appliance Repair in Temecula, CA — Same-Day Service",
        "search_description": (
            "Same-day appliance repair in Temecula, CA. Refrigerator, washer,"
            " dryer, oven & commercial repair. Warranty included. $70"
            " diagnostic waived. Call (951) 620-9609."
        ),
        "intro": (
            "Same-day appliance repair for Temecula homes and businesses — all"
            " brands serviced, warranty included, $70 diagnostic waived."
        ),
        "hero_usp": (
            "EPA-certified technicians covering Temecula and wine country."
            " OEM parts. 7 days a week. No overtime charges."
        ),
        "body": (
            "<h2>Appliance Repair Services in Temecula, CA</h2>"
            "<p>Temecula's unique mix of wine country estates, suburban"
            " neighborhoods, and a vibrant Old Town commercial district creates"
            " diverse appliance repair needs. Whether you own a home in"
            " Redhawk, Wolf Creek, or Harveston — or run a restaurant along"
            " Old Town Front Street — our EPA-certified technicians deliver"
            " same-day repair for every appliance type.</p>"
            "<h2>Serving Temecula's Premium Homes</h2>"
            "<p>Many Temecula homes feature high-end appliances from Sub-Zero,"
            " Viking, Thermador, and Bosch. Our technicians are"
            " factory-trained on these premium brands and carry specialized"
            " OEM parts. From built-in refrigerators and dual-fuel ranges to"
            " wine coolers and professional-grade dishwashers, we repair"
            " luxury appliances to factory specifications with warranty"
            " included.</p>"
            "<h2>Wine Country and Hospitality Equipment</h2>"
            "<p>Temecula Valley's wineries, tasting rooms, and restaurants"
            " depend on commercial refrigeration and kitchen equipment. A"
            " broken walk-in cooler or commercial ice machine means lost"
            " product and revenue. We prioritize commercial calls and offer"
            " same-day service for restaurants, hospitality businesses, and"
            " food service operations across the Temecula Valley.</p>"
            "<h2>Upfront Pricing with Warranty</h2>"
            "<p>Our $70 diagnostic fee is waived when you approve the repair."
            " Most residential repairs in Temecula range from $150 to $400."
            " You receive an itemized quote before work begins — no hidden"
            " fees. Every repair is backed by a warranty on parts and labor."
            " We operate 7 days a week with no overtime surcharges.</p>"
        ),
        "about_techs": (
            "<p>Our Temecula technicians hold EPA 608 certification and"
            " specialized training on premium brands like Sub-Zero, Viking, and"
            " Thermador — critical for the high-end appliances common in"
            " Temecula homes. They carry OEM parts on every truck, provide"
            " upfront quotes, and complete most repairs in one visit."
            " Background-checked and fully insured for residential and"
            " commercial properties.</p>"
        ),
    },
    "Menifee": {
        "zip_codes": "92584, 92585, 92586",
        "seo_title": "Appliance Repair in Menifee, CA — Same-Day Service",
        "search_description": (
            "Same-day appliance repair in Menifee, CA. All brands, warranty"
            " included. Refrigerator, washer, dryer & oven repair. $70"
            " diagnostic waived. Call (951) 620-9609."
        ),
        "intro": (
            "Same-day appliance repair for Menifee — certified technicians, all"
            " major brands, warranty included, $70 diagnostic waived with repair."
        ),
        "hero_usp": (
            "Local technicians serving Menifee's growing communities."
            " OEM parts on every truck. No overtime charges."
        ),
        "body": (
            "<h2>Appliance Repair for Menifee's Growing Community</h2>"
            "<p>Menifee is one of the youngest incorporated cities in"
            " California, and its rapid growth means thousands of homes with"
            " appliances still within serviceable range. From the Audie Murphy"
            " Ranch and Countryside Marketplace neighborhoods to Sun City and"
            " the Heritage Lake area, we deliver same-day appliance repair to"
            " every corner of Menifee.</p>"
            "<h2>New Homes, Modern Appliances</h2>"
            "<p>Many Menifee developments feature newer appliance models from"
            " Samsung, LG, Whirlpool, and GE. These units often need repairs"
            " that are cost-effective compared to full replacement — a failed"
            " control board, a worn-out door seal, or a faulty ice maker. Our"
            " technicians carry OEM parts for these common fixes and complete"
            " most repairs in a single visit.</p>"
            "<h2>Full-Range Appliance Service</h2>"
            "<p>We service refrigerators, freezers, washers, dryers,"
            " dishwashers, ovens, stoves, microwaves, water heaters, and AC"
            " units. Brands covered include Whirlpool, Samsung, LG, GE, Maytag,"
            " Kenmore, Frigidaire, Bosch, KitchenAid, Sub-Zero, and more."
            " Whether your appliance is 2 years old or 15, our certified"
            " technicians will assess whether repair makes financial sense —"
            " and give you an honest recommendation.</p>"
            "<h2>Affordable, Transparent Pricing</h2>"
            "<p>Our $70 diagnostic fee is waived when you approve the repair."
            " Most residential repairs in Menifee range from $150 to $400"
            " depending on the appliance and parts needed. You receive a"
            " complete quote before work starts. Every repair is backed by a"
            " warranty on parts and labor. We work 7 days a week, 8 AM to"
            " 8 PM, with no overtime charges.</p>"
        ),
        "about_techs": (
            "<p>Our Menifee technicians are Riverside County residents who know"
            " the area's neighborhoods and newer home developments. Each holds"
            " EPA 608 certification, carries factory training on all major"
            " brands, and drives a fully stocked truck. They provide clear,"
            " upfront pricing and complete most repairs in a single visit —"
            " no follow-up appointments needed.</p>"
        ),
    },
    "Beaumont": {
        "zip_codes": "92223",
        "seo_title": "Appliance Repair in Beaumont, CA — Same-Day Service",
        "search_description": (
            "Same-day appliance repair in Beaumont, CA. All brands, warranty"
            " included. $70 diagnostic waived with repair."
            " Call (951) 620-9609."
        ),
        "intro": (
            "Same-day appliance repair for Beaumont homes — certified"
            " technicians, all brands, warranty included, $70 diagnostic waived."
        ),
        "hero_usp": (
            "EPA-certified technicians serving Beaumont and the San"
            " Gorgonio Pass. Stocked trucks. No overtime."
        ),
        "body": (
            "<h2>Same-Day Appliance Repair in Beaumont, CA</h2>"
            "<p>Beaumont sits at the gateway to the San Gorgonio Pass, and its"
            " rapidly expanding residential communities — from Tournament Hills"
            " and Solera to the newer Fairway Canyon developments — all need"
            " reliable appliance service. Our technicians provide same-day"
            " repair for every major appliance type across all Beaumont"
            " neighborhoods.</p>"
            "<h2>Elevation and Climate Considerations</h2>"
            "<p>Beaumont's higher elevation means cooler winters and hot, dry"
            " summers — both of which stress household appliances differently"
            " than lower-elevation Inland Empire cities. Water heaters work"
            " harder in winter months, while refrigerators and AC systems are"
            " pushed during summer. The area's well water in some neighborhoods"
            " accelerates mineral buildup in dishwashers and washing machines."
            " Our technicians understand these local patterns and arrive with"
            " the right parts.</p>"
            "<h2>Complete Appliance Coverage</h2>"
            "<p>We repair refrigerators, freezers, washers, dryers,"
            " dishwashers, ovens, stoves, microwaves, water heaters, and AC"
            " units across all major brands. Beaumont's growing commercial"
            " sector — especially along Beaumont Avenue and Highland Springs"
            " Avenue — also relies on us for commercial refrigeration and"
            " restaurant equipment service.</p>"
            "<h2>Straightforward Pricing</h2>"
            "<p>Our $70 diagnostic is waived when you approve the repair. Most"
            " residential repairs range from $150 to $400. Every job is backed"
            " by a warranty on parts and labor. We operate 7 days a week with"
            " no overtime or weekend charges — the same rates apply whether"
            " you call at 8 AM Monday or 6 PM Sunday.</p>"
        ),
        "about_techs": (
            "<p>Technicians serving Beaumont are EPA 608 certified and trained"
            " on all major residential and commercial brands. They carry"
            " OEM parts on fully stocked trucks and are familiar with the"
            " specific appliance issues common in Beaumont's newer housing"
            " developments. Every technician is background-checked, insured,"
            " and committed to transparent, upfront pricing.</p>"
        ),
    },
    "Perris": {
        "zip_codes": "92570, 92571, 92572",
        "seo_title": "Appliance Repair in Perris, CA — Same-Day Service",
        "search_description": (
            "Same-day appliance repair in Perris, CA. Refrigerator, washer,"
            " dryer & oven repair for all brands. Warranty included. $70"
            " diagnostic waived. Call (951) 620-9609."
        ),
        "intro": (
            "Certified same-day appliance repair for Perris — all brands,"
            " OEM parts, warranty included, $70 diagnostic waived with repair."
        ),
        "hero_usp": (
            "Local technicians covering Perris and surrounding communities."
            " Same-day availability 7 days a week."
        ),
        "body": (
            "<h2>Affordable Appliance Repair in Perris, CA</h2>"
            "<p>Perris is a growing community in central Riverside County where"
            " families and businesses depend on working appliances every day."
            " From the residential neighborhoods near Perris Boulevard and"
            " the Harvest Landing community to the farms and"
            " light-industrial areas along the I-215 corridor, we provide"
            " same-day appliance repair at honest prices.</p>"
            "<h2>Budget-Friendly Repairs That Last</h2>"
            "<p>Perris homeowners value straightforward pricing and reliable"
            " workmanship. That's exactly what we deliver. Our $70 diagnostic"
            " is waived when you approve the repair, and most residential fixes"
            " cost between $150 and $400. We use OEM parts — not cheap"
            " aftermarket alternatives — so your repair lasts. Every job is"
            " backed by a warranty on parts and labor.</p>"
            "<h2>All Appliances, All Brands</h2>"
            "<p>We service refrigerators, freezers, washers, dryers,"
            " dishwashers, ovens, stoves, microwaves, water heaters, and AC"
            " units from Whirlpool, Samsung, LG, GE, Maytag, Kenmore,"
            " Frigidaire, Bosch, KitchenAid, and more. Whether your appliance"
            " is a workhorse model or a premium brand, our certified"
            " technicians have the training and parts to fix it right.</p>"
            "<h2>Commercial Equipment Service</h2>"
            "<p>Perris's commercial and industrial areas, including businesses"
            " near the Perris Valley Commerce Center, depend on reliable"
            " commercial appliances. We repair walk-in coolers, commercial"
            " ice machines, and restaurant-grade ovens and dishwashers."
            " Same-day availability for commercial clients means less"
            " downtime and less lost revenue.</p>"
        ),
        "about_techs": (
            "<p>Our Perris-area technicians are local Riverside County"
            " professionals with EPA 608 certification and factory training"
            " across all major brands. They drive fully stocked trucks and"
            " are experienced with both residential and light-commercial"
            " equipment. Every technician provides upfront quotes and is"
            " background-checked and insured for your protection.</p>"
        ),
    },
    "Canyon Lake": {
        "zip_codes": "92587",
        "seo_title": "Appliance Repair in Canyon Lake, CA — Same-Day Service",
        "search_description": (
            "Same-day appliance repair in Canyon Lake, CA. All brands, warranty"
            " included. $70 diagnostic waived with repair. Premium and"
            " standard brands. Call (951) 620-9609."
        ),
        "intro": (
            "Same-day appliance repair for Canyon Lake residents — all brands,"
            " warranty included, $70 diagnostic waived with repair."
        ),
        "hero_usp": (
            "Certified technicians serving Canyon Lake's gated communities."
            " OEM parts on every truck. No overtime."
        ),
        "body": (
            "<h2>Appliance Repair for Canyon Lake, CA</h2>"
            "<p>Canyon Lake is a private, gated community centered around the"
            " lake, with homes ranging from lakefront properties to hillside"
            " residences. The area's mix of luxury and standard appliances"
            " requires technicians who can work on both premium brands like"
            " Sub-Zero and Viking and everyday brands like Whirlpool and"
            " Samsung. Our EPA-certified team handles all of them.</p>"
            "<h2>Serving Canyon Lake's Unique Needs</h2>"
            "<p>The gated community setting means coordination matters — our"
            " technicians communicate arrival times clearly so you can arrange"
            " gate access. We carry all necessary parts on our trucks to"
            " minimize the need for return visits. Many Canyon Lake homes"
            " have upgraded kitchens with built-in refrigerators, dual-fuel"
            " ranges, and wine coolers that require specialized knowledge. Our"
            " techs are factory-trained on these units.</p>"
            "<h2>Complete Appliance Service</h2>"
            "<p>We repair refrigerators, freezers, washers, dryers,"
            " dishwashers, ovens, stoves, microwaves, water heaters, and AC"
            " units. Canyon Lake's proximity to our Lake Elsinore home base"
            " means some of the fastest response times in our service area."
            " Morning bookings typically get an afternoon slot, and we"
            " operate 7 days a week.</p>"
            "<h2>Honest Pricing, Guaranteed Work</h2>"
            "<p>Our $70 diagnostic is waived when you approve the repair."
            " You get a detailed quote before any work begins. Most"
            " residential repairs fall between $150 and $400. Every job"
            " includes a warranty on parts and labor, so if the same issue"
            " comes back, we come back and fix it free.</p>"
        ),
        "about_techs": (
            "<p>Our Canyon Lake technicians are familiar with the community's"
            " gated access procedures and the premium appliance brands"
            " commonly found in lakefront and hillside homes. Each is EPA 608"
            " certified, factory-trained, and experienced with high-end"
            " built-in and freestanding units. Background-checked and insured,"
            " they provide transparent quotes and reliable repairs.</p>"
        ),
    },
    "Norco": {
        "zip_codes": "92860",
        "seo_title": "Appliance Repair in Norco, CA — Same-Day Service",
        "search_description": (
            "Same-day appliance repair in Norco, CA. Refrigerator, washer,"
            " dryer & oven repair. All brands, warranty included. $70"
            " diagnostic waived. Call (951) 620-9609."
        ),
        "intro": (
            "Same-day appliance repair for Norco homes — certified technicians,"
            " all major brands, warranty included, $70 diagnostic waived."
        ),
        "hero_usp": (
            "EPA-certified technicians serving Norco and Horsetown USA."
            " Fully stocked trucks. No overtime charges."
        ),
        "body": (
            "<h2>Appliance Repair in Norco — Horsetown USA</h2>"
            "<p>Norco's unique semi-rural character means larger properties,"
            " well water in some areas, and appliances that face different"
            " demands than typical suburban homes. From the equestrian trails"
            " and ranch-style properties along Hamner Avenue to the"
            " neighborhoods near Hidden Valley and Norco Hills, we provide"
            " same-day appliance repair tailored to this community's needs.</p>"
            "<h2>Well Water and Appliance Wear</h2>"
            "<p>Many Norco properties rely on well water, which carries higher"
            " mineral content than municipal water. This accelerates scale"
            " buildup in water heaters, washing machines, and dishwashers —"
            " reducing efficiency and shortening component lifespan. Our"
            " technicians see these issues frequently in Norco and come"
            " prepared with the parts to address mineral-related damage."
            " Regular maintenance can prevent costly failures, and we're happy"
            " to advise on protecting your appliances.</p>"
            "<h2>All Appliances, All Brands</h2>"
            "<p>We repair refrigerators, freezers, washers, dryers,"
            " dishwashers, ovens, stoves, microwaves, water heaters, and AC"
            " units from all major manufacturers. Norco's larger properties"
            " often include additional appliances like standalone freezers and"
            " secondary refrigerators — all covered under our service. OEM"
            " parts, warranty included, no overtime charges.</p>"
            "<h2>Transparent, Flat-Rate Pricing</h2>"
            "<p>Our $70 diagnostic fee is waived when you approve the repair."
            " Most residential repairs range from $150 to $400, and you"
            " receive an itemized quote before work begins. We work 7 days"
            " a week, 8 AM to 8 PM, and never charge extra for evening or"
            " weekend appointments.</p>"
        ),
        "about_techs": (
            "<p>Our Norco technicians understand the area's semi-rural"
            " properties and the appliance challenges that come with well water"
            " and larger homes. Each holds EPA 608 certification and factory"
            " training across all major brands. They arrive with fully stocked"
            " trucks, provide honest assessments, and complete most repairs"
            " in one visit. Background-checked and fully insured.</p>"
        ),
    },
}

# ---------------------------------------------------------------------------
# Spanish translations of content
# ---------------------------------------------------------------------------

CITY_DATA_ES: dict[str, dict[str, Any]] = {
    "Lake Elsinore": {
        "seo_title": "Reparacion de Electrodomesticos en Lake Elsinore, CA",
        "search_description": (
            "Reparacion de electrodomesticos el mismo dia en Lake Elsinore, CA."
            " Refrigeradores, lavadoras, secadoras y hornos. Diagnostico de"
            " $70 — se descuenta con la reparacion. Llame (951) 620-9609."
        ),
        "intro": (
            "Reparacion de electrodomesticos el mismo dia en Lake Elsinore —"
            " todas las marcas, garantia incluida, diagnostico de $70 se"
            " descuenta con la reparacion."
        ),
        "hero_usp": (
            "Tecnicos certificados EPA con base en Lake Elsinore."
            " Piezas OEM. Sin cargos por horas extra."
        ),
    },
    "Corona": {
        "seo_title": "Reparacion de Electrodomesticos en Corona, CA",
        "search_description": (
            "Reparacion de electrodomesticos el mismo dia en Corona, CA."
            " Todas las marcas, garantia incluida. $70 diagnostico se"
            " descuenta con reparacion. Llame (951) 620-9609."
        ),
        "intro": (
            "Reparacion de electrodomesticos el mismo dia en Corona — todas"
            " las marcas, piezas OEM, garantia incluida."
        ),
        "hero_usp": (
            "Tecnicos certificados sirviendo Corona y el corredor 91."
            " Sin cargos por horas extra."
        ),
    },
    "Riverside": {
        "seo_title": "Reparacion de Electrodomesticos en Riverside, CA",
        "search_description": (
            "Reparacion de electrodomesticos el mismo dia en Riverside, CA."
            " Todas las marcas. Garantia incluida. Diagnostico de $70 se"
            " descuenta. Llame (951) 620-9609."
        ),
        "intro": (
            "Reparacion de electrodomesticos el mismo dia en Riverside —"
            " desde el centro hasta Orangecrest, garantia incluida."
        ),
        "hero_usp": (
            "Tecnicos certificados cubriendo todos los codigos postales de"
            " Riverside. Sin cargos por horas extra."
        ),
    },
    "Murrieta": {
        "seo_title": "Reparacion de Electrodomesticos en Murrieta, CA",
        "search_description": (
            "Reparacion de electrodomesticos el mismo dia en Murrieta, CA."
            " Todas las marcas, garantia incluida. Diagnostico de $70 se"
            " descuenta. Llame (951) 620-9609."
        ),
        "intro": (
            "Reparacion de electrodomesticos certificada el mismo dia en"
            " Murrieta — todas las marcas, garantia incluida."
        ),
        "hero_usp": (
            "Tecnicos con entrenamiento de fabrica sirviendo Murrieta."
            " Sin cargos por horas extra."
        ),
    },
    "Temecula": {
        "seo_title": "Reparacion de Electrodomesticos en Temecula, CA",
        "search_description": (
            "Reparacion de electrodomesticos el mismo dia en Temecula, CA."
            " Residencial y comercial. Garantia incluida. Diagnostico de"
            " $70 se descuenta. Llame (951) 620-9609."
        ),
        "intro": (
            "Reparacion de electrodomesticos el mismo dia en Temecula —"
            " todas las marcas, garantia incluida, diagnostico de $70."
        ),
        "hero_usp": (
            "Tecnicos certificados EPA cubriendo Temecula y el valle."
            " Piezas OEM. Sin cargos por horas extra."
        ),
    },
    "Menifee": {
        "seo_title": "Reparacion de Electrodomesticos en Menifee, CA",
        "search_description": (
            "Reparacion de electrodomesticos el mismo dia en Menifee, CA."
            " Todas las marcas, garantia incluida. Diagnostico de $70 se"
            " descuenta. Llame (951) 620-9609."
        ),
        "intro": (
            "Reparacion de electrodomesticos el mismo dia en Menifee —"
            " tecnicos certificados, todas las marcas, garantia incluida."
        ),
        "hero_usp": (
            "Tecnicos locales sirviendo las comunidades de Menifee."
            " Piezas OEM. Sin cargos por horas extra."
        ),
    },
    "Beaumont": {
        "seo_title": "Reparacion de Electrodomesticos en Beaumont, CA",
        "search_description": (
            "Reparacion de electrodomesticos el mismo dia en Beaumont, CA."
            " Todas las marcas, garantia incluida. $70 diagnostico se"
            " descuenta. Llame (951) 620-9609."
        ),
        "intro": (
            "Reparacion de electrodomesticos el mismo dia en Beaumont —"
            " tecnicos certificados, todas las marcas, garantia incluida."
        ),
        "hero_usp": (
            "Tecnicos certificados EPA sirviendo Beaumont y San Gorgonio"
            " Pass. Sin cargos por horas extra."
        ),
    },
    "Perris": {
        "seo_title": "Reparacion de Electrodomesticos en Perris, CA",
        "search_description": (
            "Reparacion de electrodomesticos el mismo dia en Perris, CA."
            " Todas las marcas, garantia incluida. $70 diagnostico se"
            " descuenta. Llame (951) 620-9609."
        ),
        "intro": (
            "Reparacion de electrodomesticos certificada el mismo dia en"
            " Perris — todas las marcas, piezas OEM, garantia incluida."
        ),
        "hero_usp": (
            "Tecnicos locales cubriendo Perris y comunidades cercanas."
            " Servicio el mismo dia, 7 dias a la semana."
        ),
    },
    "Canyon Lake": {
        "seo_title": "Reparacion de Electrodomesticos en Canyon Lake, CA",
        "search_description": (
            "Reparacion de electrodomesticos el mismo dia en Canyon Lake, CA."
            " Todas las marcas, garantia incluida. $70 diagnostico se"
            " descuenta. Llame (951) 620-9609."
        ),
        "intro": (
            "Reparacion de electrodomesticos el mismo dia en Canyon Lake —"
            " todas las marcas, garantia incluida, diagnostico de $70."
        ),
        "hero_usp": (
            "Tecnicos certificados sirviendo Canyon Lake. Piezas OEM."
            " Sin cargos por horas extra."
        ),
    },
    "Norco": {
        "seo_title": "Reparacion de Electrodomesticos en Norco, CA",
        "search_description": (
            "Reparacion de electrodomesticos el mismo dia en Norco, CA."
            " Todas las marcas, garantia incluida. $70 diagnostico se"
            " descuenta. Llame (951) 620-9609."
        ),
        "intro": (
            "Reparacion de electrodomesticos el mismo dia en Norco — tecnicos"
            " certificados, todas las marcas, garantia incluida."
        ),
        "hero_usp": (
            "Tecnicos certificados EPA sirviendo Norco. Camiones"
            " completamente abastecidos. Sin cargos extra."
        ),
    },
}


class Command(BaseCommand):
    help = "Populate city pages with unique SEO content, ZIP codes, and meta."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Apply changes (default is dry-run).",
        )
        parser.add_argument(
            "--city",
            type=str,
            help="Only update a specific city (by title).",
        )

    def handle(self, *args: object, **options: dict[str, Any]) -> None:
        apply = options["apply"]
        target_city = options.get("city")
        mode = "APPLYING" if apply else "DRY-RUN"

        self.stdout.write(f"\n{'=' * 60}")
        self.stdout.write(f"  City SEO Content Population — {mode}")
        self.stdout.write(f"{'=' * 60}\n")

        updated = 0

        # Process English pages
        en_pages = CityPage.objects.live().filter(locale__language_code="en")
        if target_city:
            en_pages = en_pages.filter(title=target_city)

        for page in en_pages:
            city_name = page.title
            data = CITY_DATA.get(city_name)
            if not data:
                self.stdout.write(
                    self.style.WARNING(f"  SKIP: No data for '{city_name}'")
                )
                continue

            changes = self._compute_changes(page, data, include_body=True)
            if not changes:
                self.stdout.write(
                    self.style.SUCCESS(f"  OK: {city_name} (EN) — no changes needed")
                )
                continue

            self.stdout.write(f"\n  {city_name} (EN):")
            for field, (old_len, new_len) in changes.items():
                self.stdout.write(f"    {field}: {old_len} → {new_len} chars")

            if apply:
                self._apply_changes(page, data, include_body=True)
                updated += 1
                self.stdout.write(self.style.SUCCESS("    ✓ Saved and published"))

        # Process Spanish pages
        es_pages = CityPage.objects.live().filter(locale__language_code="es")
        if target_city:
            es_pages = es_pages.filter(title=target_city)

        for page in es_pages:
            city_name = page.title
            data = CITY_DATA_ES.get(city_name)
            en_data = CITY_DATA.get(city_name)
            if not data or not en_data:
                self.stdout.write(
                    self.style.WARNING(f"  SKIP: No ES data for '{city_name}'")
                )
                continue

            # Spanish pages get meta fields + ZIP codes but NOT body content
            # (body should be professionally translated)
            merged = {
                "zip_codes": en_data["zip_codes"],
                "seo_title": data["seo_title"],
                "search_description": data["search_description"],
                "intro": data["intro"],
                "hero_usp": data["hero_usp"],
            }

            changes = self._compute_changes(page, merged, include_body=False)
            if not changes:
                self.stdout.write(
                    self.style.SUCCESS(f"  OK: {city_name} (ES) — no changes needed")
                )
                continue

            self.stdout.write(f"\n  {city_name} (ES):")
            for field, (old_len, new_len) in changes.items():
                self.stdout.write(f"    {field}: {old_len} → {new_len} chars")

            if apply:
                self._apply_changes(page, merged, include_body=False)
                updated += 1
                self.stdout.write(self.style.SUCCESS("    ✓ Saved and published"))

        self.stdout.write(f"\n{'=' * 60}")
        if apply:
            self.stdout.write(self.style.SUCCESS(f"  Done — {updated} pages updated."))
        else:
            self.stdout.write("  Dry-run complete. Run with --apply to save changes.")
        self.stdout.write(f"{'=' * 60}\n")

    def _compute_changes(
        self,
        page: CityPage,
        data: dict[str, Any],
        *,
        include_body: bool,
    ) -> dict[str, tuple[int, int]]:
        """Return dict of field → (old_len, new_len) for fields that differ."""
        changes: dict[str, tuple[int, int]] = {}

        field_map = {
            "zip_codes": "zip_codes",
            "seo_title": "seo_title",
            "search_description": "search_description",
            "intro": "intro",
            "hero_usp": "hero_usp",
        }
        if include_body:
            field_map["body"] = "body"
            field_map["about_techs"] = "about_techs"

        for data_key, model_field in field_map.items():
            if data_key not in data:
                continue
            old_val = getattr(page, model_field, "") or ""
            new_val = data[data_key]
            if old_val != new_val:
                changes[model_field] = (len(old_val), len(new_val))

        return changes

    def _apply_changes(
        self,
        page: CityPage,
        data: dict[str, Any],
        *,
        include_body: bool,
    ) -> None:
        """Apply data to a page and publish it."""
        for key in (
            "zip_codes",
            "seo_title",
            "search_description",
            "intro",
            "hero_usp",
        ):
            if key in data:
                setattr(page, key, data[key])

        if include_body:
            if "body" in data:
                page.body = data["body"]
            if "about_techs" in data:
                page.about_techs = data["about_techs"]

        revision = page.save_revision()
        revision.publish()
