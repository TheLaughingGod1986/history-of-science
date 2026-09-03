#!/usr/bin/env python3
"""Resume UAT v08 remint for unfinished / failed plates.

Keeps Explorer 05 (already reminted). Re-does 06 (bubbles still in air)
plus 02 / 07 / 08 / 10. Archives only AFTER a successful download so a
Flow timeout cannot leave RAW empty.
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
    "PHYSICS LOCK HARD: liquids are STILL clear colored fluid with a flat meniscus. "
    "ZERO bubbles, ZERO foam, ZERO sparkles, ZERO spheres in liquid OR in empty air "
    "inside flask necks. Glassware rests with visible contact on stands/pans/tables — "
    "NEVER floating with a gap. Poured streams enter the OPEN mouth of the receiving "
    "vessel and land INSIDE — NEVER miss onto the rim, outer glass, or table."
)
# Skip 05 — already reminted and looking on-model younger Explorer.
JOBS = (
    ("06_alchemist_accidents", "t2v", None),
    ("02_workshop_jars", "t2v", None),
    ("07_shelf_names_grow", "t2v", None),
    ("08_labelled_zoo", "t2v", None),
    ("10_rock_not_fire", "t2v", None),
)


def archive_after_success(pid: str, new_path: Path) -> None:
    """Move previous RAW (if any) into reject only after new clip exists."""
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
    if META.exists():
        meta = json.loads(META.read_text())
    else:
        meta = {"engine": "flow-ui", "model": MODEL, "mode": "uat-v08-resume", "plates": []}
    meta["mode"] = "uat-v08-resume"
    profile = flow.profile_path(PROFILE)
    print(f"Flow UAT v08 resume profile={profile}", flush=True)

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
                tmp = RAW / f"{pid}_v01_tmp.mp4"
                if tmp.exists():
                    tmp.unlink()
                prompt = f"{STYLE} {PHYSICS} {plates[pid]['prompt']}"
                print(f"\n=== {mode.upper()} {pid} ===", flush=True)
                kwargs = dict(
                    model=MODEL,
                    reuse_project=False,
                    attempts=2,
                    timeout_s=480,
                )
                if mode == "i2v":
                    kwargs["start_frame"] = start
                else:
                    kwargs["start_frame"] = None
                    kwargs["scenery_only"] = True
                info = flow.generate_clip(page, prompt, tmp, **kwargs)
                veo.strip_audio(tmp)
                if not tmp.exists() or tmp.stat().st_size < 400_000:
                    raise SystemExit(f"STOP: missing/small {tmp}")
                archive_after_success(pid, tmp)
                dest = RAW / f"{pid}_v01.mp4"
                meta["plates"] = [x for x in meta.get("plates", []) if x.get("id") != pid]
                meta["plates"].append({"id": pid, "mode": mode, **info})
                META.write_text(json.dumps(meta, indent=2) + "\n")
                print(f"  SAVED {dest.name} bytes={dest.stat().st_size}", flush=True)
        finally:
            ctx.close()
    print("OK UAT v08 resume finished", flush=True)


if __name__ == "__main__":
    main()
