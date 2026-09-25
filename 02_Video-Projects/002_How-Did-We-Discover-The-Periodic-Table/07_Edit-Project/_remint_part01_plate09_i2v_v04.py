#!/usr/bin/env python3
"""Remint plate 09 via start-frame I2V from approved open still (plate 01 look).

T2V kept drifting to natural-history museum. This path locks composition
from 00_open_empty_chairs.jpg then animates a lateral dolly along empty
glowing chairs at a banquet table.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-01_plates_v01.json"
RAW = PROJ / "04_Generated-Clips/part01/raw/v01_fast"
REJECT = PROJ / "04_Generated-Clips/part01/_rejected_uat_v03"
META = PROJ / "07_Edit-Project/part01_remint_plate09_i2v_v04_meta.json"
START = PROJ / "09_Final-Export/_uat_part01_v02/00_open_empty_chairs.jpg"
MODEL = "Veo 3.1 - Fast"
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
PID = "09_seating_plan_gap"
STYLE = (
    "History of Science locked look: premium Animistry-class 3D cartoon, warm "
    "cinematic light, period science world. Not photoreal. Silent picture. "
    "No readable text. No Orbit robot. Continuous motion the whole clip."
)
MOTION = (
    "Animate the attached start frame. Keep the same glowing empty wooden chairs "
    "and warm period hall. Slow lateral camera dolly along the row of EMPTY "
    "glowing chairs — chairs are the subject. Optional: reveal a long wooden "
    "banquet table beside the chairs with a few plain closed jars on occupied "
    "seats only. FORBIDDEN: museum, dinosaur, fossil, crystal cabinet, "
    "hologram, chalkboard, people, readable text."
)


def main() -> None:
    if not START.exists() or START.stat().st_size < 50_000:
        raise SystemExit(f"STOP: missing start frame {START}")
    plates = {p["id"]: p for p in json.loads(PLATES_JSON.read_text())["plates"]}
    plate = plates[PID]
    src = RAW / f"{PID}_v01.mp4"
    if src.exists():
        REJECT.mkdir(parents=True, exist_ok=True)
        dest_rej = REJECT / f"{PID}_v01_museum_t2v.mp4"
        if dest_rej.exists():
            dest_rej.unlink()
        shutil.move(str(src), str(dest_rej))
        print(f"archived {dest_rej.name}", flush=True)

    dest = RAW / f"{PID}_v01.mp4"
    if dest.exists():
        dest.unlink()

    prompt = f"{STYLE} {MOTION} {plate['prompt']}"
    meta: dict = {
        "engine": "flow-ui",
        "model": MODEL,
        "plate": PID,
        "mode": "i2v-v04",
        "start_frame": str(START),
    }
    profile = flow.profile_path(PROFILE)
    print(f"Flow I2V plate09 v04 start={START.name} profile={profile}", flush=True)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2000)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit("STOP: Flow not logged in.")
            info = flow.generate_clip(
                page,
                prompt,
                dest,
                model=MODEL,
                start_frame=START,
                reuse_project=False,
                attempts=1,
                timeout_s=700,
            )
            veo.strip_audio(dest)
            if not dest.exists() or dest.stat().st_size < 400_000:
                raise SystemExit(f"STOP: download missing/small {dest}")
            meta.update(info)
            META.write_text(json.dumps(meta, indent=2))
            print(f"SAVED {dest.name} bytes={dest.stat().st_size}", flush=True)
        finally:
            ctx.close()
    print("OK plate 09 I2V v04 finished", flush=True)


if __name__ == "__main__":
    main()
