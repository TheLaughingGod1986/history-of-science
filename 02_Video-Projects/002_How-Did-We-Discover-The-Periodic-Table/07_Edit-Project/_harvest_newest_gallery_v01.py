#!/usr/bin/env python3
"""Harvest a Flow Agent gallery mp4 into --out (fresh browser, retry until ready)."""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument(
        "--project",
        default=os.environ.get(
            "HOS_FLOW_PROJECT_URL",
            "https://flow.google.com/u/1/project/30a34afb-8d9c-4eac-83ba-012d97f6b1b5",
        ),
    )
    ap.add_argument("--index", type=int, default=-1, help="Gallery thumb index (default newest)")
    ap.add_argument(
        "--wait-s",
        type=int,
        default=int(os.environ.get("HOS_FLOW_HARVEST_WAIT_S", "150")),
        help="Wall-clock seconds to wait for a playable gallery clip",
    )
    ap.add_argument(
        "--before-thumbs",
        type=int,
        default=int(os.environ.get("HOS_FLOW_BEFORE_THUMBS", "-1")),
        help="If >=0, require gallery thumb count to exceed this before harvest",
    )
    args = ap.parse_args()

    os.environ.setdefault("ORBIT_FLOW_ACCOUNT", "benoats@googlemail.com")
    profile = flow.profile_path(
        Path(
            os.environ.get(
                "ORBIT_FLOW_PROFILE",
                str(Path.home() / ".playwright-hos-flow-profile"),
            )
        )
    )
    from playwright.sync_api import sync_playwright
    from playwright.sync_api import Error as PlaywrightError

    try:
        from playwright._impl._errors import TargetClosedError
    except Exception:  # pragma: no cover
        TargetClosedError = PlaywrightError  # type: ignore[misc, assignment]

    t0 = time.time()
    last_err = "not started"
    while time.time() - t0 < args.wait_s:
        with sync_playwright() as p:
            ctx, page = flow.launch_context(p, headed=True, profile=profile)
            captured: list[bytes] = []
            try:
                flow.ensure_flow_account(page)
                page.goto(args.project, wait_until="domcontentloaded", timeout=120_000)
                page.wait_for_timeout(3500)
                flow.dismiss_banners(page)
                thumbs = flow.collect_gallery_asb_srcs(page)
                print(
                    f"harvest poll thumbs={len(thumbs)} elapsed={time.time() - t0:.0f}s",
                    flush=True,
                )
                if args.before_thumbs >= 0 and len(thumbs) <= args.before_thumbs:
                    last_err = (
                        f"waiting for new thumb (have={len(thumbs)} "
                        f"before={args.before_thumbs})"
                    )
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
                        print(
                            f"harvest try idx={idx}/{len(thumbs)} -> {args.out}",
                            flush=True,
                        )
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
                        if got and args.out.exists() and args.out.stat().st_size >= 800_000:
                            print(
                                f"OK bytes={args.out.stat().st_size} via={got}",
                                flush=True,
                            )
                            return
                        last_err = f"idx={idx} got={got}"
                        print(f"  {last_err}", flush=True)
                        try:
                            page.keyboard.press("Escape")
                            page.wait_for_timeout(400)
                        except Exception:
                            pass
            finally:
                try:
                    ctx.close()
                except Exception:
                    pass
        time.sleep(12)

    raise SystemExit(f"harvest failed after {args.wait_s}s: {last_err}")


if __name__ == "__main__":
    main()
