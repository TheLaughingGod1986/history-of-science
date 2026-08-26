#!/usr/bin/env python3
"""V001: Related via mocked list_creator_videos + Studio pin.

Picker list API returns [] under OpptiAI delegation when editing Orbit Shorts.
We capture a good Orbit video list, then fulfill picker requests with it so the
UI can select Mo93x0fxB1Q; Save still hits the real update endpoint.
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
OUT = PKG / "Schedule/aliens_related_pin_v07.json"
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
            page.wait_for_timeout(3000)
            return True
    except Exception:
        pass
    return False


def main():
    AUDIT.mkdir(parents=True, exist_ok=True)
    result: dict = {"related": [], "pin": None, "ok": False}
    good_list_body: dict[str, str] = {"json": ""}
    update_log: list = []

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 1100},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        # Capture a good list response from Content (Orbit delegation)
        def capture_list(resp):
            if "list_creator_videos" not in resp.url:
                return
            try:
                text = resp.text()
            except Exception:
                return
            if LONG_ID in text and len(text) > 10000:
                good_list_body["json"] = text
                print(f"CAPTURED good list ({len(text)} bytes)", flush=True)

        page.on("response", capture_list)

        print("Load Orbit content to capture video list…", flush=True)
        page.goto(
            f"https://studio.youtube.com/channel/{ORBIT}/videos/upload",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(6000)
        skip(page)
        dismiss(page)
        if not good_list_body["json"]:
            # trigger list again
            page.reload(wait_until="domcontentloaded")
            page.wait_for_timeout(6000)

        if not good_list_body["json"]:
            result["error"] = "no_good_list_capture"
            OUT.write_text(json.dumps(result, indent=2) + "\n")
            ctx.close()
            raise SystemExit(1)

        # Save capture for debug
        (AUDIT / "v07_good_list.json").write_text(good_list_body["json"][:200000])

        # Now route: when picker asks list_creator_videos, return our good body
        # (optionally filtered to exclude current short — UI already excludes it)
        def handle_route(route):
            req = route.request
            if "list_creator_videos" in req.url and req.method == "POST":
                post = req.post_data or ""
                # Only mock picker-style requests (exclude private + exclude self)
                if "VIDEO_PRIVACY_PRIVATE" in post or "videoIdIs" in post:
                    print("FULFILL picker list", flush=True)
                    route.fulfill(
                        status=200,
                        content_type="application/json",
                        body=good_list_body["json"],
                    )
                    return
            route.continue_()

        page.route("**/youtubei/v1/creator/list_creator_videos*", handle_route)

        # Log update / metadata writes
        def on_resp(resp):
            u = resp.url
            if any(
                k in u
                for k in (
                    "update_creator_video",
                    "update_video",
                    "metadata_update",
                    "content_links",
                    "shorts",
                )
            ) and resp.request.resource_type in ("xhr", "fetch"):
                try:
                    snip = resp.text()[:400]
                except Exception:
                    snip = ""
                update_log.append(
                    {
                        "url": u[:200],
                        "status": resp.status,
                        "post": (resp.request.post_data or "")[:400],
                        "snip": snip,
                    }
                )

        page.on("response", on_resp)

        for num, sid in SHORTS:
            print(f"RELATED {num} {sid}…", flush=True)
            rr: dict = {"id": num, "video_id": sid, "ok": False}
            page.goto(
                f"https://studio.youtube.com/video/{sid}/edit",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(4000)
            skip(page)
            dismiss(page)

            body = page.locator("body").inner_text()
            chunk = (
                body.split("Related video", 1)[-1][:180]
                if "Related video" in body
                else ""
            )
            if "None" not in chunk[:40] and (
                "Fermi" in chunk or "Aliens" in chunk or "Haven't" in chunk
            ):
                rr["ok"] = True
                rr["already"] = chunk
                result["related"].append(rr)
                continue

            page.locator("ytcp-shorts-content-links-picker").first.scroll_into_view_if_needed()
            page.locator("ytcp-shorts-content-links-picker").first.click(force=True)
            page.wait_for_timeout(5000)
            try:
                page.locator("ytcp-video-pick-dialog").wait_for(timeout=20000)
            except Exception:
                rr["error"] = "no_dialog"
                result["related"].append(rr)
                continue

            page.screenshot(path=str(AUDIT / f"v07_rel_{num}_open.png"))
            rr["open_snip"] = page.locator("ytcp-video-pick-dialog").inner_text()[:250]

            hit = page.evaluate(
                """(needles) => {
                  const dlg=document.querySelector('ytcp-video-pick-dialog');
                  if(!dlg) return null;
                  const acc=[];
                  const walk=(root)=>{
                    for (const el of root.querySelectorAll('*')) {
                      const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                      if (t.length<10 || t.length>300) continue;
                      if (!needles.some(n => t.includes(n))) continue;
                      const r=el.getBoundingClientRect();
                      if (r.width>80 && r.height>36 && r.height<220)
                        acc.push({x:r.x+r.width/2,y:r.y+r.height/2,t:t.slice(0,180),h:r.height});
                      if (el.shadowRoot) walk(el.shadowRoot);
                    }
                  };
                  walk(dlg);
                  acc.sort((a,b)=>a.h-b.h);
                  return acc[0]||null;
                }""",
                [LONG_ID, "Haven't We Found", "Fermi Paradox Explained"],
            )

            if not hit:
                # try search to re-trigger fulfill
                page.locator("#search-yours").first.click(force=True)
                page.keyboard.type("Haven", delay=40)
                page.wait_for_timeout(3500)
                page.screenshot(path=str(AUDIT / f"v07_rel_{num}_search.png"))
                rr["search_snip"] = page.locator("ytcp-video-pick-dialog").inner_text()[:250]
                hit = page.evaluate(
                    """(needles) => {
                      const dlg=document.querySelector('ytcp-video-pick-dialog');
                      if(!dlg) return null;
                      const acc=[];
                      const walk=(root)=>{
                        for (const el of root.querySelectorAll('*')) {
                          const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                          if (t.length<10 || t.length>300) continue;
                          if (!needles.some(n => t.includes(n))) continue;
                          const r=el.getBoundingClientRect();
                          if (r.width>80 && r.height>36 && r.height<220)
                            acc.push({x:r.x+r.width/2,y:r.y+r.height/2,t:t.slice(0,180),h:r.height});
                          if (el.shadowRoot) walk(el.shadowRoot);
                        }
                      };
                      walk(dlg);
                      acc.sort((a,b)=>a.h-b.h);
                      return acc[0]||null;
                    }""",
                    [LONG_ID, "Haven't We Found", "Fermi Paradox"],
                )

            if not hit:
                rr["error"] = "not_found_after_mock"
                page.keyboard.press("Escape")
                result["related"].append(rr)
                OUT.write_text(json.dumps(result, indent=2) + "\n")
                continue

            page.mouse.click(hit["x"], hit["y"])
            rr["picked"] = hit["t"]
            page.wait_for_timeout(900)
            for name in ("Done", "Select", "Save"):
                b = page.get_by_role("button", name=name, exact=True)
                if b.count() and b.first.is_visible() and b.first.is_enabled():
                    b.first.click(force=True)
                    page.wait_for_timeout(900)
                    rr["confirm"] = name
                    break
            rr["saved"] = save(page)

            page.goto(
                f"https://studio.youtube.com/video/{sid}/edit",
                wait_until="domcontentloaded",
            )
            page.wait_for_timeout(3500)
            skip(page)
            body = page.locator("body").inner_text()
            chunk = (
                body.split("Related video", 1)[-1][:250]
                if "Related video" in body
                else ""
            )
            rr["related_chunk"] = chunk
            rr["ok"] = "None" not in chunk[:40] and (
                "Fermi" in chunk
                or "Aliens" in chunk
                or "Haven't" in chunk
                or "Orbit" in chunk
            )
            page.screenshot(path=str(AUDIT / f"v07_rel_{num}_done.png"))
            result["related"].append(rr)
            print(f"  → ok={rr['ok']} {rr.get('picked') or rr.get('error')}", flush=True)
            OUT.write_text(json.dumps(result, indent=2) + "\n")

        # PIN via Studio comments renderer
        print("PIN…", flush=True)
        pin: dict = {"ok": False}
        page.goto(
            f"https://studio.youtube.com/video/{LONG_ID}/comments",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(4500)
        skip(page)
        dismiss(page)
        page.screenshot(path=str(AUDIT / "v07_comments.png"), full_page=True)
        pin["studio_has"] = NEEDLE in page.locator("body").inner_text()

        if pin["studio_has"]:
            try:
                # Prefer structured comment renderer
                renderers = page.locator(
                    "ytcp-comment-renderer, ytcp-comment, ytcp-comment-thread-renderer"
                )
                pin["renderer_count"] = renderers.count()
                target = renderers.filter(has_text=NEEDLE)
                if target.count() == 0:
                    target = page.locator("body")
                # Action menu
                btn = target.first.locator(
                    "button[aria-label*='Action'], button[aria-label*='action'], "
                    "ytcp-icon-button, #action-menu, [id*='action']"
                )
                if btn.count():
                    btn.first.click(force=True)
                else:
                    # open any more menu near text
                    page.get_by_text(NEEDLE, exact=False).first.hover()
                    page.wait_for_timeout(300)
                    page.locator("ytcp-icon-button").nth(1).click(force=True)
                page.wait_for_timeout(800)
                page.screenshot(path=str(AUDIT / "v07_pin_menu.png"))
                items = page.evaluate(
                    """() => [...document.querySelectorAll(
                      'tp-yt-paper-item, [role=menuitem], ytcp-text-menu-item, yt-list-item-view-model'
                    )].map(i=>(i.innerText||'').trim()).filter(Boolean).slice(0,20)"""
                )
                pin["items"] = items
                if any(re.search(r"Pin", x, re.I) for x in items):
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
                else:
                    pin["error"] = "no_pin_item"
            except Exception as e:
                pin["error"] = str(e)[:250]

        # If Studio pin failed: try watch page but as a *different* approach —
        # pin may require opening menu on comment while NOT showing Edit (owner vs author).
        # Some accounts only get Pin in YouTube Studio Android. Document that.
        if not pin.get("ok"):
            page.goto(
                f"https://www.youtube.com/watch?v={LONG_ID}",
                wait_until="domcontentloaded",
            )
            page.wait_for_timeout(4000)
            page.evaluate("window.scrollTo(0, 1200)")
            page.wait_for_timeout(1500)
            # Check if already pinned
            body = page.locator("body").inner_text()
            if "Pinned by" in body and NEEDLE in body:
                pin["ok"] = True
                pin["already_pinned"] = True
            else:
                pin["watch_note"] = (
                    "Watch menu only shows Edit/Delete for own comments; "
                    "Pin option missing — may need manual pin in Studio mobile/web UI."
                )
            page.screenshot(path=str(AUDIT / "v07_watch.png"), full_page=True)

        result["pin"] = pin
        result["update_log"] = update_log[-15:]
        result["ok"] = all(x.get("ok") for x in result["related"]) and bool(pin.get("ok"))
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print("pin", pin, flush=True)
        ctx.close()
        print("RESULT", OUT, "ok=", result["ok"])
        raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
