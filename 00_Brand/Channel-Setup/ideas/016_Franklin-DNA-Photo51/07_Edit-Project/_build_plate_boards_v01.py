#!/usr/bin/env python3
"""HOS 016 (DNA: The Photograph That Revealed the Secret of Life) pre-VO plate boards v01. J0397. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/016_Franklin-DNA-Photo51/franklin_script_master_v01.md
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
        "Part 01 — The Cross in the Darkroom",
        [
            ("01_photo51_darkroom_x_cross", 0.0, 5.5, "A", False, "PHOTOGRAPH 51", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + warm amber darkroom glow and glass fibre.",
             STYLE + "King's College London, May 1952: in a warm amber-lit basement laboratory, a fine glass rod draws a glistening microscopic thread of hydrated DNA gel into a brass pinhole X-ray camera as a stark black X-shaped cross of ten layer lines resolves on a square photographic film." + QUAL_TAIL,
             {"kind": "WHEN", "label": "LONDON · MAY 1952", "hold_s": 3.5}),
            ("02_two_labs_london_cambridge", 5.5, 6.0, "B", False, "TWO LABS, ONE SECRET", "Quality",
             "Quality: readable faces (Rosalind Franklin in London; Watson and Crick in Cambridge).",
             STYLE + "Split period scene: on the left in London, Rosalind Franklin in a crisp white lab coat adjusts a brass X-ray collimator; on the right in Cambridge, James Watson and Francis Crick bolt brass rods onto a tall metal retort stand." + QUAL_TAIL,
             None),
            ("03_dna_vial_white_fibres", 11.5, 6.0, "C", False, "HOW DOES IT COPY?", "Fast",
             "Fast: daylight workbench prop shot of glass vial with white DNA paste. Nothing emissive, no face.",
             STYLE + "On a wooden laboratory bench in grey window light, a stoppered glass vial holds a spool of chalky white calf-thymus DNA fibres beside a brass microscope." + FAST_TAIL,
             {"kind": "WHEN", "label": "1951", "hold_s": 3.5}),
            ("04_photo51_helix_20_angstrom_diagram", 17.5, 8.0, "E", False, "20 ÅNGSTRÖMS WIDE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked diagram traces Photograph 51's X-shaped cross into a helical staircase 20 angstroms wide, with 10 rungs per turn rising 3.4 angstroms per step and repeating every 34 angstroms.",
             {"kind": "DATA", "label": "20 Å WIDE · 10 RUNGS PER TURN", "detail": "Inked diagram of Photograph 51's X-cross showing 10 rungs/turn, 3.4 Å step, 34 Å repeat, 20 Å diameter", "scale": "20 ångströms wide — 50,000 times thinner than a human hair", "who_card": "Rosalind Franklin (1920–1958) — King's College physical chemist · Raymond Gosling (1926–2015) — PhD student", "when_stamp": "2–6 May 1952", "hold_s": 3.8}),
            ("05_brass_microcamera_bench_pan", 25.5, 5.5, "A", False, "THE WET THREAD", "Fast",
             "Fast: daylight pan across brass microcamera and salt-bubbler glassware between code graphics so two full-frame graphics never run back to back.",
             STYLE + "In a quiet laboratory in grey window light, the camera tracks across a small cylindrical brass X-ray microcamera connected by rubber tubing to a glass wash-bottle of salt solution." + FAST_TAIL,
             None),
            ("06_two_metres_to_pluto_scale", 31.0, 8.0, "E", False, "PAST PLUTO AND BACK", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked scale comparison unspools 2 metres of DNA from a single cell nucleus and multiplies across trillions of human cells to tens of billions of kilometres reaching past Pluto and back.",
             {"kind": "DATA", "label": "2 METRES PER CELL · PAST PLUTO", "detail": "Inked comparison of 2 m DNA per diploid cell vs tens of billions of km across trillions of human cells", "scale": "tens of billions of km of DNA in you — enough to stretch past Pluto and back", "hold_s": 3.8}),
            ("07_table_three_props", 39.0, 5.5, "C", False, "FIBRE · X-RAY · CUT-OUTS", "Fast",
             "Fast: daylight prop table (callback source for Part 05). Nothing emissive.",
             STYLE + "On a wooden laboratory table in grey window light sit three objects side by side: a glass rod holding a white DNA fibre, a small square glass frame holding a developed X-ray film, and four flat hexagonal cardboard base cut-outs." + FAST_TAIL,
             None),
            ("08_explorer_kings_microcamera", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside the brass microcamera on the King's College workbench, the Explorer peers through a magnifying loupe at the four-inch square glass frame holding the dark X-cross film, traces the four arms of the X in the air, and looks up in quiet awe." + EXP_TAIL,
             None),
            ("09_blurred_plate_cambridge_door", 67.5, 5.5, "B", False, "BUILT BACKWARDS", "Fast",
             "Fast: grey window light over blurred film and lopsided wire stand as oak door closes. Nothing emissive.",
             STYLE + "In a grey-lit university room, a smeared circular X-ray film lies on a desk beside a lopsided three-stranded wire model as a heavy wooden laboratory door swings shut." + FAST_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — The Coal Chemist and the Wet Thread",
        [
            ("01_franklin_paris_coal_lab_1947", 73.0, 6.5, "A", False, "PARIS · 1947–1950", "Quality",
             "Quality: readable face (young Rosalind Franklin in Paris coal laboratory).",
             STYLE + "Paris, 1948: in a bright sunlit French laboratory, young Rosalind Franklin, late twenties with dark wavy hair in a clean white lab coat, places black lumps of coal and graphite into a brass X-ray holder." + QUAL_TAIL,
             {"kind": "FACT", "label": "STUDIED COAL BEFORE DNA", "when_stamp": "Paris · 1947–1950", "hold_s": 3.8}),
            ("02_wilkins_kings_corridor_1951", 79.5, 6.5, "A", False, "CROSSED WIRES", "Quality",
             "Quality: readable faces (Maurice Wilkins, Rosalind Franklin, and Raymond Gosling at King's College, Jan 1951).",
             STYLE + "King's College London, January 1951: tall biophysicist Maurice Wilkins in wire spectacles and a tweed jacket pauses in a basement laboratory doorway as Rosalind Franklin and young Raymond Gosling align a fine-focus X-ray tube." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Maurice Wilkins", "line_2": "(1916–2004) — King's College biophysicist", "when_stamp": "London · January 1951", "hold_s": 3.8}),
            ("03_a_dna_vs_b_dna_humidity_diagram", 86.0, 8.0, "E", False, "75% vs 92% HUMIDITY", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked two-state humidity diagram shows a 1.54-angstrom X-ray beam hitting dry crystalline A-DNA at 75% relative humidity and wet helical B-DNA stretched by 25% at 92% relative humidity.",
             {"kind": "DATA", "label": "A-DNA (75%) → B-DNA (92%)", "detail": "Inked two-state humidity diagram: dry A-DNA (75% RH) stretching 25% into wet B-DNA (92% RH) under 1.54 Å X-rays", "scale": "1.54-ångström X-rays — 3,500 times shorter than green visible light", "hold_s": 3.8}),
            ("04_photo51_missing_fourth_line", 94.0, 6.0, "A", False, "THE MISSING FOURTH LINE", "Fast",
             "Fast: matte tray view of the developed black X diffraction cross on square film. No face, nothing emissive.",
             STYLE + "Close top-down view in even light of a square photographic film resting in a shallow porcelain tray, showing a bold symmetrical black X of dark spots with the fourth horizontal row blank." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — The Inside-Out Blunder",
        [
            ("01_watson_crick_cavendish_1951", 100.0, 6.5, "B", False, "TIN AND WIRE", "Quality",
             "Quality: readable faces (James Watson and Francis Crick at the Cavendish Laboratory, Nov 1951).",
             STYLE + "Cavendish Laboratory, Cambridge, November 1951: lanky young American biologist James Watson and animated British physicist Francis Crick with brass calipers in hand bolt metal rods onto a six-foot retort stand." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "James Watson & Francis Crick", "line_2": "Watson (born 1928) · Crick (1916–2004)", "when_stamp": "Cambridge · November 1951", "hold_s": 3.8}),
            ("02_franklin_refutes_inside_out_1951", 106.5, 6.5, "B", False, "COMPLETELY INSIDE OUT", "Quality",
             "Quality: readable faces (Rosalind Franklin inspecting the flawed three-strand Cambridge model, 28 Nov 1951).",
             STYLE + "Cambridge, 28 November 1951: Rosalind Franklin stands calmly in a tailored coat before the lopsided three-stranded brass wire model, pointing decisively to its cramped central core while Watson and Crick look crestfallen." + QUAL_TAIL,
             {"kind": "WHEN", "label": "21 & 28 NOVEMBER 1951", "hold_s": 3.5}),
            ("03_bragg_bans_dna_models_1951", 113.0, 6.0, "B", False, "BANNED FROM MODELS", "Quality",
             "Quality: readable face (Cavendish director Sir Lawrence Bragg).",
             STYLE + "Cavendish Laboratory, December 1951: white-moustached director Sir Lawrence Bragg in a dark three-piece suit gestures firmly toward the dismantled brass model as wooden crates of metal jigs are closed." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Lawrence Bragg", "line_2": "(1890–1971) — Cavendish laboratory director", "fact_card": "Bragg banned their model-building", "hold_s": 3.8}),
            ("04_pauling_same_blunder_1953", 119.0, 6.5, "D", False, "THE SAME BLUNDER", "Quality",
             "Quality: readable face (chemist Linus Pauling at Caltech, Jan 1953).",
             STYLE + "Pasadena, January 1953: chemist Linus Pauling, fifties with grey hair in a dark suit, sits smiling beside a three-stranded molecular model on his desk while in Cambridge Watson and Crick read a typed manuscript in relief." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Linus Pauling", "line_2": "(1901–1994) — Caltech chemistry professor", "when_stamp": "January 1953", "hold_s": 3.8}),
        ],
    ),
    (
        4,
        "Part 04 — The Drawer Opens",
        [
            ("01_wilkins_opens_drawer_jan1953", 125.5, 6.5, "A", False, "30 JANUARY 1953", "Quality",
             "Quality: readable faces (Maurice Wilkins handing Photograph 51 to wide-eyed James Watson).",
             STYLE + "King's College London, 30 January 1953: in a quiet laboratory office, Maurice Wilkins pulls open a wooden desk drawer, lifts out the square glass-mounted print of Photograph 51, and hands it to a stunned James Watson." + QUAL_TAIL,
             {"kind": "FACT", "label": "SHOWN WITHOUT PERMISSION", "when_stamp": "London · 30 January 1953", "timeline_step": "4/6 · 30 Jan 1953 (Wilkins shows Photo 51)", "hold_s": 3.8}),
            ("02_perutz_mrc_c2_antiparallel_diagram", 132.0, 8.0, "E", False, "3 MILLION RUNGS / MM", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked crystal-symmetry diagram of Franklin's C2 monoclinic space group shows two antiparallel chains running in opposite directions (one up, one down) with 3.4-angstrom rung spacing.",
             {"kind": "DATA", "label": "C2 ANTIPARALLEL · 3.4 Å STEP", "detail": "Inked C2 monoclinic symmetry diagram showing antiparallel chains and 3.4 Å rung spacing", "scale": "3.4 ångströms between rungs — 3 million rungs stacked in a single millimetre", "who_card": "Max Perutz (1914–2002) — Cambridge molecular biologist", "when_stamp": "February 1953", "hold_s": 3.8}),
            ("03_chargaff_donohue_cardboard_cutouts", 140.0, 6.5, "B", False, "28 FEBRUARY 1953", "Quality",
             "Quality: readable faces (Jerry Donohue and James Watson sliding cardboard cut-outs at Cambridge desk).",
             STYLE + "Cavendish office, 28 February 1953: American chemist Jerry Donohue in rolled shirt-sleeves points to a textbook chemical ring while James Watson slides four flat white cardboard cut-outs across his wooden desk into matching pairs." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Erwin Chargaff & Jerry Donohue", "line_2": "Chargaff (1905–2002) · Donohue (1920–1985)", "fact_card": "Solved with cardboard cut-outs", "when_stamp": "1950 & 27–28 February 1953", "timeline_step": "5/6 · 28 Feb 1953 (Cardboard base pairs)", "hold_s": 3.8}),
            ("04_explorer_cardboard_base_pair", 146.5, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Sitting on the corner of Watson's wooden desk in Cambridge, the Explorer slides two flat white cardboard cut-outs together with his gloved hands until their notched edges click into a level rung, then grins." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — The Draft Dated 17 March",
        [
            ("01_franklin_17_march_1953_draft", 152.0, 6.0, "A", False, "17 MARCH 1953", "Fast",
             "Fast: daylight desk top-down shot of cream manuscript pages and fountain pen beside square X-ray frame. No readable text on plate, nothing emissive.",
             STYLE + "On a sunlit wooden desk at King's College, a neat stack of cream manuscript pages with fountain-pen ink underlines rests beside a fountain pen and the square glass frame of the X-ray cross." + FAST_TAIL,
             {"kind": "WHEN", "label": "17 MARCH & 25 APRIL 1953", "hold_s": 3.5}),
            ("02_timeline_1869_to_1953_6billion", 158.0, 8.5, "E", False, "6 BILLION LETTERS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 6-date timeline completes: 1869 (Miescher) · 1944 (Avery) · May 1952 (Photo 51) · 30 Jan 1953 (drawer) · 28 Feb 1953 (base pairs) · 25 Apr 1953 (Nature papers) beside a 6-billion-letter replication counter.",
             {"kind": "DATA", "label": "6 BILLION LETTERS · 1869 → 1953", "detail": "Completed 6-date DNA timeline (1869 → 25 Apr 1953) + 6-billion-base-pair cell division counter", "scale": "6 billion base-pair letters copied every time one of your cells divides", "when_stamp": "1869–1953", "hold_s": 3.8}),
            ("03_franklin_tribute_and_oxygen_handoff", 166.5, 6.5, "C", False, "WHAT BURNS THE FUEL?", "Quality",
             "Quality: candle flame under glass bell jar and portrait of Rosalind Franklin (never Fast).",
             STYLE + "Warm study workbench: three gold medals gleam softly beside a framed portrait of Rosalind Franklin, while the camera pans across the table to a glass bell jar inverted over mercury with a burning candle and a brass magnifying lens." + QUAL_TAIL,
             {"kind": "WHEN", "label": "16 APRIL 1958 · DECEMBER 1962", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
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
            "film": "016_Franklin-DNA-Photo51",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from franklin_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "016_Franklin-DNA-Photo51",
        "version": "v01",
        "written": "2026-10-16",
        "task": "J0397: HOS 016 pre-VO plate boards v01 (from franklin_script_master_v01.md + SOURCES_v01.md). Flow-first. Mint nothing. Parked for Chief.",
        "script": "franklin_script_master_v01.md (92.2 PASS)",
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
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016. Nothing in 016 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 016 DNA: The Photograph That Revealed the Secret of Life — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 16 Oct 2026, J0397. Built from `franklin_script_master_v01.md` (92.2 PASS) and `SOURCES_v01.md`.",
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
        "# 016 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 16 Oct 2026, J0397. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `franklin_script_master_v01.md` (92.2 PASS) and `SOURCES_v01.md` so 016's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Rosalind Franklin, Raymond Gosling, Maurice Wilkins, James Watson, Francis Crick, Sir Lawrence Bragg, Linus Pauling, Jerry Donohue), darkroom/candlelight scenes (Photo 51 amber darkroom, 1774 oxygen bell-jar handoff), and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight and grey-window-light prop and laboratory shots (white DNA fibres vial, brass microcamera & salt bubbler, 3-object table, blurred plate & closing oak door, matte tray view of missing 4th line, 17 March 1953 desk manuscript). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_photo51_helix_20_angstrom_diagram` — inked diagram of Photograph 51's X-cross showing 10 rungs/turn, 3.4 Å step, 34 Å repeat, 20 Å diameter (`SCALE: 20 ångströms wide — 50,000 times thinner than a human hair`)",
        "  2. `P1:06_two_metres_to_pluto_scale` — 2 metres of DNA per diploid cell vs tens of billions of km across trillions of cells (`SCALE: enough to stretch past Pluto and back`)",
        "  3. `P2:03_a_dna_vs_b_dna_humidity_diagram` — dry crystalline A-DNA (75% RH) vs wet helical B-DNA (92% RH, +25% stretch) under 1.54 Å X-rays (`SCALE: 1.54-ångström X-rays — 3,500 times shorter than green visible light`)",
        "  4. `P4:02_perutz_mrc_c2_antiparallel_diagram` — C2 monoclinic crystal symmetry showing two antiparallel chains and 3.4 Å spacing (`SCALE: 3.4 ångströms between rungs — 3 million rungs stacked in a single millimetre`)",
        "  5. `P5:02_timeline_1869_to_1953_6billion` — completed 6-date timeline (1869 → 25 Apr 1953) + 6-billion-letter replication counter (`SCALE: 6 billion base-pair letters copied every time one of your cells divides`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"016 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
