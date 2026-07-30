#!/usr/bin/env python3
"""Save long-form description + tags (under 500) + first comment. Force Save."""
from __future__ import annotations

import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = "/Users/ben/code/youtube/.playwright-youtube-profile"
ROOT = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "002_What-Happens-If-You-Fall-Into-A-Black-Hole"
)
PKG = ROOT / "11_Upload-Package"
AUDIT = PKG / "Schedule/_long_save"
OUT = PKG / "Schedule/blackhole_long_meta_save_result.json"
LONG_ID = "n7CbJrOCnU0"
DESC = (PKG / "Descriptions/blackhole_long_description_v01.txt").read_text().strip()
TAGS = (PKG / "Tags/blackhole_long_tags_v01.txt").read_text().strip()
PINNED = (PKG / "Pinned-Comments/blackhole_long_pinned-comment_v01.txt").read_text().strip()


def skip(page) -> None:
    try:
        page.get_by_role("link", name=re.compile(r"Skip", re.I)).click(timeout=1000)
    except Exception:
        pass


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    r: dict = {"id": LONG_ID, "ok": False, "tag_file_chars": len(TAGS)}

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
            f"https://studio.youtube.com/video/{LONG_ID}/edit",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(4000)
        skip(page)

        # Description
        box = page.get_by_role(
            "textbox", name=re.compile(r"tell viewers about your video", re.I)
        )
        box.first.click(force=True)
        page.keyboard.press("Meta+a")
        page.keyboard.press("Backspace")
        box.first.fill(DESC)
        page.wait_for_timeout(500)
        r["desc_filled"] = True
        page.screenshot(path=str(AUDIT / "01_desc.png"))

        # Tags — expand Show more, then find input via probe
        for _ in range(6):
            page.mouse.wheel(0, 900)
            page.wait_for_timeout(250)
        try:
            page.get_by_text("Show more", exact=True).first.click(force=True, timeout=3000)
            page.wait_for_timeout(900)
            r["show_more"] = True
        except Exception:
            try:
                page.get_by_role("button", name=re.compile(r"Show more", re.I)).first.click(
                    force=True, timeout=3000
                )
                page.wait_for_timeout(900)
                r["show_more"] = "role"
            except Exception as e:
                r["show_more_err"] = str(e)[:80]

        page.mouse.wheel(0, 800)
        page.wait_for_timeout(400)

        probe = page.evaluate(
            """() => {
              const hits=[];
              const walk=(root)=>{
                if(!root)return;
                for(const el of (root.querySelectorAll?root.querySelectorAll('input'):[])){
                  const al=(el.getAttribute('aria-label')||'');
                  const ph=(el.getAttribute('placeholder')||'');
                  if(/tag/i.test(al+' '+ph)){
                    const r=el.getBoundingClientRect();
                    if(r.width>20) hits.push({al,ph,x:r.x+r.width/2,y:r.y+r.height/2});
                  }
                }
                for(const el of (root.querySelectorAll?root.querySelectorAll('*'):[])){
                  if(el.shadowRoot) walk(el.shadowRoot);
                }
              };
              walk(document);
              return hits;
            }"""
        )
        r["probe"] = probe[:4]
        if probe:
            # Scroll element into view via click coords — if y large, wheel first
            while probe[0]["y"] > 900:
                page.mouse.wheel(0, 500)
                page.wait_for_timeout(200)
                probe = page.evaluate(
                    """() => {
                      const hits=[];
                      const walk=(root)=>{
                        if(!root)return;
                        for(const el of (root.querySelectorAll?root.querySelectorAll('input'):[])){
                          const al=(el.getAttribute('aria-label')||'');
                          const ph=(el.getAttribute('placeholder')||'');
                          if(/tag/i.test(al+' '+ph)){
                            const r=el.getBoundingClientRect();
                            if(r.width>20) hits.push({al,ph,x:r.x+r.width/2,y:r.y+r.height/2});
                          }
                        }
                        for(const el of (root.querySelectorAll?root.querySelectorAll('*'):[])){
                          if(el.shadowRoot) walk(el.shadowRoot);
                        }
                      };
                      walk(document);
                      return hits;
                    }"""
                )
                if not probe:
                    break
            page.mouse.click(probe[0]["x"], probe[0]["y"])
            page.wait_for_timeout(300)
            for _ in range(100):
                page.keyboard.press("Backspace")
            page.wait_for_timeout(300)
            for tag in [t.strip() for t in TAGS.split(",") if t.strip()]:
                page.keyboard.type(tag, delay=5)
                page.keyboard.press("Enter")
                page.wait_for_timeout(50)
            r["tags_via"] = "probe"
        else:
            r["tags_via"] = "none"

        page.wait_for_timeout(500)
        body = page.locator("body").inner_text()
        m = re.search(r"(\d{2,3})\s*/\s*500", body)
        r["counter"] = m.group(0) if m else None
        page.screenshot(path=str(AUDIT / "02_tags.png"))

        if m and int(m.group(1)) > 500:
            r["over"] = int(m.group(1)) - 500
            for _ in range(8):
                page.keyboard.press("Backspace")
                page.wait_for_timeout(80)
            body = page.locator("body").inner_text()
            m2 = re.search(r"(\d{2,3})\s*/\s*500", body)
            r["counter_after_trim"] = m2.group(0) if m2 else None

        # First comment — scroll further
        page.mouse.wheel(0, 1500)
        page.wait_for_timeout(400)
        try:
            add = page.get_by_text("Add a first comment", exact=False)
            if add.count() and add.first.is_visible():
                add.first.click(force=True)
                page.wait_for_timeout(1000)
                # Find dialog textbox
                dlg = page.locator("[role=dialog], tp-yt-paper-dialog")
                tb = dlg.get_by_role("textbox") if dlg.count() else page.get_by_role("textbox")
                # Prefer last textbox in dialog
                target = tb.last if tb.count() else None
                if target:
                    target.click(force=True)
                    page.keyboard.press("Meta+a")
                    target.fill(PINNED)
                    r["comment_filled"] = True
                    for name in ("Comment", "Save", "Done"):
                        b = dlg.get_by_role("button", name=name, exact=True) if dlg.count() else page.get_by_role("button", name=name, exact=True)
                        if b.count() and b.last.is_enabled():
                            b.last.click(force=True)
                            page.wait_for_timeout(1200)
                            r["comment_confirm"] = name
                            break
            else:
                r["comment"] = "already_set_or_missing_add"
        except Exception as e:
            r["comment_err"] = str(e)[:160]

        page.screenshot(path=str(AUDIT / "03_pre_save.png"))

        # Save
        save = page.get_by_role("button", name="Save", exact=True)
        r["save_enabled"] = bool(save.count() and save.first.is_enabled())
        if r["save_enabled"]:
            save.first.click(force=True)
            page.wait_for_timeout(3500)
            r["saved"] = True
        else:
            # Try clicking anyway / check for exceed message
            r["save_blocked"] = "exceed" in page.locator("body").inner_text().lower()
            page.screenshot(path=str(AUDIT / "03b_save_blocked.png"))

        # Verify
        page.goto(
            f"https://studio.youtube.com/video/{LONG_ID}/edit",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(4000)
        skip(page)
        body = page.locator("body").inner_text()
        r["verify_desc"] = "Hawking radiation" in body and "0:00 — Orbit's question" in body
        try:
            page.get_by_role("button", name="Show more").first.click(force=True)
            page.wait_for_timeout(600)
        except Exception:
            pass
        page.mouse.wheel(0, 2600)
        page.wait_for_timeout(400)
        body2 = page.locator("body").inner_text()
        r["verify_tag"] = "black holes explained" in body2.lower() and "spaghettification" in body2.lower()
        m3 = re.search(r"(\d{2,3})\s*/\s*500", body2)
        r["verify_counter"] = m3.group(0) if m3 else None
        r["ok"] = bool(r.get("saved") and r.get("verify_desc") and r.get("verify_tag"))
        page.screenshot(path=str(AUDIT / "04_verify.png"), full_page=True)

        OUT.write_text(json.dumps(r, indent=2) + "\n")
        print(json.dumps(r, indent=2))
        ctx.close()
        raise SystemExit(0 if r["ok"] else 1)


if __name__ == "__main__":
    main()
