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
_PLATES_V04 = PROJ / "07_Edit-Project/parts/part-02_plates_v04.json"
_PLATES_V03 = PROJ / "07_Edit-Project/parts/part-02_plates_v03.json"
_PLATES_V02 = PROJ / "07_Edit-Project/parts/part-02_plates_v02.json"
_PLATES_V01 = PROJ / "07_Edit-Project/parts/part-02_plates_v01.json"
PLATES_JSON = next(
    (p for p in (_PLATES_V04, _PLATES_V03, _PLATES_V02, _PLATES_V01) if p.exists()),
    _PLATES_V01,
)
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
# Science-card remints NEED readable English. Do not forbid text.
STYLE = (
    "History of Science locked look: premium Animistry-class 3D cartoon like Germs "
    "Part 01 PASS — warm wood, cream parchment science cards when asked. "
    "Scholar WRITING STUDY / library desk — NOT a chemistry lab, NOT alchemy workshop, "
    "NOT a modern lab. Not photoreal. Not live-action. Silent picture. "
    "No Orbit orange robot. Continuous motion the whole clip. "
)
PHYSICS = (
    "Premium finished Animistry-class 3D cartoon — NOT flat 2D placeholders, NOT unfinished shapes. "
    "ZERO jars, pots, canisters, tins, crucibles, flasks, bottles, vials, retorts, "
    "spirit lamps, Bunsen burners, tripod burners, shelves of glassware. "
    "Candles in candlesticks MAY have a small natural candle-wick flame. "
    "ZERO flames from any vessel mouth. ZERO fire under or on any object. "
    "Papers, blank cards, books, quills, rulers, toy piano OK. "
    "Objects sit on contact surfaces. Silent picture. "
)
CARD_LOCK = (
    "If this is a full-frame SCIENCE CARD: exact title and body text must be sharp readable "
    "English as given — correct spelling, factual, no Latin gibberish, no Sciener, "
    "no invented words, no blurry nonsense text. "
    "For scenery plates: NO readable text / NO information cards filling the frame. "
)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--plate-id", required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument(
        "--plates-json",
        type=Path,
        default=PLATES_JSON,
        help="Plates JSON (default: newest v0N)",
    )
    ap.add_argument(
        "--start-frame",
        type=Path,
        default=None,
        help="Optional locked start still for I2V (keeps composition; no jars)",
    )
    args = ap.parse_args()

    plates = {p["id"]: p for p in json.loads(args.plates_json.read_text())["plates"]}
    plate = plates[args.plate_id]
    if plate.get("remint") is False:
        raise SystemExit(f"plate {args.plate_id} marked remint=false — skip")
    prompt = f"{STYLE} {PHYSICS} {CARD_LOCK} {plate['prompt']}"
    if args.start_frame:
        prompt += (
            " IMAGE-TO-VIDEO from the attached start frame. Keep the same finished premium "
            "3D cartoon look and composition. Animate gentle continuous motion only. "
            "Do NOT add jars, pots, canisters, flasks, burners, or fire under vessels. "
            "Candle wick flame may stay if present. "
        )
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

    from playwright.sync_api import sync_playwright

    args.out.parent.mkdir(parents=True, exist_ok=True)
    tmp = args.out.with_name(args.out.stem + "_create_tmp.mp4")
    if tmp.exists():
        tmp.unlink()

    # v04: do NOT auto-attach local Pillow desks — they look unfinished and flip
    # Flow Create into Nano Banana (Image). Only use an explicit --start-frame
    # that is a finished Flow still. Default = scenery-only Veo T2V.
    start = args.start_frame
    if start is not None and not start.exists():
        raise SystemExit(f"start-frame missing: {start}")
    scenery_only = start is None
    print(
        f"CREATE {args.plate_id} plates={args.plates_json.name} profile={profile} "
        f"start_frame={start.name if start else None} scenery_only={scenery_only}",
        flush=True,
    )
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
            reuse_project=True,
            attempts=1,
            timeout_s=420,
            start_frame=start,
            scenery_only=scenery_only,
        )
        if not info.get("needs_gallery_harvest"):
            if tmp.exists() and tmp.stat().st_size > 800_000:
                if args.out.exists():
                    args.out.unlink()
                tmp.replace(args.out)
                print(f"SAVED_DIRECT {args.out}", flush=True)
                return
            raise SystemExit(f"CREATE did not hand off to harvest: {info}")
        print(
            f"HANDOFF {args.plate_id} media_id={info.get('media_id')}",
            flush=True,
        )
    os._exit(0)


if __name__ == "__main__":
    main()
