#!/usr/bin/env python3
"""Assemble HOS 002 Part 04 rough v01 — Empty Chairs.

Parent locked: hos_002_part03_rough_v09 sha 30060612…
  - Real Veo Fast plates under 1869 desk DNA
  - Explorer once on 06
  - Side labels cue spoken teach terms
  - Quiet curious bed (not death-ward)
  - Scores → CoS only. Do not declare PASS. No P05 until KEEP/LOCK.
  - Do not touch P01–P03.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PROJ = Path(__file__).resolve().parents[1]
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-04_plates_v01.json"
RAW = PROJ / "04_Generated-Clips/part04/raw/v01_fast"
LABEL_DIR = PROJ / "04_Generated-Clips/part04/refs/v01_side_labels"
VO = PROJ / "02_Voiceover/part04_empty_chairs_v01.wav"
BED = PROJ / "05_Music/hos_002_part01_curious_workshop_v02_norm.wav"
OUT = PROJ / "09_Final-Export/hos_002_part04_rough_v01.mp4"
KEEP_P03 = PROJ / "09_Final-Export/hos_002_part03_rough_v09.mp4"
KEEP_P03_SHA = "30060612a00d628998008c9946b8e25319b56f3b9e5613b537c5d2be989bbe4e"
ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
XFADE = 0.35
BED_VOL = 0.38
CLIP_USE = 7.9

# Ordered for spoken-meaning lock (VO align): Explorer @ ~45s = EMPTY SEATS.
PLATE_ORDER = [
    "01_chapter_empty_chairs",
    "02_mendeleev_desk_cards",
    "02b_cards_sixty_three",
    "03_what_is_element",
    "04_sort_atomic_weight",
    "05_columns_families",
    "06_explorer_leaves_gap",
    "05b_families_settle",
    "07_eka_placeholders",
    "07b_eka_names_rotate",
    "08_prediction_navigation",
    "08b_navigation_walk",
    "09_risk_bet",
    "09b_risk_hold",
    "10_family_before_weight",
    "11_publish_gaps",
    "11b_wait_and_hunt",
]

# Cue from VO alignment (part04_empty_chairs_v01_align.json) — spoken meaning lock.
SIDE_LABELS = [
    (0.0, 3.0, "EMPTY CHAIRS"),
    (3.0, 8.5, "MENDELEEV"),
    (8.5, 17.5, "ELEMENT"),
    (18.0, 23.0, "ATOMIC WEIGHT"),
    (24.0, 40.0, "PERIODIC TABLE"),
    (44.0, 49.5, "EMPTY SEATS"),
    (50.0, 56.0, "EKA-ALUMINIUM"),
    (56.0, 62.0, "EKA-BORON"),
    (62.0, 68.0, "EKA-SILICON"),
    (68.0, 83.0, "A PREDICTION"),
    (83.5, 100.0, "A BET"),
    (101.0, 118.5, "FAMILY FIRST"),
    (119.0, 127.5, "PUBLISH THE GAPS"),
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


def resolve_clip(pid: str) -> Path:
    clip = RAW / f"{pid}_v01.mp4"
    if clip.exists() and clip.stat().st_size >= 400_000:
        return clip
    raise SystemExit(f"missing plate {clip}")


def main() -> None:
    if not KEEP_P03.exists():
        raise SystemExit(f"missing locked parent {KEEP_P03}")
    p03_sha = sha256(KEEP_P03)
    if p03_sha != KEEP_P03_SHA:
        raise SystemExit(
            f"STOP: P03 sha mismatch want {KEEP_P03_SHA} got {p03_sha} — refuse assemble"
        )
    print(f"KEEP P03 sha OK {p03_sha}", flush=True)

    plates_by_id = {p["id"]: p for p in json.loads(PLATES_JSON.read_text())["plates"]}
    ordered_ids = [pid for pid in PLATE_ORDER if pid in plates_by_id]
    if len(ordered_ids) != len(PLATE_ORDER):
        missing = set(PLATE_ORDER) - set(ordered_ids)
        raise SystemExit(f"STOP: plate order missing ids {missing}")

    if not VO.exists():
        raise SystemExit(f"missing VO {VO}")
    if not BED.exists():
        raise SystemExit(f"missing bed {BED}")
    vo_dur = probe(VO)

    # Size clip_use so picture covers VO without freeze-pad.
    n = len(ordered_ids)
    # pic = n*use - (n-1)*XFADE >= vo_dur
    use = max(CLIP_USE, (vo_dur + (n - 1) * XFADE) / n + 0.05)
    use = min(use, 8.05)  # Veo Fast typical ceiling
    print(f"clip_use={use:.3f}s for n={n} VO={vo_dur:.3f}", flush=True)

    clips: list[Path] = []
    uses: list[float] = []
    for pid in ordered_ids:
        clip = resolve_clip(pid)
        d = probe(clip)
        if d < use - 0.05:
            raise SystemExit(f"short plate {clip} d={d} need>={use}")
        if d < 5.5:
            raise SystemExit(f"short plate {clip} d={d}")
        clips.append(clip)
        uses.append(use)
        print(f"  {pid}: src={d:.2f}s use={use:.2f}s {clip.name}", flush=True)

    offsets = [0.0]
    for i in range(1, len(uses)):
        offsets.append(offsets[-1] + (uses[i - 1] - XFADE))
    pic_dur = offsets[-1] + uses[-1]
    print(f"picture≈{pic_dur:.2f}s VO={vo_dur:.2f}s", flush=True)
    if pic_dur + 0.05 < vo_dur:
        raise SystemExit(
            f"picture {pic_dur:.2f} < VO {vo_dur:.2f} — mint more unique plates "
            "(no freeze-pad)"
        )

    explorer_index = ordered_ids.index("06_explorer_leaves_gap")
    explorer_start = offsets[explorer_index]
    explorer_end = explorer_start + uses[explorer_index]

    LABEL_DIR.mkdir(parents=True, exist_ok=True)
    label_pngs: list[tuple[float, float, Path]] = []
    for i, (a, b, text) in enumerate(SIDE_LABELS):
        png = LABEL_DIR / f"label_{i:02d}.png"
        render_side_label(text, png)
        label_pngs.append((a, min(b, vo_dur), png))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    inputs: list[str] = []
    for c in clips:
        inputs += ["-i", str(c)]
    inputs += ["-i", str(VO), "-i", str(BED)]
    label_input_start = n + 2
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
        f"  explorer_picture={explorer_start:.2f}–{explorer_end:.2f}\n",
        flush=True,
    )

    ICLOUD.mkdir(parents=True, exist_ok=True)
    dest = ICLOUD / OUT.name
    subprocess.run(["cp", "-f", str(OUT), str(dest)], check=True)
    watch = ICLOUD / "WATCH_part04_v01.txt"
    watch.write_text(
        "WATCH THIS FILE ONLY (Part 04 rough v01 — Empty Chairs):\n"
        f"  {OUT.name}\n\n"
        "CoS / Picture→UAT gates for this cut:\n"
        "- Title beat: Empty Chairs. Teach: element / atomic weight / periodic table / "
        "why groundbreaking = hunt before find.\n"
        "- ONE 1869 desk DNA every plate (honey wood, soft lamp, cream blank cards, night window).\n"
        "- Real Veo Fast every plate. Continuous motion. No Ken Burns.\n"
        "- Explorer ONCE on 06 only — teal trenchcoat (Germs/P03 lock), not academic blazer.\n"
        "- HARD REJECT: model-town, glowing yellow house-blocks, black house icons/map pins, "
        "central-table town, Orbit robot, photoreal, vessel fire, clear liquid glass.\n"
        "- Animistry side labels only (spoken-meaning lock).\n"
        "- VO landed 127.76s; 11 board plates + 6 unique desk-DNA coverage plates "
        "(no freeze-pad).\n"
        "- Part 01 v14 + Part 02 v06 + Part 03 v09 LOCKED — do not remint\n"
        "- Do NOT declare PASS here. Scores → CoS. No P05 until KEEP/LOCK.\n\n"
        "Do not ping Ben. Reject with stills from THIS file only.\n"
        f"keep_p03_sha={p03_sha}\n"
        f"explorer_picture={explorer_start:.3f}-{explorer_end:.3f}\n"
        f"sha256={digest}\nbytes={bytes_n}\nduration={dur:.3f}\n"
    )
    (ICLOUD / "ZZ_OPEN_PART04_V01_ONLY.txt").write_text(
        "Part 04 current cut = hos_002_part04_rough_v01.mp4\n"
        "Part 01 v14 + Part 02 v06 + Part 03 v09 are LOCKED keepers.\n"
    )
    (ICLOUD / "PART04_NEXT.txt").write_text(
        "Part 04 rough LANDED: hos_002_part04_rough_v01.mp4\n"
        "Watch WATCH_part04_v01.txt\n"
        "Scores → CoS. No P05 until KEEP/LOCK.\n"
    )
    print(f"ICLOUD {dest}", flush=True)
    print(f"WATCH {watch}", flush=True)


if __name__ == "__main__":
    main()
