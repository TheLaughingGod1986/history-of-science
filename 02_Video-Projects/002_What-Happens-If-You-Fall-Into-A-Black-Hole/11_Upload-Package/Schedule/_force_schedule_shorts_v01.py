#!/usr/bin/env python3
"""Force-schedule Video 002 Shorts via visibility accordion (V010 private path).

Uses Private → Schedule expand → date/time → Done → Save.
Also verifies long-form schedule datetime.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = "/Users/ben/code/youtube/.playwright-youtube-profile"
ROOT = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "002_What-Happens-If-You-Fall-Into-A-Black-Hole"
)
FINISH = ROOT / "11_Upload-Package/Schedule/blackhole_studio_finish_result.json"
OUT = ROOT / "11_Upload-Package/Schedule/blackhole_force_schedule_result.json"
AUDIT = ROOT / "11_Upload-Package/Schedule/_force_schedule"
LONG_ID = "n7CbJrOCnU0"
DATE_RE = re.compile(r"\d{1,2} \w{3,9} 2026")

MONTHS = {
    1: ("January", "Jan"),
    2: ("February", "Feb"),
    3: ("March", "Mar"),
    4: ("April", "Apr"),
    5: ("May", "May"),
    6: ("June", "Jun"),
    7: ("July", "Jul"),
    8: ("August", "Aug"),
    9: ("September", "Sep"),
    10: ("October", "Oct"),
    11: ("November", "Nov"),
    12: ("December", "Dec"),
}


def skip(page) -> None:
    try:
        page.get_by_role("link", name=re.compile(r"Skip", re.I)).click(timeout=1000)
    except Exception:
        pass


def dismiss(page) -> None:
    page.evaluate(
        "() => document.querySelectorAll('tp-yt-iron-overlay-backdrop').forEach(e => e.remove())"
    )


def open_visibility(page) -> None:
    page.locator("ytcp-video-metadata-visibility").first.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    page.locator("ytcp-video-metadata-visibility").first.click(force=True)
    page.wait_for_timeout(1400)


def expand_schedule(page) -> dict | None:
    dlg = page.get_by_role("dialog", name="Select video privacy")
    text = dlg.inner_text() if dlg.count() else page.locator("body").inner_text()
    if "Schedule as public" in text or DATE_RE.search(text):
        return {"via": "already_expanded"}

    rect = page.evaluate(
        """() => {
          const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]');
          let hit=null;
          const walk=(root)=>{
            for (const el of root.querySelectorAll('*')) {
              const al=el.getAttribute('aria-label')||'';
              const id=el.id||'';
              if (/click to expand/i.test(al) || id==='first-container-expand-button') {
                const r=el.getBoundingClientRect();
                if (r.width>5) hit={x:r.x+r.width/2,y:r.y+r.height/2,al};
              }
              if (el.shadowRoot) walk(el.shadowRoot);
            }
          };
          walk(dlg||document);
          return hit;
        }"""
    )
    if rect:
        page.mouse.click(rect["x"], rect["y"])
        page.wait_for_timeout(1100)
        return {"via": "expand", **rect}

    hit = page.evaluate(
        """() => {
          const hits=[];
          const walk=(root)=>{
            for (const el of root.querySelectorAll('*')) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (t!=='Schedule') continue;
              const r=el.getBoundingClientRect();
              if (r.width>200 && r.height>=20 && r.height<=100 && r.y>200) {
                hits.push({x:r.x+r.width/2,y:r.y+r.height/2,w:r.width,h:r.height});
              }
              if (el.shadowRoot) walk(el.shadowRoot);
            }
          };
          const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]');
          walk(dlg||document);
          if (!hits.length) return null;
          hits.sort((a,b)=>b.w-a.w);
          return hits[0];
        }"""
    )
    if hit:
        page.mouse.click(hit["x"], hit["y"])
        page.wait_for_timeout(1100)
        return {"via": "schedule_row", **hit}
    return None


def set_date(page, day: int, month: str, month_short: str, result: dict) -> None:
    trigger = page.locator("tp-yt-paper-dialog ytcp-text-dropdown-trigger")
    if trigger.count():
        trigger.first.click(force=True)
        page.wait_for_timeout(700)
    el = page.locator('tp-yt-paper-input[aria-label="Enter date"] input')
    date_str = f"{day} {month} 2026"
    if el.count():
        el.first.click(force=True)
        page.keyboard.press("Meta+a")
        page.keyboard.type(date_str, delay=35)
        page.keyboard.press("Enter")
        page.wait_for_timeout(500)
        result["date"] = date_str
    page.evaluate(
        """({day, mon}) => {
          const walk=(root)=>{
            for (const el of root.querySelectorAll('[aria-label]')) {
              const al=el.getAttribute('aria-label')||'';
              if (!/2026/.test(al) || !new RegExp(mon,'i').test(al)) continue;
              if (!new RegExp('\\\\b'+day+'\\\\b').test(al)) continue;
              const r=el.getBoundingClientRect();
              if (r.width>10) { el.click(); return al; }
            }
            for (const el of root.querySelectorAll('*')) {
              if (el.shadowRoot) { const x=walk(el.shadowRoot); if (x) return x; }
            }
            return null;
          };
          return walk(document);
        }""",
        {"day": day, "mon": month_short[:3]},
    )
    page.wait_for_timeout(400)
    try:
        page.get_by_text("Schedule as public", exact=True).first.click(force=True, timeout=1200)
    except Exception:
        pass


def set_time(page, time_str: str, result: dict) -> None:
    tloc = page.locator("tp-yt-paper-dialog input")
    for i in range(tloc.count()):
        try:
            v = tloc.nth(i).input_value()
        except Exception:
            continue
        if re.fullmatch(r"\d{1,2}:\d{2}", v or ""):
            tloc.nth(i).click(force=True)
            page.keyboard.press("Meta+a")
            page.keyboard.type(time_str, delay=40)
            page.wait_for_timeout(400)
            page.evaluate(
                """(t) => {
                  const walk=(root)=>{
                    for (const el of root.querySelectorAll('tp-yt-paper-item,[role=option],div,span')) {
                      if ((el.innerText||'').trim()!==t) continue;
                      const r=el.getBoundingClientRect();
                      if (r.width>30 && r.height>10 && r.height<40) { el.click(); return true; }
                    }
                    for (const el of root.querySelectorAll('*')) {
                      if (el.shadowRoot && walk(el.shadowRoot)) return true;
                    }
                    return false;
                  };
                  return walk(document);
                }""",
                time_str,
            )
            result["time"] = time_str
            break
    try:
        page.get_by_text("Schedule as public", exact=True).first.click(force=True, timeout=1200)
    except Exception:
        pass


def read_fields(page) -> dict:
    date = ""
    trig = page.locator("tp-yt-paper-dialog ytcp-text-dropdown-trigger")
    if trig.count():
        date = trig.first.inner_text().strip().replace("\n", " ")
    tval = ""
    for i in range(page.locator("tp-yt-paper-dialog input").count()):
        try:
            v = page.locator("tp-yt-paper-dialog input").nth(i).input_value()
        except Exception:
            continue
        if re.fullmatch(r"\d{1,2}:\d{2}", v or ""):
            tval = v
            break
    return {"date": date, "time": tval}


def click_done(page) -> dict | None:
    try:
        page.get_by_text("Schedule as public", exact=True).first.click(force=True, timeout=800)
        page.wait_for_timeout(300)
    except Exception:
        pass
    try:
        btn = page.get_by_role("button", name="Done", exact=True)
        if btn.count():
            target = btn.last if btn.count() > 1 else btn.first
            if target.is_visible():
                target.click(force=True, timeout=3000)
                page.wait_for_timeout(1800)
                return {"via": "role"}
    except Exception:
        pass
    coords = page.evaluate(
        """() => {
          const cands=[];
          const walk=(root)=>{
            for (const b of root.querySelectorAll('button, ytcp-button, [role=button]')) {
              const t=(b.innerText||b.textContent||'').replace(/\\s+/g,' ').trim();
              if (t!=='Done') continue;
              const r=b.getBoundingClientRect();
              if (r.width>20 && r.height>10 && r.y>300) {
                cands.push({x:r.x+r.width/2,y:r.y+r.height/2,yPos:r.y,
                  dis:!!(b.disabled||b.getAttribute('aria-disabled')==='true')});
              }
            }
            for (const el of root.querySelectorAll('*')) if (el.shadowRoot) walk(el.shadowRoot);
          };
          const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]')
            || document.querySelector('tp-yt-paper-dialog');
          walk(dlg||document);
          if (!cands.length) walk(document);
          cands.sort((a,b)=>b.yPos-a.yPos);
          return cands.find(c=>!c.dis)||cands[0]||null;
        }"""
    )
    if coords:
        page.mouse.click(coords["x"], coords["y"])
        page.wait_for_timeout(1800)
    return coords


def save_edit(page) -> bool:
    try:
        b = page.get_by_role("button", name="Save", exact=True)
        if b.count() and b.first.is_enabled():
            b.first.click(force=True)
            page.wait_for_timeout(3000)
            return True
    except Exception:
        pass
    return False


def schedule_one(page, video_id: str, day: int, month_num: int, time_str: str, tag: str) -> dict:
    month, month_short = MONTHS[month_num]
    result: dict = {
        "id": video_id,
        "ok": False,
        "tag": tag,
        "target": f"{day} {month_short} 2026 {time_str}",
    }
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    skip(page)
    dismiss(page)
    page.screenshot(path=str(AUDIT / f"{tag}_01.png"))

    try:
        open_visibility(page)
    except Exception as e:
        result["open_err"] = str(e)[:200]
        page.get_by_text(re.compile(r"Private|Visibility|Scheduled", re.I)).first.click(
            force=True
        )
        page.wait_for_timeout(1200)

    exp = expand_schedule(page)
    result["expand"] = exp
    page.screenshot(path=str(AUDIT / f"{tag}_02_expanded.png"))
    set_date(page, day, month, month_short, result)
    set_time(page, time_str, result)
    pre = read_fields(page)
    result["pre_done"] = pre
    page.screenshot(path=str(AUDIT / f"{tag}_03_filled.png"))
    result["done"] = click_done(page)
    page.wait_for_timeout(1000)
    result["saved"] = save_edit(page)
    page.wait_for_timeout(2000)

    # Verify
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    skip(page)
    body = page.locator("body").inner_text()
    result["chip_scheduled"] = "Scheduled" in body
    result["still_private"] = "Private" in body and "Scheduled" not in body
    try:
        open_visibility(page)
        expand_schedule(page)
        v = read_fields(page)
        result["verify"] = v
        result["ok"] = bool(
            result["chip_scheduled"]
            and re.search(rf"\b{day}\b", v.get("date") or "")
            and re.search(month_short, v.get("date") or "", re.I)
            and (v.get("time") or "").startswith(time_str[:4] if len(time_str) >= 4 else time_str)
        )
        if not result["ok"] and result["chip_scheduled"]:
            # Accept scheduled chip + matching day in verify date or body
            result["ok"] = bool(
                re.search(rf"\b{day}\b", (v.get("date") or "") + body)
                and re.search(month_short[:3], (v.get("date") or "") + body, re.I)
            )
        click_done(page)
    except Exception as e:
        result["verify_err"] = str(e)[:200]
        result["ok"] = result["chip_scheduled"]

    page.screenshot(path=str(AUDIT / f"{tag}_04_verify.png"))
    result["body_snip"] = [
        ln.strip()
        for ln in body.splitlines()
        if any(k in ln for k in ("Scheduled", month_short, "Aug", "Jul", time_str, "Private", "Public"))
    ][:12]
    return result


def parse_iso(iso: str) -> tuple[int, int, str]:
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})T(\d{2}:\d{2})", iso)
    if not m:
        return 6, 8, "19:00"
    return int(m.group(3)), int(m.group(2)), m.group(4)


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    data = json.loads(FINISH.read_text()) if FINISH.exists() else {}
    summary: dict = {"long": None, "shorts": [], "ok": False}

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 1000},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        print("Verify/force long-form schedule…", flush=True)
        long_res = schedule_one(page, LONG_ID, 6, 8, "19:00", "long")
        summary["long"] = long_res
        print(json.dumps(long_res, indent=2), flush=True)

        for s in data.get("shorts", []):
            vid = s.get("video_id")
            if not vid:
                continue
            day, month_num, t = parse_iso(s.get("schedule_iso", ""))
            print(f"Force-schedule Short {s.get('id')} {vid} → {day} {MONTHS[month_num][1]} {t}…", flush=True)
            try:
                r = schedule_one(page, vid, day, month_num, t, f"s{s['id']}")
                r["title"] = s.get("title")
                summary["shorts"].append(r)
                print(f"  ok={r.get('ok')} verify={r.get('verify')} chip={r.get('chip_scheduled')}", flush=True)
            except Exception as e:
                err = {"id": s.get("id"), "video_id": vid, "ok": False, "error": str(e)[:400]}
                summary["shorts"].append(err)
                print(f"  ERR {e}", flush=True)
            OUT.write_text(json.dumps(summary, indent=2) + "\n")

        ctx.close()

    summary["ok"] = bool(summary["long"] and summary["long"].get("ok")) and all(
        s.get("ok") for s in summary["shorts"]
    ) if summary["shorts"] else bool(summary["long"] and summary["long"].get("ok"))
    OUT.write_text(json.dumps(summary, indent=2) + "\n")
    print("\nRESULT", OUT)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
