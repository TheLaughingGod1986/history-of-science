#!/usr/bin/env python3
"""Assemble HOS 002 Part 03 rough v04 — empty-chair remint + skip plate 10.

Parent FAIL: hos_002_part03_rough_v03.mp4 sha b9180ca9… — EMPTY CHAIR ~72–76s
still wooden model-town hero (plate 10 under EMPTY CHAIR label).

v04:
  - REMINT 09_empty_chair_claim from v04_fast
  - SKIP 10_city_plan_lots under EMPTY CHAIR — reuse reminted 09 for that slot
  - KEEP all other plates from v02 (same as v03 keep set)
  - Source KEEP sha check on v03 parent
  - Does not remint Part 01/02. Does not remint Explorer 05. Does not ping Ben.
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
LABEL_DIR = PROJ / "04_Generated-Clips/part03/refs/v04_side_labels"
VO = PROJ / "02_Voiceover/part03_ruler_for_atoms_v01.wav"
BED = PROJ / "05_Music/hos_002_part01_curious_workshop_v02_norm.wav"
OUT = PROJ / "09_Final-Export/hos_002_part03_rough_v04.mp4"
KEEP_V03 = PROJ / "09_Final-Export/hos_002_part03_rough_v03.mp4"
KEEP_V03_SHA_PREFIX = "b9180ca9"
ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
CLIP_USE = 8.0
XFADE = 0.35
BED_VOL = 0.38

REMINT_IDS = {"09_empty_chair_claim"}
# Prefer drop/skip 10 under EMPTY CHAIR label — reuse reminted chair plate.
SKIP_UNDER_EMPTY_CHAIR = {"10_city_plan_lots"}

SIDE_LABELS = [
    (0.0, 3.5, "A RULER FOR ATOMS"),
    (7.5, 14.0, "KARLSRUHE 1860"),
    (16.0, 26.0, "ATOMIC WEIGHTS"),
    (28.0, 35.0, "A SHARED RULER"),
    (37.0, 48.0, "MASS LINE"),
    (50.0, 58.0, "PROPERTY WAVES"),
    (60.0, 68.0, "A PREDICTION"),
    # EMPTY CHAIR only while chair is on screen (09 + skipped-10 reuse).
    # Plate 11 (fix weights) starts ~76.5 — end label before that cut.
    (70.0, 76.4, "EMPTY CHAIR"),
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
    if pid in SKIP_UNDER_EMPTY_CHAIR:
        v04 = RAW_V04 / "09_empty_chair_claim_v04.mp4"
        if v04.exists() and v04.stat().st_size >= 400_000:
            return v04, "v04_chair_reuse_skip10"
        raise SystemExit(f"missing reminted v04 chair to skip-fill {pid}: {v04}")
    if pid in REMINT_IDS:
        v04 = RAW_V04 / f"{pid}_v04.mp4"
        if v04.exists() and v04.stat().st_size >= 400_000:
            return v04, "v04"
        raise SystemExit(f"missing reminted v04 plate {v04}")
    v02 = RAW_V02 / f"{pid}_v02.mp4"
    if v02.exists() and v02.stat().st_size >= 400_000:
        return v02, "v02_keep"
    raise SystemExit(f"missing kept v02 plate {v02}")


def main() -> None:
    if not KEEP_V03.exists():
        raise SystemExit(f"missing KEEP parent {KEEP_V03}")
    keep_sha = sha256(KEEP_V03)
    if not keep_sha.startswith(KEEP_V03_SHA_PREFIX):
        raise SystemExit(
            f"STOP: KEEP v03 sha mismatch want prefix {KEEP_V03_SHA_PREFIX}… got {keep_sha}"
        )
    print(f"KEEP v03 parent FAIL sha OK {keep_sha}", flush=True)

    plates = json.loads(PLATES_JSON.read_text())["plates"]
    clips: list[Path] = []
    for plate in plates:
        pid = plate["id"]
        clip, src = resolve_clip(pid)
        d = probe(clip)
        if d < 5.5:
            raise SystemExit(f"short plate {clip} d={d}")
        clips.append(clip)
        print(f"  {pid}: {d:.2f}s [{src}] {clip.name}", flush=True)

    if not VO.exists():
        raise SystemExit(f"missing VO {VO}")
    if not BED.exists():
        raise SystemExit(f"missing bed {BED}")
    vo_dur = probe(VO)
    pic_dur = len(clips) * CLIP_USE - (len(clips) - 1) * XFADE
    print(f"picture≈{pic_dur:.2f}s VO={vo_dur:.2f}s", flush=True)
    if pic_dur + 0.05 < vo_dur:
        raise SystemExit(f"picture {pic_dur:.2f} < VO {vo_dur:.2f}")

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
        # Skip-10 reuses reminted 09 (same ~8s clip). Identical trim is OK —
        # EMPTY CHAIR stays on vacant glowing chair; no model-town, no freeze-pad.
        parts.append(
            f"[{i}:v]trim=0:{CLIP_USE},setpts=PTS-STARTPTS,"
            f"scale=1920:1080:force_original_aspect_ratio=decrease,"
            f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=24,format=yuv420p[v{i}]"
        )
    vlabel = "[v0]"
    for i in range(1, n):
        out = f"[vx{i}]"
        offset = (CLIP_USE - XFADE) * i
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
        f"  duration={dur:.3f}",
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
    watch = ICLOUD / "WATCH_part03_v04.txt"
    watch.write_text(
        "WATCH THIS FILE ONLY (Part 03 rough v04 — 09 empty-chair remint; skip 10):\n"
        f"  {OUT.name}\n\n"
        "CoS / Picture→UAT gates for this cut:\n"
        "- Parent FAIL v03 sha b9180ca9…; reminted ONLY 09_empty_chair_claim\n"
        "- SKIPPED 10_city_plan_lots under EMPTY CHAIR (reuse chair plate)\n"
        "- 09: vacant glowing chair ALONE in plate-01 Karlsruhe aisle (push-in)\n"
        "- HARD REJECT: wooden model-town / blue-yellow building blocks\n"
        "- Explorer garnish once ~28–36s (plate 05 KEPT from v02)\n"
        "- All real Veo motion (no Ken Burns hero / no freeze-pad)\n"
        "- Animistry side labels (not center stamps)\n"
        "- Part 01 v14 + Part 02 v06 stay LOCKED — do not remint\n\n"
        "Do not ping Ben. Reject with stills from THIS file only.\n"
        f"keep_v03_sha={keep_sha}\n"
        f"sha256={digest}\nbytes={bytes_n}\nduration={dur:.3f}\n"
    )
    (ICLOUD / "ZZ_OPEN_PART03_V04_ONLY.txt").write_text(
        "Part 03 current cut = hos_002_part03_rough_v04.mp4\n"
        "Part 01 v14 + Part 02 v06 are PASS locked keepers.\n"
    )
    (ICLOUD / "PART03_NEXT.txt").write_text(
        "Part 03 rough LANDED: hos_002_part03_rough_v04.mp4\n"
        "Watch WATCH_part03_v04.txt\n"
        "Partial remint: 09 empty chair; skipped 10 under EMPTY CHAIR label.\n"
        "Part 01/02 remain locked keepers.\n"
    )
    print(f"ICLOUD {dest}", flush=True)
    print(f"WATCH {watch}", flush=True)


if __name__ == "__main__":
    main()
