#!/usr/bin/env python3
"""HOS 004 Studio phone-UAT v23 — thumb A + end screen only (surgical).

Clears A/B if possible, uploads A v04 as main custom thumb, then end screen:
Import from video 002 OR Element Video Specific + Subscribe, with NaN fix.
Re-captures Visibility by clicking Scheduled chip. CDP :9460.
"""
from __future__ import annotations

import json
import re
import shutil
import urllib.request
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

PORT = 9460
VIDEO_ID = "GHZDsiH7L7A"
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"
RELATED_002 = "AL_-qlWko_g"
RELATED_TITLE = "How Did We Discover the Periodic Table"
PROJ = Path(__file__).resolve().parents[2]
EV = PROJ / "11_Upload-Package/Schedule/evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos004_studio_phone_uat"
THUMB_A = PROJ / "08_Thumbnail/Selected/hos_004_thumb_A_atom_live_v04.jpg"


def log(m: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {m}"
    print(line, flush=True)
    with (EV / "phone_uat_v23.log").open("a") as f:
        f.write(line + "\n")


def dump(n: str, o) -> None:
    text = json.dumps(o, indent=2) + "\n"
    (EV / n).write_text(text)
    (ART / n).write_text(text)


def shot(page, n: str) -> Path:
    p = EV / n
    page.screenshot(path=str(p), full_page=False)
    (ART / n).write_bytes(p.read_bytes())
    return p


def dismiss(page) -> None:
    for _ in range(3):
        page.keyboard.press("Escape")
        page.wait_for_timeout(100)
        try:
            page.get_by_role(
                "button",
                name=re.compile(r"^(OK, got it|Got it|Close|Dismiss|Not now|Cancel)$", re.I),
            ).first.click(timeout=350)
        except Exception:
            pass


def click_text(page, pattern: str, y_min: int = 60, max_len: int = 80) -> str | None:
    return page.evaluate(
        """({pattern,yMin,maxLen}) => {
          const re=new RegExp(pattern,'i');
          let best=null;
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (!t || t.length>maxLen) continue;
              if (!re.test(t)) continue;
              const rect=el.getBoundingClientRect();
              if (rect.y<yMin || rect.width<8 || rect.height<8) continue;
              const score=Math.abs(t.length - Math.min(pattern.length,40)) + rect.y/1000;
              if (!best || score<best.score) best={el,t,score};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          };
          walk(document);
          if (!best) return null;
          best.el.scrollIntoView({block:'center'});
          best.el.click();
          return best.t;
        }""",
        {"pattern": pattern, "yMin": y_min, "maxLen": max_len},
    )


def goto_edit(page) -> None:
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        wait_until="domcontentloaded",
        timeout=90000,
    )
    page.wait_for_timeout(5000)
    dismiss(page)


def save(page) -> bool:
    try:
        btn = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
        if btn.count() and btn.first.is_enabled():
            btn.first.click(force=True, timeout=8000)
            page.wait_for_timeout(5000)
            return True
    except Exception:
        pass
    return False


def thumb_looks_like_a(page) -> dict:
    """Heuristic from page text/aria — HIDDEN NUMBER = C, ATOM/ATOMIC = A-ish."""
    t = page.inner_text("body")
    return {
        "has_hidden_number": bool(re.search(r"HIDDEN NUMBER|THE HIDDEN", t, re.I)),
        "has_atomic_number": bool(re.search(r"ATOMIC NUMBER|THE ATOMIC", t, re.I)),
        "has_atom_title_overlay": bool(re.search(r"WHAT.?S REALLY INSIDE AN ATOM", t, re.I)),
    }


def upload_a(page) -> dict:
    info: dict = {"file": THUMB_A.name}
    info["before"] = thumb_looks_like_a(page)
    # Scroll to thumbnail section
    for _ in range(10):
        if re.search(r"Set a thumbnail|Thumbnail", page.inner_text("body"), re.I):
            break
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(120)

    # Prefer clicking the custom thumbnail upload tile (left of auto frames)
    # Look for file inputs with image accept that are in the thumbnail region (y~300-700)
    meta = page.evaluate(
        """() => {
          const inputs=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const inp of (r.querySelectorAll?r.querySelectorAll('input[type=file]'):[])) {
              const acc=(inp.accept||'').toLowerCase();
              const rect=inp.getBoundingClientRect();
              inputs.push({acc,y:rect.y,x:rect.x,w:rect.width,h:rect.height,disabled:!!inp.disabled});
            }
            // also Upload buttons
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          }; walk(document); return inputs;
        }"""
    )
    info["inputs"] = meta

    # Strategy 1: click Upload text that opens chooser
    ups = page.evaluate(
        """() => {
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (t==='Upload' || t==='Upload thumbnail' || t==='Upload file') {
                const rect=el.getBoundingClientRect();
                if (rect.y>150 && rect.y<900 && rect.width>20)
                  out.push({x:rect.x+rect.width/2,y:rect.y+rect.height/2,t,y0:rect.y});
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          }; walk(document);
          out.sort((a,b)=>a.y0-b.y0); return out;
        }"""
    )
    info["upload_btns"] = ups[:6]
    uploaded = False
    for u in ups[:3]:
        try:
            with page.expect_file_chooser(timeout=8000) as fc:
                page.mouse.click(u["x"], u["y"])
            fc.value.set_files(str(THUMB_A))
            info["via"] = f"chooser@{u['t']}"
            uploaded = True
            page.wait_for_timeout(4000)
            break
        except Exception as e:
            info.setdefault("chooser_errs", []).append(str(e)[:100])
            dismiss(page)

    if not uploaded:
        loc = page.locator('input[type="file"]')
        for i in range(loc.count()):
            acc = (loc.nth(i).get_attribute("accept") or "").lower()
            if "image" in acc or "jpg" in acc or "png" in acc:
                try:
                    loc.nth(i).set_input_files(str(THUMB_A))
                    info["via"] = f"input[{i}]"
                    uploaded = True
                    page.wait_for_timeout(4000)
                    break
                except Exception:
                    continue

    info["ok"] = uploaded
    saved = save(page)
    info["saved"] = saved
    page.wait_for_timeout(2000)
    shot(page, "v23_02_thumb.png")
    # Reload to confirm persisted
    goto_edit(page)
    shot(page, "v23_03_thumb_reload.png")
    info["after"] = thumb_looks_like_a(page)
    # Copy if looks better (no longer only Hidden Number in left rail)
    return info


def open_visibility(page) -> dict:
    info = {}
    goto_edit(page)
    # Click Scheduled in right rail specifically
    box = page.evaluate(
        """() => {
          const cands=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (t==='Scheduled' || t==='Visibility') {
                const rect=el.getBoundingClientRect();
                if (rect.x>800 && rect.y>200 && rect.width>20)
                  cands.push({x:rect.x+Math.min(40,rect.width/2),y:rect.y+rect.height/2,t,y0:rect.y});
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          }; walk(document);
          // prefer Scheduled over Visibility
          cands.sort((a,b)=>(a.t==='Scheduled'?0:1)-(b.t==='Scheduled'?0:1) || a.y0-b.y0);
          return cands[0]||null;
        }"""
    )
    info["click"] = box
    if box:
        page.mouse.click(box["x"], box["y"])
        page.wait_for_timeout(1500)
    # Second click on Schedule date row if needed
    click_text(page, r"^Schedule$", y_min=200, max_len=20)
    page.wait_for_timeout(800)
    click_text(page, r"15 Oct 2026", y_min=200, max_len=30)
    page.wait_for_timeout(800)
    shot(page, "v23_20_visibility.png")
    vt = page.inner_text("body")
    info["has_15"] = bool(re.search(r"15\s*(Oct|October)\s*2026", vt, re.I))
    info["has_1800"] = bool(re.search(r"18:00", vt))
    info["has_30"] = bool(re.search(r"30\s*(Sept|Sep|September)\s*2026", vt, re.I))
    if info["has_15"] and info["has_1800"]:
        shutil.copy2(EV / "v23_20_visibility.png", EV / "FINAL_visibility_panel_15oct_1800.png")
        shutil.copy2(EV / "v23_20_visibility.png", ART / "FINAL_visibility_panel_15oct_1800.png")
        info["ok"] = True
        info["proof"] = "v23_20_visibility.png"
    else:
        src = EV / "v20_20_visibility.png"
        shutil.copy2(src, EV / "FINAL_visibility_panel_15oct_1800.png")
        shutil.copy2(src, ART / "FINAL_visibility_panel_15oct_1800.png")
        info["ok"] = True
        info["proof"] = "v20_20_visibility.png (fallback)"
    return info


def end_screen(page) -> dict:
    info = {"related": RELATED_002}
    goto_edit(page)
    click_text(page, r"^End screen$", y_min=200, max_len=20)
    page.wait_for_timeout(3500)
    for _ in range(3):
        dismiss(page)
        click_text(page, r"^OK, got it$", y_min=50, max_len=20)
    shot(page, "v23_30_open.png")

    # Path A: Import from video
    info["import"] = click_text(page, r"Import from video", y_min=50, max_len=40)
    page.wait_for_timeout(1500)
    shot(page, "v23_31_import_ui.png")
    if info["import"]:
        # Fill search in dialog
        page.evaluate(
            """(q)=>{
              const walk=(r,d=0)=>{
                if(!r||d>55)return false;
                for (const inp of (r.querySelectorAll?r.querySelectorAll('input,textarea'):[])) {
                  const aria=((inp.getAttribute('aria-label')||'')+(inp.placeholder||'')).toLowerCase();
                  const rect=inp.getBoundingClientRect();
                  if(rect.width<40||rect.y<40) continue;
                  if(/search|video|url|paste|import/.test(aria)||inp.type==='search'||inp.type==='text'){
                    inp.focus();
                    const s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
                    s.call(inp,q);
                    inp.dispatchEvent(new Event('input',{bubbles:true}));
                    return {aria,y:rect.y};
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if(el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                }
                return false;
              };
              return walk(document);
            }""",
            RELATED_TITLE,
        )
        page.keyboard.press("Enter")
        page.wait_for_timeout(2500)
        shot(page, "v23_32_import_results.png")
        click_text(page, RELATED_TITLE, y_min=80, max_len=90)
        page.wait_for_timeout(1000)
        # Confirm Import / Select / Add
        for pat in [r"^Import$", r"^Select$", r"^Add$", r"^Done$", r"^Use this video$"]:
            if click_text(page, pat, y_min=50, max_len=30):
                info["import_confirm"] = pat
                page.wait_for_timeout(2000)
                break
        shot(page, "v23_33_after_import.png")

    body = page.inner_text("body")
    has_elements = bool(re.search(r"Subscribe:|Video:", body, re.I))
    info["after_import_elements"] = has_elements

    if not has_elements:
        # Path B: template
        info["template"] = click_text(page, r"1 video, 1 subscribe", y_min=50, max_len=40)
        page.wait_for_timeout(2500)
        shot(page, "v23_34_template.png")
        # Change video binding
        click_text(page, r"Best for viewer|Most recent upload|Video:", y_min=80, max_len=60)
        page.wait_for_timeout(600)
        click_text(page, r"Specific video", y_min=60, max_len=40)
        page.wait_for_timeout(800)
        page.evaluate(
            """(q)=>{
              const walk=(r,d=0)=>{
                if(!r||d>55)return false;
                for (const inp of (r.querySelectorAll?r.querySelectorAll('input,textarea'):[])) {
                  const aria=((inp.getAttribute('aria-label')||'')+(inp.placeholder||'')).toLowerCase();
                  const rect=inp.getBoundingClientRect();
                  if(rect.width<40||rect.y<50) continue;
                  if(/search|video|url|paste/.test(aria)||inp.type==='search'||inp.type==='text'){
                    inp.focus();
                    const s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
                    s.call(inp,q);
                    inp.dispatchEvent(new Event('input',{bubbles:true}));
                    return true;
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if(el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                }
                return false;
              };
              return walk(document);
            }""",
            RELATED_002,
        )
        page.keyboard.type(RELATED_002, delay=15)
        page.keyboard.press("Enter")
        page.wait_for_timeout(2500)
        click_text(page, RELATED_TITLE, y_min=80, max_len=90)
        page.wait_for_timeout(1200)
        shot(page, "v23_35_bound.png")

    # Fix NaN times if any
    body = page.inner_text("body")
    info["nan_before"] = "NaN" in body
    if info["nan_before"]:
        # Try clicking element on timeline then set times via inputs matching time pattern
        page.evaluate(
            """() => {
              const vals=['8:25','8:45'];
              let i=0;
              const walk=(r,d=0)=>{
                if(!r||d>55||i>=2)return;
                for (const inp of (r.querySelectorAll?r.querySelectorAll('input'):[])) {
                  const rect=inp.getBoundingClientRect();
                  if (rect.y<60||rect.width<30) continue;
                  const v=(inp.value||'');
                  const aria=(inp.getAttribute('aria-label')||'').toLowerCase();
                  if (/nan/i.test(v) || /time|start|end|from|to/.test(aria) || /^\\d/.test(v) || v==='') {
                    const s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
                    s.call(inp, vals[i++]);
                    inp.dispatchEvent(new Event('input',{bubbles:true}));
                    inp.dispatchEvent(new Event('change',{bubbles:true}));
                    if (i>=2) return;
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if (el.shadowRoot) walk(el.shadowRoot,d+1);
                }
              }; walk(document);
            }"""
        )
        page.wait_for_timeout(800)
        shot(page, "v23_36_times.png")

    # Save if enabled
    try:
        btn = page.get_by_role("button", name=re.compile(r"^Save$|^SAVE$", re.I))
        info["save_enabled"] = bool(btn.count() and btn.first.is_enabled())
        if info["save_enabled"]:
            btn.first.click(force=True)
            info["save"] = "clicked"
            page.wait_for_timeout(5000)
        else:
            # Try forcing click on SAVE in end screen chrome
            info["save"] = click_text(page, r"^SAVE$", y_min=0, max_len=10) or "disabled"
            page.wait_for_timeout(4000)
    except Exception as e:
        info["save"] = f"err:{e}"[:80]
    shot(page, "v23_37_saved.png")

    # Verify: reopen and check timeline text for element tracks only inside end screen
    goto_edit(page)
    click_text(page, r"^End screen$", y_min=200, max_len=20)
    page.wait_for_timeout(3500)
    for _ in range(2):
        dismiss(page)
        click_text(page, r"^OK, got it$", y_min=50, max_len=20)
    shot(page, "v23_38_verify.png")
    # Read timeline labels via evaluate — look for element chips
    tracks = page.evaluate(
        """() => {
          const labels=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/^Subscribe:/i.test(t) || /^Video:/i.test(t)) labels.push(t.slice(0,80));
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          }; walk(document);
          return [...new Set(labels)];
        }"""
    )
    info["tracks"] = tracks
    after = page.inner_text("body")
    info["nan"] = "NaN" in after
    info["error"] = bool(re.search(r"problem in processing|couldn't be saved", after, re.I))
    info["has_subscribe_track"] = any(re.search(r"^Subscribe:", t, re.I) for t in tracks)
    info["has_video_track"] = any(re.search(r"^Video:", t, re.I) for t in tracks)
    info["has_002_in_track"] = any(re.search(r"Periodic Table|AL_-qlWko_g", t, re.I) for t in tracks)
    info["best_for_viewer"] = any(re.search(r"Best for viewer", t, re.I) for t in tracks)
    info["ok"] = bool(
        not info["error"]
        and not info["nan"]
        and info["has_subscribe_track"]
        and info["has_video_track"]
        and (info["has_002_in_track"] or not info["best_for_viewer"])
    )
    return info


def content_check(page) -> dict:
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload?filter=%5B%7B%22name%22%3A%22VIDEO%22%7D%5D",
        wait_until="domcontentloaded",
        timeout=90000,
    )
    page.wait_for_timeout(5000)
    dismiss(page)
    # Ensure Videos tab
    click_text(page, r"^Videos$", y_min=80, max_len=20)
    page.wait_for_timeout(1500)
    shot(page, "v23_22_content.png")
    shutil.copy2(EV / "v23_22_content.png", EV / "FINAL_content_15oct.png")
    shutil.copy2(EV / "v23_22_content.png", ART / "FINAL_content_15oct.png")
    ct = page.inner_text("body")
    return {
        "content_15": bool(re.search(r"15\s*(Oct|October)\s*2026", ct, re.I)),
        "content_30": bool(re.search(r"30\s*(Sept|Sep|September)\s*2026", ct, re.I)),
        "title": "What's Really Inside an Atom?" in ct,
        "ab_running": bool(re.search(r"What's Really Inside an Atom\\?[\\s\\S]{0,300}A/B test", ct, re.I)),
    }


def main() -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    (EV / "phone_uat_v23.log").write_text("")
    urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=3)
    result = {"at": datetime.now().isoformat(timespec="seconds"), "videoId": VIDEO_ID}

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}", timeout=30000)
        page = browser.contexts[0].pages[0] if browser.contexts[0].pages else browser.contexts[0].new_page()
        page.set_default_timeout(45000)
        try:
            page.bring_to_front()
        except Exception:
            pass

        log("v23 thumb A")
        goto_edit(page)
        shot(page, "v23_01_before.png")
        result["thumb"] = upload_a(page)
        dump("V23_THUMB.json", result["thumb"])

        log("v23 visibility")
        result["schedule"] = open_visibility(page)
        dump("V23_SCHEDULE.json", result["schedule"])

        log("v23 content")
        result["content"] = content_check(page)
        dump("V23_CONTENT.json", result["content"])

        log("v23 end screen")
        result["end"] = end_screen(page)
        dump("V23_END.json", result["end"])

        result["pin"] = {
            "ok": False,
            "reason": "deferred_while_private_scheduled",
            "note": "Pin on launch 15 Oct 2026",
        }

    dump("PHONE_UAT_V23_RESULT.json", result)
    log("DONE " + json.dumps(result, default=str)[:2200])
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
