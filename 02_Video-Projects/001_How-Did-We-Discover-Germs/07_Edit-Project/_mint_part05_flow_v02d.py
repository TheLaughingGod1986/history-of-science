#!/usr/bin/env python3
"""Part 05 UAT — remint 04 and 06 once. Fast T2V. Composition change. If Create dies: STOP."""
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
META = PROJ / "07_Edit-Project/part05_gen_meta_v02d.json"
MODEL = "Veo 3.1 - Fast"
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)

PLATES = [
    {
        "id": "04_explorer_scrubs",
        "out": "04_explorer_scrubs_v02d.mp4",
        "prompt": (
            "Premium Animistry 3D cartoon, History of Science Part 01 v08. "
            "Wide 1860s surgical theatre. Dark wood aisle, wooden benches, "
            "hanging lamps, a wooden table. One boy Explorer with messy brown "
            "hair, round gold glasses, a teal trenchcoat, tan vest, and brown "
            "bow tie walks down the aisle and leaves the room. The theatre "
            "stays. Silent. Continuous 8 seconds."
        ),
    },
    {
        "id": "06_soap_hands",
        "out": "06_soap_hands_v02d.mp4",
        "prompt": (
            "Premium Animistry 3D cartoon, History of Science Part 01 v08. "
            "Medium-wide shot of a period stone basin. A brass tap runs. "
            "A white soap bar sits on a folded cloth at the rim. White foam "
            "sits in the bowl. Clear water. Dark wood wall behind. Silent. "
            "Continuous 8 seconds."
        ),
    },
]


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
    tmp = Path(tempfile.mkdtemp(prefix="hos_p05v02d_m_"))
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


def mint_one(page, plate: dict, dest: Path) -> dict:
    print(f"  T2V {plate['id']} start=None", flush=True)
    info = flow.generate_clip(
        page,
        plate["prompt"],
        dest,
        model=MODEL,
        start_frame=None,
        scenery_only=True,
        reuse_project=False,
        attempts=1,
        timeout_s=700,
    )
    veo.strip_audio(dest)
    if not dest.exists() or dest.stat().st_size < 400_000:
        raise SystemExit(f"STOP: download missing/small {dest}")
    mv = motion_mean(dest)
    first = first_second_motion(dest)
    info["motion_mean"] = round(mv, 2)
    info["first_second_motion"] = round(first, 2)
    info["path"] = str(dest)
    info["i2v"] = False
    print(
        f"  motion_mean={mv:.2f} first_second={first:.2f} bytes={dest.stat().st_size}",
        flush=True,
    )
    extract_frames(dest)
    return info


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    meta: dict = {"engine": "flow-ui", "model": MODEL, "plates": []}
    profile = flow.profile_path(PROFILE)
    print(f"Flow profile={profile} model={MODEL} remint=04,06 T2V once", flush=True)
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2000)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit("STOP: Flow not logged in. Do not loop.")
            for plate in PLATES:
                dest = RAW / plate["out"]
                if veo.already_done(dest, min_bytes=400_000):
                    print(f"  skip {dest.name}", flush=True)
                    continue
                print(f"\n=== Fast {plate['id']} → {plate['out']} ===", flush=True)
                try:
                    info = mint_one(page, plate, dest)
                except Exception as e:
                    META.write_text(json.dumps(meta, indent=2))
                    raise SystemExit(
                        f"STOP: Create died. Do not loop. Last plate={plate['id']}"
                    ) from e
                meta.setdefault("plates", []).append({"id": plate["id"], **info})
                META.write_text(json.dumps(meta, indent=2))
        finally:
            ctx.close()
    print("OK part 05 v02d 04/06 remint finished", flush=True)


if __name__ == "__main__":
    main()
