#!/usr/bin/env python3
"""HOS 026 (The Haber-Bosch Process: How Thin Air Feeds Half the World) pre-VO plate boards v01. J0463. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/026_Haber-Bosch-Nitrogen-Bread/haber_script_master_v01.md
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
        "Part 01 — The Drops That Fed Four Billion People",
        [
            ("01_haber_lerossignol_karlsruhe_ammonia_drip_1909", 0.0, 5.5, "A", False, "BREAD OUT OF THIN AIR", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + Fritz Haber and Robert Le Rossignol in their Karlsruhe laboratory on 2 July 1909 watching a glowing 500°C, 200-atmosphere steel-and-quartz reactor condense clear liquid ammonia drops that morph into golden wheat.",
             STYLE + "In a Karlsruhe laboratory on 2 July 1909, chemist Fritz Haber and engineer Robert Le Rossignol watch a high-pressure steel-and-quartz reactor glowing warmly at 500 degrees Celsius as clear drops of liquid ammonia condense into a glass collector and ripple into golden ears of wheat." + QUAL_TAIL,
             {"kind": "WHEN", "label": "KARLSRUHE · 2 JULY 1909", "timeline_step": "2/6 · 2 Jul 1909 (Haber & Le Rossignol 200 atm tabletop ammonia drip)", "hold_s": 3.5}),
            ("02_haber_ammonia_vs_bosch_burst_steel_and_bread_shell_split", 5.5, 6.0, "B", False, "FAMINE, REACTOR, TRAGEDY", "Quality",
             "Quality: readable faces (Fritz Haber and Robert Le Rossignol collecting ammonia drops in Karlsruhe on the left; Carl Bosch examining a split steel cylinder beside a loaf of bread and an artillery shell in Ludwigshafen on the right).",
             STYLE + "Split period composition: on the left, Fritz Haber and Robert Le Rossignol collect clear liquid ammonia drops from a brass tap; on the right, metallurgist Carl Bosch inspects a burst steel cylinder beside a fresh loaf of wheat bread and a brass artillery shell." + QUAL_TAIL,
             None),
            ("03_crookes_bristol_1898_famine_warning_and_chile_nitrate", 11.5, 6.0, "C", False, "THE 1898 FAMINE WARNING", "Quality",
             "Quality: readable face (Sir William Crookes with white beard and spectacles addressing the September 1898 British Association in Bristol beside a globe showing the Chilean Atacama Desert and a triple-linked nitrogen model).",
             STYLE + "Bristol, September 1898: bearded chemist Sir William Crookes stands at a mahogany lecture podium holding a sheaf of wheat beside a globe turned to South America and a brass model of two nitrogen spheres locked by three rods." + QUAL_TAIL,
             {"kind": "WHO", "label": "William Crookes (1832–1919) — English chemist and physicist", "when_stamp": "Bristol, September 1898", "timeline_step": "1/6 · Sep 1898 (Crookes warns of global nitrogen famine)", "hold_s": 3.8}),
            ("04_n2_3h2_2nh3_200atm_500c_and_half_humanity_chart", 17.5, 8.0, "E", False, "200 ATM · 500°C → 50% OF HUMANITY FED", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked reaction and global food chart shows atmospheric N₂ (78% of air, 945 kJ/mol triple bond) + 3 H₂ compressed at 200 atmospheres and 500°C over an osmium/iron catalyst into liquid ammonia (2 NH₃), feeding ~50% of humanity (~4 billion people alive today).",
             {"kind": "DATA", "label": "N₂ + 3H₂ → 2NH₃ (200 ATM, 500°C) · FEEDS ~4 BILLION PEOPLE", "detail": "Inked reaction and population chart on period paper showing N₂ + 3H₂ → 2NH₃ at 200 atmospheres and 500°C and the share of humanity fed by synthetic Haber-Bosch nitrogen fertilizer (~50% of global food protein = ~4 billion people alive today)", "scale": "half of all the nitrogen atoms inside your muscles and DNA right now came out of a high-pressure Haber-Bosch tube", "who_card": "Fritz Haber (1868–1934) — German physical chemist · Robert Le Rossignol (1884–1976) — British chemical engineer · Carl Bosch (1874–1940) — German industrial chemist", "when_stamp": "2 July 1909 · September 1913", "hold_s": 3.8}),
            ("05_conical_high_pressure_valve_and_copper_coils_pan", 25.5, 5.5, "A", False, "HIGH-PRESSURE VALVE", "Fast",
             "Fast: daylight pan across Le Rossignol's precision-machined conical steel high-pressure valve, copper recirculation coils, and a brass manometer dial on a wooden workbench between code graphics so two full-frame graphics never run back to back. Nothing emissive.",
             STYLE + "In soft daylight on a laboratory bench, the camera tracks across a precision-machined conical steel high-pressure valve, coiled copper recirculation tubing, and a heavy brass pressure gauge." + FAST_TAIL,
             None),
            ("06_1atm_air_vs_200atm_2km_ocean_pressure_scale_chart", 31.0, 8.0, "E", False, "200 ATMOSPHERES OF PRESSURE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked pressure comparison contrasts normal sea-level air (1 atmosphere) and a car tyre (2 atmospheres) against Haber and Le Rossignol's 200-atmosphere tabletop reactor at 500°C — equivalent to the crushing weight of 2,000 metres (2 kilometres) of ocean water.",
             {"kind": "DATA", "label": "1 ATM AIR VS 200 ATM REACTOR (= 2 KM OCEAN DEPTH)", "detail": "Inked pressure scale comparing 1 atmosphere (sea-level air) vs 200 atmospheres inside Haber and Bosch's 500°C ammonia reactor (equivalent to 2,000 m ocean depth)", "scale": "200 atmospheres of pressure at 500 degrees Celsius — like squeezing red-hot gas under the weight of two kilometres of ocean water", "hold_s": 3.8}),
            ("07_table_three_props_ammonia_flask_bosch_hole_ring_wheat_sheaf", 39.0, 5.5, "C", False, "KARLSRUHE, JULY 1909", "Fast",
             "Fast: daylight prop table (callback source for Part 05: glass receiver flask of clear liquid ammonia, cross-section ring of double-walled steel drilled with Bosch holes, golden wheat sheaf). Nothing emissive.",
             STYLE + "On a wooden workbench in soft window light sit three objects side by side: a thick glass flask holding clear liquid ammonia, a machined steel cylinder ring drilled with tiny radial vent holes, and a tied sheaf of golden wheat." + FAST_TAIL,
             None),
            ("08_explorer_pulling_triple_linked_nitrogen_rings", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing on the wooden bench beside the glass ammonia collector, the Explorer tugs with both hands on two brass spheres joined by three heavy rods, fails to pull them apart until a brass pressure gauge needle swings high, and cheers as clear drops drip into the flask." + EXP_TAIL,
             None),
            ("09_basf_steel_test_cylinder_splitting_open", 67.5, 5.5, "B", False, "STEEL WALLS BURST", "Fast",
             "Fast: daylight close-up of a thick carbon-steel test pipe inside a brick test bay blistering and splitting open along a jagged crack with a puff of white vapour. Nothing emissive, no face.",
             STYLE + "In crisp daylight inside a brick-lined test bay, a thick-walled grey steel pipe groans, blisters along its flank, and splits open with a sudden hiss of white vapour." + FAST_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — The Triple-Bond Lock and the Tabletop Drip",
        [
            ("01_atacama_saltpetre_diggings_and_crookes_wheat_warning", 73.0, 6.5, "A", False, "CHILEAN SALTPETRE · 1898", "Quality",
             "Quality: readable face (Sir William Crookes holding a lump of white Chilean sodium nitrate crust while workers shovel caliche ore in the sunlit Atacama Desert).",
             STYLE + "Split period view: in the Chilean Atacama Desert, workers shovel white sodium nitrate crust into wooden carts; in Bristol in September 1898, Sir William Crookes holds up a white crystal lump beside a sheaf of wheat." + QUAL_TAIL,
             {"kind": "FACT", "label": "78% of air, yet unusable", "when_stamp": "September 1898", "hold_s": 3.8}),
            ("02_nitrogen_945kj_triple_bond_and_200atm_yield_chart", 79.5, 8.0, "E", False, "945 KJ/MOL N≡N · 200 ATM YIELD", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked bond-energy and equilibrium chart compares the N≡N triple covalent bond (945 kJ/mol, nearly 3× a C–C single bond at 348 kJ/mol) and plots ammonia equilibrium yield at 500°C rising from ~0.13% at 1 atm to ~15–20% per pass at 200 atm as 4 gas molecules (N₂ + 3H₂) compress into 2 NH₃.",
             {"kind": "DATA", "label": "N≡N 945 KJ/MOL (3× C–C) · YIELD 0.13% (1 ATM) → ~18% (200 ATM)", "detail": "Inked bond-energy & equilibrium chart on period paper comparing the N≡N triple bond (945 kJ/mol vs 348 kJ/mol C–C single bond) and ammonia yield at 500°C jumping from ~0.13% at 1 atm to ~15–20% per pass at 200 atm", "scale": "945 kilojoules per mole — a molecular lock nearly three times stronger than the carbon bonds holding wood or diamond together", "hold_s": 3.8}),
            ("03_nernst_1907_dispute_and_mittasch_2_july_1909_karlsruhe", 87.5, 6.5, "B", False, "80 MILLILITRES AN HOUR", "Quality",
             "Quality: readable faces (Walther Nernst in pince-nez challenging Fritz Haber in 1907, then Haber and Robert Le Rossignol demonstrating their 200-atmosphere osmium reactor to BASF chemist Alwin Mittasch on 2 July 1909 as ammonia drips at 80 mL/h).",
             STYLE + "Karlsruhe, 2 July 1909: Fritz Haber and young engineer Robert Le Rossignol open a precision brass tap on their high-pressure apparatus while visiting chemist Alwin Mittasch leans in to watch clear liquid ammonia drip steadily into a graduated glass tube." + QUAL_TAIL,
             {"kind": "WHO", "label": "Walther Nernst (1864–1941) — Berlin physical chemistry professor · Alwin Mittasch (1869–1953) — BASF catalytic chemist", "when_stamp": "1907 · 2 July 1909", "hold_s": 3.8}),
            ("04_scarce_osmium_powder_vial_and_recirculation_pump", 94.0, 5.5, "C", False, "SCARCE OSMIUM CATALYST", "Fast",
             "Fast: daylight macro shot of a tiny glass vial of dark grey osmium powder on a brass balance scale beside a steel recirculation pump cylinder. Nothing emissive, no face.",
             STYLE + "In crisp daylight, brass forceps place a tiny glass vial of dark grey osmium powder onto a precision balance scale beside a heavy steel recirculation pump." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 20,000 Catalyst Trials and the 'Bosch Holes'",
        [
            ("01_bosch_and_mittasch_20000_catalyst_ovens_ludwigshafen", 99.5, 6.5, "A", False, "20,000 CATALYST RUNS", "Quality",
             "Quality: readable faces (thirty-five-year-old Carl Bosch and Alwin Mittasch at BASF in Ludwigshafen in 1909–1910 testing rows of miniature high-pressure catalyst cylinders with Swedish magnetite iron ore).",
             STYLE + "Ludwigshafen, 1909–1910: metallurgist Carl Bosch and chemist Alwin Mittasch walk down a long bench of miniature high-pressure steel test ovens, inspecting dark chunks of Swedish magnetite iron ore in porcelain dishes." + QUAL_TAIL,
             {"kind": "FACT", "label": "20,000 catalyst tests", "when_stamp": "Ludwigshafen, 1909–1910", "hold_s": 3.8}),
            ("02_bosch_double_walled_liner_and_bosch_holes_diagram", 106.0, 8.0, "E", False, "SOFT-IRON LINER + BOSCH HOLES", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked metallurgical cross-section shows 200-atmosphere H₂ at 500°C diffusing into carbon steel to form explosive methane (CH₄) blisters, alongside Carl Bosch's double-walled solution: a thin carbon-free soft-iron inner liner inside a thick carbon-steel outer shell drilled with 'Bosch holes' that vent diffusing H₂ harmlessly.",
             {"kind": "DATA", "label": "200 ATM H₂ → SOFT-IRON LINER + PERFORATED STEEL 'BOSCH HOLES'", "detail": "Inked cross-section diagram on period paper of Carl Bosch's double-walled reactor: 200 atm / 500°C N₂ + H₂ core → thin carbon-free soft-iron inner liner → perforated strong carbon-steel outer shell drilled with 'Bosch holes' venting diffusing H₂ safely", "scale": "hydrogen atoms are so small they slip straight between the iron atoms of solid red-hot cannon steel and rot it from within — until Bosch drilled tiny escape holes in the outer armour", "hold_s": 3.8}),
            ("03_oppau_ammonia_plant_towers_9_september_1913", 114.0, 6.5, "B", False, "THE BOSCH HOLES", "Quality",
             "Quality: readable face (Carl Bosch standing before the towering 8-metre double-walled ammonia converter vessels at Oppau on 9 September 1913).",
             STYLE + "Oppau, Germany, 9 September 1913: Carl Bosch stands on an iron catwalk beside towering eight-metre double-walled steel ammonia converter columns studded with tiny vent holes inside a cavernous brick factory hall." + QUAL_TAIL,
             {"kind": "WHEN", "label": "OPPAU · 9 SEPTEMBER 1913 · 1918 · 1931", "timeline_step": "3/6 · 9 Sep 1913 (Bosch opens Oppau plant with iron catalyst & Bosch holes) & 5/6 · 1931 (Bosch Nobel)", "hold_s": 3.8}),
            ("04_drilled_steel_reactor_wall_section_closeup", 120.5, 5.5, "C", False, "HYDROGEN ESCAPE HOLES", "Fast",
             "Fast: daylight macro view of a thick cut section of a double-walled steel converter showing the thin inner soft-iron sleeve and the outer forged steel wall perforated with neat radial Bosch holes. Nothing emissive, no face.",
             STYLE + "In crisp daylight, the camera pans closely across a cutaway section of a massive double-walled steel cylinder, showing the thin inner soft-iron liner and the thick outer wall drilled with neat radial peepholes." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — Bread and Explosives — Midpoint Twist",
        [
            ("01_1914_blockade_munitions_and_haber_ypres_april_1915", 126.0, 6.5, "A", False, "FERTILIZER INTO EXPLOSIVES", "Quality",
             "Quality: readable face (Royal Navy blockade of Chilean nitrate ships in August 1914 while BASF ammonia towers feed nitric-acid munitions plants and Fritz Haber supervises gas cylinders in April 1915).",
             STYLE + "Split period scene: on the left, steel ammonia towers pipe gas into nitric-acid absorption columns; on the right, Fritz Haber in a dark greatcoat inspects rows of grey steel cylinders in April 1915." + QUAL_TAIL,
             {"kind": "WHEN", "label": "AUGUST 1914 · YPRES, 22 APRIL 1915", "timeline_step": "4/6 · 1914–1918 (WWI munitions & Clara Immerwahr's 1915 protest; Haber 1918 Nobel)", "hold_s": 3.8}),
            ("02_clara_immerwahr_breslau_1900_and_berlin_1915_confrontation", 132.5, 6.5, "B", False, "CLARA IMMERWAHR'S PROTEST", "Quality",
             "Quality: readable face (chemist Dr Clara Immerwahr receiving the first female doctorate at the University of Breslau in December 1900, then confronting Fritz Haber in Berlin in April–May 1915).",
             STYLE + "Breslau, December 1900 and Berlin, May 1915: chemist Dr Clara Immerwahr in a high-collared dark dress holds her doctoral scroll in a university hall, then stands gravely in a quiet Berlin study confronting Fritz Haber." + QUAL_TAIL,
             {"kind": "WHO", "label": "Clara Immerwahr (1870–1915) — German chemist", "fact_card": "First female PhD at Breslau", "when_stamp": "December 1900 · 2 May 1915", "hold_s": 3.8}),
            ("03_haber_1933_resignation_and_basel_exile_1934", 139.0, 6.5, "C", False, "EXILE IN 1933", "Quality",
             "Quality: readable face (an ageing Fritz Haber packing his leather briefcase at the Kaiser Wilhelm Institute in Berlin after resigning in April 1933, before his death in Basel on 29 January 1934).",
             STYLE + "Berlin, April 1933: an ageing Fritz Haber in a dark suit quietly closes his leather briefcase beside his laboratory desk and walks out through the stone doorway into the rain." + QUAL_TAIL,
             {"kind": "WHEN", "label": "APRIL 1933 · BASEL, 29 JANUARY 1934", "hold_s": 3.5}),
            ("04_explorer_balance_scale_wheat_sheaf_vs_artillery_shell", 145.5, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside a brass balance scale holding a golden sheaf of wheat on the left pan and a brass artillery shell on the right pan, the Explorer pours white nitrogen salt crystals from a glass flask into both pans, watching the beam tip solemnly between life and destruction." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Half the Nitrogen in Your Body and Nature's Secret",
        [
            ("01_timeline_1898_2008_and_global_nitrogen_energy_chart", 151.0, 8.5, "E", False, "1–2% WORLD ENERGY → 50% OF HUMANITY", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 6-date timeline completes: Sep 1898 (Crookes warning) · 2 Jul 1909 (Haber & Le Rossignol 200 atm drip) · 9 Sep 1913 (Bosch Oppau plant) · 1914–1918 (WWI munitions, Clara Immerwahr 1915, Haber 1918 Nobel) · 1931 (Bosch Nobel) · 2008–Today (~50% of humanity / ~4 billion people fed), alongside an inked global nitrogen balance chart (~1–2% of world energy → 150–180M tonnes NH₃/yr → 50% of human body nitrogen).",
             {"kind": "DATA", "label": "1–2% WORLD ENERGY → 150M+ TONNES NH₃/YR → FEEDS ~4B PEOPLE", "detail": "Animated 6-date timeline (Sep 1898 → 2008–Today) alongside an inked global nitrogen balance chart showing ~1–2% of world energy producing ~150–180 million tonnes of ammonia/year, feeding ~50% of humanity (~4 billion people)", "scale": "1 to 2 percent of all the energy humanity uses on Earth goes into one single chemical reaction — putting half the nitrogen atoms into your body", "fact_card": "Uses 1–2% of world energy", "when_stamp": "2008 · 1898–2008", "timeline_step": "6/6 · 2008–Today (~50% of humanity / ~4 billion people fed by Haber-Bosch)", "hold_s": 3.8}),
            ("02_clover_root_nodule_iron_nitrogenase_vs_bosch_catalyst", 159.5, 5.5, "A", False, "IRON IN SOIL AND STEEL", "Fast",
             "Fast: daylight macro view of a green clover plant with pink-tan root nodules beside a porcelain dish of dark magnetite iron catalyst granules on a wooden bench between code graphics. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden table, a fresh green clover plant with tiny root nodules sits beside a porcelain dish of dark grey magnetite iron catalyst granules." + FAST_TAIL,
             None),
            ("03_iron_molybdenum_nitrogenase_20c_vs_500c_comparison_chart", 165.0, 5.0, "E", False, "20°C ROOT IRON VS 500°C REACTOR IRON", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked comparison shows soil rhizobia nitrogenase breaking N≡N at 1 atm and 20°C using an iron-molybdenum (FeMo) cofactor cluster beside Bosch and Mittasch's promoted iron (Fe₃O₄) catalyst at 200 atm and 500°C.",
             {"kind": "DATA", "label": "SOIL FE-MO ENZYME (1 ATM, 20°C) VS BOSCH IRON CATALYST (200 ATM, 500°C)", "detail": "Inked comparison on period paper contrasting soil bacteria FeMo nitrogenase (1 atm, 20°C) with Bosch & Mittasch's promoted magnetite iron catalyst (200 atm, 500°C)", "scale": "both human factories at 500 degrees and humble clover roots at room temperature use the exact same metal — iron — to unlock nitrogen from the air", "hold_s": 3.6}),
            ("04_lovelace_1843_punched_cards_and_turing_1940_bombe_handoff", 170.0, 5.5, "C", False, "INVENTING THE COMPUTER", "Quality",
             "Quality: readable faces (Ada Lovelace in August 1843 tracing a punched card for Babbage's brass Analytical Engine, dissolving into Alan Turing in March 1940 beside the spinning bronze drums of the Bletchley Park Bombe — handoff to 027 Lovelace/Turing).",
             STYLE + "London, August 1843 and Bletchley Park, March 1940: Ada Lovelace traces a perforated pasteboard card beside brass Analytical Engine gears, dissolving into Alan Turing watching rows of spinning bronze Bombe drums." + QUAL_TAIL,
             {"kind": "WHEN", "label": "AUGUST 1843 · 18 MARCH 1940", "hold_s": 3.5}),
            ("05_table_three_callback", 175.5, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_ammonia_flask_bosch_hole_ring_wheat_sheaf (callback, £0).",
             "Reuse P1:07_table_three_props_ammonia_flask_bosch_hole_ring_wheat_sheaf [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_ammonia_flask_bosch_hole_ring_wheat_sheaf"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_ammonia_flask_bosch_hole_ring_wheat_sheaf",
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
            "film": "026_Haber-Bosch-Nitrogen-Bread",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from haber_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "026_Haber-Bosch-Nitrogen-Bread",
        "version": "v01",
        "date": "2026-10-17",
        "owner": "gemini (J0463)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/026_Haber-Bosch-Nitrogen-Bread/haber_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/026_Haber-Bosch-Nitrogen-Bread/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_Balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026. Nothing in 026 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 026 The Haber-Bosch Process: How Thin Air Feeds Half the World — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 17 Oct 2026, J0463. Built from `haber_script_master_v01.md` (92.6 PASS) and `SOURCES_v01.md`.",
        "**No mint, no spend.** Pre-VO clock timings (`177.9 s` base picture grid; re-times automatically onto Scribe word timestamps once long VO locks).",
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
        "# 026 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 17 Oct 2026, J0463. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `haber_script_master_v01.md` (92.6 PASS) and `SOURCES_v01.md` so 026's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
        "",
        "## Totals (base 26-row board before VO continuation splits)",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Fritz Haber, Robert Le Rossignol, Carl Bosch, Sir William Crookes, Walther Nernst, Alwin Mittasch, Dr Clara Immerwahr, Ada Lovelace, Alan Turing), emissive/high-temperature reactor scenes (2 July 1909 500°C/200 atm Karlsruhe ammonia synthesis answer image), and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and apparatus shots (Le Rossignol conical valve & copper coils pan, 3-object callback bench, splitting carbon-steel pipe in brick test bay, scarce osmium powder vial on balance scale, cutaway double-walled steel ring with Bosch holes, clover root nodules beside magnetite iron catalyst). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_n2_3h2_2nh3_200atm_500c_and_half_humanity_chart` — N₂ + 3H₂ → 2NH₃ reaction at 200 atm & 500°C and ~50% of humanity (~4 billion people) fed (`SCALE: half of all the nitrogen atoms inside your muscles and DNA right now came out of a high-pressure Haber-Bosch tube`)",
        "  2. `P1:06_1atm_air_vs_200atm_2km_ocean_pressure_scale_chart` — 1 atm sea-level air vs 200 atm reactor pressure (= 2,000 m ocean depth) (`SCALE: 200 atmospheres of pressure at 500 degrees Celsius — like squeezing red-hot gas under the weight of two kilometres of ocean water`)",
        "  3. `P2:02_nitrogen_945kj_triple_bond_and_200atm_yield_chart` — N≡N triple bond (945 kJ/mol vs 348 kJ/mol C–C) and 500°C equilibrium yield rising from ~0.13% at 1 atm to ~15–20% at 200 atm (`SCALE: 945 kilojoules per mole — a molecular lock nearly three times stronger than the carbon bonds holding wood or diamond together`)",
        "  4. `P3:02_bosch_double_walled_liner_and_bosch_holes_diagram` — Carl Bosch's double-walled soft-iron inner liner + perforated carbon-steel outer shell ('Bosch holes') preventing methane hydrogen embrittlement (`SCALE: hydrogen atoms are so small they slip straight between the iron atoms of solid red-hot cannon steel and rot it from within — until Bosch drilled tiny escape holes in the outer armour`)",
        "  5. `P5:01_timeline_1898_2008_and_global_nitrogen_energy_chart` — completed 6-date timeline (Sep 1898 → 2008–Today) + global nitrogen balance (~1–2% of world energy → 150–180M tonnes NH₃/yr → ~4B people fed) (`SCALE: 1 to 2 percent of all the energy humanity uses on Earth goes into one single chemical reaction — putting half the nitrogen atoms into your body`)",
        "  6. `P5:03_iron_molybdenum_nitrogenase_20c_vs_500c_comparison_chart` — soil rhizobia FeMo nitrogenase enzyme (1 atm, 20°C) vs Bosch & Mittasch's promoted iron catalyst (200 atm, 500°C) (`SCALE: both human factories at 500 degrees and humble clover roots at room temperature use the exact same metal — iron — to unlock nitrogen from the air`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:05_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_ammonia_flask_bosch_hole_ring_wheat_sheaf`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"026 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
