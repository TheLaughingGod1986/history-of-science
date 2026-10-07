#!/usr/bin/env python3
"""HOS 007: re-time and price parts/part-0N_plates_v01.json from the locked VO (no spend, mint nothing).

Claude desk task (PR #180, 7 Oct 2026): re-time the draft boards from the locked VO
(01 v03 · 02 v01 · 03 v02b · 04 v01b · 05 v01b) and price them, in the 006 format.

Input: Claude's draft boards (BOARD_V01_DRAFT, drafted from SHOT_LIST_v01.md with the script's
estimated times) and VO_RETIME_v01.json (_retime_vo_v01.py). The drafts keep every prompt, label
and note; only the timing and pricing fields are filled, except where noted below.

Each plate starts on a sentence (`s`, 1-based inside the part) or on a named word inside it, and runs
to the next plate's start (the next chapter card, or the last word + TAIL_S at the end of the film).
A plate must hold MIN_PLATE_S..CLIP_USE_S of picture (one 8 s clip less the cross-fade). The locked
VO runs 8:32 against the script's ~8:15, and Part 01 runs 100 s against 80 s, so the draft rows can't
cover it: spans over CLIP_USE_S get an added row (`added: true`), a reuse of an earlier or later KEEP
clip where a callback fits, otherwise a new mint (Fast unless a face or light needs Quality).

Engine, clip length and price as 006 (_build_plate_boards_v01.py, priced by Claude 2 Oct 2026):
Vertex list prices, video only, 1080p, GBP at 0.80; 005's takes-per-KEEP and stills-per-plate.
Held establishing shots go on Flow Fast (10 credits a take, 2 takes). The floor is today's Vertex
balance less Claude's £5 buffer (desk, 7 Oct 2026).

  python3 07_Edit-Project/_build_plate_boards_v01.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
EDIT = PROJ / "07_Edit-Project"
RETIME = json.loads((EDIT / "VO_RETIME_v01.json").read_text())
OUT = EDIT / "parts"
PLAN = EDIT / "PICTURE_PLAN_v01.json"

CLIP_USE_S = 7.9
MIN_PLATE_S = 2.4
TAIL_S = 0.6
REUSE_PAD_S = 0.5
VERTEX_LENGTHS = (4, 6, 8)

# Balances read 7 Oct 2026 (desk report hos_balances_2026-10-07): Vertex £25.59, Flow 52 credits.
VERTEX_BALANCE_GBP = 25.59
VERTEX_BUFFER_GBP = 5.00
FLOOR_GBP = round(VERTEX_BALANCE_GBP - VERTEX_BUFFER_GBP, 2)
FLOW_CREDITS_LEFT = 52
FLOW_FAST_CREDITS = 10
FLOW_TAKES_PER_PLATE = 2
USD_PER_S = {"Quality": 0.20, "Fast": 0.10}
USD_PER_STILL = 0.039
GBP_PER_USD = 0.80
TAKES_PER_KEEP = {"Quality": round(70 / 27, 2), "Fast": round(94 / 48, 2)}
STILLS_PER_PLATE = round(171 / 75, 2)

NOFLAME = " Daylight from out of frame; no candle, flame, lantern, lamp or fire in shot."
TAIL = " No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer."
F_HELD = "Fast: held establishing shot, slow push, no readable faces, nothing emissive."
F_DAY = "Fast: daylight or window light; nothing emissive in frame."
F_HANDS = "Fast: hands and props only, no face, nothing emissive."
F_WIDE = "Fast: wide shot, figures small and faces not readable, nothing emissive."
F_INK = "Fast: ink, paper, props or a flat illustrated diagram; nothing emissive."
REUSE_REASON = "Reuse: a window of a KEEP clip (callback), no new mint."

FLOW_PLATES = {"P1:04_church_dusk", "P2:08a_berkeley"}

# Per part: id -> (sentence, word or None). Draft ids keep their draft fields.
ANCHORS = {
    1: {
        "01_cow_meadow": (1, None), "02_doctor_case": (2, None), "03_table_three": (3, "milkmaid's"),
        "03b_globe_tease": (3, "medicine"), "04_church_dusk": (4, None), "07_map_shadows": (5, None),
        "07b_three_in_ten": (6, "three"), "07c_scarred": (7, None), "05_quiet_lane": (8, None),
        "06_shuttered_house": (9, None), "08_bell_tower": (9, "hear"), "09_churchyard": (9, "wonder"),
        "09b_counted": (10, None), "09c_case_again": (11, None), "10_variolation": (12, None),
        "10b_milder": (13, None), "10c_doors_close": (15, None), "11_mother_window": (16, None),
        "11b_child_cot": (18, None), "12_farm_gate": (19, None),
    },
    2: {
        "01_milking_dawn": (1, None), "02_healed_hand": (3, None), "02b_well_again": (5, None),
        "04_village_a": (6, None), "02c_laughs": (7, None), "03a_cap_and_pail": (8, None),
        "03_market_walk": (9, "you"), "05_village_b": (10, None), "05b_gate_again": (12, None),
        "06_jesty_family": (13, None), "06b_jesty_hands": (13, "scratched"), "07_jesty_table": (14, None),
        "08a_berkeley": (15, None), "08_jenner_window": (15, "edward"), "09_cuckoo": (17, None),
        "10_balloon": (17, "sent"), "10b_pail_on_desk": (18, None), "11_young_jenner": (19, None),
        "12_hunter_letter": (21, None), "12b_try_it": (22, None), "13_casebook": (24, "people"),
        "14_explorer_stool": (26, None),
    },
    3: {
        "01a_garden_path": (1, None), "01_sarah_nelmes": (1, "sarah"), "02_cow_from_lane": (2, None),
        "03_phipps_stool": (4, None), "03b_lancet_case": (5, "took"), "04_lancet_touch": (5, "placed"),
        "05_quill_writes": (6, None), "05b_week_passes": (7, None), "06_mild_fever": (8, None),
        "07_playing_garden": (9, None), "08_jenner_thinks": (10, None), "08b_uneasy_hand": (11, None),
        "08c_map_again": (12, None), "09_casebook_open": (13, None), "09b_phipps_again": (15, None),
    },
    4: {
        "01_page_turns": (1, None), "02_variolation_calm": (2, None), "03_waiting": (2, "which"),
        "04_day_one": (4, None), "05_days_pass": (6, None), "06_line_underlined": (8, None),
        "06b_still_nothing": (9, None), "07_jesty_again": (12, None), "07b_quill_again": (14, None),
        "07c_cases_again": (14, "publish"), "08_soho_press": (15, None), "08b_title_page": (16, None),
        "08c_cow_again": (16, "which"), "12_explorer_press": (17, None), "08d_doctors_scoff": (18, None),
        "09_satire": (19, "cartoonists"), "09b_boy_well": (20, None), "10a_packets": (21, None),
        "10_garden_hut": (21, "little"), "11_news_spreads": (22, None),
    },
    5: {
        "01_pasteur_1881": (1, None), "02_cow_again": (2, None), "09_meadow_golden": (4, None),
        "02b_news_again": (5, None), "04_health_workers": (6, None), "05_kit_opens": (6, "smallpox"),
        "03_globe_lights": (6, "until"), "06_assembly_1980": (7, None), "06b_churchyard_again": (8, None),
        "06c_assembly_again": (8, "been"), "08_body_learns": (10, None), "07_childs_arm": (11, None),
        "07b_kit_again": (12, None), "07c_playground": (13, None), "10_history_book": (14, None),
        "11_table_three_again": (15, None), "13_explorer_meadow": (16, None), "11b_storm_builds": (17, None),
        "12_kite_storm": (18, None),
    },
}

# Added rows: id -> ("reuse", source key) or (quality, engine_reason, side_label, prompt body)
ADDED = {
    1: {
        "03b_globe_tease": ("reuse", "P5:03_globe_lights"),
        "07b_three_in_ten": ("Fast", F_DAY, "3 IN 10",
            "A cottage windowsill in grey daylight: ten small plain wooden peg dolls stand in a row; a soft breeze, and three of them gently lie down. Calm, not frightening. Slow push in." + NOFLAME),
        "07c_scarred": ("Fast", F_WIDE, None,
            "A young woman in a shawl walks slowly away down a village lane, seen from behind, a hand on the wall as she goes; grey daylight, the camera follows at a distance. No marks shown." + NOFLAME),
        "09b_counted": ("Fast", F_DAY, None,
            "Seen from a cottage doorway: a mother tucks three small children into one shared bed in soft morning light, their faces turned away; she rests her hand on each blanket in turn." + NOFLAME),
        "09c_case_again": ("reuse", "P1:02_doctor_case"),
        "10b_milder": ("Fast", F_WIDE, "VARIOLATION",
            "The child from the surgery, well again, skips down a sunny village lane holding her mother's hand, seen from behind; the camera follows." + NOFLAME),
        "10c_doors_close": ("Fast", F_DAY, None,
            "A village lane at dusk: one cottage door closes quietly, then a second door further along closes too. No people, no marks on the doors." + NOFLAME),
        "11b_child_cot": ("Fast", F_DAY, None,
            "Over a mother's shoulder: a small child asleep in a wooden cot by a cottage window, a blanket rising and falling; soft daylight, no faces readable." + NOFLAME),
    },
    2: {
        "02b_well_again": ("Fast", F_WIDE, None,
            "The dairymaid sits on a cottage bench in a shawl sipping from a cup, then stands, stretches and picks up her pail, well again; seen at a distance." + NOFLAME),
        "02c_laughs": ("Fast", F_WIDE, None,
            "Over a low stone wall in a village lane, a dairymaid laughs and shakes her head at a worried neighbour; wide shot, faces small." + NOFLAME),
        "03a_cap_and_pail": ("Fast", F_DAY, None,
            "At the byre door in the morning, the dairymaid ties on her linen cap and lifts her wooden pail, seen from behind; the camera eases after her." + NOFLAME),
        "05b_gate_again": ("reuse", "P1:12_farm_gate"),
        "06b_jesty_hands": ("Fast", F_HANDS, None,
            "Close on a farmer's weathered hands in a rough work-coat sleeve: he holds a darning needle just above his wife's rolled sleeve, the gesture only; no wound, no blood, no needle in skin. Warm farmhouse daylight." + NOFLAME),
        "08a_berkeley": ("Fast", F_HELD, "BERKELEY",
            "Berkeley, a small Gloucestershire market town in the 1790s: a church tower, stone houses and a Georgian country house with a garden. Held wide shot, slow push. No people in shot." + NOFLAME),
        "10b_pail_on_desk": ("Fast", F_HANDS, None,
            "Jenner's study desk by the garden window: a small wooden milking pail beside the leather case-book; his hand turns the pail slowly, thinking. No face." + NOFLAME),
        "12b_try_it": ("Fast", F_HANDS, None,
            "Close on Jenner's desk: his hands set out a glass jar, a magnifying lens and an open notebook side by side, as if starting an experiment." + NOFLAME),
    },
    3: {
        "01a_garden_path": ("Fast", F_WIDE, None,
            "May blossom in a Georgian garden in Berkeley: a young dairymaid in a linen cap walks up the path to the door of the house, seen from behind." + NOFLAME),
        "03b_lancet_case": ("Fast", F_HANDS, None,
            "Close on Jenner's desk in May sunlight: his hand lifts a small ivory-handled lancet from its velvet case; the dairymaid's hand rests on the desk beside it, two or three soft round marks at most. The gesture only, nothing raw." + NOFLAME),
        "05b_week_passes": ("Fast", F_DAY, None,
            "Time-lapse over Jenner's Georgian house and garden: a week of days and nights sweeps past, shadows wheeling across the lawn; no lit windows, no lamps." ),
        "08b_uneasy_hand": ("Fast", F_HANDS, None,
            "Close on Jenner's hand resting on the closed lancet case on his desk; his fingers tap it slowly, uneasy, as the window light dims a little." + NOFLAME),
        "08c_map_again": ("reuse", "P1:07_map_shadows"),
        "09b_phipps_again": ("reuse", "P3:03_phipps_stool"),
    },
    4: {
        "06b_still_nothing": ("Fast", F_WIDE, None,
            "From Jenner's study window: his hand closes the case-book on the sill while outside on the sunny lawn the boy cartwheels, small in frame." + NOFLAME),
        "07b_quill_again": ("reuse", "P3:05_quill_writes"),
        "07c_cases_again": ("reuse", "P2:13_casebook"),
        "08b_title_page": ("Fast", F_INK, None,
            "Close on the wooden hand press: a printer's hands lift a freshly printed title page from the type; the page has no legible words (the title is added in the edit)." + NOFLAME),
        "08c_cow_again": ("reuse", "P1:01_cow_meadow"),
        "08d_doctors_scoff": ("Fast", F_WIDE, None,
            "A Georgian London coffee house: a group of doctors in wigs scoff and shake their heads over a slim pamphlet; wide shot, faces small." + NOFLAME),
        "09b_boy_well": ("reuse", "P3:07_playing_garden"),
        "10a_packets": ("Fast", F_HANDS, None,
            "Close on Jenner's hands tying small folded paper packets with string and stacking them in a basket for the post; daylight by the study window." + NOFLAME),
    },
    5: {
        "02b_news_again": ("reuse", "P4:11_news_spreads"),
        "06b_churchyard_again": ("reuse", "P1:09_churchyard"),
        "06c_assembly_again": ("reuse", "P5:06_assembly_1980"),
        "07b_kit_again": ("reuse", "P5:05_kit_opens"),
        "07c_playground": ("Fast", F_WIDE, None,
            "A sunny modern playground: children run, swing and climb, small in frame, faces not readable; the camera drifts past." + NOFLAME),
        "11b_storm_builds": ("Fast", F_WIDE, None,
            "Hot summer over 1750s Philadelphia rooftops: dark storm clouds build on the horizon while townsfolk below, small in frame, hurry indoors. No lightning." + NOFLAME),
    },
}

# Draft reuse rows (draft field `reuse_of` uses "NN/id")
DRAFT_REUSE = {"07_jesty_again": "P2:06_jesty_family", "02_cow_again": "P1:01_cow_meadow",
               "11_table_three_again": "P1:03_table_three"}

# Labels re-placed onto the plate the word lands in: id -> (label, sentence, word)
LABEL_AT = {
    1: {"10_variolation": None, "10b_milder": ("VARIOLATION", 14, None)},
    2: {"02_healed_hand": ("A MILD ILLNESS", 4, None)},
    3: {"03_phipps_stool": None, "04_lancet_touch": ("JAMES PHIPPS · AGE ABOUT 8", 5, "james")},
    4: {"03_waiting": ("WAITING", 3, None)},
}


def fmt(t: float) -> str:
    return f"{int(t // 60)}:{t % 60:05.2f}"


def key(w: str) -> str:
    return re.sub(r"[^a-z']", "", w.lower().replace("’", "'"))


def at(part: dict, s: int, word: str | None) -> float:
    sent = part["sentences"][s - 1]
    if word is None:
        return sent["film_s"]
    for t, w in part["words"]:
        if sent["start_s"] - 0.01 <= t <= sent["end_s"] and key(w) == word:
            return round(part["vo_film_start_s"] + t, 2)
    raise SystemExit(f"part {part['part']}: word {word!r} not heard in sentence {s}: {sent['text']}")


def main() -> None:
    parts = {p["part"]: p for p in RETIME["parts"]}
    drafts = {n: json.loads((OUT / f"part-{n:02d}_plates_v01.json").read_text()) for n in parts}
    rows_by_key: dict[str, dict] = {}
    boards = {}
    bad: list[tuple] = []
    for n, part in parts.items():
        draft = drafts[n]
        by_id = {r["id"]: r for r in draft["plates"]}
        missing = set(by_id) - set(ANCHORS[n])
        assert not missing, (n, missing)
        part_end = parts[n + 1]["card_in_film_s"] if n < len(parts) else part["vo_film_end_s"] + TAIL_S
        rows = []
        for pid, (s, word) in ANCHORS[n].items():
            t = at(part, s, word)
            if pid in by_id:
                row = {k: v for k, v in by_id[pid].items() if k not in ("t_s", "t")}
                row = {"id": pid, "t_s": round(t, 2), "t": fmt(t), **{k: v for k, v in row.items() if k != "id"}}
                if pid in DRAFT_REUSE:
                    row.update({"quality": "reuse", "reuse_of": DRAFT_REUSE[pid], "engine_reason": REUSE_REASON})
                    row.pop("prompt", None)
            else:
                spec = ADDED[n][pid]
                row = {"id": pid, "t_s": round(t, 2), "t": fmt(t), "explorer": False, "added": True}
                if spec[0] == "reuse":
                    row.update({"side_label": None, "quality": "reuse", "reuse_of": spec[1], "engine_reason": REUSE_REASON})
                else:
                    q, reason, label, body = spec
                    row.update({"side_label": label, "quality": q, "engine_reason": reason,
                                "prompt": "Premium Animistry-class 3D cartoon. " + body + TAIL})
            rows.append(row)
        rows.sort(key=lambda r: r["t_s"])
        for i, r in enumerate(rows):
            end = rows[i + 1]["t_s"] if i + 1 < len(rows) else part_end
            r["use_s"] = round(end - r["t_s"], 2)
            if not MIN_PLATE_S <= r["use_s"] <= CLIP_USE_S + 1e-6:
                bad.append((n, r["id"], r["t"], r["use_s"]))
            sents = part["sentences"]
            lines = [x["text"] for x in sents if r["t_s"] - 0.05 <= x["film_s"] < end - 0.05]
            first = max((x for x in sents if x["film_s"] <= r["t_s"] + 0.05), key=lambda x: x["film_s"], default=None)
            if first is not None and (not lines or first["text"] != lines[0]):
                lines.insert(0, f"(continues) {first['text']}")
            r["vo_land"] = lines
            rows_by_key[f"P{n}:{r['id']}"] = r
        for pid, spec in LABEL_AT.get(n, {}).items():
            r = next(x for x in rows if x["id"] == pid)
            if spec is None:
                r["side_label"] = None
                continue
            label, s, word = spec
            off = round(at(part, s, word) - r["t_s"], 2)
            assert 0 <= off < r["use_s"], (n, pid, off)
            r["side_label"] = label if off < 0.3 else f"{label} (on the word, +{off} s)"
        boards[n] = (draft, part, part_end, rows)
    if bad:
        raise SystemExit("plates outside {}-{} s:\n".format(MIN_PLATE_S, CLIP_USE_S)
                         + "\n".join(f"  part {n} {pid} at {t}: {u} s" for n, pid, t, u in bad))

    # clip length: own window, and every reuse window cut from it
    need = {k: min(r["use_s"] + REUSE_PAD_S, 8.0) for k, r in rows_by_key.items() if r["quality"] != "reuse"}
    for k, r in rows_by_key.items():
        if r["quality"] != "reuse":
            continue
        src = r["reuse_of"]
        assert src in need, (k, src)
        own = rows_by_key[src]["use_s"]
        clip_in = own + 0.1 if own + 0.1 + r["use_s"] + REUSE_PAD_S <= 8.0 else max(0.0, CLIP_USE_S - r["use_s"])
        end = clip_in + r["use_s"]
        assert end <= 8.0 - 0.1 + 1e-6, (k, end)
        r["clip_in_s"] = round(clip_in, 2)
        r["reuse_window"] = f"{clip_in:.2f}-{end:.2f} s of {src}" + ("" if clip_in >= own else " (overlaps its own window)")
        need[src] = max(need[src], min(end + REUSE_PAD_S, 8.0))

    cum = 0.0
    flow_credits = 0
    for k, r in rows_by_key.items():
        if r["quality"] == "reuse":
            r.update({"route": "reuse", "clip_s": 0, "cost_try1_gbp": 0.0, "cost_expected_gbp": 0.0,
                      "cum_expected_gbp": round(cum, 2), "beyond_floor": False})
            continue
        q = r["quality"]
        if k in FLOW_PLATES:
            assert q == "Fast", k
            credits = FLOW_FAST_CREDITS * FLOW_TAKES_PER_PLATE
            flow_credits += credits
            r.update({"route": "flow", "clip_s": 8, "flow_credits": credits, "cost_try1_gbp": 0.0,
                      "cost_expected_gbp": 0.0, "cum_expected_gbp": round(cum, 2), "beyond_floor": False,
                      "route_note": f"Flow Veo 3.1 Fast, {FLOW_TAKES_PER_PLATE} takes x {FLOW_FAST_CREDITS} credits; a third take moves to Vertex Fast"})
            continue
        clip = next(L for L in VERTEX_LENGTHS if L >= need[k] - 1e-6)
        try1 = USD_PER_S[q] * clip * GBP_PER_USD
        exp = try1 * TAKES_PER_KEEP[q] + STILLS_PER_PLATE * USD_PER_STILL * GBP_PER_USD
        cum += exp
        r.update({"route": "vertex", "clip_s": clip, "cost_try1_gbp": round(try1, 2),
                  "cost_expected_gbp": round(exp, 2), "cum_expected_gbp": round(cum, 2),
                  "beyond_floor": cum > FLOOR_GBP})
    assert flow_credits <= FLOW_CREDITS_LEFT, flow_credits

    totals = {"rows": 0, "mints": 0, "Quality": 0, "Fast": 0, "reuse": 0, "flow": 0, "added": 0,
              "vertex_s": {"Quality": 0, "Fast": 0}, "try1_gbp": 0.0, "expected_gbp": 0.0}
    per_part = []
    for n, (draft, part, part_end, rows) in boards.items():
        nq = sum(r["quality"] == "Quality" for r in rows)
        nf = sum(r["quality"] == "Fast" for r in rows)
        nr = sum(r["quality"] == "reuse" for r in rows)
        na = sum(bool(r.get("added")) for r in rows)
        board = {k: v for k, v in draft.items() if k != "plates"}
        board.update({
            "status": "BOARD_V01",
            "house": ("STUDIO_PLAYBOOK.md §5 · drafted by Claude 6 Oct 2026 from 07_Edit-Project/SHOT_LIST_v01.md · "
                      "re-timed from the locked VO (VO_RETIME_v01.json) and priced by the write lane, 7 Oct 2026 "
                      "(_build_plate_boards_v01.py). Rows marked `added` cover spans one 8 s clip can't hold. "
                      "Claude reviews before any mint."),
            "vo_file": f"02_Voiceover/{part['file']}",
            "vo_sha256": part["sha256"],
            "vo_duration_s": part["duration_s"],
            "chapter_card": None if n == 1 else {
                "text": part["chapter_card"], "in_s": part["card_in_film_s"], "hold_s": 1.5,
                "treatment": "soft cross-fade after the part's end + 0.6 s breath; music continues",
            },
            "vo_film_start_s": part["vo_film_start_s"],
            "part_end_film_s": round(part_end, 2),
            "clip_use_s": CLIP_USE_S,
            "xfade_s": 0.35,
            "explorer_plates": sum(bool(r["explorer"]) for r in rows),
            "counts": {"rows": len(rows), "mints": nq + nf, "Quality": nq, "Fast": nf, "reuse": nr, "added": na},
            "plates": rows,
        })
        path = OUT / f"part-{n:02d}_plates_v01.json"
        path.write_text(json.dumps(board, indent=2, ensure_ascii=False) + "\n")
        t1 = sum(r["cost_try1_gbp"] for r in rows)
        ex = sum(r["cost_expected_gbp"] for r in rows)
        nflow = sum(r["route"] == "flow" for r in rows)
        per_part.append({"part": n, "rows": len(rows), "Quality": nq, "Fast": nf, "reuse": nr, "added": na,
                         "flow": nflow, "try1_gbp": round(t1, 2), "expected_gbp": round(ex, 2)})
        for f, v in (("rows", len(rows)), ("mints", nq + nf), ("Quality", nq), ("Fast", nf), ("reuse", nr),
                     ("flow", nflow), ("added", na)):
            totals[f] += v
        for r in rows:
            if r["route"] == "vertex":
                totals["vertex_s"][r["quality"]] += r["clip_s"]
        totals["try1_gbp"] += t1
        totals["expected_gbp"] += ex
        print(f"part {n:02d}: {len(rows)} rows ({na} added) = {nq} Quality + {nf} Fast + {nr} reuse, {nflow} on Flow; "
              f"try-1 £{t1:.2f}, expected £{ex:.2f}")

    beyond = [{"key": k, "quality": r["quality"], "clip_s": r["clip_s"], "expected_gbp": r["cost_expected_gbp"],
               "cum_expected_gbp": r["cum_expected_gbp"]} for k, r in rows_by_key.items() if r.get("beyond_floor")]
    plan = {
        "film": "007_The-First-Vaccine",
        "written": "2026-10-07",
        "task": "Claude desk PR #180, 7 Oct 2026: re-time and price the 007 plate boards; mint nothing",
        "vertex_balance_gbp": VERTEX_BALANCE_GBP,
        "buffer_gbp": VERTEX_BUFFER_GBP,
        "floor_gbp": FLOOR_GBP,
        "flow": {"credits_left": FLOW_CREDITS_LEFT, "fast_credits_per_take": FLOW_FAST_CREDITS,
                 "plates": sorted(FLOW_PLATES), "credits_planned": flow_credits,
                 "note": "Flow credits are shared with 006 (on hold)."},
        "rates": {"vertex_usd_per_s": USD_PER_S, "usd_per_still": USD_PER_STILL, "gbp_per_usd_planning": GBP_PER_USD,
                  "takes_per_keep_005": TAKES_PER_KEEP, "stills_per_plate_005": STILLS_PER_PLATE},
        "vo_film_total_s": RETIME["vo_film_total_s"],
        "totals": {**totals, "try1_gbp": round(totals["try1_gbp"], 2), "expected_gbp": round(totals["expected_gbp"], 2)},
        "per_part": per_part,
        "top_up_needed_gbp": round(max(0.0, totals["expected_gbp"] - FLOOR_GBP), 2),
        "beyond_floor": beyond,
    }
    PLAN.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")
    print(f"film: {totals['rows']} rows ({totals['added']} added) = {totals['Quality']} Quality + {totals['Fast']} Fast + "
          f"{totals['reuse']} reuse ({totals['flow']} Fast on Flow, {flow_credits} credits); Vertex s {totals['vertex_s']}")
    print(f"try-1 £{totals['try1_gbp']:.2f} · expected £{totals['expected_gbp']:.2f} · usable £{FLOOR_GBP:.2f} → "
          f"top-up £{plan['top_up_needed_gbp']:.2f} · beyond floor: {len(beyond)} plates")


if __name__ == "__main__":
    main()
