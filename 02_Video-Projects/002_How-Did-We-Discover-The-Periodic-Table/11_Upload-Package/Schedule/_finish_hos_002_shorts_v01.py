#!/usr/bin/env python3
"""Finish HOS 002 Shorts on a dedicated Studio tab. Do not reuse Google One / Cloud / Facebook tabs."""
from __future__ import annotations

import importlib.util
import json
import re
import sys
import traceback
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve()
spec = importlib.util.spec_from_file_location("hos002u", HERE.with_name("_upload_hos_002_shorts_v01.py"))
u = importlib.util.module_from_spec(spec)
spec.loader.exec_module(u)

LONDON = ZoneInfo("Europe/London")
EV = u.PKG / "Schedule/evidence_2026-09-11_shorts_finish"
u.EV = EV
KNOWN = {
    "s01_empty_chairs": "uU12JA5rMWg",
    "s02_predict_metal": "nFQRWmpulTQ",
    "s03_gallium": "CnHwX1L9XHg",
    "s04_tellurium": "nba0-f7PPeU",
    "s05_other_table": "LanTHJckYx8",
}
REMAINING = {"s02_predict_metal", "s03_gallium", "s05_other_table"}


def log(msg: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    with (EV / "run.log").open("a") as f:
        f.write(line + "\n")


def dump(name: str, obj) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    (EV / name).write_text(json.dumps(obj, indent=2) + "\n")


def shot(page, name: str) -> str:
    return u.shot(page, name)


def assert_studio(page) -> None:
    if "studio.youtube.com" in (page.url or ""):
        return
    page.goto(
        f"https://studio.youtube.com/channel/{u.CHANNEL}/videos/short",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2500)
    if "studio.youtube.com" not in (page.url or ""):
        raise RuntimeError(f"lost Studio, url={page.url}")


def dedicated_studio(ctx):
    page = ctx.new_page()
    page.goto(
        f"https://studio.youtube.com/channel/{u.CHANNEL}/videos/short",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    u.dismiss(page)
    assert_studio(page)
    body = u.snip(page, 1500)
    if "History of Science" not in body and u.CHANNEL not in page.url:
        raise RuntimeError("HOS_NOT_IN_BODY")
    return page


GERMS_IDS = {
    "H1y0DXFVmw8", "iqToagXnjX0", "8_Edn_HCi1s", "sILtQxgYQk8", "93fPUG-hW0A",
    "8uBR-9oxeWs", "YX2UR1u-JCQ", "Fnb3p81u-wY", "vpuRgKXtFlY", "Lcmh5y2KMQM",
}


def list_short_ids(page) -> dict[str, str]:
    rows = page.evaluate(
        """() => {
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>45) return;
            for (const el of (r.querySelectorAll ? r.querySelectorAll('a[href]') : [])) {
              const href=el.getAttribute('href')||'';
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              const m=href.match(/\\/video\\/([A-Za-z0-9_-]{11})/)
                || href.match(/\\/shorts\\/([A-Za-z0-9_-]{11})/);
              if (m) out.push({id:m[1], t:t.slice(0,140), href});
            }
            for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : [])) {
              if (el.shadowRoot) walk(el.shadowRoot, d+1);
            }
          };
          walk(document);
          return out;
        }"""
    ) or []
    (EV / "listed_rows.json").write_text(json.dumps(rows, indent=2) + "\n")
    found: dict[str, str] = {}
    for row in rows:
        vid = row.get("id") or ""
        t = (row.get("t") or "").strip()
        if not vid or vid in GERMS_IDS or vid in {u.LONG_ID, "_C92tIJCk8A"}:
            continue
        tlow = t.lower()
        for job in u.JOBS:
            if job["title"].lower() in tlow:
                found.setdefault(job["slot"], vid)
    return found


def click_edit_draft(page) -> str:
    try:
        b = page.get_by_text("Edit draft", exact=True)
        if b.count() and b.first.is_visible():
            b.first.click(force=True, timeout=4000)
            page.wait_for_timeout(2000)
            return "clicked"
    except Exception as e:
        return f"err:{type(e).__name__}"
    try:
        b = page.get_by_role("button", name=re.compile(r"Edit draft", re.I))
        if b.count():
            b.first.click(force=True, timeout=4000)
            page.wait_for_timeout(2000)
            return "role"
    except Exception:
        pass
    return "missing"


def click_row_edit_draft(page, title: str) -> str:
    return page.evaluate(
        """(title) => {
          let row=null;
          const walk=(r,d=0)=>{
            if(!r||d>50||row) return;
            for (const el of (r.querySelectorAll ? r.querySelectorAll('ytcp-video-row') : [])) {
              const t=el.innerText||'';
              if (t.includes(title) && /Edit draft/i.test(t)) { row=el; return; }
            }
            for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : [])) {
              if (el.shadowRoot) walk(el.shadowRoot, d+1);
            }
          };
          walk(document);
          if (!row) return 'no_row';
          const clickWalk=(r,d=0)=>{
            if(!r||d>40) return false;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('button,ytcp-button,a,[role=button],ytcp-button-shape') : [])) {
              if (/^Edit draft$/i.test((el.innerText||'').trim())) { el.click(); return true; }
            }
            for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : [])) {
              if (el.shadowRoot && clickWalk(el.shadowRoot, d+1)) return true;
            }
            return false;
          };
          return clickWalk(row) ? 'clicked' : 'row_no_btn';
        }""",
        title,
    )


def set_related_tile(page) -> str:
    u.dismiss(page)
    if u.verify_wall(page):
        return "phone_verify_wall"
    widget = u.related_widget(page)
    if u.LONG_TITLE[:20] in widget and not re.search(r"\bNone\b", widget, re.I):
        return f"already:{widget}"
    try:
        for _ in range(6):
            page.mouse.wheel(0, 700)
            page.wait_for_timeout(150)
        page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>50) return false;
                for (const el of (r.querySelectorAll
                  ? r.querySelectorAll('ytcp-icon-button,button,[role=button]') : [])) {
                  const a=el.getAttribute('aria-label')||'';
                  if (/related video/i.test(a)) { el.click(); return true; }
                }
                for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : [])) {
                  if (el.shadowRoot && walk(el.shadowRoot, d+1)) return true;
                }
                return false;
              };
              return walk(document);
            }"""
        )
        page.wait_for_timeout(1200)
        tile = page.get_by_text(re.compile(r"How Did We Discover the Periodic", re.I))
        if tile.count():
            tile.first.click(timeout=6000)
            page.wait_for_timeout(800)
            save = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
            if save.count() and save.first.is_enabled():
                save.first.click(force=True)
                page.wait_for_timeout(1500)
                return "tile_saved"
            return "tile_clicked"
        return f"no_tile widget={widget}"
    except Exception as e:
        return f"err:{type(e).__name__}"


def finish_one(page, job: dict, video_id: str) -> dict:
    slot = job["slot"]
    cover = u.COVERS / job["cover"]
    item = {
        "slot": slot,
        "title": job["title"],
        "platformPostId": video_id,
        "dateLabel": job["dateLabel"],
    }
    log(f"==== finish {slot} {video_id} ====")
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    u.dismiss(page)
    assert_studio(page)
    shot(page, f"{slot}_f01_edit.png")
    item["draft"] = click_edit_draft(page)
    try:
        page.locator("ytcp-uploads-dialog").first.wait_for(timeout=12000)
        item["wizard"] = True
    except Exception:
        item["draft"] = click_edit_draft(page)
        try:
            page.locator("ytcp-uploads-dialog").first.wait_for(timeout=8000)
            item["wizard"] = True
        except Exception:
            item["wizard"] = False
    page.wait_for_timeout(800)
    item["kids"] = u.set_not_kids(page)
    item["thumb"] = u.set_image(page, cover)
    save = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
    if save.count() and save.first.is_enabled():
        save.first.click(force=True)
        page.wait_for_timeout(1200)
    # If Edit draft dropped us into the upload wizard, land on Visibility.
    vis_text = u.dlg_text(page, 2500)
    if re.search(r"Save or publish|Select a date to make your video public", vis_text, re.I):
        item["inWizard"] = True
    else:
        item["next"] = u.next_until_visibility(page)
        vis_text = u.dlg_text(page, 2500)
    item["scheduleOpen"] = u.open_schedule(page)
    page.wait_for_timeout(700)
    item["when"] = u.fill_when(page, job["day"])
    if not u.date_is(item["when"].get("after") or {}, job["day"]):
        item["whenRetry"] = u.fill_when(page, job["day"])
        item["when"]["after"] = item["whenRetry"].get("after")
    shot(page, f"{slot}_f02_when.png")
    if not u.date_is(item["when"].get("after") or {}, job["day"]):
        # Visibility dropdown on the edit page (not wizard).
        item["openVis"] = u.open_edit_visibility(page)
        item["scheduleOpen2"] = u.open_schedule(page)
        item["when3"] = u.fill_when(page, job["day"])
        shot(page, f"{slot}_f02b_when.png")
        if not u.date_is(item["when3"].get("after") or {}, job["day"]):
            item["error"] = f"date_not_set:{item['when'].get('after')}"
            item["ok"] = False
            return item
        item["when"]["after"] = item["when3"].get("after")
    item["confirm"] = u.click_schedule_btn(page)
    page.wait_for_timeout(2500)
    u.dismiss(page)
    save2 = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
    if save2.count() and save2.first.is_enabled():
        save2.first.click(force=True)
        page.wait_for_timeout(1200)
        item["visSave"] = "clicked"
    shot(page, f"{slot}_f03_after.png")
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2500)
    u.dismiss(page)
    assert_studio(page)
    item["related"] = set_related_tile(page)
    shot(page, f"{slot}_f04_related.png")
    item["relatedWidget"] = u.related_widget(page)
    item["ok"] = True
    return item


def main() -> int:
    EV.mkdir(parents=True, exist_ok=True)
    u.ART.mkdir(parents=True, exist_ok=True)
    result = {
        "ok": False,
        "channel": u.HANDLE,
        "parentId": u.LONG_ID,
        "started": datetime.now(tz=LONDON).isoformat(timespec="seconds"),
        "shorts": [],
    }
    u.ensure_chrome()
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(u.CDP, timeout=60000)
        ctx = browser.contexts[0]
        page = dedicated_studio(ctx)
        shot(page, "00_shorts_list.png")
        found = list_short_ids(page)
        result["listed"] = found
        log(f"listed {found}")
        jobs = [j for j in u.JOBS if j["slot"] in REMAINING] if "--remaining" in sys.argv else u.JOBS
        skip = {u.LONG_ID, "_C92tIJCk8A", *KNOWN.values(), *GERMS_IDS}
        body = u.snip(page, 4000)
        for job in jobs:
            vid = KNOWN.get(job["slot"]) or found.get(job["slot"])
            if not vid:
                if job["title"] not in body and job["title"] not in u.snip(page, 4000):
                    log(f"SKIP missing and not on list {job['slot']} — will not mint a duplicate")
                    result["shorts"].append({
                        "slot": job["slot"],
                        "title": job["title"],
                        "ok": False,
                        "error": "not_on_shorts_list",
                    })
                    continue
                page.goto(
                    f"https://studio.youtube.com/channel/{u.CHANNEL}/videos/short",
                    wait_until="domcontentloaded",
                    timeout=120000,
                )
                page.wait_for_timeout(2500)
                u.dismiss(page)
                assert_studio(page)
                clicked = click_row_edit_draft(page, job["title"])
                page.wait_for_timeout(2500)
                vid = u.extract_id(page, skip) or ""
                log(f"row_edit {job['slot']} {clicked} id={vid}")
                if not vid:
                    result["shorts"].append({
                        "slot": job["slot"],
                        "title": job["title"],
                        "ok": False,
                        "error": f"no_id_after_edit_draft:{clicked}",
                        "clicked": clicked,
                    })
                    dump("RESULT.json", result)
                    continue
                skip.add(vid)
            else:
                skip.add(vid)
            result["shorts"].append(finish_one(page, job, vid))
            dump("RESULT.json", result)
            log(f"{job['slot']} ok={result['shorts'][-1].get('ok')} id={vid}")
        page.goto(
            f"https://studio.youtube.com/channel/{u.CHANNEL}/videos/short",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3000)
        u.dismiss(page)
        shot(page, "99_shorts_after.png")
        result["contentSnip"] = u.snip(page, 2200)
        result["longThumb"] = u.apply_long_thumb(page)
        shot(page, "99_long_thumb.png")
        result["longSnip"] = u.snip(page, 500)
    result["ok"] = all(s.get("ok") for s in result["shorts"]) and len(result["shorts"]) == 5
    result["finished"] = datetime.now(tz=LONDON).isoformat(timespec="seconds")
    dump("RESULT.json", result)
    out = u.PKG / "Schedule/PACKAGE_UPLOAD_RESULT_2026-09-11_shorts.json"
    prev = {}
    if out.exists():
        try:
            prev = json.loads(out.read_text())
        except Exception:
            prev = {}
    prev["finish"] = result
    prev["ok"] = result["ok"]
    out.write_text(json.dumps(prev, indent=2) + "\n")
    log(f"wrote {out} ok={result['ok']}")
    print(json.dumps(result, indent=2)[:4000])
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:
        EV.mkdir(parents=True, exist_ok=True)
        (EV / "TRACE.txt").write_text(traceback.format_exc())
        raise
