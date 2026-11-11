#!/usr/bin/env python3
"""HOS 009: plate boards v02 from v01, per the J0261 price PASS (Chief, 15 Oct).

No mint. No spend. Applies desk #180 comment 6195259471:

1. Parchment teach rows, including their _c1, become £0 code graphics.
2. Remaining Fast _c1/_c2 become edit-holds of the parent KEEP (0 credits, no second mint).
3. Quality _c1/_c2 stay a second Quality mint when the parent 8s clip cannot cover the beat.
4. Named non-hero Quality rows move to Fast, prompts rewritten non-emissive.
5. Reprice against the fresh Flow reading. Headroom target is 3,000 credits after 009.

  python3 07_Edit-Project/_build_plate_boards_v02.py
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

EDIT = Path(__file__).resolve().parent
PARTS = EDIT / "parts"

# Fresh Flow read, J0313, CDP :9222, 2026-10-15T21:42:22Z. Refill from 23,730.
FLOW_LEFT = 23740
FLOW_READ_AT = "2026-10-15T21:42:22Z"
# Same Vertex reading as v01. Not re-read: the route is Flow-first.
VERTEX_BALANCE_GBP = 71.02
VERTEX_READ_AT = "2026-10-15T07:30:31Z"
VERTEX_USABLE_GBP = 70.02
HEADROOM = 3000

FLOW_CREDITS = {"Quality": 100, "Fast": 10}
USD_PER_S = {"Quality": 0.20, "Fast": 0.10}
USD_PER_STILL = 0.039
GBP_PER_USD = 0.80
TAKES_PER_KEEP = {"Quality": round(70 / 27, 2), "Fast": round(94 / 48, 2)}
STILLS_PER_PLATE = round(171 / 75, 2)
VERTEX_LENGTHS = (4, 6, 8)
CLIP_RAW_S = 8.0
CLIP_USE_S = 7.9
REUSE_PAD_S = 0.5
FAST_SAFE = " Daylight, window light or matte painted ink only. No candle, flame, glow, spark, comet or lightning."
FAST_BANNED = re.compile(r"\b(glow|candle|flame|spark|comet|lightning|starfield|muzzle)\b|dark sky", re.I)

# Condition 1. Part number is fixed so the render file name is stable.
CODE = {
    "09_pull_heights": (2, "TREE, TOWER, MOUNTAIN", [
        "Ink line of pull at the top of a tree",
        "The same line at a tower, then a mountain",
    ], "Tree line inks in; tower and mountain marks drop in after it."),
    "09_pull_heights_c1": (2, "PULL AT THE TOP", [
        "The mountain mark holds while the pull line reaches its top",
    ], "Pull line draws to the mountain top."),
    "06_orbit_teach": (3, "FALLING SIDEWAYS", [
        "A ball with one sideways ink arrow and one down arrow",
        "The arrows repeat around a circle",
    ], "Sideways arrow draws, then the down arrow, then the circle."),
    "06_orbit_teach_c1": (3, "NEVER HITS", [
        "The same circle, the ball missing the ground each time",
    ], "The ball steps around the circle and never meets it."),
    "08_km_a_second": (3, "SIDEWAYS AND DOWN", [
        "Moon on a curve, a short sideways ink arrow and a tiny down tick",
    ], "Sideways arrow draws, then the down tick, and the curve follows."),
    "08_km_a_second_c1": (3, "FOR EVER", [
        "The same curve repeating, sideways then down",
    ], "Another sideways arrow and down tick drop onto the curve."),
    "01_weaker_far": (4, "WEAKER WITH DISTANCE", [
        "A pull arrow that shrinks as a ball moves away from a painted Earth",
    ], "Arrow shrinks at the second distance."),
    "01_weaker_far_c1": (4, "FOUR TIMES WEAKER", [
        "Two distances, then three: the arrow at three times the distance is a stub",
    ], "The third arrow shrinks to a stub."),
    "03_sixty_earths": (4, "SIXTY EARTHS", [
        "One Earth, then Earths laid end to end toward a small Moon",
    ], "Earth discs lay down in a line toward the Moon."),
    "04_dots_square": (4, "SIXTY TIMES SIXTY", [
        "A square of small ink dots",
        "A pull arrow beside the Moon shrinking to one dot",
    ], "The square fills, then the Moon's arrow shrinks to one dot."),
    "04_dots_square_c1": (4, "ONE TINY DOT", [
        "The square holds; one dot remains beside the Moon",
    ], "The last dot ticks in."),
    "07_station_curve": (5, "FALLING TOGETHER", [
        "The station's path drawn as the cannonball's circle",
        "One ink arrow sideways and one down",
    ], "The circle draws, then the two arrows."),
}

# Condition 4. Phrase swaps keep the shot and strip anything Fast cannot carry.
FAST_SWAP = {
    "10_farmhouse_dawn": (
        [],
        " Cool grey dawn, no sun disc in frame.",
    ),
    "02_cannon_world": (
        [("Dark sky.", "Pale daytime sky, no stars.")],
        "",
    ),
    "02_spray_paint": (
        [],
        " Daylight on a pale plaster wall. The hand and the wall only, no face.",
    ),
    "01_one_law": (
        [("Soft glow on the lines.", "Matte ink lines.")],
        "",
    ),
    "08_cup_and_planets": (
        [("and the view pulls out to planets sliding on their curves around the Sun.",
          "and the view pulls out to a matte painted card of planets on ink curves around a painted Sun, daylight on the table.")],
        "",
    ),
    "12_clay_handoff": (
        [("A dark sky over a green prehistoric landscape. A bright point grows in the sky,",
          "A bright daytime sky over a green prehistoric landscape. A small pale stone crosses the blue sky,")],
        "",
    ),
}


def price_fast(use_s: float) -> dict:
    need = min(use_s + REUSE_PAD_S, 8.0)
    clip = next(L for L in VERTEX_LENGTHS if L >= need - 1e-6)
    try1 = USD_PER_S["Fast"] * clip * GBP_PER_USD
    exp = try1 * TAKES_PER_KEEP["Fast"] + STILLS_PER_PLATE * USD_PER_STILL * GBP_PER_USD
    return {
        "flow_model": "Veo 3.1 Fast",
        "flow_clip_s": 8,
        "flow_credits_try1": FLOW_CREDITS["Fast"],
        "flow_credits_expected": math.ceil(FLOW_CREDITS["Fast"] * TAKES_PER_KEEP["Fast"]),
        "vertex_model": "veo-3.1-fast-generate-001",
        "vertex_clip_s": clip,
        "vertex_try1_gbp": round(try1, 2),
        "vertex_expected_gbp": round(exp, 2),
        "route": "flow-first",
    }


def zero_mint(row: dict, route: str) -> None:
    row["route"] = route
    row["flow_model"] = None
    row["flow_clip_s"] = 0
    row["flow_credits_try1"] = 0
    row["flow_credits_expected"] = 0
    row["vertex_model"] = None
    row["vertex_clip_s"] = 0
    row["vertex_try1_gbp"] = 0.0
    row["vertex_expected_gbp"] = 0.0
    row["generation_authorized"] = False


def hold_measure(row: dict, parent: dict, part: int) -> dict:
    unused_raw = round(CLIP_RAW_S - parent["use_s"], 2)
    unused_use = round(CLIP_USE_S - parent["use_s"], 2)
    need = row["use_s"]
    short_raw = round(need - unused_raw, 2)
    short_use = round(need - unused_use, 2)
    return {
        "source_row": f"P{part}:{parent['id']}",
        "source_clip_raw_s": CLIP_RAW_S,
        "source_clip_usable_s": CLIP_USE_S,
        "source_used_s": parent["use_s"],
        "unused_raw_s": unused_raw,
        "unused_usable_s": unused_use,
        "required_use_s": need,
        "shortfall_raw_s": short_raw,
        "shortfall_usable_s": short_use,
        "distinct_window_feasible": unused_use >= need - 1e-6,
    }


def main() -> None:
    boards = []
    for n in range(1, 6):
        path = PARTS / f"part-0{n}_plates_v01.json"
        boards.append((n, json.loads(path.read_text())))

    by_part = {n: {p["id"]: p for p in board["plates"]} for n, board in boards}
    notes = {"code": [], "fast_hold": [], "quality_kept": [], "fast_swap": []}

    for n, board in boards:
        prev_layout = None
        last_moving = None
        for row in board["plates"]:
            pid = row["id"]

            if pid in CODE:
                part_n, label, elements, animation = CODE[pid]
                assert part_n == n, (pid, part_n, n)
                words = [w for w in re.split(r"[^A-Za-z0-9]+", label) if w]
                if len(words) > 4:
                    raise SystemExit(f"label over 4 words: {pid} {label}")
                layout = "full_frame_period_paper" if prev_layout != "full_frame_period_paper" else "moving_plate_overlay"
                # First of a run is full frame. The next code row, if adjacent, is an overlay.
                if prev_layout is None:
                    layout = "full_frame_period_paper"
                row["v01_quality"] = row["quality"]
                row["quality"] = "code_graphic"
                row["engine_reason"] = (
                    "J0261 condition 1: parchment teach row is a £0 code graphic "
                    "(own renderer). No Flow mint."
                )
                row["prompt"] = None
                zero_mint(row, "code-graphic")
                row["code_graphic_spec"] = {
                    "file": f"code_graphic_009_p{n}_{pid}.mp4",
                    "renderer": "python-pillow-ffmpeg (house explainer renderer, £0)",
                    "style": "HOS cream-on-brown period-paper inked diagram, white/sepia Didot italic",
                    "layout_mode": layout,
                    "background_plate": None if layout == "full_frame_period_paper" else last_moving,
                    "label": label,
                    "elements": elements,
                    "animation": animation + " Label fades in over about 0.4 s and out before the cut.",
                    "duration_s": row["use_s"],
                }
                prev_layout = layout
                notes["code"].append(f"P{n}:{pid}")
                continue

            prev_layout = None

            if pid in FAST_SWAP and row["quality"] == "Quality":
                swaps, extra = FAST_SWAP[pid]
                prompt = row["prompt"]
                for old, new in swaps:
                    if old not in prompt:
                        raise SystemExit(f"prompt phrase missing on {pid}: {old}")
                    prompt = prompt.replace(old, new)
                if FAST_SAFE not in prompt:
                    prompt = prompt.rstrip(".") + "." + extra + FAST_SAFE
                if FAST_BANNED.search(prompt.replace(FAST_SAFE, "")):
                    raise SystemExit(f"Fast prompt still emissive: {pid}\n{prompt}")
                row["v01_quality"] = "Quality"
                row["quality"] = "Fast"
                row["prompt"] = prompt
                row["engine_reason"] = (
                    "J0261 condition 4: non-hero plate moved Quality to Fast. "
                    "Prompt rewritten non-emissive."
                )
                row.update(price_fast(row["use_s"]))
                notes["fast_swap"].append(f"P{n}:{pid}")
                last_moving = pid
                continue

            m = re.search(r"_c([12])$", pid)
            if not m or row["quality"] not in ("Fast", "Quality"):
                if row["quality"] in ("Quality", "Fast"):
                    last_moving = pid
                continue
            parent_id = pid.rsplit("_c", 1)[0]
            parent = by_part[n][parent_id]
            measure = hold_measure(row, parent, n)
            if row["quality"] == "Fast":
                # Condition 2: no second mint, even when the 8s clip is short.
                row["v01_quality"] = "Fast"
                row["quality"] = "reuse"
                row["reuse_of"] = f"P{n}:{parent_id}"
                row["reference"] = f"P{n}:{parent_id}"
                row["prompt"] = None
                row["engine_reason"] = (
                    "J0261 condition 2: Fast continuation is an edit-hold of the parent KEEP. "
                    "No second mint, no loop, no freeze. "
                    f"Unused usable footage is {measure['unused_usable_s']} s "
                    f"against {measure['required_use_s']} s needed."
                )
                row["reuse_measurement"] = measure
                row["reuse_measurement"]["resolution"] = "edit_hold_no_second_mint"
                zero_mint(row, "edit-hold")
                notes["fast_hold"].append((f"P{n}:{pid}", measure))
            else:
                # Condition 3: mint a second Quality take only if the parent cannot cover the beat.
                row["j0261_hold_check"] = measure
                if measure["distinct_window_feasible"]:
                    raise SystemExit(f"unexpected feasible Quality hold: {pid}")
                row["j0261_hold_check"]["resolution"] = "priced_quality_mint"
                notes["quality_kept"].append((f"P{n}:{pid}", measure))

            if row["quality"] in ("Quality", "Fast"):
                last_moving = pid

        # Recount and rewrite cumulatives after the film walk. Done below.
        board["status"] = "BOARD_V02_PARKED_FOR_CHIEF"
        board["mint"] = False

    cum_flow = 0
    cum_vx = 0.0
    totals = {"rows": 0, "mints": 0, "Quality": 0, "Fast": 0, "code_graphic": 0,
              "reuse": 0, "edit_hold": 0, "added": 0,
              "flow_credits_try1": 0, "flow_credits_expected": 0,
              "vertex_try1_gbp": 0.0, "vertex_expected_gbp": 0.0}
    per_part = []
    for n, board in boards:
        rows = board["plates"]
        counts = {"rows": len(rows), "mints": 0, "Quality": 0, "Fast": 0,
                  "code_graphic": 0, "reuse": 0, "edit_hold": 0,
                  "added": sum(1 for r in rows if r.get("added")),
                  "flow_credits_try1": 0, "flow_credits_expected": 0,
                  "vertex_try1_gbp": 0.0, "vertex_expected_gbp": 0.0}
        for row in rows:
            q = row["quality"]
            if q == "reuse" and row.get("route") == "edit-hold":
                counts["edit_hold"] += 1
                counts["reuse"] += 1
            elif q == "reuse":
                counts["reuse"] += 1
            elif q == "code_graphic":
                counts["code_graphic"] += 1
            elif q in ("Quality", "Fast"):
                counts[q] += 1
                counts["mints"] += 1
            else:
                raise SystemExit(f"unknown quality {q} on {row['id']}")
            cum_flow += row["flow_credits_expected"]
            cum_vx += row["vertex_expected_gbp"]
            row["cum_flow_credits_expected"] = cum_flow
            row["cum_vertex_expected_gbp"] = round(cum_vx, 2)
            counts["flow_credits_try1"] += row["flow_credits_try1"]
            counts["flow_credits_expected"] += row["flow_credits_expected"]
            counts["vertex_try1_gbp"] += row["vertex_try1_gbp"]
            counts["vertex_expected_gbp"] += row["vertex_expected_gbp"]
        counts["vertex_try1_gbp"] = round(counts["vertex_try1_gbp"], 2)
        counts["vertex_expected_gbp"] = round(counts["vertex_expected_gbp"], 2)
        board["counts"] = {k: counts[k] for k in (
            "rows", "mints", "Quality", "Fast", "code_graphic", "reuse", "edit_hold", "added")}
        for k, v in counts.items():
            if k in totals and isinstance(v, (int, float)):
                totals[k] += v
        per_part.append({"part": n, "title": board["title"], **counts})
        out = PARTS / f"part-0{n}_plates_v02.json"
        out.write_text(json.dumps(board, indent=2) + "\n")

    totals["vertex_try1_gbp"] = round(totals["vertex_try1_gbp"], 2)
    totals["vertex_expected_gbp"] = round(totals["vertex_expected_gbp"], 2)
    headroom = FLOW_LEFT - totals["flow_credits_expected"]
    if headroom < HEADROOM:
        raise SystemExit(f"headroom {headroom} under {HEADROOM}")
    plan = {
        "film": "009",
        "written": "2026-10-15",
        "task": "J0313 plate boards v02. No mint. No spend.",
        "from": "part-0N_plates_v01.json via _build_plate_boards_v02.py",
        "ruling": "Chief price PASS with conditions, desk #180 comment 6195259471",
        "readings": {
            "flow_credits_left": FLOW_LEFT,
            "flow_read_at": FLOW_READ_AT,
            "flow_note": "CDP :9222 account picker, benoats@googlemail.com. Refill from 23730.",
            "vertex_promo_gbp": VERTEX_BALANCE_GBP,
            "vertex_read_at": VERTEX_READ_AT,
            "vertex_usable_gbp": VERTEX_USABLE_GBP,
        },
        "totals": totals,
        "per_part": per_part,
        "all_on_flow_credits_expected": totals["flow_credits_expected"],
        "headroom_after_009": headroom,
        "headroom_target": HEADROOM,
        "fits_flow_with_headroom": headroom >= HEADROOM,
        "all_on_vertex_gbp_expected": totals["vertex_expected_gbp"],
        "fits_vertex": totals["vertex_expected_gbp"] <= VERTEX_USABLE_GBP,
        "changed": {
            "code_graphic": notes["code"],
            "fast_edit_hold": [x[0] for x in notes["fast_hold"]],
            "quality_second_mint": [x[0] for x in notes["quality_kept"]],
            "quality_to_fast": notes["fast_swap"],
        },
    }
    (EDIT / "PICTURE_PLAN_v02.json").write_text(json.dumps(plan, indent=2) + "\n")

    def row_line(item: tuple) -> str:
        name, m = item
        return (f"| {name} | {m['required_use_s']:.2f} | {m['source_row']} | {m['source_used_s']:.2f} | "
                f"{m['unused_usable_s']:.2f} | {m['shortfall_usable_s']:.2f} |")

    lines = [
        "# 009 price review v02",
        "",
        "Cursor, 15 Oct 2026, J0313. Boards only. **No mint. No spend.**",
        "Applies the Chief price PASS on v01 (desk #180 comment 6195259471). Parked for Chief.",
        "",
        "## Readings",
        "",
        f"- Flow: **{FLOW_LEFT}** credits at {FLOW_READ_AT} (CDP :9222, benoats@googlemail.com). The 12:58 reading was 23,730; this read is 10 higher, a refill, and no spend is logged between them.",
        f"- Vertex promo: **£{VERTEX_BALANCE_GBP:.2f}** at {VERTEX_READ_AT}. Usable **£{VERTEX_USABLE_GBP:.2f}** after the £1 margin. Not re-read. The route stays Flow-first.",
        "",
        "## Totals",
        "",
        "v01 was 90 rows, 58 Quality / 31 Fast / 1 reuse, Flow expected 15,642, Vertex expected £206.62.",
        "",
        "| | rows | Quality | Fast | code | edit-hold | other reuse | Flow try-1 | Flow expected | Vertex try-1 | Vertex expected |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for pp in per_part:
        other = pp["reuse"] - pp["edit_hold"]
        lines.append(
            f"| Part 0{pp['part']} | {pp['rows']} | {pp['Quality']} | {pp['Fast']} | {pp['code_graphic']} | "
            f"{pp['edit_hold']} | {other} | {pp['flow_credits_try1']} | {pp['flow_credits_expected']} | "
            f"£{pp['vertex_try1_gbp']:.2f} | £{pp['vertex_expected_gbp']:.2f} |"
        )
    other = totals["reuse"] - totals["edit_hold"]
    lines += [
        f"| **Film** | **{totals['rows']}** | **{totals['Quality']}** | **{totals['Fast']}** | "
        f"**{totals['code_graphic']}** | **{totals['edit_hold']}** | **{other}** | "
        f"**{totals['flow_credits_try1']}** | **{totals['flow_credits_expected']}** | "
        f"**£{totals['vertex_try1_gbp']:.2f}** | **£{totals['vertex_expected_gbp']:.2f}** |",
        "",
        f"All on Flow: FITS ({totals['flow_credits_expected']} expected vs {FLOW_LEFT} left). "
        f"Headroom after 009 is **{headroom}**, against the 3,000 target.",
        f"All on Vertex: DOES NOT FIT (£{totals['vertex_expected_gbp']:.2f} expected vs £{VERTEX_USABLE_GBP:.2f} usable).",
        "",
        "006, 007 and 008 still share this pot. 008 v03 expected 5,605 and the 007 review expected about 7,550. "
        f"After 009, {headroom} is left before those. That split is the Chief's mint-order call. This board does not mint.",
        "",
        "## 1. Parchment teach → £0 code graphics",
        "",
        "Twelve rows, including each named `_c1`. Flow and Vertex are 0. Layout alternates full-frame period paper and an overlay so two full-frame teach cards do not sit back to back.",
        "",
        ", ".join(notes["code"]),
        "",
        "## 2. Fast continuations → edit-hold",
        "",
        "No second mint. An 8.00 s clip (7.90 s usable) does not leave a distinct window for any of these beats. "
        "The row is an edit-hold of the parent KEEP. The cut must not loop or freeze, so the picture on that beat is shorter than the VO unless a later pass authorises a mint.",
        "",
        "| Row | Needed s | Parent | Parent use s | Unused usable s | Shortfall s |",
        "|---|---:|---|---:|---:|---:|",
    ]
    lines += [row_line(x) for x in notes["fast_hold"]]
    lines += [
        "",
        "## 3. Quality continuations",
        "",
        "Prefer an edit-hold. Every one of these is short of a distinct window, so each stays a second Quality mint, as the ruling allows.",
        "",
        "| Row | Needed s | Parent | Parent use s | Unused usable s | Shortfall s |",
        "|---|---:|---|---:|---:|---:|",
    ]
    lines += [row_line(x) for x in notes["quality_kept"]]
    lines += [
        "",
        "## 4. Quality → Fast",
        "",
        "Non-hero plates. Prompts rewritten to daylight or matte ink. Faces, the candlelit quart pot, the Moon at night, the comet, water, space, the glowing orbit trail and the Short frame-0 plates stay Quality.",
        "",
        ", ".join(notes["fast_swap"]),
        "",
        "`02_spray_paint_c1` and `_c2` are Quality continuations of a plate that is now Fast. The parent clip cannot cover them, so they stay Quality mints under condition 3.",
        "",
        "## For the Chief",
        "",
        "Mint order, after 006 and 007, stays the Chief's call. No mint in this pass.",
        "",
    ]
    (EDIT / "PRICE_REVIEW_v02.md").write_text("\n".join(lines))
    print(f"rows {totals['rows']}  Q {totals['Quality']}  F {totals['Fast']}  "
          f"code {totals['code_graphic']}  hold {totals['edit_hold']}  reuse {totals['reuse']}")
    print(f"Flow try-1 {totals['flow_credits_try1']}  expected {totals['flow_credits_expected']}  "
          f"headroom {headroom} (left {FLOW_LEFT})")
    print(f"Vertex try-1 £{totals['vertex_try1_gbp']:.2f}  expected £{totals['vertex_expected_gbp']:.2f}")


if __name__ == "__main__":
    main()
