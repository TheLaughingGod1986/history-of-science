#!/usr/bin/env python3
"""UAT remint: glassware liquids + Explorer identity from Germs 001."""
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
REJECT = PROJ / "04_Generated-Clips/part01/_rejected_uat_v06"
META = PROJ / "07_Edit-Project/part01_remint_uat_v06_meta.json"
EXPLORER_STILL = PROJ / "04_Generated-Clips/part01/refs/explorer_germs_part01_lock.jpg"
MODEL = "Veo 3.1 - Fast"
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
JAR_IDS = (
    "02_workshop_jars",
    "07_shelf_names_grow",
    "08_labelled_zoo",
    "11_chemists_more_names",
    "12_workshop_hold",
)
STYLE = (
    "History of Science locked look: premium Animistry-class 3D cartoon like Germs "
    "Part 01 — smooth feature-animation motion, warm wood, cinematic light. "
    "Not photoreal. Not clay. Not steampunk gear walls. Silent picture. "
    "No readable text. No Orbit orange robot. Continuous motion the whole clip."
)
GLASS = (
    "GLASSWARE LOCK: every flask, jar, vial, and bottle is filled with CLEAR "
    "COLORED LIQUID only (amber, teal, gold, ruby, or clear) with a smooth "
    "meniscus and a slight slosh. Ores and rocks sit on wood, never inside glass. "
    "FORBIDDEN: powder stuffing, cotton stuffing, granular solids in jars, moss "
    "in jars, crystal chunks packed in glass, glowing energy orbs."
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
    if not EXPLORER_STILL.exists():
        raise SystemExit(f"STOP: missing Explorer lock still {EXPLORER_STILL}")
    plates = {p["id"]: p for p in json.loads(PLATES_JSON.read_text())["plates"]}
    RAW.mkdir(parents=True, exist_ok=True)
    meta: dict = {"engine": "flow-ui", "model": MODEL, "mode": "uat-v06", "plates": []}
    profile = flow.profile_path(PROFILE)
    print(f"Flow UAT v06 profile={profile}", flush=True)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2000)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit("STOP: Flow not logged in.")

            # Explorer first — identity from Germs Part 01 still
            pid = "05_explorer_ore_gas"
            archive(pid)
            dest = RAW / f"{pid}_v01.mp4"
            if dest.exists():
                dest.unlink()
            prompt = f"{STYLE} {GLASS} {plates[pid]['prompt']}"
            print(f"\n=== I2V Explorer {pid} ===", flush=True)
            info = flow.generate_clip(
                page,
                prompt,
                dest,
                model=MODEL,
                start_frame=EXPLORER_STILL,
                reuse_project=False,
                attempts=1,
                timeout_s=700,
            )
            veo.strip_audio(dest)
            meta["plates"].append({"id": pid, **info})
            META.write_text(json.dumps(meta, indent=2))
            print(f"  SAVED {dest.name} bytes={dest.stat().st_size}", flush=True)

            for pid in JAR_IDS:
                archive(pid)
                dest = RAW / f"{pid}_v01.mp4"
                if dest.exists():
                    dest.unlink()
                prompt = f"{STYLE} {GLASS} {plates[pid]['prompt']}"
                print(f"\n=== T2V glassware {pid} ===", flush=True)
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
                    raise SystemExit(f"STOP: missing/small {dest}")
                meta["plates"].append({"id": pid, **info})
                META.write_text(json.dumps(meta, indent=2))
                print(f"  SAVED {dest.name} bytes={dest.stat().st_size}", flush=True)
        finally:
            ctx.close()
    print("OK UAT v06 remint finished", flush=True)


if __name__ == "__main__":
    main()
