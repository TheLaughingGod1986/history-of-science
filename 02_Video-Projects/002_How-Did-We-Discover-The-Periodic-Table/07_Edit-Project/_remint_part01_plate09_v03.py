#!/usr/bin/env python3
"""Remint only plate 09 — seating plan (v01 museum drift fail)."""
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
REJECT = PROJ / "04_Generated-Clips/part01/_rejected_uat_v02"
META = PROJ / "07_Edit-Project/part01_remint_plate09_v03_meta.json"
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
    "cinematic light, period science world. Not photoreal. Not live-action. "
    "Silent picture. No readable text, logos, or UI. No Orbit orange robot. "
    "No cute atom faces. Continuous motion the whole clip."
)
HARD = (
    "SUBJECT LOCK: a long wooden banquet table with wooden chairs along both sides. "
    "Several chairs are EMPTY and glow soft gold. A few occupied seats hold plain "
    "closed jars only. Camera dollies along the EMPTY glowing chairs. "
    "FORBIDDEN: museum, dinosaur, fossil cabinet, crystal display, natural history, "
    "hologram, lightning in glass, chalkboard, periodic table poster, people."
)


def main() -> None:
    plates = {p["id"]: p for p in json.loads(PLATES_JSON.read_text())["plates"]}
    plate = plates[PID]
    src = RAW / f"{PID}_v01.mp4"
    if src.exists():
        REJECT.mkdir(parents=True, exist_ok=True)
        dest = REJECT / f"{PID}_v01_museum_drift.mp4"
        if dest.exists():
            dest.unlink()
        shutil.move(str(src), str(dest))
        print(f"archived {dest.name}", flush=True)

    dest = RAW / f"{PID}_v01.mp4"
    if dest.exists():
        dest.unlink()

    prompt = f"{STYLE} {HARD} {plate['prompt']}"
    meta: dict = {"engine": "flow-ui", "model": MODEL, "plate": PID, "mode": "t2v-v03"}
    profile = flow.profile_path(PROFILE)
    print(f"Flow remint plate09 v03 profile={profile}", flush=True)

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
                start_frame=None,
                scenery_only=True,
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
    print("OK plate 09 v03 remint finished", flush=True)


if __name__ == "__main__":
    main()
