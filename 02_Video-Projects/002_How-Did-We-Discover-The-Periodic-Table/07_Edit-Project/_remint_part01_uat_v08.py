#!/usr/bin/env python3
"""UAT v08 remint — Ben physics + Explorer identity fails.

Fails to fix:
  05 Explorer — match Germs younger-boy face; ore+gas beat; no satchel rummage / glowing chair
  06 Pour — stream enters flask mouth (not the rim/side)
  02/07/08 — no bubbles floating in air above liquid
  10 — flask fully seated on scale pan (not floating)
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
REJECT = PROJ / "04_Generated-Clips/part01/_rejected_uat_v08"
META = PROJ / "07_Edit-Project/part01_remint_uat_v08_meta.json"
START_05 = PROJ / "04_Generated-Clips/part01/refs/v01_stills/05_explorer_ore_gas_start_v08.jpg"
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
    "PHYSICS LOCK: liquids obey gravity. Bubbles exist ONLY inside liquid BELOW the "
    "meniscus. Empty air inside flask necks is clear — NEVER spheres floating in air. "
    "Glassware rests on stands/pans/tables with visible contact — NEVER floating with a gap. "
    "Poured streams enter the OPEN mouth of the receiving vessel — NEVER miss onto the rim."
)
JOBS = (
    ("05_explorer_ore_gas", "i2v", START_05),
    ("06_alchemist_accidents", "t2v", None),
    ("02_workshop_jars", "t2v", None),
    ("07_shelf_names_grow", "t2v", None),
    ("08_labelled_zoo", "t2v", None),
    ("10_rock_not_fire", "t2v", None),
)


def archive(pid: str) -> None:
    src = RAW / f"{pid}_v01.mp4"
    if not src.exists():
        return
    REJECT.mkdir(parents=True, exist_ok=True)
    dest = REJECT / f"{pid}_v01.mp4"
    if dest.exists():
        dest.unlink()
    shutil.move(str(src), str(dest))
    print(f"  archived {dest.name}", flush=True)


def main() -> None:
    plates = {p["id"]: p for p in json.loads(PLATES_JSON.read_text())["plates"]}
    if not START_05.exists() or START_05.stat().st_size < 40_000:
        raise SystemExit(f"STOP: missing Explorer start {START_05}")
    RAW.mkdir(parents=True, exist_ok=True)
    meta: dict = {"engine": "flow-ui", "model": MODEL, "mode": "uat-v08", "plates": []}
    profile = flow.profile_path(PROFILE)
    print(f"Flow UAT v08 profile={profile}", flush=True)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2000)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit("STOP: Flow not logged in.")

            for pid, mode, start in JOBS:
                if pid not in plates:
                    raise SystemExit(f"missing plate {pid}")
                archive(pid)
                dest = RAW / f"{pid}_v01.mp4"
                if dest.exists():
                    dest.unlink()
                prompt = f"{STYLE} {PHYSICS} {plates[pid]['prompt']}"
                print(f"\n=== {mode.upper()} {pid} ===", flush=True)
                kwargs = dict(
                    model=MODEL,
                    reuse_project=False,
                    attempts=1,
                    timeout_s=700,
                )
                if mode == "i2v":
                    kwargs["start_frame"] = start
                else:
                    kwargs["start_frame"] = None
                    kwargs["scenery_only"] = True
                info = flow.generate_clip(page, prompt, dest, **kwargs)
                veo.strip_audio(dest)
                if not dest.exists() or dest.stat().st_size < 400_000:
                    raise SystemExit(f"STOP: missing/small {dest}")
                meta["plates"].append({"id": pid, "mode": mode, **info})
                META.write_text(json.dumps(meta, indent=2) + "\n")
                print(f"  SAVED {dest.name} bytes={dest.stat().st_size}", flush=True)
        finally:
            ctx.close()
    print("OK UAT v08 remint finished", flush=True)


if __name__ == "__main__":
    main()
