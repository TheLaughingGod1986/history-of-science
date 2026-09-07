#!/usr/bin/env python3
"""Assemble HOS 002 Part 03 rough v06 — Atomic Weights props remint only.

Parent PASS: hos_002_part03_rough_v05.mp4 sha 3642d005…
  - REMINT 03_method_pamphlet from v06_fast (sparse H 1 / O 16 / C 12 / N 14 / S 32)
  - Optional 04_zoo_gets_ruler from v06_fast if present
  - KEEP 05 Explorer trenchcoat (v05), empty chair (v04), rest from v02
  - Same side-label cue sheet (ATOMIC WEIGHTS stays)
  - Does not remint Part 01/02. Does not ping Ben. No P04.
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
LABEL_DIR = PROJ / "04_Generated-Clips/part03/refs/v06_side_labels"
VO = PROJ / "02_Voiceover/part03_ruler_for_atoms_v01.wav"
BED = PROJ / "05_Music/hos_002_part01_curious_workshop_v02_norm.wav"
OUT = PROJ / "09_Final-Export/hos_002_part03_rough_v06.mp4"
KEEP_V05 = PROJ / "09_Final-Export/hos_002_part03_rough_v05.mp4"
KEEP_V05_SHA_PREFIX = "3642d005"
ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
CLIP_USE = 8.0
XFADE = 0.35
BED_VOL = 0.38

REMINT_IDS = {"03_method_pamphlet"}
OPTIONAL_REMINT_IDS = {"04_zoo_gets_ruler"}
EXPLORER_V05_IDS = {"05_explorer_ruler"}
CHAIR_V04_IDS = {"09_empty_chair_claim"}
SKIP_UNDER_EMPTY_CHAIR = {"10_city_plan_lots"}

SIDE_LABELS = [
    (0.0, 3.5, "A RULER FOR ATOMS"),
    (7.5, 14.0, "KARLSRUHE 1860"),
    (16.0, 26.0, "ATOMIC WEIGHTS"),
    (28.0, 35.0, "A SHARED RULER"),
    (37.0, 48.0, "MASS LINE"),
    (50.0, 58.0, "PROPERTY WAVES"),
    (60.0, 68.0, "A PREDICTION"),
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
    if pid in REMINT_IDS or pid in OPTIONAL_REMINT_IDS:
        v06 = RAW_V06 / f"{pid}_v06.mp4"
        if v06.exists() and v06.stat().st_size >= 400_000:
            return v06, "v06"
        if pid in OPTIONAL_REMINT_IDS:
            v02 = RAW_V02 / f"{pid}_v02.mp4"
            if v02.exists() and v02.stat().st_size >= 400_000:
                return v02, "v02_keep_skip_optional04"
            raise SystemExit(f"missing optional/keep plate {pid}")
        raise SystemExit(f"missing reminted v06 plate {v06}")
    v02 = RAW_V02 / f"{pid}_v02.mp4"
    if v02.exists() and v02.stat().st_size >= 400_000:
        return v02, "v02_keep"
    raise SystemExit(f"missing kept v02 plate {v02}")


def main() -> None:
    if not KEEP_V05.exists():
        raise SystemExit(f"missing KEEP parent {KEEP_V05}")
    keep_sha = sha256(KEEP_V05)
    if not keep_sha.startswith(KEEP_V05_SHA_PREFIX):
        raise SystemExit(
            f"STOP: KEEP v05 sha mismatch want prefix {KEEP_V05_SHA_PREFIX}… got {keep_sha}"
        )
    print(f"KEEP v05 parent PASS sha OK {keep_sha}", flush=True)

    plates = json.loads(PLATES_JSON.read_text())["plates"]
    clips: list[Path] = []
    used_v06_04 = False
    for plate in plates:
        pid = plate["id"]
        clip, src = resolve_clip(pid)
        if pid == "04_zoo_gets_ruler" and src == "v06":
            used_v06_04 = True
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
    watch = ICLOUD / "WATCH_part03_v06.txt"
    opt_note = (
        "04 also reminted sparse marks"
        if used_v06_04
        else "04 KEPT from v02 (03 alone judged enough / optional skip)"
    )
    watch.write_text(
        "WATCH THIS FILE ONLY (Part 03 rough v06 — Atomic Weights props remint):\n"
        f"  {OUT.name}\n\n"
        "CoS / Picture→UAT gates for this cut:\n"
        "- Parent PASS v05 sha 3642d005…; reminted REQUIRED 03_method_pamphlet only "
        f"(props). {opt_note}.\n"
        "- Under ATOMIC WEIGHTS (16–26s): a FEW papers show H 1 / O 16 / C 12 / "
        "N 14 / S 32 — phone-readable dark ink; MOST sheets stay blank.\n"
        "- HARD REJECT: every sheet covered; chicken-scratch; formula walls; Ken Burns\n"
        "- KEEP locked: hall DNA, 05 Explorer teal trenchcoat, 09 empty chair vacant, "
        "side label ATOMIC WEIGHTS, VO part03_ruler_for_atoms_v01\n"
        "- Part 01 v14 + Part 02 v06 stay LOCKED — do not remint\n"
        "- Do NOT declare PASS here. Scores → CoS. No P04.\n\n"
        "Do not ping Ben. Reject with stills from THIS file only.\n"
        f"keep_v05_sha={keep_sha}\n"
        f"sha256={digest}\nbytes={bytes_n}\nduration={dur:.3f}\n"
    )
    (ICLOUD / "ZZ_OPEN_PART03_V06_ONLY.txt").write_text(
        "Part 03 current cut = hos_002_part03_rough_v06.mp4\n"
        "Part 01 v14 + Part 02 v06 are PASS locked keepers.\n"
    )
    (ICLOUD / "PART03_NEXT.txt").write_text(
        "Part 03 rough LANDED: hos_002_part03_rough_v06.mp4\n"
        "Watch WATCH_part03_v06.txt\n"
        "Partial remint: 03 Atomic Weights props only; Explorer + empty chair KEPT.\n"
        "Part 01/02 remain locked keepers. No P04.\n"
    )
    print(f"ICLOUD {dest}", flush=True)
    print(f"WATCH {watch}", flush=True)


if __name__ == "__main__":
    main()
