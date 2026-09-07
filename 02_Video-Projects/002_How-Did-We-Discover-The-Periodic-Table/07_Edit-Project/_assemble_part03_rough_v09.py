#!/usr/bin/env python3
"""Assemble HOS 002 Part 03 rough v09 — scrub city-plan house-blocks.

Parent: hos_002_part03_rough_v08.mp4 sha 487dc2b8…
  - REMINT ONLY 10_city_plan_lots (flat ink postcard OR papers only — no house icons)
  - KEEP 08_property_waves v08 (~61s aisle)
  - KEEP EMPTY CHAIR sync + chair art (v04)
  - KEEP 03_method_pamphlet v07 swirl + desk H/C/O
  - KEEP 05 Explorer trenchcoat (v05), Karlsruhe blank (02), VO, PLATE_ORDER
  - No P01/P02 remint. No P04. Scores → CoS only. Do not declare PASS.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PROJ = Path(__file__).resolve().parents[1]
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-03_plates_v01.json"
RAW_V02 = PROJ / "04_Generated-Clips/part03/raw/v02_fast"
RAW_V04 = PROJ / "04_Generated-Clips/part03/raw/v04_fast"
RAW_V05 = PROJ / "04_Generated-Clips/part03/raw/v05_fast"
RAW_V07 = PROJ / "04_Generated-Clips/part03/raw/v07_fast"
RAW_V08 = PROJ / "04_Generated-Clips/part03/raw/v08_fast"
RAW_V09 = PROJ / "04_Generated-Clips/part03/raw/v09_fast"
LABEL_DIR = PROJ / "04_Generated-Clips/part03/refs/v09_side_labels"
VO = PROJ / "02_Voiceover/part03_ruler_for_atoms_v01.wav"
BED = PROJ / "05_Music/hos_002_part01_curious_workshop_v02_norm.wav"
OUT = PROJ / "09_Final-Export/hos_002_part03_rough_v09.mp4"
KEEP_V08 = PROJ / "09_Final-Export/hos_002_part03_rough_v08.mp4"
KEEP_V08_SHA_PREFIX = "487dc2b8"
ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
XFADE = 0.35
BED_VOL = 0.38

EARLY_USE = 7.78
CLIP_USE = 8.0

REMINT_V09_IDS = {"10_city_plan_lots"}
KEEP_V08_IDS = {"08_property_waves"}
REMINT_V07_IDS = {"03_method_pamphlet"}
EXPLORER_V05_IDS = {"05_explorer_ruler"}
CHAIR_V04_IDS = {"09_empty_chair_claim"}

PLATE_ORDER = [
    "01_hall_open_side_label",
    "02_hall_argument",
    "03_method_pamphlet",
    "04_zoo_gets_ruler",
    "05_explorer_ruler",
    "06_cards_snap_line",
    "07_light_to_heavy",
    "09_empty_chair_claim",
    "08_property_waves",
    "10_city_plan_lots",
    "11_fix_weights",
    "12_pattern_risks_public",
]

SIDE_LABELS = [
    (0.0, 3.5, "A RULER FOR ATOMS"),
    (7.5, 14.0, "KARLSRUHE 1860"),
    (16.0, 26.0, "ATOMIC WEIGHTS"),
    (25.5, 29.8, "A SHARED RULER"),
    (30.0, 36.5, "MASS LINE"),
    (36.8, 42.5, "PROPERTY WAVES"),
    (49.9, 52.3, "A PREDICTION"),
    (52.4, 58.5, "EMPTY CHAIR"),
    (76.6, 85.5, "FIX THE WEIGHTS"),
    (85.5, 89.7, "CHAOS HAS ADDRESS"),
]


def probe(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=nw=1:nk=1", str(path),
            ],
            text=True,
        ).strip()
    )


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def render_side_label(text: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    w, h = 640, 120
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((8, 8, w - 8, h - 8), radius=18, fill=(48, 30, 16, 210))
    d.rounded_rectangle((8, 8, w - 8, h - 8), radius=18, outline=(232, 214, 180, 230), width=3)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Bold.ttf", 36)
    except OSError:
        font = ImageFont.load_default()
    bb = d.textbbox((0, 0), text, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((w - tw) / 2, (h - th) / 2 - 4), text, fill=(245, 232, 205, 255), font=font)
    im.save(dest)


def resolve_clip(pid: str) -> tuple[Path, str]:
    if pid in CHAIR_V04_IDS:
        v04 = RAW_V04 / f"{pid}_v04.mp4"
        if v04.exists() and v04.stat().st_size >= 400_000:
            return v04, "v04_chair_keep"
        raise SystemExit(f"missing kept v04 chair plate {v04}")
    if pid in EXPLORER_V05_IDS:
        v05 = RAW_V05 / f"{pid}_v05.mp4"
        if v05.exists() and v05.stat().st_size >= 400_000:
            return v05, "v05_explorer_keep"
        raise SystemExit(f"missing kept v05 explorer plate {v05}")
    if pid in REMINT_V09_IDS:
        v09 = RAW_V09 / f"{pid}_v09.mp4"
        if v09.exists() and v09.stat().st_size >= 400_000:
            return v09, "v09"
        raise SystemExit(f"missing reminted v09 plate {v09}")
    if pid in KEEP_V08_IDS:
        v08 = RAW_V08 / f"{pid}_v08.mp4"
        if v08.exists() and v08.stat().st_size >= 400_000:
            return v08, "v08_waves_keep"
        raise SystemExit(f"missing kept v08 waves plate {v08}")
    if pid in REMINT_V07_IDS:
        v07 = RAW_V07 / f"{pid}_v07.mp4"
        if v07.exists() and v07.stat().st_size >= 400_000:
            return v07, "v07_swirl_keep"
        raise SystemExit(f"missing kept v07 swirl plate {v07}")
    v02 = RAW_V02 / f"{pid}_v02.mp4"
    if v02.exists() and v02.stat().st_size >= 400_000:
        return v02, "v02_keep"
    raise SystemExit(f"missing kept plate {pid}")


def clip_use_for_index(i: int, chair_index: int) -> float:
    if i < chair_index:
        return EARLY_USE
    return CLIP_USE


def main() -> None:
    if not KEEP_V08.exists():
        raise SystemExit(f"missing KEEP parent {KEEP_V08}")
    keep_sha = sha256(KEEP_V08)
    if not keep_sha.startswith(KEEP_V08_SHA_PREFIX):
        raise SystemExit(
            f"STOP: KEEP v08 sha mismatch want prefix {KEEP_V08_SHA_PREFIX}… got {keep_sha}"
        )
    print(f"KEEP v08 parent sha OK {keep_sha}", flush=True)

    plates_by_id = {p["id"]: p for p in json.loads(PLATES_JSON.read_text())["plates"]}
    ordered_ids = [pid for pid in PLATE_ORDER if pid in plates_by_id]
    if len(ordered_ids) != len(PLATE_ORDER):
        missing = set(PLATE_ORDER) - set(ordered_ids)
        raise SystemExit(f"STOP: plate order missing ids {missing}")

    chair_index = ordered_ids.index("09_empty_chair_claim")
    clips: list[Path] = []
    uses: list[float] = []
    for i, pid in enumerate(ordered_ids):
        clip, src = resolve_clip(pid)
        d = probe(clip)
        use = clip_use_for_index(i, chair_index)
        if d < use - 0.05:
            raise SystemExit(f"short plate {clip} d={d} need>={use}")
        if d < 5.5:
            raise SystemExit(f"short plate {clip} d={d}")
        clips.append(clip)
        uses.append(use)
        print(f"  {pid}: src={d:.2f}s use={use:.2f}s [{src}] {clip.name}", flush=True)

    if not VO.exists():
        raise SystemExit(f"missing VO {VO}")
    if not BED.exists():
        raise SystemExit(f"missing bed {BED}")
    vo_dur = probe(VO)

    offsets = [0.0]
    for i in range(1, len(uses)):
        offsets.append(offsets[-1] + (uses[i - 1] - XFADE))
    pic_dur = offsets[-1] + uses[-1]
    chair_start = offsets[chair_index]
    chair_end = chair_start + uses[chair_index]
    waves_index = ordered_ids.index("08_property_waves")
    city_index = ordered_ids.index("10_city_plan_lots")
    waves_start = offsets[waves_index]
    city_start = offsets[city_index]
    print(
        f"picture≈{pic_dur:.2f}s VO={vo_dur:.2f}s "
        f"chair_window={chair_start:.2f}–{chair_end:.2f}s "
        f"waves≈{waves_start:.2f} city≈{city_start:.2f}",
        flush=True,
    )
    if pic_dur + 0.05 < vo_dur:
        raise SystemExit(f"picture {pic_dur:.2f} < VO {vo_dur:.2f}")
    if not (51.5 <= chair_start <= 53.5):
        raise SystemExit(
            f"STOP: empty chair start {chair_start:.2f} not near VO chair (~52.0–52.4)"
        )

    LABEL_DIR.mkdir(parents=True, exist_ok=True)
    label_pngs: list[tuple[float, float, Path]] = []
    for i, (a, b, text) in enumerate(SIDE_LABELS):
        png = LABEL_DIR / f"label_{i:02d}.png"
        render_side_label(text, png)
        label_pngs.append((a, min(b, vo_dur), png))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    n = len(clips)
    inputs: list[str] = []
    for c in clips:
        inputs += ["-i", str(c)]
    inputs += ["-i", str(VO), "-i", str(BED)]
    label_input_start = n + 2
    for _, _, png in label_pngs:
        inputs += ["-loop", "1", "-t", "1", "-i", str(png)]

    parts: list[str] = []
    for i in range(n):
        use = uses[i]
        parts.append(
            f"[{i}:v]trim=0:{use:.3f},setpts=PTS-STARTPTS,"
            f"scale=1920:1080:force_original_aspect_ratio=decrease,"
            f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=24,format=yuv420p[v{i}]"
        )
    vlabel = "[v0]"
    for i in range(1, n):
        out = f"[vx{i}]"
        offset = offsets[i]
        parts.append(
            f"{vlabel}[v{i}]xfade=transition=fade:duration={XFADE}:offset={offset:.3f}{out}"
        )
        vlabel = out

    cur = vlabel
    for li, (a, b, _png) in enumerate(label_pngs):
        idx = label_input_start + li
        nxt = f"[vl{li}]"
        parts.append(
            f"[{idx}:v]format=rgba,scale=640:-1[lg{li}];"
            f"{cur}[lg{li}]overlay=x=1920-660:y=48:enable='between(t,{a:.3f},{b:.3f})'{nxt}"
        )
        cur = nxt

    parts.append(
        f"[{n}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
        f"atrim=0:{vo_dur:.3f},asetpts=PTS-STARTPTS[vo]"
    )
    parts.append(
        f"[{n+1}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
        f"atrim=0:{vo_dur:.3f},volume={BED_VOL}[bed]"
    )
    parts.append("[vo][bed]amix=inputs=2:duration=first:dropout_transition=0[a]")
    fc = ";".join(parts)

    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            *inputs,
            "-filter_complex", fc,
            "-map", cur, "-map", "[a]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", "-t", f"{vo_dur:.3f}",
            str(OUT),
        ],
        check=True,
    )
    digest = sha256(OUT)
    bytes_n = OUT.stat().st_size
    dur = probe(OUT)
    print(
        f"LANDED {OUT}\n"
        f"  path={OUT}\n"
        f"  bytes={bytes_n}\n"
        f"  sha256={digest}\n"
        f"  duration={dur:.3f}\n"
        f"  chair_picture={chair_start:.2f}–{chair_end:.2f}\n"
        f"  waves≈{waves_start:.2f} city≈{city_start:.2f}\n"
        f"  labels: A PREDICTION 49.9–52.3 · EMPTY CHAIR 52.4–58.5",
        flush=True,
    )

    ICLOUD.mkdir(parents=True, exist_ok=True)
    dest = ICLOUD / OUT.name
    subprocess.run(["cp", "-f", str(OUT), str(dest)], check=True)
    for old in ICLOUD.glob("hos_002_part03_rough_v*.mp4"):
        if old.name == OUT.name:
            continue
        superseded = ICLOUD / f"_SUPERSEDED_do_not_watch_{old.name}"
        if old.exists() and not superseded.exists():
            old.rename(superseded)
        elif old.exists() and superseded.exists():
            old.unlink()
    watch = ICLOUD / "WATCH_part03_v09.txt"
    watch.write_text(
        "WATCH THIS FILE ONLY (Part 03 rough v09 — scrub city-plan house-blocks):\n"
        f"  {OUT.name}\n\n"
        "CoS / Picture→UAT gates for this cut:\n"
        "- Parent v08 sha 487dc2b8…; reminted ONLY 10_city_plan_lots.\n"
        "- ~68–69s desk: flat postcard plan (grid INK only) OR papers only — "
        "HARD REJECT glowing yellow house-blocks / 3D black house icons / map pins / "
        "model-town sprawl / central-table diorama.\n"
        "- ~61s aisle / 08_property_waves KEEP from v08.\n"
        "- EMPTY CHAIR picture ~52.0–60.0; label EMPTY CHAIR 52.4–58.5 KEEP.\n"
        "- KEEP locked: 03 swirl H/C/O v07, 05 Explorer teal trenchcoat, Karlsruhe blank (02), "
        "chair art v04, VO part03_ruler_for_atoms_v01, same PLATE_ORDER.\n"
        "- Part 01 v14 + Part 02 v06 stay LOCKED — do not remint\n"
        "- Do NOT declare PASS here. Scores → CoS. No P04.\n\n"
        "Do not ping Ben. Reject with stills from THIS file only.\n"
        f"keep_v08_sha={keep_sha}\n"
        f"chair_picture={chair_start:.3f}-{chair_end:.3f}\n"
        f"waves≈{waves_start:.3f} city≈{city_start:.3f}\n"
        f"sha256={digest}\nbytes={bytes_n}\nduration={dur:.3f}\n"
    )
    (ICLOUD / "ZZ_OPEN_PART03_V09_ONLY.txt").write_text(
        "Part 03 current cut = hos_002_part03_rough_v09.mp4\n"
        "Part 01 v14 + Part 02 v06 are PASS locked keepers.\n"
    )
    (ICLOUD / "PART03_NEXT.txt").write_text(
        "Part 03 rough LANDED: hos_002_part03_rough_v09.mp4\n"
        "Watch WATCH_part03_v09.txt\n"
        "v09: scrub city-plan house-blocks on 10 only; 08 waves + chair + swirl + Explorer KEPT.\n"
        "Part 01/02 remain locked keepers. No P04.\n"
    )
    print(f"ICLOUD {dest}", flush=True)
    print(f"WATCH {watch}", flush=True)


if __name__ == "__main__":
    main()
