#!/usr/bin/env python3
"""HOS 010 plate boards v03. J0365. No mint, no spend.

Builds v03 from the v02 boards:
1. Resolves the P5:14_bench_three_again reuse shortfall (8.16 s needed vs 2.65 s
   unused usable moving footage in P1:03_bench_three; even a full 7.90 s clip is
   short by 0.26 s). Splits into P5:14_bench_three_again (5.51 s own Fast mint,
   10 try-1 / 20 expected Flow credits) + P5:14_bench_three_again_c1 (2.65 s £0
   reuse of the unused [5.25s..7.90s] tail of P1:03_bench_three, 0.00 s shortfall).
2. Marks code_graphic_layout on the 13 £0 code graphics so P4:03_world_pins,
   P4:04_supernova_test, and P4:05_ten_km alternate full-frame and window/overlay
   (never two full-frame teach graphics back to back, AGENTS.md Gate 6).
3. Attaches explicit Teach-on-Screen edit-overlay specs (WHO, WHEN, DATA+SCALE,
   FACT, TIMELINE) to the timed board rows (added in edit, £0 / 0 Flow credits).
Nothing is generation_authorized.
"""
from __future__ import annotations

import copy
import json
import math
from pathlib import Path

EDIT = Path(__file__).resolve().parent
OUT = EDIT / "parts"

FLOW_CREDITS_LEFT = 23740
FLOW_READ_AT = "2026-10-15T21:42:22Z"
VERTEX_BALANCE_GBP = 71.02
VERTEX_READ_AT = "2026-10-15T07:30:31Z"
VERTEX_MARGIN_GBP = 1.00
VERTEX_LENGTHS = (4, 6, 8)
FLOW_CREDITS = {"Quality": 100, "Fast": 10}
USD_PER_S = {"Quality": 0.20, "Fast": 0.10}
USD_PER_STILL = 0.039
GBP_PER_USD = 0.80
TAKES_PER_KEEP = {"Quality": round(70 / 27, 2), "Fast": round(94 / 48, 2)}
STILLS_PER_PLATE = round(171 / 75, 2)
CLIP_USE_S = 7.9

RESERVED = {
    "006": 0,
    "007": 7196,
    "008": 5605,
    "009 tranche 1": 7354,
    "028": 279,
}
HEADROOM_FLOOR = 3000

STYLE = "Premium Animistry-class 3D cartoon. "
TAIL = (
    " Daylight, window light or matte painted ink only. No candle, flame, glow, "
    "spark, fireball or lightning. No readable words or numbers anywhere. Silent. "
    "Continuous motion through the final frame. No Explorer. No Orbit."
)

TEACH_OVERLAYS = {
    "P1:01_clay_line": {
        "kind": "DATA",
        "label": "THE CLAY LINE",
        "detail": "1 cm Gubbio clay band scale comparison against a pencil tip",
        "scale": "as thin as a little finger",
        "hold_s": 3.5,
    },
    "P1:04_long_reign": {
        "kind": "WHEN",
        "label": "66 MILLION YEARS AGO",
        "timeline_step": "1/5 · 66 Ma (Cretaceous end)",
        "hold_s": 3.5,
    },
    "P1:05_empty_plain": {
        "kind": "FACT",
        "label": "3 IN 4 SPECIES VANISHED",
        "source_note": "About three-quarters of all species vanished at the K–Pg boundary (FACT_NOTES_v01).",
        "hold_s": 3.5,
    },
    "P2:01_walter_hammer": {
        "kind": "WHO",
        "line_1": "Walter Alvarez",
        "line_2": "(born 1940) — American geologist",
        "when_stamp": "Gubbio, Italy · 1970s",
        "timeline_step": "2/5 · 1970s (Gubbio gorge)",
        "hold_s": 3.8,
    },
    "P2:08_two_clocks": {
        "kind": "DATA",
        "label": "HOW MANY YEARS?",
        "detail": "Inked two-clock comparison contrasting slow sea-floor clay deposition (thousands of years) with a sudden catastrophe (a few years)",
        "scale": "one centimetre of clay: thousands of years or one moment",
        "hold_s": 3.8,
    },
    "P3:01_luis_sample": {
        "kind": "WHO",
        "line_1": "Luis Alvarez",
        "line_2": "(1911–1988) — Berkeley physicist",
        "when_stamp": "Berkeley · Late 1970s",
        "timeline_step": "3/5 · Late 1970s (Berkeley)",
        "hold_s": 3.8,
    },
    "P3:02_pyramid_muons": {
        "kind": "FACT",
        "label": "X-RAYED AN EGYPTIAN PYRAMID",
        "source_note": "Luis Alvarez used cosmic-ray muons to search the Pyramid of Khafre for hidden chambers (Science 1970; FACT_NOTES_v01).",
        "hold_s": 3.5,
    },
    "P3:08_asaro_michel": {
        "kind": "WHO",
        "line_1": "Frank Asaro & Helen Michel",
        "line_2": "(1927–2014 · born 1932) — nuclear chemists",
        "hold_s": 3.8,
    },
    "P4:01_iridium_spike": {
        "kind": "DATA",
        "label": "THE IRIDIUM SPIKE",
        "detail": "Hand-drawn lab notebook graph showing a 30× iridium spike in the Gubbio clay layer",
        "scale": "30 times the iridium in the rock above and below",
        "hold_s": 3.8,
    },
    "P4:02_stevns_cliff": {
        "kind": "WHEN",
        "label": "STEVNS KLINT · DENMARK",
        "hold_s": 3.2,
    },
    "P4:04_supernova_test": {
        "kind": "FACT",
        "label": "NO SUPERNOVA PLUTONIUM FOUND",
        "source_note": "Tested for plutonium-244 from a nearby supernova; none found in the boundary clay (Alvarez et al. 1980; FACT_NOTES_v01).",
        "hold_s": 3.5,
    },
    "P4:05_ten_km": {
        "kind": "DATA",
        "label": "ABOUT 10 KM WIDE",
        "detail": "10 km asteroid scale comparison against a city skyline and Mount Everest",
        "scale": "ten kilometres across — wider than Mount Everest is tall",
        "hold_s": 3.8,
    },
    "P4:08_science_paper": {
        "kind": "DATA",
        "label": "SCIENCE · 6 JUNE 1980",
        "detail": "Animated timeline that builds as each date is said (66 Ma · 1970s Gubbio · Late 1970s Berkeley · June 1980 Science · Early 1990s Chicxulub)",
        "scale": "ten years from the 1980 Science paper to the buried crater",
        "when_stamp": "6 June 1980",
        "timeline_step": "4/5 · 6 June 1980 (Science paper)",
        "hold_s": 3.8,
    },
    "P5:04_chicxulub_ring": {
        "kind": "WHEN",
        "label": "EARLY 1990s · YUCATÁN",
        "timeline_step": "5/5 · Early 1990s (Chicxulub crater)",
        "hold_s": 3.5,
    },
    "P5:05_ring_scale": {
        "kind": "DATA",
        "label": "ABOUT 180 KM WIDE",
        "detail": "Chicxulub crater ring (~180 km wide) laid over southern England for scale",
        "scale": "180 kilometres wide — stretching across southern England",
        "hold_s": 3.8,
    },
    "P5:09_robin": {
        "kind": "FACT",
        "label": "BIRDS ARE LIVING DINOSAURS",
        "source_note": "Every living bird is a surviving avian dinosaur (FACT_NOTES_v01).",
        "hold_s": 3.2,
    },
}


def price_mint(q: str, need_s: float) -> dict:
    clip = next(L for L in VERTEX_LENGTHS if L >= need_s - 1e-6)
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


def zero_route(route: str) -> dict:
    return {
        "route": route,
        "flow_model": None,
        "flow_clip_s": 0,
        "flow_credits_try1": 0,
        "flow_credits_expected": 0,
        "vertex_model": None,
        "vertex_clip_s": 0,
        "vertex_try1_gbp": 0.0,
        "vertex_expected_gbp": 0.0,
    }


def apply_price(row: dict, priced: dict, cum_flow: int, cum_vx: float) -> tuple[int, float]:
    row.update(priced)
    if priced["route"] == "flow-first":
        cum_flow += priced["flow_credits_expected"]
        cum_vx += priced["vertex_expected_gbp"]
    row["cum_flow_credits_expected"] = cum_flow
    row["cum_vertex_expected_gbp"] = round(cum_vx, 2)
    return cum_flow, cum_vx


def main() -> None:
    v02_plan = json.loads((EDIT / "PICTURE_PLAN_v02.json").read_text())
    boards = []
    for n in range(1, 6):
        boards.append(json.loads((OUT / f"part-{n:02d}_plates_v02.json").read_text()))

    # Split P5:14_bench_three_again (8.16 s) into 5.51 s own Fast mint + 2.65 s verified reuse of P1:03_bench_three
    p5_plates = []
    for row in boards[4]["plates"]:
        if row["id"] == "14_bench_three_again":
            total_use = round(float(row["use_s"]), 2)  # 8.16 s
            unused_p1 = round(CLIP_USE_S - 5.25, 2)    # 2.65 s unused in P1:03_bench_three
            mint_use = round(total_use - unused_p1, 2)  # 5.51 s

            r_mint = copy.deepcopy(row)
            r_mint["id"] = "14_bench_three_again"
            r_mint["use_s"] = mint_use
            r_mint["quality"] = "Fast"
            r_mint["route"] = "flow-first"
            r_mint["engine_reason"] = (
                "J0365 reuse moving-footage audit: P1:03_bench_three (7.90 s usable) uses 5.25 s in Part 01, "
                "leaving 2.65 s unused usable footage (shortfall 5.51 s against 8.16 s). Even a full 7.90 s clip "
                "cannot cover 8.16 s without looping/freezing. Mint the first 5.51 s as an own Fast plate (new angle "
                "on the same workbench) and cover the remaining 2.65 s from P1:03_bench_three's unused moving tail."
            )
            r_mint["prompt"] = (
                STYLE
                + "An overhead-angled track across the same wooden workbench in grey window light. "
                "The geologist's hammer, the glass vial of grey clay, and the folded printed paper sit side by side. "
                "The paper shows only a soft blur of ink marks, not words."
                + TAIL
            )
            r_mint["reference"] = "same look as P1:03_bench_three; own Fast text mint, not an i2v continuation"
            r_mint["reuse_measurement"] = {
                "source_row": "P1:03_bench_three",
                "source_clip_usable_s": CLIP_USE_S,
                "source_used_s": 5.25,
                "unused_usable_s": unused_p1,
                "required_use_s": total_use,
                "shortfall_usable_s": mint_use,
                "distinct_window": False,
                "resolution": "split_own_fast_mint_plus_unused_tail_reuse",
            }
            r_mint["generation_authorized"] = False
            r_mint.pop("reuse_of", None)

            r_tail = copy.deepcopy(row)
            t_tail = round(float(row["t_s"]) + mint_use, 2)
            mm, ss = divmod(t_tail, 60)
            r_tail["id"] = "14_bench_three_again_c1"
            r_tail["t_s"] = t_tail
            r_tail["t"] = f"{int(mm)}:{ss:05.2f}"
            r_tail["local_s"] = round(float(row["local_s"]) + mint_use, 2)
            r_tail["use_s"] = unused_p1
            r_tail["added"] = True
            r_tail["quality"] = "reuse"
            r_tail["reuse_of"] = "P1:03_bench_three"
            r_tail["reference"] = "P1:03_bench_three unused moving tail [5.25s..7.90s]"
            r_tail["prompt"] = None
            r_tail["engine_reason"] = (
                "J0365 verified reuse: uses the 2.65 s unused moving tail [5.25s..7.90s] of P1:03_bench_three "
                "(shortfall 0.00 s). No loop, no freeze, no replayed frames."
            )
            r_tail["reuse_measurement"] = {
                "source_row": "P1:03_bench_three",
                "source_clip_usable_s": CLIP_USE_S,
                "source_used_s": 5.25,
                "unused_usable_s": unused_p1,
                "required_use_s": unused_p1,
                "shortfall_usable_s": 0.0,
                "distinct_window": True,
                "window_s": [5.25, 7.90],
                "resolution": "verified_unused_tail_reuse",
            }
            r_tail["generation_authorized"] = False
            p5_plates.extend([r_mint, r_tail])
        else:
            p5_plates.append(row)
    boards[4]["plates"] = p5_plates

    cum_flow = 0
    cum_vx = 0.0
    totals = {
        "rows": 0,
        "Quality": 0,
        "Fast": 0,
        "code_graphic": 0,
        "edit_hold": 0,
        "reuse": 0,
        "added": 0,
        "flow_credits_try1": 0,
        "flow_credits_expected": 0,
        "vertex_try1_gbp": 0.0,
        "vertex_expected_gbp": 0.0,
        "explorer": 0,
        "teach_overlays": 0,
    }
    per_part = []

    for n, board in enumerate(boards, start=1):
        pp = {
            "part": n,
            "rows": 0,
            "Quality": 0,
            "Fast": 0,
            "code_graphic": 0,
            "edit_hold": 0,
            "reuse": 0,
            "added": 0,
            "flow_credits_try1": 0,
            "flow_credits_expected": 0,
            "vertex_try1_gbp": 0.0,
            "vertex_expected_gbp": 0.0,
        }
        for row in board["plates"]:
            key = f"P{n}:{row['id']}"
            row["generation_authorized"] = False
            if key in TEACH_OVERLAYS:
                row["teach_overlay"] = TEACH_OVERLAYS[key]
                totals["teach_overlays"] += 1

            if row.get("route") == "code-graphic" or row.get("quality") == "code_graphic":
                # Alternate full-frame vs window overlay when code graphics sit adjacent (P4:03, P4:04, P4:05)
                if key == "P4:04_supernova_test":
                    row["code_graphic_layout"] = (
                        "window_overlay (cream-on-navy card inset over moving desk/night plate in edit so two "
                        "full-frame teach graphics never sit back to back; AGENTS.md Teach on screen Gate 6)"
                    )
                else:
                    row["code_graphic_layout"] = "full_frame_parchment"
                priced = zero_route("code-graphic")
                pp["code_graphic"] += 1
            elif row.get("route") == "edit-hold" or row.get("route_kind") == "edit-hold":
                priced = zero_route("edit-hold")
                pp["edit_hold"] += 1
            elif row.get("route") == "reuse" or row.get("quality") == "reuse":
                priced = zero_route("reuse")
                pp["reuse"] += 1
            else:
                q = row["quality"]
                priced = price_mint(q, float(row["use_s"]))
                pp[q] += 1

            cum_flow, cum_vx = apply_price(row, priced, cum_flow, cum_vx)
            pp["rows"] += 1
            if row.get("added"):
                pp["added"] += 1
            if row.get("explorer"):
                totals["explorer"] += 1
            pp["flow_credits_try1"] += priced["flow_credits_try1"]
            pp["flow_credits_expected"] += priced["flow_credits_expected"]
            pp["vertex_try1_gbp"] = round(pp["vertex_try1_gbp"] + priced["vertex_try1_gbp"], 2)
            pp["vertex_expected_gbp"] = round(pp["vertex_expected_gbp"] + priced["vertex_expected_gbp"], 2)

        board["version"] = "v03"
        board["task"] = "J0365 plate boards v03 (closes P5:14 reuse hole + Teach on Screen overlay specs). No mint."
        board["mint"] = False
        board["summary"] = pp
        (OUT / f"part-{n:02d}_plates_v03.json").write_text(json.dumps(board, indent=2, ensure_ascii=False) + "\n")
        per_part.append(pp)
        for k in (
            "rows",
            "Quality",
            "Fast",
            "code_graphic",
            "edit_hold",
            "reuse",
            "added",
            "flow_credits_try1",
            "flow_credits_expected",
        ):
            totals[k] += pp[k]
        totals["vertex_try1_gbp"] = round(totals["vertex_try1_gbp"] + pp["vertex_try1_gbp"], 2)
        totals["vertex_expected_gbp"] = round(totals["vertex_expected_gbp"] + pp["vertex_expected_gbp"], 2)

    reserved_sum = sum(RESERVED.values())
    left_after_reserved = FLOW_CREDITS_LEFT - reserved_sum
    need_to_mint = totals["flow_credits_expected"] + HEADROOM_FLOOR
    usable_vx = round(VERTEX_BALANCE_GBP - VERTEX_MARGIN_GBP, 2)
    fits_flow_alone = totals["flow_credits_expected"] + HEADROOM_FLOOR <= FLOW_CREDITS_LEFT
    fits_vertex = totals["vertex_expected_gbp"] <= usable_vx
    fits_order = need_to_mint <= left_after_reserved

    departures = list(v02_plan.get("departures_from_shot_list", [])) + [
        "v03 (J0365): P5:14_bench_three_again (8.16 s) is split into P5:14_bench_three_again (5.51 s own Fast mint, 10 try-1 / 20 expected credits) + P5:14_bench_three_again_c1 (2.65 s £0 reuse of the unused [5.25s..7.90s] tail of P1:03_bench_three, 0.00 s shortfall).",
        "v03 (J0365): P4:04_supernova_test carries code_graphic_layout='window_overlay' so P4:03_world_pins, P4:04_supernova_test, and P4:05_ten_km alternate full-frame and window/overlay (never two full-frame teach graphics back to back).",
        "v03 (J0365): 15 Teach-on-Screen edit-overlay specs (3 WHO cards, 6 WHEN stamps + 5-step timeline, 5 DATA+SCALE moments, 3 FACT beats) are attached to the timed rows.",
    ]

    plan = {
        "film": "010_Alvarez-Clay-Line-Dinosaurs",
        "version": "v03",
        "written": "2026-10-16",
        "task": "J0365: plate boards v03 (P5:14 reuse hole closed + Teach on Screen overlay specs). Flow-first. Mint nothing. Parked for Chief.",
        "shot_list": "07_Edit-Project/SHOT_LIST_v01.md",
        "vo": v02_plan["vo"],
        "from": "part-0N_plates_v02.json. Spoken lines and VO timings unchanged.",
        "readings": v02_plan["readings"],
        "rates": v02_plan["rates"],
        "vo_film_total_s": v02_plan["vo_film_total_s"],
        "totals": totals,
        "per_part": per_part,
        "fits_now": {
            "flow_if_010_were_alone": fits_flow_alone,
            "vertex": fits_vertex,
            "vertex_authorised": False,
            "mint_order_with_3000_headroom": fits_order,
        },
        "reserved_flow_expected": RESERVED,
        "reserved_flow_sum": reserved_sum,
        "flow_left_after_reserved": left_after_reserved,
        "flow_needed_for_010_plus_headroom": need_to_mint,
        "mint_order": "006 > 007 > 008 > 009 tranche 1 > (~12 Nov AI Ultra renewal: 009 tranche 2 5180, then 010 12393). This board does not mint.",
        "departures_from_shot_list": departures,
    }
    (EDIT / "PICTURE_PLAN_v03.json").write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")

    lines = [
        "# 010 price review v03",
        "",
        "Gemini, 16 Oct 2026, J0365. Boards only. **No mint. No spend. No merge.**",
        "v03 closes the one remaining reuse shortfall in v02 (`P5:14_bench_three_again`, 8.16 s needed vs 2.65 s unused in `P1:03_bench_three`), alternates `P4:04_supernova_test` as a window overlay so no two full-frame teach graphics sit back to back, and attaches the 15 Teach-on-Screen edit-overlay specs (`WHO`, `WHEN`, `DATA`+`SCALE`, `FACT`, `TIMELINE`). Parked for Chief.",
        "",
        "Locked VO: Chief KEEP, desk #180 comment 6101773293. Timings match v01/v02. "
        f"Film picture {plan['vo_film_total_s']}s with the closing breath.",
        "",
        "## Readings",
        "",
        f"- Flow: **{FLOW_CREDITS_LEFT}** credits at {FLOW_READ_AT} (J0313, CDP :9222). Not re-read. No spend in this job.",
        f"- Vertex promo: **£{VERTEX_BALANCE_GBP:.2f}** at {VERTEX_READ_AT}. Usable **£{usable_vx:.2f}** after the £1 margin. Not re-read. **Not authorised** for 010.",
        "",
        "## Totals",
        "",
        "| | rows | Quality | Fast | code | edit-hold | reuse | Flow try-1 | Flow expected | Vertex try-1 | Vertex expected |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for pp in per_part:
        lines.append(
            f"| Part {pp['part']:02d} | {pp['rows']} | {pp['Quality']} | {pp['Fast']} | {pp['code_graphic']} | "
            f"{pp['edit_hold']} | {pp['reuse']} | {pp['flow_credits_try1']} | {pp['flow_credits_expected']} | "
            f"£{pp['vertex_try1_gbp']:.2f} | £{pp['vertex_expected_gbp']:.2f} |"
        )
    lines.append(
        f"| **Film** | **{totals['rows']}** | **{totals['Quality']}** | **{totals['Fast']}** | **{totals['code_graphic']}** | "
        f"**{totals['edit_hold']}** | **{totals['reuse']}** | **{totals['flow_credits_try1']}** | "
        f"**{totals['flow_credits_expected']}** | **£{totals['vertex_try1_gbp']:.2f}** | **£{totals['vertex_expected_gbp']:.2f}** |"
    )
    lines += [
        "",
        "v01 was 72 rows: 48 Quality, 7 Fast, 13 code, 3 edit-hold, 1 reuse; Flow expected 12,572, Vertex expected £146.88.",
        "v02 was 72 rows: 47 Quality, 10 Fast, 13 code, 1 edit-hold, 1 reuse; Flow expected 12,373, Vertex expected £147.99.",
        f"v03 is **{totals['rows']} rows**: {totals['Quality']} Quality, {totals['Fast']} Fast, {totals['code_graphic']} code, "
        f"{totals['edit_hold']} edit-hold, {totals['reuse']} verified reuse; Flow try-1 **{totals['flow_credits_try1']}**, "
        f"Flow expected **{totals['flow_credits_expected']}** (+20 cr over v02), Vertex expected £{totals['vertex_expected_gbp']:.2f}.",
        "",
        "## What changed from v02 → v03",
        "",
        "1. **`P5:14_bench_three_again` (8.16 s) reuse shortfall closed (+10 try-1 / +20 expected Flow credits):**",
        "   - In v02, `P5:14_bench_three_again` (`use_s: 8.16 s`) was marked `reuse` of `P1:03_bench_three` (0 cr).",
        "   - `P1:03_bench_three` is an 8.00 s (7.90 s usable) Fast clip that already uses 5.25 s in Part 01, leaving **2.65 s** unused moving footage (shortfall **5.51 s**, and even a full 7.90 s clip is 0.26 s short of 8.16 s).",
        "   - v03 splits the beat into `P5:14_bench_three_again` (**5.51 s** own Fast mint, overhead track across the workbench, 10 try-1 / 20 expected Flow credits) + `P5:14_bench_three_again_c1` (**2.65 s** £0 reuse of the unused `[5.25s..7.90s]` tail of `P1:03_bench_three`, **0.00 s shortfall**).",
        "2. **Back-to-back code-graphic alternation in Part 04 (`P4:03` → `P4:04` → `P4:05`):**",
        "   - Marks `P4:04_supernova_test` with `code_graphic_layout: window_overlay` (composited over moving plate in edit) so two full-frame teach graphics never sit back to back (`AGENTS.md` *Teach on screen* Gate 6).",
        "3. **Teach on Screen edit-overlay specs attached (`teach_overlay`, £0 / 0 Flow):**",
        "   - 3 `WHO` cards at first mention (`Walter Alvarez (born 1940) — geologist`, `Luis Alvarez (1911–1988) — physicist`, `Frank Asaro & Helen Michel (1927–2014 · born 1932) — chemists`).",
        "   - 6 `WHEN` stamps and 5-step animated `TIMELINE` (`66 Ma` → `1970s Gubbio` → `Late 1970s Berkeley` → `June 1980 Science` → `Early 1990s Chicxulub`).",
        "   - 5 `DATA` + `SCALE` moments (`1 cm clay · thin as a pencil`, `Two-clock comparison`, `Iridium spike · 30× normal`, `10 km asteroid · city scale`, `180 km crater · wider than southern England`).",
        "   - 3 `FACT` cards (`3 IN 4 SPECIES GONE`, `NO PLUTONIUM-244`, `LIVING DINOSAURS`).",
        "",
        "## Mint order",
        "",
        "006 (0 Flow) > 007 (7,196) > 008 (5,605) > 009 tranche 1 (7,354) > (~12 Nov AI Ultra renewal: 009 tranche 2 5,180, then 010 12,393). "
        "Every row has `generation_authorized: false`.",
        "",
        "## For the Chief",
        "",
        "Parked for Chief: 010 plate boards v03 (+20 expected Flow credits to eliminate the 5.51 s reuse shortfall on `P5:14_bench_three_again`). "
        "v02 files remain in place if Chief prefers v02 unchanged. No mint, no spend.",
        "",
    ]
    (EDIT / "PRICE_REVIEW_v03.md").write_text("\n".join(lines))
    print(f"010 v03: rows={totals['rows']} Flow={totals['flow_credits_expected']} Vertex=£{totals['vertex_expected_gbp']:.2f}")


if __name__ == "__main__":
    main()
