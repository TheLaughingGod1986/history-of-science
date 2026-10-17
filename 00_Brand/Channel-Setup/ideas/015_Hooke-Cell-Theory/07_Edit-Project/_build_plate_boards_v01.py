#!/usr/bin/env python3
"""HOS 015 (Cells: The Slice of Cork That Changed Biology) pre-VO plate boards v01. J0397. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/015_Hooke-Cell-Theory/hooke_script_master_v01.md
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
        "Part 01 — The Billion Tiny Rooms",
        [
            ("01_cork_shaving_microscope_open", 0.0, 5.5, "A", False, "ONE BILLION ROOMS", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + oil lamp & water-globe glow on microscope.",
             STYLE + "London, January 1665: in a warm candlelit workshop, a sharp steel penknife shaves a translucent wafer of pale bark from a bottle cork and slides it beneath a tilted red-leather and brass microscope lit by a glowing glass water-globe." + QUAL_TAIL,
             {"kind": "WHEN", "label": "LONDON · JANUARY 1665", "hold_s": 3.5}),
            ("02_micrographia_cork_scan", 5.5, 6.0, "A", False, "HOW CELLS DIVIDE", "archive",
             "Flow-first: real public-domain archive scan avoids Veo lettering risk (£0 / 0 cr).",
             "Public-domain archive scan: Robert Hooke, Micrographia (London, 1665), Schem. XI Fig. 1 (copperplate engraving of microscopic cork cells, Royal Society / Wellcome Collection, Public Domain).",
             None),
            ("03_oak_bark_hand_glass", 11.5, 6.0, "B", False, "SOLID FLESH?", "Fast",
             "Fast: daylight workbench prop shot of oak bark and simple hand lens. Nothing emissive, no face.",
             STYLE + "On an oak workbench in grey window light, a rough piece of cork oak bark rests beside an anatomical sketch of muscle fibres and a simple brass hand magnifying glass." + FAST_TAIL,
             {"kind": "WHEN", "label": "1660s", "hold_s": 3.5}),
            ("04_cubic_inch_cork_1_25_billion", 17.5, 8.0, "E", False, "1.25 BILLION CELLS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked cubic-inch cork diagram counts 1,080 pores along one edge and multiplies to 1,259,712,000 cells beside a sugar lump scale comparison.",
             {"kind": "DATA", "label": "1.25 BILLION IN A CUBIC INCH", "detail": "Inked cubic-inch cork diagram showing 1,080 pores per inch and 1,259,712,000 cells per cubic inch", "scale": "1.25 billion cells in a cube the size of a sugar lump", "who_card": "Robert Hooke (1635–1703) — Royal Society curator", "when_stamp": "January 1665", "hold_s": 3.8}),
            ("05_honeycomb_cork_macro_pan", 25.5, 5.5, "A", False, "TINY MONKS' ROOMS", "Fast",
             "Fast: matte microscopic view of cork honeycomb walls between code graphics so two full-frame graphics never run back to back.",
             STYLE + "Through a circular brass microscope eyepiece in even light, hundreds of neat rectangular pale-gold cork chambers fill the field like a honeycomb." + FAST_TAIL,
             None),
            ("06_30_trillion_human_cells_scale", 31.0, 8.0, "E", False, "30 TRILLION CELLS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked scale comparison contrasts 1.25 billion cork cells in a cubic inch with 30 trillion living cells in an adult human body as one cell cleaves into 2, 4, and 8.",
             {"kind": "DATA", "label": "30 TRILLION CELLS IN YOU", "detail": "Inked comparison of 1,259,712,000 cork cells per cubic inch vs ~30 trillion human cells", "scale": "30 trillion cells in you — 3,700 times the number of people on Earth", "hold_s": 3.8}),
            ("07_table_three_props", 39.0, 5.5, "B", False, "PENKNIFE · CORK · MICROSCOPE", "Fast",
             "Fast: daylight prop table (callback source for Part 05). Nothing emissive.",
             STYLE + "On a wooden workbench in grey window light sit three objects side by side: a steel penknife, a pale bottle cork, and a tilted red-leather and brass compound microscope." + FAST_TAIL,
             None),
            ("08_explorer_hooke_microscope", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside Hooke's workbench, the Explorer peers through the brass eyepiece of the tilted red-leather microscope, glances at the tiny cork shaving on the needle stage, and steps back in wonder." + EXP_TAIL,
             None),
            ("09_empty_portrait_frame_candle", 67.5, 5.5, "C", False, "NO SURVIVING PORTRAIT", "Quality",
             "Quality: candle flame flickering out before empty gilt frame (never Fast).",
             STYLE + "On a dark wood-panelled wall at the Royal Society, a heavy gilt portrait frame hangs empty in shadow as a single candle flame below it flickers out." + QUAL_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — The Book That Kept London Awake",
        [
            ("01_pepys_reads_until_2am_1665", 73.0, 6.5, "C", False, "PEPYS READ UNTIL 2 A.M.", "Quality",
             "Quality: readable face (Samuel Pepys in bed by candlelight).",
             STYLE + "London, 21 January 1665: naval administrator Samuel Pepys, early thirties in a velvet indoor coat, sits up in bed by warm candlelight turning a large copperplate engraving of a flea while a mantel clock points to two o'clock." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Samuel Pepys", "line_2": "(1633–1703) — Royal Navy administrator", "fact_card": "Pepys read until 2 a.m.", "when_stamp": "London · 21 January 1665", "hold_s": 3.8}),
            ("02_hooke_boyle_gresham_1662", 79.5, 6.5, "A", False, "CURATOR OF EXPERIMENTS", "Quality",
             "Quality: readable faces (young Robert Hooke and Robert Boyle at Gresham College, 1662).",
             STYLE + "Gresham College, London, 1662: young Robert Hooke, late twenties with shoulder-length brown hair and a slight stoop in a plain wool coat, adjusts a brass air pump and microscope before Robert Boyle and fellows of the Royal Society." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Robert Boyle", "line_2": "(1627–1691) — natural philosopher", "when_stamp": "London · 1662", "hold_s": 3.8}),
            ("03_hooke_brine_globe_optics_diagram", 86.0, 8.0, "E", False, "MAGNIFIED 50 TIMES", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked optical diagram traces light from Hooke's oil lamp through a round brine-filled glass condenser globe and convex lens onto the cork specimen for 50x magnification.",
             {"kind": "DATA", "label": "50× MAGNIFICATION", "detail": "Inked optical diagram of Hooke's oil-lamp and brine-globe condenser focusing light for ~30x–50x magnification", "scale": "magnified 50 times — making a flea look as long as a cat", "hold_s": 3.8}),
            ("04_cork_cross_and_lengthwise_walls", 94.0, 5.5, "A", False, "EMPTY WALLS", "Fast",
             "Fast: daylight/matte view of crosswise and lengthwise cork slices on brass pin. Nothing emissive.",
             STYLE + "Close macro view in clear light of a pale cork wafer mounted on a brass needle stage, showing rows of empty rectangular cell walls with no living fluid inside." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — The Missing Portrait and the Dinner Table",
        [
            ("01_hooke_vs_newton_feud_1703", 99.5, 6.5, "C", False, "A THIRTY-YEAR FEUD", "Quality",
             "Quality: readable faces (Robert Hooke and Royal Society president Isaac Newton, 1703).",
             STYLE + "London, November 1703: Isaac Newton, sixties with long white hair in a dark velvet coat, presides in the carved wooden chair of the Royal Society under chandelier light." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Isaac Newton", "line_2": "(1642–1727) — Royal Society president", "when_stamp": "3 March & 30 November 1703", "timeline_step": "2/6 · 1703 (Hooke dies; Newton becomes President)", "hold_s": 3.8}),
            ("02_gresham_move_portrait_1710", 106.0, 6.0, "C", False, "PORTRAIT VANISHED · 1710", "Fast",
             "Fast: grey daylight hall with wooden crates and an empty hook on oak panelling. No face, nothing emissive.",
             STYLE + "London, 1710: in a high-windowed stone hall at Gresham College in grey daylight, packed wooden instrument crates sit on the floor beneath an empty brass picture hook on the oak wall." + FAST_TAIL,
             {"kind": "FACT", "label": "PORTRAIT VANISHED AROUND 1710", "when_stamp": "London · 1710", "hold_s": 3.8}),
            ("03_lister_lens_and_brown_nucleus_1831", 112.0, 6.5, "D", False, "THE NUCLEUS · 1831", "Quality",
             "Quality: readable faces (Joseph Jackson Lister and Scottish botanist Robert Brown, 1830–1831).",
             STYLE + "London, 1831: Scottish botanist Robert Brown peers through a brass achromatic microscope at a green orchid leaf while beside him Joseph Jackson Lister holds a pair of precision-ground crown and flint glass lenses." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Robert Brown & Joseph Jackson Lister", "line_2": "Brown (1773–1858) · Lister (1786–1869)", "when_stamp": "London · 1830–1831", "timeline_step": "3/6 · 1831 (Brown names the 'nucleus')", "hold_s": 3.8}),
            ("04_schleiden_schwann_berlin_dinner_1838", 118.5, 6.5, "D", False, "PLANTS AND ANIMALS · 1838", "Quality",
             "Quality: readable faces + candlelit Berlin dinner table (Matthias Schleiden and Theodor Schwann).",
             STYLE + "Berlin, October 1838: over porcelain coffee cups at a warm candlelit dining table, botanist Matthias Schleiden sketches a plant cell with a dark nucleus on a slip of paper as physiologist Theodor Schwann leans in with wide eyes." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Matthias Schleiden & Theodor Schwann", "line_2": "Schleiden (1804–1881) · Schwann (1810–1882)", "when_stamp": "Berlin · October 1838 & 1839", "timeline_step": "4/6 · 1838–1839 (Plant & animal cell theory)", "hold_s": 3.8}),
        ],
    ),
    (
        4,
        "Part 04 — The Sugar-Crystal Mistake and the Attic Lab",
        [
            ("01_crystal_mistake_vs_binary_division", 125.0, 8.0, "E", False, "CRYSTALS OR DIVISION?", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, a two-panel inked diagram contrasts Schleiden and Schwann's false crystal-in-fluid model on the left with Robert Remak's binary frog-egg cleavage (1 -> 2 -> 4 -> 8 -> 16) on the right.",
             {"kind": "DATA", "label": "1 → 2 → 4 → 8 → 16", "detail": "Two-panel inked explainer: false crystal model vs Remak's binary cell division (1 -> 2 -> 4 -> 8 -> 16)", "scale": "one cell doubling 45 times — enough to build all 30 trillion cells in an adult human", "hold_s": 3.8}),
            ("02_remak_charite_attic_lab_1852", 133.0, 6.5, "D", False, "ROBERT REMAK · 1852", "Quality",
             "Quality: readable face (embryologist Robert Remak in his Berlin attic laboratory).",
             STYLE + "Charité Hospital, Berlin, 1852: in a cramped low-beamed attic laboratory lit by a dormer window, bearded embryologist Robert Remak in a dark frock coat drips solution onto frog eggs in a glass dish beneath his brass microscope." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Robert Remak", "line_2": "(1815–1865) — Berlin embryologist", "fact_card": "Barred from a professorship", "when_stamp": "Berlin · 1841–1852", "timeline_step": "5/6 · 1852 (Remak proves cell division)", "hold_s": 3.8}),
            ("03_explorer_frog_egg_cleavage", 139.5, 5.5, "D", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "In the corner of Remak's Berlin attic laboratory, the Explorer watches a single dark frog egg in a glass watch-dish pinch cleanly down the middle into two cells, holds up two gloved fingers to match, and beams." + EXP_TAIL,
             None),
            ("04_virchow_omnis_cellula_1855", 145.0, 6.5, "D", False, "OMNIS CELLULA E CELLULA", "Quality",
             "Quality: readable face (pathologist Rudolf Virchow writing at his desk in April 1855).",
             STYLE + "April 1855: pathologist Rudolf Virchow, mid-thirties in wire spectacles and dark coat, writes with a steel dip pen at a stack-lined medical desk while Robert Remak's 1852 paper lies open beside him." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Rudolf Virchow", "line_2": "(1821–1902) — German pathologist", "fact_card": "Left Remak's name out", "when_stamp": "April 1855 & 1858", "hold_s": 3.8}),
        ],
    ),
    (
        5,
        "Part 05 — The Unbroken Chain",
        [
            ("01_cell_lifespan_comparison_chart", 151.5, 8.0, "E", False, "EVERY SEVEN YEARS?", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked three-bar lifespan chart compares human gut lining cells (3–5 days), red blood cells (120 days), and cerebral cortex neurons (your whole life).",
             {"kind": "DATA", "label": "DAYS vs YOUR WHOLE LIFE", "detail": "Inked cell-lifespan chart: gut lining (3–5 days), red blood cells (120 days), brain neurons (lifetime)", "scale": "3 to 5 days for gut cells vs a lifetime for brain neurons", "hold_s": 3.8}),
            ("02_red_blood_cells_and_neurons_plate", 159.5, 5.5, "B", False, "BUILT TO LAST", "Fast",
             "Fast: matte microscopic view of red blood corpuscles on a glass slide between code graphics so two full-frame graphics never run back to back.",
             STYLE + "On a sunlit brass microscope stage, a glass slide holds a drop of crimson blood beside an inked anatomical drawing of a branching nerve cell." + FAST_TAIL,
             None),
            ("03_timeline_1665_to_1855_complete", 165.0, 8.5, "E", False, "190 YEARS · 1665 → 1855", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 6-date timeline completes: 1665 (Hooke's cork) · 1703 (Hooke's death) · 1831 (Brown's nucleus) · 1838–1839 (Schleiden & Schwann) · 1852 (Remak's division) · 1855 (Omnis cellula e cellula).",
             {"kind": "DATA", "label": "190 YEARS · 1665 → 1855", "detail": "Completed 6-date timeline from Hooke's Micrographia (1665) to Omnis cellula e cellula (1855)", "scale": "190 years from Hooke's cork slice (1665) to Omnis cellula e cellula (1855)", "when_stamp": "1665–1855", "hold_s": 3.8}),
            ("04_dividing_nucleus_mendel_handoff", 173.5, 6.0, "B", False, "INSIDE THE NUCLEUS", "Fast",
             "Fast: daylight microscope bench with dividing-cell sketch and garden pea notebook. Nothing emissive.",
             STYLE + "In daylight on a wooden workbench, a brass microscope sits beside a botanical notebook of garden pea pods and a glass dish showing a dividing cell nucleus." + FAST_TAIL,
             None),
            ("05_table_three_callback", 179.5, 2.4, "B", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props (callback, £0).",
             "Reuse P1:07_table_three_props [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
            "archive": 0,
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
                row["reuse_of"] = "P1:07_table_three_props"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props",
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
            "film": "015_Hooke-Cell-Theory",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from hooke_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "archive": sum(p["archive"] for p in per_part_summary),
        "reuse": sum(p["reuse"] for p in per_part_summary),
        "flow_credits_try1": sum(p["flow_credits_try1"] for p in per_part_summary),
        "flow_credits_expected": sum(p["flow_credits_expected"] for p in per_part_summary),
        "vertex_try1_gbp": round(sum(p["vertex_try1_gbp"] for p in per_part_summary), 2),
        "vertex_expected_gbp": round(sum(p["vertex_expected_gbp"] for p in per_part_summary), 2),
        "explorer": 2,
        "teach_overlays": overlay_count,
    }

    plan = {
        "film": "015_Hooke-Cell-Theory",
        "version": "v01",
        "written": "2026-10-16",
        "task": "J0397: HOS 015 pre-VO plate boards v01 (from hooke_script_master_v01.md + SOURCES_v01.md). Flow-first. Mint nothing. Parked for Chief.",
        "script": "hooke_script_master_v01.md (94.0 PASS)",
        "facts_pass": "SOURCES_v01.md (18 rows)",
        "vo_status": "Awaiting Chief script sign-off and long VO recording; rows re-time automatically onto Scribe STT once VO locks.",
        "readings": {
            "flow_credits_left": 23740,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015. Nothing in 015 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 015 Cells: The Slice of Cork That Changed Biology — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 16 Oct 2026, J0397. Built from `hooke_script_master_v01.md` (94.0 PASS) and `SOURCES_v01.md`.",
        "**No mint, no spend.** Pre-VO clock timings (`181.9 s` base picture grid; re-times automatically onto Scribe word timestamps once long VO locks).",
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
        "# 015 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 16 Oct 2026, J0397. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `hooke_script_master_v01.md` (94.0 PASS) and `SOURCES_v01.md` so 015's full plate board rows, non-emissive Fast prompts, £0 code graphics, public-domain archive scan, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
        "",
        "## Totals (base 26-row board before VO continuation splits)",
        "",
        "| Part | Title | Rows | Quality | Fast | £0 code | £0 archive | £0 reuse | Flow try-1 | Flow expected | Vertex try-1 | Vertex expected |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for p in per_part_summary:
        pr_lines.append(
            f"| Part 0{p['part']} | {p['title']} | {p['rows']} | {p['Quality']} | {p['Fast']} | {p['code_graphic']} | {p['archive']} | {p['reuse']} | {p['flow_credits_try1']} | {p['flow_credits_expected']} | £{p['vertex_try1_gbp']:.2f} | £{p['vertex_expected_gbp']:.2f} |"
        )
    pr_lines.append(
        f"| **Film** | | **{totals['rows']}** | **{totals['Quality']}** | **{totals['Fast']}** | **{totals['code_graphic']}** | **{totals['archive']}** | **{totals['reuse']}** | **{totals['flow_credits_try1']}** | **{totals['flow_credits_expected']}** | **£{totals['vertex_try1_gbp']:.2f}** | **£{totals['vertex_expected_gbp']:.2f}** |"
    )
    pr_lines.extend([
        "",
        "## Route breakdown",
        "",
        f"- **Quality ({totals['Quality']} rows):** readable faces (Robert Hooke, Samuel Pepys, Robert Boyle, Isaac Newton, Joseph Jackson Lister, Robert Brown, Matthias Schleiden, Theodor Schwann, Robert Remak, Rudolf Virchow), candle/lamp/water-globe light scenes, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight and matte microscopic/prop shots (oak bark & hand lens, honeycomb cork walls, 3-object table, cork cross/lengthwise walls, 1710 Gresham College crates, blood slide & neuron sketch, dividing cell bench). Zero candles, flames, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_cubic_inch_cork_1_25_billion` — inked cubic-inch cork diagram (1,080 pores/inch, 1,259,712,000 cells/in³) (`SCALE: 1.25 billion cells in a cube the size of a sugar lump`)",
        "  2. `P1:06_30_trillion_human_cells_scale` — 1.25B cork cells vs 30T human cells (`SCALE: 30 trillion cells in you — 3,700 times the number of people on Earth`)",
        "  3. `P2:03_hooke_brine_globe_optics_diagram` — inked optical diagram of Hooke's oil lamp and brine-globe condenser (`SCALE: magnified 50 times — making a flea look as long as a cat`)",
        "  4. `P4:01_crystal_mistake_vs_binary_division` — false crystal-in-fluid model vs Remak's binary frog-egg division (`SCALE: one cell doubling 45 times — enough to build all 30 trillion cells in an adult human`)",
        "  5. `P5:01_cell_lifespan_comparison_chart` — gut lining (3–5 days), red blood cells (120 days), cerebral cortex neurons (lifetime)",
        "  6. `P5:03_timeline_1665_to_1855_complete` — completed 6-date timeline 1665 → 1855 (`SCALE: 190 years from Hooke's cork slice to Omnis cellula e cellula`)",
        f"- **£0 public-domain archive scan ({totals['archive']} row, lettering-risk avoided):** `P1:02_micrographia_cork_scan` — Hooke's *Micrographia* (1665), Schem. XI Fig. 1 copperplate engraving of cork pores.",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:05_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"015 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
