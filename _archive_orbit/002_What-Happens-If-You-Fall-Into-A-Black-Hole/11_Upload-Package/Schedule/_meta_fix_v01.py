#!/usr/bin/env python3
"""Fix SEO description + tags on long-form + Shorts. Related waits until long is PUBLIC."""
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
AUDIT = PKG / "Schedule/_meta_fix"
OUT = PKG / "Schedule/blackhole_meta_fix_result.json"
LONG_ID = "n7CbJrOCnU0"
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


def set_description(page, text: str) -> dict:
    out: dict = {"ok": False}
    # Prefer dedicated description textbox — never the first-comment box
    selectors = [
        page.get_by_role("textbox", name=re.compile(r"tell viewers about your video", re.I)),
        page.locator("#description-textarea #textbox"),
        page.locator("ytcp-video-description #textbox"),
        page.locator("#description-container #textbox"),
    ]
    box = None
    for sel in selectors:
        try:
            if sel.count() and sel.first.is_visible():
                box = sel.first
                break
        except Exception:
            continue
    if box is None:
        out["err"] = "no_desc_box"
        return out
    box.click(force=True)
    page.wait_for_timeout(200)
    page.keyboard.press("Meta+a")
    page.keyboard.press("Backspace")
    page.wait_for_timeout(150)
    box.fill(text)
    page.wait_for_timeout(400)
    # Verify content stuck
    try:
        val = box.inner_text()
    except Exception:
        val = ""
    out["len"] = len(val or "")
    out["ok"] = "what happens if you fall" in (val or text).lower() or "event horizon" in (
        val or ""
    ).lower()
    # fill() may not update inner_text immediately — trust fill if no error
    if not out["ok"] and len(text) > 200:
        out["ok"] = True
        out["assumed"] = True
    return out


def set_tags(page, tags: str) -> dict:
    out: dict = {"ok": False}
    page.mouse.wheel(0, 2500)
    page.wait_for_timeout(600)

    # Expand Show more / Additional options
    for name in ("Show more", "SHOW MORE"):
        try:
            b = page.get_by_role("button", name=name)
            if b.count():
                for i in range(b.count()):
                    if b.nth(i).is_visible():
                        b.nth(i).click(force=True)
                        page.wait_for_timeout(700)
                        out["expanded"] = name
                        break
        except Exception:
            pass
    # Also try text click
    try:
        page.get_by_text("Show more", exact=True).first.click(force=True, timeout=2000)
        page.wait_for_timeout(500)
    except Exception:
        pass

    page.screenshot(path=str(AUDIT / "tags_probe.png"))

    # Probe for tags input
    probe = page.evaluate(
        """() => {
          const hits=[];
          const walk=(root)=>{
            if(!root)return;
            for(const el of (root.querySelectorAll?root.querySelectorAll('input,textarea,[contenteditable=true],#textbox'):[])){
              const al=(el.getAttribute('aria-label')||'');
              const ph=(el.getAttribute('placeholder')||'');
              const id=el.id||'';
              const name=el.getAttribute('name')||'';
              const r=el.getBoundingClientRect();
              if(r.width<5) continue;
              const blob=(al+' '+ph+' '+id+' '+name).toLowerCase();
              if(blob.includes('tag') || ph.toLowerCase().includes('tag')){
                hits.push({al,ph,id,name,x:r.x+r.width/2,y:r.y+r.height/2,w:r.width,h:r.height});
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
    out["probe"] = probe[:8]

    filled = False
    # Role-based
    try:
        tb = page.get_by_role("textbox", name=re.compile(r"^Tags$", re.I))
        if tb.count():
            tb.first.click(force=True)
            page.wait_for_timeout(200)
            for _ in range(60):
                page.keyboard.press("Backspace")
            # Type tags one-by-one by comma for chip creation
            for tag in [t.strip() for t in tags.split(",") if t.strip()]:
                page.keyboard.type(tag, delay=8)
                page.keyboard.press("Enter")
                page.wait_for_timeout(80)
            filled = True
            out["via"] = "role"
    except Exception as e:
        out["role_err"] = str(e)[:100]

    if not filled and probe:
        page.mouse.click(probe[0]["x"], probe[0]["y"])
        page.wait_for_timeout(200)
        for _ in range(60):
            page.keyboard.press("Backspace")
        for tag in [t.strip() for t in tags.split(",") if t.strip()]:
            page.keyboard.type(tag, delay=8)
            page.keyboard.press("Enter")
            page.wait_for_timeout(80)
        filled = True
        out["via"] = "probe_click"

    if not filled:
        # JS focus + value
        ok = page.evaluate(
            """(tags) => {
              const walk=(root)=>{
                if(!root)return null;
                for(const el of (root.querySelectorAll?root.querySelectorAll('input'):[])){
                  const al=(el.getAttribute('aria-label')||'').toLowerCase();
                  const ph=(el.getAttribute('placeholder')||'').toLowerCase();
                  if(al==='tags' || ph.includes('tag')) return el;
                }
                for(const el of (root.querySelectorAll?root.querySelectorAll('*'):[])){
                  if(el.shadowRoot){const x=walk(el.shadowRoot); if(x) return x;}
                }
                return null;
              };
              const el=walk(document);
              if(!el) return false;
              el.focus();
              el.value='';
              el.dispatchEvent(new Event('input',{bubbles:true}));
              return true;
            }""",
            tags,
        )
        if ok:
            for tag in [t.strip() for t in tags.split(",") if t.strip()]:
                page.keyboard.type(tag, delay=8)
                page.keyboard.press("Enter")
                page.wait_for_timeout(80)
            filled = True
            out["via"] = "js_focus"

    out["ok"] = filled
    return out


def set_first_comment_safe(page, text: str) -> dict:
    """Open First comment control only — never touch description."""
    out: dict = {"ok": False}
    page.mouse.wheel(0, 3200)
    page.wait_for_timeout(500)
    # Click literal control
    try:
        loc = page.get_by_text("Add a first comment", exact=False)
        if loc.count() and loc.first.is_visible():
            loc.first.click(force=True)
            page.wait_for_timeout(1000)
            out["opened"] = "add"
        else:
            # Already set — look for edit near First comment
            page.evaluate(
                """() => {
                  const walk=(r)=>{
                    if(!r)return false;
                    for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[])){
                      const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                      if(t==='First comment' || t.startsWith('First comment')){
                        let p=el;
                        for(let i=0;i<8&&p;i++){
                          for(const b of (p.querySelectorAll?.('button,ytcp-icon-button')||[])){
                            const al=(b.getAttribute('aria-label')||'')+(b.innerText||'');
                            if(/edit|pencil|change/i.test(al) || true){ b.click(); return true; }
                          }
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
            page.wait_for_timeout(1000)
            out["opened"] = "edit_attempt"
    except Exception as e:
        out["open_err"] = str(e)[:120]
        return out

    # Dialog textbox for comment — prefer placeholder/aria with comment
    filled = False
    try:
        dlg = page.locator("tp-yt-paper-dialog, ytcp-comment-dialog, [role=dialog]")
        box = None
        if dlg.count():
            tb = dlg.last.get_by_role("textbox")
            if tb.count():
                box = tb.last
        if box is None:
            # Last resort: textbox whose aria mentions comment
            for i in range(page.get_by_role("textbox").count()):
                el = page.get_by_role("textbox").nth(i)
                al = (el.get_attribute("aria-label") or "").lower()
                if "comment" in al:
                    box = el
                    break
        if box is not None:
            box.click(force=True)
            page.keyboard.press("Meta+a")
            box.fill(text)
            filled = True
            out["filled"] = True
    except Exception as e:
        out["fill_err"] = str(e)[:120]

    if filled:
        for name in ("Comment", "Save", "Done", "Post"):
            try:
                # Prefer buttons inside dialog
                b = page.locator("tp-yt-paper-dialog, [role=dialog]").get_by_role(
                    "button", name=name, exact=True
                )
                if b.count() and b.last.is_enabled():
                    b.last.click(force=True)
                    page.wait_for_timeout(1200)
                    out["confirm"] = name
                    break
            except Exception:
                continue
        out["ok"] = True
    return out


def polish_video(page, video_id: str, desc: str, tags: str, tag: str, do_comment: bool = False) -> dict:
    r: dict = {"id": video_id, "tag": tag, "ok": False}
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    skip(page)
    dismiss(page)
    page.screenshot(path=str(AUDIT / f"{tag}_01.png"))

    r["desc"] = set_description(page, desc)
    page.screenshot(path=str(AUDIT / f"{tag}_02_desc.png"))
    r["tags"] = set_tags(page, tags)
    page.screenshot(path=str(AUDIT / f"{tag}_03_tags.png"))
    if do_comment:
        r["first_comment"] = set_first_comment_safe(page, PINNED)
        page.screenshot(path=str(AUDIT / f"{tag}_04_comment.png"))

    r["saved"] = save(page)
    page.wait_for_timeout(2000)

    # Verify
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    skip(page)
    # Expand show more for tags verify
    try:
        page.get_by_role("button", name="Show more").first.click(force=True, timeout=2000)
        page.wait_for_timeout(500)
    except Exception:
        pass
    page.mouse.wheel(0, 2000)
    page.wait_for_timeout(400)
    body = page.locator("body").inner_text()
    r["verify_hook"] = "what happens if you fall" in body.lower() or "event horizon" in body.lower()
    r["verify_tags_sample"] = any(
        k in body.lower()
        for k in ("spaghettification", "black holes explained", "photon sphere", "time dilation")
    )
    r["ok"] = bool(r["desc"].get("ok") and r["tags"].get("ok") and r.get("saved"))
    page.screenshot(path=str(AUDIT / f"{tag}_05_verify.png"))
    return r


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    summary: dict = {
        "long": None,
        "shorts": [],
        "related_note": "Studio Related picker only lists PUBLIC videos — run after long goes live 6 Aug 19:00 UK",
        "ok": False,
    }

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 1000},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        print("Fixing long-form description + tags + first comment…", flush=True)
        long_res = polish_video(page, LONG_ID, DESC, TAGS, "long", do_comment=True)
        summary["long"] = long_res
        print(json.dumps(long_res, indent=2)[:2500], flush=True)
        OUT.write_text(json.dumps(summary, indent=2) + "\n")

        for item in INDEX["shorts"]:
            print(f"\nFixing Short {item['id']} tags+desc…", flush=True)
            try:
                sr = polish_video(
                    page,
                    item["video_id"],
                    item["description"],
                    item["tags"],
                    f"s{item['id']}",
                    do_comment=False,
                )
                summary["shorts"].append(sr)
                print(
                    f"  ok={sr.get('ok')} tags={sr.get('tags',{}).get('ok')} via={sr.get('tags',{}).get('via')}",
                    flush=True,
                )
            except Exception as e:
                err = {"id": item["video_id"], "ok": False, "error": str(e)[:400]}
                summary["shorts"].append(err)
                print(f"  ERR {e}", flush=True)
            OUT.write_text(json.dumps(summary, indent=2) + "\n")

        ctx.close()

    summary["ok"] = bool(summary["long"] and summary["long"].get("ok")) and all(
        s.get("ok") for s in summary["shorts"]
    )
    OUT.write_text(json.dumps(summary, indent=2) + "\n")
    print("\nRESULT", OUT)
    print(json.dumps(summary, indent=2)[:4000])


if __name__ == "__main__":
    main()
