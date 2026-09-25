#!/usr/bin/env python3
"""07b try2 — try1 FAIL (chair fire / miniature armchair). One retry.

KEEP 08_prediction_navigation v25 try1 (walk toward vacant chair).
Do not assemble try1 07b (ZERO fire lock).
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
QA_DIR = PROJ / "07_Edit-Project/_qa_part04_v25_kill_moondesk"
START_COUNTER = QA_DIR / "start_counter.json"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL") or "Veo 3.1 - Fast"
REQUIRED_EMAIL = "benoats@googlemail.com"
MAX_STARTS = 3
PLATE_LIBRARY = "4b8ed25"

PROMPT = (
    "TEXT-TO-VIDEO. Plate 07b_eka_names_rotate try2 — placeholder names rotate. "
    "VO: he names the missing seats. Eka-aluminium. Eka-boron. Eka-silicon. Placeholders. "
    "ONE continuous 8s take, stylised 3D cartoon. "
    "HERO: THREE standing blank cream cards in a row on a warm wood tabletop, MACRO close. "
    "A soft gold GLOW (not fire) hops left → middle → right card, like naming three empty seats. "
    "Camera: slow side-slide along the three cards. "
    "HARD: ZERO fire, ZERO flame, ZERO sparks, ZERO burning, ZERO miniature chair, "
    "ZERO furniture morph, ZERO lava. Cards stay cards. Glow is a light, not a flame. "
    "NO moon window. NO wide flasks+lamp still-life. No Explorer. No readable letters. "
    "CLEAN LIGHT: lamp shade HIDES the bulb if a lamp exists. "
    "Continuous real Veo motion the WHOLE 8 seconds — never freeze, never Ken Burns still. "
    f"Silent. Plate-library lock {PLATE_LIBRARY}. Animistry-class stylised 3D cartoon."
)


def bump() -> int:
    QA_DIR.mkdir(parents=True, exist_ok=True)
    n = 0
    if START_COUNTER.exists():
        try:
            n = int(json.loads(START_COUNTER.read_text()).get("starts", 0))
        except Exception:
            n = 0
    n += 1
    START_COUNTER.write_text(
        json.dumps(
            {
                "cycle": "v25_kill_moondesk",
                "plate": "07b_eka_names_rotate",
                "try": "2",
                "starts": n,
                "max_starts": MAX_STARTS,
                "try1": "FAIL fire/miniature chair",
                "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
            },
            indent=2,
        )
        + "\n"
    )
    if n > MAX_STARTS:
        raise SystemExit(f"STOP_TO_COS: already used {n - 1}/{MAX_STARTS} Flow starts")
    print(f"start_counter={n}/{MAX_STARTS} plate=07b try2", flush=True)
    return n


def assert_auth(page) -> dict:
    blob = (page.content() + "\n" + (page.inner_text("body") or "")).lower()
    if any(x in blob for x in ("passkey", "verifying it's you", "verifying it’s you")):
        raise SystemExit("STOP_TO_COS BLOCKED_AUTH: passkey wall")
    if "ultra" not in blob:
        raise SystemExit("STOP_TO_COS BLOCKED_AUTH: ULTRA badge missing")
    return {"ultra": True}


def main() -> None:
    for need in ("TEXT-TO-VIDEO", "8s", "lava", "Ken Burns", "4b8ed25"):
        if need.lower() not in PROMPT.lower():
            raise SystemExit(f"ABORT: prompt missing {need}")
    bump()
    out_json = PROJ / "07_Edit-Project/_qa_part04_v20_flow/submit_07b_eka_names_rotate_try2_v25.json"
    tmp = Path("/tmp/hos_v25_07b_try2_stub.mp4")
    if tmp.exists():
        tmp.unlink()
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=180000)
        time.sleep(3)
        for name in ("Agree", "Got it", "Accept all"):
            try:
                page.get_by_role("button", name=name).first.click(timeout=1500)
            except Exception:
                pass
        print(f"auth={assert_auth(page)}", flush=True)
        info: dict = {}
        try:
            info = flow.generate_clip(
                page,
                PROMPT,
                tmp,
                model=MODEL,
                timeout_s=70,
                attempts=1,
                scenery_only=True,
            )
        except Exception as e:
            info = {"error": str(e), "project_url": page.url or ""}
            print(f"submit note: {e}", flush=True)
        project_url = str(
            info.get("project_url") or info.get("url") or page.url or ""
        ).split("?")[0].rstrip("/")
        out = {
            "plate": "07b_eka_names_rotate",
            "try": "2_v25",
            "project_url": project_url,
            "info": {k: v for k, v in info.items() if k != "path"},
            "mode": "T2V",
            "model": MODEL,
            "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "paint": "banned",
            "try1": "FAIL fire",
        }
        out_json.write_text(json.dumps(out, indent=2) + "\n")
        print(json.dumps(out, indent=2), flush=True)
        if "/project/" not in project_url:
            raise SystemExit("no project url")


if __name__ == "__main__":
    main()
