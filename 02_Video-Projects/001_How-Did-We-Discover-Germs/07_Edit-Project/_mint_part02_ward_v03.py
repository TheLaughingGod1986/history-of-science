#!/usr/bin/env python3
"""Mint Part 02 plate 08 ward v03 — Flow Veo 3.1 Lite I2V, locked camera, acting only."""
from __future__ import annotations

import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

import orbit_flow_veo_ui as flow  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
STILL = PROJ / "04_Generated-Clips/part02/refs/08_ward_vs_lens_v03.jpg"
OUT = PROJ / "04_Generated-Clips/part02/raw/v03_flow/08_ward_vs_lens_v03.mp4"
MODEL = "Veo 3.1 - Lite"
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)

PROMPT = (
    "IMAGE-TO-VIDEO. Premium Animistry-class 3D cartoon. LOCKED CAMERA — no push-in, "
    "no zoom, no dolly, no Ken Burns, no reframing. Tripod locked. "
    "Animate ONLY subjects already in the start frame: Victorian nurses walk mid-stride "
    "down the ward aisle (legs and arms moving, apron cloth sways), steam/haze drifts "
    "through sunbeams, bed quilts and curtain cloth gently move, sparse faceless 3D "
    "germs (rods/spheres/spirals ONLY — no faces, no eyes, no mouths) slowly drift. "
    "Brass microscope stays in frame as a physical object. Continuous real motion the "
    "whole 8 seconds. Silent picture. "
    "FORBIDDEN: camera push, zoom, orbit, pan that replaces acting; 2D neon overlay; "
    "HUD circles; Explorer child; Orbit robot; Omni Flash; Nano Banana; modern hospital; "
    "readable text; photoreal live-action."
)


def main() -> None:
    if not STILL.exists():
        raise SystemExit(f"missing still {STILL}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    profile = flow.profile_path(PROFILE)
    print(f"profile={profile} model={MODEL}", flush=True)
    print(f"still={STILL}", flush=True)
    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=False, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2000)
            if not flow.looks_logged_in(page):
                raise SystemExit(
                    "Flow not logged in. Complete Google Flow Ultra login on this VM, then rerun."
                )
            info = flow.generate_clip(
                page,
                PROMPT,
                OUT,
                model=MODEL,
                start_frame=STILL,
                timeout_s=900,
                reuse_project=False,
                scenery_only=False,
                attempts=1,
            )
            print(f"OK {OUT} bytes={OUT.stat().st_size} info={info}", flush=True)
        finally:
            ctx.close()


if __name__ == "__main__":
    main()
