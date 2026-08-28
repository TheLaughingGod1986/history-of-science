#!/usr/bin/env python3
"""Audit tags one video at a time with crash recovery."""
from __future__ import annotations

import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = "/Users/ben/code/youtube/.playwright-youtube-profile"
ROOT = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "002_What-Happens-If-You-Fall-Into-A-Black-Hole"
)
AUDIT = ROOT / "11_Upload-Package/Schedule/_tag_audit"
OUT = ROOT / "11_Upload-Package/Schedule/blackhole_tag_audit_result.json"

VIDEOS = [
    ("long", "n7CbJrOCnU0"),
    ("s01", "eZGAhF8dN7w"),
    ("s02", "C4GuFEFGySI"),
    ("s03", "hdlr1soUwNA"),
    ("s04", "80S5E-AWFhA"),
    ("s05", "olnaYqeOtFs"),
    ("s06", "5nMieBeymKU"),
    # extras discovered on channel content list
    ("extra_a", "--CxhjNqtSY"),
    ("extra_b", "MO19iXYCu0c"),
    ("extra_c", "Mo93x0fxB1Q"),
    ("extra_d", "UWwNKYf_aU8"),
    ("extra_e", "z-DLqoSoEBo"),
]


def skip(page) -> None:
    try:
        page.get_by_role("link", name=re.compile(r"Skip", re.I)).click(timeout=800)
    except Exception:
        pass


def expand_show_more(page) -> None:
    for _ in range(6):
        page.mouse.wheel(0, 800)
        page.wait_for_timeout(180)
    try:
        page.get_by_text("Show more", exact=True).first.click(force=True, timeout=2000)
        page.wait_for_timeout(600)
    except Exception:
        try:
            page.get_by_role("button", name=re.compile(r"Show more", re.I)).first.click(
                force=True, timeout=2000
            )
            page.wait_for_timeout(600)
        except Exception:
            pass
    page.mouse.wheel(0, 500)
    page.wait_for_timeout(300)


def read_tags(page) -> dict:
    expand_show_more(page)
    chips = page.evaluate(
        """() => {
          const chips = [];
          const walk = (root) => {
            if (!root) return;
            for (const el of (root.querySelectorAll ? root.querySelectorAll('ytcp-chip') : [])) {
              const t = (el.innerText || '').replace(/\\s+/g, ' ').trim().split('\\n')[0].trim();
              if (t && t.length < 80 && !/^×$/.test(t)) chips.push(t);
            }
            for (const el of (root.querySelectorAll ? root.querySelectorAll('*') : [])) {
              if (el.shadowRoot) walk(el.shadowRoot);
            }
          };
          walk(document);
          return [...new Set(chips)];
        }"""
    )
    body = page.locator("body").inner_text()
    m = re.search(r"(\d{1,3})\s*/\s*500", body)
    counter = m.group(0) if m else None
    chars = int(m.group(1)) if m else 0
    return {
        "chips": chips,
        "chip_count": len(chips),
        "counter": counter,
        "chars": chars,
        "has_tags": chars > 0 or len(chips) > 0,
        "weak": chars < 200 and len(chips) < 8,
    }


def audit_one(playwright, tag: str, vid: str) -> dict:
    row: dict = {"tag": tag, "id": vid}
    ctx = playwright.chromium.launch_persistent_context(
        PROFILE,
        headless=False,
        channel="chrome",
        args=["--disable-blink-features=AutomationControlled"],
        viewport={"width": 1400, "height": 1000},
    )
    try:
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(
            f"https://studio.youtube.com/video/{vid}/edit",
            wait_until="domcontentloaded",
            timeout=90000,
        )
        page.wait_for_timeout(3000)
        skip(page)
        try:
            row["title"] = (page.locator("#textbox").first.inner_text() or "")[:140]
        except Exception:
            row["title"] = ""
        tags = read_tags(page)
        row.update(tags)
        page.screenshot(path=str(AUDIT / f"{tag}_{vid}_tags.png"), full_page=False)
        print(
            f"{tag} {vid}: chars={tags.get('counter')} chips={tags.get('chip_count')} "
            f"has={tags.get('has_tags')} weak={tags.get('weak')} title={row.get('title','')[:50]!r}",
            flush=True,
        )
    except Exception as e:
        row["err"] = str(e)[:260]
        print(f"{tag} {vid}: ERR {row['err']}", flush=True)
    finally:
        try:
            ctx.close()
        except Exception:
            pass
    return row


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    # Resume from previous if present
    prev = {}
    if OUT.exists():
        try:
            prev = {v["id"]: v for v in json.loads(OUT.read_text()).get("videos", []) if v.get("has_tags") and not v.get("err")}
        except Exception:
            prev = {}

    results = []
    with sync_playwright() as p:
        for tag, vid in VIDEOS:
            if vid in prev and not prev[vid].get("weak"):
                print(f"{tag} {vid}: skip (already audited OK)", flush=True)
                results.append(prev[vid])
                continue
            results.append(audit_one(p, tag, vid))

    out = {
        "videos": results,
        "missing_or_weak": [v for v in results if (not v.get("has_tags")) or v.get("weak") or v.get("err")],
        "ok": all(v.get("has_tags") and not v.get("weak") and not v.get("err") for v in results),
    }
    OUT.write_text(json.dumps(out, indent=2))
    print(
        json.dumps(
            {
                "ok": out["ok"],
                "count": len(results),
                "weak_or_missing": [
                    {"tag": v["tag"], "id": v["id"], "chars": v.get("chars"), "chips": v.get("chip_count"), "err": v.get("err")}
                    for v in out["missing_or_weak"]
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
