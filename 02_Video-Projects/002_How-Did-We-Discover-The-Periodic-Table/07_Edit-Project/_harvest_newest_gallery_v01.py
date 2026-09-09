#!/usr/bin/env python3
"""Harvest Flow gallery mp4 via live Chrome CDP (network video URL + Download)."""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import time
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow  # noqa: E402

flow.FLOW_HOME = os.environ.get("ORBIT_FLOW_HOME", "https://flow.google.com/")


def is_mp4(path: Path) -> bool:
    if not path.exists() or path.stat().st_size < 400_000:
        return False
    head = path.read_bytes()[:64]
    return b"ftyp" in head and not head.startswith(b"\xff\xd8\xff")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--project", required=True)
    ap.add_argument("--project-url", dest="project_alias", default=None)
    ap.add_argument("--index", type=int, default=-1)
    ap.add_argument("--wait-s", type=int, default=int(os.environ.get("HOS_FLOW_HARVEST_WAIT_S", "480")))
    ap.add_argument("--before-thumbs", type=int, default=int(os.environ.get("HOS_FLOW_BEFORE_THUMBS", "-1")))
    ap.add_argument("--cdp", default=os.environ.get("ORBIT_FLOW_CDP", "http://127.0.0.1:9222"))
    args = ap.parse_args()
    if args.project_alias:
        args.project = args.project_alias
    if os.environ.get("HOS_FLOW_REQUIRE_CDP", "1") != "1":
        raise SystemExit("STOP_TO_COS: harvest requires CDP")

    from playwright.sync_api import sync_playwright

    args.out.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    last = "not started"
    while time.time() - t0 < args.wait_s:
        with sync_playwright() as p:
            print(f"harvest CDP attach {args.cdp}", flush=True)
            browser = p.chromium.connect_over_cdp(args.cdp)
            ctx = browser.contexts[0]
            page = ctx.new_page()
            captured: list[tuple[str, str]] = []

            def on_response(resp):
                try:
                    ct = (resp.headers.get("content-type") or "").lower()
                    url = resp.url
                    if resp.status == 200 and (
                        "video/mp4" in ct
                        or ("/video/" in url and "flow-content.google" in url)
                        or "googlevideo" in url
                    ):
                        captured.append((url, ct))
                except Exception:
                    pass

            page.on("response", on_response)
            try:
                page.goto(args.project, wait_until="domcontentloaded", timeout=120_000)
                page.wait_for_timeout(3000)
                flow.dismiss_banners(page)
                # Videos tab
                try:
                    page.get_by_role("button", name=re.compile(r"^Videos$", re.I)).first.click(timeout=2500)
                    page.wait_for_timeout(1500)
                except Exception:
                    pass
                thumbs = flow.collect_gallery_asb_srcs(page)
                print(f"harvest poll thumbs={len(thumbs)} elapsed={time.time()-t0:.0f}s", flush=True)
                if args.before_thumbs >= 0 and len(thumbs) <= args.before_thumbs:
                    last = f"waiting new thumb have={len(thumbs)} before={args.before_thumbs}"
                    print(" ", last, flush=True)
                    page.wait_for_timeout(8000)
                    continue
                if not thumbs:
                    last = "no thumbs"
                    print(" ", last, flush=True)
                    page.wait_for_timeout(8000)
                    continue

                idxs = [max(0, min(args.index, len(thumbs)-1))] if args.index >= 0 else list(range(len(thumbs)-1, -1, -1))[:3]
                for idx in idxs:
                    # click matching asb img
                    src = thumbs[idx]
                    print(f"harvest try idx={idx} src={src[-40:]}", flush=True)
                    loc = page.locator(f'img[src="{src}"], video[src="{src}"]')
                    try:
                        if loc.count():
                            loc.first.click(timeout=8000)
                        else:
                            page.locator('img[src*="/asb/"]').nth(idx).click(timeout=8000)
                    except Exception as e:
                        last = f"thumb click {e}"
                        print(" ", last, flush=True)
                        continue
                    page.wait_for_timeout(2500)

                    # Prefer network video URL (most reliable on this Mini CDP session)
                    if captured:
                        cookies = ctx.cookies()
                        cookie_hdr = "; ".join(
                            f"{c['name']}={c['value']}"
                            for c in cookies
                            if "google" in (c.get("domain") or "")
                        )
                        for url, ct in reversed(captured):
                            if "video" not in ct and "/video/" not in url:
                                continue
                            try:
                                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Cookie": cookie_hdr})
                                data = urllib.request.urlopen(req, timeout=90).read()
                                tmp = args.out.with_suffix(".net.tmp.mp4")
                                tmp.write_bytes(data)
                                if is_mp4(tmp):
                                    tmp.replace(args.out)
                                    print(f"OK net bytes={args.out.stat().st_size} {url[:90]}", flush=True)
                                    page.close()
                                    return
                            except Exception as e:
                                last = f"net {e}"
                                print(" ", last, flush=True)

                    # Download menu fallback
                    try:
                        page.get_by_role("button", name=re.compile(r"Download media", re.I)).first.click(timeout=4000)
                        page.wait_for_timeout(800)
                        with page.expect_download(timeout=60000) as di:
                            page.get_by_role("menuitem", name=re.compile(r"720p|Original", re.I)).first.click(timeout=5000)
                        dl = di.value
                        tmp = args.out.with_suffix(".dl.tmp.mp4")
                        dl.save_as(str(tmp))
                        if is_mp4(tmp):
                            tmp.replace(args.out)
                            print(f"OK download bytes={args.out.stat().st_size}", flush=True)
                            page.close()
                            return
                    except Exception as e:
                        last = f"download {e}"
                        print(" ", last, flush=True)

                    # library harvest helper
                    try:
                        captured_bytes: list[bytes] = []
                        got = flow.harvest_agent_gallery_mp4(
                            page, args.out, captured_bytes, before_asb=set(thumbs) - {src}
                        )
                        if got and is_mp4(args.out):
                            print(f"OK helper via={got} bytes={args.out.stat().st_size}", flush=True)
                            page.close()
                            return
                        last = f"helper got={got}"
                    except Exception as e:
                        last = f"helper {e}"
                        print(" ", last, flush=True)
            finally:
                try:
                    page.close()
                except Exception:
                    pass
        time.sleep(3)

    raise SystemExit(f"FAIL harvest after {args.wait_s}s: {last}")


if __name__ == "__main__":
    main()
