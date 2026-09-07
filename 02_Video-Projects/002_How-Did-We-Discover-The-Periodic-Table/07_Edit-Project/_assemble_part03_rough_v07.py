#!/usr/bin/env python3
"""Assemble HOS 002 Part 03 rough v07 — empty-chair sync + swirl mid-air marks.

Parent: hos_002_part03_rough_v06.mp4 sha a1285f9a…
  - REMINT 03_method_pamphlet from v07_fast (desk KEEP + 2–3 mid-air H 1 / C 12 / O 16)
  - EDIT-ONLY: slide empty chair under VO ~52.0–58.5; labels EMPTY CHAIR + A PREDICTION
  - KEEP chair art (v04) — no Flow remint of chair
  - Restore 10_city_plan under spoken "city plan" (~68s) now that EMPTY CHAIR label moved
  - KEEP 05 Explorer trenchcoat (v05), Karlsruhe blank (02), VO part03_ruler_for_atoms_v01
  - Skip 04 remint (v02 keep). No P01/P02 remint. No P04. Scores → CoS only.
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
RAW_V06 = PROJ / "04_Generated-Clips/part03/raw/v06_fast"
RAW_V07 = PROJ / "04_Generated-Clips/part03/raw/v07_fast"
LABEL_DIR = PROJ / "04_Generated-Clips/part03/refs/v07_side_labels"
VO = PROJ / "02_Voiceover/part03_ruler_for_atoms_v01.wav"
BED = PROJ / "05_Music/hos_002_part01_curious_workshop_v02_norm.wav"
OUT = PROJ / "09_Final-Export/hos_002_part03_rough_v07.mp4"
KEEP_V06 = PROJ / "09_Final-Export/hos_002_part03_rough_v06.mp4"
KEEP_V06_SHA_PREFIX = "a1285f9a"
ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
XFADE = 0.35
BED_VOL = 0.38

# Mild early compress so plate 09 (reordered to index 7) starts ~52.0 under spoken chair.
EARLY_USE = 7.78  # plates before empty chair
CLIP_USE = 8.0

REMINT_IDS = {"03_method_pamphlet"}
EXPLORER_V05_IDS = {"05_explorer_ruler"}
CHAIR_V04_IDS = {"09_empty_chair_claim"}
# v06 skipped 10 under late EMPTY CHAIR label; v07 restores city plan for VO ~68s.
SKIP_UNDER_EMPTY_CHAIR: set[str] = set()

# Reorder: pull empty chair earlier (before property waves) so it lands on VO ~52.
PLATE_ORDER = [
    "01_hall_open_side_label",
    "02_hall_argument",
    "03_method_pamphlet",
    "04_zoo_gets_ruler",
    "05_explorer_ruler",
    "06_cards_snap_line",
    "07_light_to_heavy",
    "09_empty_chair_claim",  # moved earlier
    "08_property_waves",
    "10_city_plan_lots",  # restored — spoken "city plan" ~67.9
    "11_fix_weights",
    "12_pattern_risks_public",
]

# Labels retimed to spoken words (align.json). EMPTY CHAIR + A PREDICTION required.
SIDE_LABELS = [
    (0.0, 3.5, "A RULER FOR ATOMS"),
    (7.5, 14.0, "KARLSRUHE 1860"),
    (16.0, 26.0, "ATOMIC WEIGHTS"),
    (25.5, 29.8, "A SHARED RULER"),  # spoken ruler ~25.6
    (30.0, 36.5, "MASS LINE"),  # spoken mass ~30.4 / ~42
    (36.8, 42.5, "PROPERTY WAVES"),  # spoken waves ~36.9 — was fighting chair at 50–58
    (49.9, 52.3, "A PREDICTION"),  # spoken prediction ~49.91
    (52.4, 58.5, "EMPTY CHAIR"),  # spoken chair/empty ~52.4; hold ~6.1s
    (76.6, 85.5, "FIX THE WEIGHTS"),
    (85.5, 89.7, "CHAOS HAS ADDRESS"),  # leave unless fights; Chaos spoken ~80.2
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
    if pid in SKIP_UNDER_EMPTY_CHAIR:
        v04 = RAW_V04 / "09_empty_chair_claim_v04.mp4"
        if v04.exists() and v04.stat().st_size >= 400_000:
            return v04, "v04_chair_reuse_skip10"
        raise SystemExit(f"missing reminted v04 chair to skip-fill {pid}: {v04}")
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
    if pid in REMINT_IDS:
        v07 = RAW_V07 / f"{pid}_v07.mp4"
        if v07.exists() and v07.stat().st_size >= 400_000:
            return v07, "v07"
        raise SystemExit(f"missing reminted v07 plate {v07}")
    # Optional: if a leftover v06 04 exists and is marked, still prefer v02 keep (skip 04).
    v02 = RAW_V02 / f"{pid}_v02.mp4"
    if v02.exists() and v02.stat().st_size >= 400_000:
        return v02, "v02_keep"
    # Fallback: v06 remint of 04 if v02 missing (should not happen).
    v06 = RAW_V06 / f"{pid}_v06.mp4"
    if v06.exists() and v06.stat().st_size >= 400_000:
        return v06, "v06_fallback"
    raise SystemExit(f"missing kept plate {pid}")


def clip_use_for_index(i: int, chair_index: int) -> float:
    if i < chair_index:
        return EARLY_USE
    return CLIP_USE


def main() -> None:
    if not KEEP_V06.exists():
        raise SystemExit(f"missing KEEP parent {KEEP_V06}")
    keep_sha = sha256(KEEP_V06)
    if not keep_sha.startswith(KEEP_V06_SHA_PREFIX):
        raise SystemExit(
            f"STOP: KEEP v06 sha mismatch want prefix {KEEP_V06_SHA_PREFIX}… got {keep_sha}"
        )
    print(f"KEEP v06 parent sha OK {keep_sha}", flush=True)

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

    # Picture timeline with variable uses + xfade
    offsets = [0.0]
    for i in range(1, len(uses)):
        offsets.append(offsets[-1] + (uses[i - 1] - XFADE))
    pic_dur = offsets[-1] + uses[-1]
    chair_start = offsets[chair_index]
    chair_end = chair_start + uses[chair_index]
    print(
        f"picture≈{pic_dur:.2f}s VO={vo_dur:.2f}s "
        f"chair_window={chair_start:.2f}–{chair_end:.2f}s",
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
    watch = ICLOUD / "WATCH_part03_v07.txt"
    watch.write_text(
        "WATCH THIS FILE ONLY (Part 03 rough v07 — EMPTY CHAIR sync + swirl mid-air marks):\n"
        f"  {OUT.name}\n\n"
        "CoS / Picture→UAT gates for this cut:\n"
        "- Parent v06 sha a1285f9a…; reminted REQUIRED 03_method_pamphlet only (props).\n"
        "- 04 SKIPPED (v02 keep). Empty chair art KEPT from v04 — NO Flow remint of chair.\n"
        "- Under ATOMIC WEIGHTS (16–26s): desk marks KEEP + 2–3 mid-air sheets show "
        "H 1 / C 12 / O 16 — phone-readable dark ink; MOST sheets stay blank.\n"
        "- EMPTY CHAIR picture ~52.0–58.5 under spoken chair/empty; label EMPTY CHAIR "
        "52.4–58.5 (not over city-plan).\n"
        "- A PREDICTION ~49.9–52.3 on spoken prediction.\n"
        "- HARD REJECT: reminted empty chair; model-town; EMPTY CHAIR over city-plan; "
        "every sheet marked; Ken Burns\n"
        "- KEEP locked: hall DNA, 05 Explorer teal trenchcoat, Karlsruhe blank (02), "
        "VO part03_ruler_for_atoms_v01\n"
        "- Part 01 v14 + Part 02 v06 stay LOCKED — do not remint\n"
        "- Do NOT declare PASS here. Scores → CoS. No P04.\n\n"
        "Do not ping Ben. Reject with stills from THIS file only.\n"
        f"keep_v06_sha={keep_sha}\n"
        f"chair_picture={chair_start:.3f}-{chair_end:.3f}\n"
        f"sha256={digest}\nbytes={bytes_n}\nduration={dur:.3f}\n"
    )
    (ICLOUD / "ZZ_OPEN_PART03_V07_ONLY.txt").write_text(
        "Part 03 current cut = hos_002_part03_rough_v07.mp4\n"
        "Part 01 v14 + Part 02 v06 are PASS locked keepers.\n"
    )
    (ICLOUD / "PART03_NEXT.txt").write_text(
        "Part 03 rough LANDED: hos_002_part03_rough_v07.mp4\n"
        "Watch WATCH_part03_v07.txt\n"
        "v07: empty-chair edit sync + 03 swirl mid-air H/C/O; Explorer + chair art KEPT.\n"
        "Part 01/02 remain locked keepers. No P04.\n"
    )
    print(f"ICLOUD {dest}", flush=True)
    print(f"WATCH {watch}", flush=True)


if __name__ == "__main__":
    main()
