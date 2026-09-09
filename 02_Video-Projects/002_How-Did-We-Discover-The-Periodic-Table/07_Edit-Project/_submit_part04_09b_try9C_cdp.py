#!/usr/bin/env python3
"""Dedicated 09b_risk_hold try9C submit on live Mini CDP — cardless moon DNA, CLEAN LAMP (no lava drip)."""
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
START = PROJ / "04_Generated-Clips/part04/refs/v20_start_frames/09b_risk_hold_start_v20.jpg"
LOCK = PROJ / "04_Generated-Clips/part04/refs/v20_start_frames/09b_risk_hold_start_v20_try9C_cardless_t0.jpg"
KEEP_TRY8 = PROJ / "04_Generated-Clips/part04/refs/v20_start_frames/09b_risk_hold_start_v20_try8_KEEP_cf182dc.jpg"
FORBIDDEN_FLAT = "2a651abc673e719af8f6647f264da28a45d41950473489193c72f9a0c4481182"
OUT = PROJ / "07_Edit-Project/_qa_part04_v20_flow/submit_09b_risk_hold_try9C.json"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL") or "Veo 3.1 - Fast"
REQUIRED_EMAIL = "benoats@googlemail.com"

_mint = (Path(__file__).resolve().parent / "_mint_part04_flow_v20.py").read_text()
_m = re.search(r"(STYLE = [\s\S]*?PROMPTS = \{[\s\S]*?\n\})\n\n\ndef ", _mint)
if not _m:
    # fallback: PROMPTS may be named differently in some revisions
    _m = re.search(r"(STYLE = [\s\S]*?PROMPTS\s*=\s*\{[\s\S]*?\n\})\n\n\ndef ", _mint)
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
    if REQUIRED_EMAIL.lower() not in blob and "benoats@googlemail.com" not in blob:
        # soft: Flow home sometimes hides email until account chip opens
        print("WARN: email not visible in DOM yet; continuing if ULTRA present", flush=True)
    if "ultra" not in blob:
        raise SystemExit("STOP_TO_COS BLOCKED_AUTH: ULTRA badge missing")
    return {"ultra": True, "email_hint": REQUIRED_EMAIL in blob}


def main() -> None:
    if not START.exists():
        raise SystemExit(f"missing {START}")
    s = sha(START)
    if s == FORBIDDEN_FLAT:
        raise SystemExit("ABORT: active start is try6/7 flat DNA")
    if KEEP_TRY8.exists() and s == sha(KEEP_TRY8):
        raise SystemExit(
            "ABORT: active start still try8 KEEP cf182dc (drip baked under shade) — need try9 nodrip lock"
        )
    if LOCK.exists() and s != sha(LOCK):
        raise SystemExit("ABORT: active start != try9C t=0.00 cardless nodrip lock")
    bans = ("lava drip", "molten teardrop", "molten bead", "fire spit", "CARDLESS")
    missing = [b for b in bans if b.lower() not in PROMPT.lower()]
    if missing:
        raise SystemExit(f"ABORT: prompt missing bans {missing}")
    if "Empty Chairs" not in PROMPT and "Empty chairs" not in PROMPT:
        raise SystemExit("ABORT: prompt must allow soft Empty Chairs panel")

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

        tmp = Path("/tmp/hos_v20_09b_try9C_stub.mp4")
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
            "try": "9B",
            "project_url": project_url,
            "info": {k: v for k, v in info.items() if k != "path"},
            "start": str(START),
            "start_sha256": s,
            "start_dna": "try9C alternate cardless KEEP from v01 empty-chair moon t=0.00 (nodrip); NOT try8 KEEP cf182dc drip-baked; NOT flat 2a651abc",
            "model": MODEL,
            "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "auth": auth,
            "prompt_has_lava_drip_ban": True,
            "prompt_has_molten_teardrop_ban": True,
            "prompt_has_fire_spit_ban": True,
            "prompt_has_cardless": True,
            "prompt_allows_soft_empty_chairs": True,
            "parent_try8_uat": "HARD FAIL CLEAN LIGHT — lamp lava drip / molten teardrop under shade continuous ~t1–t8; flats CLEARED",
            "paint": "banned",
        }
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(out, indent=2) + "\n")
        print(json.dumps(out, indent=2), flush=True)
        if "/project/" not in project_url:
            raise SystemExit("no project url after submit")


if __name__ == "__main__":
    main()
