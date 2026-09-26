#!/usr/bin/env python3
"""Wait for Flow project gallery clip, then download via flow-content.google/video network URL."""
from __future__ import annotations
import argparse, json, re, time, urllib.request
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
    ap.add_argument("--min-thumbs", type=int, default=1)
    args = ap.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    last = "start"
    while time.time() - t0 < args.wait_s:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(CDP)
            ctx = browser.contexts[0]
            page = ctx.new_page()
            captured: list[tuple[str, str]] = []

            def on_resp(resp):
                try:
                    ct = (resp.headers.get("content-type") or "").lower()
                    url = resp.url
                    if resp.status == 200 and ("video/mp4" in ct or ("/video/" in url and "flow-content.google" in url)):
                        captured.append((url, ct))
                except Exception:
                    pass

            page.on("response", on_resp)
            try:
                page.goto(args.project, wait_until="domcontentloaded", timeout=120000)
                time.sleep(3)
                for name in ("Agree", "Accept all"):
                    try:
                        page.get_by_role("button", name=re.compile(name, re.I)).first.click(timeout=1200)
                    except Exception:
                        pass
                try:
                    page.get_by_role("button", name=re.compile(r"^Videos$", re.I)).first.click(timeout=2500)
                    time.sleep(1.5)
                except Exception:
                    pass
                thumbs = page.locator('img[src*="/asb/"]')
                n = thumbs.count()
                body = ""
                try:
                    body = page.inner_text("body")
                except Exception:
                    pass
                pct = None
                m = re.search(r"(\d{1,3})%", body)
                if m:
                    pct = int(m.group(1))
                print(f"poll thumbs={n} pct={pct} elapsed={time.time()-t0:.0f}s captured={len(captured)}", flush=True)
                if n < args.min_thumbs and (pct is None or pct < 100):
                    last = f"waiting gen thumbs={n} pct={pct}"
                    time.sleep(10)
                    continue
                # open newest thumb
                if n == 0:
                    last = "no thumbs yet"
                    time.sleep(8)
                    continue
                thumbs.nth(n - 1).click(timeout=8000)
                time.sleep(3)
                # try open download to stimulate video URL
                try:
                    page.get_by_role("button", name=re.compile(r"Download media", re.I)).first.click(timeout=3000)
                    time.sleep(1)
                except Exception:
                    pass
                # play if possible
                try:
                    page.locator("video").first.click(timeout=2000)
                except Exception:
                    pass
                time.sleep(2)
                if not captured:
                    # wait a bit more for network
                    time.sleep(5)
                cookies = ctx.cookies()
                cookie_hdr = "; ".join(f"{c['name']}={c['value']}" for c in cookies if "google" in (c.get("domain") or ""))
                for url, ct in reversed(captured):
                    try:
                        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Cookie": cookie_hdr})
                        data = urllib.request.urlopen(req, timeout=90).read()
                        tmp = args.out.with_suffix(".tmp.mp4")
                        tmp.write_bytes(data)
                        if is_mp4(tmp):
                            tmp.replace(args.out)
                            print(json.dumps({"ok": True, "bytes": args.out.stat().st_size, "url": url[:120]}))
                            return
                    except Exception as e:
                        last = f"net {e}"
                        print(last, flush=True)
                last = f"opened thumb but no mp4 captured={len(captured)}"
            finally:
                try:
                    page.close()
                except Exception:
                    pass
        time.sleep(5)
    raise SystemExit(f"FAIL after {args.wait_s}s: {last}")


if __name__ == "__main__":
    main()
