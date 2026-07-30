#!/usr/bin/env python3
"""V001 retry: Related Shorts → long (public) + pin first comment on watch page.

Studio Related picker only lists PUBLIC videos.
Proven pattern: ytcp-shorts-content-links-picker + ytcp-video-pick-dialog
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
INDEX = json.loads((ROOT / "10_Shorts/SHORTS_UPLOAD_INDEX.json").read_text())
PKG = ROOT / "11_Upload-Package"
LONG_ID = INDEX["long_id"]
LONG_TITLE = INDEX["long_title"]
# Full title as shown in Studio / watch
LONG_TITLE_FULL = (
    "Why Haven't We Found Aliens Yet? The Fermi Paradox Explained | Orbit's Cosmic Journey"
)
PINNED = (PKG / "Pinned-Comments/aliens_long_pinned-comment_v01.txt").read_text().strip()
OUT = PKG / "Schedule/aliens_related_pin_v03.json"
AUDIT = PKG / "Schedule/_studio_audit_shorts_v001"

SHORTS = [(s["id"], s["video_id"]) for s in INDEX["shorts"]]


def skip(page) -> None:
    try:
        page.get_by_role("link", name=re.compile(r"Skip", re.I)).click(timeout=1000)
    except Exception:
        pass


def dismiss(page) -> None:
    page.evaluate(
        "() => document.querySelectorAll('tp-yt-iron-overlay-backdrop').forEach(e => e.remove())"
    )
    for name in ("Got it", "Dismiss", "Close", "Not now"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=600)
        except Exception:
            pass


def save(page) -> bool:
    try:
        b = page.get_by_role("button", name="Save", exact=True)
        if b.count() and b.first.is_enabled():
            b.first.click(force=True)
            page.wait_for_timeout(3000)
            return True
    except Exception:
        pass
    return False


def check_long_public(page) -> dict:
    info: dict = {"id": LONG_ID, "public": False}
    page.goto(
        f"https://studio.youtube.com/video/{LONG_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    skip(page)
    dismiss(page)
    loc = page.locator("ytcp-video-metadata-visibility")
    chip = loc.first.inner_text().replace("\n", " ").strip() if loc.count() else ""
    info["chip"] = chip[:200]
    info["public"] = bool(
        re.search(r"\bPublic\b", chip) and not re.search(r"\bScheduled\b", chip, re.I)
    )
    page.screenshot(path=str(AUDIT / "long_visibility_v03.png"))
    return info


def dialog_dump(page) -> dict:
    return page.evaluate(
        """() => {
          const dlg = document.querySelector('ytcp-video-pick-dialog');
          if (!dlg) return {exists:false};
          const text = (dlg.innerText||'').slice(0,800);
          const tags = [];
          const walk = (root, depth) => {
            if (!root || depth>8) return;
            for (const el of root.querySelectorAll('*')) {
              const n = el.tagName.toLowerCase();
              if (/ytcp-|yt-|tp-yt-/.test(n) || el.id) {
                const r = el.getBoundingClientRect();
                if (r.width>20 && r.height>8)
                  tags.push({n, id:el.id||'', al:el.getAttribute('aria-label')||'',
                    t:(el.innerText||'').replace(/\\s+/g,' ').trim().slice(0,80),
                    w:Math.round(r.width), h:Math.round(r.height)});
              }
              if (el.shadowRoot) walk(el.shadowRoot, depth+1);
            }
          };
          walk(dlg, 0);
          // inputs
          const inputs = [];
          const walkIn = (root) => {
            for (const el of root.querySelectorAll('input,textarea,[contenteditable=true]')) {
              const r = el.getBoundingClientRect();
              inputs.push({tag:el.tagName, id:el.id, ph:el.placeholder||'',
                val:el.value||'', w:Math.round(r.width), h:Math.round(r.height)});
            }
            for (const el of root.querySelectorAll('*')) if (el.shadowRoot) walkIn(el.shadowRoot);
          };
          walkIn(dlg);
          return {exists:true, text, tags:tags.slice(0,40), inputs};
        }"""
    )


def fill_search(page, query: str) -> str:
    """Fill search with multiple strategies; return method used."""
    # Strategy 1: #search-yours (may be host; find inner input)
    filled = page.evaluate(
        """(q) => {
          const dlg = document.querySelector('ytcp-video-pick-dialog');
          if (!dlg) return 'no_dlg';
          const tryFill = (el) => {
            if (!el) return false;
            el.focus();
            if ('value' in el) {
              el.value = '';
              el.dispatchEvent(new Event('input', {bubbles:true}));
              el.value = q;
              el.dispatchEvent(new Event('input', {bubbles:true}));
              el.dispatchEvent(new Event('change', {bubbles:true}));
              return true;
            }
            if (el.isContentEditable) {
              el.textContent = q;
              el.dispatchEvent(new Event('input', {bubbles:true}));
              return true;
            }
            return false;
          };
          const host = dlg.querySelector('#search-yours') || document.querySelector('#search-yours');
          if (host) {
            if (tryFill(host)) return 'host';
            if (host.shadowRoot) {
              const inp = host.shadowRoot.querySelector('input,textarea,[contenteditable=true]');
              if (tryFill(inp)) return 'host_shadow';
            }
            const inp = host.querySelector('input,textarea,[contenteditable=true]');
            if (tryFill(inp)) return 'host_child';
          }
          // any input in dialog (incl shadow)
          const walk = (root) => {
            for (const el of root.querySelectorAll('input,textarea,[contenteditable=true]')) {
              const ph = (el.placeholder||'') + (el.getAttribute('aria-label')||'');
              if (/search/i.test(ph) || el.id.includes('search')) {
                if (tryFill(el)) return 'walk_'+el.tagName;
              }
            }
            for (const el of root.querySelectorAll('*')) {
              if (el.shadowRoot) {
                const x = walk(el.shadowRoot);
                if (x) return x;
              }
            }
            return null;
          };
          return walk(dlg) || 'fail';
        }""",
        query,
    )
    if filled and filled != "fail" and filled != "no_dlg":
        page.wait_for_timeout(400)
        # Also type via keyboard to trigger search debounce
        try:
            page.locator("ytcp-video-pick-dialog input").first.click(force=True, timeout=1500)
            page.keyboard.press("Meta+a")
            page.keyboard.press("Backspace")
            page.keyboard.type(query, delay=25)
            return f"kb+{filled}"
        except Exception:
            return filled
    # Playwright fill fallback
    for sel in (
        "ytcp-video-pick-dialog #search-yours input",
        "ytcp-video-pick-dialog input",
        "#search-yours input",
    ):
        loc = page.locator(sel)
        if loc.count():
            loc.first.click(force=True)
            page.keyboard.press("Meta+a")
            page.keyboard.press("Backspace")
            loc.first.fill(query)
            return f"fill:{sel}"
    try:
        box = page.get_by_placeholder(re.compile(r"Search your videos", re.I))
        if box.count():
            box.first.click(force=True)
            page.keyboard.press("Meta+a")
            page.keyboard.type(query, delay=25)
            return "placeholder_type"
    except Exception:
        pass
    return "none"


def open_picker(page, r: dict) -> bool:
    picker = page.locator(
        "ytcp-shorts-content-links-picker #linked-video-editor-link, "
        "ytcp-shorts-content-links-picker ytcp-text-dropdown-trigger, "
        "ytcp-shorts-content-links-picker"
    )
    if picker.count():
        picker.first.scroll_into_view_if_needed()
        picker.first.click(force=True)
        r["opened"] = "shorts_picker"
    else:
        page.get_by_text("Related video", exact=True).first.scroll_into_view_if_needed()
        page.get_by_text("Related video", exact=True).first.click(force=True)
        r["opened"] = "label"
    page.wait_for_timeout(2000)
    try:
        page.locator("ytcp-video-pick-dialog").wait_for(timeout=20000)
        return True
    except Exception:
        r["error"] = "no_dialog"
        return False


def pick_cell(page, r: dict) -> bool:
    cells = page.locator("ytcp-video-pick-dialog ytcp-video-list-cell-video")
    if not cells.count():
        cells = page.locator(
            "ytcp-video-pick-dialog ytcp-entity-card, "
            "ytcp-video-pick-dialog [role='option'], "
            "ytcp-video-pick-dialog ytcp-video-row"
        )
    r["cell_count"] = cells.count()
    # Also try clicking by text match in dialog
    needles = [
        LONG_ID,
        "Why Haven't We Found Aliens",
        "Fermi Paradox Explained",
        "Orbit's Cosmic Journey",
        "Haven't We Found Aliens",
    ]
    for i in range(cells.count()):
        t = cells.nth(i).inner_text()
        is_short = bool(re.search(r"\b0:\d{2}\b", t)) and not re.search(
            r"\b1[0-9]:\d{2}\b|\b[2-9]:\d{2}\b", t
        )
        if any(n in t for n in needles) and not is_short:
            cells.nth(i).click(force=True)
            r["picked"] = t[:200]
            return True
    # JS click by title
    hit = page.evaluate(
        """(needles) => {
          const dlg = document.querySelector('ytcp-video-pick-dialog');
          if (!dlg) return null;
          const cands = [];
          const walk = (root) => {
            for (const el of root.querySelectorAll('*')) {
              const t = (el.innerText||'').replace(/\\s+/g,' ').trim();
              if (!t || t.length < 10 || t.length > 300) continue;
              if (!needles.some(n => t.includes(n))) continue;
              const r = el.getBoundingClientRect();
              if (r.width > 80 && r.height > 30 && r.height < 200)
                cands.push({x:r.x+r.width/2, y:r.y+r.height/2, t:t.slice(0,160), h:r.height});
              if (el.shadowRoot) walk(el.shadowRoot);
            }
          };
          walk(dlg);
          cands.sort((a,b)=>a.h-b.h);
          return cands[0]||null;
        }""",
        needles,
    )
    if hit:
        page.mouse.click(hit["x"], hit["y"])
        r["picked"] = hit["t"]
        r["picked_via"] = "js_coords"
        return True
    return False


def set_related(page, num: str, sid: str) -> dict:
    r: dict = {"id": num, "video_id": sid, "ok": False}
    page.goto(
        f"https://studio.youtube.com/video/{sid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    skip(page)
    dismiss(page)

    # Already set?
    body0 = page.locator("body").inner_text()
    chunk0 = body0.split("Related video", 1)[-1][:200] if "Related video" in body0 else ""
    if "None" not in chunk0[:40] and (
        "Fermi" in chunk0 or "Aliens" in chunk0 or "Orbit" in chunk0
    ):
        r["ok"] = True
        r["already"] = chunk0[:120]
        return r

    if not open_picker(page, r):
        page.screenshot(path=str(AUDIT / f"rel_v03_{num}_nodlg.png"))
        return r

    page.wait_for_timeout(2500)  # allow default list to populate
    page.screenshot(path=str(AUDIT / f"rel_v03_{num}_open.png"))
    r["dump_open"] = dialog_dump(page)

    # Try without search first (browse default list)
    if pick_cell(page, r):
        r["search"] = "none_default"
    else:
        queries = [
            "Haven't We Found",
            "Fermi Paradox Explained",
            LONG_TITLE,
            LONG_TITLE_FULL,
            LONG_ID,
            "Aliens",
            "Orbit",
            "Why Haven",
        ]
        for q in queries:
            method = fill_search(page, q)
            page.wait_for_timeout(2800)
            body = page.locator("ytcp-video-pick-dialog").inner_text()
            r.setdefault("searches", []).append(
                {"q": q, "method": method, "snip": body[:180]}
            )
            page.screenshot(path=str(AUDIT / f"rel_v03_{num}_q_{q[:12].replace('/','')}.png"))
            if "No matching results" in body:
                continue
            if pick_cell(page, r):
                r["search"] = q
                break
        else:
            r["error"] = "not_found"
            r["dump_fail"] = dialog_dump(page)
            page.keyboard.press("Escape")
            return r

    page.wait_for_timeout(800)
    for name in ("Done", "Select", "Save"):
        b = page.get_by_role("button", name=name, exact=True)
        if b.count() and b.first.is_visible() and b.first.is_enabled():
            b.first.click(force=True)
            page.wait_for_timeout(900)
            r["confirm"] = name
            break

    r["saved"] = save(page)
    page.goto(
        f"https://studio.youtube.com/video/{sid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    skip(page)
    dismiss(page)
    body = page.locator("body").inner_text()
    chunk = body.split("Related video", 1)[-1][:250] if "Related video" in body else ""
    r["related_chunk"] = chunk
    r["ok"] = "None" not in chunk[:40] and (
        "Fermi" in chunk
        or "Aliens" in chunk
        or "Alone" in chunk
        or "Orbit" in chunk
        or "Haven't" in chunk
    )
    page.screenshot(path=str(AUDIT / f"rel_v03_{num}_done.png"))
    return r


def pin_via_studio_edit(page) -> dict:
    """Try Studio edit-page first comment (sometimes available)."""
    r: dict = {"ok": False, "via": "studio_edit"}
    page.goto(
        f"https://studio.youtube.com/video/{LONG_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    skip(page)
    dismiss(page)
    for _ in range(8):
        page.mouse.wheel(0, 900)
        page.wait_for_timeout(200)
    page.screenshot(path=str(AUDIT / "pin_v03_studio_edit.png"), full_page=True)
    try:
        box = page.get_by_role(
            "textbox", name=re.compile(r"Add a first comment|first comment", re.I)
        )
        if box.count() == 0:
            page.get_by_text(re.compile(r"Add a first comment", re.I)).first.click(
                force=True, timeout=3000
            )
            page.wait_for_timeout(600)
            box = page.get_by_role("textbox", name=re.compile(r"comment", re.I))
        if box.count():
            box.first.click(force=True)
            page.keyboard.type(PINNED, delay=3)
            page.wait_for_timeout(400)
            for name in ("Comment", "Post", "Save"):
                b = page.get_by_role("button", name=name, exact=True)
                if b.count() and b.first.is_enabled():
                    b.first.click(force=True)
                    page.wait_for_timeout(2000)
                    r["posted"] = True
                    r["ok"] = True
                    break
        else:
            r["error"] = "no_first_comment_box"
    except Exception as e:
        r["error"] = str(e)[:250]
    return r


def pin_via_watch(page) -> dict:
    r: dict = {"ok": False, "via": "watch"}
    page.goto(
        f"https://www.youtube.com/watch?v={LONG_ID}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(5000)
    for name in ("Accept all", "Reject all", "Got it"):
        try:
            b = page.get_by_role("button", name=name, exact=False)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=1000)
        except Exception:
            pass

    # Scroll comments into view
    page.evaluate("window.scrollTo(0, 900)")
    page.wait_for_timeout(2000)
    page.evaluate("window.scrollTo(0, 1400)")
    page.wait_for_timeout(1500)

    # Activate comment box (YouTube uses contenteditable)
    activated = page.evaluate(
        """() => {
          const sels = [
            '#simplebox-placeholder',
            'ytd-comment-simplebox-renderer #placeholder-area',
            '#placeholder-area',
            '#contenteditable-root',
            'ytd-commentbox #contenteditable-root',
          ];
          for (const s of sels) {
            const el = document.querySelector(s);
            if (el) { el.click(); return s; }
          }
          return null;
        }"""
    )
    r["activated"] = activated
    page.wait_for_timeout(800)

    # Type into contenteditable
    typed = page.evaluate(
        """(text) => {
          const root = document.querySelector(
            'ytd-commentbox #contenteditable-root, #contenteditable-root'
          );
          if (!root) return false;
          root.focus();
          root.innerText = text;
          root.dispatchEvent(new InputEvent('input', {bubbles:true, data:text}));
          return true;
        }""",
        PINNED,
    )
    if not typed:
        try:
            box = page.get_by_role("textbox", name=re.compile(r"Add a comment", re.I))
            box.first.click(force=True)
            page.keyboard.insert_text(PINNED)
            typed = True
        except Exception as e:
            r["type_err"] = str(e)[:200]
    r["typed"] = bool(typed)
    page.wait_for_timeout(600)
    page.screenshot(path=str(AUDIT / "pin_v03_watch_typed.png"))

    # Click Comment submit
    submitted = page.evaluate(
        """() => {
          const btns = [
            ...document.querySelectorAll(
              '#submit-button button, ytd-button-renderer#submit-button button, #submit-button'
            )
          ];
          for (const b of btns) {
            const dis = b.disabled || b.getAttribute('aria-disabled')==='true';
            const r = b.getBoundingClientRect();
            if (!dis && r.width>10) { b.click(); return 'dom'; }
          }
          return null;
        }"""
    )
    if not submitted:
        try:
            b = page.get_by_role("button", name="Comment", exact=True)
            if b.count() and b.first.is_enabled():
                b.first.click(force=True)
                submitted = "role"
        except Exception as e:
            r["submit_err"] = str(e)[:200]
    r["submitted"] = submitted
    page.wait_for_timeout(3500)
    page.screenshot(path=str(AUDIT / "pin_v03_watch_posted.png"))

    # Sort newest + pin
    try:
        page.get_by_text("Sort by", exact=False).first.click(force=True, timeout=3000)
        page.wait_for_timeout(500)
        page.get_by_text("Newest first", exact=False).first.click(force=True)
        page.wait_for_timeout(2000)
    except Exception:
        pass

    needle = "best explains the silence"
    # Reload to ensure comment appears
    page.reload(wait_until="domcontentloaded")
    page.wait_for_timeout(4000)
    page.evaluate("window.scrollTo(0, 1200)")
    page.wait_for_timeout(1500)
    try:
        page.get_by_text("Sort by", exact=False).first.click(force=True, timeout=2000)
        page.wait_for_timeout(400)
        page.get_by_text("Newest first", exact=False).first.click(force=True)
        page.wait_for_timeout(1500)
    except Exception:
        pass

    comment = page.locator("ytd-comment-thread-renderer").filter(has_text=needle)
    r["comment_count"] = comment.count()
    if comment.count() == 0:
        # maybe already posted earlier
        body = page.locator("body").inner_text()
        r["has_needle"] = needle in body
        if not r["has_needle"]:
            r["error"] = "comment_not_found"
            page.screenshot(path=str(AUDIT / "pin_v03_watch_missing.png"), full_page=True)
            r["ok"] = bool(submitted)
            return r

    try:
        thread = comment.first
        # action menu (three dots)
        menu = thread.locator(
            "#action-menu button, #action-menu yt-icon-button, "
            "ytd-menu-renderer yt-icon-button, #button-shape button"
        )
        if menu.count():
            menu.first.click(force=True)
        else:
            # last icon button in thread header
            thread.locator("yt-icon-button, button[aria-label*='Action']").last.click(
                force=True
            )
        page.wait_for_timeout(700)
        pin_item = page.get_by_text(re.compile(r"^Pin$", re.I))
        if pin_item.count() == 0:
            pin_item = page.get_by_role("menuitem", name=re.compile(r"Pin", re.I))
        pin_item.first.click(force=True)
        page.wait_for_timeout(800)
        for name in ("Pin", "Confirm", "OK"):
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True)
                page.wait_for_timeout(1200)
                break
        r["pinned"] = True
        r["ok"] = True
        r["posted"] = True
    except Exception as e:
        r["pin_err"] = str(e)[:250]
        r["ok"] = bool(submitted)  # posted but pin failed
        r["posted"] = bool(submitted)

    page.screenshot(path=str(AUDIT / "pin_v03_watch_final.png"), full_page=True)
    return r


def pin_via_studio_comments(page) -> dict:
    r: dict = {"ok": False, "via": "studio_comments"}
    page.goto(
        f"https://studio.youtube.com/video/{LONG_ID}/comments",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    skip(page)
    dismiss(page)
    page.screenshot(path=str(AUDIT / "pin_v03_studio_comments.png"), full_page=True)
    needle = "best explains the silence"
    try:
        row = page.get_by_text(needle, exact=False)
        if row.count() == 0:
            r["error"] = "comment_not_in_studio"
            return r
        row.first.click(force=True)
        page.wait_for_timeout(500)
        # open menu near comment
        page.get_by_role("button", name=re.compile(r"Action|More|menu", re.I)).first.click(
            force=True, timeout=3000
        )
        page.wait_for_timeout(500)
        page.get_by_text(re.compile(r"Pin", re.I)).first.click(force=True)
        page.wait_for_timeout(800)
        for name in ("Pin", "Confirm", "OK"):
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True)
                break
        r["ok"] = True
        r["pinned"] = True
    except Exception as e:
        r["error"] = str(e)[:250]
    return r


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    result: dict = {
        "long_id": LONG_ID,
        "long_public": None,
        "related": [],
        "pin": None,
        "ok": False,
    }
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 1100},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        print("CHECK long public…", flush=True)
        result["long_public"] = check_long_public(page)
        print(f"  → {result['long_public']}", flush=True)
        OUT.write_text(json.dumps(result, indent=2) + "\n")

        if not result["long_public"].get("public"):
            print("WARN: long not Public — Related picker may stay empty", flush=True)

        for num, sid in SHORTS:
            print(f"RELATED {num} {sid}…", flush=True)
            try:
                rr = set_related(page, num, sid)
            except Exception as e:
                rr = {"id": num, "video_id": sid, "ok": False, "error": str(e)[:300]}
            result["related"].append(rr)
            print(
                f"  → ok={rr.get('ok')} {rr.get('error') or rr.get('picked','')[:80]}",
                flush=True,
            )
            OUT.write_text(json.dumps(result, indent=2) + "\n")

        print("PIN studio edit…", flush=True)
        pin = pin_via_studio_edit(page)
        if not pin.get("ok"):
            print("PIN watch…", flush=True)
            pin = pin_via_watch(page)
        if pin.get("posted") and not pin.get("pinned"):
            print("PIN studio comments…", flush=True)
            pin2 = pin_via_studio_comments(page)
            if pin2.get("ok"):
                pin = pin2
            else:
                pin["studio_comments"] = pin2
        result["pin"] = pin
        print(f"  → {pin}", flush=True)

        ctx.close()

    result["ok"] = all(x.get("ok") for x in result["related"]) and bool(
        result.get("pin", {}).get("ok")
    )
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print("RESULT", OUT, "ok=", result["ok"])
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
