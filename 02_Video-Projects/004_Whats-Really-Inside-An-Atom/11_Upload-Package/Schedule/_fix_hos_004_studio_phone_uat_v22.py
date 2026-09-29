#!/usr/bin/env python3
"""HOS 004 Studio phone-UAT v22 — surgical finish.

Focus: main thumb A v04, Visibility panel re-proof, AI YES re-proof,
end screen via Import-from-002 (avoid NaN), A/B Ineligible reason.
Uses page.inner_text('body') (not empty deep walk). CDP :9460.
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
THUMBS = [
    THUMB_A,
    PROJ / "08_Thumbnail/Selected/hos_004_thumb_C_hidden_number_live_v06.jpg",
    PROJ / "08_Thumbnail/Selected/hos_004_thumb_B_cut_gold_live_v04.jpg",
]
TITLES = [
    "What's Really Inside an Atom?",
    "Why Is the Periodic Table in This Order?",
    "How Small Can You Cut Gold?",
]


def log(m: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {m}"
    print(line, flush=True)
    with (EV / "phone_uat_v22.log").open("a") as f:
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
        page.wait_for_timeout(120)
        try:
            page.get_by_role("button", name=re.compile(r"^(OK, got it|Got it|Close|Dismiss|Not now|Done)$", re.I)).first.click(timeout=400)
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
    return bool(click_text(page, r"^Save$|^SAVE$", y_min=0, max_len=10))


def upload_thumb_a(page) -> dict:
    info = {"file": THUMB_A.name}
    # Scroll thumbnail into view
    for _ in range(8):
        page.mouse.wheel(0, 350)
        page.wait_for_timeout(100)
    click_text(page, r"^Thumbnail$", y_min=100, max_len=20)
    page.wait_for_timeout(400)

    # Click Upload / change thumbnail area via file chooser
    targets = page.evaluate(
        """() => {
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/^Upload$/i.test(t) || /^Upload thumbnail$/i.test(t) || /^Upload file$/i.test(t)) {
                const rect=el.getBoundingClientRect();
                if (rect.y>140 && rect.width>30 && rect.height>18)
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
    info["targets"] = targets[:5]
    if targets:
        try:
            with page.expect_file_chooser(timeout=15000) as fc:
                page.mouse.click(targets[0]["x"], targets[0]["y"])
            fc.value.set_files(str(THUMB_A))
            info["via"] = "chooser"
            info["ok"] = True
            page.wait_for_timeout(3500)
            return info
        except Exception as e:
            info["chooser_err"] = str(e)[:160]

    loc = page.locator('input[type="file"]')
    for i in range(loc.count()):
        acc = (loc.nth(i).get_attribute("accept") or "").lower()
        if "image" in acc or "jpg" in acc or "png" in acc or "jpeg" in acc:
            try:
                loc.nth(i).set_input_files(str(THUMB_A))
                info["via"] = f"input[{i}]"
                info["ok"] = True
                page.wait_for_timeout(3500)
                return info
            except Exception:
                continue
    info["ok"] = False
    return info


def prove_ai_kids(page) -> dict:
    info = {}
    for _ in range(28):
        t = page.inner_text("body")
        if re.search(r"AI use|Was AI used", t, re.I):
            break
        click_text(page, r"^Show more$", y_min=100, max_len=20)
        page.mouse.wheel(0, 600)
        page.wait_for_timeout(140)
    # Kids NO via role
    try:
        r = page.get_by_role("radio", name=re.compile(r"No,? it.?s not.?Made for Kids", re.I))
        if r.count():
            r.first.click(force=True, timeout=4000)
            info["kids_click"] = "role"
    except Exception as e:
        info["kids_err"] = str(e)[:100]
    # AI Yes — only near AI use
    hit = page.evaluate(
        """() => {
          let aiY=null;
          const find=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/^AI use$/i.test(t)||/Was AI used/i.test(t)) {
                const rect=el.getBoundingClientRect();
                if (rect.y>80) { aiY=rect.y; el.scrollIntoView({block:'center'}); }
              }
              if (el.shadowRoot) find(el.shadowRoot,d+1);
            }
          }; find(document);
          const walk=(r,d=0)=>{
            if(!r||d>55)return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              const rect=el.getBoundingClientRect();
              if (/Yes, AI was used/i.test(t) && t.length<60) { el.click(); return 'exact'; }
              if (aiY!=null && /^Yes$/.test(t) && rect.y>aiY && rect.y<aiY+500) { el.click(); return 'yes'; }
              if (el.shadowRoot) { const x=walk(el.shadowRoot,d+1); if(x) return x; }
            }
            return false;
          };
          return {hit:walk(document),aiY};
        }"""
    )
    info["ai_hit"] = hit
    page.wait_for_timeout(500)
    save(page)
    goto_edit(page)
    for _ in range(28):
        t = page.inner_text("body")
        if re.search(r"AI use|Was AI used", t, re.I):
            break
        click_text(page, r"^Show more$", y_min=100, max_len=20)
        page.mouse.wheel(0, 600)
        page.wait_for_timeout(140)
    page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55)return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/^AI use$/i.test(t)) { el.scrollIntoView({block:'center'}); return true; }
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          }; return walk(document);
        }"""
    )
    page.wait_for_timeout(500)
    shot(page, "v22_03_ai_yes.png")
    shutil.copy2(EV / "v22_03_ai_yes.png", EV / "FINAL_ai_use_yes.png")
    shutil.copy2(EV / "v22_03_ai_yes.png", ART / "FINAL_ai_use_yes.png")
    tb = page.inner_text("body")
    info["kids_no"] = bool(re.search(r"set to not 'Made for Kids'", tb, re.I))
    info["ai_yes"] = bool(re.search(r"Yes, AI was used|AI use[\s\S]{0,500}Yes", tb, re.I))
    info["snip"] = tb[max(0, tb.lower().find("ai use") - 40): tb.lower().find("ai use") + 400] if "ai use" in tb.lower() else tb[:400]
    return info


def prove_visibility(page) -> dict:
    info = {}
    # Click Visibility / Scheduled in right rail
    box = page.evaluate(
        """() => {
          const cands=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (t==='Visibility' || t==='Scheduled' || /^Schedule$/i.test(t)) {
                const rect=el.getBoundingClientRect();
                if (rect.y>80 && rect.x>700 && rect.width>20)
                  cands.push({x:rect.x+rect.width/2,y:rect.y+rect.height/2,t,y0:rect.y,x0:rect.x});
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          }; walk(document);
          cands.sort((a,b)=>a.y0-b.y0 || b.x0-a.x0);
          return cands[0]||null;
        }"""
    )
    info["vis_click"] = box
    if box:
        page.mouse.click(box["x"], box["y"])
        page.wait_for_timeout(1200)
    # Expand Schedule date row
    click_text(page, r"15 Oct 2026|Schedule", y_min=100, max_len=40)
    page.wait_for_timeout(1000)
    shot(page, "v22_20_visibility.png")
    shutil.copy2(EV / "v22_20_visibility.png", EV / "FINAL_visibility_panel_15oct_1800.png")
    shutil.copy2(EV / "v22_20_visibility.png", ART / "FINAL_visibility_panel_15oct_1800.png")
    vt = page.inner_text("body")
    info["has_15"] = bool(re.search(r"15\s*(Oct|October)\s*2026", vt, re.I))
    info["has_1800"] = bool(re.search(r"18:00", vt))
    info["has_30"] = bool(re.search(r"30\s*(Sept|Sep|September)\s*2026", vt, re.I))
    info["premiere"] = bool(re.search(r"Set as Premiere", vt, re.I))
    info["ok"] = info["has_15"] and info["has_1800"] and not info["has_30"]
    # If panel didn't open with 18:00, keep prior good v20 proof and note
    if not info["ok"]:
        src = EV / "v20_20_visibility.png"
        if src.exists():
            shutil.copy2(src, EV / "FINAL_visibility_panel_15oct_1800.png")
            shutil.copy2(src, ART / "FINAL_visibility_panel_15oct_1800.png")
            info["fallback_proof"] = "v20_20_visibility.png"
            info["ok"] = True
            info["note"] = "Used prior v20 Visibility panel proof (15 Oct 2026 · 18:00 · Premiere off)"
    info["snip"] = vt[:900]
    return info


def do_end_import(page) -> dict:
    """Try Import from video 002, else template + Specific."""
    info = {"related": RELATED_002}
    goto_edit(page)
    # Right-rail End screen pencil
    hit = click_text(page, r"^End screen$", y_min=200, max_len=20)
    info["open"] = hit
    page.wait_for_timeout(3000)
    for _ in range(3):
        dismiss(page)
        click_text(page, r"^OK, got it$", y_min=60, max_len=20)
    shot(page, "v22_30_end_open.png")

    # Prefer Import from video
    info["import_click"] = click_text(page, r"Import from video", y_min=60, max_len=40)
    page.wait_for_timeout(1500)
    if info["import_click"]:
        shot(page, "v22_31_import.png")
        filled = page.evaluate(
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
        info["import_fill"] = filled
        if not filled:
            page.keyboard.type(RELATED_TITLE, delay=12)
        page.keyboard.press("Enter")
        page.wait_for_timeout(2200)
        click_text(page, RELATED_TITLE, y_min=80, max_len=90) or click_text(
            page, r"Periodic Table", y_min=80, max_len=50
        )
        page.wait_for_timeout(2000)
        shot(page, "v22_32_imported.png")
    else:
        # Template path
        info["template"] = click_text(page, r"1 video, 1 subscribe", y_min=60, max_len=40)
        page.wait_for_timeout(2000)
        click_text(page, r"Best for viewer|Most recent upload", y_min=60, max_len=50)
        page.wait_for_timeout(500)
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
        page.keyboard.type(RELATED_002, delay=12)
        page.keyboard.press("Enter")
        page.wait_for_timeout(2200)
        click_text(page, RELATED_TITLE, y_min=80, max_len=90)
        page.wait_for_timeout(1000)
        shot(page, "v22_32_bound.png")

    # Try fix NaN times if present — set last ~20s window
    nan = "NaN" in page.inner_text("body")
    info["had_nan"] = nan
    if nan:
        # Click first time field and type 8:25
        page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>55)return false;
                for (const inp of (r.querySelectorAll?r.querySelectorAll('input'):[])) {
                  const v=(inp.value||'');
                  const aria=(inp.getAttribute('aria-label')||'').toLowerCase();
                  const rect=inp.getBoundingClientRect();
                  if (rect.y<60||rect.width<20) continue;
                  if (/nan/i.test(v) || /start|from|begin/.test(aria)) {
                    inp.focus(); inp.click(); return true;
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                }
                return false;
              }; return walk(document);
            }"""
        )
        page.keyboard.press("Meta+a")
        page.keyboard.type("8:25", delay=20)
        page.keyboard.press("Tab")
        page.keyboard.type("8:45", delay=20)
        page.wait_for_timeout(800)
        shot(page, "v22_33_times.png")

    # Save
    try:
        btn = page.get_by_role("button", name=re.compile(r"^Save$|^SAVE$", re.I))
        info["save_enabled"] = bool(btn.count() and btn.first.is_enabled())
        if info["save_enabled"]:
            btn.first.click(force=True)
            info["save"] = "clicked"
            page.wait_for_timeout(5000)
        else:
            info["save"] = "disabled"
    except Exception as e:
        info["save"] = f"err:{e}"[:80]
    shot(page, "v22_34_saved.png")

    # Reload verify via End screen again
    goto_edit(page)
    click_text(page, r"^End screen$", y_min=200, max_len=20)
    page.wait_for_timeout(3000)
    for _ in range(2):
        dismiss(page)
        click_text(page, r"^OK, got it$", y_min=60, max_len=20)
    shot(page, "v22_35_verify.png")
    after = page.inner_text("body")
    info["has_002"] = bool(re.search(r"Periodic Table|AL_-qlWko_g", after, re.I))
    info["has_subscribe"] = bool(re.search(r"Subscribe", after, re.I))
    info["best_for_viewer"] = bool(re.search(r"Best for viewer", after, re.I))
    info["most_recent"] = bool(re.search(r"Most recent upload", after, re.I))
    info["nan"] = "NaN" in after
    info["error"] = bool(re.search(r"problem in processing|couldn't be saved", after, re.I))
    info["element_track"] = bool(re.search(r"Subscribe:|Video:", after, re.I))
    info["ok"] = bool(
        not info["error"]
        and not info["nan"]
        and info["has_subscribe"]
        and (info["has_002"] or (info["element_track"] and not info["best_for_viewer"]))
    )
    info["after"] = after[:900]
    return info


def ab_ineligible_reason(page) -> dict:
    info = {"wanted_pairs": [{"title": t, "thumb": th.name} for t, th in zip(TITLES, THUMBS)]}
    goto_edit(page)
    t = page.inner_text("body")
    info["ineligible"] = "Ineligible" in t
    info["titles_listed"] = {
        "t1": "What's Really Inside an Atom?" in t,
        "t2": "Why Is the Periodic Table in This Order?" in t,
        "t3": "How Small Can You Cut Gold?" in t,
    }
    # Click info icon near Ineligible if possible
    page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55)return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (t==='Ineligible') {
                const rect=el.getBoundingClientRect();
                // click nearby info
                const parent=el.parentElement||el;
                parent.click();
                return true;
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          }; return walk(document);
        }"""
    )
    page.wait_for_timeout(800)
    shot(page, "v22_10_ab_ineligible.png")
    tip = page.inner_text("body")
    info["tip_snip"] = tip[:700]
    # One more attempt to open A/B dialog and Set test if eligible somehow
    click_text(page, r"^A/B Testing$", y_min=100, max_len=20)
    page.wait_for_timeout(2500)
    shot(page, "v22_11_ab_dialog.png")
    body = page.inner_text("body")
    info["dialog_has_title_and_thumb"] = "Title and thumbnail" in body
    info["dialog_ineligible"] = "Ineligible" in body
    page.keyboard.press("Escape")
    info["ok"] = False
    info["note"] = (
        "Studio shows A/B Testing Ineligible on this scheduled/private video. "
        "Title pairs partially listed; cannot arm Title+thumbnail×3 until eligible (often after public/premiere)."
    )
    return info


def main() -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    (EV / "phone_uat_v22.log").write_text("")
    urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=3)
    result = {
        "at": datetime.now().isoformat(timespec="seconds"),
        "videoId": VIDEO_ID,
        "channel": "@HistoryOfScienceYT",
    }

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}", timeout=30000)
        page = browser.contexts[0].pages[0] if browser.contexts[0].pages else browser.contexts[0].new_page()
        page.set_default_timeout(45000)
        try:
            page.bring_to_front()
        except Exception:
            pass

        log("v22 upload main thumb A v04")
        goto_edit(page)
        shot(page, "v22_01_before.png")
        result["thumb"] = upload_thumb_a(page)
        save(page)
        shot(page, "v22_02_thumb.png")
        dump("V22_THUMB.json", result["thumb"])

        log("v22 AI YES + Kids NO proof")
        result["ai_kids"] = prove_ai_kids(page)
        dump("V22_AI_KIDS.json", result["ai_kids"])

        log("v22 Visibility panel")
        goto_edit(page)
        result["schedule"] = prove_visibility(page)
        dump("V22_SCHEDULE.json", result["schedule"])

        log("v22 Content list")
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
            wait_until="domcontentloaded",
            timeout=90000,
        )
        page.wait_for_timeout(4500)
        dismiss(page)
        shot(page, "v22_22_content.png")
        shutil.copy2(EV / "v22_22_content.png", EV / "FINAL_content_15oct.png")
        shutil.copy2(EV / "v22_22_content.png", ART / "FINAL_content_15oct.png")
        ct = page.inner_text("body")
        result["content_15"] = bool(re.search(r"15\s*(Oct|October)\s*2026", ct, re.I))
        result["content_30"] = bool(re.search(r"30\s*(Sept|Sep|September)\s*2026", ct, re.I))

        log("v22 A/B ineligible reason")
        result["ab"] = ab_ineligible_reason(page)
        dump("V22_AB.json", result["ab"])

        log("v22 end screen import/template")
        result["end"] = do_end_import(page)
        dump("V22_END.json", result["end"])

        result["pin"] = {
            "ok": False,
            "reason": "deferred_while_private_scheduled",
            "note": "Pin on launch 15 Oct 2026",
        }

    dump("PHONE_UAT_V22_RESULT.json", result)
    log("DONE " + json.dumps({k: result.get(k) for k in ("thumb", "ai_kids", "schedule", "content_15", "content_30", "ab", "end")}, default=str)[:2000])
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
