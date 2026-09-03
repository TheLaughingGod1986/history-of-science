#!/usr/bin/env python3
"""PROBE ONLY — Part 03 plate 01_hands_arrive. Veo 3.1 Fast I2V.

Do not mint 02–10. Do not assemble. If Fast refuses ingredients, STOP.
If still-push / Ken Burns / freeze, STOP. One take.
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
STILL = PROJ / "04_Generated-Clips/part03/refs/01_hands_arrive_v01.jpg"
RAW = PROJ / "04_Generated-Clips/part03/raw/v02_fast_probe"
DEST = RAW / "01_hands_arrive_v01.mp4"
META = PROJ / "07_Edit-Project/part03_probe01_fast_meta_v01.json"
MODEL = "Veo 3.1 - Fast"
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
PROMPT = (
    "IMAGE-TO-VIDEO of the attached start frame. Premium Animistry 3D cartoon. "
    "ACTION OPEN: unwashed doctor's hands and a folded cloth are ALREADY moving "
    "in the first second — they reach toward the childbirth bed, the cloth unfolds, "
    "fingers touch the rail. Camera TRANSLATES with the hands into the warm ward "
    "from frame 1. Not a locked still. Not a zoom. Not Ken Burns. Not an empty corridor. "
    "Continuous motion the whole 8 seconds. SCENERY FIRST: bed, curtains, hands, cloth. "
    "NO living cloud. NO germ city. NO split-world. NO floating macro microbes. "
    "NO Explorer. NO Orbit. Silent. No readable text. Not photoreal. Not a modern hospital."
)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_dur(p: Path) -> float:
    r = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(p),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(r.stdout.strip())


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
    tmp = Path(tempfile.mkdtemp(prefix="hos_p03_probe_"))
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
    a = gray_at(mp4, 0.04)
    b = gray_at(mp4, 1.00)
    return mean_abs(a, b)


def extract_frames(mp4: Path, dest_dir: Path) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    for t, name in ((0.04, "t000"), (0.50, "t050"), (1.00, "t100"), (4.00, "t400")):
        subprocess.run(
            [
                "ffmpeg", "-y", "-ss", f"{t:.2f}", "-i", str(mp4),
                "-frames:v", "1", "-q:v", "2", str(dest_dir / f"{name}.jpg"),
            ],
            check=True,
            capture_output=True,
        )


def _blocked_ingredients(err: BaseException) -> bool:
    t = str(err).lower()
    return (
        "image ingredient" in t
        or "cannot use image" in t
        or "create blocked" in t
    )


def main() -> None:
    if not STILL.exists():
        raise SystemExit(f"STOP: missing still {STILL}")
    if veo.already_done(DEST, min_bytes=400_000):
        raise SystemExit(
            f"STOP: probe dest already exists {DEST} — do not overwrite, do not remint a pile."
        )
    RAW.mkdir(parents=True, exist_ok=True)
    profile = flow.profile_path(PROFILE)
    print(f"PROBE 01 Fast I2V profile={profile} still={STILL.name}", flush=True)
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=False, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2000)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit("STOP: Flow not logged in. Do not loop.")
            try:
                info = flow.generate_clip(
                    page,
                    PROMPT,
                    DEST,
                    model=MODEL,
                    start_frame=STILL,
                    timeout_s=700,
                    reuse_project=False,
                    scenery_only=False,
                    attempts=2,
                )
            except Exception as e:
                print(f"STOP: Flow failed on 01_hands_arrive: {e}", flush=True)
                if _blocked_ingredients(e):
                    raise SystemExit(
                        "STOP: Fast refused image ingredients. Do not loop. "
                        "Do not fake Quality."
                    ) from e
                raise SystemExit(
                    "STOP: Flow is out or Create failed. Do not loop."
                ) from e
        finally:
            ctx.close()

    veo.strip_audio(DEST)
    if not DEST.exists() or DEST.stat().st_size < 400_000:
        raise SystemExit(f"STOP: download missing/small {DEST}")
    mv = motion_mean(DEST)
    first = first_second_motion(DEST)
    dur = probe_dur(DEST)
    digest = sha256(DEST)
    frames = RAW / "_probe01_frames"
    extract_frames(DEST, frames)
    meta = {
        "id": "01_hands_arrive",
        "model": MODEL,
        "path": str(DEST),
        "bytes": DEST.stat().st_size,
        "duration": dur,
        "sha256": digest,
        "motion_mean": round(mv, 2),
        "first_second_motion": round(first, 2),
        **info,
    }
    META.write_text(json.dumps(meta, indent=2))
    print(f"PATH {DEST}", flush=True)
    print(f"DUR {dur:.3f}", flush=True)
    print(f"SHA256 {digest}", flush=True)
    print(f"SIZE {DEST.stat().st_size}", flush=True)
    print(f"motion_mean={mv:.2f} first_second={first:.2f}", flush=True)
    if mv < 1.4:
        reject = DEST.with_name(f"_rejected_still_{DEST.name}")
        DEST.rename(reject)
        raise SystemExit(
            f"STOP: still-push / Ken Burns / freeze (motion_mean={mv:.2f}). "
            "Do not remint a pile."
        )
    if first < 2.0:
        reject = DEST.with_name(f"_rejected_no_translate_{DEST.name}")
        DEST.rename(reject)
        raise SystemExit(
            f"STOP: first second does not translate (first_second={first:.2f}). "
            "Do not remint a pile."
        )
    print("PROBE 01 saved — STOP for UAT. Do not mint 02–10.", flush=True)


if __name__ == "__main__":
    main()
