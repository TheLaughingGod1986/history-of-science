#!/usr/bin/env python3
"""Harvest a Flow gallery mp4 into --out via live Chrome CDP (no fresh profile)."""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow  # noqa: E402

flow.FLOW_HOME = os.environ.get("ORBIT_FLOW_HOME", "https://flow.google.com/")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--project", required=True, help="Flow project URL")
    ap.add_argument("--project-url", dest="project_alias", default=None)
    ap.add_argument("--index", type=int, default=-1, help="Gallery thumb index (default newest)")
    ap.add_argument(
        "--wait-s",
        type=int,
        default=int(os.environ.get("HOS_FLOW_HARVEST_WAIT_S", "480")),
    )
    ap.add_argument(
        "--before-thumbs",
        type=int,
        default=int(os.environ.get("HOS_FLOW_BEFORE_THUMBS", "-1")),
    )
    ap.add_argument(
        "--cdp",
        default=os.environ.get("ORBIT_FLOW_CDP", "http://127.0.0.1:9222"),
    )
    args = ap.parse_args()
    if args.project_alias and not args.project:
        args.project = args.project_alias
    if not args.project:
        ap.error("--project required")

    from playwright.sync_api import sync_playwright
    from playwright.sync_api import Error as PlaywrightError

    try:
        from playwright._impl._errors import TargetClosedError
    except Exception:  # pragma: no cover
        TargetClosedError = PlaywrightError  # type: ignore[misc, assignment]

    cdp = args.cdp
    require_cdp = os.environ.get("HOS_FLOW_REQUIRE_CDP", "1") == "1"
    if not require_cdp:
        raise SystemExit("STOP_TO_COS: harvest requires CDP (HOS_FLOW_REQUIRE_CDP=1)")

    t0 = time.time()
    last_err = "not started"
    args.out.parent.mkdir(parents=True, exist_ok=True)

    while time.time() - t0 < args.wait_s:
        with sync_playwright() as p:
            print(f"harvest CDP attach {cdp}", flush=True)
            browser = p.chromium.connect_over_cdp(cdp)
            ctx = browser.contexts[0]
            page = ctx.new_page()
            captured: list[bytes] = []
            try:
                page.goto(args.project, wait_until="domcontentloaded", timeout=120_000)
                page.wait_for_timeout(4000)
                flow.dismiss_banners(page)
                thumbs = flow.collect_gallery_asb_srcs(page)
                print(
                    f"harvest poll thumbs={len(thumbs)} elapsed={time.time() - t0:.0f}s url={page.url}",
                    flush=True,
                )
                # Still generating?
                body = ""
                try:
                    body = page.inner_text("body")
                except Exception:
                    pass
                if any(x in body.lower() for x in ("% ", "generating", "in progress")) and len(thumbs) <= max(args.before_thumbs, 0):
                    last_err = "generation still running"
                    print(f"  {last_err}", flush=True)
                    page.wait_for_timeout(8000)
                    continue

                if args.before_thumbs >= 0 and len(thumbs) <= args.before_thumbs:
                    last_err = f"waiting for new thumb (have={len(thumbs)} before={args.before_thumbs})"
                    print(f"  {last_err}", flush=True)
                elif not thumbs:
                    last_err = "no gallery thumbs yet"
                    print(f"  {last_err}", flush=True)
                else:
                    if args.index >= 0:
                        candidates = [max(0, min(args.index, len(thumbs) - 1))]
                    else:
                        candidates = list(range(len(thumbs) - 1, -1, -1))[:5]
                    for idx in candidates:
                        src = thumbs[idx]
                        before = set(thumbs) - {src}
                        if args.out.exists():
                            args.out.unlink()
                        print(f"harvest try idx={idx}/{len(thumbs)} -> {args.out}", flush=True)
                        try:
                            got = flow.harvest_agent_gallery_mp4(
                                page, args.out, captured, before_asb=before
                            )
                        except TargetClosedError as e:
                            last_err = f"idx={idx} target_closed: {e}"
                            print(f"  {last_err}", flush=True)
                            break
                        except PlaywrightError as e:
                            last_err = f"idx={idx} playwright: {e}"
                            print(f"  {last_err}", flush=True)
                            break
                        if got and args.out.exists() and args.out.stat().st_size >= 400_000:
                            print(f"OK bytes={args.out.stat().st_size} via={got}", flush=True)
                            try:
                                page.close()
                            except Exception:
                                pass
                            return
                        last_err = f"idx={idx} got={got}"
                        print(f"  {last_err}", flush=True)
                        try:
                            page.keyboard.press("Escape")
                            page.wait_for_timeout(400)
                        except Exception:
                            pass
            except Exception as e:
                last_err = f"loop err: {e}"
                print(f"  {last_err}", flush=True)
            finally:
                try:
                    page.close()
                except Exception:
                    pass
        time.sleep(4)

    raise SystemExit(f"FAIL harvest after {args.wait_s}s: {last_err}")


if __name__ == "__main__":
    main()
