#!/usr/bin/env python3
"""Pin channel comment on GHZDsiH7L7A via Studio Comments tab (scheduled/private).

CDP :9460. No links. keyboard.type only (no TrustedHTML/innerHTML).
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

PORT = 9460
VID = "GHZDsiH7L7A"
PIN = (
    Path(__file__).resolve().parents[1]
    / "Pinned-Comments/atom_long_pinned-comment_v01.txt"
).read_text().strip()
EV = Path(__file__).resolve().parents[2] / "11_Upload-Package/Schedule/evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos004_studio_phone_uat"
BEN = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"


def log(m: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {m}"
    print(line, flush=True)
    with (EV / "pin_v07.log").open("a") as f:
        f.write(line + "\n")


def dump(n: str, o) -> None:
    t = json.dumps(o, indent=2) + "\n"
    (EV / n).write_text(t)
    (ART / n).write_text(t)


def shot(page, n: str) -> None:
    p = EV / n
    page.screenshot(path=str(p), full_page=False)
    (ART / n).write_bytes(p.read_bytes())
    if n.startswith("BEN_"):
        (BEN / n).write_bytes(p.read_bytes())


def dismiss(page) -> None:
    for _ in range(3):
        page.keyboard.press("Escape")
        page.wait_for_timeout(80)


def clear_filters(page) -> None:
    """Remove Unresponded / other filters so we can see our comment."""
    try:
        # Click filters that look removable
        page.evaluate(
            """() => {
              const chips = [...document.querySelectorAll('button, yt-chip-cloud-chip-renderer, ytcp-chip, [role=button]')];
              for (const c of chips) {
                const t = (c.innerText||'').trim();
                if (/Unresponded|Response status/i.test(t)) {
                  // try clear via X or click again
                  const x = c.querySelector('[aria-label*="Remove"], [aria-label*="Clear"], button');
                  if (x) x.click();
                  else c.click();
                }
              }
            }"""
        )
        page.wait_for_timeout(500)
    except Exception:
        pass
    # Also try "Published" dropdown → All / clear search
    try:
        page.get_by_text(re.compile(r"Response status", re.I)).first.click(timeout=800)
        page.wait_for_timeout(300)
        page.get_by_text(re.compile(r"^All$|Any|Responded and unresponded", re.I)).first.click(
            timeout=800
        )
    except Exception:
        pass


def main() -> None:
    assert "http" not in PIN.lower() and "/go/" not in PIN
    info = {"text": PIN, "ok": False, "steps": []}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        ctx = browser.contexts[0]
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        page.goto(
            f"https://studio.youtube.com/video/{VID}/comments",
            wait_until="commit",
            timeout=90000,
        )
        page.wait_for_timeout(4000)
        dismiss(page)
        clear_filters(page)
        shot(page, "pin_v07_01_tab.png")

        # Click Add a comment...
        focused = False
        for sel in (
            'div[aria-label*="Add a comment"]',
            'div[contenteditable="true"]',
            "#contenteditable-root",
            'ytcp-comment-box div[contenteditable="true"]',
            'textarea[aria-label*="Add a comment"]',
            'textarea',
        ):
            try:
                loc = page.locator(sel).first
                if loc.count() == 0:
                    continue
                loc.click(timeout=2000)
                page.wait_for_timeout(300)
                focused = True
                info["steps"].append(f"focus:{sel}")
                break
            except Exception as e:
                info["steps"].append(f"miss:{sel}:{type(e).__name__}")

        if not focused:
            try:
                page.get_by_text(re.compile(r"Add a comment", re.I)).first.click(timeout=2500)
                page.wait_for_timeout(400)
                focused = True
                info["steps"].append("focus:text")
            except Exception as e:
                info["reason"] = f"no_box:{type(e).__name__}"
                dump("COMMENTS_V07_PIN.json", info)
                shot(page, "pin_v07_no_box.png")
                log(f"FAIL {info}")
                return

        # Type
        page.keyboard.press("Meta+a")
        page.keyboard.press("Backspace")
        page.keyboard.type(PIN, delay=15)
        page.wait_for_timeout(500)
        info["steps"].append("typed")
        shot(page, "pin_v07_02_typed.png")

        # Submit Comment
        posted = False
        for role_name in (r"^Comment$", r"^Reply$"):
            try:
                btns = page.get_by_role("button", name=re.compile(role_name))
                n = btns.count()
                for i in range(n):
                    b = btns.nth(i)
                    try:
                        if b.is_visible() and b.is_enabled():
                            b.click(timeout=2000)
                            posted = True
                            info["steps"].append(f"submit:{role_name}:{i}")
                            break
                    except Exception:
                        continue
                if posted:
                    break
            except Exception:
                pass
        if not posted:
            # JS click Comment button near the box
            try:
                ok = page.evaluate(
                    """() => {
                      const btns = [...document.querySelectorAll('button, ytcp-button, tp-yt-paper-button')];
                      for (const b of btns) {
                        const t = (b.innerText||'').trim();
                        if (t === 'Comment' && !b.disabled) { b.click(); return true; }
                      }
                      return false;
                    }"""
                )
                posted = bool(ok)
                info["steps"].append(f"js_submit:{ok}")
            except Exception as e:
                info["steps"].append(f"js_submit_err:{type(e).__name__}")

        page.wait_for_timeout(4000)
        shot(page, "pin_v07_03_posted.png")
        clear_filters(page)
        page.wait_for_timeout(1000)
        # Reload comments
        page.reload(wait_until="commit")
        page.wait_for_timeout(3500)
        dismiss(page)
        clear_filters(page)
        shot(page, "pin_v07_04_list.png")

        body = page.inner_text("body")
        has_text = "periodic table" in body.lower() or PIN[:35] in body
        info["has_text"] = has_text
        info["steps"].append(f"has_text:{has_text}")

        if not has_text:
            # Try searching
            try:
                search = page.get_by_placeholder(re.compile(r"Search", re.I)).first
                if search.count():
                    search.fill("periodic table")
                    page.keyboard.press("Enter")
                    page.wait_for_timeout(2000)
                    body = page.inner_text("body")
                    has_text = "periodic table" in body.lower()
                    info["has_text"] = has_text
                    shot(page, "pin_v07_04b_search.png")
            except Exception:
                pass

        # Pin via kebab / action menu on the comment
        pinned = False
        try:
            # Hover comment row containing text
            row = page.locator(
                "ytcp-comment, ytcp-comment-row, ytd-comment-thread-renderer, [class*='comment']"
            ).filter(has_text=re.compile(r"periodic table", re.I)).first
            if row.count():
                row.hover(timeout=2000)
                page.wait_for_timeout(300)
                info["steps"].append("hovered_row")
            # Action menu buttons
            for sel in (
                'button[aria-label*="Action"]',
                'button[aria-label*="More"]',
                'button[aria-label*="options"]',
                'ytcp-icon-button[aria-label*="Action"]',
                'ytcp-icon-button[aria-label*="More"]',
            ):
                try:
                    loc = page.locator(sel).first
                    if loc.count():
                        loc.click(timeout=1500)
                        info["steps"].append(f"menu:{sel}")
                        break
                except Exception:
                    continue
            page.wait_for_timeout(500)
            # Pin menu item
            for pat in (r"^Pin$", r"^Pin comment$", r"Pin"):
                try:
                    page.get_by_text(re.compile(pat, re.I)).first.click(timeout=1500)
                    pinned = True
                    info["steps"].append(f"pin_item:{pat}")
                    break
                except Exception:
                    continue
            if pinned:
                page.wait_for_timeout(600)
                try:
                    page.get_by_role("button", name=re.compile(r"^Pin$", re.I)).last.click(
                        timeout=2000
                    )
                    info["steps"].append("pin_confirm")
                except Exception:
                    # dialog Confirm
                    try:
                        page.get_by_role("button", name=re.compile(r"^Confirm$|^Pin comment$", re.I)).click(
                            timeout=1500
                        )
                        info["steps"].append("pin_confirm2")
                    except Exception:
                        pass
                page.wait_for_timeout(2500)
        except Exception as e:
            info["steps"].append(f"pin_err:{type(e).__name__}:{e}")

        shot(page, "pin_v07_05_after.png")
        shot(page, "BEN_004_pinned_comment.png")
        body = page.inner_text("body")
        info["body_has_pinned"] = bool(re.search(r"Pinned|pinned", body))
        info["body_has_text"] = "periodic table" in body.lower() or PIN[:30] in body
        info["ok"] = bool(info["body_has_text"] and (pinned or info["body_has_pinned"]))
        if info["ok"]:
            info["reason"] = "pinned"
        elif info["body_has_text"]:
            info["reason"] = "posted_pin_unconfirmed"
            info["ok"] = False
        else:
            info["reason"] = "comment_not_found_after_post"

        # Probe DOM for comment box state for debugging
        try:
            info["dom"] = page.evaluate(
                """() => {
                  const eds = [...document.querySelectorAll('[contenteditable=true], textarea')].map(e => ({
                    tag: e.tagName, aria: e.getAttribute('aria-label'), text: (e.innerText||e.value||'').slice(0,80)
                  }));
                  return {eds: eds.slice(0,8), bodyHasAdd: /Add a comment/i.test(document.body.innerText)};
                }"""
            )
        except Exception:
            pass

        dump("COMMENTS_V07_PIN.json", info)
        log(f"DONE ok={info['ok']} reason={info.get('reason')} steps={info['steps']}")


if __name__ == "__main__":
    main()
