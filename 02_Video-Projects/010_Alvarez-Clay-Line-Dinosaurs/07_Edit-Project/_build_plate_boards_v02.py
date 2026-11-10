#!/usr/bin/env python3
"""HOS 010 plate boards v02. J0334. No mint, no spend.

Applies the J0314 Chief price-pass conditions on the v01 boards. Timings, spoken
lines and teach-diagram rows are copied from v01. Nothing is generation_authorized.
"""
from __future__ import annotations

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

# Reserved expected ahead of 010, from the later price passes. 009 tranche 2
# (5,180) waits for the ~12 Nov renewal and is not in this sum.
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

# Own Fast mints. A new angle, same look, not an i2v of a clip that cannot cover the beat.
FAST_MINTS = {
    "P1:03_bench_three_c1": (
        "Closer along the same wooden workbench. The vial of grey clay is already set "
        "and the geologist's hammer rests beside it. The printed page lies open as a blur "
        "of marks, not words. The camera slides toward the vial. Grey window light."
    ),
    "P5:07_deccan_note_c1": (
        "The camera travels low along the same cooled lava. The distant line of old flows "
        "stays under the haze. No eruption, no fire, no animals. Daylight."
    ),
    "P5:07_deccan_note_c2": (
        "A wider angle on the same old lava flows. The camera rises slightly as the haze "
        "sits over the cooled rock. No eruption, no fire, no animals. Daylight."
    ),
}
ASARO = "P3:08_asaro_michel_c1"


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
    boards = []
    for n in range(1, 6):
        boards.append(json.loads((OUT / f"part-{n:02d}_plates_v01.json").read_text()))

    for n, board in enumerate(boards, start=1):
        for row in board["plates"]:
            key = f"P{n}:{row['id']}"
            if key in FAST_MINTS:
                meas = dict(row["reuse_measurement"])
                meas["distinct_window"] = False
                meas["resolution"] = "own_fast_mint"
                parent = meas["source_row"]
                row["quality"] = "Fast"
                row["engine_reason"] = (
                    "J0334, J0314 condition 2 (J0313 lesson): the parent clip cannot cover "
                    f"this beat (shortfall {meas['shortfall_usable_s']} s usable). Own Fast mint, "
                    "new angle, same look as the parent. No edit-hold, no loop, no freeze."
                )
                row["prompt"] = STYLE + FAST_MINTS[key] + TAIL
                row["reference"] = f"same look as {parent}; own Fast text mint, not an i2v continuation"
                row["v01_quality"] = "Fast"
                row["v01_parent_quality"] = "Fast"
                row["reuse_measurement"] = meas
                row["generation_authorized"] = False
                row.pop("route_kind", None)
                row.pop("reuse_of", None)
                row.pop("i2v_from", None)
                row.pop("quality_continuation", None)
            elif key == ASARO:
                meas_q = row["quality_continuation"]
                parent = meas_q["source_row"]
                row["quality"] = "reuse"
                row["route_kind"] = "edit-hold"
                row["reuse_of"] = parent
                row["reference"] = parent
                row["prompt"] = None
                row["engine_reason"] = (
                    "J0334, J0314 condition 3: shortfall is only "
                    f"{meas_q['shortfall_usable_s']} s. Prefer an edit-hold of the parent "
                    "Quality plate. No second Quality mint."
                )
                row["v01_quality"] = "Quality"
                row["reuse_measurement"] = {
                    "source_row": parent,
                    "source_clip_usable_s": CLIP_USE_S,
                    "source_used_s": round(CLIP_USE_S - meas_q["unused_usable_s"], 2),
                    "unused_usable_s": meas_q["unused_usable_s"],
                    "required_use_s": meas_q["required_use_s"],
                    "shortfall_usable_s": meas_q["shortfall_usable_s"],
                    "distinct_window": False,
                    "resolution": "edit-hold",
                }
                row["quality_continuation"] = {
                    **meas_q,
                    "kept_as": "edit-hold of the parent. Shortfall 0.06 s. No second Quality mint.",
                }
                row["generation_authorized"] = False
                row.pop("i2v_from", None)

        board["mint"] = False
        board["status"] = "BOARD_V02_PARKED_FOR_CHIEF"
        board["house"] = (
            "STUDIO_PLAYBOOK.md §5. v02 applies the J0314 price-pass conditions (J0334, "
            "16 Oct 2026, _build_plate_boards_v02.py) on the v01 boards. Timings stay on "
            "the locked VO. Nothing here is generation_authorized. No mint."
        )

    # Price in film order. Untouched mint rows keep their v01 try-1 and expected.
    cum_flow = 0
    cum_vx = 0.0
    for n, board in enumerate(boards, start=1):
        for row in board["plates"]:
            key = f"P{n}:{row['id']}"
            if key in FAST_MINTS:
                need = min(row["use_s"] + 0.5, 8.0)
                priced = price_mint("Fast", need)
            elif key == ASARO or row.get("route_kind") == "edit-hold":
                priced = zero_route("edit-hold")
            elif row["quality"] == "reuse":
                priced = zero_route("reuse")
            elif row["quality"] == "code_graphic":
                priced = zero_route("code-graphic")
            else:
                priced = {
                    "route": row["route"],
                    "flow_model": row["flow_model"],
                    "flow_clip_s": row["flow_clip_s"],
                    "flow_credits_try1": row["flow_credits_try1"],
                    "flow_credits_expected": row["flow_credits_expected"],
                    "vertex_model": row["vertex_model"],
                    "vertex_clip_s": row["vertex_clip_s"],
                    "vertex_try1_gbp": row["vertex_try1_gbp"],
                    "vertex_expected_gbp": row["vertex_expected_gbp"],
                }
            cum_flow, cum_vx = apply_price(row, priced, cum_flow, cum_vx)
            if row.get("generation_authorized"):
                raise SystemExit(f"{key} is generation_authorized")

    per_part = []
    totals = {k: 0 for k in (
        "rows", "Quality", "Fast", "code_graphic", "edit_hold", "reuse", "added",
        "flow_credits_try1", "flow_credits_expected")}
    totals["vertex_try1_gbp"] = 0.0
    totals["vertex_expected_gbp"] = 0.0
    totals["explorer"] = 0
    for n, board in enumerate(boards, start=1):
        rows = board["plates"]
        counts = {
            "rows": len(rows),
            "Quality": sum(r["quality"] == "Quality" for r in rows),
            "Fast": sum(r["quality"] == "Fast" for r in rows),
            "code_graphic": sum(r["quality"] == "code_graphic" for r in rows),
            "edit_hold": sum(r.get("route") == "edit-hold" for r in rows),
            "reuse": sum(r["quality"] == "reuse" and r.get("route") == "reuse" for r in rows),
            "added": sum(bool(r.get("added")) for r in rows),
        }
        ne = sum(bool(r["explorer"]) for r in rows)
        board["explorer_plates"] = ne
        board["counts"] = counts
        (OUT / f"part-{n:02d}_plates_v02.json").write_text(
            json.dumps(board, indent=2, ensure_ascii=False) + "\n")
        pp = dict(counts)
        pp["part"] = n
        pp["flow_credits_try1"] = sum(r["flow_credits_try1"] for r in rows)
        pp["flow_credits_expected"] = sum(r["flow_credits_expected"] for r in rows)
        pp["vertex_try1_gbp"] = round(sum(r["vertex_try1_gbp"] for r in rows), 2)
        pp["vertex_expected_gbp"] = round(sum(r["vertex_expected_gbp"] for r in rows), 2)
        per_part.append(pp)
        for f in ("rows", "Quality", "Fast", "code_graphic", "edit_hold", "reuse", "added",
                  "flow_credits_try1", "flow_credits_expected"):
            totals[f] += pp[f]
        totals["vertex_try1_gbp"] += pp["vertex_try1_gbp"]
        totals["vertex_expected_gbp"] += pp["vertex_expected_gbp"]
        totals["explorer"] += ne
        print(f"part {n:02d}: {pp['rows']} rows = {pp['Quality']} Q + {pp['Fast']} F + "
              f"{pp['code_graphic']} code + {pp['edit_hold']} hold + {pp['reuse']} reuse; "
              f"Flow {pp['flow_credits_expected']} · Vertex £{pp['vertex_expected_gbp']:.2f}")

    totals["vertex_try1_gbp"] = round(totals["vertex_try1_gbp"], 2)
    totals["vertex_expected_gbp"] = round(totals["vertex_expected_gbp"], 2)
    if totals["code_graphic"] != 13:
        raise SystemExit(f"code graphics {totals['code_graphic']} != 13")
    if totals["edit_hold"] != 1:
        raise SystemExit(f"edit-holds {totals['edit_hold']} != 1")
    usable_vx = round(VERTEX_BALANCE_GBP - VERTEX_MARGIN_GBP, 2)
    reserved_sum = sum(RESERVED.values())
    left_after_reserved = FLOW_CREDITS_LEFT - reserved_sum
    need_to_mint = totals["flow_credits_expected"] + HEADROOM_FLOOR
    fits_flow_alone = totals["flow_credits_expected"] <= FLOW_CREDITS_LEFT
    fits_vertex = totals["vertex_expected_gbp"] <= usable_vx
    fits_order = left_after_reserved >= need_to_mint

    v01 = json.loads((EDIT / "PICTURE_PLAN_v01.json").read_text())
    departures = list(v01["departures_from_shot_list"]) + [
        "v02: P1:03_bench_three_c1, P5:07_deccan_note_c1 and P5:07_deccan_note_c2 are own Fast mints. Their shortfalls (2.6 s, 6.22 s, 6.22 s) would leave a picture hole.",
        "v02: P3:08_asaro_michel_c1 is an edit-hold of its parent. The shortfall is 0.06 s, so it is not a second Quality mint.",
        "v02: the 13 teach diagrams stay £0 code graphics. No row is generation_authorized.",
    ]
    plan = {
        "film": "010_Alvarez-Clay-Line-Dinosaurs",
        "written": "2026-10-16",
        "task": "J0334: plate boards v02 from the J0314 price-pass conditions. Flow-first. Mint nothing. Parked for Chief.",
        "shot_list": "07_Edit-Project/SHOT_LIST_v01.md",
        "vo": v01["vo"],
        "from": "part-0N_plates_v01.json. Spoken lines, t_s and use_s are unchanged.",
        "readings": v01["readings"],
        "rates": v01["rates"],
        "vo_film_total_s": v01["vo_film_total_s"],
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
        "mint_order": "006 > 007 > 008 > 009 tranche 1 > 010. 009 tranche 2 (5180) waits for the ~12 Nov renewal and is not reserved here. This board does not mint.",
        "departures_from_shot_list": departures,
    }
    (EDIT / "PICTURE_PLAN_v02.json").write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")

    holds = []
    fasts = []
    qcont = []
    for n, board in enumerate(boards, start=1):
        for row in board["plates"]:
            key = f"P{n}:{row['id']}"
            if row.get("route") == "edit-hold":
                m = row["reuse_measurement"]
                holds.append((key, row["use_s"], m["source_row"], m["unused_usable_s"], m["shortfall_usable_s"]))
            if key in FAST_MINTS:
                m = row["reuse_measurement"]
                fasts.append((key, row["use_s"], m["source_row"], m["shortfall_usable_s"],
                              row["flow_credits_try1"], row["flow_credits_expected"]))
            qc = row.get("quality_continuation")
            if qc and row["quality"] == "Quality":
                qcont.append((key, row["use_s"], qc["source_row"], qc["unused_usable_s"], qc["shortfall_usable_s"]))

    lines = [
        "# 010 price review v02",
        "",
        "Cursor, 16 Oct 2026, J0334. Boards only. **No mint. No spend. No merge.**",
        "v02 applies the J0314 Chief price-pass conditions on the v01 boards. Parked for Chief.",
        "",
        "Locked VO: Chief KEEP, desk #180 comment 6101773293. Timings are the v01 times. "
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
        f"v01 was 48 Quality, 7 Fast, 3 edit-hold, Flow expected 12,572, Vertex expected £146.88.",
        f"v02 is {totals['Quality']} Quality, {totals['Fast']} Fast, {totals['edit_hold']} edit-hold, "
        f"Flow expected **{totals['flow_credits_expected']}**, Vertex expected £{totals['vertex_expected_gbp']:.2f}.",
        "",
        f"All on Flow, if 010 minted alone: {'FITS' if fits_flow_alone else 'DOES NOT FIT'} "
        f"({totals['flow_credits_expected']} expected vs {FLOW_CREDITS_LEFT} left).",
        f"All on Vertex: DOES NOT FIT (£{totals['vertex_expected_gbp']:.2f} expected vs £{usable_vx:.2f} usable). Not authorised.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010. This board does not mint. 010 mints only when a live Flow reading "
        f"covers {totals['flow_credits_expected']} plus at least {HEADROOM_FLOOR} after the reserved expected "
        "for 006–009 and authorised OWB Flow (028).",
        "",
        "| Reserved | Flow expected | Source |",
        "|---|---:|---|",
        "| 006 | 0 | KEEPs, J0331 |",
        "| 007 | 7196 | J0322 price pass |",
        "| 008 | 5605 | boards v03 |",
        "| 009 tranche 1 | 7354 | boards v04 |",
        "| 028 (OWB) | 279 | authorised Flow, two Veo plates |",
        f"| **Sum** | **{reserved_sum}** | |",
        "",
        "009 tranche 2 is 5,180 and is not in the sum. It waits for the ~12 Nov renewal.",
        "",
        f"On the {FLOW_READ_AT} reading, {FLOW_CREDITS_LEFT} − {reserved_sum} leaves **{left_after_reserved}**. "
        f"010 needs {totals['flow_credits_expected']} + {HEADROOM_FLOOR} = **{need_to_mint}**. "
        f"{'FITS' if fits_order else 'DOES NOT FIT'} today "
        f"(short by {need_to_mint - left_after_reserved}).",
        "",
        "Rates are unchanged: Flow Fast 10 / Quality 100 a take; expected uses 005's takes-per-KEEP "
        "(Quality 2.59, Fast 1.96) plus stills. Vertex is list price, 1080p, £0.80 per dollar, clip length 4/6/8 s.",
        "",
        "## 1. Teach diagrams → £0 code graphics",
        "",
        f"{totals['code_graphic']} rows. Unchanged. Flow and Vertex are 0.",
        "",
        "## 2. Fast holes → own Fast mints",
        "",
        "These three are no longer edit-holds. Each is its own Fast mint. Try-1 is 10, expected is 20.",
        "",
        "| Row | Needed s | Parent | Shortfall s | Try-1 | Expected |",
        "|---|---:|---|---:|---:|---:|",
    ]
    for key, need, parent, gap, try1, exp in fasts:
        lines.append(f"| {key} | {need} | {parent} | {gap} | {try1} | {exp} |")
    lines += [
        "",
        "## 3. Quality continuations",
        "",
        "Each stays a second Quality mint where the shortfall is real.",
        "",
        "| Row | Needed s | Parent | Unused usable s | Shortfall s |",
        "|---|---:|---|---:|---:|",
    ]
    for key, need, parent, unused, gap in qcont:
        lines.append(f"| {key} | {need} | {parent} | {unused} | {gap} |")
    lines += [
        "",
        "Exception: P3:08_asaro_michel_c1, shortfall 0.06 s, is an edit-hold of P3:08_asaro_michel. "
        "It is not in the table above and it is not priced.",
        "",
        "## 4. Edit-hold",
        "",
        "| Row | Needed s | Parent | Unused usable s | Shortfall s |",
        "|---|---:|---|---:|---:|",
    ]
    for key, need, parent, unused, gap in holds:
        lines.append(f"| {key} | {need} | {parent} | {unused} | {gap} |")
    lines += ["", "## What changed against the shot list", ""]
    for item in departures:
        lines.append(f"- {item}")
    lines += [
        "",
        "## For the Chief",
        "",
        "Parked for Chief: 010 plate boards v02. No mint, no spend, no merge. "
        "Vertex stays unauthorised. generation_authorized is false on every row.",
        "",
    ]
    (EDIT / "PRICE_REVIEW_v02.md").write_text("\n".join(lines))
    print(f"film Flow {totals['flow_credits_expected']}  Vertex £{totals['vertex_expected_gbp']:.2f}")
    print(f"reserved {reserved_sum}  left {left_after_reserved}  need {need_to_mint}  "
          f"{'FIT' if fits_order else 'SHORT'}")


if __name__ == "__main__":
    main()
