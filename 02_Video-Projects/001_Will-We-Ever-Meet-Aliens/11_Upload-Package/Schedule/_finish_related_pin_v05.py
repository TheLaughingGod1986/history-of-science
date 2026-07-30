#!/usr/bin/env python3
"""Capture list_creator_videos for Related picker; pin as Orbit identity."""
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
OUT = PKG / "Schedule/aliens_related_pin_v05.json"
ORBIT = "UC_esArsDKd3GJvOkeO0DUog"
OPPTI = "UCXRVwrCxXpN_o9gvuHPKAPQ"
LONG_ID = "Mo93x0fxB1Q"
SHORTS = ["z-DLqoSoEBo", "UWwNKYf_aU8", "MO19iXYCu0c", "--CxhjNqtSY"]
PINNED = (PKG / "Pinned-Comments/aliens_long_pinned-comment_v01.txt").read_text().strip()
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


def main():
    AUDIT.mkdir(parents=True, exist_ok=True)
    result: dict = {"list_calls": [], "related": [], "pin": None}

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
                data = resp.json()
            except Exception:
                data = {"raw": resp.text()[:2000]}
            # Extract video ids/titles shallowly
            text = json.dumps(data)
            ids = re.findall(r'"videoId"\s*:\s*"([A-Za-z0-9_-]{11})"', text)
            titles = re.findall(r'"title"\s*:\s*\{[^}]*"simpleText"\s*:\s*"([^"]+)"', text)
            if not titles:
                titles = re.findall(r'"simpleText"\s*:\s*"([^"]{8,120})"', text)[:30]
            entry = {
                "status": resp.status,
                "url": resp.url[:120],
                "ids": list(dict.fromkeys(ids))[:40],
                "titles": titles[:20],
                "has_long": LONG_ID in text,
                "has_orbit": ORBIT in text,
                "has_oppti": OPPTI in text,
                "len": len(text),
                "snip": text[:600],
            }
            # request post data
            try:
                entry["post"] = (resp.request.post_data or "")[:800]
            except Exception:
                pass
            result["list_calls"].append(entry)
            print(
                f"LIST ids={len(entry['ids'])} has_long={entry['has_long']} "
                f"titles={entry['titles'][:3]}",
                flush=True,
            )
            (AUDIT / "v05_list_creator_videos.json").write_text(
                json.dumps(result["list_calls"], indent=2) + "\n"
            )

        page.on("response", on_response)

        # Ensure Studio is on Orbit channel
        print("Switch Orbit channel…", flush=True)
        page.goto(
            f"https://studio.youtube.com/channel/{ORBIT}/videos/upload",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(4000)
        skip(page)
        dismiss(page)
        page.screenshot(path=str(AUDIT / "v05_orbit_content.png"))
        body = page.locator("body").inner_text()
        result["content_titles"] = [
            ln.strip()
            for ln in body.splitlines()
            if "Orbit" in ln or "Aliens" in ln or "Fermi" in ln or "Black Hole" in ln
        ][:20]
        print("content titles hint:", result["content_titles"][:8], flush=True)

        # Open picker once and dump list
        sid = SHORTS[0]
        print(f"Open picker on {sid}…", flush=True)
        page.goto(
            f"https://studio.youtube.com/video/{sid}/edit",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3500)
        skip(page)
        dismiss(page)
        page.locator("ytcp-shorts-content-links-picker").first.scroll_into_view_if_needed()
        page.locator("ytcp-shorts-content-links-picker").first.click(force=True)
        page.wait_for_timeout(10000)  # wait for list API
        page.screenshot(path=str(AUDIT / "v05_picker.png"))
        result["picker_text"] = page.locator("ytcp-video-pick-dialog").inner_text()[:400]

        # If list empty, try typing a character to force search API
        page.locator("#search-yours").first.click(force=True)
        page.keyboard.type("a", delay=80)
        page.wait_for_timeout(5000)
        page.screenshot(path=str(AUDIT / "v05_picker_a.png"))
        result["picker_a"] = page.locator("ytcp-video-pick-dialog").inner_text()[:400]
        page.keyboard.press("Escape")

        # If we got list with long id, set related on all shorts
        has_long = any(c.get("has_long") for c in result["list_calls"])
        result["api_has_long"] = has_long
        print(f"api_has_long={has_long} calls={len(result['list_calls'])}", flush=True)

        if has_long or True:
            # Try setting related with longer waits + search "Black" / known titles from API
            search_terms = ["Aliens", "Fermi", "Black", "Orbit", LONG_ID]
            # Prefer titles from API that look like long-form
            for c in result["list_calls"]:
                for t in c.get("titles") or []:
                    if t and t not in search_terms:
                        search_terms.insert(0, t[:40])

            for i, sid in enumerate(SHORTS, 1):
                print(f"RELATED {i} {sid}…", flush=True)
                rr = {"id": f"{i:02d}", "video_id": sid, "ok": False}
                page.goto(
                    f"https://studio.youtube.com/video/{sid}/edit",
                    wait_until="domcontentloaded",
                    timeout=120000,
                )
                page.wait_for_timeout(3000)
                skip(page)
                dismiss(page)
                # already?
                body = page.locator("body").inner_text()
                chunk = (
                    body.split("Related video", 1)[-1][:180]
                    if "Related video" in body
                    else ""
                )
                if "None" not in chunk[:30] and (
                    "Fermi" in chunk or "Aliens" in chunk or "Orbit" in chunk or "Black" in chunk
                ):
                    rr["ok"] = True
                    rr["already"] = chunk
                    result["related"].append(rr)
                    continue

                page.locator("ytcp-shorts-content-links-picker").first.click(force=True)
                page.wait_for_timeout(4000)
                try:
                    page.locator("ytcp-video-pick-dialog").wait_for(timeout=15000)
                except Exception:
                    rr["error"] = "no_dialog"
                    result["related"].append(rr)
                    continue

                picked = False
                for q in search_terms[:12]:
                    page.locator("#search-yours").first.click(force=True)
                    page.keyboard.press("Meta+a")
                    page.keyboard.type(q, delay=30)
                    page.wait_for_timeout(3200)
                    dlg = page.locator("ytcp-video-pick-dialog").inner_text()
                    if "No matching results" in dlg and "Choose" in dlg:
                        # still try cells
                        pass
                    cells = page.locator(
                        "ytcp-video-pick-dialog ytcp-video-list-cell-video, "
                        "ytcp-video-pick-dialog [role=option]"
                    )
                    # Also click any visible row containing long title fragments
                    hit = page.evaluate(
                        """(needles) => {
                          const dlg=document.querySelector('ytcp-video-pick-dialog');
                          if(!dlg) return null;
                          const walk=(root, acc)=>{
                            for (const el of root.querySelectorAll('*')) {
                              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                              if (t.length<12 || t.length>250) continue;
                              if (!needles.some(n=>n && t.includes(n))) continue;
                              const r=el.getBoundingClientRect();
                              if (r.width>100 && r.height>40 && r.height<180)
                                acc.push({x:r.x+r.width/2,y:r.y+r.height/2,t:t.slice(0,160),h:r.height});
                              if (el.shadowRoot) walk(el.shadowRoot, acc);
                            }
                            return acc;
                          };
                          const acc=walk(dlg,[]);
                          acc.sort((a,b)=>a.h-b.h);
                          return acc[0]||null;
                        }""",
                        [LONG_ID, "Haven't We Found", "Fermi Paradox", "Black Hole", "Orbit's Cosmic"],
                    )
                    if hit:
                        page.mouse.click(hit["x"], hit["y"])
                        rr["picked"] = hit["t"]
                        rr["search"] = q
                        picked = True
                        break
                    if cells.count():
                        # click first non-short if possible
                        for ci in range(min(cells.count(), 8)):
                            t = cells.nth(ci).inner_text()
                            if re.search(r"\b1[0-9]:\d{2}\b|\b[2-9]:\d{2}\b", t) or LONG_ID in t or "Fermi" in t:
                                cells.nth(ci).click(force=True)
                                rr["picked"] = t[:160]
                                rr["search"] = q
                                picked = True
                                break
                    if picked:
                        break
                    rr.setdefault("tries", []).append({"q": q, "snip": dlg[:120], "cells": cells.count()})

                if not picked:
                    rr["error"] = "not_found"
                    page.keyboard.press("Escape")
                    result["related"].append(rr)
                    OUT.write_text(json.dumps(result, indent=2) + "\n")
                    continue

                page.wait_for_timeout(700)
                for name in ("Done", "Select", "Save"):
                    b = page.get_by_role("button", name=name, exact=True)
                    if b.count() and b.first.is_visible() and b.first.is_enabled():
                        b.first.click(force=True)
                        page.wait_for_timeout(800)
                        break
                rr["saved"] = save(page)
                page.goto(
                    f"https://studio.youtube.com/video/{sid}/edit",
                    wait_until="domcontentloaded",
                )
                page.wait_for_timeout(2800)
                body = page.locator("body").inner_text()
                chunk = (
                    body.split("Related video", 1)[-1][:220]
                    if "Related video" in body
                    else ""
                )
                rr["related_chunk"] = chunk
                rr["ok"] = "None" not in chunk[:40]
                page.screenshot(path=str(AUDIT / f"v05_rel_{i:02d}.png"))
                result["related"].append(rr)
                print(f"  → {rr.get('ok')} {rr.get('picked') or rr.get('error')}", flush=True)
                OUT.write_text(json.dumps(result, indent=2) + "\n")

        # PIN as Orbit channel identity
        print("PIN as Orbit…", flush=True)
        pin = {"ok": False, "via": "watch_orbit_identity"}
        page.goto(
            f"https://www.youtube.com/watch?v={LONG_ID}",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(5000)
        page.evaluate("window.scrollTo(0, 1100)")
        page.wait_for_timeout(2000)

        # Click comment placeholder then switch identity avatar
        page.evaluate(
            """() => {
              const el=document.querySelector('#simplebox-placeholder, #placeholder-area');
              if (el) el.click();
            }"""
        )
        page.wait_for_timeout(800)
        # Open author switcher
        switched = page.evaluate(
            """() => {
              // avatar button near comment box
              const box=document.querySelector('ytd-comment-simplebox-renderer, ytd-commentbox');
              if (!box) return 'no_box';
              const img=box.querySelector('#author-thumbnail button, #author-thumbnail, yt-img-shadow, button');
              if (img) { img.click(); return 'thumb'; }
              return 'no_thumb';
            }"""
        )
        pin["switch_click"] = switched
        page.wait_for_timeout(1000)
        page.screenshot(path=str(AUDIT / "v05_identity_menu.png"))
        # Choose Orbit with Ben
        chose = page.evaluate(
            """() => {
              const items=[...document.querySelectorAll(
                'ytd-account-item-renderer, tp-yt-paper-item, yt-list-item-view-model, [role=option], yt-formatted-string'
              )];
              for (const i of items) {
                const t=(i.innerText||'');
                if (/Orbit with Ben/i.test(t)) { i.click(); return t.slice(0,80); }
              }
              // also try menuitem
              return null;
            }"""
        )
        pin["chose"] = chose
        page.wait_for_timeout(1000)
        page.screenshot(path=str(AUDIT / "v05_identity_chosen.png"))

        # Type + submit
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
              const b=document.querySelector('#submit-button button, ytd-button-renderer#submit-button button');
              if (b && !b.disabled) { b.click(); return true; }
              return false;
            }"""
        )
        page.wait_for_timeout(4000)
        page.screenshot(path=str(AUDIT / "v05_posted.png"))

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

        thread = page.locator("ytd-comment-thread-renderer").filter(has_text=NEEDLE)
        pin["found"] = thread.count()
        if thread.count():
            page.evaluate(
                """(needle) => {
                  const threads=[...document.querySelectorAll('ytd-comment-thread-renderer')];
                  const t=threads.find(el => (el.innerText||'').includes(needle));
                  if (!t) return;
                  const menu=t.querySelector('#action-menu yt-icon-button, #action-menu button, ytd-menu-renderer yt-icon-button');
                  if (menu) menu.click();
                }""",
                NEEDLE,
            )
            page.wait_for_timeout(800)
            menu_items = page.evaluate(
                """() => [...document.querySelectorAll(
                  'ytd-menu-service-item-renderer, tp-yt-paper-item, [role=menuitem], yt-list-item-view-model'
                )].map(i=>(i.innerText||'').trim()).filter(Boolean).slice(0,15)"""
            )
            pin["menu_items"] = menu_items
            pinned = page.evaluate(
                """() => {
                  const items=[...document.querySelectorAll(
                    'ytd-menu-service-item-renderer, tp-yt-paper-item, [role=menuitem], yt-list-item-view-model, span, yt-formatted-string'
                  )];
                  for (const i of items) {
                    const t=(i.innerText||'').trim();
                    if (/^Pin$/i.test(t) || /^Pin comment$/i.test(t)) { i.click(); return t; }
                  }
                  return null;
                }"""
            )
            pin["pin_click"] = pinned
            page.wait_for_timeout(900)
            if pinned:
                page.evaluate(
                    """() => {
                      for (const b of document.querySelectorAll('button, yt-button-shape button')) {
                        const t=(b.innerText||'').trim();
                        if (/^Pin$/i.test(t) || /^Confirm$/i.test(t)) { b.click(); return t; }
                      }
                    }"""
                )
                page.wait_for_timeout(2000)
                pin["ok"] = True
                pin["pinned"] = True
            else:
                pin["error"] = "no_pin_option"
        else:
            pin["error"] = "comment_not_found"
            pin["body_has"] = NEEDLE in page.locator("body").inner_text()

        page.screenshot(path=str(AUDIT / "v05_pin_final.png"), full_page=True)
        result["pin"] = pin
        print("pin", pin, flush=True)

        result["ok"] = all(r.get("ok") for r in result["related"]) and bool(pin.get("ok"))
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        ctx.close()
        print("RESULT", OUT, "ok=", result["ok"])


if __name__ == "__main__":
    main()
