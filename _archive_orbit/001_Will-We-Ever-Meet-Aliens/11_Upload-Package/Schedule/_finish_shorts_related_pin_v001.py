#!/usr/bin/env python3
"""V001: upload Shorts (private) → schedule → related to long → pin first comment.

Long (public): Mo93x0fxB1Q
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = "/Users/ben/code/youtube/.playwright-youtube-profile"
ROOT = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens"
)
INDEX = json.loads((ROOT / "10_Shorts/SHORTS_UPLOAD_INDEX.json").read_text())
PKG = ROOT / "11_Upload-Package"
CHANNEL = "TBD_CREATE_HISTORY_OF_SCIENCE_CHANNEL"
LONG_ID = INDEX["long_id"]
LONG_TITLE = INDEX["long_title"]
PINNED = (PKG / "Pinned-Comments/aliens_long_pinned-comment_v01.txt").read_text().strip()
OUT = PKG / "Schedule/aliens_shorts_finish_result.json"
AUDIT = PKG / "Schedule/_studio_audit_shorts_v001"

MONTHS = {
    8: ("August", "Aug"),
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
    for name in ("Got it", "Dismiss", "Close", "Not now"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=600)
        except Exception:
            pass


def next_vis(page) -> None:
    for _ in range(12):
        dismiss(page)
        text = (
            page.locator("ytcp-uploads-dialog").inner_text()
            if page.locator("ytcp-uploads-dialog").count()
            else ""
        )
        if "Save or publish" in text or (
            page.get_by_text("Private", exact=False).count() and "Public" in text
        ):
            return
        nxt = page.get_by_role("button", name="Next", exact=True)
        if nxt.count() and nxt.first.is_enabled():
            nxt.first.click(force=True)
            page.wait_for_timeout(1200)
        else:
            break


def extract_vid(page) -> str:
    body = page.locator("body").inner_text()
    for pat in (
        r"https://youtu\.be/([A-Za-z0-9_-]{11})",
        r"/video/([A-Za-z0-9_-]{11})/",
        r"watch\?v=([A-Za-z0-9_-]{11})",
    ):
        m = re.search(pat, body)
        if m and m.group(1) not in ("upload", "shorts"):
            return m.group(1)
    m = re.search(r"/video/([A-Za-z0-9_-]{11})/", page.url)
    return m.group(1) if m else ""


def upload_one(page, item: dict) -> dict:
    path = ROOT / item["file"]
    r: dict = {"id": item["id"], "title": item["title"], "ok": False}
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload?d=ud",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2000)
    dismiss(page)
    inputs = page.locator('input[type="file"]')
    if inputs.count():
        inputs.first.set_input_files(str(path))
    else:
        with page.expect_file_chooser(timeout=20000) as fc:
            page.get_by_role("button", name="Select files").click(force=True)
        fc.value.set_files(str(path))

    title_box = page.get_by_role(
        "textbox", name=re.compile(r"title that describes", re.I)
    )
    title_box.wait_for(timeout=180000)
    title_box.fill(item["title"])
    desc_box = page.get_by_role(
        "textbox", name=re.compile(r"tell viewers about your video", re.I)
    )
    desc_box.click(force=True)
    desc_box.fill(item["description"])
    try:
        page.get_by_text("No, it's not 'Made for Kids'", exact=False).click(force=True)
    except Exception:
        pass
    try:
        page.get_by_role("radio", name=re.compile(r"Yes, AI was used", re.I)).click(
            force=True, timeout=2000
        )
    except Exception:
        pass
    try:
        page.get_by_role("button", name="Show more").click(force=True, timeout=2000)
        page.wait_for_timeout(400)
        page.get_by_role("textbox", name="Tags").fill(item["tags"])
        page.keyboard.press("Enter")
        r["tags"] = True
    except Exception as e:
        r["tags_err"] = str(e)[:120]

    next_vis(page)
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
    page.wait_for_timeout(400)
    page.get_by_role("button", name="Save", exact=True).last.click(force=True)
    page.wait_for_timeout(8000)
    dismiss(page)
    vid = extract_vid(page)
    r["video_id"] = vid
    r["url"] = f"https://youtu.be/{vid}" if vid else ""
    r["ok"] = bool(vid)
    page.screenshot(path=str(AUDIT / f"upload_{item['id']}.png"))
    try:
        page.get_by_role("button", name="Close").click(force=True, timeout=2000)
    except Exception:
        pass
    return r


def open_visibility(page) -> None:
    page.locator("ytcp-video-metadata-visibility").first.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    page.locator("ytcp-video-metadata-visibility").first.click(force=True)
    page.wait_for_timeout(1400)


def expand_schedule(page) -> dict | None:
    dlg = page.get_by_role("dialog", name="Select video privacy")
    text = dlg.inner_text() if dlg.count() else page.locator("body").inner_text()
    if "Schedule as public" in text or re.search(r"\d{1,2} \w{3,9} 2026", text):
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
                hits.push({x:r.x+r.width/2,y:r.y+r.height/2,w:r.width});
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


def set_date_time(page, day: int, month_num: int, time_str: str, result: dict) -> None:
    month, month_short = MONTHS[month_num]
    trigger = page.locator("tp-yt-paper-dialog ytcp-text-dropdown-trigger")
    if trigger.count():
        trigger.first.click(force=True)
        page.wait_for_timeout(700)
    el = page.locator('tp-yt-paper-input[aria-label="Enter date"] input')
    date_str = f"{day} {month} 2026"
    if el.count():
        el.first.click(force=True)
        page.keyboard.press("Meta+a")
        page.keyboard.type(date_str, delay=30)
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
    tloc = page.locator("tp-yt-paper-dialog input")
    for i in range(tloc.count()):
        try:
            v = tloc.nth(i).input_value()
        except Exception:
            continue
        if re.fullmatch(r"\d{1,2}:\d{2}", v or ""):
            tloc.nth(i).click(force=True)
            page.keyboard.press("Meta+a")
            page.keyboard.type(time_str, delay=35)
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


def click_done(page) -> None:
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
                return
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


def schedule_one(page, item: dict, video_id: str) -> dict:
    result: dict = {
        "id": item["id"],
        "video_id": video_id,
        "ok": False,
        "target": item["schedule_iso"],
    }
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    skip(page)
    dismiss(page)
    try:
        open_visibility(page)
    except Exception:
        page.get_by_text(re.compile(r"Private|Visibility|Scheduled", re.I)).first.click(
            force=True
        )
        page.wait_for_timeout(1200)
    result["expand"] = expand_schedule(page)
    set_date_time(page, item["day"], item["month"], item["time"], result)
    click_done(page)
    result["saved"] = save_edit(page)
    page.wait_for_timeout(2000)
    body = page.locator("body").inner_text()
    result["visibility_snip"] = ""
    if "Visibility" in body:
        result["visibility_snip"] = body.split("Visibility", 1)[-1][:180]
    result["ok"] = "Scheduled" in result["visibility_snip"] or "Schedule" in body
    page.screenshot(path=str(AUDIT / f"sched_{item['id']}.png"))
    return result


def set_related(page, sid: str, num: str) -> dict:
    r: dict = {"id": num, "video_id": sid, "ok": False}
    page.goto(
        f"https://studio.youtube.com/video/{sid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    skip(page)
    dismiss(page)
    picker = page.locator("ytcp-shorts-content-links-picker")
    if picker.count():
        picker.first.scroll_into_view_if_needed()
        picker.first.click(force=True)
    else:
        page.get_by_text("Related video", exact=True).first.click(force=True)
    page.wait_for_timeout(1500)
    try:
        page.locator("ytcp-video-pick-dialog").wait_for(timeout=15000)
    except Exception:
        r["error"] = "no_dialog"
        return r
    search = page.locator("ytcp-video-pick-dialog #search-yours")
    if not search.count():
        search = page.get_by_placeholder(re.compile(r"Search your videos", re.I))
    for q in (LONG_TITLE, LONG_ID, "Fermi Paradox", "Aliens"):
        search.first.fill(q)
        page.wait_for_timeout(2500)
        body = page.locator("ytcp-video-pick-dialog").inner_text()
        if "No matching results" not in body:
            break
    else:
        r["error"] = "not_found"
        page.keyboard.press("Escape")
        return r
    cells = page.locator("ytcp-video-pick-dialog ytcp-video-list-cell-video")
    if not cells.count():
        cells = page.locator("ytcp-video-pick-dialog ytcp-entity-card")
    for i in range(cells.count()):
        t = cells.nth(i).inner_text()
        is_short = bool(re.search(r"\b0:\d{2}\b", t)) and not re.search(
            r"\b1[0-9]:\d{2}\b", t
        )
        if (LONG_ID in t or "Fermi" in t or "Aliens" in t or "Alone" in t) and not is_short:
            cells.nth(i).click(force=True)
            r["picked"] = t[:160]
            break
    else:
        r["error"] = "no_cell"
        page.keyboard.press("Escape")
        return r
    page.wait_for_timeout(800)
    for name in ("Done", "Select", "Save"):
        b = page.get_by_role("button", name=name, exact=True)
        if b.count() and b.first.is_visible() and b.first.is_enabled():
            b.first.click(force=True)
            page.wait_for_timeout(800)
            break
    r["saved"] = save_edit(page)
    page.goto(f"https://studio.youtube.com/video/{sid}/edit", wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    body = page.locator("body").inner_text()
    chunk = body.split("Related video", 1)[-1][:250] if "Related video" in body else ""
    r["related_chunk"] = chunk
    r["ok"] = "None" not in chunk[:40] and (
        "Fermi" in chunk or "Aliens" in chunk or "Alone" in chunk or "Orbit" in chunk
    )
    page.screenshot(path=str(AUDIT / f"rel_{num}.png"))
    return r


def pin_first_comment(page) -> dict:
    r: dict = {"ok": False}
    page.goto(
        f"https://studio.youtube.com/video/{LONG_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    skip(page)
    for _ in range(8):
        page.mouse.wheel(0, 700)
        page.wait_for_timeout(200)
    body = page.locator("body").inner_text()
    r["has_add"] = "Add a first comment" in body
    r["snippet"] = body.split("First comment", 1)[-1][:250] if "First comment" in body else ""
    if "Add a first comment" in body:
        page.get_by_text("Add a first comment", exact=False).first.click(force=True)
        page.wait_for_timeout(1200)
        page.keyboard.type(PINNED, delay=3)
        page.wait_for_timeout(400)
        for name in ("Comment", "Save", "Done", "Post"):
            b = page.get_by_role("button", name=name, exact=True)
            if b.count():
                for i in range(b.count() - 1, -1, -1):
                    try:
                        if b.nth(i).is_visible() and b.nth(i).is_enabled():
                            b.nth(i).click(force=True)
                            page.wait_for_timeout(1500)
                            r["confirm"] = name
                            break
                    except Exception:
                        continue
                if r.get("confirm"):
                    break
        if save_edit(page):
            r["saved"] = True
        r["ok"] = True
    else:
        r["already"] = True
        r["ok"] = "silence" in r["snippet"].lower() or "Orbit" in r["snippet"]
    page.screenshot(path=str(AUDIT / "pin_comment.png"), full_page=True)
    return r


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    result: dict = {
        "long_id": LONG_ID,
        "long_url": INDEX["long_url"],
        "uploads": [],
        "schedules": [],
        "related": [],
        "pin": None,
        "ok": False,
    }
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 1000},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        # 1) Upload
        for item in INDEX["shorts"]:
            print(f"UPLOAD {item['id']} {item['title']}…", flush=True)
            try:
                ur = upload_one(page, item)
            except Exception as e:
                ur = {"id": item["id"], "ok": False, "error": str(e)[:300]}
                page.screenshot(path=str(AUDIT / f"upload_{item['id']}_err.png"))
            result["uploads"].append(ur)
            print(f"  → {ur.get('url') or ur}", flush=True)
            OUT.write_text(json.dumps(result, indent=2) + "\n")

        # map ids
        id_by_num = {
            u["id"]: u.get("video_id")
            for u in result["uploads"]
            if u.get("video_id")
        }

        # 2) Schedule
        for item in INDEX["shorts"]:
            vid = id_by_num.get(item["id"])
            if not vid:
                result["schedules"].append({"id": item["id"], "ok": False, "error": "no_id"})
                continue
            print(f"SCHEDULE {item['id']} {vid} → {item['schedule_iso']}…", flush=True)
            try:
                sr = schedule_one(page, item, vid)
            except Exception as e:
                sr = {"id": item["id"], "video_id": vid, "ok": False, "error": str(e)[:300]}
            result["schedules"].append(sr)
            print(f"  → ok={sr.get('ok')} {sr.get('visibility_snip','')[:80]}", flush=True)
            OUT.write_text(json.dumps(result, indent=2) + "\n")

        # 3) Related (long is public)
        for item in INDEX["shorts"]:
            vid = id_by_num.get(item["id"])
            if not vid:
                result["related"].append({"id": item["id"], "ok": False, "error": "no_id"})
                continue
            print(f"RELATED {item['id']} → {LONG_ID}…", flush=True)
            try:
                rr = set_related(page, vid, item["id"])
            except Exception as e:
                rr = {"id": item["id"], "video_id": vid, "ok": False, "error": str(e)[:300]}
            result["related"].append(rr)
            print(f"  → ok={rr.get('ok')} {rr.get('error') or rr.get('picked','')[:60]}", flush=True)
            OUT.write_text(json.dumps(result, indent=2) + "\n")

        # 4) Pin first comment on long
        print("PIN first comment on long…", flush=True)
        try:
            result["pin"] = pin_first_comment(page)
        except Exception as e:
            result["pin"] = {"ok": False, "error": str(e)[:300]}
        print(f"  → {result['pin']}", flush=True)

        ctx.close()

    result["ok"] = (
        all(u.get("ok") for u in result["uploads"])
        and all(s.get("ok") for s in result["schedules"])
        and all(r.get("ok") for r in result["related"])
        and bool(result.get("pin", {}).get("ok"))
    )
    # persist video ids back into index
    for item in INDEX["shorts"]:
        item["video_id"] = id_by_num.get(item["id"], "")
    (ROOT / "10_Shorts/SHORTS_UPLOAD_INDEX.json").write_text(
        json.dumps(INDEX, indent=2) + "\n"
    )
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print("RESULT", OUT, "ok=", result["ok"])
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
