#!/usr/bin/env python3
"""v02 calendar restore — harden Done→Save so Private/Schedule actually stick.

@HistoryOfScienceYT CDP :9460 only. No thumb changes. No new uploads.
"""
from __future__ import annotations

import json
import re
import traceback
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9460"
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"
HANDLE = "@HistoryOfScienceYT"
RELATED = "_C92tIJCk8A"
RELATED_RE = re.compile(r"How Did We Discover Germs", re.I)
LONDON = ZoneInfo("Europe/London")

EV = Path(
    "/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/"
    "001_How-Did-We-Discover-Germs/11_Upload-Package/Schedule/"
    "evidence_2026-09-06_calendar_restore"
)
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"

JOBS = [
    {
        "slot": "s04",
        "id": "sILtQxgYQk8",
        "title": "A flask that proved germs come from outside",
        "day": 7,
        "label": "Mon 7 Sep 2026 11:30 Europe/London",
    },
    {
        "slot": "s05",
        "id": "93fPUG-hW0A",
        "title": "Invisible life is still everywhere",
        "day": 8,
        "label": "Tue 8 Sep 2026 11:30 Europe/London",
    },
]

PUBLICS = [
    {"id": "H1y0DXFVmw8", "title": "Germs don't cast a shadow"},
    {"id": "iqToagXnjX0", "title": "Microbes in a drop of pond water"},
    {"id": "8_Edn_HCi1s", "title": "Germs hitch a ride on you"},
]

TWINS = [
    "8uBR-9oxeWs",
    "YX2UR1u-JCQ",
    "Fnb3p81u-wY",
    "vpuRgKXtFlY",
    "Lcmh5y2KMQM",
]


import subprocess
import urllib.request
import time

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PROFILE = str(Path.home() / ".hos-chrome-youtube-studio")
PORT = 9460


def chrome_up() -> bool:
    try:
        urllib.request.urlopen(f"{CDP}/json/version", timeout=2).read()
        return True
    except Exception:
        return False


def hard_reset_chrome() -> None:
    log("hard_reset_chrome")
    subprocess.call(["pkill", "-f", f"remote-debugging-port={PORT}"])
    time.sleep(2)
    p = Path(PROFILE)
    for name in ("SingletonLock", "SingletonSocket", "SingletonCookie", "DevToolsActivePort"):
        try:
            (p / name).unlink()
        except FileNotFoundError:
            pass
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
            "https://studio.youtube.com/",
        ],
        stdout=open("/tmp/hos_chrome_9460.log", "a"),
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    for i in range(90):
        if chrome_up():
            log(f"chrome_up_{i}")
            return
        time.sleep(0.5)
    raise RuntimeError("chrome_failed")


def log(msg: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    with (EV / "run_v02.log").open("a") as f:
        f.write(line + "\n")


def shot(page, name: str) -> str:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    dest = EV / name
    try:
        page.screenshot(path=str(dest), full_page=True)
        try:
            (ART / name).write_bytes(dest.read_bytes())
        except Exception:
            pass
        return str(dest)
    except Exception as e:
        log(f"shot_err {name}: {e}")
        return ""


def body(page, n: int = 8000) -> str:
    try:
        return page.inner_text("body")[:n]
    except Exception as e:
        return str(e)


def dismiss(page) -> None:
    for name in ["Got it", "Dismiss", "Not now", "Close", "No thanks", "Skip"]:
        try:
            b = page.get_by_role("button", name=re.compile(rf"^{name}$", re.I))
            if b.count() and b.first.is_visible():
                b.first.click(timeout=500, force=True)
        except Exception:
            pass
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass


def wait_studio(page, timeout_s: int = 90) -> bool:
    page.wait_for_load_state("domcontentloaded")
    for _ in range(timeout_s * 2):
        t = body(page, 1500)
        if "Choose an account" in t or "Signed out" in t:
            return False
        if page.locator(
            "ytcp-navigation-drawer, ytcp-app, ytcp-video-metadata-editor"
        ).count():
            return True
        page.wait_for_timeout(500)
    return False


def open_edit(page, vid: str) -> None:
    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    wait_studio(page)
    page.wait_for_timeout(1600)
    dismiss(page)


def visibility(page) -> str:
    # Prefer the right-rail visibility chip text.
    chip = page.evaluate(
        """()=>{
      let hit='';
      const walk=(r,d=0)=>{
        if(!r||d>50||hit) return;
        for(const el of (r.querySelectorAll?r.querySelectorAll('ytcp-video-metadata-visibility,ytcp-text-dropdown-trigger,div,span'):[])){
          const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
          if(/^Visibility\\s+(Private|Public|Unlisted|Scheduled\\b.*)$/i.test(t)){
            hit=t; return;
          }
          if(/^(Private|Public|Unlisted)$/i.test(t) && t.length<20){
            // keep looking for fuller label
          }
        }
        for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
          if(el.shadowRoot) walk(el.shadowRoot,d+1);
      };
      walk(document);
      if(hit) return hit;
      const body=document.body.innerText||'';
      let m=body.match(/Visibility\\s*\\n?\\s*(Private|Public|Unlisted|Scheduled[^\\n]*)/i);
      if(m) return 'Visibility '+m[1].trim();
      m=body.match(/Scheduled\\s+for\\s+[^\\n]+/i);
      return m?m[0].trim():'';
    }"""
    )
    return chip or ""


def thumb_hint(page) -> dict:
    return page.evaluate(
        """()=>{
      const out={custom:false, imgs:[]};
      const walk=(r,d=0)=>{
        if(!r||d>45) return;
        for(const img of (r.querySelectorAll?r.querySelectorAll('img'):[])){
          const src=img.getAttribute('src')||'';
          if(/thumbnail|i\\.ytimg|ggpht|googleusercontent/i.test(src)){
            out.imgs.push({src:src.slice(0,160), w:img.naturalWidth||0});
          }
        }
        for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
          if(el.shadowRoot) walk(el.shadowRoot,d+1);
      };
      walk(document);
      out.custom = out.imgs.some(i=>i.w>80);
      return out;
    }"""
    )


def save_enabled(page) -> bool:
    return bool(
        page.evaluate(
            """()=>{
      const walk=(r,d=0)=>{
        if(!r||d>50) return false;
        for(const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,[role=button]'):[])){
          const t=(el.innerText||'').trim();
          if(/^Save$/i.test(t)){
            const dis=el.disabled || el.getAttribute('aria-disabled')==='true' || el.classList.contains('disabled');
            if(!dis) return true;
          }
        }
        for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
          if(el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
        return false;
      };
      return walk(document);
    }"""
        )
    )


def page_save(page) -> dict:
    """Click main Save; wait until it greys out or toast appears."""
    info = {"enabled_before": save_enabled(page)}
    # Try role first
    clicked = False
    save = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
    if save.count():
        try:
            if save.first.is_enabled():
                save.first.click(force=True, timeout=4000)
                clicked = True
                info["via"] = "role"
        except Exception as e:
            info["role_err"] = str(e)[:120]
    if not clicked:
        clicked = bool(
            page.evaluate(
                """()=>{
          const walk=(r,d=0)=>{
            if(!r||d>50) return false;
            for(const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,[role=button]'):[])){
              if(/^Save$/i.test((el.innerText||'').trim())){
                const dis=el.disabled || el.getAttribute('aria-disabled')==='true';
                if(!dis){ el.click(); return true; }
              }
            }
            for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            return false;
          };
          return walk(document);
        }"""
            )
        )
        if clicked:
            info["via"] = "js"
    info["clicked"] = clicked
    if not clicked:
        info["ok"] = False
        return info
    # Wait for save to settle
    for i in range(40):
        page.wait_for_timeout(400)
        if not save_enabled(page):
            info["grey_after_ms"] = i * 400
            break
        t = body(page, 1200)
        if re.search(r"saved|published|scheduled", t, re.I):
            info["toast"] = True
            break
    page.wait_for_timeout(1200)
    info["enabled_after"] = save_enabled(page)
    info["ok"] = clicked and (not info.get("enabled_after", True) or info.get("toast"))
    return info


def open_vis(page) -> bool:
    ok = page.evaluate(
        """()=>{
      const walk=(r,d=0)=>{
        if(!r||d>55) return false;
        for(const el of (r.querySelectorAll?r.querySelectorAll('ytcp-icon-button,button,[role=button]'):[])){
          if(/edit video visibility status/i.test(el.getAttribute('aria-label')||'')){
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
    return bool(ok)


def vis_dialog_open(page) -> bool:
    return bool(
        re.search(r"Save or publish", body(page, 4000), re.I)
        and re.search(r"Private", body(page, 4000), re.I)
    )


def click_radio(page, label: str) -> str:
    """Click Private/Unlisted/Public/Schedule radio inside Save-or-publish dialog."""
    # Prefer Playwright role
    try:
        radio = page.get_by_role("radio", name=re.compile(rf"^{re.escape(label)}$", re.I))
        if radio.count():
            radio.first.click(force=True, timeout=3000)
            page.wait_for_timeout(600)
            return f"role:{label}"
    except Exception:
        pass
    hit = page.evaluate(
        """(label)=>{
      const re=new RegExp('^'+label+'$','i');
      let dlg=null;
      const find=(r,d=0)=>{
        if(!r||d>50||dlg) return;
        for(const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-dialog,ytcp-dialog'):[])){
          const t=el.innerText||'';
          if(/Save or publish/i.test(t) && /Private/i.test(t)){ dlg=el; return; }
        }
        for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
          if(el.shadowRoot) find(el.shadowRoot,d+1);
      };
      find(document);
      if(!dlg) return null;
      let hit=null;
      const walk=(r,d=0)=>{
        if(!r||d>45||hit) return;
        for(const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-radio-button,[role=radio]'):[])){
          const t=((el.innerText||'')+' '+(el.getAttribute('aria-label')||'')).replace(/\\s+/g,' ').trim();
          if(re.test(t.split('\\n')[0].trim()) || re.test(t)){ el.click(); hit=t.slice(0,60); return; }
        }
        // Schedule is sometimes not a radio — click labeled row
        for(const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,div,span'):[])){
          const t=((el.innerText||'')+' '+(el.getAttribute('aria-label')||'')).replace(/\\s+/g,' ').trim();
          if(re.test(t) && t.length<40){ el.click(); hit='row:'+t; return; }
        }
        for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
          if(el.shadowRoot) walk(el.shadowRoot,d+1);
      };
      walk(dlg); return hit;
    }""",
        label,
    )
    page.wait_for_timeout(700)
    return hit or ""


def click_done(page) -> str:
    try:
        btn = page.get_by_role("button", name=re.compile(r"^Done$", re.I))
        if btn.count() and btn.first.is_enabled():
            btn.first.click(force=True, timeout=4000)
            page.wait_for_timeout(1000)
            return "role:Done"
    except Exception:
        pass
    hit = page.evaluate(
        """()=>{
      let dlg=null;
      const find=(r,d=0)=>{
        if(!r||d>50||dlg) return;
        for(const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-dialog,ytcp-dialog'):[])){
          const t=el.innerText||'';
          if(/Save or publish/i.test(t)){ dlg=el; return; }
        }
        for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
          if(el.shadowRoot) find(el.shadowRoot,d+1);
      };
      find(document);
      const root=dlg||document;
      let hit=null;
      const walk=(r,d=0)=>{
        if(!r||d>45||hit) return;
        for(const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,[role=button]'):[])){
          if(/^Done$/i.test((el.innerText||'').trim()) && !el.disabled){ el.click(); hit='js:Done'; return; }
        }
        for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
          if(el.shadowRoot) walk(el.shadowRoot,d+1);
      };
      walk(root); return hit;
    }"""
    )
    page.wait_for_timeout(1000)
    return hit or ""


def fill_schedule(page, day: int) -> dict:
    info: dict = {"day": day}
    cur = page.evaluate(
        """()=>{
      let hit='';
      const walk=(r,d=0)=>{
        if(!r||d>50||hit) return;
        for(const el of (r.querySelectorAll?r.querySelectorAll('ytcp-text-dropdown-trigger,ytcp-dropdown-trigger'):[])){
          const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
          if(/^\\d{1,2}\\s+Sept\\s+2026$/i.test(t)){ hit=t; return; }
        }
        for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
          if(el.shadowRoot) walk(el.shadowRoot,d+1);
      };
      walk(document); return hit;
    }"""
    )
    info["date_before"] = cur
    if not re.search(rf"^{day}\\s+Sept\\s+2026$", cur or "", re.I):
        page.evaluate(
            """()=>{
          const walk=(r,d=0)=>{
            if(!r||d>50) return false;
            for(const el of (r.querySelectorAll?r.querySelectorAll('ytcp-text-dropdown-trigger,ytcp-dropdown-trigger'):[])){
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if(/^\\d{1,2}\\s+Sept\\s+2026$/i.test(t)){ el.click(); return true; }
            }
            for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            return false;
          };
          return walk(document);
        }"""
        )
        page.wait_for_timeout(900)
        picked = page.evaluate(
            """(day)=>{
          let hit=null;
          const walk=(r,d=0)=>{
            if(!r||d>55||hit) return;
            for(const el of (r.querySelectorAll?r.querySelectorAll('button,[role=gridcell],div,span'):[])){
              const t=(el.innerText||'').trim();
              const aria=el.getAttribute('aria-label')||'';
              const rct=el.getBoundingClientRect();
              if(rct.width<8||rct.height<8||rct.width>90) continue;
              if(t===String(day) || new RegExp('\\\\b'+day+'\\\\b').test(aria)){
                el.click(); hit=aria||t; return;
              }
            }
            for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot) walk(el.shadowRoot,d+1);
          };
          walk(document); return hit;
        }""",
            day,
        )
        info["date_picked"] = picked
        page.wait_for_timeout(700)

    focused = page.evaluate(
        """()=>{
      let el=null;
      const walk=(r,d=0)=>{
        if(!r||d>55||el) return;
        for(const inp of (r.querySelectorAll?r.querySelectorAll('input'):[])){
          if(/^\\d{1,2}:\\d{2}$/.test(inp.value||'')){ el=inp; return; }
        }
        for(const n of (r.querySelectorAll?r.querySelectorAll('*'):[]))
          if(n.shadowRoot) walk(n.shadowRoot,d+1);
      };
      walk(document);
      if(!el) return {ok:false};
      el.focus(); el.select && el.select();
      return {ok:true, old:el.value||''};
    }"""
    )
    info["time_focus"] = focused
    if focused and focused.get("ok"):
        page.keyboard.press("Meta+a")
        page.keyboard.type("11:30", delay=40)
        page.keyboard.press("Tab")
        page.wait_for_timeout(500)
        info["time_typed"] = "11:30"

    after = page.evaluate(
        """()=>{
      let date='', time='';
      const walk=(r,d=0)=>{
        if(!r||d>50) return;
        for(const el of (r.querySelectorAll?r.querySelectorAll('ytcp-text-dropdown-trigger,div,span'):[])){
          const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
          if(/^\\d{1,2}\\s+Sept\\s+2026$/i.test(t)) date=t;
        }
        for(const inp of (r.querySelectorAll?r.querySelectorAll('input'):[])){
          if(/^\\d{1,2}:\\d{2}$/.test(inp.value||'')) time=inp.value;
        }
        for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
          if(el.shadowRoot) walk(el.shadowRoot,d+1);
      };
      walk(document); return {date, time};
    }"""
    )
    info["after"] = after
    info["ok"] = bool(
        after
        and re.search(rf"^{day}\\s+Sept", after.get("date") or "", re.I)
        and str(after.get("time") or "").startswith("11:30")
    )
    return info


def commit_visibility(page, mode: str, day: int | None = None) -> dict:
    """mode: private | schedule. Save WHILE dialog open (Save goes blue on pick), then Done+Save."""
    notes = []
    if not open_vis(page):
        return {"ok": False, "error": "open_vis_failed"}
    if not vis_dialog_open(page):
        notes.append("dialog_maybe_missing")
    shot(page, f"v02_{mode}_dialog_open.png")

    if mode == "private":
        notes.append(f"radio={click_radio(page, 'Private')}")
        page.wait_for_timeout(600)
        shot(page, "v02_private_selected.png")
    else:
        notes.append(f"radio={click_radio(page, 'Schedule')}")
        page.wait_for_timeout(1200)
        shot(page, "v02_schedule_panel.png")
        dt = fill_schedule(page, day or 7)
        notes.append(f"dt={dt}")
        shot(page, "v02_schedule_filled.png")
        if not dt.get("ok"):
            notes.append("dt_soft_fail")

    # KEY FIX: main Save turns blue while dialog is open after Private/Schedule pick.
    # Click Save FIRST while dialog still open, then Done, then Save again if needed.
    notes.append(f"save_enabled_pre={save_enabled(page)}")
    save1 = page_save(page)
    notes.append(f"save_while_open={save1}")
    page.wait_for_timeout(1000)

    # Confirm unpublish / schedule prompts if any
    for name in ["Set private", "Set to private", "Update", "Confirm", "Schedule", "Yes", "OK"]:
        try:
            b = page.get_by_role("button", name=re.compile(rf"^{re.escape(name)}$", re.I))
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=1500)
                notes.append(f"confirm={name}")
                page.wait_for_timeout(1000)
        except Exception:
            pass

    if vis_dialog_open(page):
        notes.append(f"done={click_done(page)}")
        for _ in range(20):
            if not vis_dialog_open(page):
                break
            page.wait_for_timeout(250)
        notes.append(f"dialog_closed={not vis_dialog_open(page)}")
        notes.append(f"save_enabled_post_done={save_enabled(page)}")
        save2 = page_save(page)
        notes.append(f"save_after_done={save2}")
        save_info = save2 if save2.get("clicked") else save1
    else:
        save_info = save1
        # still try save if enabled
        if save_enabled(page):
            save3 = page_save(page)
            notes.append(f"save_extra={save3}")
            save_info = save3 if save3.get("clicked") else save_info

    page.wait_for_timeout(1500)
    return {"ok": bool(save_info.get("ok") or save_info.get("clicked")), "notes": notes, "save": save_info}


def make_private(page, vid: str, slot: str) -> dict:
    open_edit(page, vid)
    shot(page, f"v02_10_{slot}_{vid}_before.png")
    thumb0 = thumb_hint(page)
    vis0 = visibility(page)
    if re.search(r"Private", vis0 or "", re.I) and not re.search(
        r"Public", vis0 or "", re.I
    ):
        return {
            "ok": True,
            "already": True,
            "visibility_before": vis0,
            "visibility_after": vis0,
            "thumb_before": thumb0,
            "thumb_after": thumb0,
        }

    last = {}
    for attempt in range(1, 4):
        log(f"  private attempt {attempt}")
        last = commit_visibility(page, "private")
        open_edit(page, vid)
        vis1 = visibility(page)
        shot(page, f"v02_13_{slot}_{vid}_after_private_a{attempt}.png")
        if re.search(r"Private", vis1 or "", re.I) and not re.search(
            r"^Visibility Public$|^Public$", vis1 or "", re.I
        ):
            return {
                "ok": True,
                "visibility_before": vis0,
                "visibility_after": vis1,
                "thumb_before": thumb0,
                "thumb_after": thumb_hint(page),
                "commit": last,
                "attempts": attempt,
            }
        last["visibility_after_attempt"] = vis1
    return {
        "ok": False,
        "visibility_before": vis0,
        "visibility_after": visibility(page),
        "thumb_before": thumb0,
        "thumb_after": thumb_hint(page),
        "commit": last,
    }


def make_schedule(page, job: dict) -> dict:
    vid, slot, day = job["id"], job["slot"], job["day"]
    open_edit(page, vid)
    shot(page, f"v02_20_{slot}_{vid}_before.png")
    thumb0 = thumb_hint(page)
    vis0 = visibility(page)
    last = {}
    for attempt in range(1, 4):
        log(f"  schedule attempt {attempt} day={day}")
        last = commit_visibility(page, "schedule", day=day)
        open_edit(page, vid)
        vis1 = visibility(page)
        snip = body(page, 3500)
        shot(page, f"v02_23_{slot}_{vid}_after_sched_a{attempt}.png")
        ok = bool(
            re.search(r"Scheduled", vis1 or snip, re.I)
            and (
                re.search(
                    rf"{day}\\s*Sept|{day}\\s*Sep|Sept(?:ember)?\\s*{day}",
                    vis1 or snip,
                    re.I,
                )
                or re.search(r"11:30|11\\.30", snip)
            )
        )
        if ok:
            return {
                "ok": True,
                "visibility_before": vis0,
                "visibility_after": vis1,
                "thumb_before": thumb0,
                "thumb_after": thumb_hint(page),
                "commit": last,
                "attempts": attempt,
                "label": job["label"],
                "snip": snip[:500],
            }
        last["visibility_after_attempt"] = vis1
    return {
        "ok": False,
        "visibility_before": vis0,
        "visibility_after": visibility(page),
        "thumb_before": thumb0,
        "thumb_after": thumb_hint(page),
        "commit": last,
        "label": job["label"],
    }


def related_trigger(page) -> str:
    return (
        page.evaluate(
            """()=>{
      let hit='';
      const walk=(r,d=0)=>{
        if(!r||d>50||hit) return;
        for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[])){
          const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
          if(/^Related video\\b/i.test(t) && t.length<280){ hit=t; return; }
        }
        for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
          if(el.shadowRoot) walk(el.shadowRoot,d+1);
      };
      walk(document); return hit;
    }"""
        )
        or ""
    )


def check_related(page, vid: str, slot: str) -> dict:
    open_edit(page, vid)
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(800)
    trig = related_trigger(page)
    shot(page, f"v02_30_{slot}_{vid}_related.png")
    ok = bool(RELATED_RE.search(trig) or RELATED in trig) or (
        "Related video" in trig and "None" not in trig and len(trig) > 18
    )
    return {"ok": ok, "trigger": trig}


def snapshot(page, vid: str, tag: str) -> dict:
    open_edit(page, vid)
    shot(page, f"{tag}_{vid}.png")
    return {
        "id": vid,
        "visibility": visibility(page),
        "thumb": thumb_hint(page),
        "related": related_trigger(page),
        "shot": f"{tag}_{vid}.png",
    }


def ensure_hos(page) -> dict:
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    ok = wait_studio(page)
    dismiss(page)
    t = body(page, 2500)
    shot(page, "v02_00_hos_boot.png")
    return {
        "ok": ok
        and (
            "History of Science" in t
            or HANDLE.lower() in t.lower()
            or CHANNEL in page.url
        ),
        "url": page.url,
        "snippet": t[:400],
    }


def main() -> int:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    result = {
        "started": datetime.now(tz=LONDON).isoformat(timespec="seconds"),
        "version": "v02",
        "channel": HANDLE,
        "channelId": CHANNEL,
        "related": RELATED,
        "steps": {
            "1_private_now": [],
            "2_schedule_related": [],
            "3_leave_public": [],
            "4_old_twins": [],
        },
        "ok": False,
    }
    try:
        if not chrome_up():
            hard_reset_chrome()
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(CDP, timeout=60000)
            ctx = browser.contexts[0]
            page = next(
                (pg for pg in ctx.pages if "studio.youtube.com" in (pg.url or "")),
                None,
            ) or ctx.new_page()

            boot = ensure_hos(page)
            result["boot"] = boot
            log(f"boot ok={boot.get('ok')} url={boot.get('url')}")
            if not boot.get("ok"):
                result["error"] = "NOT_HOS"
                (EV / "RESULT_V02.json").write_text(json.dumps(result, indent=2))
                return 2

            for job in JOBS:
                log(f"PRIVATE {job['id']}")
                item = make_private(page, job["id"], job["slot"])
                item.update({"id": job["id"], "title": job["title"]})
                result["steps"]["1_private_now"].append(item)
                (EV / "RESULT_V02_PARTIAL.json").write_text(json.dumps(result, indent=2))
                log(f"  private ok={item.get('ok')} vis={item.get('visibility_after')}")

            for job in JOBS:
                log(f"SCHEDULE {job['id']} -> {job['label']}")
                sched = make_schedule(page, job)
                log(f"  schedule ok={sched.get('ok')} vis={sched.get('visibility_after')}")
                rel = check_related(page, job["id"], job["slot"])
                log(f"  related ok={rel.get('ok')} trig={rel.get('trigger')}")
                open_edit(page, job["id"])
                page.evaluate("window.scrollTo(0,0)")
                page.wait_for_timeout(500)
                shot(page, f"v02_40_{job['slot']}_{job['id']}_final_top.png")
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(500)
                shot(page, f"v02_41_{job['slot']}_{job['id']}_final_related.png")
                result["steps"]["2_schedule_related"].append(
                    {
                        "id": job["id"],
                        "title": job["title"],
                        "label": job["label"],
                        "schedule": sched,
                        "related": rel,
                        "final_visibility": visibility(page),
                        "final_related": related_trigger(page),
                        "final_thumb": thumb_hint(page),
                        "ok": bool(sched.get("ok") and rel.get("ok")),
                    }
                )
                (EV / "RESULT_V02_PARTIAL.json").write_text(json.dumps(result, indent=2))

            for it in PUBLICS:
                log(f"SNAPSHOT public {it['id']}")
                snap = snapshot(page, it["id"], "v02_50_public")
                snap["title"] = it["title"]
                result["steps"]["3_leave_public"].append(snap)

            for tid in TWINS:
                log(f"SNAPSHOT twin {tid}")
                try:
                    result["steps"]["4_old_twins"].append(
                        snapshot(page, tid, "v02_60_twin")
                    )
                except Exception as e:
                    result["steps"]["4_old_twins"].append(
                        {"id": tid, "error": str(e)[:200]}
                    )

            page.goto(
                f"https://studio.youtube.com/channel/{CHANNEL}/videos/short",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            wait_studio(page)
            page.wait_for_timeout(3000)
            dismiss(page)
            shot(page, "v02_90_content_shorts.png")
            result["content_shorts_shot"] = "v02_90_content_shorts.png"
            result["content_snip"] = body(page, 4000)

            priv_ok = all(x.get("ok") for x in result["steps"]["1_private_now"])
            sched_ok = all(x.get("ok") for x in result["steps"]["2_schedule_related"])
            pub_ok = all(
                re.search(r"Public", (x.get("visibility") or ""), re.I)
                for x in result["steps"]["3_leave_public"]
            )
            result["ok"] = bool(priv_ok and sched_ok and pub_ok)
            result["summary"] = {
                "private_ok": priv_ok,
                "schedule_related_ok": sched_ok,
                "publics_still_public": pub_ok,
            }
            result["finished"] = datetime.now(tz=LONDON).isoformat(timespec="seconds")
            (EV / "RESULT_V02.json").write_text(json.dumps(result, indent=2))
            # Also write RESULT.json as canonical for this restore
            (EV / "RESULT.json").write_text(json.dumps(result, indent=2))
            log(f"DONE ok={result['ok']} summary={result['summary']}")
            return 0 if result["ok"] else 1
    except Exception as e:
        result["error"] = str(e)
        result["traceback"] = traceback.format_exc()
        (EV / "RESULT_V02.json").write_text(json.dumps(result, indent=2))
        (EV / "RESULT.json").write_text(json.dumps(result, indent=2))
        log(f"FAIL {e}")
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
