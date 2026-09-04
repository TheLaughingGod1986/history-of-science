#!/usr/bin/env python3
"""Part 03 Flow Veo 3.1 Fast — all real motion plates. No Ken Burns.

CoS gate (Part 01 v11 + Part 02 v06): real Veo every beat, side labels in assemble,
Explorer once, no center stamps. Do not remint 01/02. Do not ping Ben.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-03_plates_v01.json"
RAW = PROJ / "04_Generated-Clips/part03/raw/v01_fast"
META = PROJ / "07_Edit-Project/part03_mint_flow_v01_meta.json"
EXPLORER_LOCK = PROJ / "04_Generated-Clips/part01/refs/explorer_germs_part01_lock.jpg"
EXPLORER_START = PROJ / "04_Generated-Clips/part03/refs/v01_stills/05_explorer_ruler_start.jpg"
MODEL = "Veo 3.1 - Fast"
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
STYLE = (
    "History of Science locked look: premium Animistry-class 3D cartoon, warm "
    "cinematic light, 1860 Karlsruhe congress-hall continuity. Not photoreal. "
    "Not live-action. Silent picture. No readable text, logos, or UI. "
    "No Orbit orange robot. Continuous real camera and object motion the whole clip. "
    "Never a still photo with Ken Burns. Never a dead-center full-screen title stamp."
)


def dest_for(plate_id: str) -> Path:
    return RAW / f"{plate_id}_v01.mp4"


def ensure_explorer_start() -> Path | None:
    if EXPLORER_START.exists() and EXPLORER_START.stat().st_size > 40_000:
        return EXPLORER_START
    if not EXPLORER_LOCK.exists():
        print(f"WARN missing explorer lock {EXPLORER_LOCK}", flush=True)
        return None
    EXPLORER_START.parent.mkdir(parents=True, exist_ok=True)
    bed = EXPLORER_START.with_name("_hall_bed.png")
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "lavfi", "-i", "color=c=0xC4A574:s=1920x1080:d=1",
            "-frames:v", "1", str(bed),
        ],
        check=True,
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(bed), "-i", str(EXPLORER_LOCK),
            "-filter_complex",
            "[1:v]scale=720:-1[ch];[0:v][ch]overlay=(W-w)/2:(H-h)/2+80",
            "-frames:v", "1", str(EXPLORER_START),
        ],
        check=True,
    )
    bed.unlink(missing_ok=True)
    return EXPLORER_START if EXPLORER_START.exists() else EXPLORER_LOCK


def pick_google_account(page) -> None:
    """If Flow bounced to the account chooser, pick the Ultra account."""
    url = page.url or ""
    if "accounts.google.com" not in url:
        return
    for needle in ("benoats@googlemail.com", "benoats86@gmail.com"):
        loc = page.get_by_text(needle, exact=False)
        if loc.count():
            print(f"  account chooser → {needle}", flush=True)
            loc.first.click(timeout=8000)
            page.wait_for_timeout(7000)
            return


def main() -> None:
    only = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    plates = json.loads(PLATES_JSON.read_text())["plates"]
    RAW.mkdir(parents=True, exist_ok=True)
    meta: dict = {"engine": "flow-ui", "model": MODEL, "raw": str(RAW), "plates": []}
    if META.exists():
        try:
            meta = json.loads(META.read_text())
        except Exception:
            pass
    by_id = {p["id"]: p for p in meta.get("plates", []) if "id" in p}
    explorer_start = ensure_explorer_start()
    profile = flow.profile_path(PROFILE)
    print(f"Flow profile={profile} model={MODEL} plates={len(plates)}", flush=True)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2500)
            pick_google_account(page)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit(
                    "STOP: Flow not logged in. Do not Ken-Burns. "
                    "Re-auth with: python3 04_Audio/tools/orbit_flow_veo_ui.py --login"
                )
            for i, plate in enumerate(plates):
                pid = plate["id"]
                if only and pid not in only and not any(pid.startswith(x) for x in only):
                    continue
                dest = dest_for(pid)
                if veo.already_done(dest, min_bytes=400_000):
                    print(f"  skip {dest.name}", flush=True)
                    by_id[pid] = {"id": pid, "status": "exists", "out": str(dest)}
                    continue
                prompt = f"{STYLE} {plate['prompt']}"
                start = explorer_start if plate.get("explorer") else None
                kind = "I2V" if start else "T2V"
                print(f"\n=== Fast {kind} {pid} ({i+1}/{len(plates)}) ===", flush=True)
                try:
                    info = flow.generate_clip(
                        page,
                        prompt,
                        dest,
                        model=MODEL,
                        start_frame=start,
                        scenery_only=(start is None),
                        reuse_project=False,
                        attempts=1,
                        timeout_s=700,
                    )
                except Exception as e:
                    by_id[pid] = {"id": pid, "status": "fail", "error": str(e)[:500]}
                    meta["plates"] = list(by_id.values())
                    META.write_text(json.dumps(meta, indent=2))
                    raise SystemExit(f"STOP: Flow failed on {pid}: {e}") from e
                veo.strip_audio(dest)
                if not dest.exists() or dest.stat().st_size < 400_000:
                    raise SystemExit(f"STOP: download missing/small {dest}")
                by_id[pid] = {"id": pid, "status": "ok", "out": str(dest), **info}
                meta["plates"] = list(by_id.values())
                META.write_text(json.dumps(meta, indent=2))
                print(f"  SAVED {dest.name} bytes={dest.stat().st_size}", flush=True)
        finally:
            ctx.close()

    ok = sum(1 for p in by_id.values() if p.get("status") in {"ok", "exists"})
    want = len(only) if only else len(plates)
    print(f"OK part 03 Flow mint finished ok={ok} want={want}", flush=True)
    if ok < want:
        sys.exit(2)


if __name__ == "__main__":
    main()
