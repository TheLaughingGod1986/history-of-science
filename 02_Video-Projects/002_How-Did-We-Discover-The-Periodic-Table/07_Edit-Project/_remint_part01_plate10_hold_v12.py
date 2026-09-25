#!/usr/bin/env python3
"""Remint Part 01 plate 10 HOLD via Flow Veo — ore IN pan, shimmer only, no clear flasks."""
from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips/part01/raw/v01_fast"
REJECT = PROJ / "04_Generated-Clips/part01/_rejected_uat_v12_plate10"
DEST = RAW / "10_rock_not_fire_v01.mp4"
MODEL = "Veo 3.1 - Fast"
PROFILE = Path(os.environ.get("ORBIT_FLOW_PROFILE", str(Path.home() / ".playwright-hos-flow-profile")))
PROMPT = (
    "History of Science locked look: premium Animistry-class 3D cartoon workshop, warm cinematic light. "
    "Not photoreal. Silent. No readable text. No Orbit. Continuous gentle camera drift. "
    "ONE continuous wide shot (no split-screen). "
    "LEFT: dark rough ore chunk on a COLD metal grate. Only a subtle colourless heat shimmer / air haze rises — "
    "NO flames, NO fire, NO orange coals, NO burning, NO fire plumes, NO orange wisps, NO smoke plumes. "
    "RIGHT: classic brass balance scale. LEFT hanging pan holds heavy dark ore sitting FLAT INSIDE the pan metal — "
    "ore rests on the pan floor, pan clearly depressed, chains taut. RIGHT pan empty. "
    "Table around the scale EMPTY of glassware — ZERO clear glass flasks, ZERO bottles, ZERO liquid in glass. "
    "Background shelves: OPAQUE ceramic jars and sealed metal canisters ONLY — zero clear glass anywhere in frame. "
    "HARD REJECT: clear glass, liquid in glass, flames, fire, floating ore, hanging pots, split-screen, text, Orbit."
)

def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    REJECT.mkdir(parents=True, exist_ok=True)
    profile = flow.profile_path(PROFILE)
    print(f"Flow remint plate10 HOLD profile={profile}", flush=True)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2500)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit("STOP: Flow not logged in")
            tmp = REJECT / "10_rock_not_fire_new.mp4"
            info = flow.generate_clip(
                page, PROMPT, tmp, model=MODEL, start_frame=None,
                scenery_only=True, reuse_project=False, attempts=2, timeout_s=700,
            )
            veo.strip_audio(tmp)
            if not tmp.exists() or tmp.stat().st_size < 400_000:
                raise SystemExit("STOP: plate10 download missing/small")
            if DEST.exists():
                shutil.move(str(DEST), str(REJECT / "10_rock_not_fire_v01_prev.mp4"))
            shutil.move(str(tmp), str(DEST))
            print(f"SAVED {DEST} bytes={DEST.stat().st_size} info={info}", flush=True)
        finally:
            ctx.close()

if __name__ == "__main__":
    main()
