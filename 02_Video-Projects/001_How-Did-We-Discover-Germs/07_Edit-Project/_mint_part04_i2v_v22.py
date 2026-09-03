#!/usr/bin/env python3
"""Part 04 v22 — ONE Fast I2V of 08_passengers from t72 lock still.

Punch-in on 08_v21 failed (second bottles + sprites on the neck).
Do not T2V. Do not remint. If Create dies or the take is a straight neck
or a second bottle: STOP. Do not assemble.
"""
from __future__ import annotations

import hashlib
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
RAW = PROJ / "04_Generated-Clips/part04/raw/v01_fast_probe"
META = PROJ / "07_Edit-Project/part04_gen_meta_v22.json"
START = RAW / "_start_t72_pasteur_i2v_v22.jpg"
DEST = RAW / "08_passengers_v22.mp4"
PROMPT = (
    "IMAGE-TO-VIDEO of the attached start frame. Hold this EXACT Pasteur flask — "
    "do not change the neck. The only neck is the S-curve swan-neck already in the "
    "still. Round-bottom sitting on wood. Fine dust motes in a sunbeam only. Empty "
    "wood around the bottle. NO other glassware. NO second flask. NO conical. "
    "NO stand. NO germ sprites. NO spiked blobs. NO neck change. Camera already "
    "eases in the first second. Continuous 8s. Silent. No text. Do NOT freeze."
)
MODEL = "Veo 3.1 - Fast"
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


def gray_at(mp4: Path, t: float, w: int = 320, h: int = 180) -> bytes:
    return subprocess.check_output(
        [
            "ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(mp4),
            "-frames:v", "1", "-vf", f"scale={w}:{h},format=gray",
            "-f", "rawvideo", "-pix_fmt", "gray", "pipe:1",
        ]
    )


def motion_mean(mp4: Path) -> float:
    tmp = Path(tempfile.mkdtemp(prefix="hos_p04_m_"))
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


def first_second_motion(mp4: Path) -> float:
    return mean_abs(gray_at(mp4, 0.04), gray_at(mp4, 1.00))


def extract_frames(mp4: Path, dest_dir: Path) -> None:
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
    if not START.exists() or START.stat().st_size < 10_000:
        raise SystemExit(f"STOP: missing t72 start frame {START}")
    if veo.already_done(DEST, min_bytes=400_000):
        print(f"already have {DEST.name} — no Flow", flush=True)
        return
    profile = flow.profile_path(PROFILE)
    print(f"Flow profile={profile} model={MODEL} I2V start={START.name}", flush=True)
    meta: dict = {"engine": "flow-ui", "model": MODEL, "plates": []}
    if META.exists():
        try:
            meta = json.loads(META.read_text())
        except Exception:
            pass

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2000)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit("STOP: Flow not logged in. Do not loop.")
            print("=== ONE Fast I2V 08_passengers from t72 lock ===", flush=True)
            try:
                info = flow.generate_clip(
                    page,
                    PROMPT,
                    DEST,
                    model=MODEL,
                    start_frame=START,
                    scenery_only=False,
                    reuse_project=False,
                    attempts=1,
                    timeout_s=700,
                )
            except Exception as e:
                META.write_text(json.dumps(meta, indent=2))
                raise SystemExit(
                    f"STOP: Create/I2V died. Do not remint. Do not assemble. {e}"
                ) from e
            veo.strip_audio(DEST)
            if not DEST.exists() or DEST.stat().st_size < 400_000:
                raise SystemExit("STOP: I2V download missing/small. Do not remint.")
            mv = motion_mean(DEST)
            first = first_second_motion(DEST)
            info["motion_mean"] = round(mv, 2)
            info["first_second_motion"] = round(first, 2)
            info["path"] = str(DEST)
            info["i2v"] = True
            info["start_frame"] = str(START)
            print(
                f"  motion_mean={mv:.2f} first_second={first:.2f} bytes={DEST.stat().st_size}",
                flush=True,
            )
            extract_frames(DEST, RAW / f"_qa_{DEST.stem}")
            if mv < STILL_MEAN or first < STILL_FIRST:
                reject = DEST.with_name(f"_rejected_still_{DEST.name}")
                DEST.rename(reject)
                META.write_text(json.dumps(meta, indent=2))
                raise SystemExit(
                    f"STOP: I2V still-push first={first:.2f} mean={mv:.2f}. "
                    "Do not remint. Do not assemble."
                )
            meta.setdefault("plates", []).append({"id": "08_passengers", **info})
            META.write_text(json.dumps(meta, indent=2))
        finally:
            ctx.close()
    print(f"OK I2V saved {DEST} sha256={sha256(DEST)}", flush=True)
    print("QA frames extracted — inspect neck/second-bottle before assemble", flush=True)


if __name__ == "__main__":
    main()
