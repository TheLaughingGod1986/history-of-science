#!/usr/bin/env python3
"""T&C + end screen for wwcjcFfC-5M. Starts Chrome in new session so it survives."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import time
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright
import importlib.util as iu

PORT = 9460
CDP = f"http://127.0.0.1:{PORT}"
PROFILE = str(Path.home() / ".hos-chrome-youtube-studio")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HOS = "UCXp7HkBIl1LgaznXuZHJyRg"
VID = "wwcjcFfC-5M"
GERMS = "_C92tIJCk8A"
TITLE = "The Tied Arm That Proved Your Blood Circulates"
HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
THUMB_B = FILM / "08_Thumbnail/Selected/hos_005_thumb_B_it_goes_round_v02.jpg"
THUMB_B_SHA = "17672532bf5d6f5f9f62205e75c5dc2b744b93d40139df3d3f0204872deb9c6a"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/DESK_2026-10-03_005_v02_upload"
OUT = FILM / "11_Upload-Package/evidence_2026-10-03_v02_studio"
LONDON = ZoneInfo("Europe/London")
ART.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
log = []


def L(msg, **kw):
    row = {"at": datetime.now(LONDON).isoformat(timespec="seconds"), "msg": msg, **kw}
    log.append(row)
    print(json.dumps(row, default=str)[:2200], flush=True)


def ensure_chrome():
    try:
        urllib.request.urlopen(f"{CDP}/json/version", timeout=2).read()
        L("CDP_UP")
        return
    except Exception:
        pass
    for name in ("SingletonLock", "SingletonSocket", "SingletonCookie"):
        p = Path(PROFILE) / name
        if p.exists():
            try:
                p.unlink()
            except Exception:
                pass
    subprocess.Popen(
        [
            CHROME,
            f"--remote-debugging-port={PORT}",
            "--remote-allow-origins=*",
            f"--user-data-dir={PROFILE}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-background-timer-throttling",
            "--disable-renderer-backgrounding",
            f"https://studio.youtube.com/channel/{HOS}",
        ],
        stdout=open("/tmp/hos_chrome_9460_tc_es.log", "w"),
        stderr=subprocess.STDOUT,
        start_new_session=True,  # survive shell process-group kill
    )
    for i in range(60):
        time.sleep(0.4)
        try:
            urllib.request.urlopen(f"{CDP}/json/version", timeout=1).read()
            L("CDP_STARTED", i=i)
            return
        except Exception:
            pass
    raise SystemExit("chrome_failed")


def load_step():
    _s = iu.spec_from_file_location("step", HERE / "_studio_step_v01.py")
    step = iu.module_from_spec(_s)
    _s.loader.exec_module(step)
    return step


def av_ok(a):
    return a.get("chip") == "Visibility Scheduled" and a.get("not_kids") and not a.get("kids_yes")


def main():
    assert hashlib.sha256(THUMB_B.read_bytes()).hexdigest() == THUMB_B_SHA
    ensure_chrome()
    step = load_step()

    def save_check(page, label):
        s = step.u.page_save(page)
        page.wait_for_timeout(3500)
        a = step.sw.av(page, step.u)
        r = {"label": label, "save": s, "visibility": a.get("chip"), "not_kids": a.get("not_kids"), "kids_yes": a.get("kids_yes")}
        L("SAVE", **r)
        if not av_ok(a):
            raise SystemExit(f"STOP {label} {a}")
        return r

    def shot(page, name):
        p = ART / f"{name}.png"
        page.screenshot(path=str(p))
        L("shot", path=str(p))
        return str(p)

    def click_btn(page, name):
        loc = page.get_by_role("button", name=name, exact=True).filter(visible=True)
        if loc.count() == 0:
            return False
        loc.first.click(timeout=8000)
        page.wait_for_timeout(2500)
        return True

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP, timeout=60000)
        page = browser.contexts[0].pages[0] if browser.contexts[0].pages else browser.contexts[0].new_page()
        page.set_default_timeout(60000)
        page.goto(f"https://studio.youtube.com/video/{VID}/edit", wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(4500)
        step.u.dismiss(page)
        body = page.inner_text("body")
        if "History of Science" not in body:
            raise SystemExit("not HOS")
        step.sw.show_more(page)
        a0 = step.sw.av(page, step.u)
        L("av0", av=a0)
        if not av_ok(a0):
            raise SystemExit(f"bad av {a0}")
        shot(page, "tces_00_start")

        # --- Test & Compare (mirror _studio_tc_v01) ---
        page.evaluate(step.ts.CLICK_JS, "Undo changes")
        page.wait_for_timeout(1200)
        page.evaluate("window.scrollTo(0,0)")
        if not click_btn(page, "A/B Testing"):
            page.evaluate(step.ts.CLICK_JS, "A/B Testing")
            page.wait_for_timeout(2500)
        if click_btn(page, "New test"):
            click_btn(page, "Continue")
        page.locator("ytcp-chip").filter(has_text="Thumbnail only").first.click()
        page.wait_for_timeout(2000)
        shot(page, "tc_mode")
        with page.expect_file_chooser(timeout=15000) as fc:
            page.locator('[aria-label="Upload thumbnail 2"]').first.click()
        fc.value.set_files(str(THUMB_B))
        page.wait_for_timeout(8000)
        dom = page.evaluate(step.ts.DOM_JS)
        # DOM_JS may return list or dict
        items = dom if isinstance(dom, list) else (dom.get("items") or dom.get("nodes") or [])
        uploaded = [d.get("aria", "") for d in items if isinstance(d, dict) and str(d.get("aria", "")).startswith("Uploaded thumbnail")]
        left = [d.get("aria", "") for d in items if isinstance(d, dict) and str(d.get("aria", "")).startswith("Upload thumbnail")]
        # fallback scan
        if not uploaded and not left:
            body_aria = page.evaluate("""() => {
              const out=[];
              const walk=(r,d=0)=>{
                if(!r||d>55) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('[aria-label]'):[])) {
                  const a=el.getAttribute('aria-label')||'';
                  if (/thumbnail/i.test(a)) out.push(a);
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,d+1);
              }; walk(document); return out;
            }""")
            L("tc_aria_scan", aria=body_aria)
            uploaded = [a for a in body_aria if a.startswith("Uploaded thumbnail")]
            left = [a for a in body_aria if a.startswith("Upload thumbnail")]
        set_btn = page.get_by_role("button", name="Set test", exact=True).filter(visible=True).first
        set_enabled = set_btn.evaluate("el => !(el.disabled || el.getAttribute('aria-disabled')==='true')")
        ready = "Thumbnail test ready" in page.inner_text("body")
        title_ok = TITLE in page.inner_text("body")
        L("tc_state", uploaded=uploaded, left=left, set_enabled=set_enabled, ready=ready, title_ok=title_ok)
        shot(page, "tc_filled")
        ok = set_enabled and ready and title_ok and "Upload thumbnail 2" not in left
        if not ok:
            raise SystemExit(f"TC setup not ready: {json.dumps(dict(uploaded=uploaded,left=left,set_enabled=set_enabled,ready=ready))}")
        set_btn.click()
        page.wait_for_timeout(3000)
        shot(page, "tc_set")
        save_check(page, "tc")
        page.goto(f"https://studio.youtube.com/video/{VID}/edit", wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(4500)
        step.u.dismiss(page)
        a = step.sw.av(page, step.u)
        L("tc_reopen_av", av=a)
        if not av_ok(a):
            raise SystemExit(f"STOP tc reopen {a}")
        page.evaluate("window.scrollTo(0,0)")
        click_btn(page, "A/B Testing")
        shot(page, "tc_verify")
        vbody = page.inner_text("body")
        L("tc_verify", snip=vbody[-1500:])
        if re.search(r"Run a new test", vbody, re.I):
            page.evaluate(step.ts.CLICK_JS, "Cancel")
            page.wait_for_timeout(600)
            L("tc_cancel_new")
        page.keyboard.press("Escape")
        page.wait_for_timeout(1000)

        # --- End screen ---
        for _ in range(3):
            page.keyboard.press("Escape")
            page.wait_for_timeout(120)
        page.evaluate(step.ts.CLICK_JS, "End screen")
        page.wait_for_timeout(3500)
        shot(page, "es_01_open")
        if re.search(r"Oops", page.inner_text("body"), re.I):
            raise SystemExit("End screen Oops")
        page.evaluate("""() => {
          let hit=null; const walk=(r,d=0)=>{
            if(!r||d>55||hit) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim().replace(/\\s+/g,' ');
              if (/1 video,?\\s*1 subscribe/i.test(t) && t.length<50) {
                const b=el.getBoundingClientRect(); if(b.width>10){el.click(); hit=t; return;}
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return hit;
        }""")
        page.wait_for_timeout(2000)
        shot(page, "es_02_template")
        page.evaluate("""() => {
          let hit=null; const walk=(r,d=0)=>{
            if(!r||d>55||hit) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/Most recent upload|Best for viewer/i.test(t) && t.length<40){el.click(); hit=t; return;}
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return hit;
        }""")
        page.wait_for_timeout(500)
        page.evaluate("""() => {
          let hit=null; const walk=(r,d=0)=>{
            if(!r||d>55||hit) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/^Specific video$/i.test(t)){el.click(); hit=t; return;}
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return hit;
        }""")
        page.wait_for_timeout(1000)
        shot(page, "es_03_specific")
        filled = page.evaluate("""(q)=>{
          let hit=null; const walk=(r,d=0)=>{
            if(!r||d>55||hit) return;
            for (const inp of (r.querySelectorAll?r.querySelectorAll('input,textarea'):[])) {
              const aria=((inp.getAttribute('aria-label')||'')+(inp.placeholder||'')).toLowerCase();
              const rect=inp.getBoundingClientRect();
              if (rect.width<40||rect.y<50) continue;
              if (/search|video|url|paste/.test(aria) || inp.type==='search' || inp.type==='text') {
                inp.focus();
                const proto=inp.tagName==='TEXTAREA'?HTMLTextAreaElement.prototype:HTMLInputElement.prototype;
                Object.getOwnPropertyDescriptor(proto,'value').set.call(inp,q);
                inp.dispatchEvent(new Event('input',{bubbles:true}));
                hit={aria:aria.slice(0,60),y:Math.round(rect.y)}; return;
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return hit;
        }""", GERMS)
        L("es_filled", filled=filled)
        page.keyboard.press("Enter")
        page.wait_for_timeout(2500)
        shot(page, "es_04_search")
        picked = page.evaluate("""()=>{
          let hit=null; const walk=(r,d=0)=>{
            if(!r||d>55||hit) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/How Did We Discover Germs/i.test(t) && t.length<120){
                const b=el.getBoundingClientRect();
                if(b.width>20&&b.y>60){el.click(); hit={t:t.slice(0,90),y:b.y}; return;}
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return hit;
        }""")
        L("es_picked", picked=picked)
        page.wait_for_timeout(1500)
        shot(page, "es_05_picked")
        # Try to move video element top-left (best-effort)
        page.evaluate("""() => {
          // drag first end-screen element if present
          const el = document.querySelector('ytve-endscreen-editor, .endscreen-element, [class*=endscreen]');
          return !!el;
        }""")
        for label in ("Save", "Done"):
            if click_btn(page, label):
                L("es_save", label=label)
                break
        shot(page, "es_06_saved")
        page.goto(f"https://studio.youtube.com/video/{VID}/edit", wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(4000)
        step.u.dismiss(page)
        a = step.sw.av(page, step.u)
        L("es_av", av=a)
        if not av_ok(a):
            raise SystemExit(f"STOP es {a}")
        # visibility + premiere
        page.evaluate(step.ts.CLICK_JS, "Visibility Scheduled") or page.evaluate(step.ts.CLICK_JS, "Visibility")
        page.wait_for_timeout(2000)
        shot(page, "visibility_final")
        L("vis", snip=page.inner_text("body")[-800:])
        prem = page.evaluate("""()=>{
          let hit=null; const walk=(r,d=0)=>{
            if(!r||d>55||hit) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=checkbox],tp-yt-paper-checkbox'):[])) {
              const lab=(el.getAttribute('aria-label')||el.innerText||'');
              if(!/premiere/i.test(lab)) continue;
              const checked=el.getAttribute('aria-checked')==='true';
              hit={lab:lab.slice(0,80),checked};
              if(checked){el.click(); hit.unchecked=true;}
              return;
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return hit;
        }""")
        L("premiere", prem=prem)
        page.keyboard.press("Escape")
        page.wait_for_timeout(400)
        # reopen ES verify
        page.evaluate(step.ts.CLICK_JS, "End screen")
        page.wait_for_timeout(3000)
        eb = page.inner_text("body")
        L("es_reopen", germs=("Germs" in eb), sub=("Subscribe" in eb), snip=eb[:800])
        shot(page, "es_08_reopen")

    out = OUT / "TC_ES_COMMIT_RESULT.json"
    out.write_text(json.dumps({"vid": VID, "log": log}, indent=2, default=str) + "\n")
    print("WROTE", out)


if __name__ == "__main__":
    main()
