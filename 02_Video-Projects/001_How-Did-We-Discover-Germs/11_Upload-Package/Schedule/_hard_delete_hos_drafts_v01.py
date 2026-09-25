#!/usr/bin/env python3
"""Delete ID-less Draft / pending upload rows on HOS Shorts shelf."""
from __future__ import annotations

import json
import re
import urllib.request
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

PORT = 9460
CDP = f"http://127.0.0.1:{PORT}"
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"
ALLOWLIST = {
    "_C92tIJCk8A",
    "H1y0DXFVmw8",
    "iqToagXnjX0",
    "8_Edn_HCi1s",
    "sILtQxgYQk8",
    "93fPUG-hW0A",
}
EV = Path(
    "/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/"
    "001_How-Did-We-Discover-Germs/11_Upload-Package/Schedule/"
    "evidence_2026-09-07_hard_delete"
)


def dump(name, obj):
    (EV / name).write_text(json.dumps(obj, indent=2) + "\n")


def shot(page, name):
    page.screenshot(path=str(EV / name), full_page=False)


def body(page, n=8000):
    try:
        return page.inner_text("body")[:n]
    except Exception as e:
        return str(e)


def click_js(page, pattern: str) -> bool:
    return bool(
        page.evaluate(
            """(pat)=>{
          const re=new RegExp(pat,'i');
          const walk=(r,d=0)=>{
            if(!r||d>50) return false;
            for(const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,[role=button],tp-yt-paper-item,[role=menuitem],div,span,a'):[])){
              const t=(el.innerText||'').trim();
              if(re.test(t)){
                const box=el.getBoundingClientRect();
                if(box.width>6 && box.height>6){ el.click(); return t.slice(0,80); }
              }
            }
            for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot){ const x=walk(el.shadowRoot,d+1); if(x) return x; }
            return false;
          };
          return walk(document);
        }""",
            pattern,
        )
    )


def check_ack(page) -> bool:
    return bool(
        page.evaluate(
            """()=>{
      const walk=(r,d=0)=>{
        if(!r||d>50) return false;
        for(const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-checkbox,ytcp-checkbox-lit,input[type=checkbox],[role=checkbox]'):[])){
          const near=el.closest && el.closest('ytcp-confirmation-dialog,tp-yt-paper-dialog,ytcp-dialog');
          const nearT=near?((near.innerText||'').slice(0,600)):'';
          const t=((el.innerText||'')+' '+(el.getAttribute('aria-label')||'')+' '+nearT);
          if(/I understand that deleting|deleting this video is permanent/i.test(t)){
            if(el.getAttribute('aria-checked')==='true' || el.checked) return 'already';
            el.click(); return 'clicked';
          }
        }
        for(const el of (r.querySelectorAll?r.querySelectorAll('yt-formatted-string,span,div,label'):[])){
          if(/^I understand that deleting this video is permanent/i.test((el.innerText||'').trim())){
            el.click(); return 'label';
          }
        }
        for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
          if(el.shadowRoot){ const x=walk(el.shadowRoot,d+1); if(x) return x; }
        return false;
      };
      return walk(document);
    }"""
        )
    )


def click_enabled_delete_forever(page) -> bool:
    return bool(
        page.evaluate(
            """()=>{
      const walk=(r,d=0)=>{
        if(!r||d>50) return false;
        for(const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,[role=button]'):[])){
          if(!/^Delete forever$/i.test((el.innerText||'').trim())) continue;
          const dis=el.disabled || el.getAttribute('aria-disabled')==='true';
          const box=el.getBoundingClientRect();
          if(!dis && box.width>20){ el.click(); return true; }
        }
        for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
          if(el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
        return false;
      };
      return walk(document);
    }"""
        )
    )


def count_edit_draft(page) -> int:
    return int(
        page.evaluate(
            """()=>{
      let n=0;
      const walk=(r,d=0)=>{
        if(!r||d>50) return;
        for(const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,a,[role=button],span,div'):[])){
          if(/^Edit draft$/i.test((el.innerText||'').trim())) n++;
        }
        for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
          if(el.shadowRoot) walk(el.shadowRoot,d+1);
      };
      walk(document);
      return n;
    }"""
        )
    )


def list_ids(page):
    return page.evaluate(
        """()=>{
      const out=[];
      const walk=(r,d=0)=>{
        if(!r||d>50) return;
        for(const a of (r.querySelectorAll?r.querySelectorAll('a[href*="/video/"]'):[])){
          const m=(a.getAttribute('href')||'').match(/\\/video\\/([A-Za-z0-9_-]{11})/);
          if(m) out.push(m[1]);
        }
        for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
          if(el.shadowRoot) walk(el.shadowRoot,d+1);
      };
      walk(document);
      return [...new Set(out)];
    }"""
    )


def open_first_edit_draft(page) -> bool:
    return bool(
        page.evaluate(
            """()=>{
      const walk=(r,d=0)=>{
        if(!r||d>50) return false;
        for(const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,a,[role=button]'):[])){
          if(/^Edit draft$/i.test((el.innerText||'').trim())){
            const box=el.getBoundingClientRect();
            if(box.width>8){ el.click(); return true; }
          }
        }
        for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
          if(el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
        return false;
      };
      return walk(document);
    }"""
        )
    )


def open_options(page):
    return page.evaluate(
        """()=>{
      const walk=(r,d=0)=>{
        if(!r||d>50) return null;
        for(const el of (r.querySelectorAll?r.querySelectorAll('ytcp-icon-button,button,[role=button]'):[])){
          const a=(el.getAttribute('aria-label')||'');
          if(/options|more actions|more options|^More$/i.test(a)){
            const box=el.getBoundingClientRect();
            if(box.width>8){ el.click(); return a; }
          }
        }
        for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
          if(el.shadowRoot){ const x=walk(el.shadowRoot,d+1); if(x) return x; }
        return null;
      };
      return walk(document);
    }"""
    )


def goto_shorts(page):
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/short",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2800)


def main() -> int:
    assert urllib.request.urlopen(f"{CDP}/json/version", timeout=2).read()
    notes = []
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = next(
            (p for p in ctx.pages if "studio.youtube.com" in (p.url or "")),
            None,
        ) or ctx.new_page()

        goto_shorts(page)
        shot(page, "95_drafts_before.png")
        before_drafts = count_edit_draft(page)
        before_ids = list_ids(page)
        notes.append(f"before_drafts={before_drafts} ids={before_ids}")

        for i in range(12):
            goto_shorts(page)
            n = count_edit_draft(page)
            if n == 0:
                notes.append(f"no_more_drafts_at_{i}")
                break
            # Prefer cancel upload if present
            if click_js(page, r"^Cancel upload$"):
                notes.append(f"cancel_upload_{i}")
                page.wait_for_timeout(800)
                for pat in [r"^Cancel upload$", r"^Confirm$", r"^Yes$", r"^OK$", r"^Done$"]:
                    click_js(page, pat)
                page.wait_for_timeout(1200)
                continue

            if not open_first_edit_draft(page):
                notes.append(f"no_edit_draft_{i}")
                break
            page.wait_for_timeout(2500)
            # Capture any id that appeared
            url = page.url or ""
            m = re.search(r"/video/([A-Za-z0-9_-]{11})", url)
            vid = m.group(1) if m else None
            notes.append(f"opened_draft_{i}_vid={vid}_url={url[:120]}")
            if vid and vid in ALLOWLIST:
                notes.append(f"ABORT_allowlist_draft={vid}")
                dump("DRAFT_CLEAN_ABORT.json", {"notes": notes})
                return 4
            shot(page, f"95_draft_open_{i}.png")
            open_options(page)
            page.wait_for_timeout(700)
            click_js(page, r"^Delete(?: forever)?$|^Move to trash$")
            page.wait_for_timeout(900)
            check_ack(page)
            page.wait_for_timeout(500)
            if not click_enabled_delete_forever(page):
                click_js(page, r"^Delete forever$|^Delete$|^Confirm$")
            page.wait_for_timeout(2500)
            shot(page, f"95_draft_deleted_{i}.png")
            notes.append(f"deleted_draft_{i}")

        goto_shorts(page)
        page.wait_for_timeout(2000)
        # scroll
        for _ in range(6):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(400)
        shot(page, "96_drafts_after.png")
        after_drafts = count_edit_draft(page)
        after_ids = list_ids(page)
        non_allow = [i for i in after_ids if i not in ALLOWLIST]
        t = body(page, 5000)
        report = {
            "at": datetime.now().isoformat(timespec="seconds"),
            "before_drafts": before_drafts,
            "after_drafts": after_drafts,
            "before_ids": before_ids,
            "after_ids": after_ids,
            "non_allowlist_ids": non_allow,
            "has_draft_text": bool(re.search(r"\bDraft\b|Edit draft", t)),
            "has_uploading": bool(re.search(r"Uploading|Cancel upload", t, re.I)),
            "notes": notes,
            "ok": after_drafts == 0 and not non_allow,
        }
        dump("DRAFT_CLEAN.json", report)
        print(json.dumps(report, indent=2))
        return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
