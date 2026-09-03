#!/usr/bin/env python3
"""Part 03 Flow Veo 3.1 Fast I2V. Skip-existing. STOP if Flow is out. No loop."""
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
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-03_plates_v01.json"
REFS = PROJ / "04_Generated-Clips/part03/refs"
RAW = PROJ / "04_Generated-Clips/part03/raw/v01_flow"
META = PROJ / "07_Edit-Project/part03_gen_meta_v01.json"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL", "Veo 3.1 - Fast")
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
FACELESS = (
    "Keep microbes FACELESS if present: rods/spheres/spirals only. "
    "NO eyes NO mouths NO smiles. Continuous motion whole clip — never freeze. "
    "Premium 3D cartoon matching start frame. Silent. NOT photoreal. "
    "NOT modern hospital. No Orbit robot. No readable text."
)


def mean_abs(a: bytes, b: bytes) -> float:
    n = min(len(a), len(b))
    if n == 0:
        return 0.0
    return sum(abs(a[i] - b[i]) for i in range(n)) / n


def motion_mean(mp4: Path) -> float:
    tmp = Path(tempfile.mkdtemp(prefix="hos_p03_m_"))
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
                ["ffmpeg", "-v", "error", "-i", str(p), "-f", "rawvideo", "-pix_fmt", "gray", "pipe:1"]
            )
            for p in pngs
        ]
        diffs = [mean_abs(arr[i], arr[i + 1]) for i in range(len(arr) - 1)]
        return sum(diffs) / len(diffs) if diffs else 0.0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> None:
    plates = json.loads(PLATES_JSON.read_text())["plates"]
    RAW.mkdir(parents=True, exist_ok=True)
    missing = [
        p for p in plates
        if not veo.already_done(RAW / f"{p['id']}_v01.mp4", min_bytes=400_000)
    ]
    meta = {"engine": "flow-ui", "model": MODEL, "plates": []}
    if META.exists():
        try:
            meta = json.loads(META.read_text())
        except Exception:
            pass
    if not missing:
        print("all Flow clips present — no Flow", flush=True)
        META.write_text(json.dumps(meta, indent=2))
        return

    profile = flow.profile_path(PROFILE)
    print(f"Flow profile={profile} model={MODEL} missing={len(missing)}", flush=True)
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=False, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2000)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit("STOP: Flow not logged in. Do not loop.")
            for i, plate in enumerate(plates):
                dest = RAW / f"{plate['id']}_v01.mp4"
                still = REFS / f"{plate['id']}_v01.jpg"
                if veo.already_done(dest, min_bytes=400_000):
                    print(f"  skip {dest.name}", flush=True)
                    continue
                if not still.exists():
                    raise SystemExit(f"STOP: missing still {still}")
                prompt = f"{plate['prompt']} {FACELESS}"
                print(f"\n=== Flow I2V {plate['id']} ({i+1}/{len(plates)}) ===", flush=True)
                try:
                    info = flow.generate_clip(
                        page,
                        prompt,
                        dest,
                        model=MODEL,
                        start_frame=still,
                        timeout_s=700,
                        reuse_project=False,
                        scenery_only=not plate.get("explorer", False),
                        attempts=2,
                    )
                except Exception as e:
                    print(f"STOP: Flow failed on {plate['id']}: {e}", flush=True)
                    META.write_text(json.dumps(meta, indent=2))
                    raise SystemExit(
                        "STOP: Flow is out or Create failed. Do not loop. "
                        f"Last plate={plate['id']}"
                    ) from e
                veo.strip_audio(dest)
                if not dest.exists() or dest.stat().st_size < 400_000:
                    raise SystemExit(f"STOP: download missing/small {dest}")
                mv = motion_mean(dest)
                print(f"  motion_mean={mv:.2f} bytes={dest.stat().st_size}", flush=True)
                if mv < 1.4:
                    reject = dest.with_name(f"_rejected_still_{dest.name}")
                    dest.rename(reject)
                    raise SystemExit(
                        f"STOP: {plate['id']} looks still-push (mean={mv:.2f}). "
                        "Do not ship Ken Burns. Do not loop Flow."
                    )
                meta.setdefault("plates", []).append(
                    {"id": plate["id"], **info, "motion_mean": round(mv, 2), "path": str(dest)}
                )
                META.write_text(json.dumps(meta, indent=2))
        finally:
            ctx.close()
    print("OK all plates minted", flush=True)


if __name__ == "__main__":
    main()
