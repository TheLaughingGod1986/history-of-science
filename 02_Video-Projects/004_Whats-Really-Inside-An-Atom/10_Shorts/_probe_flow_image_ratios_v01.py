#!/usr/bin/env python3
"""Probe Flow Image / Nano Banana aspect options on CDP :9222 (NEW tab only)."""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow  # noqa: E402

CDP = os.environ.get("ORBIT_FLOW_CDP", "http://127.0.0.1:9222")
PINNED = os.environ.get(
    "HOS_FLOW_PROJECT_URL",
    "https://flow.google.com/project/30a34afb-8d9c-4eac-83ba-012d97f6b1b5",
)
OUT = Path(__file__).resolve().parent / "covers_live_v02" / "stills" / "_qa_mint"


def main() -> int:
    from playwright.sync_api import sync_playwright

    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        page = ctx.new_page()
        try:
            page.goto(PINNED, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2500)
            flow.dismiss_banners(page)
            # Open settings pill
            flow._open_prompt_settings_pill(page)
            page.wait_for_timeout(900)
            # Click Image / Banana
            page.evaluate(
                """() => {
                  for (const b of document.querySelectorAll('button,[role=radio],[role=tab]')) {
                    const t = ((b.innerText||'')+' '+(b.getAttribute('aria-label')||'')).trim();
                    if ((/\\bimage\\b/i.test(t) || /banana/i.test(t)) && !/video|veo|omni/i.test(t)) {
                      b.click(); return t.slice(0,80);
                    }
                  }
                  return null;
                }"""
            )
            page.wait_for_timeout(700)
            page.screenshot(path=str(OUT / "probe_settings_open.png"), full_page=False)
            dump = page.evaluate(
                """() => {
                  const nodes = [...document.querySelectorAll(
                    'button,[role=radio],[role=option],[role=menuitem],label,span'
                  )];
                  const out = [];
                  for (const b of nodes) {
                    const t = ((b.innerText||'')+' '+(b.getAttribute('aria-label')||'')
                               +' '+(b.getAttribute('data-value')||'')).trim().replace(/\\n/g,' ');
                    if (!t || t.length > 90) continue;
                    if (/crop_|\\d\\s*[:×x]\\s*\\d|portrait|landscape|square|banana|image|video|9:16|3:4|16:9|1:1|4:3|4:5|2:3/i.test(t)) {
                      const r = b.getBoundingClientRect();
                      if (r.width < 6 || r.height < 6) continue;
                      out.push({t:t.slice(0,90), w:Math.round(r.width), h:Math.round(r.height),
                                role:b.getAttribute('role'), tag:b.tagName});
                    }
                  }
                  // dedupe
                  const seen = new Set();
                  return out.filter(x => { if (seen.has(x.t)) return false; seen.add(x.t); return true; });
                }"""
            )
            (OUT / "probe_ratio_options.json").write_text(json.dumps(dump, indent=2) + "\n")
            print(json.dumps(dump, indent=2))
            pill = page.evaluate(
                """() => {
                  for (const b of document.querySelectorAll('button')) {
                    const t = (b.innerText || '').trim().replace(/\\n/g, ' ');
                    if (/Nano Banana|Video ·|Omni|Veo|crop_|Image/i.test(t)) {
                      const r = b.getBoundingClientRect();
                      if (r.width > 40 && r.height > 16) return t.slice(0, 140);
                    }
                  }
                  return '';
                }"""
            )
            print("PILL", pill)
            return 0
        finally:
            try:
                page.close()
            except Exception:
                pass


if __name__ == "__main__":
    raise SystemExit(main())
