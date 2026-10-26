#!/usr/bin/env python3
"""J0967: HOS stayed-to-watch build rules for unbuilt Shorts (c56 FIX v2). Plans only.

Writes and checks the v02 cut plans. It does not render, generate, upload,
or spend. Rules (STAYED60 audit #14–#16, Ben 25 Oct 2026; Chief c56 26 Oct 2026):

- the first cut (S01) ends by 2.85 s on the end of the hook line (effective end <= 2.85 s after merging same-plate runs)
- body rows sit in 2.50–3.80 s, cutting on word ends (0 <= gap <= 0.10 s)
- each row's `spoken` contains only the words inside that row (no overlap across rows)
- no two adjacent body rows use the same plate (unless in_s/out_s are >= 2.0 s apart with a scene-change score)
- each row records `plate_dur_s` with `plate_dur_s >= use_s`, and notes sit in `note`, never inside `source_long_plate`
- the loop tail is 1.0 s or less, on the frame-0 plate
- no "watch the full film" banner, no video id and no code text on any end card
- 006 BUILD_RULE_v02 and S7 record `media_root` on the NAS archive path; S7 is `planned` on 10_mint_jar_t1 + 11_candle_tall_t1, while S5/S6/S8 stay `unbuilt`

    python3 00_Brand/Channel-Setup/tools/hos_build_rule_v02.py --check
    python3 00_Brand/Channel-Setup/tools/hos_build_rule_v02.py --write
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
MAIN_CHECKOUT = Path("/Users/benjaminoats/YouTube/History Of Science")
NAS_006_ROOT = Path(
    "/Volumes/data/mac-mini-archive/hos-worktrees/2026-10-22/hos-006-trees/"
    "02_Video-Projects/006_Trees-Are-Made-Of-Air"
)
LOCAL_007_ROOT = Path(
    "/Users/benjaminoats/YouTube/hos-007-vaccine/02_Video-Projects/007_The-First-Vaccine"
)

HI = 3.80
LO = 2.50
S01_MAX = 2.85
S01_MIN = 1.80
TAIL = 1.00
MAX_WORD_GAP = 0.10
YT_ID = re.compile(r"\b[A-Za-z0-9_-]{11}\b")
PAREN_NOTE = re.compile(r"\(([^)]+)\)")

# 009 Short B: drop 0.31 s from the 0.41 s pause at 0.68–1.09 (keep a 0.10 s gap).
PAUSE_TRIM = {("009", "Short_B"): {"cut_s": 0.84, "remove_s": 0.31}}

RULES = {
    "job": "J0967",
    "s01_ends_by_s": S01_MAX,
    "body_cut_s": [LO, HI],
    "word_end_gap_s_max": MAX_WORD_GAP,
    "adjacent_same_plate": False,
    "loop_tail_s_max": TAIL,
    "full_film_banner": False,
    "end_card_video_id": None,
    "end_card_code_text": None,
    "render": False,
    "generation": False,
    "gbp": 0,
}

# Non-repeating body plate sequences per Short, using only existing on-disk/NAS/board plates from the same film.
PLATES_006 = {
    "Short_A": [
        "part01/raw/v01/01_willow_air_t1",
        "part01/raw/v01/10_van_helmont_sack_t1",
        "part02/raw/v01/03_willow_shoot_scale_t1",
        "part02/raw/v01/02_balance_200_t1",
        "part02/raw/v01/06_garden_years_t2",
        "part02/raw/v01/09_weights_169_t1",
        "part02/raw/v01/13_tree_vs_pinch_t1",
    ],
    "Short_B": [
        "part03/raw/v01/10_mint_jar_t1",
        "part03/raw/v01/11_candle_tall_t1",
        "part03/raw/v01/08_candles_out_t1",
        "part03/raw/v01/10_mint_jar_t1",
        "part03/raw/v01/11_candle_tall_t1",
        "part04/raw/v01/06_collect_blaze_t3",
        "part03/raw/v01/14_trees_breathe_t1",
    ],
    "Short_C": [
        "part04/raw/v01/05_bubbles_macro_t1",
        "part04/raw/v01/01_villa_t1",
        "part04/raw/v01/03_plunge_leaf_t1",
        "part04/raw/v01/04_sunny_window_t1",
        "part04/raw/v01/05_bubbles_macro_t1",
        "part03/raw/v01/18_dark_window_t1",
        "part04/raw/v01/12_shutters_open_t1",
        "part04/raw/v01/14_leaf_glow_t1",
    ],
    "s04_photosynthesis": [
        "04_Generated-Clips/part05/raw/v01/06_leaf_in_t1.mp4",
        "04_Generated-Clips/part02/raw/v01/05_pure_water_t1.mp4",
        "04_Generated-Clips/part05/raw/v01/07_sugar_oxygen_t1.mp4",
        "04_Generated-Clips/part04/raw/v01/05_bubbles_macro_t1.mp4",
        "04_Generated-Clips/part05/raw/v01/08_sugar_wood_t1.mp4",
        "04_Generated-Clips/part05/raw/v01/14_built_from_sky_t1.mp4",
        "04_Generated-Clips/part05/raw/v01/11_trunk_pie_t1.mp4",
        "04_Generated-Clips/part01/raw/v01/01_willow_air_t1.mp4",
    ],
    "s05_charcoal_gas": [
        "04_Generated-Clips/part02/raw/v01/18_charcoal_hearth_t1.mp4",
        "04_Generated-Clips/part02/raw/v01/19_ash_mound_t1.mp4",
        "04_Generated-Clips/part02/raw/v01/20_shimmer_coals_t1.mp4",
        "04_Generated-Clips/part02/raw/v01/21_gas_window_t1.mp4",
        "04_Generated-Clips/part02/raw/v01/stretches_v03/15_desk_candle_t1_above_desk_v03.mp4",
        "04_Generated-Clips/part05/raw/v01/06_leaf_in_t1.mp4",
        "04_Generated-Clips/part02/raw/v01/06_garden_years_t2.mp4",
        "04_Generated-Clips/part02/raw/v01/22_shimmer_willow_t1.mp4",
    ],
    "s06_ingenhousz_oxygen": [
        "04_Generated-Clips/part04/raw/v01/05_bubbles_macro_t1.mp4",
        "04_Generated-Clips/part04/raw/v01/03_plunge_leaf_t1.mp4",
        "04_Generated-Clips/part04/raw/v01/06_collect_blaze_t3.mp4",
        "04_Generated-Clips/part03/raw/v01/11_candle_tall_t1.mp4",
        "04_Generated-Clips/part04/raw/v01/04_sunny_window_t1.mp4",
        "04_Generated-Clips/part03/raw/v01/18_dark_window_t1.mp4",
        "04_Generated-Clips/part04/raw/v01/12_shutters_open_t1.mp4",
        "04_Generated-Clips/part04/raw/v01/10_only_green_t2.mp4",
        "04_Generated-Clips/part04/raw/v01/11_night_jars_t1.mp4",
    ],
    "s07_priestley_mint": [
        "04_Generated-Clips/part03/raw/v01/11_candle_tall_t1.mp4",
        "04_Generated-Clips/part03/raw/v01/08_candles_out_t1.mp4",
        "04_Generated-Clips/part03/raw/v01/07_priestley_t1.mp4",
        "04_Generated-Clips/part03/raw/v01/10_mint_jar_t1.mp4",
        "04_Generated-Clips/part03/raw/v01/09_injured_air_t1.mp4",
        "04_Generated-Clips/part04/raw/v01/06_collect_blaze_t3.mp4",
        "04_Generated-Clips/part03/raw/v01/15_quill_vegetable_t1.mp4",
        "04_Generated-Clips/part03/raw/v01/14_trees_breathe_t1.mp4",
    ],
    "s08_willow_pot": [
        "04_Generated-Clips/part01/raw/v01/11_shoot_in_pot_t1.mp4",
        "04_Generated-Clips/part01/raw/v01/10_van_helmont_sack_t1.mp4",
        "04_Generated-Clips/part02/raw/v01/03_willow_shoot_scale_t1.mp4",
        "04_Generated-Clips/part02/raw/v01/04_lid_rain_t1.mp4",
        "04_Generated-Clips/part02/raw/v01_trim/08_haul_tree_t1_trim_0to4p8.mp4",
        "04_Generated-Clips/part02/raw/v01/13_tree_vs_pinch_t1.mp4",
        "04_Generated-Clips/part02/raw/v01/12_pointer_short_t1.mp4",
        "04_Generated-Clips/part01/raw/v01/02_balance_trunk_t1.mp4",
    ],
}

PLATES_FILMS = {
    ("007", "Short_B"): [
        "P2:03_market_walk",
        "P2:01_milking_dawn",
        "P2:02_healed_hand",
        "P2:02b_well_again",
        "P1:05_quiet_lane",
        "P1:06_shuttered_house",
        "P2:08_jenner_window",
        "P2:13_casebook",
        "P5:09_meadow_golden",
    ],
    ("007", "Short_C"): [
        "P5:03_globe_lights",
        "P1:07b_three_in_ten",
        "P3:04_lancet_touch",
        "P3:07_playing_garden",
        "P5:04_health_workers",
        "P5:05_kit_opens",
        "P5:06_assembly_1980",
        "P5:10_history_book",
    ],
    ("008", "Short_A"): [
        "P1:01_kite_open",
        "P3:19_kite_climb",
        "P3:13_key_ribbon",
        "P3:25_fibres_rise",
        "P4:02_knuckle_spark",
        "P4:08_teach_charge",
        "P4:10_richmann_rod",
    ],
    ("008", "Short_C"): [
        "P5:06_rod_fitting",
        "P5:01_house_rod",
        "P5:08_looking_path",
        "P5:09_wood_vs_metal",
        "P1:12_steeple_fire",
        "P5:10_metal_easy",
        "P5:11_safe_path",
        "P5:14_safe_towers",
        "P5:19_skyline_strike",
    ],
    ("009", "Short_A"): [
        "P1:01_moon_falling",
        "P3:08_km_a_second",
        "P3:07_ball_to_moon",
        "P3:05_shot_orbit",
        "P2:07_orchard_bench",
        "P2:08_the_apple",
        "P3:06_orbit_teach",
        "P5:09_orchard_dusk",
    ],
    ("009", "Short_B"): [
        "P4:05_minute_second",
        "P1:02_apple_and_moon",
        "P4:06_pretty_nearly",
        "P4:03_sixty_earths",
        "P4:01_weaker_far",
        "P4:04_dots_square",
        "P4:06_pretty_nearly",
        "P5:01_one_law",
    ],
    ("010", "Short_A"): [
        "P1:01_clay_line",
        "P2:01_walter_hammer",
        "P1:08_hand_on_rock",
        "P2:03_tiny_shells",
        "P2:05_almost_none",
        "P3:08_asaro_michel",
        "P4:01_iridium_spike",
        "P4:06_dust_veil",
    ],
    ("010", "Short_C"): [
        "P5:09_robin",
        "P4:06_dust_veil",
        "P5:11_why_survive",
        "P5:08_all_at_once",
        "P5:09_robin",
        "P5:13_window_song",
        "P5:10_explorer_robin",
        "P5:12_clay_callback",
    ],
}

PLATES_S7 = [
    ("04_Generated-Clips/part03/raw/v01/10_mint_jar_t1.mp4", 0.0, 2.56),
    ("04_Generated-Clips/part03/raw/v01/11_candle_tall_t1.mp4", 0.0, 3.40),
    ("04_Generated-Clips/part03/raw/v01/10_mint_jar_t1.mp4", 2.56, 5.71),
    ("04_Generated-Clips/part03/raw/v01/11_candle_tall_t1.mp4", 3.40, 7.13),
    ("04_Generated-Clips/part03/raw/v01/10_mint_jar_t1.mp4", 4.88, 8.00),
    ("04_Generated-Clips/part03/raw/v01/11_candle_tall_t1.mp4", 4.64, 8.00),
]

_PROBE_CACHE: dict[str, float] = {}
_BOARD_CACHE: dict[str, dict[str, float]] = {}


def resolve_repo_file(root: Path, rel: str | Path) -> Path:
    p = root / rel
    if p.exists():
        return p
    alt = MAIN_CHECKOUT / rel
    if alt.exists():
        return alt
    return p


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def dump(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n")


def dur(row: dict) -> float:
    return round(row["t_end_s"] - row["t_start_s"], 3)


def end_card() -> dict:
    return {
        "text": None,
        "video_id": None,
        "code_text": None,
        "full_film_banner": False,
    }


def probe_duration(path: Path) -> float | None:
    key = str(path)
    if key in _PROBE_CACHE:
        return _PROBE_CACHE[key]
    if not path.exists():
        return None
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=nw=1:nk=1",
            str(path),
        ],
        text=True,
    ).strip()
    val = round(float(out), 3)
    _PROBE_CACHE[key] = val
    return val


def resolve_nas_plate(media_root: Path, plate: str) -> Path:
    clean = PAREN_NOTE.sub("", plate).strip()
    if clean.startswith("04_Generated-Clips/"):
        rel = clean
    else:
        rel = f"04_Generated-Clips/{clean}"
    if not rel.endswith(".mp4"):
        rel += ".mp4"
    return media_root / rel


def film_board_durations(root: Path, folder: str) -> dict[str, float]:
    if folder in _BOARD_CACHE:
        return _BOARD_CACHE[folder]
    parts_dir = resolve_repo_file(root, f"02_Video-Projects/{folder}/07_Edit-Project/parts")
    plate_map: dict[str, float] = {}
    if parts_dir.exists():
        for p in sorted(parts_dir.glob("part-*_plates_v*.json")):
            d = load(p)
            pnum = int(d["part"])
            for r in d.get("plates", []):
                pid = f"P{pnum}:{r['id']}"
                cs = float(r.get("flow_clip_s") or r.get("clip_s") or r.get("use_s") or 8.0)
                plate_map[pid] = round(cs, 3)
    # Also check on-disk 007 clips if available
    if folder.startswith("007_") and LOCAL_007_ROOT.exists():
        for mp4 in sorted((LOCAL_007_ROOT / "04_Generated-Clips").rglob("*.mp4")):
            if mp4.name.startswith("._"):
                continue
            part_str = mp4.parts[-4]  # part01..part05
            if part_str.startswith("part0"):
                pnum = int(part_str[-1])
                stem = re.sub(r"_t\d+$", "", mp4.stem)
                pid = f"P{pnum}:{stem}"
                if pid not in plate_map:
                    d_s = probe_duration(mp4)
                    if d_s:
                        plate_map[pid] = d_s
    _BOARD_CACHE[folder] = plate_map
    return plate_map


def lookup_plate_duration(root: Path, folder_or_film: str, plate: str, media_root: str | None) -> tuple[bool, float | None]:
    if plate == "UNBUILT":
        return True, None
    # Check if an explicit note inside plate caps duration, e.g. "(2.78 s)"
    m = re.search(r"\((\d+(?:\.\d+)?)\s*s", plate)
    noted_cap = round(float(m.group(1)), 3) if m else None
    clean = PAREN_NOTE.sub("", plate).strip()

    if folder_or_film in ("006", "006_Trees-Are-Made-Of-Air", "BUILD_RULE_S5_S8_v02.json", "docs"):
        if not media_root:
            return False, noted_cap
        fp = resolve_nas_plate(Path(media_root), clean)
        d = probe_duration(fp)
        if d is None:
            return False, noted_cap
        return True, (min(d, noted_cap) if noted_cap is not None else d)

    folder_map = {
        "007": "007_The-First-Vaccine",
        "008": "008_Lightning-Franklin",
        "009": "009_The-Falling-Moon-Gravity",
        "010": "010_Alvarez-Clay-Line-Dinosaurs",
    }
    folder = folder_map.get(folder_or_film, folder_or_film)
    bmap = film_board_durations(root, folder)
    if clean in bmap:
        d = bmap[clean]
        return True, (min(d, noted_cap) if noted_cap is not None else d)
    return False, noted_cap


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
                words.append((buf, round(float(w0), 3), round(float(w1), 3)))
                buf = ""
            continue
        if not buf:
            w0 = a
        buf += ch
        w1 = b
    if buf:
        words.append((buf, round(float(w0), 3), round(float(w1), 3)))
    return words


def stt_words(path: Path) -> list[tuple[str, float, float]]:
    data = json.loads(path.read_text())
    out: list[tuple[str, float, float]] = []
    for w in data["words"]:
        if w.get("type") != "word":
            continue
        t, a, b = str(w["text"]), float(w["start"]), float(w["end"])
        if t == "3,600" and b - a > 1.0:
            parts = ["Three", "thousand", "six", "hundred"]
            step = (b - a) / len(parts)
            for k, p in enumerate(parts):
                out.append((p, round(a + k * step, 3), round(a + (k + 1) * step, 3)))
        else:
            out.append((t, round(a, 3), round(b, 3)))
    return out


def lift_words_006(root: Path, sid: str, d: dict, media_root: Path) -> list[tuple[str, float, float]]:
    align_rel = d["vo_source"].replace(".mp3", "_align.json")
    align_path = media_root / align_rel
    if not align_path.exists():
        align_path = resolve_repo_file(root, f"02_Video-Projects/006_Trees-Are-Made-Of-Air/{align_rel}")
    all_w = words_from_align(align_path)
    take = d["vo_take_indices"]
    tw = [all_w[i] for i in take]
    for idx in range(len(tw)):
        if idx == 0 or take[idx] != take[idx - 1] + 1:
            tw[idx] = (tw[idx][0][:1].upper() + tw[idx][0][1:], tw[idx][1], tw[idx][2])
    spans: list[list[float]] = []
    raw_gap = round(d["max_pause_s"] * d["atempo"], 3)
    for i, (_, s, e) in enumerate(tw):
        if sid in ("s04_photosynthesis", "s05_charcoal_gas"):
            s0 = s if i == 0 else s - 0.06
            e0 = e + 0.06
            if spans and s0 - spans[-1][1] <= raw_gap:
                spans[-1][1] = max(spans[-1][1], e0)
            elif spans:
                spans.append([max(s0, spans[-1][1] + 0.0), e0])
            else:
                spans.append([s0, e0])
        elif sid == "s06_ingenhousz_oxygen":
            s0 = max(0.0, s - 0.04)
            e0 = e + 0.06
            if spans and i > 0 and take[i] == take[i - 1] + 1 and s0 - spans[-1][1] <= raw_gap:
                spans[-1][1] = max(spans[-1][1], e0)
            else:
                spans.append([s0, e0])
        else:
            s0 = max(0.0, s - 0.02 if i == 0 else s - 0.04)
            e0 = e + 0.06
            if spans and i > 0 and take[i] == take[i - 1] + 1 and s0 - spans[-1][1] <= raw_gap:
                spans[-1][1] = max(spans[-1][1], e0)
            else:
                spans.append([s0, e0])
    out_t = 0.0
    remap: list[tuple[float, float, float]] = []
    for k, (s, e) in enumerate(spans):
        if k:
            out_t += raw_gap
        remap.append((s, e, out_t))
        out_t += e - s
    mapped: list[tuple[str, float, float]] = []
    for w, s, e in tw:
        for rs, re_, ot in remap:
            if rs <= s <= re_:
                mapped.append((w, round((ot + s - rs) / d["atempo"], 3), round((ot + e - rs) / d["atempo"], 3)))
                break
    tl_path = resolve_repo_file(
        root, f"02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/_work_{sid}_v01/timeline.json"
    )
    tl = load(tl_path)
    vo_ov = [o for o in tl["overlays"] if o["role"] == "vo"]
    idx = 0
    cal: list[tuple[str, float, float]] = []
    for o in vo_ov:
        n_w = len(o["text"].split())
        chunk_w = mapped[idx : idx + n_w]
        shift = round(o["t0"] - chunk_w[0][1], 3)
        for wtxt, a, b in chunk_w:
            cal.append((wtxt, round(a + shift, 3), round(b + shift, 3)))
        idx += n_w
    cal[-1] = (cal[-1][0], cal[-1][1], round(vo_ov[-1]["t1"] - 0.25, 3))
    return cal


def find_word_cuts(
    words: list[tuple[str, float, float]],
    vo_end: float,
    s01_min: float = LO,
    s01_max: float = S01_MAX,
    lo: float = LO,
    hi: float = HI,
) -> list[dict] | None:
    # Check if the opening hook sentence ends inside [S01_MIN - 0.10, s01_max]
    for i, (wtxt, _a, b) in enumerate(words):
        if b > s01_max + 1e-6:
            break
        nxt_a = words[i + 1][1] if i + 1 < len(words) else 999.0
        max_b = min(b + MAX_WORD_GAP, nxt_a - 0.002)
        if wtxt[-1:] in ".?!" and S01_MIN - 1e-6 <= max_b and b <= s01_max + 1e-6:
            s01_min = min(s01_min, S01_MIN)
            break

    def solve(first_floor: float) -> list[tuple[int, float]] | None:
        n = len(words)
        nodes: list[tuple[int, float]] = [(-1, 0.0)]
        for i in range(n - 1):
            _wtxt, _w0, w1 = words[i]
            cap = max(0.0, min(MAX_WORD_GAP, words[i + 1][1] - w1 - 0.002))
            steps = sorted(
                set([0.0, round(cap, 3)] + [round(x, 2) for x in (0.02, 0.04, 0.06, 0.07, 0.08, 0.09, 0.10) if x <= cap])
            )
            for s in steps:
                nodes.append((i, round(w1 + s, 3)))
        nodes.append((n - 1, round(vo_end, 3)))
        dp: dict[int, tuple[float, int | None]] = {0: (0.0, None)}
        for v in range(1, len(nodes)):
            wi_v, t_v = nodes[v]
            best_v: tuple[float, int] | None = None
            for u, (sc_u, _) in dp.items():
                wi_u, t_u = nodes[u]
                if wi_v <= wi_u:
                    continue
                d = round(t_v - t_u, 3)
                if u == 0:
                    if not (first_floor - 1e-6 <= d <= s01_max + 1e-6):
                        continue
                else:
                    if not (lo - 1e-6 <= d <= hi + 1e-6):
                        continue
                add = 0.0
                if v < len(nodes) - 1:
                    wtxt = words[wi_v][0]
                    if wtxt[-1:] in ".?!":
                        add += 25.0 if u == 0 else 12.0
                    elif wtxt[-1:] in ",;:":
                        add += 10.0 if u == 0 else 5.0
                    if u == 0 and wtxt[-1:] not in ".?!":
                        add += d * 3.0
                    if abs(t_v - words[wi_v][2]) < 0.002:
                        add += 0.5
                    add -= abs(d - 3.1) * 0.2
                cand = (sc_u + add, u)
                if best_v is None or cand[0] > best_v[0]:
                    best_v = cand
            if best_v is not None:
                dp[v] = best_v
        last_idx = len(nodes) - 1
        if last_idx not in dp:
            return None
        path: list[tuple[int, float]] = []
        cur = last_idx
        while cur != 0:
            path.append(nodes[cur])
            cur = dp[cur][1]  # type: ignore[assignment]
        path.reverse()
        return path

    sol = solve(s01_min) or solve(S01_MIN)
    if not sol:
        raise SystemExit(f"cannot cut {vo_end:.3f}s VO on word boundaries within {lo}-{hi}s")
    out: list[dict] = []
    prev_i, prev_t = 0, 0.0
    for k, (wi, tc) in enumerate(sol, 1):
        spoken = " ".join(x[0] for x in words[prev_i : wi + 1])
        w_end = round(words[wi][2], 3)
        gap = round(tc - w_end, 3)
        out.append(
            {
                "id": f"S{k:02d}",
                "t_start_s": round(prev_t, 3),
                "t_end_s": round(tc, 3),
                "use_s": round(tc - prev_t, 3),
                "word_end_s": w_end,
                "word_gap_s": gap,
                "spoken": spoken,
            }
        )
        prev_i, prev_t = wi + 1, tc
    return out


def build_rows(
    root: Path,
    folder_or_film: str,
    words: list[tuple[str, float, float]],
    vo_end: float,
    plates: list[str] | list[tuple[str, float, float]],
    route: str,
    media_root: str | None,
    loop_plate: str | None = None,
    loop_note: str | None = None,
    loop_dur_override: float | None = None,
) -> list[dict]:
    cuts = find_word_cuts(words, vo_end)
    assert cuts is not None
    if len(plates) < len(cuts):
        raise SystemExit(f"{folder_or_film}: {len(cuts)} rows but only {len(plates)} plates provided")
    rows: list[dict] = []
    for cut, p_spec in zip(cuts, plates):
        if isinstance(p_spec, tuple):
            plate, in_s, out_s = p_spec
        else:
            plate, in_s, out_s = p_spec, None, None
        ok, pdur = lookup_plate_duration(root, folder_or_film, plate, media_root)
        row: dict = {
            "id": cut["id"],
            "t_start_s": cut["t_start_s"],
            "t_end_s": cut["t_end_s"],
            "use_s": cut["use_s"],
            "word_end_s": cut["word_end_s"],
            "word_gap_s": cut["word_gap_s"],
            "source_long_plate": plate,
            "plate_dur_s": pdur,
            "route": route,
            "spoken": cut["spoken"],
            "flow_credits_expected": 0,
        }
        if in_s is not None and out_s is not None:
            row["in_s"] = round(in_s, 3)
            row["out_s"] = round(out_s, 3)
        rows.append(row)
    first_plate = plates[0][0] if isinstance(plates[0], tuple) else plates[0]
    lp = loop_plate or first_plate
    _ok, ldur = lookup_plate_duration(root, folder_or_film, lp, media_root)
    if loop_dur_override is not None:
        ldur = loop_dur_override
    tail_start = round(vo_end, 3)
    rows.append(
        {
            "id": "loop_tail",
            "t_start_s": tail_start,
            "t_end_s": round(tail_start + TAIL, 3),
            "use_s": TAIL,
            "role": "loop_tail",
            "route": route,
            "source_long_plate": lp,
            "plate_dur_s": ldur,
            "spoken": "",
            "note": loop_note or "Matched frame-0 plate after the last word. No banner, no video id, no code text.",
        }
    )
    return rows


def shift_words(words: list[tuple[str, float, float]], remove: float) -> list[tuple[str, float, float]]:
    return [(t, round(a - remove, 3), round(b - remove, 3)) for t, a, b in words]


def drop_dateline(words: list[tuple[str, float, float]], phrase: str) -> tuple[list[tuple[str, float, float]], float]:
    n = len(phrase.split())
    got = " ".join(w for w, _a, _b in words[:n])
    if got != phrase:
        raise SystemExit(f"dateline {phrase!r} not at the start ({got!r})")
    nxt = words[n][1]
    remove = round(nxt - 0.06, 3)
    return shift_words(words[n:], remove), remove


def plan_006_abc(root: Path, media_root: str) -> dict:
    vo = resolve_repo_file(root, "02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/vo_20261004")
    specs = [
        {
            "id": "Short_A",
            "align": vo / "t1_willow_air_vo_v02_align.json",
            "vo": "10_Shorts/vo_20261004/t1_willow_air_vo_v02.mp3",
            "drop_title_from": "The",
            "title_note": "Trim the spoken title from the word The (The Willow Tree That Was Made of Air) off the existing take. No new VO.",
        },
        {
            "id": "Short_B",
            "align": vo / "t2_mint_fixed_vo_v03_align.json",
            "vo": "10_Shorts/vo_20261004/t2_mint_fixed_vo_v03b.mp3",
        },
        {
            "id": "Short_C",
            "align": vo / "t3_bubbles_sunlight_vo_v01_align.json",
            "vo": "10_Shorts/vo_20261004/t3_bubbles_sunlight_vo_v01.mp3",
        },
    ]
    shorts = []
    for spec in specs:
        sid = spec["id"]
        words = words_from_align(spec["align"])
        note = None
        if spec.get("drop_title_from"):
            idx = next(i for i, (w, _a, _b) in enumerate(words) if w == spec["drop_title_from"])
            note = spec["title_note"]
            t_end = round(words[idx - 1][2], 3)
            words = words[:idx]
        else:
            t_end = round(words[-1][2], 3)
        plates = PLATES_006[sid]
        rows = build_rows(root, "006", words, t_end, plates, "reuse-long-plate", media_root)
        item: dict = {
            "id": sid,
            "vo": spec["vo"],
            "vo_duration_s": t_end,
            "first_cut_s": rows[0]["t_end_s"],
            "frame0_plate": plates[0],
            "rows": rows,
            "loop_tail_s": TAIL,
            "end_card": end_card(),
            "full_film_banner": False,
            "render": False,
            "promoted_long_title_window_s": [9.0, 14.0],
            "promoted_long_title": "The Willow Tree That Was Made of Air",
        }
        if note:
            item["vo_trim"] = {"drop_spoken_title_from_s": t_end, "note": note}
            item["duration_note"] = (
                f"Speech ends at {t_end:.2f} s. With the 1.0 s loop the Short is {t_end + TAIL:.2f} s, "
                "under the 22 s band. The audit asked for this title trim. No words were added."
            )
        if sid == "Short_B":
            item["duration_note"] = (
                "Cuts are timed from t2_mint_fixed_vo_v03_align.json (21.60 s). "
                "The locked take named in VO_LOCK is t2_mint_fixed_vo_v03b.mp3 at 23.20 s. "
                "Re-time these cuts to that locked take before any render. No new VO."
            )
        shorts.append(item)
    return {"film": "006", "part": "Short A-C", "media_root": media_root, **RULES, "shorts": shorts}


def plan_006_lifts(root: Path, media_root: str) -> dict:
    base = resolve_repo_file(root, "02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts")
    shorts = []
    for path in sorted(base.glob("SHORT_s0[4-8]_*.json")):
        data = load(path)
        sid = data["id"]
        vo_end = round(float(data["vo_s"]), 3)
        words = lift_words_006(root, sid, data, Path(media_root))
        plates = PLATES_006[sid]
        rows = build_rows(
            root,
            "006",
            words,
            vo_end,
            plates,
            "reuse-existing-plate",
            media_root,
            loop_note="One-second return to the frame-0 plate. No end-card line, no video id, no code text.",
        )
        shorts.append(
            {
                "id": sid,
                "replaces": path.name,
                "vo_duration_s": vo_end,
                "first_cut_s": rows[0]["t_end_s"],
                "frame0_plate": plates[0],
                "rows": rows,
                "loop_tail_s": TAIL,
                "end_card": end_card(),
                "full_film_banner": False,
                "render": False,
                "retired_assembler": f"_build_short_{sid}_v01.py",
            }
        )
    return {"film": "006", "part": "s04-s08", "media_root": media_root, **RULES, "shorts": shorts}


def plan_films(root: Path) -> list[tuple[Path, dict]]:
    out = []
    for film, folder in (
        ("007", "007_The-First-Vaccine"),
        ("008", "008_Lightning-Franklin"),
        ("009", "009_The-Falling-Moon-Gravity"),
        ("010", "010_Alvarez-Clay-Line-Dinosaurs"),
    ):
        src = resolve_repo_file(root, f"02_Video-Projects/{folder}/10_Shorts/SHORTS_PICTURE_PLAN_v01.json")
        if not src.exists():
            src = resolve_repo_file(root, f"02_Video-Projects/{folder}/10_Shorts/SHORTS_PICTURE_PLAN_v02.json")
        data = load(src)
        data["version"] = "v02"
        data["written"] = "2026-10-26"
        data["task"] = "J0967: stayed-to-watch build rules (c56 FIX v2). Plans only, no render, no generation."
        data["rules"] = RULES
        new_shorts = []
        for s in data["shorts"]:
            short = json.loads(json.dumps(s))
            key = (film, short["id"])
            stt_p = resolve_repo_file(
                root, f"02_Video-Projects/{folder}/10_Shorts/vo_v02/stt/{short['stem']}/stt_raw.json"
            )
            words = stt_words(stt_p)
            vo_end = round(float(short["vo_duration_s"]), 3)
            if key in PAUSE_TRIM:
                spec = PAUSE_TRIM[key]
                cut_s, rem_s = spec["cut_s"], spec["remove_s"]
                words = [
                    (t, round(a if a <= cut_s else a - rem_s, 3), round(b if b <= cut_s else b - rem_s, 3))
                    for t, a, b in words
                ]
                if not short.get("vo_pause_trim"):
                    vo_end = round(vo_end - rem_s, 3)
                short["vo_duration_s"] = vo_end
                short["vo_pause_trim"] = {
                    "cut_s": 1.09,
                    "remove_s": rem_s,
                    "why": "009 Short B sentence-1 pause 0.68–1.09 s (0.41 s) trimmed to a 0.10 s gap. Existing take, no new VO.",
                }
                ov = short.get("teach_overlay")
                if ov and ov["t_start_s"] > 1.09:
                    ov["t_start_s"] = round(ov["t_start_s"] - rem_s, 3)
                    ov["t_end_s"] = round(ov["t_end_s"] - rem_s, 3)
                win = short.get("promoted_long_title_window_s")
                if win and win[0] == 9.0:
                    short["promoted_long_title_window_s"] = [round(win[0] - rem_s, 3), round(win[1] - rem_s, 3)]
            plates = PLATES_FILMS[key]
            loop_note = None
            loop_dur = None
            if key == ("010", "Short_C"):
                loop_note = (
                    "4.00 s loop window on P5:09_robin; P1:04_long_reign (2.78 s) replaced on S07 by P5:10_explorer_robin (8.00 s). "
                    "Matched frame-0 plate after the last word. No banner, no video id, no code text."
                )
                loop_dur = 4.0
            rows = build_rows(
                root,
                folder,
                words,
                vo_end,
                plates,
                "reuse-long-plate",
                None,
                loop_note=loop_note,
                loop_dur_override=loop_dur,
            )
            short["rows"] = rows
            short["first_cut_s"] = rows[0]["t_end_s"]
            short["loop_tail_s"] = TAIL
            short["end_card"] = end_card()
            short["full_film_banner"] = False
            short["render"] = False
            short["frame0_plate"] = plates[0]
            new_shorts.append(short)
        data["shorts"] = new_shorts
        data["totals"]["rows"] = sum(len(s["rows"]) for s in data["shorts"])
        dest = root / "02_Video-Projects" / folder / "10_Shorts" / "SHORTS_PICTURE_PLAN_v02.json"
        out.append((dest, data))
    return out


def plan_standalone(root: Path, media_root: str) -> dict:
    stt = resolve_repo_file(root, "docs/STANDALONE_SHORTS_TEST_2026-10/vo_v01/stt")
    specs = [
        (
            "s5_penzias_pigeons",
            "hos_sa_s5_penzias_pigeons_vo_v01",
            "In 1964,",
            "unbuilt",
            "Still horn plate. No moving Penzias plate in the checkout or NAS archive. Stay unbuilt.",
        ),
        (
            "s6_fleming_mould",
            "hos_sa_s6_fleming_mould_vo_v01",
            "In 1928,",
            "unbuilt",
            "No petri or microbe moving plate on disk in 001. Stay unbuilt.",
        ),
        (
            "s7_priestley_mint",
            "hos_sa_s7_priestley_mint_vo_v01",
            "In 1771,",
            "planned",
            "Planned on existing 006 part03 moving plates on NAS (10_mint_jar_t1 frame 0 + 11_candle_tall_t1). Plan-only, not built, no generation.",
        ),
        (
            "s8_hales_blood",
            "hos_sa_s8_hales_blood_vo_v01",
            None,
            "unbuilt",
            "Still tube plate. No moving Hales plate on disk in 005. Stay unbuilt.",
        ),
    ]
    shorts = []
    for sid, stem, dateline, status, why in specs:
        words = stt_words(stt / stem / "stt_raw.json")
        if dateline:
            words, remove = drop_dateline(words, dateline)
            trim = {"drop": dateline, "remove_s": remove, "claim_starts_s": 0.06}
        else:
            lead = 0.05 - words[0][1]
            words = [(t, round(a + lead, 3), round(b + lead, 3)) for t, a, b in words]
            trim = {"onset_to_s": 0.05, "shift_s": round(lead, 3)}
        t_end = round(words[-1][2], 3)
        if sid == "s7_priestley_mint":
            rows = build_rows(
                root,
                "006",
                words,
                t_end,
                PLATES_S7,
                "reuse-existing-plate",
                media_root,
                loop_plate="04_Generated-Clips/part03/raw/v01/10_mint_jar_t1.mp4",
                loop_note="Matched frame-0 moving plate 10_mint_jar_t1 on NAS. No banner, no video id, no code text.",
            )
            item: dict = {
                "id": sid,
                "status": "planned",
                "media_root": media_root,
                "why": why,
                "vo_trim": trim,
                "vo_duration_s": t_end,
                "first_cut_s": rows[0]["t_end_s"],
                "frame0": "04_Generated-Clips/part03/raw/v01/10_mint_jar_t1.mp4",
                "intended_moving_plates": [
                    "04_Generated-Clips/part03/raw/v01/10_mint_jar_t1.mp4",
                    "04_Generated-Clips/part03/raw/v01/11_candle_tall_t1.mp4",
                ],
                "intended_plates_on_disk": True,
                "rows": rows,
                "loop_tail_s": TAIL,
                "end_card": end_card(),
                "full_film_banner": False,
                "render": False,
                "generation": False,
            }
        else:
            cuts = find_word_cuts(words, t_end)
            assert cuts is not None
            rows = [
                {
                    **c,
                    "source_long_plate": "UNBUILT",
                    "plate_dur_s": None,
                    "route": "unbuilt",
                    "flow_credits_expected": 0,
                }
                for c in cuts
            ]
            rows.append(
                {
                    "id": "loop_tail",
                    "t_start_s": t_end,
                    "t_end_s": round(t_end + TAIL, 3),
                    "use_s": TAIL,
                    "role": "loop_tail",
                    "source_long_plate": "UNBUILT",
                    "plate_dur_s": None,
                    "spoken": "",
                    "note": "Frame-0 plate, once a moving plate exists. No banner.",
                }
            )
            item = {
                "id": sid,
                "status": status,
                "why": why,
                "vo_trim": trim,
                "vo_duration_s": t_end,
                "first_cut_s": rows[0]["t_end_s"],
                "rows": rows,
                "loop_tail_s": TAIL,
                "end_card": end_card(),
                "full_film_banner": False,
                "render": False,
                "generation": False,
                "frame0": "moving plate or unbuilt",
            }
        shorts.append(item)
    return {"part": "S5-S8", **RULES, "shorts": shorts}


def load_words_for_short(root: Path, parent_name: str, short: dict, media_root: str | None) -> list[tuple[str, float, float]]:
    sid = short["id"]
    if parent_name == "006_Trees-Are-Made-Of-Air":
        vo_dir = resolve_repo_file(root, "02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/vo_20261004")
        if sid == "Short_A":
            w = words_from_align(vo_dir / "t1_willow_air_vo_v02_align.json")
            idx = next(i for i, (wt, _, _) in enumerate(w) if wt == "The")
            return w[:idx]
        if sid == "Short_B":
            return words_from_align(vo_dir / "t2_mint_fixed_vo_v03_align.json")
        if sid == "Short_C":
            return words_from_align(vo_dir / "t3_bubbles_sunlight_vo_v01_align.json")
        src_p = next(( resolve_repo_file(root, "02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/SHORT_s04_photosynthesis_v01.json").parent ).glob(f"SHORT_{sid}_*.json"))
        mr = Path(media_root) if media_root else NAS_006_ROOT
        return lift_words_006(root, sid, load(src_p), mr)
    if parent_name in (
        "007_The-First-Vaccine",
        "008_Lightning-Franklin",
        "009_The-Falling-Moon-Gravity",
        "010_Alvarez-Clay-Line-Dinosaurs",
    ):
        stem = short["stem"]
        stt_p = resolve_repo_file(root, f"02_Video-Projects/{parent_name}/10_Shorts/vo_v02/stt/{stem}/stt_raw.json")
        w = stt_words(stt_p)
        if parent_name.startswith("009_") and sid == "Short_B":
            w = [(t, round(a if a <= 0.84 else a - 0.31, 3), round(b if b <= 0.84 else b - 0.31, 3)) for t, a, b in w]
        return w
    stt_dir = resolve_repo_file(root, "docs/STANDALONE_SHORTS_TEST_2026-10/vo_v01/stt")
    stem_map = {
        "s5_penzias_pigeons": ("hos_sa_s5_penzias_pigeons_vo_v01", "In 1964,"),
        "s6_fleming_mould": ("hos_sa_s6_fleming_mould_vo_v01", "In 1928,"),
        "s7_priestley_mint": ("hos_sa_s7_priestley_mint_vo_v01", "In 1771,"),
        "s8_hales_blood": ("hos_sa_s8_hales_blood_vo_v01", None),
    }
    stem, dl = stem_map[sid]
    w = stt_words(stt_dir / stem / "stt_raw.json")
    if dl:
        w, _ = drop_dateline(w, dl)
    else:
        lead = 0.05 - w[0][1]
        w = [(t, round(a + lead, 3), round(b + lead, 3)) for t, a, b in w]
    return w


def body_rows(short: dict) -> list[dict]:
    return [r for r in short["rows"] if r.get("role") != "loop_tail"]


def same_plate_without_inout(a: dict, b: dict) -> bool:
    pa = a.get("source_long_plate") or ""
    pb = b.get("source_long_plate") or ""
    if not pa or pa == "UNBUILT" or pa != pb:
        return False
    if a.get("in_s") is None or b.get("in_s") is None or a.get("out_s") is None or b.get("out_s") is None:
        return True
    if abs(float(b["in_s"]) - float(a["in_s"])) < 2.0 - 1e-6:
        return True
    if not b.get("scene_change_score"):
        return True
    return False


def check_short(
    root: Path,
    parent_name: str,
    label: str,
    short: dict,
    plan_media_root: str | None,
    errors: list[str],
) -> None:
    rows = short["rows"]
    media_root = short.get("media_root") or plan_media_root
    if parent_name == "006_Trees-Are-Made-Of-Air" and not media_root:
        errors.append(f"{label}: missing media_root for 006 plates")
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
    if body[0]["t_end_s"] < S01_MIN - 0.011:
        errors.append(f"{label}: S01 is only {body[0]['t_end_s']} s")

    # Effective S01 end after merging adjacent same-plate runs at the start
    eff_s01_end = body[0]["t_end_s"]
    for idx in range(1, len(body)):
        if same_plate_without_inout(body[idx - 1], body[idx]):
            eff_s01_end = body[idx]["t_end_s"]
        else:
            break
    if eff_s01_end > S01_MAX + 0.011:
        errors.append(
            f"{label}: S01 effective end after merging same-plate run ({body[0]['source_long_plate']}) is {eff_s01_end:.2f} s (> {S01_MAX} s)"
        )

    # Check adjacent same-plate runs across all body rows
    i = 0
    while i < len(body):
        j = i
        while j + 1 < len(body) and same_plate_without_inout(body[j], body[j + 1]):
            j += 1
        if j > i:
            hold = round(body[j]["t_end_s"] - body[i]["t_start_s"], 2)
            errors.append(
                f"{label}: back-to-back same plate {body[i]['source_long_plate']} on {body[i]['id']}-{body[j]['id']} (real hold {hold:.2f} s)"
            )
        i = j + 1

    # Load words to verify cuts on word ends and non-overlapping spoken text
    words = load_words_for_short(root, parent_name, short, media_root)
    prev = 0.0
    prev_spoken_norm = ""
    for idx, row in enumerate(body):
        if abs(row["t_start_s"] - prev) > 0.02:
            errors.append(f"{label}: gap before {row['id']} ({prev} -> {row['t_start_s']})")
        d = dur(row)
        if idx > 0 and (d < LO - 0.011 or d > HI + 0.011):
            errors.append(f"{label}: {row['id']} is {d:.2f} s ({row['t_start_s']}-{row['t_end_s']})")
        prev = row["t_end_s"]

        # Word-end check on interior cuts
        if idx < len(body) - 1:
            t_cut = row["t_end_s"]
            matched_word = None
            for wi, (_wt, _wa, wb) in enumerate(words):
                gap = round(t_cut - wb, 3)
                nxt_start = words[wi + 1][1] if wi + 1 < len(words) else 999.0
                if -0.005 <= gap <= MAX_WORD_GAP + 0.005 and t_cut <= nxt_start + 0.005:
                    matched_word = (wi, wb, gap)
                    break
            if matched_word is None:
                errors.append(f"{label}: {row['id']} cut at {t_cut:.2f} s falls mid-word or > {MAX_WORD_GAP:.2f} s after word end")

        # Spoken overlap / mismatch check: assign each word to the unique row containing its midpoint
        row_words_map: dict[int, list[str]] = {r_i: [] for r_i in range(len(body))}
        for wt, wa, wb in words:
            mid = 0.5 * (wa + wb)
            for r_i, r_obj in enumerate(body):
                if r_obj["t_start_s"] - 1e-6 <= mid <= r_obj["t_end_s"] + 1e-6:
                    row_words_map[r_i].append(wt)
                    break
        expected_spoken = " ".join(row_words_map[idx])
        actual_spoken = (row.get("spoken") or "").strip()
        if not actual_spoken:
            errors.append(f"{label}: {row['id']} has empty spoken text")
        elif prev_spoken_norm and (prev_spoken_norm in actual_spoken or actual_spoken in prev_spoken_norm):
            errors.append(f"{label}: {row['id']} spoken text overlaps with previous row")
        elif actual_spoken != expected_spoken:
            errors.append(f"{label}: {row['id']} spoken does not match words in [{row['t_start_s']}, {row['t_end_s']}]")
        prev_spoken_norm = actual_spoken

    # Plate existence, notes-in-plate, and plate_dur_s >= use_s checks
    for row in rows:
        plate = row.get("source_long_plate") or ""
        if "(" in plate or ")" in plate or "+" in plate:
            errors.append(f"{label}: {row['id']} has notes or bundle inside source_long_plate ({plate!r})")
        if plate == "UNBUILT":
            continue
        use_s = round(float(row.get("use_s") or dur(row)), 3)
        pdur = row.get("plate_dur_s")
        exists, resolved_dur = lookup_plate_duration(root, parent_name, plate, media_root)
        if not exists:
            errors.append(f"{label}: {row['id']} plate {plate!r} does not resolve under media_root/board")
        if pdur is None:
            errors.append(f"{label}: {row['id']} missing plate_dur_s")
        else:
            if float(pdur) < use_s - 0.01:
                errors.append(f"{label}: {row['id']} plate_dur_s {pdur} < use_s {use_s}")
        if resolved_dur is not None and resolved_dur < use_s - 0.01:
            errors.append(f"{label}: {row['id']} resolved plate duration {resolved_dur} s < use_s {use_s} s ({plate})")

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
        parent_name = path.parent.parent.name
        plan_media_root = data.get("media_root")
        for short in data["shorts"]:
            label = f"{parent_name}/{short['id']}"
            check_short(root, parent_name, label, short, plan_media_root, errors)
            if path.name.startswith("BUILD_RULE_S5"):
                sid = short["id"]
                if short.get("generation") or short.get("render"):
                    errors.append(f"{label}: S5–S8 must have no generation and no render")
                if sid == "s7_priestley_mint":
                    if short.get("status") != "planned":
                        errors.append(f"{label}: S7 must have status 'planned' (got {short.get('status')!r})")
                    if not short.get("media_root"):
                        errors.append(f"{label}: S7 missing media_root")
                    for row in short["rows"]:
                        if row["source_long_plate"] == "UNBUILT":
                            errors.append(f"{label}: {row['id']} is still UNBUILT despite NAS plates existing")
                else:
                    if short.get("status") != "unbuilt":
                        errors.append(f"{label}: {sid} must stay 'unbuilt'")
                    for row in short["rows"]:
                        if row["source_long_plate"] != "UNBUILT":
                            errors.append(f"{label}: {row['id']} names a plate ({row['source_long_plate']})")
    return errors


def write_all(root: Path) -> None:
    media_root = str(NAS_006_ROOT)
    abc = plan_006_abc(root, media_root)
    lifts = plan_006_lifts(root, media_root)
    combined = {
        "film": "006",
        "media_root": media_root,
        **RULES,
        "shorts": abc["shorts"] + lifts["shorts"],
    }
    dump(root / "02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/BUILD_RULE_v02.json", combined)
    for path, data in plan_films(root):
        dump(path, data)
    dump(root / "docs/STANDALONE_SHORTS_TEST_2026-10/BUILD_RULE_S5_S8_v02.json", plan_standalone(root, media_root))


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
