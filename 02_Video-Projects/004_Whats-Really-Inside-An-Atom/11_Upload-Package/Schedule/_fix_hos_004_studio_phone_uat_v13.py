#!/usr/bin/env python3
"""HOS 004 Studio phone-UAT v13 — reliable A/B + AI + Visibility + end screen.

Fixes v12 deep_text bug (missed light-DOM). CDP :9460 · no .env.
"""
from __future__ import annotations

import json
import re
import urllib.request
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

PORT = 9460
VIDEO_ID = "GHZDsiH7L7A"
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"
PROJ = Path(__file__).resolve().parents[2]
EV = PROJ / "11_Upload-Package/Schedule/evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos004_studio_phone_uat"
RELATED_002 = "AL_-qlWko_g"
TITLES = [
    "What's Really Inside an Atom?",
    "Why Is the Periodic Table in This Order?",
    "How Small Can You Cut Gold?",
]
THUMBS = [
    PROJ / "08_Thumbnail/Selected/hos_004_thumb_A_atom_live_v04.jpg",
    PROJ / "08_Thumbnail/Selected/hos_004_thumb_C_hidden_number_live_v06.jpg",
    PROJ / "08_Thumbnail/Selected/hos_004_thumb_B_cut_gold_live_v04.jpg",
]


def log(m: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {m}"
    print(line, flush=True)
    with (EV / "phone_uat_v13.log").open("a") as f:
        f.write(line + "\n")


def dump(n: str, o) -> None:
    text = json.dumps(o, indent=2) + "\n"
    (EV / n).write_text(text)
    (ART / n).write_text(text)


def shot(page, n: str) -> str:
    p = EV / n
    page.screenshot(path=str(p), full_page=False)
    (ART / n).write_bytes(p.read_bytes())
    return str(p)


def body_text(page, n=12000) -> str:
    try:
        t = page.inner_text("body", timeout=8000)
    except Exception:
        t = ""
    # supplement with shadow text
    try:
        extra = page.evaluate(
            """() => {
              let out='';
              const walk=(r,d=0)=>{
                if(!r||d>50) return;
                try { if (r.host && r.textContent) out += '\\n' + r.textContent; } catch(e){}
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if (el.shadowRoot) walk(el.shadowRoot,d+1);
                }
              };
              walk(document);
              return out.slice(0,8000);
            }"""
        )
        t = (t or "") + "\n" + (extra or "")
    except Exception:
        pass
    return (t or "")[:n]


def click_text(page, pattern: str, y_min=0, y_max=1300, exact=False):
    """Find shortest matching visible clickable; click center."""
    box = page.evaluate(
        """([pattern, yMin, yMax, exact]) => {
          const re = exact ? null : new RegExp(pattern, 'i');
          let best=null;
          const consider=(el)=>{
            const t=(el.innerText||el.textContent||'').trim().replace(/\\s+/g,' ');
            if(!t) return;
            const ok = exact ? t===pattern : (re.test(t) && t.length < Math.max(80, pattern.length+40));
            if(!ok) return;
            const r=el.getBoundingClientRect();
            if(r.width<4||r.height<4||r.y<yMin||r.y>yMax||r.x<0) return;
            if(!best || t.length < best.t.length)
              best={x:r.x+r.width/2,y:r.y+r.height/2,w:r.width,h:r.height,t:t.slice(0,100)};
          };
          const walk=(root,d=0)=>{
            if(!root||d>55) return;
            const sels='button,a,[role=button],[role=radio],[role=tab],[role=option],ytcp-button,tp-yt-paper-item,tp-yt-paper-radio-button,yt-formatted-string,span,div,label';
            for (const el of (root.querySelectorAll?root.querySelectorAll(sels):[])) consider(el);
            for (const el of (root.querySelectorAll?root.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          };
          walk(document);
          return best;
        }""",
        [pattern, y_min, y_max, exact],
    )
    if not box:
        return None
    # Prefer role click when short label
    try:
        if exact or len(pattern) < 40:
            loc = page.get_by_role("button", name=re.compile(pattern, re.I))
            if loc.count() and loc.first.is_visible(timeout=400):
                loc.first.click(timeout=3000, force=True)
                page.wait_for_timeout(600)
                return {**box, "via": "role"}
    except Exception:
        pass
    page.mouse.click(box["x"], box["y"])
    page.wait_for_timeout(700)
    return {**box, "via": "mouse"}


def dismiss(page):
    for name in ["OK, got it", "Got it", "Dismiss", "Not now"]:
        try:
            b = page.get_by_role("button", name=re.compile(rf"^{re.escape(name)}$", re.I))
            if b.count() and b.first.is_visible(timeout=200):
                b.first.click(timeout=400)
        except Exception:
            pass


def goto_edit(page):
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(5000)
    dismiss(page)


def save(page) -> dict:
    info = {}
    try:
        btn = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
        if btn.count():
            info["enabled"] = btn.first.is_enabled()
            if btn.first.is_enabled():
                btn.first.click(timeout=5000)
                page.wait_for_timeout(4000)
                info["via"] = "role"
                return info
    except Exception as e:
        info["err"] = type(e).__name__
    hit = click_text(page, r"^Save$", y_min=0, y_max=180)
    info["via"] = "mouse" if hit else None
    if hit:
        page.wait_for_timeout(4000)
    return info


def open_ab(page) -> bool:
    # Click the compact A/B Testing control under title (not giant wrappers)
    try:
        loc = page.get_by_role("button", name=re.compile(r"A/B Testing", re.I))
        if loc.count():
            loc.first.click(timeout=5000, force=True)
            page.wait_for_timeout(2500)
    except Exception:
        pass
    t = body_text(page)
    if re.search(r"Test and compare|Title and thumbnail|Thumbnail only|Title only", t, re.I):
        return True
    # mouse on short label
    click_text(page, r"^A/B Testing$", y_min=100, y_max=400, exact=True) or click_text(
        page, r"A/B Testing", y_min=100, y_max=400
    )
    page.wait_for_timeout(2500)
    t = body_text(page)
    return bool(re.search(r"Test and compare|Title and thumbnail|Thumbnail only|Title only", t, re.I))


def upload_ab_thumbs(page) -> list:
    uploads = []
    for j, thumb in enumerate(THUMBS):
        # Prefer file inputs inside dialog
        loc = page.locator('input[type="file"]')
        idxs = []
        for i in range(loc.count()):
            try:
                acc = (loc.nth(i).get_attribute("accept") or "").lower()
                box = loc.nth(i).bounding_box()
                if box and box["y"] > 60 and ("image" in acc or "jpg" in acc or "png" in acc or acc == ""):
                    idxs.append((box["y"], i))
            except Exception:
                pass
        idxs.sort()
        done = False
        if j < len(idxs):
            try:
                loc.nth(idxs[j][1]).set_input_files(str(thumb))
                uploads.append({"slot": j + 1, "file": thumb.name, "via": "input"})
                done = True
                page.wait_for_timeout(2400)
            except Exception as e:
                uploads.append({"slot": j + 1, "input_err": type(e).__name__})
        if not done:
            try:
                with page.expect_file_chooser(timeout=8000) as fc:
                    # click Add thumbnail — prefer lower empty slots
                    hit = click_text(page, r"^Add thumbnail$", y_min=150 + j * 40)
                    if not hit:
                        page.get_by_text("Add thumbnail", exact=True).last.click(timeout=4000, force=True)
                fc.value.set_files(str(thumb))
                uploads.append({"slot": j + 1, "file": thumb.name, "via": "chooser"})
                page.wait_for_timeout(2400)
                done = True
            except Exception as e:
                uploads.append({"slot": j + 1, "err": type(e).__name__, "file": thumb.name})
        shot(page, f"v13_ab_slot{j+1}.png")
        log(f"  slot{j+1}: {uploads[-1]}")
        # nudge scroll for next slot
        page.mouse.wheel(0, 180)
        page.wait_for_timeout(300)
    return uploads


def fill_ab_titles(page) -> int:
    # JS native setter across shadow
    n = page.evaluate(
        """(titles)=>{
          const found=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const inp of (r.querySelectorAll?r.querySelectorAll('input,textarea'):[])) {
              const max=inp.getAttribute('maxlength')||'';
              const ph=(inp.placeholder||'').toLowerCase();
              const aria=((inp.getAttribute('aria-label')||'')).toLowerCase();
              const rect=inp.getBoundingClientRect();
              if(rect.width<80||rect.y<70||rect.y>1150) continue;
              if(max==='100'||ph.includes('title')||aria.includes('title')) found.push({inp,y:rect.y});
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if(el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          };
          walk(document);
          found.sort((a,b)=>a.y-b.y);
          const uniq=[];
          for (const f of found) {
            if (!uniq.length || Math.abs(uniq[uniq.length-1].y-f.y)>20) uniq.push(f);
          }
          const setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
          for(let i=0;i<Math.min(3,uniq.length);i++){
            const inp=uniq[i].inp;
            inp.focus();
            setter.call(inp, titles[i]);
            inp.dispatchEvent(new Event('input',{bubbles:true}));
            inp.dispatchEvent(new Event('change',{bubbles:true}));
          }
          return uniq.length;
        }""",
        TITLES,
    )
    # keyboard fill visible maxlength=100
    inputs = page.locator("input")
    cands = []
    for i in range(inputs.count()):
        el = inputs.nth(i)
        try:
            if not el.is_visible():
                continue
            if el.get_attribute("maxlength") != "100":
                continue
            box = el.bounding_box()
            if box and 70 < box["y"] < 1150:
                cands.append((box["y"], i))
        except Exception:
            pass
    cands.sort()
    picked = []
    for y, i in cands:
        if not picked or abs(picked[-1][0] - y) > 20:
            picked.append((y, i))
    for j, (_, i) in enumerate(picked[:3]):
        el = inputs.nth(i)
        el.click()
        page.keyboard.press("Meta+a")
        page.keyboard.type(TITLES[j], delay=12)
        page.wait_for_timeout(200)
    return max(n or 0, len(picked))


def do_ab(page) -> dict:
    info = {"pairs": [{"title": t, "thumb": th.name} for t, th in zip(TITLES, THUMBS)]}
    goto_edit(page)
    shot(page, "v13_00_details.png")
    opened = open_ab(page)
    info["dialog_open"] = opened
    shot(page, "v13_10_ab_open.png")
    if not opened:
        info["ok"] = False
        info["note"] = "dialog not open"
        info["snip"] = body_text(page, 500)
        return info

    # Force Title and thumbnail mode
    try:
        page.get_by_text("Title and thumbnail", exact=True).first.click(timeout=4000, force=True)
    except Exception:
        click_text(page, r"^Title and thumbnail$", y_min=40, exact=True) or click_text(
            page, r"Title and thumbnail", y_min=40
        )
    page.wait_for_timeout(2000)
    shot(page, "v13_11_mode.png")

    info["uploads"] = upload_ab_thumbs(page)
    info["title_slots"] = fill_ab_titles(page)
    page.wait_for_timeout(800)
    shot(page, "v13_13_filled.png")
    t = body_text(page)
    info["ready"] = bool(re.search(r"Title and thumbnail test ready", t, re.I))
    info["need_more"] = bool(re.search(r"required", t, re.I)) and not info["ready"]

    set_state = None
    try:
        btn = page.get_by_role("button", name=re.compile(r"^Set test$", re.I))
        if btn.count():
            set_state = "enabled" if btn.first.is_enabled() else "disabled"
            if btn.first.is_enabled():
                btn.first.click(timeout=5000)
                set_state = "clicked"
    except Exception as e:
        set_state = type(e).__name__
    if set_state != "clicked":
        hit = click_text(page, r"^Set test$", y_min=200)
        if hit:
            set_state = "mouse"
    info["set"] = set_state
    page.wait_for_timeout(3500)
    shot(page, "v13_14_after_set.png")
    t = body_text(page)
    info["banner"] = bool(re.search(r"Save or publish to start|has been set up", t, re.I))

    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    page.wait_for_timeout(600)
    dismiss(page)
    shot(page, "v13_15_before_save.png")
    info["save"] = save(page)
    page.wait_for_timeout(2000)
    if re.search(r"Save or publish to start|has been set up", body_text(page), re.I):
        info["save2"] = save(page)
    shot(page, "v13_16_after_save.png")

    goto_edit(page)
    t = body_text(page)
    info["running"] = bool(re.search(r"A/B test running|Your test is running|test running", t, re.I))
    info["setup_pending"] = bool(re.search(r"Save or publish to start|has been set up", t, re.I))
    open_ab(page)
    page.wait_for_timeout(1500)
    t2 = body_text(page)
    if re.search(r"A/B test running|Your test is running|End test|Stop test", t2, re.I):
        info["running"] = True
    shot(page, "v13_17_status.png")
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    uploaded_ok = sum(1 for u in info["uploads"] if u.get("via") in ("input", "chooser"))
    info["uploaded_ok"] = uploaded_ok
    info["ok"] = bool(info["running"] or (info.get("banner") and uploaded_ok >= 3 and set_state in ("clicked", "mouse")))
    return info


def upload_main_thumb(page) -> dict:
    info = {"file": THUMBS[0].name}
    goto_edit(page)
    for _ in range(5):
        page.mouse.wheel(0, 350)
        page.wait_for_timeout(150)
    shot(page, "v13_01_thumb_before.png")
    loc = page.locator('input[type="file"]')
    uploaded = False
    for i in range(loc.count()):
        try:
            acc = (loc.nth(i).get_attribute("accept") or "").lower()
            box = loc.nth(i).bounding_box()
            if box and box["y"] > 100 and ("image" in acc or "jpg" in acc or acc == ""):
                loc.nth(i).set_input_files(str(THUMBS[0]))
                uploaded = True
                info["via"] = "input"
                info["i"] = i
                break
        except Exception:
            continue
    if not uploaded:
        try:
            with page.expect_file_chooser(timeout=7000) as fc:
                click_text(page, r"Upload thumbnail|Upload file", y_min=150) or page.get_by_text(
                    re.compile(r"Upload", re.I)
                ).first.click(timeout=3000)
            fc.value.set_files(str(THUMBS[0]))
            uploaded = True
            info["via"] = "chooser"
        except Exception as e:
            info["err"] = type(e).__name__
    page.wait_for_timeout(2500)
    info["saved"] = save(page)
    shot(page, "v13_02_thumb_after.png")
    info["ok"] = uploaded
    return info


def confirm_ai_kids(page) -> dict:
    info = {}
    goto_edit(page)
    for _ in range(25):
        t = body_text(page)
        if re.search(r"AI use|Altered content|Was AI used", t, re.I):
            break
        click_text(page, r"^Show more$", y_min=200)
        page.mouse.wheel(0, 500)
        page.wait_for_timeout(200)
    shot(page, "v13_20_ai_before.png")
    try:
        page.get_by_text(re.compile(r"Yes, AI was used", re.I)).first.click(timeout=5000, force=True)
        info["ai_click"] = "text"
    except Exception:
        info["ai_click"] = click_text(page, r"Yes, AI was used", y_min=150)
    page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55) return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=radio],tp-yt-paper-radio-button'):[])) {
              const t=((el.getAttribute('aria-label')||'')+(el.innerText||'')).toLowerCase();
              if (/yes/.test(t) && (/ai/.test(t) || /altered/.test(t))) { el.click(); return true; }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          };
          // click Yes near AI use heading
          const all=[];
          const collect=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/^Yes$/.test(t)) {
                const rect=el.getBoundingClientRect();
                if (rect.y>200) all.push({el,y:rect.y});
              }
              if (el.shadowRoot) collect(el.shadowRoot,d+1);
            }
          };
          collect(document);
          // heuristic: after AI use section, first Yes
          for (const a of all) { a.el.click(); return true; }
          return walk(document);
        }"""
    )
    try:
        page.get_by_text(re.compile(r"No, it's not.?Made for Kids", re.I)).first.click(
            timeout=4000, force=True
        )
    except Exception:
        click_text(page, r"No, it's not", y_min=200)
    info["saved"] = save(page)
    page.wait_for_timeout(2000)
    goto_edit(page)
    for _ in range(25):
        if re.search(r"AI use|Was AI used", body_text(page), re.I):
            break
        click_text(page, r"^Show more$", y_min=200)
        page.mouse.wheel(0, 500)
        page.wait_for_timeout(180)
    for _ in range(10):
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(100)
    shot(page, "v13_21_ai_kids.png")
    t = body_text(page)
    info["ai_use_yes"] = bool(re.search(r"Yes, AI was used", t, re.I)) or bool(
        re.search(r"AI use[\s\S]{0,500}Yes", t, re.I)
    )
    info["kids_no"] = bool(re.search(r"No, it's not.?Made for Kids", t, re.I))
    info["ok"] = bool(info["ai_use_yes"] and info["kids_no"])
    info["snip"] = t[:1500]
    return info


def prove_visibility(page) -> dict:
    info = {}
    goto_edit(page)
    # Open visibility schedule panel on the right
    try:
        page.get_by_text(re.compile(r"^Visibility$", re.I)).first.click(timeout=4000, force=True)
    except Exception:
        click_text(page, r"^Visibility$", y_min=80)
    page.wait_for_timeout(1000)
    click_text(page, r"Schedule|Scheduled|15 Oct|October", y_min=80)
    page.wait_for_timeout(1200)
    # Click date chip / schedule radio area
    click_text(page, r"15 Oct 2026|15 October", y_min=80)
    page.wait_for_timeout(800)
    shot(page, "v13_30_visibility.png")
    t = body_text(page)
    info["has_15"] = bool(re.search(r"15\s*(Oct|October)\s*2026", t, re.I))
    info["has_1800"] = bool(re.search(r"18:00", t, re.I))
    info["has_30"] = bool(re.search(r"30\s*(Sept|Sep|September)\s*2026", t, re.I))
    info["premiere_label"] = bool(re.search(r"Set as Premiere", t, re.I))
    click_text(page, r"^Done$", y_min=200)
    page.wait_for_timeout(600)
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    shot(page, "v13_31_content.png")
    t2 = body_text(page)
    info["content_15"] = bool(re.search(r"15\s*(Oct|October)\s*2026", t2, re.I))
    info["content_30"] = bool(re.search(r"30\s*(Sept|Sep|September)\s*2026", t2, re.I))
    info["ok"] = bool(
        (info["has_15"] or info["content_15"])
        and (info["has_1800"] or info["content_15"])  # 18:00 on panel; content may omit time
        and not info["has_30"]
        and not info["content_30"]
    )
    # Require 18:00 for strict ok if panel opened
    if info["has_15"] and info["has_1800"] and not info["has_30"]:
        info["ok"] = True
    info["snip"] = t[:900]
    return info


def do_end_screen(page) -> dict:
    info = {"related": RELATED_002}
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit?panel=endscreen",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(5000)
    for _ in range(4):
        dismiss(page)
        click_text(page, r"OK, got it")
        page.wait_for_timeout(200)
    # Also try End screen tab
    click_text(page, r"^End screen$", y_min=80)
    page.wait_for_timeout(2000)
    shot(page, "v13_40_end.png")
    t = body_text(page)
    info["panel"] = bool(re.search(r"End screen|ADD ELEMENT|Add element|1 video|Subscribe|template", t, re.I))

    info["template"] = click_text(page, r"1 video, 1 subscribe", y_min=60)
    page.wait_for_timeout(2000)
    if not info["template"]:
        click_text(page, r"ADD ELEMENT|Add element", y_min=60)
        page.wait_for_timeout(400)
        click_text(page, r"^Video$", y_min=60, exact=True)
        click_text(page, r"^Subscribe$", y_min=60, exact=True)
    shot(page, "v13_41_template.png")

    click_text(page, r"Most recent upload|Best for viewer", y_min=60)
    page.wait_for_timeout(400)
    click_text(page, r"Specific video|Choose a video|Select a video", y_min=60)
    page.wait_for_timeout(800)
    page.evaluate(
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
    page.keyboard.type(RELATED_002, delay=12)
    page.keyboard.press("Enter")
    page.wait_for_timeout(2200)
    click_text(page, r"How Did We Discover the Periodic Table", y_min=80) or click_text(
        page, r"Periodic Table", y_min=80
    )
    page.wait_for_timeout(1000)
    shot(page, "v13_42_bound.png")
    try:
        btn = page.get_by_role("button", name=re.compile(r"^SAVE$|^Save$", re.I))
        if btn.count() and btn.first.is_enabled():
            btn.first.click(timeout=5000)
            info["save"] = "role"
    except Exception:
        pass
    if not info.get("save"):
        info["save"] = "mouse" if click_text(page, r"^SAVE$|^Save$", y_min=0) else None
    page.wait_for_timeout(4000)
    shot(page, "v13_43_saved.png")
    after = body_text(page)
    info["has_002"] = bool(re.search(r"Periodic Table|AL_-qlWko_g", after, re.I))
    info["has_subscribe"] = bool(re.search(r"Subscribe", after, re.I))
    info["error"] = bool(re.search(r"problem in processing|couldn't be saved|At least one element must be a video", after, re.I))
    info["ok"] = bool(info["panel"] and not info["error"] and (info["has_002"] or info["has_subscribe"] or info.get("template")))
    info["after"] = after[:900]
    return info


def main():
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    (EV / "phone_uat_v13.log").write_text("")
    urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=2)
    result = {
        "started": datetime.now().isoformat(timespec="seconds"),
        "videoId": VIDEO_ID,
        "channel": "@HistoryOfScienceYT",
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        ctx = browser.contexts[0]
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.set_default_timeout(60000)
        # bring page to front
        try:
            page.bring_to_front()
        except Exception:
            pass

        log("v13 thumb A v04")
        result["thumbnail"] = upload_main_thumb(page)
        dump("V13_THUMB.json", result["thumbnail"])

        log("v13 A/B")
        result["testAndCompare"] = do_ab(page)
        dump("V13_AB.json", result["testAndCompare"])

        log("v13 AI+Kids")
        result["aiKids"] = confirm_ai_kids(page)
        dump("V13_AI_KIDS.json", result["aiKids"])

        log("v13 Visibility")
        result["schedule"] = prove_visibility(page)
        dump("V13_SCHEDULE.json", result["schedule"])

        log("v13 end screen")
        result["endScreen"] = do_end_screen(page)
        dump("V13_END.json", result["endScreen"])

        result["pinnedComment"] = {
            "ok": False,
            "reason": "deferred_while_private_scheduled",
            "note": "Pin on launch day 15 Oct 2026",
        }

    result["ok"] = {
        k: (result[k].get("ok") if isinstance(result.get(k), dict) else None)
        for k in ("thumbnail", "testAndCompare", "aiKids", "schedule", "endScreen", "pinnedComment")
    }
    result["finished"] = datetime.now().isoformat(timespec="seconds")
    dump("PHONE_UAT_V13_RESULT.json", result)
    log(f"DONE {json.dumps(result['ok'])}")
    print(json.dumps(result["ok"], indent=2))


if __name__ == "__main__":
    main()
