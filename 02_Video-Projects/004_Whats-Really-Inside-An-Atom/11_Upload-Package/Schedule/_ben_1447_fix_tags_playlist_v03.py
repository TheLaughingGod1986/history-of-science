#!/usr/bin/env python3
"""Fix corrupted tags (concatenated chips) + create How We Found Out playlist for longs."""
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
SWEEP = (
    REPO
    / "02_Video-Projects/004_Whats-Really-Inside-An-Atom/11_Upload-Package/Schedule"
    / "_ben_1447_whole_channel_studio_v01.py"
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


def load_mod(path):
    spec = importlib.util.spec_from_file_location("m", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def shot(page, name):
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    p = EV / name
    page.screenshot(path=str(p))
    shutil.copy2(p, ART / name)


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
        page.wait_for_timeout(200)


def scroll_tags(page):
    page.evaluate(
        """()=>{
          const walk=(r,d=0)=>{
            if(!r||d>55) return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (t==='Tags' || t.startsWith('Tags\\n')) { el.scrollIntoView({block:'center'}); return true; }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            return false;
          }; return walk(document);
        }"""
    )
    page.wait_for_timeout(300)


def read_chips(page) -> list[str]:
    return page.evaluate(
        """()=>{
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('ytcp-chip'):[])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim().replace(/×$/,'').trim();
              if (t && t.length<90) out.push(t);
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          return [...new Set(out)];
        }"""
    )


def clear_all_chips(page) -> int:
    n = 0
    for _ in range(60):
        hit = page.evaluate(
            """()=>{
              const walk=(r,d=0)=>{
                if(!r||d>55) return null;
                for (const el of (r.querySelectorAll?r.querySelectorAll('ytcp-chip #delete-icon, ytcp-chip button, ytcp-chip [aria-label*=Remove], ytcp-chip [aria-label*=remove], ytcp-chip [aria-label*=Delete], ytcp-chip iron-icon'):[])) {
                  const b=el.getBoundingClientRect();
                  if (b.width>6&&b.height>6&&b.y>40&&b.y<1100) {
                    el.click();
                    return {ok:true,y:b.y};
                  }
                }
                // fallback: chip itself has remove at right
                for (const el of (r.querySelectorAll?r.querySelectorAll('ytcp-chip'):[])) {
                  const b=el.getBoundingClientRect();
                  if (b.width>30&&b.height>14&&b.y>40&&b.y<1100)
                    return {click_xy:true, x:b.x+b.width-10, y:b.y+b.height/2};
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
                return null;
              }; return walk(document);
            }"""
        )
        if not hit:
            break
        if hit.get("click_xy"):
            page.mouse.click(hit["x"], hit["y"])
        page.wait_for_timeout(220)
        n += 1
    return n


def tags_input(page):
    return page.evaluate(
        """()=>{
          const walk=(r,d=0)=>{
            if(!r||d>55) return null;
            for (const el of (r.querySelectorAll?r.querySelectorAll('input'):[])) {
              const aria=(el.getAttribute('aria-label')||'')+(el.getAttribute('placeholder')||'');
              const b=el.getBoundingClientRect();
              if (b.width>60&&b.height>10&&b.y>40&&b.y<1100 && /tag/i.test(aria))
                return {x:b.x+b.width/2,y:b.y+b.height/2,aria};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
            return null;
          }; return walk(document);
        }"""
    )


def set_tags(page, want: list[str]) -> dict:
    scroll_tags(page)
    before = read_chips(page)
    # already exact?
    if [t.lower() for t in before] == [t.lower() for t in want] and len(before) == len(want):
        return {"already": True, "chips": before}
    removed = clear_all_chips(page)
    # also select-all in input and delete residual text
    loc = tags_input(page)
    if loc:
        page.mouse.click(loc["x"], loc["y"])
        page.wait_for_timeout(150)
        page.keyboard.press("Meta+a")
        page.keyboard.press("Backspace")
        page.wait_for_timeout(200)
    # clear again if any chips remain
    removed += clear_all_chips(page)
    mid = read_chips(page)
    added = []
    loc = tags_input(page)
    if not loc:
        return {"error": "no_input", "before": before, "mid": mid, "removed": removed}
    for tag in want:
        page.mouse.click(loc["x"], loc["y"])
        page.wait_for_timeout(100)
        page.keyboard.type(tag, delay=18)
        page.keyboard.press("Enter")
        page.wait_for_timeout(350)
        added.append(tag)
    chips = read_chips(page)
    ok = [t.lower() for t in chips] == [t.lower() for t in want]
    # tolerate order differences
    if not ok:
        ok = set(t.lower() for t in chips) == set(t.lower() for t in want) and len(chips) == len(want)
    return {"before": before, "removed": removed, "mid": mid, "added": added, "chips": chips, "ok": ok}


def page_save(page, u):
    try:
        s = u.page_save(page)
        page.wait_for_timeout(2400)
        return s
    except Exception:
        return page.evaluate(
            """()=>{
              const walk=(r,d=0)=>{
                if(!r||d>50) return null;
                for (const el of (r.querySelectorAll?r.querySelectorAll('ytcp-button,button'):[])) {
                  if (/^Save$/i.test((el.innerText||'').trim())) {
                    if (el.getAttribute('aria-disabled')==='true') return {ok:false,disabled:true};
                    el.click(); return {ok:true};
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
                return null;
              }; return walk(document);
            }"""
        )


def create_playlist_on_channel(page) -> dict:
    page.goto(
        f"https://studio.youtube.com/channel/{HOS}/playlists",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    body = page.inner_text("body")
    out = {"page": "playlists", "already": PLAYLIST in body}
    if out["already"]:
        shot(page, "playlist_already_exists.png")
        return out
    # New playlist button
    btn = page.evaluate(
        """()=>{
          const walk=(r,d=0)=>{
            if(!r||d>50) return null;
            for (const el of (r.querySelectorAll?r.querySelectorAll('ytcp-button,button,[role=button]'):[])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (/^New playlist$/i.test(t) || /^Create$/i.test(t)) {
                const b=el.getBoundingClientRect();
                if (b.width>40&&b.height>16&&b.y>40) return {x:b.x+b.width/2,y:b.y+b.height/2,t};
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
            return null;
          }; return walk(document);
        }"""
    )
    out["btn"] = btn
    if not btn:
        shot(page, "playlist_no_new_btn.png")
        return {**out, "ok": False, "error": "no_new_btn"}
    page.mouse.click(btn["x"], btn["y"])
    page.wait_for_timeout(1500)
    shot(page, "playlist_create_dialog.png")
    # title input
    inp = page.evaluate(
        """()=>{
          const walk=(r,d=0)=>{
            if(!r||d>55) return null;
            for (const el of (r.querySelectorAll?r.querySelectorAll('input,textarea'):[])) {
              const b=el.getBoundingClientRect();
              const ph=(el.getAttribute('placeholder')||'')+(el.getAttribute('aria-label')||'');
              if (b.width>80&&b.height>10&&b.y>40&&b.y<1100)
                return {x:b.x+b.width/2,y:b.y+b.height/2,ph:ph.slice(0,60)};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
            return null;
          }; return walk(document);
        }"""
    )
    out["inp"] = inp
    if inp:
        page.mouse.click(inp["x"], inp["y"])
        page.wait_for_timeout(200)
        page.keyboard.press("Meta+a")
        page.keyboard.type(PLAYLIST, delay=20)
        page.wait_for_timeout(400)
    else:
        page.keyboard.type(PLAYLIST, delay=20)
    # Create
    page.evaluate(
        """()=>{
          const walk=(r,d=0)=>{
            if(!r||d>50) return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('ytcp-button,button'):[])) {
              const t=(el.innerText||'').trim();
              if (/^Create$/i.test(t)) { el.click(); return true; }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            return false;
          }; return walk(document);
        }"""
    )
    page.wait_for_timeout(2500)
    page.goto(
        f"https://studio.youtube.com/channel/{HOS}/playlists",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2500)
    out["after_body_has"] = PLAYLIST in page.inner_text("body")
    out["ok"] = out["after_body_has"]
    shot(page, "playlist_created.png")
    return out


def add_long_to_playlist(page, u, vid: str) -> dict:
    page.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(2500)
    u.dismiss(page)
    show_more(page)
    before = page.evaluate(
        """()=>{
          const el=document.querySelector('ytcp-video-metadata-playlists');
          return el?(el.innerText||'').replace(/\\s+/g,' ').trim().slice(0,160):'';
        }"""
    )
    out = {"before": before}
    if "How We Found Out" in before:
        out["already"] = True
        out["ok"] = True
        return out
    page.evaluate(
        """()=>{
          const el=document.querySelector('ytcp-video-metadata-playlists');
          if(!el) return;
          el.scrollIntoView({block:'center'});
          (el.querySelector('ytcp-text-dropdown-trigger')||el).click();
        }"""
    )
    page.wait_for_timeout(1400)
    chk = page.evaluate(
        """(name)=>{
          const walk=(r,d=0)=>{
            if(!r||d>55) return null;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=checkbox],tp-yt-paper-checkbox,ytcp-checkbox-lit'):[])) {
              const lab=(el.getAttribute('aria-label')||el.innerText||'').replace(/\\s+/g,' ');
              if (lab.includes(name) || /How We Found Out/i.test(lab)) {
                const on=el.getAttribute('aria-checked')==='true';
                if (!on) el.click();
                return {lab:lab.slice(0,120), before:on, after:el.getAttribute('aria-checked')};
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
            return null;
          }; return walk(document);
        }""",
        PLAYLIST,
    )
    out["check"] = chk
    page.evaluate(
        """()=>{
          const walk=(r,d=0)=>{
            if(!r||d>50) return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('ytcp-button,button'):[])) {
              if (/^Done$/i.test((el.innerText||'').trim())) { el.click(); return true; }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            return false;
          }; return walk(document);
        }"""
    )
    page.wait_for_timeout(700)
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    out["after"] = page.evaluate(
        """()=>{
          const el=document.querySelector('ytcp-video-metadata-playlists');
          return el?(el.innerText||'').replace(/\\s+/g,' ').trim().slice(0,160):'';
        }"""
    )
    if "How We Found Out" in (out.get("after") or "") or (chk and str(chk.get("after")) == "true"):
        out["save"] = page_save(page, u)
        out["ok"] = True
    else:
        out["ok"] = False
    return out


def main():
    sweep = load_mod(SWEEP)
    catalog = sweep.CATALOG
    u = load_mod(U004)
    inv = json.loads(
        (Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos_full_inventory.json").read_text()
    )
    ids = [v["id"] for v in inv["videos"]]
    results = {"tags": [], "playlist_create": None, "playlist_add": []}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9460")
        page = browser.contexts[0].new_page()
        page.set_default_timeout(60000)
        page.goto(f"https://studio.youtube.com/channel/{HOS}", wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(2000)
        u.dismiss(page)

        for vid in ids:
            want = catalog[vid]["tags"]
            print(f"TAGS {vid}", flush=True)
            page.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded", timeout=120000)
            page.wait_for_timeout(2600)
            u.dismiss(page)
            if re.search(r"\bOops\b", page.inner_text("body"), re.I):
                results["tags"].append({"id": vid, "oops": True})
                shot(page, f"{vid}_tags_OOPS.png")
                continue
            show_more(page)
            info = set_tags(page, want)
            out = {"id": vid, "want": want, **info}
            if info.get("already"):
                out["changed"] = False
            elif info.get("ok"):
                out["save"] = page_save(page, u)
                page.wait_for_timeout(800)
                show_more(page)
                scroll_tags(page)
                out["verify"] = read_chips(page)
                out["changed"] = True
                out["ok"] = set(t.lower() for t in out["verify"]) == set(t.lower() for t in want)
            else:
                out["ok"] = False
            shot(page, f"{vid}_tags_final.png")
            results["tags"].append(out)
            print(f"  ok={out.get('ok')} chips={out.get('verify') or out.get('chips')}", flush=True)

        print("PLAYLIST CREATE", flush=True)
        results["playlist_create"] = create_playlist_on_channel(page)
        print(" ", results["playlist_create"], flush=True)

        if results["playlist_create"].get("ok") or results["playlist_create"].get("already"):
            for vid in LONGS:
                print(f"PLAYLIST ADD {vid}", flush=True)
                pl = add_long_to_playlist(page, u, vid)
                results["playlist_add"].append({"id": vid, **pl})
                shot(page, f"{vid}_playlist_v03.png")
                print(f"  ok={pl.get('ok')} after={pl.get('after')}", flush=True)

        page.close()

    dest = EV / "FIX3_TAGS_PLAYLIST.json"
    payload = {"at": datetime.now(LONDON).isoformat(timespec="seconds"), **results}
    dest.write_text(json.dumps(payload, indent=2, default=str))
    shutil.copy2(dest, ART / "FIX3_TAGS_PLAYLIST.json")
    print("WROTE", dest)


if __name__ == "__main__":
    main()
