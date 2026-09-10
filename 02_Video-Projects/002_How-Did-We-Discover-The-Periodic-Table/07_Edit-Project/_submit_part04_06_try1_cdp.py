#!/usr/bin/env python3
"""Dedicated 06_explorer_leaves_gap try1 submit on live Mini CDP.

DNA (CoS next plate after 09b CLEAN LIGHT lamp-loop park):
  OTS/back Explorer garnish + 1869 card-desk + soft glowing vacant seat/gap.
  Light = daytime window OR soft off-world bounce ONLY.
  ZERO practical table lamp in frame (no gooseneck / shade / bulb / shade-cup).

Start = crop-only lock (paint banned) from v10 back card-desk DNA with lamp ejected.
Plate-library 4b8ed25. Continuous plate UAT before any assemble.
Auth: Mini CDP benoats@googlemail.com ULTRA. STOP on passkey.
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
REF = PROJ / "04_Generated-Clips/part04/refs/v20_start_frames"
START = REF / "06_explorer_leaves_gap_start_v20.jpg"
LOCK = REF / "06_explorer_leaves_gap_start_v20_try1_ots_nolamp_windowbounce.jpg"
BANNED_ORE = REF / "06_explorer_leaves_gap_start_v20_pre_try1_nolamp.jpg"
OUT = PROJ / "07_Edit-Project/_qa_part04_v20_flow/submit_06_explorer_leaves_gap_try1.json"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL") or "Veo 3.1 - Fast"
REQUIRED_EMAIL = "benoats@googlemail.com"

PROMPT = (
    "IMAGE-TO-VIDEO of the attached start frame. Animate THIS exact beat only. "
    "Plate 06_explorer_leaves_gap try1 — EMPTY SEATS garnish: ONE finished Explorer "
    "(teal trenchcoat house lock, full chestnut crown finished — ZERO mid-crown unfinished hair) "
    "seen as toy-scale garnish in PROFILE / BACK / OTS (not face-on hero). "
    "1869 card-desk DNA: warm wood desk, cream written cards in stacks, bookcase behind OK. "
    "Explorer has just pinned a card and steps slightly back, leaving a soft glowing vacant seat / gap "
    "on the desk — soft warm glow only, NOT chair fire, NOT lava, NOT molten bead. "
    "Sparse readable marks on a few cards OK; ZERO unfinished flat blank cards. "
    "CLEAN LIGHT (HARD for full 8s): daytime WINDOW spill and/or soft OFF-WORLD bounce ONLY. "
    "THERE IS NO PRACTICAL TABLE LAMP IN FRAME — zero gooseneck, zero lampshade, zero bulb, "
    "zero shade-cup (open or closed), zero brass desk lamp, zero wall sconce, zero candle fixture. "
    "Do NOT invent any lamp/fixture mid-clip on any edge. If light would read as a lamp fixture → FAIL. "
    "HOUSE HARD FAIL forever (t0–t8): lava drip, molten bead, chair fire, unfinished flat cards, "
    "mid-crown unfinished Explorer hair, open shade-cup, visible underside bulb, invented brass lamp, "
    "model-town / yellow house-blocks, twins, academic blazer Explorer, Orbit robot. "
    "Exactly ONE Explorer. Glasses OK when face turns into view. Continuous real Veo motion. "
    "LOCKED TRIPOD CAMERA — do NOT widen, zoom out, or pan to reveal a lamp off-frame. "
    "Finished cinematic stylised 3D. Silent. Paint banned. "
    "Plate-library lock 4b8ed25. NOT ore/gas workshop room. NOT face-on specimen hero."
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def main() -> None:
    if not LOCK.exists():
        raise SystemExit(f"ABORT: missing try1 lock {LOCK}")
    if sha(START) != sha(LOCK):
        START.write_bytes(LOCK.read_bytes())
        print(f"synced ACTIVE start <- {LOCK.name}", flush=True)
    if BANNED_ORE.exists() and sha(START) == sha(BANNED_ORE):
        raise SystemExit("ABORT: active start is banned face-on ore+lamp DNA")
    if sha(START) != sha(LOCK):
        raise SystemExit("ABORT: active start != try1 nolamp lock")

    for need in (
        "NO PRACTICAL TABLE LAMP",
        "shade-cup",
        "WINDOW",
        "OFF-WORLD",
        "molten bead",
        "mid-crown",
        "1869",
        "OTS",
        "4b8ed25",
        "LOCKED TRIPOD",
    ):
        if need.lower() not in PROMPT.lower():
            raise SystemExit(f"ABORT: prompt missing {need}")

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

        tmp = Path("/tmp/hos_v20_06_try1_stub.mp4")
        if tmp.exists():
            tmp.unlink()
        info: dict = {}
        try:
            info = flow.generate_clip(
                page,
                PROMPT,
                tmp,
                model=MODEL,
                start_frame=START,
                timeout_s=70,
                attempts=1,
                scenery_only=True,
            )
        except Exception as e:
            info = {
                "error": str(e),
                "project_url": getattr(page, "_orbit_flow_project_url", None) or (page.url or ""),
            }
            print(f"submit note: {e}", flush=True)

        project_url = (
            info.get("project_url")
            or info.get("url")
            or getattr(page, "_orbit_flow_project_url", None)
            or page.url
            or ""
        )
        project_url = str(project_url).split("?")[0].rstrip("/")
        out = {
            "plate": "06_explorer_leaves_gap",
            "try": 1,
            "project_url": project_url,
            "info": {k: v for k, v in info.items() if k != "path"},
            "start": str(START),
            "start_sha256": sha(START),
            "start_dna": (
                "try1 OTS/back Explorer + 1869 card-desk + soft glow vacant gap; "
                "CLEAN=window/off-world bounce ONLY; ZERO practical lamp; "
                "crop-only from v10 back DNA (paint banned); plate-library 4b8ed25"
            ),
            "plate_library_lock_sha": "4b8ed25",
            "model": MODEL,
            "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "auth": auth,
            "paint": "banned",
            "assemble": False,
            "parent": "09b CLEAN LIGHT parked after try8-13 lamp invent STOP; next=06",
        }
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(out, indent=2) + "\n")
        print(json.dumps(out, indent=2), flush=True)
        if "/project/" not in project_url:
            raise SystemExit("no project url after submit")


if __name__ == "__main__":
    main()
