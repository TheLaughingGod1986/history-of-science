#!/usr/bin/env python3
"""Harvest the newest Flow Agent gallery mp4 into --out (fresh browser)."""
from __future__ import annotations

import argparse
import os
import sys
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
    args = ap.parse_args()

    os.environ.setdefault("ORBIT_FLOW_ACCOUNT", "benoats@googlemail.com")
    profile = flow.profile_path(
        Path(os.environ.get("ORBIT_FLOW_PROFILE", str(Path.home() / ".playwright-hos-flow-profile")))
    )
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        captured: list[bytes] = []
        try:
            flow.ensure_flow_account(page)
            page.goto(args.project, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(3500)
            flow.dismiss_banners(page)
            thumbs = flow.collect_gallery_asb_srcs(page)
            if not thumbs:
                raise SystemExit("no gallery thumbs")
            idx = args.index if args.index >= 0 else len(thumbs) - 1
            idx = max(0, min(idx, len(thumbs) - 1))
            src = thumbs[idx]
            before = set(thumbs) - {src}
            print(f"harvest idx={idx}/{len(thumbs)} -> {args.out}", flush=True)
            got = flow.harvest_agent_gallery_mp4(
                page, args.out, captured, before_asb=before
            )
            if not got or not args.out.exists() or args.out.stat().st_size < 800_000:
                raise SystemExit(f"harvest failed got={got}")
            print(f"OK bytes={args.out.stat().st_size} via={got}", flush=True)
        finally:
            ctx.close()


if __name__ == "__main__":
    main()
