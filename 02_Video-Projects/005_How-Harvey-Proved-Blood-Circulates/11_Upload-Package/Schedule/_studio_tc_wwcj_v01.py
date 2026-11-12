#!/usr/bin/env python3
"""J0101: HOS 005 Test & Compare on the scheduled long `wwcjcFfC-5M`. Thumbnail only, A v02 (live main) + B v02,
one title: the package Ben signed off on 2 Oct, which went on the stray `0IfXGSX7Ypw` that day.

Stops without touching anything if Studio says a test already exists ("Run a new test? ... deleted"): never Continue.

  python3 _studio_tc_wwcj_v01.py            # dry run: build the test, screenshot, close unsaved
  python3 _studio_tc_wwcj_v01.py --commit   # Set test + Save, re-read Audience/Visibility, reopen and verify
"""
from __future__ import annotations

import hashlib
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
step.VID = VID
step.ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/J0101_2026-10-10_005_wwcj"
FILM = HERE.parents[1]
THUMB_B = FILM / "08_Thumbnail/Selected/hos_005_thumb_B_it_goes_round_v02.jpg"
THUMB_B_SHA = "17672532bf5d6f5f9f62205e75c5dc2b744b93d40139df3d3f0204872deb9c6a"
TITLE = "The Tied Arm That Proved Your Blood Circulates"
OUT = HERE.parent / "evidence_2026-10-10_studio"


def main():
    commit = "--commit" in sys.argv
    assert hashlib.sha256(THUMB_B.read_bytes()).hexdigest() == THUMB_B_SHA
    tag = "commit" if commit else "dry"
    res = {"vid": VID, "commit": commit, "steps": []}
    n = [0]

    def snap(page, label):
        n[0] += 1
        res["steps"].append({"shot": step.shot(page, f"tc_{tag}_{n[0]:02d}_{label}")})

    def click(page, name):
        loc = page.get_by_role("button", name=name, exact=True).filter(visible=True)
        if loc.count() == 0:
            return False
        loc.first.click(timeout=8000)
        page.wait_for_timeout(3500)
        return True

    def write():
        res["at"] = datetime.now(step.LONDON).isoformat(timespec="seconds")
        OUT.mkdir(parents=True, exist_ok=True)
        out = OUT / f"TC_{tag.upper()}_RESULT.json"
        out.write_text(json.dumps(res, indent=1, ensure_ascii=False, default=str))
        print("wrote", out, flush=True)

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(step.CDP, timeout=60000)
        page = step.page_for(browser)
        page.set_default_timeout(60000)
        if not step.sw.ensure_hos(page, step.u)["ok"]:
            raise SystemExit("not on HOS channel; stop")
        page.goto(f"https://studio.youtube.com/video/{VID}/edit", wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(4500)
        step.u.dismiss(page)
        assert VID in page.url, page.url
        res["av_start"] = step.report(page)
        page.evaluate("window.scrollTo(0,0)")
        click(page, "A/B Testing")
        if "Run a new test?" in page.inner_text("body"):
            snap(page, "existing_test")
            click(page, "Cancel")
            res["stop"] = "a test already exists on this video; Cancelled, nothing changed"
            print("STOP", res["stop"], flush=True)
            write()
            return
        click(page, "New test")
        if "Run a new test?" in page.inner_text("body"):
            snap(page, "existing_test")
            click(page, "Cancel")
            res["stop"] = "a test already exists on this video; Cancelled, nothing changed"
            print("STOP", res["stop"], flush=True)
            write()
            return
        page.locator("ytcp-chip").filter(has_text="Thumbnail only").first.click()
        page.wait_for_timeout(2000)
        snap(page, "mode")
        with page.expect_file_chooser() as fc:
            page.locator('[aria-label="Upload thumbnail 2"]').first.click()
        fc.value.set_files(str(THUMB_B))
        page.wait_for_timeout(8000)
        dom = page.evaluate(step.ts.DOM_JS)
        res["uploaded_slots"] = [d["aria"] for d in dom if d["aria"].startswith("Uploaded thumbnail")]
        res["upload_slots_left"] = [d["aria"] for d in dom if d["aria"].startswith("Upload thumbnail")]
        set_btn = page.get_by_role("button", name="Set test", exact=True).filter(visible=True).first
        res["set_enabled"] = set_btn.evaluate("el => !(el.disabled || el.getAttribute('aria-disabled')==='true')")
        body = page.inner_text("body")
        res["body_title_ok"] = TITLE in body
        res["ready"] = "Thumbnail test ready" in body
        snap(page, "filled")
        print(json.dumps({k: res[k] for k in ("uploaded_slots", "upload_slots_left", "set_enabled", "body_title_ok", "ready")}), flush=True)
        ok = (res["set_enabled"] and res["ready"] and res["body_title_ok"]
              and "Upload thumbnail 2" not in res["upload_slots_left"])
        if commit and ok:
            set_btn.click()
            page.wait_for_timeout(3000)
            snap(page, "set")
            res["save"] = step.u.page_save(page)
            page.wait_for_timeout(5000)
            res["av_after_save"] = step.report(page)
            page.goto(f"https://studio.youtube.com/video/{VID}/edit", wait_until="domcontentloaded", timeout=120000)
            page.wait_for_timeout(4500)
            step.u.dismiss(page)
            res["av_reopen"] = step.report(page)
            page.evaluate("window.scrollTo(0,0)")
            step.sw.scroll_find(page, r"Thumbnail")
            page.wait_for_timeout(1500)
            snap(page, "verify_thumbnail_panel")
            res["verify_text"] = page.inner_text("body")[:4000]
        elif commit:
            res["stop"] = "setup not as expected; nothing saved"
            print("STOP", res["stop"], flush=True)
        if not commit or res.get("stop"):
            page.keyboard.press("Escape")
            page.wait_for_timeout(1000)
            page.evaluate(step.ts.CLICK_JS, "Undo changes")
    write()


if __name__ == "__main__":
    main()
