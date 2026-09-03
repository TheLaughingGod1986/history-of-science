#!/usr/bin/env python3
"""Remint Part 01 UAT fails: 01 open text, 05 Explorer, 09 seating.

No Gemini key in this session — all three are Flow Veo 3.1 Fast T2V with
hardened prompts. Explorer identity is locked in the prompt text (sheet
I2V parks hero). Archives rejected v01. STOP on Create failure.
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
REJECT = PROJ / "04_Generated-Clips/part01/_rejected_uat_v01"
META = PROJ / "07_Edit-Project/part01_remint_uat_v02_meta.json"
MODEL = "Veo 3.1 - Fast"
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
REMINT_IDS = ("01_empty_chairs_open", "05_explorer_ore_gas", "09_seating_plan_gap")
STYLE = (
    "History of Science locked look: premium Animistry-class 3D cartoon, warm "
    "cinematic light, period science world. Not photoreal. Not live-action. "
    "Not a modern lab. Silent picture. No readable text, logos, or UI. "
    "No Orbit orange robot. No cute atom faces. Continuous motion the whole clip."
)
EXPLORER_LOCK = (
    "CRITICAL Explorer identity lock (exactly one boy): messy wavy brown hair "
    "(not neat/slick), large expressive eyes, round thin gold wire-rim glasses, "
    "teal-blue long overcoat with small gold atom lapel pin, tan waistcoat, "
    "plain white shirt (never striped), dark brown floppy bow tie, brown trousers "
    "rolled at cuffs, cream socks, sturdy brown lace-up boots, brown leather "
    "satchel with brass compass on the strap. Feature-animation 3D cartoon polish."
)
EXPLORER_NEG = (
    "Forbidden: striped shirt, neat slick haircut, adult redesign, no glasses, "
    "wrong coat colour, missing bow tie, missing satchel, twin Explorers, "
    "Orbit orange robot, smiley faces on rocks, eyes on ores, cute mascot rocks, "
    "readable text, chalkboard writing."
)


def archive_old(plate_id: str) -> None:
    src = RAW / f"{plate_id}_v01.mp4"
    if not src.exists():
        return
    REJECT.mkdir(parents=True, exist_ok=True)
    dest = REJECT / f"{plate_id}_v01.mp4"
    if dest.exists():
        dest.unlink()
    shutil.move(str(src), str(dest))
    print(f"  archived {dest.name}", flush=True)


def main() -> None:
    plates = {p["id"]: p for p in json.loads(PLATES_JSON.read_text())["plates"]}
    for pid in REMINT_IDS:
        if pid not in plates:
            raise SystemExit(f"missing plate {pid}")

    RAW.mkdir(parents=True, exist_ok=True)
    meta: dict = {
        "engine": "flow-ui",
        "model": MODEL,
        "remint": list(REMINT_IDS),
        "mode": "t2v-hardened",
        "plates": [],
    }
    profile = flow.profile_path(PROFILE)
    print(f"Flow remint UAT v02 profile={profile} ids={REMINT_IDS}", flush=True)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2000)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit("STOP: Flow not logged in. Do not loop.")

            for pid in REMINT_IDS:
                archive_old(pid)
                plate = plates[pid]
                dest = RAW / f"{pid}_v01.mp4"
                # Always remint these UAT fails — do not skip-existing
                if dest.exists():
                    dest.unlink()
                if pid == "05_explorer_ore_gas":
                    prompt = f"{STYLE} {EXPLORER_LOCK} {plate['prompt']} {EXPLORER_NEG}"
                else:
                    prompt = f"{STYLE} {plate['prompt']}"
                print(f"\n=== remint T2V {pid} ===", flush=True)
                try:
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
                except Exception as e:
                    META.write_text(json.dumps(meta, indent=2))
                    raise SystemExit(f"STOP: Flow failed on {pid}: {e}") from e
                veo.strip_audio(dest)
                if not dest.exists() or dest.stat().st_size < 400_000:
                    raise SystemExit(f"STOP: download missing/small {dest}")
                meta["plates"].append({"id": pid, **info})
                META.write_text(json.dumps(meta, indent=2))
                print(f"  SAVED {dest.name} bytes={dest.stat().st_size}", flush=True)
        finally:
            ctx.close()
    print("OK part 01 UAT remint v02 finished", flush=True)


if __name__ == "__main__":
    main()
