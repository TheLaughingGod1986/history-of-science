#!/usr/bin/env python3
"""HOS 035 (Insulin & Diabetes: The 2 AM Note and the One-Dollar Patent) pre-VO plate boards v01. J0494. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/035_Banting-Best-Collip-Insulin/opening_and_outline_v00.md
and SOURCES_v00.md. Nothing is generation_authorized.
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
        "Part 01 — The 2:00 a.m. Note in Ontario and the Hospital Ward in Toronto",
        [
            ("01_banting_1920_2am_note_and_thompson_1922_toronto_awakening", 0.0, 5.5, "A", False, "THE $1 INSULIN MIRACLE", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + in a dim bedroom in London, Ontario, at 2:00 a.m. on 31 October 1920, 29-year-old surgeon Frederick Banting scribbles a 25-word note in his bedside pad, dissolving to Toronto General Hospital on 23 January 1922 as 14-year-old Leonard Thompson wakes and sits up after receiving James Collip's purified insulin injection.",
             STYLE + "In a dim bedroom in London, Ontario, at two in the morning on 31 October 1920, twenty-nine-year-old surgeon Frederick Banting scribbles a note in a bedside pad, dissolving to a bright ward at Toronto General Hospital on 23 January 1922 as fourteen-year-old Leonard Thompson sits up smiling beside a glass syringe." + QUAL_TAIL,
             {"kind": "WHEN", "label": "LONDON, ONTARIO, 31 OCTOBER 1920 · TORONTO, 23 JANUARY 1922", "timeline_step": "2/5 · 31 Oct 1920 (Banting's 2:00 a.m. 25-word note) & 4/5 · 23 Jan 1922 (Collip's purified insulin saves Leonard Thompson)", "hold_s": 3.5}),
            ("02_2am_notebook_collip_alcohol_flask_and_one_dollar_patent_split", 5.5, 6.0, "B", False, "NOTEBOOK, ALCOHOL, $1 PATENT", "Quality",
             "Quality: complex three-part split composition (Frederick Banting's 31 October 1920 2:00 a.m. notebook page and rooftop lab with Charles Best in July 1921 on the left; James Collip's 90% alcohol precipitation flask and Leonard Thompson's chart on 23 January 1922 in the centre; the $1 US patent assignment of January 1923 on the right).",
             STYLE + "Three-panel period composition: on the left, a small lined bedside notepad beside a glass syringe; in the centre, a chemist's glass flask with white snow-like insulin precipitate settling at the bottom; on the right, a ribboned patent parchment resting beside three silver one-dollar coins." + QUAL_TAIL,
             None),
            ("03_ward_h_toronto_11_january_1922_leonard_thompson_frail_in_bed", 11.5, 6.0, "C", False, "65 POUNDS — NEAR COMA", "Quality",
             "Quality: readable faces (inside Ward H at Toronto General Hospital on 11 January 1922, 14-year-old Leonard Thompson lies frail in bed as Frederick Banting and Charles Best check his bedside chart).",
             STYLE + "Inside a 1922 hospital ward in Toronto, young surgeon Frederick Banting and student Charles Best in white coats stand beside the bed of frail fourteen-year-old Leonard Thompson, checking his clinical chart." + QUAL_TAIL,
             {"kind": "WHEN", "label": "TORONTO, 11 JANUARY 1922", "hold_s": 3.5}),
            ("04_islets_of_langerhans_1_percent_and_520_to_120_mg_dl_glucose_chart", 17.5, 8.0, "E", False, "1%–2% ISLETS OF LANGERHANS · BLOOD GLUCOSE 520 → 120 MG/DL IN 24H", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked blood-sugar and islet chart shows the pancreas's two cell types — 98% digestive acinar cells (secreting trypsin that destroys insulin) vs 1%–2% Islets of Langerhans (discovered in 1869, secreting insulin) — alongside Leonard Thompson's blood glucose dropping from 520 mg/dL (5.2× normal) to 120 mg/dL within 24 hours of James Collip's purified insulin injection on 23 January 1922.",
             {"kind": "DATA", "label": "ISLETS OF LANGERHANS (1%–2%) & LEONARD THOMPSON GLUCOSE (520 → 120 MG/DL IN 24H)", "detail": "Inked blood-sugar and islet chart on period paper showing Islets of Langerhans making up 1%–2% of pancreas mass, and Leonard Thompson's blood glucose dropping from 520 mg/dL to 120 mg/dL within 24 hours on 23 January 1922", "scale": "the insulin-making islets make up barely one percent of your pancreas — a pinch of cells weighing a single gram — yet one purified shot dropped a dying boy's blood sugar more than fourfold in a single day", "who_card": "Frederick Banting (1891–1941) — Canadian surgeon and medical scientist · Charles Best (1899–1978) — Canadian-American medical student · John Macleod (1876–1935) — Scottish physiologist · James Collip (1892–1965) — Canadian biochemist", "when_stamp": "31 October 1920 · 30 July 1921 · 23 January 1922", "hold_s": 3.8}),
            ("05_chilled_mortar_pestle_ringer_saline_and_glass_syringe_pan", 25.5, 5.5, "A", False, "TORONTO ROOFTOP LAB, 1921", "Fast",
             "Fast: daylight macro pan across Banting and Best's chilled porcelain mortar and pestle, a bottle of Ringer's saline solution, filter paper in a glass funnel, and a graduated glass syringe on a wooden bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a laboratory bench, the camera pans across a chilled porcelain mortar and pestle, a glass funnel with filter paper, a bottle of clear saline, and a graduated glass syringe." + FAST_TAIL,
             None),
            ("06_85g_pancreas_vs_1g_islets_and_520_vs_120_mg_dl_vials_card", 31.0, 8.0, "E", False, "ONE GRAM OF CELLS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked mass and concentration bar compares a whole ~85-gram human pancreas (98% digestive enzyme tissue) against ~1 gram of Islets of Langerhans (1%–2% of mass, lighter than a paperclip) and two blood-test vials showing 520 mg/dL vs 120 mg/dL glucose.",
             {"kind": "DATA", "label": "85 G PANCREAS (98% DIGESTIVE ENZYMES) VS ~1 G ISLETS OF LANGERHANS (1%–2%)", "detail": "Inked mass & concentration bar comparing an ~85 g human pancreas (98% digestive enzyme tissue) vs ~1 g of Islets of Langerhans (1%–2%) and blood glucose falling from 520 mg/dL to 120 mg/dL", "scale": "one gram of islet cells is lighter than a single paperclip — hidden inside ninety-eight percent digestive tissue that destroys them the moment you grind the organ up", "hold_s": 3.8}),
            ("07_table_three_props_2am_note_alcohol_flask_one_dollar_patent", 39.0, 5.5, "C", False, "1920 TO 1923", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Banting's bedside notebook and pencil, Collip's glass precipitation flask and insulin vial, and the 1923 patent sheet with three silver dollar coins). Nothing emissive.",
             STYLE + "On a wooden workbench in soft window light sit three objects side by side: a small lined notepad with a wooden pencil, a clear glass vial beside a precipitation flask, and a folded parchment document with three silver coins." + FAST_TAIL,
             None),
            ("08_explorer_golden_insulin_key_unlocking_cell_door_for_sugar_cubes", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing before a locked cell door while white sugar cubes pile up outside in the bloodstream channel, the Explorer inserts a tiny golden insulin key into the receptor lock: the door swings wide open and the sugar cubes tumble inside." + EXP_TAIL,
             None),
            ("09_banting_and_best_rooftop_lab_july_1921_with_dog_marjorie", 67.5, 5.5, "B", False, "TORONTO, 30 JULY 1921", "Quality",
             "Quality: readable faces (Frederick Banting and 22-year-old Charles Best in the rooftop laboratory at the University of Toronto in July 1921 holding a glass syringe as playful dog Marjorie wags her tail beside them).",
             STYLE + "In a sunlit University of Toronto rooftop laboratory in July 1921, Frederick Banting and young student Charles Best in rolled-up sleeves smile beside a healthy terrier wagging her tail on an examination table." + QUAL_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — Starving in a Sea of Sugar & the 2:00 a.m. Notebook",
        [
            ("01_minkowski_1889_strasbourg_and_banting_1920_london_ontario_4_dollars", 73.0, 6.5, "A", False, "EARNED $4 HIS FIRST MONTH", "Quality",
             "Quality: readable faces (Oskar Minkowski in Strasbourg in 1889 linking the pancreas to diabetes, alongside 29-year-old Frederick Banting in London, Ontario, on 30–31 October 1920 reading Moses Barron's paper in his empty medical office).",
             STYLE + "Split period scene: on the left in Strasbourg in 1889, bearded physician Oskar Minkowski inspects a laboratory jar beside a microscope; on the right in London, Ontario, in October 1920, young surgeon Frederick Banting reads a medical journal at his desk." + QUAL_TAIL,
             {"kind": "WHO", "label": "Oskar Minkowski (1858–1931) — German-Russian physician and physiologist", "fact_card": "Earned $4 his first month", "when_stamp": "1869 · 1889 · 31 October 1920", "timeline_step": "1/5 · 1869 & 1889 (Langerhans spots islets; Minkowski links pancreas to diabetes)", "hold_s": 3.8}),
            ("02_whole_ground_pancreas_trypsin_destruction_vs_duct_ligation_diagram", 79.5, 8.0, "E", False, "98% TRYPSIN ENZYME DESTRUCTION VS BANTING'S DUCT-LIGATION METHOD", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked comparison diagram contrasts a whole ground pancreas (98% acinar trypsin enzymes digesting and destroying the 1%–2% islet insulin) against Frederick Banting's 31 October 1920 duct-ligation method (acinar enzyme cells degenerate over 6–8 weeks, leaving pure insulin-producing Islets of Langerhans intact).",
             {"kind": "DATA", "label": "WHOLE GROUND PANCREAS (98% TRYPSIN DESTROYS INSULIN) VS DUCT LIGATION (ISLETS INTACT)", "detail": "Inked comparison diagram on period paper showing a whole ground pancreas (98% acinar trypsin enzymes destroying the 1%–2% islet insulin) vs Banting's 31 October 1920 duct-ligation method (acinar cells degenerate, leaving pure Islets of Langerhans intact)", "scale": "ninety-eight percent of the pancreas is a factory of meat-dissolving digestive enzymes — so grinding up a whole pancreas was like throwing a delicate hormone key straight into a vat of acid", "hold_s": 3.8}),
            ("03_banting_31_october_1920_bedside_notepad_25_words_closeup", 87.5, 6.5, "B", False, "31 OCTOBER 1920 — 2:00 A.M.", "Fast",
             "Fast: daylight close-up of Frederick Banting's small lined bedside notepad and wooden pencil resting beside an open medical journal and a brass pocket watch showing two o'clock. Nothing emissive, no face.",
             STYLE + "In soft daylight on a bedside table, a small lined notepad and wooden pencil rest beside an open medical journal and a brass pocket watch pointing to two o'clock." + FAST_TAIL,
             None),
            ("04_microscope_view_islets_of_langerhans_islands_in_acinar_tissue", 94.0, 5.5, "C", False, "ISLETS OF LANGERHANS · 1869", "Fast",
             "Fast: daylight circular microscope view showing pale round clusters of Islets of Langerhans scattered like tiny islands (~1%–2% of the tissue) surrounded by darker digestive acinar cells. Nothing emissive, no face.",
             STYLE + "Through a circular microscope field in bright transmitted light, pale round cell islands stand out clearly amidst darker surrounding pancreatic tissue." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — The Coin Flip, the Rooftop Lab & Dog #408",
        [
            ("01_best_and_noble_may_1921_coin_flip_and_macleod_toronto_lab", 99.5, 6.5, "A", False, "BEST WON A COIN TOSS", "Quality",
             "Quality: readable faces (22-year-old physiology students Charles Best and Clark Noble flipping a silver coin at the University of Toronto in May 1921 while Professor John Macleod hands Frederick Banting the keys to the rooftop laboratory).",
             STYLE + "At the University of Toronto in May 1921, two twenty-two-year-old students, Charles Best and Clark Noble, flip a silver coin in a sunlit corridor while Professor John Macleod hands laboratory keys to Frederick Banting." + QUAL_TAIL,
             {"kind": "FACT", "label": "Best won a coin toss", "when_stamp": "17 May 1921 · 30 July 1921 · November 1921", "timeline_step": "3/5 · 30 Jul 1921 (Banting & Best's islet extract drops Dog #408's blood sugar by 40% in 1h)", "hold_s": 3.8}),
            ("02_dog_408_30_july_1921_blood_glucose_200_to_120_mg_dl_curve", 106.0, 8.0, "E", False, "30 JULY 1921 (DOG #408): 4 ML EXTRACT DROPS BLOOD SUGAR 200 → 120 MG/DL IN 1H (−40%)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked blood-glucose curve from Banting and Best's 30 July 1921 Toronto lab notebook (Dog #408) shows venous blood glucose falling from 0.20% (200 mg/dL) to 0.12% (120 mg/dL) — a 40% drop in 1 hour — after 4 mL of chilled degenerated pancreas extract.",
             {"kind": "DATA", "label": "30 JULY 1921 (DOG #408): 4 ML EXTRACT → BLOOD GLUCOSE 200 → 120 MG/DL IN 1 HOUR", "detail": "Inked blood-glucose curve on period paper from Banting & Best's 30 July 1921 Toronto lab notebook (Dog #408) showing blood glucose falling from 200 mg/dL to 120 mg/dL (−40%) in 1 hour after 4 mL of degenerated pancreas extract", "scale": "four millilitres of chilled saltwater extract — less than a single teaspoon — dropped a dying dog's blood sugar by forty percent in sixty minutes", "hold_s": 3.8}),
            ("03_banting_and_best_30_july_1921_colorimeter_blood_sugar_test", 114.0, 6.5, "B", False, "30 JULY 1921 — 0.20 TO 0.12", "Quality",
             "Quality: readable faces (Frederick Banting and Charles Best on 30 July 1921 in the sweltering Toronto rooftop lab holding up a Duboscq colorimeter tube showing Dog #408's blood sugar plunged from 0.20% to 0.12%).",
             STYLE + "In the Toronto rooftop laboratory on 30 July 1921, Charles Best peers into a brass colorimeter beside colored glass test tubes and turns excitedly to Frederick Banting as their terrier stands up alertly." + QUAL_TAIL,
             None),
            ("04_duboscq_colorimeter_and_graduated_test_tubes_bench_closeup", 120.5, 5.5, "C", False, "4 ML SALTWATER EXTRACT", "Fast",
             "Fast: daylight macro shot of Charles Best's brass Duboscq blood-sugar colorimeter beside a rack of blue Folin-Wu glucose test tubes and a 5 mL glass syringe on a wooden lab bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a laboratory table, a brass optical colorimeter stands beside a wooden rack of blue-tinted glass test tubes and a small graduated glass syringe." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — The Failed First Shot, the Alcohol Secret & the $1 Patent — Midpoint Twist",
        [
            ("01_collip_january_1922_90_percent_alcohol_purification_and_1_dollar_patent", 126.0, 6.5, "A", False, "SOLD PATENT FOR $1 EACH", "Quality",
             "Quality: readable faces (visiting biochemist James Collip in Toronto in January 1922 holding up a glass flask where pure insulin precipitates like white snow at >90% alcohol, dissolving to Banting, Best, and Collip in January 1923 signing the US insulin patent over to the University of Toronto for $1 each).",
             STYLE + "Split period scene: on the left in January 1922, biochemist James Collip in a white lab coat holds a glass flask up to the window light as fine white insulin floccules settle in clear alcohol; on the right in January 1923, Banting, Best, and Collip sign a patent parchment beside three silver one-dollar coins." + QUAL_TAIL,
             {"kind": "FACT", "label": "Sold patent for $1 each", "when_stamp": "11 January 1922 · 23 January 1922 · 23 January 1923 · October 1923", "timeline_step": "4/5 · 23 Jan 1922 (Collip's 90%–95% alcohol insulin saves Leonard Thompson) & 5/5 · 23 Jan & Oct 1923 ($1 patent & Nobel Prize)", "hold_s": 3.8}),
            ("02_11_jan_crude_extract_vs_23_jan_1922_collip_purified_insulin_chart", 132.5, 8.0, "E", False, "11 JAN CRUDE (440 → 320 MG/DL, ABSCESS) VS 23 JAN COLLIP PURIFIED (520 → 120 MG/DL IN 24H)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked purification and clinical chart compares Banting and Best's 11 January 1922 crude extract (blood glucose 440 → 320 mg/dL, sterile abscess, ketones unchanged) against James Collip's 90%–95% alcohol-purified insulin on 23 January 1922 (Leonard Thompson's blood glucose 520 → 120 mg/dL in 24h; 24-hour urine glucose 71.1 g → 8.7 g).",
             {"kind": "DATA", "label": "11 JAN CRUDE (440 → 320 MG/DL) VS 23 JAN COLLIP 90%–95% ALCOHOL INSULIN (520 → 120 MG/DL)", "detail": "Inked purification & clinical chart on period paper comparing 11 January 1922 crude extract (440 → 320 mg/dL, abscess) vs James Collip's 90%–95% alcohol-purified insulin on 23 January 1922 (Leonard Thompson's blood glucose 520 → 120 mg/dL in 24h; urine glucose 71.1 g → 8.7 g)", "scale": "raising alcohol from 80% to 95% turned a muddy extract that caused abscesses into a crystal-clear cure that dropped a dying teenager's blood sugar from 520 to 120 in a single day", "hold_s": 3.8}),
            ("03_toronto_ward_1922_children_waking_from_diabetic_comas", 140.5, 6.5, "B", False, "23 JANUARY 1922 — AWAKENING", "Quality",
             "Quality: readable faces (Toronto hospital ward in early 1922 as Frederick Banting, Charles Best, and James Collip move along a row of beds with purified insulin and joyful parents embrace children sitting up awake).",
             STYLE + "Inside a sunlit 1922 Toronto hospital ward, doctors Frederick Banting, Charles Best, and James Collip walk between white iron beds as recovering children sit up and embrace their relieved parents." + QUAL_TAIL,
             None),
            ("04_explorer_graduated_alcohol_cylinder_80_to_95_percent_snow_flask", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Pouring clear alcohol from a graduated cylinder into a glass flask of muddy brown extract, the Explorer filters out dark impurities at the first mark, then pours to the top mark and claps as pure white insulin crystals drift down like snow." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Sugar Doesn't Cause Type 1 Diabetes & the Two Oranges That Cured Scurvy",
        [
            ("01_timeline_1869_1923_and_type1_vs_type2_51_amino_acids_chart", 152.5, 8.5, "E", False, "1869–1923 TIMELINE · TYPE 1 (NO KEY) VS TYPE 2 (RUSTED LOCK) · 51 AMINO ACIDS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 5-date timeline completes: 1869 & 1889 (Langerhans & Minkowski) · 31 Oct 1920 (Banting's 2:00 a.m. note) · 30 Jul 1921 (Banting & Best save Dog #408) · 23 Jan 1922 (Collip's purified insulin saves Leonard Thompson) · 23 Jan & Oct 1923 ($1 patent & 4-way shared Nobel Prize), alongside an inked diagram comparing Type 1 (autoimmune loss of beta cells = missing insulin key) vs Type 2 (insulin-resistant receptor lock) and Sanger's 51-amino-acid human insulin structure.",
             {"kind": "DATA", "label": "1869–1923 TIMELINE & TYPE 1 (MISSING KEY) VS TYPE 2 (RESISTANT LOCK) · 51 AMINO ACIDS", "detail": "Animated 5-date timeline (1869 → 1923) alongside an inked comparison of Type 1 (missing insulin key) vs Type 2 (resistant receptor lock) and human insulin's 51 amino acids (sequenced 1955, recombinant E. coli 1978)", "scale": "fifty-one amino acids linked into one tiny protein molecule — sold for a single dollar in 1923 so hundreds of millions of people could live", "fact_card": "51 amino acids save millions", "when_stamp": "1955 · 1978", "timeline_step": "5/5 · 23 Jan & Oct 1923 (Banting, Best & Collip sell US patent for $1 each; Nobel shared four ways)", "hold_s": 3.8}),
            ("02_type1_missing_key_vs_type2_resistant_lock_cell_models_macro", 161.0, 5.5, "A", False, "MISSING KEY VS RUSTED LOCK", "Fast",
             "Fast: daylight tabletop anatomical model comparing two cell doors side by side: on the left, a pristine keyhole with no golden insulin key present (Type 1); on the right, a golden insulin key pressing against a stiff, corroded lock mechanism (Type 2). Nothing emissive, no face.",
             STYLE + "In crisp daylight, a two-part brass and wood mechanical model contrasts an empty keyhole on a closed cell door on the left with a golden key meeting a stiff, rusted lock on the right." + FAST_TAIL,
             None),
            ("03_lind_1747_hms_salisbury_oranges_and_eijkman_1890_java_rice_handoff", 166.5, 6.5, "C", False, "TWO ORANGES & THE FIRST CLINICAL TRIAL", "Quality",
             "Quality: readable faces (Scottish Royal Navy surgeon James Lind aboard HMS Salisbury on 20 May 1747 handing two oranges and a lemon to scurvy-stricken sailors in the world's first controlled clinical trial, beside Dutch physician Christiaan Eijkman in Java in 1890 feeding unpolished brown rice to chickens — handoff to 036 Scurvy & Vitamins).",
             STYLE + "Aboard HMS Salisbury on 20 May 1747 and in Java in 1890: Royal Navy surgeon James Lind in a blue eighteenth-century coat hands two fresh oranges and a lemon to a sailor in a wooden ship sickbay, while Dutch doctor Christiaan Eijkman feeds brown rice to lively chickens in a tropical courtyard." + QUAL_TAIL,
             {"kind": "WHEN", "label": "20 MAY 1747 · 1890", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_2am_note_alcohol_flask_one_dollar_patent (callback, £0).",
             "Reuse P1:07_table_three_props_2am_note_alcohol_flask_one_dollar_patent [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_2am_note_alcohol_flask_one_dollar_patent"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_2am_note_alcohol_flask_one_dollar_patent",
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
            "film": "035_Banting-Best-Collip-Insulin",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from opening_and_outline_v00.md; retimes onto Scribe STT once VO locks)",
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
        "film": "035_Banting-Best-Collip-Insulin",
        "version": "v01",
        "date": "2026-10-17",
        "owner": "gemini (J0494)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/035_Banting-Best-Collip-Insulin/opening_and_outline_v00.md",
        "sources": "00_Brand/Channel-Setup/ideas/035_Banting-Best-Collip-Insulin/SOURCES_v00.md",
        "credit_snapshot": {
            "flow_Balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035. Nothing in 035 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 035 Insulin & Diabetes: The 2 AM Note and the One-Dollar Patent — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 17 Oct 2026, J0494. Built from `opening_and_outline_v00.md` and `SOURCES_v00.md`.",
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
        "# 035 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 17 Oct 2026, J0494. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `opening_and_outline_v00.md` and `SOURCES_v00.md` so 035's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Frederick Banting, Charles Best, John Macleod, James Collip, Leonard Thompson, Oskar Minkowski, James Lind, Christiaan Eijkman), and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (chilled mortar & pestle with Ringer's saline & glass syringe pan, 3-object callback bench, 31 Oct 1920 2:00 a.m. notepad & pocket watch, microscope view of Islets of Langerhans, Duboscq blood-sugar colorimeter & Folin-Wu tubes, Type 1 missing key vs Type 2 resistant lock mechanical model). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_islets_of_langerhans_1_percent_and_520_to_120_mg_dl_glucose_chart` — Islets of Langerhans (1%–2% of pancreas mass) + Leonard Thompson's blood glucose dropping from 520 mg/dL to 120 mg/dL in 24 hours on 23 Jan 1922 (`SCALE: the insulin-making islets make up barely one percent of your pancreas — a pinch of cells weighing a single gram — yet one purified shot dropped a dying boy's blood sugar more than fourfold in a single day`)",
        "  2. `P1:06_85g_pancreas_vs_1g_islets_and_520_vs_120_mg_dl_vials_card` — ~85 g human pancreas (98% digestive enzyme tissue) vs ~1 g Islets of Langerhans (<1 paperclip) + 520 vs 120 mg/dL vials (`SCALE: one gram of islet cells is lighter than a single paperclip — hidden inside ninety-eight percent digestive tissue that destroys them the moment you grind the organ up`)",
        "  3. `P2:02_whole_ground_pancreas_trypsin_destruction_vs_duct_ligation_diagram` — whole ground pancreas (98% acinar trypsin destroys insulin) vs Banting's 31 Oct 1920 duct-ligation degeneration method leaving pure Islets intact (`SCALE: ninety-eight percent of the pancreas is a factory of meat-dissolving digestive enzymes — so grinding up a whole pancreas was like throwing a delicate hormone key straight into a vat of acid`)",
        "  4. `P3:02_dog_408_30_july_1921_blood_glucose_200_to_120_mg_dl_curve` — Banting & Best's 30 July 1921 Dog #408 blood-glucose curve: 4 mL extract drops blood glucose from 200 mg/dL to 120 mg/dL (−40%) in 1 hour (`SCALE: four millilitres of chilled saltwater extract — less than a single teaspoon — dropped a dying dog's blood sugar by forty percent in sixty minutes`)",
        "  5. `P4:02_11_jan_crude_extract_vs_23_jan_1922_collip_purified_insulin_chart` — 11 Jan 1922 crude extract (440 → 320 mg/dL, abscess) vs James Collip's 23 Jan 1922 90%–95% alcohol-purified insulin (520 → 120 mg/dL in 24h; urine glucose 71.1 g → 8.7 g) (`SCALE: raising alcohol from 80% to 95% turned a muddy extract that caused abscesses into a crystal-clear cure that dropped a dying teenager's blood sugar from 520 to 120 in a single day`)",
        "  6. `P5:01_timeline_1869_1923_and_type1_vs_type2_51_amino_acids_chart` — completed 5-date timeline (1869 → 1923) + Type 1 (missing key) vs Type 2 (resistant lock) + human insulin's 51 amino acids (`SCALE: fifty-one amino acids linked into one tiny protein molecule — sold for a single dollar in 1923 so hundreds of millions of people could live`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_2am_note_alcohol_flask_one_dollar_patent`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"035 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
