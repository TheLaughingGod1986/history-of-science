#!/usr/bin/env python3
"""Ben 20:03 Phase A — Channel Settings (dialog-aware, no Escape while open)."""
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
    with (EV / "growth_A_v02.log").open("a") as f:
        f.write(line + "\n")


def dump(n, o):
    t = json.dumps(o, indent=2) + "\n"
    (EV / n).write_text(t)
    (ART / n).write_text(t)


def shot(page, n, ben=False):
    p = EV / n
    page.screenshot(path=str(p), full_page=False)
    (ART / n).write_bytes(p.read_bytes())
    if ben or n.startswith("BEN_"):
        (BEN / n).write_bytes(p.read_bytes())
    return p


def dlg(page):
    return page.locator("ytcp-settings-dialog, ytcp-channel-settings-dialog").first


def open_settings(page):
    # Close any leftover dialog first
    try:
        if dlg(page).count() and dlg(page).is_visible():
            dlg(page).get_by_role("button", name=re.compile(r"^Close$")).first.click(timeout=1500)
            page.wait_for_timeout(600)
    except Exception:
        pass
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}",
        wait_until="commit",
        timeout=90000,
    )
    page.wait_for_timeout(3500)
    # Prefer mouse click on Settings nav item (most reliable)
    hit = page.evaluate(
        """() => {
          const items=[...document.querySelectorAll('tp-yt-paper-icon-item, ytcp-ve')];
          for (const el of items) {
            const t=(el.innerText||'').trim();
            if (t==='Settings') {
              const r=el.getBoundingClientRect();
              if (r.height>10) return {x:r.x+r.width/2,y:r.y+r.height/2};
            }
          }
          return null;
        }"""
    )
    if hit:
        page.mouse.click(hit["x"], hit["y"])
    else:
        page.get_by_text(re.compile(r"^Settings$"), exact=True).last.click(timeout=5000)
    page.wait_for_timeout(2500)
    # Wait until settings dialog content is present
    for _ in range(20):
        if page.locator("ytcp-settings-dialog").count() and "Upload defaults" in (
            page.locator("ytcp-settings-dialog").inner_text()
            if page.locator("ytcp-settings-dialog").count()
            else ""
        ):
            break
        page.wait_for_timeout(200)
    d = dlg(page)
    if not d.count():
        raise RuntimeError("settings dialog not open")
    try:
        txt = d.inner_text(timeout=3000)
    except Exception:
        txt = ""
    if "Upload defaults" not in txt and "General" not in txt:
        raise RuntimeError(f"settings dialog empty: {txt[:200]!r}")
    return d


def nav(d, label: str):
    d.get_by_text(re.compile(rf"^{re.escape(label)}$"), exact=False).first.click(timeout=4000)
    page_wait = d.page
    page_wait.wait_for_timeout(1200)


def click_text(d, pattern: str, timeout=3000):
    d.get_by_text(re.compile(pattern, re.I)).first.click(timeout=timeout)


def save_dialog(d) -> bool:
    try:
        btn = d.get_by_role("button", name=re.compile(r"^Save$")).first
        if btn.is_enabled():
            btn.click(timeout=3000)
            d.page.wait_for_timeout(2500)
            return True
        return False
    except Exception:
        return False


def main():
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    result = {"at": datetime.now().isoformat(timespec="seconds"), "phase": "A_v02"}

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        page = browser.contexts[0].pages[0] if browser.contexts[0].pages else browser.contexts[0].new_page()

        # Channel check
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
            wait_until="commit",
            timeout=90000,
        )
        page.wait_for_timeout(3000)
        t = page.inner_text("body")
        assert (HANDLE in t or "History of Science" in t) and not re.search(
            r"Orbit With Ben|OpptiAI", t, re.I
        )
        shot(page, "BEN_growth_00_channel.png", ben=True)

        # ── A1 Audience ──
        d = open_settings(page)
        shot(page, "BEN_growth_A_settings.png", ben=True)
        nav(d, "Channel")
        page.wait_for_timeout(800)
        # Advanced settings sub-tab
        try:
            d.get_by_text(re.compile(r"^Advanced settings$", re.I)).first.click(timeout=3000)
        except Exception:
            d.get_by_text(re.compile(r"Advanced", re.I)).first.click(timeout=3000)
        page.wait_for_timeout(1500)
        # scroll audience into view inside dialog
        for _ in range(8):
            txt = d.inner_text()
            if re.search(r"Made for Kids|Audience", txt, re.I):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(150)
        shot(page, "BEN_growth_A1_audience_BEFORE.png", ben=True)
        before_txt = d.inner_text()
        before = {
            "not_kids_selected": bool(
                re.search(r"No, set this channel as not Made for Kids", before_txt, re.I)
            ),
            "yes_selected_guess": bool(
                re.search(r"Yes, set this channel as Made for Kids", before_txt, re.I)
            ),
            "snip": before_txt[:2000],
        }
        # Check which radio is checked via aria
        radios = page.evaluate(
            """() => {
              const d=document.querySelector('ytcp-settings-dialog, ytcp-channel-settings-dialog');
              if(!d) return [];
              const out=[];
              const walk=(r,depth=0)=>{
                if(!r||depth>40) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('[role=radio],input[type=radio],tp-yt-paper-radio-button'):[])) {
                  const t=((el.getAttribute('aria-label')||'')+' '+(el.innerText||'')).trim();
                  if (/kids|Audience|Yes|No/i.test(t)) {
                    out.push({t:t.slice(0,120), checked: el.getAttribute('aria-checked')==='true' || el.checked===true});
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,depth+1);
              }; walk(d); return out;
            }"""
        )
        before["radios"] = radios
        checked = [r for r in radios if r.get("checked")]
        before["checked"] = checked
        before["state"] = "unknown"
        for r in checked:
            if re.search(r"No.*not Made for Kids|not made for kids", r["t"], re.I):
                before["state"] = "not_kids"
            elif re.search(r"Yes.*Made for Kids", r["t"], re.I) and "not" not in r["t"].lower():
                before["state"] = "kids"
        result["A1_before"] = before
        log(f"A1 before state={before['state']} radios={checked}")

        # Click No
        try:
            d.get_by_text(
                re.compile(r"No, set this channel as not Made for Kids", re.I)
            ).first.click(timeout=4000)
            result["A1_clicked"] = True
        except Exception as e:
            result["A1_click_err"] = type(e).__name__
            # JS fallback
            result["A1_clicked"] = page.evaluate(
                """() => {
                  const d=document.querySelector('ytcp-settings-dialog');
                  const walk=(r,depth=0)=>{
                    if(!r||depth>40) return false;
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                      const t=(el.innerText||'').trim();
                      if (/No, set this channel as not Made for Kids/i.test(t) && t.length<80) {
                        el.click(); return true;
                      }
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot){ if(walk(el.shadowRoot,depth+1)) return true; }
                    return false;
                  }; return walk(d);
                }"""
            )
        page.wait_for_timeout(500)
        result["A1_saved"] = save_dialog(d)
        page.wait_for_timeout(1500)

        # Reopen for after proof
        try:
            d.get_by_role("button", name=re.compile(r"^Close$")).first.click(timeout=2000)
        except Exception:
            pass
        page.wait_for_timeout(800)
        d = open_settings(page)
        nav(d, "Channel")
        try:
            d.get_by_text(re.compile(r"^Advanced settings$", re.I)).first.click(timeout=3000)
        except Exception:
            d.get_by_text(re.compile(r"Advanced", re.I)).first.click(timeout=3000)
        page.wait_for_timeout(1500)
        for _ in range(8):
            if re.search(r"Made for Kids|Audience", d.inner_text(), re.I):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(120)
        shot(page, "BEN_growth_A1_audience_AFTER.png", ben=True)
        after_txt = d.inner_text()
        radios2 = page.evaluate(
            """() => {
              const d=document.querySelector('ytcp-settings-dialog, ytcp-channel-settings-dialog');
              const out=[];
              const walk=(r,depth=0)=>{
                if(!r||depth>40) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('[role=radio],input[type=radio],tp-yt-paper-radio-button'):[])) {
                  const t=((el.getAttribute('aria-label')||'')+' '+(el.innerText||'')).trim();
                  if (/kids|Yes|No/i.test(t)) out.push({t:t.slice(0,120), checked: el.getAttribute('aria-checked')==='true' || el.checked===true});
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,depth+1);
              }; walk(d); return out;
            }"""
        )
        after = {"radios": radios2, "snip": after_txt[:2000]}
        after["state"] = "unknown"
        for r in radios2:
            if r.get("checked") and re.search(r"No.*not Made for Kids", r["t"], re.I):
                after["state"] = "not_kids"
            if r.get("checked") and re.search(r"Yes.*Made for Kids", r["t"], re.I) and "not" not in r["t"].lower():
                after["state"] = "kids"
        result["A1_after"] = after
        result["A1_ok"] = after["state"] == "not_kids"
        log(f"A1 after={after['state']} ok={result['A1_ok']}")

        # ── A2 Upload defaults Basic ──
        nav(d, "Upload defaults")
        page.wait_for_timeout(1000)
        try:
            d.get_by_text(re.compile(r"^Basic info$", re.I)).first.click(timeout=2000)
        except Exception:
            pass
        page.wait_for_timeout(1000)
        shot(page, "BEN_growth_A2_basic_BEFORE.png", ben=True)
        a2 = {"steps": []}
        # Category
        try:
            # Find category dropdown
            d.get_by_text(re.compile(r"^Category$", re.I)).first.click(timeout=2000)
            page.wait_for_timeout(400)
            page.get_by_text(re.compile(r"^Education$", re.I)).first.click(timeout=2000)
            a2["steps"].append("category_education")
        except Exception as e:
            a2["category_err"] = type(e).__name__
        # Language
        try:
            d.get_by_text(re.compile(r"Video language|Language", re.I)).first.click(timeout=2000)
            page.wait_for_timeout(400)
            page.get_by_text(re.compile(r"English \(United Kingdom\)", re.I)).first.click(timeout=3000)
            a2["steps"].append("lang_en_uk")
        except Exception as e:
            a2["lang_err"] = type(e).__name__
        # Caption certification
        try:
            d.get_by_text(re.compile(r"Caption certification", re.I)).first.click(timeout=2000)
            page.wait_for_timeout(400)
            page.get_by_text(
                re.compile(r"never aired on television in the US", re.I)
            ).first.click(timeout=3000)
            a2["steps"].append("caption_cert")
        except Exception as e:
            a2["cert_err"] = type(e).__name__
        # Licence
        try:
            d.get_by_text(re.compile(r"Licence|License", re.I)).first.click(timeout=2000)
            page.wait_for_timeout(400)
            page.get_by_text(re.compile(r"Standard YouTube", re.I)).first.click(timeout=2000)
            a2["steps"].append("licence")
        except Exception as e:
            a2["licence_err"] = type(e).__name__
        # Visibility Private — look for visibility control
        try:
            # Often a dropdown showing Public/Private/Unlisted
            for label in (r"^Public$", r"^Unlisted$", r"^Private$", r"^Visibility$"):
                try:
                    d.get_by_text(re.compile(label, re.I)).first.click(timeout=1200)
                    page.wait_for_timeout(300)
                    break
                except Exception:
                    continue
            page.get_by_text(re.compile(r"^Private$", re.I)).first.click(timeout=2000)
            a2["steps"].append("visibility_private")
        except Exception as e:
            a2["vis_err"] = type(e).__name__
        a2["saved"] = save_dialog(d)
        page.wait_for_timeout(1000)
        shot(page, "BEN_growth_A2_basic_AFTER.png", ben=True)
        a2["snip"] = d.inner_text()[:2000]
        result["A2"] = a2
        log(f"A2 {a2}")

        # ── A3 Upload defaults Advanced ──
        try:
            d.get_by_text(re.compile(r"^Advanced settings$", re.I)).first.click(timeout=3000)
        except Exception:
            # may need to re-nav Upload defaults
            nav(d, "Upload defaults")
            d.get_by_text(re.compile(r"Advanced", re.I)).first.click(timeout=3000)
        page.wait_for_timeout(1500)
        shot(page, "BEN_growth_A3_advanced_BEFORE.png", ben=True)
        a3 = {"steps": []}
        # Scroll
        for _ in range(12):
            if re.search(r"Comments|embedding|remixing", d.inner_text(), re.I):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(120)

        # Comments — open and set Hold potentially inappropriate / On
        try:
            # Click the Comments value dropdown
            page.evaluate(
                """() => {
                  const d=document.querySelector('ytcp-settings-dialog');
                  const walk=(r,depth=0)=>{
                    if(!r||depth>45) return null;
                    let commentsEl=null;
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                      if ((el.innerText||'').trim()==='Comments') { commentsEl=el; break; }
                    }
                    if (commentsEl) {
                      let p=commentsEl.parentElement;
                      for (let i=0;i<8&&p;i++) {
                        const btn=p.querySelector('button,[role=button],ytcp-dropdown-trigger,tp-yt-paper-button');
                        if (btn) { btn.click(); return 'btn'; }
                        p=p.parentElement;
                      }
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot){ const x=walk(el.shadowRoot,depth+1); if(x) return x; }
                    return null;
                  }; return walk(d);
                }"""
            )
            page.wait_for_timeout(600)
            # Prefer Hold potentially inappropriate
            try:
                page.get_by_text(
                    re.compile(r"Hold potentially inappropriate comments for review", re.I)
                ).first.click(timeout=2000)
                a3["steps"].append("comments_hold")
            except Exception:
                try:
                    page.get_by_text(re.compile(r"^On$", re.I)).first.click(timeout=1500)
                    a3["steps"].append("comments_on")
                except Exception as e:
                    a3["comments_err"] = type(e).__name__
        except Exception as e:
            a3["comments_err2"] = type(e).__name__

        # Sort Top
        try:
            page.evaluate(
                """() => {
                  const d=document.querySelector('ytcp-settings-dialog');
                  const walk=(r,depth=0)=>{
                    if(!r||depth>45) return false;
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                      if (/^Sort by$/i.test((el.innerText||'').trim())) {
                        let p=el.parentElement;
                        for(let i=0;i<8&&p;i++){ const b=p.querySelector('button,[role=button],ytcp-dropdown-trigger'); if(b){b.click();return true;} p=p.parentElement; }
                      }
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) if(walk(el.shadowRoot,depth+1)) return true;
                    return false;
                  }; return walk(d);
                }"""
            )
            page.wait_for_timeout(400)
            page.get_by_text(re.compile(r"^Top$", re.I)).first.click(timeout=2000)
            a3["steps"].append("sort_top")
        except Exception as e:
            a3["sort_err"] = type(e).__name__

        # Checkboxes
        toggles = page.evaluate(
            """() => {
              const d=document.querySelector('ytcp-settings-dialog');
              const rules=[
                [/like count|Show how many viewers like/i, true],
                [/Allow embedding/i, true],
                [/subscriptions feed|notify subscribers/i, true],
                [/automatic chapters/i, true],
              ];
              const out=[];
              const walk=(r,depth=0)=>{
                if(!r||depth>45) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('[role=checkbox],input[type=checkbox],tp-yt-paper-checkbox'):[])) {
                  const label=((el.getAttribute('aria-label')||'')+' '+(el.innerText||'')+' '+(el.parentElement?.innerText||'')).trim();
                  const on=el.getAttribute('aria-checked')==='true'||el.checked===true;
                  for (const [re, want] of rules) {
                    if (re.test(label)) {
                      if (want && !on) { el.click(); out.push('on:'+label.slice(0,50)); }
                      if (!want && on) { el.click(); out.push('off:'+label.slice(0,50)); }
                    }
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,depth+1);
              }; walk(d); return out;
            }"""
        )
        a3["toggles"] = toggles

        # Shorts remixing
        try:
            page.evaluate(
                """() => {
                  const d=document.querySelector('ytcp-settings-dialog');
                  const walk=(r,depth=0)=>{
                    if(!r||depth>45) return false;
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                      const t=(el.innerText||'').trim();
                      if (/Shorts remixing|Remixing/i.test(t) && t.length<40) {
                        let p=el.parentElement;
                        for(let i=0;i<8&&p;i++){ const b=p.querySelector('button,[role=button],ytcp-dropdown-trigger'); if(b){b.click();return true;} p=p.parentElement; }
                      }
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) if(walk(el.shadowRoot,depth+1)) return true;
                    return false;
                  }; return walk(d);
                }"""
            )
            page.wait_for_timeout(500)
            page.get_by_text(re.compile(r"Allow video and audio remixing", re.I)).first.click(
                timeout=2500
            )
            a3["steps"].append("remixing")
        except Exception as e:
            a3["remix_err"] = type(e).__name__

        a3["saved"] = save_dialog(d)
        page.wait_for_timeout(1000)
        shot(page, "BEN_growth_A3_advanced_AFTER.png", ben=True)
        a3["snip"] = d.inner_text()[:2500]
        result["A3"] = a3
        log(f"A3 {a3.get('steps')} toggles={a3.get('toggles')} saved={a3.get('saved')}")

        # ── A4 Channel Basic info ──
        nav(d, "Channel")
        page.wait_for_timeout(600)
        try:
            d.get_by_text(re.compile(r"^Basic info$", re.I)).first.click(timeout=3000)
        except Exception:
            pass
        page.wait_for_timeout(1200)
        shot(page, "BEN_growth_A4_basic_BEFORE.png", ben=True)
        a4 = {"steps": [], "has_orbit": bool(re.search(r"Orbit With Ben|OpptiAI", d.inner_text(), re.I))}
        # Country
        try:
            d.get_by_text(re.compile(r"^Country$", re.I)).first.click(timeout=2000)
            page.wait_for_timeout(400)
            page.get_by_text(re.compile(r"^United Kingdom$", re.I)).first.click(timeout=3000)
            a4["steps"].append("country_uk")
        except Exception as e:
            a4["country_err"] = type(e).__name__
        # Keywords
        try:
            filled = page.evaluate(
                """(kw) => {
                  const d=document.querySelector('ytcp-settings-dialog');
                  const boxes=[...d.querySelectorAll('textarea, input')];
                  for (const b of boxes) {
                    const aria=(b.getAttribute('aria-label')||'')+(b.getAttribute('placeholder')||'');
                    const near=(b.closest('ytcp-form-textarea, ytcp-form-input-container')?.innerText||'');
                    if (/keyword/i.test(aria+near)) {
                      const proto=b.tagName==='TEXTAREA'?HTMLTextAreaElement.prototype:HTMLInputElement.prototype;
                      Object.getOwnPropertyDescriptor(proto,'value').set.call(b, kw);
                      b.dispatchEvent(new Event('input',{bubbles:true}));
                      return 'ok';
                    }
                  }
                  return null;
                }""",
                KEYWORDS,
            )
            a4["keywords"] = filled
            if not filled:
                d.get_by_text(re.compile(r"^Keywords$", re.I)).first.click(timeout=2000)
                page.keyboard.press("Meta+a")
                page.keyboard.type(KEYWORDS, delay=5)
                a4["keywords"] = "typed"
            a4["steps"].append("keywords")
        except Exception as e:
            a4["keywords_err"] = type(e).__name__
        a4["saved"] = save_dialog(d)
        page.wait_for_timeout(1000)
        shot(page, "BEN_growth_A4_basic_AFTER.png", ben=True)
        a4["snip"] = d.inner_text()[:2000]
        result["A4"] = a4
        log(f"A4 {a4}")

        # ── A5 Branding — do not add watermark ──
        # Branding is under Customisation usually, not Settings. Check Settings for watermark refs; also open Customisation → Branding
        try:
            d.get_by_role("button", name=re.compile(r"^Close$")).first.click(timeout=2000)
        except Exception:
            pass
        page.wait_for_timeout(800)
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/editing/images",
            wait_until="commit",
            timeout=90000,
        )
        page.wait_for_timeout(3500)
        shot(page, "BEN_growth_A5_branding.png", ben=True)
        body = page.inner_text("body")
        result["A5"] = {
            "url": page.url,
            "has_watermark": bool(re.search(r"Video watermark|Watermark", body, re.I)),
            "note": "Did not add branding watermark / subscribe graphics",
            "snip": body[:1200],
        }
        log(f"A5 watermark_section={result['A5']['has_watermark']}")

        dump("GROWTH_A_V02_RESULT.json", result)
        log(f"DONE A1_ok={result.get('A1_ok')}")


if __name__ == "__main__":
    main()
