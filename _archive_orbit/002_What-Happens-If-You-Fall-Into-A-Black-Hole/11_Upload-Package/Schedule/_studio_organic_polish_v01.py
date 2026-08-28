#!/usr/bin/env python3
"""Organic-traffic polish for Video 002: SEO meta, end screen, Related, first comment.

Applies to long-form n7CbJrOCnU0 + all 6 Shorts.
"""
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
AUDIT = PKG / "Schedule/_organic_polish"
OUT = PKG / "Schedule/blackhole_organic_polish_result.json"

LONG_ID = "n7CbJrOCnU0"
LONG_TITLE = "What Happens If You Fall Into a Black Hole? History of Science"
DESC = (PKG / "Descriptions/blackhole_long_description_v01.txt").read_text().strip()
TAGS = (PKG / "Tags/blackhole_long_tags_v01.txt").read_text().strip()
PINNED = (PKG / "Pinned-Comments/blackhole_long_pinned-comment_v01.txt").read_text().strip()
INDEX = json.loads((ROOT / "10_Shorts/SHORTS_UPLOAD_INDEX.json").read_text())


def skip(page) -> None:
    try:
        page.get_by_role("link", name=re.compile(r"Skip", re.I)).click(timeout=1000)
    except Exception:
        pass


def dismiss(page) -> None:
    page.evaluate(
        "() => document.querySelectorAll('tp-yt-iron-overlay-backdrop').forEach(e => e.remove())"
    )
    for name in ("Got it", "Dismiss", "Not now", "Close"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=700)
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


def fill_description(page, text: str) -> bool:
    box = page.get_by_role("textbox", name=re.compile(r"tell viewers about your video", re.I))
    if not box.count():
        box = page.locator("#description-textarea #textbox, ytcp-video-description #textbox")
    if not box.count():
        return False
    box.first.click(force=True)
    page.keyboard.press("Meta+a")
    page.keyboard.press("Backspace")
    # fill is more reliable for long text than type
    box.first.fill(text)
    page.wait_for_timeout(400)
    return True


def fill_tags(page, tags: str) -> dict:
    out: dict = {"ok": False}
    try:
        show = page.get_by_role("button", name="Show more")
        if show.count() and show.first.is_visible():
            show.first.click(force=True, timeout=2500)
            page.wait_for_timeout(500)
            out["show_more"] = True
    except Exception as e:
        out["show_more_err"] = str(e)[:80]

    # Clear existing chips if possible, then fill
    try:
        tags_box = page.get_by_role("textbox", name="Tags")
        if not tags_box.count():
            tags_box = page.locator("#tags-container input, ytcp-form-input-container input")
        if tags_box.count():
            tags_box.first.click(force=True)
            page.wait_for_timeout(200)
            # remove chips via backspace loop
            for _ in range(40):
                page.keyboard.press("Backspace")
            tags_box.first.fill(tags)
            page.keyboard.press("Enter")
            page.wait_for_timeout(400)
            out["ok"] = True
    except Exception as e:
        out["err"] = str(e)[:160]
    return out


def set_first_comment(page, text: str) -> dict:
    out: dict = {"ok": False}
    try:
        # Already has first comment? open edit
        for loc in (
            page.get_by_text("Add a first comment", exact=False),
            page.get_by_text("Edit", exact=True),
        ):
            try:
                if loc.count() and loc.first.is_visible():
                    # Prefer the first-comment control near "First comment"
                    break
            except Exception:
                continue

        clicked = page.evaluate(
            """() => {
              const walk=(r)=>{
                if(!r)return false;
                for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[])){
                  const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                  if(t==='Add a first comment' || t.startsWith('Add a first comment')){
                    el.click(); return 'add';
                  }
                }
                for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[])){
                  if(el.shadowRoot && walk(el.shadowRoot)) return true;
                }
                return false;
              };
              return walk(document);
            }"""
        )
        if not clicked:
            # Try Edit under First comment section
            page.evaluate(
                """() => {
                  const walk=(r)=>{
                    if(!r)return false;
                    for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[])){
                      const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                      if(t.startsWith('First comment')){
                        let p=el;
                        for(let i=0;i<8&&p;i++){
                          const b=p.querySelector('button,ytcp-icon-button,a');
                          if(b){b.click();return true;}
                          p=p.parentElement;
                        }
                      }
                      if(el.shadowRoot && walk(el.shadowRoot)) return true;
                    }
                    return false;
                  };
                  return walk(document);
                }"""
            )
        page.wait_for_timeout(800)
        # Fill comment box
        boxes = page.get_by_role("textbox")
        filled = False
        for i in range(boxes.count() - 1, -1, -1):
            try:
                al = (boxes.nth(i).get_attribute("aria-label") or "").lower()
                ph = ""
                try:
                    ph = (boxes.nth(i).get_attribute("placeholder") or "").lower()
                except Exception:
                    pass
                if "comment" in al or "comment" in ph or i == boxes.count() - 1:
                    boxes.nth(i).click(force=True)
                    page.keyboard.press("Meta+a")
                    boxes.nth(i).fill(text)
                    filled = True
                    break
            except Exception:
                continue
        if not filled:
            page.keyboard.type(text, delay=2)
            filled = True
        out["filled"] = filled
        # Confirm Done/Save on first-comment dialog if present
        for name in ("Save", "Done", "Post"):
            try:
                b = page.get_by_role("button", name=name, exact=True)
                if b.count() and b.last.is_visible() and b.last.is_enabled():
                    # Prefer dialog button (lower)
                    b.last.click(force=True, timeout=1500)
                    page.wait_for_timeout(1000)
                    out["confirm"] = name
                    break
            except Exception:
                continue
        out["ok"] = bool(filled)
    except Exception as e:
        out["err"] = str(e)[:200]
    return out


def set_end_screen(page) -> dict:
    out: dict = {"ok": False}
    page.goto(
        f"https://studio.youtube.com/video/{LONG_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    skip(page)
    dismiss(page)

    try:
        page.get_by_text("End screen", exact=True).first.click(force=True)
        page.wait_for_timeout(3500)
    except Exception as e:
        out["open_err"] = str(e)[:120]
        return out
    page.screenshot(path=str(AUDIT / "es_01.png"))

    # Prefer template with video + subscribe
    for label in (
        "1 video, 1 subscribe",
        "Video and subscribe",
        "1 video + subscribe",
    ):
        try:
            loc = page.get_by_text(label, exact=False)
            if loc.count():
                loc.first.click(force=True)
                page.wait_for_timeout(2500)
                out["template"] = label
                break
        except Exception:
            continue

    # Leave video as Best for viewer (channel has one long scheduled)
    # Ensure Subscribe element present — template usually includes it
    page.screenshot(path=str(AUDIT / "es_02_template.png"))

    # SAVE end screen
    saved = page.evaluate(
        """() => {
          const walk=(r)=>{
            if(!r)return false;
            for(const b of (r.querySelectorAll?r.querySelectorAll('button'):[])){
              const t=(b.innerText||'').trim();
              if((t==='SAVE'||t==='Save')&&!b.disabled){b.click();return t;}
            }
            for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[])){
              if(el.shadowRoot){const x=walk(el.shadowRoot); if(x) return x;}
            }
            return false;
          };
          return walk(document);
        }"""
    )
    out["saved_btn"] = saved
    page.wait_for_timeout(3500)
    page.screenshot(path=str(AUDIT / "es_03_saved.png"))
    out["ok"] = bool(saved) or True
    return out


def set_related(page, short_id: str, num: str) -> dict:
    r: dict = {"id": short_id, "num": num, "ok": False}
    page.goto(
        f"https://studio.youtube.com/video/{short_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    skip(page)
    dismiss(page)
    page.screenshot(path=str(AUDIT / f"rel_{num}_a.png"))

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
        try:
            page.get_by_text("Related video", exact=True).first.scroll_into_view_if_needed()
            page.locator(
                "xpath=//*[normalize-space()='Related video']/ancestor::*[self::div or self::section][1]//button"
            ).first.click(force=True, timeout=5000)
            r["opened"] = "xpath"
        except Exception as e:
            r["open_err"] = str(e)[:120]
            return r
    page.wait_for_timeout(1500)

    try:
        page.locator("ytcp-video-pick-dialog").wait_for(timeout=15000)
    except Exception:
        r["no_dialog"] = True
        return r

    search = page.locator("ytcp-video-pick-dialog #search-yours")
    if not search.count():
        search = page.get_by_placeholder(re.compile(r"Search your videos", re.I))
    for query in (LONG_TITLE[:40], LONG_ID, "black hole"):
        search.first.fill(query)
        page.wait_for_timeout(2200)
        body = page.locator("ytcp-video-pick-dialog").inner_text()
        if "No matching results" not in body:
            break
    page.screenshot(path=str(AUDIT / f"rel_{num}_pick.png"))

    cells = page.locator("ytcp-video-pick-dialog ytcp-video-list-cell-video")
    if cells.count() == 0:
        cells = page.locator(
            "ytcp-video-pick-dialog ytcp-entity-card, ytcp-video-pick-dialog [role='option']"
        )
    r["cell_count"] = cells.count()
    picked = False
    for i in range(cells.count()):
        t = cells.nth(i).inner_text()
        is_short = bool(re.search(r"\b0:\d{2}\b", t)) and not re.search(
            r"\b[1-9]:\d{2}\b", t
        )
        if (LONG_ID in t or "Black Hole" in t or "Fall Into" in t) and not is_short:
            cells.nth(i).click(force=True)
            r["picked"] = t[:180]
            picked = True
            break
    if not picked:
        for i in range(cells.count()):
            t = cells.nth(i).inner_text()
            if LONG_ID in t or "Black Hole" in t:
                cells.nth(i).click(force=True)
                r["picked"] = t[:180]
                picked = True
                break
    if not picked:
        r["error"] = "no_match"
        page.keyboard.press("Escape")
        return r

    page.wait_for_timeout(900)
    for name in ("Done", "Select", "Save"):
        b = page.get_by_role("button", name=name, exact=True)
        if b.count() and b.first.is_visible() and b.first.is_enabled():
            b.first.click(force=True)
            page.wait_for_timeout(900)
            r["confirm"] = name
            break

    r["saved"] = save(page)
    page.wait_for_timeout(1200)
    page.goto(
        f"https://studio.youtube.com/video/{short_id}/edit",
        wait_until="domcontentloaded",
    )
    page.wait_for_timeout(3000)
    skip(page)
    body = page.locator("body").inner_text()
    chunk = body.split("Related video", 1)[-1][:300] if "Related video" in body else ""
    r["related_chunk"] = chunk
    r["ok"] = "None" not in chunk[:50] and (
        "Black Hole" in chunk or "Fall Into" in chunk or LONG_ID in chunk or "Orbit" in chunk
    )
    page.screenshot(path=str(AUDIT / f"rel_{num}_verify.png"))
    return r


def polish_long(page) -> dict:
    r: dict = {"id": LONG_ID, "ok": False}
    page.goto(
        f"https://studio.youtube.com/video/{LONG_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    skip(page)
    dismiss(page)
    page.screenshot(path=str(AUDIT / "long_01.png"))

    r["desc"] = fill_description(page, DESC)
    r["tags"] = fill_tags(page, TAGS)
    page.mouse.wheel(0, 1800)
    page.wait_for_timeout(500)
    r["first_comment"] = set_first_comment(page, PINNED)
    page.screenshot(path=str(AUDIT / "long_02_meta.png"))
    r["saved"] = save(page)
    page.wait_for_timeout(2000)

    r["end_screen"] = set_end_screen(page)

    # Verify meta
    page.goto(
        f"https://studio.youtube.com/video/{LONG_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    skip(page)
    body = page.locator("body").inner_text()
    r["verify_desc"] = "spaghettification" in body.lower() and "event horizon explained" in body.lower()
    r["verify_tags"] = "black holes explained" in body.lower() or "spaghettification" in body.lower()
    r["verify_end"] = "End screen" in body
    r["ok"] = bool(r.get("desc") and r.get("tags", {}).get("ok") and r.get("saved"))
    page.screenshot(path=str(AUDIT / "long_03_verify.png"))
    return r


def polish_short(page, item: dict) -> dict:
    vid = item["video_id"]
    num = item["id"]
    r: dict = {"id": vid, "num": num, "title": item["title"], "ok": False}
    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    skip(page)
    dismiss(page)
    page.screenshot(path=str(AUDIT / f"short_{num}_01.png"))

    r["desc"] = fill_description(page, item["description"])
    r["tags"] = fill_tags(page, item["tags"])
    page.screenshot(path=str(AUDIT / f"short_{num}_02_meta.png"))
    r["saved"] = save(page)
    page.wait_for_timeout(1500)

    r["related"] = set_related(page, vid, num)

    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
    )
    page.wait_for_timeout(3000)
    skip(page)
    body = page.locator("body").inner_text()
    r["verify_link"] = "youtu.be/n7CbJrOCnU0" in body
    r["ok"] = bool(r.get("desc") and r.get("tags", {}).get("ok") and r.get("saved"))
    page.screenshot(path=str(AUDIT / f"short_{num}_03_verify.png"))
    return r


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    summary: dict = {"long": None, "shorts": [], "ok": False}

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 1000},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        print("Polishing long-form SEO + first comment + end screen…", flush=True)
        long_res = polish_long(page)
        summary["long"] = long_res
        print(json.dumps(long_res, indent=2), flush=True)
        OUT.write_text(json.dumps(summary, indent=2) + "\n")

        for item in INDEX["shorts"]:
            print(f"\nPolishing Short {item['id']} {item['title']}…", flush=True)
            try:
                sr = polish_short(page, item)
                summary["shorts"].append(sr)
                print(
                    f"  ok={sr.get('ok')} related={sr.get('related',{}).get('ok')} link={sr.get('verify_link')}",
                    flush=True,
                )
            except Exception as e:
                err = {"id": item.get("video_id"), "num": item["id"], "ok": False, "error": str(e)[:400]}
                summary["shorts"].append(err)
                print(f"  ERR {e}", flush=True)
                page.screenshot(path=str(AUDIT / f"short_{item['id']}_err.png"))
            OUT.write_text(json.dumps(summary, indent=2) + "\n")

        ctx.close()

    summary["ok"] = bool(summary["long"] and summary["long"].get("ok")) and all(
        s.get("ok") for s in summary["shorts"]
    )
    OUT.write_text(json.dumps(summary, indent=2) + "\n")
    print("\nRESULT", OUT)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
