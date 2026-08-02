#!/usr/bin/env python3
"""Replace Orbit Shorts on YouTube Studio with kinetic-caption v02 files.

For each short in SHORTS_UPLOAD_INDEX:
  1) Delete the old scheduled/private draft (or private a public one)
  2) Upload the v02 file with funnel description + tags
  3) Schedule to the same UK slot (or publish-now if the slot has passed)
  4) Update the index with the new video_id

Channel: Orbit with Ben (UC_esArsDKd3GJvOkeO0DUog)
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

PROFILE = "/Users/ben/code/youtube/.playwright-youtube-profile"
CHANNEL = "UC_esArsDKd3GJvOkeO0DUog"
LONDON = ZoneInfo("Europe/London")
ROOTS = [
    Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens"),
    Path(
        "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
        "002_What-Happens-If-You-Fall-Into-A-Black-Hole"
    ),
    Path(
        "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
        "003_Exoplanets-Strangest-Alien-Worlds"
    ),
]
AUDIT = Path(
    "/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/audits/shorts_v02_replace"
)
OUT = AUDIT / "youtube_replace_v02_result.json"
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


def dismiss(page) -> None:
    for name in ("Got it", "Dismiss", "Not now", "Close"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=600)
        except Exception:
            pass
    try:
        if page.get_by_text("Cancel upload", exact=False).count():
            page.get_by_role("button", name="Close", exact=True).first.click(
                force=True, timeout=1000
            )
    except Exception:
        pass


def delete_video(page, vid: str, sid: str) -> dict:
    """Delete a Studio video. Works best for scheduled/private drafts."""
    r: dict = {"old_id": vid, "deleted": False}
    if not vid:
        return r
    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2800)
    dismiss(page)
    # Options menu (⋮)
    clicked = page.evaluate(
        """() => {
          const walk=(root)=>{
            for (const el of root.querySelectorAll('button,[role=button],ytcp-icon-button')) {
              const al=(el.getAttribute('aria-label')||'').toLowerCase();
              if (al.includes('options') || al.includes('more options') || al.includes('more actions')) {
                const box=el.getBoundingClientRect();
                if (box.width>8) { el.click(); return al; }
              }
            }
            for (const el of root.querySelectorAll('*')) {
              if (el.shadowRoot) { const x=walk(el.shadowRoot); if (x) return x; }
            }
            return null;
          };
          return walk(document);
        }"""
    )
    r["menu"] = clicked
    page.wait_for_timeout(700)
    deleted = page.evaluate(
        """() => {
          const walk=(root)=>{
            for (const el of root.querySelectorAll('tp-yt-paper-item,[role=menuitem],yt-formatted-string,span,div')) {
              const t=(el.innerText||'').trim();
              if (/^Delete(?: forever)?$/i.test(t) || /^Move to trash$/i.test(t)) {
                const box=el.getBoundingClientRect();
                if (box.width>20 && box.height>10) { el.click(); return t; }
              }
            }
            for (const el of root.querySelectorAll('*')) {
              if (el.shadowRoot) { const x=walk(el.shadowRoot); if (x) return x; }
            }
            return null;
          };
          return walk(document);
        }"""
    )
    r["delete_item"] = deleted
    page.wait_for_timeout(900)
    # Confirm
    for label in ("Delete forever", "Delete", "Move to trash", "Confirm"):
        try:
            b = page.get_by_role("button", name=re.compile(rf"^{label}$", re.I))
            if b.count() and b.last.is_visible():
                b.last.click(force=True, timeout=1500)
                r["confirm"] = label
                r["deleted"] = True
                break
        except Exception:
            pass
    page.wait_for_timeout(2500)
    page.screenshot(path=str(AUDIT / f"del_{sid}_{vid}.png"))
    return r


def next_vis(page) -> None:
    for _ in range(14):
        dismiss(page)
        dlg = page.locator("ytcp-uploads-dialog")
        text = dlg.inner_text() if dlg.count() else ""
        if "Save or publish" in text and ("Private" in text or "Public" in text):
            return
        nxt = page.get_by_role("button", name="Next", exact=True)
        if nxt.count() and nxt.first.is_enabled():
            nxt.first.click(force=True)
            page.wait_for_timeout(1400)
        else:
            page.wait_for_timeout(700)


def extract_vid(page) -> str:
    body = page.locator("body").inner_text()
    for pat in (
        r"https://youtu\.be/([A-Za-z0-9_-]{6,})",
        r"/video/([A-Za-z0-9_-]{6,})/",
    ):
        for m in re.finditer(pat, body):
            vid = m.group(1)
            if vid not in ("upload", "shorts"):
                return vid
    m = re.search(r"/video/([A-Za-z0-9_-]{11})/", page.url)
    return m.group(1) if m else ""


def open_upload(page) -> None:
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload?d=ud",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2500)
    dismiss(page)


def upload_one(page, root: Path, item: dict, *, publish_now: bool) -> dict:
    path = root / item["file"]
    if not path.exists():
        raise FileNotFoundError(path)
    open_upload(page)
    inputs = page.locator('input[type="file"]')
    if inputs.count():
        inputs.first.set_input_files(str(path))
    else:
        with page.expect_file_chooser(timeout=25000) as fc:
            page.get_by_role("button", name=re.compile(r"Select files?", re.I)).click(
                force=True
            )
        fc.value.set_files(str(path))

    title_box = page.get_by_role(
        "textbox", name=re.compile(r"title that describes", re.I)
    )
    title_box.wait_for(timeout=240000)
    page.wait_for_timeout(1200)
    title_box.fill(item["title"])
    desc_box = page.get_by_role(
        "textbox", name=re.compile(r"tell viewers about your video", re.I)
    )
    desc_box.click(force=True)
    desc_box.fill(item.get("description") or "")

    try:
        page.get_by_text("No, it's not 'Made for Kids'", exact=False).click(force=True)
    except Exception:
        pass
    try:
        page.get_by_role("radio", name=re.compile(r"Yes, AI was used", re.I)).click(
            force=True, timeout=2500
        )
    except Exception:
        try:
            page.get_by_text("Yes, AI was used", exact=False).click(force=True)
        except Exception:
            pass

    try:
        for _ in range(4):
            page.mouse.wheel(0, 450)
            page.wait_for_timeout(60)
        page.get_by_text("Show more", exact=True).first.click(force=True, timeout=2000)
        page.wait_for_timeout(350)
        tags_box = page.get_by_role("textbox", name=re.compile(r"^Tags$", re.I))
        if tags_box.count():
            tags_box.first.fill(item.get("tags") or "")
            page.keyboard.press("Enter")
    except Exception:
        pass

    # Related / end screen funnel hint lives in description; related video set later if UI allows
    next_vis(page)

    if publish_now:
        page.evaluate(
            """() => {
              const walk=(r)=>{
                if(!r)return false;
                for(const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-radio-button,[role=radio]'):[])){
                  const t=(el.innerText||'').toLowerCase();
                  if(t.includes('public') && !t.includes('schedule')){ el.click(); return true; }
                }
                for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[])){
                  if(el.shadowRoot && walk(el.shadowRoot)) return true;
                }
                return false;
              };
              return walk(document.querySelector('ytcp-uploads-dialog')||document);
            }"""
        )
    else:
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

    saved = False
    for label in ("Publish", "Save", "Done"):
        try:
            btn = page.get_by_role("button", name=label, exact=True)
            if btn.count() and btn.last.is_enabled():
                btn.last.click(force=True)
                saved = True
                break
        except Exception:
            pass
    if not saved:
        raise RuntimeError("no Publish/Save/Done")
    page.wait_for_timeout(9000)
    dismiss(page)
    vid = extract_vid(page)
    try:
        page.locator("ytcp-uploads-dialog #close-button").click(force=True, timeout=2000)
    except Exception:
        try:
            page.get_by_role("button", name="Close", exact=True).last.click(
                force=True, timeout=1500
            )
        except Exception:
            page.keyboard.press("Escape")
    page.wait_for_timeout(800)
    return {
        "id": item["id"],
        "title": item["title"],
        "video_id": vid,
        "url": f"https://youtu.be/{vid}" if vid else "",
        "file": item["file"],
        "publish_now": publish_now,
        "ok": bool(vid),
    }


def expand_schedule(page) -> None:
    page.evaluate(
        """() => {
          const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]');
          const walk=(root)=>{
            for (const el of root.querySelectorAll('*')) {
              const al=el.getAttribute('aria-label')||'';
              const id=el.id||'';
              if (/click to expand/i.test(al) || id==='first-container-expand-button' || id==='second-container-expand-button') {
                const r=el.getBoundingClientRect();
                if (r.width>5) { el.click(); return true; }
              }
              if (el.shadowRoot && walk(el.shadowRoot)) return true;
            }
            return false;
          };
          return walk(dlg||document);
        }"""
    )
    page.wait_for_timeout(900)
    try:
        page.get_by_text("Schedule", exact=True).first.click(force=True)
    except Exception:
        pass
    page.wait_for_timeout(500)


def set_date_time(page, day: int, month_num: int, time_str: str, result: dict) -> None:
    month, month_short = MONTHS[month_num]
    date_str = f"{day} {month} 2026"
    trigger = page.locator("tp-yt-paper-dialog ytcp-text-dropdown-trigger")
    if trigger.count():
        trigger.first.click(force=True)
        page.wait_for_timeout(500)
    el = page.locator('tp-yt-paper-input[aria-label="Enter date"] input')
    if el.count():
        el.first.click(force=True)
        page.keyboard.press("Meta+a")
        page.keyboard.type(date_str, delay=24)
        page.keyboard.press("Enter")
        page.wait_for_timeout(400)
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
    page.wait_for_timeout(300)
    tloc = page.locator("tp-yt-paper-dialog input")
    for i in range(tloc.count()):
        try:
            v = tloc.nth(i).input_value()
        except Exception:
            continue
        if re.fullmatch(r"\d{1,2}:\d{2}", v or ""):
            tloc.nth(i).click(force=True)
            page.keyboard.press("Meta+a")
            page.keyboard.type(time_str, delay=28)
            page.wait_for_timeout(250)
            result["time"] = time_str
            break
    try:
        page.get_by_text("Schedule as public", exact=True).first.click(
            force=True, timeout=1000
        )
    except Exception:
        pass


def schedule_one(page, vid: str, day: int, month: int, time_str: str, sid: str) -> dict:
    result: dict = {"id": sid, "video_id": vid, "ok": False}
    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    dismiss(page)
    page.locator("ytcp-video-metadata-visibility").first.scroll_into_view_if_needed()
    page.wait_for_timeout(200)
    page.locator("ytcp-video-metadata-visibility").first.click(force=True)
    page.wait_for_timeout(1200)
    expand_schedule(page)
    set_date_time(page, day, month, time_str, result)
    page.screenshot(path=str(AUDIT / f"sched_{sid}.png"))
    try:
        page.get_by_role("button", name="Done", exact=True).last.click(force=True)
        page.wait_for_timeout(1600)
        result["done"] = True
    except Exception as e:
        result["done_err"] = str(e)[:120]
    try:
        b = page.get_by_role("button", name="Save", exact=True)
        if b.count() and b.first.is_enabled():
            b.first.click(force=True)
            page.wait_for_timeout(3200)
            result["saved"] = True
    except Exception:
        pass
    try:
        vis = page.locator("ytcp-video-metadata-visibility").first.inner_text()
    except Exception:
        vis = ""
    result["visibility"] = vis[:200]
    result["ok"] = "Scheduled" in vis or bool(result.get("date"))
    return result


def set_related(page, vid: str, related: str, sid: str) -> dict:
    """Best-effort related-video funnel on the Shorts editor."""
    out: dict = {"related": related, "ok": False}
    if not vid or not related:
        return out
    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2800)
    dismiss(page)
    try:
        page.get_by_text(re.compile(r"related video|end screen", re.I)).first.click(
            force=True, timeout=3000
        )
        page.wait_for_timeout(800)
    except Exception:
        pass
    # Try add-related search by video id
    try:
        box = page.get_by_role("textbox", name=re.compile(r"search|add video", re.I))
        if box.count():
            box.first.fill(related)
            page.keyboard.press("Enter")
            page.wait_for_timeout(1500)
            page.get_by_role("button", name=re.compile(r"add|select", re.I)).first.click(
                force=True, timeout=2500
            )
            out["ok"] = True
    except Exception as e:
        out["err"] = str(e)[:160]
    try:
        b = page.get_by_role("button", name="Save", exact=True)
        if b.count() and b.first.is_enabled():
            b.first.click(force=True)
            page.wait_for_timeout(2500)
    except Exception:
        pass
    page.screenshot(path=str(AUDIT / f"related_{sid}.png"))
    return out


def parse_slot(item: dict) -> tuple[int, int, str, datetime]:
    iso = item.get("schedule_iso") or ""
    dt = datetime.fromisoformat(iso) if iso else None
    if item.get("schedule"):
        day = int(item["schedule"]["day"])
        month = int(item["schedule"]["month"])
        time_str = item["schedule"]["time"]
    elif dt:
        day, month, time_str = dt.day, dt.month, dt.strftime("%H:%M")
    else:
        day = int(item.get("day") or 1)
        month = int(item.get("month") or 8)
        time_str = item.get("time") or "12:30"
        dt = datetime(2026, month, day, *map(int, time_str.split(":")), tzinfo=LONDON)
    if dt is None:
        hh, mm = map(int, time_str.split(":"))
        dt = datetime(2026, month, day, hh, mm, tzinfo=LONDON)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=LONDON)
    return day, month, time_str, dt


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    only = set(sys.argv[1:])  # optional project folder name filters
    now = datetime.now(LONDON)
    all_results: list[dict] = []

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 900},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        dismiss(page)

        for root in ROOTS:
            if only and root.name not in only:
                continue
            index_path = root / "10_Shorts/SHORTS_UPLOAD_INDEX.json"
            data = json.loads(index_path.read_text())
            long_id = data.get("long_id") or data.get("related_to_long")
            if not long_id:
                m = re.search(
                    r"youtu\.be/([A-Za-z0-9_-]+)",
                    data.get("long_url") or data.get("long_placeholder") or "",
                )
                long_id = m.group(1) if m else ""

            for item in data.get("shorts", []):
                day, month, time_str, dt = parse_slot(item)
                publish_now = dt <= now
                # Public aliens already live: still replace with new upload + publish now,
                # then delete/private the old ID so the funnel asset is the v02 file.
                print(
                    f"[{root.name}] S{item['id']} {item.get('title','')[:40]}… "
                    f"{'PUBLISH NOW' if publish_now else f'SCHEDULE {day}/{month} {time_str}'}",
                    flush=True,
                )
                row: dict = {
                    "project": root.name,
                    "id": item["id"],
                    "old_id": item.get("video_id"),
                    "title": item.get("title"),
                }
                try:
                    row["delete"] = delete_video(page, item.get("video_id") or "", item["id"])
                except Exception as e:
                    row["delete"] = {"error": str(e)[:240]}
                try:
                    up = upload_one(page, root, item, publish_now=publish_now)
                    row["upload"] = up
                    new_id = up.get("video_id") or ""
                    if new_id and not publish_now:
                        row["schedule"] = schedule_one(
                            page, new_id, day, month, time_str, item["id"]
                        )
                    if new_id and long_id:
                        row["related"] = set_related(page, new_id, long_id, item["id"])
                    if new_id:
                        item["old_video_id"] = item.get("video_id")
                        item["video_id"] = new_id
                        item["url"] = f"https://youtu.be/{new_id}"
                        item["visibility"] = "public" if publish_now else "scheduled"
                        item["published_now"] = bool(publish_now)
                        item["caption_style"] = "finalverdict-yellow-white-v02"
                        item["replaced_at"] = now.isoformat()
                    row["ok"] = bool(new_id)
                    print(f"  → {row.get('upload',{}).get('url')}", flush=True)
                except Exception as e:
                    row["ok"] = False
                    row["error"] = str(e)[:400]
                    print(f"  ERR {e}", flush=True)
                    page.screenshot(path=str(AUDIT / f"err_{root.name}_{item['id']}.png"))
                    for _ in range(3):
                        page.keyboard.press("Escape")
                        page.wait_for_timeout(250)
                        dismiss(page)
                all_results.append(row)

            data["updated"] = now.date().isoformat()
            data["v02_replace"] = True
            index_path.write_text(json.dumps(data, indent=2) + "\n")

        ctx.close()

    OUT.write_text(
        json.dumps(
            {"ran_at": now.isoformat(), "ok": sum(1 for r in all_results if r.get("ok")), "results": all_results},
            indent=2,
        )
        + "\n"
    )
    print(OUT)
    print(f"OK {sum(1 for r in all_results if r.get('ok'))}/{len(all_results)}")


if __name__ == "__main__":
    main()
