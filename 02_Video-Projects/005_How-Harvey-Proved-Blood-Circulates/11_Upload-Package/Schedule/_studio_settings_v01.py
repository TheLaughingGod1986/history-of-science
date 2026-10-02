#!/usr/bin/env python3
"""HOS 005 Studio §9 settings on 0IfXGSX7Ypw. One setting per save; Audience + Visibility re-read after each.

  python3 _studio_settings_v01.py list              # open each dropdown, list options, Escape (no save)
  python3 _studio_settings_v01.py commit [step …]   # steps: paid caption type england level exam places moderation
Stops at once if a save leaves Visibility not Scheduled or Audience not 'not made for kids'.
"""
from __future__ import annotations

import importlib.util as iu
import json
import re
import sys
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
_s = iu.spec_from_file_location("step", HERE / "_studio_step_v01.py")
step = iu.module_from_spec(_s)
_s.loader.exec_module(step)
eng = step.load("eng", step.MAIN / "_ben_1954_england_level_exam_v01.py")
u, sw = step.u, step.sw
EXAM = "GCSE Biology"

DROPDOWNS = {
    "caption": (r"^Caption certification", r"never aired on television"),
    "type": (r"^Type ", r"^Concept overview"),
    "moderation": (r"^Moderation", r"^(Basic|Hold potentially inappropriate)"),
}


def prep(page):
    sw.show_more(page)
    for _ in range(14):
        page.mouse.wheel(0, 700)
        page.wait_for_timeout(60)


def trigger_text(page, pat):
    return page.evaluate("""(pat) => { const re=new RegExp(pat,'i'); let hit=null;
      const walk=(r,d=0)=>{ if(!r||d>55||hit) return;
        for (const el of (r.querySelectorAll?r.querySelectorAll('ytcp-text-dropdown-trigger,ytcp-dropdown-trigger'):[])) {
          const t=(el.innerText||'').replace(/\\s+/g,' ').trim(); if (re.test(t)) { hit=t; return; } }
        for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,d+1);
      }; walk(document); return hit; }""", pat)


def open_list(page, trig):
    eng.open_dd(page, trig)
    page.wait_for_timeout(1200)
    return eng.list_opts(page)


def ok_av(a):
    return a.get("chip") == "Visibility Scheduled" and a.get("not_kids") and not a.get("kids_yes")


def save_check(page, label):
    s = u.page_save(page)
    page.wait_for_timeout(3500)
    a = sw.av(page, u)
    r = {"label": label, "save": s, "visibility": a.get("chip"), "not_kids": a.get("not_kids"),
         "kids_yes": a.get("kids_yes")}
    print("   SAVE", json.dumps(r, default=str), flush=True)
    if not ok_av(a):
        raise SystemExit(f"STOP after {label}: Audience/Visibility not as expected {a}")
    return r


def do_dropdown(page, key):
    trig, want = DROPDOWNS[key]
    before = trigger_text(page, trig)
    if before and re.search(want, before.split(" ", 2)[-1] if key != "type" else before[5:], re.I):
        return {"key": key, "already": before}
    opts = open_list(page, trig)
    pick = next((o for o in opts if re.search(want, o, re.I)), None)
    res = {"key": key, "before": before, "options": opts[:25], "pick": pick}
    if not pick:
        page.keyboard.press("Escape")
        res["stop"] = "wanted option not listed; nothing changed"
        return res
    res["click"] = eng.js_click_option(page, pick)
    page.wait_for_timeout(900)
    res["mid"] = trigger_text(page, trig)
    if not res["mid"] or pick.split(" ")[0] not in res["mid"]:
        page.keyboard.press("Escape")
        res["stop"] = "trigger did not take the option; nothing saved"
        return res
    res["saved"] = save_check(page, key)
    res["after"] = trigger_text(page, trig)
    return res


def do_paid(page):
    sw.scroll_find(page, r"Paid promotion")
    hit = sw.click_radio(page, r"No, my video doesn.?t include paid promotion")
    res = {"key": "paid", "hit": hit}
    if hit and hit.get("checked"):
        res["already"] = True
        return res
    res["saved"] = save_check(page, "paid_no")
    return res


def do_places(page):
    sw.scroll_find(page, r"Allow automatic places")
    c = sw.set_check(page, r"Allow automatic places", False)
    res = {"key": "places", "check": c}
    if c.get("before") is True and c.get("after") is False:
        res["saved"] = save_check(page, "places_off")
    return res


def main():
    mode = sys.argv[1]
    steps = sys.argv[2:] or ["paid", "caption", "type", "england", "level", "exam", "places", "moderation"]
    out = {"mode": mode, "steps": []}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(step.CDP, timeout=60000)
        page = step.page_for(browser)
        page.set_default_timeout(60000)
        hos = sw.ensure_hos(page, u)
        if not hos["ok"]:
            raise SystemExit("not on HOS channel; stop")
        page.goto(f"https://studio.youtube.com/video/{step.VID}/edit", wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(4500)
        u.dismiss(page)
        page.evaluate(step.ts.CLICK_JS, "Undo changes")
        page.wait_for_timeout(1500)
        prep(page)
        out["start"] = step.report(page)
        if mode == "list":
            for key, (trig, _) in DROPDOWNS.items():
                out["steps"].append({"key": key, "trigger": trigger_text(page, trig), "options": open_list(page, trig)[:40]})
                page.keyboard.press("Escape")
                page.wait_for_timeout(600)
            for key, pat in (("academic", r"Academic system"), ("level", r"^Level")):
                out["steps"].append({"key": key, "trigger": trigger_text(page, pat), "options": open_list(page, pat)[:60]})
                page.keyboard.press("Escape")
                page.wait_for_timeout(600)
        else:
            for s in steps:
                print("STEP", s, flush=True)
                if s == "paid":
                    r = do_paid(page)
                elif s in DROPDOWNS:
                    r = do_dropdown(page, s)
                elif s == "england":
                    r = eng.set_england(page, u)
                    page.wait_for_timeout(1500)
                    a = sw.av(page, u)
                    r["av"] = a
                    if not ok_av(a):
                        raise SystemExit(f"STOP after england: {a}")
                elif s == "level":
                    r = eng.set_level_14_16(page, u)
                    a = sw.av(page, u)
                    r["av"] = a
                    if not ok_av(a):
                        raise SystemExit(f"STOP after level: {a}")
                elif s == "exam":
                    r = eng.set_exam_if_listed(page, u, EXAM)
                    a = sw.av(page, u)
                    r["av"] = a
                    if not ok_av(a):
                        raise SystemExit(f"STOP after exam: {a}")
                elif s == "places":
                    r = do_places(page)
                else:
                    raise SystemExit(f"unknown step {s}")
                print("  ", json.dumps(r, ensure_ascii=False, default=str)[:900], flush=True)
                out["steps"].append(r)
                prep(page)
            page.goto(f"https://studio.youtube.com/video/{step.VID}/edit", wait_until="domcontentloaded", timeout=120000)
            page.wait_for_timeout(4500)
            u.dismiss(page)
            prep(page)
            out["reopen"] = step.report(page, {"edu": eng.edu_triggers(page)})
            out["reopen_shot"] = step.shot(page, "settings_reopen")
        out["at"] = datetime.now(step.LONDON).isoformat(timespec="seconds")
        dest = HERE.parent / "evidence_2026-10-02_studio" / f"SETTINGS_{mode.upper()}_RESULT.json"
        dest.write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str))
        if mode == "list":
            print(json.dumps(out["steps"], ensure_ascii=False, indent=0)[:5000])
        print("wrote", dest, flush=True)


if __name__ == "__main__":
    main()
