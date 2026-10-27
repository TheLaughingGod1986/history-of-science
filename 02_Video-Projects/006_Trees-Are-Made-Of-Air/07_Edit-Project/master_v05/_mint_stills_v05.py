#!/usr/bin/env python3
"""HOS 006 master v05 (J0886): Mint 4 replacement Nano Banana 2 16:9 stills on Flow (0 Flow credits).

1. 02_balance_trunk_v05.png (0:07, #02): Whole willow tree (washed root ball, trunk, and green weeping canopy) sitting directly ON the left brass scale pan, weighing it down low while a small heap of dark soil on the right brass pan is lifted high in the air.
2. 05_pure_water_v05.png (1:26, #17 & 7:16, #80): Young willow tree growing directly up out of the soil in the terracotta pot through the central hole of the perforated tin-plated iron lid, while Jan Baptist van Helmont (full upper body, shoulders and arms visible) pours clear water from a copper watering can onto the perforated lid around the trunk.
3. 17_notebook_tick_v05.png (4:28, #50): Joseph Priestley (full upper body, head, shoulders, sleeves and arms naturally connected in house 3D cartoon style) seated at his wooden laboratory desk holding a feather quill pen over an open notebook showing only a simple ink tick mark and an X cross mark (zero text/words).
4. 10_only_green_v05.png (5:29, #61): Three clear glass jars of water on a sunny windowsill — left jar with submerged pale root (no bubbles), middle jar with submerged red flower (no bubbles), right jar with submerged green leaf underwater below a flat meniscus, with completely clear dry air above all jars and zero bubbles in the air.
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
EDIT_DIR = REPO / "02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project"
OUT_DIR = EDIT_DIR / "master_v05"
STILLS_DIR = OUT_DIR / "stills"
NAS_MEDIA = Path(
    "/Volumes/data/mac-mini-archive/hos-worktrees/2026-10-22/hos-006-trees/02_Video-Projects/006_Trees-Are-Made-Of-Air"
)

sys.path.insert(0, str(REPO / "04_Audio/tools"))
sys.path.insert(0, str(EDIT_DIR))

import orbit_flow_veo_ui as flow  # noqa: E402
import _flow_still_v01 as still_tool  # noqa: E402
import _mint_flow_cdp_v01 as mint_tool  # noqa: E402

still_tool.MEDIA_CLIPS = STILLS_DIR
still_tool.STYLE_REFS = [
    NAS_MEDIA / "04_Generated-Clips/part04/refs/v01_vertex_stills/04_sunny_window_v01.jpg",
    NAS_MEDIA / "04_Generated-Clips/part03/refs/v01_vertex_stills/10_mint_jar_v01.jpg",
]

LOOK = mint_tool.LOOK

STILLS = [
    {
        "id": "02_balance_trunk_v05",
        "part": "01",
        "core": (
            "Golden-hour green meadow in warm sunlight. In the centre stands a monumental antique brass two-pan balance scale. "
            "Sitting directly ON the left wide brass scale pan is a whole willow tree — its washed brown root ball resting flat "
            "inside the left brass scale pan, with its sturdy bark trunk and full cascade of green weeping willow leaves rising "
            "straight up from the pan, weighing the left pan down low near the grass. The right brass scale pan is lifted high in "
            "the air, holding only a small heap of dark brown soil. No tree growing in the grass behind the scale; the only willow "
            "tree is the one sitting with its roots inside the left brass scale pan. No text, letters or numbers."
        ),
    },
    {
        "id": "05_pure_water_v05",
        "part": "02",
        "core": (
            "1640s Flemish brick-walled courtyard in warm sunlight. In the centre foreground stands a large smooth terracotta clay "
            "garden pot. Growing directly up out of the centre of the terracotta pot is a young green weeping willow tree — its "
            "sturdy woody trunk emerging straight up through the central hole of a flat circular perforated tin-plated iron lid "
            "fitted neatly over the top rim of the pot, with leafy green willow branches spreading above the pot. No other tree "
            "stands behind the pot. Standing on the right beside the pot is Jan Baptist van Helmont (1640s Flemish physician in "
            "black doublet, plain white linen collar, shoulder-length dark hair and neat beard, full upper body, shoulders and arms "
            "clearly visible), tilting a polished copper watering can so clear water pours onto the perforated metal lid around the "
            "willow trunk. No text or numbers."
        ),
    },
    {
        "id": "17_notebook_tick_v05",
        "part": "03",
        "core": (
            "1770s English sunlit study by a multi-pane window. Joseph Priestley (18th-century English natural philosopher in dark "
            "brown coat, white linen cravat, and white powdered curly wig, full upper body, head, shoulders, coat sleeves and both "
            "arms clearly visible in the 3D cartoon house style) sits at his oak laboratory desk looking thoughtfully down at an "
            "open cream leather-bound notebook on the desk in front of him. His right hand — connected naturally to his cuffed coat "
            "sleeve, forearm and shoulder — holds a feather quill pen poised over the open notebook page, which shows only two simple "
            "bold ink symbols drawn on blank cream paper (one neat check tick mark and one X cross mark, with zero letters, zero "
            "words, and zero handwriting lines). On the right side of the oak desk stands a clear glass bell jar over a wooden water "
            "trough and a small white pillar candle. Warm daylight, no text or readable characters anywhere."
        ),
    },
    {
        "id": "10_only_green_v05",
        "part": "04",
        "core": (
            "1779 sunlit wooden windowsill in front of a bright paned window looking out onto a soft green garden. Three identical "
            "wide clear hand-blown glass jars filled with crystal-clear water sit side by side in a neat row on the wooden sill: "
            "in the left jar, a pale beige plant root submerged in clear still water with zero bubbles; in the middle jar, a single "
            "red five-petaled flower blossom submerged in clear still water with zero bubbles; in the right jar, a single fresh green "
            "leaf submerged deep underwater below a calm flat water meniscus, with tiny silver oxygen bubbles clinging only to the "
            "submerged green leaf surface underwater. Above the flat water surface inside all three jars and in the sunlit air above "
            "the jars, the air is completely empty, clean and dry with zero bubbles, zero droplets and zero dust specks in the air. "
            "No text or labels."
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
    log_path = OUT_DIR / "FLOW_STILLS_LOG_v05.json"
    log = json.loads(log_path.read_text()) if log_path.exists() else {
        "film": "006_Trees-Are-Made-Of-Air",
        "job": "J0886",
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

    print("ALL 4 STILLS MINTED AT 0 CREDITS", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
