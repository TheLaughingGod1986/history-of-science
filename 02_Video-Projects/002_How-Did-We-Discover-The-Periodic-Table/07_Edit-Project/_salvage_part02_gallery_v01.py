#!/usr/bin/env python3
"""Salvage already-generated Part 02 Flow gallery clips without reminting.

Uses Agent UI gallery play → googlevideo network capture (same path as
orbit_flow_veo_ui.harvest_agent_gallery_mp4). Saves into raw/v01_fast/.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips" / "part02" / "raw" / "v01_fast"
# Latest project that already holds chapter-card gens (x2 → 2 variants).
DEFAULT_PROJECT = os.environ.get(
    "HOS_FLOW_SALVAGE_PROJECT",
    "https://flow.google.com/u/1/project/30a34afb-8d9c-4eac-83ba-012d97f6b1b5",
)


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("ORBIT_FLOW_ACCOUNT", "benoats@googlemail.com")
    os.environ.setdefault("ORBIT_FLOW_HOME", "https://flow.google.com/u/1/")
    profile = flow.profile_path(
        Path(
            os.environ.get(
                "ORBIT_FLOW_PROFILE",
                str(Path.home() / ".playwright-hos-flow-profile"),
            )
        )
    )
    project = DEFAULT_PROJECT
    print(f"salvage project={project}", flush=True)
    print(f"out={RAW}", flush=True)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        captured: list[bytes] = []

        def _on_resp(resp) -> None:
            try:
                ct = (resp.headers.get("content-type") or "").lower()
                url = (resp.url or "").lower()
                if not (
                    "video" in ct
                    or url.endswith(".mp4")
                    or "videoplayback" in url
                    or "googlevideo.com" in url
                ):
                    return
                if resp.status != 200:
                    return
                body = resp.body()
                if len(body) > 150_000 and (b"ftyp" in body[:64] or "video" in ct):
                    captured.append(body)
                    print(f"  network mp4 bytes={len(body)}", flush=True)
            except Exception:
                pass

        page.on("response", _on_resp)
        try:
            flow.ensure_flow_account(page)
            page.goto(project, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(4000)
            flow.dismiss_banners(page)

            thumbs = flow.collect_gallery_asb_srcs(page)
            print(f"gallery thumbs={len(thumbs)}", flush=True)
            if not thumbs:
                raise SystemExit("No gallery thumbs — open a project that already has media")

            # Harvest each thumb into numbered salvage files (newest last).
            for i, src in enumerate(thumbs):
                dest = RAW / f"_salvage_gallery_{i+1:02d}.mp4"
                if dest.exists() and dest.stat().st_size > 800_000:
                    print(f"  skip existing {dest.name}", flush=True)
                    continue
                before = set(thumbs[:i])  # treat earlier as "before" so we target this one
                # Point harvest at this specific thumb by temporarily limiting DOM order:
                # harvest picks the last *new* thumb; pass before_asb = all except this src.
                before_asb = set(thumbs) - {src}
                print(f"  harvesting thumb {i+1}/{len(thumbs)} → {dest.name}", flush=True)
                got = flow.harvest_agent_gallery_mp4(
                    page, dest, captured, before_asb=before_asb
                )
                if got and dest.exists():
                    print(f"  OK {dest.name} bytes={dest.stat().st_size} via={got}", flush=True)
                else:
                    print(f"  FAIL thumb {i+1}", flush=True)
                page.keyboard.press("Escape")
                page.wait_for_timeout(800)
        finally:
            ctx.close()
    print("salvage done", flush=True)


if __name__ == "__main__":
    main()
