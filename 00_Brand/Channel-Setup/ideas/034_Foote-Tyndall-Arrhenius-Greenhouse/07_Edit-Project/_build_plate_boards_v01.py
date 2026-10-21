#!/usr/bin/env python3
"""HOS 034 (The Greenhouse Effect: The Forgotten 1856 Sunlit Tube Experiment) pre-VO plate boards v01. J0494. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/034_Foote-Tyndall-Arrhenius-Greenhouse/greenhouse_script_master_v01.md
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
        "Part 01 — The Sunlit Glass Cylinders in New York and the Brass Tube in London",
        [
            ("01_foote_1856_sunlit_glass_cylinders_and_tyndall_1859_rock_salt_tube", 0.0, 5.5, "A", False, "WHY EARTH ISN'T FROZEN", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + in a sunlit garden in Seneca Falls, New York, in summer 1856, 37-year-old Eunice Newton Foote watches the mercury thermometer inside a 30-inch glass cylinder filled with carbon dioxide climb to 125 °F while an identical cylinder of ordinary air stays 19 °F cooler, dissolving to the basement of the Royal Institution in London on 18 May 1859 as John Tyndall fires invisible infrared heat through a brass tube sealed with rock-salt lenses.",
             STYLE + "In a sunlit garden in Seneca Falls in summer 1856, scientist Eunice Newton Foote in an 1850s dress inspects two thirty-inch glass cylinders fitted with mercury thermometers, dissolving to the Royal Institution basement in London in May 1859 as physicist John Tyndall adjusts a four-foot brass tube sealed with rock-salt plates." + QUAL_TAIL,
             {"kind": "WHEN", "label": "SENECA FALLS, SUMMER 1856 · LONDON, 18 MAY 1859", "timeline_step": "2/5 · 23 Aug 1856 (Eunice Foote's sunlit CO₂ cylinder experiments) & 3/5 · 18 May 1859 (John Tyndall's rock-salt infrared tube)", "hold_s": 3.5}),
            ("02_foote_cylinders_tyndall_spectrophotometer_arrhenius_ledger_split", 5.5, 6.0, "B", False, "TUBES, INFRARED, ICE AGES", "Quality",
             "Quality: complex three-part split composition (Eunice Newton Foote's 1856 sunlit glass cylinders and mercury thermometers on the left; John Tyndall's 1859 brass infrared ratio spectrophotometer at the Royal Institution in the centre; Svante Arrhenius's 1895–1896 ledger of 10,000 pencil calculations in Stockholm on the right).",
             STYLE + "Three-panel period composition: on the left, two tall sunlit glass cylinders with mercury thermometers; in the centre, a four-foot brass spectrophotometer tube with rock-salt windows and a brass galvanometer; on the right, stacks of handwritten calculation ledgers beside a terrestrial globe." + QUAL_TAIL,
             None),
            ("03_albany_23_august_1856_aaas_joseph_henry_reading_foote_paper", 11.5, 6.0, "C", False, "BARRED FROM THE PODIUM", "Quality",
             "Quality: readable faces (inside the Eighth Annual Meeting of the American Association for the Advancement of Science in Albany on 23 August 1856, Smithsonian Secretary Joseph Henry stands at the podium reading Eunice Newton Foote's manuscript while Foote watches from the benches).",
             STYLE + "Inside an 1856 lecture hall in Albany, New York, bearded professor Joseph Henry reads a manuscript aloud at a wooden podium while Eunice Newton Foote sits attentively in the front audience row." + QUAL_TAIL,
             {"kind": "WHEN", "label": "ALBANY, 23 AUGUST 1856", "hold_s": 3.5}),
            ("04_99_percent_n2_o2_vs_trace_co2_h2o_33c_warming_chart", 17.5, 8.0, "E", False, "99% N₂/O₂ (0% IR) VS TRACE CO₂ & H₂O (+33 °C WARMING)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked atmospheric-composition and heat-trapping chart shows visible sunlight warming the ground and outgoing thermal infrared escaping freely through 99% of dry air (78% N₂ + 21% O₂ = 0% IR absorption) while trace water vapour and carbon dioxide (~0.04% / 4 in 10,000 molecules) absorb and re-radiate infrared, raising Earth's average surface temperature by ~33 °C (from −18 °C to +15 °C).",
             {"kind": "DATA", "label": "99% N₂ + O₂ (TRANSPARENT TO IR) VS TRACE CO₂ & H₂O (−18 °C → +15 °C = +33 °C)", "detail": "Inked atmospheric-composition & heat-trapping chart on period paper showing 99% of dry air (78% N₂ + 21% O₂) absorbing 0% of outgoing thermal infrared vs trace CO₂ (~0.03%–0.04%) and water vapour raising Earth's average temperature by ~33 °C (from −18 °C to +15 °C)", "scale": "carbon dioxide makes up just four molecules out of every ten thousand in dry air — yet together with water vapour it keeps Earth thirty-three degrees Celsius warmer than a frozen bare rock", "who_card": "Eunice Newton Foote (1819–1888) — American scientist and inventor · John Tyndall (1820–1893) — Irish experimental physicist · Svante Arrhenius (1859–1927) — Swedish physical chemist", "when_stamp": "23 August 1856 · 18 May 1859 · April 1896", "hold_s": 3.8}),
            ("05_foote_30_inch_glass_cylinders_and_brass_air_pump_pan", 25.5, 5.5, "A", False, "SENECA FALLS, 1856", "Fast",
             "Fast: daylight macro pan across Eunice Foote's brass reciprocating air pump, stopcocks, and two 30-inch glass receivers fitted with mercury thermometers on a sunlit wooden table between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a garden table, the camera pans across a brass piston air pump, brass stopcocks, and two thirty-inch glass cylinders containing mercury thermometers." + FAST_TAIL,
             None),
            ("06_10000_molecule_grid_9900_n2_o2_vs_4_co2_molecules_card", 31.0, 8.0, "E", False, "4 IN 10,000 MOLECULES", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked 10,000-molecule grid compares 7,808 nitrogen and 2,095 oxygen molecules (transparent to thermal infrared) against ~3–4 carbon dioxide molecules per 10,000 (~280–420 ppm) trapping outgoing infrared waves.",
             {"kind": "DATA", "label": "4 MOLECULES IN 10,000 (~0.04% CO₂) TRAPPING OUTGOING INFRARED HEAT", "detail": "Inked 10,000-molecule grid comparing 7,808 nitrogen + 2,095 oxygen molecules (transparent to infrared) vs ~3–4 carbon dioxide molecules per 10,000 (~280–420 ppm)", "scale": "four molecules in ten thousand is like four drops of ink in a five-gallon bucket of water — yet those four molecules block infrared heat that passes straight through the other nine thousand nine hundred", "hold_s": 3.8}),
            ("07_table_three_props_foote_cylinders_tyndall_rock_salt_arrhenius_ledger", 39.0, 5.5, "C", False, "1856 TO 1896", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Eunice Foote's glass cylinder and thermometer, John Tyndall's polished rock-salt lens mount and brass tube section, and Svante Arrhenius's handwritten calculation ledger and pencil). Nothing emissive.",
             STYLE + "On a wooden workbench in soft window light sit three objects side by side: a tall glass cylinder with a mercury thermometer, a brass lens holder fitted with a clear rock-salt crystal plate, and an open ledger of handwritten tables beside a wooden pencil." + FAST_TAIL,
             None),
            ("08_explorer_oxygen_dumbbells_vs_vibrating_co2_tuning_fork", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing between a miniature Sun model and a tiny spinning Earth globe, the Explorer lets yellow sunbeams pass past a pair of two-ball oxygen models, then holds up a three-ball carbon dioxide molecule model that vibrates like a tuning fork when an outgoing red wave hits it and warms its hands." + EXP_TAIL,
             None),
            ("09_foote_november_1856_printed_journal_page_and_thermometer", 67.5, 5.5, "B", False, "NOVEMBER 1856 JOURNAL", "Quality",
             "Quality: readable face (Eunice Newton Foote in late 1856 holding the printed November 1856 issue of The American Journal of Science and Arts beside her glass cylinder and thermometer).",
             STYLE + "In her study in November 1856, scientist Eunice Newton Foote holds an open printed scientific journal beside her tall glass cylinder and mercury thermometer." + QUAL_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — Fourier's Frozen Earth, Agassiz's Ice Age & Eunice Foote's 1856 Glass Cylinders",
        [
            ("01_fourier_1824_paris_agassiz_1837_alps_and_foote_1856_cylinders", 73.0, 6.5, "A", False, "FORGOTTEN FOR 155 YEARS", "Quality",
             "Quality: readable faces (French mathematician Joseph Fourier in Paris in 1824 calculating Earth's heat balance, Swiss geologist Louis Agassiz in July 1837 examining glacier-scratched Alpine boulders, and Eunice Newton Foote in summer 1856 pumping carbon dioxide into a 30-inch glass cylinder).",
             STYLE + "Split period scene: on the left, French mathematician Joseph Fourier in an 1820s coat writes heat equations beside a globe while Swiss geologist Louis Agassiz inspects a glacier-scarred boulder; on the right, Eunice Newton Foote pumps carbon dioxide gas into a sunlit glass cylinder." + QUAL_TAIL,
             {"kind": "WHO", "label": "Joseph Fourier (1768–1830) — French mathematician and physicist · Louis Agassiz (1807–1873) — Swiss-American geologist", "fact_card": "Forgotten for 155 years", "when_stamp": "1824 · 24 July 1837 · November 1856 · 2011", "timeline_step": "1/5 · 1824–1827 & 24 Jul 1837 (Fourier calculates dark-heat blanket; Agassiz proposes Ice Ages)", "hold_s": 3.8}),
            ("02_foote_1856_thermometer_chart_dry_damp_air_and_125f_co2", 79.5, 8.0, "E", False, "DRY AIR (96 °F) VS DAMP AIR (108 °F) · COMMON AIR (106 °F) VS CO₂ (125 °F)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked thermometer chart from Eunice Foote's November 1856 paper compares dry air (96 °F / 35.6 °C) vs damp air (108 °F / 42.2 °C), and ambient air (106 °F / 41.1 °C) vs carbonic acid gas / CO₂ (125 °F / 51.7 °C, +19 °F hotter) in sunlit 30-inch glass cylinders.",
             {"kind": "DATA", "label": "FOOTE'S 1856 CYLINDERS: COMMON AIR (106 °F) VS CARBONIC ACID GAS / CO₂ (125 °F)", "detail": "Inked thermometer chart on period paper from Eunice Foote's November 1856 paper comparing dry air (96 °F) vs damp air (108 °F), and ambient air (106 °F) vs carbonic acid gas / CO₂ (125 °F / 51.7 °C) in sunlit 30-inch glass cylinders", "scale": "inside a 30-inch glass tube in the New York sun, carbon dioxide climbed 19 degrees Fahrenheit hotter than ordinary air — the first experimental clue to how changing air changes Earth's climate", "hold_s": 3.8}),
            ("03_foote_two_30_inch_glass_receivers_mercury_climbing_to_125f", 87.5, 6.5, "B", False, "125 °F IN CARBONIC ACID GAS", "Fast",
             "Fast: daylight close-up of Eunice Foote's two 30-inch glass receivers standing side by side in bright sunlight as the silver mercury column inside the carbon dioxide tube rises higher than the air tube. Nothing emissive, no face.",
             STYLE + "In crisp sunlight on a wooden garden bench, two identical thirty-inch glass cylinders stand side by side with silver mercury thermometers inside, one mercury column visibly higher than the other." + FAST_TAIL,
             None),
            ("04_alpine_glacier_polished_erratic_boulder_with_parallel_scratches", 94.0, 5.5, "C", False, "NEUCHÂTEL · 24 JULY 1837", "Fast",
             "Fast: daylight close-up of a huge granite erratic boulder in a green Swiss Alpine valley scored with deep parallel glacial striations beside a retreating valley glacier. Nothing emissive, no face.",
             STYLE + "In bright Alpine daylight, a massive granite boulder sits in a green valley, its polished stone face carved with parallel glacial scratch lines beneath snowy peaks." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — John Tyndall's 1859 Rock-Salt Spectrophotometer & the 99% Shock",
        [
            ("01_tyndall_1859_royal_institution_rock_salt_spectrophotometer", 99.5, 6.5, "A", False, "ROYAL INSTITUTION · 18 MAY 1859", "Quality",
             "Quality: readable face (Irish physicist John Tyndall in the basement of the Royal Institution in London on 18 May 1859 – 7 February 1861 adjusting his four-foot brass ratio spectrophotometer tube fitted with rock-salt windows and a boiling-water Leslie cube).",
             STYLE + "In the Royal Institution basement in London on 18 May 1859, sideburned Irish physicist John Tyndall in a Victorian waistcoat adjusts a four-foot horizontal brass tube fitted with clear rock-salt crystal endplates and a copper hot-water cube." + QUAL_TAIL,
             {"kind": "FACT", "label": "99% of air traps no heat", "when_stamp": "18 May 1859 · 7 February 1861", "timeline_step": "3/5 · 18 May 1859 (John Tyndall's rock-salt spectrophotometer proves H₂O and CO₂ absorb infrared)", "hold_s": 3.8}),
            ("02_tyndall_1859_1861_infrared_absorption_bar_chart_n2_o2_vs_co2", 106.0, 8.0, "E", False, "RELATIVE IR ABSORPTION: N₂ (1) · O₂ (1) VS CO₂ (90) · N₂O (355) · COAL GAS (>1,000)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked spectrophotometer schematic and bar chart from John Tyndall's 1859–1861 Royal Society experiments compares relative infrared absorption at 1 atmosphere: Nitrogen (1), Oxygen (1), Dry Air (1) vs Carbon Dioxide (90), Nitrous Oxide (355), and Coal Gas (>1,000), alongside humid air absorbing ~70× more thermal radiation than dry air.",
             {"kind": "DATA", "label": "TYNDALL'S IR ABSORPTION CHART: N₂/O₂ (1) VS CO₂ (90) & HUMID AIR (~70×)", "detail": "Inked spectrophotometer diagram & bar chart on period paper from Tyndall's 1859–1861 Royal Society experiments comparing relative infrared absorption at 1 atm: Nitrogen (1), Oxygen (1), Dry Air (1) vs Carbon Dioxide (90), Nitrous Oxide (355), and Coal Gas (>1,000), alongside humid air (~70× dry air)", "scale": "pound for pound, a three-atom molecule of carbon dioxide or water vapour absorbs thousands of times more infrared heat than the two-atom oxygen and nitrogen molecules that make up 99% of every breath you take", "hold_s": 3.8}),
            ("03_tyndall_opening_co2_stopcock_as_galvanometer_needle_swings", 114.0, 6.5, "B", False, "18 MAY 1859 — ROCK-SALT TUBE", "Quality",
             "Quality: readable face and hands (John Tyndall on 18 May 1859 opening a brass stopcock to let trace carbon dioxide into the rock-salt tube and watching the galvanometer needle swing wildly across the dial).",
             STYLE + "In the Royal Institution laboratory on 18 May 1859, John Tyndall turns a brass stopcock on a glass gas bag feeding his brass spectrophotometer tube and leans over a dial as the brass galvanometer needle swings sharply." + QUAL_TAIL,
             None),
            ("04_polished_rock_salt_crystal_lens_and_copper_leslie_cube_closeup", 120.5, 5.5, "C", False, "ROCK-SALT WINDOWS", "Fast",
             "Fast: daylight macro shot of a transparent cleaved block of rock salt beside a polished circular rock-salt window mounted on the end of Tyndall's four-foot brass tube and a matte copper Leslie cube. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a laboratory bench, a clear cubic crystal of rock salt sits beside a circular rock-salt lens mounted on a brass tube flange and a matte copper water cube." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — Svante Arrhenius's 10,000 Hand Calculations & the Coal Twist — Midpoint Twist",
        [
            ("01_arrhenius_1895_stockholm_10000_hand_calculations_lamplight", 126.0, 6.5, "A", False, "STOCKHOLM · 1894–1896 · 10,000 SUMS", "Quality",
             "Quality: lamplit scene + readable face (Swedish physical chemist Svante Arrhenius in Stockholm between Christmas Eve 1894 and April 1896 working by lamplight through stacks of handwritten ledger sheets completing 10,000 to 100,000 pencil calculations).",
             STYLE + "In a Stockholm study in 1895, Swedish chemist Svante Arrhenius in pince-nez glasses writes rows of pencil figures across tall stacks of ledger sheets by the warm light of a brass oil lamp." + QUAL_TAIL,
             {"kind": "FACT", "label": "10,000 sums done by hand", "when_stamp": "April 1896 · 1903 · 1908 · May 1967", "timeline_step": "4/5 · Apr 1896 (Svante Arrhenius's 10,000 hand calculations quantify CO₂ warming & Ice Age cooling)", "hold_s": 3.8}),
            ("02_arrhenius_1896_co2_halving_doubling_curve_vs_manabe_1967_chart", 132.5, 8.0, "E", False, "0.5× CO₂ (−4 TO −5 °C ICE AGE) · 2.0× CO₂ (+5 TO +6 °C VS MANABE 1967 +2.3–3 °C)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked calculation table and curve from Svante Arrhenius's April 1896 paper shows global temperature change vs atmospheric CO₂ multiplier: 0.67× CO₂ → −3.2 °C; 0.5× CO₂ (halved) → −4 to −5 °C (Ice Age); 1.0× CO₂ → baseline; and 2.0× CO₂ (doubled) → +5 to +6 °C, compared alongside Syukuro Manabe and Richard Wetherald's May 1967 computer model (+2.3 to +3.0 °C).",
             {"kind": "DATA", "label": "ARRHENIUS (APRIL 1896): 0.5× CO₂ (−4 TO −5 °C) & 2× CO₂ (+5 TO +6 °C VS 1967 +2.3–3 °C)", "detail": "Inked calculation table & curve on period paper from Svante Arrhenius's April 1896 paper showing 0.5× CO₂ → −4 to −5 °C (Ice Age) and 2.0× CO₂ → +5 to +6 °C, compared with Manabe & Wetherald's May 1967 computer model (+2.3 to +3.0 °C)", "scale": "working only with pencil and paper in 1895, Arrhenius calculated a warming curve for doubled carbon dioxide within two degrees of today's fastest supercomputers", "hold_s": 3.8}),
            ("03_arrhenius_april_1896_table_vii_and_1908_coal_chimneys", 140.5, 6.5, "B", False, "APRIL 1896 — FIRST CLIMATE MODEL", "Quality",
             "Quality: readable face (Svante Arrhenius in Stockholm in April 1896 holding his published Philosophical Magazine paper beside his 1908 book Worlds in the Making, with smoky Victorian industrial coal chimneys outside the window).",
             STYLE + "In Stockholm in 1896, Svante Arrhenius holds open his printed scientific paper of latitude tables beside a window overlooking nineteenth-century brick factory chimneys puffing dark coal smoke into the sky." + QUAL_TAIL,
             None),
            ("04_explorer_abacus_10000_sums_sliding_co2_lever_half_to_double", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Sitting behind a mountain of yellowed ledger pages with a tiny pencil worn down to a stub, the Explorer tallies a final bead on a wooden abacus, slides a brass lever on a globe stand left as frost coats the continents, then slides it right as the frost melts away." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why a Real Garden Greenhouse Works Differently & the $1 Medical Miracle",
        [
            ("01_timeline_1824_1958_and_keeling_mauna_loa_315_to_420_ppm_chart", 152.5, 8.5, "E", False, "1824–1958 TIMELINE & KEELING CURVE (280 → 315 → >420 PPM CO₂)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 5-date timeline completes: 1824–1827 & 24 Jul 1837 (Fourier & Agassiz) · 23 Aug 1856 (Eunice Foote's sunlit CO₂ cylinders) · 18 May 1859 (John Tyndall's rock-salt spectrophotometer) · Apr 1896 (Svante Arrhenius's 10,000 hand calculations) · Mar 1958–present (Charles David Keeling's Mauna Loa curve rising from 315 ppm to >420 ppm), alongside an inked comparison of a glass garden roof (blocking convection) vs Earth's infrared radiative blanket.",
             {"kind": "DATA", "label": "1824–1958 TIMELINE & MAUNA LOA CO₂ CURVE (280 → 315 → >420 PPM)", "detail": "Animated 5-date timeline (1824 → 1958) alongside Charles David Keeling's Mauna Loa CO₂ curve rising from 280 ppm pre-industrial and 315 ppm in March 1958 to >420 ppm today", "scale": "from 280 parts per million before the Industrial Revolution to 315 in 1958 and over 420 today — a 50% rise in Earth's four-in-ten-thousand trace thermostat gas in less than two centuries", "fact_card": "315 to 420 ppm on Mauna Loa", "when_stamp": "March 1958 · 1824–1958", "timeline_step": "5/5 · Mar 1958–present (Keeling's Mauna Loa curve tracks CO₂ from 315 to >420 ppm)", "hold_s": 3.8}),
            ("02_glass_garden_greenhouse_roof_vs_planetary_atmosphere_model", 161.0, 5.5, "A", False, "ROOF VS RADIATION BLANKET", "Fast",
             "Fast: daylight architectural model comparing a glass garden greenhouse trapping rising warm air beneath physical glass panes on the left against a cross-section of Earth's open atmosphere with trace three-atom gas molecules re-radiating heat downward on the right. Nothing emissive, no face.",
             STYLE + "In crisp daylight, a two-part tabletop model contrasts a glass-roofed garden conservatory holding in rising air on the left with a layered atmospheric globe model on the right." + FAST_TAIL,
             None),
            ("03_banting_1920_2am_note_and_1922_toronto_insulin_ward_handoff", 166.5, 6.5, "C", False, "THE $1 INSULIN MIRACLE", "Quality",
             "Quality: readable faces (29-year-old Canadian surgeon Frederick Banting at 2:00 a.m. on 31 October 1920 in London, Ontario, scribbling his 25-word note in bed, beside Charles Best and James Collip in a Toronto hospital ward in January 1922 waking dying diabetic children with purified insulin — handoff to 035 Insulin).",
             STYLE + "London, Ontario, 31 October 1920, and Toronto, January 1922: young surgeon Frederick Banting scribbles a note in a bedside pad at night, dissolving to a bright hospital ward where Banting, Charles Best, and James Collip hold a clear glass vial of insulin beside a smiling boy sitting up in bed." + QUAL_TAIL,
             {"kind": "WHEN", "label": "31 OCTOBER 1920 · JANUARY 1922", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_foote_cylinders_tyndall_rock_salt_arrhenius_ledger (callback, £0).",
             "Reuse P1:07_table_three_props_foote_cylinders_tyndall_rock_salt_arrhenius_ledger [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_foote_cylinders_tyndall_rock_salt_arrhenius_ledger"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_foote_cylinders_tyndall_rock_salt_arrhenius_ledger",
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
            "film": "034_Foote-Tyndall-Arrhenius-Greenhouse",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from greenhouse_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "034_Foote-Tyndall-Arrhenius-Greenhouse",
        "version": "v01",
        "date": "2026-10-17",
        "owner": "gemini (J0494)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/034_Foote-Tyndall-Arrhenius-Greenhouse/greenhouse_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/034_Foote-Tyndall-Arrhenius-Greenhouse/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_Balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034. Nothing in 034 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 034 The Greenhouse Effect: The Forgotten 1856 Sunlit Tube Experiment — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 17 Oct 2026, J0494. Built from `greenhouse_script_master_v01.md` (93.4 PASS) and `SOURCES_v01.md`.",
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
        "# 034 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 17 Oct 2026, J0494. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `greenhouse_script_master_v01.md` (93.4 PASS) and `SOURCES_v01.md` so 034's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Eunice Newton Foote, Joseph Henry, John Tyndall, Svante Arrhenius, Joseph Fourier, Louis Agassiz, Frederick Banting, Charles Best, James Collip), lamplit Stockholm calculation scene, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (Foote's 30-inch glass cylinders & brass air pump pan, 3-object callback bench, sunlit cylinders at 125 °F, Alpine glacial erratic boulder with striations, polished rock-salt crystal window & copper Leslie cube, glass garden greenhouse vs open atmospheric radiation model). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_99_percent_n2_o2_vs_trace_co2_h2o_33c_warming_chart` — 99% of dry air (78% N₂ + 21% O₂) absorbing 0% of outgoing thermal infrared vs trace CO₂ (~0.04%) and water vapour raising Earth's average temperature by ~33 °C (−18 °C → +15 °C) (`SCALE: carbon dioxide makes up just four molecules out of every ten thousand in dry air — yet together with water vapour it keeps Earth thirty-three degrees Celsius warmer than a frozen bare rock`)",
        "  2. `P1:06_10000_molecule_grid_9900_n2_o2_vs_4_co2_molecules_card` — 10,000-molecule grid comparing 7,808 N₂ + 2,095 O₂ molecules vs ~3–4 CO₂ molecules (~280–420 ppm) (`SCALE: four molecules in ten thousand is like four drops of ink in a five-gallon bucket of water — yet those four molecules block infrared heat that passes straight through the other nine thousand nine hundred`)",
        "  3. `P2:02_foote_1856_thermometer_chart_dry_damp_air_and_125f_co2` — Eunice Foote's November 1856 sunlit cylinder data: dry air (96 °F) vs damp air (108 °F), and common air (106 °F) vs carbonic acid gas / CO₂ (125 °F / 51.7 °C) (`SCALE: inside a 30-inch glass tube in the New York sun, carbon dioxide climbed 19 degrees Fahrenheit hotter than ordinary air — the first experimental clue to how changing air changes Earth's climate`)",
        "  4. `P3:02_tyndall_1859_1861_infrared_absorption_bar_chart_n2_o2_vs_co2` — John Tyndall's 1859–1861 relative infrared absorption chart: N₂ (1), O₂ (1), Dry Air (1) vs CO₂ (90), N₂O (355), Coal Gas (>1,000) & humid air (~70×) (`SCALE: pound for pound, a three-atom molecule of carbon dioxide or water vapour absorbs thousands of times more infrared heat than the two-atom oxygen and nitrogen molecules that make up 99% of every breath you take`)",
        "  5. `P4:02_arrhenius_1896_co2_halving_doubling_curve_vs_manabe_1967_chart` — Svante Arrhenius's April 1896 CO₂ curve: 0.5× CO₂ → −4 to −5 °C (Ice Age) and 2.0× CO₂ → +5 to +6 °C vs Manabe & Wetherald's May 1967 computer model (+2.3 to +3.0 °C) (`SCALE: working only with pencil and paper in 1895, Arrhenius calculated a warming curve for doubled carbon dioxide within two degrees of today's fastest supercomputers`)",
        "  6. `P5:01_timeline_1824_1958_and_keeling_mauna_loa_315_to_420_ppm_chart` — completed 5-date timeline (1824 → 1958) + Keeling Mauna Loa CO₂ curve rising from 280 ppm pre-industrial and 315 ppm in March 1958 to >420 ppm today (`SCALE: from 280 parts per million before the Industrial Revolution to 315 in 1958 and over 420 today — a 50% rise in Earth's four-in-ten-thousand trace thermostat gas in less than two centuries`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_foote_cylinders_tyndall_rock_salt_arrhenius_ledger`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"034 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
