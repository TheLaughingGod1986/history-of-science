#!/usr/bin/env python3
"""Assemble HOS 002 Part 04 rough v04 — scrub house silhouettes ×2.

Parent: hos_002_part04_rough_v03.mp4 sha 79dd7650…
  - REMINT: 02b_cards_sixty_three + 09_risk_bet + 09b_risk_hold
  - KEEP v02's 05/06 sky fills + other v01 plates, VO, bed, labels, PLATE_ORDER
  - P01–P03 FROZEN (P03 sha 30060612…)
  - Scores → CoS only. Do not declare PASS. Do not ping Ben.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PROJ = Path(__file__).resolve().parents[1]
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-04_plates_v01.json"
RAW_V01 = PROJ / "04_Generated-Clips/part04/raw/v01_fast"
RAW_V02 = PROJ / "04_Generated-Clips/part04/raw/v02_fast"
RAW_V04 = PROJ / "04_Generated-Clips/part04/raw/v04_fast"
LABEL_DIR = PROJ / "04_Generated-Clips/part04/refs/v04_side_labels"
VO = PROJ / "02_Voiceover/part04_empty_chairs_v01.wav"
BED = PROJ / "05_Music/hos_002_part01_curious_workshop_v02_norm.wav"
OUT = PROJ / "09_Final-Export/hos_002_part04_rough_v04.mp4"
KEEP_V03 = PROJ / "09_Final-Export/hos_002_part04_rough_v03.mp4"
KEEP_V03_SHA = "79dd7650cb582b548ae4c1c0aa98e4938ff8ec90ba654dea9c0b5c5574ee62e8"
KEEP_P03 = PROJ / "09_Final-Export/hos_002_part03_rough_v09.mp4"
KEEP_P03_SHA = "30060612a00d628998008c9946b8e25319b56f3b9e5613b537c5d2be989bbe4e"
ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
XFADE = 0.35
BED_VOL = 0.38
CLIP_USE = 7.9

REMINT_V04_IDS = {"02b_cards_sixty_three", "09_risk_bet", "09b_risk_hold"}
KEEP_V02_IDS = {"05_columns_families", "06_explorer_leaves_gap"}

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


def resolve_clip(pid: str) -> tuple[Path, str]:
    if pid in REMINT_V04_IDS:
        v04 = RAW_V04 / f"{pid}_v04.mp4"
        if v04.exists() and v04.stat().st_size >= 400_000:
            return v04, "v04_scrub"
        raise SystemExit(f"missing reminted v04 plate {v04}")
    if pid in KEEP_V02_IDS:
        v02 = RAW_V02 / f"{pid}_v02.mp4"
        if v02.exists() and v02.stat().st_size >= 400_000:
            return v02, "v02_window_keep"
        raise SystemExit(f"missing v02 KEEP plate {v02}")
    v01 = RAW_V01 / f"{pid}_v01.mp4"
    if v01.exists() and v01.stat().st_size >= 400_000:
        return v01, "v01_keep"
    raise SystemExit(f"missing plate {v01}")


def main() -> None:
    if not KEEP_P03.exists():
        raise SystemExit(f"missing locked parent {KEEP_P03}")
    p03_sha = sha256(KEEP_P03)
    if p03_sha != KEEP_P03_SHA:
        raise SystemExit(
            f"STOP: P03 sha mismatch want {KEEP_P03_SHA} got {p03_sha} — refuse assemble"
        )
    print(f"KEEP P03 sha OK {p03_sha}", flush=True)

    if not KEEP_V03.exists():
        raise SystemExit(f"missing parent v03 {KEEP_V03}")
    v03_sha = sha256(KEEP_V03)
    if v03_sha != KEEP_V03_SHA:
        raise SystemExit(
            f"STOP: v03 parent sha mismatch want {KEEP_V03_SHA} got {v03_sha}"
        )
    print(f"KEEP v03 parent sha OK {v03_sha}", flush=True)

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

    n = len(ordered_ids)
    use = max(CLIP_USE, (vo_dur + (n - 1) * XFADE) / n + 0.05)
    use = min(use, 8.05)
    print(f"clip_use={use:.3f}s for n={n} VO={vo_dur:.3f}", flush=True)

    clips: list[Path] = []
    uses: list[float] = []
    sources: list[str] = []
    for pid in ordered_ids:
        clip, src = resolve_clip(pid)
        d = probe(clip)
        if d < use - 0.05:
            raise SystemExit(f"short plate {clip} d={d} need>={use}")
        if d < 5.5:
            raise SystemExit(f"short plate {clip} d={d}")
        clips.append(clip)
        uses.append(use)
        sources.append(src)
        print(f"  {pid}: src={d:.2f}s use={use:.2f}s [{src}] {clip.name}", flush=True)

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
    columns_index = ordered_ids.index("05_columns_families")
    columns_start = offsets[columns_index]
    columns_end = columns_start + uses[columns_index]
    plate02b_index = ordered_ids.index("02b_cards_sixty_three")
    plate02b_start = offsets[plate02b_index]
    plate02b_end = plate02b_start + uses[plate02b_index]
    plate09_index = ordered_ids.index("09_risk_bet")
    plate09_start = offsets[plate09_index]
    plate09_end = plate09_start + uses[plate09_index]
    plate09b_index = ordered_ids.index("09b_risk_hold")
    plate09b_start = offsets[plate09b_index]
    plate09b_end = plate09b_start + uses[plate09b_index]

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
    reminted = [pid for pid, src in zip(ordered_ids, sources) if src == "v04_scrub"]
    print(
        f"LANDED {OUT}\n"
        f"  path={OUT}\n"
        f"  bytes={bytes_n}\n"
        f"  sha256={digest}\n"
        f"  duration={dur:.3f}\n"
        f"  reminted={reminted}\n"
        f"  plate02b_picture={plate02b_start:.2f}–{plate02b_end:.2f}\n"
        f"  columns_picture={columns_start:.2f}–{columns_end:.2f}\n"
        f"  explorer_picture={explorer_start:.2f}–{explorer_end:.2f}\n"
        f"  plate09_picture={plate09_start:.2f}–{plate09_end:.2f}\n"
        f"  plate09b_picture={plate09b_start:.2f}–{plate09b_end:.2f}\n"
        f"  keep_p03_sha={p03_sha}\n"
        f"  parent_v03_sha={v03_sha}\n",
        flush=True,
    )

    meta_path = PROJ / "07_Edit-Project/part04_rough_v04_land_meta.json"
    meta_path.write_text(
        json.dumps(
            {
                "cut": OUT.name,
                "path": str(OUT.relative_to(PROJ)),
                "bytes": bytes_n,
                "duration_s": dur,
                "sha256": digest,
                "parent_v03_sha256": v03_sha,
                "reminted_plates": reminted,
                "flow_account": "benoats@googlemail.com",
                "p03_untouched_sha256": p03_sha,
                "plate02b_picture_s": [plate02b_start, plate02b_end],
                "columns_picture_s": [columns_start, columns_end],
                "explorer_picture_s": [explorer_start, explorer_end],
                "plate09_picture_s": [plate09_start, plate09_end],
                "plate09b_picture_s": [plate09b_start, plate09b_end],
                "hos_uat": str(ICLOUD / OUT.name),
                "watch": "WATCH_part04_v04.txt",
                "note": (
                    "Scrub house silhouettes ×2: books ~18–21 (02b) + "
                    "A BET window town ~91–97 (09/09b). KEEP v02 05/06 sky. "
                    "Scores → CoS only. Do not declare PASS."
                ),
            },
            indent=2,
        )
        + "\n"
    )

    ICLOUD.mkdir(parents=True, exist_ok=True)
    dest = ICLOUD / OUT.name
    subprocess.run(["cp", "-f", str(OUT), str(dest)], check=True)
    watch = ICLOUD / "WATCH_part04_v04.txt"
    watch.write_text(
        "WATCH THIS FILE ONLY (Part 04 rough v04 — scrub house silhouettes ×2):\n"
        f"  {OUT.name}\n\n"
        "CoS / Picture→UAT gates for this cut:\n"
        "- Parent v03 FAIL A ~18–21s: brown house silhouettes / scrub masks on books.\n"
        "- Parent v03 FAIL B ~91–97s: model-town / rooftop silhouettes on A BET window.\n"
        "- Reminted: 02b_cards_sixty_three + 09_risk_bet + 09b_risk_hold.\n"
        "- Whole-cut scan: zero house shapes desk OR window at ~18–21 AND ~91–97.\n"
        "- KEEP: ~38–44s night sky only · Explorer teal · glowing chair · Empty Chairs.\n"
        "- Real Veo Fast remint. Continuous motion. No Ken Burns. No silhouette fills.\n"
        "- Part 01 v14 + Part 02 v06 + Part 03 v09 LOCKED — do not remint\n"
        "- Do NOT declare PASS here. Scores → CoS. No P05 until KEEP/LOCK.\n\n"
        "Do not ping Ben. Reject with stills from THIS file only.\n"
        f"keep_p03_sha={p03_sha}\n"
        f"parent_v03_sha={v03_sha}\n"
        f"reminted={','.join(reminted)}\n"
        f"plate02b_picture={plate02b_start:.3f}-{plate02b_end:.3f}\n"
        f"columns_picture={columns_start:.3f}-{columns_end:.3f}\n"
        f"explorer_picture={explorer_start:.3f}-{explorer_end:.3f}\n"
        f"plate09_picture={plate09_start:.3f}-{plate09_end:.3f}\n"
        f"plate09b_picture={plate09b_start:.3f}-{plate09b_end:.3f}\n"
        f"sha256={digest}\nbytes={bytes_n}\nduration={dur:.3f}\n"
    )
    (ICLOUD / "ZZ_OPEN_PART04_V04_ONLY.txt").write_text(
        "Part 04 current cut = hos_002_part04_rough_v04.mp4\n"
        "Part 01 v14 + Part 02 v06 + Part 03 v09 are LOCKED keepers.\n"
        "v03 was UAT FAIL (house silhouettes ×2) — watch v04 only.\n"
    )
    (ICLOUD / "PART04_NEXT.txt").write_text(
        "Part 04 rough remint LANDED: hos_002_part04_rough_v04.mp4\n"
        "Watch WATCH_part04_v04.txt\n"
        "Scores → CoS. No P05 until KEEP/LOCK.\n"
    )
    print(f"ICLOUD {dest}", flush=True)
    print(f"WATCH {watch}", flush=True)
    print(f"META {meta_path}", flush=True)


if __name__ == "__main__":
    main()
