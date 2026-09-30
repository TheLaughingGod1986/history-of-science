#!/usr/bin/env python3
"""Mint THREE lettered HOS Short covers via Flow Image / Nano Banana on CDP :9222.

Ben 12:59: paint lettering INTO the image (not system-font overlay). Style refs =
Gallium in the Gap + Tellurium before Iodine. Keep scenes / Explorer / clear edges.
Spell-check letter-by-letter; regenerate on misspell.

HARD: new Flow tab only; never touch Studio :9460; max 2 tries each.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow  # noqa: E402

# Reuse Image-mode helpers from v02 mint
V02 = Path(__file__).resolve().parent / "_mint_covers_live_v02_stills_cdp.py"
spec = importlib.util.spec_from_file_location("mint_v02", V02)
v02 = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(v02)

CDP = os.environ.get("ORBIT_FLOW_CDP", "http://127.0.0.1:9222")
REQUIRED = "benoats@googlemail.com"
PINNED = os.environ.get(
    "HOS_FLOW_PROJECT_URL",
    "https://flow.google.com/project/30a34afb-8d9c-4eac-83ba-012d97f6b1b5",
)

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE / "covers_live_v05"
QA_DIR = OUT_DIR / "_qa_mint"
REJECT_DIR = OUT_DIR / "_rejected"
LOG_PATH = OUT_DIR / "MINT_LOG.json"
SCENES = OUT_DIR / "_scenes"

GALLIUM = REPO / (
    "02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/"
    "08_Thumbnail/Shorts/hos_002_s03_gallium_cover_live_v02.jpg"
)
TELLURIUM = REPO / (
    "02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/"
    "08_Thumbnail/Shorts/hos_002_s04_tellurium_cover_live_v02.jpg"
)

LETTER_LOCK = (
    "LETTER STYLE LOCK from the two attached live Short covers (Gallium / Tellurium): "
    "paint HUGE chunky bevelled 3D display letters INTO the image — cream and gold faces, "
    "thick dark outline, deep extrude/drop shadow. Three stacked lines across the TOP of "
    "the frame filling about 85 to 90 percent of the width. The middle line is the SAME "
    "chunky bevelled style, just smaller, painted TEAL. Letters must NOT touch the frame "
    "edges — leave a clear margin. This is painted illustration lettering baked into the "
    "artwork, NOT a UI overlay, NOT a transparent text box, NOT a system font stamp."
)

SCENE_LOCK = (
    "SCENE LOCK from the attached scene ingredient: keep the same painted scene, hero "
    "objects, lighting, and the Explorer (messy brown hair, round gold glasses, teal coat, "
    "tan vest, satchel) in the same place and scale. Do not replace the scene. Only add "
    "or replace the top lettering stack."
)

HARD_REJECT = (
    "HARD REJECT: film-frame letterbox, watermark, HUD, Orbit orange robot, photoreal "
    "photo, live-action, flat paper sticker text, thin serif overlay, misspelled words."
)


def letter_prompt(lines: list[tuple[str, str]], scene_note: str) -> str:
    """lines = [(text, role)] role in cream|teal|gold"""
    L1, L2, L3 = lines
    return f"""{LETTER_LOCK}
{SCENE_LOCK}
Premium Animistry-class painted 3D cartoon still, PORTRAIT 9:16 tall frame.
{scene_note}

EXACT LETTERING — spell letter-by-letter, zero typos, zero extra letters:
Line 1 ({L1[1]}, large chunky): {L1[0]}
Line 2 ({L2[1]}, smaller chunky teal): {L2[0]}
Line 3 ({L3[1]}, BIGGEST gold punch): {L3[0]}

Confirm spelling: {" / ".join(t for t, _ in lines)}
Silent still. Single frame.
{HARD_REJECT}"""


COVERS = {
    "s01": {
        "out": "hos_004_s01_how_small_cover_live_v05.jpg",
        "scene": SCENES / "s01_scene.jpg",
        "expect": ["HOW", "so", "SMALL?"],
        "lines": [("HOW", "cream"), ("so", "teal"), ("SMALL?", "gold")],
        "scene_note": (
            "Victorian library desk: giant gold coin under a knife; Explorer small in "
            "lower third reacting amazed."
        ),
    },
    "s02": {
        "out": "hos_004_s02_every_eighth_cover_live_v05.jpg",
        "scene": SCENES / "s02_scene.jpg",
        "expect": ["EVERY", "eighth", "ELEMENT?"],
        "lines": [("EVERY", "cream"), ("eighth", "teal"), ("ELEMENT?", "gold")],
        "scene_note": (
            "Scholar desk with a row of eight blank cream cards; eighth card soft gold "
            "glow; Explorer small lower right reacting."
        ),
    },
    "s06": {
        "out": "hos_001_s06_carbolic_spray_cover_live_v05.jpg",
        "scene": SCENES / "s06_scene.jpg",
        "expect": ["THE", "carbolic", "SPRAY"],
        "lines": [("THE", "cream"), ("carbolic", "teal"), ("SPRAY", "gold")],
        "scene_note": (
            "1860s operating theatre: carbolic mist spraying over a wooden table with "
            "instruments; white cloth — NO open wounds, NO blood; period surgeon at the "
            "spray. Portrait crop focusing on spray mist and table."
        ),
    },
}


def spell_ok(path: Path, expect: list[str]) -> tuple[bool, str]:
    """Human-scale spell check via top-band heuristics + mandatory manual note.

    We cannot rely on tesseract here. Check that the top band has cream/gold/teal
    mass (lettering present) and leave exact spelling to visual Read after mint.
    """
    from PIL import Image

    im = Image.open(path).convert("RGB")
    w, h = im.size
    band = im.crop((0, 0, w, int(h * 0.38)))
    pix = list(band.resize((90, 40)).getdata())
    cream = sum(1 for r, g, b in pix if r > 200 and g > 180 and b > 140 and r >= g)
    gold = sum(1 for r, g, b in pix if r > 180 and 120 < g < 220 and b < 120 and r > b + 40)
    teal = sum(1 for r, g, b in pix if g > 110 and b > 110 and r < 140 and g > r + 15)
    n = len(pix)
    ok = cream > 0.02 * n and gold > 0.02 * n and teal > 0.008 * n
    detail = f"cream={cream/n:.3f} gold={gold/n:.3f} teal={teal/n:.3f} expect={'/'.join(expect)}"
    return ok, detail


def mint_one(page, key: str, try_n: int, credits0) -> dict:
    spec_c = COVERS[key]
    prompt = letter_prompt(spec_c["lines"], spec_c["scene_note"])
    if try_n == 2:
        prompt += (
            "\nRETRY: previous try had wrong or missing letters. Spell EXACTLY "
            f"{' / '.join(spec_c['expect'])}. Bigger punch word. Teal middle must be "
            "chunky bevelled like the gold/cream letters, just smaller."
        )
    raw_path = QA_DIR / f"{key}_try{try_n}_raw.png"
    final_jpg = OUT_DIR / spec_c["out"]
    final_png = final_jpg.with_suffix(".png")
    print(f"\n=== LETTERED MINT {key} try={try_n} → {final_jpg.name} ===", flush=True)

    v02.close_overlays(page)
    v02.select_image_9x16(page)
    credits_before, active = v02.read_credits(page)
    v02.close_overlays(page)

    v02.clear_prompt_attachments(page)
    # Attach order: Gallium (type), Tellurium (type), scene (composition)
    refs = [GALLIUM, TELLURIUM, spec_c["scene"]]
    attached = 0
    for ref in refs:
        if not ref.exists():
            print(f"  MISSING ref {ref}", flush=True)
            continue
        try:
            if v02.attach_style_ref_image_mode(page, ref):
                attached += 1
        except Exception as e:
            print(f"  attach fail {ref.name}: {e}", flush=True)
    chips = v02.ingredient_chip_count(page)
    print(
        f"  credits_before={credits_before} account={active} "
        f"attached={attached} chips={chips} pill={v02.pill_text(page)!r}",
        flush=True,
    )
    if chips < 2:
        raise RuntimeError(f"Need ≥2 ingredient chips (got {chips})")

    box = flow.editor_box(page)
    if not box:
        raise RuntimeError("prompt editor missing")
    page.mouse.click(box["x"] + min(box["w"] - 40, 200), box["y"] + max(8, box["h"] / 2))
    page.wait_for_timeout(150)
    page.keyboard.press("End")
    page.wait_for_timeout(80)
    existing = flow._editor_prompt_text(page) or ""
    if existing and not existing.lower().startswith("what do you want"):
        page.keyboard.insert_text("\n\n")
    page.keyboard.insert_text(prompt)
    page.wait_for_timeout(400)
    got = flow._editor_prompt_text(page) or ""
    chips_after = v02.ingredient_chip_count(page)
    print(f"  prompt_len={len(got)} chips_after={chips_after}", flush=True)
    if len(got) < 80:
        raise RuntimeError("prompt not armed")
    if chips_after < 2:
        print("  WARN chips lost — re-attaching", flush=True)
        for ref in refs:
            if ref.exists():
                try:
                    v02.attach_style_ref_image_mode(page, ref)
                except Exception as e:
                    print(f"  re-attach warn: {e}", flush=True)

    before_srcs = v02.gallery_media_srcs(page)
    page.screenshot(path=str(QA_DIR / f"{key}_try{try_n}_armed.png"), full_page=False)
    v02.submit_create(page)
    page.wait_for_timeout(900)
    confirmed = flow.confirm_generation_spend(page, timeout_s=12.0)
    print(f"  confirm_spend={confirmed}", flush=True)
    try:
        flow.dismiss_soft_prompts(page)
    except Exception:
        pass
    page.wait_for_timeout(2000)

    v02.download_newest_portrait(page, raw_path, before_srcs=before_srcs, timeout_s=300)
    tmp_img = QA_DIR / f"{key}_try{try_n}_decoded.png"
    from PIL import Image

    Image.open(raw_path).convert("RGB").save(tmp_img)
    verdict, reason, qa_meta = v02.qa_still(tmp_img)
    print(f"  QA geometry {verdict}: {reason}", flush=True)

    if verdict == "KEEP":
        v02.normalize_to_png(tmp_img, final_png)
        Image.open(final_png).convert("RGB").save(final_jpg, quality=92, optimize=True)
        ok_spell, spell_detail = spell_ok(final_jpg, spec_c["expect"])
        qa_meta["spell_heuristic"] = spell_detail
        if not ok_spell:
            verdict, reason = "FAIL", f"lettering colours weak: {spell_detail}"
            REJECT_DIR.mkdir(parents=True, exist_ok=True)
            shutil.copy2(final_png, REJECT_DIR / f"{key}_try{try_n}_noletters.png")
            print(f"  SPELL/COLOUR FAIL {spell_detail}", flush=True)
        else:
            reason = f"{reason}; {spell_detail}"
    else:
        REJECT_DIR.mkdir(parents=True, exist_ok=True)
        rej = REJECT_DIR / f"{key}_try{try_n}_{int(time.time())}.png"
        v02.normalize_to_png(tmp_img, rej)

    credits_after, _ = v02.read_credits(page)
    used = None
    if credits_before is not None and credits_after is not None:
        used = max(0, credits_before - credits_after)

    entry = {
        "key": key,
        "try": try_n,
        "out": str(final_jpg) if verdict == "KEEP" else None,
        "expect": spec_c["expect"],
        "raw": str(tmp_img),
        "account": active,
        "credits_before": credits_before,
        "credits_after": credits_after,
        "credits_used": used,
        "attached_refs": attached,
        "qa": verdict,
        "qa_reason": reason,
        "qa_meta": qa_meta,
        "pill": v02.pill_text(page),
        "pulled": datetime.now(timezone.utc).isoformat(),
    }
    (QA_DIR / f"{key}_try{try_n}.meta.json").write_text(json.dumps(entry, indent=2) + "\n")
    print(f"  RESULT {verdict} {reason}", flush=True)
    return entry


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=sorted(COVERS.keys()), action="append")
    ap.add_argument("--max-tries", type=int, default=2)
    args = ap.parse_args()
    keys = args.only or ["s01", "s02", "s06"]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    QA_DIR.mkdir(parents=True, exist_ok=True)
    REJECT_DIR.mkdir(parents=True, exist_ok=True)
    for c in COVERS.values():
        if not c["scene"].exists():
            raise SystemExit(f"missing scene {c['scene']}")
    if not GALLIUM.exists() or not TELLURIUM.exists():
        raise SystemExit("missing Gallium/Tellurium style refs")

    from playwright.sync_api import sync_playwright

    log: dict = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "cdp": CDP,
        "engine": "Flow Image / Nano Banana / 9:16 lettered covers",
        "style_refs": [str(GALLIUM), str(TELLURIUM)],
        "covers": {},
    }

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        page = ctx.new_page()
        try:
            page.goto(PINNED, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2800)
            flow.dismiss_banners(page)
            if "/project/" not in (page.url or ""):
                page.goto(
                    "https://flow.google.com/", wait_until="domcontentloaded", timeout=120_000
                )
                page.wait_for_timeout(2000)
                flow.dismiss_banners(page)
            credits0, active = v02.read_credits(page)
            log["credits_before_batch"] = credits0
            log["account"] = active
            print(f"GATE account={active} credits={credits0} url={page.url}", flush=True)
            if active and active not in {REQUIRED.lower(), "benoats@gmail.com"}:
                raise SystemExit(f"STOP wrong account: {active}")
            if credits0 is not None and credits0 < 30:
                raise SystemExit(f"STOP low credits={credits0}")

            for key in keys:
                attempts = []
                kept = None
                for try_n in range(1, args.max_tries + 1):
                    try:
                        entry = mint_one(page, key, try_n, credits0)
                        attempts.append(entry)
                        if entry.get("qa") == "KEEP" and entry.get("out"):
                            kept = entry
                            break
                    except Exception as e:
                        err = {
                            "key": key,
                            "try": try_n,
                            "qa": "ERROR",
                            "qa_reason": str(e),
                            "pulled": datetime.now(timezone.utc).isoformat(),
                        }
                        attempts.append(err)
                        print(f"  ERROR {key} try{try_n}: {e}", flush=True)
                        page.screenshot(
                            path=str(QA_DIR / f"{key}_try{try_n}_error.png"), full_page=False
                        )
                log["covers"][key] = {
                    "kept": kept,
                    "attempts": attempts,
                    "status": "KEEP" if kept else "FAIL",
                }

            credits1, _ = v02.read_credits(page)
            log["credits_after_batch"] = credits1
            log["finished_at"] = datetime.now(timezone.utc).isoformat()
            LOG_PATH.write_text(json.dumps(log, indent=2) + "\n")
            print(f"\nLOG → {LOG_PATH}", flush=True)
            print(json.dumps({k: v["status"] for k, v in log["covers"].items()}, indent=2))
            fails = [k for k, v in log["covers"].items() if v["status"] != "KEEP"]
            return 1 if fails else 0
        finally:
            try:
                page.close()
            except Exception:
                pass


if __name__ == "__main__":
    raise SystemExit(main())
