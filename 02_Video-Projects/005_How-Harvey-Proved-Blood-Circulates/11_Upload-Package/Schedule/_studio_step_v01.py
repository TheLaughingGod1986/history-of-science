#!/usr/bin/env python3
"""HOS 005 Studio, one step at a time over desktop Studio CDP (:9460). @HistoryOfScienceYT only.

Never saves unless the step is `save`. Every step prints Audience + Visibility and writes a screenshot.

  python3 _studio_step_v01.py open [edit|translations|analytics]   # HOS check, open the page
  python3 _studio_step_v01.py shot <name>
  python3 _studio_step_v01.py dom <name>                # dialog buttons/inputs (or page if no dialog)
  python3 _studio_step_v01.py click "<exact text>" <name>
  python3 _studio_step_v01.py find "<regex>" <name>     # scroll to text
  python3 _studio_step_v01.py text <name>               # body text tail
  python3 _studio_step_v01.py save <name>               # page Save, then re-read Audience + Visibility
"""
from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

VID = "0IfXGSX7Ypw"
HOS = "UCXp7HkBIl1LgaznXuZHJyRg"
CDP = "http://127.0.0.1:9460"
LONDON = ZoneInfo("Europe/London")
MAIN = Path("/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/004_Whats-Really-Inside-An-Atom/11_Upload-Package/Schedule")
DESK_TC = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/DESK_2026-10-01_tc"
OUT = Path(__file__).resolve().parents[1] / "evidence_2026-10-02_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/DESK_2026-10-02_005_upload"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


u = load("u004", MAIN / "_upload_hos_004_shorts_v01.py")
sw = load("sweep", MAIN / "_ben_1447_whole_channel_studio_v01.py")
ts = load("tcs", DESK_TC / "tc_step.py")


def page_for(browser):
    for c in browser.contexts:
        for pg in c.pages:
            if VID in pg.url:
                return pg
    return browser.contexts[0].new_page()


def shot(page, name):
    ART.mkdir(parents=True, exist_ok=True)
    p = ART / f"{name}.png"
    page.screenshot(path=str(p))
    return str(p)


def report(page, extra=None):
    a = sw.av(page, u)
    out = {"at": datetime.now(LONDON).isoformat(timespec="seconds"), "url": page.url,
           "visibility": a.get("chip"), "not_kids": a.get("not_kids"), "kids_yes": a.get("kids_yes"),
           "ai": sw.read_ai(page)}
    if extra:
        out.update(extra)
    print(json.dumps(out, ensure_ascii=False, default=str)[:3000], flush=True)
    return out


def main():
    cmd = sys.argv[1]
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = page_for(browser)
        page.set_default_timeout(60000)
        extra = {}
        if cmd == "open":
            where = sys.argv[2] if len(sys.argv) > 2 else "edit"
            hos = sw.ensure_hos(page, u)
            extra["hos"] = {"ok": hos["ok"], "url": hos["url"]}
            if not hos["ok"]:
                print(json.dumps(extra))
                raise SystemExit("not on HOS channel; stop")
            page.goto(f"https://studio.youtube.com/video/{VID}/{where}", wait_until="domcontentloaded", timeout=120000)
            page.wait_for_timeout(4000)
            u.dismiss(page)
            if where == "edit":
                sw.show_more(page)
            name = f"open_{where}"
        elif cmd == "shot":
            name = sys.argv[2]
        elif cmd == "dom":
            name = sys.argv[2]
            print(json.dumps(page.evaluate(ts.DOM_JS), ensure_ascii=False)[:8000])
        elif cmd == "click":
            extra["clicked"] = page.evaluate(ts.CLICK_JS, sys.argv[2])
            page.wait_for_timeout(2500)
            name = sys.argv[3]
        elif cmd == "find":
            extra["found"] = sw.scroll_find(page, sys.argv[2])
            name = sys.argv[3]
        elif cmd == "text":
            name = sys.argv[2]
            print(page.inner_text("body")[-4000:])
        elif cmd == "state":
            name = sys.argv[2]
            sw.show_more(page)
            for _ in range(14):
                page.mouse.wheel(0, 700)
                page.wait_for_timeout(80)
            ed = load("eng", MAIN / "_ben_1954_england_level_exam_v01.py")
            extra["edu"] = ed.edu_triggers(page)
            extra["radios"] = page.evaluate("""() => {
              const out=[]; const walk=(r,d=0)=>{ if(!r||d>55) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('[role=radio],[role=checkbox],tp-yt-paper-checkbox'):[])) {
                  const lab=(el.getAttribute('aria-label')||el.innerText||'').replace(/\\s+/g,' ').trim();
                  if (lab) out.push((el.getAttribute('aria-checked')==='true'?'[x] ':'[ ] ')+lab.slice(0,90)); }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,d+1);
              }; walk(document); return [...new Set(out)]; }""")
            extra["triggers"] = page.evaluate("""() => {
              const out=[]; const walk=(r,d=0)=>{ if(!r||d>55) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('ytcp-text-dropdown-trigger,ytcp-dropdown-trigger'):[]))
                  out.push((el.innerText||'').replace(/\\s+/g,' ').trim().slice(0,100));
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,d+1);
              }; walk(document); return [...new Set(out)]; }""")
        elif cmd == "save":
            extra["save"] = u.page_save(page)
            page.wait_for_timeout(3000)
            name = sys.argv[2]
        else:
            raise SystemExit(f"unknown {cmd}")
        extra["shot"] = shot(page, name)
        report(page, extra)


if __name__ == "__main__":
    main()
