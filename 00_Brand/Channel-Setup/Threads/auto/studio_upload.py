#!/usr/bin/env python3
"""
Orbit Threads CDP client — post one short as a Threads video via Chrome.

Uses the logged-in @orbitwithben session (port 9222 by default).
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

_AUTO = Path(__file__).resolve().parent
if str(_AUTO) not in sys.path:
    sys.path.insert(0, str(_AUTO))

from playwright.sync_api import Page, sync_playwright

from _sib import load

config = load("config")

HOME = "https://www.threads.com/"


def body(page: Page) -> str:
    try:
        return page.inner_text("body")
    except Exception:
        return ""


def click_text(page: Page, *labels: str) -> bool:
    for label in labels:
        try:
            b = page.get_by_role(
                "button", name=re.compile(rf"^{re.escape(label)}$", re.I)
            )
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=4000)
                return True
        except Exception:
            pass
        try:
            loc = page.get_by_text(label, exact=True)
            if loc.count():
                loc.first.click(force=True, timeout=4000)
                return True
        except Exception:
            pass
    return False


def dismiss(page: Page) -> None:
    for label in ("Not now", "Close", "Got it", "Dismiss", "Skip"):
        click_text(page, label)


def fill_caption(page: Page, caption: str) -> bool:
    selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[aria-label*="Empty text field" i][contenteditable="true"]',
        'div[contenteditable="true"]',
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
            page.keyboard.type(caption[:480], delay=2)
            return True
        except Exception:
            continue
    return False


def _attach_media(page: Page, video_path: Path) -> bool:
    file_input = page.locator("input[type=file]")
    if file_input.count():
        try:
            file_input.first.set_input_files(str(video_path))
            return True
        except Exception:
            pass

    # Open media picker then set files
    page.evaluate(
        """() => {
                          for (const el of document.querySelectorAll('[aria-label],[role=button],button,svg')) {
                            const a=(el.getAttribute('aria-label')||'').toLowerCase();
                            if (/photo|video|media|gallery|attach|image/.test(a)) {
                              (el.closest('button,[role=button]')||el).click();
                              return a;
                            }
                          }
                        }"""
    )
    page.wait_for_timeout(800)
    file_input = page.locator("input[type=file]")
    if not file_input.count():
        return False
    try:
        file_input.first.set_input_files(str(video_path))
        return True
    except Exception as e:
        raise RuntimeError(f"upload_error: {e}") from e


def _click_post(page: Page) -> str | None:
    clicked = page.evaluate(
        """() => {
                  for (const b of document.querySelectorAll('button,[role=button]')) {
                    const t=(b.innerText||'').trim();
                    if (/^(Post|Publish|Share)$/i.test(t)) { b.click(); return t; }
                  }
                  return null;
                }"""
    )
    if clicked:
        return clicked
    if click_text(page, "Post", "Publish", "Share"):
        return "Post"
    return None


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
    port = int(port or creds.get("cdp_port") or 9222)
    username = creds.get("threads_username") or creds.get("username") or "orbitwithben"
    out: dict = {
        "status": "failed",
        "method": "cdp",
        "file": str(video_path),
        "caption": caption,
        "needle": needle,
        "port": port,
    }
    if not video_path.exists():
        out["status"] = "missing_file"
        out["error"] = f"missing file: {video_path}"
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
        page.goto(HOME, wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(2000)
        dismiss(page)

        text = body(page)
        if "Log in" in text and "Edit profile" not in text and f"@{username}" not in text.lower():
            # Soft check — profile nav usually present when logged in
            if "Profile" not in text and "New thread" not in text:
                out["status"] = "threads_not_logged_in"
                if audit_dir:
                    audit_dir.mkdir(parents=True, exist_ok=True)
                    page.screenshot(path=str(audit_dir / "not_logged_in.png"))
                return out

        # Open composer
        opened = click_text(page, "New thread", "Create")
        if not opened:
            try:
                page.get_by_label(
                    "Empty text field. Type to compose a new post."
                ).first.click(timeout=4000)
                opened = True
            except Exception:
                pass
        page.wait_for_timeout(1200)

        try:
            attached = _attach_media(page, video_path)
        except RuntimeError as e:
            out["status"] = "upload_failed"
            out["error"] = str(e)
            if audit_dir:
                audit_dir.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(audit_dir / "upload_fail.png"))
            return out

        if not attached:
            out["status"] = "upload_failed"
            out["error"] = "no file input"
            if audit_dir:
                audit_dir.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(audit_dir / "upload_fail.png"))
            return out

        page.wait_for_timeout(3000)
        out["caption_ok"] = fill_caption(page, caption)
        if audit_dir:
            audit_dir.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(audit_dir / f"before_{video_path.stem}.png"))

        posted = False
        for attempt in range(5):
            label = _click_post(page)
            out[f"attempt_{attempt + 1}"] = label or "no_button"
            page.wait_for_timeout(2500)
            dismiss(page)
            txt = body(page).lower()
            if needle.lower() in txt or "view" in txt or "posted" in txt:
                # Composer usually closes after success
                if page.locator('text=New thread').count() == 0 or "What's new?" in body(page):
                    posted = True
                    break
            # If composer gone, treat as posted click
            if "cancel" not in txt.lower() or page.locator('text=Cancel').count() == 0:
                if label:
                    posted = True
                    break

        if audit_dir:
            page.screenshot(path=str(audit_dir / "after_post.png"))

        # Confirm on profile
        page.goto(
            f"https://www.threads.com/@{username}",
            wait_until="domcontentloaded",
            timeout=90000,
        )
        page.wait_for_timeout(3000)
        confirmed = needle.lower() in body(page).lower()
        out["url"] = page.url
        out["status"] = "ok" if confirmed else ("posted_click" if posted else "unconfirmed")
        if out["status"] == "posted_click":
            # Treat click-success without profile confirm as soft ok for ledger
            out["status"] = "unconfirmed"
        if confirmed:
            out["status"] = "ok"
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
