#!/usr/bin/env python3
"""HOS 014 (Fossils: The 12-Year-Old Girl Who Found Sea Dragons) pre-VO plate boards v01. J0397. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/014_Anning-Fossils-Extinction/anning_script_master_v01.md
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
        "Part 01 — The Eye in the Cliff",
        [
            ("01_lyme_cliff_eye_ring", 0.0, 5.5, "A", False, "SEA DRAGONS", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + ocean spray on Lyme Regis shale.",
             STYLE + "Lyme Regis, 1811: under dark storm-washed blue-grey sea cliffs with Atlantic spray in the background, a child's small wool-sleeved hand brushes wet clay from a four-foot stone jaw and a dinner-plate-sized bony eye ring." + QUAL_TAIL,
             {"kind": "WHEN", "label": "LYME REGIS · 1811", "hold_s": 3.5}),
            ("02_hammer_splits_shale_candle", 5.5, 6.0, "B", False, "ONE SMALL HAMMER", "Quality",
             "Quality: warm candlelight on fossil skeleton (never Fast).",
             STYLE + "On a wooden workbench in warm candlelight, a small iron fossil-collecting hammer taps a split slab of dark grey shale, revealing the gleaming ribs and spine of a fish-shaped reptile." + QUAL_TAIL,
             None),
            ("03_mammoth_tusk_blank_globe", 11.5, 6.0, "C", False, "STILL HIDING SOMEWHERE?", "Fast",
             "Fast: daylight museum table with tusk and blank terrestrial globe. Nothing emissive, no face.",
             STYLE + "In a tall eighteenth-century museum hall in grey window light, a huge curved fossil mammoth tusk rests on an oak table beside a brass-mounted terrestrial globe showing blank uncharted oceans." + FAST_TAIL,
             {"kind": "WHEN", "label": "LATE 1700s", "hold_s": 3.5}),
            ("04_17ft_ichthyosaur_rowing_boat", 17.5, 8.0, "E", False, "17 FEET LONG", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked scale diagram compares the 17-foot (5.2 m) 1811–1812 Ichthyosaurus skeleton and its 4-foot skull against a 15-foot wooden family rowing boat.",
             {"kind": "DATA", "label": "17 FEET · 5.2 METRES", "detail": "Inked scale comparison of 17-foot (5.2 m) Ichthyosaurus skeleton against a family rowing boat", "scale": "seventeen feet long — longer than a family rowing boat", "who_card": "Mary Anning (1799–1847) — fossil collector · Joseph Anning (1796–1849) — Mary's brother", "when_stamp": "Lyme Regis · 1811–1812", "hold_s": 3.8}),
            ("05_shale_ribs_exposed_pan", 25.5, 5.5, "A", False, "UNLIKE ANYTHING ALIVE", "Fast",
             "Fast: overcast daylight pan along fossil ribs in shale between code graphics so two full-frame graphics never run back to back.",
             STYLE + "In grey coastal daylight, the camera tracks slowly along a five-metre stone slab of dark blue-grey shale packed with curved ribs, paddle bones, and a long pointed jaw." + FAST_TAIL,
             None),
            ("06_35_neck_bones_vs_giraffe", 31.0, 8.0, "E", False, "35 NECK BONES", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked bone-count diagram compares the 7 cervical vertebrae of a giraffe with the 35 curving neck vertebrae of Anning's 1823 Plesiosaurus.",
             {"kind": "DATA", "label": "35 NECK BONES vs 7", "detail": "Inked anatomical comparison of 35 cervical vertebrae in Plesiosaurus vs 7 in a giraffe", "scale": "five times as many neck bones as a giraffe", "hold_s": 3.8}),
            ("07_table_three_props", 39.0, 5.5, "B", False, "HAMMER · AMMONITE · SKULL", "Fast",
             "Fast: daylight fossil shop table (callback source for Part 05). Nothing emissive.",
             STYLE + "On a wooden table inside a coastal fossil shop in grey window light sit three objects side by side: a small iron geology hammer, a coiled golden ammonite, and a fossilised belemnite ink chamber." + FAST_TAIL,
             None),
            ("08_explorer_fossil_shop", 62.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside the wooden table in the Lyme Regis fossil shop, the Explorer holds his brass magnifying glass over the huge bony eye ring of the ichthyosaur skull, steps back to take in the full tail, and tips his hat in respect." + EXP_TAIL,
             None),
            ("09_lightning_cliffs_waves", 67.5, 5.5, "A", False, "THE CRUMBLING CLIFFS", "Quality",
             "Quality: lightning flash and ocean waves on dark cliffs (never Fast).",
             STYLE + "At dusk on the Dorset coast, a bright flash of lightning illuminates the dark layered Blue Lias cliffs as foamy Atlantic waves pull back across wet shingle." + QUAL_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — Curiosities on the Beach",
        [
            ("01_cuvier_paris_elephant_jaws_1796", 73.0, 6.5, "C", False, "LOST SPECIES?", "Quality",
             "Quality: readable face (young Georges Cuvier in Paris, 1796).",
             STYLE + "Paris, 1796: young anatomist Georges Cuvier, late twenties in a high collar and dark coat, stands at an oak museum table comparing an Indian elephant skull, an African elephant skull, and a giant fossil mammoth jaw." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Georges Cuvier", "line_2": "(1769–1832) — Paris anatomist", "when_stamp": "Paris · 1796", "timeline_step": "1/7 · 1796 (Cuvier's mammoth paper)", "hold_s": 3.8}),
            ("02_elm_tree_baby_revived_1800", 79.5, 6.0, "D", False, "19 AUGUST 1800", "Quality",
             "Quality: readable faces + warm cottage firelight reviving baby Mary.",
             STYLE + "Lyme Regis, 19 August 1800: inside a stone cottage lit by a warm hearth, anxious neighbours gently lift fifteen-month-old baby Mary from a wooden basin of warm water wrapped in a wool blanket." + QUAL_TAIL,
             {"kind": "FACT", "label": "SURVIVED A LIGHTNING STRIKE", "when_stamp": "Lyme Regis · 19 August 1800", "timeline_step": "2/7 · 1800 (Mary survives lightning)", "hold_s": 3.8}),
            ("03_richard_anning_beach_shale", 85.5, 6.5, "A", False, "SNAKE-STONES", "Quality",
             "Quality: readable faces (Richard Anning and young Mary on Lyme Regis beach) + sea waves.",
             STYLE + "Lyme Regis beach, 1800s: cabinetmaker Richard Anning in a canvas apron kneels with young Mary beneath crumbling blue-grey shale ledges, chipping out coiled ammonites and tapered belemnites." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Richard Anning", "line_2": "(1766–1810) — cabinetmaker and collector", "hold_s": 3.8}),
            ("04_curiosity_table_outside_cottage", 92.0, 5.5, "B", False, "CURIOSITIES FOR SALE", "Fast",
             "Fast: daylight wooden table outside cottage door with coiled ammonites. No face, nothing emissive.",
             STYLE + "Outside a stone cottage door in coastal daylight, a small wooden table displays neatly arranged coiled ammonites and polished fossil vertebrae on a white cloth." + FAST_TAIL,
             {"kind": "WHEN", "label": "NOVEMBER 1810", "hold_s": 3.5}),
            ("05_timeline_1796_1812_23_pounds", 97.5, 8.0, "E", False, "£23 · HALF A YEAR'S WAGES", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an animated timeline builds (1796 · 1800 · 1810 · 1811–1812) beside an inked stack of 23 gold sovereigns compared against half a year's farm labourer wages.",
             {"kind": "DATA", "label": "£23 · HALF A YEAR'S WAGES", "detail": "Timeline 1796 → 1812 beside 23-pound coin stack scale comparison", "scale": "twenty-three pounds — half a year's labourer wages", "hold_s": 3.8}),
            ("06_four_foot_skull_in_shale_1811", 105.5, 5.5, "A", False, "FOUR-FOOT SKULL", "Fast",
             "Fast: overcast coastal daylight close-up of 4-foot stone jaw protruding from grey shale. Nothing emissive.",
             STYLE + "In grey winter daylight at the foot of a wet shale cliff, a four-foot fossilised jaw lined with interlocking conical teeth protrudes from crumbling blue-grey rock." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — The Seventeen-Foot Fish-Lizard",
        [
            ("01_mary_chips_ichthyosaur_1812", 111.0, 6.5, "A", False, "CHIPPED FROM SHALE", "Quality",
             "Quality: readable face (12-year-old Mary Anning excavating skeleton on beach) + waves.",
             STYLE + "Lyme Regis cliffs, 1812: twelve-year-old Mary Anning in a wool shawl chips carefully with her small hammer around heavy stone blocks of ribs and vertebrae while quarrymen help lift a slab onto a wooden cart." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1811–1812", "timeline_step": "3/7 · 1811–1812 (First Ichthyosaurus)", "hold_s": 3.8}),
            ("02_ichthyosaur_dinner_plate_eye_diagram", 117.5, 8.0, "E", False, "DINNER-PLATE EYE RINGS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked anatomical diagram of Ichthyosaurus highlights its dolphin snout, crocodile teeth, fish vertebrae, four paddles, and a bony sclerotic eye ring compared to a dinner plate.",
             {"kind": "DATA", "label": "EYE RINGS · DINNER-PLATE WIDE", "detail": "Inked anatomy diagram of Ichthyosaurus with bony sclerotic eye-ring scale comparison", "scale": "eye rings as wide as dinner plates", "hold_s": 3.8}),
            ("03_henley_and_home_1814_paper", 125.5, 6.5, "C", False, "NOT NAMED IN THE PAPER", "Quality",
             "Quality: readable faces (Henry Hoste Henley and Sir Everard Home at the Royal Society, 1814).",
             STYLE + "London, 1814: in a wood-panelled Royal Society library lit by tall windows, surgeon Sir Everard Home in a dark Regency coat holds up a copperplate engraving of the fossil skull before seated gentlemen." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Sir Everard Home", "line_2": "(1756–1832) — London surgeon · Henry Hoste Henley — lord of the manor", "fact_card": "Not named in the paper", "when_stamp": "London · 1814", "hold_s": 3.8}),
            ("04_birch_auction_1820_gavel", 132.0, 6.0, "C", False, "£400 TO SAVE THEM", "Quality",
             "Quality: readable faces (Colonel Thomas Birch and London auction crowd, 15 May 1820).",
             STYLE + "London, 15 May 1820: in an elegant showroom, an auctioneer's wooden gavel falls beside displayed fossil slabs as Colonel Thomas Birch watches wealthy collectors bid." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Thomas Birch", "line_2": "fossil collector — 15 May 1820 auction", "when_stamp": "15 May 1820", "hold_s": 3.8}),
        ],
    ),
    (
        4,
        "Part 04 — The Fake That Proved Extinction",
        [
            ("01_mary_plesiosaurus_slab_1823", 138.0, 6.5, "A", False, "PLESIOSAURUS · 1823", "Quality",
             "Quality: readable face (24-year-old Mary Anning over the 9-foot Plesiosaurus slab).",
             STYLE + "Lyme Regis, 10 December 1823: twenty-four-year-old Mary Anning kneels over a flat grey limestone slab containing a complete nine-foot reptile skeleton with four broad paddles and a long curving neck." + QUAL_TAIL,
             {"kind": "WHEN", "label": "10 DECEMBER 1823", "timeline_step": "4/7 · 10 Dec 1823 (Complete Plesiosaurus)", "hold_s": 3.8}),
            ("02_cuvier_conybeare_buckland_1824", 144.5, 6.5, "C", False, "SUSPECTED A FORGERY", "Quality",
             "Quality: readable faces (Cuvier in Paris, William Conybeare and William Buckland in England).",
             STYLE + "Split period study scene: on the left, Georges Cuvier in Paris peers suspiciously through a magnifying glass at a sketch of a long-necked skeleton; on the right, English geologists William Conybeare and William Buckland trace the unbroken stone seams on the slab." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "William Conybeare & William Buckland", "line_2": "Conybeare (1787–1857) · Buckland (1784–1856)", "fact_card": "Cuvier suspected a forgery", "hold_s": 3.8}),
            ("03_geological_society_1824_hall", 151.0, 6.0, "C", False, "20 FEBRUARY 1824", "Quality",
             "Quality: readable faces in packed London lecture room under chandelier light.",
             STYLE + "Geological Society of London, 20 February 1824: William Conybeare holds up a wide folding drawing of the Plesiosaurus skeleton before tiered rows of gentlemen in dark Regency coats." + QUAL_TAIL,
             {"kind": "WHEN", "label": "LONDON · 20 FEBRUARY 1824", "timeline_step": "5/7 · 20 Feb 1824 (Geological Society)", "hold_s": 3.8}),
            ("04_closed_oak_doors_barred", 157.0, 5.5, "C", False, "BARRED FROM THE ROOM", "Fast",
             "Fast: grey corridor daylight on closed oak doors. Nothing emissive, no readable text on plate.",
             STYLE + "In a quiet stone corridor in grey daylight, tall panelled oak double doors stand firmly shut with a polished brass latch." + FAST_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Stones That Were Ancient Meals",
        [
            ("01_coprolite_cracked_scales_1824", 162.5, 6.0, "B", False, "ANCIENT DROPPINGS", "Fast",
             "Fast: daylight workbench macro of cracked grey stone revealing fish scales. No face, nothing emissive.",
             STYLE + "On a wooden workbench in daylight, a small hammer taps open a twisted grey stone, revealing tiny dark glossy fish scales and fossilised bone fragments locked inside." + FAST_TAIL,
             {"kind": "WHEN", "label": "1824–1829", "timeline_step": "6/7 · 1824–1829 (Coprolites & food chain)", "hold_s": 3.8}),
            ("02_explorer_coprolite_lens", 168.5, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "At the corner of the Lyme Regis workbench, the Explorer peers through his brass magnifying glass at the cracked grey stone, spots a tiny glinting fish scale inside, and recoils with a delighted grin." + EXP_TAIL,
             None),
            ("03_belemnite_fossil_ink_sketch", 174.0, 6.0, "B", False, "FOSSIL INK STILL WROTE", "Quality",
             "Quality: readable face (Mary Anning grinding fossil sepia ink and drawing with quill).",
             STYLE + "At her Lyme Regis table, Mary Anning grinds a dried black fossil ink chamber with a drop of water in a white porcelain dish and dips a quill pen to draw a rich sepia sketch of a fossil skull." + QUAL_TAIL,
             {"kind": "FACT", "label": "FOSSIL INK STILL WROTE", "hold_s": 3.8}),
            ("04_jurassic_food_chain_timeline", 180.0, 8.5, "E", False, "200 MILLION YEARS OLD", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Jurassic food chain (belemnite → fish → small ichthyosaur → 17-ft ichthyosaur) builds above the completed 1796 → 1847 timeline.",
             {"kind": "DATA", "label": "JURASSIC FOOD CHAIN · 1796 → 1847", "detail": "Inked Jurassic food chain and completed 1796 → 1847 timeline", "scale": "200-million-year-old ink still dark enough to draw with", "when_stamp": "9 March 1847", "hold_s": 3.8}),
            ("05_lyme_cliffs_strata_pan", 188.5, 5.5, "A", False, "BLUE LIAS STRATA", "Fast",
             "Fast: daylight pan across Blue Lias rock layers between code graphics so two full-frame graphics never run back to back.",
             STYLE + "In crisp coastal daylight, the camera pans across the alternating horizontal bands of blue-grey limestone and dark shale in the Lyme Regis cliffs." + FAST_TAIL,
             None),
            ("06_land_dinosaur_vs_sea_reptiles", 194.0, 8.0, "E", False, "SEA REPTILES, NOT DINOSAURS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked anatomical comparison contrasts a land dinosaur standing with straight pillar legs beneath its hips on the left against flippered Ichthyosaurus and Plesiosaurus on the right.",
             {"kind": "FACT", "label": "SEA REPTILES, NOT DINOSAURS", "detail": "Inked posture comparison: erect-limbed land dinosaur vs flippered marine reptiles", "hold_s": 3.8}),
            ("07_table_three_callback", 202.0, 2.4, "B", False, None, "reuse",
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
            "film": "014_Anning-Fossils-Extinction",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from anning_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "014_Anning-Fossils-Extinction",
        "version": "v01",
        "written": "2026-10-16",
        "task": "J0397: HOS 014 pre-VO plate boards v01 (from anning_script_master_v01.md + SOURCES_v01.md). Flow-first. Mint nothing. Parked for Chief.",
        "script": "anning_script_master_v01.md (94.0 PASS)",
        "facts_pass": "SOURCES_v01.md (28 rows)",
        "vo_status": "Awaiting Chief script sign-off and long VO recording; rows re-time automatically onto Scribe STT once VO locks.",
        "readings": {
            "flow_credits_left": 23740,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014. Nothing in 014 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 014 Fossils: The 12-Year-Old Girl Who Found Sea Dragons — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 16 Oct 2026, J0397. Built from `anning_script_master_v01.md` (94.0 PASS) and `SOURCES_v01.md`.",
        "**No mint, no spend.** Pre-VO clock timings (`204.4 s` base picture grid; re-times automatically onto Scribe word timestamps once long VO locks).",
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
        "# 014 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 16 Oct 2026, J0397. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `anning_script_master_v01.md` (94.0 PASS) and `SOURCES_v01.md` so 014's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
        "",
        "## Totals (base 30-row board before VO continuation splits)",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Mary Anning, Joseph Anning, Richard Anning, Georges Cuvier, Sir Everard Home, Thomas Birch, William Conybeare, William Buckland), ocean waves/lightning/candlelight scenes, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight and grey-window-light prop and cliff shots (mammoth tusk & globe, fossil ribs in shale, 3-object fossil shop table, curiosity table outside cottage, 4-foot jaw in shale, closed oak doors at Geological Society, cracked coprolite stone, Blue Lias cliff strata). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_17ft_ichthyosaur_rowing_boat` — inked 17-foot (5.2 m) Ichthyosaurus vs family rowing boat scale comparison (`SCALE: seventeen feet long — longer than a family rowing boat`)",
        "  2. `P1:06_35_neck_bones_vs_giraffe` — inked 35 cervical vertebrae in Plesiosaurus vs 7 in a giraffe (`SCALE: five times as many neck bones as a giraffe`)",
        "  3. `P2:05_timeline_1796_1812_23_pounds` — animated timeline (1796 · 1800 · 1810 · 1811–1812) beside £23 coin stack (`SCALE: twenty-three pounds — half a year's labourer wages`)",
        "  4. `P3:02_ichthyosaur_dinner_plate_eye_diagram` — inked anatomy diagram of Ichthyosaurus with bony sclerotic eye ring (`SCALE: eye rings as wide as dinner plates`)",
        "  5. `P5:04_jurassic_food_chain_timeline` — inked Jurassic food chain + completed 1796 → 1847 timeline (`SCALE: 200-million-year-old ink still dark enough to draw with`)",
        "  6. `P5:06_land_dinosaur_vs_sea_reptiles` — inked posture comparison of erect-limbed land dinosaur vs flippered marine reptiles",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:07_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"014 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
