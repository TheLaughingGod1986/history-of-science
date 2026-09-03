#!/usr/bin/env python3
"""UAT v08b remint — redesign beats that keep failing physics.

Avoid Veo failure modes:
  06 — no pour stream (flare blooms inside seated flask)
  02/07/08 — corked flat-bottom bottles (no open-neck air bubbles)
  10 — corked flat bottle seated in pan + rock heat shimmer (no fire)

Skip 05 (Explorer already on-model).
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
REJECT = PROJ / "04_Generated-Clips/part01/_rejected_uat_v08b"
META = PROJ / "07_Edit-Project/part01_remint_uat_v08b_meta.json"
MODEL = "Veo 3.1 - Fast"
PROFILE = Path(
    os.environ.get("ORBIT_FLOW_PROFILE", str(Path.home() / ".playwright-hos-flow-profile"))
)
STYLE = (
    "History of Science locked look: premium Animistry-class 3D cartoon like Germs "
    "Part 01 — smooth feature-animation motion, warm wood, cinematic light. "
    "Not photoreal. Silent picture. No readable text. No Orbit orange robot. "
    "Continuous motion the whole clip."
)
PHYSICS = (
    "PHYSICS LOCK: prefer CORKED flat-bottom bottles seated on wood or pans. "
    "NO pouring streams. NO open-neck bubbles. NO floating glassware. "
    "Liquids are STILL with flat meniscus — ZERO bubbles or sparkles."
)
JOBS = (
    "06_alchemist_accidents",
    "02_workshop_jars",
    "07_shelf_names_grow",
    "08_labelled_zoo",
    "10_rock_not_fire",
)


def archive_after_success(pid: str, new_path: Path) -> None:
    prev = RAW / f"{pid}_v01.mp4"
    if prev.exists() and prev.resolve() != new_path.resolve():
        REJECT.mkdir(parents=True, exist_ok=True)
        dest = REJECT / f"{pid}_v01.mp4"
        if dest.exists():
            dest.unlink()
        shutil.move(str(prev), str(dest))
        print(f"  archived previous {dest.name}", flush=True)
    if new_path.resolve() != prev.resolve():
        if prev.exists():
            prev.unlink()
        shutil.move(str(new_path), str(prev))


def main() -> None:
    plates = {p["id"]: p for p in json.loads(PLATES_JSON.read_text())["plates"]}
    RAW.mkdir(parents=True, exist_ok=True)
    meta: dict = {"engine": "flow-ui", "model": MODEL, "mode": "uat-v08b", "plates": []}
    profile = flow.profile_path(PROFILE)
    print(f"Flow UAT v08b profile={profile}", flush=True)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2000)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit("STOP: Flow not logged in.")

            for pid in JOBS:
                if pid not in plates:
                    raise SystemExit(f"missing plate {pid}")
                tmp = RAW / f"{pid}_v01_tmp.mp4"
                if tmp.exists():
                    tmp.unlink()
                prompt = f"{STYLE} {PHYSICS} {plates[pid]['prompt']}"
                print(f"\n=== T2V {pid} ===", flush=True)
                info = flow.generate_clip(
                    page,
                    prompt,
                    tmp,
                    model=MODEL,
                    reuse_project=False,
                    attempts=2,
                    timeout_s=420,
                    start_frame=None,
                    scenery_only=True,
                )
                veo.strip_audio(tmp)
                # Guard against wrong-media contamination (e.g. food clips)
                if tmp.stat().st_size < 800_000:
                    raise SystemExit(f"STOP: suspect tiny download {tmp} bytes={tmp.stat().st_size}")
                archive_after_success(pid, tmp)
                dest = RAW / f"{pid}_v01.mp4"
                meta["plates"].append({"id": pid, "mode": "t2v", **info})
                META.write_text(json.dumps(meta, indent=2) + "\n")
                print(f"  SAVED {dest.name} bytes={dest.stat().st_size}", flush=True)
        finally:
            ctx.close()
    print("OK UAT v08b remint finished", flush=True)


if __name__ == "__main__":
    main()
