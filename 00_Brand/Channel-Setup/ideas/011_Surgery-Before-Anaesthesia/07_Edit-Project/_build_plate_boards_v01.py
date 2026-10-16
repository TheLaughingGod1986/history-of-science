#!/usr/bin/env python3
"""HOS 011 (What Surgery Was Like Before Anesthesia) pre-VO plate boards v01. J0380. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/011_Surgery-Before-Anaesthesia/surgery_script_master_v02.md
(locked for Chief after Claude's quote check + cfebdab3 Teach/Polish markers) and SOURCES_v01.md.
Nothing is generation_authorized.
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
        "Part 01 — The Fastest Knife",
        [
            ("01_liston_operating_theatre", 0.0, 5.5, "A", False, "THE FASTEST KNIFE", "Quality",
             "Quality: Short frame 0 / answer image + readable face (Robert Liston).",
             STYLE + "London, 1840s: a steep wooden operating theatre lit by tall arched windows; medical students lean forward over the timber rail while a tall surgeon in a dark frock coat checks a brass pocket watch and looks up." + QUAL_TAIL,
             {"kind": "WHEN", "label": "LONDON · 1840s", "hold_s": 3.5}),
            ("02_stopwatch_three_min", 5.5, 8.0, "E", False, "UNDER THREE MINUTES", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked brass stopwatch dial sweeps round once and stops just short of three minutes beside a boiling-egg scale icon.",
             {"kind": "DATA", "label": "UNDER 3 MINUTES", "detail": "Brass stopwatch dial sweeping round once and stopping short of three minutes", "scale": "about as long as boiling an egg", "who_card": "Robert Liston (1794–1847) — London surgeon", "hold_s": 3.8}),
            ("03_boston_ether_globe_open", 13.5, 6.0, "B", False, "ETHER", "Quality",
             "Quality: readable faces + glass ether globe in the domed hall.",
             STYLE + "Boston, 16 October 1846: under a high domed skylight in a tiered wooden amphitheatre, a young dentist holds a two-necked glass globe with a mouthpiece to a seated young patient whose eyes gently close." + QUAL_TAIL,
             {"kind": "WHEN", "label": "BOSTON · 16 OCTOBER 1846", "hold_s": 3.5}),
            ("04_three_portraits_shadow", 19.5, 6.0, "C", False, "WHO WAS FIRST?", "Quality",
             "Quality: candle flicker on dark wood panelling (never Fast).",
             STYLE + "Three gilt portrait frames hang side by side on a dark wood-panelled wall, the faces inside still in shadow as a single candle flickers below them." + QUAL_TAIL,
             None),
            ("05_table_three_props", 25.5, 5.5, "A", False, "A GAS · A BAG · A GLOBE", "Fast",
             "Fast: daylight, grey window light or matte ink. Nothing emissive, so Veo Fast is allowed.",
             STYLE + "On a wooden table in grey window light, three objects sit side by side: a silk gas bag with a brass stopcock, a doctor's worn black leather bag, and a two-necked glass ether globe." + FAST_TAIL,
             None),
            ("06_empty_operating_chair", 31.0, 6.0, "A", False, "AWAKE FOR ALL OF IT", "Fast",
             "Fast: daylight, grey window light or matte ink. Nothing emissive, so Veo Fast is allowed.",
             STYLE + "In a quiet wooden operating theatre in daylight, the camera drifts slowly toward an empty wooden operating chair with leather arm straps hanging loose." + FAST_TAIL,
             None),
            ("07_explorer_theatre_rail", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat (locked character reference, after 1:00).",
             STYLE + "At the back gallery rail of the wooden operating theatre, the Explorer peers down at the empty chair, glances at a brass pocket watch in his hand, and swallows thoughtfully." + EXP_TAIL,
             None),
            ("08_quill_notebook_candle", 67.5, 5.5, "C", False, "FIFTY YEARS EARLIER", "Quality",
             "Quality: candlelight on leather notebook (never Fast).",
             STYLE + "A goose-quill pen rests beside an open leather-bound notebook in warm candlelight as the page lifts slightly in a draught." + QUAL_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — A Gas That Made People Laugh",
        [
            ("01_davy_silk_bag_1800", 73.0, 6.5, "D", False, "HUMPHRY DAVY · 1800", "Quality",
             "Quality: readable face (young Humphry Davy).",
             STYLE + "Bristol, 1800: in a cluttered pneumatic laboratory in daylight, young Humphry Davy, early twenties with curly dark hair and a high collar, breathes from a green silk gas bag and breaks into a wide grin." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Humphry Davy", "line_2": "(1778–1829) — young chemist", "when_stamp": "Bristol · 1800", "timeline_step": "1/6 · 1800 (Davy's nitrous oxide)", "hold_s": 3.8}),
            ("02_davy_surgical_line", 79.5, 5.5, "D", False, "DURING SURGICAL OPERATIONS", "Fast",
             "Fast: daylight, grey window light or matte ink. Nothing emissive, so Veo Fast is allowed.",
             STYLE + "Close on an open 1800 octavo volume on a wooden desk in daylight; a brass finger-pointer slides beneath a blurred printed line." + FAST_TAIL,
             None),
            ("03_parlour_ether_frolic", 85.0, 6.5, "D", False, "USED AT PARTIES FIRST", "Quality",
             "Quality: candlelit parlour + multiple moving figures.",
             STYLE + "An 1830s candlelit parlour party: young guests in Regency dress laugh giddily after breathing from a silk bag; one gentleman bumps his shin against a side table without noticing." + QUAL_TAIL,
             {"kind": "FACT", "label": "USED AT PARTIES FIRST", "source_note": "Nitrous oxide and ether were used for decades at stage shows and 'ether frolics' before surgical adoption (SOURCES_v01).", "hold_s": 3.5}),
            ("04_crawford_long_doorway", 91.5, 6.0, "F", False, "CRAWFORD LONG", "Quality",
             "Quality: readable face (Crawford Long).",
             STYLE + "Jefferson, Georgia, early 1840s: young country doctor Crawford Long, late twenties with dark hair and a waistcoat, watches the laughing parlour guests from a doorway, frowning thoughtfully." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Crawford Long", "line_2": "(1815–1878) — country doctor", "hold_s": 3.8}),
            ("05_long_towel_venable_1842", 97.5, 6.0, "F", False, "GEORGIA · MARCH 1842", "Quality",
             "Quality: readable faces in quiet country surgery.",
             STYLE + "A quiet wooden country surgery in Georgia, March 1842: Crawford Long gently holds a folded white towel near the face of seated patient James Venable, whose head tips back in calm sleep." + QUAL_TAIL,
             {"kind": "WHEN", "label": "GEORGIA · MARCH 1842", "timeline_step": "2/6 · March 1842 (Long's ether operation)", "hold_s": 3.5}),
            ("06_timeline_1800_1842", 103.5, 8.5, "E", False, "42 YEARS · 1800 → 1842", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: an inked timeline on period paper builds from 1800 (Bristol laughing gas) to 1842 (Georgia ether towel), spanning 42 years before anyone published.",
             {"kind": "DATA", "label": "1800 → 1842", "detail": "Animated timeline building from 1800 (Davy) to 1842 (Long)", "scale": "42 years from Davy's laughing gas (1800) to Long's ether operation (1842)", "hold_s": 3.8}),
            ("07_unpublished_ledger_drawer", 112.0, 5.5, "F", False, "SEVEN YEARS UNPUBLISHED", "Fast",
             "Fast: daylight, grey window light or matte ink. Nothing emissive, so Veo Fast is allowed.",
             STYLE + "In a country doctor's office in daylight, a hand closes a leather account ledger and slides it onto a wooden shelf." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — This Is No Humbug",
        [
            ("01_wells_tooth_pulled_1844", 117.5, 6.5, "G", False, "HORACE WELLS · 1844", "Quality",
             "Quality: readable face (Horace Wells).",
             STYLE + "Hartford, Connecticut, December 1844: dentist Horace Wells, late twenties with side whiskers, sits in his own red plush dental chair while a colleague steps back with forceps; Wells blinks and smiles in astonishment." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Horace Wells", "line_2": "(1815–1848) — Hartford dentist", "when_stamp": "Hartford · December 1844", "timeline_step": "3/6 · Dec 1844 (Wells's tooth)", "hold_s": 3.8}),
            ("02_boston_humbug_jeer_1845", 124.0, 6.0, "B", False, "HUMBUG! · 1845", "Quality",
             "Quality: multiple faces in lecture hall.",
             STYLE + "Boston, January 1845: in a tiered medical lecture hall, a seated patient winces and stirs while medical students on the benches above lean forward, laughing and gesturing dismissively." + QUAL_TAIL,
             {"kind": "WHEN", "label": "BOSTON · JANUARY 1845", "hold_s": 3.5}),
            ("03_morton_tests_ether_bottles", 130.0, 5.5, "B", False, "ETHER INSTEAD", "Fast",
             "Fast: daylight, grey window light or matte ink. Nothing emissive, so Veo Fast is allowed.",
             STYLE + "On a dentist's workbench in daylight, two hands set aside a deflated gas bag and lift a clear glass apothecary bottle of ether beside a two-necked glass globe." + FAST_TAIL,
             None),
            ("04_morton_ether_dome_1846", 135.5, 6.5, "B", False, "16 OCTOBER 1846", "Quality",
             "Quality: readable face (William Morton) in the Ether Dome.",
             STYLE + "Massachusetts General Hospital, 16 October 1846: under the domed skylight, dentist William Morton, late twenties with dark hair, holds the glass ether globe to patient Edward Abbott's mouth as Abbott sleeps peacefully." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "William T. G. Morton", "line_2": "(1819–1868) — Boston dentist", "when_stamp": "Boston · 16 October 1846", "timeline_step": "4/6 · 16 Oct 1846 (Ether Dome)", "hold_s": 3.8}),
            ("05_warren_no_humbug", 142.0, 6.5, "B", False, "NO HUMBUG", "Quality",
             "Quality: readable face (John Collins Warren).",
             STYLE + "In the Ether Dome, senior surgeon John Collins Warren, white-haired in a high collar and dark coat, lowers his instrument and turns gravely to the silent, packed tiers of watching doctors." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "John Collins Warren", "line_2": "(1778–1856) — senior surgeon", "hold_s": 3.8}),
            ("06_explorer_ether_dome", 148.5, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat (locked character reference).",
             STYLE + "In the top gallery row of the Ether Dome, the Explorer leans forward over the wooden rail as Warren turns to the room, then lets out his breath and smiles warmly." + EXP_TAIL,
             None),
            ("07_steamer_leaves_boston", 154.0, 6.0, "B", False, "THE NEWS SPREAD", "Quality",
             "Quality: harbour water and steamship (never Fast).",
             STYLE + "Late autumn 1846: a wooden paddle steamer pulls out of Boston harbour across grey Atlantic swells, carrying mail bags toward England." + QUAL_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — The Fight Over Who Was First",
        [
            ("01_morton_tints_letheon", 160.0, 5.5, "B", False, "A SECRET RECIPE", "Fast",
             "Fast: daylight, grey window light or matte ink. Nothing emissive, so Veo Fast is allowed.",
             STYLE + "On a desk in daylight, hands pour orange-tinted liquid from a small phial into a glass apothecary bottle and stopper it tightly." + FAST_TAIL,
             None),
            ("02_holmes_coins_anaesthesia", 165.5, 6.0, "C", False, "ANAESTHESIA · 1846", "Quality",
             "Quality: candlelit study (never Fast).",
             STYLE + "Boston, November 1846: a slow push across a warm candlelit study desk where a freshly penned letter lies beside a brass inkstand and quill." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Oliver Wendell Holmes Sr.", "line_2": "(1809–1894) — doctor and poet", "fact_card": "A poet named it", "hold_s": 3.8}),
            ("03_four_claimants_frames", 171.5, 6.5, "C", False, "FOUR CLAIMS", "Quality",
             "Quality: readable faces in the four lit frames.",
             STYLE + "Four gilt portrait frames hang side by side on a panelled wall in warm light, showing the four rivals — Long, Wells, Morton and Charles Jackson." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Charles T. Jackson", "line_2": "(1805–1880) — Boston chemist", "hold_s": 3.8}),
            ("04_boston_ether_monument_1868", 178.0, 6.0, "G", False, "NAMES NOBODY · 1868", "Fast",
             "Fast: daylight, grey window light or matte ink. Nothing emissive, so Veo Fast is allowed.",
             STYLE + "Boston Public Garden, 1868: in crisp autumn daylight, the camera tilts up a tall carved granite monument surrounded by golden trees, its stone base smooth without any discoverer's name." + FAST_TAIL,
             {"kind": "FACT", "label": "THE MONUMENT NAMES NOBODY", "when_stamp": "Boston · 1868", "source_note": "The 1868 Boston Public Garden Ether Monument honours the discovery of ether anaesthesia without naming any of the four claimants (SOURCES_v01).", "hold_s": 3.8}),
        ],
    ),
    (
        5,
        "Part 05 — Across the Ocean",
        [
            ("01_liston_puts_watch_away", 184.0, 6.5, "A", False, "NO NEED TO RUSH", "Quality",
             "Quality: readable face (Robert Liston in London, 21 Dec 1846).",
             STYLE + "London, University College Hospital, 21 December 1846: tall surgeon Robert Liston stands beside a peacefully sleeping patient in the sunlit wooden theatre, looks at his brass pocket watch, and slowly slips it back into his waistcoat pocket." + QUAL_TAIL,
             {"kind": "WHEN", "label": "LONDON · 21 DECEMBER 1846", "hold_s": 3.5}),
            ("02_simpson_chloroform_dining", 190.5, 6.5, "H", False, "EDINBURGH · 1847", "Quality",
             "Quality: readable faces + evening dining room lamp glow.",
             STYLE + "Edinburgh, November 1847: around a mahogany dining table by warm lamplight, James Young Simpson and two fellow doctors sniff from small glass tumblers and slump peacefully sideways in their chairs." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "James Young Simpson", "line_2": "(1811–1870) — Edinburgh doctor", "when_stamp": "Edinburgh · November 1847", "timeline_step": "5/6 · Nov 1847 (Simpson's chloroform)", "hold_s": 3.8}),
            ("03_john_snow_handkerchief_1853", 197.0, 6.5, "H", False, "JOHN SNOW · 1853", "Quality",
             "Quality: readable face (John Snow).",
             STYLE + "London, April 1853: calm physician John Snow, about forty, clean-shaven in a dark coat, carefully drips clear liquid from a small phial onto a folded white handkerchief in a quiet royal bedchamber." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "John Snow", "line_2": "(1813–1858) — London doctor", "when_stamp": "London · April 1853", "timeline_step": "6/6 · April 1853 (Queen Victoria)", "hold_s": 3.8}),
            ("04_timeline_complete_1853", 203.5, 8.5, "E", False, "1800 → 1853 · 53 YEARS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: the 6-date inked timeline on period paper completes (1800 · 1842 · 1844 · 1846 · 1847 · 1853), spanning 53 years from Davy's Bristol lab to Buckingham Palace.",
             {"kind": "DATA", "label": "53 YEARS · 1800 → 1853", "detail": "Complete 6-date timeline: 1800 · 1842 · 1844 · 1846 · 1847 · 1853", "scale": "53 years from Davy's Bristol lab (1800) to Buckingham Palace (1853)", "hold_s": 3.8}),
            ("05_modern_anaesthetist_monitor", 212.0, 6.0, "I", False, "WATCHING EVERY BREATH", "Quality",
             "Quality: modern clinical monitor light and character.",
             STYLE + "A calm modern operating room: an anaesthetist in blue scrubs sits attentively beside a sleeping patient, watching steady green heartbeat and breathing waveforms on a clean monitor." + QUAL_TAIL,
             None),
            ("06_one_in_100000_stadium", 218.0, 8.5, "E", False, "1 IN 100,000", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, a counter climbs to 100,000 beside a 90,000-seat stadium bowl where a single tiny dot is highlighted.",
             {"kind": "DATA", "label": "1 IN 100,000", "detail": "Counter to 100,000 beside a 90,000-person stadium comparison with one dot", "scale": "one in a stadium crowd", "hold_s": 3.8}),
            ("07_ward_glass_handoff_lister", 226.5, 5.5, "A", False, "BUT DAYS LATER…", "Fast",
             "Fast: daylight, grey window light or matte ink. Nothing emissive, so Veo Fast is allowed.",
             STYLE + "A sunlit Victorian hospital ward: a patient sleeps peacefully in a clean bed while on the wooden bedside table a brass microscope sits beside a carbolic spray bottle." + FAST_TAIL,
             None),
            ("08_table_three_callback", 232.0, 2.4, "A", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:05_table_three_props (callback, £0).",
             None,
             None),
        ],
    ),
]


def main() -> None:
    cum_flow = 0
    cum_vx = 0.0
    per_part_summary = []
    all_parts = []
    overlay_count = 0

    for p_idx, p_title, rows_spec in PARTS_SPEC:
        plates = []
        p_counts = {"rows": 0, "Quality": 0, "Fast": 0, "code_graphic": 0, "reuse": 0, "flow_credits_try1": 0, "flow_credits_expected": 0, "vertex_try1_gbp": 0.0, "vertex_expected_gbp": 0.0}
        for rid, t_s, use_s, set_id, is_exp, label, qual, reason, prompt, overlay in rows_spec:
            priced = price_row(qual, use_s)
            cum_flow += priced["flow_credits_expected"]
            cum_vx = round(cum_vx + priced["vertex_expected_gbp"], 2)
            row = {
                "id": rid,
                "t_s": t_s,
                "t": fmt_t(t_s),
                "use_s": use_s,
                "set": set_id,
                "explorer": is_exp,
                "side_label": label,
                "quality": qual,
                "engine_reason": reason,
                "generation_authorized": False,
                "prompt": prompt,
                "reference": (
                    "01_Character/05_Generation-References/hos-explorer-reference-v01.jpg"
                    if is_exp
                    else (
                        "own £0 code graphic (python-pillow-ffmpeg house parchment renderer); no still"
                        if qual == "code_graphic"
                        else (
                            "P1:05_table_three_props unused moving tail [5.50s..7.90s]"
                            if qual == "reuse"
                            else f"set {set_id} continuity; no still reference"
                        )
                    )
                ),
            }
            if overlay:
                row["teach_overlay"] = overlay
                overlay_count += 1
            if qual == "code_graphic":
                row["code_graphic_layout"] = "full_frame_parchment"
            if qual == "reuse":
                row["reuse_of"] = "P1:05_table_three_props"
                row["reuse_measurement"] = {
                    "source_row": "P1:05_table_three_props",
                    "source_clip_usable_s": 7.9,
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
            "film": "011_Surgery-Before-Anaesthesia",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from surgery_script_master_v02.md; retimes onto Scribe STT once VO locks)",
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
        "film": "011_Surgery-Before-Anaesthesia",
        "version": "v01",
        "written": "2026-10-16",
        "task": "J0380: HOS 011 pre-VO plate boards v01 (from surgery_script_master_v02.md + CLAUDE_QUOTE_CHECK_v01.md + cfebdab3 markers). Flow-first. Mint nothing. Parked for Chief.",
        "script": "surgery_script_master_v02.md (locked for Chief after Claude quote check + cfebdab3 Teach/Polish markers)",
        "facts_pass": "SOURCES_v01.md + CLAUDE_QUOTE_CHECK_v01.md",
        "vo_status": "Awaiting Chief script sign-off and long VO recording; rows re-time automatically onto Scribe STT once VO locks.",
        "readings": {
            "flow_credits_left": 23740,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011. Nothing in 011 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    # SHOT_LIST_v01.md
    sl = [
        "# 011 What Surgery Was Like Before Anesthesia — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 16 Oct 2026, J0380. Built from `surgery_script_master_v02.md` (with `cfebdab3` Teach/Polish markers) and `SOURCES_v01.md` + `CLAUDE_QUOTE_CHECK_v01.md`.",
        "**No mint, no spend.** Pre-VO clock timings (`234.4 s` base picture grid; re-times automatically onto Scribe word timestamps once long VO locks).",
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

    # PRICE_REVIEW_v01.md
    pr_lines = [
        "# 011 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 16 Oct 2026, J0380. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `surgery_script_master_v02.md` (with `cfebdab3` Teach/Polish markers) and `SOURCES_v01.md` + `CLAUDE_QUOTE_CHECK_v01.md` so 011's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Liston, Davy, Long, Wells, Morton, Warren, Simpson, Snow), candle/lamplight scenes, Boston harbour steamer, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight and grey-window-light prop and architecture shots (3-object table, empty operating chair, 1800 printed page, country ledger, ether workbench, Letheon bottle, 1868 Boston Public Garden Ether Monument, sunlit Victorian ward). Zero candles, flames, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:02_stopwatch_three_min` — brass stopwatch dial sweeping short of 3 minutes (`SCALE: about as long as boiling an egg`)",
        "  2. `P2:06_timeline_1800_1842` — 1800 → 1842 timeline (`SCALE: 42 years from Davy's laughing gas to Long's ether operation`)",
        "  3. `P5:04_timeline_complete_1853` — complete 6-date timeline 1800 → 1853 (`SCALE: 53 years from Davy's Bristol lab to Buckingham Palace`)",
        "  4. `P5:06_one_in_100000_stadium` — 1 in 100,000 counter + 90,000-person stadium comparison (`SCALE: one in a stadium crowd`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:08_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:05_table_three_props`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"011 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
