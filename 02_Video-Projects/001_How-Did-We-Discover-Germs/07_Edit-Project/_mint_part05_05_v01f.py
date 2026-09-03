#!/usr/bin/env python3
"""Part 05 — remint 05 theatre_wins only. Fast T2V. No 03. No 01–04 remint.

If Create dies: STOP. Caller walks frames; one sprite remint is a second run.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips/part05/raw/v01_fast_probe"
META = PROJ / "07_Edit-Project/part05_gen_meta_v01f.json"
MODEL = "Veo 3.1 - Fast"
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
STILL_MEAN = 1.4
STILL_FIRST = 2.0
OUT_NAME = os.environ.get("HOS_P05_05_OUT", "05_theatre_wins_v01d.mp4")
PROMPT = (
    "Premium Animistry 3D cartoon, History of Science Part 01 v08 / v21. "
    "Wide 1860s wooden hospital ward already in motion. The people and the room "
    "are the picture. Patients rest in wooden beds with white linen. Nurses in "
    "blue dresses and white aprons walk the aisle and tend beds. Warm oil lamps "
    "and brass globe sconces. Clear empty air above the aisle — dust motes only, "
    "no floating characters, no floating toys, no coloured spheres in the air. "
    "Camera slowly trucks down the wooden aisle. Continuous 8 seconds. "
    "Silent. No hats. No matching twins. No modern hospital. No Orbit. "
    "No Explorer. No readable text. NOT photoreal. No freeze. No Ken Burns."
)


def mean_abs(a: bytes, b: bytes) -> float:
    n = min(len(a), len(b))
    if n == 0:
        return 0.0
    return sum(abs(a[i] - b[i]) for i in range(n)) / n


def gray_at(mp4: Path, t: float, w: int = 320, h: int = 180) -> bytes:
    return subprocess.check_output(
        [
            "ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(mp4),
            "-frames:v", "1", "-vf", f"scale={w}:{h},format=gray",
            "-f", "rawvideo", "-pix_fmt", "gray", "pipe:1",
        ]
    )


def motion_mean(mp4: Path) -> float:
    tmp = Path(tempfile.mkdtemp(prefix="hos_p05_05_m_"))
    try:
        subprocess.run(
            [
                "ffmpeg", "-y", "-i", str(mp4),
                "-vf", "fps=8,scale=320:180,format=gray",
                str(tmp / "%03d.png"),
            ],
            check=True,
            capture_output=True,
        )
        pngs = sorted(tmp.glob("*.png"))
        arr = [
            subprocess.check_output(
                [
                    "ffmpeg", "-v", "error", "-i", str(p),
                    "-f", "rawvideo", "-pix_fmt", "gray", "pipe:1",
                ]
            )
            for p in pngs
        ]
        diffs = [mean_abs(arr[i], arr[i + 1]) for i in range(len(arr) - 1)]
        return sum(diffs) / len(diffs) if diffs else 0.0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def extract_frames(mp4: Path) -> None:
    dest_dir = RAW / f"_qa_{mp4.stem}"
    dest_dir.mkdir(parents=True, exist_ok=True)
    for t, name in ((0.04, "t000"), (1.00, "t100"), (4.00, "t400"), (7.20, "t720")):
        subprocess.run(
            [
                "ffmpeg", "-y", "-ss", f"{t:.2f}", "-i", str(mp4),
                "-frames:v", "1", "-q:v", "3", str(dest_dir / f"{name}.jpg"),
            ],
            check=True,
            capture_output=True,
        )


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    dest = RAW / OUT_NAME
    if veo.already_done(dest, min_bytes=400_000):
        print(f"skip {dest.name}", flush=True)
        return
    profile = flow.profile_path(PROFILE)
    print(f"Flow profile={profile} model={MODEL} out={dest.name}", flush=True)
    from playwright.sync_api import sync_playwright

    meta: dict = {"engine": "flow-ui", "model": MODEL, "out": str(dest)}
    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2000)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit("STOP: Flow not logged in. Do not loop.")
            print(f"\n=== Fast T2V 05_theatre_wins → {dest.name} ===", flush=True)
            try:
                info = flow.generate_clip(
                    page,
                    PROMPT,
                    dest,
                    model=MODEL,
                    start_frame=None,
                    scenery_only=True,
                    reuse_project=False,
                    attempts=1,
                    timeout_s=700,
                )
            except Exception as e:
                META.write_text(json.dumps(meta, indent=2))
                raise SystemExit(
                    f"STOP: Create died. Do not loop. Last plate=05_theatre_wins ({e})"
                ) from e
            veo.strip_audio(dest)
            if not dest.exists() or dest.stat().st_size < 400_000:
                raise SystemExit(f"STOP: download missing/small {dest}")
            mv = motion_mean(dest)
            first = mean_abs(gray_at(dest, 0.04), gray_at(dest, 1.00))
            info["motion_mean"] = round(mv, 2)
            info["first_second_motion"] = round(first, 2)
            info["path"] = str(dest)
            print(
                f"  motion_mean={mv:.2f} first_second={first:.2f} bytes={dest.stat().st_size}",
                flush=True,
            )
            if mv < STILL_MEAN or first < STILL_FIRST:
                dest.rename(dest.with_name(f"_rejected_still_{dest.name}"))
                raise SystemExit("STOP: still-push on 05. Do not loop.")
            extract_frames(dest)
            meta["plate"] = info
            META.write_text(json.dumps(meta, indent=2))
        finally:
            ctx.close()
    print("OK 05 mint finished", flush=True)


if __name__ == "__main__":
    main()
