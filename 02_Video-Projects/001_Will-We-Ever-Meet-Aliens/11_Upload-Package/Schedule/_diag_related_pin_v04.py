#!/usr/bin/env python3
"""Diagnose Related picker + finish pin for V001."""
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
OUT = PKG / "Schedule/aliens_related_pin_v04.json"
CHANNEL = "UC_esArsDKd3GJvOkeO0DUog"
LONG_ID = "Mo93x0fxB1Q"
SHORT_ID = "z-DLqoSoEBo"
NEEDLE = "best explains the silence"


def skip(page):
    try:
        page.get_by_role("link", name=re.compile(r"Skip", re.I)).click(timeout=800)
    except Exception:
        pass


def dismiss(page):
    for name in ("Got it", "Dismiss", "Close", "Not now"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=500)
        except Exception:
            pass


def main():
    AUDIT.mkdir(parents=True, exist_ok=True)
    result = {"api": [], "pin": None, "related": None}

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 1100},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        # Capture XHR related to video search / linked content
        def on_response(resp):
            u = resp.url
            if any(
                k in u
                for k in (
                    "video_picker",
                    "creator_videos",
                    "list_creator",
                    "search",
                    "linked_content",
                    "content_links",
                    "youtubei",
                )
            ):
                if resp.request.resource_type in ("xhr", "fetch"):
                    try:
                        body = resp.text()[:1500]
                    except Exception:
                        body = ""
                    result["api"].append(
                        {"url": u[:250], "status": resp.status, "snip": body[:400]}
                    )

        page.on("response", on_response)

        # 1) Confirm channel content lists the long
        print("CONTENT list…", flush=True)
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/short",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3000)
        skip(page)
        dismiss(page)
        # switch to Videos tab
        try:
            page.get_by_role("tab", name=re.compile(r"^Videos$", re.I)).click(force=True)
            page.wait_for_timeout(2500)
        except Exception:
            page.goto(
                f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
                wait_until="domcontentloaded",
            )
            page.wait_for_timeout(3000)
        body = page.locator("body").inner_text()
        result["content_has_long"] = LONG_ID in body or "Haven't We Found Aliens" in body
        result["content_snip"] = body[:500]
        page.screenshot(path=str(AUDIT / "v04_content.png"))
        print(f"  has_long={result['content_has_long']}", flush=True)

        # 2) Open related picker and probe API + tabs
        print("PICKER probe…", flush=True)
        page.goto(
            f"https://studio.youtube.com/video/{SHORT_ID}/edit",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3500)
        skip(page)
        dismiss(page)
        picker = page.locator("ytcp-shorts-content-links-picker")
        picker.first.scroll_into_view_if_needed()
        picker.first.click(force=True)
        page.wait_for_timeout(3000)
        page.locator("ytcp-video-pick-dialog").wait_for(timeout=20000)

        # Wait longer for empty default load / API
        page.wait_for_timeout(8000)
        page.screenshot(path=str(AUDIT / "v04_picker_wait.png"))

        # Inspect tab labels
        tabs = page.evaluate(
            """() => {
              const dlg=document.querySelector('ytcp-video-pick-dialog');
              const out=[];
              const walk=(root)=>{
                for (const el of root.querySelectorAll('tp-yt-paper-tab, [role=tab]')) {
                  out.push({id:el.id, t:(el.innerText||'').trim(), al:el.getAttribute('aria-label')||'',
                    selected:el.getAttribute('aria-selected')||el.className});
                }
                for (const el of root.querySelectorAll('*')) if (el.shadowRoot) walk(el.shadowRoot);
              };
              walk(dlg||document);
              return out;
            }"""
        )
        result["tabs"] = tabs
        print("tabs", tabs, flush=True)

        # Click each tab
        for tid in ("search-yours-tab", "search-any-tab", "search-playlist-tab"):
            clicked = page.evaluate(
                """(id) => {
                  const el=document.querySelector('#'+id) || document.getElementById(id);
                  if (!el) return false;
                  el.click();
                  return true;
                }""",
                tid,
            )
            result.setdefault("tab_clicks", {})[tid] = clicked
            page.wait_for_timeout(2000)
            page.screenshot(path=str(AUDIT / f"v04_tab_{tid}.png"))

        # Focus search and type slowly; also try URL
        inp = page.locator("#search-yours")
        inp.first.click(force=True)
        page.keyboard.type("Why", delay=120)
        page.wait_for_timeout(4000)
        page.screenshot(path=str(AUDIT / "v04_search_why.png"))
        result["after_why"] = page.locator("ytcp-video-pick-dialog").inner_text()[:300]

        # Clear and paste URL
        page.keyboard.press("Meta+a")
        page.keyboard.type(f"https://youtu.be/{LONG_ID}", delay=20)
        page.wait_for_timeout(4000)
        page.screenshot(path=str(AUDIT / "v04_search_url.png"))
        result["after_url"] = page.locator("ytcp-video-pick-dialog").inner_text()[:300]

        # Try search-any if visible
        any_inp = page.locator("#search-any")
        if any_inp.count():
            # make visible by clicking its tab
            page.evaluate(
                """() => {
                  const t=document.querySelector('#search-any-tab');
                  if (t) t.click();
                }"""
            )
            page.wait_for_timeout(1000)
            try:
                any_inp.first.click(force=True, timeout=2000)
                page.keyboard.type(f"https://www.youtube.com/watch?v={LONG_ID}", delay=15)
                page.wait_for_timeout(4000)
                page.screenshot(path=str(AUDIT / "v04_search_any.png"))
                result["after_any"] = page.locator("ytcp-video-pick-dialog").inner_text()[:400]
            except Exception as e:
                result["any_err"] = str(e)[:200]

        # Dump #videos children
        result["videos_dom"] = page.evaluate(
            """() => {
              const v=document.querySelector('#videos');
              if (!v) return null;
              return {
                html: v.innerHTML.slice(0,800),
                text: (v.innerText||'').slice(0,400),
                childCount: v.children.length,
                tags: [...v.querySelectorAll('*')].slice(0,30).map(e=>e.tagName)
              };
            }"""
        )

        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

        # 3) Pin the existing comment on watch page
        print("PIN…", flush=True)
        page.goto(
            f"https://www.youtube.com/watch?v={LONG_ID}",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(5000)
        page.evaluate("window.scrollTo(0, 1100)")
        page.wait_for_timeout(2000)
        try:
            page.get_by_text("Sort by", exact=False).first.click(force=True, timeout=3000)
            page.wait_for_timeout(400)
            page.get_by_text("Newest first", exact=False).first.click(force=True)
            page.wait_for_timeout(1500)
        except Exception:
            pass

        pin = {"ok": False, "via": "watch_v04"}
        thread = page.locator("ytd-comment-thread-renderer").filter(has_text=NEEDLE)
        pin["found"] = thread.count()
        if thread.count():
            # Hover to reveal menu
            thread.first.hover()
            page.wait_for_timeout(400)
            # Click the three-dot menu specifically
            clicked_menu = page.evaluate(
                """(needle) => {
                  const threads=[...document.querySelectorAll('ytd-comment-thread-renderer')];
                  const t=threads.find(el => (el.innerText||'').includes(needle));
                  if (!t) return 'no_thread';
                  // Prefer #action-menu
                  const menu = t.querySelector('#action-menu yt-icon-button, #action-menu button, ytd-menu-renderer yt-icon-button');
                  if (menu) { menu.click(); return 'action_menu'; }
                  const buttons=[...t.querySelectorAll('button, yt-icon-button')];
                  for (const b of buttons) {
                    const al=(b.getAttribute('aria-label')||'')+(b.getAttribute('title')||'');
                    if (/action|more|menu/i.test(al)) { b.click(); return al; }
                  }
                  // rightmost small button near author
                  const cands=buttons.map(b=>{
                    const r=b.getBoundingClientRect();
                    return {b, x:r.x, y:r.y, w:r.width, h:r.height};
                  }).filter(c=>c.w>10 && c.w<50 && c.h>10 && c.h<50);
                  cands.sort((a,b)=>b.x-a.x);
                  if (cands[0]) { cands[0].b.click(); return 'rightmost'; }
                  return 'fail';
                }""",
                NEEDLE,
            )
            pin["menu"] = clicked_menu
            page.wait_for_timeout(800)
            page.screenshot(path=str(AUDIT / "v04_pin_menu.png"))

            # Read menu items
            menu_text = page.evaluate(
                """() => {
                  const items=[...document.querySelectorAll(
                    'ytd-menu-service-item-renderer, tp-yt-paper-item, [role=menuitem], yt-list-item-view-model'
                  )];
                  return items.map(i=>(i.innerText||'').trim()).filter(Boolean).slice(0,20);
                }"""
            )
            pin["menu_items"] = menu_text
            print("menu_items", menu_text, flush=True)

            # Click Pin if present
            pinned = page.evaluate(
                """() => {
                  const items=[...document.querySelectorAll(
                    'ytd-menu-service-item-renderer, tp-yt-paper-item, [role=menuitem], yt-list-item-view-model, yt-formatted-string'
                  )];
                  for (const i of items) {
                    const t=(i.innerText||'').trim();
                    if (/^Pin$/i.test(t) || /^Pin comment$/i.test(t)) {
                      i.click();
                      return t;
                    }
                  }
                  return null;
                }"""
            )
            pin["pin_click"] = pinned
            page.wait_for_timeout(1000)
            if pinned:
                # confirm dialog
                page.evaluate(
                    """() => {
                      const btns=[...document.querySelectorAll('button, yt-button-shape button, tp-yt-paper-button')];
                      for (const b of btns) {
                        const t=(b.innerText||'').trim();
                        if (/^Pin$/i.test(t) || /^Confirm$/i.test(t)) { b.click(); return t; }
                      }
                      return null;
                    }"""
                )
                page.wait_for_timeout(2000)
                pin["ok"] = True
            else:
                # Maybe need to switch to Orbit channel identity for pin
                pin["error"] = "no_pin_in_menu"
        else:
            pin["error"] = "comment_missing"
            # check page text
            pin["body_has"] = NEEDLE in page.locator("body").inner_text()

        page.screenshot(path=str(AUDIT / "v04_pin_final.png"), full_page=True)
        result["pin"] = pin
        print("pin", pin, flush=True)

        # Keep only last ~15 API snips that look relevant
        result["api"] = [
            a
            for a in result["api"]
            if any(
                k in a["url"]
                for k in (
                    "creator",
                    "picker",
                    "linked",
                    "content_link",
                    "search",
                    "list_videos",
                )
            )
        ][-20:]

        OUT.write_text(json.dumps(result, indent=2) + "\n")
        ctx.close()
        print("WROTE", OUT)


if __name__ == "__main__":
    main()
