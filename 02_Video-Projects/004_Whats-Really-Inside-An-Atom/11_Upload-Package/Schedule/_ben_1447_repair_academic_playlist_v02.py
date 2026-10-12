#!/usr/bin/env python3
"""Repair v02: Level=Grade 10 (Secondary leaf); create/add How We Found Out playlist on longs.

Academic system "United Kingdom" is NOT in Studio taxonomy (England is; UK is not).
Per Ben 14:47 "United Kingdom if listed" → record won't-save, do not substitute.
GCSE exams remain not in taxonomy under UAE → leave recorded from main sweep.
"""
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
LEVEL_LEAF = "Grade 10"  # selectable leaf under Secondary school header


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
        page.wait_for_timeout(250)


def undo(page) -> bool:
    return bool(
        page.evaluate(
            """()=>{
          const walk=(r,d=0)=>{
            if(!r||d>50) return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button'):[])) {
              if (/^Undo changes$/i.test((el.innerText||'').trim())) { el.click(); return true; }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            return false;
          }; return walk(document);
        }"""
        )
    )


def edu_triggers(page) -> list[str]:
    return page.evaluate(
        """()=>{
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('ytcp-text-dropdown-trigger'):[])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (/Academic|Level|Exam/i.test(t)) out.push(t);
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return out;
        }"""
    )


def open_dd(page, pat: str):
    return page.evaluate(
        """(pat)=>{
          const re=new RegExp(pat,'i');
          const walk=(r,d=0)=>{
            if(!r||d>55) return null;
            for (const el of (r.querySelectorAll?r.querySelectorAll('ytcp-text-dropdown-trigger'):[])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ');
              if (re.test(t)) { el.scrollIntoView({block:'center'}); el.click(); return t.slice(0,100); }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
            return null;
          }; return walk(document);
        }""",
        pat,
    )


def js_click_option(page, want: str):
    return page.evaluate(
        """(want)=>{
          const walk=(r,d=0)=>{
            if(!r||d>55) return null;
            for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-item,[role=option]'):[])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (t===want) {
                const b=el.getBoundingClientRect();
                if (b.width>40&&b.height>14&&b.y>40&&b.y<1100) { el.click(); return {ok:true,t,y:b.y}; }
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
            return null;
          }; return walk(document);
        }""",
        want,
    )


def page_save(page, u) -> dict:
    try:
        s = u.page_save(page)
        page.wait_for_timeout(2200)
        return {"via": "u.page_save", "result": s}
    except Exception as e:
        ok = page.evaluate(
            """()=>{
              const walk=(r,d=0)=>{
                if(!r||d>50) return null;
                for (const el of (r.querySelectorAll?r.querySelectorAll('ytcp-button,button'):[])) {
                  if (/^Save$/i.test((el.innerText||'').trim())) {
                    if (el.getAttribute('aria-disabled')==='true') return {ok:false, disabled:true};
                    el.click(); return {ok:true};
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
                return null;
              }; return walk(document);
            }"""
        )
        page.wait_for_timeout(2200)
        return {"via": "fallback", "result": ok, "err": str(e)[:120]}


def set_level_grade10(page, u) -> dict:
    before = edu_triggers(page)
    if any(f"Level {LEVEL_LEAF}" in t for t in before):
        return {"already": True, "before": before}
    open_dd(page, r"Level")
    page.wait_for_timeout(800)
    click = js_click_option(page, LEVEL_LEAF)
    page.wait_for_timeout(700)
    mid = edu_triggers(page)
    out = {"before": before, "click": click, "mid": mid}
    if any(LEVEL_LEAF in t for t in mid):
        out["save"] = page_save(page, u)
        out["after"] = edu_triggers(page)
        out["ok"] = any(LEVEL_LEAF in t for t in out["after"])
    else:
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        out["ok"] = False
        out["would_not_save"] = "level_grade10_pick_failed"
    return out


def confirm_uk_absent(page) -> dict:
    """Probe once: United Kingdom not in Academic taxonomy."""
    open_dd(page, r"Academic system")
    page.wait_for_timeout(700)
    page.keyboard.press("Meta+a")
    page.keyboard.press("Backspace")
    page.wait_for_timeout(200)
    page.keyboard.type("United Kingdom", delay=35)
    page.wait_for_timeout(1100)
    opts = page.evaluate(
        """()=>{
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-item,[role=option]'):[])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              const b=el.getBoundingClientRect();
              if (t && b.width>40&&b.height>14&&b.y>40&&b.y<1100) out.push(t);
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          return [...new Set(out)];
        }"""
    )
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    page.wait_for_timeout(300)
    return {
        "united_kingdom_listed": "United Kingdom" in opts,
        "england_listed_elsewhere": True,  # confirmed prior probe
        "sample": opts[:20],
    }


def playlist_text(page) -> str:
    return page.evaluate(
        """()=>{
          const el=document.querySelector('ytcp-video-metadata-playlists');
          return el ? (el.innerText||'').replace(/\\s+/g,' ').trim().slice(0,200) : '';
        }"""
    )


def ensure_playlist_on_long(page, u) -> dict:
    before = playlist_text(page)
    out = {"before": before}
    if "How We Found Out" in before:
        out["already"] = True
        out["ok"] = True
        return out
    # open dialog
    page.evaluate(
        """()=>{
          const el=document.querySelector('ytcp-video-metadata-playlists');
          if(!el) return false;
          el.scrollIntoView({block:'center'});
          const t=el.querySelector('ytcp-text-dropdown-trigger');
          (t||el).click();
          return true;
        }"""
    )
    page.wait_for_timeout(1500)
    dlg = page.evaluate(
        """()=>{
          const d=document.querySelector('ytcp-playlist-dialog');
          return d ? (d.innerText||'').slice(0,800) : '';
        }"""
    )
    out["dialog"] = dlg[:400]
    if "How We Found Out" not in dlg:
        # create new playlist
        created = page.evaluate(
            """(name)=>{
              const dlg=document.querySelector('ytcp-playlist-dialog');
              if(!dlg) return {ok:false, reason:'no_dialog'};
              // click New playlist
              const walkClick=(r,d=0)=>{
                if(!r||d>40) return false;
                for (const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,a,[role=button]'):[])) {
                  if (/New playlist/i.test((el.innerText||'').trim())) { el.click(); return true; }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot && walkClick(el.shadowRoot,d+1)) return true;
                return false;
              };
              const clicked=walkClick(dlg) || (dlg.shadowRoot && walkClick(dlg.shadowRoot));
              return {clicked};
            }""",
            PLAYLIST,
        )
        out["new_click"] = created
        page.wait_for_timeout(1000)
        # type name into visible dialog input
        typed = page.evaluate(
            """(name)=>{
              const inputs=[...document.querySelectorAll('tp-yt-paper-dialog input, ytcp-playlist-dialog input, input')];
              for (const inp of inputs) {
                const b=inp.getBoundingClientRect();
                if (b.width>80&&b.height>10&&b.y>40&&b.y<1100 && inp.offsetParent!==null) {
                  inp.focus(); inp.value=''; inp.dispatchEvent(new Event('input',{bubbles:true}));
                  return {x:b.x+b.width/2,y:b.y+b.height/2};
                }
              }
              return null;
            }""",
            PLAYLIST,
        )
        out["input"] = typed
        if typed:
            page.mouse.click(typed["x"], typed["y"])
            page.wait_for_timeout(200)
            page.keyboard.press("Meta+a")
            page.keyboard.type(PLAYLIST, delay=20)
            page.wait_for_timeout(400)
            # Create / Done button
            page.evaluate(
                """()=>{
                  const walk=(r,d=0)=>{
                    if(!r||d>50) return false;
                    for (const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button'):[])) {
                      const t=(el.innerText||'').trim();
                      if (/^(Create|Done)$/i.test(t)) { el.click(); return t; }
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                      if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                    return false;
                  }; return walk(document);
                }"""
            )
            page.wait_for_timeout(1500)
    # re-open if needed and check the playlist
    page.evaluate(
        """()=>{
          const el=document.querySelector('ytcp-video-metadata-playlists');
          if(!el) return;
          const t=el.querySelector('ytcp-text-dropdown-trigger');
          (t||el).click();
        }"""
    )
    page.wait_for_timeout(1200)
    chk = page.evaluate(
        """(name)=>{
          const walk=(r,d=0)=>{
            if(!r||d>55) return null;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=checkbox],tp-yt-paper-checkbox,ytcp-checkbox-lit'):[])) {
              const lab=(el.getAttribute('aria-label')||el.innerText||'').replace(/\\s+/g,' ');
              if (lab.includes(name) || /How We Found Out/i.test(lab)) {
                const on=el.getAttribute('aria-checked')==='true' || el.getAttribute('aria-checked')===true;
                if (!on) el.click();
                return {lab:lab.slice(0,100), before:on, after:el.getAttribute('aria-checked')};
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
    # Done
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
    page.wait_for_timeout(800)
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    out["after_text"] = playlist_text(page)
    if "How We Found Out" in (out.get("after_text") or "") or (chk and chk.get("after") in ("true", True)):
        out["save"] = page_save(page, u)
        out["ok"] = True
    else:
        out["ok"] = False
        out["would_not_save"] = "playlist_how_we_found_out_missing_or_uncheckable"
    return out


def main():
    inv = json.loads(
        (Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos_full_inventory.json").read_text()
    )
    ids = [v["id"] for v in inv["videos"]]
    u = load_u()
    results = []
    uk_probe = None
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9460")
        page = browser.contexts[0].new_page()
        page.set_default_timeout(60000)
        assert ensure_hos(page, u)
        for i, vid in enumerate(ids):
            print(f"REPAIR2 {vid}", flush=True)
            page.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded", timeout=120000)
            page.wait_for_timeout(2800)
            u.dismiss(page)
            if re.search(r"\bOops\b", page.inner_text("body"), re.I):
                results.append({"id": vid, "oops": True})
                shot(page, f"{vid}_repair2_OOPS.png")
                continue
            if undo(page):
                page.wait_for_timeout(1200)
            show_more(page)
            out = {"id": vid, "changed": [], "would_not_save": []}
            if uk_probe is None:
                uk_probe = confirm_uk_absent(page)
                out["uk_probe"] = uk_probe
                if not uk_probe.get("united_kingdom_listed"):
                    out["would_not_save"].append("academic_system:United Kingdom_not_in_taxonomy")
            else:
                out["would_not_save"].append("academic_system:United Kingdom_not_in_taxonomy")
            lev = set_level_grade10(page, u)
            out["level"] = lev
            if lev.get("already"):
                out["changed"].append("level_grade10_already")
            elif lev.get("ok"):
                out["changed"].append("level_grade10")
            else:
                out["would_not_save"].append(lev.get("would_not_save") or "level_grade10_failed")
            if vid in LONGS:
                pl = ensure_playlist_on_long(page, u)
                out["playlist"] = pl
                if pl.get("already"):
                    out["changed"].append("playlist_already")
                elif pl.get("ok"):
                    out["changed"].append("playlist_how_we_found_out")
                else:
                    out["would_not_save"].append(pl.get("would_not_save") or "playlist_failed")
            out["edu_after"] = edu_triggers(page)
            out["visibility_snip"] = re.search(r"Visibility[^\n]{0,40}", page.inner_text("body"))
            out["not_kids"] = "not made for kids" in page.inner_text("body").lower() or "No, it's not made for kids" in page.inner_text("body")
            shot(page, f"{vid}_repair2_final.png")
            results.append(out)
            print(
                f"  level_ok={lev.get('ok') or lev.get('already')} pl={out.get('playlist',{}).get('ok')} edu={out['edu_after']}",
                flush=True,
            )
        page.close()
    dest = EV / "REPAIR2_RESULT.json"
    payload = {
        "at": datetime.now(LONDON).isoformat(timespec="seconds"),
        "uk_probe": uk_probe,
        "level_leaf": LEVEL_LEAF,
        "note": "United Kingdom absent from Academic system; Secondary school is non-selectable header → Grade 10 leaf",
        "results": results,
    }
    dest.write_text(json.dumps(payload, indent=2, default=str))
    shutil.copy2(dest, ART / "REPAIR2_RESULT.json")
    print("WROTE", dest)


if __name__ == "__main__":
    main()
