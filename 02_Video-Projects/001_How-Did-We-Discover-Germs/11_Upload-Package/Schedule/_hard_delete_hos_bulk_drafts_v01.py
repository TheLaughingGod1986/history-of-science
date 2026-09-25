#!/usr/bin/env python3
"""Bulk-delete HOS draft/upload leftovers via More actions → Delete forever."""
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
TWINS = [
    "8uBR-9oxeWs",
    "YX2UR1u-JCQ",
    "Fnb3p81u-wY",
    "vpuRgKXtFlY",
    "Lcmh5y2KMQM",
]
EV = Path(
    "/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/"
    "001_How-Did-We-Discover-Germs/11_Upload-Package/Schedule/"
    "evidence_2026-09-07_hard_delete"
)


def dump(name, obj):
    (EV / name).write_text(json.dumps(obj, indent=2) + "\n")


def main() -> int:
    assert urllib.request.urlopen(f"{CDP}/json/version", timeout=2).read()
    notes: list = []
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = next(
            (p for p in ctx.pages if "studio.youtube.com" in (p.url or "")),
            None,
        ) or ctx.new_page()

        def shot(name: str) -> None:
            page.screenshot(path=str(EV / name))

        def click_text(pat: str):
            return page.evaluate(
                """(pat)=>{
              const re=new RegExp(pat,'i');
              const cands=[];
              const walk=(r,d=0)=>{
                if(!r||d>50) return;
                for(const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,[role=button],tp-yt-paper-item,[role=menuitem],span,div,a'):[])){
                  const t=(el.innerText||'').trim();
                  if(!re.test(t)) continue;
                  const box=el.getBoundingClientRect();
                  if(box.width>8 && box.height>8 && box.top>-20 && box.top<window.innerHeight+20) cands.push({el,t,box});
                }
                for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,d+1);
              };
              walk(document);
              if(!cands.length) return null;
              cands.sort((a,b)=>(b.box.width*b.box.height)-(a.box.width*a.box.height));
              cands[0].el.click(); return cands[0].t.slice(0,80);
            }""",
                pat,
            )

        def clear_selection() -> None:
            click_text(r"^Close$")
            page.keyboard.press("Escape")
            page.wait_for_timeout(300)
            page.evaluate(
                """()=>{
              const walk=(r,d=0)=>{
                if(!r||d>40) return false;
                for(const el of (r.querySelectorAll?r.querySelectorAll('ytcp-icon-button,button,[role=button]'):[])){
                  const a=(el.getAttribute('aria-label')||'');
                  if(/clear selection|Close|Deselect/i.test(a)){ el.click(); return a; }
                }
                for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot){ const x=walk(el.shadowRoot,d+1); if(x) return x; }
                return false;
              };
              return walk(document);
            }"""
            )

        def select_drafts_only() -> int:
            return int(
                page.evaluate(
                    """()=>{
              let n=0;
              const walk=(r,d=0)=>{
                if(!r||d>50) return;
                for(const row of (r.querySelectorAll?r.querySelectorAll('ytcp-video-row'):[])){
                  const t=row.innerText||'';
                  if(/\\bPublic\\b|\\bScheduled\\b/i.test(t)) continue;
                  if(!(/\\bDraft\\b|Uploading|Pending/i.test(t))) continue;
                  const boxes=[];
                  const walk2=(rr,dd=0)=>{
                    if(!rr||dd>25) return;
                    for(const el of (rr.querySelectorAll?rr.querySelectorAll('tp-yt-paper-checkbox,ytcp-checkbox-lit,input[type=checkbox],[role=checkbox]'):[])){
                      const box=el.getBoundingClientRect();
                      if(box.width>8) boxes.push(el);
                    }
                    for(const el of (rr.querySelectorAll?rr.querySelectorAll('*'):[]))
                      if(el.shadowRoot) walk2(el.shadowRoot,dd+1);
                  };
                  walk2(row);
                  if(boxes.length){
                    const el=boxes[0];
                    const checked=el.getAttribute('aria-checked')==='true' || el.checked;
                    if(!checked){ el.click(); n++; }
                  }
                }
                for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot) walk(el.shadowRoot,d+1);
              };
              walk(document); return n;
            }"""
                )
            )

        def ack_delete() -> bool:
            page.evaluate(
                """()=>{
              const walk=(r,d=0)=>{
                if(!r||d>50) return false;
                for(const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-checkbox,ytcp-checkbox-lit,input[type=checkbox],[role=checkbox]'):[])){
                  const near=el.closest && el.closest('ytcp-confirmation-dialog,tp-yt-paper-dialog,ytcp-dialog');
                  const nearT=near?((near.innerText||'').slice(0,700)):'';
                  if(/I understand that deleting|deleting this video is permanent/i.test(((el.innerText||'')+' '+nearT))){
                    if(!(el.getAttribute('aria-checked')==='true' || el.checked)) el.click();
                    return true;
                  }
                }
                for(const el of (r.querySelectorAll?r.querySelectorAll('label,span,div,yt-formatted-string'):[])){
                  if(/^I understand that deleting this video is permanent/i.test((el.innerText||'').trim())){
                    el.click(); return true;
                  }
                }
                for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                return false;
              };
              return walk(document);
            }"""
            )
            page.wait_for_timeout(500)
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

        def row_summary():
            return page.evaluate(
                """()=>{
              const rows=[];
              const walk=(r,d=0)=>{
                if(!r||d>50) return;
                for(const el of (r.querySelectorAll?r.querySelectorAll('ytcp-video-row'):[])){
                  const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                  const vis=/\\bPublic\\b/.test(t)?'Public':/\\bScheduled\\b/.test(t)?'Scheduled':/Uploading|Pending/.test(t)?'Uploading':/\\bDraft\\b/.test(t)?'Draft':'Other';
                  rows.push({vis,t:t.slice(0,160)});
                }
                for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot) walk(el.shadowRoot,d+1);
              };
              walk(document);
              const seen=new Set(); const out=[];
              for(const r of rows){ if(seen.has(r.t)) continue; seen.add(r.t); out.push(r);}
              return out;
            }"""
            )

        def list_ids():
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
              walk(document); return [...new Set(out)];
            }"""
            )

        for rnd in range(6):
            page.goto(
                f"https://studio.youtube.com/channel/{CHANNEL}/videos/short",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(2800)
            clear_selection()
            page.wait_for_timeout(400)
            for _ in range(5):
                page.mouse.wheel(0, 1000)
                page.wait_for_timeout(250)
            page.evaluate("window.scrollTo(0,0)")
            page.wait_for_timeout(400)
            n = select_drafts_only()
            notes.append(f"round={rnd} selected={n}")
            shot(f"105_selected_{rnd}.png")
            if n == 0:
                notes.append("no_drafts_selected")
                break
            more = click_text(r"^More actions$")
            notes.append(f"more={more}")
            page.wait_for_timeout(800)
            shot(f"105_more_{rnd}.png")
            deleted_item = click_text(r"^Delete(?: forever)?$|^Move to trash$")
            notes.append(f"menu_del={deleted_item}")
            page.wait_for_timeout(900)
            shot(f"105_dialog_{rnd}.png")
            ok = ack_delete()
            notes.append(f"ack={ok}")
            if not ok:
                click_text(r"^Delete$|^Confirm$")
                page.wait_for_timeout(500)
                ok = ack_delete()
                notes.append(f"ack2={ok}")
            page.wait_for_timeout(2800)
            shot(f"105_after_{rnd}.png")
            notes.append({"after": row_summary()})

        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/short",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3000)
        clear_selection()
        for _ in range(6):
            page.mouse.wheel(0, 1200)
            page.wait_for_timeout(300)
        page.evaluate("window.scrollTo(0,0)")
        page.wait_for_timeout(400)
        shot("106_FINAL_shorts.png")
        summary = row_summary()
        drafts = [r for r in summary if r["vis"] in ("Draft", "Uploading")]
        ids = list_ids()
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(2500)
        shot("106_FINAL_videos.png")
        ids2 = list_ids()
        all_ids = sorted(set(ids + ids2))
        twin = {}
        for vid in TWINS:
            page.goto(
                f"https://studio.youtube.com/video/{vid}/edit",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(1400)
            t = page.inner_text("body")[:400]
            twin[vid] = bool(re.search(r"Oops|not found|unavailable|no longer", t, re.I))
            shot(f"106_twin_{vid}.png")

        report = {
            "at": datetime.now().isoformat(timespec="seconds"),
            "channelId": CHANNEL,
            "notes": notes,
            "summary": summary,
            "drafts_left": drafts,
            "ids": all_ids,
            "non_allow": [i for i in all_ids if i not in ALLOWLIST],
            "twins_gone": twin,
            "remaining_shelf_count": len(all_ids),
            "deleted_ids": TWINS,
            "ok": (
                not drafts
                and not [i for i in all_ids if i not in ALLOWLIST]
                and all(twin.values())
                and ALLOWLIST.issubset(set(all_ids))
            ),
        }
        dump("RESULT_FINAL.json", report)
        lines = [
            "# HOS hard delete — FINAL 2026-09-07",
            "",
            f"Channel: `{CHANNEL}` (@HistoryOfScienceYT only)",
            "",
            f"**OK:** {report['ok']}",
            f"**Remaining shelf count (IDs):** {report['remaining_shelf_count']}",
            "",
            "## Deleted twins",
            "",
        ]
        for tvid in TWINS:
            lines.append(f"- `{tvid}` gone={twin[tvid]}")
        lines += ["", "## Remaining IDs", ""]
        for i in all_ids:
            lines.append(f"- `{i}`")
        lines += ["", f"Draft/upload rows left: {drafts or 'none'}", ""]
        (EV / "REPORT.md").write_text("\n".join(lines) + "\n")
        print(json.dumps({k: report[k] for k in ["ok", "remaining_shelf_count", "ids", "non_allow", "drafts_left", "twins_gone"]}, indent=2))
        print("NOTES", json.dumps(notes, indent=2)[:2500])
        return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
