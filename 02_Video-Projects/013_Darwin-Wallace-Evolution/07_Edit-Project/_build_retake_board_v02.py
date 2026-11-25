#!/usr/bin/env python3
"""HOS 013 take-3 retake board v02 (J3757). Mints nothing, spends nothing, opens no browser.

Builds RETAKE_BOARD_v02.json and RETAKE_BOARD_v02.md for the 2 rows the acting Chief
ruled RETAKE again after take 2 (J3747): row 49 and row 63. Each row gets a fresh
start-still prompt (take 3, Flow Nano Banana 2, 0 credits) and a take-3 video prompt.

Not read and not changed: REVIEW_STATE.json, archive_v01_pass1/, archive_v01_retake1/,
the 10 capability-held rows (56-62, 64-66, J3178), the 6 clean take-2 rows
(3, 10, 24, 28, 47, 54) and J2529.

  python3 _build_retake_board_v02.py            # write the JSON and the page
  python3 _build_retake_board_v02.py --check    # re-check the committed JSON only
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_JSON = HERE / "RETAKE_BOARD_v02.json"
OUT_MD = HERE / "RETAKE_BOARD_v02.md"

ROWS = (49, 63)
HELD_ROWS = (56, 57, 58, 59, 60, 61, 62, 64, 65, 66)
CLEAN_TAKE2_ROWS = (3, 10, 24, 28, 47, 54)

# Flow balance after the J3747 take-2 mint, as given in the J3757 brief. This job did not
# open Flow. The mint job reads the live balance itself before any Create.
BALANCE = {"credits": 22650, "read_at": "after J3747 (25 Nov 2026)",
           "source": "J3757 brief (acting Chief, J3747 close-out); not re-read in this job"}
HEADROOM_FLOOR = 3000
QUALITY_RETRY = 2.59           # PICTURE_PLAN_v02 standard Quality retry allowance
PRICE = {"Nano Banana 2 still": 0, "Veo 3.1 - Quality": 100, "Veo 3.1 - Lite": 5,
         "Omni 1.2 Flash per second": 3}
QUALITY_RETIRES = "2026-12-05"
STILL_DIR = ("/Volumes/data/studio-live/History Of Science/02_Video-Projects/"
             "013_Darwin-Wallace-Evolution/04_Generated-Clips/part{part}/refs/v01_flow_stills/")

STILL_TAIL = (" Daylight, window light or matte painted ink only. No candle, flame, glow, spark, "
              "fireball or lightning. No readable words or numbers anywhere. No Explorer. No Orbit.")
VIDEO_TAIL = (" Daylight, window light or matte painted ink only. No candle, flame, glow, spark, "
              "fireball or lightning. No readable words or numbers anywhere. Silent. "
              "Continuous motion through the final frame. No Explorer. No Orbit.")

SPEC = {
    49: {
        "row_id": "P4:12_lyell_hooker_bundle", "part": "04",
        "plate_board": "parts/part-04_plates_v02.json", "stem": "P04_12_lyell_hooker_bundle",
        "take_1_still_sha256": "696d7eb39e0f083c174125456ed882bcab881ce7a0082be26f8c88f53a6661b1",
        "take_2_clip_sha256": "7045735282bdb79ff497840baf4bfb908880604917c5f35ef9b00b6dcfe3d04f",
        "take_2_defect": (
            "At 2.0-2.5 s the left gentleman hands the brown tied bundle to the top-hatted gentleman, who "
            "already carries a light ribbon-tied parcel under his left arm. At 3.0-5.5 s (inside the used "
            "0.00-5.36 s) the light parcel merges into one shrinking brown bundle; at 6.0-7.0 s the light "
            "parcel is back and the brown bundle is gone (acting Chief, J3747)."),
        "root_cause": (
            "The take-1 start still already shows two bulky separate bundles (one under an arm, one thick "
            "stack on the step). With one carrier on the steps, the model dissolves one of them."),
        "fix": (
            "Fresh start still with exactly one tied bundle, already in one gentleman's hands. No hand-off, "
            "nothing put down, nothing on the steps. The other gentleman walks beside him with empty hands."),
        "still": (
            "Premium Animistry-class 3D cartoon. In London daylight, two Victorian gentlemen in dark frock "
            "coats and top hats stand side by side at the foot of wide pale stone steps, seen from the side. "
            "The nearer gentleman holds exactly one thick bundle of cream manuscript pages, tied once with a "
            "dark ribbon, in both hands against his chest. The other gentleman's hands are empty at his "
            "sides. There is exactly one bundle in the picture. Nothing else is carried, and nothing lies on "
            "the steps or the ground. Soft overcast daylight, matte painted stone."),
        "video": (
            "Premium Animistry-class 3D cartoon. In London daylight, two Victorian gentlemen climb wide pale "
            "stone steps side by side at a calm walking pace. One gentleman carries exactly one ribbon-tied "
            "manuscript bundle in both hands against his chest for the whole clip. The other gentleman walks "
            "beside him with empty hands. The bundle is never handed over, never put down and never splits, "
            "and it keeps the same size, colour and shape. No second parcel appears at any time. The stone "
            "steps stay fixed."),
    },
    63: {
        "row_id": "P6:06a_origin_fifth_edition", "part": "06",
        "plate_board": "parts/part-06_plates_v02.json", "stem": "P06_06a_origin_fifth_edition",
        "take_1_still_sha256": "53c7c7a697aa850218f50232e70d0e5def938bc09b87b2d13e8a7e8badd12589",
        "take_2_clip_sha256": "42ddd51a2b09e3e17ece9a1b9bd56bc17cb3be50bb5d3ad4a96030163f8ec84b",
        "take_2_defect": (
            "Bright golden light comes out of the inside of the green book at 0.0-2.0 s (inside the used "
            "0.00-4.96 s), against the no-glow rule. The front cover is jaggedly cracked across the middle "
            "(0.0-2.0 s) and morphs flat into green pages (2.5-3.5 s). The folded letter curls into the air "
            "and flips itself (4.0-4.5 s) (acting Chief, J3747)."),
        "root_cause": (
            "The take-1 start still itself has the cracked green cover and a warm yellow-orange light inside "
            "the open pages, so any clip started from it fails at 0.0 s."),
        "fix": (
            "Mandatory fresh start still: the book closed, whole and flat, lit only by cool grey window "
            "light, so there is no open gutter for light to come from at frame 0. In the clip one hand lays "
            "the cover open; the letter and the spectacles do not move."),
        "still": (
            "Premium Animistry-class 3D cartoon. Close on a mahogany desk beside a window, lit only by cool "
            "grey overcast window light from the left side. A green cloth-bound book lies closed and flat on "
            "the desk. Its cover is whole, smooth and undamaged, with no crack, tear or crease. Beside the "
            "book one folded handwritten letter lies flat on the desk, with ink scribble lines only. A pair "
            "of round wire spectacles rests on the desk next to the letter. Matte cream page edges, neutral "
            "grey-beige shadows. No warm, yellow, gold or orange light anywhere, and no light comes from "
            "inside the book."),
        "video": (
            "Premium Animistry-class 3D cartoon. Close in cool grey window light on a mahogany desk. One "
            "sleeved hand slowly lifts the front cover of the green cloth-bound book by its edge and lays it "
            "open flat on the desk. The cover stays whole, smooth and green, and it hinges at the spine like "
            "a real book. The pages inside are matte cream paper with ink scribble lines, lit only by the "
            "grey window from one side, and the gutter between the pages stays in soft neutral shadow. No "
            "warm, yellow or gold light at any time. The folded letter stays flat on the desk and the "
            "spectacles stay where they are for the whole clip."),
        "alternative": (
            "If the Chief would sooner have no hand in frame: the same still with the book already open "
            "flat at its first pages, and a slow push-in with one page settling. Not written up here; "
            "it puts an open gutter in frame 0, which is where both earlier takes went gold."),
    },
}

# sha256 of each take-3 prompt, pinned. A prompt edit without a new pin fails --check.
PINNED = {
    49: {"still": "b08b71a86a2e8e123d54ab71f69be577106fd23a7bbc3ca059ec6489c59af4e2",
         "video": "b80f34a68cad9496e2b6d9ade8baa64826a89a99ffa49c0666b3602ba5aad250"},
    63: {"still": "331f7c47ab5a7556a9354862ec4a264bfd86a75b9ad445f53c6ea8f916bdb220",
         "video": "2ff63983f8092a5f2804192316f538a25b0c51a8b91eebb865db697eceb86350"},
}

# No real person may be named in a prompt. Place names stay.
NAME_RE = re.compile(
    r"\b(darwin|wallace|malthus|lyell|hooker|gould|fitzroy|mendel|huxley|spencer|bell|"
    r"charles|alfred|thomas|joseph|emma|erasmus)\b", re.I)
TERM_RE = re.compile(r"same dna|lab dna|ken burns|photoreal|omni 1\.1", re.I)


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def prompts(n: int) -> dict[str, str]:
    return {"still": SPEC[n]["still"] + STILL_TAIL, "video": SPEC[n]["video"] + VIDEO_TAIL}


def check_prompt(n: int, kind: str, text: str) -> None:
    m = NAME_RE.search(text) or TERM_RE.search(text)
    if m:
        raise SystemExit(f"row {n}: {kind} prompt has a forbidden word: {m.group(0)!r}")
    if not text.startswith("Premium Animistry-class 3D cartoon. "):
        raise SystemExit(f"row {n}: {kind} prompt does not open with the house style line")
    if not text.endswith(STILL_TAIL if kind == "still" else VIDEO_TAIL):
        raise SystemExit(f"row {n}: {kind} prompt has lost the house tail")
    if sha(text) != PINNED[n][kind]:
        raise SystemExit(f"row {n}: {kind} prompt sha256 {sha(text)} is not the pinned one")


def plate(n: int) -> dict:
    spec = SPEC[n]
    doc = json.loads((HERE / spec["plate_board"]).read_text())
    for p in doc["plates"]:
        if f"P{int(doc['part'])}:{p['id']}" == spec["row_id"]:
            return p
    raise SystemExit(f"row {n}: {spec['row_id']} is not in {spec['plate_board']}")


def build() -> dict:
    rows = []
    for n in ROWS:
        spec, p, pr = SPEC[n], plate(n), prompts(n)
        for kind, text in pr.items():
            check_prompt(n, kind, text)
        still_dir = STILL_DIR.format(part=spec["part"])
        rows.append({
            "n": n, "row_id": spec["row_id"], "plate_board": spec["plate_board"],
            "film_window_s": [p["t_s"], p["t_end_s"]], "use_s": p["use_s"], "take": 3,
            "take_2_clip": f"{spec['stem']}_t2.mp4", "take_2_clip_sha256": spec["take_2_clip_sha256"],
            "take_2_defect": spec["take_2_defect"], "root_cause": spec["root_cause"], "fix": spec["fix"],
            "prompt_locked_v02": p["prompt"], "prompt_locked_v02_sha256": sha(p["prompt"]),
            "start_still_take_1": {"file": f"{still_dir}{spec['stem']}_t1.png",
                                   "sha256": spec["take_1_still_sha256"], "reuse": False,
                                   "why": "carries the defect at frame 0"},
            "start_still_take_3": {"file": f"{still_dir}{spec['stem']}_t3.png", "exists": False,
                                   "model": "Flow Nano Banana 2", "credits": 0, "aspect": "16:9",
                                   "prompt": pr["still"], "prompt_sha256": sha(pr["still"]),
                                   "accept_before_video": (
                                       "exactly one bundle, two gentlemen, nothing on the steps"
                                       if n == 49 else
                                       "book closed and whole, no crack, no warm or gold light, "
                                       "letter and spectacles flat on the desk")},
            "video_take_3": {"file": f"{spec['stem']}_t3.mp4", "clip_s": 8,
                             "prompt": pr["video"], "prompt_sha256": sha(pr["video"])},
            **({"alternative": spec["alternative"]} if "alternative" in spec else {}),
            "price": {
                "pre_5_dec": {"model": "Veo 3.1 - Quality", "clip_s": 8, "credits": PRICE["Veo 3.1 - Quality"]},
                "post_5_dec_lite": {"model": "Veo 3.1 - Lite", "clip_s": 6, "credits": PRICE["Veo 3.1 - Lite"]},
                "post_5_dec_omni": {"model": "Omni 1.2 Flash", "clip_s": 8, "credits": 8 * 3},
            },
            "generation_authorized": False,
        })
    a = sum(r["price"]["pre_5_dec"]["credits"] for r in rows)
    lite = sum(r["price"]["post_5_dec_lite"]["credits"] for r in rows)
    omni = sum(r["price"]["post_5_dec_omni"]["credits"] for r in rows)

    def option(name, models, try1, note):
        expected = round(try1 * QUALITY_RETRY)
        return {"option": name, "models": models, "still_credits": 0, "credits_try_1": try1,
                "credits_expected": expected, "balance_after_try_1": BALANCE["credits"] - try1,
                "balance_after_expected": BALANCE["credits"] - expected,
                "clears_3000_floor": BALANCE["credits"] - expected >= HEADROOM_FLOOR, "note": note}

    return {
        "job": "J3757", "film": "HOS:013", "version": "v02", "follows": "RETAKE_BOARD_v01.json (J3738), J3747",
        "mint": False, "status": "RETAKE_BOARD_V02_PARKED_FOR_CHIEF", "spend": {"gbp": 0, "flow_credits": 0},
        "rows_in_board": list(ROWS),
        "rows_not_touched": {"capability_held": list(HELD_ROWS), "capability_held_owner": "J3178",
                             "clean_take_2": list(CLEAN_TAKE2_ROWS),
                             "also": ["REVIEW_STATE.json", "archive_v01_pass1/", "archive_v01_retake1/", "J2529"]},
        "balance": BALANCE, "headroom_floor": HEADROOM_FLOOR,
        "prices": {**PRICE, "veo_3_1_quality_retires": QUALITY_RETIRES, "source": "studio/RULES.md, J3691"},
        "options": [
            option("A: before 5 Dec", "2 x Nano Banana 2 still + 2 x Veo 3.1 - Quality, 8 s", a,
                   "Same model as the 48 KEEP plates and the 6 clean take-2 plates. No new-model style UAT. "
                   "Must be minted before 5 Dec 2026."),
            option("B1: after 5 Dec, Lite", "2 x Nano Banana 2 still + 2 x Veo 3.1 - Lite", lite,
                   "Needs a first-use style UAT against the KEEP plates in parts 04 and 06. "
                   "Retry rate for Lite is not measured; 2.59x is the Quality figure."),
            option("B2: after 5 Dec, Omni", "2 x Nano Banana 2 still + 2 x Omni 1.2 Flash, 8 s", omni,
                   "720p. Needs a first-use style UAT. Retry rate not measured."),
        ],
        "recommendation": "A. 200 credits is under 1% of the balance, it keeps one look per part and it needs "
                          "no new-model UAT. It only exists until 5 Dec 2026. Worker advice; the Chief decides.",
        "mint_order": ["1. Mint each take-3 still (0 credits) and check it against accept_before_video.",
                       "2. Only from an accepted still, mint the take-3 clip.",
                       "3. Take-3 clips go to the Chief's review; keep is not set by the mint job."],
        "prompt_checks": {"real_person_names": 0, "forbidden_terms": 0, "prompts": 4, "pinned_sha256": True},
        "rows": rows,
    }


def check(doc: dict) -> None:
    if [r["n"] for r in doc["rows"]] != list(ROWS) or doc["rows_in_board"] != list(ROWS):
        raise SystemExit("board rows are not 49 and 63")
    if set(doc["rows_in_board"]) & (set(HELD_ROWS) | set(CLEAN_TAKE2_ROWS)):
        raise SystemExit("a row this board must not touch is in it")
    for r in doc["rows"]:
        n = r["n"]
        if plate(n)["prompt"] != r["prompt_locked_v02"]:
            raise SystemExit(f"row {n}: locked prompt differs from the plate board")
        for kind, got in (("still", r["start_still_take_3"]), ("video", r["video_take_3"])):
            check_prompt(n, kind, got["prompt"])
            if got["prompt_sha256"] != PINNED[n][kind]:
                raise SystemExit(f"row {n}: {kind} prompt hash is not the pinned one")
        if r["generation_authorized"] or r["start_still_take_1"]["reuse"] or r["take"] != 3:
            raise SystemExit(f"row {n}: authorisation, still reuse or take number wrong")
        if r["take_2_clip_sha256"] != SPEC[n]["take_2_clip_sha256"]:
            raise SystemExit(f"row {n}: take-2 clip hash differs")
    if doc["mint"] or doc["spend"] != {"gbp": 0, "flow_credits": 0}:
        raise SystemExit("board must mint nothing and spend nothing")
    a = doc["options"][0]
    if a["credits_try_1"] != 200 or a["balance_after_try_1"] != 22450 or not a["clears_3000_floor"]:
        raise SystemExit("option A is not 2 x 100 from 22,650")
    if [o["credits_try_1"] for o in doc["options"][1:]] != [10, 48]:
        raise SystemExit("option B is not 10 (Lite) and 48 (Omni)")


def markdown(doc: dict) -> str:
    bal = doc["balance"]
    out = [
        "# 013 take-3 retake board v02: Darwin & Wallace",
        "",
        "**Written 25 Nov 2026 (`J3757`). Spend: `£0` / `0` Flow credits. Nothing minted, no browser opened. "
        "`generation_authorized` is `false` on both rows. Parked for the Chief's price PASS and mint GO.**",
        "",
        "Covers only the 2 rows the acting Chief ruled RETAKE again after take 2 (`J3747`): rows `49` and `63`. "
        "Both failed because the take-1 start still already held the fault, so each row gets a **fresh start "
        "still** (take 3, Flow Nano Banana 2, 0 credits) and a new video prompt.",
        "",
        "Not read or changed: `REVIEW_STATE.json`, `archive_v01_pass1/`, `archive_v01_retake1/`, the 10 "
        "capability-held rows (`56-62, 64-66`, `J3178`), the 6 clean take-2 rows (`3, 10, 24, 28, 47, 54`), `J2529`.",
        "",
        "Built by `_build_retake_board_v02.py`. Machine copy: `RETAKE_BOARD_v02.json`.",
        "",
        "## 1. Price",
        "",
        f"Flow balance: **{bal['credits']:,} credits** ({bal['read_at']}, from the job brief; this job did not "
        f"open Flow). The mint job reads the live balance before any Create. Headroom floor: {doc['headroom_floor']:,}.",
        "",
        "| Option | Models | Stills | First try | Expected (2.59x) | Balance after first try | Balance after expected | Clears floor |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for o in doc["options"]:
        out.append(f"| **{o['option']}** | {o['models']} | {o['still_credits']} | {o['credits_try_1']:,} | "
                   f"{o['credits_expected']:,} | {o['balance_after_try_1']:,} | {o['balance_after_expected']:,} | "
                   f"{'yes' if o['clears_3000_floor'] else 'NO'} |")
    out += [""] + [f"- **{o['option']}:** {o['note']}" for o in doc["options"]] + [
        "",
        f"**Recommendation (worker advice, the Chief decides):** {doc['recommendation']}",
        "",
        "## 2. Mint order",
        "",
    ] + [f"- {step}" for step in doc["mint_order"]] + [
        "",
        "## 3. Prompt checks",
        "",
        "- Real person names in the 4 take-3 prompts: **0** (checked by the builder).",
        "- Forbidden terms (`same DNA`, `lab DNA`, Ken Burns, photoreal, retired Omni): **0**.",
        "- Each prompt's sha256 is pinned in the builder; `--check` fails on an unpinned edit.",
        "- The take-1 start stills are marked `reuse: false`.",
    ]
    for r in doc["rows"]:
        still, video = r["start_still_take_3"], r["video_take_3"]
        out += [
            "",
            f"## Row {r['n']} · `{r['row_id']}` · take 3",
            "",
            f"Film window {r['film_window_s'][0]:.2f}-{r['film_window_s'][1]:.2f} s, uses {r['use_s']:.2f} s "
            f"of an 8 s clip.",
            "",
            f"- **Take-2 fault:** {r['take_2_defect']}",
            f"- **Cause:** {r['root_cause']}",
            f"- **Fix:** {r['fix']}",
            f"- **Accept the still only if:** {still['accept_before_video']}.",
        ]
        if "alternative" in r:
            out.append(f"- **Alternative:** {r['alternative']}")
        out += ["", f"Start-still prompt (`{still['prompt_sha256'][:12]}`):", "", "```", still["prompt"], "```",
                "", f"Video prompt (`{video['prompt_sha256'][:12]}`):", "", "```", video["prompt"], "```"]
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--print-pins", action="store_true", help="print the sha256 of each prompt and stop")
    args = ap.parse_args()
    if args.print_pins:
        print(json.dumps({n: {k: sha(v) for k, v in prompts(n).items()} for n in ROWS}, indent=1))
        return 0
    if args.check:
        check(json.loads(OUT_JSON.read_text()))
        print("RETAKE_BOARD_v02: check PASS (2 rows, 4 prompts, 0 names, 0 forbidden terms, 0 credits)")
        return 0
    doc = build()
    check(doc)
    OUT_JSON.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
    OUT_MD.write_text(markdown(doc))
    print(f"wrote {OUT_JSON.name} and {OUT_MD.name}: 2 rows, option A {doc['options'][0]['credits_try_1']} credits")
    return 0


if __name__ == "__main__":
    sys.exit(main())
