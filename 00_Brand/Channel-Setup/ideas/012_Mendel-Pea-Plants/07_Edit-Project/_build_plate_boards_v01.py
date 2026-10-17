#!/usr/bin/env python3
"""HOS 012 (Genetics: The Monk Who Counted 28,000 Pea Plants) pre-VO plate boards v01. J0397. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/012_Mendel-Pea-Plants/mendel_script_master_v01.md
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
        exp = try1 * TAKES_PER_KEEP[q] + STILLS_PER_PLATE * USD_PER_USD_STILL_GBP if False else (
            try1 * TAKES_PER_KEEP[q] + STILLS_PER_PLATE * USD_PER_STILL * GBP_PER_USD
        )
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
        "Part 01 — The Trait That Skipped a Generation",
        [
            ("01_pod_six_smooth_two_wrinkled", 0.0, 5.5, "A", False, "HIDDEN TRAITS", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + close hands splitting pod.",
             STYLE + "Brünn, 1856: warm morning sunlight streams into a walled monastery garden; hands in a dark friar's wool sleeve split open a fresh green pea pod, revealing six smooth golden peas and two wrinkled green ones side by side." + QUAL_TAIL,
             {"kind": "WHEN", "label": "BRÜNN · 1856", "hold_s": 3.5}),
            ("02_paintbrush_pollen_cross", 5.5, 6.0, "A", False, "ONE PAINTBRUSH", "Fast",
             "Fast: daylight macro shot of flower and brush. Nothing emissive, no face.",
             STYLE + "In clear garden daylight, a fine camel-hair paintbrush lifts bright yellow pollen from a white pea blossom and touches it gently to a purple pea blossom while a small calico bag is tied over the stem." + FAST_TAIL,
             None),
            ("03_paint_pots_vs_whole_peas", 11.5, 6.0, "B", False, "PAINT OR PEAS?", "Fast",
             "Fast: daylight workbench prop shot. Nothing emissive, no face.",
             STYLE + "On a wooden workbench in daylight, two ceramic bowls of red and white paint swirl together into pale pink, while beside them two whole dried peas — one bright yellow, one bright green — rest side by side on dark wood." + FAST_TAIL,
             {"kind": "WHO", "line_1": "Charles Darwin", "line_2": "(1809–1882) — English naturalist", "when_stamp": "1850s", "hold_s": 3.8}),
            ("04_28000_pea_plants_counter", 17.5, 8.0, "E", False, "28,000 PEA PLANTS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked counter climbs to 28,000 pea plants beside the 35-by-7-metre St Thomas's Abbey experimental garden plan and a city park rose garden scale comparison.",
             {"kind": "DATA", "label": "28,000 PEA PLANTS", "detail": "Inked counter climbing to 28,000 pea plants beside the 35m x 7m abbey garden plan", "scale": "more plants than a city park rose garden", "who_card": "Gregor Mendel (1822–1884) — Augustinian friar", "when_stamp": "St Thomas's Abbey · 1856–1863", "hold_s": 3.8}),
            ("05_abbey_trellis_rows_pan", 25.5, 5.5, "A", False, "UNBROKEN PACKETS", "Fast",
             "Fast: sunlit garden trellises between code graphics so two full-frame graphics never run back to back.",
             STYLE + "In a sunlit monastery courtyard, the camera rises slowly over long wooden trellises covered in climbing green pea vines with white and purple blossoms stretching along a warm stone wall." + FAST_TAIL,
             None),
            ("06_7324_seeds_two_litre_jar", 31.0, 8.0, "E", False, "7,324 SEEDS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked scale bar fills a two-litre glass jar to the brim with 7,324 dried smooth and wrinkled peas.",
             {"kind": "DATA", "label": "7,324 SEEDS", "detail": "Inked scale bar showing 7,324 seeds filling a 2-litre glass jar", "scale": "enough peas to fill a two-litre glass jar", "hold_s": 3.8}),
            ("07_table_three_props", 39.0, 5.5, "B", False, "BRUSH · TWEEZERS · POD", "Fast",
             "Fast: daylight prop table (callback source for Part 05). Nothing emissive.",
             STYLE + "On a wooden potting table in grey window light sit three objects side by side: a fine camel-hair paintbrush, a pair of brass forceps, and an open green pea pod." + FAST_TAIL,
             None),
            ("08_explorer_abbey_workbench", 62.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "At the edge of the abbey workbench, the Explorer peers through his round gold glasses at two wooden bowls of smooth and wrinkled peas, rolls one of each between his fingers, and looks up at a stack of leather notebooks in wonder." + EXP_TAIL,
             None),
            ("09_corridor_bell_candle", 67.5, 5.5, "C", False, "FAILED TWICE", "Quality",
             "Quality: candlelit stone corridor and friar closing notebook (never Fast).",
             STYLE + "In a warm candlelit monastery study, a young friar in a dark habit closes a ruled notebook beside a brass microscope as a small brass hand bell rings in the stone corridor." + QUAL_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — The Friar Who Failed Twice",
        [
            ("01_vienna_exam_fail_1850", 73.0, 6.0, "D", False, "VIENNA · 1850", "Quality",
             "Quality: readable faces (28-year-old Gregor Mendel and Vienna examiner).",
             STYLE + "Vienna, summer 1850: in a wood-panelled university examination room, twenty-eight-year-old Gregor Mendel in round spectacles and a dark coat hands a written sheet across a polished desk while an older examiner slowly shakes his head." + QUAL_TAIL,
             {"kind": "FACT", "label": "FAILED TEACHER EXAM TWICE", "when_stamp": "Vienna · 1850", "hold_s": 3.8}),
            ("02_abbot_napp_gates_1843", 79.0, 6.0, "A", False, "BRÜNN · 1843", "Quality",
             "Quality: readable faces (Abbot Cyrill Napp welcoming young Mendel).",
             STYLE + "St Thomas's Abbey, Brünn, 1843: tall wooden monastery gates open onto a sunlit stone courtyard as Abbot Cyrill Napp, fifties with warm eyes in an Augustinian robe, welcomes the young farmer's son." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Cyrill Napp", "line_2": "(1792–1867) — Abbot of Brünn", "when_stamp": "Brünn · 1843", "timeline_step": "1/7 · 1843 (Enters St Thomas's Abbey)", "hold_s": 3.8}),
            ("03_doppler_vienna_lecture_1851", 85.0, 6.5, "D", False, "CHRISTIAN DOPPLER", "Quality",
             "Quality: readable face (Professor Christian Doppler at the Vienna slate board).",
             STYLE + "University of Vienna lecture hall, 1851: Professor Christian Doppler, late forties in a dark frock coat with chalk in hand, sketches wave curves on a large slate board while young Mendel takes careful notes on a wooden bench." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Christian Doppler", "line_2": "(1803–1853) — Vienna physics professor", "when_stamp": "Vienna · 1851–1853", "timeline_step": "2/7 · 1851–1853 (Studies under Doppler)", "hold_s": 3.8}),
            ("04_mendel_walks_out_ill_1856", 91.5, 6.0, "D", False, "WALKED OUT ILL", "Quality",
             "Quality: readable face (Mendel pressing hand to forehead in May 1856 exam).",
             STYLE + "Vienna, May 1856: in a quiet exam room, Gregor Mendel presses a hand to his forehead over an unwritten examination paper, rises slowly from his desk, and walks out into the corridor." + QUAL_TAIL,
             {"kind": "WHEN", "label": "MAY 1856", "hold_s": 3.5}),
            ("05_potting_bench_34_packets", 97.5, 5.5, "A", False, "34 SEED VARIETIES", "Fast",
             "Fast: daylight potting bench with seed packets. Nothing emissive, no face.",
             STYLE + "In a sunlit monastery potting shed, thirty-four small folded cream paper seed packets sit lined up in neat rows along a weathered wooden bench beside clay flowerpots." + FAST_TAIL,
             {"kind": "FACT", "label": "TESTED 34 SEED VARIETIES", "when_stamp": "Brünn · 1854–1856", "hold_s": 3.8}),
            ("06_timeline_1843_1856_packets", 103.0, 8.0, "E", False, "34 PACKETS · SHED SHELF", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an animated timeline builds (1843 · 1850 · 1851 · 1854 · 1856) beneath an inked garden shed shelf lined with 34 seed packets and 22 pure lines.",
             {"kind": "DATA", "label": "34 SEED PACKETS", "detail": "Timeline building 1843 → 1856 beside 34 seed packets on a garden shed shelf", "scale": "34 seed packets — enough to line a garden shed shelf", "hold_s": 3.8}),
            ("07_sealed_pea_keel_blossom", 111.0, 5.5, "A", False, "SEALED LIKE A TENT", "Fast",
             "Fast: daylight close-up of white pea flower petals. Nothing emissive.",
             STYLE + "Close macro shot in warm garden sunlight of a white pea blossom whose folded lower petals form a tightly closed boat-shaped keel around the centre of the flower." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — The Trait That Vanished",
        [
            ("01_mendel_forceps_253_crosses", 116.5, 6.5, "A", False, "253 HAND CROSSES", "Quality",
             "Quality: readable face (Mendel kneeling by trellis with forceps and brush).",
             STYLE + "Brünn abbey garden, spring 1856: Gregor Mendel kneels beside a wooden pea trellis in morning sunlight, using fine brass forceps to open a green bud and a camel-hair brush to dab golden pollen onto the stigma." + QUAL_TAIL,
             {"kind": "WHEN", "label": "SPRING 1856", "hold_s": 3.5}),
            ("02_first_gen_100_percent_smooth", 123.0, 5.5, "B", False, "100% SMOOTH", "Fast",
             "Fast: daylight workbench shot of two parent bowls and open pod. No face, nothing emissive.",
             STYLE + "On a wooden bench in daylight, a bowl of smooth round yellow peas sits on the left and a bowl of angular wrinkled peas on the right; between them, a freshly split green pod reveals a row of completely smooth round peas." + FAST_TAIL,
             None),
            ("03_bar_chart_5474_vs_1850", 128.5, 8.0, "E", False, "THREE TO ONE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked bar chart draws 5,474 smooth vs 1,850 wrinkled (2.96:1) and 6,022 yellow vs 2,001 green (3.01:1) beside a two-kilogram kitchen scale.",
             {"kind": "DATA", "label": "3 TO 1 · 5,474 : 1,850", "detail": "Inked bar chart of 5,474 smooth vs 1,850 wrinkled (2.96:1) and 6,022 yellow vs 2,001 green (3.01:1)", "scale": "three smooth for every wrinkled one, a two-kilogram pile", "hold_s": 3.8}),
            ("04_brass_scale_two_kg_bowls", 136.5, 5.5, "B", False, "TWO KILOGRAMS OF PEAS", "Fast",
             "Fast: daylight brass balance scale between code graphics so two full-frame graphics never run back to back.",
             STYLE + "On a sunlit wooden table, dried golden peas pour from a scoop into a deep brass scale pan until the balance arm tips against a heavy two-kilogram iron weight." + FAST_TAIL,
             None),
            ("05_punnett_grid_aa_explainer", 142.0, 8.0, "E", False, "DOMINANT & RECESSIVE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked 2x2 grid combines one pollen element (A or a) with one egg element (A or a) into AA, Aa, aA (three smooth) and aa (one wrinkled).",
             {"kind": "FACT", "label": "COINED DOMINANT & RECESSIVE", "detail": "Inked 2x2 grid showing AA, Aa, aA (3 smooth) and aa (1 wrinkled)", "hold_s": 3.8}),
            ("06_explorer_three_to_one_tally", 150.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside Mendel's potting bench, the Explorer traces four wooden slots containing three smooth golden peas and one wrinkled green pea with a gloved finger and smiles as the pattern clicks." + EXP_TAIL,
             None),
            ("07_brunn_lecture_1865", 155.5, 6.5, "D", False, "8 FEBRUARY 1865", "Quality",
             "Quality: readable faces + evening gas/oil lamps at the Brünn Natural Science Society.",
             STYLE + "Brünn, evening of 8 February 1865: Gregor Mendel stands at a wooden lectern in a warm lamp-lit hall before forty seated gentlemen in dark coats, holding his handwritten pages." + QUAL_TAIL,
             {"kind": "WHEN", "label": "BRÜNN · 8 FEB & 8 MAR 1865", "timeline_step": "4/7 · Feb–Mar 1865 & 1866 (Brünn lectures & paper)", "hold_s": 3.8}),
        ],
    ),
    (
        4,
        "Part 04 — The Hawkweed Trap",
        [
            ("01_unopened_1866_reprints", 162.0, 5.5, "C", False, "NOBODY UNDERSTOOD", "Fast",
             "Fast: grey window light over library table and uncut paper booklets. Nothing emissive.",
             STYLE + "Across a quiet European library table in grey window light, bound grey paper reprint booklets sit unopened with uncut page edges gathering dust." + FAST_TAIL,
             None),
            ("02_nageli_munich_letters_1866", 167.5, 6.5, "D", False, "CARL VON NÄGELI", "Quality",
             "Quality: readable face (Munich botany professor Carl von Nägeli in spectacles).",
             STYLE + "Munich, 1866: bearded botany professor Carl von Nägeli in wire spectacles sits at a specimen-strewn study desk reading a handwritten letter beside pressed dried hawkweed plants." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Carl von Nägeli", "line_2": "(1817–1891) — Munich botany professor", "when_stamp": "Munich · 1866–1873", "hold_s": 3.8}),
            ("03_hawkweed_magnifying_lens", 174.0, 6.0, "A", False, "THE HAWKWEED TRAP", "Quality",
             "Quality: readable face (Mendel squinting through lens at tiny yellow hawkweed floret with mirror light).",
             STYLE + "In the abbey workroom, Gregor Mendel squints through a brass magnifying lens with a fine steel needle over a tiny yellow-orange hawkweed flower cluster lit by a small angled mirror." + QUAL_TAIL,
             {"kind": "FACT", "label": "HAWKWEED CLONES ITS SEEDS", "when_stamp": "1903", "hold_s": 3.8}),
            ("04_abbot_mendel_tax_ledgers_1868", 180.0, 6.0, "C", False, "MY TIME WILL COME", "Quality",
             "Quality: readable face (older Abbot Mendel wearing pectoral cross).",
             STYLE + "St Thomas's Abbey, March 1868: an older Gregor Mendel wearing a gold Abbot's pectoral cross over his habit stands beside tall leather tax ledgers and gazes out the window toward his quiet garden." + QUAL_TAIL,
             {"kind": "WHEN", "label": "MARCH 1868", "hold_s": 3.5}),
            ("05_courtyard_brazier_burning_1884", 186.0, 6.0, "C", False, "6 JANUARY 1884", "Quality",
             "Quality: fire and glowing embers in winter snow (never Fast).",
             STYLE + "St Thomas's Abbey courtyard, 6 January 1884: in falling winter snow, black-robed novices drop stacks of loose handwritten papers into an iron brazier as orange sparks rise into the dusk." + QUAL_TAIL,
             {"kind": "WHEN", "label": "6 JANUARY 1884", "timeline_step": "5/7 · 6 Jan 1884 (Mendel dies; notes burned)", "hold_s": 3.8}),
        ],
    ),
    (
        5,
        "Part 05 — Three Letters in the Spring of 1900",
        [
            ("01_timeline_35_year_gap_1900", 192.0, 8.5, "E", False, "35 YEARS · 1865 → 1900", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the animated timeline spans from 1865 across a 35-year gap bracket to Spring 1900 and 1905 (1843 · 1856 · 1865 · 1866 · 1884 · 1900 · 1905).",
             {"kind": "DATA", "label": "35 YEARS · 1865 → 1900", "detail": "Complete 7-date timeline with 35-year gap bracket from 1865 to Spring 1900", "scale": "thirty-five years — longer than a human generation", "when_stamp": "Spring 1900", "hold_s": 3.8}),
            ("02_three_rediscoverers_1900", 200.5, 6.5, "D", False, "REDISCOVERED IN 1900", "Quality",
             "Quality: readable faces (Hugo de Vries, Carl Correns, Erich von Tschermak).",
             STYLE + "Spring 1900: three triptych study panels in warm lamplight show botanists Hugo de Vries in Amsterdam, Carl Correns in Tübingen, and Erich von Tschermak in Vienna each holding open the 1866 Brünn journal." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "De Vries · Correns · Tschermak", "line_2": "Hugo de Vries (1848–1935) · Carl Correns (1864–1933) · Erich von Tschermak (1871–1962)", "hold_s": 3.8}),
            ("03_bateson_cambridge_1905", 207.0, 6.0, "D", False, "GENETICS · 1905", "Quality",
             "Quality: readable face (William Bateson at his Cambridge desk).",
             STYLE + "Cambridge, April 1905: biologist William Bateson, forties with a thick moustache in a tweed coat, dips a fountain pen and writes earnestly at a sunlit wooden desk piled with pea-breeding records." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "William Bateson", "line_2": "(1861–1926) — Cambridge biologist", "when_stamp": "18 April 1905", "timeline_step": "7/7 · 1905 (Bateson coins 'genetics')", "hold_s": 3.8}),
            ("04_single_switch_vs_polygenic_curve", 213.0, 8.0, "E", False, "MANY GENES TOGETHER", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, a single two-way brass switch (6 ft tall vs 1 ft dwarf pea stems) contrasts with a row of twelve small sliders adding up to a smooth bell curve of human heights.",
             {"kind": "DATA", "label": "MANY GENES TOGETHER", "detail": "Inked diagram comparing single-gene pea switch (6 ft vs 1 ft) with polygenic bell curve of human height", "scale": "six feet tall vs one foot tall pea stems", "hold_s": 3.8}),
            ("05_darwin_down_house_unread", 221.0, 6.5, "C", False, "THE UNREAD ANSWER", "Quality",
             "Quality: readable face (older bearded Charles Darwin in candlelit study).",
             STYLE + "Down House, England: an older white-bearded Charles Darwin sits in his warm lamp-lit study surrounded by finch specimens and open notebooks, while on a high bookshelf a German journal sits uncut." + QUAL_TAIL,
             None),
            ("06_table_three_callback", 227.5, 2.4, "B", False, None, "reuse",
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
            "film": "012_Mendel-Pea-Plants",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from mendel_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "012_Mendel-Pea-Plants",
        "version": "v01",
        "written": "2026-10-16",
        "task": "J0397: HOS 012 pre-VO plate boards v01 (from mendel_script_master_v01.md + SOURCES_v01.md). Flow-first. Mint nothing. Parked for Chief.",
        "script": "mendel_script_master_v01.md (94.0 PASS)",
        "facts_pass": "SOURCES_v01.md (33 rows)",
        "vo_status": "Awaiting Chief script sign-off and long VO recording; rows re-time automatically onto Scribe STT once VO locks.",
        "readings": {
            "flow_credits_left": 23740,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012. Nothing in 012 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 012 Genetics: The Monk Who Counted 28,000 Pea Plants — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 16 Oct 2026, J0397. Built from `mendel_script_master_v01.md` (94.0 PASS) and `SOURCES_v01.md`.",
        "**No mint, no spend.** Pre-VO clock timings (`229.9 s` base picture grid; re-times automatically onto Scribe word timestamps once long VO locks).",
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
        "# 012 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 16 Oct 2026, J0397. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `mendel_script_master_v01.md` (94.0 PASS) and `SOURCES_v01.md` so 012's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
        "",
        "## Totals (base 34-row board before VO continuation splits)",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Mendel, Abbot Cyrill Napp, Christian Doppler, Carl von Nägeli, Hugo de Vries, Carl Correns, Erich von Tschermak, William Bateson, Charles Darwin), candle/lamp/fire scenes (abbey study candle, Brünn 1865 evening lecture, 1884 snow brazier), and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight and grey-window-light prop and garden shots (paintbrush cross, paint pots vs peas, abbey trellises, 3-object table, 34 seed packets on bench, sealed pea keel blossom, smooth parent bowls, brass balance scale, unopened 1866 reprints). Zero candles, flames, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_28000_pea_plants_counter` — inked counter climbing to 28,000 pea plants beside the 35×7 m abbey garden plan (`SCALE: more plants than a city park rose garden`)",
        "  2. `P1:06_7324_seeds_two_litre_jar` — inked scale bar filling a 2-litre glass jar with 7,324 seeds (`SCALE: enough peas to fill a two-litre glass jar`)",
        "  3. `P2:06_timeline_1843_1856_packets` — animated timeline (1843 · 1850 · 1851 · 1854 · 1856) beside 34 seed packets (`SCALE: enough to line a garden shed shelf`)",
        "  4. `P3:03_bar_chart_5474_vs_1850` — inked bar chart of 5,474 smooth vs 1,850 wrinkled (2.96:1) and 6,022 yellow vs 2,001 green (3.01:1) (`SCALE: three smooth for every wrinkled one, a two-kilogram pile`)",
        "  5. `P3:05_punnett_grid_aa_explainer` — inked 2×2 grid combining pollen and egg elements (`AA, Aa, aA` vs `aa`)",
        "  6. `P5:01_timeline_35_year_gap_1900` — completed 7-date timeline (1843 → 1905) with 35-year gap bracket (`SCALE: thirty-five years — longer than a human generation`)",
        "  7. `P5:04_single_switch_vs_polygenic_curve` — single two-way pea switch (6 ft vs 1 ft) vs polygenic sliders forming human height bell curve",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:06_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"012 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
