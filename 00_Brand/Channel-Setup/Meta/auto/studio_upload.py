#!/usr/bin/env python3
"""
Orbit Meta Business Suite CDP client — post one Reel via Chrome.

Fallback when Graph API credentials / App Review are not ready.
Posts cross-post targets depending on what's selected in the logged-in Suite
session (Facebook Page + Instagram professional).
"""
from __future__ import annotations

import re
import time
from pathlib import Path

import sys
from pathlib import Path as _Path

_AUTO = _Path(__file__).resolve().parent
if str(_AUTO) not in sys.path:
    sys.path.insert(0, str(_AUTO))

from playwright.sync_api import Page, sync_playwright

from _sib import load

config = load("config")

COMPOSER = "https://business.facebook.com/latest/reels_composer"
CONTENT = "https://business.facebook.com/latest/content_calendar"


def body(page: Page) -> str:
    try:
        return page.inner_text("body")
    except Exception:
        return ""


def click_button(page: Page, *labels: str) -> bool:
    for label in labels:
        try:
            b = page.get_by_role("button", name=re.compile(rf"^{re.escape(label)}$", re.I))
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=4000)
                return True
        except Exception:
            pass
        try:
            loc = page.locator(f'button:has-text("{label}")').first
            if loc.count() and loc.is_visible():
                loc.click(force=True, timeout=4000)
                return True
        except Exception:
            pass
    return False


def dismiss_modals(page: Page) -> None:
    for label in ("Not now", "Close", "Got it", "Dismiss", "Skip", "Cancel"):
        click_button(page, label)


def fill_caption(page: Page, caption: str) -> bool:
    selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[aria-label*="caption" i][contenteditable="true"]',
        'div[aria-label*="Write" i][contenteditable="true"]',
        'textarea[placeholder*="caption" i]',
        'textarea[aria-label*="caption" i]',
    ]
    for sel in selectors:
        try:
            el = page.locator(sel).first
            if not el.count():
                continue
            el.click(force=True, timeout=4000)
            page.wait_for_timeout(200)
            page.keyboard.press("Meta+a")
            page.keyboard.press("Backspace")
            page.keyboard.type(caption[:2100], delay=2)
            return True
        except Exception:
            continue
    return False


def wait_upload_ready(page: Page, timeout_s: float = 180) -> bool:
    end = time.time() + timeout_s
    while time.time() < end:
        dismiss_modals(page)
        text = body(page).lower()
        if any(
            x in text
            for x in (
                "share reel",
                "publish",
                "next",
                "add a caption",
                "write a caption",
                "reel details",
            )
        ):
            # Prefer presence of caption box or Share/Publish
            if page.locator('div[contenteditable="true"], textarea').count():
                return True
            if page.get_by_role("button", name=re.compile(r"Share|Publish|Next", re.I)).count():
                return True
        page.wait_for_timeout(1000)
    return False


def click_publish(page: Page) -> bool:
    for label in ("Share", "Publish", "Post", "Next"):
        if click_button(page, label):
            page.wait_for_timeout(800)
            # Sometimes Next then Share
            if label == "Next":
                continue
            return True
    return False


def confirm_posted(page: Page, needle: str, timeout_s: float = 90) -> bool:
    end = time.time() + timeout_s
    needle_l = needle.lower()
    while time.time() < end:
        text = body(page).lower()
        if any(
            x in text
            for x in (
                "reel shared",
                "reel published",
                "your reel is shared",
                "posted",
                "is live",
            )
        ):
            return True
        if needle_l and needle_l in text:
            return True
        page.wait_for_timeout(1500)
    try:
        page.goto(CONTENT, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(4000)
        return needle_l in body(page).lower()
    except Exception:
        return False


def post_short(
    *,
    video_path: Path,
    caption: str,
    confirm_needle: str | None = None,
    audit_dir: Path | None = None,
    page: Page | None = None,
    port: int | None = None,
) -> dict:
    video_path = Path(video_path)
    needle = confirm_needle or caption[:48]
    creds = config.load_credentials()
    port = int(port or creds.get("cdp_port") or 9223)
    out: dict = {
        "status": "started",
        "method": "cdp",
        "file": str(video_path),
        "caption": caption,
        "needle": needle,
        "port": port,
    }
    if not video_path.exists():
        out["status"] = "missing_file"
        return out

    own_pw = page is None
    pw = None
    if own_pw:
        pw = sync_playwright().start()
        browser = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
        page = browser.contexts[0].new_page()
        page.bring_to_front()

    assert page is not None
    try:
        page.goto(COMPOSER, wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(2000)
        dismiss_modals(page)

        file_input = page.locator('input[type="file"]').first
        if not file_input.count():
            # Try click upload affordance then re-query
            click_button(page, "Add video", "Upload", "Select video")
            page.wait_for_timeout(1000)
            file_input = page.locator('input[type="file"]').first

        if not file_input.count():
            out["status"] = "no_file_input"
            out["url"] = page.url
            if audit_dir:
                audit_dir.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(audit_dir / f"no_input_{video_path.stem}.png"))
            return out

        file_input.set_input_files(str(video_path))
        if not wait_upload_ready(page):
            out["status"] = "upload_timeout"
            out["url"] = page.url
            return out

        out["caption_ok"] = fill_caption(page, caption)
        if audit_dir:
            audit_dir.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(audit_dir / f"before_{video_path.stem}.png"))

        ok = False
        for attempt in range(5):
            click_publish(page)
            page.wait_for_timeout(1200)
            dismiss_modals(page)
            if confirm_posted(page, needle, timeout_s=40):
                ok = True
                break
            out[f"attempt_{attempt + 1}"] = "not_confirmed"

        if audit_dir:
            page.screenshot(path=str(audit_dir / f"after_{video_path.stem}.png"))

        # CDP path posts both destinations when Suite cross-post is enabled in session
        plat = {
            "instagram": {"status": "ok" if ok else "unconfirmed", "method": "cdp"},
            "facebook": {"status": "ok" if ok else "unconfirmed", "method": "cdp"},
        }
        out["platforms"] = plat
        out["status"] = "ok" if ok else "unconfirmed"
        out["url"] = page.url
        return out
    finally:
        if own_pw:
            try:
                if page:
                    page.close()
            except Exception:
                pass
            if pw:
                pw.stop()
