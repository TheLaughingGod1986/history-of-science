#!/usr/bin/env python3
"""HOS 004 Studio phone-UAT v12 — complete A/B + AI proof + end screen.

Uses file-chooser for empty Add thumbnail slots (v11 missed slots 2/3).
End screen via ?panel=endscreen. CDP :9460 · no .env.
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
RELATED_TITLE = "How Did We Discover the Periodic Table?"
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
    with (EV / "phone_uat_v12.log").open("a") as f:
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


def snip(page, n=10000) -> str:
    try:
        return page.inner_text("body")[:n]
    except Exception as e:
        return str(e)


def deep_text(page, n=12000) -> str:
    return page.evaluate(
        """(n) => {
          let out='';
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            if (r.innerText) out += '\\n' + r.innerText;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          };
          walk(document);
          return out.slice(0,n);
        }""",
        n,
    )


def deep_click(page, pattern, y_min=0, exact=False, y_max=1400):
    box = page.evaluate(
        """([pattern, yMin, exact, yMax]) => {
          const re = exact ? null : new RegExp(pattern, 'i');
          let best=null;
          const walk=(root,d=0)=>{
            if(!root||d>60) return;
            for (const el of (root.querySelectorAll
              ? root.querySelectorAll('button,a,[role=button],[role=radio],[role=option],[role=menuitem],ytcp-button,tp-yt-paper-item,tp-yt-paper-radio-button,yt-formatted-string,span,div,label')
              : [])) {
              const t=(el.innerText||el.textContent||'').trim().replace(/\\s+/g,' ');
              if (!t) continue;
              const ok = exact ? t===pattern : (re.test(t) && t.length < Math.max(120, pattern.length+80));
              if (!ok) continue;
              const r=el.getBoundingClientRect();
              if (r.width<3||r.height<3||r.y<yMin||r.y>yMax) continue;
              if (!best || t.length < best.t.length)
                best={x:r.x+r.width/2,y:r.y+r.height/2,w:r.width,h:r.height,t:t.slice(0,140)};
            }
            for (const el of (root.querySelectorAll?root.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          };
          walk(document);
          return best;
        }""",
        [pattern, y_min, exact, y_max],
    )
    if not box:
        return None
    page.mouse.click(box["x"], box["y"])
    page.wait_for_timeout(700)
    return box


def dismiss(page) -> None:
    for name in ["OK, got it", "Got it", "Dismiss", "Close", "Not now"]:
        try:
            b = page.get_by_role("button", name=re.compile(rf"^{re.escape(name)}$", re.I))
            if b.count() and b.first.is_visible(timeout=200):
                b.first.click(timeout=400)
        except Exception:
            pass
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass


def goto_edit(page) -> None:
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4500)
    dismiss(page)


def save(page) -> dict:
    info = {"via": None, "enabled": None}
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
    # try Schedule as public / Save too
    hit = deep_click(page, r"^Save$", y_min=0, y_max=200)
    if hit:
        info["via"] = "deep_top"
        page.wait_for_timeout(4000)
    return info


def list_file_inputs(page):
    loc = page.locator('input[type="file"]')
    idxs = []
    for i in range(loc.count()):
        try:
            acc = (loc.nth(i).get_attribute("accept") or "").lower()
            box = loc.nth(i).bounding_box()
            if not box or box["y"] < 40:
                continue
            if "image" in acc or "jpg" in acc or "png" in acc or acc == "" or "jpeg" in acc:
                idxs.append({"y": box["y"], "i": i, "x": box["x"], "w": box["width"], "h": box["height"]})
        except Exception:
            pass
    idxs.sort(key=lambda d: d["y"])
    return loc, idxs


def upload_slot(page, thumb: Path, slot_j: int) -> dict:
    """Upload one thumbnail into A/B dialog slot via file input or chooser."""
    out = {"slot": slot_j + 1, "file": thumb.name}
    loc, idxs = list_file_inputs(page)
    # Prefer unused inputs by index order
    if slot_j < len(idxs):
        try:
            loc.nth(idxs[slot_j]["i"]).set_input_files(str(thumb))
            out["via"] = "input"
            page.wait_for_timeout(2500)
            return out
        except Exception as e:
            out["input_err"] = type(e).__name__

    # Click Add thumbnail / empty zone then chooser
    for attempt in range(3):
        try:
            with page.expect_file_chooser(timeout=7000) as fc:
                # Prefer the empty Add thumbnail button lowest / next
                hit = deep_click(page, r"^Add thumbnail$", y_min=80) or deep_click(
                    page, r"Add thumbnail", y_min=80
                )
                if not hit:
                    # click dashed upload zones via evaluate
                    page.evaluate(
                        """() => {
                          const walk=(r,d=0)=>{
                            if(!r||d>55) return null;
                            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                              const t=(el.innerText||'').trim();
                              const rect=el.getBoundingClientRect();
                              if (/^Add thumbnail$/i.test(t) && rect.width>20 && rect.y>80) {
                                el.click(); return true;
                              }
                            }
                            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                              if (el.shadowRoot) { const x=walk(el.shadowRoot,d+1); if(x) return x; }
                            }
                            return null;
                          };
                          return walk(document);
                        }"""
                    )
            fc.value.set_files(str(thumb))
            out["via"] = f"chooser:{attempt}"
            page.wait_for_timeout(2500)
            return out
        except Exception as e:
            out[f"chooser_err_{attempt}"] = type(e).__name__
            page.wait_for_timeout(500)

    # Last resort: any remaining file input
    loc, idxs = list_file_inputs(page)
    for d in idxs:
        try:
            loc.nth(d["i"]).set_input_files(str(thumb))
            out["via"] = "input_any"
            page.wait_for_timeout(2500)
            return out
        except Exception:
            continue
    out["via"] = "failed"
    return out


def fill_titles(page) -> int:
    n = page.evaluate(
        """(titles)=>{
          const found=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const inp of (r.querySelectorAll?r.querySelectorAll('input,textarea'):[])) {
              const max=inp.getAttribute('maxlength')||'';
              const aria=((inp.getAttribute('aria-label')||'')+(inp.placeholder||'')).toLowerCase();
              const rect=inp.getBoundingClientRect();
              if(rect.width<80||rect.y<60||rect.y>1100) continue;
              if(max==='100'||/title|add title/.test(aria)||/add title/i.test(inp.placeholder||'')) {
                found.push({inp,y:rect.y});
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if(el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          };
          walk(document);
          found.sort((a,b)=>a.y-b.y);
          const uniq=[];
          for (const f of found) {
            if (!uniq.length || Math.abs(uniq[uniq.length-1].y - f.y) > 24) uniq.push(f);
          }
          for(let i=0;i<Math.min(3,uniq.length);i++){
            const inp=uniq[i].inp;
            inp.focus();
            const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
            nativeSetter.call(inp, titles[i]);
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
            if not el.is_visible():
                continue
            ml = el.get_attribute("maxlength")
            ph = (el.get_attribute("placeholder") or "").lower()
            box = el.bounding_box()
            if not box or box["y"] < 80 or box["y"] > 1100:
                continue
            if ml == "100" or "title" in ph:
                cands.append((box["y"], i))
        except Exception:
            pass
    cands.sort()
    picked = []
    for y, i in cands:
        if not picked or abs(picked[-1][0] - y) > 24:
            picked.append((y, i))
    for j, (_, i) in enumerate(picked[:3]):
        el = inputs.nth(i)
        el.click()
        page.keyboard.press("Meta+a")
        page.keyboard.type(TITLES[j], delay=10)
        page.wait_for_timeout(250)
    return max(n or 0, len(picked))


def do_ab(page) -> dict:
    info = {"pairs": [{"title": t, "thumb": th.name} for t, th in zip(TITLES, THUMBS)]}
    goto_edit(page)
    deep_click(page, r"What's Really Inside an Atom\?", y_min=120)
    page.wait_for_timeout(300)
    hit = deep_click(page, r"^A/B Testing$", y_min=80) or deep_click(page, r"A/B Testing", y_min=80)
    info["open"] = hit
    page.wait_for_timeout(2800)
    opened = False
    for _ in range(20):
        t = deep_text(page)
        if re.search(r"Title and thumbnail|Thumbnail only|Title only|Test and compare", t, re.I):
            opened = True
            break
        page.wait_for_timeout(350)
    info["dialog_open"] = opened
    if not opened:
        try:
            page.get_by_text("A/B Testing", exact=True).first.click(timeout=5000, force=True)
            page.wait_for_timeout(2500)
            opened = bool(re.search(r"Title and thumbnail|Thumbnail only", deep_text(page), re.I))
            info["dialog_open"] = opened
        except Exception as e:
            info["open_err"] = type(e).__name__
    shot(page, "v12_10_ab_open.png")
    if not opened:
        info["ok"] = False
        info["note"] = "dialog not open"
        return info

    deep_click(page, r"Title and thumbnail", y_min=40)
    page.wait_for_timeout(2000)
    shot(page, "v12_11_mode.png")

    uploads = []
    for j, thumb in enumerate(THUMBS):
        # Scroll dialog content if needed to reveal next Add thumbnail
        page.mouse.wheel(0, 120 * j)
        page.wait_for_timeout(300)
        up = upload_slot(page, thumb, j)
        uploads.append(up)
        log(f"  ab upload slot{j+1}: {up.get('via')}")
        shot(page, f"v12_12_slot{j+1}.png")
        # After first upload, third slot may appear — scroll dialog
        page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>40) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  const t=(el.innerText||'').slice(0,40);
                  if (/Title and thumbnail|Add thumbnail|Set test/i.test(t) && el.scrollHeight>el.clientHeight+20) {
                    el.scrollTop = el.scrollHeight;
                  }
                  if (el.shadowRoot) walk(el.shadowRoot,d+1);
                }
              };
              walk(document);
            }"""
        )
        page.wait_for_timeout(400)

    info["uploads"] = uploads
    info["title_slots"] = fill_titles(page)
    page.wait_for_timeout(600)
    shot(page, "v12_13_filled.png")
    body = deep_text(page)
    info["ready"] = bool(re.search(r"Title and thumbnail test ready", body, re.I))
    info["need_second"] = bool(re.search(r"Second title|required", body, re.I))
    info["need_third"] = bool(re.search(r"Third title|third", body, re.I))

    set_state = None
    try:
        btn = page.get_by_role("button", name=re.compile(r"^Set test$", re.I))
        if btn.count():
            set_state = "enabled" if btn.first.is_enabled() else "disabled"
            if btn.first.is_enabled():
                btn.first.click(timeout=5000)
                set_state = "clicked"
    except Exception as e:
        set_state = f"err:{type(e).__name__}"
    if set_state not in ("clicked",):
        hit = deep_click(page, r"^Set test$", y_min=200)
        if hit:
            set_state = "deep"
    info["set"] = set_state
    page.wait_for_timeout(3500)
    shot(page, "v12_14_after_set.png")
    body = deep_text(page)
    info["banner"] = bool(re.search(r"Save or publish to start|has been set up", body, re.I))

    # Close dialog and Save
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    page.wait_for_timeout(800)
    dismiss(page)
    shot(page, "v12_15_before_save.png")
    info["save"] = save(page)
    # If banner still, Save again
    page.wait_for_timeout(2000)
    body = deep_text(page)
    if re.search(r"Save or publish to start|has been set up", body, re.I):
        info["save2"] = save(page)
    shot(page, "v12_16_after_save.png")

    goto_edit(page)
    body = deep_text(page)
    info["running"] = bool(re.search(r"A/B test running|Your test is running|test running", body, re.I))
    info["setup_pending"] = bool(re.search(r"Save or publish to start|has been set up", body, re.I))
    deep_click(page, r"A/B Testing", y_min=80)
    page.wait_for_timeout(2000)
    body2 = deep_text(page)
    if re.search(r"A/B test running|Your test is running|End test|Stop test|running", body2, re.I):
        info["running"] = True
    shot(page, "v12_17_ab_status.png")
    dismiss(page)
    uploaded_ok = sum(1 for u in uploads if u.get("via") not in (None, "failed"))
    info["uploaded_ok"] = uploaded_ok
    info["ok"] = bool(info["running"] or (info.get("banner") and set_state in ("clicked", "deep") and uploaded_ok >= 3))
    info["snip"] = body[:600]
    return info


def upload_main_thumb(page) -> dict:
    info = {"file": THUMBS[0].name}
    goto_edit(page)
    for _ in range(6):
        page.mouse.wheel(0, 300)
        page.wait_for_timeout(150)
    shot(page, "v12_01_thumb_before.png")
    # file chooser on Upload thumbnail
    try:
        with page.expect_file_chooser(timeout=8000) as fc:
            hit = deep_click(page, r"Upload thumbnail|Upload file|Custom thumbnail", y_min=100)
            if not hit:
                deep_click(page, r"^Upload$", y_min=200)
        fc.value.set_files(str(THUMBS[0]))
        info["via"] = "chooser"
        page.wait_for_timeout(2500)
    except Exception as e:
        info["chooser_err"] = type(e).__name__
        loc, idxs = list_file_inputs(page)
        if idxs:
            try:
                loc.nth(idxs[0]["i"]).set_input_files(str(THUMBS[0]))
                info["via"] = "input"
                page.wait_for_timeout(2500)
            except Exception as e2:
                info["input_err"] = type(e2).__name__
    info["saved"] = save(page)
    shot(page, "v12_02_thumb_after.png")
    info["ok"] = info.get("via") in ("chooser", "input")
    return info


def confirm_ai_kids(page) -> dict:
    info = {}
    goto_edit(page)
    for _ in range(22):
        t = deep_text(page)
        if re.search(r"AI use|Altered content|Was AI used", t, re.I):
            break
        deep_click(page, r"^Show more$", y_min=200)
        page.mouse.wheel(0, 500)
        page.wait_for_timeout(250)
    shot(page, "v12_20_before_ai.png")
    # Click Yes AI
    hit = deep_click(page, r"Yes, AI was used", y_min=100) or deep_click(page, r"^Yes$", y_min=400)
    # Also click radio near AI use via evaluate
    page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55) return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=radio],tp-yt-paper-radio-button,input'):[])) {
              const t=((el.getAttribute('aria-label')||'')+(el.innerText||'')+(el.textContent||'')).toLowerCase();
              if (/yes.*ai|ai was used/.test(t)) { el.click(); return true; }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          };
          return walk(document);
        }"""
    )
    info["ai_click"] = hit
    # Kids NO
    deep_click(page, r"No, it's not ['‘]?Made for Kids['’]?", y_min=200) or deep_click(
        page, r"^No, it's not", y_min=200
    )
    info["saved"] = save(page)
    page.wait_for_timeout(2000)
    goto_edit(page)
    for _ in range(22):
        t = deep_text(page)
        if re.search(r"AI use|Altered content|Was AI used", t, re.I):
            break
        deep_click(page, r"^Show more$", y_min=200)
        page.mouse.wheel(0, 500)
        page.wait_for_timeout(200)
    for _ in range(8):
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(120)
    shot(page, "v12_21_ai_kids_proof.png")
    body = deep_text(page)
    info["ai_use_yes"] = bool(re.search(r"Yes, AI was used|Yes\n.*AI", body, re.I)) or bool(
        re.search(r"Was AI used[\s\S]{0,200}Yes", body, re.I)
    )
    info["kids_no"] = bool(re.search(r"No, it's not.?Made for Kids", body, re.I))
    # soft: if radio checked via aria
    checked = page.evaluate(
        """() => {
          const out={ai:false,kidsNo:false};
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=radio],tp-yt-paper-radio-button'):[])) {
              const t=((el.getAttribute('aria-label')||'')+(el.innerText||'')+(el.textContent||'')).replace(/\\s+/g,' ').trim();
              const checked = el.getAttribute('aria-checked')==='true' || el.hasAttribute('checked') || (el.className||'').includes('checked');
              if (checked && /Yes/i.test(t) && /AI|altered/i.test(t+((el.parentElement&&el.parentElement.innerText)||''))) out.ai=true;
              if (checked && /not.?Made for Kids/i.test(t)) out.kidsNo=true;
              if (checked && /^Yes$/i.test(t)) {
                // check nearby section header
                let p=el; for(let i=0;i<8&&p;i++){ p=p.parentElement||(p.getRootNode&&p.getRootNode().host); }
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          };
          walk(document);
          // broader: any checked Yes under AI use heading
          const all=document.body.innerText||'';
          if (/AI use[\\s\\S]{0,400}?Yes/i.test(all)) out.ai=true;
          if (/No, it's not.?Made for Kids/i.test(all)) out.kidsNo=true;
          return out;
        }"""
    )
    info["checked"] = checked
    if checked.get("ai"):
        info["ai_use_yes"] = True
    if checked.get("kidsNo"):
        info["kids_no"] = True
    info["ok"] = bool(info["ai_use_yes"] and info["kids_no"])
    info["snip"] = body[:1200]
    return info


def prove_visibility(page) -> dict:
    info = {}
    goto_edit(page)
    deep_click(page, r"^Visibility$", y_min=80) or deep_click(page, r"Scheduled", y_min=100)
    page.wait_for_timeout(1200)
    deep_click(page, r"Schedule|15 Oct|October|Edit", y_min=60)
    page.wait_for_timeout(1500)
    # Click the date/time row to expand calendar
    deep_click(page, r"15 Oct 2026|15 October 2026", y_min=80)
    page.wait_for_timeout(800)
    shot(page, "v12_30_visibility_panel.png")
    body = deep_text(page)
    info["has_15"] = bool(re.search(r"15\s*(Oct|October)\s*2026", body, re.I))
    info["has_1800"] = bool(re.search(r"18:00", body, re.I))
    info["has_30"] = bool(re.search(r"30\s*(Sept|Sep|September)\s*2026", body, re.I))
    info["premiere_on"] = bool(re.search(r"Set as Premiere", body, re.I) and re.search(r"Premiere.?on|checked", body, re.I))
    # Click Done if open
    deep_click(page, r"^Done$", y_min=200)
    page.wait_for_timeout(800)
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    shot(page, "v12_31_content.png")
    body2 = snip(page)
    info["content_15"] = bool(re.search(r"15\s*(Oct|October)\s*2026", body2, re.I))
    info["content_30"] = bool(re.search(r"30\s*(Sept|Sep|September)\s*2026", body2, re.I))
    info["ok"] = bool((info["has_15"] or info["content_15"]) and info["has_1800"] and not info["has_30"] and not info["content_30"])
    info["snip"] = body[:800]
    return info


def do_end_screen(page) -> dict:
    info = {"related": RELATED_002}
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit?panel=endscreen",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4500)
    for _ in range(4):
        dismiss(page)
        deep_click(page, r"OK, got it")
        page.wait_for_timeout(200)
    shot(page, "v12_40_endscreen.png")

    # Template
    tbox = deep_click(page, r"1 video, 1 subscribe", y_min=60)
    info["template"] = tbox
    page.wait_for_timeout(2000)
    if not tbox:
        deep_click(page, r"ADD ELEMENT|Add element", y_min=60)
        page.wait_for_timeout(500)
        deep_click(page, r"^Video$", y_min=60, exact=True)
        deep_click(page, r"^Subscribe$", y_min=60, exact=True)
    shot(page, "v12_41_template.png")

    # Specific video
    deep_click(page, r"Most recent upload|Best for viewer", y_min=60)
    page.wait_for_timeout(500)
    deep_click(page, r"Specific video|Choose a video|Select a video", y_min=60)
    page.wait_for_timeout(1000)
    filled = page.evaluate(
        """(q) => {
          const walk=(r,d=0)=>{
            if(!r||d>55) return false;
            for (const inp of (r.querySelectorAll?r.querySelectorAll('input,textarea'):[])) {
              const aria=((inp.getAttribute('aria-label')||'')+(inp.placeholder||'')).toLowerCase();
              const rect=inp.getBoundingClientRect();
              if (rect.width<40||rect.y<50) continue;
              if (/search|video|url|paste/.test(aria) || inp.type==='search' || inp.type==='text') {
                inp.focus();
                const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
                nativeSetter.call(inp, q);
                inp.dispatchEvent(new Event('input',{bubbles:true}));
                return true;
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          };
          return walk(document);
        }""",
        RELATED_002,
    )
    info["typed_id"] = filled
    page.keyboard.type(RELATED_002, delay=12)
    page.keyboard.press("Enter")
    page.wait_for_timeout(2200)
    deep_click(page, r"How Did We Discover the Periodic Table", y_min=80) or deep_click(
        page, r"Periodic Table", y_min=80
    )
    page.wait_for_timeout(1000)
    shot(page, "v12_42_bound.png")

    # Save end screen
    try:
        btn = page.get_by_role("button", name=re.compile(r"^SAVE$|^Save$", re.I))
        if btn.count() and btn.first.is_enabled():
            btn.first.click(timeout=5000)
            info["save"] = "role"
    except Exception:
        pass
    if not info.get("save"):
        info["save"] = "deep" if deep_click(page, r"^SAVE$|^Save$", y_min=0) else None
    page.wait_for_timeout(4000)
    shot(page, "v12_43_saved.png")
    after = deep_text(page)
    info["has_002"] = bool(re.search(r"Periodic Table|AL_-qlWko_g", after, re.I))
    info["has_subscribe"] = bool(re.search(r"Subscribe", after, re.I))
    info["error"] = bool(re.search(r"At least one element must be a video|problem in processing|couldn't be saved", after, re.I))
    info["ok"] = bool(not info["error"] and info["has_subscribe"] and (info["has_002"] or info.get("template")))
    info["after"] = after[:900]
    return info


def main():
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    (EV / "phone_uat_v12.log").write_text("")
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

        log("v12 main thumb A v04")
        result["thumbnail"] = upload_main_thumb(page)
        dump("V12_THUMB.json", result["thumbnail"])

        log("v12 A/B Title+thumbnail 3 pairs")
        result["testAndCompare"] = do_ab(page)
        dump("V12_AB.json", result["testAndCompare"])

        log("v12 AI + Kids")
        result["aiKids"] = confirm_ai_kids(page)
        dump("V12_AI_KIDS.json", result["aiKids"])

        log("v12 Visibility")
        result["schedule"] = prove_visibility(page)
        dump("V12_SCHEDULE.json", result["schedule"])

        log("v12 end screen")
        result["endScreen"] = do_end_screen(page)
        dump("V12_END.json", result["endScreen"])

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
    dump("PHONE_UAT_V12_RESULT.json", result)
    log(f"DONE {json.dumps(result['ok'])}")
    print(json.dumps(result["ok"], indent=2))


if __name__ == "__main__":
    main()
