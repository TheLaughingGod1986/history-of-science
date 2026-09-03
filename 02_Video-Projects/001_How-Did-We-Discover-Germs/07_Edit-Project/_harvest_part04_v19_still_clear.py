#!/usr/bin/env python3
"""Download the already-submitted v19 STILL CLEAR Fast take. NO Create."""
from __future__ import annotations

import hashlib
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
RAW = PROJ / "04_Generated-Clips/part04/raw/v01_fast_probe"
DEST = RAW / "04_still_clear_v19.mp4"
PROJECT = "862353da-4815-4028-af6c-c71515ede323"
URL = f"https://labs.google/fx/tools/flow/project/{PROJECT}"
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
STILL_MEAN = 1.4
STILL_FIRST = 2.0


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def mean_abs(a: bytes, b: bytes) -> float:
    n = min(len(a), len(b))
    if n == 0:
        return 0.0
    return sum(abs(a[i] - b[i]) for i in range(n)) / n


def gray_at(mp4: Path, t: float) -> bytes:
    return subprocess.check_output(
        [
            "ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(mp4),
            "-frames:v", "1", "-vf", "scale=320:180,format=gray",
            "-f", "rawvideo", "-pix_fmt", "gray", "pipe:1",
        ]
    )


def motion_mean(mp4: Path) -> float:
    tmp = Path(tempfile.mkdtemp(prefix="hos_p04_h19_"))
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
    if veo.already_done(DEST, min_bytes=400_000):
        print(f"already have {DEST}", flush=True)
        return
    profile = flow.profile_path(PROFILE)
    print(f"HARVEST no-Create project={PROJECT} dest={DEST}", flush=True)
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        try:
            page.goto(URL, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2500)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit("STOP: Flow not logged in. Do not loop.")
            before = set()
            print(f"  wait_and_download from {page.url}", flush=True)
            mid = flow.wait_and_download(
                page, DEST, before_ids=before, timeout_s=700, min_elapsed_s=0
            )
            veo.strip_audio(DEST)
            if not DEST.exists() or DEST.stat().st_size < 400_000:
                raise SystemExit("STOP: harvest missing/small. Do not Create.")
            mv = motion_mean(DEST)
            first = mean_abs(gray_at(DEST, 0.04), gray_at(DEST, 1.00))
            extract_frames(DEST)
            print(
                f"SAVED {DEST} mid={mid} bytes={DEST.stat().st_size} "
                f"sha256={sha256(DEST)} motion={mv:.2f} first={first:.2f}",
                flush=True,
            )
            if mv < STILL_MEAN or first < STILL_FIRST:
                raise SystemExit(
                    f"STOP: harvested take is still-push first={first:.2f} mean={mv:.2f}. "
                    "Do not remint. Do not Create."
                )
        finally:
            ctx.close()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback

        traceback.print_exc()
        raise
