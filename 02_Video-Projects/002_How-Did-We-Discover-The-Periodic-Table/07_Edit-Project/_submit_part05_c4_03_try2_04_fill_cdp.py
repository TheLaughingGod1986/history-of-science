#!/usr/bin/env python3
"""Part 05 cycle v01_c4 — remint Explorer (new framing) + mint 04 wall-slot fill.

03 try1 FAIL: giant disembodied palm, no Explorer. Silver melt was PASS.
P04 lesson: palm-CU DNA hid the character → waist-up so glasses + teal stay in frame.
04: MACRO one wall-grid slot fills with Ga silver sheen. No desk fire-trenches.

Max 2 starts. Auth Mini CDP Ultra. Paint banned. T2V Quality.
Do NOT I2V the identity sheet.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow

flow.FLOW_HOME = os.environ.get("ORBIT_FLOW_HOME", "https://flow.google.com/")
CDP = os.environ.get("ORBIT_FLOW_CDP", "http://127.0.0.1:9222")
PROJ = Path(__file__).resolve().parents[1]
QA_DIR = PROJ / "07_Edit-Project/_qa_part05_v01_flow"
START_COUNTER = QA_DIR / "start_counter.json"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL") or "Veo 3.1 - Quality"
REQUIRED_EMAIL = "benoats@googlemail.com"
MAX_STARTS = 2
CYCLE = "v01_c4_03_ms_04_fill"
PLATE_LIBRARY = "4b8ed25"

BANNED_STILL = (
    "HARD FORBIDDEN COMPOSITION (P04 Ben reject): do NOT show a wide honey-wood desk "
    "with a full moon in the LEFT window, purple/green flasks, white mortar, stacked "
    "papers, three blank cards on the desk, desk-lamp on the RIGHT, clay pots, and a "
    "faint empty chair back. That exact still-life is BANNED for the full 8 seconds. "
)

CLEAN = (
    "CLEAN LIGHT (HARD for full 8s): THERE IS NO PRACTICAL TABLE LAMP — "
    "zero shade, zero bulb, zero shade-cup, zero brass desk lamp. "
    "Daytime window bounce ONLY. "
    "ZERO lava, ZERO molten bead, ZERO orange melt, ZERO fire, ZERO flame, ZERO sparks. "
    "ZERO fire-pits cut into wood. ZERO glowing trenches in a desk. "
    "Gallium is cool dull SILVER like tin, never orange, never glowing like a furnace. "
    "No Orbit. No twins. No model-town / yellow house-blocks. No paint. "
    "Continuous real Veo motion the WHOLE 8 seconds — never freeze, never Ken Burns still. "
    f"Silent. Plate-library lock {PLATE_LIBRARY}. Animistry-class stylised 3D cartoon. "
    + BANNED_STILL
)

PROMPT_03 = (
    "TEXT-TO-VIDEO. Plate 03_explorer_gallium_palm try2 — Gallium. NEW FRAMING. "
    "VO beat: eighteen seventy-five, gallium, almost liquid in a warm room. "
    "ONE continuous 8s take. "
    "CAMERA: WAIST-UP medium shot of a standing boy. His HEAD, round gold glasses, "
    "and dark teal trenchcoat MUST stay in frame the whole 8 seconds. "
    "FORBIDDEN: giant disembodied hand filling the frame, palm-only close-up, no face. "
    "ONE finished Explorer boy: messy wavy chestnut-brown hair covering the full crown, "
    "round gold wire-rim glasses CLEARLY VISIBLE, large eyes with pupils, "
    "dark teal trenchcoat, mustard/tan vest, brown bow tie, white shirt, brown satchel. "
    "Human fingers, not mitts. He looks DOWN at his own palm, not at the camera. "
    "HERO ACTION: a SMALL cool SILVERY puddle of room-temp gallium in one palm — "
    "dull silver like tin, a small blob, NOT orange, NOT lava, NOT a glowing bead. "
    "The palm is a lower-third prop. The boy is the subject. "
    "Soft 1869 wood classroom behind, out of focus. Not a lecture hall. Not toy-scale OTS. "
    "Not an academic blazer. Finished hair. Continuous look + slow silver melt. "
    + CLEAN
    + "Exactly ONE Explorer."
)

PROMPT_04 = (
    "TEXT-TO-VIDEO. Plate 04_gallium_fills_seat try1 — 1875. "
    "VO beat: gallium takes its seat. "
    "ONE continuous 8s take. MACRO on ONE vacant card-sized cell on a cream-card WALL GRID. "
    "Solid wood behind the empty cell — NOT a hole, NOT a trench, NOT a fire-pit cut in a desk. "
    "A cream card with a sparse Ga mark slides into that cell and a cool SILVER sheen settles. "
    "Empty seat = a blank card space on the wall. Daytime. No person. No lamp. No flasks. "
    "Continuous seat-fill the whole 8 seconds. Distinct from the wide wall-chart and the pin-hands plates. "
    + CLEAN
    + "No Explorer."
)

JOBS = [
    {
        "plate": "03_explorer_gallium_palm",
        "try": "2_v01",
        "which": "waist_up_gallium",
        "prompt": PROMPT_03,
        "out": QA_DIR / "submit_03_explorer_gallium_palm_try2.json",
        "note": "waist-up Explorer; silver puddle prop; no identity-sheet I2V",
    },
    {
        "plate": "04_gallium_fills_seat",
        "try": "1_v01",
        "which": "wall_slot_fill",
        "prompt": PROMPT_04,
        "out": QA_DIR / "submit_04_gallium_fills_seat_try1.json",
        "note": "MACRO wall cell fill; silver not lava; no desk trenches",
    },
]


def bump_start_counter(plate: str) -> int:
    QA_DIR.mkdir(parents=True, exist_ok=True)
    n = 0
    if START_COUNTER.exists():
        try:
            prev = json.loads(START_COUNTER.read_text())
            if prev.get("cycle") == CYCLE:
                n = int(prev.get("starts", 0))
        except Exception:
            n = 0
    n += 1
    START_COUNTER.write_text(
        json.dumps(
            {
                "cycle": CYCLE,
                "plate": plate,
                "starts": n,
                "max_starts": MAX_STARTS,
                "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
            },
            indent=2,
        )
        + "\n"
    )
    if n > MAX_STARTS:
        raise SystemExit(f"STOP_TO_COS: already used {n - 1}/{MAX_STARTS} Flow starts")
    print(f"start_counter={n}/{MAX_STARTS} plate={plate} cycle={CYCLE}", flush=True)
    return n


def assert_auth(page) -> dict:
    html = page.content()
    try:
        body = page.inner_text("body")
    except Exception:
        body = ""
    blob = (html + "\n" + body).lower()
    if any(
        x in blob
        for x in (
            "passkey",
            "verifying it's you",
            "verifying it’s you",
            "use your passkey",
        )
    ):
        raise SystemExit("STOP_TO_COS BLOCKED_AUTH: passkey wall")
    if REQUIRED_EMAIL.lower() not in blob and "googlemail.com" not in blob:
        print("WARN: email not visible in DOM yet; continuing if ULTRA present", flush=True)
    if "ultra" not in blob:
        for sel in (
            '[aria-label*="Account details"]',
            '[aria-label*="Google Account"]',
            "text=ULTRA",
        ):
            try:
                page.locator(sel).first.click(timeout=1200)
                time.sleep(1)
                blob = (page.content() + "\n" + page.inner_text("body")).lower()
                break
            except Exception:
                pass
    if "ultra" not in blob:
        raise SystemExit("STOP_TO_COS BLOCKED_AUTH: ULTRA badge missing")
    return {"ultra": True, "email_hint": REQUIRED_EMAIL.lower() in blob}


def submit_one(page, job: dict) -> dict:
    for need in ("TEXT-TO-VIDEO", "8s", "lava", "Ken Burns", "4b8ed25"):
        if need.lower() not in job["prompt"].lower():
            raise SystemExit(f"ABORT: prompt missing {need}")
    start_n = bump_start_counter(job["plate"])
    tmp = Path(f"/tmp/hos_p05_{job['plate']}_{job['try']}_stub.mp4")
    if tmp.exists():
        tmp.unlink()
    info: dict = {}
    try:
        info = flow.generate_clip(
            page,
            job["prompt"],
            tmp,
            model=MODEL,
            timeout_s=70,
            attempts=1,
            scenery_only=True,
        )
    except Exception as e:
        info = {
            "error": str(e),
            "project_url": getattr(page, "_orbit_flow_project_url", None) or (page.url or ""),
        }
        print(f"submit note ({job['plate']}): {e}", flush=True)

    project_url = (
        info.get("project_url")
        or info.get("url")
        or getattr(page, "_orbit_flow_project_url", None)
        or page.url
        or ""
    )
    project_url = str(project_url).split("?")[0].rstrip("/")
    out = {
        "plate": job["plate"],
        "try": job["try"],
        "which": job["which"],
        "start_n": start_n,
        "max_starts": MAX_STARTS,
        "cycle": CYCLE,
        "project_url": project_url,
        "info": {k: v for k, v in info.items() if k != "path"},
        "start_frame": None,
        "mode": "T2V",
        "model": MODEL,
        "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "paint": "banned",
        "assemble": False,
        "note": job["note"],
    }
    job["out"].parent.mkdir(parents=True, exist_ok=True)
    job["out"].write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2), flush=True)
    if "/project/" not in project_url:
        raise SystemExit(f"no project url after submit ({job['plate']})")
    return out


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = ctx.new_page()
        page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=180000)
        time.sleep(3)
        for name in ("Agree", "Got it", "Accept all"):
            try:
                page.get_by_role("button", name=name).first.click(timeout=1500)
            except Exception:
                pass
        auth = assert_auth(page)
        print(f"auth={auth}", flush=True)
        urls = []
        for job in JOBS:
            try:
                page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=180000)
                time.sleep(2)
            except Exception:
                pass
            urls.append(submit_one(page, job).get("project_url"))
            time.sleep(2)
        print(json.dumps({"submitted": urls, "next": "harvest 03 try2 + 04 try1 → plate UAT"}, indent=2), flush=True)


if __name__ == "__main__":
    main()
