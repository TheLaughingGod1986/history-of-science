#!/usr/bin/env python3
"""Fix tags via Studio: Delete-key chip clear (works), then type tags + Enter + save."""
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
    page.wait_for_timeout(350)


def read_chips(page) -> list[str]:
    return page.evaluate(
        """()=>[...document.querySelectorAll('ytcp-chip')].map(c =>
          (c.innerText||'').replace(/\\s+/g,' ').trim().replace(/×$/,'').trim()
        ).filter(Boolean)"""
    )


def clear_chips_delete_key(page) -> int:
    """Focus each chip and press Delete until none remain."""
    n = 0
    for _ in range(50):
        chips = page.evaluate(
            """()=>[...document.querySelectorAll('ytcp-chip')].map(c=>{
              const b=c.getBoundingClientRect();
              return {t:(c.innerText||'').trim(), x:b.x+Math.min(20,b.width/2), y:b.y+b.height/2, w:b.width};
            }).filter(c=>c.w>10)"""
        )
        if not chips:
            break
        # always delete first chip
        c = chips[0]
        page.mouse.click(c["x"], c["y"])
        page.wait_for_timeout(120)
        page.keyboard.press("Delete")
        page.wait_for_timeout(220)
        n += 1
        # if chip still there, try Backspace
        still = page.evaluate(
            """(t)=>{
              return [...document.querySelectorAll('ytcp-chip')].some(c => (c.innerText||'').trim()===t);
            }""",
            c["t"],
        )
        if still:
            page.mouse.click(c["x"], c["y"])
            page.wait_for_timeout(80)
            page.keyboard.press("Backspace")
            page.wait_for_timeout(220)
    return n


def tags_input_xy(page):
    return page.evaluate(
        """()=>{
          const walk=(r,d=0)=>{
            if(!r||d>55) return null;
            for (const el of (r.querySelectorAll?r.querySelectorAll('input'):[])) {
              const aria=(el.getAttribute('aria-label')||'')+(el.getAttribute('placeholder')||'');
              const b=el.getBoundingClientRect();
              if (b.width>60&&b.height>10&&b.y>40&&b.y<1100 && /tag/i.test(aria))
                return {x:b.x+b.width/2,y:b.y+b.height/2};
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
    if set(t.lower() for t in before) == set(t.lower() for t in want) and len(before) == len(want):
        # also reject any concatenated garbage even if set equal somehow
        if not any(len(t) > 40 or re.search(r"history of \w+history", t) for t in before):
            return {"already": True, "chips": before}
    removed = clear_chips_delete_key(page)
    mid = read_chips(page)
    # clear residual input text
    loc = tags_input_xy(page)
    if loc:
        page.mouse.click(loc["x"], loc["y"])
        page.wait_for_timeout(100)
        page.keyboard.press("Meta+a")
        page.keyboard.press("Backspace")
        page.wait_for_timeout(150)
    # if chips remain, clear again
    if mid:
        removed += clear_chips_delete_key(page)
        mid = read_chips(page)
    loc = tags_input_xy(page)
    added = []
    if not loc:
        return {"before": before, "removed": removed, "mid": mid, "error": "no_input"}
    for tag in want:
        page.mouse.click(loc["x"], loc["y"])
        page.wait_for_timeout(80)
        page.keyboard.type(tag, delay=20)
        page.keyboard.press("Enter")
        page.wait_for_timeout(400)
        added.append(tag)
        # re-find input (layout may shift)
        loc = tags_input_xy(page) or loc
    chips = read_chips(page)
    ok = set(t.lower() for t in chips) == set(t.lower() for t in want) and len(chips) == len(want)
    # reject concatenation artifacts
    if any(re.search(r"history of \w+history|antisepti|spontaneou|periohistory|mendelehistory|elementhistory|listhistory", t) for t in chips):
        ok = False
    return {"before": before, "removed": removed, "mid": mid, "added": added, "chips": chips, "ok": ok}


def page_save(page, u):
    try:
        s = u.page_save(page)
        page.wait_for_timeout(2500)
        return s
    except Exception:
        r = page.evaluate(
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
        page.wait_for_timeout(2500)
        return r


def main():
    sweep = load_mod(SWEEP)
    catalog = sweep.CATALOG
    u = load_mod(U004)
    inv = json.loads(
        (Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos_full_inventory.json").read_text()
    )
    ids = [v["id"] for v in inv["videos"]]
    results = []
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9460")
        page = browser.contexts[0].new_page()
        page.set_default_timeout(60000)
        page.goto(f"https://studio.youtube.com/channel/{HOS}", wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(2000)
        u.dismiss(page)
        for vid in ids:
            want = catalog[vid]["tags"]
            print(f"TAGS4 {vid}", flush=True)
            page.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded", timeout=120000)
            page.wait_for_timeout(2600)
            u.dismiss(page)
            if re.search(r"\bOops\b", page.inner_text("body"), re.I):
                results.append({"id": vid, "oops": True})
                shot(page, f"{vid}_tags4_OOPS.png")
                continue
            if undo(page):
                page.wait_for_timeout(1200)
            show_more(page)
            info = set_tags(page, want)
            out = {"id": vid, "want": want, **info}
            if info.get("already"):
                out["ok"] = True
                out["changed"] = False
            elif info.get("ok"):
                out["save"] = page_save(page, u)
                page.wait_for_timeout(600)
                # re-open verify
                page.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded", timeout=120000)
                page.wait_for_timeout(2200)
                show_more(page)
                scroll_tags(page)
                out["verify"] = read_chips(page)
                out["ok"] = set(t.lower() for t in out["verify"]) == set(t.lower() for t in want) and len(out["verify"]) == len(want)
                out["changed"] = True
            else:
                out["ok"] = False
                # still save if we got closer? no — undo
                if undo(page):
                    page.wait_for_timeout(800)
            shot(page, f"{vid}_tags4_final.png")
            results.append(out)
            print(f"  ok={out.get('ok')} chips={out.get('verify') or out.get('chips')}", flush=True)
        page.close()
    dest = EV / "TAGS4_RESULT.json"
    payload = {"at": datetime.now(LONDON).isoformat(timespec="seconds"), "results": results}
    dest.write_text(json.dumps(payload, indent=2, default=str))
    shutil.copy2(dest, ART / "TAGS4_RESULT.json")
    ok_n = sum(1 for r in results if r.get("ok"))
    print(f"DONE ok={ok_n}/{len(results)} -> {dest}")


if __name__ == "__main__":
    main()
