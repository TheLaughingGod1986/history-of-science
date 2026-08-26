#!/usr/bin/env python3
"""One-plate Flow probe with debug logging."""
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow
from playwright.sync_api import sync_playwright

still = REPO / "02_Video-Projects/001_How-Did-We-Discover-Germs/04_Generated-Clips/part02/refs/01_chapter_lab_scope_v01.jpg"
dest = REPO / "02_Video-Projects/001_How-Did-We-Discover-Germs/04_Generated-Clips/part02/raw/v01_flow/01_chapter_lab_scope_v01.mp4"
dest.parent.mkdir(parents=True, exist_ok=True)
prompt = (
    "Premium 3D cartoon Victorian science study. Brass microscope on desk. "
    "Slow continuous camera push. Silent. Match start frame. Never freeze."
)
profile = flow.profile_path(Path.home() / ".playwright-hos-flow-profile")
print("profile", profile, "still", still.exists(), flush=True)
with sync_playwright() as p:
    ctx, page = flow.launch_context(p, headed=False, profile=profile)
    try:
        info = flow.generate_clip(
            page,
            prompt,
            dest,
            model="Veo 3.1 - Fast",
            start_frame=still,
            timeout_s=480,
            reuse_project=False,
            scenery_only=True,
            attempts=1,
        )
        print("OK", info, dest.stat().st_size if dest.exists() else 0, flush=True)
    finally:
        ctx.close()
