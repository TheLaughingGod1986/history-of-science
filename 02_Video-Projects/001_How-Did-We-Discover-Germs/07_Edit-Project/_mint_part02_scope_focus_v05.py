#!/usr/bin/env python3
"""Mint Part 02 plate 08_scope_focus v05 — Flow Veo 3.1 Lite I2V.

New beat (not the ward). Locked 3/4 brass microscope. Period hand on the
focus wheel. Drop racks blur → sharp faceless cells. Camera 100% locked.
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
STILL = PROJ / "04_Generated-Clips/part02/refs/08_scope_focus_v05.jpg"
RAW = PROJ / "04_Generated-Clips/part02/raw/v05_flow"
OUT = RAW / "08_scope_focus_v05.mp4"
MODEL = "Veo 3.1 - Lite"
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
WARD_NAMES = (
    "08_ward_vs_lens",
    "ward_vs_lens",
)

# No "continuous camera" — that wrapper invented Ken Burns on v02–v04.
PROMPT = (
    "IMAGE-TO-VIDEO of the attached start frame. Premium Animistry 3D cartoon. "
    "CAMERA 100 PERCENT LOCKED on a three-quarter brass microscope. "
    "No zoom, no push, no pan, no tilt, no dolly, no Ken Burns, no reframing. "
    "First and last frame share the exact same framing. The microscope stays "
    "the same size and screen position. "
    "Animate ONLY: (1) the period hand fingers TURN the fine-focus wheel, "
    "(2) the brass wheel ROTATES, (3) the bead of water on the slide SHIMMERS, "
    "(4) rack focus INSIDE the drop — starts soft/blurry, snaps sharp on "
    "faceless 3D rods and spiked spheres living IN the bead, not floating in air. "
    "Hands only — no face, no head, no Explorer child, no Orbit robot. "
    "No hospital ward, no modern lab, no overlay germs outside the drop, "
    "no smiling germs, no readable text. Silent 8 seconds."
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
        print(f"  create_state {json.dumps(last)[:400]}", flush=True)
        if enabled:
            return last
        page.wait_for_timeout(1500)
    return last


def mint_once(dest: Path) -> None:
    if any(w in dest.name for w in WARD_NAMES):
        raise SystemExit(f"REFUSED: will not write a ward plate ({dest.name})")
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
                    "STOP: Flow Create stayed disabled. Do not fake a zoom. "
                    f"state={state}"
                )
            print("  submitting Create…", flush=True)
            flow.submit_create(page)
            flow.confirm_generation_spend(page)
            print("  waiting for Veo Lite mp4…", flush=True)
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
    for t, name in ((0.0, "t00"), (2.0, "t02"), (4.0, "t04"), (6.0, "t06"), (7.8, "t78")):
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
    if "ward" in STILL.name.lower():
        raise SystemExit("REFUSED: will not I2V a ward still")
    attempt = os.environ.get("HOS_V05_ATTEMPT", "a")
    dest = OUT if attempt == "a" else RAW / f"08_scope_focus_v05_{attempt}.mp4"
    mint_once(dest)
    qa = extract_qa(dest)
    print(f"QA_DIR {qa}", flush=True)
    print(f"PLATE {dest}", flush=True)
    print(f"PLATE_SHA256 {sha256(dest)}", flush=True)


if __name__ == "__main__":
    main()
