#!/usr/bin/env python3
"""Batch-delete @OpptiAI comments from Orbit Studio Community inbox."""
from __future__ import annotations

import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = "/Users/ben/code/youtube/.playwright-youtube-profile"
PKG = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens/11_Upload-Package"
)
AUDIT = PKG / "Schedule/_studio_audit_shorts_v001"
OUT = PKG / "Schedule/aliens_cleanup_oppti_comments_v03.json"
ORBIT = "TBD_CREATE_HISTORY_OF_SCIENCE_CHANNEL"
LONG_ID = "Mo93x0fxB1Q"
PINNED = (PKG / "Pinned-Comments/aliens_long_pinned-comment_v01.txt").read_text().strip()
NEEDLE = "best explains the silence"


def skip(page):
    try:
        page.get_by_role("link", name=re.compile(r"Skip", re.I)).click(timeout=800)
    except Exception:
        pass


def main():
    AUDIT.mkdir(parents=True, exist_ok=True)
    result: dict = {"ok": False, "actions": []}

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 1100},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        page.goto(
            f"https://studio.youtube.com/channel/{ORBIT}/comments/inbox",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(5000)
        skip(page)
        page.screenshot(path=str(AUDIT / "cleanup_v03_inbox.png"), full_page=True)

        # Select all OpptiAI comment checkboxes via JS
        for round_i in range(8):
            selected = page.evaluate(
                """() => {
                  const rows=[...document.querySelectorAll(
                    'ytcp-comment-thread, ytcp-comment, ytcp-comments-table-row, tr, ytcp-entity-card'
                  )];
                  let n=0;
                  const walk=(root)=>{
                    for (const el of root.querySelectorAll('*')) {
                      const t=(el.innerText||'');
                      if (!/@OpptiAI|@opptiai/i.test(t)) continue;
                      if (!/best explains the silence|Orbit.s next film/i.test(t)) continue;
                      // find checkbox in this subtree / ancestors
                      let node=el;
                      for (let i=0;i<8 && node;i++) {
                        const cb=node.querySelector(
                          'tp-yt-paper-checkbox, input[type=checkbox], ytcp-checkbox-lit, [role=checkbox]'
                        );
                        if (cb) {
                          const r=cb.getBoundingClientRect();
                          if (r.width>5) { cb.click(); n++; break; }
                        }
                        node=node.parentElement;
                      }
                    }
                  };
                  walk(document);
                  // also select by aria
                  for (const cb of document.querySelectorAll(
                    'tp-yt-paper-checkbox, [role=checkbox], input[type=checkbox]'
                  )) {
                    // only those near Oppti text
                    const row=cb.closest('ytcp-comment-thread, ytcp-comment, tr, ytcp-entity-card, div');
                    const t=row?.innerText||'';
                    if (/@OpptiAI/i.test(t) && /silence/i.test(t)) {
                      const checked=cb.getAttribute('aria-checked')==='true' || cb.checked;
                      if (!checked) { cb.click(); n++; }
                    }
                  }
                  return n;
                }"""
            )
            result["actions"].append({"round": round_i, "selected": selected})
            page.screenshot(path=str(AUDIT / f"cleanup_v03_sel_{round_i}.png"))
            if not selected:
                # try clicking each "Select comment for batch" button near Oppti
                clicked = page.evaluate(
                    """() => {
                      let n=0;
                      for (const b of document.querySelectorAll(
                        'button[aria-label*="Select comment"], ytcp-icon-button[aria-label*="Select comment"], [aria-label*="Select comment for batch"]'
                      )) {
                        // check nearby text
                        const row=b.closest('ytcp-comment, ytcp-comment-thread, div');
                        const t=row?.innerText||'';
                        if (/@OpptiAI/i.test(t)) { b.click(); n++; }
                      }
                      return n;
                    }"""
                )
                result["actions"].append({"batch_select": clicked})
                if not clicked:
                    break
            page.wait_for_timeout(600)

            # Click Delete toolbar button
            del_btn = page.evaluate(
                """() => {
                  for (const b of document.querySelectorAll(
                    'button, ytcp-button, yt-button-shape button, [role=button]'
                  )) {
                    const t=(b.innerText||b.getAttribute('aria-label')||'').trim();
                    if (/^Delete$/i.test(t) || /Delete selected/i.test(t)) {
                      const r=b.getBoundingClientRect();
                      if (r.width>10 && r.y<200) { b.click(); return t; }
                    }
                  }
                  // any visible Delete in toolbar
                  for (const b of document.querySelectorAll('button, ytcp-button')) {
                    const t=(b.innerText||'').trim();
                    if (/^Delete$/i.test(t)) { b.click(); return 'Delete-any'; }
                  }
                  return null;
                }"""
            )
            result["actions"].append({"delete_btn": del_btn})
            page.wait_for_timeout(900)
            page.screenshot(path=str(AUDIT / f"cleanup_v03_del_{round_i}.png"))
            # confirm
            page.evaluate(
                """() => {
                  for (const b of document.querySelectorAll('button, ytcp-button, yt-button-shape button')) {
                    const t=(b.innerText||'').trim();
                    if (/^Delete$/i.test(t) || /^Confirm$/i.test(t)) { b.click(); return t; }
                  }
                }"""
            )
            page.wait_for_timeout(2500)
            page.reload(wait_until="domcontentloaded")
            page.wait_for_timeout(4000)
            skip(page)
            body = page.locator("body").inner_text()
            if not re.search(r"@OpptiAI|@opptiai", body, re.I):
                break

        page.screenshot(path=str(AUDIT / "cleanup_v03_after.png"), full_page=True)
        body = page.locator("body").inner_text()
        result["inbox_has_oppti"] = bool(re.search(r"@OpptiAI|@opptiai", body, re.I))

        # Per-row delete fallback
        if result["inbox_has_oppti"]:
            for round_i in range(10):
                hit = page.evaluate(
                    """() => {
                      const nodes=[...document.querySelectorAll('*')];
                      for (const el of nodes) {
                        const t=(el.innerText||'');
                        if (t.length>800 || t.length<40) continue;
                        if (!/@OpptiAI/i.test(t)) continue;
                        if (!/silence/i.test(t)) continue;
                        const r=el.getBoundingClientRect();
                        if (r.width<100 || r.height<40) continue;
                        // find action button to the right
                        let row=el;
                        for (let i=0;i<6;i++) {
                          const btns=[...row.querySelectorAll(
                            'ytcp-icon-button, button[aria-label*="Action"], button[aria-label*="More"]'
                          )];
                          for (const b of btns) {
                            const al=b.getAttribute('aria-label')||'';
                            if (/Action|More|options/i.test(al)) {
                              b.click(); return al;
                            }
                          }
                          // rightmost small button
                          const all=[...row.querySelectorAll('ytcp-icon-button, button')].map(b=>{
                            const rr=b.getBoundingClientRect();
                            return {b,x:rr.x,w:rr.width,h:rr.height};
                          }).filter(x=>x.w>8&&x.w<50&&x.h>8&&x.h<50);
                          all.sort((a,b)=>b.x-a.x);
                          if (all[0]) { all[0].b.click(); return 'rightmost'; }
                          row=row.parentElement;
                          if (!row) break;
                        }
                      }
                      return null;
                    }"""
                )
                if not hit:
                    break
                page.wait_for_timeout(700)
                page.evaluate(
                    """() => {
                      for (const n of document.querySelectorAll(
                        'tp-yt-paper-item, [role=menuitem], span'
                      )) {
                        if (/^Delete$/i.test((n.innerText||'').trim())) { n.click(); return; }
                      }
                    }"""
                )
                page.wait_for_timeout(800)
                page.evaluate(
                    """() => {
                      for (const b of document.querySelectorAll('button, ytcp-button')) {
                        if (/^Delete$/i.test((b.innerText||'').trim())) { b.click(); return; }
                      }
                    }"""
                )
                page.wait_for_timeout(2000)
                result["actions"].append({"row_delete": hit})
                page.reload(wait_until="domcontentloaded")
                page.wait_for_timeout(3500)
                skip(page)
                if not re.search(
                    r"@OpptiAI", page.locator("body").inner_text(), re.I
                ):
                    break

        page.screenshot(path=str(AUDIT / "cleanup_v03_final_inbox.png"), full_page=True)
        body = page.locator("body").inner_text()
        result["inbox_has_oppti"] = bool(re.search(r"@OpptiAI|@opptiai", body, re.I))

        # Verify watch
        page.goto(
            f"https://www.youtube.com/watch?v={LONG_ID}",
            wait_until="domcontentloaded",
        )
        page.wait_for_timeout(5000)
        page.evaluate("window.scrollTo(0, 1200)")
        page.wait_for_timeout(2000)
        wbody = page.locator("body").inner_text()
        result["watch_has_oppti"] = bool(re.search(r"opptiai|OpptiAI", wbody, re.I))
        result["watch_has_needle"] = NEEDLE in wbody
        page.screenshot(path=str(AUDIT / "cleanup_v03_watch.png"), full_page=True)

        # Post ONE Orbit comment if clean
        if not result["watch_has_oppti"] and not result["watch_has_needle"]:
            # switch comment identity to Orbit
            page.evaluate(
                "() => document.querySelector('#simplebox-placeholder, #placeholder-area')?.click()"
            )
            page.wait_for_timeout(600)
            page.evaluate(
                """() => {
                  document.querySelector(
                    'ytd-comment-simplebox-renderer #author-thumbnail button, #author-thumbnail'
                  )?.click();
                }"""
            )
            page.wait_for_timeout(800)
            page.evaluate(
                """() => {
                  for (const n of document.querySelectorAll(
                    'ytd-account-item-renderer, tp-yt-paper-item, yt-formatted-string'
                  )) {
                    if (/History of Science/i.test(n.innerText||'')) { n.click(); return; }
                  }
                }"""
            )
            page.wait_for_timeout(800)
            page.screenshot(path=str(AUDIT / "cleanup_v03_id.png"))
            typed = page.evaluate(
                """(text) => {
                  const root=document.querySelector(
                    'ytd-commentbox #contenteditable-root, #contenteditable-root'
                  );
                  if (!root) return false;
                  root.focus();
                  root.innerText=text;
                  root.dispatchEvent(new InputEvent('input',{bubbles:true,data:text}));
                  return true;
                }""",
                PINNED,
            )
            page.wait_for_timeout(400)
            page.evaluate(
                """() => {
                  const b=document.querySelector('#submit-button button');
                  if (b && !b.disabled) b.click();
                }"""
            )
            page.wait_for_timeout(3500)
            result["posted"] = {"typed": typed}
            page.reload(wait_until="domcontentloaded")
            page.wait_for_timeout(4000)
            page.evaluate("window.scrollTo(0, 1200)")
            page.wait_for_timeout(1500)
            wbody = page.locator("body").inner_text()
            result["final_authors"] = page.evaluate(
                """(needle) => [...document.querySelectorAll('ytd-comment-thread-renderer')]
                  .filter(t=>(t.innerText||'').includes(needle))
                  .map(t=>(t.querySelector('#author-text')?.innerText||'').trim())""",
                NEEDLE,
            )
            result["final_has_oppti"] = bool(
                re.search(r"opptiai|OpptiAI", wbody, re.I)
            )

        result["ok"] = (not result.get("inbox_has_oppti")) and (
            not result.get("final_has_oppti", result.get("watch_has_oppti"))
        )
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2)[:2500], flush=True)
        ctx.close()
        raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
