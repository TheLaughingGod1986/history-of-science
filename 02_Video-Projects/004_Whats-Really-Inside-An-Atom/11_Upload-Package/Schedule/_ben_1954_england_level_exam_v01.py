#!/usr/bin/env python3
"""Ben 19:54 — Academic England on all 22; Level closest to 14–16 if saves; Exam GCSE if listed.

HOS only. One setting per save. Re-read Audience + Visibility after each save.
Do not touch playlist How We Found Out. Playlist: How Did We Discover…? | History of Science.
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
SWEEP = (
    REPO
    / "02_Video-Projects/004_Whats-Really-Inside-An-Atom/11_Upload-Package/Schedule"
    / "_ben_1447_whole_channel_studio_v01.py"
)
EV = (
    REPO
    / "02_Video-Projects/004_Whats-Really-Inside-An-Atom/11_Upload-Package/Schedule"
    / "evidence_2026-09-30_england_1954"
)
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts" / "BEN_1954_england"
LONDON = ZoneInfo("Europe/London")
HOS = "UCXp7HkBIl1LgaznXuZHJyRg"
PLAYLIST = "How Did We Discover"
LONGS_ORDER = ["_C92tIJCk8A", "AL_-qlWko_g", "frP_YrNShsU"]  # 004 GHZDsiH7L7A → launch day 15 Oct
LEVEL_CANDIDATES = ["Key stage 4", "Year 10", "Year 11", "Key stage 3"]


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


def edu_triggers(page) -> list[str]:
    return page.evaluate(
        """()=>{
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('ytcp-text-dropdown-trigger'):[])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (/Academic|Level|Exam|Type |Video language|Title and description|Education|Concept|England|United|Key stage|Year /i.test(t)
                  || t.startsWith('English') || t==='None' || t==='Select')
                out.push(t.slice(0,120));
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return [...new Set(out)];
        }"""
    )


def audience_vis(page) -> dict:
    body = page.inner_text("body")
    vis_m = re.search(r"Visibility\s*\n\s*(\w+)", body)
    return {
        "not_kids": ("No, it's not" in body and "Made for Kids" in body) or "not Made for Kids" in body,
        "visibility": vis_m.group(1) if vis_m else "",
        "kids_yes": "Yes, it's Made for Kids" in body and "No, it's not" not in body[: body.find("Age restriction") + 1] if "Age restriction" in body else False,
    }


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


def list_opts(page) -> list[str]:
    return page.evaluate(
        """()=>{
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-item,[role=option]'):[])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              const b=el.getBoundingClientRect();
              if (t && b.width>40&&b.height>14&&b.y>40&&b.y<1100) out.push(t.slice(0,90));
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          return [...new Set(out)];
        }"""
    )


def page_save(page, u) -> dict:
    try:
        s = u.page_save(page)
        page.wait_for_timeout(2400)
        return {"via": "u", "result": s}
    except Exception as e:
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
        page.wait_for_timeout(2400)
        return {"via": "fb", "result": r, "err": str(e)[:80]}


def reread(page) -> dict:
    return {"edu": edu_triggers(page), **audience_vis(page)}


def set_england(page, u) -> dict:
    before = edu_triggers(page)
    if any("Academic system England" in t for t in before):
        return {"already": True, "before": before}
    open_dd(page, r"Academic system")
    page.wait_for_timeout(700)
    page.keyboard.press("Meta+a")
    page.keyboard.press("Backspace")
    page.wait_for_timeout(150)
    page.keyboard.type("Engl", delay=40)
    page.wait_for_timeout(1100)
    pick = js_click_option(page, "England")
    page.wait_for_timeout(700)
    mid = edu_triggers(page)
    out = {"before": before, "pick": pick, "mid": mid}
    if any("England" in t for t in mid):
        out["save"] = page_save(page, u)
        out["after_save"] = reread(page)
        out["ok"] = any("Academic system England" in t for t in out["after_save"]["edu"])
    else:
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        out["ok"] = False
    return out


def set_level_14_16(page, u) -> dict:
    """Closest England option to ages 14–16; only if it persists after save+reload check mid."""
    before = edu_triggers(page)
    open_dd(page, r"^Level|Level ")
    page.wait_for_timeout(800)
    opts = list_opts(page)
    out = {"before": before, "opts_sample": opts[:40]}
    pick_want = None
    for cand in LEVEL_CANDIDATES:
        if cand in opts:
            pick_want = cand
            break
    if not pick_want:
        # any Key stage / Year 10-11
        for o in opts:
            if re.search(r"Key stage 4|Year 1[01]", o):
                pick_want = o
                break
    if not pick_want:
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        out["ok"] = False
        out["would_not_save"] = "no_14_16_level_option"
        return out
    click = js_click_option(page, pick_want)
    page.wait_for_timeout(700)
    mid = edu_triggers(page)
    out["want"] = pick_want
    out["click"] = click
    out["mid"] = mid
    if any(pick_want in t for t in mid):
        out["save"] = page_save(page, u)
        out["after_save"] = reread(page)
        out["ok"] = any(pick_want in t for t in out["after_save"]["edu"])
        if not out["ok"]:
            out["would_not_save"] = f"level_{pick_want}_reverted"
    else:
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        out["ok"] = False
        out["would_not_save"] = f"level_{pick_want}_pick_failed"
    return out


def set_exam_if_listed(page, u, exam: str) -> dict:
    before = edu_triggers(page)
    # click exam input
    hit = page.evaluate(
        """()=>{
          const walk=(r,d=0)=>{
            if(!r||d>55) return null;
            for (const el of (r.querySelectorAll?r.querySelectorAll('input'):[])) {
              const lab=el.getAttribute('aria-label')||'';
              if (/Exam/i.test(lab)) {
                const b=el.getBoundingClientRect();
                if (b.width>40&&b.y>40) { el.scrollIntoView({block:'center'}); el.click(); return {x:b.x+b.width/2,y:b.y+b.height/2}; }
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
            return null;
          }; return walk(document);
        }"""
    )
    out = {"exam_want": exam, "input": hit, "before": before}
    if not hit:
        out["ok"] = False
        out["would_not_save"] = "exam_input_missing"
        return out
    page.wait_for_timeout(400)
    page.keyboard.press("Meta+a")
    page.keyboard.press("Backspace")
    page.wait_for_timeout(150)
    page.keyboard.type(exam, delay=30)
    page.wait_for_timeout(1200)
    opts = list_opts(page)
    out["opts"] = opts[:30]
    exact = [o for o in opts if o == exam]
    if not exact:
        # reject AP / CBSE false friends
        exact = [o for o in opts if exam.lower() in o.lower() and "AP " not in o and "CBSE" not in o]
    if not exact:
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        out["ok"] = False
        out["blank"] = True
        out["would_not_save"] = f"exam_{exam}_not_in_taxonomy"
        return out
    click = js_click_option(page, exact[0])
    page.wait_for_timeout(700)
    out["click"] = click
    out["save"] = page_save(page, u)
    out["after_save"] = reread(page)
    out["ok"] = any(exam.split()[0] in t for t in out["after_save"]["edu"]) or any(
        exam in t for t in out["after_save"]["edu"]
    )
    if not out["ok"]:
        out["would_not_save"] = f"exam_{exam}_did_not_persist"
    return out


def ensure_playlist(page, u) -> dict:
    before = page.evaluate(
        """()=>{
          const el=document.querySelector('ytcp-video-metadata-playlists');
          return el?(el.innerText||'').replace(/\\s+/g,' ').trim().slice(0,200):'';
        }"""
    )
    out = {"before": before}
    if "How Did We Discover" in before:
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
        """()=>{
          const walk=(r,d=0)=>{
            if(!r||d>55) return null;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=checkbox],tp-yt-paper-checkbox,ytcp-checkbox-lit'):[])) {
              const lab=(el.getAttribute('aria-label')||el.innerText||'').replace(/\\s+/g,' ');
              if (/How Did We Discover/i.test(lab)) {
                const on=el.getAttribute('aria-checked')==='true';
                if (!on) el.click();
                return {lab:lab.slice(0,120), before:on, after:el.getAttribute('aria-checked')};
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
            return null;
          }; return walk(document);
        }"""
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
          return el?(el.innerText||'').replace(/\\s+/g,' ').trim().slice(0,200):'';
        }"""
    )
    if "How Did We Discover" in (out.get("after") or "") or (chk and str(chk.get("after")) == "true"):
        out["save"] = page_save(page, u)
        out["reread"] = reread(page)
        out["ok"] = True
    else:
        out["ok"] = False
    return out


def parse_final(edu: list[str]) -> dict:
    academic = next((t for t in edu if t.startswith("Academic system")), "Academic system ?")
    level = next((t for t in edu if t.startswith("Level")), "Level ?")
    exam = next((t for t in edu if "Exam" in t or t.startswith("GCSE")), "Exam blank/None")
    return {"academic": academic, "level": level, "exam": exam}


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
        assert HOS in page.url or "History of Science" in page.inner_text("body")

        for vid in ids:
            meta = catalog[vid]
            exam = meta["exam"]
            print(f"ENGLAND {vid} exam={exam}", flush=True)
            page.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded", timeout=120000)
            page.wait_for_timeout(2600)
            u.dismiss(page)
            if re.search(r"\bOops\b", page.inner_text("body"), re.I):
                results.append({"id": vid, "oops": True, "title": meta.get("film")})
                shot(page, f"{vid}_OOPS.png")
                continue
            show_more(page)
            out = {
                "id": vid,
                "film": meta["film"],
                "kind": meta["kind"],
                "exam_want": exam,
                "title": page.title(),
            }
            # 1) Academic England
            eng = set_england(page, u)
            out["england"] = eng
            show_more(page)
            # 2) Level
            lev = set_level_14_16(page, u)
            out["level"] = lev
            show_more(page)
            # 3) Exam if listed
            ex = set_exam_if_listed(page, u, exam)
            out["exam"] = ex
            # 4) Playlist for public longs 001-003
            if vid in LONGS_ORDER:
                pl = ensure_playlist(page, u)
                out["playlist"] = pl
            # final reload verify
            page.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded", timeout=120000)
            page.wait_for_timeout(2200)
            show_more(page)
            final = reread(page)
            out["final"] = final
            out["saved_fields"] = parse_final(final["edu"])
            out["audience_ok"] = final.get("not_kids")
            out["visibility"] = final.get("visibility")
            shot(page, f"{vid}_99_final.png")
            results.append(out)
            print(
                f"  {out['saved_fields']} aud={out['audience_ok']} vis={out['visibility']} "
                f"eng={eng.get('ok') or eng.get('already')} lev={lev.get('ok')} exam={ex.get('ok') or ex.get('blank')}",
                flush=True,
            )
        page.close()

    dest = EV / "ENGLAND_1954_RESULT.json"
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    payload = {
        "at": datetime.now(LONDON).isoformat(timespec="seconds"),
        "ordered_by": "Ben 19:54",
        "channel_id": HOS,
        "playlist_policy": "How Did We Discover…? | History of Science (001→003 now; 004 on launch day 15 Oct 18:00)",
        "results": results,
    }
    dest.write_text(json.dumps(payload, indent=2, default=str))
    shutil.copy2(dest, ART / "ENGLAND_1954_RESULT.json")
    # compact table
    table = []
    for r in results:
        sf = r.get("saved_fields") or {}
        table.append(
            {
                "id": r["id"],
                "film": r.get("film"),
                "kind": r.get("kind"),
                "academic": sf.get("academic"),
                "level": sf.get("level"),
                "exam": sf.get("exam"),
                "audience_ok": r.get("audience_ok"),
                "visibility": r.get("visibility"),
                "playlist": (r.get("playlist") or {}).get("ok"),
            }
        )
    (ART / "ENGLAND_1954_TABLE.json").write_text(json.dumps(table, indent=2))
    print("WROTE", dest, "n=", len(results))


if __name__ == "__main__":
    main()
