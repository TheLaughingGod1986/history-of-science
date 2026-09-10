#!/usr/bin/env python3
"""Assemble HOS 002 Part 05 rough v01 — The Guests Arrive.

Plate-first: do not run until every plate in KEEP_REMINTS exists and has passed
continuous-playback UAT. Fail if picture < VO (no freeze-pad).

P04 lessons: unique plates, xfade 0.35, CLIP_USE 7.9, looped workshop bed,
cream-on-brown house end card after last picture. Paint banned.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PROJ = Path(__file__).resolve().parents[1]
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-05_plates_v01.json"
RAW_V01Q = PROJ / "04_Generated-Clips/part05/raw/v01_quality"
LABEL_DIR = PROJ / "04_Generated-Clips/part05/refs/v01_side_labels"
VO = PROJ / "02_Voiceover/part05_the_guests_arrive_v01.wav"
BED = PROJ / "05_Music/hos_002_part01_curious_workshop_v02_loop130_norm.wav"
OUT = PROJ / "09_Final-Export/hos_002_part05_rough_v01.mp4"
SWIFT = PROJ / "07_Edit-Project/_render_hos_end_card.swift"
KEEP_P04 = PROJ / "09_Final-Export/hos_002_part04_rough_v25.mp4"
KEEP_P04_SHA = "e78027c0c58abe9284f7b85de693a08caabd3ad8ee45b64624eadd0329942bb1"
KEEP_P03 = PROJ / "09_Final-Export/hos_002_part03_rough_v09.mp4"
KEEP_P03_SHA = "30060612a00d628998008c9946b8e25319b56f3b9e5613b537c5d2be989bbe4e"
ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
XFADE = 0.35
BED_VOL = 0.38
CLIP_USE = 7.9
END_CARD_S = 3.5

KEEP_MANIFEST = PROJ / "07_Edit-Project/part05_keep_manifest_v01.json"


def load_keep() -> dict[str, tuple[Path, str]]:
    man = json.loads(KEEP_MANIFEST.read_text())
    out: dict[str, tuple[Path, str]] = {}
    for pid, rec in man["keep"].items():
        out[pid] = (PROJ / rec["path"], rec["sha256"])
    return out


KEEP_REMINTS = load_keep()

SIDE_LABELS = [
    (0.0, 6.0, "THE GUESTS"),
    (6.0, 14.0, "1875"),
    (14.0, 22.0, "GALLIUM"),
    (22.0, 30.0, "SCANDIUM"),
    (30.0, 38.0, "GERMANIUM"),
    (38.0, 46.0, "NOT A BLUFF"),
    (46.0, 58.0, "NAVIGATION"),
    (58.0, 70.0, "NOBLE GASES"),
    (70.0, 82.0, "ATOMIC NUMBER"),
    (82.0, 94.0, "YOUR WORLD"),
    (94.0, 108.0, "A CITY"),
    (108.0, 200.0, "EMPTY STILL"),
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


def render_end_card_png(dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    bin_path = Path("/tmp/render_hos_end_card_002")
    subprocess.run(
        ["swiftc", "-o", str(bin_path), str(SWIFT)],
        check=True,
    )
    subprocess.run([str(bin_path), str(dest)], check=True)


def main() -> None:
    if not KEEP_P04.exists() or sha256(KEEP_P04) != KEEP_P04_SHA:
        raise SystemExit("STOP: Part 04 v25 lock missing or sha mismatch — do not remint 04")
    if not KEEP_P03.exists() or sha256(KEEP_P03) != KEEP_P03_SHA:
        raise SystemExit("STOP: Part 03 v09 lock missing or sha mismatch")
    if not VO.exists():
        raise SystemExit(f"missing VO {VO}")
    if not BED.exists():
        raise SystemExit(f"missing bed {BED}")

    plates = json.loads(PLATES_JSON.read_text())["plates"]
    ordered_ids = [p["id"] for p in plates]
    missing: list[str] = []
    clips: list[Path] = []
    for pid in ordered_ids:
        if pid not in KEEP_REMINTS:
            missing.append(f"{pid} (not KEEP yet)")
            continue
        clip, want = KEEP_REMINTS[pid]
        if not clip.exists() or clip.stat().st_size < 400_000:
            missing.append(f"{pid} missing {clip}")
            continue
        got = sha256(clip)
        if got != want:
            missing.append(f"{pid} sha mismatch want {want} got {got}")
            continue
        clips.append(clip)
    if missing:
        raise SystemExit(
            "STOP plate-first: do not assemble until KEEP UAT. Missing:\n  "
            + "\n  ".join(missing)
        )

    vo_dur = probe(VO)
    n = len(clips)
    uses = [min(CLIP_USE, probe(c)) for c in clips]
    offsets = [0.0]
    for i in range(1, n):
        offsets.append(offsets[-1] + uses[i - 1] - XFADE)
    pic_dur = offsets[-1] + uses[-1]
    print(f"picture≈{pic_dur:.2f}s VO={vo_dur:.2f}s", flush=True)
    if pic_dur + 0.05 < vo_dur:
        raise SystemExit(
            f"picture {pic_dur:.2f} < VO {vo_dur:.2f} — mint more unique plates "
            "(no freeze-pad)"
        )

    LABEL_DIR.mkdir(parents=True, exist_ok=True)
    label_pngs: list[tuple[float, float, Path]] = []
    for i, (a, b, text) in enumerate(SIDE_LABELS):
        png = LABEL_DIR / f"label_{i:02d}.png"
        render_side_label(text, png)
        label_pngs.append((a, min(b, vo_dur), png))

    card_png = PROJ / "04_Generated-Clips/part05/refs/end_card.png"
    render_end_card_png(card_png)
    card_mp4 = PROJ / "04_Generated-Clips/part05/refs/end_card.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-loop", "1", "-i", str(card_png), "-t", f"{END_CARD_S:.3f}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "24",
            str(card_mp4),
        ],
        check=True,
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    inputs: list[str] = []
    for c in clips:
        inputs += ["-i", str(c)]
    inputs += ["-i", str(VO), "-i", str(BED), "-i", str(card_mp4)]
    label_input_start = n + 3
    for _, _, png in label_pngs:
        inputs += ["-loop", "1", "-t", "1", "-i", str(png)]

    parts: list[str] = []
    for i in range(n):
        u = uses[i]
        parts.append(
            f"[{i}:v]trim=0:{u:.3f},setpts=PTS-STARTPTS,"
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

    card_in = n + 2
    parts.append(
        f"[{card_in}:v]scale=1920:1080,fps=24,format=yuv420p,setpts=PTS-STARTPTS[card]"
    )
    join_at = vo_dur - 0.35
    parts.append(
        f"{cur}[card]xfade=transition=fade:duration=0.35:offset={join_at:.3f}[vout]"
    )
    total = vo_dur + END_CARD_S - 0.35

    parts.append(
        f"[{n}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
        f"atrim=0:{vo_dur:.3f},asetpts=PTS-STARTPTS,"
        f"apad=pad_dur={END_CARD_S:.3f}[vo]"
    )
    parts.append(
        f"[{n+1}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
        f"atrim=0:{total:.3f},volume={BED_VOL}[bed]"
    )
    parts.append("[vo][bed]amix=inputs=2:duration=first:dropout_transition=0[a]")
    fc = ";".join(parts)

    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            *inputs,
            "-filter_complex", fc,
            "-map", "[vout]", "-map", "[a]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", "-t", f"{total:.3f}",
            str(OUT),
        ],
        check=True,
    )
    digest = sha256(OUT)
    print(f"LANDED {OUT} sha256={digest} dur={probe(OUT):.3f}", flush=True)
    watch = (
        f"WATCH THIS FILE ONLY (Part 05 rough v01 — The Guests Arrive):\n  {OUT.name}\n"
        f"sha256={digest}\n"
        "Plate-first KEEP assemble. Scores → CoS. Do not declare PASS.\n"
    )
    (PROJ / "07_Edit-Project/WATCH_part05_v01.txt").write_text(watch)
    ICLOUD.mkdir(parents=True, exist_ok=True)
    dest = ICLOUD / OUT.name
    subprocess.run(["cp", "-f", str(OUT), str(dest)], check=True)
    (ICLOUD / "WATCH_part05_v01.txt").write_text(watch)
    print(f"ICLOUD {dest}", flush=True)


if __name__ == "__main__":
    main()
