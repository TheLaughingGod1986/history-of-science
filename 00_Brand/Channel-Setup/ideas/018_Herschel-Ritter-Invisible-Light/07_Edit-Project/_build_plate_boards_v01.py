#!/usr/bin/env python3
"""HOS 018 (Infrared: The Thermometer Experiment That Found Invisible Light) pre-VO plate boards v01. J0413. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/018_Herschel-Ritter-Invisible-Light/herschel_script_master_v01.md
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
        "Part 01 — The Thermometer in the Dark",
        [
            ("01_slough_prism_thermometer_in_dark", 0.0, 5.5, "A", False, "HOTTER IN THE DARK", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + dramatic sunbeam prism rainbow in darkened room and rising mercury column.",
             STYLE + "Slough, England, 11 February 1800: in a darkened Georgian study, a single shaft of sunlight passes through a crown-glass prism in the window shutter and casts a vivid rainbow across a slanted wooden board; half an inch past the red edge, in the pitch-dark shadow, the silver mercury column inside a blackened-bulb thermometer climbs rapidly upward." + QUAL_TAIL,
             {"kind": "WHEN", "label": "SLOUGH · 11 FEBRUARY 1800", "hold_s": 3.5}),
            ("02_two_experimenters_slough_jena", 5.5, 6.0, "B", False, "TWO ENDS OF THE RAINBOW", "Quality",
             "Quality: readable faces (William Herschel in England; Johann Wilhelm Ritter in Jena).",
             STYLE + "Split period composition: on the left in England, William Herschel leans over his slanted wooden prism board and three mercury thermometers; on the right in Jena, Johann Wilhelm Ritter watches white silver-chloride paper turn jet-black in the dark shadow past the violet band." + QUAL_TAIL,
             None),
            ("03_newton_prism_and_brass_telescope", 11.5, 6.0, "C", False, "SEVEN COLOURS ONLY?", "Fast",
             "Fast: daylight workbench prop shot of glass prism on wooden stand beside a brass telescope tube. Nothing emissive, no face.",
             STYLE + "In daylight on a wooden study table, a triangular glass prism on a brass stand rests beside an eighteenth-century optics drawing and a polished brass refracting telescope." + FAST_TAIL,
             {"kind": "WHEN", "label": "1666 · WINTER 1800", "hold_s": 3.5}),
            ("04_herschel_thermometer_bar_chart", 17.5, 8.0, "E", False, "+9°F IN THE DARK", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked bar chart compares Herschel's 1800 thermometer rises across violet (+2°F), green (+3.25°F), red (+6.875°F in 10 min), and the dark infrared zone half an inch beyond red (+9°F / 5°C in 16 min).",
             {"kind": "DATA", "label": "+2°F VIOLET · +6.875°F RED · +9°F DARK", "detail": "Inked bar chart of Herschel's thermometer readings across violet (+2°F), green (+3.25°F), red (+6.875°F) and dark infrared (+9°F in 16 min)", "scale": "half an inch past red — the width of a thumb into complete darkness, yet hotter than the brightest visible light", "who_card": "William Herschel (1738–1822) — Hanoverian-British astronomer · Johann Wilhelm Ritter (1776–1810) — German natural philosopher", "when_stamp": "11 February 1800 · 22 February 1801", "hold_s": 3.8}),
            ("05_cardboard_slit_three_thermometers_pan", 25.5, 5.5, "A", False, "BLACKENED BULBS", "Fast",
             "Fast: daylight pan across slanted wooden board and three blackened-bulb thermometers between code graphics so two full-frame graphics never run back to back.",
             STYLE + "In soft daylight, the camera tracks across a slanted wooden board holding three matched mercury thermometers with Indian-ink blackened bulbs behind a cardboard screen with a narrow slit." + FAST_TAIL,
             None),
            ("06_em_spectrum_piano_postage_stamp_scale", 31.0, 8.0, "E", False, "ONE TINY SLIVER", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked electromagnetic spectrum scale unfurls like a long keyboard comparing the 380–750 nm visible band (<0.01% of the spectrum, one octave) against infrared (750 nm – 1 mm) and ultraviolet (10–380 nm).",
             {"kind": "DATA", "label": "380–750 NM · ONE OCTAVE (<0.01%)", "detail": "Inked electromagnetic spectrum scale comparing the 380–750 nm visible band against infrared and ultraviolet", "scale": "if the full electromagnetic spectrum stretched from London to New York, the rainbow your eyes can see would be narrower than a postage stamp", "hold_s": 3.8}),
            ("07_table_three_props_prism_thermometer_paper", 39.0, 5.5, "C", False, "SLOUGH, FEBRUARY 1800", "Fast",
             "Fast: daylight prop table (callback source for Part 05: brass-mounted prism, blackened mercury thermometer, strip of silver-chloride paper). Nothing emissive.",
             STYLE + "On a wooden laboratory workbench in soft window light sit three objects side by side: a brass-mounted crown-glass prism, a wooden-backed mercury thermometer with a blackened bulb, and a white strip of silver-coated paper." + FAST_TAIL,
             None),
            ("08_explorer_slough_prism_table", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing on the wooden prism table beside Thermometer No. 1 in the dark shadow past the red band, the Explorer holds a brass hand-mirror just outside the rainbow, feels the invisible warmth on its gloved palm, and looks from the rising mercury column to the prism with wide eyes." + EXP_TAIL,
             None),
            ("09_smoked_solar_filter_and_sheet_music", 67.5, 5.5, "B", False, "FROM MUSIC TO THE SUN", "Fast",
             "Fast: daylight desk shot of coloured glass telescope filters beside handwritten symphony sheet music and a brass oboe reed case. Nothing emissive.",
             STYLE + "In daylight on a Georgian study desk, dark red and dark green round glass telescope filters rest beside handwritten symphony sheet music and a wooden oboe." + FAST_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — The Musician's Burned Filters and the Three Thermometers",
        [
            ("01_william_and_caroline_bath_mirror", 85.0, 6.5, "A", False, "BATH · 1773–1781", "Quality",
             "Quality: readable faces (William Herschel grinding speculum mirror by hand while Caroline Herschel spoon-feeds him supper).",
             STYLE + "Bath, England, 1781: in a Georgian parlour turned workshop, William Herschel in rolled shirt-sleeves grinds a circular speculum-metal telescope mirror by hand while his sister Caroline Herschel in a mob cap holds an open notebook and feeds him a spoonful of supper." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Caroline Herschel", "line_2": "(1750–1848) — Hanoverian-British astronomer", "fact_card": "Composed 24 symphonies first", "when_stamp": "Bath, 1773–1781 · 13 March 1781", "timeline_step": "2/7 · 13 Mar 1781 (Herschel discovers Uranus)", "hold_s": 3.8}),
            ("02_red_vs_green_solar_filters", 91.5, 6.0, "B", False, "RED BURNS, GREEN COOLS", "Quality",
             "Quality: readable face (William Herschel at garden telescope swapping cracked red solar filter for cool green filter).",
             STYLE + "Slough garden observatory, early 1800: William Herschel steps back from a brass telescope eyepiece, lifts out a dark red glass filter cracked by intense solar heat, and slots in a cool dark green glass filter." + QUAL_TAIL,
             None),
            ("03_three_thermometers_colour_test", 97.5, 6.0, "C", False, "THREE THERMOMETERS", "Fast",
             "Fast: close view of wooden prism stand where single bands of violet, green, and red light fall through a cardboard slit onto Thermometer No. 1 beside two shaded control thermometers. No face, no flame.",
             STYLE + "Close view of Herschel's slanted wooden prism stand: a narrow band of deep red light passes through a slit in a cardboard screen onto the blackened bulb of Thermometer No. 1 while Thermometers No. 2 and No. 3 sit in the shade." + FAST_TAIL,
             {"kind": "WHEN", "label": "27 MARCH 1800", "hold_s": 3.5}),
        ],
    ),
    (
        3,
        "Part 03 — Into the Dark: Infrared and Ritter's Ultraviolet Twin",
        [
            ("01_five_parallel_lines_past_red", 103.5, 6.0, "A", False, "HALF AN INCH PAST RED", "Fast",
             "Fast: close view of gloved hands sliding Thermometer No. 1 onto the first of five ruled parallel ink lines half an inch into the dark shadow beyond the red edge of the rainbow. No face, no readable text.",
             STYLE + "Close top-down view of a white paper sheet on Herschel's prism board: five parallel ink lines sit spaced half an inch apart in the dark shadow past the red edge of the rainbow as Thermometer No. 1 slides onto the first line in the dark and its mercury column rises." + FAST_TAIL,
             {"kind": "WHEN", "label": "24 APRIL 1800", "timeline_step": "3/7 · 11 Feb 1800 (Herschel discovers infrared)", "hold_s": 3.5}),
            ("02_ritter_jena_silver_chloride_1801", 109.5, 6.5, "B", False, "JENA · 22 FEBRUARY 1801", "Quality",
             "Quality: readable face (24-year-old Johann Wilhelm Ritter in Jena laying white silver-chloride paper beyond violet).",
             STYLE + "University of Jena, 22 February 1801: twenty-four-year-old Johann Wilhelm Ritter with tousled dark hair and a frock coat leans over a prism spectrum on a wooden table, placing a damp white strip of silver-chloride paper into the dark shadow past the violet edge where it turns jet-black." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Carl Wilhelm Scheele", "line_2": "(1742–1786) — Swedish pharmaceutical chemist", "fact_card": "Found ultraviolet with silver salt", "when_stamp": "1777 · Jena, 22 February 1801", "timeline_step": "5/7 · 22 Feb 1801 (Ritter discovers ultraviolet)", "hold_s": 3.8}),
            ("03_dual_infrared_ultraviolet_spectrum_diagram", 116.0, 8.0, "E", False, "TWICE AS SHORT AS RED", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked dual-spectrum diagram shows Herschel's thermometer peak 0.5 inches beyond the 750 nm red edge (+9°F in 16 min, +5.25°F at 1 inch) and Ritter's silver-chloride (AgCl) chemical blackening peak beyond the 380 nm violet edge.",
             {"kind": "DATA", "label": "<380 NM UV (AGCL) · >750 NM IR (+9°F)", "detail": "Inked dual-spectrum diagram showing Herschel's infrared heating peak 0.5 in past 750 nm red (+9°F) and Ritter's AgCl ultraviolet darkening peak past 380 nm violet", "scale": "380 nm violet to 750 nm red — ultraviolet waves are twice as short as red light, packing enough punch to break chemical bonds and sunburn your skin", "hold_s": 3.8}),
        ],
    ),
    (
        4,
        "Part 04 — The Discoverer's Doubt: Midpoint Twist",
        [
            ("01_herschel_glass_trap_poker_nov1800", 124.0, 6.5, "A", False, "6 NOVEMBER 1800", "Quality",
             "Quality: readable face (William Herschel) + red-hot glowing iron poker behind clear crown glass (never Fast).",
             STYLE + "Slough, 6 November 1800: William Herschel holds a clear pane of crown glass between a glowing red-hot iron poker and a blackened mercury thermometer, frowning as bright light shines through while the thermometer stays cool." + QUAL_TAIL,
             {"kind": "FACT", "label": "HERSCHEL THOUGHT HEAT WASN'T LIGHT", "when_stamp": "6 November 1800", "timeline_step": "4/7 · 6 Nov 1800 (Herschel's glass trap)", "hold_s": 3.8}),
            ("02_plate_xx_and_young_wavelengths_diagram", 130.5, 8.0, "E", False, "1,400 WAVES / DIME", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked reproduction of Herschel's November 1800 Plate XX curve compares visual brightness (~555 nm peak) against radiant heat (>750 nm peak), alongside Thomas Young's November 1801 two-slit wave interference rings (1/36,000 inch red ~700 nm vs 1/60,000 inch violet ~420 nm).",
             {"kind": "DATA", "label": "555 NM EYE PEAK VS >750 NM HEAT · 700 NM RED", "detail": "Inked comparison of Herschel's Nov 1800 brightness vs heat curves and Young's Nov 1801 wavelengths (1/36,000 in red vs 1/60,000 in violet)", "scale": "700 nanometres for red light — 1,400 waves of red light fit across the thickness of a single dime", "who_card": "Thomas Young (1773–1829) — English physician & physicist", "when_stamp": "November 1801", "timeline_step": "6/7 · Nov 1801 (Young's wave wavelengths)", "hold_s": 3.8}),
            ("03_melloni_rock_salt_and_maxwell", 138.5, 6.5, "B", False, "ONE ELECTROMAGNETIC WAVE", "Quality",
             "Quality: readable faces (Macedonio Melloni with rock-salt prism in Naples; James Clerk Maxwell in London).",
             STYLE + "Split period scene: on the left in Naples (1831), Italian physicist Macedonio Melloni focuses invisible heat through a transparent crystal prism carved from rock salt onto a brass thermopile; on the right in London (1865), bearded Scottish physicist James Clerk Maxwell stands beside wave curves on a slate board." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Macedonio Melloni & James Clerk Maxwell", "line_2": "Melloni (1798–1854) · Maxwell (1831–1879)", "when_stamp": "1831–1835 · 1865", "timeline_step": "7/7 · 1865 (Maxwell's electromagnetic waves)", "hold_s": 3.8}),
            ("04_explorer_melloni_rock_salt_bench", 145.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside Melloni's brass optical bench, the Explorer swaps a pane of ordinary window glass for a clear block of rock salt in front of the brass cone thermopile, watches the galvanometer needle swing wide, and nods in triumph." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — The Greenhouse Trap, James Webb and the Frog-Leg Spark",
        [
            ("01_timeline_1666_1865_and_body_10000nm", 150.5, 8.5, "E", False, "10,000 NM · 15× RED", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 7-date timeline completes: 1666 (Newton) · 13 Mar 1781 (Uranus) · 11 Feb 1800 (Infrared) · 6 Nov 1800 (Glass trap) · 22 Feb 1801 (Ultraviolet) · Nov 1801 (Young) · 1865 (Maxwell), alongside an inked thermal scale comparing visible red (750 nm) to a 37°C human body radiating at 10,000 nm (10 µm).",
             {"kind": "DATA", "label": "10,000 NM BODY HEAT · 1666 → 1865", "detail": "Completed 7-date invisible-light timeline (1666 → 1865) alongside 37°C human body 10,000 nm (10 µm) infrared radiation scale", "scale": "your body radiates at 10,000 nanometres — infrared waves 15 times longer than the deepest red your eyes can see", "fact_card": "Your body glows in infrared", "when_stamp": "1666–1865", "hold_s": 3.8}),
            ("02_window_trap_to_jwst_gold_mirror", 159.0, 6.0, "A", False, "13.5 BILLION LIGHT-YEARS", "Fast",
             "Fast: sunlit glass window pane transitioning to a 3D cartoon golden hexagonal segmented space telescope mirror against deep dark space (no glowing flares or stars that flicker). Nothing emissive.",
             STYLE + "From a sunlit Georgian glass window pane, the scene opens out to a five-layered silver sunshield and eighteen hexagonal gold-coated mirror segments floating silently in the cold shadow of deep space." + FAST_TAIL,
             None),
            ("03_volta_pile_frog_leg_spark_handoff", 165.0, 6.5, "C", False, "ANIMAL OR METAL?", "Quality",
             "Quality: electric spark jumping from Voltaic pile wire to frog leg on iron railing (handoff to 019 Galvani/Volta; sparks never on Fast).",
             STYLE + "Pavia and Jena, March 1800: on a laboratory workbench beside a strip of silver-chloride paper stands a tall stack of alternating zinc and silver discs separated by brine-soaked cardboard; as a brass wire touches an iron railing holding a frog's leg, a bright blue electric spark snaps across the gap." + QUAL_TAIL,
             {"kind": "WHEN", "label": "MARCH 1800", "hold_s": 3.5}),
            ("04_table_three_callback", 171.5, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_prism_thermometer_paper (callback, £0).",
             "Reuse P1:07_table_three_props_prism_thermometer_paper [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_prism_thermometer_paper"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_prism_thermometer_paper",
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
            "film": "018_Herschel-Ritter-Invisible-Light",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from herschel_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "018_Herschel-Ritter-Invisible-Light",
        "version": "v01",
        "written": "2026-10-16",
        "task": "J0413: HOS 018 pre-VO plate boards v01 (from herschel_script_master_v01.md + SOURCES_v01.md). Flow-first. Mint nothing. Parked for Chief.",
        "script": "herschel_script_master_v01.md (94.8 PASS)",
        "facts_pass": "SOURCES_v01.md (13 rows)",
        "vo_status": "Awaiting Chief script sign-off and long VO recording; rows re-time automatically onto Scribe STT once VO locks.",
        "readings": {
            "flow_credits_left": 23740,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018. Nothing in 018 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 018 Infrared: The Thermometer Experiment That Found Invisible Light — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 16 Oct 2026, J0413. Built from `herschel_script_master_v01.md` (94.8 PASS) and `SOURCES_v01.md`.",
        "**No mint, no spend.** Pre-VO clock timings (`173.9 s` base picture grid; re-times automatically onto Scribe word timestamps once long VO locks).",
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
        "# 018 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 16 Oct 2026, J0413. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `herschel_script_master_v01.md` (94.8 PASS) and `SOURCES_v01.md` so 018's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
        "",
        "## Totals (base 23-row board before VO continuation splits)",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (William Herschel, Caroline Herschel, Johann Wilhelm Ritter, Macedonio Melloni, James Clerk Maxwell), emissive/beam/spark scenes (Slough sunbeam rainbow in darkened study, red-hot iron poker behind crown glass, Voltaic pile spark jumping to frog leg), and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (Newton prism & brass telescope, 3 blackened thermometers behind cardboard slit, 3-object Slough workbench, solar filters & symphony sheet music, 3-thermometer colour test, 5 ruled parallel lines past red, window glass to chilled JWST gold mirror). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_herschel_thermometer_bar_chart` — Herschel's 1800 thermometer rises across violet (+2°F), green (+3.25°F), red (+6.875°F) and dark infrared 0.5 in past red (+9°F in 16 min) (`SCALE: half an inch past red — the width of a thumb into complete darkness, yet hotter than the brightest visible light`)",
        "  2. `P1:06_em_spectrum_piano_postage_stamp_scale` — 380–750 nm visible band (<0.01% of EM spectrum, one octave) vs full spectrum (`SCALE: if the full electromagnetic spectrum stretched from London to New York, the rainbow your eyes can see would be narrower than a postage stamp`)",
        "  3. `P3:03_dual_infrared_ultraviolet_spectrum_diagram` — Herschel's infrared heating peak (>750 nm, +9°F) and Ritter's AgCl ultraviolet darkening peak (<380 nm) (`SCALE: 380 nm violet to 750 nm red — ultraviolet waves are twice as short as red light, packing enough punch to break chemical bonds and sunburn your skin`)",
        "  4. `P4:02_plate_xx_and_young_wavelengths_diagram` — Herschel's Nov 1800 Plate XX brightness (~555 nm) vs heat (>750 nm) curves + Thomas Young's Nov 1801 wave interference wavelengths (`SCALE: 700 nanometres for red light — 1,400 waves of red light fit across the thickness of a single dime`)",
        "  5. `P5:01_timeline_1666_1865_and_body_10000nm` — completed 7-date timeline (1666 → 1865) + 37°C human body radiating at 10,000 nm (10 µm) (`SCALE: your body radiates at 10,000 nanometres — infrared waves 15 times longer than the deepest red your eyes can see`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_prism_thermometer_paper`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"018 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
