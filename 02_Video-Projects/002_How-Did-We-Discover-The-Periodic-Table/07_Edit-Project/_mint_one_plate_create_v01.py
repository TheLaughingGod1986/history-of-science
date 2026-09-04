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
_PLATES_V03 = PROJ / "07_Edit-Project/parts/part-02_plates_v03.json"
_PLATES_V02 = PROJ / "07_Edit-Project/parts/part-02_plates_v02.json"
_PLATES_V01 = PROJ / "07_Edit-Project/parts/part-02_plates_v01.json"
PLATES_JSON = (
    _PLATES_V03
    if _PLATES_V03.exists()
    else (_PLATES_V02 if _PLATES_V02.exists() else _PLATES_V01)
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
    "Not photoreal. Not live-action. Not a modern lab. Silent picture. "
    "No Orbit orange robot. Continuous motion the whole clip. "
)
PHYSICS = (
    "OPAQUE ceramic jars / sealed metal canisters only when props appear. "
    "ZERO clear glass flasks with liquid. ZERO bubbles floating in air. "
    "ZERO floating glassware. Objects sit IN or ON contact surfaces. "
    "FIRE RULE (hard): the ONLY allowed flame is a candle wick in a candlestick or wall sconce. "
    "ZERO spirit lamps. ZERO Bunsen burners. ZERO tripod burners. ZERO open fire under any pot, jar, crucible, or canister. "
    "Jars, pots, canisters, crucibles MUST NEVER be on fire and MUST NEVER sit above a flame. "
    "ZERO flames, smoke plumes, or glowing vapor from jar or pot mouths. "
    "ZERO pots on fire. ZERO jars on fire. "
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
        help="Plates JSON (default: v02 if present else v01)",
    )
    args = ap.parse_args()

    plates = {p["id"]: p for p in json.loads(args.plates_json.read_text())["plates"]}
    plate = plates[args.plate_id]
    if plate.get("remint") is False:
        raise SystemExit(f"plate {args.plate_id} marked remint=false — skip")
    prompt = f"{STYLE} {PHYSICS} {CARD_LOCK} {plate['prompt']}"
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

    print(
        f"CREATE {args.plate_id} plates={args.plates_json.name} profile={profile}",
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
            start_frame=None,
            scenery_only=True,
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
