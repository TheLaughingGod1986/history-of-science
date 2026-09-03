#!/usr/bin/env python3
"""Part 03 v02 start frames — scenery-first, no germ-macro overlays.

GEMINI keys are empty. Compose from locked Part 01 v08 + Part 02 lab stills.
Do not overlay micro assets on plates 01–04 (or 09). No living-cloud stills.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
P01 = PROJ / "04_Generated-Clips/part01/refs/v08_stills"
P02 = PROJ / "04_Generated-Clips/part02/refs"
OUT = PROJ / "04_Generated-Clips/part03/refs"


def ff(*args: str) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *args],
        check=True,
    )


def copy_scale(src: Path, dest: Path) -> None:
    ff(
        "-i", str(src),
        "-vf",
        "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,format=yuv420p",
        "-frames:v", "1", "-q:v", "2", str(dest),
    )


def crop_tighter(src: Path, dest: Path, x: int, y: int) -> None:
    """Scale up then crop — used so 08 is not the same frame as 01."""
    ff(
        "-i", str(src),
        "-vf",
        f"scale=1600:900:force_original_aspect_ratio=increase,"
        f"crop=1280:720:{x}:{y},format=yuv420p",
        "-frames:v", "1", "-q:v", "2", str(dest),
    )


def crop_top(src: Path, dest: Path) -> None:
    """Keep the room/desk; drop foreground germ garnish at the bottom."""
    ff(
        "-i", str(src),
        "-vf",
        "scale=1280:900:force_original_aspect_ratio=increase,"
        "crop=1280:720:0:0,format=yuv420p",
        "-frames:v", "1", "-q:v", "2", str(dest),
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = {
        "01_hands_arrive": P01 / "09_hands_clean.jpg",
        "02_perfume_windows": P01 / "03_curtains_clean.jpg",
        "03_bedside_hands": P01 / "05_instruments_clean.jpg",
        "04_autopsy_to_ward": P01 / "02_corridor_clean.jpg",
        "05_wash_works": P01 / "10_ward_clean.jpg",
        "06_explorer_crosses": P01 / "04_explorer_clean.jpg",
        "07_mocked": P01 / "06_fever_clean.jpg",
        "09_they_still_sneer": P01 / "10_ward_clean.jpg",
    }
    for slug, src in jobs.items():
        if not src.exists():
            raise SystemExit(f"missing source still {src}")
        dest = OUT / f"{slug}_v01.jpg"
        copy_scale(src, dest)
        print("OK", dest.name, dest.stat().st_size, flush=True)

    dest08 = OUT / "08_prestige_hands_v01.jpg"
    crop_tighter(P01 / "09_hands_clean.jpg", dest08, 0, 80)
    print("OK", dest08.name, dest08.stat().st_size, flush=True)

    dest10 = OUT / "10_flask_in_the_room_v01.jpg"
    lab = P02 / "01_chapter_lab_scope_v01.jpg"
    if not lab.exists():
        raise SystemExit(f"missing lab still {lab}")
    crop_top(lab, dest10)
    print("OK", dest10.name, dest10.stat().st_size, flush=True)

    need = [
        "01_hands_arrive",
        "02_perfume_windows",
        "03_bedside_hands",
        "04_autopsy_to_ward",
        "05_wash_works",
        "06_explorer_crosses",
        "07_mocked",
        "08_prestige_hands",
        "09_they_still_sneer",
        "10_flask_in_the_room",
    ]
    missing = [p for p in need if not (OUT / f"{p}_v01.jpg").exists()]
    if missing:
        raise SystemExit(f"missing composed stills {missing}")
    print("ALL v02 stills ready (no germ overlay on 01-04)", flush=True)


if __name__ == "__main__":
    main()
