#!/usr/bin/env python3
"""Part 01 v20 — remint END AISLE only. Flow Veo 3.1 Fast I2V.

Quality cannot use image ingredients (Flow tooltip). Fast is the HOS I2V
path on the Ultra plan. Two 8s walks, same aisle, same direction.
Take 2 starts on take 1 last frame. Reject still+zoom / Lite-if-still.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

import orbit_flow_veo_ui as flow  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
REF = PROJ / "04_Generated-Clips/part01/refs/v20_aisle"
RAW = PROJ / "04_Generated-Clips/part01/raw/v20_aisle"
STILL_T1 = REF / "aisle_start_v10_67_70.jpg"
OUT_T1 = RAW / "aisle_walk_t1.mp4"
OUT_T2 = RAW / "aisle_walk_t2.mp4"
REJECT = RAW / "_rejected"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL", "Veo 3.1 - Fast")
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)

PROMPT_T1 = (
    "IMAGE-TO-VIDEO of the attached start frame. Premium Animistry 3D cartoon. "
    "Same Victorian death-ward aisle. SHOT: a slow continuous walk down the aisle "
    "toward the far window. Camera dolly TRANSLATES forward from the first frame — "
    "beds, lamps, and floorboards recede past the lens. NOT a locked still. NOT a "
    "zoom. NOT Ken Burns. MUST MOVE the whole 8 seconds: camera walks forward, and "
    "the faceless 3D rods and spiked spheres already in the air drift with parallax "
    "in real 3D space. Sparse, not cute, not a neon overlay, no faces. They live in "
    "the room light. A trolley or cloth may ease as we pass. No Explorer, no orange "
    "Orbit robot, no readable text, no modern hospital. Silent. Continuous motion "
    "through the last frame."
)

PROMPT_T2 = (
    "IMAGE-TO-VIDEO of the attached start frame. Continue the SAME slow walk down "
    "this SAME Victorian death-ward aisle, SAME direction toward the far window. "
    "Camera keeps TRANSLATING forward from frame 1 — not a locked still, not a zoom, "
    "not Ken Burns. Faceless 3D rods and spiked spheres keep drifting in 3D space, "
    "sparse, not cute, not a neon overlay. No Explorer, no Orbit, no text, no modern "
    "hospital. Silent. Continuous 8 seconds through the last frame."
)


def extract_last_frame(mp4: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-sseof", "-0.05", "-i", str(mp4),
            "-update", "1", "-frames:v", "1", "-q:v", "2", str(dest),
        ],
        check=True,
        capture_output=True,
    )


def wait_create_enabled(page, *, timeout_s: float = 45) -> dict:
    t0 = time.time()
    last: dict = {}
    while time.time() - t0 < timeout_s:
        flow.dismiss_banners(page)
        flow._dismiss_asset_search_modal(page)
        last = page.evaluate(
            """() => {
              const hits = [];
              for (const b of document.querySelectorAll('button,[role="button"]')) {
                const t = (b.innerText || b.getAttribute('aria-label') || '')
                  .trim().replace(/\\n/g, ' ');
                if (!/arrow_forward|^Create$/i.test(t)) continue;
                if (/add_2|new project|error|cancel/i.test(t)) continue;
                const r = b.getBoundingClientRect();
                hits.push({
                  t: t.slice(0, 60),
                  dis: !!(b.disabled || b.getAttribute('aria-disabled') === 'true'),
                  w: Math.round(r.width),
                });
              }
              return { hits };
            }"""
        )
        enabled = [
            h for h in last.get("hits", []) if not h.get("dis") and h.get("w", 0) >= 8
        ]
        print(f"  create_state {json.dumps(last)[:300]}", flush=True)
        if enabled:
            return last
        page.wait_for_timeout(1500)
    return last


def mint(still: Path, prompt: str, out: Path) -> dict:
    if not still.exists():
        raise SystemExit(f"missing still {still}")
    out.parent.mkdir(parents=True, exist_ok=True)
    print(f"profile={PROFILE}", flush=True)
    print(f"model={MODEL}", flush=True)
    print(f"still={still}", flush=True)
    print(f"out={out}", flush=True)
    t0 = time.time()
    with sync_playwright() as p:
        ctx, page = flow.launch_context(
            p, headed=False, profile=flow.profile_path(PROFILE)
        )
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2000)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit("Flow not logged in.")
            url = flow.ensure_project(page)
            print(f"  flow: {url}", flush=True)
            flow.ensure_agent_session(page)
            before = flow.collect_media_ids(page)
            flow.configure_veo_settings(
                page, model=MODEL, frames_mode=False, ingredients_mode=True
            )
            print("  attaching start frame (Ingredients + Animate)…", flush=True)
            if not flow.attach_image_to_prompt(page, still):
                raise SystemExit("start-frame attach failed")
            if flow.try_context_animate(page):
                flow.configure_veo_settings(
                    page, model=MODEL, frames_mode=False, ingredients_mode=True
                )
            flow.set_prompt(page, prompt)
            if flow._prompt_attachment_count(page) < 1:
                print("  chip missing — re-attaching", flush=True)
                flow.attach_image_to_prompt(page, still)
                flow.set_prompt(page, prompt)
            if flow._prompt_attachment_count(page) < 1:
                raise SystemExit("Start-frame prompt chip missing")
            state = wait_create_enabled(page, timeout_s=45)
            enabled = [
                h for h in state.get("hits", []) if not h.get("dis") and h.get("w", 0) >= 8
            ]
            if not enabled:
                print(f"  Create not listed — submit_create anyway {state}", flush=True)
            print("  submitting Create…", flush=True)
            flow.submit_create(page)
            flow.confirm_generation_spend(page)
            flow.wait_and_download(
                page, out, before_ids=before, timeout_s=1200, min_elapsed_s=20
            )
        finally:
            ctx.close()
    if not out.exists() or out.stat().st_size < 400_000:
        raise SystemExit(f"download missing/small {out}")
    meta = {
        "seconds": round(time.time() - t0, 1),
        "bytes": out.stat().st_size,
        "model": MODEL,
        "start_frame": str(still),
    }
    print(json.dumps(meta, indent=2), flush=True)
    print(f"SAVED {out} bytes={out.stat().st_size}", flush=True)
    return meta


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--take", choices=("1", "2"), required=True)
    args = ap.parse_args()
    if "Lite" in MODEL:
        raise SystemExit("Refuse Lite for this remint — Quality/Ultra only.")
    if args.take == "1":
        mint(STILL_T1, PROMPT_T1, OUT_T1)
        return
    if not OUT_T1.exists():
        raise SystemExit("take 1 missing — mint take 1 first")
    last = REF / "aisle_t1_last.jpg"
    extract_last_frame(OUT_T1, last)
    print(f"take2 start={last}", flush=True)
    mint(last, PROMPT_T2, OUT_T2)


if __name__ == "__main__":
    main()
