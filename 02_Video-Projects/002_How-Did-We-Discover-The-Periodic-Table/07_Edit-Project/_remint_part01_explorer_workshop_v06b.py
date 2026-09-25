#!/usr/bin/env python3
"""Remint Explorer into the locked liquid workshop (not the Germs ward)."""
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
RAW = PROJ / "04_Generated-Clips/part01/raw/v01_fast"
REJECT = PROJ / "04_Generated-Clips/part01/_rejected_uat_v06"
START = PROJ / "09_Final-Export/_uat_part01_v06/02_jars.jpg"
DEST = RAW / "05_explorer_ore_gas_v01.mp4"
META = PROJ / "07_Edit-Project/part01_remint_explorer_workshop_v06b_meta.json"
MODEL = "Veo 3.1 - Fast"
PROFILE = Path(os.environ.get("ORBIT_FLOW_PROFILE", str(Path.home() / ".playwright-hos-flow-profile")))
PROMPT = (
    "IMAGE-TO-VIDEO of the attached chemistry workshop. Keep these CLEAR COLORED "
    "LIQUID flasks. The History of Science Explorer from film 1 ENTERS this exact "
    "workshop: young boy, messy wavy brown hair, round gold wire-rim glasses, "
    "teal-blue long overcoat with gold atom lapel pin, tan waistcoat, white shirt, "
    "dark brown floppy bow tie, rolled brown trousers, brown lace-up boots "
    "(never furry cuffs), brown satchel with brass compass. Exactly ONE boy. "
    "He lifts a heavy dark ore in one hand and a glass jar of CLEAR glowing blue "
    "LIQUID in the other, baffled both count as stuff. Continuous acting. "
    "Ores stay on the wood. No powder in jars. No twins. No Orbit. Silent."
)


def main() -> None:
    if not START.exists():
        raise SystemExit(f"STOP missing start {START}")
    if DEST.exists():
        REJECT.mkdir(parents=True, exist_ok=True)
        arch = REJECT / "05_explorer_ore_gas_v01_ward.mp4"
        if arch.exists():
            arch.unlink()
        shutil.move(str(DEST), str(arch))
    from playwright.sync_api import sync_playwright
    profile = flow.profile_path(PROFILE)
    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2000)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit("STOP: Flow not logged in.")
            info = flow.generate_clip(
                page, PROMPT, DEST, model=MODEL, start_frame=START,
                reuse_project=False, attempts=1, timeout_s=700,
            )
            veo.strip_audio(DEST)
            META.write_text(json.dumps({"id": "05_explorer_ore_gas", **info}, indent=2))
            print(f"SAVED {DEST} bytes={DEST.stat().st_size}", flush=True)
        finally:
            ctx.close()


if __name__ == "__main__":
    main()
