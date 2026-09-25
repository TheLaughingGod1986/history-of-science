#!/usr/bin/env python3
"""Remint plate 09 v06 — I2V from a SOLID banquet-chair still.

v05 mid/end read as real chairs; the open ~1s was still translucent/ghost.
Animate the attached opaque start frame. Do not restore holograms.
Writes a candidate first; only swaps RAW after a successful download.
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
REJECT = PROJ / "04_Generated-Clips/part01/_rejected_uat_v05"
META = PROJ / "07_Edit-Project/part01_remint_plate09_i2v_v06_meta.json"
START = PROJ / "04_Generated-Clips/part01/refs/v01_stills/09_banquet_solid_v06.jpg"
CANDIDATE = RAW / "09_seating_plan_gap_v06_candidate.mp4"
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
    "cinematic light, period science workshop. Not photoreal. Silent picture. "
    "No readable text. No Orbit robot. Continuous motion."
)
MOTION = (
    "IMAGE-TO-VIDEO of the attached start frame. Keep EVERY chair SOLID OPAQUE "
    "carved wood with cream upholstery — real furniture on the floor, never "
    "see-through, never ghost, never hologram, never miniature icons. Long "
    "wooden banquet table with closed plain jars on the TABLE only. Slow "
    "lateral dolly past the empty full-size chairs. HARD REJECT: translucent "
    "chairs, ghost chairs, glowing flat silhouettes, holograms, energy orbs, "
    "lightning flasks, chalkboard writing, museum, dinosaur, people, Orbit."
)


def main() -> None:
    if not START.exists() or START.stat().st_size < 50_000:
        raise SystemExit(f"STOP: missing start frame {START}")
    plate = {p["id"]: p for p in json.loads(PLATES_JSON.read_text())["plates"]}[PID]
    if CANDIDATE.exists():
        CANDIDATE.unlink()
    CANDIDATE.parent.mkdir(parents=True, exist_ok=True)
    prompt = f"{STYLE} {MOTION} {plate['prompt']}"
    meta: dict = {
        "engine": "flow-ui",
        "model": MODEL,
        "plate": PID,
        "mode": "i2v-v06",
        "start_frame": str(START),
    }
    profile = flow.profile_path(PROFILE)
    print(f"Flow I2V plate09 v06 start={START.name}", flush=True)
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
                CANDIDATE,
                model=MODEL,
                start_frame=START,
                reuse_project=False,
                attempts=1,
                timeout_s=700,
            )
            veo.strip_audio(CANDIDATE)
            if not CANDIDATE.exists() or CANDIDATE.stat().st_size < 400_000:
                raise SystemExit(f"STOP: download missing/small {CANDIDATE}")
            src = RAW / f"{PID}_v01.mp4"
            REJECT.mkdir(parents=True, exist_ok=True)
            if src.exists():
                dest_rej = REJECT / f"{PID}_v01_i2v_v05.mp4"
                if dest_rej.exists():
                    dest_rej.unlink()
                shutil.move(str(src), str(dest_rej))
                print(f"archived {dest_rej.name}", flush=True)
            shutil.copy2(CANDIDATE, src)
            meta.update(info)
            META.write_text(json.dumps(meta, indent=2) + "\n")
            print(f"SAVED {src.name} bytes={src.stat().st_size}", flush=True)
        finally:
            ctx.close()
    print("OK plate 09 I2V v06 finished", flush=True)


if __name__ == "__main__":
    main()
