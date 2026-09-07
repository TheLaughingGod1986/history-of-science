#!/usr/bin/env python3
"""Verify HOS hard-delete result + cancel ID-less draft/upload junk."""
from __future__ import annotations

import json
import re
import time
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
    EV.mkdir(parents=True, exist_ok=True)
    (EV / name).write_text(json.dumps(obj, indent=2) + "\n")


def shot(page, name):
    dest = EV / name
    page.screenshot(path=str(dest), full_page=False)
    return str(dest)


def body(page, n=8000):
    try:
        return page.inner_text("body")[:n]
    except Exception as e:
        return str(e)


def list_rows(page):
    return page.evaluate(
        """()=>{
      const out=[];
      const walk=(r,d=0)=>{
        if(!r||d>50) return;
        for(const a of (r.querySelectorAll?r.querySelectorAll('a[href*="/video/"]'):[])){
          const m=(a.getAttribute('href')||'').match(/\\/video\\/([A-Za-z0-9_-]{11})/);
          if(!m) continue;
          let row=a;
          for(let i=0;i<12&&row;i++){
            if((row.innerText||'').length>40) break;
            row=row.parentElement;
          }
          out.push({id:m[1], text:((row&&row.innerText)||'').replace(/\\s+/g,' ').trim().slice(0,280)});
        }
        for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
          if(el.shadowRoot) walk(el.shadowRoot,d+1);
      };
      walk(document);
      const map={};
      for(const o of out){
        if(!map[o.id] || o.text.length>(map[o.id].text||'').length) map[o.id]=o;
      }
      return Object.values(map);
    }"""
    )


def click_named(page, name: str) -> bool:
    try:
        loc = page.get_by_role("button", name=re.compile(rf"^{re.escape(name)}$", re.I))
        if loc.count() and loc.last.is_visible():
            loc.last.click(force=True, timeout=2500)
            return True
    except Exception:
        pass
    return bool(
        page.evaluate(
            """(name)=>{
          const re=new RegExp('^'+name.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&')+'$','i');
          const walk=(r,d=0)=>{
            if(!r||d>50) return false;
            for(const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,[role=button],div,span'):[])){
              const t=(el.innerText||'').trim();
              if(re.test(t)){
                const box=el.getBoundingClientRect();
                if(box.width>8 && box.height>8){ el.click(); return true; }
              }
            }
            for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            return false;
          };
          return walk(document);
        }""",
            name,
        )
    )


def video_gone(page, vid: str) -> bool:
    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2000)
    t = body(page, 2500)
    return bool(
        re.search(
            r"not found|doesn't exist|unavailable|no longer available|"
            r"Oops, something went wrong|something went wrong",
            t,
            re.I,
        )
    )


def main() -> int:
    assert urllib.request.urlopen(f"{CDP}/json/version", timeout=2).read()
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = next(
            (p for p in ctx.pages if "studio.youtube.com" in (p.url or "")),
            None,
        ) or ctx.new_page()

        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/short",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3000)
        # Cancel stuck uploads (force-click even if Playwright thinks hidden)
        cancel_notes = []
        for i in range(12):
            hit = page.evaluate(
                """()=>{
              const walk=(r,d=0)=>{
                if(!r||d>50) return false;
                for(const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,[role=button],div'):[])){
                  if(/^Cancel upload$/i.test((el.innerText||'').trim())){
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
            if not hit:
                break
            cancel_notes.append(f"cancel_{i}")
            page.wait_for_timeout(800)
            for name in ["Cancel upload", "Confirm", "Yes", "OK", "Done"]:
                click_named(page, name)
            page.wait_for_timeout(1200)
            page.goto(
                f"https://studio.youtube.com/channel/{CHANNEL}/videos/short",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(2000)

        # Scroll and inventory both tabs
        all_map = {}
        by_tab = {}
        for key, url in [
            ("videos", f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload"),
            ("shorts", f"https://studio.youtube.com/channel/{CHANNEL}/videos/short"),
        ]:
            page.goto(url, wait_until="domcontentloaded", timeout=120000)
            page.wait_for_timeout(2800)
            for _ in range(8):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(500)
            rows = list_rows(page)
            by_tab[key] = rows
            shot(page, f"90_verify_{key}.png")
            for r in rows:
                all_map[r["id"]] = {**r, "tab": key}
            # Detect draft/pending text without id
            t = body(page, 6000)
            by_tab[f"{key}_body_has_draft"] = bool(re.search(r"\bDraft\b|Edit draft", t))
            by_tab[f"{key}_body_has_uploading"] = bool(
                re.search(r"Uploading|Cancel upload|Pending", t, re.I)
            )
            by_tab[f"{key}_snip"] = t[:1200]

        shelf_ids = sorted(all_map.keys())
        non_allow = [i for i in shelf_ids if i not in ALLOWLIST]
        missing_allow = sorted(ALLOWLIST - set(shelf_ids))

        twin_status = {}
        for vid in TWINS:
            twin_status[vid] = {"gone": video_gone(page, vid)}
            shot(page, f"91_twin_{vid}.png")

        allow_status = {}
        for vid in sorted(ALLOWLIST):
            allow_status[vid] = {"gone": video_gone(page, vid)}
            shot(page, f"92_allow_{vid}.png")

        report = {
            "at": datetime.now().isoformat(timespec="seconds"),
            "channelId": CHANNEL,
            "cancel_notes": cancel_notes,
            "shelf_ids": shelf_ids,
            "shelf_count": len(shelf_ids),
            "non_allowlist_left": non_allow,
            "missing_allowlist_from_shelf": missing_allow,
            "twins_gone": {k: v["gone"] for k, v in twin_status.items()},
            "allowlist_gone": {k: v["gone"] for k, v in allow_status.items()},
            "by_tab_counts": {k: len(v) if isinstance(v, list) else v for k, v in by_tab.items() if k in ("videos", "shorts")},
            "draft_upload_flags": {
                "videos_draft": by_tab.get("videos_body_has_draft"),
                "videos_uploading": by_tab.get("videos_body_has_uploading"),
                "shorts_draft": by_tab.get("shorts_body_has_draft"),
                "shorts_uploading": by_tab.get("shorts_body_has_uploading"),
            },
            "ok": (
                not non_allow
                and all(twin_status[t]["gone"] for t in TWINS)
                and all(not allow_status[a]["gone"] for a in ALLOWLIST)
            ),
        }
        # Re-check shelf after cancels
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/short",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(2500)
        shot(page, "93_shorts_final.png")
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(2500)
        shot(page, "94_videos_final.png")

        dump("VERIFY.json", report)
        md = [
            "# HOS hard delete VERIFY — 2026-09-07",
            "",
            f"Channel: `{CHANNEL}`",
            "",
            f"**OK:** {report['ok']}",
            f"**Remaining shelf count:** {report['shelf_count']}",
            "",
            "## Shelf IDs",
            "",
        ]
        for i in shelf_ids:
            md.append(f"- `{i}` {'ALLOWLIST' if i in ALLOWLIST else 'LEFTOVER'}")
        md += ["", "## Deleted twins (gone=True expected)", ""]
        for t in TWINS:
            md.append(f"- `{t}` gone={twin_status[t]['gone']}")
        md += ["", "## Allowlist still present (gone=False expected)", ""]
        for a in sorted(ALLOWLIST):
            md.append(f"- `{a}` gone={allow_status[a]['gone']}")
        md += [
            "",
            f"Non-allowlist left: {non_allow or 'none'}",
            f"Cancel notes: {cancel_notes}",
            f"Draft/upload flags: {report['draft_upload_flags']}",
            "",
        ]
        (EV / "REPORT.md").write_text("\n".join(md) + "\n")
        # Merge into RESULT_FINAL
        dump(
            "RESULT_FINAL.json",
            {
                **report,
                "deleted_ids": TWINS,
                "remaining_shelf_count": report["shelf_count"],
            },
        )
        print(json.dumps(report, indent=2))
        return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
