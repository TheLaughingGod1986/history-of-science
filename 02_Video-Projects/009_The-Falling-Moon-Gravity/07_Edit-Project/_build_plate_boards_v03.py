#!/usr/bin/env python3
"""HOS 009: plate boards v03 from v02. J0333, Chief FIX on condition 2.

No mint. No spend. Desk #180 6202998478, mint-order split 6202968147.

v02 was right on conditions 1, 3 and 4. Condition 2's six Fast edit-holds
leave a picture hole (each parent is 2.8–6.2 s short). v03 makes each its
own Fast mint with a new angle or move and the parent's look.

  python3 07_Edit-Project/_build_plate_boards_v03.py
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

EDIT = Path(__file__).resolve().parent
PARTS = EDIT / "parts"

# Same reading as v02. This pass does not re-read Flow and does not spend.
FLOW_LEFT = 23740
FLOW_READ_AT = "2026-10-15T21:42:22Z"
VERTEX_BALANCE_GBP = 71.02
VERTEX_READ_AT = "2026-10-15T07:30:31Z"
VERTEX_USABLE_GBP = 70.02
HEADROOM = 3000

# Mint order on that reading (desk #180 6202968147). Estimates, not a spend.
FLOW_007 = 7550
FLOW_008 = 5605
# Tranche 1 may use only what leaves HEADROOM after 007 and 008 on estimate.
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

# Own Fast mints. New angle or move, same objects and light as the parent.
# Not an i2v continuation and not "same shot continues".
OWN_FAST = {
    "03_table_three_c1": (
        1,
        "From table height the camera tracks along the wood. The green apple "
        "with a red flush is already set, a small brass cannon is turned so its "
        "mouth points along the table, and a sheet of unreadable scribbles is "
        "laid between them. Grey window light. The marks are scribbles, not numbers.",
    ),
    "03_table_three_c2": (
        1,
        "The camera rises off the same wooden table toward the grey window. "
        "The green apple, the brass cannon and the sheet of scribbles stay in "
        "frame below, still in grey window light, with a plain pale wall beyond "
        "the window.",
    ),
    "09_can_he_calculate_c1": (
        3,
        "A side angle on the same table. The pen lowers toward the paper and "
        "stops just above it, beside the apple. Seen from the side of the hand, "
        "no readable face, grey window light only.",
    ),
    "06_pretty_nearly_c1": (
        4,
        "From the left side of the desk, a hand lifts one corner of the same page. "
        "Two short columns of unreadable marks still end level with each other. "
        "Window light, no digits.",
    ),
    "10_write_it_down_c1": (
        4,
        "A side view of the same desk. Another closed stack of pages is set down "
        "beside the man, who is still seen from behind. Window light only. "
        "No readable face.",
    ),
    "03_halley_comet_path_c1": (
        5,
        "The same painted-parchment card, camera tilting along the long ink ellipse. "
        "The small ink marker steps from the far side of the loop toward the near side. "
        "Matte ink only, no digits, no tail.",
    ),
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
        path = PARTS / f"part-0{n}_plates_v02.json"
        boards.append((n, json.loads(path.read_text())))

    minted = []
    for n, board in boards:
        for row in board["plates"]:
            pid = row["id"]
            if pid not in OWN_FAST:
                continue
            part_n, beat = OWN_FAST[pid]
            if part_n != n:
                raise SystemExit(f"{pid} is in part {n}, expected {part_n}")
            if row.get("route") != "edit-hold" or row.get("v01_quality") != "Fast":
                raise SystemExit(f"{pid} is not a v02 Fast edit-hold")
            prompt = "Premium Animistry-class 3D cartoon. " + beat + TAIL
            if FAST_BANNED.search(prompt):
                raise SystemExit(f"Fast prompt still emissive: {pid}\n{prompt}")
            if "same shot continues" in prompt.lower():
                raise SystemExit(f"prompt is still a continuation: {pid}")
            parent_id = pid.rsplit("_c", 1)[0]
            measure = row.get("reuse_measurement") or {}
            shortfall = measure.get("shortfall_usable_s")
            if shortfall is None or shortfall <= 0:
                raise SystemExit(f"{pid} has no positive shortfall; a hold might cover it")
            row["quality"] = "Fast"
            row["prompt"] = prompt
            row["reference"] = (
                f"same look as P{n}:{parent_id}; own Fast text mint, not an i2v continuation"
            )
            row.pop("i2v_from", None)
            row.pop("reuse_of", None)
            row["engine_reason"] = (
                "J0333 Chief FIX (desk #180 6202998478): the parent clip cannot cover "
                f"this beat (shortfall {shortfall} s usable). Own Fast mint, new angle "
                "or move, same look as the parent. No edit-hold, no loop, no freeze."
            )
            if measure:
                measure = dict(measure)
                measure["resolution"] = "own_fast_mint"
                row["reuse_measurement"] = measure
            row.update(price_fast(row["use_s"]))
            row["generation_authorized"] = False
            minted.append(f"P{n}:{pid}")
        board["status"] = "BOARD_V03_PARKED_FOR_CHIEF"
        board["mint"] = False

    if minted != [f"P{p}:{i}" for i, (p, _) in OWN_FAST.items()]:
        raise SystemExit(f"minted {minted}")

    # Recount, then assign tranches. Continuations that stay Quality are tranche 2.
    flat = []
    for n, board in boards:
        for row in board["plates"]:
            flat.append((n, row))

    for n, row in flat:
        q = row["quality"]
        if q == "Quality" and is_continuation(row["id"]):
            row["tranche"] = 2
            row["tranche_why"] = (
                "Second Quality mint. Tranche 2, after the AI Ultra renewal "
                "(~12 Nov, confirm with a live read). Desk #180 6202968147."
            )
        elif q in ("Quality", "Fast"):
            row["tranche"] = 1
            why = "Parent or Fast plate. Tranche 1, after 007 and 008, inside the 3,000 headroom."
            if row["id"] in OWN_FAST:
                why = (
                    "Own Fast mint for a beat the parent cannot cover. "
                    "Tranche 1 with the other Fast plates. J0333."
                )
            row["tranche_why"] = why
        else:
            row["tranche"] = 0
            row["tranche_why"] = "£0. Code graphic or reuse. Not in either Flow tranche."

    def expected(rows: list) -> int:
        return sum(r["flow_credits_expected"] for _, r in rows)

    t1 = [(n, r) for n, r in flat if r["tranche"] == 1]
    # The six stay. Shrink by moving the latest Quality parent into tranche 2.
    moved = []
    while expected(t1) > TRANCHE1_CAP:
        parents = [(n, r) for n, r in t1 if r["quality"] == "Quality"]
        if not parents:
            raise SystemExit(
                f"tranche 1 still {expected(t1)} over cap {TRANCHE1_CAP} with no Quality parent left to move"
            )
        n, row = max(parents, key=lambda item: (item[0], item[1]["t_s"]))
        row["tranche"] = 2
        row["tranche_why"] = (
            "Latest Quality parent moved out of tranche 1 so a live read stays at or above "
            f"3,000 after 007 (~{FLOW_007}), 008 ({FLOW_008}) and this tranche "
            f"(cap {TRANCHE1_CAP} on the {FLOW_READ_AT} reading). "
            "Mint it at the start of tranche 2. Chief can name a different Quality parent to wait instead."
        )
        row["tranche_moved_from"] = 1
        moved.append(f"P{n}:{row['id']}")
        t1 = [(nn, r) for nn, r in flat if r["tranche"] == 1]

    for key in OWN_FAST:
        hit = [r for _, r in flat if r["id"] == key]
        if len(hit) != 1 or hit[0]["tranche"] != 1 or hit[0]["quality"] != "Fast":
            raise SystemExit(f"{key} did not stay a tranche-1 Fast mint")

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
        out = PARTS / f"part-0{n}_plates_v03.json"
        out.write_text(json.dumps(board, indent=2) + "\n")

    totals["vertex_try1_gbp"] = round(totals["vertex_try1_gbp"], 2)
    totals["vertex_expected_gbp"] = round(totals["vertex_expected_gbp"], 2)
    if totals["edit_hold"] != 0:
        raise SystemExit(f"edit-holds left: {totals['edit_hold']}")
    if totals["Fast"] != 25 or totals["Quality"] != 52:
        raise SystemExit(f"unexpected counts Q {totals['Quality']} F {totals['Fast']}")

    t1_rows = [(n, r) for n, r in flat if r["tranche"] == 1]
    t2_rows = [(n, r) for n, r in flat if r["tranche"] == 2]
    t1_flow = expected(t1_rows)
    t2_flow = expected(t2_rows)
    t1_try = sum(r["flow_credits_try1"] for _, r in t1_rows)
    t2_try = sum(r["flow_credits_try1"] for _, r in t2_rows)
    after = FLOW_LEFT - FLOW_007 - FLOW_008 - t1_flow
    if after < HEADROOM:
        raise SystemExit(f"headroom after tranche 1 is {after}")
    if t1_flow + t2_flow != totals["flow_credits_expected"]:
        raise SystemExit("tranche credits do not add up")

    q_exp = math.ceil(FLOW_CREDITS["Quality"] * TAKES_PER_KEEP["Quality"])
    f_exp = math.ceil(FLOW_CREDITS["Fast"] * TAKES_PER_KEEP["Fast"])

    def bucket(rows: list, quality: str) -> tuple[int, int]:
        picked = [r for _, r in rows if r["quality"] == quality]
        return len(picked), sum(r["flow_credits_expected"] for r in picked)

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

    plan = {
        "film": "009",
        "written": "2026-10-15",
        "task": "J0333 plate boards v03. No mint. No spend.",
        "from": "part-0N_plates_v02.json via _build_plate_boards_v03.py",
        "ruling": (
            "Chief FIX on condition 2, desk #180 6202998478. "
            "Mint-order split 6202968147 supersedes the whole-and-last line in 6202998478."
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
            "note": "Expected is ceil(try-1 times takes-per-keep). Same rates as v02.",
        },
        "totals": totals,
        "per_part": per_part,
        "own_fast_mints": minted,
        "tranches": {
            "order": "006 needs 0 Flow, then 007, then 008, then 009 tranche 1, then 009 tranche 2",
            "flow_007_estimate": FLOW_007,
            "flow_008_estimate": FLOW_008,
            "headroom_after_any_mint": HEADROOM,
            "tranche_1_cap_on_this_reading": TRANCHE1_CAP,
            "tranche_1_rows": len(t1_rows),
            "tranche_1_flow_try1": t1_try,
            "tranche_1_flow_expected": t1_flow,
            "tranche_1_quality_rows": bucket(t1_rows, "Quality")[0],
            "tranche_1_fast_rows": bucket(t1_rows, "Fast")[0],
            "left_after_007_008_and_tranche_1": after,
            "moved_to_tranche_2": moved,
            "tranche_2_rows": len(t2_rows),
            "tranche_2_flow_try1": t2_try,
            "tranche_2_flow_expected": t2_flow,
            "tranche_2_quality_continuations": sum(
                1 for _, r in t2_rows if r["quality"] == "Quality" and is_continuation(r["id"])
            ),
            "tranche_2_when": "After the AI Ultra renewal, about 12 Nov 2026. Confirm with a live read.",
            "shrink_rule": (
                "If 007 or 008 overrun, move the latest Quality parent still in tranche 1 "
                "into tranche 2 until a live read stays at or above 3,000. "
                "The six J0333 Fast mints stay in tranche 1 until every Quality parent has moved."
            ),
        },
        "all_on_flow_credits_expected": totals["flow_credits_expected"],
        "all_on_vertex_gbp_expected": totals["vertex_expected_gbp"],
        "fits_vertex": totals["vertex_expected_gbp"] <= VERTEX_USABLE_GBP,
        "fits_flow_as_one_block": FLOW_LEFT - totals["flow_credits_expected"] >= HEADROOM,
    }
    (EDIT / "PICTURE_PLAN_v03.json").write_text(json.dumps(plan, indent=2) + "\n")

    lines = [
        "# 009 price review v03",
        "",
        "Cursor, 15 Oct 2026, J0333. Boards only. **No mint. No spend. No merge.**",
        "v02 (PR #331, 38bb802) stands on conditions 1, 3 and 4. This pass fixes condition 2",
        "(Chief, desk #180 6202998478) and splits the mint into two tranches",
        "(Chief, desk #180 6202968147). That split supersedes the whole-and-last line in 6202998478. Parked for Chief.",
        "",
        "## Readings",
        "",
        f"- Flow: **{FLOW_LEFT}** credits at {FLOW_READ_AT} (the v02 read, CDP :9222). Not re-read. Nothing spent.",
        f"- Vertex promo: **£{VERTEX_BALANCE_GBP:.2f}** at {VERTEX_READ_AT}. Usable **£{VERTEX_USABLE_GBP:.2f}** after the £1 margin. The route stays Flow-first.",
        "",
        "## Rates",
        "",
        "Same rates as v01 and v02. Expected credits are `ceil(try-1 × takes per keep)`.",
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
        "v02 was 90 rows, 52 Quality / 19 Fast / 12 code / 6 edit-hold / 1 other reuse, Flow expected 13,848.",
        "v03 adds six Fast mints and clears the six edit-holds. Row count stays 90.",
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
        "006 needs 0 Flow. Then 007, then 008, then 009 in two tranches. Every mint job reads Flow live first and stops if the read after its spend would drop below 3,000. If 007 or 008 overrun, tranche 1 shrinks from the latest Quality parent still in it, and that row moves to tranche 2. The six Fast mints below stay in tranche 1 until every Quality parent has moved. No top-up.",
        "",
        f"On this reading the cap for tranche 1 is {FLOW_LEFT} − {FLOW_007} − {FLOW_008} − {HEADROOM} = **{TRANCHE1_CAP}**.",
        "",
        "## 1. Parchment teach → £0 code graphics",
        "",
        "Unchanged from v02. Twelve rows. Flow and Vertex are 0. They sit in neither tranche.",
        "",
        "## 2. Six Fast continuations → own Fast mints",
        "",
        "Each parent is an 8.00 s clip (7.90 s usable) and is short of the next beat, so an edit-hold would leave a picture hole. v03 mints each beat on its own, Fast, with a new angle or move and the parent's look. Try-1 is 10, expected is 20, each.",
        "",
        "| Row | Needed s | Parent | Shortfall s | Try-1 | Expected | Tranche |",
        "|---|---:|---|---:|---:|---:|---:|",
    ]
    for n, row in flat:
        if row["id"] not in OWN_FAST:
            continue
        m = row["reuse_measurement"]
        lines.append(
            f"| P{n}:{row['id']} | {m['required_use_s']:.2f} | {m['source_row']} | "
            f"{m['shortfall_usable_s']:.2f} | {row['flow_credits_try1']} | "
            f"{row['flow_credits_expected']} | {row['tranche']} |"
        )
    lines += [
        "",
        "Distinct beats:",
        "",
    ]
    for pid, (part_n, beat) in OWN_FAST.items():
        lines.append(f"- P{part_n}:{pid}: {beat}")
    lines += [
        "",
        f"Six rows, Flow try-1 **60**, expected **{6 * f_exp}**.",
        "",
        "## 3. Quality continuations stay second Quality mints",
        "",
        "Unchanged from v02. The parent clip cannot cover any of them. The split note said 22; the v02 condition-3 table has **24** rows, and all 24 stay Quality mints here (including `02_spray_paint_c1` and `_c2`, whose parent is now Fast and still cannot cover them).",
        "",
        "## 4. Quality → Fast",
        "",
        "Unchanged from v02: P1:10_farmhouse_dawn, P3:02_cannon_world, P4:02_spray_paint, P5:01_one_law, P5:08_cup_and_planets, P5:12_clay_handoff.",
        "",
        "## Tranches",
        "",
        f"| | Rows | Quality | Fast | Flow try-1 | Flow expected |",
        f"|---|---:|---:|---:|---:|---:|",
        f"| Tranche 1, now-ish, after 007 and 008 | {len(t1_rows)} | {bucket(t1_rows, 'Quality')[0]} | {bucket(t1_rows, 'Fast')[0]} | {t1_try} | {t1_flow} |",
        f"| Tranche 2, after the ~12 Nov renewal | {len(t2_rows)} | {bucket(t2_rows, 'Quality')[0]} | {bucket(t2_rows, 'Fast')[0]} | {t2_try} | {t2_flow} |",
        f"| **009** | **{len(t1_rows) + len(t2_rows)}** | **{totals['Quality']}** | **{totals['Fast']}** | **{totals['flow_credits_try1']}** | **{totals['flow_credits_expected']}** |",
        "",
        f"After 007 (~{FLOW_007}), 008 ({FLOW_008}) and tranche 1 ({t1_flow}) the reading would show **{after}** left, against the 3,000 floor.",
        "",
        "Tranche 1 is the parents and the Fast plates, including the six new Fast mints, minus the Quality parents that did not fit:",
        "",
    ]
    if moved:
        lines.append(", ".join(moved) + ".")
    else:
        lines.append("None. The full parent-and-Fast set fits under the cap.")
    lines += [
        "",
        "Those moved rows mint at the start of tranche 2, before any continuation of the same plate.",
        "",
        "Tranche 2 is those moved rows plus the 24 second-Quality continuations. Confirm the renewal with a live read before it starts. 009 picture is due Sun 15 Nov.",
        "",
        "## If tranche 2 slips past ~13 Nov",
        "",
        "These continuation beats would have to sit as an edit-hold of the parent. The parent clip cannot cover them, so the picture on that beat would be shorter than the VO. A picture hole is not allowed while the row is still a planned mint; this list is the hole if the renewal slips.",
        "",
        "| Beat | Needed s | Parent | Shortfall s | Expected credits |",
        "|---|---:|---|---:|---:|",
    ]
    lines += slip_lines()
    lines += [
        "",
        "Quality parents moved into tranche 2 have no earlier clip to hold. Until tranche 2 mints them, that beat has no plate:",
        "",
    ]
    if moved:
        for name in moved:
            lines.append(f"- {name}")
    else:
        lines.append("- None.")
    lines += [
        "",
        "## For the Chief",
        "",
        "No mint in this pass. PR #331 stays open. Vertex does not fit. Flow fits only as the split above.",
        "",
        "The one Quality parent that does not fit tranche 1 is the latest one, P5:10_explorer_bench "
        "(the closer: \"It is falling towards you, right now.\"). It waits for tranche 2. "
        "Chief can name a different Quality parent to wait instead. The six Fast mints stay in tranche 1.",
        "",
    ]
    (EDIT / "PRICE_REVIEW_v03.md").write_text("\n".join(lines) + "\n")
    print(f"rows {totals['rows']}  Q {totals['Quality']}  F {totals['Fast']}  "
          f"code {totals['code_graphic']}  hold {totals['edit_hold']}  reuse {totals['reuse']}")
    print(f"Flow try-1 {totals['flow_credits_try1']}  expected {totals['flow_credits_expected']}")
    print(f"tranche 1 {t1_flow} ({len(t1_rows)} rows)  after {after}  cap {TRANCHE1_CAP}")
    print(f"tranche 2 {t2_flow} ({len(t2_rows)} rows)  moved {moved}")
    print(f"Vertex expected £{totals['vertex_expected_gbp']:.2f}")


if __name__ == "__main__":
    main()
