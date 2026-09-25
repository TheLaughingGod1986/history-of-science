#!/usr/bin/env python3
"""Part 05 plate 02 try3 — NEW FRAMING after 2 desk FAILs.

try1 HOLD: open lamp bulb. try2 FAIL: fire in a cutout desk slot.
P04 lesson: after 2 same-DNA FAILs → new framing, not a harder desk prompt.
This take: adult hands PIN cream cards onto the WALL CHART. No desk trenches.
Same cycle v01_c2_02_nolamp (start 2/2). Auth Mini CDP Ultra. Paint banned.
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
CYCLE = "v01_c2_02_nolamp"
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
    "ZERO lava, ZERO molten bead, ZERO fire, ZERO flame, ZERO sparks, ZERO fire-pits in wood. "
    "No Explorer. No Orbit. No model-town / yellow house-blocks. No paint. "
    "No flasks. No mortar. No HUD. Blank cream cards OK. "
    "Continuous real Veo motion the WHOLE 8 seconds — never freeze, never Ken Burns still. "
    f"Silent. Plate-library lock {PLATE_LIBRARY}. Animistry-class stylised 3D cartoon. "
    + BANNED_STILL
)

PROMPT_02 = (
    "TEXT-TO-VIDEO. Plate 02_guests_as_work try3 — they arrive as work. NEW FRAMING. "
    "VO beat: the guests do not arrive as a dream; they arrive as work. "
    "ONE continuous 8s take, stylised 3D cartoon 1869 classroom. "
    "HERO ACTION (must be readable muted): adult human hands (no boy, no Explorer) "
    "PIN cream cards onto a wooden WALL CHART of cream cards. "
    "Empty seats are blank card-sized spaces on the grid — solid wood behind, "
    "NOT a hole, NOT a trench, NOT a slot cut into a desk. "
    "Soft warm daylight on the empty card-spaces. Hands pin one card into a waiting space. "
    "TIGHT on the wall and hands. No chemist desk with cutouts. "
    "Continuous the whole 8 seconds. "
    + CLEAN
)

JOBS = [
    {
        "plate": "02_guests_as_work",
        "which": "wall_pin_work",
        "prompt": PROMPT_02,
        "out": QA_DIR / "submit_02_guests_as_work_try3.json",
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
    tmp = Path(f"/tmp/hos_p05_{job['plate']}_try3_stub.mp4")
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
        "try": "3_v01_wallpin",
        "which": job["which"],
        "start_n": start_n,
        "max_starts": MAX_STARTS,
        "project_url": project_url,
        "info": {k: v for k, v in info.items() if k != "path"},
        "start_frame": None,
        "mode": "T2V",
        "model": MODEL,
        "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "paint": "banned",
        "assemble": False,
        "note": "try2 FAIL fire-in-slot; try3 wall-pin, no desk trenches",
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
        print(json.dumps({"submitted": urls, "next": "harvest 02 try3 → plate UAT"}, indent=2), flush=True)


if __name__ == "__main__":
    main()
