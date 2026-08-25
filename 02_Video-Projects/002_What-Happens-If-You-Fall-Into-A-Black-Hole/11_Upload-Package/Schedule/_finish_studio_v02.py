#!/usr/bin/env python3
"""Finish Video 002 in YouTube Studio: schedule long-form + upload/schedule Shorts.

Proven patterns from OpptiAI V010 force-schedule / shorts upload.
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = "/Users/ben/code/youtube/.playwright-youtube-profile"
ROOT = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "002_What-Happens-If-You-Fall-Into-A-Black-Hole"
)
CHANNEL = "TBD_CREATE_HISTORY_OF_SCIENCE_CHANNEL"
LONG_ID = "n7CbJrOCnU0"
LONG_URL = f"https://youtu.be/{LONG_ID}"
AUDIT = ROOT / "11_Upload-Package/Schedule/_studio_finish"
OUT = ROOT / "11_Upload-Package/Schedule/blackhole_studio_finish_result.json"
INDEX = json.loads((ROOT / "10_Shorts/SHORTS_UPLOAD_INDEX.json").read_text())

DAY = 6
MONTH = "August"
MONTH_SHORT = "Aug"
TIME = "19:00"
DATE_STR = f"{DAY} {MONTH} 2026"


def skip(page) -> None:
    try:
        page.get_by_role("link", name=re.compile(r"Skip", re.I)).click(timeout=1000)
    except Exception:
        pass


def dismiss(page) -> None:
    page.evaluate(
        "() => document.querySelectorAll('tp-yt-iron-overlay-backdrop').forEach(e => e.remove())"
    )
    for name in ("Got it", "Dismiss", "Not now", "Close"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=700)
        except Exception:
            pass
    try:
        if page.get_by_text("Auto-generated thumbnail", exact=False).count():
            page.get_by_role("button", name="Cancel", exact=True).click(force=True, timeout=1000)
    except Exception:
        pass


def open_visibility(page) -> None:
    page.locator("ytcp-video-metadata-visibility").first.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    page.locator("ytcp-video-metadata-visibility").first.click(force=True)
    page.wait_for_timeout(1400)


def expand_schedule(page) -> dict | None:
    body = page.locator("body").inner_text()
    if "Schedule as public" in body or re.search(r"\d{1,2} \w{3,9} 2026", body):
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


def set_date_time(page, result: dict, day: int, month: str, time_str: str) -> None:
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
        """({day, month}) => {
          const walk=(root)=>{
            for (const el of root.querySelectorAll('[aria-label]')) {
              const al=el.getAttribute('aria-label')||'';
              if (!/2026/.test(al)) continue;
              if (!new RegExp(month, 'i').test(al)) continue;
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
        {"day": day, "month": month[:3]},
    )
    page.wait_for_timeout(400)

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


def save_edit(page) -> None:
    try:
        b = page.get_by_role("button", name="Save", exact=True)
        if b.count() and b.first.is_enabled():
            b.first.click(force=True)
            page.wait_for_timeout(2500)
    except Exception:
        pass


def schedule_video(page, video_id: str, day: int, month: str, time_str: str, tag: str) -> dict:
    result: dict = {"id": video_id, "ok": False, "tag": tag}
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    skip(page)
    dismiss(page)
    page.screenshot(path=str(AUDIT / f"{tag}_01_edit.png"))
    try:
        open_visibility(page)
    except Exception as e:
        result["open_vis_err"] = str(e)[:200]
        # fallback: click Private/Draft chip text
        page.get_by_text(re.compile(r"Draft|Private|Visibility", re.I)).first.click(force=True)
        page.wait_for_timeout(1200)
    expand_schedule(page)
    page.screenshot(path=str(AUDIT / f"{tag}_02_expanded.png"))
    set_date_time(page, result, day, month, time_str)
    page.screenshot(path=str(AUDIT / f"{tag}_03_datetime.png"))
    click_done(page)
    page.wait_for_timeout(1500)
    dismiss(page)
    save_edit(page)
    page.wait_for_timeout(2000)
    page.screenshot(path=str(AUDIT / f"{tag}_04_done.png"))
    body = page.locator("body").inner_text()
    result["has_schedule"] = "Schedule" in body or "scheduled" in body.lower()
    result["body_snip"] = "\n".join(
        [
            ln.strip()
            for ln in body.splitlines()
            if any(k in ln for k in ("Schedule", "Aug", "Jul", "19:", "12:", "Private", "Public", "Draft"))
        ][:20]
    )
    result["ok"] = True
    return result


def next_to_visibility(page) -> None:
    for _ in range(12):
        dismiss(page)
        text = ""
        try:
            text = page.locator("ytcp-uploads-dialog").inner_text(timeout=2000)
        except Exception:
            text = page.locator("body").inner_text()
        if "Save or publish" in text and "Private" in text and "Public" in text:
            return
        nxt = page.get_by_role("button", name="Next", exact=True)
        if nxt.count() and nxt.first.is_enabled():
            nxt.first.click(force=True)
            page.wait_for_timeout(1500)
        else:
            break


def extract_vid(page, known: set[str]) -> str:
    body = page.locator("body").inner_text()
    for pat in (
        r"https://youtu\.be/([A-Za-z0-9_-]+)",
        r"youtube\.com/watch\?v=([A-Za-z0-9_-]+)",
        r"/video/([A-Za-z0-9_-]{6,})/",
    ):
        for m in re.finditer(pat, body):
            vid = m.group(1)
            if vid not in known and vid not in ("upload", "shorts"):
                return vid
    m = re.search(r"/video/([A-Za-z0-9_-]{6,})/", page.url)
    return m.group(1) if m else ""


def upload_short_private(page, item: dict, known: set[str]) -> dict:
    path = ROOT / item["file"]
    desc = item["description"].replace("{{LONG_VIDEO_URL}}", LONG_URL)
    result = {"id": item["id"], "title": item["title"], "ok": False, "schedule_iso": item["schedule_iso"]}
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload?d=ud",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2500)
    skip(page)
    dismiss(page)

    inputs = page.locator('input[type="file"]')
    if inputs.count():
        inputs.first.set_input_files(str(path))
    else:
        # Create → Upload videos
        try:
            page.get_by_role("button", name=re.compile(r"^Create$")).click(force=True)
            page.wait_for_timeout(600)
            page.get_by_text(re.compile(r"Upload videos", re.I)).click(force=True)
            page.wait_for_timeout(1000)
        except Exception:
            pass
        inputs = page.locator('input[type="file"]')
        if inputs.count():
            inputs.first.set_input_files(str(path))
        else:
            with page.expect_file_chooser(timeout=30000) as fc:
                page.get_by_role("button", name="Select files").click(force=True)
            fc.value.set_files(str(path))

    title_box = page.get_by_role("textbox", name=re.compile(r"title that describes", re.I))
    title_box.wait_for(timeout=240000)
    page.wait_for_timeout(1500)
    title_box.fill(item["title"])
    desc_box = page.get_by_role("textbox", name=re.compile(r"tell viewers about your video", re.I))
    desc_box.click(force=True)
    desc_box.fill(desc)
    try:
        page.get_by_text("No, it's not 'Made for Kids'", exact=False).click(force=True)
    except Exception:
        pass
    try:
        page.get_by_role("radio", name=re.compile(r"Yes, AI was used", re.I)).click(
            force=True, timeout=2500
        )
    except Exception:
        pass

    dismiss(page)
    page.screenshot(path=str(AUDIT / f"short_{item['id']}_details.png"))
    next_to_visibility(page)
    dismiss(page)

    page.evaluate(
        """() => {
          const walk=(r)=>{
            if(!r)return false;
            for(const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-radio-button,[role=radio]'):[])){
              const t=(el.innerText||'').toLowerCase();
              if(t.includes('private') && !t.includes('schedule')){ el.click(); return true; }
            }
            for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[])){
              if(el.shadowRoot && walk(el.shadowRoot)) return true;
            }
            return false;
          };
          return walk(document.querySelector('ytcp-uploads-dialog')||document);
        }"""
    )
    page.wait_for_timeout(500)

    # Footer Save
    coords = page.evaluate(
        """() => {
          let best=null;
          const walk=(root)=>{
            if(!root)return;
            for(const b of (root.querySelectorAll?root.querySelectorAll('button,ytcp-button,[role=button]'):[])){
              const t=(b.innerText||'').replace(/\\s+/g,' ').trim();
              if(t!=='Save') continue;
              const r=b.getBoundingClientRect();
              if(r.width>20&&r.height>8&&r.y>500){
                const score=r.y*1000+r.width;
                if(!best||score>best.score) best={x:r.x+r.width/2,y:r.y+r.height/2,score};
              }
            }
            for(const el of (root.querySelectorAll?root.querySelectorAll('*'):[])){
              if(el.shadowRoot) walk(el.shadowRoot);
            }
          };
          walk(document.querySelector('ytcp-uploads-dialog')||document);
          return best;
        }"""
    )
    if coords:
        page.mouse.click(coords["x"], coords["y"])
    else:
        page.get_by_role("button", name="Save", exact=True).last.click(force=True)
    page.wait_for_timeout(9000)
    dismiss(page)
    page.screenshot(path=str(AUDIT / f"short_{item['id']}_saved.png"))

    vid = extract_vid(page, known)
    if not vid:
        # Content list fallback
        try:
            page.get_by_role("button", name="Close").click(force=True, timeout=2000)
        except Exception:
            pass
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/short",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3000)
        body = page.locator("body").inner_text()
        if item["title"][:20] in body:
            # grab first unknown youtu.be near title is hard; use links
            vids = re.findall(r"/video/([A-Za-z0-9_-]{6,})/", page.content())
            for v in vids:
                if v not in known:
                    vid = v
                    break
    result["video_id"] = vid
    result["url"] = f"https://youtu.be/{vid}" if vid else ""
    result["ok"] = bool(vid)
    if vid:
        known.add(vid)
    try:
        page.get_by_role("button", name="Close").click(force=True, timeout=1500)
    except Exception:
        pass
    return result


def parse_schedule_iso(iso: str) -> tuple[int, str, str]:
    # 2026-08-06T21:00:00+01:00
    m = re.match(r"2026-(\d{2})-(\d{2})T(\d{2}:\d{2})", iso)
    if not m:
        return DAY, MONTH, TIME
    month_num = int(m.group(1))
    day = int(m.group(2))
    t = m.group(3)
    months = [
        "",
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    return day, months[month_num], t


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    summary: dict = {
        "long_id": LONG_ID,
        "long_url": LONG_URL,
        "long_schedule": None,
        "shorts": [],
        "ok": False,
    }
    known = {LONG_ID}

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 1000},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        print("Scheduling long-form…", flush=True)
        long_res = schedule_video(page, LONG_ID, DAY, MONTH, TIME, "long")
        summary["long_schedule"] = long_res
        print(json.dumps(long_res, indent=2), flush=True)

        # Save after schedule
        try:
            page.get_by_role("button", name="Save", exact=True).first.click(force=True)
            page.wait_for_timeout(2000)
        except Exception:
            pass

        for item in INDEX["shorts"]:
            print(f"Uploading Short {item['id']} {item['title']}…", flush=True)
            try:
                up = upload_short_private(page, item, known)
                summary["shorts"].append(up)
                print(f"  uploaded {up.get('url')}", flush=True)
                if up.get("video_id"):
                    day, month, t = parse_schedule_iso(item["schedule_iso"])
                    print(f"  scheduling Short {item['id']} → {day} {month} {t}…", flush=True)
                    sch = schedule_video(page, up["video_id"], day, month, t, f"s{item['id']}")
                    up["schedule"] = sch
                    print(f"  schedule ok={sch.get('ok')} {sch.get('body_snip','')[:120]}", flush=True)
            except Exception as e:
                err = {"id": item["id"], "ok": False, "error": str(e)[:400]}
                summary["shorts"].append(err)
                print(f"  ERR {e}", flush=True)
                page.screenshot(path=str(AUDIT / f"short_{item['id']}_err.png"))

        ctx.close()

    summary["ok"] = bool(summary["long_schedule"] and summary["long_schedule"].get("ok"))
    OUT.write_text(json.dumps(summary, indent=2) + "\n")
    print("\nRESULT", OUT)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
