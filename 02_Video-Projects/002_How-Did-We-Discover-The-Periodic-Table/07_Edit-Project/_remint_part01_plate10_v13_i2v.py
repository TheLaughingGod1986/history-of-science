#!/usr/bin/env python3
"""ONE-SHOT remint Part 01 plate 10 — Flow Veo (I2V preferred, T2V fallback). Lite OK.

UAT FAIL: orange embers under ore grate → colourless shimmer only.
KEEP: ore IN brass pan · no clear flask beside scale · continuous motion · no Orbit.
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
RAW = PROJ / "04_Generated-Clips/part01/raw/v01_fast"
REJECT = PROJ / "04_Generated-Clips/part01/_rejected_uat_v13_plate10"
START = PROJ / "07_Edit-Project/_qa_v13_plate10_prep/p10_start.png"
DEST = RAW / "10_rock_not_fire_v01.mp4"
META = PROJ / "07_Edit-Project/part01_remint_plate10_v13_meta.json"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL", "Veo 3.1 - Lite")
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)

SCENE = (
    "History of Science locked look: premium Animistry-class 3D cartoon workshop, "
    "warm cinematic light. Not photoreal. Silent. No readable text. No Orbit robot. "
    "Continuous gentle camera drift the whole clip — never a still freeze, never Ken Burns. "
    "ONE continuous wide shot. "
    "LEFT: dark rough ore chunk on a COLD metal grate. ONLY a subtle colourless heat shimmer / "
    "air refraction haze rises through the grate — NO orange, NO red, NO yellow glow, NO embers, "
    "NO coals, NO flames, NO fire, NO burning, NO fire plumes, NO orange wisps. Under the grate: "
    "dark cool metal shadow with colourless shimmer only. "
    "RIGHT: classic brass balance scale. LEFT hanging pan holds heavy dark ore sitting FLAT "
    "INSIDE the pan metal — ore on the pan floor, pan clearly depressed, chains taut. RIGHT pan empty. "
    "Table around the scale EMPTY of glassware — ZERO clear glass flasks beside the scale. "
    "Background shelves: prefer OPAQUE ceramic jars and sealed metal canisters; minimise clear glass. "
    "HARD REJECT: orange/red fire or ember glow under the grate, clear flask beside the scale, "
    "floating ore, hanging pots, split-screen, text, Orbit, Ken Burns still-push."
)

I2V_PROMPT = (
    "IMAGE-TO-VIDEO of the attached start frame. Keep THIS exact workshop composition. "
    + SCENE
)

T2V_PROMPT = (
    "TEXT-TO-VIDEO scenery only (no character reference). "
    + SCENE
)


def main() -> None:
    if not START.exists():
        raise SystemExit(f"STOP: missing start frame {START}")
    RAW.mkdir(parents=True, exist_ok=True)
    REJECT.mkdir(parents=True, exist_ok=True)
    profile = flow.profile_path(PROFILE)
    print(f"Flow plate10 v13 model={MODEL} profile={profile}", flush=True)
    print(f"  start_frame={START}", flush=True)

    from playwright.sync_api import sync_playwright

    meta: dict = {
        "engine": "flow-ui",
        "model": MODEL,
        "mode": "i2v-v13-plate10",
        "plates": [],
    }
    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(3000)
            for _ in range(3):
                flow.dismiss_banners(page)
                page.wait_for_timeout(700)
            logged = False
            for attempt in range(1, 4):
                if flow.looks_logged_in(page):
                    logged = True
                    break
                print(f"  login check miss {attempt}/3 — retrying…", flush=True)
                page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
                page.wait_for_timeout(2500)
                flow.dismiss_banners(page)
            if not logged:
                raise SystemExit(
                    "STOP: Flow not logged in. "
                    "Re-auth: python3 04_Audio/tools/orbit_flow_veo_ui.py --login"
                )

            tmp = REJECT / "10_rock_not_fire_v13_new.mp4"
            if tmp.exists():
                tmp.unlink()

            info: dict
            print("\n=== I2V 10_rock_not_fire (colourless shimmer) ===", flush=True)
            try:
                info = flow.generate_clip(
                    page,
                    I2V_PROMPT,
                    tmp,
                    model=MODEL,
                    start_frame=START,
                    scenery_only=False,
                    reuse_project=False,
                    attempts=2,
                    timeout_s=700,
                )
            except Exception as i2v_err:
                print(f"  I2V failed: {i2v_err}", flush=True)
                print("\n=== FALLBACK T2V scenery (colourless shimmer lock) ===", flush=True)
                if tmp.exists():
                    tmp.unlink()
                info = flow.generate_clip(
                    page,
                    T2V_PROMPT,
                    tmp,
                    model=MODEL,
                    start_frame=None,
                    scenery_only=True,
                    reuse_project=False,
                    attempts=2,
                    timeout_s=700,
                )
                info = {**info, "fallback": "t2v-scenery-after-i2v-fail"}

            veo.strip_audio(tmp)
            if not tmp.exists() or tmp.stat().st_size < 400_000:
                raise SystemExit("STOP: plate10 download missing/small")
            if DEST.exists():
                prev = REJECT / "10_rock_not_fire_v01_prev_from_v12.mp4"
                if prev.exists():
                    prev.unlink()
                shutil.move(str(DEST), str(prev))
                print(f"  archived previous → {prev.name}", flush=True)
            shutil.move(str(tmp), str(DEST))
            meta["plates"].append(
                {
                    "id": "10_rock_not_fire",
                    "status": "ok",
                    "out": str(DEST),
                    "bytes": DEST.stat().st_size,
                    **info,
                }
            )
            META.write_text(json.dumps(meta, indent=2) + "\n")
            print(f"SAVED {DEST} bytes={DEST.stat().st_size}", flush=True)
            print(f"info={info}", flush=True)
        finally:
            ctx.close()
    print("OK plate10 v13 remint finished", flush=True)


if __name__ == "__main__":
    main()
