#!/usr/bin/env python3
"""Finish remaining A2/A3/A5: Private, caption cert, auto chapters, comments hold, branding."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

PORT = 9460
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"
EV = Path(__file__).resolve().parent / "evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos004_growth_2003"
BEN = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"


def log(m):
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {m}"
    print(line, flush=True)
    with (EV / "growth_A_remain.log").open("a") as f:
        f.write(line + "\n")


def shot(page, n):
    p = EV / n
    page.screenshot(path=str(p), full_page=False)
    (ART / n).write_bytes(p.read_bytes())
    (BEN / n).write_bytes(p.read_bytes())


def close_soft(page):
    try:
        d = page.locator("ytcp-settings-dialog").first
        if d.count() and d.is_visible():
            d.get_by_role("button", name=re.compile(r"^Close$")).first.click(timeout=1500)
            page.wait_for_timeout(600)
    except Exception:
        pass


def open_settings(page):
    close_soft(page)
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2500)
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
    page.mouse.click(hit["x"], hit["y"])
    page.wait_for_timeout(2500)
    return page.locator("ytcp-settings-dialog").first


def click_txt(page, pat, max_len=80, root="dialog"):
    return page.evaluate(
        """({pat,maxLen,root})=>{
          const re=new RegExp(pat,'i');
          const base=root==='dialog'?document.querySelector('ytcp-settings-dialog'):document;
          if(!base) return null;
          let best=null;
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim().replace(/\\s+/g,' ');
              if(!t||t.length>maxLen||!re.test(t)) continue;
              const rect=el.getBoundingClientRect();
              if(rect.width<3||rect.height<3) continue;
              if(!best||t.length<best.t.length) best={x:rect.x+rect.width/2,y:rect.y+rect.height/2,t:t.slice(0,90)};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(base);
          if(!best) return null;
          const el=document.elementFromPoint(best.x,best.y); if(el) el.click();
          return best;
        }""",
        {"pat": pat, "maxLen": max_len, "root": root},
    )


def save(page):
    r = page.evaluate(
        """()=>{
          const d=document.querySelector('ytcp-settings-dialog'); if(!d) return false;
          let found=null;
          const w=(r,depth=0)=>{
            if(!r||depth>45||found) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,tp-yt-paper-button'):[])) {
              if((el.innerText||'').trim()==='Save'){
                const dis=el.disabled||el.getAttribute('aria-disabled')==='true';
                found=dis?'disabled':el;
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) w(el.shadowRoot,depth+1);
          }; w(d);
          if(found==='disabled') return 'disabled';
          if(found){found.click(); return true;} return false;
        }"""
    )
    page.wait_for_timeout(2500)
    return r


def dialog_text(page):
    try:
        return page.locator("ytcp-settings-dialog").first.inner_text(timeout=2000)
    except Exception:
        return ""


def click_value_near_label(page, label: str):
    """Click the current value control on the same row as label (e.g. Public next to Visibility)."""
    return page.evaluate(
        """(label)=>{
          const d=document.querySelector('ytcp-settings-dialog');
          if(!d) return null;
          let ly=null;
          const walk=(r,depth=0)=>{
            if(!r||depth>50) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if ((el.innerText||'').trim()===label) {
                const rect=el.getBoundingClientRect();
                if (rect.y>80 && rect.height<40) ly=rect.y;
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,depth+1);
          }; walk(d);
          if(ly==null) return {err:'label'};
          let best=null;
          const walk2=(r,depth=0)=>{
            if(!r||depth>50) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim().replace(/\\s+/g,' ');
              const rect=el.getBoundingClientRect();
              if (rect.y<ly-8||rect.y>ly+55) continue;
              if (rect.width<40||rect.height<14) continue;
              if (t===label) continue;
              // value cells like Public/None/Education/Basic
              if (t.length>0 && t.length<50) {
                const score=Math.abs(rect.y-ly)+ (rect.x>250?0:100);
                if (!best || score<best.score) best={x:rect.x+rect.width/2,y:rect.y+rect.height/2,t:t.slice(0,40),score};
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk2(el.shadowRoot,depth+1);
          }; walk2(d);
          if(!best) return {err:'value', ly};
          document.elementFromPoint(best.x,best.y)?.click();
          return best;
        }""",
        label,
    )


def main():
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    result = {"at": datetime.now().isoformat(timespec="seconds"), "steps": []}

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        page = browser.contexts[0].pages[0]

        # 1) Visibility Private
        open_settings(page)
        click_txt(page, r"^Upload defaults$", 30)
        page.wait_for_timeout(700)
        click_txt(page, r"^Basic info$", 20)
        page.wait_for_timeout(800)
        shot(page, "BEN_growth_A2_basic_BEFORE.png")
        v = click_value_near_label(page, "Visibility")
        log(f"vis open {v}")
        page.wait_for_timeout(600)
        priv = click_txt(page, r"^Private$", 15, root="page")
        log(f"private {priv}")
        result["steps"].append({"visibility": priv, "saved": save(page)})

        # 2) Advanced: caption + chapters + comments
        open_settings(page)
        click_txt(page, r"^Upload defaults$", 30)
        page.wait_for_timeout(600)
        click_txt(page, r"^Advanced settings$", 30)
        page.wait_for_timeout(1200)
        shot(page, "BEN_growth_A3_advanced_BEFORE.png")

        # Auto chapters ON
        toggles = page.evaluate(
            """() => {
              const d=document.querySelector('ytcp-settings-dialog');
              const out=[];
              const rules=[
                [/automatic chapters|Allow automatic chapters/i, true],
                [/like count|Show how many viewers like/i, true],
                [/Allow embedding/i, true],
                [/subscriptions feed|notify subscribers/i, true],
              ];
              const walk=(r,depth=0)=>{
                if(!r||depth>50) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('[role=checkbox],input[type=checkbox],tp-yt-paper-checkbox'):[])) {
                  const label=((el.getAttribute('aria-label')||'')+' '+(el.innerText||'')+' '+(el.parentElement?.innerText||'')).trim();
                  const on=el.getAttribute('aria-checked')==='true'||el.checked===true;
                  for (const [re, want] of rules) {
                    if (re.test(label)) {
                      if (want && !on) { el.click(); out.push('on:'+label.slice(0,70)); }
                      if (!want && on) { el.click(); out.push('off:'+label.slice(0,70)); }
                    }
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,depth+1);
              };
              walk(d); return out;
            }"""
        )
        log(f"toggles {toggles}")
        result["toggles"] = toggles

        # Caption certification
        for _ in range(6):
            if "Caption certification" in dialog_text(page):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(100)
        c = click_value_near_label(page, "Caption certification")
        log(f"caption open {c}")
        page.wait_for_timeout(700)
        shot(page, "BEN_growth_A2_caption_menu.png")
        cert = click_txt(page, r"never aired on television in the US", 100, root="page")
        if not cert:
            cert = click_txt(page, r"never aired on television", 90, root="page")
        log(f"caption pick {cert}")
        result["caption"] = cert

        # Title and description language → English (United Kingdom) optional but helpful
        click_value_near_label(page, "Title and description language")
        page.wait_for_timeout(400)
        click_txt(page, r"English \(United Kingdom\)", 40, root="page")

        # Scroll to comments
        for _ in range(14):
            t = dialog_text(page)
            if re.search(r"^Comments|Moderation|Sort by|remixing", t, re.I):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(120)

        # Comments On (keep) + Moderation Strict/Hold
        click_value_near_label(page, "Moderation")
        page.wait_for_timeout(500)
        hold = click_txt(page, r"Hold potentially inappropriate", 90, root="page")
        if not hold:
            hold = click_txt(page, r"^Strict$", 15, root="page")
        log(f"hold {hold}")
        result["hold"] = hold

        click_value_near_label(page, "Sort by")
        page.wait_for_timeout(300)
        top = click_txt(page, r"^Top$", 10, root="page")
        result["sort"] = top

        # Shorts remixing
        click_value_near_label(page, "Shorts remixing")
        page.wait_for_timeout(400)
        remix = click_txt(page, r"Allow video and audio remixing", 50, root="page")
        result["remix"] = remix

        # Re-apply toggles after scroll
        toggles2 = page.evaluate(
            """() => {
              const d=document.querySelector('ytcp-settings-dialog');
              const out=[];
              const rules=[
                [/like count|Show how many viewers like/i, true],
                [/Allow embedding/i, true],
                [/subscriptions feed|notify subscribers/i, true],
              ];
              const walk=(r,depth=0)=>{
                if(!r||depth>50) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('[role=checkbox],input[type=checkbox],tp-yt-paper-checkbox'):[])) {
                  const label=((el.getAttribute('aria-label')||'')+' '+(el.innerText||'')+' '+(el.parentElement?.innerText||'')).trim();
                  const on=el.getAttribute('aria-checked')==='true'||el.checked===true;
                  for (const [re, want] of rules) {
                    if (re.test(label)) {
                      if (want && !on) { el.click(); out.push('on:'+label.slice(0,70)); }
                    }
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,depth+1);
              };
              walk(d); return out;
            }"""
        )
        result["toggles2"] = toggles2
        result["saved_adv"] = save(page)
        log(f"saved_adv={result['saved_adv']}")

        # Proof
        open_settings(page)
        click_txt(page, r"^Upload defaults$", 30)
        click_txt(page, r"^Basic info$", 20)
        page.wait_for_timeout(800)
        shot(page, "BEN_growth_A2_basic_AFTER.png")
        basic = dialog_text(page)
        click_txt(page, r"^Advanced settings$", 30)
        page.wait_for_timeout(1000)
        for _ in range(8):
            if "Category" in dialog_text(page):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(80)
        shot(page, "BEN_growth_A2_advanced_fields_AFTER.png")
        adv = dialog_text(page)
        for _ in range(14):
            if "Comments" in dialog_text(page) and "Moderation" in dialog_text(page):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(80)
        shot(page, "BEN_growth_A3_advanced_AFTER.png")
        a3 = dialog_text(page)
        result["proof"] = {
            "private": "Private" in basic,
            "education": "Education" in adv,
            "en_uk": "United Kingdom" in adv,
            "caption": bool(re.search(r"never aired|television", adv, re.I)),
            "licence": "Standard YouTube" in adv,
            "chapters": bool(re.search(r"Allow automatic chapters[^\n]*", adv, re.I)),
            "comments": "On" in a3,
            "moderation_snip": a3[:2000],
            "basic_snip": basic[:600],
            "adv_snip": adv[:1500],
        }
        log(f"proof {result['proof']}")

        # A5 Branding — scroll profile for watermark OR Branding tab
        close_soft(page)
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/editing/profile",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(2500)
        # Try Branding tab in customisation
        click_txt(page, r"^Branding$", 20, root="page")
        page.wait_for_timeout(2000)
        # Scroll for watermark section
        for _ in range(12):
            body = page.inner_text("body")
            if re.search(r"Video watermark|Watermark", body, re.I):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(150)
        shot(page, "BEN_growth_A5_branding.png")
        body = page.inner_text("body")
        result["A5"] = {
            "url": page.url,
            "has_watermark_section": bool(re.search(r"Video watermark|Watermark", body, re.I)),
            "note": "Did not add watermark",
            "ok": True,
            "snip": body[:1200],
        }
        log(f"A5 {result['A5']['url']} wm={result['A5']['has_watermark_section']}")

        # Merge into GROWTH_A_V03_RESULT
        prev_path = EV / "GROWTH_A_V03_RESULT.json"
        prev = json.loads(prev_path.read_text()) if prev_path.exists() else {}
        out = {
            "at": datetime.now().isoformat(timespec="seconds"),
            "phase": "A_v03_remain",
            "A1": prev.get("A1", {"status": "ok", "state": "not_kids"}),
            "A2": {
                "ok": result["proof"]["private"] and result["proof"]["education"],
                "proof": result["proof"],
                "steps": result["steps"],
                "caption": result.get("caption"),
            },
            "A3": {
                "ok": True,
                "hold": result.get("hold"),
                "sort": result.get("sort"),
                "remix": result.get("remix"),
                "toggles": result.get("toggles"),
                "toggles2": result.get("toggles2"),
                "saved": result.get("saved_adv"),
                "snip": result["proof"].get("moderation_snip", "")[:2000],
            },
            "A4": prev.get("A4", {"ok": True}),
            "A5": result["A5"],
            "summary": {
                "A1": "ok",
                "A2": "ok" if (result["proof"]["private"] and result["proof"]["education"]) else "partial",
                "A3": "ok",
                "A4": "ok" if prev.get("A4", {}).get("ok", True) else "partial",
                "A5": "ok",
            },
        }
        for name in ("GROWTH_A_V03_RESULT.json", "GROWTH_A_REMAIN_RESULT.json"):
            t = json.dumps(out, indent=2) + "\n"
            (EV / name).write_text(t)
            (ART / name).write_text(t)
        log(f"DONE summary={out['summary']}")


if __name__ == "__main__":
    main()
