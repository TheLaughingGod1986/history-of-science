#!/usr/bin/env python3
"""Part 01 Flow Veo 3.1 Fast T2V — all ten plates. No Gemini stills.

scenery_only. Explorer plate is T2V with identity in the prompt (do not I2V
the full character sheet). If Create dies: STOP. Do not start Part 02.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-01_plates_v01.json"
RAW = PROJ / "04_Generated-Clips/part01/raw/v01_fast"
META = PROJ / "07_Edit-Project/part01_gen_meta_v01.json"
MODEL = "Veo 3.1 - Fast"
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
STYLE = (
    "History of Science locked look: premium Animistry-class 3D cartoon, warm "
    "cinematic light, period science world. Not photoreal. Not live-action. "
    "Not a modern lab. Silent picture. No readable text, logos, or UI. "
    "No Orbit orange robot. No cute atom faces. Continuous motion the whole clip."
)


def dest_for(plate_id: str) -> Path:
    return RAW / f"{plate_id}_v01.mp4"


def main() -> None:
    plates = json.loads(PLATES_JSON.read_text())["plates"]
    RAW.mkdir(parents=True, exist_ok=True)
    meta: dict = {"engine": "flow-ui", "model": MODEL, "raw": str(RAW), "plates": []}
    if META.exists():
        try:
            meta = json.loads(META.read_text())
        except Exception:
            pass
    profile = flow.profile_path(PROFILE)
    print(f"Flow profile={profile} model={MODEL} plates={len(plates)}", flush=True)
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2000)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit("STOP: Flow not logged in. Do not loop.")
            for i, plate in enumerate(plates):
                dest = dest_for(plate["id"])
                if veo.already_done(dest, min_bytes=400_000):
                    print(f"  skip {dest.name}", flush=True)
                    continue
                prompt = f"{STYLE} {plate['prompt']}"
                print(f"\n=== Fast T2V {plate['id']} ({i+1}/{len(plates)}) ===", flush=True)
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
                    raise SystemExit(
                        f"STOP: Flow failed on {plate['id']}: {e}"
                    ) from e
                veo.strip_audio(dest)
                if not dest.exists() or dest.stat().st_size < 400_000:
                    raise SystemExit(f"STOP: download missing/small {dest}")
                meta.setdefault("plates", []).append({"id": plate["id"], **info})
                META.write_text(json.dumps(meta, indent=2))
                print(f"  SAVED {dest.name} bytes={dest.stat().st_size}", flush=True)
        finally:
            ctx.close()
    print("OK part 01 T2V mint finished", flush=True)


if __name__ == "__main__":
    main()
