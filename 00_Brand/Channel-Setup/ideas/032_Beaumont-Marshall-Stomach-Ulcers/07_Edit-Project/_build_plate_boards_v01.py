#!/usr/bin/env python3
"""HOS 032 (Stomach Ulcers: Why a Doctor Drank a Beaker of Bacteria) pre-VO plate boards v01. J0494. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/032_Beaumont-Marshall-Stomach-Ulcers/ulcers_script_master_v01.md
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
        "Part 01 — The Silk String in Michigan and the Beaker in Perth",
        [
            ("01_beaumont_1825_silk_string_and_marshall_1984_drinking_beaker", 0.0, 5.5, "A", False, "WHY HE DRANK BACTERIA", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + at Fort Mackinac, Michigan, in May 1825, US Army surgeon William Beaumont lowers a piece of boiled beef tied to a silk string into a healed keyhole in fur trapper Alexis St. Martin's side, dissolving to Royal Perth Hospital in July 1984 as 32-year-old Dr Barry Marshall drinks a cloudy glass beaker teeming with a billion Helicobacter pylori bacteria.",
             STYLE + "At Fort Mackinac in May 1825, US Army surgeon William Beaumont in a blue coat holds a silk thread tied to a small piece of beef beside fur trapper Alexis St. Martin, dissolving to Perth in July 1984 as young physician Barry Marshall in a white lab coat drinks a cloudy glass beaker of broth." + QUAL_TAIL,
             {"kind": "WHEN", "label": "MACKINAC ISLAND, MAY 1825 · PERTH, JULY 1984", "timeline_step": "2/5 · May 1825–Dec 1833 (Beaumont's 238 silk-string experiments) & 4/5 · Jul 1984 (Marshall drinks 10⁹ H. pylori)", "hold_s": 3.5}),
            ("02_silk_string_acid_vial_easter_petri_dish_nobel_split", 5.5, 6.0, "B", False, "WINDOW, ACID, BACTERIA", "Quality",
             "Quality: complex three-part split composition (William Beaumont's 1825 silk-string food parcels and glass vial of hydrochloric gastric acid on the left; Robin Warren and Barry Marshall's 5-day April 1982 Easter Petri dish of H. pylori in the centre; Marshall drinking the bacterial broth in July 1984 and his 2005 Nobel medal on the right).",
             STYLE + "Three-panel period composition: on the left, a silk string tied to food parcels beside a glass vial of clear gastric juice; in the centre, a glass Petri dish dotted with translucent bacterial colonies inside a warm incubator; on the right, a doctor raising a glass beaker beside a gold medal." + QUAL_TAIL,
             None),
            ("03_mackinac_island_1822_fur_store_shotgun_accident_beaumont", 11.5, 6.0, "C", False, "A WINDOW INTO THE STOMACH", "Quality",
             "Quality: readable faces (inside the American Fur Company store on Mackinac Island on 6 June 1822, post surgeon William Beaumont rushes to dress 20-year-old French-Canadian voyageur Alexis St. Martin's chest and stomach wound as smoke clears).",
             STYLE + "Inside a timber fur-trading post on Mackinac Island on 6 June 1822, US Army surgeon William Beaumont rushes with bandages toward injured young voyageur Alexis St. Martin as faint powder smoke drifts across wooden barrels." + QUAL_TAIL,
             {"kind": "WHEN", "label": "MACKINAC ISLAND, 6 JUNE 1822", "timeline_step": "1/5 · 6 Jun 1822 & Dec 1823 (St. Martin's wound; Prout discovers gastric HCl)", "hold_s": 3.5}),
            ("04_stomach_acid_ph_1_5_and_h_pylori_ammonia_shield_chart", 17.5, 8.0, "E", False, "PH 1.5 ACID & H. PYLORI AMMONIA SHIELD", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked pH and ulcer-cause chart shows William Beaumont's 1825–1833 gastric fistula experiments (pH 1.5–2.0 hydrochloric acid dissolving meat in 2–4 hours) alongside Robin Warren and Barry Marshall's 1982–1984 discovery of Helicobacter pylori using urease enzyme to neutralise stomach acid in an ammonia shield and cause ~80% of gastric ulcers and ~90% of duodenal ulcers.",
             {"kind": "DATA", "label": "PH 1.5 GASTRIC ACID VS H. PYLORI UREASE AMMONIA SHIELD (80–90% OF ULCERS)", "detail": "Inked pH and ulcer-cause chart on period paper showing human stomach acid at pH 1.5–2.0 (nearly as acidic as battery acid at pH 0.8 and 10⁶× more acidic than pure water at pH 7.0) and H. pylori causing ~80% of gastric ulcers and ~90% of duodenal ulcers", "scale": "human stomach acid sits near pH 1.5 — strong enough to dissolve a zinc nail and a million times more acidic than pure water, yet H. pylori wraps itself in an ammonia bubble to survive inside it", "who_card": "William Beaumont (1785–1853) — American Army surgeon · Alexis St. Martin (1802–1880) — Canadian fur voyageur · Robin Warren (1937–2024) — Australian pathologist · Barry Marshall (born 1951) — Australian physician and microbiologist", "when_stamp": "May 1825 · April 1982 · July 1984", "hold_s": 3.8}),
            ("05_beaumont_silk_string_food_parcels_and_pocket_watch_pan", 25.5, 5.5, "A", False, "FORT MACKINAC, 1825", "Fast",
             "Fast: daylight macro pan across Beaumont's wooden table holding a brass pocket watch, a spool of silk thread tied to tiny cubes of boiled beef and cabbage, and a glass vial of clear gastric fluid between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a frontier wooden desk, the camera pans across a brass pocket watch, a silk thread tied to small cubes of beef and cabbage, and a stoppered glass vial of clear liquid." + FAST_TAIL,
             None),
            ("06_ph_scale_bar_water_7_vs_gastric_acid_1_5_vs_battery_acid_card", 31.0, 8.0, "E", False, "PH 1.5 STOMACH ACID", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked pH scale bar compares pure water (pH 7.0), lemon juice (pH 2.2), human gastric hydrochloric acid (pH 1.5 = ~300,000–1,000,000× higher H⁺ concentration than water), and car battery acid (pH 0.8) against an H. pylori bacterium puffing out an alkaline ammonia cloud.",
             {"kind": "DATA", "label": "PH 7.0 WATER VS PH 1.5 GASTRIC ACID (~1,000,000× H⁺ CONCENTRATION)", "detail": "Inked pH scale bar comparing pure water (pH 7.0), lemon juice (pH 2.2), human gastric juice (pH 1.5), and battery acid (pH 0.8) against an H. pylori ammonia cloud", "scale": "stomach acid is nearly a million times more acidic than drinking water — so harsh that doctors assumed the stomach was as sterile as a bottle of bleach", "hold_s": 3.8}),
            ("07_table_three_props_silk_string_vial_petri_dish_beaker", 39.0, 5.5, "C", False, "1825 TO 1984", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Beaumont's glass vial of gastric juice with a silk string and pocket watch, Warren and Marshall's agar Petri dish, and Marshall's glass beaker of broth). Nothing emissive.",
             STYLE + "On a wooden laboratory bench in soft window light sit three objects side by side: a glass vial with a silk string and brass pocket watch, a covered glass Petri dish, and a clear glass beaker of broth." + FAST_TAIL,
             None),
            ("08_explorer_fishing_rod_silk_line_beef_cube_in_acid_flask", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Holding a miniature fishing rod with a silk line, the Explorer lowers a tiny cube of roast beef into a bubbling glass flask of gastric juice, checks its brass pocket watch as the beef melts away, and then spots a spiral bacterium with spinning tail flagella swimming happily inside a pale ammonia bubble." + EXP_TAIL,
             None),
            ("09_beaumont_holding_gastric_juice_vial_up_to_candle_cabin", 67.5, 5.5, "B", False, "MACKINAC CABIN · 1825", "Quality",
             "Quality: candlelit scene + readable face (William Beaumont holding a glass vial of clear gastric juice up to a candle in his Michigan cabin).",
             STYLE + "In a warm candlelit frontier cabin in Michigan in 1825, surgeon William Beaumont holds a clear glass vial of gastric fluid up to the candle flame and inspects it closely." + QUAL_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — The Musket Blast and 238 Silk-String Experiments",
        [
            ("01_beaumont_examining_st_martin_fistula_and_prout_1823_london_hcl", 73.0, 6.5, "A", False, "238 SILK-STRING TESTS", "Quality",
             "Quality: readable faces (US Army surgeon William Beaumont examining the healed valve-like fistula on Alexis St. Martin's side at Fort Mackinac in May 1825, while English chemist William Prout in London in December 1823 distils hydrochloric acid from stomach fluid).",
             STYLE + "Split period scene: on the left at Fort Mackinac in May 1825, surgeon William Beaumont in a blue Army coat holds a silk thread beside Alexis St. Martin's bandaged side; on the right in London in December 1823, chemist William Prout distils clear hydrochloric acid in a glass retort." + QUAL_TAIL,
             {"kind": "WHO", "label": "William Prout (1785–1850) — English chemist and physician", "fact_card": "238 silk-string tests", "when_stamp": "23 December 1823 · May 1825 · August 1825 · December 1833", "hold_s": 3.8}),
            ("02_beaumont_1833_digestion_time_chart_eggs_beef_pork", 79.5, 8.0, "E", False, "EGGS (~1H) VS BOILED BEEF (2H 45M) VS ROAST PORK (5H 15M)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked digestion-time chart from William Beaumont's December 1833 book compares boiled tripe and whipped eggs (~1 hour), boiled beef (~2 hours 45 minutes), and roast pork (~5 hours 15 minutes) alongside in-vitro hydrochloric acid + pepsin digestion at 37.8 °C (100 °F).",
             {"kind": "DATA", "label": "BEAUMONT'S 1833 DIGESTION CHART: EGGS (1H) · BEEF (2H 45M) · PORK (5H 15M)", "detail": "Inked digestion-time chart on period paper from Beaumont's December 1833 book comparing boiled tripe & whipped eggs (~1 hour), boiled beef (~2 hours 45 minutes), and roast pork (~5 hours 15 minutes) alongside in-vitro hydrochloric acid digestion at 37.8 °C (100 °F)", "scale": "by pulling a silk thread in and out of a living stomach 238 times, Beaumont timed digestion to the minute — from one hour for eggs to over five hours for roast pork", "hold_s": 3.8}),
            ("03_beaumont_glass_vial_in_100f_warm_sand_bath_dissolving_beef", 87.5, 6.5, "B", False, "DIGESTION IN A GLASS VIAL", "Fast",
             "Fast: daylight close-up of a clear glass vial of gastric juice resting in a warm sand bath at 100 °F with a brass thermometer beside it as a cube of boiled beef slowly dissolves into fine threads. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden table, a stoppered glass vial containing a small cube of beef sits in a warm pan of sand beside a brass thermometer as the meat fibres gently dissolve." + FAST_TAIL,
             None),
            ("04_beaumont_1833_printed_book_and_silk_thread_food_samples", 94.0, 5.5, "C", False, "PLATTSBURGH · DECEMBER 1833", "Fast",
             "Fast: daylight macro shot of William Beaumont's 1833 leather-bound book resting open beside a brass pocket watch and three glass vials holding digested food samples at 1 hour, 2 hours 45 minutes, and 5 hours. Nothing emissive, no face.",
             STYLE + "In soft daylight on a desk, a leather-bound nineteenth-century volume lies open beside a brass pocket watch and three clear glass vials showing stages of dissolved food." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — The 'No Acid, No Ulcer' Dogma and the Forgotten Easter Petri Dish",
        [
            ("01_warren_1979_microscope_biopsy_and_marshall_1981_perth_partnership", 99.5, 6.5, "A", False, "ROYAL PERTH HOSPITAL · 1979–1982", "Quality",
             "Quality: readable faces (pathologist Robin Warren looking through his microscope at a silver-stained stomach biopsy on his birthday, 11 June 1979, at Royal Perth Hospital, joined by young internal-medicine registrar Barry Marshall in July 1981).",
             STYLE + "In a pathology laboratory at Royal Perth Hospital in 1981, bearded pathologist Robin Warren peers through a binocular microscope at a stained biopsy slide while young doctor Barry Marshall leans in beside him." + QUAL_TAIL,
             {"kind": "FACT", "label": "Left over 5-day Easter", "when_stamp": "11 June 1979 · July 1981 · 13 April 1982", "timeline_step": "3/5 · 11 Jun 1979 & 13 Apr 1982 (Warren spots spiral bacteria; 5-day Easter incubator grows H. pylori)", "hold_s": 3.8}),
            ("02_warren_marshall_100_patient_easter_incubation_chart", 106.0, 8.0, "E", False, "0 COLONIES AT 48H VS 1 MM COLONIES AT 5 DAYS (100% DUODENAL ULCERS)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked biopsy and incubation chart from Warren and Marshall's 100-patient Perth study (1982–1984) shows 0 colonies at 48 hours (Plates #1–#34 discarded) vs 1 mm H. pylori colonies at 5 days (120 hours over Easter 1982 on Plate #35), present in 100% of duodenal ulcer patients (13/13) and 82% of gastric ulcer patients (18/22).",
             {"kind": "DATA", "label": "48H (0 COLONIES) VS 5-DAY EASTER INCUBATION (100% DUODENAL · 82% GASTRIC ULCERS)", "detail": "Inked biopsy & incubation chart on period paper from Warren & Marshall's 100-patient Perth study (1982–1984) showing 0 colonies at 48 hours vs 1 mm H. pylori colonies at 5 days (120 hours), present in 100% of duodenal ulcer patients (13/13) and 82% of gastric ulcer patients (18/22)", "scale": "throwing Petri dishes away after two days blinded doctors for decades — three extra days over the Easter weekend revealed the germ in nearly every duodenal ulcer patient", "hold_s": 3.8}),
            ("03_easter_tuesday_13_april_1982_incubator_plate_35_colonies", 114.0, 6.5, "B", False, "13 APRIL 1982 — PLATE #35", "Quality",
             "Quality: readable faces (on Tuesday 13 April 1982 at Royal Perth Hospital after the 5-day Easter holiday, Barry Marshall and Robin Warren hold up biopsy agar plate #35 covered in gleaming 1-millimetre transparent colonies of Helicobacter pylori).",
             STYLE + "Inside the Royal Perth Hospital microbiology room on 13 April 1982, Barry Marshall and Robin Warren hold a chocolate-agar Petri dish up to the window light, smiling at dozens of tiny glistening transparent colonies." + QUAL_TAIL,
             None),
            ("04_silver_stained_corkscrew_h_pylori_microscope_view_pan", 120.5, 5.5, "C", False, "SPIRAL BACTERIA UNDER MUCUS", "Fast",
             "Fast: daylight microscope view panning across curved, corkscrew-shaped black silver-stained Helicobacter pylori bacteria nestled beneath the golden-amber mucus layer of the stomach lining. Nothing emissive, no face.",
             STYLE + "Through a circular microscope field in bright transmitted light, dozens of curved spiral bacteria with fine tail flagella nestle along a warm amber mucosal ridge." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — The Doctor Who Drank a Billion Bacteria — Midpoint Twist",
        [
            ("01_marshall_july_1984_fremantle_drinking_billion_h_pylori_beaker", 126.0, 6.5, "A", False, "JULY 1984 · ONE BILLION BACTERIA", "Quality",
             "Quality: readable face (at Fremantle Hospital in July 1984, 32-year-old Dr Barry Marshall scrapes a Petri dish of live Helicobacter pylori into a glass beaker of beef broth and gulps the 10⁹ bacterial suspension down).",
             STYLE + "In a Fremantle Hospital laboratory in July 1984, thirty-two-year-old Dr Barry Marshall in a white coat scrapes colonies from an agar dish into a small glass beaker of broth and drinks it down in one bold gulp." + QUAL_TAIL,
             {"kind": "FACT", "label": "Drank a billion bacteria", "when_stamp": "16 June 1984 · July 1984 · 2005", "timeline_step": "4/5 · Jul 1984 (Marshall drinks 10⁹ H. pylori, proves gastritis on Day 10 & cures on Day 14)", "hold_s": 3.8}),
            ("02_marshall_14_day_self_experiment_and_urease_ammonia_diagram", 132.5, 8.0, "E", False, "DAY 0 (10⁹ CFU) → DAY 5 GASTRITIS → DAY 10 BIOPSY → DAY 14 CURE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked timeline and mechanism diagram of Barry Marshall's July 1984 self-experiment shows Day 0 (baseline clean biopsy + drinks 10⁹ H. pylori), Day 5–8 (achlorhydric vomiting & gastritis), Day 10 (biopsy proves heavy H. pylori colonisation), and Day 14 (cured by tinidazole antibiotic + bismuth), alongside H. pylori's urease enzyme splitting urea into alkaline ammonia (NH₃) to neutralise pH 1.5 acid.",
             {"kind": "DATA", "label": "MARSHALL'S 14-DAY SELF-EXPERIMENT & UREASE AMMONIA SHIELD", "detail": "Inked timeline and mechanism diagram on period paper of Barry Marshall's July 1984 self-experiment (Day 0: drinks 10⁹ H. pylori; Day 5–8: gastritis; Day 10: biopsy proof; Day 14: antibiotic + bismuth cure) alongside urease splitting urea into alkaline ammonia (NH₃)", "scale": "one billion spiral bacteria in a single glass of broth — using an enzyme shield to turn lethal stomach acid into a cosy neutral home in just five days", "hold_s": 3.8}),
            ("03_marshall_day_10_endoscopy_biopsy_and_2005_stockholm_nobel", 140.5, 6.5, "B", False, "DAY 10 BIOPSY PROOF", "Quality",
             "Quality: readable faces (Fremantle Hospital endoscopy suite in July 1984 on Day 10 as Barry Marshall undergoes a second biopsy proving swarms of H. pylori, dissolving to Robin Warren and Barry Marshall receiving their 2005 Nobel Prize medals in Stockholm).",
             STYLE + "Split scene: on the left in July 1984, Dr Barry Marshall sits in an examination room beside an endoscope tube and a positive biopsy slide; on the right in Stockholm in 2005, Barry Marshall and Robin Warren in evening dress hold their gold Nobel medals." + QUAL_TAIL,
             None),
            ("04_explorer_white_coat_corkscrew_bacterium_ammonia_umbrella", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Wearing a tiny white lab coat beside a giant corkscrew bacterium, the Explorer watches the microbe spin its tail propellers through the mucus layer while spraying an umbrella of pale alkaline mist that fizzes and neutralises falling red drops of acid." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Your Stomach Doesn't Digest Itself & the Sparks Inside Your Brain",
        [
            ("01_timeline_1822_2005_and_1mm_mucus_bicarbonate_barrier_chart", 152.5, 8.5, "E", False, "1 MM MUCUS-BICARBONATE SHIELD (PH 1.5 LUMEN VS PH 7.0 WALL)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 5-date timeline completes: 6 Jun 1822 & Dec 1823 (St. Martin's wound; Prout discovers gastric HCl) · May 1825–Dec 1833 (Beaumont's 238 silk-string experiments) · 11 Jun 1979 & 13 Apr 1982 (Warren & Marshall culture H. pylori over Easter) · Jul 1984 (Marshall drinks 10⁹ H. pylori & cures on Day 14) · 2005 (Nobel Prize), alongside an inked cross-section of the 1-millimetre mucus-bicarbonate shield keeping the stomach wall at neutral pH 7.0 against pH 1.5 lumen acid.",
             {"kind": "DATA", "label": "1822–2005 TIMELINE & 1 MM MUCUS-BICARBONATE SHIELD (PH 1.5 → PH 7.0)", "detail": "Animated 5-date timeline (1822 → 2005) alongside an inked cross-section of the 1-millimetre mucus-bicarbonate shield keeping the stomach wall at neutral pH 7.0 against pH 1.5 lumen acid", "scale": "a mucus-and-bicarbonate shield just one millimetre thick separates pH 1.5 acid strong enough to dissolve metal from the delicate pH 7.0 cells of your stomach wall", "fact_card": "1 mm mucus shield saves gut", "when_stamp": "1822–2005", "timeline_step": "5/5 · 2005 (Warren & Marshall win the Nobel Prize in Physiology or Medicine)", "hold_s": 3.8}),
            ("02_stomach_1mm_mucus_bicarbonate_layer_cross_section_macro", 161.0, 5.5, "A", False, "THE 1 MM BICARBONATE SHIELD", "Fast",
             "Fast: daylight macro cross-section model of the stomach lining showing a 1-millimetre translucent coat of mucus releasing fine alkaline bicarbonate bubbles that neutralise descending red acid droplets before they touch the pink epithelial cells below. Nothing emissive, no face.",
             STYLE + "In crisp daylight, a detailed cross-section shows a one-millimetre protective blanket of thick mucus releasing tiny alkaline bubbles that neutralise descending red droplets above healthy pink stomach cells." + FAST_TAIL,
             None),
            ("03_cajal_1888_barcelona_neurons_and_loewi_1921_frog_hearts_handoff", 166.5, 6.5, "C", False, "SPARKS AND SYNAPSES", "Quality",
             "Quality: readable faces (Spanish anatomist Santiago Ramón y Cajal in Barcelona in May 1888 sketching jet-black silver-stained brain neurons at his kitchen table, beside Otto Loewi in Graz in March 1921 waking at 3:00 a.m. to connect two beating frog hearts — handoff to 033 Neurons & Synapses).",
             STYLE + "Barcelona, May 1888, and Graz, March 1921: bearded Spanish anatomist Santiago Ramón y Cajal sketches branching black neurons beside a brass microscope at his kitchen table, while pharmacologist Otto Loewi transfers clear drops between two glass frog-heart chambers." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1887 · MARCH 1921", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_silk_string_vial_petri_dish_beaker (callback, £0).",
             "Reuse P1:07_table_three_props_silk_string_vial_petri_dish_beaker [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_silk_string_vial_petri_dish_beaker"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_silk_string_vial_petri_dish_beaker",
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
            "film": "032_Beaumont-Marshall-Stomach-Ulcers",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from ulcers_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "032_Beaumont-Marshall-Stomach-Ulcers",
        "version": "v01",
        "date": "2026-10-17",
        "owner": "gemini (J0494)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/032_Beaumont-Marshall-Stomach-Ulcers/ulcers_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/032_Beaumont-Marshall-Stomach-Ulcers/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_Balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032. Nothing in 032 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 032 Stomach Ulcers: Why a Doctor Drank a Beaker of Bacteria — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 17 Oct 2026, J0494. Built from `ulcers_script_master_v01.md` (91.6 PASS) and `SOURCES_v01.md`.",
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
        "# 032 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 17 Oct 2026, J0494. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `ulcers_script_master_v01.md` (91.6 PASS) and `SOURCES_v01.md` so 032's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (William Beaumont, Alexis St. Martin, Robin Warren, Barry Marshall, William Prout, Santiago Ramón y Cajal, Otto Loewi), Beaumont's candlelit cabin vial, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (Beaumont's pocket watch & silk-string food parcels pan, 3-object callback bench, 100 °F sand-bath glass vial dissolving beef, Beaumont's 1833 book & vials, silver-stained spiral H. pylori microscope field, 1 mm mucus-bicarbonate cross-section). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_stomach_acid_ph_1_5_and_h_pylori_ammonia_shield_chart` — pH 1.5–2.0 gastric HCl vs H. pylori urease ammonia shield causing ~80% of gastric and ~90% of duodenal ulcers (`SCALE: human stomach acid sits near pH 1.5 — strong enough to dissolve a zinc nail and a million times more acidic than pure water, yet H. pylori wraps itself in an ammonia bubble to survive inside it`)",
        "  2. `P1:06_ph_scale_bar_water_7_vs_gastric_acid_1_5_vs_battery_acid_card` — pH 7.0 pure water vs pH 2.2 lemon juice vs pH 1.5 human gastric juice (~10⁶× H⁺) vs pH 0.8 battery acid (`SCALE: stomach acid is nearly a million times more acidic than drinking water — so harsh that doctors assumed the stomach was as sterile as a bottle of bleach`)",
        "  3. `P2:02_beaumont_1833_digestion_time_chart_eggs_beef_pork` — Beaumont's December 1833 digestion-time chart: whipped eggs & tripe (~1h), boiled beef (~2h 45m), roast pork (~5h 15m) + 37.8 °C in-vitro HCl digestion (`SCALE: by pulling a silk thread in and out of a living stomach 238 times, Beaumont timed digestion to the minute — from one hour for eggs to over five hours for roast pork`)",
        "  4. `P3:02_warren_marshall_100_patient_easter_incubation_chart` — Warren & Marshall's 100-patient Perth study (0 colonies at 48h vs 1 mm colonies at 5 days over Easter 1982; 100% of duodenal ulcers [13/13] & 82% of gastric ulcers [18/22]) (`SCALE: throwing Petri dishes away after two days blinded doctors for decades — three extra days over the Easter weekend revealed the germ in nearly every duodenal ulcer patient`)",
        "  5. `P4:02_marshall_14_day_self_experiment_and_urease_ammonia_diagram` — Barry Marshall's July 1984 self-experiment (Day 0: 10⁹ CFU; Day 5–8: gastritis; Day 10: biopsy proof; Day 14: antibiotic + bismuth cure) + urease splitting urea into NH₃ (`SCALE: one billion spiral bacteria in a single glass of broth — using an enzyme shield to turn lethal stomach acid into a cosy neutral home in just five days`)",
        "  6. `P5:01_timeline_1822_2005_and_1mm_mucus_bicarbonate_barrier_chart` — completed 5-date timeline (1822 → 2005) + 1 mm mucus-bicarbonate shield keeping the stomach wall at pH 7.0 against pH 1.5 acid (`SCALE: a mucus-and-bicarbonate shield just one millimetre thick separates pH 1.5 acid strong enough to dissolve metal from the delicate pH 7.0 cells of your stomach wall`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_silk_string_vial_petri_dish_beaker`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"032 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
