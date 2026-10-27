#!/usr/bin/env python3
"""HOS 009: plate boards v04 from v03. J0335, Chief FIX on J0333.

No mint. No spend. No merge.

1. Six continuations sit on Fast parents but were priced as second Quality
   mints. A Quality cut against a Fast parent jumps look. Each becomes its
   own Fast mint: new angle or move, parent's look, 20 expected, tranche 1.
2. The closer (P5:10_explorer_bench) mints in tranche 1. The two short
   Quality parents between £0 code graphics wait in tranche 2 instead.
   If tranche 2 slips, hold or extend that neighbouring code graphic.

  python3 07_Edit-Project/_build_plate_boards_v04.py
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

EDIT = Path(__file__).resolve().parent
PARTS = EDIT / "parts"

# Same reading as v02 and v03. This pass does not re-read Flow and does not spend.
FLOW_LEFT = 23740
FLOW_READ_AT = "2026-10-15T21:42:22Z"
VERTEX_BALANCE_GBP = 71.02
VERTEX_READ_AT = "2026-10-15T07:30:31Z"
VERTEX_USABLE_GBP = 70.02
HEADROOM = 3000
FLOW_007 = 7550
FLOW_008 = 5605
TRANCHE1_CAP = FLOW_LEFT - FLOW_007 - FLOW_008 - HEADROOM

FLOW_CREDITS = {"Quality": 100, "Fast": 10}
USD_PER_S = {"Quality": 0.20, "Fast": 0.10}
USD_PER_STILL = 0.039
GBP_PER_USD = 0.80
TAKES_PER_KEEP = {"Quality": round(70 / 27, 2), "Fast": round(94 / 48, 2)}
STILLS_PER_PLATE = round(171 / 75, 2)
VERTEX_LENGTHS = (4, 6, 8)
FAST_BANNED = re.compile(
    r"\b(glow|candle|flame|spark|comet|lightning|starfield|muzzle)\b|dark sky",
    re.I,
)

# Own Fast mints on a Fast parent. New angle or move, same objects and light.
MATCH_FAST = {
    (4, "02_spray_paint_c1"): (
        "From the side of the same pale plaster wall, the hand steps back. "
        "Daylight. The small dark spot of paint spreads into a wider, paler patch "
        "as the hand moves away. The hand and the wall only, no face."
    ),
    (4, "02_spray_paint_c2"): (
        "The camera drops to the height of the pale plaster wall and tracks along "
        "the edge of the wider pale patch. The same hand finishes and lowers. "
        "Daylight. The hand and the wall only, no face."
    ),
    (5, "01_one_law_c1"): (
        "The camera tilts across the same painted card, from the painted Sun out "
        "along one matte ink line to a planet, then on toward Jupiter and its moons. "
        "Matte ink only. Daylight on the card."
    ),
    (5, "08_cup_and_planets_c1"): (
        "A side angle on the same wooden table. The cup is already past the edge "
        "and falling, while the matte painted card of planets on ink curves stays "
        "on the wall behind. Daylight."
    ),
    (5, "08_cup_and_planets_c2"): (
        "From the floor, the camera rises off the fallen cup toward the same painted "
        "card. The painted Sun and the ink curves fill the frame. Daylight on the "
        "table and the card."
    ),
    (5, "12_clay_handoff_c1"): (
        "The camera tracks along the rock face in bright daytime. The same thin pale "
        "band of clay runs across the stone, and above the rock the small pale stone "
        "is already crossing the blue sky. No impact, no fire, no creatures hurt."
    ),
}

# Short Quality parents deferred so the closer stays in tranche 1.
# Slip fallback is a £0 hold or extension of the neighbouring code graphic.
DEFER = {
    (2, "10_how_high"): {
        "neighbours": ["P2:09_pull_heights"],
        "why": (
            "J0335: deferred so the closer P5:10_explorer_bench stays in tranche 1. "
            "Short Quality parent (2.58 s) next to the £0 code graphic P2:09_pull_heights. "
            "If tranche 2 slips, hold or extend that code graphic. No picture hole."
        ),
    },
    (3, "07_ball_to_moon"): {
        "neighbours": ["P3:06_orbit_teach", "P3:08_km_a_second"],
        "why": (
            "J0335: deferred so the closer P5:10_explorer_bench stays in tranche 1. "
            "Short Quality parent (2.84 s) between the £0 code graphics "
            "P3:06_orbit_teach and P3:08_km_a_second. "
            "If tranche 2 slips, hold or extend those code graphics. No picture hole."
        ),
    },
}

CLOSER = (5, "10_explorer_bench")

# J0333 own-Fast rows. They stay Fast in tranche 1.
J0333_FAST = {
    "03_table_three_c1",
    "03_table_three_c2",
    "09_can_he_calculate_c1",
    "06_pretty_nearly_c1",
    "10_write_it_down_c1",
    "03_halley_comet_path_c1",
}

TAIL = (
    " No readable words or numbers anywhere. Silent. Continuous motion through "
    "the final frame. No Explorer. No Orbit."
)


def price_fast(use_s: float) -> dict:
    need = min(use_s + 0.5, 8.0)
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


def is_continuation(pid: str) -> bool:
    return bool(re.search(r"_c[12]$", pid))


def main() -> None:
    boards = []
    for n in range(1, 6):
        path = PARTS / f"part-0{n}_plates_v03.json"
        boards.append((n, json.loads(path.read_text())))

    minted = []
    for n, board in boards:
        by_id = {row["id"]: row for row in board["plates"]}
        for (part_n, pid), beat in MATCH_FAST.items():
            if part_n != n:
                continue
            row = by_id.get(pid)
            if row is None:
                raise SystemExit(f"missing P{n}:{pid}")
            if row.get("quality") != "Quality" or row.get("tranche") != 2:
                raise SystemExit(f"P{n}:{pid} is not a v03 tranche-2 Quality mint")
            parent_id = pid.rsplit("_c", 1)[0]
            parent = by_id.get(parent_id)
            if parent is None or parent.get("quality") != "Fast":
                raise SystemExit(f"P{n}:{pid} parent is not Fast")
            measure = row.get("j0261_hold_check") or row.get("reuse_measurement") or {}
            shortfall = measure.get("shortfall_usable_s")
            if not isinstance(shortfall, (int, float)) or shortfall <= 0:
                raise SystemExit(f"P{n}:{pid} has no positive shortfall")
            prompt = "Premium Animistry-class 3D cartoon. " + beat + TAIL
            if FAST_BANNED.search(prompt):
                raise SystemExit(f"Fast prompt still emissive: P{n}:{pid}\n{prompt}")
            if "same shot continues" in prompt.lower():
                raise SystemExit(f"prompt is still a continuation: P{n}:{pid}")
            row["quality"] = "Fast"
            row["prompt"] = prompt
            row["reference"] = (
                f"same look as P{n}:{parent_id}; own Fast text mint, not an i2v continuation"
            )
            row.pop("i2v_from", None)
            row.pop("reuse_of", None)
            row["engine_reason"] = (
                "J0335 Chief FIX: this continuation sat on a Fast parent but was priced "
                "as a second Quality mint, so the cut would jump look. Own Fast mint, "
                f"new angle or move, same look as P{n}:{parent_id}. "
                f"The parent clip cannot cover the beat (shortfall {shortfall} s usable)."
            )
            if measure:
                measure = dict(measure)
                measure["resolution"] = "own_fast_mint"
                if row.get("j0261_hold_check") is not None:
                    row["j0261_hold_check"] = measure
                else:
                    row["reuse_measurement"] = measure
            row.update(price_fast(row["use_s"]))
            row["generation_authorized"] = False
            row["tranche"] = 1
            row["tranche_why"] = (
                "Own Fast mint so the cut matches the Fast parent. "
                "Tranche 1 with the other Fast plates. J0335."
            )
            row.pop("tranche_moved_from", None)
            minted.append(f"P{n}:{pid}")
        board["status"] = "BOARD_V04_PARKED_FOR_CHIEF"
        board["mint"] = False

    if minted != [f"P{p}:{i}" for (p, i) in MATCH_FAST]:
        raise SystemExit(f"minted {minted}")

    flat = []
    for n, board in boards:
        for row in board["plates"]:
            flat.append((n, row))

    deferred = []
    for n, row in flat:
        key = (n, row["id"])
        if key in DEFER:
            if row["quality"] != "Quality" or is_continuation(row["id"]):
                raise SystemExit(f"P{n}:{row['id']} is not a Quality parent")
            spec = DEFER[key]
            # Neighbours must be £0 code graphics on this board.
            board = next(b for pn, b in boards if pn == n)
            by_id = {r["id"]: r for r in board["plates"]}
            for name in spec["neighbours"]:
                nid = name.split(":", 1)[1]
                nb = by_id.get(nid)
                if nb is None or nb.get("quality") != "code_graphic":
                    raise SystemExit(f"{name} is not a code graphic next to P{n}:{row['id']}")
                if nb.get("flow_credits_expected") != 0:
                    raise SystemExit(f"{name} is not £0")
            row["tranche"] = 2
            row["tranche_why"] = spec["why"]
            row["tranche_moved_from"] = 1
            row["slip_fallback"] = (
                "£0 hold or extension of " + " and ".join(spec["neighbours"])
            )
            deferred.append(f"P{n}:{row['id']}")
        elif key == CLOSER:
            if row["quality"] != "Quality":
                raise SystemExit("closer is not Quality")
            row["tranche"] = 1
            row["tranche_why"] = (
                "J0335: the closer mints in tranche 1, not last. "
                "\"It is falling towards you, right now.\""
            )
            row.pop("tranche_moved_from", None)
            row.pop("slip_fallback", None)

    if deferred != [f"P{p}:{i}" for (p, i) in DEFER]:
        raise SystemExit(f"deferred {deferred}")

    for n, row in flat:
        if (n, row["id"]) == CLOSER and row["tranche"] != 1:
            raise SystemExit("closer left tranche 1")
        if row["id"] in J0333_FAST and (row["tranche"] != 1 or row["quality"] != "Fast"):
            raise SystemExit(f"{row['id']} did not stay a tranche-1 Fast mint")

    cum_flow = 0
    cum_vx = 0.0
    totals = {
        "rows": 0, "mints": 0, "Quality": 0, "Fast": 0, "code_graphic": 0,
        "reuse": 0, "edit_hold": 0, "added": 0,
        "flow_credits_try1": 0, "flow_credits_expected": 0,
        "vertex_try1_gbp": 0.0, "vertex_expected_gbp": 0.0,
    }
    per_part = []
    for n, board in boards:
        rows = board["plates"]
        counts = {
            "rows": len(rows), "mints": 0, "Quality": 0, "Fast": 0,
            "code_graphic": 0, "reuse": 0, "edit_hold": 0,
            "added": sum(1 for r in rows if r.get("added")),
            "flow_credits_try1": 0, "flow_credits_expected": 0,
            "vertex_try1_gbp": 0.0, "vertex_expected_gbp": 0.0,
            "tranche_1": 0, "tranche_2": 0,
            "tranche_1_flow_expected": 0, "tranche_2_flow_expected": 0,
        }
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
            if row["tranche"] in (1, 2):
                counts[f"tranche_{row['tranche']}"] += 1
                counts[f"tranche_{row['tranche']}_flow_expected"] += row["flow_credits_expected"]
        counts["vertex_try1_gbp"] = round(counts["vertex_try1_gbp"], 2)
        counts["vertex_expected_gbp"] = round(counts["vertex_expected_gbp"], 2)
        board["counts"] = {
            k: counts[k] for k in (
                "rows", "mints", "Quality", "Fast", "code_graphic", "reuse", "edit_hold", "added"
            )
        }
        for k, v in counts.items():
            if k in totals and isinstance(v, (int, float)):
                totals[k] += v
        per_part.append({"part": n, "title": board["title"], **counts})
        out = PARTS / f"part-0{n}_plates_v04.json"
        out.write_text(json.dumps(board, indent=2) + "\n")

    totals["vertex_try1_gbp"] = round(totals["vertex_try1_gbp"], 2)
    totals["vertex_expected_gbp"] = round(totals["vertex_expected_gbp"], 2)

    t1_rows = [(n, r) for n, r in flat if r["tranche"] == 1]
    t2_rows = [(n, r) for n, r in flat if r["tranche"] == 2]

    def expected(rows: list) -> int:
        return sum(r["flow_credits_expected"] for _, r in rows)

    def bucket(rows: list, quality: str) -> tuple[int, int]:
        picked = [r for _, r in rows if r["quality"] == quality]
        return len(picked), sum(r["flow_credits_expected"] for r in picked)

    t1_flow = expected(t1_rows)
    t2_flow = expected(t2_rows)
    t1_try = sum(r["flow_credits_try1"] for _, r in t1_rows)
    t2_try = sum(r["flow_credits_try1"] for _, r in t2_rows)
    after = FLOW_LEFT - FLOW_007 - FLOW_008 - t1_flow
    q_exp = math.ceil(FLOW_CREDITS["Quality"] * TAKES_PER_KEEP["Quality"])
    f_exp = math.ceil(FLOW_CREDITS["Fast"] * TAKES_PER_KEEP["Fast"])
    t2_conts = sum(
        1 for _, r in t2_rows if r["quality"] == "Quality" and is_continuation(r["id"])
    )
    t1_q, _ = bucket(t1_rows, "Quality")
    t1_f, _ = bucket(t1_rows, "Fast")
    t2_q, _ = bucket(t2_rows, "Quality")

    expect = {
        "rows": 90,
        "Quality": 46,
        "Fast": 31,
        "code_graphic": 12,
        "edit_hold": 0,
        "reuse": 1,
        "flow_credits_expected": 12534,
        "flow_credits_try1": 4910,
        "t1_rows": 57,
        "t1_q": 26,
        "t1_f": 31,
        "t1_flow": 7354,
        "t1_try": 2910,
        "after": 3231,
        "t2_rows": 20,
        "t2_q": 20,
        "t2_conts": 18,
        "t2_flow": 5180,
        "t2_try": 2000,
    }
    got = {
        "rows": totals["rows"],
        "Quality": totals["Quality"],
        "Fast": totals["Fast"],
        "code_graphic": totals["code_graphic"],
        "edit_hold": totals["edit_hold"],
        "reuse": totals["reuse"],
        "flow_credits_expected": totals["flow_credits_expected"],
        "flow_credits_try1": totals["flow_credits_try1"],
        "t1_rows": len(t1_rows),
        "t1_q": t1_q,
        "t1_f": t1_f,
        "t1_flow": t1_flow,
        "t1_try": t1_try,
        "after": after,
        "t2_rows": len(t2_rows),
        "t2_q": t2_q,
        "t2_conts": t2_conts,
        "t2_flow": t2_flow,
        "t2_try": t2_try,
    }
    if got != expect:
        raise SystemExit(f"numbers drifted:\n got {got}\n expect {expect}")
    if t1_flow > TRANCHE1_CAP:
        raise SystemExit(f"tranche 1 {t1_flow} over cap {TRANCHE1_CAP}")
    if after < HEADROOM:
        raise SystemExit(f"headroom after tranche 1 is {after}")
    if t1_flow + t2_flow != totals["flow_credits_expected"]:
        raise SystemExit("tranche credits do not add up")
    if TRANCHE1_CAP != 7585:
        raise SystemExit(f"cap {TRANCHE1_CAP}")

    # Part checks: model changes only on parts 4 and 5. Tranche moves on 2, 3, 4, 5.
    part_expect = {
        1: {"Quality": 6, "Fast": 8, "flow_credits_expected": 1714, "tranche_1": 12, "tranche_2": 2},
        2: {"Quality": 16, "Fast": 0, "flow_credits_expected": 4144, "tranche_1": 10, "tranche_2": 6},
        3: {"Quality": 6, "Fast": 5, "flow_credits_expected": 1654, "tranche_1": 7, "tranche_2": 4},
        4: {"Quality": 8, "Fast": 9, "flow_credits_expected": 2252, "tranche_1": 13, "tranche_2": 4},
        5: {"Quality": 10, "Fast": 9, "flow_credits_expected": 2770, "tranche_1": 15, "tranche_2": 4},
    }
    for pp in per_part:
        want = part_expect[pp["part"]]
        for k, v in want.items():
            if pp[k] != v:
                raise SystemExit(f"part {pp['part']} {k}={pp[k]} expected {v}")

    def slip_lines() -> list[str]:
        lines = []
        for n, r in t2_rows:
            if not is_continuation(r["id"]):
                continue
            measure = r.get("j0261_hold_check") or r.get("reuse_measurement") or {}
            shortfall = measure.get("shortfall_usable_s")
            parent = measure.get("source_row") or r.get("reference")
            need = measure.get("required_use_s", r["use_s"])
            if not isinstance(shortfall, (int, float)) or shortfall <= 0:
                raise SystemExit(f"missing shortfall for slip row P{n}:{r['id']}")
            lines.append(
                f"| P{n}:{r['id']} | {float(need):.2f} | {parent} | {float(shortfall):.2f} | "
                f"{r['flow_credits_expected']} |"
            )
        return lines

    holes = slip_lines()
    if len(holes) != 18:
        raise SystemExit(f"slip continuations {len(holes)}")

    plan = {
        "film": "009",
        "written": "2026-10-15",
        "task": "J0335 plate boards v04. No mint. No spend.",
        "from": "part-0N_plates_v03.json via _build_plate_boards_v04.py",
        "ruling": (
            "Chief FIX on J0333, 15 Oct ~23:10 London, desk #180. "
            "Fast-parent continuations match the parent model. "
            "The closer stays in tranche 1. Two short Quality parents between "
            "£0 code graphics wait in tranche 2."
        ),
        "readings": {
            "flow_credits_left": FLOW_LEFT,
            "flow_read_at": FLOW_READ_AT,
            "flow_note": "Same v02 reading. Not re-read. No spend in this pass.",
            "vertex_promo_gbp": VERTEX_BALANCE_GBP,
            "vertex_read_at": VERTEX_READ_AT,
            "vertex_usable_gbp": VERTEX_USABLE_GBP,
        },
        "rates": {
            "flow_quality_try1": FLOW_CREDITS["Quality"],
            "flow_fast_try1": FLOW_CREDITS["Fast"],
            "takes_per_keep_quality": TAKES_PER_KEEP["Quality"],
            "takes_per_keep_fast": TAKES_PER_KEEP["Fast"],
            "flow_quality_expected": q_exp,
            "flow_fast_expected": f_exp,
            "note": "Expected is ceil(try-1 times takes-per-keep). Same rates as v03.",
        },
        "totals": totals,
        "per_part": per_part,
        "j0333_fast_mints": [f"P{n}:{r['id']}" for n, r in flat if r["id"] in J0333_FAST],
        "j0335_fast_mints": minted,
        "tranches": {
            "order": "006 needs 0 Flow, then 007, then 008, then 009 tranche 1, then 009 tranche 2",
            "flow_007_estimate": FLOW_007,
            "flow_008_estimate": FLOW_008,
            "headroom_after_any_mint": HEADROOM,
            "tranche_1_cap_on_this_reading": TRANCHE1_CAP,
            "tranche_1_rows": len(t1_rows),
            "tranche_1_flow_try1": t1_try,
            "tranche_1_flow_expected": t1_flow,
            "tranche_1_quality_rows": t1_q,
            "tranche_1_fast_rows": t1_f,
            "left_after_007_008_and_tranche_1": after,
            "closer_in_tranche_1": "P5:10_explorer_bench",
            "moved_to_tranche_2": deferred,
            "slip_fallback": {
                "P2:10_how_high": "£0 hold or extension of P2:09_pull_heights",
                "P3:07_ball_to_moon": "£0 hold or extension of P3:06_orbit_teach and P3:08_km_a_second",
            },
            "tranche_2_rows": len(t2_rows),
            "tranche_2_flow_try1": t2_try,
            "tranche_2_flow_expected": t2_flow,
            "tranche_2_quality_continuations": t2_conts,
            "tranche_2_deferred_parents": 2,
            "tranche_2_when": "After the AI Ultra renewal, about 12 Nov 2026. Confirm with a live read.",
            "shrink_rule": (
                "If 007 or 008 overrun, move the latest Quality parent still in tranche 1, "
                "other than the closer P5:10_explorer_bench, into tranche 2 until a live read "
                "stays at or above 3,000. Fast mints stay in tranche 1 until every other "
                "Quality parent has moved. The 3,000 floor is unchanged."
            ),
        },
        "all_on_flow_credits_expected": totals["flow_credits_expected"],
        "all_on_vertex_gbp_expected": totals["vertex_expected_gbp"],
        "fits_vertex": totals["vertex_expected_gbp"] <= VERTEX_USABLE_GBP,
        "fits_flow_as_one_block": (
            FLOW_LEFT - FLOW_007 - FLOW_008 - totals["flow_credits_expected"] >= HEADROOM
        ),
        "fits_flow_as_one_block_note": (
            "False once 007 and 008 are reserved. The film alone would leave headroom "
            "against the raw balance. It still does not mint as one block."
        ),
    }
    (EDIT / "PICTURE_PLAN_v04.json").write_text(json.dumps(plan, indent=2) + "\n")

    lines = [
        "# 009 price review v04",
        "",
        "Cursor, 15 Oct 2026, J0335. Boards only. **No mint. No spend. No merge.**",
        "v03 (PR #331, a27348b) stands on the six J0333 Fast mints, the parchment code graphics,",
        "and the 24-row continuation count. This pass applies the Chief FIX on J0333",
        "(desk #180, 15 Oct ~23:10 London). Parked for Chief.",
        "",
        "## Readings",
        "",
        f"- Flow: **{FLOW_LEFT}** credits at {FLOW_READ_AT} (the v02 read, CDP :9222). Not re-read. Nothing spent.",
        f"- Vertex promo: **£{VERTEX_BALANCE_GBP:.2f}** at {VERTEX_READ_AT}. Usable **£{VERTEX_USABLE_GBP:.2f}** after the £1 margin. The route stays Flow-first.",
        "",
        "## Rates",
        "",
        "Same rates as v01, v02 and v03. Expected credits are `ceil(try-1 × takes per keep)`.",
        "",
        "| Model | Try-1 | Takes per keep | Expected per row |",
        "|---|---:|---:|---:|",
        f"| Quality | {FLOW_CREDITS['Quality']} | {TAKES_PER_KEEP['Quality']} (70/27) | {q_exp} |",
        f"| Fast | {FLOW_CREDITS['Fast']} | {TAKES_PER_KEEP['Fast']} (94/48) | {f_exp} |",
        "",
        "Vertex, if it were the route: Quality £0.16/s, Fast £0.08/s (USD 0.20 and 0.10 at 0.80 GBP), clip lengths 4/6/8 s, plus stills. It does not fit.",
        "",
        "## Totals",
        "",
        "v03 was 90 rows, 52 Quality / 25 Fast / 12 code / 0 edit-hold / 1 other reuse, Flow expected 13,968.",
        "v04 turns six Quality continuations into Fast mints. Row count stays 90.",
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
        f"All on Flow, as one block: **{totals['flow_credits_expected']}** expected against {FLOW_LEFT} left. "
        f"That is {FLOW_LEFT - totals['flow_credits_expected']} before 007 and 008, so 009 does not mint as one block.",
        f"All on Vertex: DOES NOT FIT (£{totals['vertex_expected_gbp']:.2f} expected vs £{VERTEX_USABLE_GBP:.2f} usable).",
        "",
        "## Mint order",
        "",
        "006 needs 0 Flow. Then 007, then 008, then 009 in two tranches. Every mint job reads Flow live first and stops if the read after its spend would drop below 3,000. If 007 or 008 overrun, tranche 1 shrinks from the latest Quality parent still in it, other than the closer, and that row moves to tranche 2. Fast mints stay in tranche 1 until every other Quality parent has moved. No top-up.",
        "",
        f"On this reading the cap for tranche 1 is {FLOW_LEFT} − {FLOW_007} − {FLOW_008} − {HEADROOM} = **{TRANCHE1_CAP}**.",
        "",
        "## 1. Parchment teach → £0 code graphics",
        "",
        "Unchanged from v03. Twelve rows. Flow and Vertex are 0. They sit in neither tranche.",
        "",
        "## 2. Six J0333 Fast mints",
        "",
        "Unchanged. Each stays its own Fast mint in tranche 1, expected 20.",
        "",
        "## 2b. Six Fast-parent continuations → own Fast mints",
        "",
        "Each parent is already Fast. v03 still priced the continuation as a second Quality mint, which would jump look at the cut. v04 mints each beat on its own, Fast, with a new angle or move and the parent's look. Try-1 is 10, expected is 20, each. All six move into tranche 1.",
        "",
        "| Row | Needed s | Parent | Shortfall s | Try-1 | Expected | Tranche |",
        "|---|---:|---|---:|---:|---:|---:|",
    ]
    for n, row in flat:
        if (n, row["id"]) not in MATCH_FAST:
            continue
        m = row.get("j0261_hold_check") or row.get("reuse_measurement") or {}
        lines.append(
            f"| P{n}:{row['id']} | {float(m['required_use_s']):.2f} | {m['source_row']} | "
            f"{float(m['shortfall_usable_s']):.2f} | {row['flow_credits_try1']} | "
            f"{row['flow_credits_expected']} | {row['tranche']} |"
        )
    lines += [
        "",
        "Distinct beats:",
        "",
    ]
    for (part_n, pid), beat in MATCH_FAST.items():
        lines.append(f"- P{part_n}:{pid}: {beat}")
    lines += [
        "",
        f"Six rows, Flow try-1 **60**, expected **{6 * f_exp}**.",
        "",
        "## 3. Remaining Quality continuations",
        "",
        "Eighteen of the v03 condition-3 rows stay second Quality mints. Their parents are still Quality, and the parent clip cannot cover them. They stay in tranche 2. The other six are the Fast-parent rows in section 2b.",
        "",
        "## 4. Quality → Fast parents",
        "",
        "Unchanged from v02: P1:10_farmhouse_dawn, P3:02_cannon_world, P4:02_spray_paint, P5:01_one_law, P5:08_cup_and_planets, P5:12_clay_handoff.",
        "",
        "## Tranches",
        "",
        "| | Rows | Quality | Fast | Flow try-1 | Flow expected |",
        "|---|---:|---:|---:|---:|---:|",
        f"| Tranche 1, now-ish, after 007 and 008 | {len(t1_rows)} | {t1_q} | {t1_f} | {t1_try} | {t1_flow} |",
        f"| Tranche 2, after the ~12 Nov renewal | {len(t2_rows)} | {t2_q} | {bucket(t2_rows, 'Fast')[0]} | {t2_try} | {t2_flow} |",
        f"| **009** | **{len(t1_rows) + len(t2_rows)}** | **{totals['Quality']}** | **{totals['Fast']}** | **{totals['flow_credits_try1']}** | **{totals['flow_credits_expected']}** |",
        "",
        f"After 007 (~{FLOW_007}), 008 ({FLOW_008}) and tranche 1 ({t1_flow}) the reading would show **{after}** left, against the 3,000 floor. Cap on this reading is {TRANCHE1_CAP}.",
        "",
        "Tranche 1 is the parents and the Fast plates, including the six J0333 Fast mints, the six new Fast mints, and the closer:",
        "",
        "- P5:10_explorer_bench (\"It is falling towards you, right now.\").",
        "",
        "Deferred to tranche 2 instead, so the closer is not the row that waits:",
        "",
        "- " + ", ".join(deferred) + ".",
        "",
        "Those two mint at the start of tranche 2, before any continuation. Tranche 2 is the 18 remaining second-Quality continuations plus these two parents. Confirm the renewal with a live read before it starts. 009 picture is due Sun 15 Nov.",
        "",
        "## If tranche 2 slips past ~13 Nov",
        "",
        "These 18 continuation beats would have to sit as an edit-hold of the parent. The parent clip cannot cover them, so the picture on that beat would be shorter than the VO. A picture hole is not allowed while the row is still a planned mint; this list is the hole if the renewal slips.",
        "",
        "| Beat | Needed s | Parent | Shortfall s | Expected credits |",
        "|---|---:|---|---:|---:|",
    ]
    lines += holes
    lines += [
        "",
        "The two deferred Quality parents do not leave a hole. Their slip fallback is a £0 hold or extension of the neighbouring code graphic:",
        "",
        "| Deferred parent | Needed s | Fallback |",
        "|---|---:|---|",
        "| P2:10_how_high | 2.58 | £0 hold or extension of P2:09_pull_heights |",
        "| P3:07_ball_to_moon | 2.84 | £0 hold or extension of P3:06_orbit_teach and P3:08_km_a_second |",
        "",
        "## For the Chief",
        "",
        "No mint in this pass. PR #331 stays open. Vertex does not fit. Flow fits only as the split above.",
        "",
        "Tranche 1 is 26 Quality + 31 Fast = 7,354, under the 7,585 cap, with 3,231 left after 007, 008 and tranche 1. Tranche 2 is 18 continuations + 2 deferred parents = 20 Quality = 5,180. The film is 46 Quality + 31 Fast = 12,534.",
        "",
        "The closer is back in tranche 1. Chief can still name a different pair to wait. Fast mints stay in tranche 1.",
        "",
    ]
    (EDIT / "PRICE_REVIEW_v04.md").write_text("\n".join(lines) + "\n")

    status = EDIT.parent / "production-status.md"
    text = status.read_text()
    new = "**BOARDS v04 parked for Chief (J0335, 15 Oct). NO MINT.**"
    olds = [
        "**BOARDS v01 parked for Chief's price pass (J0261, 15 Oct). NO MINT.**",
        new,
    ]
    if new in text:
        pass
    elif olds[0] in text:
        status.write_text(text.replace(olds[0], new, 1))
    else:
        raise SystemExit("production-status picture line not found")

    print(f"rows {totals['rows']}  Q {totals['Quality']}  F {totals['Fast']}  "
          f"code {totals['code_graphic']}  hold {totals['edit_hold']}  reuse {totals['reuse']}")
    print(f"Flow try-1 {totals['flow_credits_try1']}  expected {totals['flow_credits_expected']}")
    print(f"tranche 1 {t1_q}Q+{t1_f}F = {t1_flow}  after {after}  cap {TRANCHE1_CAP}")
    print(f"tranche 2 {t2_conts} cont + {len(deferred)} parents = {t2_flow}")
    print(f"Vertex expected £{totals['vertex_expected_gbp']:.2f}  fits {plan['fits_vertex']}")
    print("deferred", deferred)


if __name__ == "__main__":
    main()
