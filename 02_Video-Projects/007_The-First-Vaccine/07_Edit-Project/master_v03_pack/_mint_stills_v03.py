#!/usr/bin/env python3
"""HOS 007 master v03 (J0887): Mint 2 replacement Nano Banana 2 16:9 stills on Flow (0 Flow credits).

1. 01_milking_dawn_v03.png (1:48, #21 P2:01_milking_dawn):
   Dairymaid seated on her three-legged wooden stool in the timber byre at dawn with both hands wrapped
   directly around the cow's udder teats, milking a stream of milk straight down from her hands into
   the wooden pail directly below the udder (resolving Ben's 1:48 'When she's milking the cow the hand is misaligned').
2. 14_explorer_stool_v03.png (3:50, #42 P2:14_explorer_stool):
   Wide shot in the timber byre where the Explorer is a small child-sized side character at house scale
   (clearly smaller than the seated adult dairymaid and cow, never dominating the frame), peering at
   the dairymaid's healed hand and the cow (resolving Ben's 3:50 'Mascot here is way to big').
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

WT = Path(__file__).resolve().parents[4]
REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
EDIT_006 = REPO / "02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project"
PACK_DIR = Path(__file__).resolve().parent
STILLS_DIR = PACK_DIR / "stills"
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
        "id": "01_milking_dawn_v03",
        "part": "02",
        "core": (
            "1790s Gloucestershire timber dairy byre at dawn with warm golden morning sunbeams slanting through "
            "the open barn doorway on the left onto the straw floor. A calm brown-and-white dairy cow stands in "
            "profile in the centre. Seated close beside the cow's flank on a low three-legged wooden milking stool "
            "is a young English dairymaid in a white linen cap, brown laced bodice, rolled sleeves and cream apron. "
            "Both of the dairymaid's hands reach directly underneath the cow's pink udder, with her fingers wrapped "
            "firmly and naturally around the udder teats, actively milking a thin white stream of milk straight down "
            "from her hands into a wooden bucket resting on the straw directly beneath her hands and the udder. "
            "Her hands physically grip the teats of the udder with zero gap or misalignment. No text, letters or numbers."
        ),
    },
    {
        "id": "14_explorer_stool_v03",
        "part": "02",
        "core": (
            "Wide establishing shot inside a spacious 1790s Gloucestershire timber dairy byre in warm morning light, "
            "camera placed well back showing the high timber roof beams, wooden stalls, and wide straw floor. On the "
            "left, a large brown-and-white dairy cow stands in her wooden stall beside a wooden bucket, and a full-grown "
            "adult English dairymaid in a white linen cap, brown bodice and cream apron sits on a wooden milking stool "
            "holding out her hand. Standing a step further back in the mid-ground on the right is the Explorer — a small "
            "petite 8-year-old boy side character who is much smaller than the adult dairymaid and cow (occupying only "
            "about one-third of the frame height, never dominating the frame), with messy wavy brown hair, round thin "
            "gold wire-rim glasses, teal-blue long coat, tan waistcoat, brown bow tie, rolled brown trousers, brown boots "
            "and a small brown leather satchel — leaning slightly forward at a respectful distance to peer curiously at "
            "the dairymaid's hand and the cow. No text, letters or numbers."
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
    log_path = PACK_DIR / "FLOW_STILLS_LOG_v03.json"
    log = json.loads(log_path.read_text()) if log_path.exists() else {
        "film": "007_The-First-Vaccine",
        "job": "J0887",
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

    print("ALL 2 STILLS MINTED AT 0 CREDITS", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
