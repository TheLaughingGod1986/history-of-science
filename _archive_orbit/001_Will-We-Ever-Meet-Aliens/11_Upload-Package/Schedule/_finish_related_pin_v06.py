#!/usr/bin/env python3
"""V001: set Related via Orbit-scoped Studio URLs + pin via Studio comments.

Root cause: bare /video/{id}/edit uses OpptiAI delegation → Related picker
list_creator_videos returns []. Channel-scoped Studio keeps Orbit delegation.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = "/Users/ben/code/youtube/.playwright-youtube-profile"
ROOT = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens"
)
PKG = ROOT / "11_Upload-Package"
AUDIT = PKG / "Schedule/_studio_audit_shorts_v001"
OUT = PKG / "Schedule/aliens_related_pin_v06.json"
ORBIT = "TBD_CREATE_HISTORY_OF_SCIENCE_CHANNEL"
LONG_ID = "Mo93x0fxB1Q"
LONG_TITLE_FRAG = "Haven't We Found Aliens"
PINNED = (PKG / "Pinned-Comments/aliens_long_pinned-comment_v01.txt").read_text().strip()
NEEDLE = "best explains the silence"
SHORTS = [
    ("01", "z-DLqoSoEBo"),
    ("02", "UWwNKYf_aU8"),
    ("03", "MO19iXYCu0c"),
    ("04", "--CxhjNqtSY"),
]


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


def save(page) -> bool:
    try:
        b = page.get_by_role("button", name="Save", exact=True)
        if b.count() and b.first.is_enabled():
            b.first.click(force=True)
            page.wait_for_timeout(2800)
            return True
    except Exception:
        pass
    return False


def edit_url(vid: str) -> str:
    # Channel-scoped edit keeps Orbit delegation context
    return f"https://studio.youtube.com/channel/{ORBIT}/video/{vid}/edit"


def warm_orbit(page):
    page.goto(
        f"https://studio.youtube.com/channel/{ORBIT}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    skip(page)
    dismiss(page)


def set_related(page, num: str, sid: str, list_log: list) -> dict:
    r: dict = {"id": num, "video_id": sid, "ok": False}
    page.goto(edit_url(sid), wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(4000)
    skip(page)
    dismiss(page)
    # If channel-scoped 404s, fall back to content→click
    if "unavailable" in page.url or page.locator("body").inner_text()[:80].lower().find(
        "error"
    ) >= 0:
        r["nav"] = "fallback_content"
        page.goto(
            f"https://studio.youtube.com/channel/{ORBIT}/videos/short",
            wait_until="domcontentloaded",
        )
        page.wait_for_timeout(3000)
        skip(page)
        # click the short row by id/title
        try:
            page.get_by_text(sid[:8], exact=False).first.click(force=True, timeout=3000)
        except Exception:
            page.goto(
                f"https://studio.youtube.com/video/{sid}/edit",
                wait_until="domcontentloaded",
            )
        page.wait_for_timeout(3500)
    else:
        r["nav"] = "channel_scoped"
        r["url"] = page.url

    body = page.locator("body").inner_text()
    chunk = body.split("Related video", 1)[-1][:180] if "Related video" in body else ""
    if "None" not in chunk[:40] and (
        "Fermi" in chunk or "Aliens" in chunk or "Orbit" in chunk or "Haven't" in chunk
    ):
        r["ok"] = True
        r["already"] = chunk
        return r

    picker = page.locator("ytcp-shorts-content-links-picker")
    if not picker.count():
        r["error"] = "no_picker"
        page.screenshot(path=str(AUDIT / f"v06_rel_{num}_nopicker.png"))
        return r
    picker.first.scroll_into_view_if_needed()
    picker.first.click(force=True)
    page.wait_for_timeout(5000)
    try:
        page.locator("ytcp-video-pick-dialog").wait_for(timeout=20000)
    except Exception:
        r["error"] = "no_dialog"
        return r

    page.screenshot(path=str(AUDIT / f"v06_rel_{num}_open.png"))
    dlg = page.locator("ytcp-video-pick-dialog").inner_text()
    r["open_snip"] = dlg[:200]

    # Prefer default list (no search) if Orbit delegation fixed it
    hit = page.evaluate(
        """(needles) => {
          const dlg=document.querySelector('ytcp-video-pick-dialog');
          if(!dlg) return null;
          const acc=[];
          const walk=(root)=>{
            for (const el of root.querySelectorAll('*')) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (t.length<12 || t.length>280) continue;
              if (!needles.some(n => t.includes(n))) continue;
              const r=el.getBoundingClientRect();
              if (r.width>100 && r.height>40 && r.height<200)
                acc.push({x:r.x+r.width/2,y:r.y+r.height/2,t:t.slice(0,180),h:r.height});
              if (el.shadowRoot) walk(el.shadowRoot);
            }
          };
          walk(dlg);
          acc.sort((a,b)=>a.h-b.h);
          return acc[0]||null;
        }""",
        [LONG_ID, LONG_TITLE_FRAG, "Fermi Paradox Explained", "Black Hole"],
    )
    if not hit:
        for q in (LONG_TITLE_FRAG, "Fermi", "Why Haven", LONG_ID, "Black"):
            page.locator("#search-yours").first.click(force=True)
            page.keyboard.press("Meta+a")
            page.keyboard.type(q, delay=25)
            page.wait_for_timeout(3500)
            hit = page.evaluate(
                """(needles) => {
                  const dlg=document.querySelector('ytcp-video-pick-dialog');
                  if(!dlg) return null;
                  const acc=[];
                  const walk=(root)=>{
                    for (const el of root.querySelectorAll('*')) {
                      const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                      if (t.length<12 || t.length>280) continue;
                      if (!needles.some(n => t.includes(n))) continue;
                      const r=el.getBoundingClientRect();
                      if (r.width>100 && r.height>40 && r.height<200)
                        acc.push({x:r.x+r.width/2,y:r.y+r.height/2,t:t.slice(0,180),h:r.height});
                      if (el.shadowRoot) walk(el.shadowRoot);
                    }
                  };
                  walk(dlg);
                  acc.sort((a,b)=>a.h-b.h);
                  return acc[0]||null;
                }""",
                [LONG_ID, LONG_TITLE_FRAG, "Fermi Paradox", "Black Hole"],
            )
            r.setdefault("searches", []).append(
                {
                    "q": q,
                    "snip": page.locator("ytcp-video-pick-dialog").inner_text()[:160],
                    "hit": bool(hit),
                }
            )
            if hit:
                r["search"] = q
                break

    # Check last list API
    if list_log:
        r["last_list"] = {
            "ids": list_log[-1].get("ids"),
            "has_long": list_log[-1].get("has_long"),
            "deleg": "Orbit"
            if "UC_esArs" in (list_log[-1].get("snip") or "")
            or "VQ19lc0Fyc" in (list_log[-1].get("snip") or "")
            else "other",
        }

    if not hit:
        r["error"] = "not_found"
        page.screenshot(path=str(AUDIT / f"v06_rel_{num}_fail.png"))
        page.keyboard.press("Escape")
        return r

    page.mouse.click(hit["x"], hit["y"])
    r["picked"] = hit["t"]
    page.wait_for_timeout(800)
    for name in ("Done", "Select", "Save"):
        b = page.get_by_role("button", name=name, exact=True)
        if b.count() and b.first.is_visible() and b.first.is_enabled():
            b.first.click(force=True)
            page.wait_for_timeout(800)
            break
    r["saved"] = save(page)

    page.goto(edit_url(sid), wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(3000)
    skip(page)
    body = page.locator("body").inner_text()
    chunk = body.split("Related video", 1)[-1][:220] if "Related video" in body else ""
    r["related_chunk"] = chunk
    r["ok"] = "None" not in chunk[:40] and (
        "Fermi" in chunk
        or "Aliens" in chunk
        or "Orbit" in chunk
        or "Haven't" in chunk
        or "Black" in chunk
    )
    page.screenshot(path=str(AUDIT / f"v06_rel_{num}_done.png"))
    return r


def pin_studio_comments(page) -> dict:
    """Pin via Studio Comments inbox / video comments."""
    r: dict = {"ok": False, "via": "studio_comments"}
    # Video-specific comments
    page.goto(
        f"https://studio.youtube.com/channel/{ORBIT}/video/{LONG_ID}/comments",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    skip(page)
    dismiss(page)
    page.screenshot(path=str(AUDIT / "v06_studio_comments.png"), full_page=True)

    # If channel-scoped comments URL fails, try classic
    if "comments" not in page.url or page.locator("body").inner_text().find(NEEDLE) < 0:
        page.goto(
            f"https://studio.youtube.com/video/{LONG_ID}/comments",
            wait_until="domcontentloaded",
        )
        page.wait_for_timeout(4000)
        skip(page)
        dismiss(page)
        page.screenshot(path=str(AUDIT / "v06_studio_comments2.png"), full_page=True)

    # Also try channel comments with search
    if NEEDLE not in page.locator("body").inner_text():
        page.goto(
            f"https://studio.youtube.com/channel/{ORBIT}/comments",
            wait_until="domcontentloaded",
        )
        page.wait_for_timeout(4000)
        skip(page)
        dismiss(page)
        try:
            search = page.get_by_placeholder(re.compile(r"Search", re.I))
            if search.count():
                search.first.fill("silence")
                page.keyboard.press("Enter")
                page.wait_for_timeout(2500)
        except Exception:
            pass
        page.screenshot(path=str(AUDIT / "v06_studio_comments3.png"), full_page=True)

    body = page.locator("body").inner_text()
    r["has_needle"] = NEEDLE in body
    if not r["has_needle"]:
        r["error"] = "comment_not_in_studio"
        return r

    # Hover/click comment row then open kebab
    try:
        page.get_by_text(NEEDLE, exact=False).first.click(force=True)
        page.wait_for_timeout(500)
    except Exception:
        pass

    # Find and click more-actions near the comment
    opened = page.evaluate(
        """(needle) => {
          const all=[...document.querySelectorAll('*')];
          let target=null;
          for (const el of all) {
            const t=(el.innerText||'');
            if (t.includes(needle) && t.length < 800) {
              const r=el.getBoundingClientRect();
              if (r.width>100 && r.height>20) { target=el; break; }
            }
          }
          if (!target) return 'no_target';
          // climb to row
          let row=target;
          for (let i=0;i<8 && row;i++) {
            const buttons=[...row.querySelectorAll('button, ytcp-icon-button, yt-icon-button, [aria-label]')];
            for (const b of buttons) {
              const al=(b.getAttribute('aria-label')||'')+(b.getAttribute('title')||'');
              if (/more|action|options|menu/i.test(al)) { b.click(); return al||'menu'; }
            }
            row=row.parentElement;
          }
          // rightmost icon button in vicinity
          const box=target.getBoundingClientRect();
          const cands=[];
          for (const b of document.querySelectorAll('button, ytcp-icon-button, yt-icon-button')) {
            const r=b.getBoundingClientRect();
            if (Math.abs(r.y-box.y)<80 && r.x>box.x && r.width>10 && r.width<60)
              cands.push({b,x:r.x});
          }
          cands.sort((a,b)=>b.x-a.x);
          if (cands[0]) { cands[0].b.click(); return 'rightmost'; }
          return 'fail';
        }""",
        NEEDLE,
    )
    r["menu_open"] = opened
    page.wait_for_timeout(900)
    page.screenshot(path=str(AUDIT / "v06_pin_menu.png"))

    items = page.evaluate(
        """() => [...document.querySelectorAll(
          'tp-yt-paper-item, ytcp-ve, [role=menuitem], yt-list-item-view-model, tp-yt-paper-listbox *'
        )].map(i=>(i.innerText||'').trim()).filter(t=>t && t.length<60).slice(0,20)"""
    )
    r["menu_items"] = items

    pinned = page.evaluate(
        """() => {
          const nodes=[...document.querySelectorAll('*')];
          for (const n of nodes) {
            const t=(n.innerText||'').trim();
            if (/^Pin comment$/i.test(t) || /^Pin$/i.test(t)) {
              const r=n.getBoundingClientRect();
              if (r.width>10 && r.height>10 && r.height<80) { n.click(); return t; }
            }
          }
          return null;
        }"""
    )
    r["pin_click"] = pinned
    page.wait_for_timeout(1000)
    if pinned:
        page.evaluate(
            """() => {
              for (const b of document.querySelectorAll('button, ytcp-button, yt-button-shape button')) {
                const t=(b.innerText||'').trim();
                if (/^Pin$/i.test(t) || /^Confirm$/i.test(t) || /^OK$/i.test(t)) {
                  b.click(); return t;
                }
              }
            }"""
        )
        page.wait_for_timeout(2000)
        r["ok"] = True
        r["pinned"] = True
    else:
        r["error"] = "no_pin_in_studio_menu"

    page.screenshot(path=str(AUDIT / "v06_pin_final.png"), full_page=True)
    return r


def pin_watch_again(page) -> dict:
    """Last resort: watch page with Orbit identity; look for Pin under ... """
    r: dict = {"ok": False, "via": "watch"}
    page.goto(
        f"https://www.youtube.com/watch?v={LONG_ID}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    page.evaluate("window.scrollTo(0, 1200)")
    page.wait_for_timeout(1500)
    # Ensure comments loaded
    page.evaluate(
        """() => {
          const t=[...document.querySelectorAll('ytd-comment-thread-renderer')];
          return t.length;
        }"""
    )
    # Use browser context menu isn't possible; try shifting+click patterns
    # Click the meatball that is sibling of published-time
    clicked = page.evaluate(
        """(needle) => {
          const threads=[...document.querySelectorAll('ytd-comment-thread-renderer')];
          const t=threads.find(el => (el.innerText||'').includes(needle));
          if (!t) return 'no';
          // Explicit: #action-menu inside #header / #body
          const selectors=[
            '#action-menu button',
            '#action-menu yt-icon-button',
            'ytd-menu-renderer yt-icon-button#button',
            'ytd-menu-renderer button',
          ];
          for (const s of selectors) {
            const el=t.querySelector(s);
            if (el) { el.click(); return s; }
          }
          return 'no_btn';
        }""",
        NEEDLE,
    )
    r["menu"] = clicked
    page.wait_for_timeout(800)
    items = page.evaluate(
        """() => [...document.querySelectorAll(
          'ytd-menu-service-item-renderer, tp-yt-paper-item, yt-list-item-view-model'
        )].map(i=>(i.innerText||'').replace(/\\s+/g,' ').trim()).filter(Boolean)"""
    )
    r["items"] = items
    if any(re.search(r"^Pin", x) for x in items):
        page.evaluate(
            """() => {
              for (const i of document.querySelectorAll(
                'ytd-menu-service-item-renderer, tp-yt-paper-item, yt-list-item-view-model'
              )) {
                if (/^Pin/i.test((i.innerText||'').trim())) { i.click(); return true; }
              }
            }"""
        )
        page.wait_for_timeout(800)
        page.evaluate(
            """() => {
              for (const b of document.querySelectorAll('button')) {
                if (/^Pin$/i.test((b.innerText||'').trim())) { b.click(); return; }
              }
            }"""
        )
        page.wait_for_timeout(1500)
        r["ok"] = True
    page.screenshot(path=str(AUDIT / "v06_watch_pin.png"))
    return r


def main():
    AUDIT.mkdir(parents=True, exist_ok=True)
    result: dict = {"related": [], "pin": None, "list_calls": [], "ok": False}
    list_log: list = []

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 1100},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        def on_response(resp):
            if "list_creator_videos" not in resp.url:
                return
            try:
                text = resp.text()
            except Exception:
                return
            ids = re.findall(r'"videoId"\s*:\s*"([A-Za-z0-9_-]{11})"', text)
            list_log.append(
                {
                    "ids": list(dict.fromkeys(ids))[:20],
                    "has_long": LONG_ID in text,
                    "snip": text[:350],
                    "deleg_orbit": "VQ19lc0Fyc" in text,
                    "deleg_oppti": "VQ1hSVndy" in text,
                }
            )

        page.on("response", on_response)

        print("Warm Orbit…", flush=True)
        warm_orbit(page)

        for num, sid in SHORTS:
            print(f"RELATED {num}…", flush=True)
            try:
                rr = set_related(page, num, sid, list_log)
            except Exception as e:
                rr = {"id": num, "video_id": sid, "ok": False, "error": str(e)[:300]}
            result["related"].append(rr)
            print(
                f"  → ok={rr.get('ok')} {rr.get('error') or rr.get('picked','')[:70]} "
                f"list={rr.get('last_list')}",
                flush=True,
            )
            OUT.write_text(json.dumps({**result, "list_tail": list_log[-3:]}, indent=2) + "\n")

        print("PIN studio…", flush=True)
        pin = pin_studio_comments(page)
        if not pin.get("ok"):
            print("PIN watch…", flush=True)
            pin2 = pin_watch_again(page)
            pin["watch"] = pin2
            if pin2.get("ok"):
                pin = pin2
        result["pin"] = pin
        print("pin", pin, flush=True)

        result["list_tail"] = list_log[-8:]
        result["ok"] = all(x.get("ok") for x in result["related"]) and bool(
            result["pin"].get("ok")
        )
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        ctx.close()
        print("RESULT", OUT, "ok=", result["ok"])
        raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
