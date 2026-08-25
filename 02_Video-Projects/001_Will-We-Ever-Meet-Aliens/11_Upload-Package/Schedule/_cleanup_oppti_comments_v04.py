#!/usr/bin/env python3
"""Delete all @OpptiAI CTA comments on V001 as OpptiAI, then post once as Orbit."""
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
OUT = PKG / "Schedule/aliens_cleanup_oppti_comments_v04.json"
LONG_ID = "Mo93x0fxB1Q"
NEEDLE = "best explains the silence"
PINNED = (PKG / "Pinned-Comments/aliens_long_pinned-comment_v01.txt").read_text().strip()


def switch_account(page, name: str) -> str | None:
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    try:
        page.locator("#avatar-btn").first.click(force=True, timeout=4000)
    except Exception:
        page.evaluate("() => document.querySelector('#avatar-btn')?.click()")
    page.wait_for_timeout(1000)
    try:
        page.get_by_text("Switch account", exact=False).first.click(force=True, timeout=3000)
        page.wait_for_timeout(1200)
    except Exception:
        pass
    chose = page.evaluate(
        """(name) => {
          const nodes=[...document.querySelectorAll(
            'ytd-account-item-renderer, tp-yt-paper-item, yt-list-item-view-model, a, yt-formatted-string'
          )];
          for (const n of nodes) {
            const t=n.innerText||'';
            if (t.includes(name)) { n.click(); return t.replace(/\\s+/g,' ').trim().slice(0,100); }
          }
          return null;
        }""",
        name,
    )
    page.wait_for_timeout(3000)
    return chose


def main():
    AUDIT.mkdir(parents=True, exist_ok=True)
    result: dict = {"deleted": 0, "ok": False}

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 1100},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        page.goto(
            f"https://www.youtube.com/watch?v={LONG_ID}",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(5000)
        result["as_oppti"] = switch_account(page, "OpptiAI")
        page.goto(
            f"https://www.youtube.com/watch?v={LONG_ID}",
            wait_until="domcontentloaded",
        )
        page.wait_for_timeout(5000)
        page.evaluate("window.scrollTo(0, 1300)")
        page.wait_for_timeout(2000)
        try:
            page.get_by_text("Sort by", exact=False).first.click(force=True, timeout=2000)
            page.wait_for_timeout(400)
            page.get_by_text("Newest first", exact=False).first.click(force=True)
            page.wait_for_timeout(1500)
        except Exception:
            pass
        page.keyboard.press("Escape")
        page.wait_for_timeout(400)
        page.screenshot(path=str(AUDIT / "cleanup_v04_start.png"), full_page=True)

        for i in range(12):
            page.keyboard.press("Escape")
            page.wait_for_timeout(300)
            info = page.evaluate(
                """(needle) => {
                  const threads=[...document.querySelectorAll('ytd-comment-thread-renderer')];
                  const t=threads.find(el => {
                    const x=el.innerText||'';
                    return /@OpptiAI|@opptiai/i.test(x) || x.includes(needle);
                  });
                  if (!t) return {found:false, total:threads.length};
                  const author=(t.querySelector('#author-text')?.innerText||'').trim();
                  const btn=t.querySelector(
                    '#action-menu button, #action-menu yt-icon-button, ytd-menu-renderer yt-icon-button#button'
                  );
                  if (!btn) return {found:true, author, no_btn:true};
                  btn.click();
                  return {found:true, author};
                }""",
                NEEDLE,
            )
            result.setdefault("rounds", []).append(info)
            if not info.get("found"):
                break
            page.wait_for_timeout(800)
            page.screenshot(path=str(AUDIT / f"cleanup_v04_menu_{i}.png"))

            # Click Delete menu item specifically (not sort)
            deleted = page.evaluate(
                """() => {
                  const items=[...document.querySelectorAll(
                    'ytd-menu-service-item-renderer, tp-yt-paper-item[role=option], yt-list-item-view-model'
                  )];
                  for (const it of items) {
                    const t=(it.innerText||'').replace(/\\s+/g,' ').trim();
                    if (t==='Delete' || t.startsWith('Delete')) {
                      it.click();
                      return t;
                    }
                  }
                  return null;
                }"""
            )
            result.setdefault("delete_clicks", []).append(deleted)
            page.wait_for_timeout(1000)
            page.screenshot(path=str(AUDIT / f"cleanup_v04_confirm_{i}.png"))

            # Confirm dialog — look for Delete button in dialog
            conf = page.evaluate(
                """() => {
                  const dlg=document.querySelector(
                    'yt-confirm-dialog-renderer, tp-yt-paper-dialog, ytd-popup-container'
                  );
                  const root=dlg||document;
                  for (const b of root.querySelectorAll('button, yt-button-renderer button, yt-button-shape button')) {
                    const t=(b.innerText||'').trim();
                    if (/^Delete$/i.test(t)) { b.click(); return 'dlg-'+t; }
                  }
                  for (const b of document.querySelectorAll('button')) {
                    const t=(b.innerText||'').trim();
                    if (/^Delete$/i.test(t)) {
                      const r=b.getBoundingClientRect();
                      if (r.y>200 && r.width>40) { b.click(); return 'page-'+t; }
                    }
                  }
                  return null;
                }"""
            )
            result.setdefault("confirms", []).append(conf)
            page.wait_for_timeout(2500)
            if deleted:
                result["deleted"] += 1
            # Don't full reload every time — wait for thread to vanish
            page.wait_for_timeout(1000)
            still = page.evaluate(
                """(needle) => {
                  return [...document.querySelectorAll('ytd-comment-thread-renderer')]
                    .filter(t => /@OpptiAI/i.test(t.innerText||'') || (t.innerText||'').includes(needle))
                    .length;
                }""",
                NEEDLE,
            )
            if still == 0:
                break
            if i % 3 == 2:
                page.reload(wait_until="domcontentloaded")
                page.wait_for_timeout(4000)
                page.evaluate("window.scrollTo(0, 1300)")
                page.wait_for_timeout(1500)
                try:
                    page.get_by_text("Sort by", exact=False).first.click(force=True, timeout=1500)
                    page.wait_for_timeout(300)
                    page.get_by_text("Newest first", exact=False).first.click(force=True)
                    page.wait_for_timeout(1000)
                except Exception:
                    pass
                page.keyboard.press("Escape")

        page.screenshot(path=str(AUDIT / "cleanup_v04_after_delete.png"), full_page=True)
        body = page.locator("body").inner_text()
        result["still_oppti"] = bool(re.search(r"@?OpptiAI|@?opptiai", body, re.I))
        result["still_needle"] = NEEDLE in body

        # Switch to Orbit and post ONE clean comment
        result["as_orbit"] = switch_account(page, "History of Science")
        page.goto(
            f"https://www.youtube.com/watch?v={LONG_ID}",
            wait_until="domcontentloaded",
        )
        page.wait_for_timeout(5000)
        page.evaluate("window.scrollTo(0, 1300)")
        page.wait_for_timeout(1500)

        # Comment identity: Orbit
        page.evaluate(
            "() => document.querySelector('#simplebox-placeholder, #placeholder-area')?.click()"
        )
        page.wait_for_timeout(700)
        page.evaluate(
            """() => {
              document.querySelector(
                'ytd-comment-simplebox-renderer #author-thumbnail button, #author-thumbnail'
              )?.click();
            }"""
        )
        page.wait_for_timeout(800)
        page.evaluate(
            """() => {
              for (const n of document.querySelectorAll(
                'ytd-account-item-renderer, tp-yt-paper-item, yt-formatted-string'
              )) {
                if (/History of Science/i.test(n.innerText||'')) { n.click(); return; }
              }
            }"""
        )
        page.wait_for_timeout(800)
        page.screenshot(path=str(AUDIT / "cleanup_v04_orbit_id.png"))

        if not result["still_needle"]:
            page.evaluate(
                """(text) => {
                  const root=document.querySelector(
                    'ytd-commentbox #contenteditable-root, #contenteditable-root'
                  );
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
        else:
            result["posted"] = False
            result["post_skip"] = "needle still present after delete"

        page.reload(wait_until="domcontentloaded")
        page.wait_for_timeout(4500)
        page.evaluate("window.scrollTo(0, 1300)")
        page.wait_for_timeout(1500)
        page.screenshot(path=str(AUDIT / "cleanup_v04_final.png"), full_page=True)
        result["final_authors"] = page.evaluate(
            """(needle) => [...document.querySelectorAll('ytd-comment-thread-renderer')]
              .filter(t => (t.innerText||'').includes(needle))
              .map(t => (t.querySelector('#author-text')?.innerText||'').trim())""",
            NEEDLE,
        )
        result["final_has_oppti"] = any(
            re.search(r"opptiai|OpptiAI", a or "", re.I)
            for a in result["final_authors"]
        )
        result["ok"] = (not result["final_has_oppti"]) and (
            bool(result.get("posted")) or bool(result["final_authors"])
        )
        # Prefer: no oppti authors at all
        body = page.locator("body").inner_text()
        result["body_has_oppti"] = bool(re.search(r"@OpptiAI|@opptiai", body, re.I))
        if result["body_has_oppti"]:
            result["ok"] = False

        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2), flush=True)
        ctx.close()
        raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
