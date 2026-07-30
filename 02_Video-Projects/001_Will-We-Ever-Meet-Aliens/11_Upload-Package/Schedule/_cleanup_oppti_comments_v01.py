#!/usr/bin/env python3
"""Delete @OpptiAI / @opptiai comments from V001 long; post CTA as Orbit with Ben."""
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
OUT = PKG / "Schedule/aliens_cleanup_oppti_comments_v01.json"
LONG_ID = "Mo93x0fxB1Q"
ORBIT = "UC_esArsDKd3GJvOkeO0DUog"
PINNED = (PKG / "Pinned-Comments/aliens_long_pinned-comment_v01.txt").read_text().strip()
NEEDLE = "best explains the silence"


def skip(page):
    try:
        page.get_by_role("link", name=re.compile(r"Skip", re.I)).click(timeout=800)
    except Exception:
        pass


def dismiss(page):
    page.keyboard.press("Escape")
    for name in ("Got it", "Dismiss", "Close", "Not now"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=400)
        except Exception:
            pass


def main():
    AUDIT.mkdir(parents=True, exist_ok=True)
    result: dict = {"deleted": [], "posted": None, "ok": False}

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 1100},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        # Studio comments for Orbit long
        page.goto(
            f"https://studio.youtube.com/channel/{ORBIT}/video/{LONG_ID}/comments",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(4500)
        skip(page)
        dismiss(page)
        # fallback URL
        if "comments" not in page.url:
            page.goto(
                f"https://studio.youtube.com/video/{LONG_ID}/comments",
                wait_until="domcontentloaded",
            )
            page.wait_for_timeout(4000)
            skip(page)

        page.screenshot(path=str(AUDIT / "cleanup_comments_before.png"), full_page=True)

        # Delete every comment that looks like OpptiAI / needle CTA from wrong author
        for round_i in range(12):
            comments = page.locator("ytcp-comment")
            n = comments.count()
            result.setdefault("rounds", []).append({"round": round_i, "count": n})
            if n == 0:
                break
            target = None
            for i in range(n):
                t = comments.nth(i).inner_text()
                author_bad = bool(
                    re.search(r"@?opptiai|@?OpptiAI", t, re.I)
                )
                has_cta = NEEDLE in t or "Orbit's next film" in t or "Orbit pinned CTA" in t
                if author_bad or (has_cta and "@Orbit" not in t.split("\n")[0]):
                    # Prefer deleting oppti authors always; also delete CTA if not Orbit
                    if author_bad or has_cta:
                        target = i
                        result["deleted"].append(t[:160])
                        break
            if target is None:
                # also delete duplicates of CTA even if Orbit authored (keep none until we repost one)
                for i in range(n):
                    t = comments.nth(i).inner_text()
                    if NEEDLE in t:
                        target = i
                        result["deleted"].append("cta:" + t[:120])
                        break
            if target is None:
                break

            c = comments.nth(target)
            c.scroll_into_view_if_needed()
            c.hover()
            page.wait_for_timeout(400)
            # Open action menu
            opened = False
            for sel in (
                "ytcp-icon-button[aria-label*='Action']",
                "button[aria-label*='Action']",
                "ytcp-icon-button[aria-label*='More']",
                "button[aria-label*='More']",
            ):
                loc = c.locator(sel)
                if loc.count():
                    loc.first.click(force=True)
                    opened = True
                    break
            if not opened:
                # rightmost icon in comment
                page.evaluate(
                    """(idx) => {
                      const cs=[...document.querySelectorAll('ytcp-comment')];
                      const c=cs[idx]; if(!c) return;
                      const btns=[...c.querySelectorAll('ytcp-icon-button, button')];
                      const cands=btns.map(b=>{
                        const r=b.getBoundingClientRect();
                        return {b,x:r.x,w:r.width};
                      }).filter(x=>x.w>8 && x.w<60);
                      cands.sort((a,b)=>b.x-a.x);
                      if (cands[0]) cands[0].b.click();
                    }""",
                    target,
                )
            page.wait_for_timeout(700)
            page.screenshot(path=str(AUDIT / f"cleanup_menu_{round_i}.png"))

            # Click Delete
            clicked = page.evaluate(
                """() => {
                  for (const n of document.querySelectorAll(
                    'tp-yt-paper-item, [role=menuitem], ytcp-text-menu-item, span, yt-formatted-string'
                  )) {
                    const t=(n.innerText||'').trim();
                    if (/^Delete$/i.test(t)) { n.click(); return t; }
                  }
                  return null;
                }"""
            )
            page.wait_for_timeout(800)
            # Confirm
            page.evaluate(
                """() => {
                  for (const b of document.querySelectorAll('button, ytcp-button, yt-button-shape button')) {
                    const t=(b.innerText||'').trim();
                    if (/^Delete$/i.test(t) || /^Confirm$/i.test(t) || /^OK$/i.test(t)) {
                      b.click(); return t;
                    }
                  }
                }"""
            )
            page.wait_for_timeout(2000)
            result.setdefault("delete_clicks", []).append(clicked)
            # refresh list
            page.reload(wait_until="domcontentloaded")
            page.wait_for_timeout(3500)
            skip(page)

        page.screenshot(path=str(AUDIT / "cleanup_comments_after_delete.png"), full_page=True)
        result["remaining"] = page.locator("ytcp-comment").count()

        # Post ONE comment as Orbit with Ben via Studio Add a comment
        # Switch composer identity if possible
        page.evaluate(
            """() => {
              const add=[...document.querySelectorAll('*')].find(e =>
                (e.innerText||'').trim()==='Add a comment...' ||
                (e.getAttribute('placeholder')||'').includes('Add a comment')
              );
              if (!add) return;
              const box=add.getBoundingClientRect();
              for (const el of document.querySelectorAll('img, button, yt-img-shadow')) {
                const r=el.getBoundingClientRect();
                if (Math.abs(r.y-box.y)<50 && r.x < box.x && r.width>20 && r.width<70) {
                  el.click(); return;
                }
              }
            }"""
        )
        page.wait_for_timeout(900)
        page.evaluate(
            """() => {
              for (const n of document.querySelectorAll(
                'tp-yt-paper-item, [role=menuitem], yt-formatted-string, ytcp-ve'
              )) {
                const t=n.innerText||'';
                if (/Orbit with Ben/i.test(t)) { n.click(); return t; }
              }
            }"""
        )
        page.wait_for_timeout(800)

        posted = {"ok": False}
        try:
            box = page.get_by_placeholder(re.compile(r"Add a comment", re.I))
            if box.count() == 0:
                page.get_by_text("Add a comment", exact=False).first.click(force=True)
                page.wait_for_timeout(400)
                box = page.get_by_role("textbox")
            box.first.click(force=True)
            page.keyboard.press("Meta+a")
            page.keyboard.press("Backspace")
            page.keyboard.type(PINNED, delay=4)
            page.wait_for_timeout(500)
            for name in ("Comment", "Reply", "Post"):
                b = page.get_by_role("button", name=name, exact=True)
                if b.count() and b.first.is_enabled():
                    b.first.click(force=True)
                    page.wait_for_timeout(3000)
                    posted["ok"] = True
                    posted["via"] = name
                    break
        except Exception as e:
            posted["error"] = str(e)[:250]

        page.screenshot(path=str(AUDIT / "cleanup_posted.png"), full_page=True)
        result["posted"] = posted

        # Verify authors on page
        page.reload(wait_until="domcontentloaded")
        page.wait_for_timeout(3500)
        body = page.locator("body").inner_text()
        result["has_oppti"] = bool(re.search(r"opptiai|OpptiAI", body, re.I))
        result["has_needle"] = NEEDLE in body
        result["comment_count"] = page.locator("ytcp-comment").count()
        # sample authors
        result["authors"] = page.evaluate(
            """() => [...document.querySelectorAll('ytcp-comment')].slice(0,8).map(c => {
              const t=(c.innerText||'').split('\\n').slice(0,3).join(' | ');
              return t.slice(0,120);
            })"""
        )
        page.screenshot(path=str(AUDIT / "cleanup_final.png"), full_page=True)

        # Try pin on the new comment if menu has it
        if result["has_needle"] and not result["has_oppti"]:
            try:
                c = page.locator("ytcp-comment").filter(has_text=NEEDLE).first
                c.hover()
                page.wait_for_timeout(300)
                ab = c.locator(
                    "ytcp-icon-button[aria-label*='Action'], button[aria-label*='Action']"
                )
                if ab.count():
                    ab.first.click(force=True)
                    page.wait_for_timeout(700)
                    items = page.evaluate(
                        """() => [...document.querySelectorAll(
                          'tp-yt-paper-item, [role=menuitem]'
                        )].map(i=>(i.innerText||'').trim()).filter(Boolean)"""
                    )
                    result["pin_menu"] = items
                    if any(re.search(r"Pin", x, re.I) for x in items):
                        page.get_by_text(re.compile(r"Pin", re.I)).first.click(force=True)
                        page.wait_for_timeout(800)
                        try:
                            page.get_by_role(
                                "button", name=re.compile(r"^Pin$", re.I)
                            ).last.click(force=True)
                        except Exception:
                            pass
                        result["pinned"] = True
            except Exception as e:
                result["pin_err"] = str(e)[:200]

        result["ok"] = (not result["has_oppti"]) and bool(posted.get("ok") or result["has_needle"])
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2)[:2500], flush=True)
        ctx.close()
        raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
