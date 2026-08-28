#!/usr/bin/env python3
"""Set first comment on long-form only (safe — does not touch description)."""
from __future__ import annotations

import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = "/Users/ben/code/youtube/.playwright-youtube-profile"
ROOT = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "002_What-Happens-If-You-Fall-Into-A-Black-Hole"
)
PINNED = (
    ROOT / "11_Upload-Package/Pinned-Comments/blackhole_long_pinned-comment_v01.txt"
).read_text().strip()
AUDIT = ROOT / "11_Upload-Package/Schedule/_first_comment"
OUT = ROOT / "11_Upload-Package/Schedule/blackhole_first_comment_result.json"
LONG_ID = "n7CbJrOCnU0"


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    r: dict = {"ok": False}
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 1000},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(
            f"https://studio.youtube.com/video/{LONG_ID}/edit",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(4000)
        for _ in range(8):
            page.mouse.wheel(0, 700)
            page.wait_for_timeout(200)
        page.screenshot(path=str(AUDIT / "01_scrolled.png"), full_page=True)
        body = page.locator("body").inner_text()
        r["has_add"] = "Add a first comment" in body
        r["has_first_section"] = "First comment" in body
        r["snippet"] = ""
        if "First comment" in body:
            r["snippet"] = body.split("First comment", 1)[-1][:250]

        if "Add a first comment" in body:
            page.get_by_text("Add a first comment", exact=False).first.click(force=True)
            page.wait_for_timeout(1200)
            # Type into focused field
            page.keyboard.type(PINNED, delay=3)
            page.wait_for_timeout(400)
            page.screenshot(path=str(AUDIT / "02_typed.png"))
            for name in ("Comment", "Save", "Done", "Post"):
                b = page.get_by_role("button", name=name, exact=True)
                if b.count():
                    for i in range(b.count() - 1, -1, -1):
                        try:
                            if b.nth(i).is_visible() and b.nth(i).is_enabled():
                                b.nth(i).click(force=True)
                                page.wait_for_timeout(1500)
                                r["confirm"] = name
                                break
                        except Exception:
                            continue
                    if r.get("confirm"):
                        break
            save = page.get_by_role("button", name="Save", exact=True)
            if save.count() and save.first.is_enabled():
                save.first.click(force=True)
                page.wait_for_timeout(2500)
                r["saved"] = True
            r["ok"] = True
        else:
            # Already has first comment text?
            r["ok"] = "spaghetti" in r["snippet"].lower() or "Orbit" in r["snippet"]
            r["already"] = True

        page.screenshot(path=str(AUDIT / "03_done.png"), full_page=True)
        OUT.write_text(json.dumps(r, indent=2) + "\n")
        print(json.dumps(r, indent=2))
        ctx.close()


if __name__ == "__main__":
    main()
