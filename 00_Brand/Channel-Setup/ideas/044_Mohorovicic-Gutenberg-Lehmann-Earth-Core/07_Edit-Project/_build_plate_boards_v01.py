#!/usr/bin/env python3
"""HOS 044 (Earth's Inner Core: How Earthquakes X-Rayed Our Planet) pre-VO plate boards v01. J0555. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/044_Mohorovicic-Gutenberg-Lehmann-Earth-Core/earth_core_script_master_v01.md
and SOURCES_v01.md. Nothing is generation_authorized.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

EDIT = Path(__file__).resolve().parent
OUT = EDIT / "parts"
OUT.mkdir(parents=True, exist_ok=True)

FLOW_CREDITS = {"Quality": 100, "Fast": 10}
USD_PER_S = {"Quality": 0.20, "Fast": 0.10}
USD_PER_STILL = 0.039
GBP_PER_USD = 0.80
TAKES_PER_KEEP = {"Quality": round(70 / 27, 2), "Fast": round(94 / 48, 2)}
STILLS_PER_PLATE = round(171 / 75, 2)
VERTEX_LENGTHS = (4, 6, 8)

STYLE = "Premium Animistry-class 3D cartoon. "
FAST_TAIL = (
    " Daylight, window light or matte painted ink only. No candle, flame, glow, "
    "spark, fireball or lightning. No readable words or numbers anywhere. Silent. "
    "Continuous motion through the final frame. No Explorer. No Orbit."
)
QUAL_TAIL = (
    " No readable words or numbers anywhere. Silent. Continuous motion through "
    "the final frame. No Explorer. No Orbit."
)
EXP_TAIL = (
    " Exactly one Explorer, on model: round gold glasses, teal long coat, finished hair. "
    "No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Orbit."
)


def fmt_t(sec: float) -> str:
    m = int(sec // 60)
    s = sec - m * 60
    return f"{m}:{s:05.2f}"


def price_row(q: str, use_s: float) -> dict:
    if q in ("Quality", "Fast"):
        clip = next(L for L in VERTEX_LENGTHS if L >= use_s - 1e-6)
        try1 = USD_PER_S[q] * clip * GBP_PER_USD
        exp = try1 * TAKES_PER_KEEP[q] + STILLS_PER_PLATE * USD_PER_STILL * GBP_PER_USD
        fexp = math.ceil(FLOW_CREDITS[q] * TAKES_PER_KEEP[q])
        return {
            "route": "flow-first",
            "flow_model": f"Veo 3.1 {q}",
            "flow_clip_s": 8,
            "flow_credits_try1": FLOW_CREDITS[q],
            "flow_credits_expected": fexp,
            "vertex_model": "veo-3.1-generate-001" if q == "Quality" else "veo-3.1-fast-generate-001",
            "vertex_clip_s": clip,
            "vertex_try1_gbp": round(try1, 2),
            "vertex_expected_gbp": round(exp, 2),
        }
    return {
        "route": "code-graphic" if q == "code_graphic" else q,
        "flow_model": None,
        "flow_clip_s": 0,
        "flow_credits_try1": 0,
        "flow_credits_expected": 0,
        "vertex_model": None,
        "vertex_clip_s": 0,
        "vertex_try1_gbp": 0.0,
        "vertex_expected_gbp": 0.0,
    }


PARTS_SPEC = [
    (
        1,
        "Part 01 — Six Thousand Kilometres Beneath Your Feet and the Cardboard Cards in Copenhagen",
        [
            ("01_inge_lehmann_1936_copenhagen_garden_cards_and_earth_inner_core_cutaway", 0.0, 5.5, "A", False, "X-RAYING THE EARTH", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + in Copenhagen in 1936, 48-year-old Danish seismologist Inge Lehmann sits at a wooden garden table sorting cardboard cards of seismograph traces from the 17 June 1929 New Zealand earthquake, diving beneath her feet through 35 km of rocky crust, 2,890 km of silicate mantle, and a liquid iron outer core into a 1,220-kilometre solid iron-nickel inner core.",
             STYLE + "In a sunlit 1936 Copenhagen garden, forty-eight-year-old Danish seismologist Inge Lehmann in a tweed jacket sorts tan cardboard index cards covered in inked wave traces at a wooden table beside a cutaway terrestrial globe revealing a solid metallic sphere inside a liquid outer core." + QUAL_TAIL,
             {"kind": "WHEN", "label": "COPENHAGEN, 1936 · 17 JUNE 1929", "timeline_step": "4/5 · 17 Jun 1929–1936 (Inge Lehmann uses New Zealand earthquake traces in the shadow zone to discover the 1,220 km-radius inner core in her paper 'P\'')", "hold_s": 3.5}),
            ("02_mohorovicic_1909_seismogram_gutenberg_1914_shadow_zone_and_lehmann_1936_split", 5.5, 6.0, "B", False, "CRUST, LIQUID CORE, SOLID CORE", "Quality",
             "Quality: complex three-part split composition (Andrija Mohorovičić's 8 October 1909 Zagreb seismograph trace showing the 35 km crust-mantle bounce on the left; Beno Gutenberg's 1914 104°–140° core shadow-zone diagram at 2,890 km depth in the centre; Inge Lehmann's 1936 cardboard cards and solid inner core model on the right).",
             STYLE + "Three-panel period composition: on the left, a brass Wiechert smoked-paper seismograph drum; in the centre, an inked cross-section of Earth's shadow zone; on the right, a stack of oatmeal-cardboard index cards beside a cutaway brass-and-iron globe." + QUAL_TAIL,
             None),
            ("03_inge_lehmann_1936_copenhagen_measuring_1929_buller_seismograms_with_ruler", 11.5, 6.0, "C", False, "COPENHAGEN, 1936", "Quality",
             "Quality: readable face (in Copenhagen in 1936, Inge Lehmann compares smoked-paper seismogram copies from Russian and European stations after the 17 June 1929 Buller earthquake in New Zealand, spotting P-wave arrivals right inside the 104°–140° shadow zone).",
             STYLE + "In a 1936 Copenhagen garden study, Danish seismologist Inge Lehmann holds a brass magnifying glass and wooden ruler over dark smoked-paper seismogram strips beside a box of hand-cut oatmeal-cardboard cards." + QUAL_TAIL,
             {"kind": "WHEN", "label": "COPENHAGEN, 1936", "timeline_step": "4/5 · 17 Jun 1929–1936 (Inge Lehmann discovers the 1,220 km-radius solid inner core in Copenhagen)", "hold_s": 3.5}),
            ("04_kola_borehole_12_2km_vs_moho_35km_gutenberg_2890km_and_lehmann_1220km_core_chart", 17.5, 8.0, "E", False, "12.2 KM DRILL (0.19%) VS MOHO (35 KM) · LIQUID CORE (2,890 KM) · SOLID INNER CORE (1,220 KM RADIUS)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked depth and scale comparison chart contrasts the deepest hole humans have ever drilled (Kola Superdeep Borehole, 12.2 km = 0.19% of Earth's 6,371 km radius) against Earth's internal layers mapped by earthquake waves: crust to Moho (~35 km), rocky mantle to Gutenberg discontinuity (2,890 km), liquid iron outer core (2,890–5,150 km), and solid iron-nickel inner core (5,150–6,371 km, radius 1,220 km at ~5,400 °C).",
             {"kind": "DATA", "label": "12.2 KM DEEPEST DRILL (0.19%) VS MOHO (35 KM), LIQUID CORE (2,890 KM) & SOLID INNER CORE (1,220 KM)", "detail": "Inked depth & scale comparison chart on period paper contrasting the deepest hole humans have ever drilled (Kola Superdeep Borehole, 12.2 km = 0.19% of Earth's 6,371 km radius) against Earth's internal layers mapped by earthquake waves: crust to Moho (~35 km), rocky mantle to Gutenberg discontinuity (2,890 km), liquid iron outer core (2,890–5,150 km), and solid iron-nickel inner core (5,150–6,371 km, radius 1,220 km at ~5,400 °C)", "scale": "if the Earth were the size of an apple, the deepest hole humans have ever drilled wouldn't even pierce a twentieth of the apple's skin — yet earthquake waves let us see all the way to the pips at the centre", "who_card": "Andrija Mohorovičić (1857–1936) — Croatian meteorologist and seismologist · Beno Gutenberg (1889–1960) — German-born seismologist · Inge Lehmann (1888–1993) — Danish mathematician and seismologist", "when_stamp": "8 October 1909 · 1914 · 1936", "hold_s": 3.8}),
            ("05_brass_slinky_spring_and_rope_on_oak_bench_with_seismogram_strip_pan", 25.5, 5.5, "A", False, "COPENHAGEN, 1936", "Fast",
             "Fast: daylight macro pan across a coiled brass spring, a braided hemp rope, a smoked-paper seismogram strip, and a stack of oatmeal-cardboard index cards on an oak table between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak study table, the camera pans smoothly across a coiled brass spring, a braided rope, a dark smoked-paper seismogram strip, and a neat stack of tan cardboard cards." + FAST_TAIL,
             None),
            ("06_p_wave_compressional_8_13_km_s_vs_s_wave_shear_blocked_at_2890km_liquid_core_chart", 31.0, 8.0, "E", False, "SOLID CORE INSIDE LIQUID IRON", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked P-wave vs S-wave speed and transmission chart compares compressional P-waves (8–13 km/s in mantle, passing through both solid rock and liquid iron, crossing Earth in ~20 minutes) against shear S-waves (4.5–7 km/s in mantle, vanishing completely at 2,890 km depth because liquids cannot support shear).",
             {"kind": "DATA", "label": "P-WAVES (8–13 KM/S, SOLID + LIQUID, 20 MIN TRANSIT) VS S-WAVES (4.5–7 KM/S, BLOCKED AT 2,890 KM)", "detail": "Inked P-wave vs S-wave speed & transmission chart showing compressional P-waves passing through solids and liquids while shear S-waves vanish completely at 2,890 km depth", "scale": "an earthquake shockwave races all the way through the centre of the Earth from New Zealand to Denmark in just twenty minutes — faster than twenty times the speed of sound", "hold_s": 3.8}),
            ("07_table_three_props_wiechert_seismograph_drum_cutaway_core_globe_oatmeal_cards", 39.0, 5.5, "C", False, "1906 TO 1971", "Fast",
             "Fast: daylight prop table (callback source for Part 05: a brass smoked-paper seismograph drum with stylus, a cutaway terrestrial globe showing mantle, liquid outer core, and solid inner core, and Inge Lehmann's box of oatmeal-cardboard calculation cards). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a brass revolving smoked-paper seismograph drum, a painted wooden cutaway globe showing concentric core layers, and a wooden box of tan cardboard index cards." + FAST_TAIL,
             None),
            ("08_explorer_tapping_brass_globe_with_mallet_to_ring_inner_silver_core_bell", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside a large cutaway brass globe on a wooden stand, the Explorer taps the top of the globe with a small rubber mallet and watches in delight as mechanical ripples travel inward, bounce off a polished silver sphere at the centre, and ring a tiny brass bell on the side." + EXP_TAIL,
             None),
            ("09_andrija_mohorovicic_october_1909_zagreb_inspecting_wiechert_seismograph", 67.5, 5.5, "B", False, "ZAGREB, OCTOBER 1909", "Quality",
             "Quality: readable face (in Zagreb in October 1909, 52-year-old Croatian meteorologist Andrija Mohorovičić examines a Wiechert smoked-paper seismograph drum with a magnifying lens).",
             STYLE + "Inside the 1909 Zagreb meteorological observatory, bearded fifty-two-year-old Croatian scientist Andrija Mohorovičić in a dark suit peers through a brass magnifying glass at white stylus traces on a black smoked-paper drum." + QUAL_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — Two Kinds of Earthquake Waves & Andrija Mohorovičić's 8 October 1909 Zagreb Discovery",
        [
            ("01_oldham_1906_wave_types_and_mohorovicic_8_oct_1909_zagreb_29_seismograms", 73.0, 6.5, "A", False, "DEEPER WAVES OVERTAKE SHALLOW", "Quality",
             "Quality: readable faces (British geologist Richard Dixon Oldham in 1900–1906 identifying P and S waves, dissolving to Croatian meteorologist Andrija Mohorovičić in Zagreb after the 8 October 1909 Pokupsko earthquake comparing smoked-paper seismograms from 29 European stations).",
             STYLE + "Split period scene: on the left in 1906, geologist Richard Dixon Oldham points to primary and secondary wave arrivals on a paper chart; on the right in Zagreb in 1909, Andrija Mohorovičić spreads twenty-nine smoked-paper seismograms across a long oak table." + QUAL_TAIL,
             {"kind": "WHO", "label": "Richard Dixon Oldham (1858–1936) — British geologist and seismologist", "fact_card": "Deeper waves overtake shallow", "when_stamp": "1900 · 1906 · 8 October 1909 · 1910 · 1970 · 1989", "timeline_step": "1/5 · 1906 (Richard Dixon Oldham identifies P-waves, S-waves, and a central Earth core) & 2/5 · 8 Oct 1909 (Andrija Mohorovičić discovers the 35 km crust-mantle Moho discontinuity after the Pokupsko earthquake near Zagreb)", "hold_s": 3.8}),
            ("02_mohorovicic_1909_crustal_5_6_km_s_vs_mantle_7_9_km_s_moho_35km_chart", 79.5, 8.0, "E", False, "8 OCT 1909 ZAGREB QUAKE: SHALLOW CRUST (5.6 KM/S) OVERTAKEN BEYOND 200 KM BY MANTLE (7.9 KM/S AT 35 KM MOHO)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked travel-time and depth diagram from Andrija Mohorovičić (1910, Potres od 8. X. 1909) shows direct crustal P-waves (~5.6 km/s) overtaken beyond 200 km epicentral distance by refracted mantle Pn-waves racing at ~7.9 km/s beneath the 35-kilometre Mohorovičić discontinuity (the Moho).",
             {"kind": "DATA", "label": "8 OCT 1909 MOHO DISCOVERY: CRUSTAL P-WAVES (5.6 KM/S) OVERTAKEN BEYOND 200 KM BY MANTLE (7.9 KM/S, 35 KM)", "detail": "Inked travel-time & depth diagram on period paper from Andrija Mohorovičić (1910, Potres od 8. X. 1909) showing direct crustal P-waves (~5.6 km/s) overtaken beyond 200 km epicentral distance by refracted mantle Pn-waves racing at ~7.9 km/s beneath the 35-kilometre Mohorovičić discontinuity (the Moho)", "scale": "just thirty-five kilometres beneath your shoes — the distance of a forty-minute motorway drive — the familiar granite and basalt of Earth's crust suddenly ends and the dense green rock of the mantle begins", "hold_s": 3.8}),
            ("03_wiechert_inverted_pendulum_seismograph_and_smoked_paper_stylus_closeup", 87.5, 6.5, "B", False, "8 OCTOBER 1909 — THE MOHO", "Fast",
             "Fast: daylight macro shot of a vintage brass-and-iron Wiechert seismograph drum where a fine metal stylus scratches a clean white wave trace across soot-blackened paper. Nothing emissive, no face.",
             STYLE + "In crisp daylight in an observatory room, a polished brass stylus arm traces a sharp white wave line across a revolving soot-blackened paper cylinder beside a brass pocket watch." + FAST_TAIL,
             None),
            ("04_granite_crust_specimen_vs_dense_green_peridotite_mantle_rock_samples_pan", 94.0, 5.5, "C", False, "35 KM — CRUST TO MANTLE", "Fast",
             "Fast: daylight close-up of two geological hand specimens on a museum tray: light speckled continental granite on the left and dense olive-green mantle peridotite beside brass balance weights on the right. Nothing emissive, no face.",
             STYLE + "In bright window light on a wooden museum tray, a pale speckled granite rock specimen sits beside a dense olive-green peridotite rock and polished brass scale weights." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — Beno Gutenberg's 1914 Shadow Zone at 2,890 Kilometres — Midpoint Twist",
        [
            ("01_gutenberg_1914_gottingen_shadow_zone_and_jeffreys_1926_liquid_core", 99.5, 6.5, "A", False, "MOLTEN IRON CORE BELOW", "Quality",
             "Quality: readable faces (24-year-old German seismologist Beno Gutenberg in Göttingen in 1914 plotting the 104°–140° P-wave shadow zone at 2,890 km depth, alongside British geophysicist Harold Jeffreys in Cambridge in 1926 proving the outer core is liquid molten metal).",
             STYLE + "Split period scene: on the left in a 1914 Göttingen observatory, young seismologist Beno Gutenberg uses brass dividers on a globe marked with a dark shadow band between 104 and 140 degrees; on the right in 1926 in Cambridge, Harold Jeffreys writes tidal rigidity equations at a blackboard." + QUAL_TAIL,
             {"kind": "WHO", "label": "Harold Jeffreys (1891–1989) — British mathematician and geophysicist", "fact_card": "Molten iron core below", "when_stamp": "1914 · 1926", "timeline_step": "3/5 · 1914–1926 (Beno Gutenberg maps the 2,890 km core-mantle boundary and 104°–140° shadow zone; Harold Jeffreys proves the outer core is liquid)", "hold_s": 3.8}),
            ("02_gutenberg_1914_2890km_core_mantle_boundary_104_140_shadow_zone_chart", 106.0, 8.0, "E", False, "2,890 KM GUTENBERG BOUNDARY: P-WAVES DROP 13.6 → 8.1 KM/S (104°–140° SHADOW ZONE) & S-WAVES STOP DEAD", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked global ray-path and shadow-zone diagram from Beno Gutenberg (1914) and Harold Jeffreys (1926) shows P-waves dropping from 13.6 km/s to 8.1 km/s at the 2,890 km core-mantle boundary (refracting inward to leave a 104°–140° P-wave shadow zone) while shear S-waves are blocked completely by the liquid iron outer core.",
             {"kind": "DATA", "label": "2,890 KM CORE BOUNDARY: P-WAVES DROP 13.6 → 8.1 KM/S (104°–140° SHADOW ZONE) · S-WAVES BLOCKED", "detail": "Inked global ray-path & shadow-zone diagram on period paper from Beno Gutenberg (1914) and Harold Jeffreys (1926) showing P-waves dropping from 13.6 km/s to 8.1 km/s at the 2,890 km core-mantle boundary (refracting inward to leave a 104°–140° P-wave shadow zone) while shear S-waves are blocked completely by the liquid iron outer core", "scale": "halfway to the centre of the Earth — two thousand eight hundred and ninety kilometres down — solid rock abruptly gives way to a roaring ocean of liquid iron wider than the planet Mars", "hold_s": 3.8}),
            ("03_spherical_glass_flask_water_lens_bending_light_beam_shadow_ring_demo", 114.0, 6.5, "B", False, "1914 — THE 2,890 KM SHADOW ZONE", "Fast",
             "Fast: daylight physics demonstration on an oak bench where a round water-filled glass flask refracts parallel painted rays on a paper board inward, leaving a dark shadow ring between 104 and 140 degrees. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a physics demonstration board painted with inked ray lines, a spherical water-filled glass flask sits at the centre of a wooden protractor ring marked from 104 to 140 degrees." + FAST_TAIL,
             None),
            ("04_gutenberg_1914_tables_brass_protractor_and_terrestrial_globe_pan", 120.5, 5.5, "C", False, "1914 — 2,890 KILOMETRES", "Fast",
             "Fast: daylight close-up of Beno Gutenberg's 1914 travel-time tables beside a brass semicircular protractor and a terrestrial globe on a wooden desk. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak desk, an open German geophysical journal of travel-time tables rests beside a brass protractor and a desktop terrestrial globe." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 17 June 1929 to 1936: Inge Lehmann's Oatmeal-Box Cards & the Paper Titled 'P\''",
        [
            ("01_inge_lehmann_1936_copenhagen_garden_oatmeal_cards_and_p_prime_paper", 126.0, 6.5, "A", False, "TWO-CHARACTER PAPER TITLE \"P'\"", "Quality",
             "Quality: readable face (48-year-old Danish seismologist Inge Lehmann in 1936 sitting in her Copenhagen garden with cardboard cards cut from oatmeal boxes, calculating the 1,220 km solid inner core from 17 June 1929 New Zealand earthquake traces and writing her paper titled 'P\'').",
             STYLE + "In a quiet 1936 Copenhagen garden, Danish seismologist Inge Lehmann sits at a wooden table surrounded by oatmeal-box cardboard cards covered in pencil calculations and writes the two-character title on a manuscript page." + QUAL_TAIL,
             {"kind": "FACT", "label": "Two-character paper title \"P'\"", "when_stamp": "17 June 1929 · 1936", "timeline_step": "4/5 · 17 Jun 1929–1936 (Inge Lehmann uses New Zealand earthquake traces in the shadow zone to discover the 1,220 km-radius inner core in her paper 'P\'')", "hold_s": 3.8}),
            ("02_lehmann_1936_p_prime_inner_core_1220km_reflection_into_shadow_zone_chart", 132.5, 8.0, "E", False, "1936 'P\'' PAPER: 1,220 KM SOLID INNER CORE (~11.2 KM/S) DEFLECTS WAVES INTO 104°–140° SHADOW ZONE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked inner-core reflection and refraction diagram from Inge Lehmann's 1936 paper 'P\'' shows PKiKP and PKIKP seismic rays from the 17 June 1929 New Zealand earthquake bouncing off and speeding through the 1,220 km-radius inner core (~11.2 km/s) to arrive inside the 104°–140° shadow zone at 19–20 minutes travel time.",
             {"kind": "DATA", "label": "1936 'P\'' DISCOVERY: 1,220 KM INNER CORE (~11.2 KM/S) BOUNCES WAVES INTO 104°–140° SHADOW ZONE", "detail": "Inked inner-core reflection & refraction diagram on period paper from Inge Lehmann's 1936 paper 'P\'' showing PKiKP and PKIKP seismic rays from the 17 June 1929 New Zealand earthquake bouncing off and speeding through the 1,220 km-radius inner core (~11.2 km/s) to arrive inside the 104°–140° shadow zone at 19–20 minutes travel time", "scale": "working alone in her garden with cardboard cards cut from oatmeal boxes, Inge Lehmann discovered a metal sphere inside the Earth nearly three-quarters the size of the Moon", "hold_s": 3.8}),
            ("03_oatmeal_cardboard_index_cards_slide_rule_and_1936_p_prime_offprint_closeup", 140.5, 6.5, "B", False, "1936 — INGE LEHMANN'S \"P'\"", "Fast",
             "Fast: daylight macro shot of Inge Lehmann's hand-cut oatmeal-cardboard calculation cards, an ivory slide rule, and her 1936 seismic offprint on a wooden garden table. Nothing emissive, no face.",
             STYLE + "In bright daylight on a wooden garden table, hand-cut tan cardboard index cards neatly pencilled with wave arrival times sit beside an ivory slide rule and a printed booklet." + FAST_TAIL,
             None),
            ("04_explorer_placing_solid_silver_ball_inside_glass_bowl_to_deflect_marble", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing at a wooden demonstration table where rolling brass marbles miss a target band around a glass bowl, the Explorer places a solid silver sphere at the centre of the bowl so a rolling marble bounces off the sphere straight into the shadow band." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why the Inner Core Is Solid, How It Powers Earth's Magnetic Shield & Why Coffee Keeps You Awake",
        [
            ("01_timeline_1906_1971_and_3_6m_atm_5400c_solid_inner_core_geodynamo_chart", 152.5, 8.5, "E", False, "1906–1971 TIMELINE · 3.6 MILLION ATM (360 GPA) AT 5,400 °C · SOLID IRON-NICKEL GEODYNAMO", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 5-date timeline completes: 1906 (Richard Dixon Oldham identifies P-waves, S-waves, and a central Earth core) · 8 Oct 1909 (Andrija Mohorovičić discovers the 35 km crust-mantle Moho discontinuity after the Pokupsko earthquake near Zagreb) · 1914–1926 (Beno Gutenberg maps the 2,890 km core-mantle boundary and 104°–140° shadow zone; Harold Jeffreys proves the outer core is liquid) · 17 Jun 1929–1936 (Inge Lehmann uses New Zealand earthquake traces in the shadow zone to discover the 1,220 km-radius inner core in her paper 'P\'') · 1940–1971 (Francis Birch and normal-mode oscillations prove 3.6 million atmospheres of pressure compress the 5,400 °C inner core into solid iron-nickel).",
             {"kind": "DATA", "label": "1906–1971 TIMELINE · 3.6 MILLION ATM (360 GPA) AT 5,400 °C LOCKS SOLID INNER CORE & MAGNETIC SHIELD", "detail": "Animated 5-date timeline (1906 → 1940–1971) alongside Francis Birch's 3.6 million atmospheres (360 GPa) inner-core pressure freezing 5,400 °C iron-nickel into a solid sphere that drives Earth's magnetic dynamo", "scale": "at the centre of the Earth, three point six million atmospheres of pressure — like stacking three thousand six hundred Eiffel Towers on your thumbnail — squeezes five-thousand-degree iron into a solid crystal ball", "who_card": "Francis Birch (1903–1992) — American geophysicist", "fact_card": "Lived to age 104", "when_stamp": "1940 · 1952 · 1971 · 1993 · 1906–1971", "timeline_step": "5/5 · 1940–1971 (Francis Birch and normal-mode oscillations prove 3.6 million atmospheres of pressure compress the 5,400 °C inner core into solid iron-nickel)", "hold_s": 3.8}),
            ("02_iron_nickel_meteorite_sphere_and_magnetic_compass_lines_model", 161.0, 5.5, "A", False, "PRESSURE BEATS TEMPERATURE", "Fast",
             "Fast: daylight cutaway museum model of Earth's solid iron-nickel inner core surrounded by curved brass magnetic field lines and a compass needle on a wooden plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a museum plinth, a polished iron-nickel sphere sits at the centre of a cutaway wooden globe surrounded by arched brass wire magnetic field lines and a brass compass." + FAST_TAIL,
             None),
            ("03_goethe_and_runge_3_oct_1819_jena_mocha_coffee_beans_caffeine_handoff", 166.5, 6.5, "C", False, "MOCHA BEANS TO BRAIN RECEPTORS", "Quality",
             "Quality: readable faces (on 3 October 1819 in Jena, Germany, 70-year-old poet Johann Wolfgang von Goethe hands a wooden box of rare Arabian mocha coffee beans to 25-year-old chemist Friedlieb Ferdinand Runge beside a flask of white caffeine needles and Solomon Snyder & John Daly's May 1981 adenosine-receptor model — handoff to 045 Caffeine & Adenosine).",
             STYLE + "In an 1819 German study in Jena, seventy-year-old poet Johann Wolfgang von Goethe in a dark coat hands a small wooden box of roasted coffee beans to young chemist Friedlieb Ferdinand Runge beside a glass dish of white needle crystals." + QUAL_TAIL,
             {"kind": "WHEN", "label": "3 OCTOBER 1819 · MAY 1981", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_wiechert_seismograph_drum_cutaway_core_globe_oatmeal_cards (callback, £0).",
             "Reuse P1:07_table_three_props_wiechert_seismograph_drum_cutaway_core_globe_oatmeal_cards [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
             None),
        ],
    ),
]


def main() -> None:
    per_part_summary = []
    all_parts = []
    cum_flow = 0
    cum_vx = 0.0
    overlay_count = 0

    for p_idx, p_title, rows_spec in PARTS_SPEC:
        plates = []
        p_counts = {
            "rows": 0,
            "Quality": 0,
            "Fast": 0,
            "code_graphic": 0,
            "reuse": 0,
            "flow_credits_try1": 0,
            "flow_credits_expected": 0,
            "vertex_try1_gbp": 0.0,
            "vertex_expected_gbp": 0.0,
        }
        for (rid, t_s, use_s, fam, exp_flag, lbl, qual, reason, prompt, overlay) in rows_spec:
            priced = price_row(qual, use_s)
            cum_flow += priced["flow_credits_expected"]
            cum_vx = round(cum_vx + priced["vertex_expected_gbp"], 2)

            row = {
                "id": rid,
                "t": fmt_t(t_s),
                "t_s": round(t_s, 2),
                "use_s": round(use_s, 2),
                "family": fam,
                "explorer": exp_flag,
                "character_reference": (
                    "01_Character/02_Explorer-Lock/explorer_ turnaround_sheet.png"
                    if exp_flag
                    else None
                ),
                "side_label": lbl,
                "quality": qual,
                "quality_reason": reason,
                "generation_authorized": False,
                "prompt": prompt if qual in ("Quality", "Fast") else None,
                "reference": prompt if qual not in ("Quality", "Fast") else None,
            }
            if overlay:
                row["teach_overlay"] = overlay
                overlay_count += 1
            if qual == "reuse":
                row["reuse_of"] = "P1:07_table_three_props_wiechert_seismograph_drum_cutaway_core_globe_oatmeal_cards"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_wiechert_seismograph_drum_cutaway_core_globe_oatmeal_cards",
                    "source_raw_s": 8.0,
                    "source_usable_s": 7.9,
                    "source_used_s": 5.5,
                    "unused_usable_s": 2.4,
                    "required_use_s": 2.4,
                    "shortfall_usable_s": 0.0,
                    "distinct_window": True,
                    "window_s": [5.5, 7.9],
                    "resolution": "verified_unused_tail_reuse",
                }
            row.update(priced)
            row["cum_flow_credits_expected"] = cum_flow
            row["cum_vertex_expected_gbp"] = cum_vx
            plates.append(row)

            p_counts["rows"] += 1
            p_counts[qual] += 1
            p_counts["flow_credits_try1"] += priced["flow_credits_try1"]
            p_counts["flow_credits_expected"] += priced["flow_credits_expected"]
            p_counts["vertex_try1_gbp"] = round(p_counts["vertex_try1_gbp"] + priced["vertex_try1_gbp"], 2)
            p_counts["vertex_expected_gbp"] = round(p_counts["vertex_expected_gbp"] + priced["vertex_expected_gbp"], 2)

        part_doc = {
            "film": "044_Mohorovicic-Gutenberg-Lehmann-Earth-Core",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from earth_core_script_master_v01.md; retimes onto Scribe STT once VO locks)",
            "mint": False,
            "summary": {"part": p_idx, "title": p_title, **p_counts},
            "plates": plates,
        }
        (OUT / f"part-{p_idx:02d}_plates_v01.json").write_text(json.dumps(part_doc, indent=2) + "\n")
        per_part_summary.append({"part": p_idx, "title": p_title, **p_counts})
        all_parts.append(part_doc)

    totals = {
        "rows": sum(p["rows"] for p in per_part_summary),
        "Quality": sum(p["Quality"] for p in per_part_summary),
        "Fast": sum(p["Fast"] for p in per_part_summary),
        "code_graphic": sum(p["code_graphic"] for p in per_part_summary),
        "reuse": sum(p["reuse"] for p in per_part_summary),
        "flow_credits_try1": sum(p["flow_credits_try1"] for p in per_part_summary),
        "flow_credits_expected": sum(p["flow_credits_expected"] for p in per_part_summary),
        "vertex_try1_gbp": round(sum(p["vertex_try1_gbp"] for p in per_part_summary), 2),
        "vertex_expected_gbp": round(sum(p["vertex_expected_gbp"] for p in per_part_summary), 2),
        "explorer": 2,
        "teach_overlays": overlay_count,
    }

    plan = {
        "film": "044_Mohorovicic-Gutenberg-Lehmann-Earth-Core",
        "version": "v01",
        "date": "2026-10-18",
        "owner": "gemini (J0555)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/044_Mohorovicic-Gutenberg-Lehmann-Earth-Core/earth_core_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/044_Mohorovicic-Gutenberg-Lehmann-Earth-Core/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044. Nothing in 044 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 044 Earth's Inner Core: How Earthquakes X-Rayed Our Planet — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 18 Oct 2026, J0555. Built from `earth_core_script_master_v01.md` (`93.0 PASS`) and `SOURCES_v01.md`.",
        "**No mint, no spend.** Pre-VO clock timings (`175.4 s` base picture grid; re-times automatically onto Scribe word timestamps once long VO locks).",
        "",
    ]
    for pdoc in all_parts:
        sl.append(f"## {pdoc['title']}")
        sl.append("")
        sl.append("| Row | Start | Dur (s) | Route / Model | Side label / Teach overlay | Prompt / Source |")
        sl.append("|---|---:|---:|---|---|---|")
        for r in pdoc["plates"]:
            rm = r.get("flow_model") or r.get("route")
            lbl = r.get("side_label") or ""
            if "teach_overlay" in r:
                lbl = f"{lbl} (`{r['teach_overlay']['kind']}`)".strip()
            pr = (r.get("prompt") or r.get("reference") or "")[:115] + "…"
            sl.append(f"| `P{pdoc['part']}:{r['id']}` | {r['t']} | {r['use_s']:.2f} | {rm} | {lbl} | {pr} |")
        sl.append("")
    (EDIT / "SHOT_LIST_v01.md").write_text("\n".join(sl) + "\n")

    pr_lines = [
        "# 044 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 18 Oct 2026, J0555. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `earth_core_script_master_v01.md` (`93.0 PASS`) and `SOURCES_v01.md` so 044's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
        "",
        "## Totals (base 25-row board before VO continuation splits)",
        "",
        "| Part | Title | Rows | Quality | Fast | £0 code | £0 reuse | Flow try-1 | Flow expected | Vertex try-1 | Vertex expected |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for p in per_part_summary:
        pr_lines.append(
            f"| Part 0{p['part']} | {p['title']} | {p['rows']} | {p['Quality']} | {p['Fast']} | {p['code_graphic']} | {p['reuse']} | {p['flow_credits_try1']} | {p['flow_credits_expected']} | £{p['vertex_try1_gbp']:.2f} | £{p['vertex_expected_gbp']:.2f} |"
        )
    pr_lines.append(
        f"| **Film** | | **{totals['rows']}** | **{totals['Quality']}** | **{totals['Fast']}** | **{totals['code_graphic']}** | **{totals['reuse']}** | **{totals['flow_credits_try1']}** | **{totals['flow_credits_expected']}** | **£{totals['vertex_try1_gbp']:.2f}** | **£{totals['vertex_expected_gbp']:.2f}** |"
    )
    pr_lines.extend([
        "",
        "## Route breakdown",
        "",
        f"- **Quality ({totals['Quality']} rows):** readable faces (Inge Lehmann, Andrija Mohorovičić, Richard Dixon Oldham, Beno Gutenberg, Harold Jeffreys, Johann Wolfgang von Goethe, Friedlieb Ferdinand Runge), 1936 Copenhagen garden study scenes, 1909 Zagreb observatory, 1914 Göttingen & 1926 Cambridge scenes, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (coiled brass spring, braided rope & smoked-paper seismogram pan, 3-object callback bench, Wiechert smoked-paper seismograph drum & stylus, continental granite vs dense green mantle peridotite rock specimens, spherical water-filled flask shadow-zone refraction demo, Gutenberg's 1914 travel-time tables & brass protractor, Lehmann's oatmeal-cardboard index cards & ivory slide rule, solid iron-nickel inner core & brass magnetic field lines model). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_kola_borehole_12_2km_vs_moho_35km_gutenberg_2890km_and_lehmann_1220km_core_chart` — Kola Superdeep Borehole (12.2 km = 0.19% of 6,371 km radius) vs Earth's seismic layers: ~35 km Moho, 2,890 km Gutenberg liquid core boundary, and 1,220 km solid inner core (`SCALE: if the Earth were the size of an apple, the deepest hole humans have ever drilled wouldn't even pierce a twentieth of the apple's skin — yet earthquake waves let us see all the way to the pips at the centre`)",
        "  2. `P1:06_p_wave_compressional_8_13_km_s_vs_s_wave_shear_blocked_at_2890km_liquid_core_chart` — compressional P-waves (8–13 km/s, solid + liquid, 20-minute trans-Earth transit) vs shear S-waves (4.5–7 km/s, blocked at 2,890 km depth) (`SCALE: an earthquake shockwave races all the way through the centre of the Earth from New Zealand to Denmark in just twenty minutes — faster than twenty times the speed of sound`)",
        "  3. `P2:02_mohorovicic_1909_crustal_5_6_km_s_vs_mantle_7_9_km_s_moho_35km_chart` — Mohorovičić's 8 October 1909 Zagreb travel-time curve (~5.6 km/s crustal P-waves overtaken beyond 200 km by ~7.9 km/s mantle Pn-waves beneath the 35 km Moho) (`SCALE: just thirty-five kilometres beneath your shoes — the distance of a forty-minute motorway drive — the familiar granite and basalt of Earth's crust suddenly ends and the dense green rock of the mantle begins`)",
        "  4. `P3:02_gutenberg_1914_2890km_core_mantle_boundary_104_140_shadow_zone_chart` — Gutenberg's 1914 2,890 km core-mantle boundary (P-wave drop 13.6 → 8.1 km/s, 104°–140° P-wave shadow zone, total S-wave block) (`SCALE: halfway to the centre of the Earth — two thousand eight hundred and ninety kilometres down — solid rock abruptly gives way to a roaring ocean of liquid iron wider than the planet Mars`)",
        "  5. `P4:02_lehmann_1936_p_prime_inner_core_1220km_reflection_into_shadow_zone_chart` — Inge Lehmann's 1936 *'P\''* inner-core reflection/refraction into the 104°–140° shadow zone at 1,220 km radius from the 17 June 1929 New Zealand quake (`SCALE: working alone in her garden with cardboard cards cut from oatmeal boxes, Inge Lehmann discovered a metal sphere inside the Earth nearly three-quarters the size of the Moon`)",
        "  6. `P5:01_timeline_1906_1971_and_3_6m_atm_5400c_solid_inner_core_geodynamo_chart` — completed 5-date timeline (1906 → 1940–1971) + Francis Birch's 3.6 million atm (360 GPa) inner-core pressure freezing 5,400 °C iron-nickel into a solid sphere that powers Earth's magnetic shield (`SCALE: at the centre of the Earth, three point six million atmospheres of pressure — like stacking three thousand six hundred Eiffel Towers on your thumbnail — squeezes five-thousand-degree iron into a solid crystal ball`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_wiechert_seismograph_drum_cutaway_core_globe_oatmeal_cards`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"044 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
