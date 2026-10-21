#!/usr/bin/env python3
"""J0101 read-only: what's set on the scheduled 005 long `wwcjcFfC-5M` (thumbnail, Test & Compare, end screen, cards).

Never saves. Never presses Continue on "Run a new test?". Screenshots go to the Mini's artifacts folder,
the text summary to evidence_2026-10-10_studio/READ_<label>.json.

  python3 _studio_read_wwcj_v01.py [label]
"""
from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
_s = importlib.util.spec_from_file_location("step", HERE / "_studio_step_v01.py")
step = importlib.util.module_from_spec(_s)
_s.loader.exec_module(step)

VID = "wwcjcFfC-5M"
STRAY = "0IfXGSX7Ypw"
step.VID = VID
step.ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/J0101_2026-10-10_005_wwcj"
OUT = HERE.parent / "evidence_2026-10-10_studio"


def main():
    label = sys.argv[1] if len(sys.argv) > 1 else "before"
    res = {"vid": VID, "label": label}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(step.CDP, timeout=60000)
        page = step.page_for(browser)
        page.set_default_timeout(60000)
        hos = step.sw.ensure_hos(page, step.u)
        res["hos_ok"] = hos["ok"]
        if not hos["ok"]:
            raise SystemExit("not on HOS channel; stop")
        page.goto(f"https://studio.youtube.com/video/{VID}/edit", wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(5000)
        step.u.dismiss(page)
        assert VID in page.url, page.url
        res["av"] = step.report(page)
        page.evaluate("window.scrollTo(0,0)")
        res["shot_top"] = step.shot(page, f"{label}_01_top")
        body = page.inner_text("body")
        res["body_head"] = body[:3500]
        res["has_ab_running_text"] = [k for k in ("Ineligible", "Test & compare", "A/B test", "Thumbnail test", "Running")
                                      if k in body]
        res["dom"] = [d for d in page.evaluate(step.ts.DOM_JS)
                      if any(w in (d.get("aria") or "") for w in ("humbnail", "A/B", "End screen", "Cards", "test"))]
        step.sw.scroll_find(page, r"End screen|Cards")
        page.wait_for_timeout(1500)
        res["shot_side"] = step.shot(page, f"{label}_02_endscreen_cards")
        body = page.inner_text("body")
        i = body.find("End screen")
        res["endscreen_cards_text"] = body[max(0, i - 200): i + 800] if i >= 0 else ""
        res["at"] = datetime.now(step.LONDON).isoformat(timespec="seconds")
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / f"READ_{label}.json"
    out.write_text(json.dumps(res, indent=1, ensure_ascii=False, default=str))
    print("wrote", out)


if __name__ == "__main__":
    main()
