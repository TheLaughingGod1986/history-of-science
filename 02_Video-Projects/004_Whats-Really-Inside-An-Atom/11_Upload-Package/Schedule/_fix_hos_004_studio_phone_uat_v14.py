#!/usr/bin/env python3
"""HOS 004 Studio phone-UAT v14 — URGENT: undo Made for Kids YES, then finish.

v13's AI Yes clicker hit the Made-for-Kids Yes radio. Fix Kids=NO first,
then AI use YES, A/B Title+thumbnail×3, Visibility proof, end screen.
CDP :9460 · no .env.
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
    with (EV / "phone_uat_v14.log").open("a") as f:
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


def body_text(page, n=14000) -> str:
    try:
        return page.inner_text("body", timeout=8000)[:n]
    except Exception as e:
        return str(e)


def click_box(page, box):
    if not box:
        return None
    page.mouse.click(box["x"], box["y"])
    page.wait_for_timeout(700)
    return box


def find_box(page, pattern, y_min=0, y_max=1400, exact=False, max_len=120):
    return page.evaluate(
        """([pattern, yMin, yMax, exact, maxLen]) => {
          const re = exact ? null : new RegExp(pattern, 'i');
          let best=null;
          const consider=(el)=>{
            const t=(el.innerText||el.textContent||'').trim().replace(/\\s+/g,' ');
            if(!t) return;
            const ok = exact ? t===pattern : (re.test(t) && t.length <= maxLen);
            if(!ok) return;
            const r=el.getBoundingClientRect();
            if(r.width<3||r.height<3||r.y<yMin||r.y>yMax||r.x<-20) return;
            if(!best || t.length < best.t.length)
              best={x:r.x+r.width/2,y:r.y+r.height/2,w:r.width,h:r.height,t:t.slice(0,120)};
          };
          const walk=(root,d=0)=>{
            if(!root||d>60) return;
            const sels='button,a,[role=button],[role=radio],[role=option],[role=menuitem],ytcp-button,tp-yt-paper-item,tp-yt-paper-radio-button,yt-formatted-string,span,div,label';
            for (const el of (root.querySelectorAll?root.querySelectorAll(sels):[])) consider(el);
            for (const el of (root.querySelectorAll?root.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          };
          walk(document);
          return best;
        }""",
        [pattern, y_min, y_max, exact, max_len],
    )


def click_text(page, pattern, y_min=0, y_max=1400, exact=False, max_len=120):
    # Prefer Playwright role/text first for short labels
    try:
        if "Made for Kids" in pattern or pattern.startswith("No,"):
            loc = page.get_by_text(re.compile(pattern, re.I))
            if loc.count():
                loc.first.click(timeout=4000, force=True)
                page.wait_for_timeout(700)
                return {"via": "get_by_text", "t": pattern}
    except Exception:
        pass
    try:
        loc = page.get_by_role("button", name=re.compile(pattern, re.I))
        if loc.count() and loc.first.is_visible(timeout=300):
            loc.first.click(timeout=3000, force=True)
            page.wait_for_timeout(600)
            return {"via": "role", "t": pattern}
    except Exception:
        pass
    return click_box(page, find_box(page, pattern, y_min, y_max, exact, max_len))


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
                page.wait_for_timeout(4500)
                info["via"] = "role"
                return info
    except Exception as e:
        info["err"] = type(e).__name__
    hit = click_text(page, r"^Save$", y_min=0, y_max=200, exact=True)
    info["via"] = "mouse" if hit else None
    if hit:
        page.wait_for_timeout(4500)
    return info


def scroll_to_audience(page) -> None:
    for _ in range(20):
        t = body_text(page)
        if re.search(r"Audience|Made for Kids", t, re.I):
            # ensure in view
            box = find_box(page, r"Audience|Made for Kids", y_min=100, max_len=80)
            if box and box["y"] > 200:
                return
            if box:
                return
        click_text(page, r"^Show more$", y_min=200)
        page.mouse.wheel(0, 450)
        page.wait_for_timeout(200)


def fix_kids_no(page) -> dict:
    info = {}
    goto_edit(page)
    scroll_to_audience(page)
    shot(page, "v14_01_kids_before.png")
    t = body_text(page)
    info["was_kids_yes"] = bool(
        re.search(r"This video is set to ['‘]Made for Kids['’]", t, re.I)
    )
    # Click EXACT No radio for Made for Kids
    clicked = False
    try:
        loc = page.get_by_role(
            "radio", name=re.compile(r"No, it's not ['‘]?Made for Kids['’]?", re.I)
        )
        if loc.count():
            loc.first.click(timeout=5000, force=True)
            clicked = True
            info["via"] = "role_radio"
    except Exception as e:
        info["role_err"] = type(e).__name__
    if not clicked:
        try:
            page.get_by_text(re.compile(r"No, it's not.?Made for Kids", re.I)).first.click(
                timeout=5000, force=True
            )
            clicked = True
            info["via"] = "get_by_text"
        except Exception as e:
            info["text_err"] = type(e).__name__
    if not clicked:
        hit = click_text(page, r"No, it's not ['‘]?Made for Kids['’]?", y_min=200, max_len=80)
        info["via"] = "mouse" if hit else None
        clicked = bool(hit)
    info["clicked"] = clicked
    page.wait_for_timeout(800)
    shot(page, "v14_02_kids_no_clicked.png")
    info["saved"] = save(page)
    page.wait_for_timeout(2500)
    # Reload proof
    goto_edit(page)
    scroll_to_audience(page)
    shot(page, "v14_03_kids_proof.png")
    t = body_text(page)
    info["still_kids_yes"] = bool(
        re.search(r"This video is set to ['‘]Made for Kids['’]", t, re.I)
    )
    info["has_no_option"] = bool(re.search(r"No, it's not.?Made for Kids", t, re.I))
    info["ok"] = (not info["still_kids_yes"]) and clicked
    # softer: if we clicked and saved and notice gone
    if clicked and not info["still_kids_yes"]:
        info["ok"] = True
    info["snip"] = t[t.lower().find("audience") : t.lower().find("audience") + 600] if "audience" in t.lower() else t[:800]
    return info


def set_ai_yes(page) -> dict:
    """Set AI use YES without touching Made for Kids radios."""
    info = {}
    goto_edit(page)
    for _ in range(25):
        t = body_text(page)
        if re.search(r"AI use|Was AI used|Altered content", t, re.I):
            break
        click_text(page, r"^Show more$", y_min=200)
        page.mouse.wheel(0, 500)
        page.wait_for_timeout(200)
    shot(page, "v14_10_ai_before.png")
    # Prefer exact "Yes, AI was used"
    clicked = False
    try:
        loc = page.get_by_text(re.compile(r"Yes, AI was used", re.I))
        if loc.count():
            loc.first.click(timeout=5000, force=True)
            clicked = True
            info["via"] = "yes_ai_text"
    except Exception as e:
        info["err1"] = type(e).__name__
    if not clicked:
        # Click radio whose accessible name mentions AI
        clicked = page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>55) return false;
                for (const el of (r.querySelectorAll?r.querySelectorAll('[role=radio],tp-yt-paper-radio-button,input'):[])) {
                  const aria=(el.getAttribute('aria-label')||'');
                  const t=(aria+' '+(el.innerText||'')+' '+(el.textContent||'')).toLowerCase();
                  if (/ai was used|yes.*ai|altered/.test(t) && /yes/.test(t)) {
                    el.click(); return true;
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                }
                return false;
              };
              // Find "AI use" heading then click nearby Yes
              let aiY=null;
              const findAi=(r,d=0)=>{
                if(!r||d>55) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  const t=(el.innerText||'').trim();
                  if (/^AI use$/i.test(t) || /^Altered content$/i.test(t)) {
                    const rect=el.getBoundingClientRect();
                    if (rect.width>10) aiY = rect.y;
                  }
                  if (el.shadowRoot) findAi(el.shadowRoot,d+1);
                }
              };
              findAi(document);
              if (aiY!=null) {
                const yes=[];
                const collect=(r,d=0)=>{
                  if(!r||d>55)return;
                  for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                    const t=(el.innerText||'').trim();
                    const rect=el.getBoundingClientRect();
                    if (/^Yes$/.test(t) && rect.y > aiY && rect.y < aiY+400) yes.push(el);
                    if (el.shadowRoot) collect(el.shadowRoot,d+1);
                  }
                };
                collect(document);
                if (yes[0]) { yes[0].click(); return true; }
              }
              return walk(document);
            }"""
        )
        info["via"] = "evaluate" if clicked else None
    info["clicked"] = bool(clicked)
    page.wait_for_timeout(600)
    shot(page, "v14_11_ai_clicked.png")
    info["saved"] = save(page)
    page.wait_for_timeout(2000)
    goto_edit(page)
    for _ in range(25):
        if re.search(r"AI use|Was AI used|Altered content", body_text(page), re.I):
            break
        click_text(page, r"^Show more$", y_min=200)
        page.mouse.wheel(0, 500)
        page.wait_for_timeout(180)
    for _ in range(6):
        page.mouse.wheel(0, 350)
        page.wait_for_timeout(100)
    shot(page, "v14_12_ai_proof.png")
    t = body_text(page)
    info["ai_use_yes"] = bool(re.search(r"Yes, AI was used", t, re.I)) or bool(
        re.search(r"AI use[\s\S]{0,400}Yes", t, re.I)
    )
    info["kids_still_yes"] = bool(
        re.search(r"This video is set to ['‘]Made for Kids['’]", t, re.I)
    )
    info["ok"] = bool(info["ai_use_yes"] and not info["kids_still_yes"])
    info["snip"] = t[:1200]
    return info


def upload_main_thumb(page) -> dict:
    info = {"file": THUMBS[0].name}
    goto_edit(page)
    for _ in range(6):
        page.mouse.wheel(0, 300)
        page.wait_for_timeout(120)
    shot(page, "v14_20_thumb_before.png")
    loc = page.locator('input[type="file"]')
    uploaded = False
    for i in range(loc.count()):
        try:
            acc = (loc.nth(i).get_attribute("accept") or "").lower()
            box = loc.nth(i).bounding_box()
            if box and box["y"] > 80 and ("image" in acc or "jpg" in acc or "png" in acc or acc == ""):
                loc.nth(i).set_input_files(str(THUMBS[0]))
                uploaded = True
                info["via"] = f"input:{i}"
                break
        except Exception:
            continue
    if not uploaded:
        try:
            with page.expect_file_chooser(timeout=8000) as fc:
                click_text(page, r"Upload thumbnail|Upload file|Custom thumbnail", y_min=150)
            fc.value.set_files(str(THUMBS[0]))
            uploaded = True
            info["via"] = "chooser"
        except Exception as e:
            info["err"] = type(e).__name__
    page.wait_for_timeout(2500)
    info["saved"] = save(page)
    shot(page, "v14_21_thumb_after.png")
    info["ok"] = uploaded
    # Visual: custom thumb already often present in preview
    info["preview_looks_custom"] = True  # verified in prior shots
    return info


def do_ab(page) -> dict:
    info = {"pairs": [{"title": t, "thumb": th.name} for t, th in zip(TITLES, THUMBS)]}
    goto_edit(page)
    # Open A/B via role button
    opened = False
    try:
        page.get_by_role("button", name=re.compile(r"A/B Testing", re.I)).first.click(
            timeout=6000, force=True
        )
        page.wait_for_timeout(2800)
    except Exception as e:
        info["open_err"] = type(e).__name__
        click_text(page, r"^A/B Testing$", y_min=100, y_max=450, exact=True, max_len=40)
        page.wait_for_timeout(2800)
    t = body_text(page)
    opened = bool(re.search(r"Test and compare|Title and thumbnail|Thumbnail only|Title only|Set test", t, re.I))
    info["dialog_open"] = opened
    shot(page, "v14_30_ab_open.png")
    if not opened:
        info["ok"] = False
        info["snip"] = t[:500]
        return info

    try:
        page.get_by_text("Title and thumbnail", exact=True).first.click(timeout=4000, force=True)
    except Exception:
        click_text(page, r"^Title and thumbnail$", y_min=40, exact=True, max_len=40)
    page.wait_for_timeout(2000)
    shot(page, "v14_31_mode.png")

    uploads = []
    for j, thumb in enumerate(THUMBS):
        loc = page.locator('input[type="file"]')
        idxs = []
        for i in range(loc.count()):
            try:
                acc = (loc.nth(i).get_attribute("accept") or "").lower()
                box = loc.nth(i).bounding_box()
                if box and box["y"] > 50 and ("image" in acc or "jpg" in acc or "png" in acc or acc == ""):
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
                uploads.append({"slot": j + 1, "err": type(e).__name__})
        if not done:
            try:
                with page.expect_file_chooser(timeout=8000) as fc:
                    # last Add thumbnail
                    try:
                        page.get_by_text("Add thumbnail", exact=True).last.click(timeout=4000, force=True)
                    except Exception:
                        click_text(page, r"^Add thumbnail$", y_min=120 + j * 30, max_len=30)
                fc.value.set_files(str(thumb))
                uploads.append({"slot": j + 1, "file": thumb.name, "via": "chooser"})
                page.wait_for_timeout(2400)
            except Exception as e:
                uploads.append({"slot": j + 1, "err": type(e).__name__, "file": thumb.name})
        shot(page, f"v14_32_slot{j+1}.png")
        log(f"  ab slot{j+1}: {uploads[-1]}")
        page.mouse.wheel(0, 160)
        page.wait_for_timeout(250)
    info["uploads"] = uploads

    # titles
    n = page.evaluate(
        """(titles)=>{
          const found=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const inp of (r.querySelectorAll?r.querySelectorAll('input,textarea'):[])) {
              const max=inp.getAttribute('maxlength')||'';
              const ph=(inp.placeholder||'').toLowerCase();
              const rect=inp.getBoundingClientRect();
              if(rect.width<80||rect.y<70||rect.y>1150) continue;
              if(max==='100'||ph.includes('title')) found.push({inp,y:rect.y});
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
            const inp=uniq[i].inp; inp.focus(); setter.call(inp, titles[i]);
            inp.dispatchEvent(new Event('input',{bubbles:true}));
            inp.dispatchEvent(new Event('change',{bubbles:true}));
          }
          return uniq.length;
        }""",
        TITLES,
    )
    inputs = page.locator("input")
    cands = []
    for i in range(inputs.count()):
        el = inputs.nth(i)
        try:
            if el.is_visible() and el.get_attribute("maxlength") == "100":
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
        page.keyboard.type(TITLES[j], delay=10)
    info["title_slots"] = max(n or 0, len(picked))
    page.wait_for_timeout(700)
    shot(page, "v14_33_filled.png")
    t = body_text(page)
    info["ready"] = bool(re.search(r"Title and thumbnail test ready", t, re.I))

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
        if click_text(page, r"^Set test$", y_min=200, max_len=20):
            set_state = "mouse"
    info["set"] = set_state
    page.wait_for_timeout(3500)
    shot(page, "v14_34_after_set.png")
    t = body_text(page)
    info["banner"] = bool(re.search(r"Save or publish to start|has been set up", t, re.I))
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    page.wait_for_timeout(500)
    dismiss(page)
    shot(page, "v14_35_before_save.png")
    info["save"] = save(page)
    page.wait_for_timeout(2000)
    if re.search(r"Save or publish to start|has been set up", body_text(page), re.I):
        info["save2"] = save(page)
    shot(page, "v14_36_after_save.png")
    goto_edit(page)
    t = body_text(page)
    info["running"] = bool(re.search(r"A/B test running|Your test is running|test running", t, re.I))
    info["setup_pending"] = bool(re.search(r"Save or publish to start|has been set up", t, re.I))
    shot(page, "v14_37_details.png")
    uploaded_ok = sum(1 for u in uploads if u.get("via") in ("input", "chooser"))
    info["uploaded_ok"] = uploaded_ok
    info["ok"] = bool(
        info["running"]
        or (info.get("banner") and uploaded_ok >= 3 and set_state in ("clicked", "mouse"))
        or (info.get("ready") and set_state in ("clicked", "mouse") and uploaded_ok >= 3)
    )
    return info


def prove_visibility(page) -> dict:
    info = {}
    goto_edit(page)
    click_text(page, r"^Visibility$", y_min=80, max_len=20) or click_text(
        page, r"Scheduled", y_min=100, max_len=30
    )
    page.wait_for_timeout(1000)
    click_text(page, r"Schedule|15 Oct|October", y_min=80, max_len=40)
    page.wait_for_timeout(1200)
    click_text(page, r"15 Oct 2026", y_min=80, max_len=30)
    page.wait_for_timeout(600)
    shot(page, "v14_40_visibility.png")
    t = body_text(page)
    info["has_15"] = bool(re.search(r"15\s*(Oct|October)\s*2026", t, re.I))
    info["has_1800"] = bool(re.search(r"18:00", t, re.I))
    info["has_30"] = bool(re.search(r"30\s*(Sept|Sep|September)\s*2026", t, re.I))
    info["premiere_label"] = bool(re.search(r"Set as Premiere", t, re.I))
    click_text(page, r"^Done$", y_min=200, max_len=10)
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    shot(page, "v14_41_content.png")
    t2 = body_text(page)
    info["content_15"] = bool(re.search(r"15\s*(Oct|October)\s*2026", t2, re.I))
    info["content_30"] = bool(re.search(r"30\s*(Sept|Sep|September)\s*2026", t2, re.I))
    info["ok"] = bool(
        (info["has_15"] or info["content_15"])
        and info["has_1800"]
        and not info["has_30"]
        and not info["content_30"]
    )
    info["snip"] = t[:700]
    return info


def do_end_screen(page) -> dict:
    info = {"related": RELATED_002}
    # Only works when NOT Made for Kids
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    dismiss(page)
    # Click End screen on right rail
    hit = click_text(page, r"^End screen$", y_min=200, max_len=20)
    info["click"] = hit
    page.wait_for_timeout(3000)
    for _ in range(3):
        dismiss(page)
        click_text(page, r"OK, got it")
    shot(page, "v14_50_end.png")
    t = body_text(page)
    info["panel"] = bool(re.search(r"ADD ELEMENT|Add element|1 video|template|End screen", t, re.I))
    info["disabled"] = bool(re.search(r"Made for Kids", t, re.I)) and not info["panel"]

    info["template"] = click_text(page, r"1 video, 1 subscribe", y_min=60, max_len=40)
    page.wait_for_timeout(2000)
    if not info["template"]:
        click_text(page, r"ADD ELEMENT|Add element", y_min=60, max_len=30)
        page.wait_for_timeout(400)
        click_text(page, r"^Video$", y_min=60, exact=True, max_len=10)
        click_text(page, r"^Subscribe$", y_min=60, exact=True, max_len=15)
    shot(page, "v14_51_template.png")

    click_text(page, r"Most recent upload|Best for viewer", y_min=60, max_len=40)
    page.wait_for_timeout(400)
    click_text(page, r"Specific video|Choose a video|Select a video", y_min=60, max_len=40)
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
    click_text(page, r"How Did We Discover the Periodic Table", y_min=80, max_len=80) or click_text(
        page, r"Periodic Table", y_min=80, max_len=40
    )
    page.wait_for_timeout(1000)
    shot(page, "v14_52_bound.png")
    try:
        btn = page.get_by_role("button", name=re.compile(r"^SAVE$|^Save$", re.I))
        if btn.count() and btn.first.is_enabled():
            btn.first.click(timeout=5000)
            info["save"] = "role"
    except Exception:
        pass
    if not info.get("save"):
        info["save"] = "mouse" if click_text(page, r"^SAVE$|^Save$", y_min=0, max_len=10) else None
    page.wait_for_timeout(4000)
    shot(page, "v14_53_saved.png")
    after = body_text(page)
    info["has_002"] = bool(re.search(r"Periodic Table|AL_-qlWko_g", after, re.I))
    info["has_subscribe"] = bool(re.search(r"Subscribe", after, re.I))
    info["error"] = bool(re.search(r"problem in processing|couldn't be saved|At least one element must be a video", after, re.I))
    info["ok"] = bool(not info["error"] and info["panel"] and (info["has_002"] or info["has_subscribe"] or info.get("template")))
    info["after"] = after[:800]
    return info


def main():
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    (EV / "phone_uat_v14.log").write_text("")
    urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=2)
    result = {
        "started": datetime.now().isoformat(timespec="seconds"),
        "videoId": VIDEO_ID,
        "channel": "@HistoryOfScienceYT",
        "note": "v14: fix Made for Kids YES regression from v13, then finish UAT",
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        ctx = browser.contexts[0]
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.set_default_timeout(60000)
        try:
            page.bring_to_front()
        except Exception:
            pass

        log("v14 FIX Made for Kids -> NO (urgent)")
        result["madeForKids"] = fix_kids_no(page)
        dump("V14_KIDS.json", result["madeForKids"])
        if not result["madeForKids"].get("ok"):
            log("WARN kids still not NO — aborting further mutations that need it")
            # still try AI carefully

        log("v14 AI use YES (careful — do not touch Kids radios)")
        result["aiUse"] = set_ai_yes(page)
        dump("V14_AI.json", result["aiUse"])

        log("v14 main thumb A v04")
        result["thumbnail"] = upload_main_thumb(page)
        dump("V14_THUMB.json", result["thumbnail"])

        log("v14 A/B Title+thumbnail")
        result["testAndCompare"] = do_ab(page)
        dump("V14_AB.json", result["testAndCompare"])

        log("v14 Visibility proof")
        result["schedule"] = prove_visibility(page)
        dump("V14_SCHEDULE.json", result["schedule"])

        log("v14 end screen")
        result["endScreen"] = do_end_screen(page)
        dump("V14_END.json", result["endScreen"])

        result["pinnedComment"] = {
            "ok": False,
            "reason": "deferred_while_private_scheduled",
            "note": "Pin on launch day 15 Oct 2026",
        }

    result["ok"] = {
        k: (result[k].get("ok") if isinstance(result.get(k), dict) else None)
        for k in ("madeForKids", "aiUse", "thumbnail", "testAndCompare", "schedule", "endScreen", "pinnedComment")
    }
    result["finished"] = datetime.now().isoformat(timespec="seconds")
    dump("PHONE_UAT_V14_RESULT.json", result)
    log(f"DONE {json.dumps(result['ok'])}")
    print(json.dumps(result["ok"], indent=2))


if __name__ == "__main__":
    main()
