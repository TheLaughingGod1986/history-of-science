#!/usr/bin/env python3
"""CoS verify: Visibility = 15 Oct 2026 18:00 UK, Premiere UNCHECKED; thumb A; AI Yes.

CDP :9460 · @HistoryOfScienceYT only. Fixes Premiere if checked; sets schedule if wrong.
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
PROJ = Path(__file__).resolve().parents[2]
EV = PROJ / "11_Upload-Package/Schedule/evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos004_studio_phone_uat"
THUMB_A = PROJ / "08_Thumbnail/Selected/hos_004_thumb_A_atom_live_v04.jpg"


def log(m: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {m}"
    print(line, flush=True)
    with (EV / "cos_verify_v01.log").open("a") as f:
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
            page.get_by_role(
                "button",
                name=re.compile(r"^(OK, got it|Got it|Close|Dismiss|Not now)$", re.I),
            ).first.click(timeout=350)
        except Exception:
            pass


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


def save_details(page) -> bool:
    try:
        btn = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
        if btn.count() and btn.first.is_enabled():
            btn.first.click(force=True, timeout=8000)
            page.wait_for_timeout(4500)
            return True
    except Exception:
        pass
    return False


def premiere_state(page) -> dict:
    """Inspect Premiere checkbox via shadow DOM — aria-checked / checked."""
    return page.evaluate(
        """() => {
          const out={found:false, checked:null, labels:[]};
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              const aria=(el.getAttribute('aria-label')||'');
              if (/Set as (?:instant )?Premiere|Premiere/i.test(t) || /Premiere/i.test(aria)) {
                if (t && t.length<80) out.labels.push(t);
              }
              // checkbox / switch near premiere
              const role=el.getAttribute('role')||'';
              const tag=(el.tagName||'').toLowerCase();
              if ((tag==='input' && el.type==='checkbox') || role==='checkbox' || role==='switch') {
                const near=((el.getAttribute('aria-label')||'')+' '+(el.innerText||'')+' '+((el.parentElement&&el.parentElement.innerText)||'')).slice(0,200);
                if (/Premiere/i.test(near)) {
                  out.found=true;
                  const ac=el.getAttribute('aria-checked');
                  if (ac!=null) out.checked = ac==='true';
                  else if (typeof el.checked==='boolean') out.checked = el.checked;
                  out.near=near.slice(0,160);
                  out.tag=tag; out.role=role;
                }
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          };
          walk(document);
          // also paper-checkbox / ytcp
          const walk2=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-checkbox,ytcp-checkbox-lit,paper-checkbox'):[])) {
              const t=(el.innerText||el.getAttribute('aria-label')||'').trim();
              if (/Premiere/i.test(t)) {
                out.found=true;
                const ac=el.getAttribute('aria-checked')||el.getAttribute('aria-selected');
                if (ac!=null) out.checked = ac==='true';
                else out.checked = el.hasAttribute('checked') || /checked|iron-selected|selected/i.test(el.className||'');
                out.near=t.slice(0,160);
                out.tag=el.tagName;
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk2(el.shadowRoot,d+1);
            }
          };
          walk2(document);
          return out;
        }"""
    )


def uncheck_premiere(page) -> dict:
    info = {"before": premiere_state(page)}
    if info["before"].get("checked") is True or info["before"].get("checked") is None:
        # Click the Premiere label/checkbox to toggle off if checked
        hit = page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>55)return false;
                for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-checkbox,ytcp-checkbox-lit,paper-checkbox,input,[role=checkbox],*'):[])) {
                  const t=((el.innerText||'')+' '+(el.getAttribute('aria-label')||'')).trim();
                  if (!/Set as (?:instant )?Premiere/i.test(t) && !(el.innerText||'').trim().match(/^Set as (?:instant )?Premiere$/i)) {
                    // also match short
                    if (!/^Set as (?:instant )?Premiere$/i.test((el.innerText||'').trim()) && !/Premiere/i.test(el.getAttribute('aria-label')||'')) continue;
                  }
                  const rect=el.getBoundingClientRect();
                  if (rect.width<8 || rect.y<80) continue;
                  const ac=el.getAttribute('aria-checked');
                  const checked = ac==='true' || el.checked===true || el.hasAttribute('checked');
                  if (checked || ac==null) {
                    el.click();
                    return {clicked:true, was:checked, t:(el.innerText||'').trim().slice(0,60)};
                  }
                  return {clicked:false, was:false, t:(el.innerText||'').trim().slice(0,60)};
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if (el.shadowRoot) { const x=walk(el.shadowRoot,d+1); if(x) return x; }
                }
                return false;
              };
              return walk(document);
            }"""
        )
        info["click"] = hit
        page.wait_for_timeout(800)
        # If still checked, click text label
        st = premiere_state(page)
        if st.get("checked") is True:
            click_text(page, r"Set as (?:instant )?Premiere", y_min=100, max_len=50)
            page.wait_for_timeout(600)
    info["after"] = premiere_state(page)
    return info


def open_visibility_schedule(page) -> dict:
    info = {}
    # Click Scheduled / Visibility in right rail
    box = page.evaluate(
        """() => {
          const cands=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (t==='Scheduled' || t==='Visibility' || t==='Schedule') {
                const rect=el.getBoundingClientRect();
                if (rect.x>700 && rect.y>150 && rect.width>20)
                  cands.push({x:rect.x+Math.min(40,rect.width/2),y:rect.y+rect.height/2,t,y0:rect.y});
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          }; walk(document);
          cands.sort((a,b)=>(a.t==='Scheduled'?0:a.t==='Schedule'?1:2)-(b.t==='Scheduled'?0:b.t==='Schedule'?1:2)||a.y0-b.y0);
          return cands[0]||null;
        }"""
    )
    info["rail"] = box
    if box:
        page.mouse.click(box["x"], box["y"])
        page.wait_for_timeout(1500)
    # Ensure Schedule radio selected
    click_text(page, r"^Schedule$", y_min=100, max_len=20)
    page.wait_for_timeout(800)
    # Open date picker / show date row
    click_text(page, r"15 Oct 2026|15 October|Schedule date|Publish date", y_min=120, max_len=40)
    page.wait_for_timeout(600)
    return info


def ensure_date_time(page) -> dict:
    """If 15 Oct / 18:00 missing from panel, try to set them."""
    info = {}
    body = page.inner_text("body")
    info["has_15_before"] = bool(re.search(r"15\s*(Oct|October)\s*2026", body, re.I))
    info["has_1800_before"] = bool(re.search(r"18:00", body))

    if not info["has_15_before"]:
        # Try open calendar and pick 15 Oct 2026
        click_text(page, r"Schedule date|Publish date|Date", y_min=120, max_len=30)
        page.wait_for_timeout(500)
        # Type into date field if present
        filled = page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>55)return false;
                for (const inp of (r.querySelectorAll?r.querySelectorAll('input'):[])) {
                  const aria=((inp.getAttribute('aria-label')||'')+(inp.placeholder||'')).toLowerCase();
                  const rect=inp.getBoundingClientRect();
                  if (rect.y<80||rect.width<40) continue;
                  if (/date|schedule|publish/.test(aria) || inp.type==='text') {
                    // prefer date-ish
                    if (/time|hour|minute/.test(aria)) continue;
                    inp.focus(); return {aria,y:rect.y};
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                }
                return false;
              };
              return walk(document);
            }"""
        )
        info["date_field"] = filled
        if filled:
            page.keyboard.press("Meta+a")
            page.keyboard.type("15 Oct 2026", delay=20)
            page.keyboard.press("Enter")
            page.wait_for_timeout(800)

    if not info["has_1800_before"]:
        # Time field
        click_text(page, r"18:00|Schedule time|Publish time|Time", y_min=120, max_len=30)
        page.wait_for_timeout(400)
        filled = page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>55)return false;
                for (const inp of (r.querySelectorAll?r.querySelectorAll('input'):[])) {
                  const aria=((inp.getAttribute('aria-label')||'')+(inp.placeholder||'')).toLowerCase();
                  const rect=inp.getBoundingClientRect();
                  if (rect.y<80||rect.width<30) continue;
                  if (/time|hour|clock/.test(aria) || /\\d{1,2}:\\d{2}/.test(inp.value||'')) {
                    inp.focus();
                    const s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
                    s.call(inp,'18:00');
                    inp.dispatchEvent(new Event('input',{bubbles:true}));
                    inp.dispatchEvent(new Event('change',{bubbles:true}));
                    return {aria,y:rect.y,val:inp.value};
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                }
                return false;
              };
              return walk(document);
            }"""
        )
        info["time_field"] = filled
        if filled:
            page.keyboard.press("Meta+a")
            page.keyboard.type("18:00", delay=25)
            page.keyboard.press("Enter")
            page.wait_for_timeout(600)
        else:
            page.keyboard.type("18:00", delay=25)
            page.keyboard.press("Enter")
            page.wait_for_timeout(600)

    body2 = page.inner_text("body")
    info["has_15_after"] = bool(re.search(r"15\s*(Oct|October)\s*2026", body2, re.I))
    info["has_1800_after"] = bool(re.search(r"18:00", body2))
    return info


def click_visibility_done_save(page) -> dict:
    info = {}
    # Done on visibility panel
    try:
        btn = page.get_by_role("button", name=re.compile(r"^Done$", re.I))
        if btn.count() and btn.first.is_enabled():
            btn.first.click(force=True)
            info["done"] = "role"
            page.wait_for_timeout(2000)
        else:
            info["done"] = click_text(page, r"^Done$", y_min=200, max_len=10)
            page.wait_for_timeout(1500)
    except Exception as e:
        info["done_err"] = str(e)[:80]
    info["save"] = save_details(page)
    return info


def upload_thumb_a(page) -> dict:
    info = {"file": THUMB_A.name}
    for _ in range(12):
        page.mouse.wheel(0, 350)
        page.wait_for_timeout(80)
        if re.search(r"thumbnail|Upload file", page.inner_text("body"), re.I):
            break
    # Prefer Upload file chooser
    ups = page.evaluate(
        """() => {
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (t==='Upload' || t==='Upload file' || t==='Upload thumbnail') {
                const rect=el.getBoundingClientRect();
                if (rect.y>150 && rect.width>20)
                  out.push({x:rect.x+rect.width/2,y:rect.y+rect.height/2,t});
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          }; walk(document); return out;
        }"""
    )
    info["ups"] = ups[:5]
    for u in ups[:3]:
        try:
            with page.expect_file_chooser(timeout=8000) as fc:
                page.mouse.click(u["x"], u["y"])
            fc.value.set_files(str(THUMB_A))
            info["via"] = f"chooser:{u['t']}"
            info["ok"] = True
            page.wait_for_timeout(4000)
            break
        except Exception as e:
            info.setdefault("errs", []).append(str(e)[:80])
            dismiss(page)
    if not info.get("ok"):
        loc = page.locator('input[type="file"]')
        for i in range(loc.count()):
            acc = (loc.nth(i).get_attribute("accept") or "").lower()
            if "image" in acc or "jpg" in acc or "png" in acc:
                try:
                    loc.nth(i).set_input_files(str(THUMB_A))
                    info["via"] = f"input[{i}]"
                    info["ok"] = True
                    page.wait_for_timeout(4000)
                    break
                except Exception:
                    continue
    info["saved"] = save_details(page)
    # Retry toast
    for _ in range(8):
        t = page.inner_text("body")
        if "trouble saving" in t.lower() or "retrying" in t.lower():
            try:
                page.get_by_text("Retry", exact=True).first.click(timeout=800)
            except Exception:
                pass
            page.wait_for_timeout(4000)
        else:
            break
    return info


def ensure_ai_yes(page) -> dict:
    info = {}
    for _ in range(28):
        t = page.inner_text("body")
        if re.search(r"AI use|Was AI used|Altered content", t, re.I):
            break
        click_text(page, r"^Show more$", y_min=100, max_len=20)
        page.mouse.wheel(0, 600)
        page.wait_for_timeout(140)
    hit = page.evaluate(
        """() => {
          let aiY=null;
          const find=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/^AI use$/i.test(t)||/Was AI used/i.test(t)||/^Altered content$/i.test(t)) {
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
    info["hit"] = hit
    page.wait_for_timeout(400)
    info["saved"] = save_details(page)
    goto_edit(page)
    for _ in range(28):
        t = page.inner_text("body")
        if re.search(r"AI use|Was AI used", t, re.I):
            break
        click_text(page, r"^Show more$", y_min=100, max_len=20)
        page.mouse.wheel(0, 600)
        page.wait_for_timeout(120)
    page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55)return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (/^AI use$/i.test((el.innerText||'').trim())) { el.scrollIntoView({block:'center'}); return true; }
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          }; return walk(document);
        }"""
    )
    page.wait_for_timeout(400)
    shot(page, "cos_v01_ai_yes.png")
    tb = page.inner_text("body")
    info["ai_yes"] = bool(re.search(r"Yes, AI was used|AI use[\\s\\S]{0,500}Yes", tb, re.I))
    # Prefer selected radio near AI
    info["ai_radio"] = page.evaluate(
        """() => {
          let aiY=null;
          const find=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (/^AI use$/i.test((el.innerText||'').trim())) {
                const rect=el.getBoundingClientRect(); if(rect.y>80) aiY=rect.y;
              }
              if (el.shadowRoot) find(el.shadowRoot,d+1);
            }
          }; find(document);
          const radios=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=radio],input[type=radio]'):[])) {
              const rect=el.getBoundingClientRect();
              if (aiY!=null && rect.y>aiY && rect.y<aiY+500) {
                radios.push({
                  t:((el.getAttribute('aria-label')||'')+' '+(el.innerText||'')).trim().slice(0,40),
                  checked: el.getAttribute('aria-checked')==='true' || el.checked===true,
                  y:rect.y
                });
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          }; walk(document);
          return {aiY,radios};
        }"""
    )
    return info


def main() -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    (EV / "cos_verify_v01.log").write_text("")
    urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=3)
    result = {
        "at": datetime.now().isoformat(timespec="seconds"),
        "videoId": VIDEO_ID,
        "note": "CoS: Visibility 15 Oct 18:00 Premiere OFF; thumb A; AI Yes",
    }

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}", timeout=30000)
        page = browser.contexts[0].pages[0] if browser.contexts[0].pages else browser.contexts[0].new_page()
        page.set_default_timeout(45000)
        try:
            page.bring_to_front()
        except Exception:
            pass

        log("cos open edit + Visibility")
        goto_edit(page)
        shot(page, "cos_v01_01_details.png")
        result["open"] = open_visibility_schedule(page)
        shot(page, "cos_v01_02_visibility_open.png")

        log("cos ensure date/time + Premiere OFF")
        result["datetime"] = ensure_date_time(page)
        result["premiere"] = uncheck_premiere(page)
        # If premiere still checked, click again
        if result["premiere"].get("after", {}).get("checked") is True:
            click_text(page, r"Set as (?:instant )?Premiere", y_min=100, max_len=50)
            page.wait_for_timeout(500)
            result["premiere"]["after2"] = premiere_state(page)

        shot(page, "cos_v01_03_visibility_panel.png")
        # Also alias as FINAL CoS proof
        shutil.copy2(EV / "cos_v01_03_visibility_panel.png", EV / "COS_visibility_15oct_1800_premiere_off.png")
        shutil.copy2(EV / "cos_v01_03_visibility_panel.png", ART / "COS_visibility_15oct_1800_premiere_off.png")
        shutil.copy2(EV / "cos_v01_03_visibility_panel.png", EV / "FINAL_visibility_panel_15oct_1800.png")
        shutil.copy2(EV / "cos_v01_03_visibility_panel.png", ART / "FINAL_visibility_panel_15oct_1800.png")

        vt = page.inner_text("body")
        prem = premiere_state(page)
        result["visibility"] = {
            "has_15": bool(re.search(r"15\s*(Oct|October)\s*2026", vt, re.I)),
            "has_1800": bool(re.search(r"18:00", vt)),
            "has_30": bool(re.search(r"30\s*(Sept|Sep|September)\s*2026", vt, re.I)),
            "premiere_checkbox": prem,
            "premiere_off": prem.get("checked") is False,
            "snip": vt[:1200],
        }
        result["visibility_save"] = click_visibility_done_save(page)

        # Re-open Visibility for clean proof after save
        goto_edit(page)
        open_visibility_schedule(page)
        page.wait_for_timeout(1000)
        shot(page, "cos_v01_04_visibility_reopen.png")
        shutil.copy2(EV / "cos_v01_04_visibility_reopen.png", EV / "COS_visibility_15oct_1800_premiere_off.png")
        shutil.copy2(EV / "cos_v01_04_visibility_reopen.png", ART / "COS_visibility_15oct_1800_premiere_off.png")
        shutil.copy2(EV / "cos_v01_04_visibility_reopen.png", EV / "FINAL_visibility_panel_15oct_1800.png")
        shutil.copy2(EV / "cos_v01_04_visibility_reopen.png", ART / "FINAL_visibility_panel_15oct_1800.png")
        vt2 = page.inner_text("body")
        prem2 = premiere_state(page)
        result["visibility_reopen"] = {
            "has_15": bool(re.search(r"15\s*(Oct|October)\s*2026", vt2, re.I)),
            "has_1800": bool(re.search(r"18:00", vt2)),
            "has_30": bool(re.search(r"30\s*(Sept|Sep|September)\s*2026", vt2, re.I)),
            "premiere_checkbox": prem2,
            "premiere_off": prem2.get("checked") is False,
            "ok": bool(
                re.search(r"15\s*(Oct|October)\s*2026", vt2, re.I)
                and re.search(r"18:00", vt2)
                and not re.search(r"30\s*(Sept|Sep|September)\s*2026", vt2, re.I)
                and prem2.get("checked") is False
            ),
        }

        log("cos thumb A v04")
        page.keyboard.press("Escape")
        page.wait_for_timeout(400)
        goto_edit(page)
        result["thumb"] = upload_thumb_a(page)
        shot(page, "cos_v01_05_thumb.png")
        goto_edit(page)
        shot(page, "cos_v01_06_thumb_reload.png")
        t = page.inner_text("body")
        # Visual: Hidden Number text is often not in DOM — rely on screenshot + heuristic
        result["thumb"]["dom_hidden_number"] = bool(re.search(r"HIDDEN NUMBER|THE HIDDEN", t, re.I))

        log("cos AI Yes")
        result["ai"] = ensure_ai_yes(page)
        shutil.copy2(EV / "cos_v01_ai_yes.png", EV / "FINAL_ai_use_yes.png")
        shutil.copy2(EV / "cos_v01_ai_yes.png", ART / "FINAL_ai_use_yes.png")

        result["ok"] = bool(
            result["visibility_reopen"].get("ok")
            and result["ai"].get("ai_yes")
        )

    dump("COS_VERIFY_V01_RESULT.json", result)
    log("DONE " + json.dumps({k: result.get(k) for k in ("visibility_reopen", "premiere", "thumb", "ai", "ok")}, default=str)[:2000])
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
