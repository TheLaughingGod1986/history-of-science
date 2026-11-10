#!/usr/bin/env python3
"""HOS 006 master v04 (J0882): Mint 6 replacement Nano Banana 2 16:9 stills on Flow (0 Flow credits).

1. 03_pot_jar_leaf_v04.png (0:09 & 8:02): Three containers on a sunlit oak table — left terracotta pot with willow shoot in dark soil; middle small terracotta pot sitting on the table with a green mint sprig growing out of its dark soil inside a clear glass bell jar covering the pot; right clear glass jar of water with a submerged green leaf beaded with tiny silver bubbles inside the water.
2. 10_van_helmont_sack_v04.png (0:49): Van Helmont in his 1640s Flemish courtyard beside a large brass two-pan balance scale; on the left brass pan sits a full open burlap sack of dark garden soil, balanced by iron weights on the right pan.
3. 03_willow_shoot_scale_v04.png (1:14): Whole young 5-pound willow tree — bare washed root ball, slender woody trunk, and green willow shoots — resting on the left brass pan of a large balance scale, balanced by a 5-pound iron weight on the right pan.
4. 04_lid_rain_v04.png (1:22): Smooth unperforated terracotta pot with a young willow sapling growing up through the centre of a flat circular tin-plated iron lid pierced with many tiny round holes covering the top rim of the pot, as gentle raindrops fall onto the top metal lid.
5. 02_hales_branch_v04.png (3:04): Stephen Hales in his 1727 study observing a freshly cut leafy green tree sprig placed sensibly upright with its cut stem submerged deep inside a wide period hand-blown glass jar of clear water on a wooden bench.
6. 03_water_level_v04.png (3:15): Close-up on the wooden laboratory bench of the period hand-blown glass jar filled with clear water; a freshly cut leafy green tree sprig stands sensibly upright inside the glass jar with its woody stem submerged in the water and tiny silver bubbles clinging to the submerged stem.
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
EDIT_DIR = REPO / "02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project"
OUT_DIR = EDIT_DIR / "master_v04"
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
        "id": "03_pot_jar_leaf_v04",
        "part": "01",
        "core": (
            "Sunlit oak laboratory table by a bright paned window. Three objects arranged clearly in a row from left to right "
            "on the wooden tabletop: on the left, a small terracotta clay pot filled with dark soil with a young green willow shoot "
            "growing out of the soil; in the middle, a small terracotta clay pot filled with dark brown soil sitting solidly on the "
            "tabletop with a fresh green sprig of mint growing out of the soil inside the pot, covered by an inverted clear glass bell "
            "jar (cloche) whose rim rests around the pot on the table; on the right, a clear glass jar filled with water containing a "
            "single submerged green leaf covered with tiny silver oxygen bubbles staying inside the water."
        ),
    },
    {
        "id": "10_van_helmont_sack_v04",
        "part": "01",
        "core": (
            "1640s Flemish walled brick courtyard in warm daylight. A large heavy brass two-pan balance scale stands on flagstones "
            "in the centre. On the left wide brass pan sits a full open-topped burlap sack of dark dried garden soil, heavy and solid, "
            "pulling the left pan down. On the right brass pan sit dark iron counterweights balancing the beam. Beside the scale stands "
            "Jan Baptist van Helmont (1640s Flemish physician in black doublet, plain white linen collar, shoulder-length dark hair and "
            "neat pointed beard), his hand steadying the brass scale beam as he studies the heavy sack of soil on the pan."
        ),
    },
    {
        "id": "03_willow_shoot_scale_v04",
        "part": "02",
        "core": (
            "1640s brick laboratory workbench in warm window light. A large sturdy brass two-pan balance scale sits on the wooden table. "
            "On the left wide brass pan rests a whole young five-pound willow sapling — complete with its clean washed bare root ball, "
            "slender woody trunk, and fresh green weeping willow shoots. On the right brass pan sits a single dark five-pound iron weight "
            "balancing the young tree. No text, letters or numbers on any object."
        ),
    },
    {
        "id": "04_lid_rain_v04",
        "part": "02",
        "core": (
            "Close three-quarter view of a large smooth unperforated terracotta garden pot standing on courtyard flagstones. A young green "
            "willow sapling grows up from the centre. Fitted neatly over the top rim of the pot around the willow trunk is a flat circular "
            "tin-plated iron lid pierced with many neat tiny round holes, like a colander lid. Gentle silver raindrops fall from above onto "
            "the perforated metal lid on top of the pot and trickle cleanly through the tiny holes into the soil below, while golden dust "
            "motes drift past outside. The clay pot sides are completely solid and smooth with no holes."
        ),
    },
    {
        "id": "02_hales_branch_v04",
        "part": "03",
        "core": (
            "1727 English parsonage study in warm morning sunlight. On the left-centre of a wooden laboratory table stands a tall wide "
            "period hand-blown glass cylinder jar filled with clear water; placed sensibly upright inside the glass jar is a freshly cut "
            "leafy green tree sprig, its woody cut stem submerged deep in the water and its green leaves rising cleanly above the neck of "
            "the glass vessel, with only the sunlit window behind the glass jar. Standing clearly to the right of the jar is Stephen Hales "
            "(1720s English country parson in black clerical coat, white collar bands, and white powdered curly wig), with both hands "
            "resting on an open leather notebook on the right side of the table as he looks across at the glass jar."
        ),
    },
    {
        "id": "03_water_level_v04",
        "part": "03",
        "core": (
            "Close-up in a sunlit 1727 laboratory of a tall wide hand-blown clear glass cylinder jar standing on a wooden bench, filled with "
            "clear water. A freshly cut leafy green tree sprig stands sensibly upright inside the glass jar with its woody cut stem submerged "
            "deep in the water, sealed around the glass rim with yellow beeswax. Tiny silver gas bubbles cling to the submerged woody stem "
            "underwater. No text or graduation numbers on the glass."
        ),
    },
    {
        "id": "04_sunny_window_v04",
        "part": "04",
        "core": (
            "1779 sunlit English country house study: a row of five clear hand-blown glass jars filled with clear water sitting on a warm "
            "oak workbench in front of a bright sunlit multi-pane window. Inside each jar of water is a submerged fresh green leaf covered "
            "in tiny silver oxygen bubbles strictly underwater inside the glass jars. Completely dry air outside the jars with zero droplets "
            "or bubbles in the air. No text or numbers."
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
    log_path = OUT_DIR / "FLOW_STILLS_LOG_v04.json"
    log = json.loads(log_path.read_text()) if log_path.exists() else {
        "film": "006_Trees-Are-Made-Of-Air",
        "job": "J0882",
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

    print("ALL 6 STILLS MINTED AT 0 CREDITS", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
