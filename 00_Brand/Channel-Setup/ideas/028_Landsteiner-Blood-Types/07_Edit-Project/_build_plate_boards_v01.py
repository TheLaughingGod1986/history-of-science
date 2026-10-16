#!/usr/bin/env python3
"""HOS 028 (Blood Types: Why Transfusions Killed Half of All Patients) pre-VO plate boards v01. J0463. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/028_Landsteiner-Blood-Types/landsteiner_script_master_v01.md
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
        "Part 01 — The Six Vials in Vienna That Saved a Hundred Million Lives",
        [
            ("01_landsteiner_vienna_1900_6x6_blood_slide_grid", 0.0, 5.5, "A", False, "WHY DID BLOOD CLUMP?", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + thirty-one-year-old Karl Landsteiner in his Vienna pathology laboratory in February 1900 pipetting clear golden blood serum onto a 6 × 6 grid of red blood drops on glass slides as half stay smooth ruby-red and half curdle into clumps.",
             STYLE + "In a Vienna pathology laboratory in February 1900, thirty-one-year-old Karl Landsteiner pipettes clear golden serum onto a six-by-six grid of red blood drops on glass slides: half the drops stay smooth ruby-red while the other half curdle into dark clumps." + QUAL_TAIL,
             {"kind": "WHEN", "label": "VIENNA · FEBRUARY 1900", "timeline_step": "3/6 · Feb 1900 & 14 Nov 1901 (Landsteiner discovers A, B, and O blood groups)", "hold_s": 3.5}),
            ("02_denys_1667_calf_landsteiner_grid_lewisohn_citrate_split", 5.5, 6.0, "B", False, "BAN, CLUMPS, BLOOD BANK", "Quality",
             "Quality: readable faces (Jean-Baptiste Denys in 1667 Paris holding a silver transfusion quill on the left; Karl Landsteiner examining his glass slide grid in the centre; Richard Lewisohn lifting a chilled bottle of citrated blood in 1915 on the right).",
             STYLE + "Three-panel period composition: on the left, seventeenth-century physician Jean-Baptiste Denys holds a silver quill tube beside a calf; in the centre, Karl Landsteiner inspects a grid of glass slides; on the right, surgeon Richard Lewisohn lifts a glass bottle of liquid red blood from an icebox." + QUAL_TAIL,
             None),
            ("03_denys_paris_december_1667_transfusion_ban", 11.5, 6.0, "C", False, "BANNED FOR 150 YEARS", "Quality",
             "Quality: readable face (Jean-Baptiste Denys in a candlelit Paris room in December 1667 disconnecting a silver transfusion quill as French magistrates seal the 1668–1670 edict outlawing human blood transfusions).",
             STYLE + "In a candlelit Paris chamber in December 1667, royal physician Jean-Baptiste Denys steps back in alarm holding a silver cannula while a black-robed magistrate presses a red wax seal onto a formal court edict." + QUAL_TAIL,
             {"kind": "WHO", "label": "Jean-Baptiste Denys (1643–1704) — French royal physician", "when_stamp": "Paris, December 1667", "timeline_step": "1/6 · Dec 1667 (Denys calf-blood crisis & 150-year transfusion ban)", "hold_s": 3.8}),
            ("04_landsteiner_1901_6x6_agglutination_matrix_chart", 17.5, 8.0, "E", False, "6 × 6 GRID → GROUPS A, B, AND O", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked 6 × 6 cross-reaction matrix from Karl Landsteiner's 14 November 1901 Vienna paper ('Über Agglutinationserscheinungen normalen menschlichen Blutes') tests the sera and red cells of six healthy lab colleagues (Dr St., Dr Plecnik, Dr Sturl, Dr Erdheim, Zaritsch, and Landsteiner), sorting human blood into Group A, Group B, and Group C (O).",
             {"kind": "DATA", "label": "14 NOV 1901 · 6 × 6 AGGLUTINATION TABLE (GROUPS A, B, AND C/O)", "detail": "Inked 6 × 6 agglutination table on period paper from Landsteiner's 14 November 1901 paper showing smooth mixing (–) vs fatal clumping (+) across Groups A, B, and C (O)", "scale": "a single mismatched transfusion can clump and shatter billions of red blood cells inside a patient's veins in minutes", "who_card": "Karl Landsteiner (1868–1943) — Austrian pathologist and immunologist", "when_stamp": "February 1900 · 14 November 1901", "hold_s": 3.8}),
            ("05_hand_cranked_centrifuge_and_six_vials_pan", 25.5, 5.5, "A", False, "VIENNA, NOVEMBER 1901", "Fast",
             "Fast: daylight pan across a brass hand-cranked laboratory centrifuge spinning six glass test tubes separated into dark red cells at the bottom and clear amber serum on top between code graphics so two full-frame graphics never run back to back. Nothing emissive.",
             STYLE + "In soft window light on a Vienna laboratory bench, a brass hand-cranked centrifuge slows to a stop, holding six glass tubes with dark red blood cells settled at the bottom and clear golden serum on top." + FAST_TAIL,
             None),
            ("06_6_min_clotting_vs_0_2_percent_sodium_citrate_scale_chart", 31.0, 8.0, "E", False, "0.2% SODIUM CITRATE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked coagulation and scale comparison contrasts untreated drawn blood clotting solid in glass in 4–6 minutes against blood mixed with 0.2% sodium citrate (2 g per litre, less than half a teaspoon) staying liquid in cold storage for 2–3 weeks, enabling 118.5 million donations/year.",
             {"kind": "DATA", "label": "4–6 MIN CLOT VS 2–3 WEEKS LIQUID (0.2% SODIUM CITRATE)", "detail": "Inked coagulation & scale chart comparing 4–6 minutes (untreated blood clotting in glass) vs 2–3 weeks (with 0.2% sodium citrate in cold storage) and 118.5 million safe blood donations per year today", "scale": "just two grammes of sodium citrate per litre of blood — less than half a teaspoon — turned a 6-minute surgical emergency into modern blood banks", "who_card": "Richard Lewisohn (1875–1961) — German-American surgeon", "when_stamp": "23 January 1915", "timeline_step": "4/6 · 23 Jan 1915 & Nov 1917 (Lewisohn's 0.2% sodium citrate & WWI blood bank)", "hold_s": 3.8}),
            ("07_table_three_props_centrifuge_vials_6x6_slide_citrate_bottle", 39.0, 5.5, "C", False, "SIX VIALS AND CITRATE", "Fast",
             "Fast: daylight prop table (callback source for Part 05: rack of six separated blood-and-serum glass vials, 6 × 6 glass slide tray, chilled glass transfusion bottle with a porcelain dish of white sodium citrate crystals). Nothing emissive.",
             STYLE + "On a wooden laboratory bench in soft window light sit three objects side by side: a wooden rack holding six glass vials of separated red cells and golden serum, a glass tray of thirty-six test drops, and a glass transfusion bottle beside white citrus salt crystals." + FAST_TAIL,
             None),
            ("08_explorer_snapping_y_antibodies_onto_a_and_o_cells", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside two oversized red blood cell models on the bench — one studded with triangular pegs and one completely smooth — the Explorer snaps Y-shaped brass clasps onto the pegged sphere so they lock tight, then watches them slide harmlessly off the smooth sphere." + EXP_TAIL,
             None),
            ("09_serum_drop_curdling_red_blood_cells_closeup", 67.5, 5.5, "B", False, "INSTANT AGGLUTINATION", "Fast",
             "Fast: daylight macro shot of a glass pipette dropping clear amber serum onto a smooth ruby-red drop on a glass slide, which immediately separates into tiny brick-red clumps. Nothing emissive, no face.",
             STYLE + "In crisp daylight, a glass dropper releases a single drop of clear amber serum onto a smooth ruby-red drop on a glass slide; within seconds the smooth red liquid curdles into distinct brick-red granules." + FAST_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — Sheep's Blood, the 150-Year Ban, and the Clumping Mystery",
        [
            ("01_denys_june_and_december_1667_lamb_and_calf_transfusions", 73.0, 6.5, "A", False, "PARIS · JUNE & DEC 1667", "Quality",
             "Quality: readable face (Jean-Baptiste Denys in Paris on 15 June 1667 transfusing 9 ounces of lamb's blood, followed by the fatal December 1667 Antoine Mauroy calf-blood crisis and the 1670 ban).",
             STYLE + "Paris, June and December 1667: royal physician Jean-Baptiste Denys holds a silver tube between a gentle lamb and a seated patient, then looks on in dismay as dark haemolysed fluid fills a glass flask." + QUAL_TAIL,
             {"kind": "FACT", "label": "Animal blood banned in 1670", "when_stamp": "15 June 1667 · December 1667 · 1670", "hold_s": 3.8}),
            ("02_1667_animal_vs_1818_blundell_untyped_vs_1901_abo_chart", 79.5, 8.0, "E", False, "1818 BLUNDELL: ~50% RANDOM CLUMPING", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked compatibility and survival chart compares 1667 animal-to-human transfusions (cross-species haemolysis, banned 1668–1670), James Blundell's 22 December 1818 – 1829 un-typed human-to-human transfusions (~50% random ABO incompatibility / coin-toss mortality), and 1901 ABO-matched transfusions.",
             {"kind": "DATA", "label": "1667 ANIMAL BAN → 1818 UN-TYPED (~50% INCOMPATIBLE) → 1901 ABO MATCH", "detail": "Inked timeline & survival chart on period paper comparing 1667 animal-to-human transfusions (banned 1668–1670), Blundell's 1818–1829 un-typed human-to-human transfusions (~50% random incompatibility), and 1901 ABO-matched transfusions", "scale": "flipping a coin with a patient's life — before blood typing, nearly half of all human blood transfusions triggered a dangerous or fatal immune reaction", "who_card": "James Blundell (1790–1878) — English obstetrician and physiologist", "when_stamp": "22 December 1818 · 1829", "timeline_step": "2/6 · 22 Dec 1818 (Blundell's first human-to-human transfusion)", "hold_s": 3.8}),
            ("03_landois_1875_greifswald_microscope_agglutination", 87.5, 6.5, "B", False, "CLUMPING AND BURSTING", "Quality",
             "Quality: readable face (German physiologist Leonard Landois in Greifswald in 1875 peering through a brass microscope at red blood cells clumping and bursting).",
             STYLE + "Greifswald, Germany, 1875: bearded physiologist Leonard Landois peers intently through a tall brass monocular microscope beside glass slides of clumped red blood cells." + QUAL_TAIL,
             {"kind": "WHO", "label": "Leonard Landois (1837–1902) — German physiologist", "when_stamp": "1875", "hold_s": 3.8}),
            ("04_blundell_brass_gravitator_and_syringe_bench", 94.0, 5.5, "C", False, "BLUNDELL'S BRASS SYRINGE", "Fast",
             "Fast: daylight close-up of James Blundell's nineteenth-century brass transfusion syringe and funnel apparatus mounted on a mahogany stand. Nothing emissive, no face.",
             STYLE + "In crisp window light, the camera tracks across an early nineteenth-century brass transfusion syringe with a conical receiving cup and flexible tubing mounted on a mahogany stand." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — Six Scientists' Blood in a 6 × 6 Grid",
        [
            ("01_landsteiner_and_five_colleagues_drawing_vials_vienna", 99.5, 6.5, "A", False, "SIX HEALTHY SCIENTISTS", "Quality",
             "Quality: readable faces (thirty-one-year-old Karl Landsteiner and his five healthy laboratory colleagues at the University of Vienna in 1900–1901 collecting small glass vials of their own blood).",
             STYLE + "University of Vienna, 1900–1901: Karl Landsteiner in a white lab coat and five healthy colleagues stand around a laboratory bench placing six small glass vials of blood into a brass centrifuge." + QUAL_TAIL,
             {"kind": "FACT", "label": "First printed in a footnote", "when_stamp": "February 1900 · 14 November 1901", "hold_s": 3.8}),
            ("02_abo_surface_antigens_2_million_markers_and_antibodies_diagram", 106.0, 8.0, "E", False, "~2 MILLION A/B MARKERS PER CELL", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked molecular diagram shows red blood cell surface antigens (~2 million A or B sugar markers per cell: Type A with A pegs, Type B with B spheres, Type AB with both, Type O smooth) and Y-shaped plasma antibodies (anti-B, anti-A, none, both), demonstrating why Type O red cells pass unattacked as universal donor.",
             {"kind": "DATA", "label": "TYPE A, B, AB, O (~2M ANTIGEN SITES/CELL) & ANTI-A / ANTI-B ANTIBODIES", "detail": "Inked molecular diagram on period paper showing red blood cell surface antigens (A pegs, B spheres, AB both, O smooth) and Y-shaped plasma antibodies demonstrating why Type O red cells are universal donor", "scale": "each red blood cell carries around 2 million microscopic A or B sugar markers on its skin — if the wrong antibody locks on, millions of cells glue together like Velcro", "who_card": "Alfred von Decastello (1872–1960) — Austrian physician · Adriano Sturli (1873–1964) — Austrian physician", "when_stamp": "1902", "hold_s": 3.8}),
            ("03_landsteiner_group_o_row_staying_smooth_on_slide_grid", 114.0, 6.5, "B", False, "GROUP A, B, AND O", "Quality",
             "Quality: readable face (Karl Landsteiner leaning over his 36-drop glass slide grid on 14 November 1901 and pointing to his own Group C/O row where every drop stays smooth ruby-red).",
             STYLE + "Vienna, 14 November 1901: Karl Landsteiner leans closely over a six-by-six grid of glass slides with a magnifying lens, pointing to the bottom row where every drop of his own red cells stays smooth and unclumped." + QUAL_TAIL,
             None),
            ("04_six_separated_vials_in_wooden_rack_closeup", 120.5, 5.5, "C", False, "CELLS AND SERUM", "Fast",
             "Fast: daylight macro view of six glass test tubes in a wooden rack showing dark red blood cells below and clear golden serum above as a glass pipette draws serum from the top layer. Nothing emissive, no face.",
             STYLE + "In crisp daylight, a glass pipette dips gently into the top layer of clear golden serum inside the first of six centrifuged glass tubes standing in a wooden rack." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — The 6-Minute Clot Trap and the 0.2% Pinch of Salt — Midpoint Twist",
        [
            ("01_carrel_1908_artery_suture_and_ottenberg_cross_match", 126.0, 6.5, "A", False, "ARTERY STITCHED TO VEIN", "Quality",
             "Quality: readable faces (French surgeon Alexis Carrel in New York on 8 March 1908 suturing a donor's radial wrist artery to a newborn infant's vein with fine silk thread, while Reuben Ottenberg cross-matches blood slides at Mount Sinai Hospital).",
             STYLE + "New York, 8 March 1908 and 1911: surgeon Alexis Carrel in a white surgical cap carefully threads a fine silk needle to join a father's wrist to his newborn infant's crib, while physician Reuben Ottenberg checks a cross-match slide nearby." + QUAL_TAIL,
             {"kind": "WHO", "label": "Alexis Carrel (1873–1944) — French surgeon and biologist · Reuben Ottenberg (1882–1959) — American physician and haematologist", "when_stamp": "New York, 8 March 1908 · 1911", "hold_s": 3.8}),
            ("02_calcium_fibrin_clot_vs_sodium_citrate_and_1917_icebox_diagram", 132.5, 8.0, "E", False, "CA²⁺ CHELATION · 1917 WWI BLOOD BANK", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked chemical diagram shows calcium ions (Ca²⁺) triggering fibrin clotting in untreated blood within 4–6 minutes on touching glass, versus Luis Agote (9 Nov 1914) and Richard Lewisohn's (23 Jan 1915) 0.2% sodium citrate chelating Ca²⁺ ions to keep blood liquid for 14–26 days in Oswald Hope Robertson's November 1917 Western Front iced ammunition-box blood depot.",
             {"kind": "DATA", "label": "0.2% SODIUM CITRATE CHELATES CA²⁺ → 14–26 DAYS IN 1917 WWI ICEBOX", "detail": "Inked diagram on period paper showing calcium-driven fibrin clotting in untreated blood (4–6 min) vs 0.2% sodium citrate chelating Ca²⁺ ions allowing 14–26 days of cold storage in Robertson's November 1917 Western Front icebox", "scale": "storing Type O blood on ice in 1917 turned transfusion from a two-surgeon emergency operation into a bottle waiting at the front line", "who_card": "Luis Agote (1868–1954) — Argentine physician · Oswald Hope Robertson (1886–1966) — American physician and researcher", "fact_card": "First blood bank in ammo boxes", "when_stamp": "9 November 1914 · 23 January 1915 · Western Front, November 1917", "hold_s": 3.8}),
            ("03_robertson_november_1917_ammo_box_blood_bank_western_front", 140.5, 6.5, "B", False, "THE FIRST BLOOD BANK", "Quality",
             "Quality: readable face (Captain Oswald Hope Robertson on the Western Front in November 1917 lifting a chilled glass bottle of Type O citrated blood packed in ice and sawdust inside a wooden artillery ammunition box).",
             STYLE + "Western Front, France, November 1917: medical officer Oswald Hope Robertson opens a hinged wooden artillery ammunition crate packed with crushed ice and sawdust and lifts out a chilled glass bottle of dark red Type O blood." + QUAL_TAIL,
             None),
            ("04_explorer_0_2_percent_sodium_citrate_spoon_6_min_stopwatch", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside two glass flasks of bright red blood and a ticking brass stopwatch, the Explorer tips a tiny measuring spoon of white sodium citrate crystals into the right flask; as the stopwatch hand hits six minutes, the left flask sets into a solid block while the right flask swirls smooth and liquid." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — The Plus and Minus (Rh) and 118 Million Donations a Year",
        [
            ("01_timeline_1667_1940_and_118_5_million_donations_chart", 152.5, 8.5, "E", False, "118.5 MILLION DONATIONS A YEAR", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 6-date timeline completes: Dec 1667 (Denys ban) · 22 Dec 1818 (Blundell human transfusion) · Feb 1900 & 14 Nov 1901 (Landsteiner ABO groups) · 23 Jan 1915 & Nov 1917 (Lewisohn 0.2% citrate & Robertson WWI blood bank) · 1930 & Jan 1940 (Landsteiner Nobel & Rh +/- factor with Alexander S. Wiener) · Today (118.5M donations/yr), alongside an inked global blood-donation counter (~3.8 bags/second).",
             {"kind": "DATA", "label": "118.5M BLOOD DONATIONS/YEAR (~3.8 BAGS EVERY SECOND WORLDWIDE)", "detail": "Animated 6-date timeline (Dec 1667 → Today) alongside an inked global transfusion chart (118.5 million annual blood donations = ~3.8 donations every second, with O-negative as universal emergency donor)", "scale": "118.5 million blood donations every year — nearly four life-saving bags of blood collected every single second around the globe", "who_card": "Alexander S. Wiener (1907–1976) — American immunohematologist", "fact_card": "118 million donations a year", "when_stamp": "1930 · January 1940 · 1667–1940", "timeline_step": "5/6 · 1930 & Jan 1940 (Landsteiner Nobel & Rh factor with Wiener) & 6/6 · Today (118.5M donations/yr)", "hold_s": 3.8}),
            ("02_rh_plus_minus_slide_and_o_negative_blood_bag_bench", 161.0, 5.5, "A", False, "O-NEGATIVE SAVES LIVES", "Fast",
             "Fast: daylight close-up of an Rh typing glass slide beside a chilled emergency transfusion bag of deep red O-negative blood on a stainless medical tray. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a clean medical tray, a glass typing slide sits beside a chilled emergency transfusion bag of deep ruby-red blood." + FAST_TAIL,
             None),
            ("03_bell_labs_1947_germanium_transistor_and_1958_microchip_handoff", 166.5, 6.5, "C", False, "THE FIRST TRANSISTOR", "Quality",
             "Quality: readable faces (Walter Brattain and John Bardeen at Bell Labs on 16 December 1947 pressing a gold-foil plastic wedge onto a germanium crystal, beside Robert Noyce and Jack Kilby's 1958–1959 silicon integrated circuit — handoff to 029 Transistor).",
             STYLE + "Murray Hill, New Jersey, 16 December 1947: physicists Walter Brattain and John Bardeen lean over a laboratory bench where a triangular plastic wedge wrapped in gold foil presses onto a gleaming germanium crystal beside a silicon microchip wafer." + QUAL_TAIL,
             {"kind": "WHEN", "label": "16 DECEMBER 1947 · 12 SEPTEMBER 1958", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_centrifuge_vials_6x6_slide_citrate_bottle (callback, £0).",
             "Reuse P1:07_table_three_props_centrifuge_vials_6x6_slide_citrate_bottle [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_centrifuge_vials_6x6_slide_citrate_bottle"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_centrifuge_vials_6x6_slide_citrate_bottle",
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
            "film": "028_Landsteiner-Blood-Types",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from landsteiner_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "028_Landsteiner-Blood-Types",
        "version": "v01",
        "date": "2026-10-17",
        "owner": "gemini (J0463)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/028_Landsteiner-Blood-Types/landsteiner_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/028_Landsteiner-Blood-Types/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_Balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028. Nothing in 028 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 028 Blood Types: Why Transfusions Killed Half of All Patients — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 17 Oct 2026, J0463. Built from `landsteiner_script_master_v01.md` (94.4 PASS) and `SOURCES_v01.md`.",
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
        "# 028 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 17 Oct 2026, J0463. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `landsteiner_script_master_v01.md` (94.4 PASS) and `SOURCES_v01.md` so 028's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Karl Landsteiner, Jean-Baptiste Denys, Richard Lewisohn, Leonard Landois, Alexis Carrel, Reuben Ottenberg, Oswald Hope Robertson, Walter Brattain, John Bardeen), candlelit scenes (December 1667 Paris transfusion ban), and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (hand-cranked centrifuge & six vials pan, 3-object callback bench, serum drop curdling red blood cells on slide, James Blundell's brass transfusion syringe, six separated glass tubes in rack, Rh typing slide beside chilled O-negative blood bag). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_landsteiner_1901_6x6_agglutination_matrix_chart` — Karl Landsteiner's 14 November 1901 6 × 6 agglutination matrix across six healthy scientists sorting Groups A, B, and C/O (`SCALE: a single mismatched transfusion can clump and shatter billions of red blood cells inside a patient's veins in minutes`)",
        "  2. `P1:06_6_min_clotting_vs_0_2_percent_sodium_citrate_scale_chart` — 4–6 min untreated clotting in glass vs 2–3 weeks liquid storage with 0.2% sodium citrate (2 g/L) (`SCALE: just two grammes of sodium citrate per litre of blood — less than half a teaspoon — turned a 6-minute surgical emergency into modern blood banks`)",
        "  3. `P2:02_1667_animal_vs_1818_blundell_untyped_vs_1901_abo_chart` — 1667 animal transfusion ban vs Blundell's 1818–1829 un-typed human transfusions (~50% random ABO incompatibility) vs 1901 ABO matching (`SCALE: flipping a coin with a patient's life — before blood typing, nearly half of all human blood transfusions triggered a dangerous or fatal immune reaction`)",
        "  4. `P3:02_abo_surface_antigens_2_million_markers_and_antibodies_diagram` — A, B, AB, and O surface antigens (~2 million sites/cell) and Y-shaped plasma antibodies (`SCALE: each red blood cell carries around 2 million microscopic A or B sugar markers on its skin — if the wrong antibody locks on, millions of cells glue together like Velcro`)",
        "  5. `P4:02_calcium_fibrin_clot_vs_sodium_citrate_and_1917_icebox_diagram` — Ca²⁺ fibrin clotting (4–6 min) vs 0.2% sodium citrate Ca²⁺ chelation enabling Robertson's November 1917 WWI Western Front blood bank (`SCALE: storing Type O blood on ice in 1917 turned transfusion from a two-surgeon emergency operation into a bottle waiting at the front line`)",
        "  6. `P5:01_timeline_1667_1940_and_118_5_million_donations_chart` — completed 6-date timeline (Dec 1667 → Today) + global blood donation counter (118.5 million donations/yr = ~3.8 bags/second) (`SCALE: 118.5 million blood donations every year — nearly four life-saving bags of blood collected every single second around the globe`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_centrifuge_vials_6x6_slide_citrate_bottle`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"028 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
