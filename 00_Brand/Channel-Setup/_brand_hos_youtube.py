#!/usr/bin/env python3
"""Brand the History of Science YouTube channel (never Orbit With Ben).

Finds @HistoryOfScience in the channel switcher (or creates it if missing),
applies Explorer avatar/banner/About copy, writes CHANNEL_META.json.

  python3 00_Brand/Channel-Setup/_brand_hos_youtube.py

First run opens Chromium for Google sign-in as benoats86@gmail.com.
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
SETUP = Path(__file__).resolve().parent
PROFILE = SETUP / ".playwright-hos-youtube-profile"
AVATAR = SETUP / "avatar_800x800.png"
BANNER = SETUP / "banner_2560x1440.png"
DESC = (SETUP / "channel_description.txt").read_text().strip()
KEYWORDS = (SETUP / "channel_keywords.txt").read_text().strip()
META_PATH = SETUP / "CHANNEL_META.json"
RESULT = SETUP / "HOS_BRAND_RESULT.json"
AUDIT = SETUP / "audit"
ORBIT_CID = "UC_esArsDKd3GJvOkeO0DUog"
OPPTIAI = "UCXRVwrCxXpN_o9gvuHPKAPQ"
DISPLAY = "History of Science"
HANDLE = "HistoryOfScience"


def shot(page, name: str) -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(AUDIT / f"hos_{name}.png"), full_page=False)


def extract_cid(url: str) -> str | None:
    m = re.search(r"/channel/(UC[\w-]{20,})", url)
    return m.group(1) if m else None


def dismiss(page) -> None:
    for label in ("Continue", "Got it", "Dismiss", "Not now", "OK", "Close", "I agree"):
        try:
            b = page.get_by_role("button", name=label, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=1200)
                page.wait_for_timeout(500)
        except Exception:
            pass


def abort_if_wrong_channel(cid: str | None) -> None:
    if cid in {ORBIT_CID, OPPTIAI}:
        raise SystemExit(
            f"Refusing to brand channel {cid} — that is Orbit With Ben or OpptiAI."
        )


def publish(page, result: dict, key: str) -> None:
    btn = page.get_by_role("button", name="Publish", exact=True)
    if btn.count() and btn.first.is_enabled():
        btn.first.click(force=True)
        page.wait_for_timeout(3500)
        result[key] = True
        dismiss(page)
    else:
        result[key] = False


def switch_or_create(page, result: dict) -> str:
    page.goto("https://www.youtube.com/channel_switcher", wait_until="domcontentloaded")
    page.wait_for_timeout(3500)
    dismiss(page)
    shot(page, "01_switcher")
    body = page.locator("body").inner_text()
    result["switcher_snip"] = body[:2500]

    if "History of Science" in body or "history of science" in body.lower():
        page.get_by_text(re.compile(r"History of Science", re.I)).first.click(force=True)
        page.wait_for_timeout(4000)
        result["switched_existing"] = True
    else:
        page.get_by_text("Create a channel", exact=True).first.click(force=True)
        page.wait_for_timeout(2500)
        dlg = page.locator("[role='dialog']")
        dlg.wait_for(state="visible", timeout=15000)
        name = page.locator("input").nth(0)
        handle = page.locator("input").nth(1)
        name.click()
        page.keyboard.press("Meta+A")
        page.keyboard.insert_text(DISPLAY)
        handle.click()
        page.keyboard.press("Meta+A")
        page.keyboard.insert_text(HANDLE)
        page.wait_for_timeout(800)
        shot(page, "01b_create_dialog")
        page.get_by_role("button", name=re.compile(r"^Create", re.I)).first.click(force=True)
        page.wait_for_timeout(5000)
        result["created_new"] = True

    page.goto("https://studio.youtube.com", wait_until="domcontentloaded")
    page.wait_for_timeout(4000)
    dismiss(page)
    cid = extract_cid(page.url)
    abort_if_wrong_channel(cid)
    if not cid:
        page.goto("https://studio.youtube.com/channel/", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        cid = extract_cid(page.url)
        abort_if_wrong_channel(cid)
    if not cid:
        raise SystemExit("Could not read a UC… channel id from Studio.")
    result["channel_id"] = cid
    result["studio_url"] = f"https://studio.youtube.com/channel/{cid}"
    return cid


def apply_branding(page, cid: str, result: dict) -> None:
    page.goto(
        f"https://studio.youtube.com/channel/{cid}/editing/profile",
        wait_until="domcontentloaded",
    )
    page.wait_for_timeout(4000)
    dismiss(page)
    shot(page, "02_profile")

    try:
        inputs = page.locator('input[type="file"]')
        if inputs.count() >= 1:
            inputs.nth(0).set_input_files(str(BANNER))
            page.wait_for_timeout(3000)
            dismiss(page)
            for label in ("Done", "Apply", "Confirm", "Save"):
                b = page.get_by_role("button", name=label, exact=True)
                if b.count() and b.first.is_visible() and b.first.is_enabled():
                    b.first.click(force=True)
                    page.wait_for_timeout(1000)
            result["banner_uploaded"] = True
        shot(page, "03_banner")
    except Exception as e:
        result["banner_error"] = str(e)
        shot(page, "03_banner_err")

    try:
        inputs = page.locator('input[type="file"]')
        if inputs.count() >= 2:
            inputs.nth(1).set_input_files(str(AVATAR))
            page.wait_for_timeout(3000)
            dismiss(page)
            for label in ("Done", "Apply", "Confirm", "Save"):
                b = page.get_by_role("button", name=label, exact=True)
                if b.count() and b.first.is_visible() and b.first.is_enabled():
                    b.first.click(force=True)
                    page.wait_for_timeout(1000)
            result["avatar_uploaded"] = True
        shot(page, "04_avatar")
    except Exception as e:
        result["avatar_error"] = str(e)
        shot(page, "04_avatar_err")

    try:
        name = page.locator('#textbox[aria-label*="Name" i], input[aria-label*="Name" i]')
        if not name.count():
            name = page.locator(
                "xpath=//*[normalize-space()='Name']/following::div[@id='textbox' or self::input][1]"
            )
        if name.count():
            name.first.click(force=True)
            page.keyboard.press("Meta+A")
            page.keyboard.insert_text(DISPLAY)
            result["name_set"] = DISPLAY
        shot(page, "05_name")
    except Exception as e:
        result["name_error"] = str(e)

    try:
        page.evaluate("window.scrollTo(0, 1400)")
        page.wait_for_timeout(400)
        desc = page.locator('#textbox[aria-label*="Description" i]')
        if not desc.count():
            boxes = page.locator("#textbox")
            desc = boxes.nth(1) if boxes.count() >= 2 else boxes
        if desc.count():
            desc.first.click(force=True)
            page.keyboard.press("Meta+A")
            page.keyboard.insert_text(DESC)
            result["description_set"] = True
        shot(page, "06_desc")
    except Exception as e:
        result["description_error"] = str(e)

    publish(page, result, "profile_published")

    page.goto(
        f"https://studio.youtube.com/channel/{cid}/editing/details",
        wait_until="domcontentloaded",
    )
    page.wait_for_timeout(3000)
    dismiss(page)
    try:
        kw = page.locator('#textbox[aria-label*="keyword" i], textarea[aria-label*="keyword" i]')
        if kw.count():
            kw.first.click(force=True)
            page.keyboard.press("Meta+A")
            page.keyboard.insert_text(KEYWORDS)
            result["keywords_set"] = True
        shot(page, "07_details")
        publish(page, result, "details_published")
    except Exception as e:
        result["keywords_error"] = str(e)
        shot(page, "07_details_err")


def write_meta(cid: str) -> None:
    meta = json.loads(META_PATH.read_text())
    meta["channel_id"] = cid
    meta["studio_url"] = f"https://studio.youtube.com/channel/{cid}"
    meta["public_url"] = f"https://www.youtube.com/channel/{cid}"
    meta["handle"] = f"@{HANDLE}"
    meta["created_at"] = time.strftime("%Y-%m-%d")
    meta["status"] = "branded_pending_verify"
    META_PATH.write_text(json.dumps(meta, indent=2) + "\n")


def main() -> None:
    if not AVATAR.exists() or not BANNER.exists():
        raise SystemExit("Missing avatar_800x800.png or banner_2560x1440.png")
    PROFILE.mkdir(parents=True, exist_ok=True)
    result = {"started_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(PROFILE),
            headless=False,
            viewport={"width": 1400, "height": 1000},
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            cid = switch_or_create(page, result)
            apply_branding(page, cid, result)
            write_meta(cid)
            result["status"] = "ok"
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            shot(page, "99_error")
            raise
        finally:
            result["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
            RESULT.write_text(json.dumps(result, indent=2) + "\n")
            ctx.close()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
