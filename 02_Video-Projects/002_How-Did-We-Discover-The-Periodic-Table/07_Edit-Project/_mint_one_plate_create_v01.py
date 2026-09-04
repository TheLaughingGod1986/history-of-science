#!/usr/bin/env python3
"""Create one Part 02 Flow plate and exit as soon as Agent gen is running.

Does not settle/harvest — the shell driver owns that so Python never sleeps
with a dying Playwright driver attached.
"""
from __future__ import annotations

import argparse
import json
import os
import signal
import sys
from pathlib import Path

signal.signal(signal.SIGPIPE, signal.SIG_IGN)
signal.signal(signal.SIGHUP, signal.SIG_IGN)

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-02_plates_v01.json"
MODEL = "Veo 3.1 - Fast"
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
PINNED_DEFAULT = (
    "https://flow.google.com/u/1/project/30a34afb-8d9c-4eac-83ba-012d97f6b1b5"
)
STYLE = (
    "History of Science locked look: premium Animistry-class 3D cartoon like Germs "
    "Part 01 and Periodic Table Part 01 PASS — warm wood period workshop, cinematic light. "
    "Not photoreal. Not live-action. Not a modern lab. Silent picture. "
    "No readable text, logos, or UI. No Orbit orange robot. Continuous motion the whole clip. "
)
PHYSICS = (
    "Prefer OPAQUE ceramic jars / sealed metal canisters / solid cylinders. "
    "ZERO clear glass flasks with liquid. ZERO bubbles floating in air. "
    "ZERO floating glassware. Objects sit IN or ON contact surfaces. "
    "Heat shimmer colourless only — no flames unless asked. "
)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--plate-id", required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    plates = {p["id"]: p for p in json.loads(PLATES_JSON.read_text())["plates"]}
    plate = plates[args.plate_id]
    prompt = f"{STYLE} {PHYSICS} {plate['prompt']}"
    pinned = (
        os.environ.get("HOS_FLOW_PROJECT_URL")
        or os.environ.get("ORBIT_FLOW_PROJECT_URL")
        or PINNED_DEFAULT
    )
    os.environ["HOS_FLOW_PROJECT_URL"] = pinned
    os.environ["ORBIT_FLOW_PROJECT_URL"] = pinned
    os.environ.setdefault("ORBIT_FLOW_ACCOUNT", "benoats@googlemail.com")
    os.environ.setdefault("ORBIT_FLOW_FORCE_NEW_PROJECT", "0")
    headed = os.environ.get("ORBIT_FLOW_HEADED", "1") not in {"0", "false", "False"}
    profile = flow.profile_path(PROFILE)
    reuse = True

    from playwright.sync_api import sync_playwright

    args.out.parent.mkdir(parents=True, exist_ok=True)
    tmp = args.out.with_name(args.out.stem + "_create_tmp.mp4")
    if tmp.exists():
        tmp.unlink()

    print(f"CREATE {args.plate_id} profile={profile}", flush=True)
    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=headed, profile=profile)
        flow.ensure_flow_account(page)
        page.goto(pinned, wait_until="domcontentloaded", timeout=120_000)
        page.wait_for_timeout(2000)
        flow.dismiss_banners(page)
        print(f"  project={page.url}", flush=True)
        info = flow.generate_clip(
            page,
            prompt,
            tmp,
            model=MODEL,
            reuse_project=reuse,
            attempts=1,
            timeout_s=420,
            start_frame=None,
            scenery_only=True,
        )
        # Leave the with-block without closing mid-gen.
        if not info.get("needs_gallery_harvest"):
            # Unexpected direct download path.
            if tmp.exists() and tmp.stat().st_size > 800_000:
                if args.out.exists():
                    args.out.unlink()
                tmp.replace(args.out)
                print(f"SAVED_DIRECT {args.out}", flush=True)
                return
            raise SystemExit(f"CREATE did not hand off to harvest: {info}")
        print(f"HANDOFF {args.plate_id} media_id={info.get('media_id')}", flush=True)
    # Force a hard exit so no Playwright destructor can kill a later wait.
    os._exit(0)


if __name__ == "__main__":
    main()
