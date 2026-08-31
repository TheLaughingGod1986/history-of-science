#!/usr/bin/env python3
"""Mint Part 02 plate 08 ward v04 — Flow Veo 3.1 Lite I2V, camera 100% locked."""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

import orbit_flow_veo_ui as flow  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
STILL = PROJ / "04_Generated-Clips/part02/refs/08_ward_vs_lens_v03.jpg"
OUT = PROJ / "04_Generated-Clips/part02/raw/v04_flow/08_ward_vs_lens_v04.mp4"
MODEL = "Veo 3.1 - Lite"
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)

# Keep under Flow's comfortable prompt length. Locked-camera + acting only.
PROMPT = (
    "IMAGE-TO-VIDEO of the attached start frame. Premium Animistry 3D cartoon. "
    "CAMERA 100 PERCENT LOCKED: no zoom, no pan, no tilt, no dolly, no Ken Burns. "
    "First and last frame share the exact same framing. Brass microscope stays "
    "the same size and screen position. Animate ONLY people and cloth already "
    "in frame: Victorian nurses walk or turn, apron and quilt cloth move, steam "
    "and haze rise through sunbeams, sparse faceless germs (rods/spheres/spirals "
    "only — no faces) drift. Continuous acting 8 seconds. Silent. "
    "No Explorer, no Orbit robot, no readable text, no modern hospital."
)


def create_state(page) -> dict:
    return page.evaluate(
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
              aria: b.getAttribute('aria-disabled'),
              title: b.getAttribute('title') || '',
              x: Math.round(r.x), y: Math.round(r.y),
              w: Math.round(r.width), h: Math.round(r.height),
            });
          }
          const ed = document.querySelector('[data-slate-editor="true"]');
          return {
            editor: (ed && (ed.innerText || '').trim().slice(0, 120)) || '',
            chips: document.querySelectorAll('img').length,
            hits,
          };
        }"""
    )


def wait_create_enabled(page, *, timeout_s: float = 60) -> dict:
    t0 = time.time()
    last = {}
    while time.time() - t0 < timeout_s:
        flow.dismiss_banners(page)
        flow._dismiss_asset_search_modal(page)
        last = create_state(page)
        enabled = [h for h in last.get("hits", []) if not h.get("dis") and h.get("w", 0) >= 8]
        print(f"  create_state {json.dumps(last)[:500]}", flush=True)
        if enabled:
            return last
        page.wait_for_timeout(1500)
    return last


def main() -> None:
    if not STILL.exists():
        raise SystemExit(f"missing still {STILL}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    print(f"profile={PROFILE} model={MODEL}", flush=True)
    print(f"still={STILL}", flush=True)
    print(f"out={OUT}", flush=True)
    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=False, profile=flow.profile_path(PROFILE))
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2000)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit("Flow not logged in.")
            print(f"  start-frame I2V: {STILL}", flush=True)
            url = flow.ensure_project(page)
            print(f"  flow: {url}", flush=True)
            flow.ensure_agent_session(page)
            before = flow.collect_media_ids(page)
            flow.configure_veo_settings(
                page, model=MODEL, frames_mode=False, ingredients_mode=True
            )
            print("  attaching start frame (Ingredients, no Animate)…", flush=True)
            if not flow.attach_image_to_prompt(page, STILL):
                raise SystemExit("start-frame attach failed")
            flow.set_prompt(page, PROMPT)
            if flow._prompt_attachment_count(page) < 1:
                print("  chip missing — re-attaching", flush=True)
                flow.attach_image_to_prompt(page, STILL)
                flow.set_prompt(page, PROMPT)
            if flow._prompt_attachment_count(page) < 1:
                raise SystemExit("Start-frame prompt chip missing")
            state = wait_create_enabled(page, timeout_s=45)
            enabled = [h for h in state.get("hits", []) if not h.get("dis") and h.get("w", 0) >= 8]
            if not enabled:
                raise SystemExit(
                    "STOP: Flow Create stayed disabled after a real prompt + still. "
                    f"state={state}. Do not fake a zoom."
                )
            print("  submitting Create…", flush=True)
            flow.submit_create(page)
            flow.confirm_generation_spend(page)
            print("  waiting for Veo Lite mp4…", flush=True)
            flow.wait_and_download(
                page, OUT, before_ids=before, timeout_s=900, min_elapsed_s=20
            )
            if not OUT.exists() or OUT.stat().st_size < 400_000:
                raise SystemExit(f"download missing/small {OUT}")
            print(f"OK {OUT} bytes={OUT.stat().st_size}", flush=True)
        finally:
            ctx.close()


if __name__ == "__main__":
    main()
