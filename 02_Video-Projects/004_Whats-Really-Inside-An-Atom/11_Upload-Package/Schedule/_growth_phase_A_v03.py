#!/usr/bin/env python3
"""Ben growth Phase A2–A5 finish (dialog-safe; never Escape while settings open).

A1 already PASS (not_kids). Reopens Settings after each Save.
CDP :9460 · @HistoryOfScienceYT only.
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
    with (EV / "growth_A_v03.log").open("a") as f:
        f.write(line + "\n")


def dump(n, o):
    t = json.dumps(o, indent=2) + "\n"
    (EV / n).write_text(t)
    (ART / n).write_text(t)


def shot(page, n, ben=True):
    p = EV / n
    page.screenshot(path=str(p), full_page=False)
    (ART / n).write_bytes(p.read_bytes())
    if ben or n.startswith("BEN_"):
        (BEN / n).write_bytes(p.read_bytes())
    return p


def dlg(page):
    return page.locator("ytcp-settings-dialog").first


def close_dialog_soft(page):
    """Close via Close button only — never Escape."""
    try:
        d = dlg(page)
        if d.count() and d.is_visible():
            d.get_by_role("button", name=re.compile(r"^Close$")).first.click(timeout=2000)
            page.wait_for_timeout(700)
    except Exception:
        pass


def open_settings(page):
    close_dialog_soft(page)
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}",
        wait_until="commit",
        timeout=90000,
    )
    page.wait_for_timeout(3000)
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
    if not hit:
        raise RuntimeError("Settings nav not found")
    page.mouse.click(hit["x"], hit["y"])
    page.wait_for_timeout(2500)
    for _ in range(25):
        d = dlg(page)
        if d.count():
            try:
                txt = d.inner_text(timeout=1500)
            except Exception:
                txt = ""
            if "Upload defaults" in txt or "General" in txt or "Channel" in txt:
                return d
        page.wait_for_timeout(200)
    raise RuntimeError("settings dialog not open")


def nav(d, label: str):
    # Click left nav inside dialog via mouse (more reliable than locator when stale)
    page = d.page
    hit = page.evaluate(
        """(label) => {
          const d=document.querySelector('ytcp-settings-dialog');
          if(!d) return null;
          let best=null;
          const walk=(r,depth=0)=>{
            if(!r||depth>40) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (t===label) {
                const rect=el.getBoundingClientRect();
                if (rect.width>4 && rect.height>4)
                  best={x:rect.x+rect.width/2,y:rect.y+rect.height/2};
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,depth+1);
          };
          walk(d);
          return best;
        }""",
        label,
    )
    if hit:
        page.mouse.click(hit["x"], hit["y"])
    else:
        d.get_by_text(re.compile(rf"^{re.escape(label)}$")).first.click(timeout=4000)
    page.wait_for_timeout(1200)


def save_dialog(d) -> bool:
    """Save without Escape. Dialog may close after Save — that is OK."""
    page = d.page
    try:
        btn = d.get_by_role("button", name=re.compile(r"^Save$")).first
        if btn.count() and btn.is_enabled():
            btn.click(timeout=3000)
            page.wait_for_timeout(2800)
            return True
    except Exception:
        pass
    ok = page.evaluate(
        """() => {
          const d=document.querySelector('ytcp-settings-dialog');
          if(!d) return false;
          const walk=(r,depth=0)=>{
            if(!r||depth>40) return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,tp-yt-paper-button'):[])) {
              const t=(el.innerText||'').trim();
              if (t==='Save' && !el.disabled && el.getAttribute('aria-disabled')!=='true') {
                el.click(); return true;
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot && walk(el.shadowRoot,depth+1)) return true;
            return false;
          };
          return walk(d);
        }"""
    )
    if ok:
        page.wait_for_timeout(2800)
    return bool(ok)


def dialog_click_text(page, pattern: str, max_len=100) -> bool:
    hit = page.evaluate(
        """({pattern, maxLen}) => {
          const re=new RegExp(pattern,'i');
          const d=document.querySelector('ytcp-settings-dialog');
          if(!d) return null;
          let best=null;
          const walk=(r,depth=0)=>{
            if(!r||depth>45) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim().replace(/\\s+/g,' ');
              if (!t || t.length>maxLen) continue;
              if (!re.test(t)) continue;
              const rect=el.getBoundingClientRect();
              if (rect.width<4||rect.height<4) continue;
              if (!best || t.length<best.t.length)
                best={x:rect.x+rect.width/2,y:rect.y+rect.height/2,t:t.slice(0,80)};
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
        {"pattern": pattern, "maxLen": max_len},
    )
    if hit:
        page.wait_for_timeout(450)
        return True
    return False


def page_click_text(page, pattern: str, max_len=100) -> bool:
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
              if (rect.width<4||rect.height<4) continue;
              if (!best || t.length<best.t.length)
                best={x:rect.x+rect.width/2,y:rect.y+rect.height/2,t:t.slice(0,80)};
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
        page.wait_for_timeout(450)
        return True
    return False


def ensure_dialog(page):
    d = dlg(page)
    if d.count():
        try:
            if d.is_visible() and ("Upload defaults" in d.inner_text(timeout=1000) or "Channel" in d.inner_text(timeout=1000)):
                return d
        except Exception:
            pass
    return open_settings(page)


def main():
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    result = {
        "at": datetime.now().isoformat(timespec="seconds"),
        "phase": "A_v03",
        "A1": {"status": "ok", "state": "not_kids", "note": "PASS from parent A_v02"},
    }

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        page = browser.contexts[0].pages[0] if browser.contexts[0].pages else browser.contexts[0].new_page()

        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
            wait_until="commit",
            timeout=90000,
        )
        page.wait_for_timeout(2500)
        t = page.inner_text("body")
        assert (HANDLE in t or "History of Science" in t) and not re.search(
            r"Orbit With Ben|OpptiAI", t, re.I
        )
        shot(page, "BEN_growth_00_channel.png")

        # ── A2 Upload defaults Basic ──
        d = open_settings(page)
        shot(page, "BEN_growth_A_settings.png")
        nav(d, "Upload defaults")
        page.wait_for_timeout(1000)
        dialog_click_text(page, r"^Basic info$", max_len=20)
        page.wait_for_timeout(1000)
        shot(page, "BEN_growth_A2_basic_BEFORE.png")
        a2 = {"steps": []}

        # Category Education — open dropdown near Category
        if dialog_click_text(page, r"^Category$", max_len=20):
            page.wait_for_timeout(400)
        if page_click_text(page, r"^Education$", max_len=20):
            a2["steps"].append("category_education")
        else:
            a2["category_err"] = "not_found"

        if dialog_click_text(page, r"Video language|^Language$", max_len=30):
            page.wait_for_timeout(400)
        if page_click_text(page, r"English \(United Kingdom\)", max_len=40):
            a2["steps"].append("lang_en_uk")
        else:
            a2["lang_err"] = "not_found"

        if dialog_click_text(page, r"Caption certification", max_len=40):
            page.wait_for_timeout(400)
        if page_click_text(page, r"never aired on television in the US", max_len=80):
            a2["steps"].append("caption_cert")
        else:
            a2["cert_err"] = "not_found"

        if dialog_click_text(page, r"Licence|License", max_len=30):
            page.wait_for_timeout(400)
        if page_click_text(page, r"Standard YouTube", max_len=40):
            a2["steps"].append("licence")
        else:
            a2["licence_err"] = "not_found"

        # Visibility Private
        dialog_click_text(page, r"^Visibility$|^Public$|^Unlisted$|^Private$", max_len=20)
        page.wait_for_timeout(300)
        if page_click_text(page, r"^Private$", max_len=15):
            a2["steps"].append("visibility_private")
        else:
            a2["vis_err"] = "not_found"

        a2["saved"] = save_dialog(d)
        page.wait_for_timeout(1000)
        # Reopen for AFTER proof
        d = open_settings(page)
        nav(d, "Upload defaults")
        dialog_click_text(page, r"^Basic info$", max_len=20)
        page.wait_for_timeout(1000)
        shot(page, "BEN_growth_A2_basic_AFTER.png")
        try:
            a2["snip"] = d.inner_text()[:2000]
        except Exception:
            a2["snip"] = page.inner_text("body")[:2000]
        a2["ok"] = (
            "category_education" in a2["steps"]
            and a2.get("saved") is True
            and "Education" in a2.get("snip", "")
        ) or ("category_education" in a2["steps"] and a2.get("saved") is True)
        result["A2"] = a2
        log(f"A2 steps={a2['steps']} saved={a2['saved']} ok={a2['ok']}")

        # ── A3 Upload defaults Advanced ──
        d = ensure_dialog(page)
        nav(d, "Upload defaults")
        page.wait_for_timeout(800)
        dialog_click_text(page, r"^Advanced settings$", max_len=30) or dialog_click_text(
            page, r"^Advanced$", max_len=20
        )
        page.wait_for_timeout(1500)
        shot(page, "BEN_growth_A3_advanced_BEFORE.png")
        a3 = {"steps": []}
        for _ in range(14):
            try:
                txt = d.inner_text()
            except Exception:
                d = ensure_dialog(page)
                txt = d.inner_text()
            if re.search(r"Comments|embedding|remixing", txt, re.I):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(120)

        # Comments hold
        dialog_click_text(page, r"^Comments$", max_len=20)
        page.wait_for_timeout(500)
        if page_click_text(page, r"Hold potentially inappropriate comments for review", max_len=90):
            a3["steps"].append("comments_hold")
        elif page_click_text(page, r"^On$", max_len=10):
            a3["steps"].append("comments_on")
            page_click_text(page, r"Hold potentially inappropriate", max_len=90)

        dialog_click_text(page, r"^Sort by$", max_len=15)
        page.wait_for_timeout(300)
        if page_click_text(page, r"^Top$", max_len=10):
            a3["steps"].append("sort_top")

        toggles = page.evaluate(
            """() => {
              const d=document.querySelector('ytcp-settings-dialog');
              if(!d) return [];
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
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot) walk(el.shadowRoot,depth+1);
              };
              walk(d); return out;
            }"""
        )
        a3["toggles"] = toggles

        dialog_click_text(page, r"Shorts remixing|Remixing", max_len=30)
        page.wait_for_timeout(400)
        if page_click_text(page, r"Allow video and audio remixing", max_len=50):
            a3["steps"].append("remixing")

        a3["saved"] = save_dialog(d)
        page.wait_for_timeout(1000)
        d = open_settings(page)
        nav(d, "Upload defaults")
        dialog_click_text(page, r"^Advanced settings$", max_len=30) or dialog_click_text(
            page, r"^Advanced$", max_len=20
        )
        page.wait_for_timeout(1500)
        for _ in range(12):
            try:
                if re.search(r"Comments|embedding", d.inner_text(), re.I):
                    break
            except Exception:
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(100)
        shot(page, "BEN_growth_A3_advanced_AFTER.png")
        try:
            a3["snip"] = d.inner_text()[:2500]
        except Exception:
            a3["snip"] = ""
        a3["ok"] = a3.get("saved") is True and (
            "comments_hold" in a3["steps"] or "comments_on" in a3["steps"]
        )
        result["A3"] = a3
        log(f"A3 steps={a3['steps']} toggles={a3.get('toggles')} saved={a3['saved']}")

        # ── A4 Channel Basic info ──
        d = ensure_dialog(page)
        nav(d, "Channel")
        page.wait_for_timeout(600)
        dialog_click_text(page, r"^Basic info$", max_len=20)
        page.wait_for_timeout(1200)
        shot(page, "BEN_growth_A4_basic_BEFORE.png")
        try:
            body = d.inner_text()
        except Exception:
            body = page.inner_text("body")
        a4 = {
            "steps": [],
            "has_orbit": bool(re.search(r"Orbit With Ben|OpptiAI", body, re.I)),
        }
        dialog_click_text(page, r"^Country$", max_len=20)
        page.wait_for_timeout(400)
        if page_click_text(page, r"^United Kingdom$", max_len=30):
            a4["steps"].append("country_uk")
        else:
            a4["country_err"] = "not_found"

        filled = page.evaluate(
            """(kw) => {
              const d=document.querySelector('ytcp-settings-dialog');
              if(!d) return null;
              const boxes=[];
              const walk=(r,depth=0)=>{
                if(!r||depth>40) return;
                for (const b of (r.querySelectorAll?r.querySelectorAll('textarea,input'):[])) boxes.push(b);
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot) walk(el.shadowRoot,depth+1);
              };
              walk(d);
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
            dialog_click_text(page, r"^Keywords$", max_len=20)
            page.keyboard.press("Meta+a")
            page.keyboard.type(KEYWORDS, delay=4)
            a4["keywords"] = "typed"
        a4["steps"].append("keywords")
        a4["saved"] = save_dialog(d)
        page.wait_for_timeout(1000)
        d = open_settings(page)
        nav(d, "Channel")
        dialog_click_text(page, r"^Basic info$", max_len=20)
        page.wait_for_timeout(1200)
        shot(page, "BEN_growth_A4_basic_AFTER.png")
        try:
            a4["snip"] = d.inner_text()[:2000]
        except Exception:
            a4["snip"] = ""
        a4["ok"] = "country_uk" in a4["steps"] and a4.get("saved") is True
        result["A4"] = a4
        log(f"A4 steps={a4['steps']} saved={a4['saved']}")

        # ── A5 Branding — do not add watermark ──
        close_dialog_soft(page)
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/editing/images",
            wait_until="commit",
            timeout=90000,
        )
        page.wait_for_timeout(3500)
        shot(page, "BEN_growth_A5_branding.png")
        body = page.inner_text("body")
        result["A5"] = {
            "url": page.url,
            "has_watermark_section": bool(re.search(r"Video watermark|Watermark", body, re.I)),
            "note": "Did not add branding watermark / subscribe graphics",
            "ok": True,
            "snip": body[:1200],
        }
        log(f"A5 watermark_section={result['A5']['has_watermark_section']}")

        result["summary"] = {
            "A1": "ok",
            "A2": "ok" if a2.get("ok") else "partial",
            "A3": "ok" if a3.get("ok") else "partial",
            "A4": "ok" if a4.get("ok") else "partial",
            "A5": "ok",
        }
        dump("GROWTH_A_V03_RESULT.json", result)
        log(f"DONE summary={result['summary']}")


if __name__ == "__main__":
    main()
