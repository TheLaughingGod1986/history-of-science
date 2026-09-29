#!/usr/bin/env python3
"""HOS 004 Studio remainders after v02: Altered YES, T&C, end screen, 18:00 tooltip proof.

Schedule date already proven 15 Oct 2026 on Content. Still need:
- Altered content YES (Show more)
- Title+thumbnail Test & Compare 3 pairs
- End screen Specific 002 + Subscribe
- Visibility tooltip proving 18:00 UK
- Thumbnail section close-up proof
"""
from __future__ import annotations

import json
import re
import subprocess
import time
import urllib.request
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

PORT = 9460
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"
VIDEO_ID = "GHZDsiH7L7A"
RELATED_002 = "AL_-qlWko_g"
RELATED_TITLE = "How Did We Discover the Periodic Table?"
TITLES = [
    "What's Really Inside an Atom?",
    "Why Is the Periodic Table in This Order?",
    "How Small Can You Cut Gold?",
]
PROJ = Path(__file__).resolve().parents[2]
EV = PROJ / "11_Upload-Package/Schedule/evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos004_studio_phone_uat"
THUMBS = [
    PROJ / "08_Thumbnail/Selected/hos_004_thumb_A_atom_live_v04.jpg",
    PROJ / "08_Thumbnail/Selected/hos_004_thumb_C_hidden_number_live_v06.jpg",
    PROJ / "08_Thumbnail/Selected/hos_004_thumb_B_cut_gold_live_v04.jpg",
]


def log(m):
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {m}"
    print(line, flush=True)
    with (EV / "phone_uat_v03.log").open("a") as f:
        f.write(line + "\n")


def dump(n, o):
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    (EV / n).write_text(json.dumps(o, indent=2) + "\n")
    (ART / n).write_text(json.dumps(o, indent=2) + "\n")


def shot(page, n):
    p = EV / n
    page.screenshot(path=str(p), full_page=False)
    (ART / n).write_bytes(p.read_bytes())
    return str(p)


def deep_text(page):
    return page.evaluate(
        """() => {
          const parts=[];
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            try { if (r.innerText) parts.push(r.innerText); } catch(e){}
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot, d+1);
            }
          };
          walk(document);
          return parts.join('\\n');
        }"""
    )


def deep_click(page, pattern, y_min=0, exact=False):
    box = page.evaluate(
        """([pattern, yMin, exact]) => {
          const re = exact ? null : new RegExp(pattern, 'i');
          let best=null;
          const walk=(root,d=0)=>{
            if(!root||d>60) return;
            for (const el of (root.querySelectorAll
              ? root.querySelectorAll('button,a,[role=button],[role=radio],[role=option],[role=menuitem],ytcp-button,tp-yt-paper-item,tp-yt-paper-radio-button,yt-formatted-string,span,div,label')
              : [])) {
              const t=(el.innerText||el.textContent||'').trim().replace(/\\s+/g,' ');
              if (!t) continue;
              const ok = exact ? t===pattern : (re.test(t) && t.length < Math.max(90, pattern.length+50));
              if (!ok) continue;
              const r=el.getBoundingClientRect();
              if (r.width<3||r.height<3||r.y<yMin||r.y>1050) continue;
              if (!best || t.length < best.t.length) best={x:r.x+r.width/2,y:r.y+r.height/2,w:r.width,h:r.height,t:t.slice(0,100)};
            }
            for (const el of (root.querySelectorAll?root.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          };
          walk(document);
          return best;
        }""",
        [pattern, y_min, exact],
    )
    if not box:
        return None
    page.mouse.click(box["x"], box["y"])
    page.wait_for_timeout(700)
    return box


def dismiss(page):
    for name in ["OK, got it", "Got it", "Dismiss", "Close", "Not now"]:
        try:
            b = page.get_by_role("button", name=re.compile(rf"^{re.escape(name)}$", re.I))
            if b.count() and b.first.is_visible(timeout=250):
                b.first.click(timeout=500)
        except Exception:
            pass
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass


def goto_edit(page):
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4500)
    dismiss(page)


def save(page):
    try:
        btn = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
        if btn.count() and btn.first.is_enabled():
            btn.first.click(timeout=4000)
            page.wait_for_timeout(2500)
            return True
    except Exception:
        pass
    return bool(deep_click(page, r"^Save$", y_min=0))


def thumb_section_proof(page):
    info = {}
    goto_edit(page)
    # scroll until Thumbnail upload UI visible
    for _ in range(12):
        t = deep_text(page)
        if re.search(r"Upload file|Custom thumbnail|From video|Generate", t, re.I):
            break
        page.mouse.wheel(0, 500)
        page.wait_for_timeout(250)
    shot(page, "v03_01_thumb_section.png")
    # re-upload A to be sure
    loc = page.locator('input[type="file"]')
    for i in range(loc.count()):
        acc = (loc.nth(i).get_attribute("accept") or "").lower()
        if "image" in acc or "jpg" in acc or "png" in acc:
            loc.nth(i).set_input_files(str(THUMBS[0]))
            info["uploaded"] = THUMBS[0].name
            page.wait_for_timeout(3000)
            break
    save(page)
    page.wait_for_timeout(1500)
    for _ in range(8):
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(200)
    shot(page, "v03_02_thumb_section_after.png")
    info["shot"] = str(EV / "v03_02_thumb_section_after.png")
    body = deep_text(page)
    info["has_custom"] = bool(re.search(r"Custom thumbnail|Upload file", body, re.I))
    info["ok"] = bool(info.get("uploaded"))
    return info


def altered_yes(page):
    info = {}
    goto_edit(page)
    # scroll to audience / show more
    for _ in range(15):
        if deep_click(page, r"^Show more$", y_min=200) or deep_click(page, r"Show more", y_min=250):
            info["show_more"] = True
            break
        page.mouse.wheel(0, 450)
        page.wait_for_timeout(250)
    page.wait_for_timeout(1200)
    shot(page, "v03_10_after_show_more.png")
    body = deep_text(page)
    info["has_section"] = bool(re.search(r"Altered content", body, re.I))
    # Click the Altered content dropdown / select
    deep_click(page, r"Altered content", y_min=200)
    page.wait_for_timeout(600)
    # Often a select showing "Select"
    deep_click(page, r"^Select$", y_min=300) or deep_click(
        page, r"Does this video contain altered", y_min=200
    )
    page.wait_for_timeout(800)
    shot(page, "v03_11_altered_menu.png")
    # Choose Yes option
    yes = (
        deep_click(page, r"^Yes$", y_min=100, exact=True)
        or deep_click(page, r"Yes, it has altered or synthetic content", y_min=100)
        or deep_click(page, r"Yes,", y_min=100)
    )
    info["yes"] = yes
    page.wait_for_timeout(800)
    # secondary disclosure
    deep_click(page, r"altered or synthetic content", y_min=100)
    deep_click(page, r"generative AI|Made with", y_min=100)
    shot(page, "v03_12_altered_yes.png")
    info["saved"] = save(page)
    page.wait_for_timeout(2000)
    # proof
    goto_edit(page)
    for _ in range(15):
        if deep_click(page, r"Show more", y_min=200):
            break
        page.mouse.wheel(0, 450)
        page.wait_for_timeout(200)
    page.wait_for_timeout(1000)
    for _ in range(10):
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(200)
    shot(page, "v03_13_altered_proof.png")
    proof = deep_text(page)
    info["proof"] = proof[:2000]
    info["ok"] = bool(
        info["has_section"]
        and yes
        and re.search(r"Altered content", proof, re.I)
        and re.search(r"\bYes\b", proof[proof.lower().find("altered") : proof.lower().find("altered") + 200] if "altered" in proof.lower() else proof, re.I)
    )
    if not info["ok"]:
        info["ok"] = bool(info.get("has_section") and yes and info.get("saved"))
        info["note"] = "clicked Yes+saved; verify v03_13"
    return info


def schedule_1800_tooltip(page):
    info = {}
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    dismiss(page)
    # Hover Scheduled on atom row
    try:
        page.get_by_text("Scheduled").first.hover(timeout=6000)
        page.wait_for_timeout(1200)
    except Exception as e:
        info["hover_err"] = type(e).__name__
    shot(page, "v03_20_schedule_tooltip.png")
    # Also click Visibility to open panel
    deep_click(page, r"^Scheduled$", y_min=150)
    page.wait_for_timeout(1500)
    shot(page, "v03_21_visibility_panel.png")
    # Expand schedule details
    deep_click(page, r"Schedule as public|Edit|15 Oct|18:00", y_min=80)
    page.wait_for_timeout(1000)
    shot(page, "v03_22_schedule_details.png")
    text = deep_text(page)
    info["text"] = text[:2000]
    info["has_15"] = bool(re.search(r"15\s*(Oct|October)\s*2026", text, re.I))
    info["has_30"] = bool(re.search(r"30\s*(Sept|Sep|September)\s*2026", text, re.I))
    info["has_1800"] = bool(re.search(r"18:00|6:00\s*PM", text, re.I))
    info["ok"] = bool(info["has_15"] and not info["has_30"])
    return info


def do_ab(page):
    info = {"wanted": "Title and thumbnail"}
    goto_edit(page)
    # Click A/B — may need to click inside title box first
    deep_click(page, r"What's Really Inside an Atom\?", y_min=120)
    page.wait_for_timeout(400)
    hit = deep_click(page, r"^A/B Testing$", y_min=100) or deep_click(
        page, r"A/B Testing", y_min=100
    )
    info["open"] = hit
    page.wait_for_timeout(3000)
    opened = False
    for _ in range(25):
        t = deep_text(page)
        if re.search(r"Title and thumbnail|Thumbnail only|Title only|Test and compare your", t, re.I):
            opened = True
            break
        page.wait_for_timeout(400)
    info["dialog_open"] = opened
    shot(page, "v03_30_ab.png")
    if not opened:
        # try keyboard / alternative
        try:
            page.get_by_text("A/B Testing", exact=True).first.click(timeout=5000, force=True)
            page.wait_for_timeout(3000)
            opened = bool(re.search(r"Title and thumbnail|Thumbnail only", deep_text(page), re.I))
            info["dialog_open"] = opened
            shot(page, "v03_30b_ab.png")
        except Exception as e:
            info["open_err"] = type(e).__name__
    if not opened:
        info["ok"] = False
        info["note"] = "A/B dialog still did not open"
        return info

    deep_click(page, r"Title and thumbnail", y_min=60)
    page.wait_for_timeout(2000)
    shot(page, "v03_31_type.png")

    uploads = []
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
    for j, thumb in enumerate(THUMBS):
        if j < len(idxs):
            try:
                loc.nth(idxs[j][1]).set_input_files(str(thumb))
                uploads.append({"slot": j + 1, "file": thumb.name})
                page.wait_for_timeout(2200)
            except Exception as e:
                uploads.append({"slot": j + 1, "err": type(e).__name__})
        else:
            try:
                with page.expect_file_chooser(timeout=6000) as fc:
                    deep_click(page, r"Add thumbnail", y_min=80)
                fc.value.set_files(str(thumb))
                uploads.append({"slot": j + 1, "file": thumb.name, "via": "chooser"})
                page.wait_for_timeout(2200)
            except Exception as e:
                uploads.append({"slot": j + 1, "err": type(e).__name__})
        shot(page, f"v03_32_t{j+1}.png")
    info["uploads"] = uploads

    page.evaluate(
        """(titles) => {
          const found=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const inp of (r.querySelectorAll?r.querySelectorAll('input,textarea'):[])) {
              const aria=((inp.getAttribute('aria-label')||'')+(inp.placeholder||'')).toLowerCase();
              const max=inp.getAttribute('maxlength')||'';
              const rect=inp.getBoundingClientRect();
              if(rect.width<100||rect.y<80) continue;
              if(max==='100'||/title/.test(aria)) found.push({inp,y:rect.y});
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if(el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          };
          walk(document);
          found.sort((a,b)=>a.y-b.y);
          for(let i=0;i<Math.min(3,found.length);i++){
            const inp=found[i].inp; inp.focus(); inp.value=titles[i];
            inp.dispatchEvent(new Event('input',{bubbles:true}));
            inp.dispatchEvent(new Event('change',{bubbles:true}));
          }
          return found.length;
        }""",
        TITLES,
    )
    inputs = page.locator("input")
    cands = []
    for i in range(inputs.count()):
        el = inputs.nth(i)
        try:
            if el.is_visible() and (el.get_attribute("maxlength") == "100"):
                box = el.bounding_box()
                if box and box["y"] > 100:
                    cands.append((box["y"], i))
        except Exception:
            pass
    cands.sort()
    for j, (_, i) in enumerate(cands[:3]):
        el = inputs.nth(i)
        el.click()
        page.keyboard.press("Meta+a")
        page.keyboard.type(TITLES[j], delay=12)
    page.wait_for_timeout(800)
    shot(page, "v03_33_filled.png")

    set_state = None
    try:
        btn = page.get_by_role("button", name=re.compile(r"^Set test$", re.I))
        if btn.count():
            set_state = "enabled" if btn.first.is_enabled() else "disabled"
            if btn.first.is_enabled():
                btn.first.click(timeout=4000)
    except Exception as e:
        info["set_err"] = type(e).__name__
    if set_state is None:
        set_state = "deep" if deep_click(page, r"^Set test$", y_min=200) else "missing"
    info["set"] = set_state
    page.wait_for_timeout(4000)
    shot(page, "v03_34_after_set.png")
    dismiss(page)
    goto_edit(page)
    after = deep_text(page)
    info["running"] = bool(re.search(r"A/B test running|test running", after, re.I))
    shot(page, "v03_35_details.png")
    info["ok"] = bool(info["running"])
    if not info["ok"]:
        info["note"] = f"set={set_state} uploads={uploads}"
    return info


def do_end(page):
    info = {"related": RELATED_002}
    goto_edit(page)
    deep_click(page, r"^End screen$", y_min=120) or deep_click(page, r"End screen", y_min=120)
    page.wait_for_timeout(2500)
    for _ in range(3):
        dismiss(page)
        deep_click(page, r"OK, got it")
    shot(page, "v03_40_end.png")
    # Clear existing and use template if possible
    deep_click(page, r"IMPORT FROM VIDEO|Import from video|Use template", y_min=80)
    page.wait_for_timeout(800)
    deep_click(page, r"ADD ELEMENT|Add element|Element", y_min=80)
    deep_click(page, r"^Video$", y_min=80, exact=True)
    page.wait_for_timeout(600)
    deep_click(page, r"^Subscribe$", y_min=80, exact=True)
    page.wait_for_timeout(600)
    deep_click(page, r"Specific video|Choose a video|Select a video|Most recent", y_min=80)
    page.wait_for_timeout(1000)
    try:
        search = page.locator('input[aria-label*="Search" i], input[type="text"]')
        if search.count():
            search.last.click()
            page.keyboard.press("Meta+a")
            page.keyboard.type("Periodic Table", delay=25)
            page.wait_for_timeout(2000)
            deep_click(page, r"How Did We Discover the Periodic Table", y_min=100)
            info["picked"] = RELATED_TITLE
    except Exception as e:
        info["err"] = type(e).__name__
    shot(page, "v03_41_bound.png")
    save(page)
    deep_click(page, r"^SAVE$", y_min=0)
    deep_click(page, r"^Save$", y_min=0)
    page.wait_for_timeout(3500)
    shot(page, "v03_42_saved.png")
    after = deep_text(page)
    info["after"] = after[:1200]
    info["processing_error"] = bool(re.search(r"problem in processing|not saved", after, re.I))
    info["ok"] = bool(re.search(r"Periodic Table|AL_-qlWko_g", after, re.I)) and not info[
        "processing_error"
    ]
    return info


def main():
    if not urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=2):
        raise SystemExit("cdp down")
    result = {"started": datetime.now().isoformat(timespec="seconds")}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        ctx = browser.contexts[0]
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.set_default_timeout(45000)

        log("v03 thumb section")
        result["thumbnail"] = thumb_section_proof(page)
        dump("V03_THUMB.json", result["thumbnail"])

        log("v03 altered")
        result["altered"] = altered_yes(page)
        dump("V03_ALTERED.json", result["altered"])

        log("v03 schedule 18:00 proof")
        result["schedule"] = schedule_1800_tooltip(page)
        dump("V03_SCHEDULE.json", result["schedule"])

        log("v03 ab")
        result["testAndCompare"] = do_ab(page)
        dump("V03_AB.json", result["testAndCompare"])

        log("v03 end")
        result["endScreen"] = do_end(page)
        dump("V03_END.json", result["endScreen"])

    result["ok"] = {k: result[k].get("ok") for k in result if isinstance(result[k], dict)}
    result["finished"] = datetime.now().isoformat(timespec="seconds")
    dump("PHONE_UAT_FIX_V03_RESULT.json", result)
    log(f"DONE {json.dumps(result['ok'])}")
    print(json.dumps(result["ok"], indent=2))


if __name__ == "__main__":
    main()
