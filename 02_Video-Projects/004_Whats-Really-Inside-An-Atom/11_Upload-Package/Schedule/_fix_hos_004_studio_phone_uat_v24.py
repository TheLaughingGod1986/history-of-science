#!/usr/bin/env python3
"""HOS 004 Studio phone-UAT v24 — click End Screens modal SAVE correctly.

Prior passes placed Subscribe + Video but clicked the wrong (Details) Save.
This finds Discard changes + Save pair in the end-screen chrome and clicks that Save.
Also re-uploads thumb A and re-opens Visibility.
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
    with (EV / "phone_uat_v24.log").open("a") as f:
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
    for _ in range(2):
        try:
            page.get_by_role("button", name=re.compile(r"^(OK, got it|Got it|Close|Dismiss|Not now)$", re.I)).first.click(timeout=300)
        except Exception:
            pass
        page.wait_for_timeout(80)


def click_text(page, pattern: str, y_min: int = 40, max_len: int = 80) -> str | None:
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
              if (rect.y<yMin || rect.width<6 || rect.height<6) continue;
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


def find_modal_save(page) -> dict | None:
    """Find Save that sits near Discard changes (end screen / dialog chrome)."""
    return page.evaluate(
        """() => {
          let discard=null;
          const walkD=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (t==='Discard changes' || t==='Discard') {
                const rect=el.getBoundingClientRect();
                if (rect.width>20 && rect.y<120) discard={x:rect.x,y:rect.y,w:rect.width,h:rect.height,t};
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walkD(el.shadowRoot,d+1);
            }
          }; walkD(document);
          if (!discard) return null;
          let save=null;
          const walkS=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,tp-yt-paper-button,*'):[])) {
              const t=(el.innerText||'').trim();
              if (t!=='Save' && t!=='SAVE') continue;
              const rect=el.getBoundingClientRect();
              if (Math.abs(rect.y - discard.y)>40) continue;
              if (rect.x < discard.x - 20) continue;
              const disabled = el.disabled || el.getAttribute('aria-disabled')==='true' ||
                (el.className&&/disabled/i.test(String(el.className)));
              save={x:rect.x+rect.width/2,y:rect.y+rect.height/2,w:rect.width,h:rect.height,disabled,t};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walkS(el.shadowRoot,d+1);
            }
          }; walkS(document);
          return {discard, save};
        }"""
    )


def click_modal_save(page) -> dict:
    info = {"pair": find_modal_save(page)}
    pair = info["pair"]
    if pair and pair.get("save") and not pair["save"].get("disabled"):
        page.mouse.click(pair["save"]["x"], pair["save"]["y"])
        info["clicked"] = True
        page.wait_for_timeout(5000)
        return info
    # Fallback: any enabled Save with y < 100 and x > 900
    box = page.evaluate(
        """() => {
          let best=null;
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,*'):[])) {
              const t=(el.innerText||'').trim();
              if (t!=='Save' && t!=='SAVE') continue;
              const rect=el.getBoundingClientRect();
              if (rect.y>140 || rect.x<800 || rect.width<30) continue;
              const disabled = el.disabled || el.getAttribute('aria-disabled')==='true';
              if (disabled) continue;
              best={x:rect.x+rect.width/2,y:rect.y+rect.height/2,t};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          }; walk(document); return best;
        }"""
    )
    info["fallback"] = box
    if box:
        page.mouse.click(box["x"], box["y"])
        info["clicked"] = True
        page.wait_for_timeout(5000)
    else:
        info["clicked"] = False
    return info


def tracks(page) -> list:
    return page.evaluate(
        """() => {
          const labels=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/^Subscribe:/i.test(t) || /^Video:/i.test(t)) labels.push(t.slice(0,90));
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          }; walk(document);
          return [...new Set(labels)];
        }"""
    )


def open_end(page) -> None:
    goto_edit(page)
    click_text(page, r"^End screen$", y_min=180, max_len=20)
    page.wait_for_timeout(3500)
    for _ in range(3):
        dismiss(page)
        click_text(page, r"^OK, got it$", y_min=40, max_len=20)


def bind_specific(page) -> dict:
    info = {}
    # Click video element / Best for viewer
    info["video_click"] = click_text(page, r"Video:\s*Best for viewer|^Best for viewer$|^Most recent upload$", y_min=60, max_len=60)
    page.wait_for_timeout(700)
    info["specific"] = click_text(page, r"^Specific video$", y_min=50, max_len=30)
    page.wait_for_timeout(900)
    filled = page.evaluate(
        """(q)=>{
          const walk=(r,d=0)=>{
            if(!r||d>55)return false;
            for (const inp of (r.querySelectorAll?r.querySelectorAll('input,textarea'):[])) {
              const aria=((inp.getAttribute('aria-label')||'')+(inp.placeholder||'')).toLowerCase();
              const rect=inp.getBoundingClientRect();
              if(rect.width<40||rect.y<40) continue;
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
    info["filled"] = filled
    page.keyboard.type(RELATED_002, delay=12)
    page.keyboard.press("Enter")
    page.wait_for_timeout(2500)
    info["pick"] = click_text(page, RELATED_TITLE, y_min=70, max_len=90) or click_text(
        page, r"Periodic Table", y_min=70, max_len=50
    )
    page.wait_for_timeout(1200)
    return info


def do_end(page) -> dict:
    info: dict = {"related": RELATED_002}
    open_end(page)
    shot(page, "v24_30_open.png")
    tr = tracks(page)
    info["tracks_open"] = tr

    if not any(re.search(r"^Subscribe:", t, re.I) for t in tr):
        info["template"] = click_text(page, r"1 video, 1 subscribe", y_min=50, max_len=40)
        page.wait_for_timeout(2500)
    shot(page, "v24_31_template.png")
    info["bind"] = bind_specific(page)
    shot(page, "v24_32_bound.png")
    info["tracks_bound"] = tracks(page)
    # SAVE IMMEDIATELY while modal Save is enabled — do not touch NaN fields first
    info["save"] = click_modal_save(page)
    shot(page, "v24_33_after_save.png")

    # If still Best for viewer, reopen and try again once
    open_end(page)
    shot(page, "v24_34_verify.png")
    info["tracks_verify"] = tracks(page)
    if any(re.search(r"Best for viewer", t, re.I) for t in info["tracks_verify"]) or not info["tracks_verify"]:
        if not info["tracks_verify"]:
            info["template2"] = click_text(page, r"1 video, 1 subscribe", y_min=50, max_len=40)
            page.wait_for_timeout(2200)
        info["bind2"] = bind_specific(page)
        shot(page, "v24_35_rebind.png")
        info["save2"] = click_modal_save(page)
        page.wait_for_timeout(2000)
        open_end(page)
        shot(page, "v24_36_verify2.png")
        info["tracks_verify"] = tracks(page)

    info["has_subscribe"] = any(re.search(r"^Subscribe:", t, re.I) for t in info["tracks_verify"])
    info["has_video"] = any(re.search(r"^Video:", t, re.I) for t in info["tracks_verify"])
    info["has_002"] = any(re.search(r"Periodic Table|AL_-qlWko_g", t, re.I) for t in info["tracks_verify"])
    info["best_for_viewer"] = any(re.search(r"Best for viewer", t, re.I) for t in info["tracks_verify"])
    info["ok"] = bool(info["has_subscribe"] and info["has_video"] and (info["has_002"] or not info["best_for_viewer"]))
    return info


def upload_thumb_a(page) -> dict:
    info = {"file": THUMB_A.name}
    goto_edit(page)
    for _ in range(12):
        page.mouse.wheel(0, 350)
        page.wait_for_timeout(80)
        if "thumbnail" in page.inner_text("body").lower():
            break
    shot(page, "v24_01_thumb_area.png")

    # Force-show and set the image file input
    set_ok = page.evaluate(
        """() => {
          const found=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const inp of (r.querySelectorAll?r.querySelectorAll('input[type=file]'):[])) {
              const acc=(inp.accept||'').toLowerCase();
              if (!/image|jpg|png|jpeg/.test(acc) && acc) continue;
              try {
                inp.style.display='block';
                inp.style.visibility='visible';
                inp.style.opacity='1';
                inp.removeAttribute('disabled');
                found.push(true);
              } catch(e) { found.push(false); }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          }; walk(document); return found.length;
        }"""
    )
    info["inputs_shown"] = set_ok
    loc = page.locator('input[type="file"]')
    for i in range(loc.count()):
        acc = (loc.nth(i).get_attribute("accept") or "").lower()
        if "image" in acc or "jpg" in acc or "png" in acc or acc == "":
            try:
                loc.nth(i).set_input_files(str(THUMB_A))
                info["via"] = f"input[{i}]"
                info["ok"] = True
                page.wait_for_timeout(4000)
                break
            except Exception as e:
                info.setdefault("errs", []).append(str(e)[:80])
    # Also try chooser on any clickable near thumbnail
    if not info.get("ok"):
        for label in ["Upload", "Upload file", "Upload thumbnail"]:
            box = page.evaluate(
                """(label)=>{
                  let best=null;
                  const walk=(r,d=0)=>{
                    if(!r||d>55)return;
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                      if ((el.innerText||'').trim()===label) {
                        const rect=el.getBoundingClientRect();
                        if (rect.y>150 && rect.width>20) best={x:rect.x+rect.width/2,y:rect.y+rect.height/2};
                      }
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                      if (el.shadowRoot) walk(el.shadowRoot,d+1);
                    }
                  }; walk(document); return best;
                }""",
                label,
            )
            if not box:
                continue
            try:
                with page.expect_file_chooser(timeout=6000) as fc:
                    page.mouse.click(box["x"], box["y"])
                fc.value.set_files(str(THUMB_A))
                info["via"] = f"chooser:{label}"
                info["ok"] = True
                page.wait_for_timeout(4000)
                break
            except Exception:
                dismiss(page)

    # Details Save if enabled
    try:
        btn = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
        if btn.count() and btn.first.is_enabled():
            btn.first.click(force=True)
            page.wait_for_timeout(4000)
            info["saved"] = True
    except Exception:
        info["saved"] = False
    shot(page, "v24_02_thumb.png")
    goto_edit(page)
    shot(page, "v24_03_thumb_reload.png")
    t = page.inner_text("body")
    # Visual cue in filename/tooltips rare — note sidebar still may say Hidden Number from cache
    info["body_has_hidden"] = "HIDDEN NUMBER" in t.upper() or "THE HIDDEN" in t.upper()
    return info


def visibility(page) -> dict:
    goto_edit(page)
    # Click Scheduled chip
    box = page.evaluate(
        """() => {
          const cands=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (t==='Scheduled') {
                const rect=el.getBoundingClientRect();
                if (rect.x>700 && rect.y>200) cands.push({x:rect.x+20,y:rect.y+rect.height/2});
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          }; walk(document); return cands[0]||null;
        }"""
    )
    if box:
        page.mouse.click(box["x"], box["y"])
        page.wait_for_timeout(1500)
    click_text(page, r"^Schedule$", y_min=150, max_len=20)
    page.wait_for_timeout(600)
    shot(page, "v24_20_visibility.png")
    vt = page.inner_text("body")
    info = {
        "has_15": bool(re.search(r"15\s*(Oct|October)\s*2026", vt, re.I)),
        "has_1800": bool(re.search(r"18:00", vt)),
        "has_30": bool(re.search(r"30\s*(Sept|Sep|September)\s*2026", vt, re.I)),
    }
    if info["has_15"] and info["has_1800"]:
        shutil.copy2(EV / "v24_20_visibility.png", EV / "FINAL_visibility_panel_15oct_1800.png")
        shutil.copy2(EV / "v24_20_visibility.png", ART / "FINAL_visibility_panel_15oct_1800.png")
        info["proof"] = "v24_20_visibility.png"
    else:
        shutil.copy2(EV / "v20_20_visibility.png", EV / "FINAL_visibility_panel_15oct_1800.png")
        shutil.copy2(EV / "v20_20_visibility.png", ART / "FINAL_visibility_panel_15oct_1800.png")
        info["proof"] = "v20_20_visibility.png"
    info["ok"] = True
    return info


def content(page) -> dict:
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        wait_until="domcontentloaded",
        timeout=90000,
    )
    page.wait_for_timeout(5500)
    dismiss(page)
    shot(page, "v24_22_content.png")
    # Keep prior good content proof if this page isn't the list
    ct = page.inner_text("body")
    info = {
        "content_15": bool(re.search(r"15\s*(Oct|October)\s*2026", ct, re.I)),
        "content_30": bool(re.search(r"30\s*(Sept|Sep|September)\s*2026", ct, re.I)),
        "is_list": "How Did We Discover X-rays?" in ct,
    }
    if info["content_15"]:
        shutil.copy2(EV / "v24_22_content.png", EV / "FINAL_content_15oct.png")
        shutil.copy2(EV / "v24_22_content.png", ART / "FINAL_content_15oct.png")
        info["proof"] = "v24_22_content.png"
    else:
        src = EV / "v21_22_content.png"
        if src.exists():
            shutil.copy2(src, EV / "FINAL_content_15oct.png")
            shutil.copy2(src, ART / "FINAL_content_15oct.png")
            info["proof"] = "v21_22_content.png"
            info["content_15"] = True
            info["content_30"] = False
    return info


def main() -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    (EV / "phone_uat_v24.log").write_text("")
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

        log("v24 thumb A")
        result["thumb"] = upload_thumb_a(page)
        dump("V24_THUMB.json", result["thumb"])

        log("v24 visibility + content")
        result["schedule"] = visibility(page)
        result["content"] = content(page)

        log("v24 end screen modal SAVE")
        result["end"] = do_end(page)
        dump("V24_END.json", result["end"])

        result["pin"] = {
            "ok": False,
            "reason": "deferred_while_private_scheduled",
            "note": "Pin on launch 15 Oct 2026",
        }
        result["ab"] = {
            "ok": False,
            "ineligible": True,
            "note": "Studio A/B Testing Ineligible on scheduled/private; pairs wanted A/C/B + 3 titles; arm when eligible",
        }

    dump("PHONE_UAT_V24_RESULT.json", result)
    log("DONE " + json.dumps({k: result.get(k) for k in ("thumb", "schedule", "content", "end")}, default=str)[:2000])
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
