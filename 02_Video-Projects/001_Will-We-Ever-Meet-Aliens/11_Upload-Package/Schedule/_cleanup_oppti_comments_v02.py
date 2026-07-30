#!/usr/bin/env python3
"""Find + delete @opptiai comments on V001 via watch page + Studio filters."""
from __future__ import annotations

import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = "/Users/ben/code/youtube/.playwright-youtube-profile"
PKG = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens/11_Upload-Package"
)
AUDIT = PKG / "Schedule/_studio_audit_shorts_v001"
OUT = PKG / "Schedule/aliens_cleanup_oppti_comments_v02.json"
LONG_ID = "Mo93x0fxB1Q"
ORBIT = "UC_esArsDKd3GJvOkeO0DUog"
NEEDLE = "best explains the silence"
PINNED = (PKG / "Pinned-Comments/aliens_long_pinned-comment_v01.txt").read_text().strip()


def skip(page):
    try:
        page.get_by_role("link", name=re.compile(r"Skip", re.I)).click(timeout=800)
    except Exception:
        pass


def switch_to_orbit(page) -> str | None:
    try:
        page.locator("#avatar-btn, button#avatar-btn").first.click(force=True, timeout=4000)
    except Exception:
        page.evaluate(
            "() => document.querySelector('#avatar-btn')?.click()"
        )
    page.wait_for_timeout(1000)
    try:
        page.get_by_text("Switch account", exact=False).first.click(force=True, timeout=3000)
        page.wait_for_timeout(1200)
    except Exception:
        pass
    chose = page.evaluate(
        """() => {
          for (const n of document.querySelectorAll(
            'ytd-account-item-renderer, tp-yt-paper-item, yt-list-item-view-model, yt-formatted-string'
          )) {
            const t=n.innerText||'';
            if (/Orbit with Ben/i.test(t)) { n.click(); return t.slice(0,80); }
          }
          return null;
        }"""
    )
    page.wait_for_timeout(2500)
    return chose


def main():
    AUDIT.mkdir(parents=True, exist_ok=True)
    result: dict = {"steps": [], "ok": False}

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 1100},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        # 1) Studio channel comments inbox (all videos) — filter published + held
        print("Studio channel comments…", flush=True)
        page.goto(
            f"https://studio.youtube.com/channel/{ORBIT}/comments/inbox",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(4500)
        skip(page)
        page.screenshot(path=str(AUDIT / "cleanup_v02_inbox.png"), full_page=True)
        result["inbox_snip"] = page.locator("body").inner_text()[:800]

        # Try Published / Held for review tabs
        for tab in ("Published", "Held for review", "Likely spam"):
            try:
                page.get_by_text(tab, exact=True).first.click(force=True, timeout=2000)
                page.wait_for_timeout(2000)
                page.screenshot(path=str(AUDIT / f"cleanup_v02_tab_{tab.replace(' ','_')}.png"))
                body = page.locator("body").inner_text()
                result["steps"].append(
                    {
                        "tab": tab,
                        "has_oppti": bool(re.search(r"opptiai|OpptiAI", body, re.I)),
                        "has_needle": NEEDLE in body,
                        "snip": body[:400],
                    }
                )
            except Exception as e:
                result["steps"].append({"tab": tab, "err": str(e)[:120]})

        # Delete from inbox if visible
        deleted = []
        for _ in range(10):
            body = page.locator("body").inner_text()
            if not re.search(r"opptiai|OpptiAI|best explains the silence", body, re.I):
                break
            # click comment row then delete
            try:
                page.get_by_text(re.compile(r"opptiai|best explains the silence", re.I)).first.click(
                    force=True, timeout=3000
                )
                page.wait_for_timeout(500)
            except Exception:
                break
            # action menu
            page.evaluate(
                """() => {
                  const btns=[...document.querySelectorAll(
                    'ytcp-icon-button[aria-label*="Action"], button[aria-label*="Action"], ytcp-icon-button[aria-label*="More"]'
                  )];
                  for (const b of btns) {
                    const r=b.getBoundingClientRect();
                    if (r.width>5 && r.y>100) { b.click(); return true; }
                  }
                  return false;
                }"""
            )
            page.wait_for_timeout(600)
            del_hit = page.evaluate(
                """() => {
                  for (const n of document.querySelectorAll(
                    'tp-yt-paper-item, [role=menuitem], span'
                  )) {
                    if (/^Delete$/i.test((n.innerText||'').trim())) { n.click(); return true; }
                  }
                  return false;
                }"""
            )
            page.wait_for_timeout(700)
            page.evaluate(
                """() => {
                  for (const b of document.querySelectorAll('button, ytcp-button')) {
                    if (/^Delete$/i.test((b.innerText||'').trim())) { b.click(); return; }
                  }
                }"""
            )
            page.wait_for_timeout(2000)
            deleted.append({"deleted": bool(del_hit)})
            page.reload(wait_until="domcontentloaded")
            page.wait_for_timeout(3000)
            skip(page)
        result["inbox_deleted"] = deleted

        # 2) Watch page as Orbit — delete own wrong-account comments if menu allows
        print("Watch page…", flush=True)
        page.goto(
            f"https://www.youtube.com/watch?v={LONG_ID}",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(5000)
        result["switched"] = switch_to_orbit(page)
        page.goto(
            f"https://www.youtube.com/watch?v={LONG_ID}",
            wait_until="domcontentloaded",
        )
        page.wait_for_timeout(5000)
        page.evaluate("window.scrollTo(0, 1200)")
        page.wait_for_timeout(2000)
        try:
            page.get_by_text("Sort by", exact=False).first.click(force=True, timeout=2000)
            page.wait_for_timeout(400)
            page.get_by_text("Newest first", exact=False).first.click(force=True)
            page.wait_for_timeout(1500)
        except Exception:
            pass
        page.screenshot(path=str(AUDIT / "cleanup_v02_watch.png"), full_page=True)

        watch_deleted = []
        for _ in range(8):
            threads = page.locator("ytd-comment-thread-renderer")
            hit = None
            for i in range(threads.count()):
                t = threads.nth(i).inner_text()
                if re.search(r"opptiai|OpptiAI", t, re.I) or (
                    NEEDLE in t and "Orbit with Ben" not in t.split("\n")[0]
                ):
                    hit = i
                    break
            if hit is None:
                break
            th = threads.nth(hit)
            th.scroll_into_view_if_needed()
            page.wait_for_timeout(300)
            th.locator(
                "#action-menu button, #action-menu yt-icon-button, ytd-menu-renderer yt-icon-button"
            ).first.click(force=True)
            page.wait_for_timeout(700)
            items = page.evaluate(
                """() => [...document.querySelectorAll(
                  'ytd-menu-service-item-renderer, tp-yt-paper-item, yt-list-item-view-model'
                )].map(i=>(i.innerText||'').replace(/\\s+/g,' ').trim()).filter(Boolean)"""
            )
            watch_deleted.append({"items": items, "i": hit})
            if any(re.search(r"^Delete", x) for x in items):
                page.evaluate(
                    """() => {
                      for (const i of document.querySelectorAll(
                        'ytd-menu-service-item-renderer, tp-yt-paper-item, yt-list-item-view-model'
                      )) {
                        if (/^Delete/i.test((i.innerText||'').trim())) { i.click(); return; }
                      }
                    }"""
                )
                page.wait_for_timeout(800)
                page.evaluate(
                    """() => {
                      for (const b of document.querySelectorAll('button')) {
                        if (/^Delete$/i.test((b.innerText||'').trim())) { b.click(); return; }
                      }
                    }"""
                )
                page.wait_for_timeout(2000)
            else:
                page.keyboard.press("Escape")
                break
            page.reload(wait_until="domcontentloaded")
            page.wait_for_timeout(4000)
            page.evaluate("window.scrollTo(0, 1200)")
            page.wait_for_timeout(1500)

        result["watch_deleted"] = watch_deleted
        page.screenshot(path=str(AUDIT / "cleanup_v02_watch_after.png"), full_page=True)
        body = page.locator("body").inner_text()
        result["watch_has_oppti"] = bool(re.search(r"opptiai|OpptiAI", body, re.I))
        result["watch_has_needle"] = NEEDLE in body

        # 3) Post as Orbit if clean
        if not result["watch_has_oppti"]:
            print("Post as Orbit…", flush=True)
            # Ensure Orbit identity on comment box
            page.evaluate(
                "() => document.querySelector('#simplebox-placeholder, #placeholder-area')?.click()"
            )
            page.wait_for_timeout(700)
            page.evaluate(
                """() => {
                  const box=document.querySelector('ytd-comment-simplebox-renderer, ytd-commentbox');
                  box?.querySelector('#author-thumbnail button, #author-thumbnail')?.click();
                }"""
            )
            page.wait_for_timeout(900)
            page.evaluate(
                """() => {
                  for (const n of document.querySelectorAll(
                    'ytd-account-item-renderer, tp-yt-paper-item, yt-formatted-string'
                  )) {
                    if (/Orbit with Ben/i.test(n.innerText||'')) { n.click(); return; }
                  }
                }"""
            )
            page.wait_for_timeout(800)
            page.screenshot(path=str(AUDIT / "cleanup_v02_identity.png"))
            page.evaluate(
                """(text) => {
                  const root=document.querySelector('ytd-commentbox #contenteditable-root, #contenteditable-root');
                  if (!root) return false;
                  root.focus();
                  root.innerText=text;
                  root.dispatchEvent(new InputEvent('input',{bubbles:true,data:text}));
                  return true;
                }""",
                PINNED,
            )
            page.wait_for_timeout(500)
            page.evaluate(
                """() => {
                  const b=document.querySelector('#submit-button button');
                  if (b && !b.disabled) b.click();
                }"""
            )
            page.wait_for_timeout(3500)
            result["posted"] = True
            page.screenshot(path=str(AUDIT / "cleanup_v02_posted.png"), full_page=True)
            page.reload(wait_until="domcontentloaded")
            page.wait_for_timeout(4000)
            page.evaluate("window.scrollTo(0, 1200)")
            page.wait_for_timeout(1500)
            body = page.locator("body").inner_text()
            result["final_has_oppti"] = bool(re.search(r"opptiai|OpptiAI", body, re.I))
            result["final_authors"] = page.evaluate(
                """(needle) => {
                  return [...document.querySelectorAll('ytd-comment-thread-renderer')]
                    .filter(t => (t.innerText||'').includes(needle))
                    .map(t => (t.querySelector('#author-text')?.innerText||'').trim())
                    .slice(0,5);
                }""",
                NEEDLE,
            )

        result["ok"] = not result.get("final_has_oppti", result.get("watch_has_oppti", True))
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2)[:3000], flush=True)
        ctx.close()
        raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
