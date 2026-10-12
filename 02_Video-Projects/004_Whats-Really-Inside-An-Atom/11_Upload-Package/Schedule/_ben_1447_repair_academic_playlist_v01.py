#!/usr/bin/env python3
"""Repair pass: Academic system = United Kingdom (not UAE); longs → How We Found Out playlist."""
from __future__ import annotations

import importlib.util
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
U004 = (
    REPO
    / "02_Video-Projects/004_Whats-Really-Inside-An-Atom/11_Upload-Package/Schedule"
    / "_upload_hos_004_shorts_v01.py"
)
EV = (
    REPO
    / "02_Video-Projects/004_Whats-Really-Inside-An-Atom/11_Upload-Package/Schedule"
    / "evidence_2026-09-30_whole_channel_1447"
)
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts" / "BEN_1447_whole_channel"
LONDON = ZoneInfo("Europe/London")
HOS = "UCXp7HkBIl1LgaznXuZHJyRg"
PLAYLIST = "History of Science: How We Found Out"
LONGS = ["_C92tIJCk8A", "AL_-qlWko_g", "frP_YrNShsU", "GHZDsiH7L7A"]


def load_u():
    spec = importlib.util.spec_from_file_location("u", U004)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def shot(page, name):
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    p = EV / name
    page.screenshot(path=str(p))
    shutil.copy2(p, ART / name)


def ensure_hos(page, u):
    page.goto(f"https://studio.youtube.com/channel/{HOS}", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(2500)
    u.dismiss(page)
    return HOS in page.url or "History of Science" in page.inner_text("body")


def show_more(page):
    for _ in range(8):
        ok = page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>45) return false;
                for (const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,[role=button]'):[])) {
                  if ((el.innerText||'').trim()==='Show more') { el.click(); return true; }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                return false;
              }; return walk(document);
            }"""
        )
        if not ok:
            break
        page.wait_for_timeout(350)


def scroll_find(page, pat):
    for _ in range(28):
        if page.evaluate(
            """(pat)=>{
              const re=new RegExp(pat,'i');
              const walk=(r,d=0)=>{
                if(!r||d>45) return false;
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  const t=(el.innerText||'').trim();
                  if (re.test(t) && t.length<80) { el.scrollIntoView({block:'center'}); return true; }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                return false;
              }; return walk(document);
            }""",
            pat,
        ):
            page.wait_for_timeout(250)
            return True
        page.mouse.wheel(0, 700)
        page.wait_for_timeout(70)
    return False


def academic_state(page):
    body = page.inner_text("body")
    return {
        "uk": "Academic system United Kingdom" in body or re.search(r"Academic system\s+United Kingdom", body),
        "uae": "United Arab Emirates" in body,
        "snip": re.search(r"Academic system[^\n]{0,60}", body),
    }


def set_academic_uk(page) -> dict:
    scroll_find(page, r"Academic system")
    # Click the Academic system dropdown value area
    trig = page.evaluate(
        """()=>{
          let lab=null;
          const walk=(r,d=0)=>{
            if(!r||d>50||lab) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (t==='Academic system' || t.startsWith('Academic system\\n')) {
                const b=el.getBoundingClientRect();
                if (b.width>20&&b.height>10&&b.y>40) lab={x:b.x,y:b.y,w:b.width,h:b.height};
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          if(!lab) return null;
          // click to the right of the label (the value control)
          return {x:lab.x+Math.min(lab.w+180, 420), y:lab.y+lab.h/2};
        }"""
    )
    out = {"trig": trig}
    if not trig:
        return {**out, "error": "no_trig"}
    page.mouse.click(trig["x"], trig["y"])
    page.wait_for_timeout(900)
    # Type carefully — "United Kingdom" not United Arab
    page.keyboard.press("Meta+a")
    page.keyboard.type("United Kingdom", delay=40)
    page.wait_for_timeout(1400)
    # Pick ONLY exact United Kingdom (reject UAE)
    pick = page.evaluate(
        """()=>{
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-item,[role=option],yt-formatted-string,div,span'):[])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (t!=='United Kingdom') continue;
              const b=el.getBoundingClientRect();
              if (b.width>40&&b.height>16&&b.y>40&&b.y<1050)
                out.push({t,x:b.x+b.width/2,y:b.y+b.height/2});
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          return out;
        }"""
    )
    out["opts"] = pick
    if pick:
        pick.sort(key=lambda o: abs(o["y"] - 500))
        page.mouse.click(pick[0]["x"], pick[0]["y"])
        page.wait_for_timeout(700)
        out["picked"] = pick[0]["t"]
    else:
        out["picked"] = None
        page.keyboard.press("Escape")
    return out


def add_playlist(page) -> dict:
    scroll_find(page, r"Playlists")
    page.wait_for_timeout(400)
    # Click "Select" / playlist add near Playlists
    btn = page.evaluate(
        """()=>{
          const walk=(r,d=0)=>{
            if(!r||d>50) return null;
            for (const el of (r.querySelectorAll?r.querySelectorAll('ytcp-button,button,[role=button]'):[])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (/^(Select|Add to playlist|Playlists)$/i.test(t) || (/playlist/i.test(t)&&t.length<28)) {
                const b=el.getBoundingClientRect();
                if (b.width>30&&b.height>16&&b.y>80)
                  return {x:b.x+b.width/2,y:b.y+b.height/2,t:t.slice(0,40)};
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
            return null;
          }; return walk(document);
        }"""
    )
    out = {"btn": btn}
    if btn:
        page.mouse.click(btn["x"], btn["y"])
        page.wait_for_timeout(1500)
    chk = page.evaluate(
        """(name)=>{
          const walk=(r,d=0)=>{
            if(!r||d>50) return null;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=checkbox],tp-yt-paper-checkbox'):[])) {
              const lab=(el.getAttribute('aria-label')||el.innerText||'').replace(/\\s+/g,' ');
              if (/How We Found Out/i.test(lab) || lab.includes(name)) {
                const on=el.getAttribute('aria-checked')==='true';
                if (!on) el.click();
                return {lab:lab.slice(0,90), before:on, after:el.getAttribute('aria-checked')==='true'};
              }
            }
            // also list checkboxes for debug
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
            return null;
          }; return walk(document);
        }""",
        PLAYLIST,
    )
    out["check"] = chk
    # Done button
    page.evaluate(
        """()=>{
          const walk=(r,d=0)=>{
            if(!r||d>50) return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button'):[])) {
              if (/^Done$/i.test((el.innerText||'').trim())) { el.click(); return true; }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            return false;
          }; return walk(document);
        }"""
    )
    page.wait_for_timeout(600)
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    return out


def main():
    inv = json.loads(
        (Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos_full_inventory.json").read_text()
    )
    ids = [v["id"] for v in inv["videos"]]
    u = load_u()
    results = []
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9460")
        page = browser.contexts[0].new_page()
        page.set_default_timeout(60000)
        assert ensure_hos(page, u)
        for vid in ids:
            print(f"REPAIR {vid}", flush=True)
            page.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded", timeout=120000)
            page.wait_for_timeout(3000)
            u.dismiss(page)
            if re.search(r"\bOops\b", page.inner_text("body"), re.I):
                results.append({"id": vid, "oops": True})
                shot(page, f"{vid}_repair_OOPS.png")
                continue
            show_more(page)
            before = academic_state(page)
            out = {"id": vid, "before": {"uk": before["uk"], "uae": before["uae"]}}
            if before["uae"] or not before["uk"]:
                pick = set_academic_uk(page)
                out["pick"] = pick
                if pick.get("picked") == "United Kingdom":
                    s = u.page_save(page)
                    page.wait_for_timeout(2200)
                    out["save"] = s
                    out["changed"] = "academic_uk"
                else:
                    out["would_not_save"] = "academic_uk_pick_failed"
            else:
                out["changed"] = "academic_already_uk"
            if vid in LONGS:
                pl = add_playlist(page)
                out["playlist"] = pl
                if pl.get("check") and (pl["check"].get("after") or pl["check"].get("before")):
                    s = u.page_save(page)
                    page.wait_for_timeout(2000)
                    out["playlist_save"] = s
                    out["playlist_ok"] = True
                else:
                    out["playlist_ok"] = False
            after = academic_state(page)
            out["after"] = {"uk": after["uk"], "uae": after["uae"]}
            shot(page, f"{vid}_repair_final.png")
            results.append(out)
            print(f"  {out.get('changed')} uk={out['after']['uk']} uae={out['after']['uae']} pl={out.get('playlist_ok')}", flush=True)
        page.close()
    dest = EV / "REPAIR_RESULT.json"
    dest.write_text(json.dumps({"at": datetime.now(LONDON).isoformat(timespec="seconds"), "results": results}, indent=2, default=str))
    shutil.copy2(dest, ART / "REPAIR_RESULT.json")
    print("WROTE", dest)


if __name__ == "__main__":
    main()
