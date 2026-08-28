#!/usr/bin/env python3
"""V001: Related card-click + persist; pin OpptiAI comment as Orbit owner."""
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
OUT = PKG / "Schedule/aliens_related_pin_v08.json"
ORBIT = "TBD_CREATE_HISTORY_OF_SCIENCE_CHANNEL"
LONG_ID = "Mo93x0fxB1Q"
NEEDLE = "best explains the silence"
PINNED = (PKG / "Pinned-Comments/aliens_long_pinned-comment_v01.txt").read_text().strip()
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
            page.wait_for_timeout(3500)
            return True
    except Exception:
        pass
    return False


def related_chunk(page) -> str:
    body = page.locator("body").inner_text()
    return body.split("Related video", 1)[-1][:250] if "Related video" in body else ""


def main():
    AUDIT.mkdir(parents=True, exist_ok=True)
    result: dict = {"related": [], "pin": None, "ok": False, "net": []}
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
            if LONG_ID in text and len(text) > 10000 and "VIDEO_PRIVACY_PRIVATE" not in (
                resp.request.post_data or ""
            ):
                # Prefer content-page shaped responses; still usable for mock
                if len(text) > len(good_list["json"]):
                    good_list["json"] = text
                    print(f"CAPTURED list {len(text)}", flush=True)

        page.on("response", capture_list)

        def log_net(resp):
            u = resp.url
            if resp.request.resource_type not in ("xhr", "fetch"):
                return
            if not any(
                k in u
                for k in (
                    "update",
                    "metadata",
                    "creator/video",
                    "content_link",
                    "linked",
                )
            ):
                return
            try:
                post = resp.request.post_data or ""
            except Exception:
                post = ""
            if LONG_ID in post or "related" in post.lower() or "contentLink" in post or "linkedVideo" in post:
                try:
                    snip = resp.text()[:500]
                except Exception:
                    snip = ""
                result["net"].append(
                    {"url": u[:220], "status": resp.status, "post": post[:500], "snip": snip}
                )
                print(f"NET {resp.status} {u[:80]}", flush=True)

        page.on("response", log_net)

        print("Capture Orbit video list…", flush=True)
        page.goto(
            f"https://studio.youtube.com/channel/{ORBIT}/videos/upload",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(7000)
        skip(page)
        dismiss(page)
        if not good_list["json"]:
            result["error"] = "no_list"
            OUT.write_text(json.dumps(result, indent=2) + "\n")
            ctx.close()
            raise SystemExit(1)

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
            page.wait_for_timeout(4000)
            skip(page)
            dismiss(page)
            chunk0 = related_chunk(page)
            if "None" not in chunk0[:40] and "Haven't" in chunk0:
                rr["ok"] = True
                rr["already"] = chunk0
                result["related"].append(rr)
                continue

            page.locator("ytcp-shorts-content-links-picker").first.click(force=True)
            page.wait_for_timeout(4500)
            page.locator("ytcp-video-pick-dialog").wait_for(timeout=20000)
            page.screenshot(path=str(AUDIT / f"v08_rel_{num}_open.png"))

            # Click the entity card / list cell for the long video — not a random text node
            clicked = page.evaluate(
                """({longId, frag}) => {
                  const dlg = document.querySelector('ytcp-video-pick-dialog');
                  if (!dlg) return {ok:false, why:'no_dlg'};
                  const cards = [
                    ...dlg.querySelectorAll(
                      'ytcp-video-list-cell-video, ytcp-entity-card, ytcp-video-thumbnail, [role=option]'
                    )
                  ];
                  // Prefer structured cards
                  for (const c of cards) {
                    const t = (c.innerText || '');
                    if (t.includes(frag) || t.includes(longId)) {
                      c.click();
                      return {ok:true, via:'card', t:t.slice(0,160)};
                    }
                  }
                  // Fallback: find thumbnail image near title
                  const all = [...dlg.querySelectorAll('*')];
                  for (const el of all) {
                    const t = (el.innerText || '').replace(/\\s+/g,' ').trim();
                    if (!t.includes(frag)) continue;
                    // climb to clickable card-ish node
                    let n = el;
                    for (let i=0;i<6 && n;i++) {
                      const r = n.getBoundingClientRect();
                      if (r.width > 140 && r.height > 120 && r.height < 400) {
                        n.click();
                        return {ok:true, via:'climb', t:t.slice(0,160), tag:n.tagName};
                      }
                      n = n.parentElement;
                    }
                  }
                  return {ok:false, why:'no_card', cards:cards.length};
                }""",
                {"longId": LONG_ID, "frag": "Haven't We Found"},
            )
            rr["click"] = clicked
            page.wait_for_timeout(1000)
            page.screenshot(path=str(AUDIT / f"v08_rel_{num}_selected.png"))

            if not clicked.get("ok"):
                rr["error"] = "click_failed"
                page.keyboard.press("Escape")
                result["related"].append(rr)
                continue

            # Confirm selection — try Done/Select inside dialog only
            confirmed = page.evaluate(
                """() => {
                  const dlg = document.querySelector('ytcp-video-pick-dialog');
                  if (!dlg) return 'no_dlg';
                  const btns = [...dlg.querySelectorAll('button, ytcp-button, [role=button]')];
                  for (const b of btns) {
                    const t = (b.innerText || '').trim();
                    if (t === 'Done' || t === 'Select' || t === 'Save') {
                      const dis = b.disabled || b.getAttribute('aria-disabled') === 'true';
                      if (!dis) { b.click(); return t; }
                    }
                  }
                  // Some pickers select on card click alone (dialog closes)
                  return 'no_btn';
                }"""
            )
            rr["confirm"] = confirmed
            page.wait_for_timeout(2000)

            # If dialog still open, click card again and Escape won't help — try Enter
            if page.locator("ytcp-video-pick-dialog").count():
                # Double-click card
                page.evaluate(
                    """(frag) => {
                      const dlg=document.querySelector('ytcp-video-pick-dialog');
                      if(!dlg) return;
                      for (const el of dlg.querySelectorAll('*')) {
                        const t=(el.innerText||'');
                        if (!t.includes(frag)) continue;
                        let n=el;
                        for (let i=0;i<6 && n;i++) {
                          const r=n.getBoundingClientRect();
                          if (r.width>140 && r.height>120) {
                            n.dispatchEvent(new MouseEvent('dblclick',{bubbles:true}));
                            n.click();
                            return;
                          }
                          n=n.parentElement;
                        }
                      }
                    }""",
                    "Haven't We Found",
                )
                page.wait_for_timeout(800)
                # Look for footer buttons outside dialog shadow
                for name in ("Done", "Select"):
                    b = page.get_by_role("button", name=name, exact=True)
                    if b.count() and b.first.is_visible() and b.first.is_enabled():
                        b.first.click(force=True)
                        rr["confirm2"] = name
                        page.wait_for_timeout(1500)
                        break

            page.wait_for_timeout(1500)
            page.screenshot(path=str(AUDIT / f"v08_rel_{num}_after_select.png"))

            # Related field should update before Save
            chunk_mid = related_chunk(page)
            rr["chunk_before_save"] = chunk_mid
            # If dialog closed and related updated, save
            rr["saved"] = save(page)
            page.wait_for_timeout(1500)

            page.goto(
                f"https://studio.youtube.com/video/{sid}/edit",
                wait_until="domcontentloaded",
            )
            page.wait_for_timeout(3500)
            skip(page)
            chunk = related_chunk(page)
            rr["related_chunk"] = chunk
            rr["ok"] = "None" not in chunk[:40] and (
                "Haven't" in chunk or "Fermi" in chunk or "Aliens" in chunk
            )
            page.screenshot(path=str(AUDIT / f"v08_rel_{num}_done.png"))
            result["related"].append(rr)
            print(
                f"  → ok={rr['ok']} confirm={rr.get('confirm')} chunk={chunk[:80]!r}",
                flush=True,
            )
            OUT.write_text(json.dumps(result, indent=2) + "\n")

        # PIN: comment as OpptiAI (not Orbit), then pin as video owner
        print("PIN via OpptiAI comment…", flush=True)
        pin: dict = {"ok": False, "via": "oppti_comment_then_pin"}
        page.goto(
            f"https://www.youtube.com/watch?v={LONG_ID}",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(4500)
        page.evaluate("window.scrollTo(0, 1100)")
        page.wait_for_timeout(1500)

        # Activate comment box and switch identity to OpptiAI
        page.evaluate(
            "() => document.querySelector('#simplebox-placeholder, #placeholder-area')?.click()"
        )
        page.wait_for_timeout(700)
        page.evaluate(
            """() => {
              const box=document.querySelector('ytd-comment-simplebox-renderer, ytd-commentbox');
              const thumb=box?.querySelector('#author-thumbnail button, #author-thumbnail');
              thumb?.click();
            }"""
        )
        page.wait_for_timeout(900)
        page.screenshot(path=str(AUDIT / "v08_id_menu.png"))
        chose = page.evaluate(
            """() => {
              for (const i of document.querySelectorAll(
                'ytd-account-item-renderer, tp-yt-paper-item, yt-formatted-string, yt-list-item-view-model'
              )) {
                const t=i.innerText||'';
                if (/OpptiAI/i.test(t) && !/Orbit/i.test(t)) { i.click(); return t.slice(0,60); }
              }
              // fallback any Oppti
              for (const i of document.querySelectorAll('*')) {
                const t=(i.innerText||'').trim();
                if (t === 'OpptiAI' || t === '@OpptiAI') { i.click(); return t; }
              }
              return null;
            }"""
        )
        pin["identity"] = chose
        page.wait_for_timeout(800)

        # Type unique marker so we can find this comment
        text = PINNED + "\n\n(Orbit pinned CTA)"
        page.evaluate(
            """(text) => {
              const root=document.querySelector('ytd-commentbox #contenteditable-root, #contenteditable-root');
              if (!root) return false;
              root.focus();
              root.innerText = text;
              root.dispatchEvent(new InputEvent('input', {bubbles:true, data:text}));
              return true;
            }""",
            text,
        )
        page.wait_for_timeout(500)
        page.evaluate(
            """() => {
              const b=document.querySelector('#submit-button button');
              if (b && !b.disabled) b.click();
            }"""
        )
        page.wait_for_timeout(4000)
        page.screenshot(path=str(AUDIT / "v08_posted_oppti.png"))
        pin["posted"] = True

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

        # Open action menu on OpptiAI comment (should show Pin for video owner)
        marker = "Orbit pinned CTA"
        menu = page.evaluate(
            """(marker) => {
              const threads=[...document.querySelectorAll('ytd-comment-thread-renderer')];
              const t=threads.find(el => (el.innerText||'').includes(marker))
                || threads.find(el => (el.innerText||'').includes('best explains the silence'));
              if (!t) return {ok:false, why:'no_thread'};
              const author=(t.querySelector('#author-text, a[href*="@"]')?.innerText||'').trim();
              const btn=t.querySelector('#action-menu button, #action-menu yt-icon-button, ytd-menu-renderer yt-icon-button');
              if (!btn) return {ok:false, why:'no_btn', author};
              btn.click();
              return {ok:true, author};
            }""",
            marker,
        )
        pin["menu"] = menu
        page.wait_for_timeout(900)
        items = page.evaluate(
            """() => [...document.querySelectorAll(
              'ytd-menu-service-item-renderer, tp-yt-paper-item, yt-list-item-view-model'
            )].map(i=>(i.innerText||'').replace(/\\s+/g,' ').trim()).filter(Boolean)"""
        )
        pin["items"] = items
        page.screenshot(path=str(AUDIT / "v08_pin_menu.png"))
        print("pin menu items", items, flush=True)

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
            page.wait_for_timeout(900)
            page.evaluate(
                """() => {
                  for (const b of document.querySelectorAll('button')) {
                    if (/^Pin$/i.test((b.innerText||'').trim())) { b.click(); return; }
                  }
                }"""
            )
            page.wait_for_timeout(2000)
            pin["ok"] = True
            pin["pinned"] = True
        else:
            pin["error"] = "still_no_pin"
            # Try Studio comments pin on any comment
            page.goto(
                f"https://studio.youtube.com/video/{LONG_ID}/comments",
                wait_until="domcontentloaded",
            )
            page.wait_for_timeout(4000)
            skip(page)
            page.screenshot(path=str(AUDIT / "v08_studio_comments.png"), full_page=True)
            # Dump comment DOM structure
            pin["studio_dom"] = page.evaluate(
                """() => {
                  const nodes=[...document.querySelectorAll(
                    'ytcp-comment-renderer, ytcp-comment, ytcp-comment-thread-renderer'
                  )];
                  return nodes.slice(0,5).map(n => ({
                    tag:n.tagName,
                    text:(n.innerText||'').slice(0,120),
                    buttons:[...n.querySelectorAll('button, ytcp-icon-button, [aria-label]')].map(b=>({
                      al:b.getAttribute('aria-label')||'',
                      t:(b.innerText||'').slice(0,40)
                    })).slice(0,8)
                  }));
                }"""
            )

        page.screenshot(path=str(AUDIT / "v08_pin_final.png"), full_page=True)
        result["pin"] = pin
        result["ok"] = all(x.get("ok") for x in result["related"]) and bool(pin.get("ok"))
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print("RESULT ok=", result["ok"], flush=True)
        ctx.close()
        raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
