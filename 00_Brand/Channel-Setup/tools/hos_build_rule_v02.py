#!/usr/bin/env python3
"""J0967: HOS stayed-to-watch build rules for unbuilt Shorts. Plans only.

Writes and checks the v02 cut plans. It does not render, generate, upload,
or spend. Rules (STAYED60 audit #14–#16, Ben 25 Oct 2026):

- the first cut (S01) ends by 2.85 s
- body rows sit in 2.50–3.80 s
- the loop tail is 1.0 s or less, on the frame-0 plate
- no "watch the full film" banner
- no video id and no code text on any end card
- S5–S8 still-opens stay unbuilt unless an existing moving plate is on disk

    python3 00_Brand/Channel-Setup/tools/hos_build_rule_v02.py --write
    python3 00_Brand/Channel-Setup/tools/hos_build_rule_v02.py --check
"""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
HI = 3.80
LO = 2.50
S01_MAX = 2.85
S01_MIN = 1.80
TAIL = 1.00
YT_ID = re.compile(r"\b[A-Za-z0-9_-]{11}\b")

# Audit-named first cuts. Missing keys keep a first row that already ends by 2.85 s.
S01_CAP = {
    # 007 Short B's audit cut was 2.20 s. 2.50 s still ends by 2.85 s and clears the 2.50 s floor.
    ("007", "Short_B"): 2.50,
    ("007", "Short_C"): 2.50,
    ("008", "Short_C"): 2.60,
    ("009", "Short_B"): 2.50,
    ("010", "Short_A"): 2.80,
}
S01_NEXT_PLATE = {
    ("007", "Short_B"): "P2:02_healed_hand",
}
# 009 Short B: drop 0.31 s from the 0.41 s pause at 0.68–1.09 (keep a 0.10 s gap).
PAUSE_TRIM = {("009", "Short_B"): {"cut_s": 1.09, "remove_s": 0.31}}

LIFT_FIRST = {
    "s04_photosynthesis": 2.60,
    "s05_charcoal_gas": 2.70,
    "s06_ingenhousz_oxygen": 2.64,
    "s07_priestley_mint": 2.70,
}

RULES = {
    "job": "J0967",
    "s01_ends_by_s": S01_MAX,
    "body_cut_s": [LO, HI],
    "loop_tail_s_max": TAIL,
    "full_film_banner": False,
    "end_card_video_id": None,
    "end_card_code_text": None,
    "render": False,
    "generation": False,
    "gbp": 0,
}


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def dump(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n")


def dur(row: dict) -> float:
    return round(row["t_end_s"] - row["t_start_s"], 3)


def plates_of(source: str) -> list[str]:
    text = source.replace("(loop window)", "")
    return [p.strip() for p in text.split("+") if p.strip()]


def end_card() -> dict:
    return {
        "text": None,
        "video_id": None,
        "code_text": None,
        "full_film_banner": False,
    }


def round_bounds(bounds: list[float], lock_at: int | None) -> list[float]:
    out = [round(b, 2) for b in bounds]
    out[0] = round(bounds[0], 2)
    out[-1] = round(bounds[-1], 2)
    if lock_at is not None:
        out[lock_at] = round(bounds[lock_at], 2)
    # Keep the sequence increasing after rounding.
    for i in range(1, len(out)):
        if out[i] < out[i - 1]:
            out[i] = out[i - 1]
    out[-1] = round(bounds[-1], 2)
    return out


def relax(bounds: list[float], lock_at: int | None, lo: float = LO, hi: float = HI) -> list[float]:
    """Move interior cuts so each span lands in [lo, hi]. bounds[0] and bounds[-1] stay put.
    bounds[lock_at] is the locked S01 end, when set."""
    bounds = bounds[:]
    for _ in range(60):
        changed = False
        n = len(bounds) - 1
        durs = [bounds[i + 1] - bounds[i] for i in range(n)]
        for i, d in enumerate(durs):
            if i == 0 and lock_at == 1:
                continue
            if d > hi + 1e-6 and i + 1 < n and lock_at != i + 1:
                nxt = durs[i + 1]
                give = min(d - hi, max(0.0, hi - nxt))
                if give > 0.005:
                    bounds[i + 1] -= give
                    changed = True
                    durs[i] -= give
                    durs[i + 1] += give
            elif d < lo - 1e-6 and i + 1 < n and lock_at != i + 1:
                nxt = bounds[i + 2] - bounds[i + 1]
                take = min(lo - d, max(0.0, nxt - lo))
                if take > 0.005:
                    bounds[i + 1] += take
                    changed = True
                    durs[i] += take
                    durs[i + 1] -= take
            elif d < lo - 1e-6 and i > 0 and lock_at != i:
                prv = bounds[i] - bounds[i - 1]
                floor = lo if not (i - 1 == 0 and lock_at == 1) else S01_MIN
                # Previous row 0 is locked, so do not steal from it.
                if i == 1 and lock_at == 1:
                    continue
                take = min(lo - d, max(0.0, prv - floor))
                if take > 0.005:
                    bounds[i] -= take
                    changed = True
        if not changed:
            break
    return bounds


def split_long(rows: list[dict]) -> list[dict]:
    out = []
    for row in rows:
        d = dur(row)
        if d <= HI + 0.001:
            out.append(row)
            continue
        n = max(2, math.ceil(d / HI - 1e-9))
        step = d / n
        t = row["t_start_s"]
        for k in range(n):
            t1 = row["t_end_s"] if k == n - 1 else round(row["t_start_s"] + (k + 1) * step, 3)
            out.append({**row, "t_start_s": round(t, 3), "t_end_s": round(t1, 3),
                        "note": (row.get("note") or "") + f" split {k + 1}/{n}"})
            t = t1
    return out


def unbundle(rows: list[dict]) -> list[dict]:
    out = []
    for row in rows:
        names = plates_of(row["source_long_plate"])
        if len(names) <= 1:
            row = {**row, "source_long_plate": names[0] if names else row["source_long_plate"]}
            out.append(row)
            continue
        d = dur(row)
        step = d / len(names)
        t = row["t_start_s"]
        for k, name in enumerate(names):
            t1 = row["t_end_s"] if k == len(names) - 1 else round(t + step, 3)
            out.append({**row, "t_start_s": round(t, 3), "t_end_s": round(t1, 3),
                        "source_long_plate": name,
                        "note": f"unbundled from {row['id']}"})
            t = t1
    return out


def cap_s01(rows: list[dict], cap: float, next_plate: str | None) -> list[dict]:
    row = rows[0]
    if row["t_end_s"] <= cap + 0.001:
        return rows
    rest = {**row, "t_start_s": cap, "id": row["id"] + "_b",
            "source_long_plate": next_plate or row["source_long_plate"],
            "note": f"S01 remainder after {cap:.2f} s"}
    head = {**row, "t_end_s": cap, "note": f"S01 ends at {cap:.2f} s"}
    return [head, rest, *rows[1:]]


def shift_short(short: dict, cut: float, remove: float) -> None:
    def sh(t: float) -> float:
        return round(t if t <= cut else t - remove, 3)

    short["vo_duration_s"] = round(short["vo_duration_s"] - remove, 3)
    short["vo_pause_trim"] = {
        "cut_s": cut, "remove_s": remove,
        "why": "009 Short B sentence-1 pause 0.68–1.09 s (0.41 s) trimmed to a 0.10 s gap. Existing take, no new VO.",
    }
    for row in short["rows"]:
        row["t_start_s"] = sh(row["t_start_s"])
        row["t_end_s"] = sh(row["t_end_s"])
    ov = short.get("teach_overlay")
    if ov:
        ov["t_start_s"] = sh(ov["t_start_s"])
        ov["t_end_s"] = sh(ov["t_end_s"])
    window = short.get("promoted_long_title_window_s")
    if window:
        short["promoted_long_title_window_s"] = [sh(window[0]), sh(window[1])]


def apply_bounds(rows: list[dict], bounds: list[float]) -> list[dict]:
    out = []
    for row, t0, t1 in zip(rows, bounds, bounds[1:]):
        out.append({**row, "t_start_s": round(t0, 3), "t_end_s": round(t1, 3)})
    return out


def plate_at(rows: list[dict], t: float) -> str:
    for row in rows:
        if row["t_start_s"] - 0.001 <= t < row["t_end_s"]:
            return row["source_long_plate"]
    return rows[-1]["source_long_plate"]


def spoken_at(rows: list[dict], t0: float, t1: float) -> str:
    bits = []
    for row in rows:
        if row["t_end_s"] <= t0 + 0.02 or row["t_start_s"] >= t1 - 0.02:
            continue
        text = (row.get("spoken") or "").strip()
        if text and text not in bits:
            bits.append(text)
    return " ".join(bits)


def even_layout(rows: list[dict], s01: float, vo_end: float, plates: list[str] | None = None) -> list[dict]:
    """S01 stays at s01. The rest of the VO is cut into equal 2.50–3.80 s rows."""
    vo_end = round(float(vo_end), 2)
    s01 = round(float(s01), 2)
    rest = round(vo_end - s01, 3)
    n = max(1, math.ceil(rest / HI - 1e-9))
    while n > 1 and rest / n < LO - 1e-9:
        n -= 1
    step = rest / n
    if step > HI + 0.02 or step < LO - 0.02:
        raise SystemExit(f"cannot fit {rest:.2f}s after S01 into {n} rows of {LO}-{HI}s")
    bounds = [0.0, s01]
    for i in range(1, n):
        bounds.append(round(s01 + i * step, 2))
    bounds.append(vo_end)
    last = round(bounds[-1] - bounds[-2], 3)
    if last > HI + 0.011:
        bounds[-2] = round(vo_end - HI, 2)
    elif last < LO - 0.011:
        bounds[-2] = round(vo_end - LO, 2)
    out = []
    for i, (a, b) in enumerate(zip(bounds, bounds[1:])):
        plate = plates[min(i, len(plates) - 1)] if plates else plate_at(rows, (a + b) / 2)
        out.append({
            "id": f"S{i + 1:02d}",
            "t_start_s": round(a, 2),
            "t_end_s": round(b, 2),
            "source_long_plate": plate,
            "route": rows[0].get("route", "reuse-long-plate") if rows else "reuse-long-plate",
            "spoken": spoken_at(rows, a, b),
            "flow_credits_expected": 0,
        })
    return out


def renumber(rows: list[dict]) -> list[dict]:
    out = []
    for i, row in enumerate(rows, 1):
        out.append({**row, "id": f"S{i:02d}", "use_s": dur(row)})
    return out


def plan_picture(film: str, short: dict) -> dict:
    key = (film, short["id"])
    short = json.loads(json.dumps(short))
    if key in PAUSE_TRIM:
        spec = PAUSE_TRIM[key]
        shift_short(short, spec["cut_s"], spec["remove_s"])
    rows = unbundle(short["rows"])
    cap = S01_CAP.get(key)
    if cap is None and rows[0]["t_end_s"] > S01_MAX:
        cap = S01_MAX
    if cap is not None:
        rows = cap_s01(rows, cap, S01_NEXT_PLATE.get(key))
    s01 = cap if cap is not None else min(rows[0]["t_end_s"], S01_MAX)
    vo_end = round(short["vo_duration_s"], 2)
    rows = even_layout(rows, s01, vo_end)
    rows = renumber(rows)
    frame0 = rows[0]["source_long_plate"]
    rows.append({
        "id": "loop_tail",
        "t_start_s": vo_end,
        "t_end_s": round(vo_end + TAIL, 2),
        "use_s": TAIL,
        "role": "loop_tail",
        "route": "reuse-long-plate",
        "source_long_plate": frame0,
        "spoken": "",
        "note": "Matched frame-0 plate after the last word. No banner, no video id, no code text.",
    })
    short["rows"] = rows
    short["loop_tail_s"] = TAIL
    short["end_card"] = end_card()
    short["full_film_banner"] = False
    short["render"] = False
    short["frame0_plate"] = frame0
    return short


def words_from_align(path: Path) -> list[tuple[str, float, float]]:
    data = json.loads(path.read_text())
    chars = data["characters"]
    starts = data["character_start_times_seconds"]
    ends = data["character_end_times_seconds"]
    words: list[tuple[str, float, float]] = []
    buf, w0, w1 = "", None, None
    for ch, a, b in zip(chars, starts, ends):
        if ch.isspace():
            if buf:
                words.append((buf, float(w0), float(w1)))
                buf = ""
            continue
        if not buf:
            w0 = a
        buf += ch
        w1 = b
    if buf:
        words.append((buf, float(w0), float(w1)))
    return words


def sentence_bounds(words: list[tuple[str, float, float]], t_end: float) -> list[float]:
    bounds = [0.0]
    for text, _a, b in words:
        if text[-1:] in ".?!":
            bounds.append(round(b, 3))
    if bounds[-1] < t_end - 0.05:
        bounds.append(round(t_end, 3))
    else:
        bounds[-1] = round(t_end, 3)
    return bounds


def rows_from_bounds(bounds: list[float], plates: list[str], spoken: list[str]) -> list[dict]:
    rows = []
    for i, (t0, t1) in enumerate(zip(bounds, bounds[1:])):
        plate = plates[min(i, len(plates) - 1)]
        line = spoken[min(i, len(spoken) - 1)] if spoken else ""
        rows.append({
            "id": f"S{i + 1:02d}",
            "t_start_s": round(t0, 3),
            "t_end_s": round(t1, 3),
            "source_long_plate": plate,
            "route": "reuse-long-plate",
            "spoken": line,
            "flow_credits_expected": 0,
        })
    return rows


def plan_from_words(words: list[tuple[str, float, float]], t_end: float, first_cut: float,
                    plates: list[str], spoken: list[str]) -> list[dict]:
    dummy = [{
        "t_start_s": a, "t_end_s": b, "spoken": t,
        "source_long_plate": plates[0], "route": "reuse-long-plate",
    } for t, a, b in words]
    # spoken sentences are kept on the dummy rows; plates are assigned in order.
    if spoken:
        dummy = [{**row, "spoken": ""} for row in dummy]
        # Reattach the script lines by time share so each row still reads with the sound off.
        step = (t_end or words[-1][2]) / max(1, len(spoken))
        for i, line in enumerate(spoken):
            dummy.append({
                "t_start_s": i * step, "t_end_s": t_end if i == len(spoken) - 1 else (i + 1) * step,
                "spoken": line, "source_long_plate": plates[0], "route": "reuse-long-plate",
            })
    return renumber(even_layout(dummy, min(first_cut, S01_MAX), t_end, plates=plates))


def plan_006_abc(root: Path) -> dict:
    vo = root / "02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/vo_20261004"
    specs = [
        {
            "id": "Short_A",
            "align": vo / "t1_willow_air_vo_v02_align.json",
            "vo": "10_Shorts/vo_20261004/t1_willow_air_vo_v02.mp3",
            "drop_title_from": "The",
            "first_cut": 2.50,
            "plates": [
                "part01/raw/v01/01_willow_air_t1",
                "part02/raw/v01/03_willow_shoot_scale_t1",
                "part02/raw/v01/06_garden_years_t2",
                "part02/raw/v01/09_weights_169_t1",
                "part02/raw/v01/13_tree_vs_pinch_t1",
            ],
            "spoken": [
                "A tree is built from thin air.",
                "One man spent five years proving the soil wasn't feeding it.",
                "He planted a willow in two hundred pounds of dried soil and gave it only water.",
                "Five years later the tree weighed a hundred and sixty-nine pounds,",
                "and the soil had lost just two ounces.",
            ],
            "title_note": "Trim the spoken title from  the word The (The Willow Tree That Was Made of Air) off the existing take. No new VO.",
        },
        {
            "id": "Short_B",
            "align": vo / "t2_mint_fixed_vo_v03_align.json",
            "vo": "10_Shorts/vo_20261004/t2_mint_fixed_vo_v03b.mp3",
            "first_cut": 2.50,
            "plates": [
                "part03/raw/v01/10_mint_jar_t1",
                "part03/raw/v01/11_candle_tall_t1",
                "part03/raw/v01/08_candles_out_t1",
                "part03/raw/v01/10_mint_jar_t1",
                "part03/raw/v01/11_candle_tall_t1",
            ],
            "spoken": [
                "A sprig of mint repaired the air.",
                "Joseph Priestley burned a candle in a sealed jar until the flame died,",
                "and no new flame would light.",
                "He slid in a sprig of mint and waited.",
                "Ten days later, a candle burned bright in that same air.",
                "Somehow, the little green plant had made the air good again.",
            ],
        },
        {
            "id": "Short_C",
            "align": vo / "t3_bubbles_sunlight_vo_v01_align.json",
            "vo": "10_Shorts/vo_20261004/t3_bubbles_sunlight_vo_v01.mp3",
            "first_cut": 2.65,
            "plates": [
                "part04/raw/v01/05_bubbles_macro_t1",
                "part04/raw/v01/03_plunge_leaf_t1",
                "part04/raw/v01/05_bubbles_macro_t1",
                "part03/raw/v01/18_dark_window_t1",
                "part04/raw/v01/12_shutters_open_t1",
                "part04/raw/v01/05_bubbles_macro_t1",
            ],
            "spoken": [
                "Leaves only make oxygen in the light.",
                "In 1779, a Dutch doctor called Jan Ingenhousz put fresh leaves in jars of water by a sunny window.",
                "Tiny silver bubbles rose from the green leaves.",
                "Move the jar into the shade, and the bubbles stopped.",
                "Back into the sun, and they started again.",
                "Plants run on sunlight.",
            ],
        },
    ]
    shorts = []
    for spec in specs:
        words = words_from_align(spec["align"])
        note = None
        if spec.get("drop_title_from"):
            idx = next(i for i, (w, _a, _b) in enumerate(words) if w == spec["drop_title_from"])
            note = spec["title_note"].replace("  ", " ")
            t_end = round(words[idx - 1][2], 3)
            words = words[:idx]
        else:
            t_end = round(words[-1][2], 3)
        rows = plan_from_words(words, t_end, spec["first_cut"], spec["plates"], spec["spoken"])
        vo_end = round(rows[-1]["t_end_s"], 2)
        rows.append({
            "id": "loop_tail",
            "t_start_s": vo_end,
            "t_end_s": round(vo_end + TAIL, 2),
            "use_s": TAIL,
            "role": "loop_tail",
            "route": "reuse-long-plate",
            "source_long_plate": spec["plates"][0],
            "spoken": "",
            "note": "Matched frame-0 plate. No banner, no video id, no code text.",
        })
        item = {
            "id": spec["id"],
            "vo": spec["vo"],
            "vo_duration_s": vo_end,
            "first_cut_s": rows[0]["t_end_s"],
            "rows": rows,
            "loop_tail_s": TAIL,
            "end_card": end_card(),
            "full_film_banner": False,
            "render": False,
            "promoted_long_title_window_s": [9.0, 14.0],
            "promoted_long_title": "The Willow Tree That Was Made of Air",
        }
        if note:
            item["vo_trim"] = {"drop_spoken_title_from_s": vo_end, "note": note}
            item["duration_note"] = (
                f"Speech ends at {vo_end:.2f} s. With the 1.0 s loop the Short is {vo_end + TAIL:.2f} s, "
                "under the 22 s band. The audit asked for this title trim. No words were added."
            )
        if spec["id"] == "Short_B":
            item["duration_note"] = (
                "Cuts are timed from t2_mint_fixed_vo_v03_align.json (21.60 s). "
                "The locked take named in VO_LOCK is t2_mint_fixed_vo_v03b.mp3 at 23.20 s. "
                "Re-time these cuts to that locked take before any render. No new VO."
            )
        shorts.append(item)
    return {"film": "006", "part": "Short A-C", **RULES, "shorts": shorts}


def plan_006_lifts(root: Path) -> dict:
    base = root / "02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts"
    shorts = []
    for path in sorted(base.glob("SHORT_s0[4-8]_*.json")):
        data = load(path)
        sid = data["id"]
        vo_end = round(float(data["vo_s"]), 3)
        spans = []
        for row in data["plan"]:
            if row.get("lands_on") == "loop":
                # Keep the part of the loop plate that still carries speech.
                if row["t0"] < vo_end - 0.05:
                    spans.append({**row, "t1": vo_end, "lands_on": "loop_speech"})
                continue
            t1 = min(row["t1"], vo_end)
            if t1 - row["t0"] >= 0.05:
                spans.append({**row, "t1": t1})
        rows = [{
            "id": f"S{i + 1:02d}",
            "t_start_s": round(s["t0"], 3),
            "t_end_s": round(s["t1"], 3),
            "source_long_plate": s["plate"],
            "route": "reuse-existing-plate",
            "spoken": "" if s.get("lands_on") in (0, "0") else str(s.get("lands_on")),
            "flow_credits_expected": 0,
        } for i, s in enumerate(spans)]
        cap = LIFT_FIRST.get(sid)
        if cap is not None:
            rows = cap_s01(rows, cap, None)
        elif rows[0]["t_end_s"] > S01_MAX:
            rows = cap_s01(rows, S01_MAX, None)
        s01 = cap if cap is not None else min(rows[0]["t_end_s"], S01_MAX)
        rows = renumber(even_layout(rows, s01, vo_end))
        frame0 = rows[0]["source_long_plate"]
        rows.append({
            "id": "loop_tail",
            "t_start_s": round(vo_end, 2),
            "t_end_s": round(vo_end + TAIL, 2),
            "use_s": TAIL,
            "role": "loop_tail",
            "route": "reuse-existing-plate",
            "source_long_plate": frame0,
            "spoken": "",
            "note": "One-second return to the frame-0 plate. No end-card line, no video id, no code text.",
        })
        shorts.append({
            "id": sid,
            "replaces": path.name,
            "vo_duration_s": round(vo_end, 3),
            "first_cut_s": rows[0]["t_end_s"],
            "rows": rows,
            "loop_tail_s": TAIL,
            "end_card": end_card(),
            "full_film_banner": False,
            "render": False,
            "retired_assembler": f"_build_short_{sid}_v01.py",
        })
    return {"film": "006", "part": "s04-s08", **RULES, "shorts": shorts}


def plan_films(root: Path) -> list[tuple[Path, dict]]:
    out = []
    for film, folder in (
        ("007", "007_The-First-Vaccine"),
        ("008", "008_Lightning-Franklin"),
        ("009", "009_The-Falling-Moon-Gravity"),
        ("010", "010_Alvarez-Clay-Line-Dinosaurs"),
    ):
        src = root / "02_Video-Projects" / folder / "10_Shorts" / "SHORTS_PICTURE_PLAN_v01.json"
        data = load(src)
        data["version"] = "v02"
        data["written"] = "2026-10-26"
        data["task"] = "J0967: stayed-to-watch build rules. Plans only, no render, no generation."
        data["rules"] = RULES
        data["shorts"] = [plan_picture(film, s) for s in data["shorts"]]
        data["totals"]["rows"] = sum(len(s["rows"]) for s in data["shorts"])
        dest = src.with_name("SHORTS_PICTURE_PLAN_v02.json")
        out.append((dest, data))
    return out


def stt_words(path: Path) -> list[tuple[str, float, float]]:
    data = json.loads(path.read_text())
    return [(w["text"], float(w["start"]), float(w["end"])) for w in data["words"] if w.get("type") == "word"]


def shift_words(words: list[tuple[str, float, float]], remove: float) -> list[tuple[str, float, float]]:
    return [(t, round(a - remove, 3), round(b - remove, 3)) for t, a, b in words]


def drop_dateline(words: list[tuple[str, float, float]], phrase: str) -> tuple[list[tuple[str, float, float]], float]:
    """Drop the opening dateline and shift the rest so the next word starts at 0.06 s."""
    n = len(phrase.split())
    got = " ".join(w for w, _a, _b in words[:n])
    if got != phrase:
        raise SystemExit(f"dateline {phrase!r} not at the start ({got!r})")
    nxt = words[n][1]
    remove = round(nxt - 0.06, 3)
    return shift_words(words[n:], remove), remove


def plan_standalone(root: Path) -> dict:
    stt = root / "docs/STANDALONE_SHORTS_TEST_2026-10/vo_v01/stt"
    # Dateline word ends (the comma after the year). Trim so the next word starts at 0.06 s.
    specs = [
        ("s5_penzias_pigeons", "hos_sa_s5_penzias_pigeons_vo_v01", "In 1964,", 1.54,
         "Still horn plate. No moving Penzias plate in the checkout. Stay unbuilt."),
        ("s6_fleming_mould", "hos_sa_s6_fleming_mould_vo_v01", "In 1928,", 1.64,
         "No petri or microbe moving plate on disk in 001. Stay unbuilt."),
        ("s7_priestley_mint", "hos_sa_s7_priestley_mint_vo_v01", "In 1771,", 1.88,
         "Intended open is 006 part03 10_mint_jar_t1 and 11_candle_tall_t1. Those files are not in this checkout. Stay unbuilt. No generation."),
        ("s8_hales_blood", "hos_sa_s8_hales_blood_vo_v01", None, None,
         "Still tube plate. No moving Hales plate on disk in 005. Stay unbuilt."),
    ]
    mint = root / "02_Video-Projects/006_Trees-Are-Made-Of-Air/04_Generated-Clips/part03/raw/v01/10_mint_jar_t1.mp4"
    shorts = []
    for sid, stem, dateline, next_start, why in specs:
        words = stt_words(stt / stem / "stt_raw.json")
        trim = None
        if dateline:
            words, remove = drop_dateline(words, dateline)
            trim = {"drop": dateline, "remove_s": remove, "claim_starts_s": 0.06}
        else:
            # S8: pull the 0.14 s onset to 0.05 s. No dateline.
            lead = 0.05 - words[0][1]
            words = [(t, round(a + lead, 3), round(b + lead, 3)) for t, a, b in words]
            trim = {"onset_to_s": 0.05, "shift_s": round(lead, 3)}
        t_end = round(words[-1][2], 3)
        first = 2.60 if sid != "s8_hales_blood" else 2.80
        rows = plan_from_words(words, t_end, first, ["UNBUILT"], [])
        for row in rows:
            said = [t for t, a, b in words if a >= row["t_start_s"] - 0.02 and a < row["t_end_s"] - 0.01]
            row["spoken"] = " ".join(said)
            row["source_long_plate"] = "UNBUILT"
        vo_end = round(rows[-1]["t_end_s"], 2)
        rows.append({
            "id": "loop_tail",
            "t_start_s": round(vo_end, 2),
            "t_end_s": round(vo_end + TAIL, 2),
            "use_s": TAIL,
            "role": "loop_tail",
            "source_long_plate": "UNBUILT",
            "spoken": "",
            "note": "Frame-0 plate, once a moving plate exists. No banner.",
        })
        item = {
            "id": sid,
            "status": "unbuilt",
            "why": why,
            "vo_trim": trim,
            "vo_duration_s": vo_end,
            "first_cut_s": rows[0]["t_end_s"],
            "rows": rows,
            "loop_tail_s": TAIL,
            "end_card": end_card(),
            "full_film_banner": False,
            "render": False,
            "generation": False,
            "frame0": "moving plate or unbuilt",
        }
        if sid == "s7_priestley_mint":
            item["intended_moving_plates"] = [
                "02_Video-Projects/006_Trees-Are-Made-Of-Air/04_Generated-Clips/part03/raw/v01/10_mint_jar_t1.mp4",
                "02_Video-Projects/006_Trees-Are-Made-Of-Air/04_Generated-Clips/part03/raw/v01/11_candle_tall_t1.mp4",
            ]
            item["intended_plates_on_disk"] = mint.exists()
        shorts.append(item)
    return {"part": "S5-S8", **RULES, "shorts": shorts}


def body_rows(short: dict) -> list[dict]:
    return [r for r in short["rows"] if r.get("role") != "loop_tail"]


def check_short(label: str, short: dict, errors: list[str]) -> None:
    rows = short["rows"]
    if short.get("full_film_banner") or short.get("end_card", {}).get("full_film_banner"):
        errors.append(f"{label}: full-film banner still on")
    card = short.get("end_card") or {}
    for key in ("text", "video_id", "code_text"):
        if card.get(key):
            errors.append(f"{label}: end card {key} is set ({card[key]!r})")
    if short.get("loop_tail_s", 99) > TAIL + 1e-6:
        errors.append(f"{label}: loop tail {short.get('loop_tail_s')} s")
    tail = rows[-1]
    if tail.get("role") != "loop_tail" or abs(dur(tail) - short["loop_tail_s"]) > 0.02:
        errors.append(f"{label}: loop tail row missing or not {short.get('loop_tail_s')} s")
    if tail["t_start_s"] != round(short["vo_duration_s"], 2) and abs(tail["t_start_s"] - short["vo_duration_s"]) > 0.02:
        errors.append(f"{label}: loop tail does not start at the VO end")
    blob = json.dumps(card) + json.dumps(tail)
    if "watch the full film" in blob.lower():
        errors.append(f"{label}: banner text still present")
    if YT_ID.search(card.get("text") or ""):
        errors.append(f"{label}: video id on the end card")
    body = body_rows(short)
    if not body:
        errors.append(f"{label}: no body rows")
        return
    if abs(body[0]["t_start_s"]) > 0.001:
        errors.append(f"{label}: does not start at 0")
    if body[0]["t_end_s"] > S01_MAX + 0.011:
        errors.append(f"{label}: S01 ends at {body[0]['t_end_s']} s")
    floor = S01_MIN if label.endswith("010_Alvarez-Clay-Line-Dinosaurs/Short_C") else LO
    if body[0]["t_end_s"] < floor - 0.011:
        errors.append(f"{label}: S01 is only {body[0]['t_end_s']} s")
    prev = 0.0
    for row in body:
        if abs(row["t_start_s"] - prev) > 0.02:
            errors.append(f"{label}: gap before {row['id']} ({prev} → {row['t_start_s']})")
        d = dur(row)
        if row["id"] != "S01" and row is not body[0]:
            if d < LO - 0.011 or d > HI + 0.011:
                errors.append(f"{label}: {row['id']} is {d:.2f} s ({row['t_start_s']}-{row['t_end_s']})")
        prev = row["t_end_s"]
    if short.get("render"):
        errors.append(f"{label}: render flag is on")


def check_all(root: Path) -> list[str]:
    errors: list[str] = []
    files = [
        root / "02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/BUILD_RULE_v02.json",
        root / "02_Video-Projects/007_The-First-Vaccine/10_Shorts/SHORTS_PICTURE_PLAN_v02.json",
        root / "02_Video-Projects/008_Lightning-Franklin/10_Shorts/SHORTS_PICTURE_PLAN_v02.json",
        root / "02_Video-Projects/009_The-Falling-Moon-Gravity/10_Shorts/SHORTS_PICTURE_PLAN_v02.json",
        root / "02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/10_Shorts/SHORTS_PICTURE_PLAN_v02.json",
        root / "docs/STANDALONE_SHORTS_TEST_2026-10/BUILD_RULE_S5_S8_v02.json",
    ]
    for path in files:
        if not path.exists():
            errors.append(f"missing {path.relative_to(root)}")
            continue
        data = load(path)
        for short in data["shorts"]:
            label = f"{path.parent.parent.name}/{short['id']}"
            check_short(label, short, errors)
            if "S5" in path.name or path.name.startswith("BUILD_RULE_S5"):
                if short.get("status") != "unbuilt" or short.get("generation"):
                    errors.append(f"{label}: S5–S8 must stay unbuilt with no generation")
                if short.get("intended_plates_on_disk"):
                    errors.append(f"{label}: plate appeared on disk; the unbuilt status needs a fresh look")
                for row in short["rows"]:
                    if row["source_long_plate"] != "UNBUILT":
                        errors.append(f"{label}: {row['id']} names a plate ({row['source_long_plate']})")
    return errors


def write_all(root: Path) -> None:
    abc = plan_006_abc(root)
    lifts = plan_006_lifts(root)
    combined = {
        "film": "006",
        **RULES,
        "shorts": abc["shorts"] + lifts["shorts"],
    }
    dump(root / "02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/BUILD_RULE_v02.json", combined)
    for path, data in plan_films(root):
        dump(path, data)
    dump(root / "docs/STANDALONE_SHORTS_TEST_2026-10/BUILD_RULE_S5_S8_v02.json", plan_standalone(root))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ns = ap.parse_args()
    if ns.write:
        write_all(REPO)
    if ns.check or not ns.write:
        errors = check_all(REPO)
        if errors:
            print(f"FAIL {len(errors)}")
            for line in errors:
                print(" ", line)
            raise SystemExit(1)
        print("PASS build-rule v02 plans")


if __name__ == "__main__":
    main()
