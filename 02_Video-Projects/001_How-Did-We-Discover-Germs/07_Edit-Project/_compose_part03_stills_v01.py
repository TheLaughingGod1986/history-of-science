#!/usr/bin/env python3
"""Part 03 start frames from locked Part 01/02 stills.

GEMINI_API_KEY is empty in 07_Edit-Project/.env — do not invent stills.
Compose / copy the Part 01 v08 + Part 02 lab stills so I2V stays on-style.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
P01 = PROJ / "04_Generated-Clips/part01/refs/v08_stills"
P02 = PROJ / "04_Generated-Clips/part02/refs"
MICRO = PROJ / "04_Generated-Clips/part01/refs/v08_micro_assets"
OUT = PROJ / "04_Generated-Clips/part03/refs"


def ff(*args: str) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *args], check=True)


def copy_scale(src: Path, dest: Path) -> None:
    ff(
        "-i", str(src),
        "-vf", "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,format=yuv420p",
        "-frames:v", "1", "-q:v", "2", str(dest),
    )


def hstack_halves(left: Path, right: Path, dest: Path) -> None:
    ff(
        "-i", str(left), "-i", str(right),
        "-filter_complex",
        "[0:v]scale=1280:720:force_original_aspect_ratio=increase,crop=640:720:320:0[l];"
        "[1:v]scale=1280:720:force_original_aspect_ratio=increase,crop=640:720:320:0[r];"
        "[l][r]hstack=inputs=2,format=yuv420p[v]",
        "-map", "[v]", "-frames:v", "1", "-q:v", "2", str(dest),
    )


def overlay_micro(base: Path, dest: Path) -> None:
    rod = MICRO / "rod_teal_v02.png"
    sph = MICRO / "sphere_amber.png"
    if not rod.exists():
        rod = MICRO / "rod_teal.png"
    extras = []
    filt = "[0:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720[b]"
    last = "b"
    n = 1
    if rod.exists():
        extras += ["-i", str(rod)]
        filt += (
            f";[{n}:v]scale=160:-1[r];"
            f"[{last}][r]overlay=180:420:format=auto[b1]"
        )
        last = "b1"
        n += 1
    if sph.exists():
        extras += ["-i", str(sph)]
        filt += (
            f";[{n}:v]scale=130:-1[s];"
            f"[{last}][s]overlay=980:380:format=auto[b2]"
        )
        last = "b2"
        n += 1
    filt += f";[{last}]format=yuv420p[v]"
    ff(*(["-i", str(base)] + extras), "-filter_complex", filt, "-map", "[v]",
       "-frames:v", "1", "-q:v", "2", str(dest))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = {
        "01_split_world": None,  # special
        "02_perfume_windows": P01 / "03_curtains_clean.jpg",
        "03_hitchhiker_hands": None,  # overlay
        "04_autopsy_to_ward": P01 / "02_corridor_clean.jpg",
        "05_wash_works": P01 / "10_ward_clean.jpg",
        "06_explorer_crosses": P01 / "04_explorer_clean.jpg",
        "07_mocked": P01 / "06_fever_clean.jpg",
        "08_prestige_hands": P01 / "09_hands_clean.jpg",
        "09_they_still_sneer": P01 / "10_ward_end_faceless.jpg",
        "10_flask_tease": P02 / "01_chapter_lab_scope_v01.jpg",
    }
    dest = OUT / "01_split_world_v01.jpg"
    hstack_halves(P01 / "03_curtains_clean.jpg", P01 / "05_instruments_sparse_faceless.jpg", dest)
    print("OK", dest.name, dest.stat().st_size, flush=True)

    for slug, src in jobs.items():
        if src is None:
            continue
        dest = OUT / f"{slug}_v01.jpg"
        if not src.exists():
            raise SystemExit(f"missing source still {src}")
        copy_scale(src, dest)
        print("OK", dest.name, dest.stat().st_size, flush=True)

    dest = OUT / "03_hitchhiker_hands_v01.jpg"
    overlay_micro(P01 / "09_hands_clean.jpg", dest)
    print("OK", dest.name, dest.stat().st_size, flush=True)

    # Prefer part02 split if we want a second look — keep composed 01.
    missing = [p for p in jobs if not (OUT / f"{p}_v01.jpg").exists()]
    if missing:
        raise SystemExit(f"missing composed stills {missing}")
    print("ALL stills ready", flush=True)


if __name__ == "__main__":
    main()
