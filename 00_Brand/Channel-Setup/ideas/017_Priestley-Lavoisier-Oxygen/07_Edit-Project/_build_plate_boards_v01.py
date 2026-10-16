#!/usr/bin/env python3
"""HOS 017 (Oxygen: The Bell-Jar Experiment That Proved Air Has Weight) pre-VO plate boards v01. J0413. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/017_Priestley-Lavoisier-Oxygen/oxygen_script_master_v01.md
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
        "Part 01 — The Mouse Under the Glass",
        [
            ("01_bowood_lens_candle_mouse", 0.0, 5.5, "A", False, "PURE OXYGEN", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + focused solar beam, dazzling candle flame, and lively brown mouse.",
             STYLE + "Bowood House laboratory, Wiltshire, 1 August 1774: a twelve-inch double-convex burning lens on a mahogany stand focuses a bright beam of sunlight onto red mercury powder inside a glass vessel inverted over silver mercury; as colourless gas fills the jar, a candle plunged inside blazes with a dazzling white flame beside a lively brown mouse." + QUAL_TAIL,
             {"kind": "WHEN", "label": "WILTSHIRE · 1 AUGUST 1774", "hold_s": 3.5}),
            ("02_two_chemists_england_paris", 5.5, 6.0, "B", False, "TWO CHEMISTS, ONE GAS", "Quality",
             "Quality: readable faces (Joseph Priestley in England; Antoine and Marie-Anne Lavoisier in Paris).",
             STYLE + "Split period composition: on the left in England, Joseph Priestley holds a glass bell jar over a pneumatic water trough; on the right in Paris, Antoine and Marie-Anne Lavoisier weigh a sealed swan-neck glass retort on a gleaming brass balance." + QUAL_TAIL,
             None),
            ("03_rusted_iron_on_wooden_scale", 11.5, 6.0, "C", False, "AN INVISIBLE FLUID?", "Fast",
             "Fast: daylight workbench prop shot of rusted iron bar tipping a wooden balance scale beside a closed leather chemistry book. Nothing emissive, no face.",
             STYLE + "In grey window light on an eighteenth-century wooden laboratory bench, a flaky rusted iron bar tips down one brass pan of a balance scale beside a shiny new iron bar and a closed leather treatise." + FAST_TAIL,
             {"kind": "WHEN", "label": "1770s", "hold_s": 3.5}),
            ("04_mouse_survival_and_balance_diagram", 17.5, 8.0, "E", False, "TWICE AS LONG · 1/400 GRAIN", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked comparison shows a mouse surviving 15 minutes in ordinary air (21% oxygen, 78% nitrogen) versus 30 minutes in Priestley's pure oxygen, alongside Lavoisier's brass balance accurate to 1/400th of a grain.",
             {"kind": "DATA", "label": "30 MIN VS 15 MIN · 1/400 GRAIN", "detail": "Inked comparison of ordinary air (21% O2, 15-min mouse survival) vs Priestley's bell-jar gas (100% O2, 30-min survival) and Lavoisier's 1/400th-grain balance", "scale": "1/400th of a grain — sensitive enough to weigh a single eyelash", "who_card": "Joseph Priestley (1733–1804) — English natural philosopher · Antoine Lavoisier (1743–1794) — French Academy chemist", "when_stamp": "1 August 1774", "hold_s": 3.8}),
            ("05_pneumatic_trough_mercury_pan", 25.5, 5.5, "A", False, "BOWOOD BENCH", "Fast",
             "Fast: daylight pan across pneumatic trough and inverted glass bell jars between code graphics so two full-frame graphics never run back to back.",
             STYLE + "In warm afternoon window light, the camera tracks smoothly across a wooden pneumatic trough filled with water and inverted glass bell jars beside a basin of silver mercury." + FAST_TAIL,
             None),
            ("06_three_bathtubs_daily_oxygen_scale", 31.0, 8.0, "E", False, "THREE BATHTUBS A DAY", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked scale comparison shows 17,000 daily human breaths drawing in 11,000 litres of air containing 550 litres of pure oxygen, filling three cast-iron bathtubs.",
             {"kind": "DATA", "label": "550 LITRES O₂ / DAY · 3 BATHTUBS", "detail": "Inked daily-breath comparison showing 17,000 breaths/day and 550 litres of pure oxygen consumed per person every day", "scale": "550 litres of oxygen a day — enough to fill three bathtubs", "hold_s": 3.8}),
            ("07_table_three_props_lens_jar_retort", 39.0, 5.5, "C", False, "BOWOOD HOUSE, 1774", "Fast",
             "Fast: daylight prop table (callback source for Part 05: 12-inch lens, glass bell jar, swan-neck retort). Nothing emissive.",
             STYLE + "On a wooden laboratory workbench in afternoon window light sit three objects side by side: a twelve-inch brass-rimmed burning lens on its mahogany stand, a tall glass bell jar, and a curved swan-neck glass retort." + FAST_TAIL,
             None),
            ("08_explorer_bowood_bell_jar", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside the mercury trough on Priestley's workbench at Bowood House, the Explorer peers through the curved glass wall of the bell jar at the lively brown mouse inside, touches the brass rim of the twelve-inch lens, and steps back with a delighted nod." + EXP_TAIL,
             None),
            ("09_leeds_brewery_vat_bubbles", 67.5, 5.5, "B", False, "THE BREWERY CLUE", "Fast",
             "Fast: daylight view of rising bubbles over a wooden beer vat in a Leeds brick courtyard. Nothing emissive.",
             STYLE + "In a daylight brick courtyard beside a Yorkshire brewery, thick blankets of tiny bubbles foam and rise across the top of a wide oak fermentation vat." + FAST_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — The Brewery Next Door and the Mouse in the Jar",
        [
            ("01_priestley_leeds_brewery_soda", 85.0, 6.5, "A", False, "LEEDS · 1767", "Quality",
             "Quality: readable face (Joseph Priestley pouring sparkling soda water between two glass tumblers).",
             STYLE + "Leeds, England, 1767: in a brick brewery courtyard, Joseph Priestley in a powdered wig and dark clerical coat leans over a bubbling wooden beer vat, pouring water back and forth between two glass tumblers until the water fizzes." + QUAL_TAIL,
             {"kind": "FACT", "label": "INVENTED FIZZY SODA WATER", "when_stamp": "Leeds, 1767 · 30 November 1773", "timeline_step": "2/7 · 1 Aug 1774 (Priestley's bell jar)", "hold_s": 3.8}),
            ("02_burning_lens_mercuric_oxide_diagram", 91.5, 8.0, "E", False, "OVER 600°C · 4–5× VOLUME", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked pneumatic-trough diagram shows sunlight focused by a 12-inch burning lens to over 600°C onto red mercuric oxide (HgO) floating on liquid mercury inside an inverted glass phial, releasing 4 to 5 times its volume in pure oxygen gas.",
             {"kind": "DATA", "label": "12-INCH LENS · >600°C · 4–5× GAS", "detail": "Inked pneumatic-trough diagram showing 12-inch lens heating red mercuric oxide over liquid mercury to release 4–5× its volume in pure oxygen", "scale": "12-inch lens focusing sunlight to over 600°C — hot enough to split solid red powder into liquid metal and gas", "when_stamp": "1 August 1774", "hold_s": 3.8}),
            ("03_mouse_30_minutes_and_siphon", 99.5, 6.5, "B", False, "TWO MICE AND MYSELF", "Quality",
             "Quality: readable face (Joseph Priestley watching lively mouse past 30 minutes and breathing through glass siphon).",
             STYLE + "Bowood House, 8 March 1775: Joseph Priestley watches a lively brown mouse groom its whiskers beneath an inverted glass receiver over mercury as a brass pocket watch sweeps past thirty minutes, then inhales from the jar through a curved glass siphon." + QUAL_TAIL,
             {"kind": "WHEN", "label": "8 MARCH 1775", "hold_s": 3.5}),
            ("04_stahl_phlogiston_furnace_1703", 106.0, 6.5, "C", False, "DEPHLOGISTICATED AIR", "Quality",
             "Quality: readable face (Georg Ernst Stahl) and glowing charcoal furnace wisps (never Fast).",
             STYLE + "Halle, Germany, 1703: German chemist Georg Ernst Stahl in a curled periwig and velvet coat gestures beside a glowing brick alchemy furnace as golden wisps rise from burning charcoal." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Georg Ernst Stahl", "line_2": "(1659–1734) — German phlogiston chemist", "when_stamp": "1703", "timeline_step": "1/7 · 1703 (Stahl's phlogiston)", "hold_s": 3.8}),
        ],
    ),
    (
        3,
        "Part 03 — The Dinner Table in Paris and the 12-Day Retort",
        [
            ("01_paris_dinner_october_1774", 112.5, 6.5, "A", False, "THE PARIS DINNER", "Quality",
             "Quality: readable faces (Antoine Lavoisier, Marie-Anne Paulze Lavoisier, and Joseph Priestley) + candlelight.",
             STYLE + "Paris Arsenal, October 1774: at a candlelit dining table, Antoine Lavoisier in a powdered wig and silk waistcoat and young Marie-Anne Paulze Lavoisier holding an English notebook and charcoal stylus listen intently across the linen table to Joseph Priestley." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Marie-Anne Paulze Lavoisier", "line_2": "(1758–1836) — French chemistry translator", "when_stamp": "Paris · October 1774", "timeline_step": "4/7 · Oct 1774 (Paris dinner)", "hold_s": 3.8}),
            ("02_easter_memoir_credit_clash", 119.0, 6.5, "B", False, "26 APRIL 1775", "Quality",
             "Quality: readable faces (Antoine Lavoisier reading Easter Memoir in Paris; outraged Joseph Priestley in England).",
             STYLE + "Split portrait scene, April 1775: in Paris, Antoine Lavoisier reads a memoir before the Royal Academy of Sciences beside a brass balance; in England, Joseph Priestley frowns over the printed French pamphlet." + QUAL_TAIL,
             {"kind": "FACT", "label": "TRIED TO CLAIM SOLE CREDIT", "when_stamp": "26 April 1775", "hold_s": 3.8}),
            ("03_swan_neck_retort_unlit_bench", 125.5, 5.5, "C", False, "TWELVE DAYS SEALED", "Fast",
             "Fast: daylight studio shot of unlit curved swan-neck glass retort linked to a bell jar over mercury before the code graphic. Nothing emissive.",
             STYLE + "In clear daylight on a marble Paris workbench, a long curved swan-neck glass retort holding liquid mercury curves into an inverted glass bell jar sitting in a trough." + FAST_TAIL,
             None),
            ("04_twelve_day_retort_mass_balance_diagram", 131.0, 8.5, "E", False, "1/5TH OF EVERY BREATH", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked two-part mass-balance diagram of Lavoisier's 12-day swan-neck retort shows 4 oz mercury in 50 cubic inches of air losing 8–9 cubic inches (~1/5th) as 45 grains of red oxide gain 3.5 grains, then heating yields 41.5 grains mercury + 3.5 grains (8–9 in³) pure oxygen.",
             {"kind": "DATA", "label": "45 GR CALX = 41.5 GR HG + 3.5 GR O₂", "detail": "Inked mass-balance diagram of Lavoisier's 12-day swan-neck retort: 50 in³ air loses 8–9 in³ (~1/5th) as 45 grains red oxide gain 3.5 grains", "scale": "8 to 9 cubic inches out of 50 — roughly 1/5th of every breath you take is oxygen", "when_stamp": "1777", "timeline_step": "5/7 · 1777 (Lavoisier names oxygen)", "hold_s": 3.8}),
        ],
    ),
    (
        4,
        "Part 04 — The Unopened Letter and the Guinea Pig in Ice",
        [
            ("01_scheele_uppsala_fire_air_letter", 139.5, 6.5, "A", False, "UPPSALA · 1772", "Quality",
             "Quality: readable face (Carl Wilhelm Scheele) + charcoal brazier glow in candlelit Uppsala apothecary.",
             STYLE + "Uppsala, Sweden, 1772 and 30 September 1774: in a cramped candlelit apothecary shop, Carl Wilhelm Scheele in an ink-stained apron traps gas in an oiled bladder over a warm brazier, then seals a handwritten French letter addressed to Paris." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Carl Wilhelm Scheele", "line_2": "(1742–1786) — Swedish pharmaceutical chemist", "fact_card": "Scheele made oxygen first (1772)", "when_stamp": "1771–1772 · 30 Sep 1774 · 1890", "timeline_step": "3/7 · 1772 (Scheele's fire air)", "hold_s": 3.8}),
            ("02_guinea_pig_ice_calorimeter", 146.0, 6.5, "B", False, "BREATHING IS BURNING", "Quality",
             "Quality: readable faces (Antoine Lavoisier and Pierre-Simon Laplace) with guinea pig in three-walled tin ice calorimeter.",
             STYLE + "Paris Arsenal, 1780–1783: Antoine Lavoisier and mathematician Pierre-Simon Laplace place a plump brown-and-white guinea pig inside a three-walled tin ice calorimeter and weigh the water melted from the middle jacket of ice in a glass beaker." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Pierre-Simon Laplace", "line_2": "(1749–1827) — French mathematician & physicist", "when_stamp": "1780–1783", "hold_s": 3.8}),
            ("03_traite_fermentation_balance_1789", 152.5, 5.5, "C", False, "NOTHING IS CREATED", "Fast",
             "Fast: daylight workbench shot of copperplate engraving beside airtight fermentation flask balanced against brass weights. Nothing emissive, no readable text.",
             STYLE + "In daylight at the Paris Arsenal, a copperplate laboratory drawing lies beside a large brass balance where an airtight glass flask of bubbling liquid holds dead-level against brass weights." + FAST_TAIL,
             {"kind": "WHEN", "label": "PARIS · 1789", "timeline_step": "6/7 · 1789 (Conservation of Mass)", "hold_s": 3.5}),
            ("04_explorer_paris_arsenal_balance", 158.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Perched on the marble base of Lavoisier's giant brass balance in the Paris Arsenal, the Explorer watches the pointer needle hold dead-centre at zero while bubbles foam inside the sealed fermentation flask, taps the glass dome, and gives an approving salute." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Where Lost Weight Goes and the Guillotine",
        [
            ("01_fat_exhaled_and_timeline_1703_1794", 163.5, 8.5, "E", False, "84% EXHALED AS GAS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked mass-conservation chart shows 10 kg of lost human fat combining with oxygen to split into 8.4 kg (84%) exhaled as CO2 and 1.6 kg (16%) as H2O, while the 7-date timeline completes across the bottom: 1703 · 1772 · 1 Aug 1774 · Oct 1774 · 1777 · 1789 · 8 May 1794.",
             {"kind": "DATA", "label": "8.4 KG OF 10 KG FAT EXHALED · 1703 → 1794", "detail": "Completed 7-date oxygen timeline (1703 → 8 May 1794) alongside 10 kg fat mass-balance chart (8.4 kg CO2 exhaled vs 1.6 kg H2O)", "scale": "8.4 kilograms out of every 10 kilograms of fat you lose is breathed out as invisible gas", "fact_card": "Exhale 84% of lost fat", "when_stamp": "1703–1794 · 2014", "hold_s": 3.8}),
            ("02_lagrange_and_marie_anne_chest", 172.0, 6.5, "A", False, "ONE HUNDRED YEARS", "Quality",
             "Quality: readable faces (mathematician Joseph-Louis Lagrange and Marie-Anne Lavoisier locking notebooks in wooden chest).",
             STYLE + "Paris, May 1794: mathematician Joseph-Louis Lagrange in a dark coat holds Lavoisier's leather treatise with a solemn expression while Marie-Anne Lavoisier locks stacks of handwritten laboratory notebooks safely inside an oak chest." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Joseph-Louis Lagrange", "line_2": "(1736–1813) — French-Italian mathematician", "when_stamp": "July 1791 · 8 May 1794 · 6 Feb 1804", "timeline_step": "7/7 · 8 May 1794 (Lavoisier guillotined)", "hold_s": 3.8}),
            ("03_herschel_prism_thermometer_handoff", 178.5, 6.0, "C", False, "HOTTER IN THE DARK", "Fast",
             "Fast: sunlit window prism casting a rainbow across a wooden table with a mercury thermometer in the dark shadow past red (handoff to 018 Herschel). Daylight/rainbow only, no flame or face.",
             STYLE + "Slough, February 1800: a glass prism mounted in a window shutter casts a bright solar rainbow across a slanted wooden board, where a blackened-bulb mercury thermometer sits in the dark shadow half an inch past the red edge." + FAST_TAIL,
             {"kind": "WHEN", "label": "FEBRUARY 1800", "hold_s": 3.5}),
            ("04_table_three_callback", 184.5, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_lens_jar_retort (callback, £0).",
             "Reuse P1:07_table_three_props_lens_jar_retort [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_lens_jar_retort"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_lens_jar_retort",
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
            "film": "017_Priestley-Lavoisier-Oxygen",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from oxygen_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "017_Priestley-Lavoisier-Oxygen",
        "version": "v01",
        "written": "2026-10-16",
        "task": "J0413: HOS 017 pre-VO plate boards v01 (from oxygen_script_master_v01.md + SOURCES_v01.md). Flow-first. Mint nothing. Parked for Chief.",
        "script": "oxygen_script_master_v01.md (93.9 PASS)",
        "facts_pass": "SOURCES_v01.md (16 rows)",
        "vo_status": "Awaiting Chief script sign-off and long VO recording; rows re-time automatically onto Scribe STT once VO locks.",
        "readings": {
            "flow_credits_left": 23740,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018. Nothing in 017 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 017 Oxygen: The Bell-Jar Experiment That Proved Air Has Weight — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 16 Oct 2026, J0413. Built from `oxygen_script_master_v01.md` (93.9 PASS) and `SOURCES_v01.md`.",
        "**No mint, no spend.** Pre-VO clock timings (`186.9 s` base picture grid; re-times automatically onto Scribe word timestamps once long VO locks).",
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
        "# 017 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 16 Oct 2026, J0413. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `oxygen_script_master_v01.md` (93.9 PASS) and `SOURCES_v01.md` so 017's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Joseph Priestley, Antoine Lavoisier, Marie-Anne Paulze Lavoisier, Georg Ernst Stahl, Carl Wilhelm Scheele, Pierre-Simon Laplace, Joseph-Louis Lagrange), candle/brazier/sun-beam scenes (Bowood burning lens + candle, Stahl alchemy furnace, Paris candlelit dinner, Uppsala brazier), and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight and grey-window-light prop and laboratory shots (rusted iron on balance scale, pneumatic trough pan, 3-object Bowood bench, bubbling Leeds beer vat, unlit swan-neck retort on marble bench, 1789 fermentation balance, sunlit Herschel prism handoff). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_mouse_survival_and_balance_diagram` — ordinary air (21% O2, 15-min mouse survival) vs Priestley's pure oxygen (30-min survival) + Lavoisier's 1/400th-grain balance (`SCALE: 1/400th of a grain — sensitive enough to weigh a single eyelash`)",
        "  2. `P1:06_three_bathtubs_daily_oxygen_scale` — 17,000 daily breaths and 550 litres of pure oxygen per day (`SCALE: 550 litres of oxygen a day — enough to fill three bathtubs`)",
        "  3. `P2:02_burning_lens_mercuric_oxide_diagram` — 12-inch burning lens (>600°C) heating red mercuric oxide over mercury to release 4–5× volume of O2 (`SCALE: 12-inch lens focusing sunlight to over 600°C — hot enough to split solid red powder into liquid metal and gas`)",
        "  4. `P3:04_twelve_day_retort_mass_balance_diagram` — Lavoisier's 12-day swan-neck retort mass balance: 50 in³ air loses 8–9 in³ (~1/5th) as 45 grains calx = 41.5 grains Hg + 3.5 grains O2 (`SCALE: 8 to 9 cubic inches out of 50 — roughly 1/5th of every breath you take is oxygen`)",
        "  5. `P5:01_fat_exhaled_and_timeline_1703_1794` — completed 7-date timeline (1703 → 8 May 1794) + 10 kg fat mass-balance chart: 8.4 kg CO2 exhaled vs 1.6 kg H2O (`SCALE: 8.4 kilograms out of every 10 kilograms of fat you lose is breathed out as invisible gas`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_lens_jar_retort`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"017 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
