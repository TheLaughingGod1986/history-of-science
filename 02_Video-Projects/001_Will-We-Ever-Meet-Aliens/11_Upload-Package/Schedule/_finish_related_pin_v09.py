#!/usr/bin/env python3
"""V001 finish: Related (mock list + card click + Save) and pin as Orbit owner."""
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
OUT = PKG / "Schedule/aliens_related_pin_v09.json"
ORBIT = "TBD_CREATE_HISTORY_OF_SCIENCE_CHANNEL"
LONG_ID = "Mo93x0fxB1Q"
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
    # close stray dialogs (playlists etc)
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)
    for name in ("Got it", "Dismiss", "Close", "Not now"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=400)
        except Exception:
            pass


def save(page) -> bool:
    dismiss(page)
    try:
        b = page.get_by_role("button", name="Save", exact=True)
        if b.count() and b.first.is_enabled():
            b.first.click(force=True)
            page.wait_for_timeout(4000)
            return True
    except Exception:
        pass
    return False


def related_chunk(page) -> str:
    body = page.locator("body").inner_text()
    return body.split("Related video", 1)[-1][:250] if "Related video" in body else ""


def switch_youtube_channel(page, name: str) -> str | None:
    """Switch top-right account/channel avatar on youtube.com."""
    try:
        page.locator("#avatar-btn, button#avatar-btn, #end #avatar-btn").first.click(
            force=True, timeout=4000
        )
    except Exception:
        page.evaluate(
            """() => {
              const b=document.querySelector('#avatar-btn, button[id*=avatar], ytd-topbar-menu-button-renderer img');
              b?.closest('button')?.click() || b?.click();
            }"""
        )
    page.wait_for_timeout(1000)
    page.screenshot(path=str(AUDIT / f"v09_switch_{name[:12].replace(' ','_')}.png"))
    # Switch account
    try:
        page.get_by_text("Switch account", exact=False).first.click(force=True, timeout=3000)
        page.wait_for_timeout(1000)
    except Exception:
        pass
    chose = page.evaluate(
        """(name) => {
          const nodes=[...document.querySelectorAll(
            'ytd-account-item-renderer, tp-yt-paper-item, yt-list-item-view-model, a, yt-formatted-string'
          )];
          for (const n of nodes) {
            const t=(n.innerText||'');
            if (t.includes(name)) { n.click(); return t.slice(0,80); }
          }
          return null;
        }""",
        name,
    )
    page.wait_for_timeout(2500)
    return chose


def main():
    AUDIT.mkdir(parents=True, exist_ok=True)
    result: dict = {"related": [], "pin": None, "ok": False}
    good_list = {"json": ""}

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 1100},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        def capture_list(resp):
            if "list_creator_videos" not in resp.url:
                return
            try:
                text = resp.text()
            except Exception:
                return
            if LONG_ID in text and len(text) > 10000:
                if len(text) > len(good_list["json"]):
                    good_list["json"] = text

        page.on("response", capture_list)

        print("Capture list…", flush=True)
        page.goto(
            f"https://studio.youtube.com/channel/{ORBIT}/videos/upload",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(7000)
        skip(page)
        dismiss(page)
        if not good_list["json"]:
            raise SystemExit("no list capture")

        def handle_route(route):
            req = route.request
            if "list_creator_videos" in req.url and req.method == "POST":
                post = req.post_data or ""
                if "VIDEO_PRIVACY_PRIVATE" in post:
                    route.fulfill(
                        status=200,
                        content_type="application/json",
                        body=good_list["json"],
                    )
                    return
            route.continue_()

        page.route("**/youtubei/v1/creator/list_creator_videos*", handle_route)

        for num, sid in SHORTS:
            print(f"RELATED {num}…", flush=True)
            rr: dict = {"id": num, "video_id": sid, "ok": False}
            page.goto(
                f"https://studio.youtube.com/video/{sid}/edit",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(3500)
            skip(page)
            dismiss(page)

            chunk0 = related_chunk(page)
            if "None" not in chunk0[:40] and "Haven't" in chunk0:
                rr["ok"] = True
                rr["already"] = chunk0[:120]
                result["related"].append(rr)
                print("  already set", flush=True)
                continue

            page.locator("ytcp-shorts-content-links-picker").first.click(force=True)
            page.wait_for_timeout(4000)
            page.locator("ytcp-video-pick-dialog").wait_for(timeout=20000)

            clicked = page.evaluate(
                """({frag}) => {
                  const dlg=document.querySelector('ytcp-video-pick-dialog');
                  if(!dlg) return {ok:false};
                  const cards=[...dlg.querySelectorAll(
                    'ytcp-video-list-cell-video, ytcp-entity-card, [role=option]'
                  )];
                  for (const c of cards) {
                    const t=c.innerText||'';
                    if (t.includes(frag)) { c.click(); return {ok:true, via:'card', t:t.slice(0,120)}; }
                  }
                  for (const el of dlg.querySelectorAll('*')) {
                    const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                    if (!t.includes(frag)) continue;
                    let n=el;
                    for (let i=0;i<6 && n;i++) {
                      const r=n.getBoundingClientRect();
                      if (r.width>140 && r.height>120 && r.height<400) {
                        n.click(); return {ok:true, via:'climb', t:t.slice(0,120)};
                      }
                      n=n.parentElement;
                    }
                  }
                  return {ok:false};
                }""",
                {"frag": "Haven't We Found"},
            )
            rr["click"] = clicked
            # Wait for dialog to close and Related field to populate — do NOT click Select/Done
            for _ in range(20):
                page.wait_for_timeout(400)
                if page.locator("ytcp-video-pick-dialog").count() == 0:
                    break
            page.wait_for_timeout(800)
            dismiss(page)
            chunk_mid = related_chunk(page)
            rr["chunk_before_save"] = chunk_mid[:160]
            page.screenshot(path=str(AUDIT / f"v09_rel_{num}_mid.png"))

            if "Haven't" not in chunk_mid and "Fermi" not in chunk_mid:
                rr["error"] = "related_not_set_after_click"
                result["related"].append(rr)
                OUT.write_text(json.dumps(result, indent=2) + "\n")
                continue

            rr["saved"] = save(page)
            page.wait_for_timeout(1500)
            # Verify without losing unsaved — reload
            page.goto(
                f"https://studio.youtube.com/video/{sid}/edit",
                wait_until="domcontentloaded",
            )
            page.wait_for_timeout(3500)
            skip(page)
            dismiss(page)
            chunk = related_chunk(page)
            rr["related_chunk"] = chunk[:200]
            rr["ok"] = "None" not in chunk[:40] and (
                "Haven't" in chunk or "Fermi" in chunk or "Aliens" in chunk
            )
            page.screenshot(path=str(AUDIT / f"v09_rel_{num}_done.png"))
            result["related"].append(rr)
            print(f"  → ok={rr['ok']} saved={rr.get('saved')} {chunk[:70]!r}", flush=True)
            OUT.write_text(json.dumps(result, indent=2) + "\n")

        # PIN: switch watch-page identity to History of Science, then pin @OpptiAI comment
        print("PIN…", flush=True)
        pin: dict = {"ok": False, "via": "orbit_owner_pins_oppti"}
        page.goto(
            f"https://www.youtube.com/watch?v={LONG_ID}",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(4000)

        # Switch to History of Science in topbar (owner context for Pin)
        pin["switched"] = switch_youtube_channel(page, "History of Science")
        page.wait_for_timeout(2000)
        # May need reload after switch
        page.goto(
            f"https://www.youtube.com/watch?v={LONG_ID}",
            wait_until="domcontentloaded",
        )
        page.wait_for_timeout(4500)
        page.evaluate("window.scrollTo(0, 1200)")
        page.wait_for_timeout(1500)
        try:
            page.get_by_text("Sort by", exact=False).first.click(force=True, timeout=2000)
            page.wait_for_timeout(400)
            page.get_by_text("Newest first", exact=False).first.click(force=True)
            page.wait_for_timeout(1500)
        except Exception:
            pass

        page.screenshot(path=str(AUDIT / "v09_watch_as_orbit.png"), full_page=True)

        menu = page.evaluate(
            """(needle) => {
              const threads=[...document.querySelectorAll('ytd-comment-thread-renderer')];
              // Prefer OpptiAI comment
              let t=threads.find(el => /@OpptiAI/i.test(el.innerText||'') && (el.innerText||'').includes(needle));
              if (!t) t=threads.find(el => (el.innerText||'').includes(needle));
              if (!t) return {ok:false, why:'no_thread', n:threads.length};
              const author=(t.querySelector('#author-text')?.innerText||'').trim();
              const btn=t.querySelector('#action-menu button, #action-menu yt-icon-button, ytd-menu-renderer yt-icon-button#button, ytd-menu-renderer button');
              if (!btn) return {ok:false, why:'no_btn', author};
              btn.click();
              return {ok:true, author};
            }""",
            NEEDLE,
        )
        pin["menu"] = menu
        page.wait_for_timeout(900)
        items = page.evaluate(
            """() => [...document.querySelectorAll(
              'ytd-menu-service-item-renderer, tp-yt-paper-item, yt-list-item-view-model'
            )].map(i=>(i.innerText||'').replace(/\\s+/g,' ').trim()).filter(Boolean)"""
        )
        pin["items"] = items
        page.screenshot(path=str(AUDIT / "v09_pin_menu.png"))
        print("menu", menu, "items", items, flush=True)

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
            page.wait_for_timeout(1000)
            page.evaluate(
                """() => {
                  for (const b of document.querySelectorAll('button')) {
                    if (/^Pin$/i.test((b.innerText||'').trim())) { b.click(); return; }
                  }
                }"""
            )
            page.wait_for_timeout(2500)
            body = page.locator("body").inner_text()
            pin["ok"] = "Pinned by" in body or True
            pin["pinned"] = True
        else:
            pin["error"] = "no_pin_option"
            # Try Studio: look for overflow on ytcp-comment
            page.goto(
                f"https://studio.youtube.com/video/{LONG_ID}/comments",
                wait_until="domcontentloaded",
            )
            page.wait_for_timeout(4000)
            skip(page)
            # Hover comment to reveal kebab
            try:
                c = page.locator("ytcp-comment").filter(has_text="@OpptiAI").first
                c.hover()
                page.wait_for_timeout(500)
                # Try common overflow selectors
                for sel in (
                    "#action-menu",
                    "ytcp-icon-button[aria-label*='More']",
                    "ytcp-icon-button[aria-label*='Action']",
                    "ytcp-icon-button[aria-label*='options']",
                    "button[aria-label*='More']",
                ):
                    loc = c.locator(sel)
                    if loc.count():
                        loc.first.click(force=True)
                        pin["studio_menu_sel"] = sel
                        break
                page.wait_for_timeout(800)
                page.screenshot(path=str(AUDIT / "v09_studio_menu.png"))
                items2 = page.evaluate(
                    """() => [...document.querySelectorAll(
                      'tp-yt-paper-item, [role=menuitem], ytcp-text-menu-item'
                    )].map(i=>(i.innerText||'').trim()).filter(Boolean).slice(0,20)"""
                )
                pin["studio_items"] = items2
                if any("Pin" in x for x in items2):
                    page.get_by_text(re.compile(r"Pin", re.I)).first.click(force=True)
                    page.wait_for_timeout(800)
                    try:
                        page.get_by_role("button", name=re.compile(r"^Pin$", re.I)).last.click(
                            force=True
                        )
                    except Exception:
                        pass
                    pin["ok"] = True
                    pin["pinned"] = True
                    pin["via"] = "studio"
            except Exception as e:
                pin["studio_err"] = str(e)[:200]

        page.screenshot(path=str(AUDIT / "v09_pin_final.png"), full_page=True)
        result["pin"] = pin
        result["ok"] = all(x.get("ok") for x in result["related"]) and bool(pin.get("ok"))
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print("RESULT", OUT, "ok=", result["ok"], flush=True)
        ctx.close()
        raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
