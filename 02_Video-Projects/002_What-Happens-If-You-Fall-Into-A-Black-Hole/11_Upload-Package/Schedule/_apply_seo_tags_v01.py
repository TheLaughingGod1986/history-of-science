#!/usr/bin/env python3
"""Apply SEO tags via clipboard paste — single browser session, stable."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = "/Users/ben/code/youtube/.playwright-youtube-profile"
BH = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "002_What-Happens-If-You-Fall-Into-A-Black-Hole"
)
AL = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens"
)
AUDIT = BH / "11_Upload-Package/Schedule/_tag_apply"
OUT = BH / "11_Upload-Package/Schedule/blackhole_tag_apply_result.json"

JOBS = [
    ("bh_s01", "eZGAhF8dN7w", BH / "11_Upload-Package/Tags/blackhole_short-01_tags_v01.txt"),
    ("bh_s02", "C4GuFEFGySI", BH / "11_Upload-Package/Tags/blackhole_short-02_tags_v01.txt"),
    ("bh_s03", "hdlr1soUwNA", BH / "11_Upload-Package/Tags/blackhole_short-03_tags_v01.txt"),
    ("bh_s04", "80S5E-AWFhA", BH / "11_Upload-Package/Tags/blackhole_short-04_tags_v01.txt"),
    ("bh_s05", "olnaYqeOtFs", BH / "11_Upload-Package/Tags/blackhole_short-05_tags_v01.txt"),
    ("bh_s06", "5nMieBeymKU", BH / "11_Upload-Package/Tags/blackhole_short-06_tags_v01.txt"),
    ("aliens_long", "Mo93x0fxB1Q", AL / "11_Upload-Package/Tags/aliens_long_tags_v01.txt"),
    ("aliens_s01", "UWwNKYf_aU8", AL / "11_Upload-Package/Tags/aliens_short-01_tags_v01.txt"),
    ("aliens_s02", "z-DLqoSoEBo", AL / "11_Upload-Package/Tags/aliens_short-02_tags_v01.txt"),
    ("aliens_s03", "MO19iXYCu0c", AL / "11_Upload-Package/Tags/aliens_short-03_tags_v01.txt"),
    ("aliens_s04", "--CxhjNqtSY", AL / "11_Upload-Package/Tags/aliens_short-04_tags_v01.txt"),
]


def skip(page) -> None:
    try:
        page.get_by_role("link", name=re.compile(r"Skip", re.I)).click(timeout=700)
    except Exception:
        pass


def pbcopy(text: str) -> None:
    subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)


def expand_show_more(page) -> None:
    for _ in range(6):
        page.mouse.wheel(0, 700)
        page.wait_for_timeout(140)
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
    page.mouse.wheel(0, 450)
    page.wait_for_timeout(250)


def tags_probe(page):
    return page.evaluate(
        """() => {
          const hits=[];
          const walk=(root)=>{
            if(!root)return;
            for(const el of (root.querySelectorAll?root.querySelectorAll('input'):[])){
              const al=(el.getAttribute('aria-label')||'');
              const ph=(el.getAttribute('placeholder')||'');
              if(/tag/i.test(al+' '+ph)){
                const r=el.getBoundingClientRect();
                if(r.width>20) hits.push({x:r.x+r.width/2,y:r.y+r.height/2});
              }
            }
            for(const el of (root.querySelectorAll?root.querySelectorAll('*'):[])){
              if(el.shadowRoot) walk(el.shadowRoot);
            }
          };
          walk(document);
          return hits;
        }"""
    )


def focus_tags(page) -> bool:
    expand_show_more(page)
    # Prefer role
    try:
        tb = page.get_by_role("textbox", name=re.compile(r"^Tags$", re.I))
        if tb.count():
            tb.first.scroll_into_view_if_needed()
            tb.first.click(force=True)
            page.wait_for_timeout(200)
            return True
    except Exception:
        pass
    probe = tags_probe(page)
    for _ in range(10):
        if probe and probe[0]["y"] <= 820:
            break
        page.mouse.wheel(0, 350)
        page.wait_for_timeout(150)
        probe = tags_probe(page)
    if not probe:
        return False
    page.mouse.click(probe[0]["x"], probe[0]["y"])
    page.wait_for_timeout(200)
    return True


def remove_chips(page) -> int:
    removed = 0
    for _ in range(30):
        pt = page.evaluate(
            """() => {
              const walk=(root)=>{
                if(!root) return null;
                for(const chip of (root.querySelectorAll?root.querySelectorAll('ytcp-chip'):[])){
                  const btn = chip.querySelector('button, ytcp-icon-button, [aria-label*=emove], [aria-label*=Remove]');
                  if(btn){
                    const r=btn.getBoundingClientRect();
                    if(r.width>1) return {x:r.x+r.width/2,y:r.y+r.height/2};
                  }
                }
                for(const el of (root.querySelectorAll?root.querySelectorAll('*'):[])){
                  if(el.shadowRoot){ const x=walk(el.shadowRoot); if(x) return x; }
                }
                return null;
              };
              return walk(document);
            }"""
        )
        if not pt:
            break
        page.mouse.click(pt["x"], pt["y"])
        page.wait_for_timeout(100)
        removed += 1
    return removed


def counter(page) -> tuple[str | None, int]:
    body = page.locator("body").inner_text()
    m = re.search(r"(\d{1,3})\s*/\s*500", body)
    if m:
        return m.group(0), int(m.group(1))
    return None, 0


def save(page) -> bool:
    try:
        b = page.get_by_role("button", name="Save", exact=True)
        if b.count() and b.first.is_enabled():
            b.first.click(force=True)
            page.wait_for_timeout(2500)
            return True
    except Exception:
        pass
    return False


def apply_tags(page, tags: str) -> dict:
    out: dict = {"ok": False}
    if not focus_tags(page):
        out["err"] = "no_tags_input"
        return out
    out["cleared"] = remove_chips(page)
    if not focus_tags(page):
        out["err"] = "lost_focus"
        return out
    # Paste whole comma-separated list, then Enter to commit last chip
    pbcopy(tags)
    page.keyboard.press("Meta+a")
    page.wait_for_timeout(80)
    page.keyboard.press("Meta+v")
    page.wait_for_timeout(400)
    page.keyboard.press("Enter")
    page.wait_for_timeout(500)
    # If paste didn't create chips (some Studio builds need per-tag Enter),
    # fall back to typing tags one-by-one slowly.
    cstr, chars = counter(page)
    out["counter_after_paste"] = cstr
    if chars < 100:
        if not focus_tags(page):
            out["err"] = "refocus_fail"
            return out
        remove_chips(page)
        focus_tags(page)
        for tag in [t.strip() for t in tags.split(",") if t.strip()]:
            page.keyboard.type(tag, delay=12)
            page.keyboard.press("Enter")
            page.wait_for_timeout(90)
        cstr, chars = counter(page)
        out["via"] = "type"
    else:
        out["via"] = "paste"
    out["counter"] = cstr
    out["chars"] = chars
    out["ok"] = chars > 150
    return out


def ensure_page(ctx, page):
    try:
        if page.is_closed():
            return ctx.new_page()
        return page
    except Exception:
        return ctx.new_page()


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    results = []
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            channel="chrome",
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-gpu",
                "--disable-dev-shm-usage",
            ],
            viewport={"width": 1400, "height": 1000},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        for label, vid, path in JOBS:
            tags = path.read_text().strip()
            row: dict = {"label": label, "id": vid, "tag_chars": len(tags)}
            try:
                page = ensure_page(ctx, page)
                page.goto(
                    f"https://studio.youtube.com/video/{vid}/edit",
                    wait_until="domcontentloaded",
                    timeout=90000,
                )
                page.wait_for_timeout(2800)
                skip(page)
                try:
                    row["title"] = (page.locator("#textbox").first.inner_text() or "")[:100]
                except Exception:
                    row["title"] = ""
                row["tags"] = apply_tags(page, tags)
                page.screenshot(path=str(AUDIT / f"{label}_{vid}_pre_save.png"))
                row["saved"] = save(page)
                page.wait_for_timeout(1200)
                # quick verify without full reload if possible
                page.reload(wait_until="domcontentloaded", timeout=90000)
                page.wait_for_timeout(2800)
                skip(page)
                expand_show_more(page)
                cstr, chars = counter(page)
                row["verify_counter"] = cstr
                row["verify_chars"] = chars
                sample = tags.split(",")[0].strip().lower()
                body = page.locator("body").inner_text().lower()
                row["verify_sample"] = sample in body
                row["ok"] = bool(row.get("saved") and chars > 150)
                page.screenshot(path=str(AUDIT / f"{label}_{vid}_verify.png"))
                print(
                    f"{label} {vid}: via={row['tags'].get('via')} "
                    f"saved={row['saved']} verify={cstr} sample={row['verify_sample']} ok={row['ok']}",
                    flush=True,
                )
            except Exception as e:
                row["ok"] = False
                row["err"] = str(e)[:260]
                print(f"{label} {vid}: ERR {row['err']}", flush=True)
                # recover page
                try:
                    page = ctx.new_page()
                except Exception:
                    pass
            results.append(row)
            OUT.write_text(
                json.dumps(
                    {
                        "results": results,
                        "ok": all(r.get("ok") for r in results),
                        "failed": [r for r in results if not r.get("ok")],
                    },
                    indent=2,
                )
            )
        ctx.close()
    failed = [r for r in results if not r.get("ok")]
    print(
        json.dumps(
            {
                "ok": not failed,
                "passed": sum(1 for r in results if r.get("ok")),
                "failed": [
                    {
                        "label": r["label"],
                        "id": r["id"],
                        "verify": r.get("verify_counter"),
                        "err": r.get("err"),
                    }
                    for r in failed
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
