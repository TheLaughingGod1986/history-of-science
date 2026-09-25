#!/usr/bin/env python3
"""Part 01 plate 10 remint v14 — Flow T2V with network mp4 capture.

I2V Add-to-Prompt is flaky; T2V scenery + network intercept is more reliable
when Flow credits are available (Ben topped up).
"""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips/part01/raw/v01_fast"
REJECT = PROJ / "04_Generated-Clips/part01/_rejected_uat_v14_plate10"
DEST = RAW / "10_rock_not_fire_v01.mp4"
META = PROJ / "07_Edit-Project/part01_remint_plate10_v14_meta.json"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL", "Veo 3.1 - Lite")
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
TIMEOUT_S = int(os.environ.get("ORBIT_FLOW_TIMEOUT_S", "900"))

PROMPT = (
    "TEXT-TO-VIDEO scenery only (no character reference). "
    "History of Science locked look: premium Animistry-class 3D cartoon workshop, "
    "warm cinematic light. Not photoreal. Silent. No readable text. No Orbit robot. "
    "Continuous gentle camera drift the whole clip — never a still freeze, never Ken Burns. "
    "ONE continuous wide shot of a Victorian chemistry workshop bench. "
    "LEFT: dark rough ore chunk resting on a COLD metal grate. ONLY a subtle colourless heat "
    "shimmer / air refraction haze rises through the grate — NO orange, NO red, NO yellow glow, "
    "NO embers, NO coals, NO flames, NO fire, NO burning. Under the grate: dark cool metal shadow "
    "with colourless shimmer only. "
    "CRITICAL: NO blue rectangle, NO cyan scrub, NO selection mask, NO UI overlay, NO blue tint "
    "box around the ore or grate — clean natural rendered pixels only. "
    "RIGHT: classic brass balance scale. LEFT hanging pan holds heavy dark ore sitting FLAT "
    "INSIDE the pan metal — ore on the pan floor, pan clearly depressed, chains taut. RIGHT pan empty. "
    "Table around the scale EMPTY of glassware — ZERO clear glass flasks beside the scale. "
    "Background shelves: OPAQUE ceramic jars and sealed metal canisters only; no clear glass flasks "
    "in the foreground. "
    "HARD REJECT: blue/cyan mask around ore, orange/red fire or ember glow under the grate, "
    "clear flask beside the scale, floating ore, hanging pots, split-screen, text, Orbit, Ken Burns."
)


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    REJECT.mkdir(parents=True, exist_ok=True)
    profile = flow.profile_path(PROFILE)
    print(f"Flow T2V plate10 v14 model={MODEL} profile={profile}", flush=True)

    from playwright.sync_api import sync_playwright

    captured: list[tuple[str, bytes]] = []

    def on_response(resp) -> None:
        try:
            url = resp.url or ""
            ct = (resp.headers or {}).get("content-type", "")
            if resp.status != 200:
                return
            if "video" in ct or url.endswith(".mp4") or "videoplayback" in url or "/video/" in url:
                body = resp.body()
                if body and len(body) > 400_000:
                    captured.append((url, body))
                    print(f"  net-capture {len(body)}b ct={ct} url={url[:100]}", flush=True)
        except Exception:
            pass

    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        page.on("response", on_response)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2500)
            for _ in range(3):
                flow.dismiss_banners(page)
                page.wait_for_timeout(500)
            if not flow.looks_logged_in(page):
                raise SystemExit("STOP: Flow not logged in — run orbit_flow_veo_ui.py --login")

            body = (page.locator("body").inner_text(timeout=8000) or "").lower()
            if "out of google flow credits" in body or "you're out of google flow credits" in body:
                shot = REJECT / "flow_no_credits_v14b.png"
                page.screenshot(path=str(shot), full_page=True)
                raise SystemExit(f"STOP: Flow out of credits. {shot}")

            tmp = REJECT / "10_rock_not_fire_v14_t2v.mp4"
            if tmp.exists():
                tmp.unlink()

            print("\n=== T2V scenery (network capture) ===", flush=True)
            info = flow.generate_clip(
                page,
                PROMPT,
                tmp,
                model=MODEL,
                start_frame=None,
                scenery_only=True,
                reuse_project=False,
                attempts=2,
                timeout_s=TIMEOUT_S,
            )
            print(f"generate_clip ok info={info}", flush=True)

            if (not tmp.exists() or tmp.stat().st_size < 400_000) and captured:
                url, body = max(captured, key=lambda x: len(x[1]))
                tmp.write_bytes(body)
                print(f"  wrote from network capture {tmp} bytes={len(body)}", flush=True)
                info = {**(info or {}), "network_capture": url[:200]}

            if not tmp.exists() or tmp.stat().st_size < 400_000:
                # last chance: click any download in page
                shot = REJECT / "flow_stall_v14b.png"
                page.screenshot(path=str(shot), full_page=True)
                raise SystemExit(f"STOP: no usable mp4. screenshot={shot} captures={len(captured)}")

            veo.strip_audio(tmp)
            if DEST.exists():
                prev = REJECT / "10_rock_not_fire_v01_prev_before_v14b.mp4"
                if prev.exists():
                    prev.unlink()
                shutil.move(str(DEST), str(prev))
            shutil.move(str(tmp), str(DEST))
            meta = {
                "engine": "flow-ui-t2v-network",
                "model": MODEL,
                "out": str(DEST),
                "bytes": DEST.stat().st_size,
                "info": info,
                "captures": len(captured),
                "updated": time.strftime("%Y-%m-%dT%H:%M:%S"),
            }
            META.write_text(json.dumps(meta, indent=2) + "\n")
            print(f"SAVED {DEST} bytes={DEST.stat().st_size}", flush=True)
        finally:
            ctx.close()
    print("OK plate10 v14b Flow T2V finished", flush=True)


if __name__ == "__main__":
    main()
