#!/usr/bin/env python3
"""Mint HOS 009 long thumbnail plates A and B at 0 Flow credits (J3262).

Flow Image, Nano Banana 2.1, 16:9, x1. Create runs only when the live page
shows "Generating will use 0 credits" and the shared Flow writer lock is held.
Lettering is added later by the cover builder. No Vertex, no video, no cash.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
FILM = HERE.parent
REPO = FILM.parents[1]
EDIT = FILM / "07_Edit-Project"
ASSETS = HERE / "_assets_v01"
LOG_PATH = HERE / "FLOW_MINT_LOG_J3262_v01.json"

sys.path.insert(0, str(REPO / "04_Audio/tools"))
sys.path.insert(0, str(REPO / "02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project"))
sys.path.insert(0, str(EDIT))
sys.path.insert(0, str(REPO / "02_Video-Projects/013_Darwin-Wallace-Evolution/07_Edit-Project"))

import _flow_still_v01 as still_tool  # noqa: E402
import _mint_flow_v01_pass1 as guard  # noqa: E402
import orbit_flow_veo_ui as flow  # noqa: E402

STYLE_REFS = [
    REPO / "00_Brand/Channel-Setup/style/long/001_how_did_we_discover_germs.jpg",
    REPO / "01_Character/05_Generation-References/hos-explorer-reference-v01.jpg",
]

LOOK = (
    "Warm 1660s English period palette. Golden library light on the left, "
    "soft orchard dusk on the right. Painted 3D cartoon, not a photograph, "
    "not a diagram, not a flat graphic. No saturation push."
)

CONCEPTS = {
    "A": {
        "stem": "hos_009_thumb_A_it_misses_plate01",
        "hook": "IT MISSES",
        "prompt": still_tool.still_prompt(
            LOOK,
            "Hero on the right two-thirds: one giant luminous full moon, about two thirds of the "
            "frame, cream and warm gold, with a single thin golden curve sweeping under it and "
            "missing the dark ground. The moon is whole, uncovered, and clear of the bottom-right corner. "
            "Lower left: the Explorer from the character reference, small, about a quarter of the frame "
            "height, teal coat, round gold glasses, satchel, looking up at the moon. He is a garnish, "
            "never the subject, and he stays in the left third. "
            "Upper left: a clear dark band of night sky and distant hedgerow with no objects in the "
            "lettering area, so cover words can be painted there later. "
            "No words, letters, numbers, or signs anywhere in the picture.",
        ),
    },
    "B": {
        "stem": "hos_009_thumb_B_one_apple_plate01",
        "hook": "ONE APPLE",
        "prompt": still_tool.still_prompt(
            LOOK,
            "Hero on the right two-thirds: one giant red-and-green apple caught in mid-air, about "
            "two thirds of the frame, in front of a sunlit Woolsthorpe apple tree and a warm stone "
            "cottage. The apple is whole, uncovered, and clear of the bottom-right corner. "
            "Lower left: the Explorer from the character reference, small, about a quarter of the "
            "frame height, teal coat, round gold glasses, satchel, looking at the apple. He is a "
            "garnish, never the subject, and he stays in the left third. "
            "Upper left: shaded golden foliage and a dark oak trunk with a clear empty band for "
            "cover words, no objects in that band. "
            "No words, letters, numbers, or signs anywhere in the picture.",
        ),
    },
}


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    only = set(sys.argv[1:]) if len(sys.argv) > 1 else {"A", "B"}
    for ref in STYLE_REFS:
        if not ref.is_file():
            raise SystemExit(f"missing style reference: {ref.name}")
    ASSETS.mkdir(parents=True, exist_ok=True)
    log = json.loads(LOG_PATH.read_text()) if LOG_PATH.exists() else {
        "film": "009",
        "job": "J3262",
        "engine": "Flow Image Nano Banana 2.1 16:9 x1 via the open Flow tab",
        "price": "0 credits",
        "plates": {},
    }

    from playwright.sync_api import sync_playwright

    with guard.SharedFlowAccounting() as accounting:
        state = accounting.snapshot()
        if state["pending"]:
            raise SystemExit("STOP shared Flow ledger has a pending charge")
        with sync_playwright() as pw:
            browser = pw.chromium.connect_over_cdp("http://127.0.0.1:9222")
            page = guard.open_flow_page(
                browser,
                flow.FLOW_HOME,
                lambda current, url: current.goto(url, wait_until="domcontentloaded", timeout=120_000),
            )
            flow.dismiss_banners(page)
            balance = guard.read_live_balance(page)
            print(f"GATE credits={balance} liability={state['liability']}", flush=True)
            log["creditsStart"] = balance
            log["liability"] = state["liability"]

            for cid in ("A", "B"):
                if cid not in only:
                    continue
                cfg = CONCEPTS[cid]
                png_dest = ASSETS / f"{cfg['stem']}.png"
                jpg_dest = ASSETS / f"{cfg['stem']}.jpg"
                evidence_path = ASSETS / f"{cfg['stem']}.create.json"
                before = guard.read_live_balance(page)
                print(f"\n=== Concept {cid} credits_before={before} ===", flush=True)
                t0 = time.time()

                row = guard.Row(
                    index=0,
                    row_id=f"J3262-thumb-{cid}",
                    part=0,
                    plate_id=f"thumb_{cid}",
                    board="08_Thumbnail",
                    quality="still",
                    flow_model="Nano Banana 2.1",
                    max_takes=1,
                    try1_credits=0,
                    flow_clip_s=0,
                    t_s=0.0,
                    t_end_s=0.0,
                    use_s=0.0,
                    explorer=True,
                    prompt=cfg["prompt"],
                    prompt_sha256="",
                    normalized_prompt_sha256="",
                )

                def create_guard(configured_page, row=row, evidence_path=evidence_path, known_balance=before):
                    guard._open_settings_trigger_if_needed(configured_page)
                    raw = configured_page.evaluate(guard.STILL_EVIDENCE_JS, None)
                    if isinstance(raw, dict):
                        safe = {
                            k: raw.get(k)
                            for k in (
                                "host",
                                "models",
                                "outputs",
                                "aspects",
                                "prices",
                                "balances",
                                "ultra",
                                "create_count",
                            )
                        }
                        print("STILL EVIDENCE " + json.dumps(safe), flush=True)
                    # Do not re-read the account menu here. That click closes the
                    # settings panel and the zero-price line disappears.
                    guard.guarded_still_create(
                        configured_page,
                        accounting,
                        reservation="J3262",
                        row=row,
                        evidence_path=evidence_path,
                        floor=0,
                        balance=known_balance,
                    )

                still_tool.make_still(
                    page,
                    cfg["prompt"],
                    png_dest,
                    timeout_s=300,
                    create_guard=create_guard,
                    style_refs=STYLE_REFS,
                    media_root=ASSETS,
                )
                after = guard.read_live_balance(page)
                used = max(0, before - after)
                elapsed = round(time.time() - t0, 1)
                print(f"  credits_after={after} used={used} elapsed={elapsed}s", flush=True)
                if used > 0:
                    raise SystemExit(f"STOP still {cid} spent {used} Flow credits")
                im = Image.open(png_dest).convert("RGB")
                if im.size != (1280, 720):
                    im = im.resize((1280, 720), Image.Resampling.LANCZOS)
                im.save(jpg_dest, "JPEG", quality=94, optimize=True, subsampling=1)
                log["plates"][cid] = {
                    "hook": cfg["hook"],
                    "png": png_dest.name,
                    "jpg": jpg_dest.name,
                    "sha256_png": sha256(png_dest),
                    "sha256_jpg": sha256(jpg_dest),
                    "size": list(im.size),
                    "creditsBefore": before,
                    "creditsAfter": after,
                    "creditsUsed": used,
                    "elapsedSeconds": elapsed,
                    "mintedAt": now(),
                }
                log["creditsEnd"] = after
                log["totalCreditsUsed"] = sum(p.get("creditsUsed", 0) for p in log["plates"].values())
                LOG_PATH.write_text(json.dumps(log, indent=2) + "\n")

    print("ALL STILLS MINTED AT 0 FLOW CREDITS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
