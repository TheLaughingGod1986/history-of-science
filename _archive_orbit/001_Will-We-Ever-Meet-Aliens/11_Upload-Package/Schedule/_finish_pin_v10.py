#!/usr/bin/env python3
"""Pin-only attempt: Studio Add-a-comment as Orbit + verify Related still set."""
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
OUT = PKG / "Schedule/aliens_pin_v10.json"
LONG_ID = "Mo93x0fxB1Q"
PINNED = (PKG / "Pinned-Comments/aliens_long_pinned-comment_v01.txt").read_text().strip()
SHORTS = ["z-DLqoSoEBo", "UWwNKYf_aU8", "MO19iXYCu0c", "--CxhjNqtSY"]
NEEDLE = "best explains the silence"


def skip(page):
    try:
        page.get_by_role("link", name=re.compile(r"Skip", re.I)).click(timeout=800)
    except Exception:
        pass


def main():
    AUDIT.mkdir(parents=True, exist_ok=True)
    result: dict = {"related_verify": [], "pin": None}

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 1100},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        # Verify related still set
        for sid in SHORTS:
            page.goto(
                f"https://studio.youtube.com/video/{sid}/edit",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(2800)
            skip(page)
            body = page.locator("body").inner_text()
            chunk = (
                body.split("Related video", 1)[-1][:120]
                if "Related video" in body
                else ""
            )
            ok = "None" not in chunk[:40] and "Haven't" in chunk
            result["related_verify"].append({"id": sid, "ok": ok, "chunk": chunk})
            print(f"related {sid} ok={ok}", flush=True)

        # Studio comments — add as Orbit if possible
        page.goto(
            f"https://studio.youtube.com/video/{LONG_ID}/comments",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(4000)
        skip(page)
        page.screenshot(path=str(AUDIT / "v10_comments.png"), full_page=True)

        pin: dict = {"ok": False}
        # Click avatar next to Add a comment to switch to Orbit
        switched = page.evaluate(
            """() => {
              // comment composer avatar
              const composers=[...document.querySelectorAll(
                'ytcp-comment-box, ytcp-video-comments, ytcp-comments'
              )];
              const root=document.querySelector('ytcp-comment-box') || document.body;
              const imgs=[...root.querySelectorAll('img, yt-img-shadow, button')];
              // click first small circular near 'Add a comment'
              const add=[...document.querySelectorAll('*')].find(e =>
                (e.innerText||'').trim()==='Add a comment...' ||
                (e.getAttribute('placeholder')||'').includes('Add a comment')
              );
              if (add) {
                const box=add.getBoundingClientRect();
                for (const el of document.querySelectorAll('img, button, yt-img-shadow')) {
                  const r=el.getBoundingClientRect();
                  if (Math.abs(r.y-box.y)<40 && r.x < box.x && r.width>20 && r.width<60) {
                    el.click(); return 'near_add';
                  }
                }
              }
              return 'no';
            }"""
        )
        pin["avatar_click"] = switched
        page.wait_for_timeout(1000)
        page.screenshot(path=str(AUDIT / "v10_avatar_menu.png"))
        chose = page.evaluate(
            """() => {
              for (const n of document.querySelectorAll(
                'tp-yt-paper-item, ytcp-ve, [role=menuitem], yt-formatted-string'
              )) {
                const t=n.innerText||'';
                if (/History of Science/i.test(t)) { n.click(); return t.slice(0,60); }
              }
              return null;
            }"""
        )
        pin["chose"] = chose
        page.wait_for_timeout(1000)

        # Type in Add a comment
        try:
            box = page.get_by_placeholder(re.compile(r"Add a comment", re.I))
            if box.count() == 0:
                page.get_by_text("Add a comment", exact=False).first.click(force=True)
                page.wait_for_timeout(500)
                box = page.get_by_role("textbox")
            box.first.click(force=True)
            page.keyboard.type(PINNED, delay=3)
            page.wait_for_timeout(500)
            for name in ("Comment", "Reply", "Post"):
                b = page.get_by_role("button", name=name, exact=True)
                if b.count() and b.first.is_enabled():
                    b.first.click(force=True)
                    pin["posted_studio"] = name
                    page.wait_for_timeout(3000)
                    break
        except Exception as e:
            pin["post_err"] = str(e)[:200]

        page.screenshot(path=str(AUDIT / "v10_after_post.png"), full_page=True)

        # Open menus on comments and dump ALL menu item texts looking for Pin
        page.reload(wait_until="domcontentloaded")
        page.wait_for_timeout(4000)
        skip(page)

        menus_found = []
        comments = page.locator("ytcp-comment")
        for i in range(min(comments.count(), 5)):
            c = comments.nth(i)
            try:
                c.hover()
                page.wait_for_timeout(300)
                # click action button
                ab = c.locator(
                    "ytcp-icon-button[aria-label*='Action'], "
                    "button[aria-label*='Action'], "
                    "ytcp-icon-button[aria-label*='More']"
                )
                if ab.count():
                    ab.first.click(force=True)
                    page.wait_for_timeout(600)
                    items = page.evaluate(
                        """() => [...document.querySelectorAll(
                          'tp-yt-paper-item, [role=menuitem], ytcp-text-menu-item'
                        )].map(i=>(i.innerText||'').trim()).filter(Boolean)"""
                    )
                    menus_found.append({"i": i, "items": items})
                    page.screenshot(path=str(AUDIT / f"v10_menu_{i}.png"))
                    if any(re.search(r"Pin", x, re.I) for x in items):
                        page.get_by_text(re.compile(r"Pin", re.I)).first.click(force=True)
                        page.wait_for_timeout(800)
                        try:
                            page.get_by_role(
                                "button", name=re.compile(r"^Pin$", re.I)
                            ).last.click(force=True)
                        except Exception:
                            pass
                        pin["ok"] = True
                        pin["pinned_from"] = i
                        break
                    page.keyboard.press("Escape")
                    page.wait_for_timeout(300)
            except Exception as e:
                menus_found.append({"i": i, "err": str(e)[:120]})

        pin["menus"] = menus_found

        # Final watch check for Pinned by
        page.goto(
            f"https://www.youtube.com/watch?v={LONG_ID}",
            wait_until="domcontentloaded",
        )
        page.wait_for_timeout(4000)
        page.evaluate("window.scrollTo(0, 1100)")
        page.wait_for_timeout(1500)
        body = page.locator("body").inner_text()
        pin["watch_pinned"] = "Pinned by" in body
        if pin["watch_pinned"]:
            pin["ok"] = True
        page.screenshot(path=str(AUDIT / "v10_watch.png"), full_page=True)

        result["pin"] = pin
        result["related_all_ok"] = all(x["ok"] for x in result["related_verify"])
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2)[:2500], flush=True)
        ctx.close()


if __name__ == "__main__":
    main()
