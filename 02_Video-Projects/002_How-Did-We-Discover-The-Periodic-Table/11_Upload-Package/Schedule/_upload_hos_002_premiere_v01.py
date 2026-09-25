#!/usr/bin/env python3
"""Upload HOS 002 long to @HistoryOfScienceYT as a Thursday Premiere.

Same Chrome session as Germs 001 (`~/.hos-chrome-youtube-studio`, CDP :9460).
Never Orbit / Oppti. Zero /go/. Do not lead with a Short.

Premiere: Thursday 17 Sep 2026 19:00 Europe/London (house cadence).
Primary thumb: live-lock A (gallium). ABC Test is blocked until after Premiere.
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
EV = PKG / "Schedule/evidence_2026-09-11_premiere"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"

VIDEO = PROJ / "09_Final-Export/hos_002_periodic_table_full_v02.mp4"
SHA_LOCK = "8a5b8dde713cd4d6d2834b49635443ebf5fda1a83de92688bf79ca91746de31f"
THUMB_A = PROJ / "08_Thumbnail/Selected/hos_002_thumb_A_gallium_live_v02.jpg"
TITLE = "How Did We Discover the Periodic Table?"
DESC = (PKG / "Descriptions/periodic_table_long_description_v01.txt").read_text()
TAGS = [
    ln.strip()
    for ln in (PKG / "Tags/periodic_table_long_tags_v01.txt").read_text().splitlines()
    if ln.strip()
]
PIN = (PKG / "Pinned-Comments/periodic_table_long_pinned-comment_v01.txt").read_text().strip()

PREMIERE_DAY = 17
PREMIERE_MONTH = "September"
PREMIERE_MONTH_SHORT = "Sept"
PREMIERE_TIME = "19:00"
PREMIERE_LABEL = "Thursday 17 Sep 2026 19:00 Europe/London"
PREMIERE_ISO = "2026-09-17T18:00:00+00:00"  # 19:00 BST


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


def studio_page(ctx):
    """Prefer an existing Studio tab. Never drive Facebook / Orbit tabs."""
    for page in ctx.pages:
        url = page.url or ""
        if "facebook.com" in url or "instagram.com" in url:
            continue
        if "studio.youtube.com" in url or "youtube.com" in url:
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


def open_upload(page) -> dict:
    """Create → Upload videos, then wait for the file input."""
    info: dict = {}
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2800)
    dismiss(page)
    if file_input_count(page):
        info["via"] = "upload_url"
        return info
    clicked = click_shadow_text(page, r"^Create$")
    info["create"] = clicked
    page.wait_for_timeout(800)
    up = click_shadow_text(page, r"^Upload videos?$")
    info["uploadVideos"] = up
    page.wait_for_timeout(2000)
    dismiss(page)
    if not file_input_count(page):
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload?d=ud",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(2500)
        dismiss(page)
        if not file_input_count(page):
            click_shadow_text(page, r"^Create$")
            page.wait_for_timeout(700)
            click_shadow_text(page, r"^Upload videos?$")
            page.wait_for_timeout(2000)
    info["fileInputs"] = file_input_count(page)
    info["intercept"] = disable_file_chooser_intercept(page)
    return info


def staging_path(path: Path) -> Path:
    """Hardlink into /tmp so the Open dialog path has no spaces."""
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


def hos_chrome_pid() -> int | None:
    try:
        out = subprocess.check_output(["lsof", "-ti", f":{PORT}"], text=True).strip()
    except subprocess.CalledProcessError:
        return None
    for pid in out.split():
        if pid.isdigit():
            return int(pid)
    return None


def cdp_set_files(page, path: Path) -> dict:
    """Ask Chrome to read the file from disk. Playwright set_input_files caps at 50MB over CDP."""
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
        info["evalType"] = (ev.get("result") or {}).get("type")
        info["evalSubtype"] = (ev.get("result") or {}).get("subtype")
        if not obj:
            info["ok"] = False
            info["reason"] = "no_file_input_object"
            return info
        session.send(
            "DOM.setFileInputFiles",
            {"files": [str(path)], "objectId": obj},
        )
        info["ok"] = True
        info["via"] = "cdp_setFileInputFiles"
        return info
    except Exception as e:
        info["ok"] = False
        info["err"] = f"{type(e).__name__}:{e}"
        return info


def pick_video_file(page, path: Path) -> dict:
    """Attach the cut. Playwright CDP cannot transfer >50MB; Chrome can read a local path."""
    info: dict = {"path": str(path), "bytes": path.stat().st_size}
    staged = staging_path(path)
    info["staged"] = str(staged)
    info["cdp"] = cdp_set_files(page, staged)
    if info["cdp"].get("ok"):
        page.wait_for_timeout(2500)
        after = dlg_text(page, 800)
        info["after"] = after[:500]
        still_picker = bool(re.search(r"Select files", after, re.I)) and not re.search(
            r"Details|Title|Uploading|Checks", after, re.I
        )
        info["ok"] = not still_picker
        info["via"] = "cdp_setFileInputFiles"
        if info["ok"]:
            return info
    info["os_dialog"] = os_open_dialog(page, staged)
    info["ok"] = bool(info["os_dialog"].get("ok"))
    info["via"] = "os_open_dialog"
    return info


def disable_file_chooser_intercept(page) -> str:
    """Let Chrome show the real macOS Open dialog (Playwright's 50MB CDP cap)."""
    try:
        session = page.context.new_cdp_session(page)
        session.send("Page.setInterceptFileChooserDialog", {"enabled": False})
        return "off"
    except Exception as e:
        return f"err:{type(e).__name__}:{e}"


def os_dialog_windows() -> list[str]:
    script = '''
tell application "System Events"
  tell process "Google Chrome"
    return name of windows
  end tell
end tell
'''
    proc = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=10)
    names = [n.strip() for n in (proc.stdout or "").split(",") if n.strip()]
    return names


def os_open_dialog(page, path: Path) -> dict:
    """Drive the native macOS Open dialog on the HOS Chrome PID only."""
    info: dict = {"intercept": disable_file_chooser_intercept(page)}
    pid = hos_chrome_pid()
    info["hosPid"] = pid
    try:
        page.bring_to_front()
    except Exception:
        pass
    click_shadow_text(page, r"^Select files?$")
    page.wait_for_timeout(1200)
    info["windows_after_click"] = os_dialog_windows()
    posix = str(path)
    subprocess.run(["pbcopy"], input=posix.encode(), check=True)
    activate = ""
    if pid:
        activate = f'''
tell application "System Events"
  set frontmost of (first process whose unix id is {pid}) to true
end tell
delay 0.4
'''
    script = f'''
{activate}
tell application "System Events"
  delay 0.3
  repeat 12 times
    set wn to name of windows of (first process whose unix id is {pid or 0})
    if (wn as text) contains "Open" then exit repeat
    delay 0.25
  end repeat
  keystroke "g" using {{command down, shift down}}
  delay 0.8
  keystroke "v" using {{command down}}
  delay 0.5
  keystroke return
  delay 1.0
  keystroke return
end tell
'''
    proc = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True,
        timeout=40,
    )
    info["returncode"] = proc.returncode
    info["stderr"] = (proc.stderr or "")[:400]
    info["stdout"] = (proc.stdout or "")[:200]
    info["windows_after_keys"] = os_dialog_windows()
    page.wait_for_timeout(4000)
    after = dlg_text(page, 800)
    info["after"] = after[:500]
    still_picker = bool(re.search(r"Select files", after, re.I)) and not re.search(
        r"Details|Title|Uploading", after, re.I
    )
    info["ok"] = proc.returncode == 0 and not still_picker
    return info


def chrome_up() -> bool:
    try:
        urllib.request.urlopen(f"{CDP}/json/version", timeout=2).read()
        return True
    except Exception:
        return False


def kill_port_chrome() -> None:
    try:
        out = subprocess.check_output(["lsof", "-ti", f":{PORT}"], text=True).strip()
    except subprocess.CalledProcessError:
        return
    for pid in out.split():
        if pid.isdigit():
            log(f"kill_pid={pid}")
            subprocess.call(["kill", pid])
    time.sleep(1.5)
    try:
        out2 = subprocess.check_output(["lsof", "-ti", f":{PORT}"], text=True).strip()
    except subprocess.CalledProcessError:
        return
    for pid in out2.split():
        if pid.isdigit():
            log(f"kill_9_pid={pid}")
            subprocess.call(["kill", "-9", pid])
    time.sleep(1)


def clear_profile_locks() -> None:
    p = Path(PROFILE)
    for name in ("SingletonLock", "SingletonSocket", "SingletonCookie", "DevToolsActivePort"):
        try:
            (p / name).unlink()
        except FileNotFoundError:
            pass


def ensure_chrome() -> None:
    if chrome_up():
        log("chrome_already_up")
        return
    kill_port_chrome()
    clear_profile_locks()
    log("starting_chrome")
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
            f"https://studio.youtube.com/channel/{CHANNEL}",
        ],
        stdout=open("/tmp/hos_chrome_9460_002.log", "a"),
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    for i in range(90):
        if chrome_up():
            log(f"chrome_up_{i}")
            return
        time.sleep(0.5)
    raise RuntimeError("chrome_failed_to_start")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def is_glue(page) -> bool:
    t = page.title() + "\n" + snip(page, 1500)
    return bool(
        re.search(
            r"Error\s*9|something went wrong|don.?t have permission|"
            r"phone.?verif|confirm you.?re not a bot|unusual traffic",
            t,
            re.I,
        )
    )


def ensure_hos(page) -> dict:
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4500)
    dismiss(page)
    body = snip(page, 2500)
    url = page.url
    if re.search(r"signin|accountchooser|Signed out", url + "\n" + body, re.I):
        return {"ok": False, "reason": "SIGNED_OUT", "url": url, "snip": body[:600]}
    if re.search(r"@OrbitWithBen|@OpptiAI", body, re.I) and "History of Science" not in body:
        return {"ok": False, "reason": "WRONG_CHANNEL", "url": url, "snip": body[:600]}
    if "History of Science" not in body and CHANNEL not in url:
        return {"ok": False, "reason": "HOS_NOT_IN_BODY", "url": url, "snip": body[:600]}
    already = bool(re.search(r"How Did We Discover the Periodic Table", body, re.I))
    return {
        "ok": True,
        "url": url,
        "title": page.title(),
        "alreadyListed": already,
        "snip": body[:600],
    }


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


def set_thumb(page) -> dict:
    info: dict = {"file": str(THUMB_A)}
    try:
        loc = page.locator('input[type="file"]')
        for i in range(loc.count()):
            acc = (loc.nth(i).get_attribute("accept") or "").lower()
            if "image" in acc or "jpeg" in acc or "jpg" in acc or "png" in acc:
                loc.nth(i).set_input_files(str(THUMB_A))
                info["ok"] = True
                info["via"] = f"input_{i}"
                page.wait_for_timeout(1200)
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
            fc.value.set_files(str(THUMB_A))
            info["ok"] = True
            info["via"] = "chooser"
            page.wait_for_timeout(1200)
            return info
    except Exception as e:
        info["chooser_err"] = f"{type(e).__name__}:{e}"
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
        if clicked:
            page.wait_for_timeout(1600)
        else:
            page.wait_for_timeout(800)
    return "no_vis"


def click_schedule_radio(page) -> str:
    """Open the Schedule date dropdown. Do not pick Public + instant Premiere."""
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


def fill_premiere_when(page) -> dict:
    info: dict = {}
    date_str = f"{PREMIERE_DAY} {PREMIERE_MONTH} 2026"
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
            PREMIERE_DAY,
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
        page.keyboard.type(PREMIERE_TIME, delay=40)
        page.keyboard.press("Tab")
        page.wait_for_timeout(400)
        info["time_typed"] = PREMIERE_TIME

    prem = page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>35) return null;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('[role=checkbox],tp-yt-paper-checkbox,ytcp-checkbox,div,span,label')
              : [])) {
              const t=((el.innerText||'')+' '+(el.getAttribute('aria-label')||''))
                .replace(/\\s+/g,' ').trim();
              if (/Premiere/i.test(t) && !/instant/i.test(t) && t.length<40) {
                el.click(); return t.slice(0,50);
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
    info["premiere_click"] = prem
    page.wait_for_timeout(500)
    return info


def click_schedule_or_done(page) -> str:
    for name in ["Schedule", "Publish", "Done", "Save"]:
        try:
            btn = page.get_by_role("button", name=re.compile(rf"^{name}$", re.I))
            if btn.count() and btn.last.is_enabled():
                btn.last.click(force=True)
                page.wait_for_timeout(4000)
                return name
        except Exception:
            continue
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
    page.wait_for_timeout(4000)
    return hit or ""


def extract_new_id(page) -> str | None:
    m = re.search(r"/video/([A-Za-z0-9_-]{11})/", page.url)
    if m:
        return m.group(1)
    body = snip(page, 12000)
    for pat in (
        r"https://youtu\.be/([A-Za-z0-9_-]{11})",
        r"watch\?v=([A-Za-z0-9_-]{11})",
        r"studio\.youtube\.com/video/([A-Za-z0-9_-]{11})",
    ):
        m = re.search(pat, body + "\n" + page.url)
        if m and m.group(1) not in {"_C92tIJCk8A"}:
            return m.group(1)
    hrefs = page.evaluate(
        """() => [...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href')||'')"""
    )
    for href in hrefs or []:
        m = re.search(r"/video/([A-Za-z0-9_-]{11})/", href or "")
        if m and m.group(1) not in {"_C92tIJCk8A"}:
            return m.group(1)
    return None


def try_pin(page, video_id: str) -> dict:
    info: dict = {"id": video_id}
    try:
        page.goto(
            f"https://studio.youtube.com/video/{video_id}/comments",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3500)
        dismiss(page)
        info["snip"] = snip(page, 800)
        # First comment is posted by the channel after upload if we typed it;
        # pin UI is Studio-only and often locked. Record only.
        info["ok"] = False
        info["reason"] = "pin_manual_if_comment_exists"
    except Exception as e:
        info["err"] = f"{type(e).__name__}:{e}"
    return info


def main() -> int:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    result: dict = {
        "ok": False,
        "method": "youtube_studio_hos_session",
        "channel": {
            "name": "History of Science",
            "handle": HANDLE,
            "channelId": CHANNEL,
            "studioUrl": f"https://studio.youtube.com/channel/{CHANNEL}",
        },
        "not": ["@OrbitWithBen", "@OpptiAI", "@HistoryOfScience"],
        "premiere": {
            "date": "2026-09-17",
            "time": PREMIERE_TIME,
            "timeZone": "Europe/London",
            "type": "premiere",
            "label": PREMIERE_LABEL,
            "iso": PREMIERE_ISO,
        },
        "madeForKids": False,
        "affiliate": "none",
        "started": datetime.now(tz=LONDON).isoformat(timespec="seconds"),
    }

    if not VIDEO.exists():
        result["error"] = f"missing {VIDEO}"
        dump("RESULT.json", result)
        log(result["error"])
        return 2
    digest = sha256(VIDEO)
    result["video"] = {
        "file": VIDEO.name,
        "sha256": digest,
        "bytes": VIDEO.stat().st_size,
        "title": TITLE,
        "thumb": THUMB_A.name,
    }
    if digest != SHA_LOCK:
        result["error"] = f"sha mismatch {digest}"
        dump("RESULT.json", result)
        log(result["error"])
        return 2
    if not THUMB_A.exists():
        result["error"] = f"missing thumb {THUMB_A}"
        dump("RESULT.json", result)
        return 2

    try:
        ensure_chrome()
    except Exception as e:
        result["error"] = f"chrome:{e}"
        dump("RESULT.json", result)
        return 2

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP, timeout=60000)
        ctx = browser.contexts[0]
        page = studio_page(ctx)
        try:
            page.bring_to_front()
        except Exception:
            pass
        hos = ensure_hos(page)
        result["hos"] = hos
        shot(page, "00_hos_dashboard.png")
        dump("AUTH.json", hos)
        if not hos.get("ok"):
            result["error"] = hos.get("reason") or "HOS_NOT_READY"
            dump("RESULT.json", result)
            return 2
        if hos.get("alreadyListed"):
            result["error"] = "already_listed_abort"
            dump("RESULT.json", result)
            log("ABORT already listed — do not mint a second id")
            return 3

        result["openUpload"] = open_upload(page)
        shot(page, "01_upload_dialog.png")
        if is_glue(page):
            result["error"] = "GLUE"
            shot(page, "01b_glue.png")
            dump("RESULT.json", result)
            return 2

        picked = pick_video_file(page, VIDEO)
        result["filePick"] = picked
        shot(page, "01b_after_file_pick.png")
        if not picked.get("ok"):
            result["error"] = "NO_FILE_PICKER"
            dump("RESULT.json", result)
            return 2

        result["details"] = fill_title_desc(page)
        shot(page, "02_details_title.png")
        result["audience"] = set_not_kids_and_ai(page)
        result["tags"] = set_tags(page)
        result["thumb"] = set_thumb(page)
        shot(page, "03_details_filled.png")

        result["next"] = next_until_visibility(page)
        shot(page, "04_visibility.png")
        result["scheduleRadio"] = click_schedule_radio(page)
        page.wait_for_timeout(800)
        result["when"] = fill_premiere_when(page)
        shot(page, "05_premiere_when.png")
        result["confirmClick"] = click_schedule_or_done(page)
        page.wait_for_timeout(5000)
        dismiss(page)
        shot(page, "06_after_schedule.png")
        result["confirmSnip"] = snip(page, 1500)

        new_id = extract_new_id(page)
        if not new_id:
            page.wait_for_timeout(4000)
            new_id = extract_new_id(page)
        result["video"]["platformPostId"] = new_id
        result["video"]["platformUrl"] = f"https://youtu.be/{new_id}" if new_id else None
        result["video"]["watchUrl"] = (
            f"https://www.youtube.com/watch?v={new_id}" if new_id else None
        )
        result["ok"] = bool(new_id)
        if new_id:
            result["studioEdit"] = f"https://studio.youtube.com/video/{new_id}/edit"
            result["pin"] = try_pin(page, new_id)
            shot(page, "07_comments.png")
            page.goto(
                f"https://studio.youtube.com/video/{new_id}/edit",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(3500)
            dismiss(page)
            result["editSnip"] = snip(page, 1200)
            shot(page, "08_edit.png")

    result["finished"] = datetime.now(tz=LONDON).isoformat(timespec="seconds")
    dump("RESULT.json", result)
    out = PKG / "Schedule/PACKAGE_UPLOAD_RESULT_2026-09-11_premiere.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    log(f"wrote {out} ok={result.get('ok')} id={result.get('video', {}).get('platformPostId')}")
    print(json.dumps(result, indent=2)[:4000])
    return 0 if result.get("ok") else 1


def tick_set_as_premiere(page) -> str:
    """Tick Schedule → Set as Premiere. Never Public → instant Premiere."""
    hit = page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>40) return null;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('[role=checkbox],tp-yt-paper-checkbox,ytcp-checkbox-lit,ytcp-checkbox')
              : [])) {
              const t=((el.innerText||'')+' '+(el.getAttribute('aria-label')||''))
                .replace(/\\s+/g,' ').trim();
              if (/Set as Premiere/i.test(t) && !/instant/i.test(t)) {
                const on = el.getAttribute('aria-checked')==='true' || el.checked === true;
                if (!on) el.click();
                return (on ? 'already:' : 'ticked:') + t.slice(0,40);
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
    page.wait_for_timeout(600)
    return hit or ""


def finish_existing(video_id: str) -> int:
    """Schedule Premiere on an already-uploaded HOS 002 draft. Do not mint a second id."""
    EV.mkdir(parents=True, exist_ok=True)
    result: dict = {
        "ok": False,
        "mode": "finish_draft",
        "videoId": video_id,
        "premiere": PREMIERE_LABEL,
        "started": datetime.now(tz=LONDON).isoformat(timespec="seconds"),
    }
    ensure_chrome()
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP, timeout=60000)
        ctx = browser.contexts[0]
        page = studio_page(ctx)
        try:
            page.bring_to_front()
        except Exception:
            pass
        page.goto(
            f"https://studio.youtube.com/video/{video_id}/edit",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3500)
        dismiss(page)
        shot(page, "10_draft_edit.png")
        clicked = click_shadow_text(page, r"^Edit draft$")
        result["editDraft"] = clicked
        page.wait_for_timeout(2500)
        if not file_input_count(page) and "Details" not in dlg_text(page, 400):
            page.get_by_role("button", name=re.compile(r"Edit draft", re.I)).first.click(
                timeout=8000
            )
            page.wait_for_timeout(2500)
        shot(page, "11_draft_dialog.png")
        result["tags"] = set_tags(page)
        shot(page, "12_tags_trimmed.png")
        result["audience"] = set_not_kids_and_ai(page)
        result["next"] = next_until_visibility(page)
        shot(page, "13_visibility.png")
        result["scheduleRadio"] = click_schedule_radio(page)
        page.wait_for_timeout(900)
        result["when"] = fill_premiere_when(page)
        shot(page, "14_premiere_when.png")
        if not (
            result["when"].get("date_typed")
            or result["when"].get("date_picked")
            or result["when"].get("time_typed")
        ):
            result["confirmClick"] = "skipped_no_when"
        else:
            result["premiereBox"] = tick_set_as_premiere(page)
            shot(page, "14b_premiere_ticked.png")
            result["confirmClick"] = click_schedule_or_done(page)
        page.wait_for_timeout(5000)
        dismiss(page)
        shot(page, "15_after_schedule.png")
        page.goto(
            f"https://studio.youtube.com/video/{video_id}/edit",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3500)
        dismiss(page)
        body = snip(page, 2500)
        result["editSnip"] = body[:1500]
        result["scheduled"] = bool(
            re.search(r"17\s+(Sept|Sep|September)\s+2026|Premiere|Scheduled", body, re.I)
        )
        result["stillDraft"] = bool(re.search(r"draft state", body, re.I))
        shot(page, "16_edit_after.png")
        result["ok"] = bool(result.get("scheduled")) or not result.get("stillDraft")
    result["finished"] = datetime.now(tz=LONDON).isoformat(timespec="seconds")
    dump("FINISH.json", result)
    out = PKG / "Schedule/PACKAGE_UPLOAD_RESULT_2026-09-11_premiere.json"
    prev = {}
    if out.exists():
        try:
            prev = json.loads(out.read_text())
        except Exception:
            prev = {}
    prev["finishDraft"] = result
    prev["ok"] = bool(result.get("ok"))
    if video_id:
        prev.setdefault("video", {})["platformPostId"] = video_id
        prev["video"]["platformUrl"] = f"https://youtu.be/{video_id}"
        prev["video"]["watchUrl"] = f"https://www.youtube.com/watch?v={video_id}"
    out.write_text(json.dumps(prev, indent=2) + "\n")
    log(f"finish {video_id} ok={result.get('ok')} scheduled={result.get('scheduled')}")
    print(json.dumps(result, indent=2)[:4000])
    return 0 if result.get("ok") else 1


def premiere_tick_existing(video_id: str) -> int:
    """Turn on Set as Premiere for an already-scheduled listing."""
    EV.mkdir(parents=True, exist_ok=True)
    result: dict = {
        "ok": False,
        "mode": "premiere_tick",
        "videoId": video_id,
        "started": datetime.now(tz=LONDON).isoformat(timespec="seconds"),
    }
    ensure_chrome()
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP, timeout=60000)
        ctx = browser.contexts[0]
        page = studio_page(ctx)
        try:
            page.bring_to_front()
        except Exception:
            pass
        page.goto(
            f"https://studio.youtube.com/video/{video_id}/edit",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3000)
        dismiss(page)
        shot(page, "20_before_premiere_tick.png")
        vis = page.get_by_text(re.compile(r"^Scheduled$", re.I))
        if vis.count():
            vis.first.click(force=True)
            page.wait_for_timeout(1200)
            result["clickedScheduled"] = True
        else:
            click_shadow_text(page, r"^Scheduled$")
            page.wait_for_timeout(1000)
            result["clickedScheduled"] = "shadow"
        shot(page, "21_visibility_popover.png")
        result["premiereBox"] = tick_set_as_premiere(page)
        if not result["premiereBox"]:
            try:
                page.get_by_text("Set as Premiere", exact=False).first.click(
                    force=True, timeout=4000
                )
                result["premiereBox"] = "text_click"
            except Exception as e:
                result["premiereBox"] = f"err:{type(e).__name__}"
        shot(page, "22_premiere_ticked.png")
        result["save"] = click_schedule_or_done(page)
        if not result["save"]:
            try:
                page.get_by_role(
                    "button", name=re.compile(r"^(Save|Done|Schedule)$", re.I)
                ).last.click(force=True, timeout=4000)
                result["save"] = "role"
            except Exception:
                result["save"] = click_shadow_text(page, r"^(Save|Done|Schedule)$")
        page.wait_for_timeout(3500)
        shot(page, "23_after_premiere_tick.png")
        body = snip(page, 2000)
        result["snip"] = body[:800]
        result["ok"] = bool(re.search(r"Premiere", body, re.I) or result.get("premiereBox"))
    result["finished"] = datetime.now(tz=LONDON).isoformat(timespec="seconds")
    dump("PREMIERE_TICK.json", result)
    log(f"premiere_tick {video_id} {json.dumps(result)[:800]}")
    print(json.dumps(result, indent=2)[:3000])
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    try:
        vid = "AL_-qlWko_g"
        if "--id" in sys.argv:
            vid = sys.argv[sys.argv.index("--id") + 1]
        if "--premiere-tick" in sys.argv:
            raise SystemExit(premiere_tick_existing(vid))
        if "--finish" in sys.argv:
            raise SystemExit(finish_existing(vid))
        raise SystemExit(main())
    except Exception:
        EV.mkdir(parents=True, exist_ok=True)
        (EV / "TRACE.txt").write_text(traceback.format_exc())
        raise
