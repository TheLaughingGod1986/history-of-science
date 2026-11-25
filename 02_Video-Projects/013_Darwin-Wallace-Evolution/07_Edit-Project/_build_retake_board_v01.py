#!/usr/bin/env python3
"""HOS 013 retake prompt and price board v01 (J3738). Mints nothing, spends nothing.

Builds RETAKE_BOARD_v01.json and RETAKE_BOARD_v01.md for the 8 pass-1 rows the Chief
ruled RETAKE in J2529 (rows 3, 10, 24, 28, 47, 49, 54, 63). The 10 capability-held
rows (56-62, 64-66, J3178) are not read into the board and are not touched.

  python3 _build_retake_board_v01.py --owb <orbit-with-ben checkout>
  python3 _build_retake_board_v01.py --check     # re-check the committed JSON only
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_JSON = HERE / "RETAKE_BOARD_v01.json"
OUT_MD = HERE / "RETAKE_BOARD_v01.md"

RETAKE_ROWS = (3, 10, 24, 28, 47, 49, 54, 63)
HELD_ROWS = (56, 57, 58, 59, 60, 61, 62, 64, 65, 66)

# Flow balance: last daily reading in orbit-with-ben 05_Analytics/ai_spend/ledger.jsonl.
# The mint job must read the live balance itself before any Create.
BALANCE = {"credits": 23450, "read_at": "2026-11-24T08:30:22Z",
           "source": "orbit-with-ben 05_Analytics/ai_spend/ledger.jsonl (mini-daily Flow reading)"}
HEADROOM_FLOOR = 3000          # _mint_flow_v01_pass1.py DETACHED_HEADROOM_FLOOR
RETAKE_HOLD = 700              # J2529 REVIEW_STATE retake_reservation_credits (7 rows; row 63 not added)
QUALITY_RETRY = 2.59           # PICTURE_PLAN_v02 standard Quality retry allowance
PRICE = {"Veo 3.1 - Quality": 100, "Veo 3.1 - Lite": 5, "Omni 1.2 Flash per second": 3}
QUALITY_RETIRES = "2026-12-05"

# One fix sentence per row, answering the recorded Chief defect. Added to the locked
# prompt; nothing in the locked prompt is removed or reworded.
FIX = {
    3: ("At about 2.9-3.1 s a fist separates from the sleeve and a second hand fragment shows top right "
        "(desk comment 6815859027, in force by 6815870258).",
        "Exactly two hands are in frame, and each hand stays whole and joined to its sleeved forearm "
        "for the whole clip. Exactly three finch skins."),
    10: ("Steel dip pen until about 3.5 s; by about 4.0 s it is a modern pen with barrel and clip "
         "(desk comment 6815859027, in force by 6815870258).",
         "The pen is a plain wooden holder with a steel nib for the whole clip, with no clip, cap or button. "
         "He dips it and draws, and the pen stays the same object."),
    24: ("Flame climbs clear of the top of the chimney glass at 4.5-5.0 s (desk comment 6822411223).",
         "The lamp flame stays small and steady inside its glass chimney for the whole clip "
         "and never rises above the glass."),
    28: ("Parent finch beak shifts dark grey (0.0-2.0 s) to bright orange (3.0-4.5 s) with a head and body "
         "morph (desk comment 6829662956).",
         "The parent finch's beak stays dark grey-black and the same size and shape for the whole clip, "
         "and its head and body keep one form."),
    47: ("Tied bundle rises off the book at about 2.5 s without a hand and vanishes by about 3.0 s "
         "(desk comments 6830884885 / 6830918005).",
         "The manuscript and the packet stay resting on the desk for the whole clip. "
         "Nothing lifts unless a hand is holding it, and nothing disappears."),
    49: ("Carried parcel under the arm smears at 0.85 s and dissolves by 1.00 s "
         "(desk comments 6830884885 / 6830918005).",
         "The tied bundle stays one solid parcel under the carrying gentleman's arm for the whole clip "
         "and keeps its shape. The stone steps stay fixed."),
    54: ("Sheet under the hand turns from a white written page at 2.80 s to a blank tan curl at 2.90 s "
         "(desk comments 6831422974 / 6831444565).",
         "The page under his hand stays the same flat cream sheet, covered in ink scribble lines, "
         "for the whole clip. It never turns blank and never curls."),
    63: ("Warm gold light in the gutter of the open book from about 2.0 s to 4.5 s, forbidden by the prompt "
         "(desk comments 7020824090 / 7023130641).",
         "The open pages stay matte cream paper lit only by the grey window from one side, "
         "and the gutter between the pages stays in soft neutral shadow."),
}

# Rows lit by a lamp: fragile light under studio/RULES.md, so no unverified Lite after 5 Dec.
FRAGILE_LIGHT = {10: "warm lamplight", 24: "warm oil lamp light"}

# No real person may be named in a prompt. Place names in the locked prompts stay.
NAME_RE = re.compile(
    r"\b(darwin|wallace|malthus|lyell|hooker|gould|fitzroy|mendel|huxley|spencer|bell|"
    r"charles|alfred|thomas|joseph|emma|erasmus)\b", re.I)
TERM_RE = re.compile(r"same dna|lab dna|ken burns|photoreal|omni 1\.1", re.I)
TAIL_MARKERS = (" Daylight, window light", " No readable words")


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def retake_prompt(locked: str, fix: str) -> str:
    cut = min(i for i in (locked.find(m) for m in TAIL_MARKERS) if i > 0)
    return f"{locked[:cut]} {fix}{locked[cut:]}"


def check_prompt(row: int, locked: str, prompt: str) -> None:
    for label, text in (("locked", locked), ("retake", prompt)):
        m = NAME_RE.search(text) or TERM_RE.search(text)
        if m:
            raise SystemExit(f"row {row}: {label} prompt has a forbidden word: {m.group(0)!r}")
    cut = min(i for i in (locked.find(m) for m in TAIL_MARKERS) if i > 0)
    if not (prompt.startswith(locked[:cut]) and prompt.endswith(locked[cut:])):
        raise SystemExit(f"row {row}: retake prompt does not keep the locked prompt whole")
    if "No readable words or numbers anywhere." not in prompt or "Silent." not in prompt:
        raise SystemExit(f"row {row}: house tail missing")


def plates() -> dict[str, dict]:
    out = {}
    for path in sorted((HERE / "parts").glob("part-0*_plates_v02.json")):
        doc = json.loads(path.read_text())
        for plate in doc["plates"]:
            out[f"P{int(doc['part'])}:{plate['id']}"] = {**plate, "_board": f"parts/{path.name}"}
    return out


def receipts(owb: Path) -> dict[str, dict]:
    found: dict[str, dict] = {}

    def walk(node):
        if isinstance(node, dict):
            if node.get("row_id") and isinstance(node.get("input"), dict) and node.get("prompt_sha256"):
                found[node["row_id"]] = node
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    for path in sorted((owb / "jobs/reviews/J2529").glob("BATCH_*_RECEIPT.json")):
        walk(json.loads(path.read_text()))
    return found


def clip_seconds(use_s: float) -> int:
    return 8 if use_s > 6 else (6 if use_s > 4 else 4)


def build(owb: Path) -> dict:
    state_path = owb / "jobs/reviews/J2529/REVIEW_STATE.json"
    state_raw = state_path.read_bytes()
    state = json.loads(state_raw)
    if tuple(state["summary"]["retake_rows"]) != RETAKE_ROWS:
        raise SystemExit("REVIEW_STATE retake rows are not 3, 10, 24, 28, 47, 49, 54, 63")
    by_n = {r["n"]: r for r in state["rows"]}
    board, recs, rows = plates(), receipts(owb), []
    for n in RETAKE_ROWS:
        st = by_n[n]
        if st["status"] != "RETAKE" or st["keep"]:
            raise SystemExit(f"row {n} is not a confirmed RETAKE")
        plate, rec = board[st["row_id"]], recs[st["row_id"]]
        locked = plate["prompt"]
        if rec["prompt_sha256"] != sha(locked):
            raise SystemExit(f"row {n}: take-1 prompt differs from the locked v02 prompt")
        defect, fix = FIX[n]
        prompt = retake_prompt(locked, fix)
        check_prompt(n, locked, prompt)
        use_s = plate["use_s"]
        secs = clip_seconds(use_s)
        fragile = FRAGILE_LIGHT.get(n)
        rows.append({
            "n": n, "row_id": st["row_id"], "plate_board": plate["_board"],
            "film_window_s": st["film_window_s"], "use_s": use_s, "take": 2,
            "take_1_clip_sha256": st["clip_sha256"], "ruling_comment": st["ruling_comment"],
            "defect": defect, "fix_sentence": fix,
            "prompt_locked": locked, "prompt_locked_sha256": sha(locked),
            "prompt_retake": prompt, "prompt_retake_sha256": sha(prompt),
            "start_still": rec["input"]["file"], "start_still_sha256": rec["input"]["sha256"],
            "fragile_light": fragile,
            "price": {
                "pre_5_dec": {"model": "Veo 3.1 - Quality", "clip_s": 8, "credits": PRICE["Veo 3.1 - Quality"]},
                "post_5_dec": ({"model": "Omni 1.2 Flash", "clip_s": 8, "credits": 8 * 3,
                                "why": f"{fragile}: fragile light, Lite is not UAT-verified on it"}
                               if fragile else
                               {"model": "Veo 3.1 - Lite", "clip_s": secs, "credits": PRICE["Veo 3.1 - Lite"]}),
                "post_5_dec_all_omni": {"model": "Omni 1.2 Flash", "clip_s": 8, "credits": 8 * 3},
            },
            "generation_authorized": False,
        })
    a = sum(r["price"]["pre_5_dec"]["credits"] for r in rows)
    b = sum(r["price"]["post_5_dec"]["credits"] for r in rows)
    c = sum(r["price"]["post_5_dec_all_omni"]["credits"] for r in rows)

    def option(name, model, try1, expected, note):
        return {"option": name, "models": model, "credits_try_1": try1, "credits_expected": expected,
                "balance_after_try_1": BALANCE["credits"] - try1,
                "balance_after_expected": BALANCE["credits"] - expected,
                "clears_3000_floor": BALANCE["credits"] - expected >= HEADROOM_FLOOR, "note": note}

    return {
        "job": "J3738", "film": "HOS:013", "version": "v01", "mint": False,
        "status": "RETAKE_BOARD_V01_PARKED_FOR_CHIEF", "spend": {"gbp": 0, "flow_credits": 0},
        "source": {"review_state": "orbit-with-ben jobs/reviews/J2529/REVIEW_STATE.json",
                   "review_state_sha256": hashlib.sha256(state_raw).hexdigest(),
                   "review_state_updated_at": state["updated_at"]},
        "rows_in_board": list(RETAKE_ROWS),
        "rows_not_touched": {"rows": list(HELD_ROWS), "owner": "J3178",
                             "why": "moving_video_input capability hold; keep stays unset"},
        "balance": BALANCE, "headroom_floor": HEADROOM_FLOOR,
        "retake_hold_recorded": {"credits": RETAKE_HOLD, "rows": 7,
                                 "gap": "row 63 was added to the list without raising the hold; "
                                        "option A needs 800, so the Chief raises the hold by 100"},
        "prices": {**PRICE, "veo_3_1_quality_retires": QUALITY_RETIRES, "source": "studio/RULES.md, J3691"},
        "options": [
            option("A: before 5 Dec", "8 x Veo 3.1 - Quality, 8 s", a, round(a * QUALITY_RETRY),
                   "Same model as the 48 KEEP plates and the same start stills. Must be minted before 5 Dec 2026."),
            option("B: after 5 Dec, mixed", "6 x Veo 3.1 - Lite + 2 x Omni 1.2 Flash (rows 10, 24), 8 s", b,
                   round(b * QUALITY_RETRY),
                   "Needs a first-use style UAT for each new model against the KEEP plates in the same part. "
                   "Omni is 720p. Retry rate for these models is not measured; 2.59x is the Quality figure."),
            option("C: after 5 Dec, all Omni", "8 x Omni 1.2 Flash, 8 s", c, round(c * QUALITY_RETRY),
                   "One new model instead of two. 720p. First-use style UAT still needed."),
        ],
        "recommendation": "A. 800 credits is 3.4% of the balance, it keeps one look per part, and it needs "
                          "no new-model UAT. It only exists until 5 Dec 2026. Worker advice; the Chief decides.",
        "prompt_checks": {"real_person_names": 0, "forbidden_terms": 0,
                          "locked_prompt_kept_whole": True, "rows": len(rows)},
        "rows": rows,
    }


def check(doc: dict) -> None:
    if [r["n"] for r in doc["rows"]] != list(RETAKE_ROWS):
        raise SystemExit("board rows are not the 8 confirmed RETAKE rows")
    if set(doc["rows_in_board"]) & set(HELD_ROWS):
        raise SystemExit("a capability-held row is in the board")
    board = plates()
    for r in doc["rows"]:
        if board[r["row_id"]]["prompt"] != r["prompt_locked"]:
            raise SystemExit(f"row {r['n']}: locked prompt differs from the plate board")
        check_prompt(r["n"], r["prompt_locked"], r["prompt_retake"])
        if sha(r["prompt_retake"]) != r["prompt_retake_sha256"] or r["generation_authorized"]:
            raise SystemExit(f"row {r['n']}: prompt hash or authorisation wrong")
    if doc["mint"] or doc["spend"] != {"gbp": 0, "flow_credits": 0}:
        raise SystemExit("board must mint nothing and spend nothing")
    if doc["options"][0]["credits_try_1"] != 800:
        raise SystemExit("option A is not 8 x 100")


def markdown(doc: dict) -> str:
    bal = doc["balance"]
    out = [
        "# 013 retake prompt and price board v01: Darwin & Wallace",
        "",
        "**Written 25 Nov 2026 (`J3738`). Spend: `£0` / `0` Flow credits. Nothing minted. "
        "`generation_authorized` is `false` on every row. Parked for the Chief's price PASS and mint GO.**",
        "",
        "Covers only the 8 pass-1 rows the Chief ruled RETAKE in `J2529` "
        "(rows `3, 10, 24, 28, 47, 49, 54, 63`). The 10 capability-held rows (`56-62, 64-66`) stay with "
        "`J3178`; this board does not read or change their marks.",
        "",
        "Built by `_build_retake_board_v01.py` from the v02 plate boards and the J2529 receipts. "
        "Machine copy: `RETAKE_BOARD_v01.json`.",
        "",
        "## 1. Price",
        "",
        f"Flow balance: **{bal['credits']:,} credits** (daily reading {bal['read_at']}, from the spend ledger; "
        "this job did not open Flow). The mint job reads the live balance before any Create. "
        f"Headroom floor: {doc['headroom_floor']:,}.",
        "",
        "| Option | Models | First try | Expected (2.59x) | Balance after first try | Balance after expected | Clears floor |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for o in doc["options"]:
        out.append(f"| **{o['option']}** | {o['models']} | {o['credits_try_1']:,} | {o['credits_expected']:,} | "
                   f"{o['balance_after_try_1']:,} | {o['balance_after_expected']:,} | "
                   f"{'yes' if o['clears_3000_floor'] else 'NO'} |")
    out += [""] + [f"- **{o['option']}:** {o['note']}" for o in doc["options"]] + [
        "",
        f"**Recommendation (worker advice, the Chief decides):** {doc['recommendation']}",
        "",
        f"**Hold gap:** the recorded retake hold is {doc['retake_hold_recorded']['credits']} credits for 7 rows. "
        "Row 63 joined the list without raising it. Option A needs 800, so the Chief raises the hold by 100.",
        "",
        "**Rows 24, 47 and 49:** the Chief's rulings said \"same locked prompt\". Each row below carries both "
        "the locked prompt and the retake prompt (locked prompt plus one fix sentence), so the Chief can pick "
        "either at the price PASS.",
        "",
        "## 2. Prompt checks",
        "",
        "- Real person names in any prompt: **0** (checked by the builder on all 16 prompts).",
        "- Forbidden terms (`same DNA`, `lab DNA`, Ken Burns, photoreal, retired Omni): **0**.",
        "- Every retake prompt keeps its locked v02 prompt whole, word for word, and adds one sentence.",
        "- Every take-1 prompt hash in the J2529 receipts matches the locked v02 prompt.",
        "- Start still: the same pinned still as take 1 (path and sha256 in the JSON).",
        "",
        "## 3. Rows",
        "",
        "| # | Row | Film window | Use | Before 5 Dec | After 5 Dec (option B) |",
        "|---:|---|---|---:|---|---|",
    ]
    for r in doc["rows"]:
        p = r["price"]
        out.append(f"| {r['n']} | `{r['row_id']}` | {r['film_window_s'][0]:.2f}-{r['film_window_s'][1]:.2f} s | "
                   f"{r['use_s']:.2f} s | {p['pre_5_dec']['model']}, {p['pre_5_dec']['credits']} | "
                   f"{p['post_5_dec']['model']} {p['post_5_dec']['clip_s']} s, {p['post_5_dec']['credits']} |")
    for r in doc["rows"]:
        out += [
            "",
            f"### Row {r['n']} · `{r['row_id']}` · take 2",
            "",
            f"- **Defect (Chief):** {r['defect']}",
            f"- **Fix sentence:** {r['fix_sentence']}",
        ]
        if r["fragile_light"]:
            out.append(f"- **Fragile light:** {r['fragile_light']}. No unverified `Veo 3.1 - Lite` after 5 Dec.")
        out += ["", "Retake prompt:", "", "```", r["prompt_retake"], "```"]
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--owb", type=Path)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if args.check:
        check(json.loads(OUT_JSON.read_text()))
        print("RETAKE_BOARD_v01: check PASS (8 rows, 0 names, 0 forbidden terms, 0 credits)")
        return 0
    if not args.owb:
        ap.error("--owb <orbit-with-ben checkout> is needed to build")
    doc = build(args.owb)
    check(doc)
    OUT_JSON.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
    OUT_MD.write_text(markdown(doc))
    print(f"wrote {OUT_JSON.name} and {OUT_MD.name}: 8 rows, option A {doc['options'][0]['credits_try_1']} credits")
    return 0


if __name__ == "__main__":
    sys.exit(main())
