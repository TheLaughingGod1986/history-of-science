#!/usr/bin/env python3
"""Mint Part 02 plate 08_drop_hits_slide v06 — Flow Veo 3.1 Quality I2V.

New beat (not ward, not v05 wheel). Locked close 3/4 brass-framed slide.
Period dropper at top. Drop falls, hits, spreads. Camera 100% locked.
"""
from __future__ import annotations

import hashlib
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
STILL = PROJ / "04_Generated-Clips/part02/refs/08_drop_hits_slide_v06.jpg"
RAW = PROJ / "04_Generated-Clips/part02/raw/v06_flow"
OUT = RAW / "08_drop_hits_slide_v06.mp4"
# Quality cannot use image ingredients ("You cannot use image ingredients
# with this model"). Fast is Ultra-plan I2V — never Lite for this beat.
MODEL = "Veo 3.1 - Fast"
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
BANNED = ("08_ward_vs_lens", "ward_vs_lens", "08_scope_focus", "scope_focus")

# No "continuous camera" — that wrapper invented Ken Burns on v02–v05.
PROMPT = (
    "IMAGE-TO-VIDEO of the attached start frame. Premium Animistry 3D cartoon. "
    "CAMERA 100 PERCENT LOCKED on a close three-quarter brass-framed glass slide. "
    "No zoom, no push, no pan, no tilt, no dolly, no Ken Burns, no reframing. "
    "First and last frame share the exact same framing. The slide stays the "
    "same size and screen position. "
    "Animate ONLY the drop action: the pendant pond-water drop DETACHES from "
    "the period glass dropper at the top, FALLS straight down through the air, "
    "HITS the empty glass (the slap), SPLASHES and SPREADS into a trembling "
    "bead that WOBBLES then settles. After impact, sparse faceless 3D rods "
    "and spiked spheres are already living INSIDE the bead — not morphing in, "
    "not fading in as an overlay. "
    "Hands and dropper only — no face, no Explorer, no Orbit robot. "
    "No hospital ward, no modern plastic pipette, no smiling germs, no text. "
    "Silent 8 seconds."
)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


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
              x: Math.round(r.x), y: Math.round(r.y),
              w: Math.round(r.width), h: Math.round(r.height),
            });
          }
          const ed = document.querySelector('[data-slate-editor="true"]');
          return {
            editor: (ed && (ed.innerText || '').trim().slice(0, 120)) || '',
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
        print(f"  create_state {json.dumps(last)[:400]}", flush=True)
        if enabled:
            return last
        page.wait_for_timeout(1500)
    return last


def mint_once(dest: Path) -> None:
    if any(b in dest.name for b in BANNED):
        raise SystemExit(f"REFUSED: will not write a banned plate ({dest.name})")
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"profile={PROFILE} model={MODEL}", flush=True)
    print(f"still={STILL}", flush=True)
    print(f"out={dest}", flush=True)
    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=False, profile=flow.profile_path(PROFILE))
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
            print("  attaching start frame (Ingredients, Quality, no Animate)…", flush=True)
            if not flow.attach_image_to_prompt(page, STILL):
                raise SystemExit("start-frame attach failed")
            flow.set_prompt(page, PROMPT)
            if flow._prompt_attachment_count(page) < 1:
                flow.attach_image_to_prompt(page, STILL)
                flow.set_prompt(page, PROMPT)
            if flow._prompt_attachment_count(page) < 1:
                raise SystemExit("Start-frame prompt chip missing")
            state = wait_create_enabled(page, timeout_s=20)
            enabled = [h for h in state.get("hits", []) if not h.get("dis") and h.get("w", 0) >= 8]
            try:
                btns = page.evaluate(
                    """() => [...document.querySelectorAll('button,[role="button"]')]
                      .map(b => (b.innerText || b.getAttribute('aria-label') || '')
                        .trim().replace(/\\n/g,' ')).filter(t => t).slice(0, 60)"""
                )
                print(f"  PAGE_BUTTONS {btns}", flush=True)
            except Exception as e:
                print(f"  PAGE_BUTTONS err {e}", flush=True)
            if not enabled:
                print(f"  create_state empty/disabled — trying submit_create anyway {state}", flush=True)
            print("  submitting Create (Veo 3.1 Quality)…", flush=True)
            flow.submit_create(page)
            flow.confirm_generation_spend(page)
            print("  waiting for Veo Quality mp4…", flush=True)
            flow.wait_and_download(
                page, dest, before_ids=before, timeout_s=900, min_elapsed_s=20
            )
            if not dest.exists() or dest.stat().st_size < 400_000:
                raise SystemExit(f"download missing/small {dest}")
            print(f"OK {dest} bytes={dest.stat().st_size} sha={sha256(dest)}", flush=True)
        finally:
            ctx.close()


def extract_qa(plate: Path) -> Path:
    qa = plate.parent / "qa"
    qa.mkdir(parents=True, exist_ok=True)
    for t, name in (
        (0.0, "t00"),
        (1.0, "t01"),
        (2.0, "t02"),
        (3.5, "t35"),
        (5.0, "t50"),
        (7.8, "t78"),
    ):
        dest = qa / f"{name}.jpg"
        subprocess.run(
            [
                "ffmpeg", "-y", "-ss", f"{t:.2f}", "-i", str(plate),
                "-frames:v", "1", "-update", "1", "-q:v", "3", str(dest),
            ],
            check=True,
            capture_output=True,
        )
    return qa


def main() -> None:
    if not STILL.exists():
        raise SystemExit(f"missing still {STILL}")
    low = STILL.name.lower()
    if any(b in low for b in BANNED) or "ward" in low:
        raise SystemExit("REFUSED: will not I2V a ward/v05 still")
    attempt = os.environ.get("HOS_V06_ATTEMPT", "a")
    dest = OUT if attempt == "a" else RAW / f"08_drop_hits_slide_v06_{attempt}.mp4"
    mint_once(dest)
    qa = extract_qa(dest)
    print(f"QA_DIR {qa}", flush=True)
    print(f"PLATE {dest}", flush=True)
    print(f"PLATE_SHA256 {sha256(dest)}", flush=True)


if __name__ == "__main__":
    main()
