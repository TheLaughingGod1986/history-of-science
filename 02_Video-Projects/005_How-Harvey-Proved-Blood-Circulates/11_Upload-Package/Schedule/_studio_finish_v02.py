#!/usr/bin/env python3
"""HOS 005 v02 Studio finish on wwcjcFfC-5M. One setting per save; Audience+Visibility re-read."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
import importlib.util as iu

_s = iu.spec_from_file_location("step", HERE / "_studio_step_v01.py")
step = iu.module_from_spec(_s)
_s.loader.exec_module(step)

_e = iu.spec_from_file_location("es", HERE / "_es_lib_v01.py")
es = iu.module_from_spec(_e)
_e.loader.exec_module(es)

VID = step.VID  # wwcjcFfC-5M
HOS = step.HOS
ART = step.ART
OUT = step.OUT
LONDON = ZoneInfo("Europe/London")
FILM = HERE.parents[1]
THUMB_B = FILM / "08_Thumbnail/Selected/hos_005_thumb_B_it_goes_round_v02.jpg"
THUMB_B_SHA = "17672532bf5d6f5f9f62205e75c5dc2b744b93d40139df3d3f0204872deb9c6a"
GERMS = "_C92tIJCk8A"
TITLE = "The Tied Arm That Proved Your Blood Circulates"

OUT.mkdir(parents=True, exist_ok=True)
ART.mkdir(parents=True, exist_ok=True)
LOG = []


def log(msg, **kw):
    row = {"at": datetime.now(LONDON).isoformat(timespec="seconds"), "msg": msg, **kw}
    LOG.append(row)
    print(json.dumps(row, ensure_ascii=False, default=str)[:2500], flush=True)


def av_ok(a):
    return a.get("chip") == "Visibility Scheduled" and a.get("not_kids") and not a.get("kids_yes")


def save_check(page, label):
    s = step.u.page_save(page)
    page.wait_for_timeout(3500)
    a = step.sw.av(page, step.u)
    r = {"label": label, "save": s, "visibility": a.get("chip"), "not_kids": a.get("not_kids"), "kids_yes": a.get("kids_yes")}
    log("SAVE", **r)
    if not av_ok(a):
        raise SystemExit(f"STOP after {label}: {a}")
    return r


def shot(page, name):
    p = step.shot(page, name)
    log("shot", path=p)
    return p


def ensure_show_more(page):
    step.sw.show_more(page)
    for _ in range(20):
        body = page.inner_text("body")
        if re.search(r"Altered content|AI was used|AI wasn't used|Paid promotion|Caption certification", body, re.I):
            break
        page.mouse.wheel(0, 800)
        page.wait_for_timeout(80)


def click_ai_yes(page):
    return page.evaluate(
        """() => {
          let hit=null;
          const walk=(r,d=0)=>{
            if(!r||d>60||hit) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('[role=radio],input[type=radio],tp-yt-paper-radio-button,[aria-checked]')
              : [])) {
              const al=(el.getAttribute('aria-label')||'').trim();
              let own=(el.innerText||'').trim().replace(/\\s+/g,' ');
              if (!own) {
                const fs=el.querySelector && el.querySelector('yt-formatted-string, .label, span');
                if (fs) own=(fs.innerText||'').trim().replace(/\\s+/g,' ');
              }
              const blob=(al+' '+own).toLowerCase();
              // Must be AI/altered Yes — never kids Yes / paid Yes
              if (/made for kids|paid promotion|contains paid/.test(blob)) continue;
              if (/(yes,?\\s*ai was used|altered or synthetic.*yes|^yes\\b.*ai|ai was used)/i.test(blob)
                  || (/^yes/i.test(own) && /ai|altered|synthetic/i.test(al+own))) {
                const rect=el.getBoundingClientRect();
                if (rect.width<2||rect.height<2) continue;
                el.click();
                hit={al:al.slice(0,80), own:own.slice(0,80), x:rect.x, y:rect.y};
                return;
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot, d+1);
          };
          walk(document); return hit;
        }"""
    )


def do_altered(page):
    ensure_show_more(page)
    ai0 = step.sw.read_ai(page)
    log("ai_before", ai=ai0)
    if ai0.get("yes"):
        log("altered_already_yes")
        shot(page, "altered_already")
        return {"already": True, "ai": ai0}
    # scroll to altered
    for _ in range(25):
        body = page.inner_text("body")
        if re.search(r"Altered content|altered or synthetic", body, re.I):
            break
        page.keyboard.press("PageDown")
        page.wait_for_timeout(100)
    hit = click_ai_yes(page)
    log("altered_click", hit=hit)
    page.wait_for_timeout(800)
    shot(page, "altered_clicked")
    if not hit:
        raise SystemExit("could not find Altered Yes radio")
    save_check(page, "altered")
    ai1 = step.sw.read_ai(page)
    log("ai_after", ai=ai1)
    shot(page, "altered_saved")
    return {"hit": hit, "ai": ai1}


def do_settings(page):
    # Reuse _studio_settings_v01 commit path by importing
    spec = iu.spec_from_file_location("settings", HERE / "_studio_settings_v01.py")
    settings = iu.module_from_spec(spec)
    spec.loader.exec_module(settings)
    settings.prep(page)
    results = []
    # paid promotion No — click No if needed
    # Use settings module steps that exist: caption, type, england, places, moderation
    # First: paid promotion No via evaluate
    paid = page.evaluate(
        """() => {
          let hit=null;
          const walk=(r,d=0)=>{
            if(!r||d>55||hit) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=radio],tp-yt-paper-radio-button'):[])) {
              const al=(el.getAttribute('aria-label')||'').toLowerCase();
              const own=(el.innerText||'').trim().toLowerCase();
              const blob=al+' '+own;
              if (!/paid promotion|contains paid|paid product/.test(blob) && !(/\\bno\\b/.test(own) && d<3)) {
                // look for nearby paid context via parent text
              }
            }
            // Better: find section then No
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/^Paid promotion$/i.test(t) || /My video contains paid promotion/i.test(t)) {
                // walk siblings for No radio
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot) walk(el.shadowRoot,d+1);
          };
          // Direct: aria-label containing paid + No
          const walk2=(r,d=0)=>{
            if(!r||d>60||hit) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=radio],tp-yt-paper-radio-button'):[])) {
              const al=(el.getAttribute('aria-label')||'');
              if (/paid promotion/i.test(al) && /\\bno\\b/i.test(al)) {
                el.click(); hit={al:al.slice(0,100)}; return;
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot) walk2(el.shadowRoot,d+1);
          };
          walk2(document); return hit;
        }"""
    )
    log("paid_click", hit=paid)
    if paid:
        page.wait_for_timeout(500)
        results.append(save_check(page, "paid_no"))

    # caption certification
    for key in ("caption", "type", "moderation"):
        try:
            r = settings.do_dropdown(page, key)
            log("dropdown", key=key, r=r)
            if r and not r.get("already"):
                results.append(save_check(page, key))
            elif r and r.get("already"):
                log("already", key=key, before=r.get("already"))
        except Exception as e:
            log("dropdown_err", key=key, err=str(e))
            raise

    # england academic system
    try:
        eng = settings.eng
        # open Academic system / England via known helper if present
        if hasattr(eng, "set_england"):
            eng.set_england(page)
            results.append(save_check(page, "england"))
        else:
            # fallback click England
            hit = page.evaluate(step.ts.CLICK_JS, "England") if hasattr(step, "ts") else None
            # use settings list path
            settings.prep(page)
            # try open Academic system dropdown
            before = settings.trigger_text(page, r"Academic system|Education system|Country")
            log("academic_before", before=before)
            if before and re.search(r"England", before or "", re.I):
                log("england_already")
            else:
                opts = settings.open_list(page, r"^Academic system|^Education|^Country")
                log("academic_opts", opts=(opts or [])[:20])
                pick = next((o for o in (opts or []) if re.search(r"England", o, re.I)), None)
                if pick:
                    page.evaluate(step.ts.CLICK_JS, pick)
                    page.wait_for_timeout(800)
                    results.append(save_check(page, "england"))
    except Exception as e:
        log("england_err", err=str(e)[:400])

    # places Off
    try:
        places = page.evaluate(
            """() => {
              let hit=null;
              const walk=(r,d=0)=>{
                if(!r||d>60||hit) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('[role=switch],tp-yt-paper-toggle-button,button'):[])) {
                  const al=(el.getAttribute('aria-label')||'');
                  const t=(el.innerText||'');
                  if (/automatic places|places/i.test(al+t)) {
                    const pressed=el.getAttribute('aria-checked')||el.getAttribute('aria-pressed');
                    hit={al:al.slice(0,80), pressed, tag:el.tagName};
                    if (pressed==='true' || /on/i.test(pressed||'')) { el.click(); hit.clicked=true; }
                    return;
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot) walk(el.shadowRoot,d+1);
              }; walk(document); return hit;
            }"""
        )
        log("places", hit=places)
        if places and places.get("clicked"):
            results.append(save_check(page, "places_off"))
    except Exception as e:
        log("places_err", err=str(e)[:300])

    shot(page, "settings_done")
    return results


def do_tc(page):
    assert hashlib.sha256(THUMB_B.read_bytes()).hexdigest() == THUMB_B_SHA
    # Undo any dirty first
    page.evaluate(step.ts.CLICK_JS, "Undo changes")
    page.wait_for_timeout(1000)
    # Open A/B Testing
    opened = page.evaluate(step.ts.CLICK_JS, "A/B Testing")
    log("tc_open", opened=opened)
    page.wait_for_timeout(2500)
    shot(page, "tc_01_open")
    # Thumbnail only mode
    page.evaluate(step.ts.CLICK_JS, "Thumbnail")
    page.wait_for_timeout(1000)
    # Or "Thumbnails" / mode radios
    page.evaluate(
        """() => {
          let hit=null;
          const walk=(r,d=0)=>{
            if(!r||d>55||hit) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/^Thumbnail only$/i.test(t) || /^Thumbnails$/i.test(t)) {
                const b=el.getBoundingClientRect();
                if (b.width>4) { el.click(); hit=t; return; }
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return hit;
        }"""
    )
    page.wait_for_timeout(1000)
    shot(page, "tc_02_mode")
    # Upload B as second thumb — look for file input / Add
    # Use file chooser on "Add" or second slot
    inputs = page.locator('input[type=file]')
    log("file_inputs", count=inputs.count())
    # Try clicking Add thumbnail / upload in dialog
    # Fallback: use existing TC script logic by importing after page is open
    # Simpler approach: run the existing _studio_tc_v01 with page already on edit —
    # actually call its internals mid-flight is hard. Replicate key upload:
    uploaded = False
    for sel in ['input[type=file]', 'input[accept*="image"]']:
        loc = page.locator(sel)
        n = loc.count()
        for i in range(n):
            try:
                loc.nth(i).set_input_files(str(THUMB_B))
                uploaded = True
                log("tc_uploaded_b", i=i, sel=sel)
                page.wait_for_timeout(2000)
                break
            except Exception as e:
                log("tc_upload_try", i=i, err=str(e)[:120])
        if uploaded:
            break
    shot(page, "tc_03_filled")
    # Set test
    for label in ("Set test", "Save", "Done"):
        if page.get_by_role("button", name=label, exact=True).filter(visible=True).count():
            page.get_by_role("button", name=label, exact=True).filter(visible=True).first.click(timeout=8000)
            page.wait_for_timeout(2000)
            log("tc_btn", label=label)
            break
    shot(page, "tc_04_set")
    # Page Save
    save_check(page, "tc")
    shot(page, "tc_05_saved")
    return {"uploaded_b": uploaded}


def do_endscreen(page):
    # Close dialogs
    for _ in range(3):
        page.keyboard.press("Escape")
        page.wait_for_timeout(150)
    # Open End screen
    hit = es.click(page, "End screen", wait=3000)
    if not hit:
        # try via evaluate exact
        hit = page.evaluate(step.ts.CLICK_JS, "End screen")
        page.wait_for_timeout(3000)
    log("es_open", hit=hit)
    shot(page, "es_01_open")
    body = page.inner_text("body")
    if re.search(r"Oops, something went wrong", body, re.I):
        raise SystemExit("End screen Oops")
    # Template
    t = None
    for pat in ("1 video, 1 subscribe", "1 video, 1 Subscribe"):
        t = es.click(page, pat, wait=2000)
        if t:
            break
    if not t:
        page.evaluate(
            """() => {
              let hit=null;
              const walk=(r,d=0)=>{
                if(!r||d>55||hit) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  const txt=(el.innerText||'').trim().replace(/\\s+/g,' ');
                  if (/1 video,?\\s*1 subscribe/i.test(txt) && txt.length<40) {
                    el.click(); hit=txt; return;
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot) walk(el.shadowRoot,d+1);
              }; walk(document); return hit;
            }"""
        )
        page.wait_for_timeout(2000)
    log("es_template", t=t)
    shot(page, "es_02_template")
    # Specific video
    es.click(page, "Most recent upload", wait=600) or es.click(page, "Best for viewer", wait=600)
    page.wait_for_timeout(400)
    s = es.click(page, "Specific video", wait=1000)
    log("es_specific", s=s)
    shot(page, "es_03_specific")
    # Search germs id
    filled = page.evaluate(
        """(q) => {
          let hit=null;
          const walk=(r,d=0)=>{
            if(!r||d>55||hit) return;
            for (const inp of (r.querySelectorAll?r.querySelectorAll('input,textarea'):[])) {
              const aria=((inp.getAttribute('aria-label')||'')+(inp.placeholder||'')).toLowerCase();
              const rect=inp.getBoundingClientRect();
              if (rect.width<40||rect.y<50) continue;
              if (/search|video|url|paste/.test(aria) || inp.type==='search' || inp.type==='text') {
                inp.focus();
                const proto = inp.tagName==='TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
                Object.getOwnPropertyDescriptor(proto,'value').set.call(inp, q);
                inp.dispatchEvent(new Event('input',{bubbles:true}));
                hit={aria:aria.slice(0,60), y:Math.round(rect.y)};
                return;
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot) walk(el.shadowRoot,d+1);
          };
          walk(document); return hit;
        }""",
        GERMS,
    )
    log("es_filled", filled=filled)
    page.wait_for_timeout(300)
    page.keyboard.press("Enter")
    page.wait_for_timeout(2500)
    shot(page, "es_04_search")
    # Pick Germs title
    picked = page.evaluate(
        """() => {
          let hit=null;
          const walk=(r,d=0)=>{
            if(!r||d>55||hit) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/How Did We Discover Germs/i.test(t) && t.length<120) {
                const b=el.getBoundingClientRect();
                if (b.width>20 && b.y>60) { el.click(); hit={t:t.slice(0,90),y:b.y}; return; }
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return hit;
        }"""
    )
    log("es_picked", picked=picked)
    page.wait_for_timeout(1500)
    shot(page, "es_05_picked")
    # Save end screen
    for label in ("Save", "Done"):
        btn = page.get_by_role("button", name=label, exact=True).filter(visible=True)
        if btn.count():
            btn.first.click(timeout=8000)
            page.wait_for_timeout(3000)
            log("es_save_btn", label=label)
            break
    shot(page, "es_06_saved")
    # Back to details if needed
    if "endscreen" in page.url or "end_screen" in page.url:
        page.goto(f"https://studio.youtube.com/video/{VID}/edit", wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(4000)
        step.u.dismiss(page)
    a = step.sw.av(page, step.u)
    log("es_av", av=a)
    if not av_ok(a):
        raise SystemExit(f"STOP after endscreen: {a}")
    shot(page, "es_07_verify")
    return {"picked": picked, "germs": GERMS}


def scroll_visibility(page):
    # Open visibility panel / screenshot schedule
    page.evaluate(step.ts.CLICK_JS, "Visibility Scheduled") or page.evaluate(step.ts.CLICK_JS, "Visibility")
    page.wait_for_timeout(2000)
    shot(page, "visibility_schedule")
    # Premiere OFF check via body
    body = page.inner_text("body")
    premiere = bool(re.search(r"Premiere", body, re.I))
    log("visibility_panel", premiere_mentioned=premiere, snip=body[-800:])
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else "all"
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(step.CDP, timeout=60000)
        page = step.page_for(browser)
        page.set_default_timeout(60000)
        # Ensure live page
        if VID not in page.url or len(page.inner_text("body")) < 200:
            # close dead and reopen
            page.goto(f"https://studio.youtube.com/video/{VID}/edit", wait_until="domcontentloaded", timeout=120000)
            page.wait_for_timeout(4000)
        # Soft HOS check — avoid ensure_hos navigate which can ERR_ABORT on single-tab Studio.
        body0 = page.inner_text("body")
        url0 = page.url
        hos_ok = ("History of Science" in body0) or ("UCXp7HkBIl1LgaznXuZHJyRg" in url0) or ("studio.youtube.com" in url0 and VID in url0)
        # Confirm via channel switcher / header if present
        if "Orbit" in body0 and "History of Science" not in body0:
            raise SystemExit("WRONG CHANNEL suspected (Orbit text without HOS)")
        log("hos_ok", hos={"ok": hos_ok, "url": url0, "has_hos_name": "History of Science" in body0})
        if not hos_ok:
            raise SystemExit("not HOS")
        step.u.dismiss(page)
        step.sw.show_more(page)
        shot(page, "00_start")
        a0 = step.sw.av(page, step.u)
        log("av_start", av=a0)
        if not av_ok(a0):
            raise SystemExit(f"bad start AV {a0}")

        if only in ("all", "altered"):
            do_altered(page)
        if only in ("all", "settings"):
            do_settings(page)
        if only in ("all", "tc"):
            do_tc(page)
        if only in ("all", "endscreen"):
            do_endscreen(page)
        if only in ("all", "visibility"):
            scroll_visibility(page)

        # final shots
        page.goto(f"https://studio.youtube.com/video/{VID}/edit", wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(4000)
        step.u.dismiss(page)
        step.sw.show_more(page)
        a = step.sw.av(page, step.u)
        ai = step.sw.read_ai(page)
        log("final", av=a, ai=ai)
        shot(page, "final_details")
        scroll_visibility(page)

    out_path = OUT / "STUDIO_FINISH_V02_RESULT.json"
    out_path.write_text(json.dumps({"vid": VID, "log": LOG}, indent=2, default=str) + "\n")
    print("WROTE", out_path)


if __name__ == "__main__":
    main()
