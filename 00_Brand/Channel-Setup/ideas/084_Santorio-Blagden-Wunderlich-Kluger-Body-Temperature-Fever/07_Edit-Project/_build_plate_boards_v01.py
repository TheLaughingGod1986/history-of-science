#!/usr/bin/env python3
"""HOS 084 (Fever: Why Your Brain Heats Your Blood to 39°C) pre-VO plate boards v01. J0753. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/084_Santorio-Blagden-Wunderlich-Kluger-Body-Temperature-Fever/body_temp_fever_script_master_v01.md
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
        "Part 01 — The 126 °C Room Where a Beefsteak Cooked While the Scientists Stayed at 37 °C",
        [
            ("01_charles_blagden_1775_126c_beefsteak_room_sweat_and_hypothalamus_37c_to_39c_fever_dial", 0.0, 5.5, "A", False, "126 °C ROOM, 37 °C BODY", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + side by side, inside Charles Blagden and George Fordyce's red-hot brick room in London on 23 January 1775 a wall thermometer reads 260 °F (126 °C) as a raw beefsteak sizzles on a tin plate and eggs roast hard while droplets of sweat evaporate off Blagden's skin keeping his under-tongue thermometer at 37.8 °C (100 °F), beside a cross-section of the human brain's hypothalamus dialling the core thermostat from 37.0 °C up to 39.0 °C during a fever.",
             STYLE + "Split historical-and-physiological scene: on the left in 1775 London, Royal Society physician Charles Blagden stands inside a heated brick chamber wiping sweat as a beefsteak cooks on a tin plate beside a wall thermometer; on the right, a cutaway brain shows the anterior hypothalamus dialling internal blood temperature up to a protective fever." + QUAL_TAIL,
             {"kind": "WHEN", "label": "LONDON, 23 JANUARY 1775", "timeline_step": "1/3 · 1612–1614 & 23 Jan 1775 (Santorio Santorio invents the scaled clinical mouth thermometer and weighing chair, and Charles Blagden steps into a 126 °C heated room with a raw beefsteak to prove evaporative sweat cooling)", "hold_s": 3.5}),
            ("02_santorio_1612_blagden_1775_wunderlich_1868_1m_readings_and_barbour_beeson_kluger_1912_1975_split", 5.5, 6.0, "B", False, "126 °C ROOM, 1 MILLION READINGS, FEVER SURVIVAL", "Quality",
             "Quality: complex three-part composition (Santorio Santorio in Padua in 1612 testing his clinical mouth thermometer and Charles Blagden in London in 1775 inside his 126 °C heated room; Carl Reinhold August Wunderlich in Leipzig in 1868 plotting 1,000,000 thermometer readings; and Henry Barbour in 1912, Paul Beeson in 1948, and Matthew Kluger in 1975 testing the hypothalamic thermostat and desert iguanas).",
             STYLE + "Three-panel period composition: on the left, Santorio Santorio in 1612 Padua on his hanging weighing chair with a curved glass mouth thermometer beside Charles Blagden in 1775 London; in the centre, Carl Wunderlich in 1868 Leipzig charting patient temperature curves; on the right, Henry Barbour, Paul Beeson, and Matthew Kluger in 1975 Michigan with a desert iguana under a heat lamp." + QUAL_TAIL,
             None),
            ("03_human_core_37c_thermoregulation_gauge_between_32c_hypothermia_and_42c_protein_denaturation", 11.5, 6.0, "C", False, "THE 5-DEGREE RAZOR'S EDGE", "Quality",
             "Quality: complex physiological reveal (a split thermal gauge of the human body showing core temperature locked at 37.0 °C / 98.6 °F across external air from −20 °C snow to +45 °C desert, bracketed by the fatal 42 °C protein denaturation ceiling above and the 32 °C hypothermia arrhythmia floor below).",
             STYLE + "In a split anatomical scene, a human figure stands half in a freezing snowstorm and half in a sun-baked desert while the heart and brain core stay steady on a brass thermal gauge between a frozen lower limit and an overheated upper limit." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1612 · 23 JANUARY 1775 · 1868 · 1912 · 1948 · 1975", "timeline_step": "1/3 · 1612 & 1775 (Santorio & Blagden) · 2/3 · 1868 & 1912 (Wunderlich & Barbour) · 3/3 · 1948 & 1975 (Beeson & Kluger)", "hold_s": 3.5}),
            ("04_blagden_1775_126c_sweat_cooling_wunderlich_1868_37c_and_beeson_kluger_hypothalamic_fever_chart", 17.5, 8.0, "E", False, "BLAGDEN (1775): 126 °C ROOM VS 37.8 °C CORE (580 CAL / 2,428 J PER GRAM SWEAT) · WUNDERLICH (1868): 37.0 °C · PYROGEN SET-POINT (37 → 39 °C)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Human Thermoregulation, Evaporative Cooling, Hypothalamic Set-Point & Fever Survival chart from Santorio Santorio (1612–1614), Charles Blagden (1775 Phil. Trans. R. Soc. 65: 111–123), Carl Wunderlich (1868 Das Verhalten der Eigenwärme in Krankheiten), Henry Barbour (1912), Paul Beeson (1948), and Matthew Kluger (1975 Science 188: 166–168) shows 1) Heat loss via sweat evaporation (580 cal / 2,428 J per gram of water) + skin vasodilation vs heat production via shivering + vasoconstriction; 2) Wunderlich's 37.0 °C (98.6 °F) daily circadian curve; and 3) White blood cell pyrogens (IL-1 → PGE₂) shifting the anterior hypothalamic set-point from 37 °C to 39 °C.",
             {"kind": "DATA", "label": "CHARLES BLAGDEN (1775) 126 °C (260 °F) ROOM VS 37.8 °C (100 °F) CORE & EVAPORATIVE SWEAT COOLING (580 CAL / 2,428 J PER GRAM) CHART", "detail": "Inked Charles Blagden (1775) 126 °C (260 °F) room vs 37.8 °C (100 °F) core temperature & evaporative cooling latent heat chart (2,428 joules / 580 calories carried away per gram of evaporated sweat) on period paper", "scale": "evaporating a single litre of sweat off your skin carries away five hundred and eighty kilocalories of heat — enough thermal energy to bring more than five large mugs of ice-cold water to a rolling boil", "who_card": "Santorio Santorio (1561–1636) — Venetian physician and physiologist · Charles Blagden (1748–1820) — British physician and physicist · Carl Reinhold August Wunderlich (1815–1877) — German physician and professor · Henry Gray Barbour (1886–1943) — American pharmacologist and physiologist · Paul Bruce Beeson (1908–2006) — American physician and researcher · Matthew Jay Kluger (born 1945) — American physiologist", "when_stamp": "1612 · 23 January 1775 · 1868 · 1912 · 1948 · 1975", "hold_s": 3.8}),
            ("05_santorio_glass_thermoscope_blagden_1775_phil_trans_and_wunderlich_1868_thermometer_pan", 25.5, 5.5, "A", False, "37 °C TO 39 °C SET-POINT", "Fast",
             "Fast: daylight macro pan across Santorio's curved glass bead thermoscope, Charles Blagden's 1775 Philosophical Transactions volume, and Carl Wunderlich's foot-long 1868 Leipzig mercury thermometer on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak laboratory bench, the camera pans smoothly across a curved glass bead thermoscope, an open 1775 scientific volume, and a long glass mercury thermometer in a wooden case." + FAST_TAIL,
             None),
            ("06_wunderlich_1868_1m_readings_and_barbour_beeson_1912_1948_hypothalamic_fever_chills_crisis_chart", 31.0, 8.0, "E", False, "LEIPZIG, 1868", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked Carl Wunderlich (1868 Leipzig) 1,000,000-Reading Thermometry & Hypothalamic Fever Set-Point Reset diagram compares normal 37.0 °C homeostasis against a 39.0 °C fever set-point (where 37 °C blood feels 'cold' and triggers chills/shivering on the way up, and resetting back to 37 °C triggers drenching sweat when the fever 'breaks').",
             {"kind": "DATA", "label": "1868 CARL WUNDERLICH (1,000,000 READINGS, 37.0 °C) & 1912–1948 BARBOUR/BEESON HYPOTHALAMIC SET-POINT (37 → 39 °C CHILLS & CRISIS SWEAT) CURVE", "detail": "Inked Wunderlich (1868) & Barbour/Beeson (1912–1948) hypothalamic set-point vs actual core temperature curve (37.0 °C normal → 39.0 °C pyrogen set-point → chills phase → crisis sweat phase) on period paper", "scale": "Carl Wunderlich's foot-long mercury thermometer took twenty minutes in a patient's armpit for a single reading — meaning his one million measurements in Leipzig took more than three hundred thousand hours of human waiting", "hold_s": 3.8}),
            ("07_table_three_props_1612_thermoscope_1775_oiled_vs_open_water_flasks_and_1866_allbutt_pocket_thermometer", 39.0, 5.5, "C", False, "1612 TO 1975", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Santorio's 1612 curved glass mouth thermoscope, Blagden's 1775 paired open vs oil-sealed water evaporation flasks, and Allbutt and Wunderlich's 1866–1868 clinical mercury thermometers). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a curved glass mouth thermoscope on a brass stand, two glass flasks of water one sealed with a golden oil layer, and a velvet-lined pocket thermometer case." + FAST_TAIL,
             None),
            ("08_explorer_turning_giant_brass_hypothalamus_thermostat_dial_from_37_to_39_as_white_blood_cell_delivers_pyrogen", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside a giant brass hypothalamus thermostat dial mounted on an anatomical brain pedestal, the Explorer receives a spherical immune messenger orb from a sculpted white blood cell and rotates the heavy brass pointer clockwise to raise the set-point as mechanical heat fins open below." + EXP_TAIL,
             None),
            ("09_matthew_kluger_1975_michigan_desert_iguana_thermal_gradient_chamber_fever_survival", 67.5, 5.5, "B", False, "ANN ARBOR, 1975", "Quality",
             "Quality: readable face (at the University of Michigan in Ann Arbor in 1975, American physiologist Matthew Jay Kluger watches an infected desert iguana Dipsosaurus dorsalis move to the warm end of a sand-bottomed thermal gradient chamber to raise its body temperature by 2 °C and survive).",
             STYLE + "In a 1975 University of Michigan physiology laboratory, physiologist Matthew Kluger leans over a long glass-walled desert sand terrarium watching a sandy desert iguana bask at the warm end beside a thermometer probe." + QUAL_TAIL,
             {"kind": "WHEN", "label": "ANN ARBOR, 1975", "timeline_step": "3/3 · 1948 & 1975 (Paul Beeson discovers leukocyte pyrogens that raise the hypothalamic set-point, and Matthew Kluger proves in desert iguanas that fever triples survival against bacterial infection)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 1612 & 23 January 1775: Santorio's Mouth Thermometer & Charles Blagden's 126 °C (260 °F) Beefsteak Room (Evaporating Sweat)",
        [
            ("01_santorio_1612_padua_weighing_chair_and_charles_blagden_23_jan_1775_london_126c_beefsteak_room", 73.0, 6.5, "A", False, "SWEAT COOLED A 126°C ROOM", "Quality",
             "Quality: readable faces (Venetian physician Santorio Santorio in Padua in 1612–1614 sitting on his hanging steelyard balance chair with his curved glass mouth thermometer, dissolving to Royal Society physicians Charles Blagden and George Fordyce with botanist Joseph Banks on 23 January 1775 standing inside a brick room heated to 260 °F / 126 °C beside a cooking raw beefsteak and an oiled vs open flask of water).",
             STYLE + "Split period scene: on the left in 1612 Padua, Venetian physician Santorio Santorio sits in his suspended wooden steelyard weighing chair holding a curved glass mouth thermoscope; on the right in 1775 London, Charles Blagden, George Fordyce, and Joseph Banks stand inside a heated brick chamber wiping sweat beside a cooked beefsteak on a tin plate and two glass water flasks." + QUAL_TAIL,
             {"kind": "FACT", "label": "Sweat cooled a 126°C room", "who_card": "George Fordyce (1736–1802) — Scottish physician and chemist · Joseph Banks (1743–1820) — British naturalist and botanist", "when_stamp": "1612 · 1614 · 23 January 1775", "timeline_step": "1/3 · 1612–1614 & 23 Jan 1775 (Santorio invents the clinical mouth thermometer & weighing chair; Blagden proves evaporative sweat cooling in a 126 °C room)", "hold_s": 3.8}),
            ("02_santorio_1614_weighing_chair_and_blagden_1775_126c_beefsteak_evaporation_chart", 79.5, 8.0, "E", False, "1612–1614 SANTORIO (DE STATICA MEDICINA) & 23 JAN 1775 CHARLES BLAGDEN (PHIL. TRANS.: 126 °C ROOM VS 37.8 °C BODY & 580 CAL/G SWEAT)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Santorio Santorio (1614 De Statica Medicina) weighing-chair water-loss balance & Charles Blagden (1775 Phil. Trans. R. Soc. 65: 111–123) 126 °C (260 °F) room vs 37.8 °C body temperature & oiled-vs-open water flask evaporation chart.",
             {"kind": "DATA", "label": "1614 SANTORIO WEIGHING-CHAIR PERSPIRATION & 1775 BLAGDEN (PHIL. TRANS.) 126 °C ROOM VS 37.8 °C BODY & OILED-VS-OPEN FLASK CHART", "detail": "Inked Santorio Santorio (1614 De Statica Medicina) weighing-chair water-loss balance & Charles Blagden (1775 Phil. Trans. R. Soc. 65: 111–123) 126 °C (260 °F) room vs 37.8 °C body temperature & oiled-vs-open water flask evaporation chart on period paper", "scale": "inside Blagden's 126-degree room, a dead slab of beefsteak cooked in thirty-three minutes because dead meat cannot sweat — while the living scientists stood beside it unharmed because evaporating sweat turned their skin into a self-cooling refrigerator", "hold_s": 3.8}),
            ("03_london_1775_phil_trans_paper_ivory_scale_thermometers_and_oiled_vs_open_water_flasks_closeup", 87.5, 6.5, "B", False, "23 JANUARY 1775 — BLAGDEN'S 126 °C HEATED ROOM", "Fast",
             "Fast: daylight macro shot of Charles Blagden's 1775 Philosophical Transactions paper beside ivory-mounted glass thermometers and two glass flasks (one open to the air, one sealed with a layer of oil) on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1775 London laboratory table, an open Royal Society journal sits beside two ivory-mounted mercury thermometers and a pair of glass water flasks, one topped with a layer of oil." + FAST_TAIL,
             None),
            ("04_padua_1614_steelyard_weighing_chair_scale_model_and_glass_thermoscope_pan", 94.0, 5.5, "C", False, "SANTORIO'S WEIGHING CHAIR & THERMOSCOPE", "Fast",
             "Fast: daylight close-up pan across a wooden model of Santorio Santorio's suspended steelyard weighing chair balanced by brass counterweights beside a coiled glass mouth thermoscope on an oak bench. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak bench, a wooden steelyard weighing chair suspended from a brass balance beam sits beside a curved glass mouth thermoscope." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 1868 & 1912: Carl Wunderlich's 1,000,000 Readings (37.0 °C / 98.6 °F) & Henry Barbour's Brain Thermostat — Midpoint Twist",
        [
            ("01_carl_wunderlich_1868_leipzig_1m_readings_37c_and_henry_barbour_1912_vienna_hypothalamic_thermode", 99.5, 6.5, "A", False, "1 MILLION READINGS SET 37°C", "Quality",
             "Quality: readable faces (German physician Carl Reinhold August Wunderlich in Leipzig in 1868 charting over 1,000,000 axillary thermometer readings across 25,000 patients to establish 37.0 °C / 98.6 °F alongside Thomas Clifford Allbutt's 1866 pocket thermometer, dissolving to American pharmacologist Henry Gray Barbour in Vienna in 1912 warming and cooling the anterior hypothalamus with a tiny silver water-thermode).",
             STYLE + "Split period scene: on the left in 1868 Leipzig, Professor Carl Wunderlich holds a foot-long mercury thermometer beside stacks of twenty-five thousand patient fever charts and Thomas Clifford Allbutt's small pocket thermometer; on the right in 1912 Vienna, Henry Barbour adjusts a fine silver water-thermode tube over an anatomical brain model." + QUAL_TAIL,
             {"kind": "FACT", "label": "1 million readings set 37°C", "who_card": "Thomas Clifford Allbutt (1836–1925) — British physician", "when_stamp": "1866 · 1868 · 1912", "timeline_step": "2/3 · 1866, 1868 & 1912 (Following Allbutt's pocket thermometer, Carl Wunderlich analyses 1,000,000 armpit readings across 25,000 patients in Leipzig to define 37.0 °C, and Henry Barbour discovers the brain's thermostat in the anterior hypothalamus)", "hold_s": 3.8}),
            ("02_wunderlich_1868_circadian_36_2_to_37_5c_range_and_barbour_1912_anterior_hypothalamus_thermode_chart", 106.0, 8.0, "E", False, "1868 CARL WUNDERLICH (25,000 PATIENTS, 36.2–37.5 °C CIRCADIAN RANGE AROUND 37.0 °C) & 1912 HENRY BARBOUR (HYPOTHALAMIC THERMOSTAT)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Carl Wunderlich (1868 Das Verhalten der Eigenwärme in Krankheiten) 25,000-patient circadian temperature range (36.2–37.5 °C around 37.0 °C / 98.6 °F) & Henry Barbour (1912 Arch. Exp. Pathol. Pharmakol. 70: 1–26) anterior hypothalamic thermode warming-vs-cooling response chart.",
             {"kind": "DATA", "label": "1868 WUNDERLICH (36.2 °C DAWN TO 37.5 °C EVENING AROUND 37.0 °C) & 1912 BARBOUR ANTERIOR HYPOTHALAMUS THERMODE CHART", "detail": "Inked Carl Wunderlich (1868 Das Verhalten der Eigenwärme in Krankheiten) 25,000-patient circadian temperature range (36.2–37.5 °C around 37.0 °C / 98.6 °F) & Henry Barbour (1912 Arch. Exp. Pathol. Pharmakol. 70: 1–26) anterior hypothalamic thermode warming-vs-cooling response chart on period paper", "scale": "the thermostat that controls all thirty-seven trillion cells in your body — deciding when you sweat and when you shiver — sits in the preoptic hypothalamus at the base of your brain and is no bigger than a single garden pea", "hold_s": 3.8}),
            ("03_leipzig_1868_eigenwarme_book_30cm_thermometer_vs_1866_allbutt_6inch_pocket_thermometer_closeup", 114.0, 6.5, "B", False, "1868 & 1912 — WUNDERLICH'S 37 °C & BARBOUR'S HYPOTHALAMUS", "Fast",
             "Fast: daylight macro shot of Carl Wunderlich's 1868 Das Verhalten der Eigenwärme in Krankheiten open to its folding lithographed fever curves beside a 30-cm Leipzig hospital thermometer, Thomas Clifford Allbutt's 15-cm pocket thermometer, and Barbour's silver water-thermode on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an 1868 Leipzig medical desk, an open German thermometry volume with folding fever-curve plates sits beside a thirty-centimetre hospital thermometer, a six-inch pocket thermometer in a leather case, and a fine silver water-thermode tube." + FAST_TAIL,
             None),
            ("04_cutaway_brain_model_showing_pea_sized_preoptic_anterior_hypothalamus_thermostat_and_silver_thermode_pan", 120.5, 5.5, "C", False, "THE PEA-SIZED HYPOTHALAMIC THERMOSTAT", "Fast",
             "Fast: daylight close-up pan across a painted anatomical cutaway brain model highlighting the pea-sized preoptic anterior hypothalamus at the base of the brain connected to a brass-and-silver water-thermode demonstrator on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a painted anatomical cross-section model of the human brain highlights the tiny anterior hypothalamus region connected to a brass water-circulation tube." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 1948 & 1975: Paul Beeson's Immune Pyrogens & Matthew Kluger's Fever-Seeking Iguanas",
        [
            ("01_paul_beeson_1948_leukocyte_pyrogen_and_matthew_kluger_1975_desert_iguana_75_percent_fever_survival", 126.0, 6.5, "A", False, "LIZARDS SEEK FEVER TO LIVE", "Quality",
             "Quality: readable faces (American physician Paul Bruce Beeson in 1948 isolating leukocyte endogenous pyrogen from white blood cells, dissolving to physiologist Matthew Jay Kluger at the University of Michigan in 1975 watching bacteria-infected desert iguanas Dipsosaurus dorsalis move under a warm sunlamp to raise their temperature by 2 °C and achieve 75% survival).",
             STYLE + "Split period scene: on the left in 1948 Atlanta, physician Paul Beeson holds a centrifuge tube of separated white blood cells beside a hypothalamic fever chart; on the right in 1975 Michigan, Matthew Kluger observes desert iguanas gathering at the warm end of a sand chamber." + QUAL_TAIL,
             {"kind": "FACT", "label": "Lizards seek fever to live", "when_stamp": "1948 · 1975", "timeline_step": "3/3 · 1948 & 1975 (Paul Beeson proves white blood cells release endogenous pyrogens to raise the hypothalamic set-point, and Matthew Kluger proves in desert iguanas that fever triples survival)", "hold_s": 3.8}),
            ("02_beeson_1948_il1_pge2_pyrogen_pathway_and_kluger_1975_science_desert_iguana_75_vs_25_survival_chart", 132.5, 8.0, "E", False, "1948 PAUL BEESON (LEUKOCYTE PYROGEN IL-1 → PGE₂) & 1975 MATTHEW KLUGER (SCIENCE: DESERT IGUANA FEVER 75% VS 25% SURVIVAL)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Paul Beeson (1948 J. Clin. Invest. 27: 524) & Matthew Kluger (1975 Science 188: 166–168) desert iguana (Dipsosaurus dorsalis) behavioural fever survival curve (75% survival at 40–42 °C febrile temperature vs 25% survival at 38 °C afebrile / antipyretic-treated temperature).",
             {"kind": "DATA", "label": "1948 BEESON (PYROGEN SET-POINT) & 1975 MATTHEW KLUGER (SCIENCE: DESERT IGUANA 75% FEBRILE SURVIVAL VS 25% AFEBRILE SURVIVAL) CHART", "detail": "Inked Paul Beeson (1948 J. Clin. Invest. 27: 524) & Matthew Kluger (1975 Science 188: 166–168) desert iguana (Dipsosaurus dorsalis) behavioural fever survival curve (75% survival at 40–42 °C febrile temperature vs 25% survival at 38 °C afebrile / antipyretic-treated temperature) on period paper", "scale": "raising your body temperature by just two degrees Celsius in a fever forces your cells to burn about twenty-five percent more energy — equivalent to jogging several miles without ever leaving your bed, a price evolution gladly pays because that extra heat supercharges your immune cells and starves bacteria of iron", "hold_s": 3.8}),
            ("03_michigan_1975_science_fever_and_survival_offprint_sand_terrarium_thermometer_and_1948_jci_closeup", 140.5, 6.5, "B", False, "1948 & 1975 — BEESON'S PYROGEN & KLUGER'S FEVER SURVIVAL", "Fast",
             "Fast: daylight macro shot of Matthew Kluger's April 1975 Science paper 'Fever and survival' and Paul Beeson's 1948 Journal of Clinical Investigation volume beside a glass sand-gradient thermometer rig on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1975 physiology bench, an open scientific journal showing a lizard survival graph sits beside a sand-filled glass temperature-gradient box with brass thermometer probes." + FAST_TAIL,
             None),
            ("04_explorer_guiding_desert_iguana_to_warm_side_of_terrarium_as_immune_shields_lock_away_iron_from_bacteria", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside a split desert sand terrarium with a cool shaded side and a warm sunlit side, the Explorer gestures a friendly sculpted desert iguana onto the warm sand as tiny brass shields lock iron spheres away from sluggish bacteria models." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — The Living Furnace & Thermostat — & Why Your Textbook's Tongue Map Was Wrong",
        [
            ("01_timeline_1612_1975_and_human_thermoregulation_sweat_hypothalamus_fever_survival_chart", 152.5, 8.5, "E", False, "1612–1975 TIMELINE · SANTORIO THERMOMETER, BLAGDEN 126 °C SWEAT, WUNDERLICH 37 °C, BARBOUR HYPOTHALAMUS & BEESON-KLUGER FEVER", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 3-era timeline completes: 1612–1614 & 23 Jan 1775 (Santorio Santorio invents the scaled clinical mouth thermometer and weighing chair, and Charles Blagden steps into a 126 °C heated room with a raw beefsteak to prove evaporative sweat cooling) · 1866, 1868 & 1912 (Following Allbutt's pocket thermometer, Carl Wunderlich analyses 1,000,000 armpit readings across 25,000 patients in Leipzig to define 37.0 °C, and Henry Barbour discovers the brain's thermostat in the anterior hypothalamus) · 1948 & 1975 (Paul Beeson discovers leukocyte pyrogens that raise the hypothalamic set-point, and Matthew Kluger proves in desert iguanas that fever triples survival against bacterial infection).",
             {"kind": "DATA", "label": "1612–1975 BODY TEMPERATURE & FEVER TIMELINE · SANTORIO, BLAGDEN, WUNDERLICH, BARBOUR, BEESON & KLUGER", "detail": "Animated timeline (1612 → 1975) alongside an inked summary of clinical thermometry, evaporative sweat cooling, the 37.0 °C hypothalamic set-point, and pyrogen fever survival", "scale": "from a 126-degree brick oven in Georgian London to one million thermometer readings in Leipzig and fever-seeking lizards in Michigan, scientists discovered how a pea-sized thermostat in your brain guards the thirty-seven-degree fire of life", "when_stamp": "1612–1975", "timeline_step": "3/3 · 1612–1975 timeline complete", "hold_s": 3.8}),
            ("02_clinical_mercury_thermometer_and_hypothalamus_model_beside_kelp_and_glutamate_crystals_on_plinth_pan", 161.0, 5.5, "A", False, "EVAPORATING SWEAT, 37 °C & FEVER", "Fast",
             "Fast: daylight close-up of a clinical mercury thermometer and brass hypothalamic thermostat dial beside a porcelain dish of white glutamate crystals and dried konbu kelp on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a glass clinical thermometer and brass thermostat dial sit beside dried dark-green kelp leaves and a porcelain dish of white crystals." + FAST_TAIL,
             None),
            ("03_hanig_1901_boring_1942_tongue_map_myth_ikeda_1908_38kg_kelp_umami_and_zuker_2002_receptors_handoff", 166.5, 6.5, "C", False, "TONGUE MAP MYTH, 38 KG KELP & UMAMI RECEPTORS", "Quality",
             "Quality: readable faces (David Pauli Hänig in Leipzig in 1901 and Edwin Boring at Harvard in 1942 with the misread Tongue Map debunked by Virginia Collings in 1974, Kikunae Ikeda in Tokyo on 25 July 1908 isolating 30 g of glutamate umami crystals from 38 kg of konbu kelp, and Charles Zuker in 2002 mapping T1R1+T1R3 umami taste receptors — handoff to 085 Taste Buds, the Tongue Map Myth & Umami).",
             STYLE + "Split period scene: on the left in 1908 Tokyo, chemist Kikunae Ikeda holds up a porcelain dish of white glutamate crystals beside a giant stack of dried kelp and a crossed-out four-zone tongue chart; on the right in 2002, Charles Zuker points to a five-taste receptor map." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1901 · 25 JULY 1908 · 1942 · 1974 · 2002", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1612_thermoscope_1775_oiled_vs_open_water_flasks_and_1866_allbutt_pocket_thermometer (callback, £0).",
             "Reuse P1:07_table_three_props_1612_thermoscope_1775_oiled_vs_open_water_flasks_and_1866_allbutt_pocket_thermometer [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1612_thermoscope_1775_oiled_vs_open_water_flasks_and_1866_allbutt_pocket_thermometer"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1612_thermoscope_1775_oiled_vs_open_water_flasks_and_1866_allbutt_pocket_thermometer",
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
            "film": "084_Santorio-Blagden-Wunderlich-Kluger-Body-Temperature-Fever",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from body_temp_fever_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "084_Santorio-Blagden-Wunderlich-Kluger-Body-Temperature-Fever",
        "version": "v01",
        "date": "2026-10-21",
        "owner": "gemini (J0753)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/084_Santorio-Blagden-Wunderlich-Kluger-Body-Temperature-Fever/body_temp_fever_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/084_Santorio-Blagden-Wunderlich-Kluger-Body-Temperature-Fever/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077 > 078 > 079 > 080 > 081 > 082 > 083 > 084 > 085 > 086. Nothing in 084 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 084 Fever: Why Your Brain Heats Your Blood to 39°C — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 21 Oct 2026, J0753. Built from `body_temp_fever_script_master_v01.md` (`91.4/100 PASS`) and `SOURCES_v01.md`.",
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
        "# 084 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 21 Oct 2026, J0753. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `body_temp_fever_script_master_v01.md` (`91.4/100 PASS`) and `SOURCES_v01.md` so 084's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Santorio Santorio, Charles Blagden, George Fordyce, Joseph Banks, Thomas Clifford Allbutt, Carl Reinhold August Wunderlich, Henry Gray Barbour, Paul Bruce Beeson, Matthew Jay Kluger, Kikunae Ikeda, Charles S. Zuker), 23 January 1775 London `126 °C` (`260 °F`) beefsteak room & evaporative sweat proof, 1868 Leipzig `1,000,000` thermometer readings (`37.0 °C`) & 1912 Vienna `anterior hypothalamus` thermostat proof, 1948 leukocyte `endogenous pyrogens` & 1975 Michigan desert iguana (`75% vs 25%`) fever survival proof, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (Santorio's glass bead thermoscope, Blagden's 1775 *Phil. Trans.* volume & Wunderlich's 1868 thermometer pan, 3-object callback bench, 1775 ivory-mounted thermometers with open vs oil-sealed water evaporation flasks, wooden steelyard weighing-chair scale model, 1868 *Das Verhalten der Eigenwärme* folding fever-curve plates with 30-cm Leipzig vs 15-cm Allbutt pocket thermometers, cutaway brain model highlighting the pea-sized anterior hypothalamus & silver water-thermode, 1975 *Science* 'Fever and survival' offprint with sand temperature-gradient box, clinical thermometer & thermostat dial beside dried *konbu* kelp and glutamate crystals on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_blagden_1775_126c_sweat_cooling_wunderlich_1868_37c_and_beeson_kluger_hypothalamic_fever_chart` — Charles Blagden (1775) `126 °C` room vs `37.8 °C` core temperature & evaporative cooling latent heat (`2,428 J / 580 cal` per gram) chart (`SCALE: evaporating a single litre of sweat off your skin carries away five hundred and eighty kilocalories of heat — enough thermal energy to bring more than five large mugs of ice-cold water to a rolling boil`)",
        "  2. `P1:06_wunderlich_1868_1m_readings_and_barbour_beeson_1912_1948_hypothalamic_fever_chills_crisis_chart` — Carl Wunderlich (1868 Leipzig, 1,000,000 readings) & Barbour/Beeson (1912–1948) hypothalamic set-point (`37.0 °C → 39.0 °C`) chills & crisis sweat curve (`SCALE: Carl Wunderlich's foot-long mercury thermometer took twenty minutes in a patient's armpit for a single reading — meaning his one million measurements in Leipzig took more than three hundred thousand hours of human waiting`)",
        "  3. `P2:02_santorio_1614_weighing_chair_and_blagden_1775_126c_beefsteak_evaporation_chart` — Santorio Santorio (1614 *De Statica Medicina*) weighing-chair water-loss balance & Charles Blagden (1775 *Phil. Trans.*) `126 °C` room oiled-vs-open flask evaporation chart (`SCALE: inside Blagden's 126-degree room, a dead slab of beefsteak cooked in thirty-three minutes because dead meat cannot sweat — while the living scientists stood beside it unharmed because evaporating sweat turned their skin into a self-cooling refrigerator`)",
        "  4. `P3:02_wunderlich_1868_circadian_36_2_to_37_5c_range_and_barbour_1912_anterior_hypothalamus_thermode_chart` — Carl Wunderlich (1868) 25,000-patient circadian temperature range (`36.2–37.5 °C` around `37.0 °C`) & Henry Barbour (1912) anterior hypothalamic thermode warming-vs-cooling response chart (`SCALE: the thermostat that controls all thirty-seven trillion cells in your body — deciding when you sweat and when you shiver — sits in the preoptic hypothalamus at the base of your brain and is no bigger than a single garden pea`)",
        "  5. `P4:02_beeson_1948_il1_pge2_pyrogen_pathway_and_kluger_1975_science_desert_iguana_75_vs_25_survival_chart` — Paul Beeson (1948 *J. Clin. Invest.*) & Matthew Kluger (1975 *Science*) desert iguana (*Dipsosaurus dorsalis*) behavioural fever survival curve (`75% vs 25%`) (`SCALE: raising your body temperature by just two degrees Celsius in a fever forces your cells to burn about twenty-five percent more energy — equivalent to jogging several miles without ever leaving your bed, a price evolution gladly pays because that extra heat supercharges your immune cells and starves bacteria of iron`)",
        "  6. `P5:01_timeline_1612_1975_and_human_thermoregulation_sweat_hypothalamus_fever_survival_chart` — completed timeline (1612 → 1975) + clinical thermometry, evaporative sweat cooling, `37.0 °C` hypothalamic set-point & fever survival (`SCALE: from a 126-degree brick oven in Georgian London to one million thermometer readings in Leipzig and fever-seeking lizards in Michigan, scientists discovered how a pea-sized thermostat in your brain guards the thirty-seven-degree fire of life`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1612_thermoscope_1775_oiled_vs_open_water_flasks_and_1866_allbutt_pocket_thermometer`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077 > 078 > 079 > 080 > 081 > 082 > 083 > 084 > 085 > 086. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"084 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
