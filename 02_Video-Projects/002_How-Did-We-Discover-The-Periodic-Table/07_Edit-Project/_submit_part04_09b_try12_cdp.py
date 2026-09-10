#!/usr/bin/env python3
"""Dedicated 09b_risk_hold try12 submit on live Mini CDP.

DNA: RIGHT-CAM / bookshelf-LEFT — NO left desk invent zone.
ZERO desk-lamp/gooseneck/shade/bulb/fixture; CLEAN LIGHT=moon+window spill+soft ambient ONLY
(warm fill behind camera / out of world only). Cardless empty-chair moon KEEP.
Bible 8ddbf99 — NEVER soft-pass molten bead under shade cup. Paint banned. No assemble.
Max 2 starts (A then B). If both invent left fixture → STOP_TO_COS.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
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
START = REF / "09b_risk_hold_start_v20.jpg"
LOCK = REF / "09b_risk_hold_start_v20_try12_rightcam_bookshelfL.jpg"
START_B = REF / "09b_risk_hold_start_v20_try12B_rightcam_tq.jpg"
TRY11 = REF / "09b_risk_hold_start_v20_try11_zerolamp_moonwin.jpg"
TRY10D = REF / "09b_risk_hold_start_v20_try10D_nolamp_tightL.jpg"
KEEP_TRY8 = REF / "09b_risk_hold_start_v20_try8_KEEP_cf182dc.jpg"
TRY10A = REF / "09b_risk_hold_start_v20_try10_nocup_sidelit.jpg"
FORBIDDEN_FLAT = "2a651abc673e719af8f6647f264da28a45d41950473489193c72f9a0c4481182"
OUT_A = PROJ / "07_Edit-Project/_qa_part04_v20_flow/submit_09b_risk_hold_try12.json"
OUT_B = PROJ / "07_Edit-Project/_qa_part04_v20_flow/submit_09b_risk_hold_try12B.json"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL") or "Veo 3.1 - Fast"
REQUIRED_EMAIL = "benoats@googlemail.com"

_mint = (Path(__file__).resolve().parent / "_mint_part04_flow_v20.py").read_text()
_m = re.search(r"(STYLE = [\s\S]*?PROMPTS = \{[\s\S]*?\n\})\n\n\ndef ", _mint)
if not _m:
    raise SystemExit("could not extract PROMPTS from mint")
_ns: dict = {}
exec(_m.group(1), _ns)
PROMPT = _ns["PROMPTS"]["09b_risk_hold"]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


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
            '[aria-label*="Google Account"]',
            'img[alt*="Google Account"]',
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
    which = (os.environ.get("HOS_09B_TRY12_START") or "A").upper().strip()
    if which == "B":
        want = START_B
        out_path = OUT_B
        dna_tag = (
            "try12B RIGHT-CAM tq bookshelfL: H-FLIP try11 zerolamp moon KEEP cropR06 — "
            "BOOKSHELVES LEFT / moon+empty-chair RIGHT; ZERO fixture; CLEAN=moon+window+ambient "
            "(warm behind camera only); LOCKED FRAMING; bible 8ddbf99; Soft Empty Chairs OK; "
            "finished 3D; NOT try10/try11 left-crop family; paint banned"
        )
    else:
        which = "A"
        want = LOCK
        out_path = OUT_A
        dna_tag = (
            "try12A RIGHT-CAM bookshelfL: H-FLIP try11 zerolamp moon KEEP cropR04 — "
            "BOOKSHELVES LEFT / moon+empty-chair RIGHT; ZERO gooseneck/shade/bulb/fixture; "
            "CLEAN LIGHT=moon+window spill+soft ambient ONLY (warm behind camera / out of world); "
            "LOCKED FRAMING; bible 8ddbf99; Soft Empty Chairs OK; finished 3D; NOT try10/try11; paint banned"
        )

    if not START.exists():
        raise SystemExit(f"missing {START}")
    if not want.exists():
        raise SystemExit(f"ABORT: missing try12 start {want}")
    if sha(START) != sha(want):
        START.write_bytes(want.read_bytes())
        print(f"synced ACTIVE start <- {want.name}", flush=True)

    s = sha(START)
    if s == FORBIDDEN_FLAT:
        raise SystemExit("ABORT: active start is flat DNA")
    if KEEP_TRY8.exists() and s == sha(KEEP_TRY8):
        raise SystemExit("ABORT: try8 KEEP drip-baked DNA")
    if TRY10A.exists() and s == sha(TRY10A):
        raise SystemExit("ABORT: try10A DNA (cup returned)")
    if TRY10D.exists() and s == sha(TRY10D):
        raise SystemExit("ABORT: try10D left-crop family")
    if TRY11.exists() and s == sha(TRY11):
        raise SystemExit("ABORT: active start still try11 left-crop family — need try12 rightcam lock")
    if s != sha(want):
        raise SystemExit("ABORT: active start != chosen try12 lock")

    for need in (
        "molten bead",
        "shade cup",
        "CARDLESS",
        "8ddbf99",
        "MOONLIGHT",
        "WINDOW SPILL",
        "ambient",
        "fixture",
        "gooseneck",
        "try11",
        "try12",
        "LOCKED FRAMING",
        "BOOKSHELVES",
        "LEFT",
        "RIGHT",
    ):
        if need.lower() not in PROMPT.lower():
            raise SystemExit(f"ABORT: prompt missing {need}")
    for ban in (
        "OFF-SCREEN / OFF-FRAME wall",
        "OFF-SCREEN bounce",
        "warm bounce from an OFF",
    ):
        if ban.lower() in PROMPT.lower():
            raise SystemExit(f"ABORT: prompt still has bounce cue: {ban}")

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

        tmp = Path(f"/tmp/hos_v20_09b_try12{which}_stub.mp4")
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
            "plate": "09b_risk_hold",
            "try": f"12{which}",
            "project_url": project_url,
            "info": {k: v for k, v in info.items() if k != "path"},
            "start": str(START),
            "start_sha256": s,
            "start_dna": dna_tag,
            "plate_library_lock_sha": "4b8ed25",
            "bible": "8ddbf99",
            "model": MODEL,
            "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "auth": auth,
            "parent_try9_uat": "FORMAL HARD FAIL molten bead — bible 8ddbf99 (contact + t3.8/t5.8/t7.3)",
            "parent_try10A_D": "SELF_REJECT — open shade cup + molten bead mid-clip",
            "parent_try11": "SELF_REJECT — invents desk-lamp fixture mid-clip (shade/gooseneck t5.8/t7.3)",
            "paint": "banned",
            "assemble": False,
            "max_starts": 2,
            "stop_rule": "If A and B both invent left fixture → STOP_TO_COS",
        }
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(out, indent=2) + "\n")
        print(json.dumps(out, indent=2), flush=True)
        if "/project/" not in project_url:
            raise SystemExit("no project url after submit")


if __name__ == "__main__":
    main()
