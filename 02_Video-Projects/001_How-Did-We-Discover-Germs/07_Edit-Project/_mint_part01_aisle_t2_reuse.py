#!/usr/bin/env python3
"""Take 2 on the project that already minted take 1. Dump buttons if Create dies."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

import orbit_flow_veo_ui as flow  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
STILL = PROJ / "04_Generated-Clips/part01/refs/v20_aisle/aisle_t1_last.jpg"
OUT = PROJ / "04_Generated-Clips/part01/raw/v20_aisle/aisle_walk_t2.mp4"
# Project that successfully minted take 1.
PROJECT = (
    "https://labs.google/fx/tools/flow/project/ca19bfec-e6dc-4a9b-94d7-dc9cd19368fe"
)
MODEL = "Veo 3.1 - Fast"
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
PROMPT = (
    "IMAGE-TO-VIDEO of the attached start frame. Continue the SAME slow walk down "
    "this SAME Victorian death-ward aisle, SAME direction toward the far window. "
    "Camera keeps TRANSLATING forward from frame 1 — not a locked still, not a zoom, "
    "not Ken Burns. Faceless 3D rods and spiked spheres keep drifting in 3D space, "
    "sparse, not cute, not a neon overlay. No Explorer, no Orbit, no text, no modern "
    "hospital. Silent. Continuous 8 seconds through the last frame."
)


def dump_buttons(page) -> None:
    btns = page.evaluate(
        """() => [...document.querySelectorAll('button,[role="button"]')]
          .map(b => {
            const t = (b.innerText || b.getAttribute('aria-label') || '')
              .trim().replace(/\\n/g,' ');
            const r = b.getBoundingClientRect();
            return t ? `${t.slice(0,80)} dis=${b.disabled} ${Math.round(r.w)}x${Math.round(r.h)}` : '';
          }).filter(Boolean).slice(0, 80)"""
    )
    print(f"  BUTTONS {json.dumps(btns)[:2000]}", flush=True)
    print(f"  URL {page.url}", flush=True)
    print(f"  TITLE {page.title()}", flush=True)


def main() -> None:
    if not STILL.exists():
        raise SystemExit(f"missing {STILL}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    print(f"reuse {PROJECT}", flush=True)
    with sync_playwright() as p:
        ctx, page = flow.launch_context(
            p, headed=False, profile=flow.profile_path(PROFILE)
        )
        try:
            page.goto(PROJECT, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2500)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit("Flow not logged in.")
            dump_buttons(page)
            meta = flow.generate_clip(
                page,
                PROMPT,
                OUT,
                model=MODEL,
                timeout_s=1200,
                start_frame=STILL,
                reuse_project=True,
            )
            print(json.dumps(meta, indent=2), flush=True)
            print(f"SAVED {OUT} bytes={OUT.stat().st_size}", flush=True)
        except Exception:
            dump_buttons(page)
            raise
        finally:
            ctx.close()


if __name__ == "__main__":
    main()
