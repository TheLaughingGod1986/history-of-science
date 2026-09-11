#!/usr/bin/env python3
"""Upload HOS 002 punch Shorts + live-lock covers. Re-apply long thumb A.

@HistoryOfScienceYT only. Zero /go/. Never Public on finish — Schedule 11:30 London.
Related ▶ AL_-qlWko_g. Do not lead the channel with a Short.
"""
from __future__ import annotations

import json
import re
import subprocess
import time
import traceback
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

PORT = 9460
CDP = f"http://127.0.0.1:{PORT}"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PROFILE = str(Path.home() / ".hos-chrome-youtube-studio")
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"
HANDLE = "@HistoryOfScienceYT"
LONG_ID = "AL_-qlWko_g"
LONG_TITLE = "How Did We Discover the Periodic Table?"
LONDON = ZoneInfo("Europe/London")
TIME = "11:30"

PROJ = Path(__file__).resolve().parents[2]
PKG = PROJ / "11_Upload-Package"
EV = PKG / "Schedule/evidence_2026-09-11_shorts"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"
SHORTS_DIR = PROJ / "10_Shorts"
COVERS = PROJ / "08_Thumbnail/Shorts"
LONG_THUMB = PROJ / "08_Thumbnail/Selected/hos_002_thumb_A_gallium_live_v02.jpg"
JOBS = json.loads((PKG / "Shorts/SHORTS_LISTINGS_v01.json").read_text())["items"]

TAGS = [
    "How Did We Discover the Periodic Table?",
    "periodic table history",
    "dmitri mendeleev",
    "mendeleev",
    "predicted elements",
    "gallium",
    "scandium",
    "germanium",
    "atomic weight",
    "history of science",
    "history of chemistry",
    "missing elements",
    "empty chairs",
    "science shorts",
    "chemistry history",
]


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
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    dest = EV / name
    try:
        page.screenshot(path=str(dest), full_page=False)
        try:
            (ART / name).write_bytes(dest.read_bytes())
        except Exception:
            pass
        return str(dest)
    except Exception as e:
        log(f"shot_err {name}: {e}")
        return ""


def snip(page, n: int = 2500) -> str:
    try:
        return page.inner_text("body")[:n]
    except Exception as e:
        return f"<snip err {e}>"


def dlg_text(page, n: int = 4000) -> str:
    try:
        dlg = page.locator("ytcp-uploads-dialog")
        if dlg.count():
            return dlg.inner_text()[:n]
    except Exception:
        pass
    return snip(page, n)


def dismiss(page) -> None:
    for name in ["Got it", "Dismiss", "Not now", "No thanks", "Skip"]:
        try:
            b = page.get_by_role("button", name=re.compile(rf"^{name}$", re.I))
            if b.count() and b.first.is_visible():
                b.first.click(timeout=500, force=True)
        except Exception:
            pass
    try:
        if page.locator("ytcp-uploads-dialog").count():
            return
        page.keyboard.press("Escape")
    except Exception:
        pass


def studio_page(ctx):
    for page in ctx.pages:
        url = page.url or ""
        if "facebook.com" in url or "instagram.com" in url:
            continue
        if "studio.youtube.com" in url:
            return page
    page = ctx.new_page()
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    return page


def click_shadow_text(page, pattern: str) -> str | None:
    return page.evaluate(
        """(pattern) => {
          const re = new RegExp(pattern, 'i');
          const walk=(r,d=0)=>{
            if(!r||d>40) return null;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('button,ytcp-button,[role=button],tp-yt-paper-item,yt-formatted-string,div,span')
              : [])) {
              const t=((el.innerText||'')+' '+(el.getAttribute('aria-label')||''))
                .replace(/\\s+/g,' ').trim();
              if (re.test(t) && t.length<48) {
                const box=el.getBoundingClientRect();
                if (box.width>20 && box.height>10) { el.click(); return t.slice(0,60); }
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
        }""",
        pattern,
    )


def file_input_count(page) -> int:
    return int(
        page.evaluate(
            """() => {
              let n=0;
              const walk=(r,d=0)=>{
                if(!r||d>40) return;
                n += (r.querySelectorAll ? r.querySelectorAll('input[type=file]').length : 0);
                for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
                  if (el.shadowRoot) walk(el.shadowRoot, d+1);
              };
              walk(document); return n;
            }"""
        )
        or 0
    )


def chrome_up() -> bool:
    try:
        urllib.request.urlopen(f"{CDP}/json/version", timeout=2).read()
        return True
    except Exception:
        return False


def ensure_chrome() -> None:
    if chrome_up():
        log("chrome_already_up")
        return
    raise RuntimeError("HOS Chrome CDP :9460 is down — do not relaunch from this script")


def probe(path: Path) -> float:
    r = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(path),
        ],
        check=True, capture_output=True, text=True,
    )
    return float(r.stdout.strip())


def open_upload(page) -> dict:
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2500)
    dismiss(page)
    info: dict = {}
    if file_input_count(page):
        info["via"] = "upload_url"
        return info
    click_shadow_text(page, r"^Create$")
    page.wait_for_timeout(700)
    click_shadow_text(page, r"^Upload videos?$")
    page.wait_for_timeout(1800)
    info["fileInputs"] = file_input_count(page)
    return info


def attach_file(page, path: Path) -> dict:
    info: dict = {"path": str(path), "bytes": path.stat().st_size}
    loc = page.locator('input[type="file"]')
    if loc.count():
        try:
            loc.first.set_input_files(str(path))
            info["ok"] = True
            info["via"] = "locator"
            return info
        except Exception as e:
            info["locator_err"] = f"{type(e).__name__}:{e}"
    try:
        session = page.context.new_cdp_session(page)
        ev = session.send(
            "Runtime.evaluate",
            {
                "expression": """(() => {
                  const walk=(r,d=0)=>{
                    if(!r||d>50) return null;
                    if (r.querySelector) {
                      const inp=r.querySelector('input[type=file]');
                      if (inp) return inp;
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
                })()"""
            },
        )
        obj = (ev.get("result") or {}).get("objectId")
        if not obj:
            info["ok"] = False
            info["reason"] = "no_file_input"
            return info
        session.send("DOM.setFileInputFiles", {"files": [str(path)], "objectId": obj})
        info["ok"] = True
        info["via"] = "cdp"
        return info
    except Exception as e:
        info["ok"] = False
        info["err"] = f"{type(e).__name__}:{e}"
        return info


def fill_title_desc(page, title: str, desc: str) -> dict:
    info: dict = {}
    box = page.get_by_role("textbox", name=re.compile(r"title|describe", re.I)).first
    box.wait_for(timeout=180000)
    try:
        box.fill(title)
        info["title"] = "fill"
    except Exception:
        box.click()
        page.keyboard.press("Meta+A")
        page.keyboard.type(title, delay=10)
        info["title"] = "type"
    try:
        d = page.get_by_role("textbox", name=re.compile(r"tell viewers|description", re.I)).first
        d.click(force=True)
        d.fill(desc)
        info["desc"] = True
    except Exception as e:
        info["desc"] = f"err:{type(e).__name__}"
    return info


def set_not_kids(page) -> str:
    try:
        page.get_by_text(re.compile(r"No, it.?s not.?Made for Kids", re.I)).click(force=True)
        return "no"
    except Exception as e:
        t = dlg_text(page, 1500)
        if re.search(r"not.?Made for Kids", t, re.I):
            return "already"
        return f"err:{type(e).__name__}"


def set_tags(page, extra: str) -> dict:
    blob = ", ".join([extra] + TAGS)
    if len(blob) > 480:
        blob = blob[:480].rsplit(",", 1)[0]
    info: dict = {"chars": len(blob)}
    try:
        for _ in range(5):
            page.mouse.wheel(0, 500)
            page.wait_for_timeout(60)
        more = page.get_by_text("Show more", exact=True)
        if more.count():
            more.first.click(force=True, timeout=1500)
            page.wait_for_timeout(300)
        box = page.get_by_role("textbox", name=re.compile(r"^Tags$", re.I))
        if box.count():
            box.first.click(force=True)
            page.keyboard.press("Meta+A")
            page.keyboard.press("Backspace")
            box.first.fill(blob)
            page.keyboard.press("Enter")
            info["ok"] = True
        else:
            info["ok"] = False
    except Exception as e:
        info["ok"] = False
        info["err"] = f"{type(e).__name__}"
    return info


def set_image(page, path: Path) -> dict:
    info: dict = {"file": path.name}
    loc = page.locator('input[type="file"]')
    for i in range(loc.count()):
        try:
            acc = (loc.nth(i).get_attribute("accept") or "").lower()
            if "image" in acc or "jpeg" in acc or "jpg" in acc or "png" in acc:
                loc.nth(i).set_input_files(str(path))
                info["ok"] = True
                info["via"] = f"input_{i}"
                page.wait_for_timeout(1500)
                return info
        except Exception as e:
            info[f"err_{i}"] = type(e).__name__
    try:
        up = page.get_by_text(re.compile(r"Upload file|Upload thumbnail|Custom thumbnail", re.I))
        if up.count():
            with page.expect_file_chooser(timeout=8000) as fc:
                up.first.click(force=True)
            fc.value.set_files(str(path))
            info["ok"] = True
            info["via"] = "chooser"
            page.wait_for_timeout(1500)
            return info
    except Exception as e:
        info["chooser_err"] = type(e).__name__
    info["ok"] = False
    return info


def next_until_visibility(page) -> str:
    for i in range(18):
        dismiss(page)
        text = dlg_text(page, 3500)
        on_vis = bool(
            re.search(r"Save or publish|When will (your|this) video", text, re.I)
            or (
                re.search(r"\bPrivate\b", text)
                and re.search(r"\bPublic\b", text)
                and re.search(r"\bSchedule\b", text)
            )
        )
        if on_vis:
            return f"vis_{i}"
        nxt = page.get_by_role("button", name=re.compile(r"^Next$", re.I))
        clicked = False
        if nxt.count() and nxt.first.is_enabled():
            nxt.first.click(force=True)
            clicked = True
        if not clicked:
            clicked = bool(click_shadow_text(page, r"^Next$"))
        page.wait_for_timeout(1400 if clicked else 700)
    return "no_vis"


def open_schedule(page) -> str:
    try:
        loc = page.get_by_text("Select a date to make your video public", exact=False)
        if loc.count():
            loc.first.click(force=True, timeout=4000)
            page.wait_for_timeout(900)
            return "select_date_copy"
    except Exception:
        pass
    return click_shadow_text(page, r"^Schedule$") or ""


def read_schedule_dt(page) -> dict:
    return page.evaluate(
        """() => {
          let date='', time='';
          const walk=(r,d=0)=>{
            if(!r||d>45) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('ytcp-text-dropdown-trigger,ytcp-dropdown-trigger,div,span') : [])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (/^\\d{1,2}\\s+(Sept|Sep|September)\\s+2026$/i.test(t)) date=t;
            }
            for (const inp of (r.querySelectorAll ? r.querySelectorAll('input') : [])) {
              if (/^\\d{1,2}:\\d{2}$/.test(inp.value||'')) time=inp.value;
            }
            for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : [])) {
              if (el.shadowRoot) walk(el.shadowRoot, d+1);
            }
          };
          walk(document);
          return {date, time};
        }"""
    )


def date_is(dt: dict, day: int) -> bool:
    blob = f"{(dt or {}).get('date','')} {(dt or {}).get('time','')}"
    return bool(re.search(rf"\b{day}\s+(Sept|Sep|September)\s+2026", blob, re.I)) and (
        str((dt or {}).get("time") or "").startswith("11:30")
    )


def fill_when(page, day: int) -> dict:
    """Open the Sept 2026 date dropdown, pick `day`, type 11:30. Never leave the default."""
    info: dict = {"day": day, "time": TIME}
    opened = page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>50) return false;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('ytcp-text-dropdown-trigger,ytcp-dropdown-trigger,tp-yt-paper-input')
              : [])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              const aria=el.getAttribute('aria-label')||'';
              if (/\\d{1,2}\\s+(Sept|Sep|September)\\s+2026/i.test(t)
                  || /Enter date|Select date/i.test(aria)) {
                el.click(); return t.slice(0,40) || aria.slice(0,40);
              }
            }
            for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : [])) {
              if (el.shadowRoot) {
                const x=walk(el.shadowRoot, d+1);
                if (x) return x;
              }
            }
            return false;
          };
          return walk(document);
        }"""
    )
    info["date_open"] = opened
    page.wait_for_timeout(700)
    date_str = f"{day} September 2026"
    el = page.locator('tp-yt-paper-input[aria-label="Enter date"] input')
    if el.count():
        el.first.click(force=True)
        page.keyboard.press("Meta+a")
        page.keyboard.type(date_str, delay=25)
        page.keyboard.press("Enter")
        info["date_typed"] = date_str
        page.wait_for_timeout(400)
    else:
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
                  if (box.width<8 || box.height<8 || box.width>90) continue;
                  if (t===String(day)) {
                    el.click(); hit=aria||t; return;
                  }
                }
                for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : [])) {
                  if (el.shadowRoot) walk(el.shadowRoot, d+1);
                }
              };
              walk(document); return hit;
            }""",
            day,
        )
        info["date_picked"] = picked
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
        page.keyboard.press("Meta+a")
        page.keyboard.type(TIME, delay=35)
        page.keyboard.press("Tab")
        info["time_typed"] = TIME
    page.wait_for_timeout(400)
    info["after"] = read_schedule_dt(page)
    return info


def click_schedule_btn(page) -> str:
    """Confirm Schedule. Never click Publish / Public — that would go live now."""
    try:
        done = page.get_by_role("button", name=re.compile(r"^Done$", re.I))
        if page.locator("tp-yt-paper-dialog, ytcp-date-picker").count() and done.count():
            done.first.click(force=True, timeout=1500)
            page.wait_for_timeout(400)
    except Exception:
        pass
    for name in ["Schedule", "Done", "Save"]:
        try:
            btn = page.get_by_role("button", name=re.compile(rf"^{name}$", re.I))
            if btn.count() and btn.last.is_enabled():
                btn.last.click(force=True)
                page.wait_for_timeout(3500)
                return name
        except Exception:
            continue
    hit = click_shadow_text(page, r"^(Schedule|Done)$")
    page.wait_for_timeout(3000)
    return hit or ""


def extract_id(page, skip: set[str]) -> str | None:
    m = re.search(r"/video/([A-Za-z0-9_-]{11})/", page.url)
    if m and m.group(1) not in skip:
        return m.group(1)
    blob = snip(page, 12000) + "\n" + page.url
    for pat in (
        r"youtube\.com/shorts/([A-Za-z0-9_-]{11})",
        r"https://youtu\.be/([A-Za-z0-9_-]{11})",
        r"watch\?v=([A-Za-z0-9_-]{11})",
        r"studio\.youtube\.com/video/([A-Za-z0-9_-]{11})",
    ):
        m = re.search(pat, blob)
        if m and m.group(1) not in skip:
            return m.group(1)
    hrefs = page.evaluate(
        """() => [...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href')||'')"""
    )
    for href in hrefs or []:
        m = re.search(r"/video/([A-Za-z0-9_-]{11})/", href or "")
        if m and m.group(1) not in skip:
            return m.group(1)
    return None


def verify_wall(page) -> bool:
    blob = snip(page, 4000)
    return bool(
        re.search(
            r"verify (it.?s you|your phone)|Unlock more on YouTube|Confirm it.?s you",
            blob,
            re.I,
        )
    )


def related_widget(page) -> str:
    return page.evaluate(
        """() => {
          const t=document.body.innerText||'';
          const m=t.match(/Related video[^\\n]{0,80}/i);
          return m ? m[0].replace(/\\s+/g,' ').trim() : '';
        }"""
    )


def set_related(page, video_id: str) -> str:
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    dismiss(page)
    if verify_wall(page):
        return "phone_verify_wall"
    widget = related_widget(page)
    if (LONG_ID in widget or LONG_TITLE in widget) and not re.search(r"\bNone\b", widget, re.I):
        return "already_or_present"
    try:
        for _ in range(8):
            page.mouse.wheel(0, 900)
            page.wait_for_timeout(200)
        pencil = page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>50) return null;
                for (const el of (r.querySelectorAll
                  ? r.querySelectorAll('ytcp-icon-button,button,[role=button]') : [])) {
                  const a=el.getAttribute('aria-label')||'';
                  if (/related video|Add a related|Select video/i.test(a)) {
                    el.click(); return a.slice(0,60);
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
        add = page.get_by_text(re.compile(r"Add (a )?related video|Select video|Add video", re.I))
        if not pencil and add.count():
            add.first.click(timeout=4000)
        elif not pencil:
            page.get_by_text(re.compile(r"Related video", re.I)).first.click(timeout=4000)
        page.wait_for_timeout(1000)
        box = page.locator(
            "tp-yt-paper-input input, input[type='text'], input[aria-label*='Search' i]"
        ).first
        box.click(timeout=4000)
        box.fill(LONG_ID)
        page.wait_for_timeout(1800)
        hit = page.get_by_text(re.compile(rf"{re.escape(LONG_TITLE)}|{re.escape(LONG_ID)}", re.I))
        if hit.count():
            hit.first.click(timeout=5000)
            page.wait_for_timeout(700)
        save = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
        if save.count() and save.first.is_enabled():
            save.first.click(timeout=4000)
            page.wait_for_timeout(2000)
            return "set_saved"
        return "picked_save_grey"
    except Exception as e:
        return f"err:{type(e).__name__}"


def close_empty_upload(page) -> str:
    try:
        dlg = page.locator("ytcp-uploads-dialog")
        if not dlg.count():
            return "none"
        t = dlg.inner_text()[:400]
        if re.search(r"Select files|Drag and drop", t, re.I) and not re.search(
            r"Checks complete|Checks in progress|Checks pending", t, re.I
        ):
            page.keyboard.press("Escape")
            page.wait_for_timeout(400)
            return "escaped_empty"
        return "busy_leave"
    except Exception as e:
        return f"err:{type(e).__name__}"


def open_edit_visibility(page) -> str:
    try:
        ed = page.get_by_role("button", name=re.compile(r"Edit draft", re.I))
        if ed.count() and ed.first.is_visible():
            ed.first.click(force=True, timeout=3000)
            page.wait_for_timeout(1200)
    except Exception:
        pass
    try:
        vis = page.get_by_text(re.compile(r"^Visibility$", re.I))
        if vis.count():
            vis.first.click(force=True, timeout=3000)
            page.wait_for_timeout(800)
            return "visibility_text"
    except Exception:
        pass
    hit = page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55) return false;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('ytcp-icon-button,button,[role=button]') : [])) {
              const a=el.getAttribute('aria-label')||'';
              if (/edit video visibility status|Visibility/i.test(a)) {
                el.click(); return a.slice(0,60);
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
    page.wait_for_timeout(1200)
    return str(hit or "")


def repair_existing(page, job: dict, video_id: str) -> dict:
    slot = job["slot"]
    cover = COVERS / job["cover"]
    item: dict = {
        "slot": slot,
        "title": job["title"],
        "file": job["file"],
        "cover": job["cover"],
        "dateLabel": job["dateLabel"],
        "platformPostId": video_id,
        "platformUrl": f"https://youtube.com/shorts/{video_id}",
        "repaired": True,
    }
    log(f"==== repair {slot} {video_id} ====")
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    dismiss(page)
    shot(page, f"{slot}_repair_01_edit.png")
    item["kids"] = set_not_kids(page)
    item["thumbEdit"] = set_image(page, cover)
    save = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
    if save.count() and save.first.is_enabled():
        save.first.click(force=True)
        page.wait_for_timeout(1500)
        item["thumbSave"] = "clicked"
    item["openVis"] = open_edit_visibility(page)
    page.wait_for_timeout(800)
    item["scheduleOpen"] = open_schedule(page)
    page.wait_for_timeout(800)
    item["when"] = fill_when(page, job["day"])
    if not date_is(item["when"].get("after") or {}, job["day"]):
        item["whenRetry"] = fill_when(page, job["day"])
        item["when"]["after"] = item["whenRetry"].get("after")
    shot(page, f"{slot}_repair_02_when.png")
    if not date_is(item["when"].get("after") or {}, job["day"]):
        item["error"] = f"date_not_set:{item['when'].get('after')}"
        item["ok"] = False
        return item
    item["confirm"] = click_schedule_btn(page)
    page.wait_for_timeout(2500)
    dismiss(page)
    save2 = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
    if save2.count() and save2.first.is_enabled():
        save2.first.click(force=True)
        page.wait_for_timeout(1500)
        item["visSave"] = "clicked"
    shot(page, f"{slot}_repair_03_after.png")
    item["related"] = set_related(page, video_id)
    shot(page, f"{slot}_repair_04_related.png")
    item["relatedWidget"] = related_widget(page)
    item["ok"] = True
    return item


def apply_long_thumb(page) -> dict:
    info: dict = {"file": LONG_THUMB.name}
    page.goto(
        f"https://studio.youtube.com/video/{LONG_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    dismiss(page)
    shot(page, "00_long_before_thumb.png")
    info["upload"] = set_image(page, LONG_THUMB)
    save = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
    if save.count() and save.first.is_enabled():
        save.first.click(force=True)
        page.wait_for_timeout(2000)
        info["save"] = "clicked"
    else:
        info["save"] = "not_enabled"
    shot(page, "01_long_after_thumb.png")
    info["snip"] = snip(page, 600)
    return info


def description_for(title: str) -> str:
    return (
        f"{title}\n\n"
        f"Watch the full film — {LONG_TITLE}:\n"
        f"https://www.youtube.com/watch?v={LONG_ID}\n\n"
        "History of Science · Discovery. Wonder. Proof. · @HistoryOfScienceYT\n\n"
        "#PeriodicTable #HistoryOfScience #Mendeleev #Science #Shorts"
    )


def upload_one(page, job: dict, skip_ids: set[str]) -> dict:
    slot = job["slot"]
    video = SHORTS_DIR / job["file"]
    cover = COVERS / job["cover"]
    item: dict = {
        "slot": slot,
        "title": job["title"],
        "file": job["file"],
        "cover": job["cover"],
        "dateLabel": job["dateLabel"],
    }
    if not video.exists() or not cover.exists():
        item["error"] = "missing_file"
        return item
    dur = probe(video)
    item["duration"] = dur
    if dur >= 40:
        item["error"] = f"duration_{dur}"
        return item
    log(f"==== {slot} {job['title']} ====")
    item["open"] = open_upload(page)
    shot(page, f"{slot}_01_dialog.png")
    attached = attach_file(page, video)
    item["attach"] = attached
    if not attached.get("ok"):
        item["error"] = "NO_FILE"
        shot(page, f"{slot}_fail_attach.png")
        return item
    page.wait_for_timeout(2500)
    item["details"] = fill_title_desc(page, job["title"], description_for(job["title"]))
    item["kids"] = set_not_kids(page)
    try:
        page.get_by_text(re.compile(r"Yes, AI was used", re.I)).first.click(force=True, timeout=2000)
        item["ai"] = "yes"
    except Exception:
        item["ai"] = "skip"
    item["tags"] = set_tags(page, job["title"])
    item["thumb"] = set_image(page, cover)
    shot(page, f"{slot}_02_details.png")
    item["next"] = next_until_visibility(page)
    shot(page, f"{slot}_03_vis.png")
    item["scheduleOpen"] = open_schedule(page)
    page.wait_for_timeout(800)
    item["when"] = fill_when(page, job["day"])
    if not date_is(item["when"].get("after") or {}, job["day"]):
        item["whenRetry"] = fill_when(page, job["day"])
        item["when"]["after"] = item["whenRetry"].get("after")
    shot(page, f"{slot}_04_when.png")
    if not date_is(item["when"].get("after") or {}, job["day"]):
        item["error"] = f"date_not_set:{item['when'].get('after')}"
        return item
    item["confirm"] = click_schedule_btn(page)
    page.wait_for_timeout(4000)
    dismiss(page)
    item["confirmSnip"] = dlg_text(page, 1800)
    shot(page, f"{slot}_05_after.png")
    if re.search(r"\bPublic\b", item["confirmSnip"] or "") and re.search(
        r"now|published", item["confirmSnip"] or "", re.I
    ):
        item["error"] = "went_public"
        return item
    new_id = extract_id(page, skip_ids)
    if not new_id:
        page.wait_for_timeout(2500)
        new_id = extract_id(page, skip_ids)
    item["platformPostId"] = new_id
    item["platformUrl"] = f"https://youtube.com/shorts/{new_id}" if new_id else None
    if new_id:
        skip_ids.add(new_id)
        item["related"] = set_related(page, new_id)
        shot(page, f"{slot}_06_related.png")
        if verify_wall(page):
            item["thumbEdit"] = "phone_verify_wall"
        else:
            item["thumbEdit"] = set_image(page, cover)
            save = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
            if save.count() and save.first.is_enabled():
                save.first.click(force=True)
                page.wait_for_timeout(1500)
                item["thumbSave"] = "clicked"
        shot(page, f"{slot}_07_edit.png")
        item["ok"] = True
    else:
        item["ok"] = False
        item["error"] = "no_id"
    return item


def main() -> int:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    result: dict = {
        "ok": False,
        "channel": HANDLE,
        "channelId": CHANNEL,
        "parentId": LONG_ID,
        "parentTitle": LONG_TITLE,
        "affiliate": "none",
        "madeForKids": False,
        "started": datetime.now(tz=LONDON).isoformat(timespec="seconds"),
        "shorts": [],
    }
    ensure_chrome()
    skip = {LONG_ID, "_C92tIJCk8A"}
    known = {"s01_empty_chairs": "uU12JA5rMWg"}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP, timeout=60000)
        ctx = browser.contexts[0]
        page = studio_page(ctx)
        try:
            page.bring_to_front()
        except Exception:
            pass
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3500)
        dismiss(page)
        result["closeUpload"] = close_empty_upload(page)
        body = snip(page, 2000)
        if re.search(r"signin|Signed out", page.url + "\n" + body, re.I):
            result["error"] = "SIGNED_OUT"
            dump("RESULT.json", result)
            return 2
        if "History of Science" not in body and CHANNEL not in page.url:
            result["error"] = "HOS_NOT_IN_BODY"
            dump("RESULT.json", result)
            return 2
        shot(page, "00_dashboard.png")
        result["longThumb"] = apply_long_thumb(page)
        for job in JOBS:
            vid = known.get(job["slot"])
            if vid:
                skip.add(vid)
                item = repair_existing(page, job, vid)
            else:
                item = upload_one(page, job, skip)
            result["shorts"].append(item)
            dump("RESULT.json", result)
            log(f"{job['slot']} ok={item.get('ok')} id={item.get('platformPostId')}")
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3000)
        shot(page, "99_content_after.png")
        result["contentSnip"] = snip(page, 1800)
    result["ok"] = all(s.get("ok") for s in result["shorts"]) and len(result["shorts"]) == 5
    result["finished"] = datetime.now(tz=LONDON).isoformat(timespec="seconds")
    dump("RESULT.json", result)
    out = PKG / "Schedule/PACKAGE_UPLOAD_RESULT_2026-09-11_shorts.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    log(f"wrote {out} ok={result['ok']}")
    print(json.dumps(result, indent=2)[:5000])
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:
        EV.mkdir(parents=True, exist_ok=True)
        (EV / "TRACE.txt").write_text(traceback.format_exc())
        raise
