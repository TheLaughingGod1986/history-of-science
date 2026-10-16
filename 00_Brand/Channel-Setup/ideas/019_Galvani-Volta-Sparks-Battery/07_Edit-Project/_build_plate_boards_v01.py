#!/usr/bin/env python3
"""HOS 019 (The First Battery: How a Twitching Frog Leg Changed the World) pre-VO plate boards v01. J0430. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/019_Galvani-Volta-Sparks-Battery/galvani_script_master_v01.md
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
        "Part 01 — The Kick on the Balcony",
        [
            ("01_bologna_balcony_frog_hook_spark_to_pile", 0.0, 5.5, "A", False, "THE KICK ON THE BALCONY", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + electric contact spark as brass hook touches iron balcony railing and dissolves to Voltaic coin pile.",
             STYLE + "Bologna, Italy, 20 September 1786: on a sunlit stone balcony, a dissected frog leg hangs from a curved brass hook; the instant the brass hook swings against the black iron railing, a tiny blue-gold spark snaps at the contact point and the frog's leg kicks sharply upward, dissolving into a tall column of stacked silver and zinc discs soaked in salt water." + QUAL_TAIL,
             {"kind": "WHEN", "label": "BOLOGNA · 20 SEPTEMBER 1786", "timeline_step": "2/7 · 20 Sep 1786 (Brass hook on iron balcony)", "hold_s": 3.5}),
            ("02_two_rivals_galvani_and_volta", 5.5, 6.0, "B", False, "TWO RIVALS, TWO TRUTHS", "Quality",
             "Quality: readable faces (Luigi and Lucia Galvani in Bologna; Alessandro Volta in Pavia).",
             STYLE + "Split period composition: on the left in Bologna, Luigi and Lucia Galvani touch a brass hook and steel scalpel to a frog nerve on an anatomy table; on the right in Pavia, Alessandro Volta stacks alternating silver and zinc discs separated by brine-soaked cardboard." + QUAL_TAIL,
             None),
            ("03_leyden_jar_and_nerve_drawing", 11.5, 6.0, "C", False, "SPIRITS OR SPARKS?", "Quality",
             "Quality: electrostatic discharge flash from glass Leyden jar beside an eighteenth-century anatomical nerve illustration.",
             STYLE + "In a darkened eighteenth-century cabinet, a glass Leyden jar with a brass rod discharges a brief blue electric flash beside a parchment anatomical drawing of human arm nerves." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1780S", "hold_s": 3.5}),
            ("04_volta_pile_vs_neuron_action_potential_chart", 17.5, 8.0, "E", False, "30 PAIRS (~30 V) VS -70 MV NERVE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked comparison shows Volta's March 1800 bimetallic pile of 30 silver-and-zinc pairs (~1 V per pair, continuous current) alongside a single human neuron firing a -70 mV to +40 mV (110 mV) action potential.",
             {"kind": "DATA", "label": "30 PAIRS (~1 V EACH) · -70 MV TO +40 MV NERVE", "detail": "Inked comparison of Volta's 1800 silver-zinc pile (~1 V per cell pair, 30 pairs continuous current) vs the nerve action potential inside living muscle and brain cells (-70 mV resting to +40 mV peak, 110 mV swing)", "scale": "70 millivolts across a nerve membrane — a tiny voltage, yet across a cell wall so thin that its electric field is stronger than a lightning bolt", "who_card": "Luigi Galvani (1737–1798) — Bolognese physician & anatomist · Lucia Galeazzi Galvani (1743–1788) — Bolognese anatomy experimenter · Alessandro Volta (1745–1827) — Pavia physics professor", "when_stamp": "20 September 1786 · 20 March 1800", "hold_s": 3.8}),
            ("05_bologna_workbench_brass_hook_and_coins_pan", 25.5, 5.5, "A", False, "BIMETALLIC ARC", "Fast",
             "Fast: daylight pan across Bolognese wooden table with curved brass hooks, iron plate, and silver/zinc discs between code graphics so two full-frame graphics never run back to back.",
             STYLE + "In soft daylight, the camera tracks across a wooden anatomy workbench holding curved brass hooks, a flat iron plate, and stacked silver and zinc discs beside a bowl of salt water." + FAST_TAIL,
             None),
            ("06_brain_86b_neurons_20w_scale_chart", 31.0, 8.0, "E", False, "20 WATTS IN YOUR HEAD", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked human nervous-system scale shows 86 billion brain neurons firing nerve impulses at up to 120 metres per second (270 mph) while drawing just 20 watts of total electrical power.",
             {"kind": "DATA", "label": "86 BILLION NEURONS · 270 MPH · 20 WATTS", "detail": "Inked human nervous-system scale showing 86 billion neurons firing at up to 120 m/s (270 mph) on 20 watts of total power", "scale": "86 billion neurons running on 20 watts — less power than the dim bulb inside your refrigerator", "hold_s": 3.8}),
            ("07_table_three_props_hook_pile_glass_knife", 39.0, 5.5, "C", False, "BOLOGNA, 1786", "Fast",
             "Fast: daylight prop table (callback source for Part 05: curved brass hook on iron bar, stack of silver/zinc coins, curved glass dissection knife). Nothing emissive.",
             STYLE + "On a sunlit wooden workbench in Bologna sit three objects side by side: a curved brass hook resting on an iron bar, a tall stack of silver and zinc discs, and a transparent curved glass dissection knife." + FAST_TAIL,
             None),
            ("08_explorer_bologna_bimetallic_fork", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing on the wooden workbench in Bologna beside the brass conductor rod, the Explorer touches a tiny bimetallic fork of copper and silver to a drop of salt water, feels its metal antenna tingle with a gentle buzz, and steps back in surprise." + EXP_TAIL,
             None),
            ("09_spinning_glass_globe_to_calm_balcony_sky", 67.5, 5.5, "B", False, "NO STORM IN THE SKY", "Fast",
             "Fast: daylight transition from unlit glass friction globe and brass chain on wooden table out to a calm, clear blue autumn sky over the Bologna iron balcony railing. Nothing emissive.",
             STYLE + "In warm afternoon daylight, the camera moves past a stationary glass globe machine with brass chains on a wooden table out through open French doors to a calm, cloudless blue sky above a black iron garden balcony railing." + FAST_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — The Scalpel Spark and the Iron Balcony",
        [
            ("01_luigi_and_lucia_scalpel_spark_1780", 85.0, 6.5, "A", False, "BOLOGNA · 6 NOVEMBER 1780", "Quality",
             "Quality: readable faces (Luigi Galvani and Lucia Galeazzi Galvani) + electrostatic spark jumping across the table as steel scalpel touches frog nerve.",
             STYLE + "Bologna, Italy, 6 November 1780: in their home laboratory, Luigi Galvani in powdered wig and dark coat and Lucia Galeazzi Galvani in a silk dress holding an open notebook watch an assistant touch the crural nerve of a dissected frog leg with a steel scalpel just as a blue spark jumps from a distant electrostatic machine across the table." + QUAL_TAIL,
             {"kind": "FACT", "label": "Lucia spotted the first spark", "when_stamp": "Bologna, 6 November 1780", "timeline_step": "1/7 · 6 Nov 1780 (Galvani & Lucia's scalpel spark)", "hold_s": 3.8}),
            ("02_brass_hooks_on_iron_balcony_1786", 91.5, 6.0, "B", False, "BRASS ON IRON", "Fast",
             "Fast: calm clear evening daylight on stone balcony, close-up of gloved hands pressing curved brass hook against black iron railing as frog leg kicks. No face, no spark.",
             STYLE + "On a calm, clear autumn evening on a stone garden balcony in Bologna, gloved hands press a curved brass hook holding a prepared frog leg against a black wrought-iron railing bar, and the leg kicks sharply upward." + FAST_TAIL,
             {"kind": "WHEN", "label": "20 SEPTEMBER 1786", "hold_s": 3.5}),
            ("03_biological_leyden_jar_30ms_diagram", 97.5, 8.0, "E", False, "ANIMAL ELECTRICITY?", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked comparison shows Galvani's 1791 biological Leyden jar model (muscle storing internal animal electricity discharged through the nerve at 30 metres per second) beside a glass Leyden jar.",
             {"kind": "DATA", "label": "30 M/S FROG NERVE · <2 MILLISECONDS", "detail": "Inked comparison diagram of Galvani's 1791 biological Leyden jar model (nerve and muscle storing internal animal electricity) and frog sciatic nerve conduction at 30 metres per second", "scale": "30 metres per second in a frog nerve — crossing the entire leg in less than two-thousandths of a second", "when_stamp": "1791", "timeline_step": "3/7 · 1791 (Galvani's animal electricity commentary)", "hold_s": 3.8}),
            ("04_de_viribus_1791_commentary_plates", 105.5, 5.5, "C", False, "PUBLISHED IN 1791", "Fast",
             "Fast: daylight close-up of copperplate engraving illustrations of frog preparations, Leyden jar and electrostatic machine on a wooden desk. Nothing emissive.",
             STYLE + "In soft window light on a wooden study desk, folded copperplate engravings showing frog legs, brass arcs, and a glass Leyden jar lie open beside brass dividers and a quill pen." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — The Coin on the Tongue and the Pile of Metal",
        [
            ("01_volta_pavia_coin_on_tongue_1792", 111.0, 6.5, "A", False, "PAVIA · 1792", "Quality",
             "Quality: readable face (Alessandro Volta at University of Pavia placing tin strip and silver coin on his tongue).",
             STYLE + "University of Pavia, 1792: physics professor Alessandro Volta in a curled wig and burgundy coat leans over his laboratory table, places a strip of shiny tin on the tip of his tongue and a silver spoon further back, and touches their outer ends together with a startled wince at the sour electrical taste." + QUAL_TAIL,
             {"kind": "FACT", "label": "Tested coins on his tongue", "when_stamp": "Pavia, 1792", "hold_s": 3.8}),
            ("02_volta_stacking_pile_and_banks_letter_1800", 117.5, 6.5, "B", False, "THE FIRST BATTERY", "Quality",
             "Quality: readable faces (Alessandro Volta in Como stacking 30 silver-zinc pairs; Sir Joseph Banks at the Royal Society in London).",
             STYLE + "Como, March 1800: Alessandro Volta carefully stacks thirty alternating circular discs of silver and zinc separated by salt-water-soaked pasteboard discs between glass rods, while in London Royal Society President Sir Joseph Banks holds Volta's French letter." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Joseph Banks", "line_2": "(1743–1820) — Royal Society president", "when_stamp": "20 March 1800 · 26 June 1800", "timeline_step": "5/7 · 20 Mar 1800 (Volta's battery letter)", "hold_s": 3.8}),
            ("03_voltaic_pile_cutaway_30_pairs_diagram", 124.0, 8.0, "E", False, "30 PAIRS · ~1 VOLT EACH", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked cutaway diagram of Volta's March 1800 Voltaic pile shows 30 alternating pairs of silver (Ag) and zinc (Zn) discs separated by brine-soaked cardboard discs, generating ~1 volt per cell pair (~30 volts total continuous current).",
             {"kind": "DATA", "label": "30 AG/ZN PAIRS · ~1 V PER PAIR (~30 V CONTINUOUS)", "detail": "Inked cutaway diagram of Volta's March 1800 Voltaic pile of 30 alternating silver (Ag) and zinc (Zn) pairs separated by brine-soaked cardboard, producing ~0.76 to 1.1 volts per pair (~30 volts continuous current)", "scale": "1 volt per silver-zinc pair — stack 30 pairs and you feel a sharp electric shock in wet hands that flows continuously instead of vanishing in one spark", "hold_s": 3.8}),
            ("04_torpedo_ray_and_crown_of_cups_bench", 132.0, 5.5, "C", False, "CONTINUOUS CURRENT", "Fast",
             "Fast: daylight workbench shot of Volta's 'crown of cups' (glass goblets filled with salt water linked by copper-zinc metallic arcs) beside a naturalist drawing of an electric torpedo ray. Nothing emissive.",
             STYLE + "In daylight on a wooden laboratory bench, a circle of glass goblets filled with brine linked by curved copper-and-zinc arcs sits beside an eighteenth-century naturalist illustration of an electric torpedo fish." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — The Metal-Free Twitch and the Corpse That Opened Its Eyes",
        [
            ("01_galvani_aldini_glass_knife_zero_metal_1794", 137.5, 6.5, "A", False, "ZERO METAL · 1794", "Quality",
             "Quality: readable faces (Luigi Galvani and nephew Giovanni Aldini in Bologna using a glass knife to drape bare frog nerve onto muscle with zero metal).",
             STYLE + "Bologna, 1794: Luigi Galvani and his nephew Giovanni Aldini in a dark frock coat use a transparent glass knife to lift a bare frog sciatic nerve and drop it directly onto a second frog muscle on a glass plate with no metal anywhere; the muscle kicks sharply." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Giovanni Aldini", "line_2": "(1762–1834) — Bolognese physics professor", "fact_card": "Kicked with zero metal", "when_stamp": "Bologna, 1794 · 1797", "timeline_step": "4/7 · 1794 (Galvani's metal-free nerve twitch)", "hold_s": 3.8}),
            ("02_aldini_london_1803_and_mary_shelley_1818", 144.0, 6.5, "B", False, "SPARKING FRANKENSTEIN", "Quality",
             "Quality: readable faces + candlelit gothic writing scene (Giovanni Aldini with 120-plate trough battery at Royal College of Surgeons in 1803; young Mary Shelley writing Frankenstein by candlelight in 1818).",
             STYLE + "Split period scene: on the left in London (17 January 1803), Giovanni Aldini holds conducting rods from a 120-plate zinc-and-copper trough battery in an anatomical theatre; on the right by warm candlelight (1818), young Mary Shelley writes with a quill pen at a wooden desk." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Mary Shelley", "line_2": "(1797–1851) — English gothic novelist", "when_stamp": "London, 17 January 1803 · 1818", "timeline_step": "6/7 · 17 Jan 1803 (Aldini's London demonstration)", "hold_s": 3.8}),
            ("03_du_bois_reymond_action_potential_1848_diagram", 150.5, 8.0, "E", False, "-70 MV TO +40 MV IN 1 MS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, Emil du Bois-Reymond's 1848 multi-turn coil galvanometer trace sits beside an inked neuron membrane diagram showing sodium (Na+) and potassium (K+) ions flipping the membrane voltage from -70 mV to +40 mV (110 mV swing in 1 millisecond).",
             {"kind": "DATA", "label": "-70 MV TO +40 MV (110 MV SWING IN 1 MS)", "detail": "Inked nerve-membrane diagram showing sodium (Na+) and potassium (K+) ions rushing across a neuron membrane to flip the voltage from -70 mV to +40 mV (the action potential measured by du Bois-Reymond in 1848)", "scale": "-70 millivolts to +40 millivolts in one millisecond — firing up to 1,000 times a second along your nerves", "who_card": "Emil du Bois-Reymond (1818–1896) — German electrophysiologist", "when_stamp": "Berlin, 1848", "timeline_step": "7/7 · 1848 (du Bois-Reymond measures the nerve impulse)", "hold_s": 3.8}),
            ("04_explorer_berlin_galvanometer_salute", 158.5, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside du Bois-Reymond's multi-thousand-turn coil galvanometer in Berlin, the Explorer watches the suspended magnetic needle swing briskly as a nerve fires, then looks from Volta's coin pile to the nerve trace and gives a two-handed salute to both." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Your Brain Runs on Salt Water and the Twitching Compass",
        [
            ("01_timeline_1780_1848_and_axon_dominoes", 164.0, 8.5, "E", False, "120 M/S (270 MPH) · DOMINO WAVE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 7-date timeline completes: 6 Nov 1780 (Scalpel spark) · 20 Sep 1786 (Iron balcony) · 1791 (Animal electricity) · 1794 (Metal-free twitch) · 20 Mar 1800 (Volta's battery) · 17 Jan 1803 (Aldini London) · 1848 (du Bois-Reymond nerve pulse), alongside an inked falling-dominoes diagram of Na+/K+ ion gates regenerating a 110 mV pulse at up to 120 m/s (270 mph).",
             {"kind": "DATA", "label": "120 M/S (270 MPH) · 1780 → 1848 TIMELINE", "detail": "Animated 7-date timeline (1780 → 1848) alongside an inked axon domino diagram showing Na+/K+ ion gates regenerating a 110 mV pulse at up to 120 metres per second (270 mph)", "scale": "120 metres per second (270 mph) — a nerve signal races from your toe to your brain in less than a fiftieth of a second", "fact_card": "Nerves fire like dominoes", "when_stamp": "1780–1848", "hold_s": 3.8}),
            ("02_water_electrolysis_bubbles_may_1800", 172.5, 6.0, "A", False, "EVERY HEARTBEAT, EVERY PHONE", "Fast",
             "Fast: daylight laboratory glass tube where streams of tiny hydrogen and oxygen bubbles rise from two brass wires connected to a Voltaic pile beside a modern cylindrical battery cell. Nothing emissive.",
             STYLE + "In bright daylight on a laboratory bench, streams of tiny gas bubbles rise from two brass wires submerged in a glass water tube connected to a Voltaic coin pile, transitioning smoothly to a sleek modern battery cell." + FAST_TAIL,
             {"kind": "WHEN", "label": "MAY 1800", "hold_s": 3.5}),
            ("03_copenhagen_compass_twitch_handoff_1820", 178.5, 6.5, "C", False, "THE COMPASS TWITCHES", "Quality",
             "Quality: candlelit Copenhagen lecture hall + readable face of Danish professor Hans Christian Ørsted watching compass needle jerk sideways under a battery wire (handoff to 021 Faraday/Ørsted).",
             STYLE + "Copenhagen, 21 April 1820: in a candlelit lecture hall, Danish physics professor Hans Christian Ørsted connects a platinum wire to a Voltaic battery pile directly above a glass-enclosed magnetic compass needle, and watches in astonishment as the needle jerks ninety degrees sideways." + QUAL_TAIL,
             {"kind": "WHEN", "label": "COPENHAGEN · 21 APRIL 1820", "hold_s": 3.5}),
            ("04_table_three_callback", 185.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_hook_pile_glass_knife (callback, £0).",
             "Reuse P1:07_table_three_props_hook_pile_glass_knife [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_hook_pile_glass_knife"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_hook_pile_glass_knife",
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
            "film": "019_Galvani-Volta-Sparks-Battery",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from galvani_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "019_Galvani-Volta-Sparks-Battery",
        "version": "v01",
        "written": "2026-10-17",
        "task": "J0430: HOS 019 pre-VO plate boards v01 (from galvani_script_master_v01.md + SOURCES_v01.md). Flow-first. Mint nothing. Parked for Chief.",
        "script": "galvani_script_master_v01.md (91.9 PASS)",
        "facts_pass": "SOURCES_v01.md (10 rows)",
        "vo_status": "Awaiting Chief script sign-off and long VO recording; rows re-time automatically onto Scribe STT once VO locks.",
        "readings": {
            "flow_credits_left": 23740,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019. Nothing in 019 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 019 The First Battery: How a Twitching Frog Leg Changed the World — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 17 Oct 2026, J0430. Built from `galvani_script_master_v01.md` (91.9 PASS) and `SOURCES_v01.md`.",
        "**No mint, no spend.** Pre-VO clock timings (`187.4 s` base picture grid; re-times automatically onto Scribe word timestamps once long VO locks).",
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
        "# 019 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 17 Oct 2026, J0430. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `galvani_script_master_v01.md` (91.9 PASS) and `SOURCES_v01.md` so 019's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Luigi Galvani, Lucia Galeazzi Galvani, Alessandro Volta, Sir Joseph Banks, Giovanni Aldini, Mary Shelley, Hans Christian Ørsted), emissive/spark/candlelight scenes (balcony contact spark, Leyden jar flash, 1780 scalpel spark, 1818 Frankenstein candlelight, 1820 Copenhagen lecture hall), and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (Bologna bimetallic workbench, 3-object callback table, stationary friction globe to clear balcony sky, brass hooks on iron railing, 1791 *De Viribus* copperplates, Volta's crown of cups & torpedo ray drawing, May 1800 water electrolysis bubbles). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_volta_pile_vs_neuron_action_potential_chart` — Volta's 1800 silver-zinc pile (30 pairs, ~1 V per pair) vs living neuron action potential (-70 mV to +40 mV, 110 mV swing) (`SCALE: 70 millivolts across a nerve membrane — a tiny voltage, yet across a cell wall so thin that its electric field is stronger than a lightning bolt`)",
        "  2. `P1:06_brain_86b_neurons_20w_scale_chart` — 86 billion brain neurons firing at up to 120 m/s (270 mph) on 20 W total power (`SCALE: 86 billion neurons running on 20 watts — less power than the dim bulb inside your refrigerator`)",
        "  3. `P2:03_biological_leyden_jar_30ms_diagram` — Galvani's 1791 biological Leyden jar model and frog sciatic nerve conduction at 30 m/s (`SCALE: 30 metres per second in a frog nerve — crossing the entire leg in less than two-thousandths of a second`)",
        "  4. `P3:03_voltaic_pile_cutaway_30_pairs_diagram` — cutaway diagram of Volta's March 1800 30-pair Ag/Zn pile (~1 V/pair, ~30 V continuous current) (`SCALE: 1 volt per silver-zinc pair — stack 30 pairs and you feel a sharp electric shock in wet hands that flows continuously instead of vanishing in one spark`)",
        "  5. `P4:03_du_bois_reymond_action_potential_1848_diagram` — du Bois-Reymond's 1848 galvanometer trace + Na+/K+ membrane flip (-70 mV to +40 mV in 1 ms) (`SCALE: -70 millivolts to +40 millivolts in one millisecond — firing up to 1,000 times a second along your nerves`)",
        "  6. `P5:01_timeline_1780_1848_and_axon_dominoes` — completed 7-date timeline (1780 → 1848) + 120 m/s (270 mph) falling-dominoes axon diagram (`SCALE: 120 metres per second (270 mph) — a nerve signal races from your toe to your brain in less than a fiftieth of a second`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_hook_pile_glass_knife`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"019 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
