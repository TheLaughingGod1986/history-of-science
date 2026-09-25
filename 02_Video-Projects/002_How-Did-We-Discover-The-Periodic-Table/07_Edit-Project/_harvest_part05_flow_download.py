#!/usr/bin/env python3
"""Harvest Flow project mp4 via CDP: open generated-video thumb → Download → 720p.

P04 lesson: submit scripts time out on download; harvest later from project_url.
"""
from __future__ import annotations
import argparse, re, time
from pathlib import Path
from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"


def is_mp4(path: Path) -> bool:
    if not path.exists() or path.stat().st_size < 400_000:
        return False
    head = path.read_bytes()[:64]
    return b"ftyp" in head and not head.startswith(b"\xff\xd8\xff")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--wait-s", type=int, default=600)
    args = ap.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    last = "start"
    while time.time() - t0 < args.wait_s:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(CDP)
            page = browser.contexts[0].new_page()
            try:
                page.goto(args.project, wait_until="domcontentloaded", timeout=120000)
                time.sleep(3)
                for name in ("Agree", "Accept all"):
                    try:
                        page.get_by_role("button", name=re.compile(name, re.I)).first.click(timeout=1200)
                    except Exception:
                        pass
                thumbs = page.locator('img[alt*="Generated video" i], img[src*="/asb/"]')
                n = thumbs.count()
                print(f"poll thumbs={n} elapsed={time.time()-t0:.0f}s", flush=True)
                if n == 0:
                    last = "no thumbs"
                    time.sleep(8)
                    continue
                target = None
                for i in range(n):
                    alt = (thumbs.nth(i).get_attribute("alt") or "").lower()
                    if "generated video" in alt:
                        target = thumbs.nth(i)
                        break
                if target is None:
                    target = thumbs.nth(n - 1)
                target.click(timeout=8000)
                time.sleep(2)
                opened = False
                for loc in (
                    page.get_by_role("button", name=re.compile(r"Download media", re.I)),
                    page.locator('button[aria-label*="Download" i]'),
                    page.get_by_text("Download media", exact=False),
                ):
                    try:
                        if loc.count() and loc.first.is_visible():
                            loc.first.click(timeout=4000, force=True)
                            opened = True
                            time.sleep(1)
                            break
                    except Exception:
                        pass
                if not opened:
                    last = "no download menu"
                    page.keyboard.press("Escape")
                    time.sleep(5)
                    continue
                for lab in (r"720p", r"Original size", r"Download$"):
                    try:
                        with page.expect_download(timeout=90000) as di:
                            page.get_by_text(re.compile(lab, re.I)).first.click(timeout=4000, force=True)
                        dl = di.value
                        tmp = args.out.with_suffix(".dl.tmp.mp4")
                        dl.save_as(str(tmp))
                        if is_mp4(tmp):
                            tmp.replace(args.out)
                            print(f"OK bytes={args.out.stat().st_size} via={lab}", flush=True)
                            return
                        last = f"bad download bytes={tmp.stat().st_size if tmp.exists() else 0}"
                    except Exception as e:
                        last = f"dl {lab}: {e}"
                        print(last, flush=True)
                try:
                    page.keyboard.press("Escape")
                except Exception:
                    pass
            finally:
                try:
                    page.close()
                except Exception:
                    pass
        time.sleep(6)
    raise SystemExit(f"FAIL after {args.wait_s}s: {last}")


if __name__ == "__main__":
    main()
