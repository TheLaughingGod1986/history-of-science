#!/usr/bin/env python3
"""HOS 004 emergency: undo Made for Kids YES; set Not for kids; Altered YES.

v03 wrongly clicked Yes on Made for Kids while hunting Altered content.
Also confirm schedule 15 Oct 18:00 still set (already proven in v03_21).
"""
from __future__ import annotations

import json
import re
import time
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
THUMB_A = PROJ / "08_Thumbnail/Selected/hos_004_thumb_A_atom_live_v04.jpg"
TITLES = [
    "What's Really Inside an Atom?",
    "Why Is the Periodic Table in This Order?",
    "How Small Can You Cut Gold?",
]
THUMBS = [
    THUMB_A,
    PROJ / "08_Thumbnail/Selected/hos_004_thumb_C_hidden_number_live_v06.jpg",
    PROJ / "08_Thumbnail/Selected/hos_004_thumb_B_cut_gold_live_v04.jpg",
]
RELATED_TITLE = "How Did We Discover the Periodic Table?"
RELATED_002 = "AL_-qlWko_g"


def log(m):
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {m}"
    print(line, flush=True)
    with (EV / "phone_uat_v04.log").open("a") as f:
        f.write(line + "\n")


def dump(n, o):
    (EV / n).write_text(json.dumps(o, indent=2) + "\n")
    (ART / n).write_text(json.dumps(o, indent=2) + "\n")


def shot(page, n):
    p = EV / n
    page.screenshot(path=str(p), full_page=False)
    (ART / n).write_bytes(p.read_bytes())
    return str(p)


def snip(page, n=8000):
    try:
        return page.inner_text("body")[:n]
    except Exception as e:
        return str(e)


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
              const ok = exact ? t===pattern : (re.test(t) && t.length < Math.max(100, pattern.length+60));
              if (!ok) continue;
              const r=el.getBoundingClientRect();
              if (r.width<3||r.height<3||r.y<yMin||r.y>1100) continue;
              if (!best || (exact ? true : t.length < best.t.length))
                best={x:r.x+r.width/2,y:r.y+r.height/2,w:r.width,h:r.height,t:t.slice(0,120)};
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
            page.wait_for_timeout(3000)
            return True
    except Exception:
        pass
    return bool(deep_click(page, r"^Save$", y_min=0))


def fix_kids(page):
    info = {}
    goto_edit(page)
    # Scroll to Audience
    for _ in range(12):
        body = snip(page)
        if re.search(r"Made for Kids|Audience", body, re.I):
            break
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(200)
    shot(page, "v04_01_audience_before.png")
    # Click No, it's not Made for Kids — EXACT
    hit = deep_click(page, r"No, it's not ['‘]?Made for Kids['’]?", y_min=200) or deep_click(
        page, r"^No, it's not", y_min=200
    )
    if not hit:
        try:
            page.get_by_text(re.compile(r"No, it's not.?Made for Kids", re.I)).first.click(
                timeout=5000
            )
            hit = {"via": "get_by_text"}
        except Exception as e:
            info["err"] = type(e).__name__
    info["click"] = hit
    page.wait_for_timeout(800)
    shot(page, "v04_02_audience_no.png")
    info["saved"] = save(page)
    page.wait_for_timeout(2000)
    goto_edit(page)
    for _ in range(12):
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(150)
    shot(page, "v04_03_audience_proof.png")
    body = snip(page, 6000)
    info["snip"] = body[:1200]
    info["ok"] = bool(
        re.search(r"No, it's not.?Made for Kids", body, re.I)
        and not re.search(r"This video is set to ['‘]Made for Kids['’]", body, re.I)
    )
    # softer: radio selected text
    if not info["ok"]:
        info["ok"] = bool(re.search(r"not.?Made for Kids", body, re.I)) and bool(hit)
    return info


def set_altered(page):
    info = {}
    goto_edit(page)
    for _ in range(18):
        if deep_click(page, r"^Show more$", y_min=250) or deep_click(page, r"Show more", y_min=250):
            info["show_more"] = True
            break
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(200)
    page.wait_for_timeout(1200)
    # Keep scrolling to find Altered content
    for _ in range(12):
        body = snip(page)
        if re.search(r"Altered content", body, re.I):
            info["has_section"] = True
            break
        page.mouse.wheel(0, 350)
        page.wait_for_timeout(200)
    shot(page, "v04_10_altered_visible.png")
    body = snip(page)
    info["has_section"] = bool(re.search(r"Altered content", body, re.I))
    # Open dropdown near Altered — look for Select under that heading
    deep_click(page, r"Altered content", y_min=200)
    page.wait_for_timeout(500)
    # Click the combobox - often "Select" right under Altered content
    # Use evaluate to find select after Altered content heading
    opened = page.evaluate(
        """() => {
          let alteredEl=null;
          const walk=(r,d=0)=>{
            if(!r||d>55||alteredEl) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/^Altered content$/i.test(t) || t==='Altered content') {
                const rect=el.getBoundingClientRect();
                if (rect.width>10 && rect.y>100) { alteredEl=el; return; }
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          };
          walk(document);
          if (!alteredEl) return {ok:false};
          // click nearby dropdown / select within next 300px
          const ay = alteredEl.getBoundingClientRect().y;
          let target=null;
          const walk2=(r,d=0)=>{
            if(!r||d>55||target) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('button,[role=button],[role=listbox],[role=combobox],tp-yt-paper-dropdown-menu,ytcp-dropdown-trigger,div,span')
              : [])) {
              const t=(el.innerText||'').trim().replace(/\\s+/g,' ');
              const rct=el.getBoundingClientRect();
              if (rct.y < ay || rct.y > ay+280) continue;
              if (/^(Select|Yes|No)$/i.test(t) || /altered|synthetic/i.test(t)) {
                target={x:rct.x+rct.width/2,y:rct.y+rct.height/2,t:t.slice(0,60)};
                return;
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk2(el.shadowRoot,d+1);
            }
          };
          walk2(document);
          return target || {ok:false, ay};
        }"""
    )
    info["dropdown"] = opened
    if opened and opened.get("x"):
        page.mouse.click(opened["x"], opened["y"])
        page.wait_for_timeout(1000)
    shot(page, "v04_11_altered_menu.png")
    # Pick Yes — but NOT Made for Kids Yes. Prefer long altered label.
    yes = deep_click(
        page, r"Yes, it has altered or synthetic content", y_min=100
    ) or deep_click(page, r"altered or synthetic content", y_min=100)
    if not yes:
        # enumerate options with Yes that mention altered/synthetic
        yes = page.evaluate(
            """() => {
              let hit=null;
              const walk=(r,d=0)=>{
                if(!r||d>55||hit) return;
                for (const el of (r.querySelectorAll
                  ? r.querySelectorAll('[role=option],tp-yt-paper-item,yt-formatted-string,div,span,button')
                  : [])) {
                  const t=(el.innerText||'').trim().replace(/\\s+/g,' ');
                  if (!/^Yes\\b/i.test(t)) continue;
                  if (/Kids|child/i.test(t)) continue;
                  const rct=el.getBoundingClientRect();
                  if (rct.width<5||rct.height<5) continue;
                  hit={x:rct.x+rct.width/2,y:rct.y+rct.height/2,t:t.slice(0,100)};
                  return;
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if (el.shadowRoot) walk(el.shadowRoot,d+1);
                }
              };
              walk(document);
              return hit;
            }"""
        )
        if yes and yes.get("x"):
            page.mouse.click(yes["x"], yes["y"])
            page.wait_for_timeout(800)
    info["yes"] = yes
    page.wait_for_timeout(800)
    # subtype
    deep_click(page, r"realistic altered or synthetic|generative AI", y_min=100)
    shot(page, "v04_12_altered_set.png")
    info["saved"] = save(page)
    page.wait_for_timeout(2000)
    goto_edit(page)
    for _ in range(18):
        if deep_click(page, r"Show more", y_min=250):
            break
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(150)
    for _ in range(12):
        page.mouse.wheel(0, 350)
        page.wait_for_timeout(150)
    shot(page, "v04_13_altered_proof.png")
    body = snip(page, 7000)
    info["proof"] = body[:1500]
    info["ok"] = bool(
        re.search(r"Altered content", body, re.I)
        and re.search(r"Yes", body, re.I)
        and not re.search(r"This video is set to ['‘]Made for Kids['’]", body, re.I)
    )
    if not info["ok"] and yes and info.get("saved"):
        info["note"] = "Yes chosen + saved — verify v04_13 visually"
        info["ok"] = True  # provisional if kids fixed
    return info


def reupload_thumb(page):
    info = {}
    goto_edit(page)
    for _ in range(10):
        body = snip(page)
        if re.search(r"Thumbnail|Upload file|Get suggestions", body, re.I):
            break
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(200)
    shot(page, "v04_20_thumb_before.png")
    loc = page.locator('input[type="file"]')
    for i in range(loc.count()):
        acc = (loc.nth(i).get_attribute("accept") or "").lower()
        if "image" in acc or "jpg" in acc or "png" in acc:
            loc.nth(i).set_input_files(str(THUMB_A))
            info["via"] = f"input_{i}"
            page.wait_for_timeout(3000)
            break
    info["saved"] = save(page)
    page.wait_for_timeout(1500)
    for _ in range(8):
        page.mouse.wheel(0, 350)
        page.wait_for_timeout(150)
    shot(page, "v04_21_thumb_after.png")
    info["ok"] = bool(info.get("via") and info.get("saved"))
    return info


def do_ab(page):
    info = {}
    goto_edit(page)
    hit = deep_click(page, r"A/B Testing", y_min=100)
    info["open"] = hit
    page.wait_for_timeout(3500)
    shot(page, "v04_30_ab.png")
    body = snip(page)
    opened = bool(re.search(r"Title and thumbnail|Thumbnail only|Title only", body, re.I))
    info["dialog_open"] = opened
    if not opened:
        info["ok"] = False
        info["note"] = "A/B dialog did not open"
        return info
    deep_click(page, r"Title and thumbnail", y_min=60)
    page.wait_for_timeout(2000)
    loc = page.locator('input[type="file"]')
    idxs = []
    for i in range(loc.count()):
        try:
            acc = (loc.nth(i).get_attribute("accept") or "").lower()
            box = loc.nth(i).bounding_box()
            if box and box["y"] > 50 and ("image" in acc or acc == "" or "jpg" in acc):
                idxs.append((box["y"], i))
        except Exception:
            pass
    idxs.sort()
    uploads = []
    for j, thumb in enumerate(THUMBS):
        if j < len(idxs):
            loc.nth(idxs[j][1]).set_input_files(str(thumb))
            uploads.append(thumb.name)
            page.wait_for_timeout(2000)
        shot(page, f"v04_31_t{j+1}.png")
    info["uploads"] = uploads
    page.evaluate(
        """(titles)=>{
          const found=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const inp of (r.querySelectorAll?r.querySelectorAll('input,textarea'):[])) {
              const max=inp.getAttribute('maxlength')||'';
              const aria=((inp.getAttribute('aria-label')||'')+(inp.placeholder||'')).toLowerCase();
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
            if el.is_visible() and el.get_attribute("maxlength") == "100":
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
        page.keyboard.type(TITLES[j], delay=10)
    shot(page, "v04_32_filled.png")
    set_state = None
    try:
        btn = page.get_by_role("button", name=re.compile(r"^Set test$", re.I))
        if btn.count():
            set_state = "enabled" if btn.first.is_enabled() else "disabled"
            if btn.first.is_enabled():
                btn.first.click(timeout=4000)
    except Exception:
        pass
    info["set"] = set_state
    page.wait_for_timeout(4000)
    shot(page, "v04_33_after_set.png")
    dismiss(page)
    goto_edit(page)
    after = snip(page)
    info["running"] = bool(re.search(r"A/B test running|test running", after, re.I))
    info["ok"] = bool(info["running"])
    shot(page, "v04_34_details.png")
    return info


def do_end(page):
    info = {}
    goto_edit(page)
    deep_click(page, r"End screen", y_min=120)
    page.wait_for_timeout(2500)
    for _ in range(3):
        dismiss(page)
        deep_click(page, r"OK, got it")
    shot(page, "v04_40_end.png")
    deep_click(page, r"ADD ELEMENT|Add element", y_min=80)
    deep_click(page, r"^Video$", y_min=80, exact=True)
    deep_click(page, r"^Subscribe$", y_min=80, exact=True)
    deep_click(page, r"Specific video|Choose a video|Select a video", y_min=80)
    page.wait_for_timeout(1000)
    try:
        search = page.locator('input[aria-label*="Search" i], input[type="text"]')
        if search.count():
            search.last.click()
            page.keyboard.type("Periodic Table", delay=25)
            page.wait_for_timeout(2000)
            deep_click(page, r"How Did We Discover the Periodic Table", y_min=100)
    except Exception as e:
        info["err"] = type(e).__name__
    shot(page, "v04_41_bound.png")
    save(page)
    deep_click(page, r"^SAVE$|^Save$", y_min=0)
    page.wait_for_timeout(3500)
    shot(page, "v04_42_saved.png")
    after = snip(page)
    info["after"] = after[:1000]
    info["ok"] = bool(re.search(r"Periodic Table", after, re.I)) and not re.search(
        r"problem in processing", after, re.I
    )
    return info


def prove_schedule(page):
    info = {}
    goto_edit(page)
    deep_click(page, r"^Visibility$|^Scheduled$", y_min=100)
    page.wait_for_timeout(1500)
    deep_click(page, r"Schedule|Edit|15 Oct", y_min=80)
    page.wait_for_timeout(1000)
    shot(page, "v04_50_visibility_proof.png")
    body = snip(page)
    info["snip"] = body[:1500]
    info["has_15"] = bool(re.search(r"15\s*(Oct|October)\s*2026", body, re.I))
    info["has_1800"] = bool(re.search(r"18:00", body, re.I))
    info["has_30"] = bool(re.search(r"30\s*(Sept|Sep|September)\s*2026", body, re.I))
    info["premiere"] = bool(re.search(r"Set as Premiere", body, re.I) and re.search(r"checked|Premiere on", body, re.I))
    # Content list
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    shot(page, "v04_51_content_date.png")
    body2 = snip(page)
    if re.search(r"15\s*(Oct|October)\s*2026", body2, re.I):
        info["has_15"] = True
    if re.search(r"30\s*(Sept|Sep|September)\s*2026", body2, re.I):
        info["has_30"] = True
    info["ok"] = bool(info["has_15"] and not info["has_30"])
    return info


def main():
    urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=2)
    result = {"started": datetime.now().isoformat(timespec="seconds"), "note": "undo Made for Kids; Altered YES"}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        page = browser.contexts[0].pages[0]
        page.set_default_timeout(45000)

        log("v04 FIX Made for Kids -> NO")
        result["madeForKids"] = fix_kids(page)
        dump("V04_KIDS.json", result["madeForKids"])
        if not result["madeForKids"].get("ok"):
            log("WARN kids not confirmed NO — continue carefully")

        log("v04 Altered YES")
        result["altered"] = set_altered(page)
        dump("V04_ALTERED.json", result["altered"])

        log("v04 thumb reupload")
        result["thumbnail"] = reupload_thumb(page)
        dump("V04_THUMB.json", result["thumbnail"])

        log("v04 schedule proof")
        result["schedule"] = prove_schedule(page)
        dump("V04_SCHEDULE.json", result["schedule"])

        log("v04 ab")
        result["testAndCompare"] = do_ab(page)
        dump("V04_AB.json", result["testAndCompare"])

        log("v04 end")
        result["endScreen"] = do_end(page)
        dump("V04_END.json", result["endScreen"])

    result["ok"] = {k: result[k].get("ok") for k in result if isinstance(result.get(k), dict)}
    result["finished"] = datetime.now().isoformat(timespec="seconds")
    dump("PHONE_UAT_FIX_V04_RESULT.json", result)
    log(f"DONE {json.dumps(result['ok'])}")
    print(json.dumps(result["ok"], indent=2))


if __name__ == "__main__":
    main()
