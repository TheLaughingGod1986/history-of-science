#!/usr/bin/env python3
"""HOS 007 master v04 (J0925): Mint 3 replacement Nano Banana 2 16:9 stills on Flow (0 Flow credits).

1. 07b_three_in_ten_v04.png (0:38, #007 P1:07b_three_in_ten):
   Ten intact one-piece turned oak wooden peg-doll figures resting solidly on top of an oak cottage windowsill
   in grey daylight (seven standing upright, three lying on their sides on the solid wood shelf; nothing passes
   through solid objects).
2. 06b_jesty_hands_v04.png (2:40, #031 P2:06b_jesty_hands):
   18th-century folding steel medical lancet held at a flat shallow grazing angle scratching the surface of the
   skin on a forearm (two shallow surface scratches only, with no needle going into the arm).
3. 04_lancet_touch_v04.png (4:22, #048 P3:04_lancet_touch):
   Edward Jenner in his sunlit 1796 Berkeley study gently holding a small folding steel lancet at a shallow
   grazing angle to 8-year-old James Phipps's clean upper arm (no AI artefact on the boy's arm, no needle going in).
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
EDIT_006 = REPO / "02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project"
PACK_DIR = Path(__file__).resolve().parent
NAS_WORK = Path("/Volumes/data/mac-mini-archive/scratch/J0925")
STILLS_DIR = NAS_WORK / "stills"
NAS_MEDIA_006 = Path(
    "/Volumes/data/mac-mini-archive/hos-worktrees/2026-10-22/hos-006-trees/02_Video-Projects/006_Trees-Are-Made-Of-Air"
)

sys.path.insert(0, str(REPO / "04_Audio/tools"))
sys.path.insert(0, str(EDIT_006))

import orbit_flow_veo_ui as flow  # noqa: E402
import _flow_still_v01 as still_tool  # noqa: E402
import _mint_flow_cdp_v01 as mint_tool  # noqa: E402

still_tool.MEDIA_CLIPS = STILLS_DIR
still_tool.STYLE_REFS = [
    NAS_MEDIA_006 / "04_Generated-Clips/part04/refs/v01_vertex_stills/04_sunny_window_v01.jpg",
    NAS_MEDIA_006 / "04_Generated-Clips/part03/refs/v01_vertex_stills/10_mint_jar_v01.jpg",
]

LOOK = mint_tool.LOOK

STILLS = [
    {
        "id": "07b_three_in_ten_v04",
        "part": "01",
        "core": (
            "18th-century English country cottage interior in soft overcast grey daylight: close view along a thick "
            "solid rough-hewn oak wooden windowsill in front of a mullioned cottage window overlooking misty green "
            "fields. Resting firmly on top of the solid flat oak windowsill are ten small plain unpainted turned-wood "
            "peg-doll figures in a single row: seven of the wooden peg-doll figures stand upright on their flat wooden "
            "bases, and three intact one-piece wooden peg-doll figures lie horizontally on their sides resting solidly "
            "on top of the oak windowsill surface. Every wooden figure is one solid piece of turned oak wood resting "
            "cleanly on top of the solid wooden shelf. No candle, flame, lantern, lamp or fire in shot. No text, "
            "letters or numbers."
        ),
    },
    {
        "id": "06b_jesty_hands_v04",
        "part": "02",
        "core": (
            "Close shot in warm 18th-century English farmhouse daylight over an oak table: weathered hands in a rough "
            "country wool coat sleeve hold a small authentic 18th-century folding tortoiseshell-and-steel medical "
            "lancet at a flat shallow grazing angle against the surface of a rolled cream linen sleeve and bare forearm, "
            "gently making two tiny shallow surface scratches along the top of the skin. The flat leaf-shaped steel "
            "lancet blade glides almost horizontally across the skin surface only — no needle, no syringe, nothing "
            "piercing or going vertically into the arm, no blood. Warm daylight from a window out of frame; no candle, "
            "flame, lantern, lamp or fire in shot. No text, letters or numbers."
        ),
    },
    {
        "id": "04_lancet_touch_v04",
        "part": "03",
        "core": (
            "Medium-close shot in a bright sunlit 1796 Gloucestershire Georgian study with a mullioned window and wooden "
            "bookshelves behind: Edward Jenner (kind Georgian country doctor in his late forties, powdered hair tied "
            "back with a dark ribbon, dark charcoal-brown wool coat, crisp white linen neckcloth) leans forward gently "
            "beside an 8-year-old English country boy (James Phipps, short tidy brown hair, plain tan wool waistcoat "
            "over a cream linen shirt with one sleeve rolled up to the upper arm, watching calmly and bravely). "
            "Jenner's right hand holds a small authentic 18th-century folding steel medical lancet at a shallow grazing "
            "angle lightly touching the surface of the boy's clean upper arm to make two tiny shallow surface scratches "
            "— the boy's arm skin is completely clean and smooth with no protruding objects, no needle going in, no "
            "blood, and no artefacts. Warm daylight from the window; no candle, flame, lantern, lamp or fire in shot. "
            "No text, letters or numbers."
        ),
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    from playwright.sync_api import sync_playwright

    STILLS_DIR.mkdir(parents=True, exist_ok=True)
    log_path = PACK_DIR / "FLOW_STILLS_LOG_v04.json"
    log = json.loads(log_path.read_text()) if log_path.exists() else {
        "film": "007_The-First-Vaccine",
        "job": "J0925",
        "engine": "Flow Image Nano Banana 2 16:9 (0 Flow credits)",
        "stills": {},
        "balance_reads": [],
    }

    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(mint_tool.CDP)
        page = mint_tool.flow_page(browser, flow)
        credits, account = mint_tool.read_account(page)
        print(f"GATE account={account} credits={credits}", flush=True)
        if account != mint_tool.REQUIRED or mint_tool.FORBIDDEN in (account or ""):
            raise SystemExit(f"STOP wrong Flow account: {account}")
        log["balance_reads"].append({"at": now(), "credits": credits, "when": "start"})
        log_path.write_text(json.dumps(log, indent=2) + "\n")

        for item in STILLS:
            sid = item["id"]
            dest = STILLS_DIR / f"{sid}.png"
            if dest.exists() and dest.stat().st_size > 100_000:
                print(f"SKIP {sid}: already minted ({dest.name})", flush=True)
                continue
            prompt = still_tool.still_prompt(LOOK, item["core"])
            print(f"\n=== MINT STILL {sid} ===", flush=True)
            still_tool.make_still(page, prompt, dest)
            after, _ = mint_tool.read_account(page)
            used = 0 if (credits is None or after is None) else max(0, credits - after)
            credits = after
            log["stills"][sid] = {
                "id": sid,
                "part": item["part"],
                "file": str(dest),
                "sha256": sha256(dest),
                "prompt": prompt,
                "credits_used": used,
                "credits_after": after,
                "at": now(),
            }
            log["balance_reads"].append({"at": now(), "credits": after, "after": sid})
            log_path.write_text(json.dumps(log, indent=2) + "\n")
            print(f"  -> OK {sid} used={used} balance={after}", flush=True)
            if used > 0:
                raise SystemExit(f"STOP still cost {used} credits > 0")

    print("ALL 3 STILLS MINTED AT 0 CREDITS", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
