#!/usr/bin/env python3
"""Post + pin the Germs full-film funnel comment on a public Short.

Usage (Playwright Chromium already logged into History of Science):
  python3 _pin_short_funnel_comment_v01.py --id YX2UR1u-JCQ

Do not run against Orbit / Oppti. Zero /go/.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PIN = (ROOT / "Pinned-Comments/germs_shorts_pinned-comment_v01.txt").read_text().strip()
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True, help="YouTube Short id")
    ap.add_argument("--headed", action="store_true")
    args = ap.parse_args()

    url = f"https://www.youtube.com/shorts/{args.id}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.headed, channel="chrome")
        context = browser.new_context()
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(2500)
        page.get_by_role("button", name="View comments").click()
        page.wait_for_timeout(1200)
        page.get_by_text("Add a comment").first.click()
        page.wait_for_timeout(400)
        page.locator("#contenteditable-root").first.fill(PIN)
        page.get_by_role("button", name="Comment", exact=True).click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="Action menu").first.click()
        page.wait_for_timeout(400)
        page.get_by_role("menu").locator("a").filter(has_text="Pin").click()
        page.wait_for_timeout(400)
        page.get_by_role("dialog").get_by_role("button", name="Pin").click()
        page.wait_for_timeout(1500)
        assert "Pinned by" in page.inner_text("body")
        print(f"PINNED ok {args.id}")
        browser.close()


if __name__ == "__main__":
    main()
