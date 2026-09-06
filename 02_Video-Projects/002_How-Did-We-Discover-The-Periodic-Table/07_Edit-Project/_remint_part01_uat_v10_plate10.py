#!/usr/bin/env python3
"""Remint plate 10 only — Ben UAT still shows clear flask + fire-looking haze.

Target:
  LEFT: dark ore on cold grate, heat shimmer ONLY (no flames)
  RIGHT: ore FLAT INSIDE hanging brass pan (pan depressed)
  ZERO clear glass flasks on the table
  Opaque ceramic / metal jars on shelves only
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips/part01/raw/v01_fast"
REJECT = PROJ / "04_Generated-Clips/part01/_rejected_uat_v10_plate10"
META = PROJ / "07_Edit-Project/part01_remint_uat_v10_plate10_meta.json"
PID = "10_rock_not_fire"
MODEL = "Veo 3.1 - Fast"
PROFILE = Path(
    os.environ.get("ORBIT_FLOW_PROFILE", str(Path.home() / ".playwright-hos-flow-profile"))
)

PROMPT = (
    "History of Science locked look: premium Animistry-class 3D cartoon like Germs Part 01 — "
    "warm wood workshop, cinematic light. Not photoreal. Silent. No readable text. No Orbit. "
    "No modern news. No food. Continuous gentle camera drift. "
    "ONE continuous wide shot of a period chemistry workshop (no split-screen). "
    "LEFT: a dark rough ore chunk sits on a COLD metal grate. Only a subtle colourless heat "
    "shimmer / air haze rises — NO flames, NO fire, NO orange coals, NO burning, NO fire plumes, "
    "NO orange wisps. "
    "RIGHT: a classic brass balance scale. The LEFT hanging pan holds a heavy dark ore chunk "
    "sitting FLAT INSIDE the pan metal — ore rests on the pan floor, pan clearly depressed, "
    "chains taut to the pan rim only. The RIGHT pan is empty. "
    "Table surface around the scale is EMPTY of glassware — ZERO clear glass flasks, ZERO bottles, "
    "ZERO liquid in glass, ZERO hanging vessels. "
    "Background shelves: OPAQUE ceramic jars and sealed metal canisters ONLY. "
    "HARD REJECT: any clear glass flask or bottle beside the scale, liquid in glass, flames, fire, "
    "floating ore above the pan, hanging pots, split-screen, text, Orbit, news, food."
)


def probe_dur(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=nw=1:nk=1",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def archive_after_success(new_path: Path) -> None:
    prev = RAW / f"{PID}_v01.mp4"
    if prev.exists() and prev.resolve() != new_path.resolve():
        REJECT.mkdir(parents=True, exist_ok=True)
        dest = REJECT / f"{PID}_v01_prev.mp4"
        if dest.exists():
            dest.unlink()
        shutil.move(str(prev), str(dest))
        print(f"  archived previous → {dest.name}", flush=True)
    final = RAW / f"{PID}_v01.mp4"
    if new_path.resolve() != final.resolve():
        if final.exists():
            final.unlink()
        shutil.move(str(new_path), str(final))


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    REJECT.mkdir(parents=True, exist_ok=True)
    meta: dict = {"engine": "flow-ui", "model": MODEL, "mode": "uat-v10-plate10", "plates": []}
    profile = flow.profile_path(PROFILE)
    print(f"Flow remint plate10 profile={profile}", flush=True)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2000)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                # Flow host moved; dump URL for debug then soft-continue if New project visible
                print(f"WARN looks_logged_in=False url={page.url}", flush=True)
                try:
                    body = page.locator("body").inner_text(timeout=5000)[:1500].lower()
                except Exception:
                    body = ""
                if "new project" not in body and "/project/" not in (page.url or "").lower():
                    raise SystemExit("STOP: Flow not logged in.")
                print("  continuing — New project visible on flow.google.com", flush=True)

            ok = False
            last_err: Exception | None = None
            for attempt in range(1, 5):
                tmp = RAW / f"{PID}_v01_tmp.mp4"
                if tmp.exists():
                    tmp.unlink()
                print(f"\n=== T2V {PID} attempt {attempt} ===", flush=True)
                try:
                    info = flow.generate_clip(
                        page,
                        PROMPT,
                        tmp,
                        model=MODEL,
                        reuse_project=False,
                        attempts=1,
                        timeout_s=420,
                        start_frame=None,
                        scenery_only=True,
                    )
                    veo.strip_audio(tmp)
                    dur = probe_dur(tmp)
                    size = tmp.stat().st_size
                    print(f"  dur={dur:.2f}s bytes={size}", flush=True)
                    if size < 800_000 or dur < 5.5 or dur > 12.0:
                        bad = REJECT / f"{PID}_contam_attempt{attempt}.mp4"
                        if bad.exists():
                            bad.unlink()
                        shutil.move(str(tmp), str(bad))
                        print("  REJECT duration/size", flush=True)
                        continue
                    archive_after_success(tmp)
                    dest = RAW / f"{PID}_v01.mp4"
                    meta["plates"].append({"id": PID, "mode": "t2v", "duration": dur, **info})
                    META.write_text(json.dumps(meta, indent=2) + "\n")
                    print(f"  SAVED {dest.name} bytes={dest.stat().st_size}", flush=True)
                    ok = True
                    break
                except Exception as e:  # noqa: BLE001
                    last_err = e
                    print(f"  error: {e}", flush=True)
            if not ok:
                raise SystemExit(f"STOP: failed {PID}: {last_err}")
        finally:
            ctx.close()
    print("OK plate10 remint finished", flush=True)


if __name__ == "__main__":
    main()
