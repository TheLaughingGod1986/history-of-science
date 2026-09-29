#!/usr/bin/env python3
"""HOS 004 Studio phone-UAT v21 — live audit + finish remaining Ben items.

Order: main thumb A v04 → AI YES / Kids NO → A/B Title+thumbnail×3 →
Visibility 15 Oct 18:00 proof → end screen Specific 002 + Subscribe →
Content list check. Pin deferred while private/scheduled. CDP :9460 only.
"""
from __future__ import annotations

import json
import re
import shutil
import urllib.request
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

PORT = 9460
VIDEO_ID = "GHZDsiH7L7A"
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"
RELATED_002 = "AL_-qlWko_g"
RELATED_TITLE = "How Did We Discover the Periodic Table"
PROJ = Path(__file__).resolve().parents[2]
EV = PROJ / "11_Upload-Package/Schedule/evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos004_studio_phone_uat"
ART2 = Path("/opt/cursor/artifacts")
THUMBS = [
    PROJ / "08_Thumbnail/Selected/hos_004_thumb_A_atom_live_v04.jpg",
    PROJ / "08_Thumbnail/Selected/hos_004_thumb_C_hidden_number_live_v06.jpg",
    PROJ / "08_Thumbnail/Selected/hos_004_thumb_B_cut_gold_live_v04.jpg",
]
TITLES = [
    "What's Really Inside an Atom?",
    "Why Is the Periodic Table in This Order?",
    "How Small Can You Cut Gold?",
]


def log(m: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {m}"
    print(line, flush=True)
    with (EV / "phone_uat_v21.log").open("a") as f:
        f.write(line + "\n")


def dump(n: str, o) -> None:
    text = json.dumps(o, indent=2) + "\n"
    (EV / n).write_text(text)
    (ART / n).write_text(text)


def shot(page, n: str) -> Path:
    p = EV / n
    page.screenshot(path=str(p), full_page=False)
    (ART / n).write_bytes(p.read_bytes())
    try:
        ART2.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, ART2 / n)
    except Exception:
        pass
    return p


def dismiss(page) -> None:
    for _ in range(3):
        page.keyboard.press("Escape")
        page.wait_for_timeout(120)
        page.evaluate(
            """() => {
          const walk=(r,d=0)=>{
            if(!r||d>40)return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button'):[])) {
              const t=(el.innerText||'').trim();
              if (/^(Continue|Cancel|Close|Done|OK|Dismiss|Got it|OK, got it|Not now)$/i.test(t)) {
                el.click(); return t;
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          };
          return walk(document);
        }"""
        )


def deep_click(page, pattern: str, y_min: int = 60, max_len: int = 80) -> str | None:
    return page.evaluate(
        """({pattern,yMin,maxLen}) => {
          const re=new RegExp(pattern,'i');
          let best=null;
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (!t || t.length>maxLen) continue;
              if (!re.test(t)) continue;
              const rect=el.getBoundingClientRect();
              if (rect.y<yMin || rect.width<8 || rect.height<8) continue;
              const score=Math.abs(t.length-pattern.length)+rect.y/1000;
              if (!best || score<best.score) best={el,t,score,rect};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          };
          walk(document);
          if (!best) return null;
          best.el.scrollIntoView({block:'center'});
          best.el.click();
          return best.t;
        }""",
        {"pattern": pattern, "yMin": y_min, "maxLen": max_len},
    )


def body_text(page) -> str:
    return page.evaluate(
        """() => {
          let out='';
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            try { out += '\\n' + (r.innerText||''); } catch(e){}
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          };
          walk(document);
          return out;
        }"""
    )


def goto_edit(page) -> None:
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        wait_until="domcontentloaded",
        timeout=90000,
    )
    page.wait_for_timeout(4500)
    dismiss(page)


def save(page) -> bool:
    try:
        btn = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
        if btn.count() and btn.first.is_enabled():
            btn.first.click(force=True, timeout=8000)
            page.wait_for_timeout(4500)
            return True
    except Exception:
        pass
    hit = page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55)return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button'):[])) {
              const t=(el.innerText||'').trim();
              if (t==='Save'||t==='SAVE') {
                if (el.disabled||el.getAttribute('aria-disabled')==='true') continue;
                el.click(); return t;
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          }; return walk(document);
        }"""
    )
    if hit:
        page.wait_for_timeout(4500)
        return True
    return False


def show_more_until(page, needle: str, scrolls: int = 24) -> bool:
    for _ in range(scrolls):
        t = body_text(page)
        if re.search(needle, t, re.I):
            return True
        deep_click(page, r"^Show more$", y_min=100, max_len=20)
        page.mouse.wheel(0, 550)
        page.wait_for_timeout(160)
    return bool(re.search(needle, body_text(page), re.I))


def ensure_kids_no(page) -> dict:
    info = {}
    show_more_until(page, r"Audience|Made for Kids|AI use")
    # Prefer role radio Not made for kids
    try:
        radio = page.get_by_role("radio", name=re.compile(r"No,? it.?s not.?Made for Kids|Not made for kids", re.I))
        if radio.count():
            radio.first.click(force=True, timeout=4000)
            info["via"] = "role_radio"
    except Exception as e:
        info["role_err"] = str(e)[:120]
    if not info.get("via"):
        info["via"] = deep_click(page, r"No, it's not.?Made for Kids", y_min=120, max_len=80)
    page.wait_for_timeout(600)
    return info


def ensure_ai_yes(page) -> dict:
    info = {}
    show_more_until(page, r"AI use|Was AI used|Altered content")
    hit = page.evaluate(
        """() => {
          let aiY=null;
          const find=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/^AI use$/i.test(t)||/Was AI used/i.test(t)||/^Altered content$/i.test(t)) {
                const rect=el.getBoundingClientRect();
                if (rect.y>80) aiY=rect.y;
              }
              if (el.shadowRoot) find(el.shadowRoot,d+1);
            }
          }; find(document);
          const walk=(r,d=0)=>{
            if(!r||d>55)return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              const rect=el.getBoundingClientRect();
              if (/Yes, AI was used/i.test(t) && t.length<60) { el.click(); return 'exact'; }
              if (aiY!=null && /^Yes$/.test(t) && rect.y>aiY && rect.y<aiY+480 && rect.width>10) {
                el.click(); return 'yes_near_ai';
              }
              if (el.shadowRoot) { const x=walk(el.shadowRoot,d+1); if(x) return x; }
            }
            return false;
          };
          return {hit:walk(document),aiY};
        }"""
    )
    info["hit"] = hit
    page.wait_for_timeout(500)
    return info


def upload_main_thumb(page) -> dict:
    info = {"file": THUMBS[0].name}
    for _ in range(6):
        page.mouse.wheel(0, 280)
        page.wait_for_timeout(80)
    # Prefer file chooser on Upload / thumbnail area
    adds = page.evaluate(
        """() => {
          const adds=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/^Upload(?: thumbnail)?$/i.test(t) || /Upload file/i.test(t)) {
                const rect=el.getBoundingClientRect();
                if (rect.y>120 && rect.width>40 && rect.height>20)
                  adds.push({x:rect.x+rect.width/2,y:rect.y+rect.height/2,t,y0:rect.y});
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          }; walk(document);
          adds.sort((a,b)=>a.y0-b.y0); return adds;
        }"""
    )
    if adds:
        try:
            with page.expect_file_chooser(timeout=12000) as fc:
                page.mouse.click(adds[0]["x"], adds[0]["y"])
            fc.value.set_files(str(THUMBS[0]))
            info["via"] = "chooser"
            info["ok"] = True
            page.wait_for_timeout(2800)
            return info
        except Exception as e:
            info["chooser_err"] = str(e)[:160]
    loc = page.locator('input[type="file"]')
    for i in range(loc.count()):
        acc = (loc.nth(i).get_attribute("accept") or "").lower()
        if "image" in acc or "jpg" in acc or "png" in acc or "jpeg" in acc:
            try:
                loc.nth(i).set_input_files(str(THUMBS[0]))
                info["via"] = f"input[{i}]"
                info["ok"] = True
                page.wait_for_timeout(2800)
                return info
            except Exception:
                continue
    info["ok"] = False
    return info


def do_ab(page) -> dict:
    info: dict = {
        "pairs": [{"title": t, "thumb": th.name} for t, th in zip(TITLES, THUMBS)]
    }
    deep_click(page, r"^A/B Testing$", y_min=100, max_len=20)
    page.wait_for_timeout(2800)
    try:
        page.get_by_text("Title and thumbnail", exact=True).first.click(timeout=5000, force=True)
        info["mode"] = "role"
    except Exception:
        info["mode"] = deep_click(page, r"^Title and thumbnail$", y_min=80, max_len=40)
    page.wait_for_timeout(2200)
    shot(page, "v21_10_ab_open.png")

    uploads = []
    for j, thumb in enumerate(THUMBS):
        done = False
        # Re-find Add thumbnail each time; click the topmost remaining empty slot
        for attempt in range(3):
            adds = page.evaluate(
                """() => {
                  const adds=[];
                  const walk=(r,d=0)=>{
                    if(!r||d>55)return;
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                      if ((el.innerText||'').trim()==='Add thumbnail') {
                        const rect=el.getBoundingClientRect();
                        if (rect.y>100 && rect.width>80 && rect.height>30)
                          adds.push({x:rect.x+rect.width/2,y:rect.y+rect.height/2,y0:rect.y});
                      }
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                      if (el.shadowRoot) walk(el.shadowRoot,d+1);
                    }
                  }; walk(document);
                  adds.sort((a,b)=>a.y0-b.y0);
                  const uniq=[];
                  for (const a of adds) {
                    if (!uniq.length || Math.abs(uniq[uniq.length-1].y0-a.y0)>40) uniq.push(a);
                  }
                  return uniq;
                }"""
            )
            if not adds:
                page.wait_for_timeout(800)
                continue
            target = adds[0]  # always topmost remaining Add thumbnail
            try:
                with page.expect_file_chooser(timeout=12000) as fc:
                    page.mouse.click(target["x"], target["y"])
                fc.value.set_files(str(thumb))
                uploads.append({"slot": j + 1, "via": "chooser", "file": thumb.name, "attempt": attempt})
                done = True
                page.wait_for_timeout(3000)
                break
            except Exception as e:
                uploads.append({"slot": j + 1, "attempt": attempt, "err": str(e)[:100]})
                page.keyboard.press("Escape")
                page.wait_for_timeout(400)
        if not done:
            # Fallback: nth image file input inside dialog
            loc = page.locator('input[type="file"]')
            idxs = []
            for i in range(loc.count()):
                acc = (loc.nth(i).get_attribute("accept") or "").lower()
                if "image" in acc or "jpg" in acc or "png" in acc or "jpeg" in acc:
                    idxs.append(i)
            if j < len(idxs):
                try:
                    loc.nth(idxs[j]).set_input_files(str(thumb))
                    uploads.append({"slot": j + 1, "via": "input", "file": thumb.name})
                    done = True
                    page.wait_for_timeout(2800)
                except Exception as e:
                    uploads.append({"slot": j + 1, "err": f"input:{e}"[:120]})
            else:
                uploads.append({"slot": j + 1, "err": "fail"})
        shot(page, f"v21_11_slot{j+1}.png")
        log(f"  ab slot {uploads[-1]}")

    info["uploads"] = uploads

    for i, label in enumerate(["Add title 1", "Add title 2", "Add title 3"]):
        box = page.evaluate(
            """(label)=>{
              let best=null;
              const walk=(r,d=0)=>{
                if(!r||d>55)return;
                for (const node of (r.querySelectorAll?r.querySelectorAll('[contenteditable=true]'):[])) {
                  if ((node.getAttribute('aria-label')||'')===label) {
                    const rect=node.getBoundingClientRect();
                    best={x:rect.x+Math.min(120,rect.width/2),y:rect.y+Math.min(24,rect.height/2)};
                  }
                }
                for (const node of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if (node.shadowRoot) walk(node.shadowRoot,d+1);
                }
              }; walk(document); return best;
            }""",
            label,
        )
        if not box:
            continue
        page.mouse.click(box["x"], box["y"])
        page.keyboard.press("Meta+a")
        page.keyboard.press("Backspace")
        page.keyboard.type(TITLES[i], delay=10)
        page.wait_for_timeout(180)

    info["vals"] = page.evaluate(
        """() => {
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const node of (r.querySelectorAll?r.querySelectorAll('[contenteditable=true]'):[])) {
              const aria=node.getAttribute('aria-label')||'';
              if (/Add title/.test(aria)) out.push({aria,val:(node.textContent||'').trim()});
            }
            for (const node of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (node.shadowRoot) walk(node.shadowRoot,d+1);
            }
          }; walk(document); return out;
        }"""
    )
    shot(page, "v21_12_filled.png")
    body = body_text(page)
    info["ready"] = bool(re.search(r"Title and thumbnail test ready", body, re.I))
    info["ineligible"] = bool(re.search(r"Ineligible", body, re.I))
    set_state = "missing"
    try:
        btn = page.get_by_role("button", name=re.compile(r"^Set test$", re.I))
        if btn.count():
            set_state = "enabled" if btn.first.is_enabled() else "disabled"
            if btn.first.is_enabled():
                btn.first.click(force=True)
                set_state = "clicked"
                page.wait_for_timeout(3000)
    except Exception as e:
        set_state = f"err:{e}"[:80]
    info["set"] = set_state
    shot(page, "v21_13_after_set.png")
    banner = body_text(page)
    info["banner"] = {
        "title_and_thumb": bool(re.search(r"title and thumbnail test has been set up", banner, re.I)),
        "title_only": bool(re.search(r"A title test has been set up", banner, re.I)),
        "save_or_publish": bool(re.search(r"Save or publish to start", banner, re.I)),
        "ineligible": bool(re.search(r"Ineligible", banner, re.I)),
    }
    page.keyboard.press("Escape")
    page.wait_for_timeout(400)
    info["saved"] = save(page)
    shot(page, "v21_14_after_save.png")
    titles_ok = [v.get("val") for v in info.get("vals") or []]
    info["titles_match"] = titles_ok == TITLES
    slots_ok = sum(1 for u in uploads if u.get("file"))
    info["slots_uploaded"] = slots_ok
    info["ok"] = bool(
        info["banner"].get("title_and_thumb")
        or (info["ready"] and set_state == "clicked" and slots_ok >= 3 and info["titles_match"])
    )
    return info


def do_visibility(page) -> dict:
    info = {}
    deep_click(page, r"^Visibility$", y_min=80, max_len=20) or deep_click(
        page, r"^Scheduled$", y_min=80, max_len=20
    )
    page.wait_for_timeout(900)
    deep_click(page, r"15 Oct 2026|Schedule", y_min=100, max_len=40)
    page.wait_for_timeout(1200)
    shot(page, "v21_20_visibility.png")
    # Also copy as FINAL alias
    shutil.copy2(EV / "v21_20_visibility.png", EV / "FINAL_visibility_panel_15oct_1800.png")
    shutil.copy2(EV / "v21_20_visibility.png", ART / "FINAL_visibility_panel_15oct_1800.png")
    try:
        shutil.copy2(EV / "v21_20_visibility.png", ART2 / "FINAL_visibility_panel_15oct_1800.png")
    except Exception:
        pass
    vt = body_text(page)
    info["has_15"] = bool(re.search(r"15\s*(Oct|October)\s*2026", vt, re.I))
    info["has_1800"] = bool(re.search(r"18:00", vt))
    info["has_30"] = bool(re.search(r"30\s*(Sept|Sep|September)\s*2026", vt, re.I))
    info["premiere_off"] = not bool(re.search(r"Premiere\s*on|Set as Premiere", vt, re.I) and re.search(r"checked|selected", vt, re.I))
    info["snip"] = vt[:1200]
    info["ok"] = info["has_15"] and not info["has_30"]
    # If 18:00 missing from text, schedule may still be correct (panel image proof)
    if info["has_15"] and not info["has_1800"]:
        # Try open date/time editors for clearer proof
        deep_click(page, r"18:00|Publish date|Schedule", y_min=100, max_len=40)
        page.wait_for_timeout(800)
        shot(page, "v21_21_visibility_time.png")
        vt2 = body_text(page)
        info["has_1800"] = bool(re.search(r"18:00", vt2))
        info["snip2"] = vt2[:800]
    return info


def do_end_screen(page) -> dict:
    info = {"related": RELATED_002}
    goto_edit(page)
    # Prefer Editor → End screen
    deep_click(page, r"^Editor$", y_min=80, max_len=20)
    page.wait_for_timeout(2500)
    dismiss(page)
    deep_click(page, r"^End screen$", y_min=80, max_len=20)
    page.wait_for_timeout(3000)
    for _ in range(3):
        dismiss(page)
        deep_click(page, r"^OK, got it$", y_min=60, max_len=20)
    shot(page, "v21_30_end_open.png")
    t = body_text(page)
    info["panel"] = bool(re.search(r"ADD ELEMENT|Add element|1 video|template|End screen", t, re.I))
    info["kids_block"] = bool(re.search(r"Made for Kids", t, re.I)) and not info["panel"]

    info["template"] = deep_click(page, r"1 video, 1 subscribe", y_min=60, max_len=40)
    page.wait_for_timeout(2200)
    if not info["template"]:
        deep_click(page, r"ADD ELEMENT|Add element", y_min=60, max_len=30)
        page.wait_for_timeout(400)
        deep_click(page, r"^Video$", y_min=60, max_len=10)
        page.wait_for_timeout(400)
        deep_click(page, r"^Subscribe$", y_min=60, max_len=15)
        page.wait_for_timeout(800)
    shot(page, "v21_31_template.png")

    # Bind Specific video 002 — avoid leaving Best for viewer
    deep_click(page, r"Best for viewer|Most recent upload|Video:", y_min=60, max_len=60)
    page.wait_for_timeout(500)
    deep_click(page, r"Specific video|Choose a video|Select a video", y_min=60, max_len=40)
    page.wait_for_timeout(900)

    filled = page.evaluate(
        """(q)=>{
          const walk=(r,d=0)=>{
            if(!r||d>55)return false;
            for (const inp of (r.querySelectorAll?r.querySelectorAll('input,textarea'):[])) {
              const aria=((inp.getAttribute('aria-label')||'')+(inp.placeholder||'')).toLowerCase();
              const rect=inp.getBoundingClientRect();
              if(rect.width<40||rect.y<50) continue;
              if(/search|video|url|paste/.test(aria)||inp.type==='search'||inp.type==='text'){
                inp.focus();
                const s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
                s.call(inp,q);
                inp.dispatchEvent(new Event('input',{bubbles:true}));
                return true;
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if(el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          };
          return walk(document);
        }""",
        RELATED_002,
    )
    info["search_fill"] = filled
    if not filled:
        page.keyboard.type(RELATED_002, delay=15)
    page.keyboard.press("Enter")
    page.wait_for_timeout(2400)
    deep_click(page, RELATED_TITLE, y_min=80, max_len=90) or deep_click(
        page, r"Periodic Table", y_min=80, max_len=50
    )
    page.wait_for_timeout(1200)
    shot(page, "v21_32_bound.png")
    info["save"] = save(page)
    # Also try SAVE uppercase in editor chrome
    if not info["save"]:
        info["save"] = bool(deep_click(page, r"^SAVE$", y_min=0, max_len=10))
        page.wait_for_timeout(4000)
    shot(page, "v21_33_saved.png")

    # Reload verify
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        wait_until="domcontentloaded",
        timeout=90000,
    )
    page.wait_for_timeout(4000)
    dismiss(page)
    deep_click(page, r"^Editor$", y_min=80, max_len=20)
    page.wait_for_timeout(2000)
    deep_click(page, r"^End screen$", y_min=80, max_len=20)
    page.wait_for_timeout(3000)
    for _ in range(2):
        dismiss(page)
        deep_click(page, r"^OK, got it$", y_min=60, max_len=20)
    shot(page, "v21_34_verify.png")
    after = body_text(page)
    info["has_002"] = bool(re.search(r"Periodic Table|AL_-qlWko_g", after, re.I))
    info["has_subscribe"] = bool(re.search(r"\bSubscribe\b", after, re.I))
    info["best_for_viewer"] = bool(re.search(r"Best for viewer", after, re.I))
    info["most_recent"] = bool(re.search(r"Most recent upload", after, re.I))
    info["error"] = bool(
        re.search(r"problem in processing|couldn't be saved|At least one element must be a video", after, re.I)
    )
    info["ok"] = bool(
        not info["error"]
        and info["has_002"]
        and info["has_subscribe"]
        and not info["best_for_viewer"]
    )
    info["after"] = after[:1000]
    return info


def main() -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    (EV / "phone_uat_v21.log").write_text("")
    urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=3)
    result = {
        "at": datetime.now().isoformat(timespec="seconds"),
        "videoId": VIDEO_ID,
        "channel": "@HistoryOfScienceYT",
        "note": "v21 finish pass after Ben phone UAT 18:51",
    }

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}", timeout=30000)
        page = browser.contexts[0].pages[0] if browser.contexts[0].pages else browser.contexts[0].new_page()
        page.set_default_timeout(45000)
        try:
            page.bring_to_front()
        except Exception:
            pass

        log("v21 details + main thumb A v04")
        goto_edit(page)
        shot(page, "v21_01_details.png")
        t0 = body_text(page)
        result["title_ok"] = "What's Really Inside an Atom?" in t0
        result["ineligible_on_load"] = "Ineligible" in t0
        result["thumb"] = upload_main_thumb(page)
        save(page)
        shot(page, "v21_02_thumb.png")

        log("v21 Kids NO + AI YES")
        goto_edit(page)
        result["kids"] = ensure_kids_no(page)
        result["ai"] = ensure_ai_yes(page)
        save(page)
        goto_edit(page)
        show_more_until(page, r"AI use|Audience|Made for Kids")
        page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>55)return false;
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  const t=(el.innerText||'').trim();
                  if (/^AI use$/i.test(t)||/^Audience$/i.test(t)) {
                    el.scrollIntoView({block:'center'}); return t;
                  }
                  if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                }
                return false;
              }; return walk(document);
            }"""
        )
        page.wait_for_timeout(400)
        shot(page, "v21_03_ai_kids.png")
        tb = body_text(page)
        result["kids_no"] = bool(re.search(r"set to not 'Made for Kids'|No, it's not.?Made for Kids", tb, re.I))
        result["kids_yes_bad"] = bool(re.search(r"set to 'Made for Kids'", tb, re.I))
        result["ai_yes"] = bool(re.search(r"Yes, AI was used|AI use[\s\S]{0,600}Yes", tb, re.I))
        dump("V21_AI_KIDS.json", {
            "kids_no": result["kids_no"],
            "kids_yes_bad": result["kids_yes_bad"],
            "ai_yes": result["ai_yes"],
            "kids": result["kids"],
            "ai": result["ai"],
        })

        log("v21 A/B Title+thumbnail ×3")
        goto_edit(page)
        result["ab"] = do_ab(page)
        dump("V21_AB.json", result["ab"])

        log("v21 Visibility 15 Oct 18:00")
        goto_edit(page)
        result["schedule"] = do_visibility(page)
        dump("V21_SCHEDULE.json", result["schedule"])

        log("v21 Content list")
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
            wait_until="domcontentloaded",
            timeout=90000,
        )
        page.wait_for_timeout(4500)
        dismiss(page)
        shot(page, "v21_22_content.png")
        ct = body_text(page)
        result["content_15"] = bool(re.search(r"15\s*(Oct|October)\s*2026", ct, re.I))
        result["content_30"] = bool(re.search(r"30\s*(Sept|Sep|September)\s*2026", ct, re.I))
        result["content_ab"] = bool(
            re.search(r"What's Really Inside an Atom\?[\s\S]{0,400}A/B test", ct, re.I)
        )

        log("v21 end screen Specific 002 + Subscribe")
        result["end"] = do_end_screen(page)
        dump("V21_END.json", result["end"])

        result["pin"] = {
            "ok": False,
            "reason": "deferred_while_private_scheduled",
            "note": "Pin on launch 15 Oct 2026",
        }

    dump("PHONE_UAT_V21_RESULT.json", result)
    log(
        "DONE "
        + json.dumps(
            {
                k: result.get(k)
                for k in (
                    "kids_no",
                    "ai_yes",
                    "schedule",
                    "content_15",
                    "content_30",
                    "content_ab",
                    "ab",
                    "end",
                    "thumb",
                )
            },
            default=str,
        )[:1800]
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
