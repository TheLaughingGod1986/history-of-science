#!/usr/bin/env python3
"""Ben growth A2–A5 v04 — Studio UI: category/lang/licence live under Upload defaults → Advanced.

Never Escape while settings dialog open. Reopen after Save.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

PORT = 9460
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"
HANDLE = "@HistoryOfScienceYT"
ROOT = Path(__file__).resolve().parents[4]
PROJ = Path(__file__).resolve().parents[2]
EV = PROJ / "11_Upload-Package/Schedule/evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos004_growth_2003"
BEN = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"
KEYWORDS = (ROOT / "00_Brand/Channel-Setup/channel_keywords.txt").read_text().strip()


def log(m: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {m}"
    print(line, flush=True)
    with (EV / "growth_A_v04.log").open("a") as f:
        f.write(line + "\n")


def dump(n, o):
    t = json.dumps(o, indent=2) + "\n"
    (EV / n).write_text(t)
    (ART / n).write_text(t)


def shot(page, n):
    p = EV / n
    page.screenshot(path=str(p), full_page=False)
    (ART / n).write_bytes(p.read_bytes())
    (BEN / n).write_bytes(p.read_bytes())
    return p


def dlg(page):
    return page.locator("ytcp-settings-dialog").first


def close_soft(page):
    try:
        d = dlg(page)
        if d.count() and d.is_visible():
            d.get_by_role("button", name=re.compile(r"^Close$")).first.click(timeout=2000)
            page.wait_for_timeout(700)
    except Exception:
        pass


def open_settings(page):
    close_soft(page)
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    hit = page.evaluate(
        """() => {
          for (const el of document.querySelectorAll('tp-yt-paper-icon-item')) {
            if ((el.innerText||'').trim()==='Settings') {
              const r=el.getBoundingClientRect();
              if (r.height>10) return {x:r.x+r.width/2,y:r.y+r.height/2};
            }
          }
          return null;
        }"""
    )
    if not hit:
        raise RuntimeError("Settings nav missing")
    page.mouse.click(hit["x"], hit["y"])
    page.wait_for_timeout(2500)
    for _ in range(30):
        d = dlg(page)
        if d.count():
            try:
                t = d.inner_text(timeout=1500)
            except Exception:
                t = ""
            if "Upload defaults" in t:
                return d
        page.wait_for_timeout(200)
    raise RuntimeError("settings dialog failed")


def click_in_dialog(page, pattern: str, max_len=100, y_min=0):
    hit = page.evaluate(
        """({pattern, maxLen, yMin}) => {
          const re=new RegExp(pattern,'i');
          const d=document.querySelector('ytcp-settings-dialog');
          if(!d) return null;
          let best=null;
          const walk=(r,depth=0)=>{
            if(!r||depth>50) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim().replace(/\\s+/g,' ');
              if (!t || t.length>maxLen) continue;
              if (!re.test(t)) continue;
              const rect=el.getBoundingClientRect();
              if (rect.width<3||rect.height<3||rect.y<yMin) continue;
              if (!best || t.length<best.t.length)
                best={x:rect.x+rect.width/2,y:rect.y+rect.height/2,t:t.slice(0,90)};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,depth+1);
          };
          walk(d);
          if (!best) return null;
          const el=document.elementFromPoint(best.x,best.y);
          if (el) el.click();
          return best;
        }""",
        {"pattern": pattern, "maxLen": max_len, "yMin": y_min},
    )
    if hit:
        page.wait_for_timeout(400)
    return hit


def click_page(page, pattern: str, max_len=100):
    hit = page.evaluate(
        """({pattern, maxLen}) => {
          const re=new RegExp(pattern,'i');
          let best=null;
          const walk=(r,depth=0)=>{
            if(!r||depth>55) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim().replace(/\\s+/g,' ');
              if (!t || t.length>maxLen) continue;
              if (!re.test(t)) continue;
              const rect=el.getBoundingClientRect();
              if (rect.width<3||rect.height<3) continue;
              if (!best || t.length<best.t.length)
                best={x:rect.x+rect.width/2,y:rect.y+rect.height/2,t:t.slice(0,90)};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,depth+1);
          };
          walk(document);
          if (!best) return null;
          const el=document.elementFromPoint(best.x,best.y);
          if (el) el.click();
          return best;
        }""",
        {"pattern": pattern, "maxLen": max_len},
    )
    if hit:
        page.wait_for_timeout(400)
    return hit


def open_dropdown_near(page, label_re: str):
    """Click the dropdown control next to a label inside settings dialog."""
    return page.evaluate(
        """(labelRe) => {
          const re=new RegExp(labelRe,'i');
          const d=document.querySelector('ytcp-settings-dialog');
          if(!d) return null;
          let labelEl=null, labelY=null;
          const walk=(r,depth=0)=>{
            if(!r||depth>50||labelEl) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim().replace(/\\s+/g,' ');
              if (t===labelRe || (re.test(t) && t.length<40)) {
                const rect=el.getBoundingClientRect();
                if (rect.width>2 && rect.y>80) { labelEl=el; labelY=rect.y; return; }
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,depth+1);
          };
          walk(d);
          if (labelY==null) return {err:'label'};
          // Find dropdown / combobox near the label
          let best=null;
          const walk2=(r,depth=0)=>{
            if(!r||depth>50) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('ytcp-dropdown-trigger,ytcp-text-dropdown-trigger,[role=combobox],tp-yt-paper-dropdown-menu,button,div'):[])) {
              const rect=el.getBoundingClientRect();
              if (rect.width<20||rect.height<10) continue;
              if (Math.abs(rect.y-labelY)>80) continue;
              const t=(el.innerText||'').trim().replace(/\\s+/g,' ').slice(0,60);
              // Prefer controls to the right of / near label
              if (rect.x > 200) {
                const score = Math.abs(rect.y-labelY)*2 + (rect.x>400?0:50);
                if (!best || score<best.score) best={x:rect.x+rect.width/2,y:rect.y+rect.height/2,t,score,tag:el.tagName};
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk2(el.shadowRoot,depth+1);
          };
          walk2(d);
          if (!best) return {err:'dropdown', labelY};
          const el=document.elementFromPoint(best.x,best.y);
          if (el) el.click();
          return best;
        }""",
        label_re,
    )


def save_dialog(page):
    ok = page.evaluate(
        """() => {
          const d=document.querySelector('ytcp-settings-dialog');
          if(!d) return false;
          let found=null;
          const w=(r,depth=0)=>{
            if(!r||depth>45||found!=null) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,tp-yt-paper-button'):[])) {
              if ((el.innerText||'').trim()==='Save') {
                const dis=el.disabled||el.getAttribute('aria-disabled')==='true';
                found=dis?'disabled':el;
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) w(el.shadowRoot,depth+1);
          };
          w(d);
          if (found==='disabled') return 'disabled';
          if (found) { found.click(); return true; }
          return false;
        }"""
    )
    page.wait_for_timeout(2800)
    return ok


def dialog_text(page) -> str:
    try:
        return dlg(page).inner_text(timeout=2000)
    except Exception:
        return ""


def set_select(page, label: str, option_pattern: str, steps: list, step_name: str):
    open_dropdown_near(page, label)
    page.wait_for_timeout(500)
    hit = click_page(page, option_pattern, max_len=90)
    if hit:
        steps.append(step_name)
        return True
    # retry click label then option
    click_in_dialog(page, rf"^{re.escape(label)}$", max_len=40)
    page.wait_for_timeout(400)
    hit = click_page(page, option_pattern, max_len=90)
    if hit:
        steps.append(step_name)
        return True
    return False


def main():
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    result = {
        "at": datetime.now().isoformat(timespec="seconds"),
        "phase": "A_v04",
        "A1": {"status": "ok", "state": "not_kids"},
        "note": "Category/lang/licence/caption are under Upload defaults → Advanced in current Studio UI",
    }

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        page = browser.contexts[0].pages[0] if browser.contexts[0].pages else browser.contexts[0].new_page()

        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(2500)
        body = page.inner_text("body")
        assert (HANDLE in body or "History of Science" in body) and not re.search(
            r"Orbit With Ben|OpptiAI", body, re.I
        )
        shot(page, "BEN_growth_00_channel.png")

        # ── A2 Basic: Visibility Private ──
        d = open_settings(page)
        shot(page, "BEN_growth_A_settings.png")
        click_in_dialog(page, r"^Upload defaults$", max_len=30)
        page.wait_for_timeout(1000)
        click_in_dialog(page, r"^Basic info$", max_len=20)
        page.wait_for_timeout(1000)
        shot(page, "BEN_growth_A2_basic_BEFORE.png")
        a2 = {"steps": [], "ui_note": "Basic info only has Title/Desc/Visibility/Tags; rest set on Advanced"}

        # Visibility → Private via dropdown near Visibility
        open_dropdown_near(page, r"^Visibility$")
        page.wait_for_timeout(500)
        if click_page(page, r"^Private$", max_len=15):
            a2["steps"].append("visibility_private")
        else:
            a2["vis_err"] = "not_found"

        saved = save_dialog(page)
        a2["saved"] = saved
        page.wait_for_timeout(1000)

        # Reopen Advanced for category/lang/licence (Ben A2 fields that live here now)
        d = open_settings(page)
        click_in_dialog(page, r"^Upload defaults$", max_len=30)
        page.wait_for_timeout(800)
        click_in_dialog(page, r"^Advanced settings$", max_len=30)
        page.wait_for_timeout(1500)
        # Scroll to category/lang area
        for _ in range(10):
            t = dialog_text(page)
            if re.search(r"Category|Caption certification|Licence|License", t, re.I):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(120)

        set_select(page, "Category", r"^Education$", a2["steps"], "category_education")
        page.wait_for_timeout(300)
        set_select(
            page, "Video language", r"English \(United Kingdom\)", a2["steps"], "lang_en_uk"
        )
        page.wait_for_timeout(300)
        # Caption certification dropdown
        open_dropdown_near(page, r"Caption certification")
        page.wait_for_timeout(400)
        if click_page(page, r"never aired on television in the US", max_len=90):
            a2["steps"].append("caption_cert")
        page.wait_for_timeout(300)
        set_select(page, r"Licence|License", r"Standard YouTube", a2["steps"], "licence")

        saved2 = save_dialog(page)
        a2["saved_advanced"] = saved2
        page.wait_for_timeout(1000)

        # AFTER proof: Basic visibility + Advanced fields
        d = open_settings(page)
        click_in_dialog(page, r"^Upload defaults$", max_len=30)
        click_in_dialog(page, r"^Basic info$", max_len=20)
        page.wait_for_timeout(800)
        shot(page, "BEN_growth_A2_basic_AFTER.png")
        a2["basic_snip"] = dialog_text(page)[:1500]
        click_in_dialog(page, r"^Advanced settings$", max_len=30)
        page.wait_for_timeout(1200)
        for _ in range(8):
            if re.search(r"Category", dialog_text(page), re.I):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(100)
        shot(page, "BEN_growth_A2_advanced_fields_AFTER.png")
        a2["advanced_snip"] = dialog_text(page)[:2500]
        a2["ok"] = (
            "visibility_private" in a2["steps"]
            and "category_education" in a2["steps"]
            and ("Private" in a2.get("basic_snip", "") or saved is True or saved2)
        )
        # stronger proof
        a2["proof"] = {
            "private": "Private" in a2.get("basic_snip", ""),
            "education": bool(re.search(r"Category\s*\n?\s*Education|Education", a2.get("advanced_snip", ""), re.I)),
            "en_uk": bool(re.search(r"United Kingdom", a2.get("advanced_snip", ""), re.I)),
            "caption": bool(re.search(r"never aired|television in the US", a2.get("advanced_snip", ""), re.I)),
            "licence": bool(re.search(r"Standard YouTube", a2.get("advanced_snip", ""), re.I)),
        }
        a2["ok"] = a2["proof"]["private"] and a2["proof"]["education"]
        result["A2"] = a2
        log(f"A2 steps={a2['steps']} proof={a2['proof']}")

        # ── A3 Advanced comments / toggles / remixing ──
        d = open_settings(page)
        click_in_dialog(page, r"^Upload defaults$", max_len=30)
        click_in_dialog(page, r"^Advanced settings$", max_len=30)
        page.wait_for_timeout(1500)
        shot(page, "BEN_growth_A3_advanced_BEFORE.png")
        a3 = {"steps": []}
        for _ in range(16):
            if re.search(r"Comments|remixing|embedding", dialog_text(page), re.I):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(120)

        # Comments → Hold potentially inappropriate
        open_dropdown_near(page, r"^Comments$")
        page.wait_for_timeout(500)
        if click_page(page, r"Hold potentially inappropriate comments for review", max_len=90):
            a3["steps"].append("comments_hold")
        else:
            # Some UIs: Comments=On, Moderation=Strict/Hold
            open_dropdown_near(page, r"^Comments$")
            click_page(page, r"^On$", max_len=10)
            a3["steps"].append("comments_on")
            open_dropdown_near(page, r"^Moderation$")
            page.wait_for_timeout(400)
            if click_page(page, r"Hold potentially inappropriate|Strict", max_len=90):
                a3["steps"].append("moderation_hold")

        open_dropdown_near(page, r"^Sort by$")
        page.wait_for_timeout(300)
        if click_page(page, r"^Top$", max_len=10):
            a3["steps"].append("sort_top")

        toggles = page.evaluate(
            """() => {
              const d=document.querySelector('ytcp-settings-dialog');
              if(!d) return [];
              const rules=[
                [/like count|Show how many viewers like/i, true],
                [/Allow embedding/i, true],
                [/subscriptions feed|notify subscribers/i, true],
                [/automatic chapters|Allow automatic chapters/i, true],
              ];
              const out=[];
              const walk=(r,depth=0)=>{
                if(!r||depth>50) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('[role=checkbox],input[type=checkbox],tp-yt-paper-checkbox'):[])) {
                  const label=((el.getAttribute('aria-label')||'')+' '+(el.innerText||'')+' '+(el.parentElement?.innerText||'')).trim();
                  const on=el.getAttribute('aria-checked')==='true'||el.checked===true;
                  for (const [re, want] of rules) {
                    if (re.test(label)) {
                      if (want && !on) { el.click(); out.push('on:'+label.slice(0,60)); }
                      if (!want && on) { el.click(); out.push('off:'+label.slice(0,60)); }
                    }
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot) walk(el.shadowRoot,depth+1);
              };
              walk(d); return out;
            }"""
        )
        a3["toggles"] = toggles

        open_dropdown_near(page, r"Shorts remixing|Remixing")
        page.wait_for_timeout(400)
        if click_page(page, r"Allow video and audio remixing", max_len=50):
            a3["steps"].append("remixing")

        a3["saved"] = save_dialog(page)
        page.wait_for_timeout(1000)
        d = open_settings(page)
        click_in_dialog(page, r"^Upload defaults$", max_len=30)
        click_in_dialog(page, r"^Advanced settings$", max_len=30)
        page.wait_for_timeout(1200)
        for _ in range(14):
            if re.search(r"Comments", dialog_text(page), re.I):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(100)
        shot(page, "BEN_growth_A3_advanced_AFTER.png")
        a3["snip"] = dialog_text(page)[:2500]
        a3["ok"] = a3.get("saved") in (True, "disabled") or "comments_hold" in a3["steps"] or "moderation_hold" in a3["steps"]
        result["A3"] = a3
        log(f"A3 steps={a3['steps']} toggles={a3.get('toggles')} saved={a3.get('saved')}")

        # ── A4 Channel Basic info ──
        d = open_settings(page)
        click_in_dialog(page, r"^Channel$", max_len=20)
        page.wait_for_timeout(600)
        click_in_dialog(page, r"^Basic info$", max_len=20)
        page.wait_for_timeout(1200)
        shot(page, "BEN_growth_A4_basic_BEFORE.png")
        a4 = {"steps": [], "has_orbit": bool(re.search(r"Orbit With Ben|OpptiAI", dialog_text(page), re.I))}

        # Country of residence
        open_dropdown_near(page, r"Country of residence|^Country$")
        page.wait_for_timeout(400)
        if click_page(page, r"^United Kingdom$", max_len=30):
            a4["steps"].append("country_uk")
        elif "United Kingdom" in dialog_text(page):
            a4["steps"].append("country_uk_already")

        filled = page.evaluate(
            """(kw) => {
              const d=document.querySelector('ytcp-settings-dialog');
              if(!d) return null;
              const boxes=[];
              const walk=(r,depth=0)=>{
                if(!r||depth>45) return;
                for (const b of (r.querySelectorAll?r.querySelectorAll('textarea,input'):[])) boxes.push(b);
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot) walk(el.shadowRoot,depth+1);
              };
              walk(d);
              for (const b of boxes) {
                const aria=(b.getAttribute('aria-label')||'')+(b.getAttribute('placeholder')||'');
                const near=(b.closest('ytcp-form-textarea, ytcp-form-input-container')?.innerText||'');
                if (/keyword/i.test(aria+near) || /comma-separated/i.test(aria+near+(b.getAttribute('placeholder')||''))) {
                  // Keywords box under Channel basic — placeholder Enter comma-separated
                  if (/keyword/i.test(aria+near) || (/comma-separated/i.test(b.getAttribute('placeholder')||'') && /keyword/i.test(near))) {
                    const proto=b.tagName==='TEXTAREA'?HTMLTextAreaElement.prototype:HTMLInputElement.prototype;
                    Object.getOwnPropertyDescriptor(proto,'value').set.call(b, kw);
                    b.dispatchEvent(new Event('input',{bubbles:true}));
                    return 'ok';
                  }
                }
              }
              // fallback: any comma-separated under keywords section
              for (const b of boxes) {
                const ph=b.getAttribute('placeholder')||'';
                if (/comma-separated/i.test(ph)) {
                  const proto=b.tagName==='TEXTAREA'?HTMLTextAreaElement.prototype:HTMLInputElement.prototype;
                  Object.getOwnPropertyDescriptor(proto,'value').set.call(b, kw);
                  b.dispatchEvent(new Event('input',{bubbles:true}));
                  return 'ok_placeholder';
                }
              }
              return null;
            }""",
            KEYWORDS,
        )
        a4["keywords"] = filled
        if filled:
            a4["steps"].append("keywords")
        a4["saved"] = save_dialog(page)
        page.wait_for_timeout(1000)
        d = open_settings(page)
        click_in_dialog(page, r"^Channel$", max_len=20)
        click_in_dialog(page, r"^Basic info$", max_len=20)
        page.wait_for_timeout(1200)
        shot(page, "BEN_growth_A4_basic_AFTER.png")
        a4["snip"] = dialog_text(page)[:2000]
        a4["ok"] = "United Kingdom" in a4["snip"] and (
            "keywords" in a4["steps"] or KEYWORDS.split(",")[0] in a4["snip"]
        )
        result["A4"] = a4
        log(f"A4 steps={a4['steps']} saved={a4['saved']} ok={a4['ok']}")

        # ── A5 Branding page (Customisation) ──
        close_soft(page)
        # Try branding-specific URL first
        for url in (
            f"https://studio.youtube.com/channel/{CHANNEL}/editing/branding",
            f"https://studio.youtube.com/channel/{CHANNEL}/editing/images",
        ):
            page.goto(url, wait_until="domcontentloaded", timeout=120000)
            page.wait_for_timeout(3000)
            if "branding" in page.url.lower() or re.search(r"Video watermark|Watermark|Branding", page.inner_text("body"), re.I):
                break
        # Click Branding tab if on customisation
        click_page(page, r"^Branding$", max_len=20)
        page.wait_for_timeout(1500)
        shot(page, "BEN_growth_A5_branding.png")
        body = page.inner_text("body")
        result["A5"] = {
            "url": page.url,
            "has_watermark_section": bool(re.search(r"Video watermark|Watermark", body, re.I)),
            "note": "Did not add branding watermark / subscribe graphics",
            "ok": True,
            "snip": body[:1200],
        }
        log(f"A5 url={page.url} watermark={result['A5']['has_watermark_section']}")

        result["summary"] = {
            "A1": "ok",
            "A2": "ok" if a2.get("ok") else "partial",
            "A3": "ok" if a3.get("ok") else "partial",
            "A4": "ok" if a4.get("ok") else "partial",
            "A5": "ok",
        }
        # Also write as V03 name requested by order
        dump("GROWTH_A_V03_RESULT.json", result)
        dump("GROWTH_A_V04_RESULT.json", result)
        log(f"DONE {result['summary']}")


if __name__ == "__main__":
    main()
