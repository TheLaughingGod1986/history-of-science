#!/usr/bin/env python3
"""J0967: HOS stayed-to-watch build rules for unbuilt Shorts (c56 + Acting-Chief 6425168160 FIX). Plans only.

Writes and checks the v02 cut plans. It does not render, generate, upload,
or spend. Rules (STAYED60 audit #14–#16, Ben 25 Oct 2026; Chief c56 26 Oct 2026;
Acting-Chief 6425168160 26 Oct 2026):

- the first cut (S01) ends by 2.85 s on the end of the completed hook sentence (effective end <= 2.85 s after merging same-plate runs); any Short whose signed-off VO hook sentence ends > 2.85 s must not silently pass as planned, and is explicitly blocked with `hook_conflict` and a bounded existing-word hook edit proposal (no silent VO word changes)
- body rows sit in 2.50–3.80 s, cutting on word ends (0 <= gap <= 0.10 s)
- each row's `spoken` contains only the words inside that row (no overlap across rows)
- no two adjacent body rows use the same plate (unless in_s/out_s are >= 2.0 s apart with a scene-change score, and 0 <= in_s < out_s <= probed_dur_s with out_s - in_s >= use_s)
- `lookup_plate_duration` resolves and `ffprobe`s actual local/NAS `.mp4` media files only; JSON plate boards are never treated as proof of an existing clip, and any Short/row whose `.mp4` clip is missing on disk/NAS is explicitly marked `blocked_missing_plates` / `blocked_missing_plate` (`plate_on_disk: false`, `probed_dur_s: null`)
- 006 Short_B is timed against the locked 23.20 s `t2_mint_fixed_vo_v03b.mp3` and matching 23.20 s `t2_mint_fixed_vo_v03b_align.json`; 006 Short_A's 20.92 s total duration stays visible as an explicit unresolved build constraint
- the loop tail is 1.0 s or less, on the frame-0 plate
- no "watch the full film" banner, no video id and no code text on any end card
- 006 BUILD_RULE_v02, 007 SHORTS_PICTURE_PLAN_v02, and S7 record `media_root` resolving real `.mp4` plates; S7 is `planned` (plan-only) on NAS `10_mint_jar_t1` + `11_candle_tall_t1`, while S5/S6/S8 stay `unbuilt`

    python3 00_Brand/Channel-Setup/tools/hos_build_rule_v02.py --check
    python3 00_Brand/Channel-Setup/tools/hos_build_rule_v02.py --write
    python3 00_Brand/Channel-Setup/tools/hos_build_rule_v02.py --test-negatives
"""
from __future__ import annotations

import argparse
import copy
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
SHORT_MIN_TOTAL_S = 22.00
YT_ID = re.compile(r"\b[A-Za-z0-9_-]{11}\b")
PAREN_NOTE = re.compile(r"\(([^)]+)\)")

# 009 Short B: drop 0.31 s from the 0.41 s pause at 0.68–1.09 (keep a 0.10 s gap).
PAUSE_TRIM = {("009", "Short_B"): {"cut_s": 0.84, "remove_s": 0.31}}

# Bounded existing-word hook edit proposals for Shorts whose signed-off VO sentence 1 exceeds 2.85 s.
HOOK_CONFLICT_PROPOSALS = {
    ("006_Trees-Are-Made-Of-Air", "s04_photosynthesis"): (
        "Sentence 1 ('A leaf takes in carbon dioxide through tiny pores.') ends at 3.25 s in the lifted long VO "
        "(2.76 s pure speech), so S01 cuts after 'tiny' at 2.57 s. Lawful pause trimming within the 1.06x studio "
        "atempo cap cannot fit all 9 words by 2.85 s; unapproved existing-word/gap-trim option at 1.00x (within "
        "the 1.06x cap): trim 'through tiny pores' (1.87-3.25 s) on the existing take so 'A leaf takes in carbon "
        "dioxide.' completes at 1.84 s <= 2.85 s, or leave the hook explicitly unresolved and blocked (no speed exception)."
    ),
    ("006_Trees-Are-Made-Of-Air", "s05_charcoal_gas"): (
        "Sentence 1 ('Van Helmont also burned sixty-two pounds of charcoal and found just one pound of ash left behind.') "
        "ends at 7.22 s in the lifted long VO (S01 cuts after 'sixty-two' at 2.72 s). Unapproved existing-word option: "
        "drop 'Van Helmont also' and split/tighten on 'burned sixty-two pounds of charcoal' with Chief approval, or "
        "leave the hook explicitly unresolved and blocked."
    ),
    ("006_Trees-Are-Made-Of-Air", "s06_ingenhousz_oxygen"): (
        "Sentence 1 ('Tiny silver bubbles appear on the green leaf and rise to the top.') ends at 4.59 s in the lifted "
        "long VO (S01 cuts after 'green' at 2.54 s). Unapproved existing-word/gap-trim option at 1.00x (within the "
        "1.06x cap): end hook clause after 'leaf' (3.07 s -> 2.78 s via inter-word gap trim) on the existing take, "
        "or leave the hook explicitly unresolved and blocked awaiting Chief sign-off."
    ),
    ("006_Trees-Are-Made-Of-Air", "s07_priestley_mint"): (
        "Lifted long-VO sentence 1 ('If you burn a candle inside a sealed glass jar, the flame soon dies...') runs to "
        "8.20 s (S01 cuts after 'glass' at 2.40 s). Superseded by locked 006 Short_B (t2_mint_fixed_vo_v03b.mp3), whose "
        "hook 'A sprig of mint repaired the air.' completes at 2.24 s <= 2.85 s."
    ),
    ("006_Trees-Are-Made-Of-Air", "s08_willow_pot"): (
        "Lifted long-VO sentence 1 ('He took a big clay pot and filled it with two hundred pounds of soil...') runs to "
        "8.96 s (S01 cuts after 'with' at 2.84 s). Superseded by locked 006 Short_A (t1_willow_air_vo_v02.mp3), whose "
        "hook 'A tree is built from thin air.' completes at 2.16 s <= 2.85 s."
    ),
    ("007_The-First-Vaccine", "Short_B"): (
        "Sentence 1 ('The first vaccine began with milkmaids, who never caught smallpox.') ends at 4.60 s (3.48 s pure "
        "speech); S01 cuts after the main clause 'milkmaids' at 2.72 s while the relative clause 'who never caught "
        "smallpox.' lands in S02 (2.72-4.60 s). Unapproved existing-word option: splice existing words 'milkmaids never "
        "caught smallpox.' (1.88-4.60 s -> 0.06-2.32 s) as sentence 1, or leave the hook explicitly unresolved and "
        "blocked awaiting Chief sign-off."
    ),
    ("008_Lightning-Franklin", "Short_C"): (
        "Sentence 1 ('That thin metal rod on top of tall buildings was Benjamin Franklin\\'s idea.') ends at 4.84 s "
        "(3.72 s pure speech); S01 cuts mid-phrase after 'tall' at 2.40 s while 'buildings was Benjamin Franklin\\'s "
        "idea.' runs in S02 through 4.90 s. Unapproved existing-word option: excise prepositional phrase 'on top of tall "
        "buildings' (1.48-3.06 s) on the existing take so 'That thin metal rod was Benjamin Franklin\\'s idea.' "
        "completes at 2.84 s <= 2.85 s, or leave the hook explicitly unresolved and blocked awaiting Chief sign-off."
    ),
    ("009_The-Falling-Moon-Gravity", "Short_B"): (
        "Sentence 1 ('In one minute, the moon falls about as far as an apple falls in one second.') ends at 4.27 s "
        "(3.18 s pure speech even after the 0.31 s pause trim); S01 cuts after 'apple' at 2.75 s while 'falls in one "
        "second.' lands in S02. Both time intervals ('In one minute' and 'in one second') must be preserved for the "
        "lunar-vs-apple comparison, and the 16-word hook cannot fit <= 2.85 s using existing words and lawful pause "
        "trims (or within the 1.06x studio atempo cap); keep this Short explicitly blocked and unresolved (no new VO, "
        "scientific claim, approved wording change, or speed exception is authorised)."
    ),
    ("010_Alvarez-Clay-Line-Dinosaurs", "Short_A"): (
        "Sentence 1 ('This thin line of clay marks the end of the dinosaurs.') ends at 3.28 s (2.62 s pure speech); "
        "S01 cuts after 'the' at 2.40 s while 'dinosaurs.' lands at the start of S02 (2.40-3.28 s). Unapproved "
        "existing-word/gap-trim option at 1.00x (within the 1.06x cap): tighten sentence-1 onset and inter-word gaps "
        "by 0.48 s (or excise 'of clay' [1.06-1.42 s]) on the existing take so 'dinosaurs.' finishes at 2.80 s <= 2.85 s, "
        "or leave the hook explicitly unresolved and blocked awaiting Chief sign-off."
    ),
    ("docs", "s5_penzias_pigeons"): (
        "Sentence 1 ('the afterglow of the Big Bang was blamed on pigeons.') ends at 3.76 s after dateline drop; "
        "S01 cuts after 'blamed' at 2.58 s. Short stays unbuilt (no moving horn plate)."
    ),
    ("docs", "s8_hales_blood"): (
        "Sentence 1 ('A horse\\'s blood climbed eight feet up a glass tube.') ends at 3.71 s; S01 cuts after 'a' at "
        "2.81 s. Short stays unbuilt (no moving Hales plate)."
    ),
}

RULES = {
    "job": "J0967",
    "s01_ends_by_s": S01_MAX,
    "s01_requires_completed_hook": True,
    "body_cut_s": [LO, HI],
    "word_end_gap_s_max": MAX_WORD_GAP,
    "adjacent_same_plate": False,
    "plate_must_exist_on_disk": True,
    "loop_tail_s_max": TAIL,
    "full_film_banner": False,
    "end_card_video_id": None,
    "end_card_code_text": None,
    "render": False,
    "generation": False,
    "gbp": 0,
}

# Non-repeating body plate sequences per Short.
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

# S7 uses the 2 existing 8.00 s moving plates on NAS with non-overlapping in_s/out_s windows matching each row's use_s.
PLATES_S7 = [
    ("04_Generated-Clips/part03/raw/v01/10_mint_jar_t1.mp4", 0.0, 2.80),
    ("04_Generated-Clips/part03/raw/v01/11_candle_tall_t1.mp4", 0.0, 2.92),
    ("04_Generated-Clips/part03/raw/v01/10_mint_jar_t1.mp4", 2.80, 5.92),
    ("04_Generated-Clips/part03/raw/v01/11_candle_tall_t1.mp4", 2.92, 6.68),
    ("04_Generated-Clips/part03/raw/v01/10_mint_jar_t1.mp4", 4.88, 8.00),
    ("04_Generated-Clips/part03/raw/v01/11_candle_tall_t1.mp4", 4.64, 8.00),
]

_PROBE_CACHE: dict[str, float] = {}
_BOARD_CACHE: dict[str, dict[str, float]] = {}

FOLDER_MAP = {
    "006": "006_Trees-Are-Made-Of-Air",
    "007": "007_The-First-Vaccine",
    "008": "008_Lightning-Franklin",
    "009": "009_The-Falling-Moon-Gravity",
    "010": "010_Alvarez-Clay-Line-Dinosaurs",
}


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
    if not path.exists() or not path.is_file():
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


def resolve_plate_path(root: Path, folder_or_film: str, plate: str, media_root: str | None) -> Path | None:
    """Resolve `plate` to an actual `.mp4` file on local disk or NAS. Never consults JSON boards."""
    if not plate or plate == "UNBUILT":
        return None
    clean = PAREN_NOTE.sub("", plate).strip()
    folder = FOLDER_MAP.get(folder_or_film, folder_or_film)

    candidate_roots: list[Path] = []
    if media_root:
        candidate_roots.append(Path(media_root))
    if folder in ("006_Trees-Are-Made-Of-Air", "BUILD_RULE_S5_S8_v02.json", "docs"):
        candidate_roots.append(resolve_repo_file(root, "02_Video-Projects/006_Trees-Are-Made-Of-Air"))
    elif folder.startswith(("007_", "008_", "009_", "010_")):
        candidate_roots.append(resolve_repo_file(root, f"02_Video-Projects/{folder}"))
        if folder.startswith("007_") and LOCAL_007_ROOT not in candidate_roots:
            candidate_roots.append(LOCAL_007_ROOT)

    # Case 1: P{n}:{stem} identifier
    m_pid = re.match(r"^P(\d+):([A-Za-z0-9_.-]+)$", clean)
    if m_pid:
        pnum = int(m_pid.group(1))
        stem = m_pid.group(2)
        for croot in candidate_roots:
            part_dir = croot / f"04_Generated-Clips/part0{pnum}/raw/v01"
            if not part_dir.exists():
                continue
            direct = part_dir / f"{stem}.mp4"
            if direct.exists() and direct.is_file():
                return direct
            matches = sorted(
                p for p in part_dir.glob(f"{stem}_t*.mp4") if not p.name.startswith("._") and p.is_file()
            )
            if matches:
                return matches[0]
        return None

    # Case 2: relative path under 04_Generated-Clips
    if clean.startswith("04_Generated-Clips/"):
        rel = clean
    else:
        rel = f"04_Generated-Clips/{clean}"
    if not rel.endswith(".mp4"):
        rel += ".mp4"
    for croot in candidate_roots:
        fp = croot / rel
        if fp.exists() and fp.is_file():
            return fp
    return None


def board_spec_duration(root: Path, folder_or_film: str, plate: str) -> float | None:
    """Return planned clip length from 07_Edit-Project/parts JSON board (metadata only, NOT proof of file existence)."""
    folder = FOLDER_MAP.get(folder_or_film, folder_or_film)
    if folder not in _BOARD_CACHE:
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
        _BOARD_CACHE[folder] = plate_map
    m = re.search(r"\((\d+(?:\.\d+)?)\s*s", plate)
    noted_cap = round(float(m.group(1)), 3) if m else None
    clean = PAREN_NOTE.sub("", plate).strip()
    bmap = _BOARD_CACHE[folder]
    if clean in bmap:
        d = bmap[clean]
        return min(d, noted_cap) if noted_cap is not None else d
    return noted_cap


def lookup_plate_duration(
    root: Path, folder_or_film: str, plate: str, media_root: str | None
) -> tuple[bool, float | None]:
    """Resolve `plate` to an on-disk/NAS `.mp4` file and probe its duration via ffprobe.

    Never treats JSON board metadata as an existing clip: if no `.mp4` exists on disk/NAS,
    returns `(False, noted_cap)`.
    """
    if plate == "UNBUILT":
        return False, None
    m = re.search(r"\((\d+(?:\.\d+)?)\s*s", plate)
    noted_cap = round(float(m.group(1)), 3) if m else None
    if folder_or_film in ("006", "006_Trees-Are-Made-Of-Air", "BUILD_RULE_S5_S8_v02.json", "docs") and not media_root:
        return False, noted_cap
    fp = resolve_plate_path(root, folder_or_film, plate, media_root)
    if fp is None:
        return False, noted_cap
    d = probe_duration(fp)
    if d is None:
        return False, noted_cap
    return True, (min(d, noted_cap) if noted_cap is not None else d)


def words_from_align(path: Path) -> list[tuple[str, float, float]]:
    data = json.loads(path.read_text())
    if "words" in data and isinstance(data["words"], list) and data["words"] and "word" in data["words"][0]:
        return [
            (str(w["word"]), round(float(w["start"]), 3), round(float(w["end"]), 3))
            for w in data["words"]
        ]
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


def hook_sentence_info(words: list[tuple[str, float, float]]) -> tuple[int, str, float]:
    """Return `(word_idx, full_hook_sentence, end_s)` for the opening sentence of `words`."""
    idx = next((i for i, (wt, _wa, _wb) in enumerate(words) if wt[-1:] in ".?!"), len(words) - 1)
    text = " ".join(w[0] for w in words[: idx + 1])
    end_s = round(words[idx][2], 3)
    return idx, text, end_s


def find_word_cuts(
    words: list[tuple[str, float, float]],
    vo_end: float,
    s01_min: float = LO,
    s01_max: float = S01_MAX,
    lo: float = LO,
    hi: float = HI,
) -> list[dict] | None:
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
        on_disk, probed_dur = lookup_plate_duration(root, folder_or_film, plate, media_root)
        board_dur = board_spec_duration(root, folder_or_film, plate)
        pdur = probed_dur if on_disk else board_dur
        row: dict = {
            "id": cut["id"],
            "t_start_s": cut["t_start_s"],
            "t_end_s": cut["t_end_s"],
            "use_s": cut["use_s"],
            "word_end_s": cut["word_end_s"],
            "word_gap_s": cut["word_gap_s"],
            "source_long_plate": plate,
            "plate_on_disk": on_disk,
            "probed_dur_s": probed_dur if on_disk else None,
            "plate_dur_s": pdur,
            "status": "planned" if on_disk else "blocked_missing_plate",
            "route": route,
            "spoken": cut["spoken"],
            "flow_credits_expected": 0,
        }
        if not on_disk and board_dur is not None:
            row["board_dur_s"] = board_dur
        if in_s is not None and out_s is not None:
            row["in_s"] = round(in_s, 3)
            row["out_s"] = round(out_s, 3)
        rows.append(row)
    first_plate = plates[0][0] if isinstance(plates[0], tuple) else plates[0]
    lp = loop_plate or first_plate
    lp_on_disk, lp_probed_dur = lookup_plate_duration(root, folder_or_film, lp, media_root)
    lp_board_dur = board_spec_duration(root, folder_or_film, lp)
    ldur = lp_probed_dur if lp_on_disk else lp_board_dur
    if loop_dur_override is not None:
        ldur = loop_dur_override
    tail_start = round(vo_end, 3)
    tail_row: dict = {
        "id": "loop_tail",
        "t_start_s": tail_start,
        "t_end_s": round(tail_start + TAIL, 3),
        "use_s": TAIL,
        "role": "loop_tail",
        "route": route,
        "source_long_plate": lp,
        "plate_on_disk": lp_on_disk,
        "probed_dur_s": lp_probed_dur if lp_on_disk else None,
        "plate_dur_s": ldur,
        "status": "planned" if lp_on_disk else "blocked_missing_plate",
        "spoken": "",
        "note": loop_note or "Matched frame-0 plate after the last word. No banner, no video id, no code text.",
    }
    if not lp_on_disk and lp_board_dur is not None:
        tail_row["board_dur_s"] = lp_board_dur
    rows.append(tail_row)
    return rows


def attach_hook_and_status_metadata(
    parent_name: str,
    short: dict,
    words: list[tuple[str, float, float]],
) -> None:
    sid = short["id"]
    body = [r for r in short["rows"] if r.get("role") != "loop_tail"]
    _h_idx, full_hook_text, hook_end_s = hook_sentence_info(words)
    s01 = body[0]
    s01_spoken = (s01.get("spoken") or "").strip()
    hook_complete = bool(
        s01_spoken.endswith((".", "!", "?"))
        and s01["t_end_s"] <= S01_MAX + 0.011
        and abs(s01["word_end_s"] - hook_end_s) <= 0.02
    )
    short["hook_complete_in_s01"] = hook_complete
    short["hook_sentence_end_s"] = hook_end_s
    all_plates_on_disk = all(
        r.get("plate_on_disk") is True for r in short["rows"] if r.get("source_long_plate") != "UNBUILT"
    ) and any(r.get("source_long_plate") != "UNBUILT" for r in short["rows"])
    short["plates_on_disk"] = all_plates_on_disk

    if not hook_complete:
        proposal = HOOK_CONFLICT_PROPOSALS.get(
            (parent_name, sid),
            f"Hook sentence ends at {hook_end_s:.2f} s (> {S01_MAX} s); requires bounded existing-word hook edit before assembly.",
        )
        short["hook_conflict"] = {
            "s01_end_s": s01["t_end_s"],
            "s01_partial_spoken": s01_spoken,
            "hook_sentence_end_s": hook_end_s,
            "full_hook_sentence": full_hook_text,
            "vo_words_changed": False,
            "bounded_edit_proposal": proposal,
        }
    else:
        short.pop("hook_conflict", None)

    # Determine explicit status
    if short.get("status") == "unbuilt":
        return
    if not hook_complete and not all_plates_on_disk:
        short["status"] = "blocked_hook_and_missing_plates"
        short["blocked_reason"] = (
            f"S01 cuts at {s01['t_end_s']:.2f} s before hook sentence ends at {hook_end_s:.2f} s, "
            "and target long plates exist only in board JSON (no .mp4 files on disk/NAS)."
        )
    elif not all_plates_on_disk:
        short["status"] = "blocked_missing_plates"
        short["blocked_reason"] = (
            "Target long plates exist only in 07_Edit-Project/parts board JSON; no .mp4 files exist on local disk or NAS yet."
        )
    elif not hook_complete:
        short["status"] = "blocked_unfinished_hook"
        short["blocked_reason"] = (
            f"S01 cuts at {s01['t_end_s']:.2f} s ({s01_spoken!r}) before the opening hook sentence finishes at {hook_end_s:.2f} s."
        )
    else:
        short["status"] = "planned"
        short.pop("blocked_reason", None)


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


def tighten_s7_hook_pauses(words: list[tuple[str, float, float]]) -> tuple[list[tuple[str, float, float]], float]:
    """Tighten the 0.16 s pause after 'a' and 0.24 s pause after 'mint' in S7 sentence 1 by 0.24 s total (0 words changed)."""
    out: list[tuple[str, float, float]] = []
    for wt, a, b in words:
        shift = 0.0
        if a >= 0.20:
            shift += 0.10
        if a >= 1.20:
            shift += 0.14
        out.append((wt, round(a - shift, 3), round(b - shift, 3)))
    return out, 0.24


def plan_006_abc(root: Path, media_root: str) -> dict:
    vo = resolve_repo_file(root, "02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/vo_20261004")
    specs = [
        {
            "id": "Short_A",
            "align": vo / "t1_willow_air_vo_v02_align.json",
            "align_rel": "10_Shorts/vo_20261004/t1_willow_air_vo_v02_align.json",
            "vo": "10_Shorts/vo_20261004/t1_willow_air_vo_v02.mp3",
            "drop_title_from": "The",
            "title_note": "Trim the spoken title from the word The (The Willow Tree That Was Made of Air) off the existing take. No new VO.",
        },
        {
            "id": "Short_B",
            "align": vo / "t2_mint_fixed_vo_v03b_align.json",
            "align_rel": "10_Shorts/vo_20261004/t2_mint_fixed_vo_v03b_align.json",
            "vo": "10_Shorts/vo_20261004/t2_mint_fixed_vo_v03b.mp3",
            "vo_duration_override_s": 23.2,
        },
        {
            "id": "Short_C",
            "align": vo / "t3_bubbles_sunlight_vo_v01_align.json",
            "align_rel": "10_Shorts/vo_20261004/t3_bubbles_sunlight_vo_v01_align.json",
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
        elif spec.get("vo_duration_override_s") is not None:
            t_end = round(float(spec["vo_duration_override_s"]), 3)
        else:
            t_end = round(words[-1][2], 3)
        plates = PLATES_006[sid]
        rows = build_rows(root, "006", words, t_end, plates, "reuse-long-plate", media_root)
        total_dur = round(t_end + TAIL, 3)
        item: dict = {
            "id": sid,
            "vo": spec["vo"],
            "align": spec["align_rel"],
            "vo_duration_s": t_end,
            "total_duration_s": total_dur,
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
        attach_hook_and_status_metadata("006_Trees-Are-Made-Of-Air", item, words)
        if note:
            item["vo_trim"] = {"drop_spoken_title_from_s": t_end, "note": note}
            item["duration_note"] = (
                f"Speech ends at {t_end:.2f} s. With the 1.0 s loop the Short is {total_dur:.2f} s, "
                "under the 22 s band. The audit asked for this title trim. No words were added."
            )
            item["unresolved_build_constraint"] = (
                f"Declared total duration is {total_dur:.2f} s ({t_end:.2f} s VO after spoken-title trim + "
                f"{TAIL:.2f} s loop), below the {SHORT_MIN_TOTAL_S:.2f} s HOS Shorts floor; no blanket length "
                "exception or production approval is granted."
            )
            item["status"] = "blocked_duration_under_22s"
        if sid == "Short_B":
            item["duration_note"] = (
                "Timed directly from t2_mint_fixed_vo_v03b_align.json (23.20 s, sha256 0f109926...) matching "
                "the locked take t2_mint_fixed_vo_v03b.mp3 (23.20 s VO + 1.00 s loop = 24.20 s total). No new VO."
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
        item: dict = {
            "id": sid,
            "replaces": path.name,
            "vo_duration_s": vo_end,
            "total_duration_s": round(vo_end + TAIL, 3),
            "first_cut_s": rows[0]["t_end_s"],
            "frame0_plate": plates[0],
            "rows": rows,
            "loop_tail_s": TAIL,
            "end_card": end_card(),
            "full_film_banner": False,
            "render": False,
            "retired_assembler": f"_build_short_{sid}_v01.py",
        }
        attach_hook_and_status_metadata("006_Trees-Are-Made-Of-Air", item, words)
        shorts.append(item)
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
        data["task"] = (
            "J0967: stayed-to-watch build rules (c56 + Acting-Chief 6425168160 FIX). "
            "Plans only, no render, no generation."
        )
        data["rules"] = RULES
        film_media_root: str | None = str(LOCAL_007_ROOT) if film == "007" else None
        data["media_root"] = film_media_root
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
                film_media_root,
                loop_note=loop_note,
                loop_dur_override=loop_dur,
            )
            short["rows"] = rows
            short["total_duration_s"] = round(vo_end + TAIL, 3)
            short["first_cut_s"] = rows[0]["t_end_s"]
            short["loop_tail_s"] = TAIL
            short["end_card"] = end_card()
            short["full_film_banner"] = False
            short["render"] = False
            short["frame0_plate"] = plates[0]
            attach_hook_and_status_metadata(folder, short, words)
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
            trim: dict = {"drop": dateline, "remove_s": remove, "claim_starts_s": 0.06}
        else:
            lead = 0.05 - words[0][1]
            words = [(t, round(a + lead, 3), round(b + lead, 3)) for t, a, b in words]
            trim = {"onset_to_s": 0.05, "shift_s": round(lead, 3)}
        if sid == "s7_priestley_mint":
            words, s1_pause_rem = tighten_s7_hook_pauses(words)
            trim["s1_pause_trim_s"] = s1_pause_rem
            trim["s1_pause_note"] = (
                "Tighten sentence-1 pauses after 'a' (-0.10 s) and 'mint' (-0.14 s) on existing take so "
                "'a sprig of mint brought dead air back to life.' completes at 2.80 s <= 2.85 s. Zero words changed."
            )
        t_end = round(words[-1][2], 3)
        total_dur = round(t_end + TAIL, 3)
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
                "total_duration_s": total_dur,
                "unresolved_build_constraint": (
                    f"Standalone ~20 s test Short: {total_dur:.2f} s total ({t_end:.2f} s VO after dateline + "
                    "sentence-1 pause trim + 1.00 s loop); keep plan-only."
                ),
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
            attach_hook_and_status_metadata("docs", item, words)
        else:
            cuts = find_word_cuts(words, t_end)
            assert cuts is not None
            rows = [
                {
                    **c,
                    "source_long_plate": "UNBUILT",
                    "plate_on_disk": False,
                    "probed_dur_s": None,
                    "plate_dur_s": None,
                    "status": "unbuilt",
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
                    "plate_on_disk": False,
                    "probed_dur_s": None,
                    "plate_dur_s": None,
                    "status": "unbuilt",
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
                "total_duration_s": total_dur,
                "first_cut_s": rows[0]["t_end_s"],
                "rows": rows,
                "loop_tail_s": TAIL,
                "end_card": end_card(),
                "full_film_banner": False,
                "render": False,
                "generation": False,
                "frame0": "moving plate or unbuilt",
            }
            attach_hook_and_status_metadata("docs", item, words)
            item["status"] = "unbuilt"
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
            align_p = vo_dir / "t2_mint_fixed_vo_v03b_align.json"
            if not align_p.exists():
                align_p = vo_dir / "t2_mint_fixed_vo_v03_align.json"
            return words_from_align(align_p)
        if sid == "Short_C":
            return words_from_align(vo_dir / "t3_bubbles_sunlight_vo_v01_align.json")
        src_p = next(
            (
                resolve_repo_file(
                    root, "02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/SHORT_s04_photosynthesis_v01.json"
                ).parent
            ).glob(f"SHORT_{sid}_*.json")
        )
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
    if sid == "s7_priestley_mint" and (short.get("vo_trim") or {}).get("s1_pause_trim_s"):
        w, _ = tighten_s7_hook_pauses(w)
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

    # Verify VO timing source and duration alignment (e.g., 006 Short_B v03b 23.20 s vs 21.60 s mismatch)
    vo_rel = short.get("vo")
    if vo_rel and parent_name == "006_Trees-Are-Made-Of-Air":
        vo_fp = resolve_repo_file(root, f"02_Video-Projects/006_Trees-Are-Made-Of-Air/{vo_rel}")
        if not vo_fp.exists() and media_root:
            vo_fp = Path(media_root) / vo_rel
        probed_vo = probe_duration(vo_fp) if vo_fp.exists() else None
        expected_vo = float(short["vo_duration_s"])
        trim_s = (short.get("vo_trim") or {}).get("drop_spoken_title_from_s")
        if probed_vo is not None and trim_s is None and abs(probed_vo - expected_vo) > 0.08:
            errors.append(
                f"{label}: vo_duration_s ({expected_vo:.2f} s) does not match probed {vo_rel} ({probed_vo:.2f} s)"
            )
        align_rel = short.get("align")
        expected_align_stem = Path(vo_rel).stem + "_align.json"
        if not align_rel or Path(align_rel).name != expected_align_stem:
            errors.append(
                f"{label}: timing alignment {align_rel!r} does not match locked VO stem {expected_align_stem!r}"
            )
    dnote = short.get("duration_note") or ""
    if "Re-time these cuts" in dnote or "21.60 s" in dnote:
        errors.append(f"{label}: duration_note still references un-retimed 21.60 s take ({dnote!r})")

    # Check under-22s total duration build constraint visibility (e.g., 006 Short_A at 20.92 s)
    total_dur = round(float(short["vo_duration_s"]) + float(short.get("loop_tail_s") or TAIL), 3)
    if total_dur < SHORT_MIN_TOTAL_S - 0.01 and short.get("status") != "unbuilt":
        if not short.get("unresolved_build_constraint"):
            errors.append(
                f"{label}: total duration {total_dur:.2f} s < {SHORT_MIN_TOTAL_S:.2f} s without explicit unresolved_build_constraint"
            )
        if parent_name == "006_Trees-Are-Made-Of-Air" and short.get("status") != "blocked_duration_under_22s":
            errors.append(
                f"{label}: 006 Short under 22 s ({total_dur:.2f} s) must have status 'blocked_duration_under_22s'"
            )

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

    # Load words to verify cuts on word ends, non-overlapping spoken text, and S01 hook completion
    words = load_words_for_short(root, parent_name, short, media_root)
    if abs(words[-1][2] - float(short["vo_duration_s"])) > 0.20:
        errors.append(
            f"{label}: last word end ({words[-1][2]:.2f} s) diverges from vo_duration_s ({short['vo_duration_s']:.2f} s)"
        )

    # Enforce S01 hook completion by 2.85 s (or explicit hook_conflict block if VO hook sentence > 2.85 s)
    _h_idx, full_hook_text, hook_end_s = hook_sentence_info(words)
    s01_spoken = (body[0].get("spoken") or "").strip()
    s01_completes_hook = bool(
        s01_spoken.endswith((".", "!", "?"))
        and body[0]["t_end_s"] <= S01_MAX + 0.011
        and abs(body[0].get("word_end_s", -99.0) - hook_end_s) <= 0.02
    )
    if hook_end_s <= S01_MAX + 0.011:
        if not s01_completes_hook:
            errors.append(
                f"{label}: hook sentence ({full_hook_text!r}) ends at {hook_end_s:.2f} s <= {S01_MAX} s, "
                f"but S01 ends at {body[0]['t_end_s']:.2f} s on {s01_spoken!r}"
            )
        if short.get("hook_complete_in_s01") is not True:
            errors.append(f"{label}: hook_complete_in_s01 must be True when hook completes at {hook_end_s:.2f} s")
    else:
        hc = short.get("hook_conflict")
        st = str(short.get("status") or "")
        if (
            short.get("hook_complete_in_s01") is not False
            or not isinstance(hc, dict)
            or not hc.get("bounded_edit_proposal")
            or hc.get("vo_words_changed") is not False
            or not (st == "unbuilt" or st.startswith("blocked_"))
        ):
            errors.append(
                f"{label}: S01 ends at {body[0]['t_end_s']:.2f} s on unfinished hook ({s01_spoken!r}); "
                f"full hook sentence ({full_hook_text!r}) ends at {hook_end_s:.2f} s (> {S01_MAX} s) and Short "
                "is not explicitly blocked with hook_conflict"
            )
        else:
            prop = str(hc.get("bounded_edit_proposal") or "")
            for m_spd in re.finditer(r"\b(\d+\.\d+)x\b", prop):
                val = float(m_spd.group(1))
                if val > 1.06 + 1e-6:
                    errors.append(
                        f"{label}: bounded_edit_proposal proposes {val:.2f}x speed above the 1.06x studio atempo cap"
                    )
            if parent_name == "009_The-Falling-Moon-Gravity" and short.get("id") == "Short_B":
                prop_l = prop.lower()
                if (
                    "drop leading 'in one minute" in prop_l
                    or 'drop leading "in one minute' in prop_l
                    or "in one minute" not in prop_l
                    or "in one second" not in prop_l
                ):
                    errors.append(
                        f"{label}: bounded_edit_proposal must preserve both time intervals ('In one minute' and 'in one second') and must not propose dropping 'In one minute'"
                    )

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

    # Real media existence, ffprobe duration, in_s/out_s window, notes-in-plate, and plate_dur_s >= use_s checks
    for row in rows:
        plate = row.get("source_long_plate") or ""
        if "(" in plate or ")" in plate or "+" in plate:
            errors.append(f"{label}: {row['id']} has notes or bundle inside source_long_plate ({plate!r})")
        if plate == "UNBUILT":
            continue
        use_s = round(float(row.get("use_s") or dur(row)), 3)
        pdur = row.get("plate_dur_s")
        exists, probed_dur = lookup_plate_duration(root, parent_name, plate, media_root)
        board_dur = board_spec_duration(root, parent_name, plate)

        if pdur is None:
            errors.append(f"{label}: {row['id']} missing plate_dur_s")
        elif float(pdur) < use_s - 0.01:
            errors.append(f"{label}: {row['id']} plate_dur_s {pdur} < use_s {use_s}")

        if board_dur is not None and board_dur < use_s - 0.01:
            errors.append(f"{label}: {row['id']} resolved plate duration {board_dur} s < use_s {use_s} s ({plate})")

        if exists and probed_dur is not None:
            if probed_dur < use_s - 0.01:
                errors.append(f"{label}: {row['id']} probed plate duration {probed_dur} s < use_s {use_s} s ({plate})")
            if row.get("plate_on_disk") is not True:
                errors.append(f"{label}: {row['id']} plate {plate!r} exists on disk but plate_on_disk is not True")
            if row.get("in_s") is not None or row.get("out_s") is not None:
                if row.get("in_s") is None or row.get("out_s") is None:
                    errors.append(f"{label}: {row['id']} has partial in_s/out_s window")
                else:
                    in_s = float(row["in_s"])
                    out_s = float(row["out_s"])
                    win_s = round(out_s - in_s, 3)
                    if in_s < -1e-6 or out_s <= in_s or out_s > probed_dur + 0.01:
                        errors.append(
                            f"{label}: {row['id']} in_s/out_s [{in_s:.2f}, {out_s:.2f}] outside probed plate [0.00, {probed_dur:.2f}]"
                        )
                    if win_s < use_s - 0.01:
                        errors.append(
                            f"{label}: {row['id']} in_s/out_s window {win_s:.2f} s < use_s {use_s:.2f} s"
                        )
        else:
            # Media file does not exist on local disk or NAS (e.g., board-only 008-010 plate)
            st = str(short.get("status") or "")
            if (
                row.get("plate_on_disk") is not False
                or row.get("probed_dur_s") is not None
                or row.get("status") != "blocked_missing_plate"
                or short.get("plates_on_disk") is not False
                or not (st == "unbuilt" or "missing_plates" in st)
            ):
                errors.append(
                    f"{label}: {row['id']} plate {plate!r} has no .mp4 media file on disk/NAS (board JSON is not proof of an existing plate) and is not explicitly marked blocked_missing_plate"
                )

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


def run_negative_checks(root: Path) -> list[str]:
    """Verify negative cases required by Acting-Chief 6425168160 all deterministically FAIL."""
    failures: list[str] = []

    # 1. Board-only clip lookup must return (False, None), never (True, 8.0)
    ok_008, dur_008 = lookup_plate_duration(root, "008", "P1:01_kite_open", None)
    if ok_008 or dur_008 is not None:
        failures.append(f"negative check 1 failed: lookup_plate_duration(008, P1:01_kite_open) returned {(ok_008, dur_008)}")

    # 2. Wrong/mismatched VO timing on 006 Short_B (21.60 s / v03_align vs 23.20 s v03b.mp3) must FAIL check_short
    p006 = load(root / "02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/BUILD_RULE_v02.json")
    sb = copy.deepcopy(next(s for s in p006["shorts"] if s["id"] == "Short_B"))
    sb["vo_duration_s"] = 21.6
    sb["align"] = "10_Shorts/vo_20261004/t2_mint_fixed_vo_v03_align.json"
    errs_vo: list[str] = []
    check_short(root, "006_Trees-Are-Made-Of-Air", "neg/006_Short_B_21p6s", sb, p006.get("media_root"), errs_vo)
    if not any("does not match probed" in e or "does not match locked VO stem" in e for e in errs_vo):
        failures.append(f"negative check 2 failed: 006 Short_B 21.60s mismatch did not trigger VO timing error ({errs_vo})")

    # 3. Board-only/missing clip claimed as available/planned on 008 Short_A must FAIL check_short
    p008 = load(root / "02_Video-Projects/008_Lightning-Franklin/10_Shorts/SHORTS_PICTURE_PLAN_v02.json")
    sa = copy.deepcopy(next(s for s in p008["shorts"] if s["id"] == "Short_A"))
    sa["status"] = "planned"
    sa["plates_on_disk"] = True
    sa["rows"][0]["status"] = "planned"
    sa["rows"][0]["plate_on_disk"] = True
    errs_clip: list[str] = []
    check_short(root, "008_Lightning-Franklin", "neg/008_Short_A_board_only", sa, p008.get("media_root"), errs_clip)
    if not any("has no .mp4 media file on disk/NAS" in e for e in errs_clip):
        failures.append(f"negative check 3 failed: board-only clip on 008 Short_A did not fail ({errs_clip})")

    # 4. Unfinished S01 hook on 008 Short_C (cuts after 'tall' at 2.40 s, hook ends at 4.84 s) treated as complete must FAIL
    sc = copy.deepcopy(next(s for s in p008["shorts"] if s["id"] == "Short_C"))
    sc["status"] = "planned"
    sc["hook_complete_in_s01"] = True
    sc.pop("hook_conflict", None)
    errs_hook: list[str] = []
    check_short(root, "008_Lightning-Franklin", "neg/008_Short_C_unfinished_hook", sc, p008.get("media_root"), errs_hook)
    if not any("unfinished hook" in e for e in errs_hook):
        failures.append(f"negative check 4 failed: unfinished S01 hook on 008 Short_C did not fail ({errs_hook})")

    # 5. Out-of-bounds in_s/out_s window on S7 must FAIL
    ps7 = load(root / "docs/STANDALONE_SHORTS_TEST_2026-10/BUILD_RULE_S5_S8_v02.json")
    s7 = copy.deepcopy(next(s for s in ps7["shorts"] if s["id"] == "s7_priestley_mint"))
    s7["rows"][0]["in_s"] = 6.5
    s7["rows"][0]["out_s"] = 9.3
    errs_inout: list[str] = []
    check_short(root, "docs", "neg/S7_bad_inout", s7, s7.get("media_root"), errs_inout)
    if not any("outside probed plate" in e for e in errs_inout):
        failures.append(f"negative check 5 failed: out-of-bounds in_s/out_s on S7 did not fail ({errs_inout})")

    # 6. Over-cap 1.12x speed proposal on 006 s04_photosynthesis must FAIL (Acting-Chief 6426967421)
    s04_neg = copy.deepcopy(next(s for s in p006["shorts"] if s["id"] == "s04_photosynthesis"))
    s04_neg["hook_conflict"]["bounded_edit_proposal"] = (
        "Bounded existing-word option: tighten sentence-1 inter-word gaps + 1.12x pace on 0.00-3.25 s."
    )
    errs_spd: list[str] = []
    check_short(root, "006_Trees-Are-Made-Of-Air", "neg/006_s04_1p12x", s04_neg, p006.get("media_root"), errs_spd)
    if not any("above the 1.06x studio atempo cap" in e for e in errs_spd):
        failures.append(f"negative check 6 failed: 1.12x speed proposal on 006 s04 did not fail ({errs_spd})")

    # 7. Dropping 'In one minute' from 009 Short_B comparison hook proposal must FAIL (Acting-Chief 6426967421)
    p009 = load(root / "02_Video-Projects/009_The-Falling-Moon-Gravity/10_Shorts/SHORTS_PICTURE_PLAN_v02.json")
    s09b_neg = copy.deepcopy(next(s for s in p009["shorts"] if s["id"] == "Short_B"))
    s09b_neg["hook_conflict"]["bounded_edit_proposal"] = (
        "Bounded existing-word option: drop leading 'In one minute,' (0.08-0.74 s) and tighten inter-word gaps."
    )
    errs_09b: list[str] = []
    check_short(root, "009_The-Falling-Moon-Gravity", "neg/009_Short_B_drop_minute", s09b_neg, p009.get("media_root"), errs_09b)
    if not any("preserve both time intervals" in e for e in errs_09b):
        failures.append(f"negative check 7 failed: dropping 'In one minute' on 009 Short_B did not fail ({errs_09b})")

    return failures


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
    ap.add_argument("--test-negatives", action="store_true")
    ns = ap.parse_args()
    if ns.write:
        write_all(REPO)
    if ns.check or ns.test_negatives or not ns.write:
        errors = check_all(REPO)
        if errors:
            print(f"FAIL {len(errors)}")
            for line in errors:
                print(" ", line)
            raise SystemExit(1)
        neg_failures = run_negative_checks(REPO)
        if neg_failures:
            print(f"FAIL negative checks ({len(neg_failures)})")
            for line in neg_failures:
                print(" ", line)
            raise SystemExit(1)
        print("PASS build-rule v02 plans (including 7 negative checks)")


if __name__ == "__main__":
    main()
