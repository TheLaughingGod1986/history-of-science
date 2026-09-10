#!/usr/bin/env python3
"""Part 05 plate 03 — Explorer gallium palm. Same cycle as 01b KEEP (start 2/2).

T2V Quality. On-model Explorer. Cool SILVER gallium, never lava.
Do NOT I2V the identity sheet. Auth Mini CDP Ultra. Paint banned.
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
CYCLE = "v01_c3_01b_empty"
PLATE_LIBRARY = "4b8ed25"

CLEAN = (
    "CLEAN LIGHT (HARD for full 8s): THERE IS NO PRACTICAL TABLE LAMP — "
    "zero shade, zero bulb, zero shade-cup, zero brass desk lamp. "
    "Daytime window bounce ONLY. "
    "ZERO lava, ZERO molten bead, ZERO orange melt, ZERO fire, ZERO flame, ZERO sparks. "
    "Gallium is cool dull SILVER like tin, never orange, never glowing like a furnace. "
    "Exactly ONE Explorer. No Orbit. No twins. No model-town. No paint. "
    "Continuous real Veo motion the WHOLE 8 seconds — never freeze, never Ken Burns still. "
    f"Silent. Plate-library lock {PLATE_LIBRARY}. Animistry-class stylised 3D cartoon. "
)

PROMPT_03 = (
    "TEXT-TO-VIDEO. Plate 03_explorer_gallium_palm try1 — Gallium. "
    "VO beat: eighteen seventy-five, gallium, almost liquid in a warm room. "
    "ONE continuous 8s take. "
    "ONE finished Explorer boy: messy wavy chestnut-brown hair covering the full crown, "
    "round gold wire-rim glasses CLEARLY VISIBLE, large eyes with pupils, "
    "dark teal trenchcoat, mustard/tan vest, brown bow tie, white shirt, brown satchel. "
    "Human fingers, not mitts. Three-quarter FRONT so glasses stay readable. "
    "HERO ACTION: a warm palm holds a cool SILVERY soft metal that puddles slowly — "
    "room-temp gallium, dull silver like tin, NOT orange, NOT lava, NOT a glowing bead. "
    "Camera: medium close on face+palm so coat, glasses, and silver puddle all read. "
    "Not a toy figurine. Not a back/OTS with no face. Not an academic blazer. "
    "Not a lecture hall. Soft 1869 wood room behind, out of focus. "
    + CLEAN
)

JOBS = [
    {
        "plate": "03_explorer_gallium_palm",
        "which": "gallium_palm",
        "prompt": PROMPT_03,
        "out": QA_DIR / "submit_03_explorer_gallium_palm_try1.json",
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
    tmp = Path(f"/tmp/hos_p05_{job['plate']}_try1_stub.mp4")
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
        "try": "1_v01",
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
        "note": "Explorer once; silver gallium; no identity-sheet I2V",
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
        print(json.dumps({"submitted": urls, "next": "harvest 03 → plate UAT"}, indent=2), flush=True)


if __name__ == "__main__":
    main()
