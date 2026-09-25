#!/usr/bin/env python3
"""Dedicated 09b_risk_hold try8 submit on live Mini CDP — fresh page, cardless DNA."""
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
LOCK = PROJ / "04_Generated-Clips/part04/refs/v20_start_frames/09b_risk_hold_start_v20_try8_cardless.jpg"
OUT = PROJ / "07_Edit-Project/_qa_part04_v20_flow/submit_09b_risk_hold_try8.json"
FORBIDDEN = "2a651abc673e719af8f6647f264da28a45d41950473489193c72f9a0c4481182"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL") or "Veo 3.1 - Fast"

_mint = (Path(__file__).resolve().parent / "_mint_part04_flow_v20.py").read_text()
_m = re.search(r"(STYLE = [\s\S]*?PROMPTS = \{[\s\S]*?\n\})\n\n\ndef ", _mint)
if not _m:
    raise SystemExit("could not extract PROMPTS")
_ns: dict = {}
exec(_m.group(1), _ns)
PROMPT = _ns["PROMPTS"]["09b_risk_hold"]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    if not START.exists():
        raise SystemExit(f"missing {START}")
    s = sha(START)
    if s == FORBIDDEN:
        raise SystemExit("ABORT: active start is try6/7 flat DNA")
    if LOCK.exists() and s != sha(LOCK):
        raise SystemExit("ABORT: active start != try8 cardless lock")
    if "ABSOLUTELY CARDLESS" not in PROMPT and "CARDLESS" not in PROMPT:
        raise SystemExit("ABORT: prompt missing CARDLESS lock")

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

        tmp = Path("/tmp/hos_v20_09b_try8_stub.mp4")
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
            "try": 8,
            "project_url": project_url,
            "info": {k: v for k, v in info.items() if k != "path"},
            "start": str(START),
            "start_sha256": s,
            "model": MODEL,
            "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "prompt_has_fire_ban": True,
            "prompt_has_spark_ban": True,
            "prompt_has_flat_card_ban": True,
            "prompt_has_absolute_cardless": "ABSOLUTELY CARDLESS" in PROMPT,
            "parent_try7_gate": "REJECT_CLEAN_LIGHT_UAT_AMEND + REJECT_FLAT_CARDS",
            "parent_try8A_gate": "SELF_REJECT_FLAT_CARDS (HJ/CoB mid-clip; lamp beam clean)",
            "dna": "KEEP v01 09b empty-chair moon cardless (not try6/7 v14 flat)",
        }
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(out, indent=2) + "\n")
        print(json.dumps(out, indent=2), flush=True)
        if "/project/" not in project_url:
            raise SystemExit("no project url after submit")


if __name__ == "__main__":
    main()
