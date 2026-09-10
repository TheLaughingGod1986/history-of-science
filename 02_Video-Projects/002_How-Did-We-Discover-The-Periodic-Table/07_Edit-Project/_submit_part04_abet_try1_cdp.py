#!/usr/bin/env python3
"""Remint A BET stretch (Ben UAT on v23): 08b + 09 only.

Ben: moon-desk scene repeats 3–4 times under A BET; needs more animation and
must explain the VO (if nothing arrives he invented imaginary metals; if something
arrives matching, the table is a machine for finding the unknown).

KEEP 09b_risk_hold try14 (three glowing vacant chairs — already VO-literal hold).
Remint:
  08b_navigation_walk — FAIL beat: empty chair stays empty / papers fade (imaginary).
  09_risk_bet        — WIN beat: matching card/ingot arrives, vacant seat fills.

T2V (no moon-desk start attach) so Veo is not locked to the repeating 08b still.
Veo 3.1 Fast. Paint banned. Max 1 start per plate this run.
Auth: Mini CDP benoats@googlemail.com ULTRA.
"""
from __future__ import annotations

import hashlib
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
QA_DIR = PROJ / "07_Edit-Project/_qa_part04_v24_plates_abet"
START_COUNTER = QA_DIR / "start_counter.json"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL") or "Veo 3.1 - Fast"
REQUIRED_EMAIL = "benoats@googlemail.com"
MAX_STARTS = 2
PLATE_LIBRARY = "4b8ed25"

CLEAN = (
    "CLEAN LIGHT (HARD for full 8s): warm practical lamp MAY exist but shade HIDES the bulb; "
    "soft continuous warm cone only. ZERO lava drip, ZERO molten bead under shade, "
    "ZERO open shade-cup, ZERO fire, ZERO flame, ZERO sparks, ZERO chair fire. "
    "No Explorer. No Orbit. No model-town / yellow house-blocks. No paint. "
    "No readable letters / element symbols / HUD / UI on cards. Blank cream cards OK. "
    "Continuous real Veo motion the WHOLE 8 seconds — never freeze, never Ken Burns still. "
    f"Silent. Plate-library lock {PLATE_LIBRARY}. Animistry-class stylised 3D cartoon."
)

PROMPT_08B = (
    "TEXT-TO-VIDEO. Plate 08b_navigation_walk try1 — A BET FAIL fork. "
    "VO beat: if nothing arrives, he invented imaginary metals. "
    "ONE continuous 8s take, stylised 3D cartoon chemist study. "
    "HERO ACTION (must be readable muted): a single empty wooden chair at a honey-wood desk "
    "sits in a vacant glowing seat-slot. Over 8 seconds the glow on that empty chair "
    "FADES and DIES — dust settles, papers on the desk go dull, the vacant seat stays EMPTY. "
    "Camera: slow push-in toward the empty chair (not a locked still). "
    "Night window with moon in BACKGROUND only — chair+desk are the subject, not another wide still-life. "
    "Do NOT repeat a wide flasks+lamp+three-blank-cards still-life. "
    "Do NOT fill the chair. Do NOT invent a person. "
    + CLEAN
)

PROMPT_09 = (
    "TEXT-TO-VIDEO. Plate 09_risk_bet try1 — A BET WIN fork. "
    "VO beat: if something arrives matching his description, the table is no longer a poster — "
    "it is a machine for finding the unknown. "
    "ONE continuous 8s take, stylised 3D cartoon chemist study. "
    "HERO ACTION (must be readable muted): a vacant glowing card-slot / empty chair at the desk "
    "RECEIVES a matching cream card that slides in from off-frame and LOCKS into the empty seat "
    "with a soft golden settle-glow (NOT fire, NOT lava). The empty chair fills with presence — "
    "the bet PAYS. Camera: start on the empty slot, then the arriving card/ingot, settle. "
    "Different framing from 08b (three-quarter desk, card-slot hero — NOT the same wide moon still-life). "
    "Do NOT leave the seat empty. Do NOT invent Explorer. Do NOT invent readable letters. "
    + CLEAN
)

JOBS = [
    {
        "plate": "08b_navigation_walk",
        "which": "fail",
        "prompt": PROMPT_08B,
        "out": PROJ / "07_Edit-Project/_qa_part04_v20_flow/submit_08b_navigation_walk_try1_abet.json",
    },
    {
        "plate": "09_risk_bet",
        "which": "win",
        "prompt": PROMPT_09,
        "out": PROJ / "07_Edit-Project/_qa_part04_v20_flow/submit_09_risk_bet_try1_abet.json",
    },
]


def bump_start_counter(plate: str) -> int:
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
                "cycle": "abet_v24",
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
    print(f"start_counter={n}/{MAX_STARTS} plate={plate}", flush=True)
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
    tmp = Path(f"/tmp/hos_v24_{job['plate']}_stub.mp4")
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
        "try": "1_abet",
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
        "ben_uat": "v23 A BET moon-desk repeats 3-4x; remint 08b FAIL + 09 WIN; KEEP 09b try14",
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
        print(json.dumps({"submitted": urls, "next": "harvest → QA → assemble v24"}, indent=2), flush=True)


if __name__ == "__main__":
    main()
