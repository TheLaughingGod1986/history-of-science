#!/usr/bin/env python3
"""HOS 003 Shorts — schedule on @HistoryOfScienceYT after Premiere videoId exists.

Never Orbit / Oppti. Zero /go/. Never Public-on-finish.
Related ▶ Premiere on every Short.

Usage:
  /tmp/hos-studio-pw-venv/bin/python \\
    02_Video-Projects/003_Invisible-Bones-X-Rays/11_Upload-Package/Schedule/_upload_hos_003_shorts_v01.py \\
    --parent VIDEO_ID
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

PORT = 9460
CDP = f"http://127.0.0.1:{PORT}"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PROFILE = str(Path.home() / ".hos-chrome-youtube-studio")
HOS = "UCXp7HkBIl1LgaznXuZHJyRg"
HANDLE = "@HistoryOfScienceYT"
LONDON = ZoneInfo("Europe/London")
PROJ = Path(
    "/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/"
    "003_Invisible-Bones-X-Rays"
)
SCHED = PROJ / "11_Upload-Package/Schedule"
EV = SCHED / "evidence_2026-09-23_shorts"
TAGS = (SCHED / "hos_003_shorts_tags_v01.txt").read_text().strip()
PARENT_TITLE = "How Did We Discover X-rays?"

JOBS = [
    {
        "slot": "s1",
        "title": "How X-rays Were Discovered by Accident",
        "file": PROJ / "10_Shorts/hos_003_s1_cardboard_glow_v01.mp4",
        "thumb": PROJ / "08_Thumbnail/Selected/hos_003_thumb_s1_accident_v03.jpg",
        "cover": PROJ / "08_Thumbnail/Selected/hos_003_s1_cover_v03.jpg",
        "desc": SCHED / "hos_003_s1_description_v01.txt",
        "day": 25,
        "date_typed": "25 September 2026",
        "time": "11:30",
        "label": "Friday 25 Sep 2026 11:30 Europe/London",
    },
    {
        "slot": "s2",
        "title": "How did Röntgen see bones without cutting",
        "file": PROJ / "10_Shorts/hos_003_s2_bones_no_knife_v01.mp4",
        "thumb": PROJ / "08_Thumbnail/Selected/hos_003_thumb_s2_rontgen_bones_v03.jpg",
        "cover": PROJ / "08_Thumbnail/Selected/hos_003_s2_cover_v03.jpg",
        "desc": SCHED / "hos_003_s2_description_v01.txt",
        "day": 26,
        "date_typed": "26 September 2026",
        "time": "11:30",
        "label": "Saturday 26 Sep 2026 11:30 Europe/London",
    },
    {
        "slot": "s3",
        "title": "The first X-ray showed a wedding ring",
        "file": PROJ / "10_Shorts/hos_003_s3_bertha_ring_v01.mp4",
        "thumb": PROJ / "08_Thumbnail/Selected/hos_003_thumb_s3_wedding_ring_v03.jpg",
        "cover": PROJ / "08_Thumbnail/Selected/hos_003_s3_cover_v03.jpg",
        "desc": SCHED / "hos_003_s3_description_v01.txt",
        "day": 27,
        "date_typed": "27 September 2026",
        "time": "11:30",
        "label": "Sunday 27 Sep 2026 11:30 Europe/London",
    },
]


def log(msg: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now(LONDON).isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    with open(EV / "run.log", "a") as f:
        f.write(line + "\n")


def dump(name: str, obj) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    (EV / name).write_text(json.dumps(obj, indent=2, default=str) + "\n")


def snip(page, n: int = 2500) -> str:
    try:
        return page.inner_text("body")[:n]
    except Exception as e:
        return f"<snip err {e}>"


def dismiss(page) -> None:
    for name in ["Got it", "Dismiss", "Not now", "Close", "No thanks", "Skip", "Done"]:
        try:
            b = page.get_by_role("button", name=re.compile(rf"^{name}$", re.I))
            if b.count() and b.first.is_visible():
                b.first.click(timeout=700, force=True)
        except Exception:
            pass


def is_glue(page) -> bool:
    t = page.title() + "\n" + snip(page, 1200)
    return bool(
        re.search(
            r"Error\s*9|something went wrong|don.?t have permission|"
            r"phone.?verif|confirm you.?re not a bot|unusual traffic",
            t,
            re.I,
        )
    )


def studio_page(ctx):
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    for pg in ctx.pages:
        url = pg.url or ""
        if any(x in url for x in ("facebook.com", "instagram.com")):
            continue
        if "studio.youtube.com" in url:
            return pg
    return page


def ensure_chrome() -> None:
    try:
        urllib.request.urlopen(f"{CDP}/json/version", timeout=1).read()
        log("CDP_UP")
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
    log_path = "/tmp/hos_chrome_9460_003.log"
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
        stdout=open(log_path, "w"),
        stderr=subprocess.STDOUT,
    )
    for _ in range(40):
        time.sleep(0.5)
        try:
            urllib.request.urlopen(f"{CDP}/json/version", timeout=1).read()
            log("CDP_STARTED")
            return
        except Exception:
            pass
    raise SystemExit("chrome_failed_to_start")


def ensure_hos(page) -> dict:
    page.goto(
        f"https://studio.youtube.com/channel/{HOS}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    dismiss(page)
    body = snip(page, 2500)
    url = page.url
    if any(x in url for x in ("accountchooser", "signin", "ServiceLogin", "identifier")):
        return {"ok": False, "reason": "LOGIN_REQUIRED", "url": url, "snip": body[:500]}
    if re.search(r"\bOrbit\b|\bOppti\b", body, re.I) and "History of Science" not in body:
        return {"ok": False, "reason": "WRONG_CHANNEL", "url": url, "snip": body[:500]}
    ok = ("History of Science" in body) or (HOS in url)
    return {"ok": ok, "url": url, "title": page.title(), "snip": body[:500]}


def extract_new_id(page) -> str | None:
    m = re.search(r"/video/([A-Za-z0-9_-]{11})/", page.url)
    if m:
        return m.group(1)
    body = snip(page, 8000)
    for pat in (
        r"https://youtu\.be/([A-Za-z0-9_-]{11})",
        r"youtube\.com/shorts/([A-Za-z0-9_-]{11})",
        r"watch\?v=([A-Za-z0-9_-]{11})",
    ):
        m = re.search(pat, body)
        if m:
            return m.group(1)
    try:
        hrefs = page.evaluate(
            "() => [...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href')||'')"
        )
        for href in hrefs:
            m = re.search(r"(?:youtu\.be/|shorts/|watch\?v=|/video/)([A-Za-z0-9_-]{11})", href)
            if m:
                return m.group(1)
    except Exception:
        pass
    return None


def next_until_visibility(page) -> str:
    for i in range(18):
        dismiss(page)
        text = snip(page, 2500)
        try:
            dlg = page.locator("ytcp-uploads-dialog")
            if dlg.count():
                text = dlg.inner_text()
        except Exception:
            pass
        if re.search(r"Visibility|Save or publish|Schedule", text, re.I) and re.search(
            r"Private|Public|Unlisted", text, re.I
        ):
            return f"vis_{i}"
        nxt = page.get_by_role("button", name=re.compile(r"^Next$", re.I))
        if nxt.count() and nxt.first.is_enabled():
            nxt.first.click(force=True)
            page.wait_for_timeout(1400)
        else:
            break
    return "no_vis"


def click_schedule_radio(page) -> str:
    try:
        page.get_by_text(re.compile(r"^Schedule$", re.I)).first.click(timeout=4000)
        page.wait_for_timeout(800)
        return "text_schedule"
    except Exception:
        pass
    hit = page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>30) return null;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('[role=radio],tp-yt-paper-radio-button,ytcp-dropdown-trigger,ytcp-text-dropdown-trigger,div,span')
              : [])) {
              const t=((el.innerText||'')+' '+(el.getAttribute('aria-label')||''))
                .replace(/\\s+/g,' ').trim();
              if (/Select a date to make your video public/i.test(t)
                  || (/^Schedule$/i.test(t) && t.length<24)) {
                const box=el.getBoundingClientRect();
                if (box.width>20) { el.click(); return t.slice(0,80); }
              }
            }
            for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : [])) {
              if (el.shadowRoot) {
                const x=walk(el.shadowRoot, d+1);
                if (x) return x;
              }
            }
            return null;
          };
          return walk(document.querySelector('ytcp-uploads-dialog') || document);
        }"""
    )
    page.wait_for_timeout(700)
    return hit or "schedule_miss"


def fill_when(page, job: dict) -> dict:
    info: dict = {"day": job["day"], "time": job["time"]}
    date_str = job["date_typed"]
    try:
        el = page.locator("input").filter(has_text=re.compile(r"Sept|date", re.I))
        if el.count():
            el.first.click(timeout=2000)
    except Exception:
        pass
    page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>40) return false;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('ytcp-text-dropdown-trigger,ytcp-dropdown-trigger')
              : [])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (/\\d{1,2}\\s+(Sept|Sep|September)\\s+2026/i.test(t)
                  || /Enter date|Select date/i.test(el.getAttribute('aria-label')||'')) {
                el.click(); return true;
              }
            }
            for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : [])) {
              if (el.shadowRoot && walk(el.shadowRoot, d+1)) return true;
            }
            return false;
          };
          return walk(document);
        }"""
    )
    page.wait_for_timeout(500)
    page.keyboard.type(date_str, delay=40)
    page.keyboard.press("Enter")
    page.wait_for_timeout(700)
    picked = page.evaluate(
        """(day) => {
          let hit=null;
          const walk=(r,d=0)=>{
            if(!r||d>50||hit) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('button,[role=gridcell],div,span') : [])) {
              const t=(el.innerText||'').trim();
              const aria=el.getAttribute('aria-label')||'';
              const box=el.getBoundingClientRect();
              if (box.width<8 || box.height<8 || box.width>110) continue;
              if (t===String(day) || new RegExp('\\\\b'+day+'\\\\b').test(aria)) {
                if (/Sept|Sep|September/i.test(aria) || t===String(day)) {
                  el.click(); hit=aria||t; return;
                }
              }
            }
            for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : [])) {
              if (el.shadowRoot) walk(el.shadowRoot, d+1);
            }
          };
          walk(document); return hit;
        }""",
        job["day"],
    )
    info["date_picked"] = picked
    info["date_typed"] = date_str
    focused = page.evaluate(
        """() => {
          let el=null;
          const walk=(r,d=0)=>{
            if(!r||d>50||el) return;
            for (const inp of (r.querySelectorAll ? r.querySelectorAll('input') : [])) {
              if (/^\\d{1,2}:\\d{2}$/.test(inp.value||'')) { el=inp; return; }
            }
            for (const n of (r.querySelectorAll ? r.querySelectorAll('*') : [])) {
              if (n.shadowRoot) walk(n.shadowRoot, d+1);
            }
          };
          walk(document);
          if (!el) return {ok:false};
          el.focus(); el.select && el.select();
          return {ok:true, old:el.value||''};
        }"""
    )
    info["time_focus"] = focused
    if focused and focused.get("ok"):
        page.keyboard.type(job["time"], delay=40)
        page.keyboard.press("Tab")
        info["time_typed"] = job["time"]
    page.wait_for_timeout(400)
    after = page.evaluate(
        """() => {
          let date='', time='';
          const walk=(r,d=0)=>{
            if(!r||d>40) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('ytcp-text-dropdown-trigger,input,span,div') : [])) {
              const t=(el.innerText||el.value||'').replace(/\\s+/g,' ').trim();
              if (/\\d{1,2}\\s+(Sept|Sep|September)\\s+2026/i.test(t) && t.length<40) date=t;
              if (/^\\d{1,2}:\\d{2}$/.test(t) || /^\\d{1,2}:\\d{2}$/.test(el.value||''))
                time = t || el.value;
            }
            for (const n of (r.querySelectorAll ? r.querySelectorAll('*') : []))
              if (n.shadowRoot) walk(n.shadowRoot, d+1);
          };
          walk(document); return {date, time};
        }"""
    )
    info["after"] = after
    return info


def click_schedule_confirm(page) -> str:
    for name in ("Schedule", "Save", "Done"):
        btn = page.get_by_role("button", name=re.compile(rf"^{name}$", re.I))
        if btn.count() and btn.last.is_enabled():
            btn.last.click(force=True)
            page.wait_for_timeout(4000)
            return name
    hit = page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>40) return null;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('button,ytcp-button,[role=button]') : [])) {
              const t=(el.innerText||'').trim();
              if (/^(Schedule|Publish|Done|Save)$/i.test(t) && !el.disabled) {
                el.click(); return t;
              }
            }
            for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : [])) {
              if (el.shadowRoot) {
                const x=walk(el.shadowRoot, d+1);
                if (x) return x;
              }
            }
            return null;
          };
          return walk(document);
        }"""
    )
    page.wait_for_timeout(3500)
    return hit or ""


def set_related(page, new_id: str, parent: str) -> str:
    page.goto(
        f"https://studio.youtube.com/video/{new_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    dismiss(page)
    body = snip(page, 6000)
    if parent in body or PARENT_TITLE in body:
        return "already_set"
    try:
        for _ in range(12):
            page.mouse.wheel(0, 1400)
            page.wait_for_timeout(200)
        add = page.get_by_text(
            re.compile(r"Add (a )?related video|Select video|Add video", re.I)
        )
        if add.count():
            add.first.click(timeout=4000)
        else:
            page.get_by_text(re.compile(r"Related video", re.I)).first.click(timeout=4000)
        page.wait_for_timeout(1000)
        box = page.locator(
            "tp-yt-paper-input input, input[type='text'], input[aria-label*='Search' i]"
        ).first
        box.click(timeout=4000)
        box.fill(parent)
        page.wait_for_timeout(2200)
        hit = page.get_by_text(
            re.compile(re.escape(PARENT_TITLE) + "|" + re.escape(parent), re.I)
        )
        if hit.count():
            hit.first.click(timeout=5000)
            page.wait_for_timeout(800)
        save = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
        if save.count() and save.first.is_enabled():
            save.first.click(timeout=4000)
            page.wait_for_timeout(2500)
            return "set_saved"
        return "picked_save_grey"
    except Exception as e:
        return f"err:{type(e).__name__}:{e}"


def upload_one(page, job: dict, parent: str) -> dict:
    path = Path(job["file"])
    desc = job["desc"].read_text().replace("PREMIERE_VIDEO_ID_TBD", parent)
    out = dict(job)
    out["file"] = str(path)
    out["thumb"] = str(job["thumb"])
    out["parent"] = parent
    page.goto(
        f"https://studio.youtube.com/channel/{HOS}/videos/upload?d=ud",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2500)
    dismiss(page)
    if is_glue(page):
        out["ok"] = False
        out["glue"] = True
        return out

    inputs = page.locator('input[type="file"]')
    if inputs.count():
        inputs.first.set_input_files(str(path))
        out["attach"] = "locator"
    else:
        with page.expect_file_chooser(timeout=20000) as fc:
            page.get_by_role("button", name=re.compile(r"Select files", re.I)).click(
                force=True
            )
        fc.value.set_files(str(path))
        out["attach"] = "chooser"

    title_box = page.get_by_role("textbox", name=re.compile(r"title|describe", re.I)).first
    title_box.wait_for(timeout=180000)
    try:
        title_box.fill(job["title"])
        out["titleFill"] = "fill"
    except Exception:
        title_box.click()
        page.keyboard.press("Meta+A")
        page.keyboard.type(job["title"])
        out["titleFill"] = "type"

    try:
        dbox = page.get_by_role(
            "textbox", name=re.compile(r"tell viewers|description", re.I)
        ).first
        dbox.click(force=True)
        dbox.fill(desc)
        out["desc"] = True
    except Exception as e:
        out["desc"] = f"err:{type(e).__name__}"

    try:
        page.get_by_text(re.compile(r"No, it.?s not.?Made for Kids", re.I)).click(
            force=True
        )
        out["kids"] = "not_kids"
    except Exception as e:
        out["kids"] = f"err:{type(e).__name__}"

    try:
        show = page.get_by_text(re.compile(r"Show more", re.I))
        if show.count():
            show.first.click(timeout=1500)
            page.wait_for_timeout(400)
        tags = page.get_by_role("textbox", name=re.compile(r"tags", re.I))
        if tags.count():
            tags.first.fill(TAGS)
            out["tags"] = True
    except Exception:
        out["tags"] = False

    thumb = Path(job["thumb"])
    try:
        up = page.get_by_text(
            re.compile(r"Upload file|Upload thumbnail|Custom thumbnail", re.I)
        )
        if up.count() and thumb.exists():
            with page.expect_file_chooser(timeout=6000) as fc:
                up.first.click(force=True)
            fc.value.set_files(str(thumb))
            out["thumbAttempt"] = "chooser"
        else:
            t_inputs = page.locator('input[type="file"]')
            if t_inputs.count() >= 2 and thumb.exists():
                t_inputs.nth(1).set_input_files(str(thumb))
                out["thumbAttempt"] = "input_1"
    except Exception as e:
        out["thumbAttempt"] = f"skip:{type(e).__name__}"

    out["next"] = next_until_visibility(page)
    out["scheduleOpen"] = click_schedule_radio(page)
    page.wait_for_timeout(600)
    out["when"] = fill_when(page, job)
    after = (out["when"] or {}).get("after") or {}
    if not after.get("date"):
        out["ok"] = False
        out["error"] = f"date_not_set:{after}"
        page.screenshot(path=str(EV / f"{job['slot']}_date_fail.png"), full_page=True)
        return out
    out["confirm"] = click_schedule_confirm(page)
    dismiss(page)
    page.wait_for_timeout(2500)
    new_id = extract_new_id(page)
    out["platformPostId"] = new_id
    out["platformUrl"] = f"https://youtube.com/shorts/{new_id}" if new_id else None
    out["uploadUrl"] = page.url
    page.screenshot(path=str(EV / f"{job['slot']}_after_schedule.png"), full_page=True)
    if not new_id:
        out["ok"] = False
        out["error"] = "no_id"
        return out
    out["related"] = set_related(page, new_id, parent)
    out["ok"] = True
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--parent", required=True, help="Premiere videoId")
    ap.add_argument("--only")
    args = ap.parse_args()
    parent = args.parent.strip()
    if len(parent) < 8:
        raise SystemExit("bad parent id")
    EV.mkdir(parents=True, exist_ok=True)
    jobs = JOBS
    if args.only:
        jobs = [j for j in jobs if j["slot"] == args.only]

    result = {
        "ok": False,
        "channel": HANDLE,
        "channelId": HOS,
        "parentId": parent,
        "parentTitle": PARENT_TITLE,
        "affiliate": "none",
        "madeForKids": False,
        "started": datetime.now(LONDON).isoformat(timespec="seconds"),
        "shorts": [],
    }
    ensure_chrome()
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = studio_page(ctx)
        page.bring_to_front()
        hos = ensure_hos(page)
        result["hos"] = hos
        page.screenshot(path=str(EV / "00_hos_boot.png"), full_page=True)
        if not hos.get("ok"):
            result["stopped"] = hos.get("reason") or "HOS_NOT_READY"
            dump("RESULT.json", result)
            log(json.dumps(result)[:1500])
            return 2
        for job in jobs:
            log(f"==== upload {job['slot']} {job['title']} ====")
            if is_glue(page):
                result["stopped"] = "GLUE_BEFORE_UPLOAD"
                break
            try:
                item = upload_one(page, job, parent)
            except Exception as e:
                item = {"slot": job["slot"], "ok": False, "error": f"{type(e).__name__}:{e}"}
                result["shorts"].append(item)
                result["stopped"] = "UPLOAD_EXCEPTION"
                dump("RESULT.json", result)
                break
            result["shorts"].append(item)
            dump("RESULT.json", result)
            if not item.get("ok"):
                result["stopped"] = item.get("error") or "SHORT_FAIL"
                break
        result["finished"] = datetime.now(LONDON).isoformat(timespec="seconds")
        result["ok"] = bool(result["shorts"]) and all(s.get("ok") for s in result["shorts"])
        dump("RESULT.json", result)
        log(f"wrote RESULT.json ok={result['ok']}")
        print(json.dumps(result, indent=2, default=str)[:4000])
        return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
