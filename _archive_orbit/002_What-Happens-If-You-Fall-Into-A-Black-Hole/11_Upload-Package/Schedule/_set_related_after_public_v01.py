#!/usr/bin/env python3
"""Set Related video on all Video 002 Shorts → long-form AFTER long is PUBLIC.

Studio Related picker only lists PUBLIC videos. Run after:
  Thu 6 Aug 2026 19:00 UK (or once n7CbJrOCnU0 is Public).

Usage:
  python _set_related_after_public_v01.py
"""
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
INDEX = json.loads((ROOT / "10_Shorts/SHORTS_UPLOAD_INDEX.json").read_text())
AUDIT = ROOT / "11_Upload-Package/Schedule/_related_after_public"
OUT = ROOT / "11_Upload-Package/Schedule/blackhole_related_after_public_result.json"
LONG_ID = "n7CbJrOCnU0"
LONG_TITLE = "What Happens If You Fall Into a Black Hole"


def skip(page) -> None:
    try:
        page.get_by_role("link", name=re.compile(r"Skip", re.I)).click(timeout=1000)
    except Exception:
        pass


def dismiss(page) -> None:
    for name in ("Close", "Dismiss", "Got it"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=800)
        except Exception:
            pass


def save(page) -> bool:
    try:
        b = page.get_by_role("button", name="Save", exact=True)
        if b.count() and b.first.is_enabled():
            b.first.click(force=True)
            page.wait_for_timeout(2500)
            return True
    except Exception:
        pass
    return False


def set_related(page, sid: str, num: str) -> dict:
    r: dict = {"id": sid, "num": num, "ok": False}
    page.goto(
        f"https://studio.youtube.com/video/{sid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    skip(page)
    dismiss(page)

    picker = page.locator("ytcp-shorts-content-links-picker")
    if picker.count():
        picker.first.scroll_into_view_if_needed()
        picker.first.click(force=True)
    else:
        page.get_by_text("Related video", exact=True).first.click(force=True)
    page.wait_for_timeout(1500)
    try:
        page.locator("ytcp-video-pick-dialog").wait_for(timeout=15000)
    except Exception:
        r["error"] = "no_dialog"
        return r

    search = page.locator("ytcp-video-pick-dialog #search-yours")
    if not search.count():
        search = page.get_by_placeholder(re.compile(r"Search your videos", re.I))
    for q in (LONG_TITLE, LONG_ID, "History of Science"):
        search.first.fill(q)
        page.wait_for_timeout(2500)
        body = page.locator("ytcp-video-pick-dialog").inner_text()
        if "No matching results" not in body:
            break
    else:
        r["error"] = "not_public_yet"
        page.keyboard.press("Escape")
        return r

    cells = page.locator("ytcp-video-pick-dialog ytcp-video-list-cell-video")
    if not cells.count():
        cells = page.locator("ytcp-video-pick-dialog ytcp-entity-card")
    for i in range(cells.count()):
        t = cells.nth(i).inner_text()
        is_short = bool(re.search(r"\b0:\d{2}\b", t)) and not re.search(
            r"\b1[0-9]:\d{2}\b", t
        )
        if (LONG_ID in t or "Black Hole" in t or "Fall Into" in t) and not is_short:
            cells.nth(i).click(force=True)
            r["picked"] = t[:160]
            break
    else:
        r["error"] = "no_cell"
        page.keyboard.press("Escape")
        return r

    page.wait_for_timeout(800)
    for name in ("Done", "Select", "Save"):
        b = page.get_by_role("button", name=name, exact=True)
        if b.count() and b.first.is_visible() and b.first.is_enabled():
            b.first.click(force=True)
            page.wait_for_timeout(800)
            break
    r["saved"] = save(page)

    page.goto(f"https://studio.youtube.com/video/{sid}/edit", wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    body = page.locator("body").inner_text()
    chunk = body.split("Related video", 1)[-1][:250] if "Related video" in body else ""
    r["related_chunk"] = chunk
    r["ok"] = "None" not in chunk[:40] and (
        "Black Hole" in chunk or "Fall Into" in chunk or "Orbit" in chunk
    )
    page.screenshot(path=str(AUDIT / f"rel_{num}.png"))
    return r


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    results = []
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 900},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        # Quick public check
        page.goto(
            f"https://studio.youtube.com/video/{LONG_ID}/edit",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3000)
        body = page.locator("body").inner_text()
        if "Scheduled" in body and "Public" not in body.split("Visibility")[0][-200:]:
            # Still check visibility chip
            if re.search(r"\bScheduled\b", body) and not re.search(
                r"Visibility\s+Public", body
            ):
                print("Long-form still Scheduled — Related picker will be empty.")
                print("Re-run after it goes Public (6 Aug 19:00 UK).")
        for item in INDEX["shorts"]:
            print(f"Related Short {item['id']}…", flush=True)
            r = set_related(page, item["video_id"], item["id"])
            results.append(r)
            print(f"  ok={r.get('ok')} {r.get('error') or r.get('picked','')[:60]}", flush=True)
            OUT.write_text(json.dumps({"shorts": results}, indent=2) + "\n")
        ctx.close()
    ok = all(x.get("ok") for x in results)
    OUT.write_text(json.dumps({"ok": ok, "shorts": results}, indent=2) + "\n")
    print("RESULT", OUT, "ok=", ok)
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
