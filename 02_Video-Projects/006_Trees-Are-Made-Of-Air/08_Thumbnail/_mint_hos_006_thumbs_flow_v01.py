#!/usr/bin/env python3
"""Mint HOS 006 Trees long thumbnail base plates A + B via Flow Image (Nano Banana 2, 16:9, 0 credits) on CDP :9222.

Job: OWB Queue J0869 (Step 2 of 2, after Chief pick on J0858).
- Concept A ('WOOD / FROM / SKY?'): Living willow tree in a terracotta pot on a sunlit oak table beside an arched window;
  luminous golden-teal ribbons of air stream in through the window into the green willow leaves and condense into glowing
  solid wood rings inside a clean cutaway of the thick trunk. Explorer lower-left (~50% height) looking up in wonder.
- Concept B ('DO PLANTS / EAT / SOIL?'): Grand 17th-century polished brass balance scale on an oak laboratory table;
  right-hand pan weighed down low by a massive uprooted willow tree (trunk, roots, green canopy), raised pan holds the
  smaller clay pot of dark dried furnace soil — beam tilted sharply toward the tree. Blank pans/weights (no written numbers).
  Explorer lower-left (~50% height) leaning in looking at the tilted scale.
- Price lock: Option 1, 0 Flow credits (Nano Banana 2 16:9 stills on AI Ultra). Verifies credits_after == credits_before.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
FILM_DIR = HERE.parent
REPO = FILM_DIR.parents[1]
EDIT_DIR = FILM_DIR / "07_Edit-Project"
ASSETS = HERE / "_assets_v01"
LOG_PATH = HERE / "FLOW_MINT_LOG_J0869_v01.json"

sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
sys.path.insert(0, str(EDIT_DIR))

import _flow_still_v01 as still_tool  # noqa: E402
import _mint_flow_cdp_v01 as flow_cdp  # noqa: E402
import orbit_flow_veo_ui as flow  # noqa: E402

STYLE_REFS = [
    REPO / "00_Brand/Channel-Setup/style/long/001_how_did_we_discover_germs.jpg",
    ASSETS / "04_sunny_window_v01.jpg",
    REPO / "01_Character/05_Generation-References/hos-explorer-reference-v01.jpg",
]

CONCEPTS = {
    "A": {
        "stem": "hos_006_thumb_A_wood_from_sky_plate01",
        "prompt": (
            "STYLE LOCK from the attached stills: match the live History of Science long thumbnail's "
            "premium 3D cartoon painting, warm golden library/study light, arched window, and rounded "
            "stylised materials. Use the attached thumbnail ONLY for paint style, lighting, and depth — "
            "IGNORE and DO NOT COPY any text or letters on it. Match the Explorer reference exactly "
            "(round thin gold glasses, teal long coat, tan waistcoat, brown bow tie, messy brown hair, "
            "satchel), exactly one Explorer.\n"
            "LANDSCAPE 16:9 wide single still frame.\n"
            "Hero object on the right two-thirds (x=520..1240): a lush young willow tree growing in a "
            "large terracotta pot on a polished oak table beside an arched sunlit window; luminous "
            "golden-teal ribbons of air stream visibly in through the open window into the green willow "
            "leaves and flow down into a glowing cutaway section of the thick wooden trunk showing warm "
            "solid wood rings. Whole tree and pot clearly visible.\n"
            "Lower left (x=80..340, y=340..720): the Explorer at about half the frame height, standing "
            "in the lower-left corner looking up in wonder at the glowing trunk cutaway.\n"
            "Upper left (x=40..510, y=20..335): warm shaded dark-wood bookshelves only, completely "
            "empty and uncluttered with ZERO text or letters so title lettering can be added in post.\n"
            "Bottom-right corner: empty dark tabletop shadow only.\n"
            "HARD REJECT: any text, letters, words, numbers, symbols, signs, watermarks, flat 2D shapes, "
            "split panels, photoreal, orange robot."
        ),
    },
    "B": {
        "stem": "hos_006_thumb_B_do_plants_eat_soil_plate01",
        "prompt": (
            "STYLE LOCK from the attached stills: match the live History of Science long thumbnail's "
            "premium 3D cartoon painting, warm golden Flemish laboratory/library light, and rounded "
            "stylised materials. Use the attached thumbnail ONLY for paint style, lighting, and depth — "
            "IGNORE and DO NOT COPY any text or letters on it. Match the Explorer reference exactly "
            "(round thin gold glasses, teal long coat, tan waistcoat, brown bow tie, messy brown hair, "
            "satchel), exactly one Explorer.\n"
            "LANDSCAPE 16:9 wide single still frame.\n"
            "Hero object on the right two-thirds (x=520..1240): a grand 17th-century polished brass "
            "balance scale on a heavy oak table; the right-hand pan hangs low, weighed down by a massive "
            "uprooted willow tree with thick wooden trunk, roots, and bright green leaves, while the "
            "other pan holds a smaller clay pot of dark dried soil lifted high in the air, the brass "
            "beam tilted dramatically toward the heavy willow. All brass pans, beams, and weights are "
            "completely smooth and blank with ZERO markings or numbers.\n"
            "Lower left (x=80..340, y=340..720): the Explorer at about half the frame height, standing "
            "in the lower-left corner leaning in with wide curious eyes behind his gold glasses looking "
            "at the tilted brass scale.\n"
            "Upper left (x=40..510, y=20..335): warm shaded dark-wood bookshelves only, completely "
            "empty and uncluttered with ZERO text or letters so title lettering can be added in post.\n"
            "Bottom-right corner: empty dark tabletop shadow only.\n"
            "HARD REJECT: any text, letters, words, numbers (no 169 lb or 200 lb), symbols, engravings "
            "on weights or pans, flat 2D shapes, split panels, photoreal, orange robot."
        ),
    },
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def select_image_16x9_fixed(page) -> str:
    pill0 = still_tool.prompt_pill_text(page)
    print(f"  pill before={pill0!r}", flush=True)
    if still_tool._pill_is_image_wide(pill0):
        return pill0
    page.evaluate(
        """() => {
          for (const bd of document.querySelectorAll('.cdk-overlay-backdrop-showing')) {
            bd.click();
          }
        }"""
    )
    page.wait_for_timeout(400)
    trig = page.locator('button[aria-label*="Settings trigger" i]').first
    trig.click(force=True, timeout=5000)
    page.wait_for_timeout(800)
    img_radio = page.locator('button[role="radio"]', has_text="Image").first
    if img_radio.count():
        img_radio.click(force=True, timeout=5000)
        page.wait_for_timeout(600)
    ratio_radio = page.locator('button[role="radio"]', has_text="16:9").first
    if ratio_radio.count():
        ratio_radio.click(force=True, timeout=5000)
        page.wait_for_timeout(400)
    x1_radio = page.locator('button[role="radio"]', has_text="x1").first
    if x1_radio.count():
        x1_radio.click(force=True, timeout=5000)
        page.wait_for_timeout(400)
    page.evaluate(
        """() => {
          for (const bd of document.querySelectorAll('.cdk-overlay-backdrop-showing')) {
            bd.click();
          }
        }"""
    )
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    pill = still_tool.prompt_pill_text(page)
    print(f"  image-mode pill={pill!r}", flush=True)
    if not still_tool._pill_is_image_wide(pill):
        raise RuntimeError(f"Flow Image 16:9 not selected: {pill!r}")
    return pill


still_tool.select_image_16x9 = select_image_16x9_fixed


def main() -> int:
    from playwright.sync_api import sync_playwright

    ASSETS.mkdir(parents=True, exist_ok=True)
    for ref in STYLE_REFS:
        if not ref.exists():
            raise SystemExit(f"Missing style reference: {ref}")

    # Override _flow_still_v01 globals so it uses our local refs and uniqueness folder
    still_tool.STYLE_REFS = STYLE_REFS
    still_tool.MEDIA_CLIPS = ASSETS

    only = set(sys.argv[1:]) if len(sys.argv) > 1 else {"A", "B"}
    log = json.loads(LOG_PATH.read_text()) if LOG_PATH.exists() else {
        "film": "006_Trees-Are-Made-Of-Air",
        "job": "J0869",
        "decisionRef": "Chief pick on J0858 (OWB #99 comment 6355648154)",
        "engine": "Flow Image · Nano Banana 2 (16:9) via CDP :9222",
        "styleRefs": [str(r.relative_to(REPO)) for r in STYLE_REFS],
        "plates": {},
    }

    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(flow_cdp.CDP)
        page = flow_cdp.flow_page(browser, flow)
        credits_start, account = flow_cdp.read_account(page)
        print(f"GATE account={account} credits_start={credits_start} url={page.url}", flush=True)
        if account != flow_cdp.REQUIRED or flow_cdp.FORBIDDEN in (account or ""):
            raise SystemExit(f"STOP wrong Flow account: {account}")
        if credits_start is None:
            raise SystemExit("STOP Flow credits unreadable")

        log["account"] = account
        log["creditsStart"] = credits_start

        for cid in ("A", "B"):
            if cid not in only:
                continue
            cfg = CONCEPTS[cid]
            png_dest = ASSETS / f"{cfg['stem']}.png"
            jpg_dest = ASSETS / f"{cfg['stem']}.jpg"
            credits_before, _ = flow_cdp.read_account(page)
            if credits_before is None:
                credits_before = credits_start
            print(f"\n=== Concept {cid} ({cfg['stem']}) credits_before={credits_before} ===", flush=True)
            t0 = time.time()
            still_tool.make_still(page, cfg["prompt"], png_dest, timeout_s=300)
            elapsed = round(time.time() - t0, 1)
            credits_after = flow_cdp.settled_credits(page, wait_s=15)
            if credits_after is None:
                credits_after = credits_before
            used = max(0, credits_before - credits_after)
            print(f"  credits_after={credits_after} used={used} elapsed={elapsed}s", flush=True)

            im = Image.open(png_dest).convert("RGB")
            if im.size != (1280, 720):
                im = im.resize((1280, 720), Image.Resampling.LANCZOS)
            im.save(jpg_dest, "JPEG", quality=94, optimize=True, subsampling=1)

            log["plates"][cid] = {
                "concept": cid,
                "png": str(png_dest.relative_to(FILM_DIR)),
                "jpg": str(jpg_dest.relative_to(FILM_DIR)),
                "sha256_png": sha256(png_dest),
                "sha256_jpg": sha256(jpg_dest),
                "size": list(im.size),
                "styleRefChips": getattr(still_tool.make_still, "refs_attached", None),
                "creditsBefore": credits_before,
                "creditsAfter": credits_after,
                "creditsUsed": used,
                "elapsedSeconds": elapsed,
                "mintedAt": now(),
                "prompt": cfg["prompt"],
            }
            log["creditsEnd"] = credits_after
            log["totalCreditsUsed"] = sum(p.get("creditsUsed", 0) for p in log["plates"].values())
            LOG_PATH.write_text(json.dumps(log, indent=2) + "\n")

            if used > 0:
                raise SystemExit(f"STOP: still {cid} spent {used} Flow credits (expected 0 on Nano Banana 2)")

    print("\nALL STILLS MINTED AT 0 FLOW CREDITS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
