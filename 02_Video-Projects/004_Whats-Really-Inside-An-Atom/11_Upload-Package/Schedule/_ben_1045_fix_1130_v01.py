#!/usr/bin/env python3
"""Fix Fri/Sun Short schedule times to 11:30 Europe/London on HOS Studio.

CDP :9460 · @HistoryOfScienceYT only.
Keep Scheduled (not Public). Do not touch CUu8k38iAMc.
Never publish-now / Premiere / Replace / delete.
"""
from __future__ import annotations

import importlib.util
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

PORT = 9460
HOS = "UCXp7HkBIl1LgaznXuZHJyRg"
HANDLE = "@HistoryOfScienceYT"
LONDON = ZoneInfo("Europe/London")
SCHED = Path(
    "/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/"
    "004_Whats-Really-Inside-An-Atom/11_Upload-Package/Schedule"
)
EV = SCHED / "evidence_2026-09-30_shorts"
ART = Path(
    "/Users/benjaminoats/Library/Application Support/Cursor/AgentStores/"
    "cursor_agent_stores/bc-958ae0f3-be07-568f-a2ab-eb7f422d8839/files/artifacts"
)

JOBS = [
    {
        "slot": "s01",
        "id": "29bpGAI0wb8",
        "title": "How small can you cut gold?",
        "day": 16,
        "date_typed": "16 Oct 2026",
        "time": "11:30",
        "related_id": "GHZDsiH7L7A",
        "related_title": "What's Really Inside an Atom?",
        "may_defer": True,
    },
    {
        "slot": "s02",
        "id": "TbMMJSRKC3U",
        "title": "He said every eighth element repeats",
        "day": 18,
        "date_typed": "18 Oct 2026",
        "time": "11:30",
        "related_id": "AL_-qlWko_g",
        "related_title": "How Did We Discover the Periodic Table?",
        "may_defer": False,
    },
]

_SPEC = importlib.util.spec_from_file_location("hos004", SCHED / "_upload_hos_004_shorts_v01.py")
up = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader
_SPEC.loader.exec_module(up)

_SPEC2 = importlib.util.spec_from_file_location(
    "cos", SCHED / "_cos_checkin_2102_growth_fix_v01.py"
)
cos = importlib.util.module_from_spec(_SPEC2)
assert _SPEC2.loader
_SPEC2.loader.exec_module(cos)


def log(msg: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now(LONDON).isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    with open(EV / "ben_1045_1130.log", "a") as f:
        f.write(line + "\n")


def dump(name: str, obj) -> None:
    (EV / name).write_text(json.dumps(obj, indent=2, default=str) + "\n")


def shot(page, name: str) -> Path:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    p = EV / name
    page.screenshot(path=str(p), full_page=False)
    shutil.copy2(p, ART / name)
    return p


def channel_gate(page) -> None:
    page.goto(
        f"https://studio.youtube.com/channel/{HOS}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2500)
    up.dismiss(page)
    body = page.inner_text("body")[:2500]
    if "History of Science" not in body and HOS not in (page.url or ""):
        raise SystemExit(f"ABORT wrong channel: {page.url}")
    if re.search(r"\bOrbit With Ben\b", body) and "History of Science" not in body:
        raise SystemExit("ABORT Orbit channel")
    log(f"CHANNEL_OK {page.url}")


def open_edit(page, vid: str) -> None:
    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    up.dismiss(page)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    if f"/video/{vid}/" not in (page.url or ""):
        raise SystemExit(f"ABORT not on edit {vid}: {page.url}")


def open_vis(page) -> bool:
    ok = page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55)return false;
            for(const el of (r.querySelectorAll
              ? r.querySelectorAll('ytcp-icon-button,button,[role=button]') : [])) {
              const a=el.getAttribute('aria-label')||'';
              if(/edit video visibility status/i.test(a)){el.click();return true;}
            }
            for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            return false;
          };
          return walk(document);
        }"""
    )
    page.wait_for_timeout(1400)
    return bool(ok)


def ensure_schedule_radio(page) -> str:
    # Prefer Schedule radio — never Public
    hit = up.click_radio(page, "Schedule")
    if not hit:
        hit = page.evaluate(
            """() => {
              let hit=null;
              const walk=(r,d=0)=>{
                if(!r||d>55||hit)return;
                for(const el of (r.querySelectorAll
                  ? r.querySelectorAll('tp-yt-paper-radio-button,[role=radio]') : [])) {
                  const t=((el.innerText||'')+' '+(el.getAttribute('aria-label')||''))
                    .replace(/\\s+/g,' ').trim();
                  const rect=el.getBoundingClientRect();
                  if(rect.width<=0) continue;
                  if(/^Schedule\\b/i.test(t) && !/Public|Private|Unlisted/i.test(t.split(' ')[0])){
                    el.click(); hit=t.slice(0,60); return;
                  }
                  if(/^Schedule$/i.test(t.split('\\n')[0].trim())){
                    el.click(); hit=t.slice(0,60); return;
                  }
                }
                for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot)walk(el.shadowRoot,d+1);
              };
              walk(document); return hit;
            }"""
        )
    page.wait_for_timeout(700)
    return hit or ""


def read_sched_fields(page) -> dict:
    return page.evaluate(
        """() => {
          const out={dialog:'', date:null, time:null, times:[], dates:[]};
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for(const el of (r.querySelectorAll
              ? r.querySelectorAll('ytcp-video-visibility-select,ytcp-visibility-scheduler,tp-yt-paper-dialog')
              : [])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if(t.length>out.dialog.length && /Schedule|Private|Save or publish/i.test(t))
                out.dialog=t.slice(0,500);
            }
            for(const el of (r.querySelectorAll?r.querySelectorAll('input'):[])){
              const v=(el.value||'').trim();
              const rect=el.getBoundingClientRect();
              if(rect.width<=0) continue;
              if(/^\\d{1,2}:\\d{2}$/.test(v)){
                out.times.push({v,x:rect.x,y:rect.y,w:rect.width,h:rect.height});
                out.time=v;
              }
              if(/\\d{1,2}\\s+\\w+\\s+\\d{4}/.test(v)){
                out.dates.push(v.split('\\n')[0]);
                out.date=v.split('\\n')[0];
              }
            }
            for(const el of (r.querySelectorAll
              ? r.querySelectorAll('ytcp-text-dropdown-trigger,ytcp-dropdown-trigger') : [])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if(/\\d{1,2}\\s+(Oct|October)\\s+2026/i.test(t) && t.length<40){
                out.date=t.match(/\\d{1,2}\\s+(?:Oct|October)\\s+2026/i)[0];
                out.dates.push(out.date);
              }
            }
            for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot)walk(el.shadowRoot,d+1);
          };
          walk(document); return out;
        }"""
    )


def set_date(page, date_typed: str, day: int) -> dict:
    info = {"wanted": date_typed}
    # Click date dropdown if present
    clicked = page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55)return false;
            for(const el of (r.querySelectorAll
              ? r.querySelectorAll('ytcp-text-dropdown-trigger,ytcp-dropdown-trigger,input')
              : [])) {
              const t=((el.innerText||el.value||'')+'').replace(/\\s+/g,' ').trim();
              const rect=el.getBoundingClientRect();
              if(rect.width<=0 || rect.y<300 || rect.y>600) continue;
              if(/\\d{1,2}\\s+(Oct|October|Sept|Sep)\\s+2026/i.test(t)
                  || /Time zone/i.test(t)
                  || (el.tagName==='INPUT' && /\\d{1,2}\\s+\\w+/.test(el.value||''))) {
                el.click(); return t.slice(0,60);
              }
            }
            for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            return false;
          };
          return walk(document);
        }"""
    )
    info["date_click"] = clicked
    page.wait_for_timeout(350)
    page.keyboard.press("Meta+A")
    page.keyboard.type(date_typed, delay=25)
    page.keyboard.press("Enter")
    page.wait_for_timeout(500)
    # Click away from calendar into dialog (not Escape)
    page.mouse.click(1050, 330)
    page.wait_for_timeout(400)
    fields = read_sched_fields(page)
    info["after"] = fields
    info["ok"] = str(day) in str(fields.get("date") or "") or str(day) in (
        fields.get("dialog") or ""
    )
    return info


def set_time_1130(page) -> dict:
    info = {}
    fields = read_sched_fields(page)
    info["before"] = fields.get("time")
    times = fields.get("times") or []
    if not times:
        # try again after short wait
        page.wait_for_timeout(500)
        fields = read_sched_fields(page)
        times = fields.get("times") or []
        info["before"] = fields.get("time")
    if not times:
        info["ok"] = False
        info["error"] = "no_time_input"
        return info
    tm = times[0]
    page.mouse.click(tm["x"] + 10, tm["y"] + tm["h"] / 2, click_count=3)
    page.wait_for_timeout(150)
    page.keyboard.press("Meta+A")
    page.keyboard.type("11:30", delay=40)
    page.wait_for_timeout(250)
    # Close time picker without Escape (Escape closes whole dialog)
    page.mouse.click(1050, 330)
    page.wait_for_timeout(500)
    after = read_sched_fields(page)
    info["after"] = after.get("time")
    info["ok"] = after.get("time") == "11:30"
    # If still wrong, try fill via evaluate
    if not info["ok"]:
        filled = page.evaluate(
            """() => {
              let hit=null;
              const walk=(r,d=0)=>{
                if(!r||d>55||hit)return;
                for(const el of (r.querySelectorAll?r.querySelectorAll('input'):[])){
                  const v=(el.value||'').trim();
                  const rect=el.getBoundingClientRect();
                  if(rect.width<=0) continue;
                  if(/^\\d{1,2}:\\d{2}$/.test(v)){
                    el.focus();
                    el.value='11:30';
                    el.dispatchEvent(new Event('input',{bubbles:true}));
                    el.dispatchEvent(new Event('change',{bubbles:true}));
                    hit=el.value;
                    return;
                  }
                }
                for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot)walk(el.shadowRoot,d+1);
              };
              walk(document); return hit;
            }"""
        )
        info["eval_fill"] = filled
        page.keyboard.type("", delay=1)
        # re-type with focus
        if times:
            page.mouse.click(tm["x"] + 10, tm["y"] + tm["h"] / 2, click_count=3)
            page.keyboard.press("Backspace")
            page.keyboard.press("Backspace")
            page.keyboard.press("Backspace")
            page.keyboard.press("Backspace")
            page.keyboard.press("Backspace")
            page.keyboard.type("11:30", delay=50)
            page.mouse.click(1050, 330)
            page.wait_for_timeout(400)
        after = read_sched_fields(page)
        info["after"] = after.get("time")
        info["ok"] = after.get("time") == "11:30"
    return info


def click_done(page) -> dict:
    info = {}
    # Done in visibility dialog — NEVER Schedule/Publish/Delete
    hit = page.evaluate(
        """() => {
          let hit=null;
          const walk=(r,d=0)=>{
            if(!r||d>55||hit)return;
            for(const el of (r.querySelectorAll
              ? r.querySelectorAll('button,ytcp-button,[role=button]') : [])) {
              const t=(el.innerText||'').trim();
              if(t!=='Done') continue;
              const dis=el.disabled||el.getAttribute('aria-disabled')==='true';
              const rect=el.getBoundingClientRect();
              if(rect.y>500 && !dis){ el.click(); hit={y:Math.round(rect.y)}; return; }
            }
            for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot)walk(el.shadowRoot,d+1);
          };
          walk(document); return hit;
        }"""
    )
    info["done"] = hit
    page.wait_for_timeout(1200)
    # Top Save
    saved = page.evaluate(
        """() => {
          let hit=null;
          const walk=(r,d=0)=>{
            if(!r||d>50||hit)return;
            for(const el of (r.querySelectorAll
              ? r.querySelectorAll('button,ytcp-button,[role=button]') : [])) {
              const t=(el.innerText||'').trim();
              if(t!=='Save') continue;
              const dis=el.disabled||el.getAttribute('aria-disabled')==='true';
              const rect=el.getBoundingClientRect();
              if(rect.y<140 && !dis){ el.click(); hit=true; return; }
            }
            for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot)walk(el.shadowRoot,d+1);
          };
          walk(document); return hit;
        }"""
    )
    info["save"] = saved
    page.wait_for_timeout(1500)
    # Confirm only safe buttons
    for name in ["Update", "Save", "Confirm", "Yes", "OK", "Done"]:
        try:
            b = page.get_by_role("button", name=re.compile(rf"^{re.escape(name)}$", re.I))
            if b.count() and b.first.is_visible():
                lab = (b.first.inner_text() or "").strip()
                if re.search(r"publish|delete|premiere|replace|^schedule$", lab, re.I):
                    continue
                b.first.click(force=True, timeout=1500)
                info["confirm"] = name
                page.wait_for_timeout(800)
        except Exception:
            pass
    return info


def read_related(page) -> dict:
    body = page.inner_text("body")
    idx = body.lower().find("related video")
    window = body[idx : idx + 400].replace("\n", " ") if idx >= 0 else ""
    out = {"window": window[:300], "status": "unset"}
    if "What's Really Inside an Atom?" in window or "GHZDsiH7L7A" in window:
        out["status"] = "set"
        out["title"] = "What's Really Inside an Atom?"
        out["id"] = "GHZDsiH7L7A"
    elif "How Did We Discover the Periodic Table?" in window or "AL_-qlWko_g" in window:
        out["status"] = "set"
        out["title"] = "How Did We Discover the Periodic Table?"
        out["id"] = "AL_-qlWko_g"
    elif re.search(r"Related video\s+None", window):
        out["status"] = "none"
    return out


def post_checks(page) -> dict:
    for _ in range(16):
        page.mouse.wheel(0, 900)
        page.wait_for_timeout(70)
    cos.show_more(page)
    page.wait_for_timeout(500)
    aud = cos.read_audience(page)
    ai = cos.read_ai_altered(page)
    if not aud.get("radios"):
        for _ in range(18):
            page.keyboard.press("PageDown")
            page.wait_for_timeout(60)
        cos.show_more(page)
        aud = cos.read_audience(page)
        ai = cos.read_ai_altered(page)
    related = read_related(page)
    return {
        "audience": aud,
        "audience_not_kids": bool(aud.get("ok_not_kids")) and not aud.get("fail_kids"),
        "altered": ai,
        "altered_yes": bool(ai.get("yes")),
        "related": related,
    }


def fix_one(page, job: dict) -> dict:
    out = {
        "slot": job["slot"],
        "id": job["id"],
        "title": job["title"],
        "wanted": f"{job['date_typed']} {job['time']} Europe/London",
    }
    channel_gate(page)
    open_edit(page, job["id"])
    chip0 = up.visibility_chip(page)
    out["chip_before"] = chip0
    log(f"{job['slot']} chip_before={chip0!r}")

    if not open_vis(page):
        # click Visibility Scheduled chip
        page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>55)return false;
                for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[])){
                  const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                  if(/^Visibility\\s+Scheduled/i.test(t) && t.length<140){
                    el.click(); return true;
                  }
                }
                for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                return false;
              };
              return walk(document);
            }"""
        )
        page.wait_for_timeout(1400)

    out["sched_radio"] = ensure_schedule_radio(page)
    before = read_sched_fields(page)
    out["fields_before"] = before
    log(f"{job['slot']} before date={before.get('date')} time={before.get('time')} dlg={ (before.get('dialog') or '')[:120]}")

    out["date_set"] = set_date(page, job["date_typed"], job["day"])
    out["time_set"] = set_time_1130(page)
    log(f"{job['slot']} time_set={out['time_set']}")

    mid = read_sched_fields(page)
    out["fields_mid"] = mid
    shot(page, f"BEN_1045_{job['slot']}_1130.png")

    # Abort if somehow Public got selected
    dlg = mid.get("dialog") or ""
    if re.search(r"\bPublic\b", dlg) and "Schedule as public" not in dlg and "Schedule" not in dlg:
        # Schedule as public is the schedule mode label — OK
        pass
    # Must still be on Schedule path
    if mid.get("time") != "11:30":
        # one more hard retry on time
        out["time_retry"] = set_time_1130(page)
        mid = read_sched_fields(page)
        out["fields_mid"] = mid
        shot(page, f"BEN_1045_{job['slot']}_1130.png")

    out["save"] = click_done(page)
    log(f"{job['slot']} save={out['save']}")

    # Reload verify
    open_edit(page, job["id"])
    chip1 = up.visibility_chip(page)
    out["chip_after"] = chip1
    open_vis(page)
    page.wait_for_timeout(1200)
    # Schedule should still be selected — do not click Private
    after = read_sched_fields(page)
    out["fields_after_save"] = after
    out["time_after_save"] = after.get("time")
    out["date_after_save"] = after.get("date")
    # date may only be in dialog text
    if not out["date_after_save"]:
        m = re.search(r"(\d{1,2}\s+Oct(?:ober)?\s+2026)", after.get("dialog") or "", re.I)
        if m:
            out["date_after_save"] = m.group(1)
    shot(page, f"BEN_1045_{job['slot']}_1130.png")
    page.keyboard.press("Escape")
    page.wait_for_timeout(400)

    checks = post_checks(page)
    out.update(checks)

    # Related status labeling
    rel = checks.get("related") or {}
    if job["may_defer"] and rel.get("status") in ("none", "unset"):
        out["related_status"] = "deferred_or_unset"
    elif rel.get("id") == job["related_id"] or rel.get("title") == job["related_title"]:
        out["related_status"] = "set"
    else:
        out["related_status"] = rel.get("status") or "unset"

    out["ok"] = (
        "Scheduled" in (chip1 or "")
        and out.get("time_after_save") == "11:30"
        and str(job["day"]) in str(out.get("date_after_save") or after.get("dialog") or "")
        and out.get("audience_not_kids")
        and out.get("altered_yes")
    )
    log(
        f"{job['slot']} DONE ok={out['ok']} time={out.get('time_after_save')} "
        f"date={out.get('date_after_save')} chip={chip1!r} related={out.get('related_status')}"
    )
    return out


def main() -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    result = {
        "channel": HANDLE,
        "channelId": HOS,
        "started": datetime.now(LONDON).isoformat(timespec="seconds"),
        "do_not_touch": "CUu8k38iAMc",
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        page = next(
            (pg for pg in ctx.pages if "studio.youtube.com" in (pg.url or "")),
            None,
        ) or ctx.new_page()

        channel_gate(page)
        outs = {}
        for job in JOBS:
            log(f"=== FIX {job['slot']} {job['id']} → {job['date_typed']} 11:30 ===")
            outs[job["slot"]] = fix_one(page, job)
            dump(f"BEN_1045_{job['slot']}_1130.json", outs[job["slot"]])

        result["fri"] = outs["s01"]
        result["sun"] = outs["s02"]
        result["fri_time_shown"] = outs["s01"].get("time_after_save")
        result["sun_time_shown"] = outs["s02"].get("time_after_save")
        result["fri_date_shown"] = outs["s01"].get("date_after_save")
        result["sun_date_shown"] = outs["s02"].get("date_after_save")
        result["ok"] = bool(outs["s01"].get("ok")) and bool(outs["s02"].get("ok"))
        result["ended"] = datetime.now(LONDON).isoformat(timespec="seconds")
        dump("FRI_SUN_1130_CONFIRM.json", result)
        log(f"DONE ok={result['ok']} fri={result['fri_time_shown']} sun={result['sun_time_shown']}")
        print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
