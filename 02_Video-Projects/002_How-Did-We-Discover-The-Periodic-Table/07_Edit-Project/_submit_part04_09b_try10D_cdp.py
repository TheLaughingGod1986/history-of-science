#!/usr/bin/env python3
"""Dedicated 09b_risk_hold try10D submit on live Mini CDP.

DNA: cropL931 nocup (lamp OFF-FRAME) + prompt ban inventing any desk-lamp prop.
Bible 8ddbf99 — NEVER soft-pass molten bead under shade cup. Paint banned. No assemble.
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
LOCK = REF / "09b_risk_hold_start_v20_try10D_nolamp_tightL.jpg"
KEEP_TRY8 = REF / "09b_risk_hold_start_v20_try8_KEEP_cf182dc.jpg"
TRY10A = REF / "09b_risk_hold_start_v20_try10_nocup_sidelit.jpg"
TRY10B = REF / "09b_risk_hold_start_v20_try10B_nocup_opaque_glow.jpg"
FORBIDDEN_FLAT = "2a651abc673e719af8f6647f264da28a45d41950473489193c72f9a0c4481182"
OUT = PROJ / "07_Edit-Project/_qa_part04_v20_flow/submit_09b_risk_hold_try10D.json"
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
    if not START.exists():
        raise SystemExit(f"missing {START}")
    if not LOCK.exists():
        raise SystemExit(f"ABORT: missing try10D lock {LOCK}")
    s = sha(START)
    if s == FORBIDDEN_FLAT:
        raise SystemExit("ABORT: active start is flat DNA")
    if KEEP_TRY8.exists() and s == sha(KEEP_TRY8):
        raise SystemExit("ABORT: try8 KEEP drip-baked DNA")
    if TRY10A.exists() and s == sha(TRY10A):
        raise SystemExit("ABORT: try10A DNA (cup returned)")
    if s != sha(LOCK):
        raise SystemExit("ABORT: active start != try10D lock")
    # try10D may share bytes with try10B cropL931 — that is intentional (same nocup DNA)
    for ban in (
        "molten bead",
        "shade cup",
        "OFF-FRAME",
        "CARDLESS",
        "8ddbf99",
        "THERE IS NO DESK LAMP",
        "LOCKED FRAMING",
        "try10C",
    ):
        if ban.lower() not in PROMPT.lower():
            raise SystemExit(f"ABORT: prompt missing {ban}")

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

        tmp = Path("/tmp/hos_v20_09b_try10D_stub.mp4")
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
            "try": "10D",
            "project_url": project_url,
            "info": {k: v for k, v in info.items() if k != "path"},
            "start": str(START),
            "start_sha256": s,
            "start_dna": (
                "try10D nolamp tightL: try9C cardless moon empty-chair cropL931+8%L — "
                "NO desk-lamp prop; LOCKED FRAMING no widen/pan-left; warm OFF-SCREEN bounce + moonlight; "
                "bible 8ddbf99; NOT try10A/B/C; paint banned"
            ),
            "model": MODEL,
            "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "auth": auth,
            "parent_try9_uat": "FORMAL HARD FAIL molten bead — bible 8ddbf99 (contact + t3.8/t5.8/t7.3)",
            "parent_try10A": "SELF_REJECT — open shade cup + drip-like protrusion mid-clip",
            "parent_try10C": "SELF_REJECT — Veo widened left, invented open shade cup + molten bead mid-clip",
            "parent_try10B": "SELF_REJECT — Veo invented open shade cup + molten bead mid-clip",
            "paint": "banned",
            "assemble": False,
        }
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(out, indent=2) + "\n")
        print(json.dumps(out, indent=2), flush=True)
        if "/project/" not in project_url:
            raise SystemExit("no project url after submit")


if __name__ == "__main__":
    main()
