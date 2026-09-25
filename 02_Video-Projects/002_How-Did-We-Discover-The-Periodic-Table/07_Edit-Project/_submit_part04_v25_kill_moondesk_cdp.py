#!/usr/bin/env python3
"""Remint 07b + 08 — kill the repeating moon-desk still-life (Ben UAT on v24).

Ben: the moon-window / flasks / lamp / three-cards / empty-chair still-life
still plays two or three times in hos_002_part04_rough_v24.

Diagnosis (v24 stills):
  ~62s 07_eka_placeholders   — same still-life (EKA-SILICON)  KEEP this cycle
  ~70s 07b_eka_names_rotate  — IDENTICAL still-life (A PREDICTION)
  ~78s 08_prediction_navigation — IDENTICAL still-life (A PREDICTION)  << Ben still
  ~86s 08b FAIL              — different angle, KEEP
  ~93s 09 WIN                — different, KEEP
  09b try14                  — three chairs, KEEP

Remint 07b + 08 only (max 2 starts). T2V, no moon-desk start attach.
Paint banned. Veo 3.1 Fast. Auth: Mini CDP benoats@googlemail.com ULTRA.
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
MAX_STARTS = 2
PLATE_LIBRARY = "4b8ed25"

BANNED_STILL = (
    "HARD FORBIDDEN COMPOSITION (the repeating still-life Ben rejected): "
    "do NOT show a wide honey-wood desk with a full moon in the LEFT window, "
    "purple/green flasks, white mortar, stacked papers, three blank cards on the "
    "desk, desk-lamp on the RIGHT, clay pots, and a faint empty chair back. "
    "That exact still-life is BANNED for the full 8 seconds. "
)

CLEAN = (
    "CLEAN LIGHT (HARD for full 8s): warm practical lamp MAY exist but shade HIDES the bulb; "
    "soft continuous warm cone only. ZERO lava drip, ZERO molten bead under shade, "
    "ZERO open shade-cup, ZERO fire, ZERO flame, ZERO sparks, ZERO chair fire. "
    "No Explorer. No Orbit. No model-town / yellow house-blocks. No paint. "
    "No readable letters / element symbols / HUD / UI on cards. Blank cream cards OK. "
    "Continuous real Veo motion the WHOLE 8 seconds — never freeze, never Ken Burns still. "
    f"Silent. Plate-library lock {PLATE_LIBRARY}. Animistry-class stylised 3D cartoon. "
    + BANNED_STILL
)

PROMPT_07B = (
    "TEXT-TO-VIDEO. Plate 07b_eka_names_rotate try1 — placeholder names rotate. "
    "VO beat: he names the missing seats (eka-aluminium, eka-boron, eka-silicon) — "
    "placeholders, not magic words. "
    "ONE continuous 8s take, stylised 3D cartoon 1869 chemist study. "
    "HERO ACTION (must be readable muted): THREE standing blank cream cards in a row "
    "on a warm wood desk. A soft gold vacant-seat glow HOPS from the left card to the "
    "middle card to the right card — the named empty seats rotating. Camera: slow orbit "
    "around the three cards (not a locked still). "
    "Daytime/warm interior. NO moon in a night window. "
    "Do NOT repeat a wide flasks+lamp+moon still-life. "
    + CLEAN
)

PROMPT_08 = (
    "TEXT-TO-VIDEO. Plate 08_prediction_navigation try1 — A PREDICTION / navigation. "
    "VO beat: discovery stops being luck — it becomes navigation: walk toward a vacant "
    "chair with an address. "
    "ONE continuous 8s take, stylised 3D cartoon 1869 wood chemist hall. "
    "HERO ACTION (must be readable muted): the CAMERA WALKS / dollies the whole 8 seconds "
    "toward ONE empty wooden chair with a soft vacant-seat glow — the chair is an address "
    "to walk toward. Continuous travel, not a locked still. "
    "Warm hall, bookshelves, floorboards. The empty glowing chair is the destination. "
    "NO moon-window still-life. NO flasks+three-blank-cards desk hero. "
    "Do NOT invent Explorer. Do NOT fill the chair with a person. "
    + CLEAN
)

JOBS = [
    {
        "plate": "07b_eka_names_rotate",
        "which": "eka_rotate",
        "prompt": PROMPT_07B,
        "out": PROJ / "07_Edit-Project/_qa_part04_v20_flow/submit_07b_eka_names_rotate_try1_v25.json",
    },
    {
        "plate": "08_prediction_navigation",
        "which": "navigation_walk",
        "prompt": PROMPT_08,
        "out": PROJ / "07_Edit-Project/_qa_part04_v20_flow/submit_08_prediction_navigation_try1_v25.json",
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
                "cycle": "v25_kill_moondesk",
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
    tmp = Path(f"/tmp/hos_v25_{job['plate']}_stub.mp4")
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
        "try": "1_v25",
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
        "ben_uat": "v24 still repeats moon-desk on 07b+08; remint those; KEEP 07/08b/09/09b",
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
        print(json.dumps({"submitted": urls, "next": "harvest → QA → assemble v25"}, indent=2), flush=True)


if __name__ == "__main__":
    main()
