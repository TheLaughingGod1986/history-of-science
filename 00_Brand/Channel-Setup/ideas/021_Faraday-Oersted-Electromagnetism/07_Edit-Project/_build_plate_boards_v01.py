#!/usr/bin/env python3
"""HOS 021 (The Electric Motor: How a Cup of Mercury Changed the World) pre-VO plate boards v01. J0430. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/021_Faraday-Oersted-Electromagnetism/faraday_script_master_v01.md
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
        "Part 01 — The Spinning Wire in the Basement",
        [
            ("01_faraday_mercury_cup_motor_1821", 0.0, 5.5, "A", False, "THE FIRST ELECTRIC MOTOR", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + copper wire whirling in rapid circles through gleaming liquid mercury around a bar magnet in the Royal Institution basement.",
             STYLE + "London, 4 September 1821: in the Royal Institution basement laboratory, a copper wire hanging from a cork dips into a gleaming glass cup of silver liquid mercury around an upright bar magnet fixed in wax; the instant a battery wire touches the cup, the copper wire whirls in rapid continuous circles around the magnet, dissolving into a giant power-station turbine." + QUAL_TAIL,
             {"kind": "WHEN", "label": "LONDON · 4 SEPTEMBER 1821", "timeline_step": "2/7 · 4 Sep 1821 (Faraday's mercury-cup motor)", "hold_s": 3.5}),
            ("02_faraday_dancing_vs_davy_blackball_and_ring", 5.5, 6.0, "B", False, "APPRENTICE VS PRESIDENT", "Quality",
             "Quality: readable faces (young Michael Faraday in his basement lab; Royal Society President Sir Humphry Davy dropping a black ball into a ballot box).",
             STYLE + "Split period composition: on the left at the Royal Institution, young Michael Faraday beams beside his spinning mercury-cup motor; on the right, Sir Humphry Davy drops a single black ball into a mahogany Royal Society ballot box while Faraday winds copper wire around an iron ring." + QUAL_TAIL,
             None),
            ("03_compass_and_voltaic_pile_divided_bench", 11.5, 6.0, "C", False, "TWO SEPARATE FORCES?", "Fast",
             "Fast: daylight wooden workbench with a brass magnetic compass on the left and a Voltaic battery pile on the right separated by a chalk line. Nothing emissive, no face.",
             STYLE + "In daylight on a wooden laboratory workbench, a brass magnetic compass and a Voltaic silver-zinc battery pile sit on opposite sides of a sharp chalk dividing line." + FAST_TAIL,
             {"kind": "WHEN", "label": "1820", "hold_s": 3.5}),
            ("04_motor_1821_and_iron_ring_1831_reversible_chart", 17.5, 8.0, "E", False, "406 FT WIRE ON 6-INCH RING", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked reversible diagram shows Step 1 (1821 mercury-cup motor: electricity + magnet → continuous circular motion) and Step 2 (29 August 1831 6-inch iron ring wound with 203 ft + 203 ft = 406 ft of copper wire: changing magnetism → electricity).",
             {"kind": "DATA", "label": "1821 MOTOR VS 1831 RING (406 FT ON 6-IN RING)", "detail": "Inked comparison diagram of Faraday's two breakthroughs — the 1821 mercury-cup motor (electricity + magnet → motion) and the 29 August 1831 iron-ring induction coil (6-inch soft iron ring wound with 203 ft + 203 ft of copper wire: changing magnetism → electricity)", "scale": "406 feet of wire wound by hand around a 6-inch iron ring — longer than a football pitch coiled onto a ring the size of a doughnut", "who_card": "Hans Christian Ørsted (1777–1851) — Copenhagen physics professor · Michael Faraday (1791–1867) — Royal Institution lab assistant", "when_stamp": "21 April 1820 · 4 September 1821 · 29 August 1831", "hold_s": 3.8}),
            ("05_calico_thread_and_iron_ring_bench_pan", 25.5, 5.5, "A", False, "HAND-WOUND COILS", "Fast",
             "Fast: daylight pan across spools of calico thread, bare copper wire, and a 6-inch soft iron ring on Faraday's wooden bench between code graphics so two full-frame graphics never run back to back.",
             STYLE + "In soft basement window light, the camera tracks across spools of white calico string, coils of copper wire, and a six-inch wrought-iron ring on a scarred wooden workbench." + FAST_TAIL,
             None),
            ("06_global_electricity_99pct_turbines_50pct_motors_chart", 31.0, 8.0, "E", False, "EVERY PLUG, EVERY MOTOR", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked global energy flow chart shows ~99% of world grid electricity generated by Faraday electromagnetic induction turbines and ~50% of world electricity consumed by Faraday electric motors.",
             {"kind": "DATA", "label": "~99% GENERATED BY TURBINES · ~50% USED BY MOTORS", "detail": "Inked global electricity chart showing ~99% of grid electricity generated by spinning electromagnetic turbines and ~50% of global electricity consumed by electric motors", "scale": "from your phone's tiny vibrating buzzer to a 1,000-megawatt power station — half of all electricity on Earth spins a Faraday motor", "hold_s": 3.8}),
            ("07_table_three_props_compass_mercury_cup_ring", 39.0, 5.5, "C", False, "COPENHAGEN, 1820", "Fast",
             "Fast: daylight prop table (callback source for Part 05: brass magnetic compass under wire, glass mercury cup with bar magnet, 6-inch iron induction ring). Nothing emissive.",
             STYLE + "On a wooden laboratory workbench in soft window light sit three objects side by side: a glass-covered brass compass beneath a wire, a glass cup of silver mercury with an upright bar magnet, and a six-inch iron ring wrapped in copper coils." + FAST_TAIL,
             None),
            ("08_explorer_copenhagen_compass_circle", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing on the wooden lecture bench in Copenhagen beside the compass, the Explorer holds its own tiny brass pocket compass near the battery wire, watches the needle swing ninety degrees sideways in a circle around the wire, and traces the invisible ring in the air with one finger." + EXP_TAIL,
             None),
            ("09_compass_needle_jerking_perpendicular_closeup", 67.5, 5.5, "B", False, "90° RIGHT ANGLE", "Fast",
             "Fast: daylight macro view of a blued-steel compass needle inside a brass case snapping briskly to a 90-degree angle perpendicular to a straight platinum wire above the glass. No face, nothing emissive.",
             STYLE + "In crisp daylight, a blued-steel magnetic compass needle inside a brass case jerks sharply to stand at a ninety-degree right angle across a straight platinum wire stretched above the glass." + FAST_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — The Sideways Compass and the Cup of Mercury",
        [
            ("01_oersted_copenhagen_lecture_21_april_1820", 85.0, 6.5, "A", False, "NINETY DEGREES SIDEWAYS", "Quality",
             "Quality: readable face (Hans Christian Ørsted in Copenhagen lecture hall on 21 April 1820 closing battery circuit over compass).",
             STYLE + "Copenhagen, 21 April 1820: Danish physics professor Hans Christian Ørsted in a dark coat and white cravat closes a Voltaic battery circuit over a magnetic compass on his lecture table and leans forward in surprise as the needle swings ninety degrees sideways." + QUAL_TAIL,
             {"kind": "WHEN", "label": "COPENHAGEN · 21 APRIL 1820 · 21 JULY 1820", "timeline_step": "1/7 · 21 Apr 1820 (Ørsted's sideways compass)", "hold_s": 3.8}),
            ("02_straight_vs_90deg_circular_magnetic_force_diagram", 91.5, 8.0, "E", False, "CIRCULAR FORCE LINES", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked force-geometry diagram contrasts straight-line central push-and-pull forces against Ørsted and Faraday's 90-degree concentric circular magnetic lines of force wrapping around a current-carrying wire.",
             {"kind": "DATA", "label": "STRAIGHT PUSH/PULL VS 90° CIRCULAR MAGNETIC FIELD", "detail": "Inked force-geometry diagram contrasting straight-line central forces (push/pull along the line joining two bodies) vs Ørsted and Faraday's 90-degree circular magnetic lines of force wrapping around a current-carrying wire", "scale": "a 90-degree sideways push — instead of pulling the wire in and stopping, the circular magnetic field chases the wire around in an endless circle", "who_card": "Humphry Davy (1778–1829) — Royal Society president · William Hyde Wollaston (1766–1828) — English physicist & chemist", "fact_card": "Left school at age 13", "when_stamp": "1813", "hold_s": 3.8}),
            ("03_faraday_mercury_cup_there_they_go_1821", 99.5, 6.5, "B", False, '"THERE THEY GO!"', "Quality",
             "Quality: readable face (29-year-old Michael Faraday dancing with joy beside his spinning mercury-cup motor in the Royal Institution basement on 3–4 September 1821).",
             STYLE + "Royal Institution basement, London, 4 September 1821: twenty-nine-year-old Michael Faraday in a laboratory apron watches the suspended copper wire whirl non-stop around the bar magnet in the glass cup of mercury and dances joyfully around the wooden table." + QUAL_TAIL,
             {"kind": "WHEN", "label": "LONDON · 3–4 SEPTEMBER 1821", "hold_s": 3.5}),
            ("04_bookbinder_press_and_bound_science_volumes", 106.0, 5.5, "C", False, "BOOKBINDER'S APPRENTICE", "Fast",
             "Fast: daylight shot of a wooden bookbinder's press, leather-bound encyclopaedia volumes, and brass finishing tools on a London workshop bench. Nothing emissive, no face.",
             STYLE + "In warm daylight on a London bookbinder's bench, a wooden screw press holds freshly stitched leather-bound science volumes beside spools of linen thread and brass tooling irons." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — The Blackball Vote and the Ten-Year Silence",
        [
            ("01_davy_presidential_chair_vs_faraday_paper_1821", 111.5, 6.5, "A", False, "MENTOR TURNS RIVAL", "Quality",
             "Quality: readable faces (Sir Humphry Davy in the Royal Society presidential chair; young Michael Faraday holding his October 1821 paper).",
             STYLE + "Split period portrait: on the left, Sir Humphry Davy sits sternly in the carved wooden presidential chair of the Royal Society; on the right in the basement lab, young Michael Faraday holds his October 1821 Quarterly Journal of Science paper beside William Hyde Wollaston." + QUAL_TAIL,
             {"kind": "WHEN", "label": "OCTOBER 1821", "hold_s": 3.5}),
            ("02_royal_society_ballot_box_single_blackball_1824", 118.0, 6.0, "B", False, "ONE BLACKBALL VOTE", "Fast",
             "Fast: daylight close-up of a polished mahogany Royal Society ballot box as a hand drops a single black wooden ball into the reject compartment beside white balls. No face, nothing emissive.",
             STYLE + "In daylight inside a wood-panelled London room, a cuffed hand drops a single black wooden ball into the drawer of a polished mahogany Royal Society ballot box." + FAST_TAIL,
             {"kind": "FACT", "label": "One blackball vote against him", "when_stamp": "8 January 1824", "timeline_step": "3/7 · 8 Jan 1824 (Royal Society ballot)", "hold_s": 3.8}),
            ("03_optical_glass_notebook_convert_magnetism_1822", 124.0, 6.0, "C", False, '"CONVERT MAGNETISM INTO ELECTRICITY"', "Fast",
             "Fast: daylight close-up of Faraday's leather pocket notebook open on a wooden bench beside a small iron cylinder, a copper wire coil, and a block of heavy optical glass. No readable text on plate, nothing emissive.",
             STYLE + "In soft window light on a wooden workbench, a small leather pocket notebook lies open beside a solid iron cylinder, a loop of copper wire, and a thick square block of optical glass." + FAST_TAIL,
             {"kind": "WHEN", "label": "1822 · 1829", "hold_s": 3.5}),
            ("04_stationary_magnet_and_dead_galvanometer", 130.0, 5.5, "A", False, "TEN YEARS OF SILENCE", "Fast",
             "Fast: daylight close-up of a heavy horseshoe magnet clamped motionless beside a copper coil while a compass detector needle sits completely still at zero. Nothing emissive.",
             STYLE + "In daylight on a laboratory bench, a heavy iron horseshoe magnet sits clamped motionless beside a spool of copper wire while a nearby brass detector needle rests dead still at zero." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — The Iron Ring and the Half-Second Twitch",
        [
            ("01_faraday_iron_ring_29_august_1831", 135.5, 6.5, "A", False, "LONDON · 29 AUGUST 1831", "Quality",
             "Quality: readable face (Michael Faraday in the Royal Institution basement on 29 August 1831 touching a battery wire to his 6-inch iron ring wound with 406 feet of copper wire as the needle jerks once).",
             STYLE + "Royal Institution basement, London, 29 August 1831: Michael Faraday touches a battery wire to Side A of his six-inch soft iron ring wound in calico-insulated copper coils, and watches intently as a suspended magnetic needle three feet away jerks once and drops back to zero." + QUAL_TAIL,
             {"kind": "FACT", "label": "Only moving magnets make current", "when_stamp": "London, 29 August 1831", "timeline_step": "4/7 · 29 Aug 1831 (Faraday's iron-ring induction)", "hold_s": 3.8}),
            ("02_transient_induction_spike_trace_1831_diagram", 142.0, 8.0, "E", False, "+I SPIKE · 0 STEADY · -I SPIKE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked galvanometer trace shows Faraday's 29 August & 17 October 1831 discovery: a sharp positive current spike (+I) at battery connect / magnet thrust into a 220-foot coil, flat zero (0) while stationary, and a negative spike (-I) when pulled out.",
             {"kind": "DATA", "label": "+I ON THRUST · 0 WHILE STILL · -I ON PULL (220-FT COIL)", "detail": "Inked galvanometer trace showing Faraday's 29 August 1831 & 17 October 1831 induction experiment (spike +I at battery connect / magnet thrust into 220-foot coil → 0 while steady → spike -I at disconnect / magnet pull out)", "scale": "zero volts from a stationary magnet, even if it weighs a ton — but move the magnet with your hand and the electrons jump immediately", "when_stamp": "17 October 1831", "hold_s": 3.8}),
            ("03_faraday_copper_disc_generator_28_october_1831", 150.0, 6.5, "B", False, "THE FIRST GENERATOR", "Quality",
             "Quality: readable face (Michael Faraday turning the crank of his 12-inch copper disc between the poles of a horseshoe magnet on 28 October 1831).",
             STYLE + "London, 28 October 1831: Michael Faraday turns the brass crank handle of a twelve-inch copper disc spinning on an axle between the poles of a large horseshoe magnet while two sliding copper contact strips draw a steady electric current to a deflected galvanometer needle." + QUAL_TAIL,
             {"kind": "WHEN", "label": "28 OCTOBER 1831", "timeline_step": "5/7 · 28 Oct 1831 (12-inch copper-disc generator)", "hold_s": 3.8}),
            ("04_explorer_220ft_coil_magnet_yank", 156.5, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside Faraday's hollow paper cylinder wrapped in 220 feet of copper wire, the Explorer holds a bar magnet completely still inside the coil while watching the dead galvanometer needle, then yanks the magnet briskly out and jumps back as the needle swings wide." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Invisible Lines of Force and the Speed of Light",
        [
            ("01_timeline_1820_1865_and_300000kms_em_wave", 162.0, 8.5, "E", False, "300,000 KM/S · 7.5× EARTH/S", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 7-date timeline completes: 21 Apr 1820 (Ørsted compass) · 4 Sep 1821 (Mercury motor) · 8 Jan 1824 (Royal Society ballot) · 29 Aug 1831 (Iron ring) · 28 Oct 1831 (Copper-disc dynamo) · 1852 (Lines of force) · 1865 (Maxwell EM waves), alongside an inked electromagnetic wave rippling at 300,000 km/s.",
             {"kind": "DATA", "label": "300,000 KM/S (7.5× EARTH/S) · 1820 → 1865", "detail": "Animated 7-date timeline (1820 → 1865) alongside an inked electromagnetic wave diagram showing Faraday's electric and magnetic field lines rippling through space at 300,000 kilometres per second", "scale": "300,000 kilometres per second — Maxwell proved Faraday's electric and magnetic lines ripple through space at the exact speed of light, seven and a half times around Earth every second", "who_card": "James Clerk Maxwell (1831–1879) — Scottish mathematical physicist", "fact_card": "Iron filings mapped the field", "when_stamp": "1852 · 1865 · 1820–1865", "timeline_step": "6/7 · 1852 & 7/7 · 1865 (Maxwell's electromagnetic waves)", "hold_s": 3.8}),
            ("02_iron_filings_waxed_paper_field_lines_1852", 170.5, 6.0, "A", False, "SPACE IS NOT EMPTY", "Fast",
             "Fast: daylight macro view of fine dark iron filings sprinkled onto white waxed paper over a bar magnet tapping gently into curved spiderweb field arcs. No face, nothing emissive.",
             STYLE + "In crisp daylight, fine dark iron filings sprinkled onto a sheet of white waxed paper over a bar magnet tap gently into symmetrical curved spiderweb arcs stretching between the poles." + FAST_TAIL,
             None),
            ("03_induction_coil_uranium_drawer_to_swedish_snow_handoff", 176.5, 6.5, "C", False, "INSIDE THE ATOM", "Quality",
             "Quality: high-voltage induction coil spark beside a wooden drawer holding uranium ore and a photographic plate, dissolving into snowy Swedish woods in December 1938 (handoff to 022 Meitner/Hahn nuclear fission).",
             STYLE + "From a brass Ruhmkorff induction coil snapping a blue spark beside a wooden desk drawer holding a dark uranium rock on a wrapped photographic plate, the scene dissolves into sunlit snow-covered pine woods in Sweden in December 1938." + QUAL_TAIL,
             {"kind": "WHEN", "label": "FEBRUARY 1896 · DECEMBER 1938", "hold_s": 3.5}),
            ("04_table_three_callback", 183.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_compass_mercury_cup_ring (callback, £0).",
             "Reuse P1:07_table_three_props_compass_mercury_cup_ring [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_compass_mercury_cup_ring"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_compass_mercury_cup_ring",
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
            "film": "021_Faraday-Oersted-Electromagnetism",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from faraday_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "021_Faraday-Oersted-Electromagnetism",
        "version": "v01",
        "written": "2026-10-17",
        "task": "J0430: HOS 021 pre-VO plate boards v01 (from faraday_script_master_v01.md + SOURCES_v01.md). Flow-first. Mint nothing. Parked for Chief.",
        "script": "faraday_script_master_v01.md (92.0 PASS)",
        "facts_pass": "SOURCES_v01.md (8 rows)",
        "vo_status": "Awaiting Chief script sign-off and long VO recording; rows re-time automatically onto Scribe STT once VO locks.",
        "readings": {
            "flow_credits_left": 23740,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021. Nothing in 021 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 021 The Electric Motor: How a Cup of Mercury Changed the World — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 17 Oct 2026, J0430. Built from `faraday_script_master_v01.md` (92.0 PASS) and `SOURCES_v01.md`.",
        "**No mint, no spend.** Pre-VO clock timings (`185.4 s` base picture grid; re-times automatically onto Scribe word timestamps once long VO locks).",
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
        "# 021 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 17 Oct 2026, J0430. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `faraday_script_master_v01.md` (92.0 PASS) and `SOURCES_v01.md` so 021's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Hans Christian Ørsted, Michael Faraday, Sir Humphry Davy, William Hyde Wollaston), emissive/spark scenes (1821 mercury-cup motor answer image, 1896/1938 induction coil spark to Swedish snow handoff), and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (compass & Voltaic pile divided bench, calico thread & 6-inch iron ring pan, 3-object callback bench, 90° compass needle closeup, London bookbinder's press & bound volumes, Royal Society mahogany ballot box with 1 blackball, 1822 pocket notebook & optical glass block, stationary horseshoe magnet & dead galvanometer, 1852 iron filings on waxed paper). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_motor_1821_and_iron_ring_1831_reversible_chart` — reversible comparison of Faraday's 1821 mercury-cup motor (electricity + magnet → motion) and 29 Aug 1831 6-inch iron ring (406 ft wire: changing magnetism → electricity) (`SCALE: 406 feet of wire wound by hand around a 6-inch iron ring — longer than a football pitch coiled onto a ring the size of a doughnut`)",
        "  2. `P1:06_global_electricity_99pct_turbines_50pct_motors_chart` — ~99% of world grid electricity generated by Faraday induction turbines and ~50% consumed by electric motors (`SCALE: from your phone's tiny vibrating buzzer to a 1,000-megawatt power station — half of all electricity on Earth spins a Faraday motor`)",
        "  3. `P2:02_straight_vs_90deg_circular_magnetic_force_diagram` — straight-line central forces vs Ørsted & Faraday's 90° concentric circular magnetic field lines (`SCALE: a 90-degree sideways push — instead of pulling the wire in and stopping, the circular magnetic field chases the wire around in an endless circle`)",
        "  4. `P4:02_transient_induction_spike_trace_1831_diagram` — Faraday's 29 Aug & 17 Oct 1831 transient current spike (+I on thrust into 220-ft coil → 0 while still → -I on pull) (`SCALE: zero volts from a stationary magnet, even if it weighs a ton — but move the magnet with your hand and the electrons jump immediately`)",
        "  5. `P5:01_timeline_1820_1865_and_300000kms_em_wave` — completed 7-date timeline (1820 → 1865) + Maxwell's 1865 electromagnetic wave rippling at 300,000 km/s (`SCALE: 300,000 kilometres per second — Maxwell proved Faraday's electric and magnetic lines ripple through space at the exact speed of light, seven and a half times around Earth every second`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_compass_mercury_cup_ring`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"021 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
