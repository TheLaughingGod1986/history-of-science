#!/usr/bin/env python3
"""Upload HOS 004 long via YouTube Studio CDP (no .env / no API / no Orbit).

Channel: @HistoryOfScienceYT (UCXp7HkBIl1LgaznXuZHJyRg) only.
Visibility: Schedule Thu 15 Oct 2026 18:00 Europe/London — normal publish, NOT Premiere.
Video: hos_004_full_v02.mp4 sha ed870939…e98e.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
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
LONDON = ZoneInfo("Europe/London")

PROJ = Path(__file__).resolve().parents[2]
PKG = PROJ / "11_Upload-Package"
EV = PKG / "Schedule/evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"

VIDEO = PROJ / "09_Final-Export/hos_004_full_v02.mp4"
SHA_LOCK = "ed870939f476d326197cdaf1403ce7064850d4286ff63aa81bc5a7584761e98e"
THUMB_A = PROJ / "08_Thumbnail/Selected/hos_004_thumb_A_atom_live_v04.jpg"
THUMB_B = PROJ / "08_Thumbnail/Selected/hos_004_thumb_B_cut_gold_live_v04.jpg"
THUMB_C = PROJ / "08_Thumbnail/Selected/hos_004_thumb_C_hidden_number_live_v06.jpg"
CAPTIONS = PKG / "Captions/hos_004_full_v02.en.srt"

TITLE = "What's Really Inside an Atom?"
TITLE_B = "Why Is the Periodic Table in This Order?"
TITLE_C = "How Small Can You Cut Gold?"
RELATED_002 = "AL_-qlWko_g"

DESC_BODY = (PKG / "Descriptions/atom_long_description_v01.txt").read_text().strip()
CHAPTERS = (PKG / "Chapters/atom_long_chapters_v01.txt").read_text().strip()
# Insert chapters like 002 (before brand line)
if "History of Science ·" in DESC_BODY and CHAPTERS:
    head, _, tail = DESC_BODY.partition("History of Science ·")
    DESC = head.rstrip() + "\n\n" + CHAPTERS + "\n\nHistory of Science ·" + tail
else:
    DESC = DESC_BODY + "\n\n" + CHAPTERS

TAGS = [
    ln.strip()
    for ln in (PKG / "Tags/atom_long_tags_v01.txt").read_text().splitlines()
    if ln.strip()
]
PIN = (PKG / "Pinned-Comments/atom_long_pinned-comment_v01.txt").read_text().strip()

SCHED_DAY = 15
SCHED_MONTH = "October"
SCHED_TIME = "18:00"
SCHED_LABEL = "Thursday 15 Oct 2026 18:00 Europe/London"
SCHED_ISO = "2026-10-15T17:00:00.000Z"


def log(msg: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    with (EV / "run.log").open("a") as f:
        f.write(line + "\n")


def dump(name: str, obj) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    (EV / name).write_text(json.dumps(obj, indent=2) + "\n")
    try:
        (ART / f"hos_004_{name}").write_text(json.dumps(obj, indent=2) + "\n")
    except Exception:
        pass


def shot(page, name: str) -> str:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    dest = EV / name
    try:
        page.screenshot(path=str(dest), full_page=False)
        (ART / f"hos_004_{name}").write_bytes(dest.read_bytes())
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
    for name in ["Got it", "Dismiss", "Not now", "No thanks", "Skip", "Close"]:
        try:
            b = page.get_by_role("button", name=re.compile(rf"^{name}$", re.I))
            if b.count() and b.first.is_visible():
                label = (b.first.inner_text() or "").strip()
                if name.lower() == "close" and page.locator("ytcp-uploads-dialog").count():
                    continue
                b.first.click(timeout=500, force=True)
        except Exception:
            pass
    try:
        if page.locator("ytcp-uploads-dialog").count():
            return
        page.keyboard.press("Escape")
    except Exception:
        pass


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
        urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=1).read()
        return True
    except Exception:
        return False


def ensure_chrome() -> None:
    if chrome_up():
        log("cdp already up")
        return
    Path(PROFILE).mkdir(parents=True, exist_ok=True)
    for name in ("SingletonLock", "SingletonSocket", "SingletonCookie"):
        p = Path(PROFILE) / name
        try:
            p.unlink()
        except FileNotFoundError:
            pass
    log_path = "/tmp/hos_chrome_9460_004.log"
    subprocess.Popen(
        [
            CHROME,
            f"--remote-debugging-port={PORT}",
            "--remote-allow-origins=*",
            f"--user-data-dir={PROFILE}",
            "--profile-directory=Default",
            "--no-first-run",
            "--no-default-browser-check",
            f"https://studio.youtube.com/channel/{CHANNEL}",
        ],
        stdout=open(log_path, "ab"),
        stderr=subprocess.STDOUT,
    )
    for _ in range(40):
        if chrome_up():
            log("cdp started")
            return
        time.sleep(0.5)
    raise SystemExit("CDP :9460 failed to start")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def staging_path(path: Path) -> Path:
    dest = Path("/tmp") / path.name
    if dest.exists():
        try:
            dest.unlink()
        except OSError:
            pass
    try:
        dest.hardlink_to(path)
    except OSError:
        subprocess.check_call(["ln", "-f", str(path), str(dest)])
    return dest


def cdp_set_files(page, path: Path) -> dict:
    info: dict = {"path": str(path)}
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
            info["reason"] = "no_file_input_object"
            return info
        session.send("DOM.setFileInputFiles", {"files": [str(path)], "objectId": obj})
        info["ok"] = True
        info["via"] = "cdp_setFileInputFiles"
        return info
    except Exception as e:
        info["ok"] = False
        info["err"] = f"{type(e).__name__}:{e}"
        return info


def ensure_hos(page) -> dict:
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4500)
    dismiss(page)
    body = snip(page, 3000)
    url = page.url
    if re.search(r"signin|accountchooser|Signed out|accounts\.google\.com", url + "\n" + body, re.I):
        return {"ok": False, "reason": "SIGNED_OUT", "url": url, "snip": body[:600]}
    if CHANNEL not in url:
        return {"ok": False, "reason": "WRONG_CHANNEL_URL", "url": url, "snip": body[:600]}
    if re.search(r"@OrbitWithBen|Orbit With Ben|@OpptiAI|OpptiAI", body, re.I) and "History of Science" not in body:
        return {"ok": False, "reason": "WRONG_CHANNEL", "url": url, "snip": body[:600]}
    if re.search(r"@HistoryOfScience(?!YT)\b", body):
        return {"ok": False, "reason": "EMPTY_HANDLE", "url": url, "snip": body[:600]}
    if "History of Science" not in body:
        return {"ok": False, "reason": "HOS_NOT_IN_BODY", "url": url, "snip": body[:600]}
    return {"ok": True, "url": url, "title": page.title(), "snip": body[:600]}


def open_upload(page) -> dict:
    info: dict = {}
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload?d=ud",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    dismiss(page)
    if not file_input_count(page):
        click_shadow_text(page, r"^Create$")
        page.wait_for_timeout(800)
        click_shadow_text(page, r"^Upload videos?$")
        page.wait_for_timeout(2000)
        dismiss(page)
    info["fileInputs"] = file_input_count(page)
    return info


def fill_title_desc(page) -> dict:
    info: dict = {}
    title_box = page.get_by_role("textbox", name=re.compile(r"title|describe", re.I)).first
    title_box.wait_for(timeout=1200000)
    try:
        title_box.fill(TITLE)
        info["title"] = "fill"
    except Exception:
        title_box.click()
        page.keyboard.press("Meta+A")
        page.keyboard.type(TITLE, delay=12)
        info["title"] = "type"
    try:
        desc = page.get_by_role(
            "textbox", name=re.compile(r"tell viewers|description", re.I)
        ).first
        desc.click(force=True)
        desc.fill(DESC)
        info["desc"] = True
        info["desc_chars"] = len(DESC)
    except Exception as e:
        info["desc"] = f"err:{type(e).__name__}"
    return info


def set_not_kids_and_ai(page) -> dict:
    info: dict = {}
    try:
        page.get_by_text(re.compile(r"No, it.?s not.?Made for Kids", re.I)).click(force=True)
        info["kids"] = "no"
    except Exception as e:
        info["kids"] = f"err:{type(e).__name__}"
    try:
        page.get_by_text(re.compile(r"Yes, AI was used", re.I)).first.click(force=True, timeout=2500)
        info["ai"] = "yes"
    except Exception:
        info["ai"] = "skip"
    return info


def set_tags(page) -> dict:
    info: dict = {}
    try:
        for _ in range(6):
            page.mouse.wheel(0, 500)
            page.wait_for_timeout(80)
        more = page.get_by_text("Show more", exact=True)
        if more.count():
            more.first.click(force=True, timeout=2000)
            page.wait_for_timeout(400)
        box = page.get_by_role("textbox", name=re.compile(r"^Tags$", re.I))
        blob = ", ".join(TAGS)
        info["chars"] = len(blob)
        if box.count():
            box.first.click(force=True)
            page.keyboard.press("Meta+A")
            page.keyboard.press("Backspace")
            box.first.fill(blob)
            page.keyboard.press("Enter")
            info["ok"] = True
        else:
            info["ok"] = False
            info["reason"] = "no_tags_box"
    except Exception as e:
        info["ok"] = False
        info["err"] = f"{type(e).__name__}:{e}"
    return info


def set_thumb(page, thumb: Path) -> dict:
    info: dict = {"file": str(thumb)}
    try:
        loc = page.locator('input[type="file"]')
        for i in range(loc.count()):
            acc = (loc.nth(i).get_attribute("accept") or "").lower()
            if "image" in acc or "jpeg" in acc or "jpg" in acc or "png" in acc:
                loc.nth(i).set_input_files(str(thumb))
                info["ok"] = True
                info["via"] = f"input_{i}"
                page.wait_for_timeout(1500)
                return info
    except Exception as e:
        info["input_err"] = f"{type(e).__name__}"
    try:
        up = page.get_by_text(
            re.compile(r"Upload file|Upload thumbnail|Custom thumbnail", re.I)
        )
        if up.count():
            with page.expect_file_chooser(timeout=8000) as fc:
                up.first.click(force=True)
            fc.value.set_files(str(thumb))
            info["ok"] = True
            info["via"] = "chooser"
            page.wait_for_timeout(1500)
            return info
    except Exception as e:
        info["chooser_err"] = f"{type(e).__name__}:{e}"
    info["ok"] = False
    return info


def next_until_visibility(page) -> str:
    for i in range(22):
        dismiss(page)
        text = dlg_text(page, 4000)
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
        if clicked:
            page.wait_for_timeout(1800)
        else:
            page.wait_for_timeout(900)
    return "no_vis"


def click_schedule_radio(page) -> str:
    try:
        loc = page.get_by_text("Select a date to make your video public", exact=False)
        if loc.count():
            loc.first.click(force=True, timeout=4000)
            page.wait_for_timeout(1000)
            return "select_date_copy"
    except Exception:
        pass
    try:
        radio = page.get_by_role("radio", name=re.compile(r"^Schedule$", re.I))
        if radio.count():
            radio.first.click(force=True, timeout=4000)
            page.wait_for_timeout(900)
            return "role:Schedule"
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
    page.wait_for_timeout(900)
    return hit or ""


def fill_schedule_when(page) -> dict:
    """Set 15 October 2026 18:00. Do NOT tick Premiere."""
    info: dict = {"premiere": False}
    date_str = f"{SCHED_DAY} {SCHED_MONTH} 2026"
    el = page.locator('tp-yt-paper-input[aria-label="Enter date"] input')
    if el.count():
        el.first.click(force=True)
        page.keyboard.press("Meta+a")
        page.keyboard.type(date_str, delay=30)
        page.keyboard.press("Enter")
        info["date_typed"] = date_str
        page.wait_for_timeout(500)
    else:
        page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>40) return false;
                for (const el of (r.querySelectorAll
                  ? r.querySelectorAll('ytcp-text-dropdown-trigger,ytcp-dropdown-trigger')
                  : [])) {
                  const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                  if (/\\d{1,2}\\s+(Oct|October)\\s+2026/i.test(t)
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
        page.wait_for_timeout(900)
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
                    if (/Oct|October/i.test(aria) || t===String(day)) {
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
            SCHED_DAY,
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
        page.keyboard.type(SCHED_TIME, delay=40)
        page.keyboard.press("Tab")
        page.wait_for_timeout(400)
        info["time_typed"] = SCHED_TIME

    # Explicitly ensure Premiere is NOT checked
    prem_state = page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>40) return null;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('[role=checkbox],tp-yt-paper-checkbox,ytcp-checkbox-lit,input[type=checkbox]')
              : [])) {
              const t=((el.innerText||'')+' '+(el.getAttribute('aria-label')||'')+' '+(el.getAttribute('aria-checked')||''))
                .replace(/\\s+/g,' ').trim();
              const label = (el.closest('label')||el.parentElement||{}).innerText||'';
              if (/Premiere/i.test(t+label) && !/instant/i.test(t+label)) {
                const checked = el.getAttribute('aria-checked')==='true' || el.checked===true || /checked/i.test(el.className||'');
                if (checked) { el.click(); return {wasChecked:true, label:(t||label).slice(0,60)}; }
                return {wasChecked:false, label:(t||label).slice(0,60)};
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
    info["premiere_state"] = prem_state
    info["premiere"] = False
    page.wait_for_timeout(400)
    return info


def click_schedule_or_done(page) -> str:
    for name in ["Schedule", "Done", "Save", "Publish"]:
        try:
            btn = page.get_by_role("button", name=re.compile(rf"^{name}$", re.I))
            if btn.count() and btn.last.is_enabled():
                # Prefer Schedule over Publish
                label = (btn.last.inner_text() or name).strip()
                if name == "Publish" and "Schedule" in dlg_text(page, 800):
                    continue
                btn.last.click(force=True)
                page.wait_for_timeout(5000)
                return label or name
        except Exception:
            continue
    hit = page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>40) return null;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('button,ytcp-button,[role=button]') : [])) {
              const t=(el.innerText||'').trim();
              if (/^(Schedule|Done|Save)$/i.test(t) && !el.disabled) {
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
    page.wait_for_timeout(5000)
    return hit or ""


def extract_new_id(page) -> str | None:
    m = re.search(r"/video/([A-Za-z0-9_-]{11})/", page.url)
    if m:
        return m.group(1)
    body = snip(page, 15000)
    for pat in (
        r"youtu\.be/([A-Za-z0-9_-]{11})",
        r"watch\?v=([A-Za-z0-9_-]{11})",
        r"/video/([A-Za-z0-9_-]{11})",
        r"Video link.*?([A-Za-z0-9_-]{11})",
    ):
        m = re.search(pat, body)
        if m:
            return m.group(1)
    return None


def wait_upload_complete(page, timeout_s: int = 2400) -> dict:
    """Wait until details form is ready (title box) after file pick."""
    info: dict = {"waited_s": 0}
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        text = dlg_text(page, 2500)
        if re.search(r"Details|title|Describe your video|Thumbnail", text, re.I):
            try:
                box = page.get_by_role("textbox", name=re.compile(r"title|describe", re.I))
                if box.count():
                    info["ok"] = True
                    info["waited_s"] = round(time.time() - t0, 1)
                    return info
            except Exception:
                pass
        if re.search(r"upload failed|couldn.?t upload|error", text, re.I):
            info["ok"] = False
            info["reason"] = "upload_error"
            info["snip"] = text[:400]
            return info
        page.wait_for_timeout(2000)
    info["ok"] = False
    info["reason"] = "timeout"
    info["waited_s"] = round(time.time() - t0, 1)
    return info


def main() -> int:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    (EV / "run.log").write_text("")

    got = sha256(VIDEO)
    if got != SHA_LOCK:
        log(f"SHA mismatch {got}")
        return 1
    if not THUMB_A.exists() or not THUMB_B.exists() or not THUMB_C.exists():
        log("missing thumbs")
        return 1

    result: dict = {
        "ok": False,
        "method": "youtube_studio_hos_session",
        "channel": {
            "name": "History of Science",
            "handle": HANDLE,
            "channelId": CHANNEL,
            "studioUrl": f"https://studio.youtube.com/channel/{CHANNEL}",
        },
        "not": ["@OrbitWithBen", "@OpptiAI", "@HistoryOfScience", "Orbit .env"],
        "video": {
            "file": VIDEO.name,
            "sha256": got,
            "title": TITLE,
            "thumb": THUMB_A.name,
        },
        "schedule": {
            "label": SCHED_LABEL,
            "publishAt": SCHED_ISO,
            "type": "schedule",
            "premiere": False,
        },
        "madeForKids": False,
        "affiliate": "none",
        "shortsUploaded": False,
    }

    ensure_chrome()
    staged = staging_path(VIDEO)
    result["staged"] = str(staged)

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = None
        for pg in ctx.pages:
            u = pg.url or ""
            if "facebook.com" in u or "instagram.com" in u:
                continue
            if "studio.youtube.com" in u or "youtube.com" in u:
                page = pg
                break
        if page is None:
            page = ctx.new_page()

        try:
            hos = ensure_hos(page)
            result["channelCheck"] = hos
            shot(page, "01_channel_check.png")
            dump("01_channel_check.json", hos)
            if not hos.get("ok"):
                result["stop"] = hos.get("reason")
                dump("RESULT.json", result)
                log(f"STOP channel: {hos.get('reason')}")
                return 2

            result["openUpload"] = open_upload(page)
            shot(page, "02_upload_dialog.png")
            pick = cdp_set_files(page, staged)
            result["pick"] = pick
            dump("02_pick.json", pick)
            if not pick.get("ok"):
                result["stop"] = "file_pick_failed"
                dump("RESULT.json", result)
                return 3

            wait = wait_upload_complete(page)
            result["uploadWait"] = wait
            shot(page, "03_details.png")
            if not wait.get("ok"):
                result["stop"] = "upload_wait_failed"
                dump("RESULT.json", result)
                return 4

            result["titleDesc"] = fill_title_desc(page)
            result["kidsAi"] = set_not_kids_and_ai(page)
            result["thumb"] = set_thumb(page, THUMB_A)
            result["tags"] = set_tags(page)
            shot(page, "04_details_filled.png")
            dump("04_details.json", {
                "titleDesc": result["titleDesc"],
                "kidsAi": result["kidsAi"],
                "thumb": result["thumb"],
                "tags": result["tags"],
            })

            result["next"] = next_until_visibility(page)
            shot(page, "05_visibility.png")
            result["scheduleRadio"] = click_schedule_radio(page)
            page.wait_for_timeout(800)
            result["when"] = fill_schedule_when(page)
            shot(page, "06_schedule_when.png")
            dump("06_schedule_when.json", result["when"])

            # Confirm no Premiere in dialog text
            vis_text = dlg_text(page, 5000)
            result["visibilityText"] = vis_text[:1200]
            if re.search(r"Premiere.*checked|Set as Premiere", vis_text, re.I) and re.search(
                r"aria-checked=\"true\"|checked", vis_text, re.I
            ):
                # try untick again
                result["when2"] = fill_schedule_when(page)

            done = click_schedule_or_done(page)
            result["doneClick"] = done
            shot(page, "07_after_schedule.png")
            page.wait_for_timeout(3000)
            dismiss(page)

            # Extract id — may need to wait / open content list
            new_id = extract_new_id(page)
            if not new_id:
                page.goto(
                    f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
                    wait_until="domcontentloaded",
                    timeout=120000,
                )
                page.wait_for_timeout(4000)
                shot(page, "08_content_list.png")
                body = snip(page, 20000)
                if TITLE in body or "What's Really Inside" in body:
                    m = re.search(
                        r"/video/([A-Za-z0-9_-]{11})/",
                        page.content() if hasattr(page, "content") else "",
                    )
                # scrape video links near title
                new_id = page.evaluate(
                    """(title) => {
                      const links=[...document.querySelectorAll('a[href*="/video/"]')];
                      for (const a of links) {
                        const row=a.closest('ytcp-video-row,ytcp-video-section-content,div')||a.parentElement;
                        const t=(row&&row.innerText||a.innerText||'');
                        if (t.includes(title) || t.includes("What's Really Inside")) {
                          const m=a.href.match(/\\/video\\/([A-Za-z0-9_-]{11})/);
                          if (m) return m[1];
                        }
                      }
                      // fallback first scheduled
                      for (const a of links) {
                        const m=a.href.match(/\\/video\\/([A-Za-z0-9_-]{11})/);
                        if (m) return m[1];
                      }
                      return null;
                    }""",
                    TITLE,
                )
            result["videoId"] = new_id
            if new_id:
                result["video"]["platformPostId"] = new_id
                result["video"]["platformUrl"] = f"https://youtu.be/{new_id}"
                result["video"]["watchUrl"] = f"https://www.youtube.com/watch?v={new_id}"
                result["video"]["studioEdit"] = (
                    f"https://studio.youtube.com/video/{new_id}/edit"
                )

            # Open edit page and verify visibility
            if new_id:
                page.goto(
                    f"https://studio.youtube.com/video/{new_id}/edit",
                    wait_until="domcontentloaded",
                    timeout=120000,
                )
                page.wait_for_timeout(4000)
                dismiss(page)
                shot(page, "09_edit.png")
                # Visibility tab
                click_shadow_text(page, r"^Visibility$")
                page.wait_for_timeout(2000)
                shot(page, "10_visibility_verify.png")
                vis_body = snip(page, 4000)
                result["visibilityVerify"] = vis_body[:1500]
                scheduled_ok = bool(
                    re.search(r"15\s+(Oct|October).*2026", vis_body, re.I)
                    or re.search(r"Scheduled", vis_body, re.I)
                )
                premiere_hit = bool(re.search(r"Premiere", vis_body, re.I)) and bool(
                    re.search(r"will premiere|Premiere on", vis_body, re.I)
                )
                result["scheduledOk"] = scheduled_ok
                result["premiereInVisibility"] = premiere_hit
                if premiere_hit:
                    result["ok"] = False
                    result["stop"] = "PREMIERE_DETECTED"
                elif scheduled_ok and new_id:
                    result["ok"] = True
                else:
                    result["ok"] = bool(new_id)
                    result["note"] = "verify schedule text manually from screenshot"

            dump("RESULT.json", result)
            out = PKG / "Schedule/PACKAGE_UPLOAD_RESULT_2026-09-29.json"
            out.write_text(json.dumps(result, indent=2) + "\n")
            (ART / "PACKAGE_UPLOAD_RESULT_2026-09-29.json").write_text(out.read_text())
            log(f"DONE ok={result.get('ok')} id={new_id} done={done}")
            return 0 if result.get("ok") or new_id else 5
        except Exception as e:
            result["error"] = f"{type(e).__name__}:{e}"
            result["trace"] = traceback.format_exc()[-2000:]
            shot(page, "99_error.png")
            dump("RESULT.json", result)
            log(f"ERROR {e}")
            return 9


if __name__ == "__main__":
    raise SystemExit(main())
