#!/usr/bin/env python3
"""Mint THREE lettered HOS Short covers via Flow Image / Nano Banana on CDP :9222.

Ben "Almost" (after live_v05): teal middles must be ALL-CAPS chunky like live
002 "IN THE" / "BEFORE" / "TABLE" — not lowercase thin. Keep scenes / Explorer.
Paint lettering INTO the image (Gallium + Tellurium style refs).

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
OUT_DIR = HERE / "covers_live_v06"
QA_DIR = OUT_DIR / "_qa_mint"
REJECT_DIR = OUT_DIR / "_rejected"
LOG_PATH = OUT_DIR / "MINT_LOG.json"
# Reuse approved v05 scenes (composition lock)
SCENES = HERE / "covers_live_v05" / "_scenes"

GALLIUM = REPO / (
    "02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/"
    "08_Thumbnail/Shorts/hos_002_s03_gallium_cover_live_v02.jpg"
)
TELLURIUM = REPO / (
    "02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/"
    "08_Thumbnail/Shorts/hos_002_s04_tellurium_cover_live_v02.jpg"
)
OTHER_TABLE = REPO / (
    "02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/"
    "08_Thumbnail/Shorts/hos_002_s05_other_table_cover_live_v02.jpg"
)

LETTER_LOCK = (
    "LETTER STYLE LOCK from the attached live Short covers (Gallium / Tellurium / "
    "What Other Table): paint HUGE chunky bevelled 3D display letters INTO the image — "
    "cream and gold faces, thick dark outline, deep extrude/drop shadow. Three stacked "
    "lines across the TOP of the frame filling about 85 to 95 percent of the width. "
    "EVERY LINE IS ALL CAPITAL LETTERS — no lowercase anywhere. "
    "The middle line is the SAME chunky bevelled block style as the gold/cream letters "
    "(just slightly smaller), painted TEAL — match the weight of live 'IN THE', 'BEFORE', "
    "and 'TABLE' exactly. NOT thin. NOT script. NOT serif. NOT lowercase. "
    "Letters must NOT touch the frame edges — leave a clear margin. Painted illustration "
    "lettering baked into the artwork, NOT a UI overlay, NOT a transparent text box, "
    "NOT a system font stamp."
)

SCENE_LOCK = (
    "SCENE LOCK from the attached scene ingredient: keep the same painted scene, hero "
    "objects, lighting, and the Explorer (messy brown hair, round gold glasses, teal coat, "
    "tan vest, satchel) in the same place and scale. Do not replace the scene. Only add "
    "or replace the top lettering stack."
)

HARD_REJECT = (
    "HARD REJECT: film-frame letterbox, watermark, HUD, Orbit orange robot, photoreal "
    "photo, live-action, flat paper sticker text, thin serif overlay, lowercase teal, "
    "thin teal, script teal, misspelled words."
)


def letter_prompt(lines: list[tuple[str, str]], scene_note: str) -> str:
    L1, L2, L3 = lines
    return f"""{LETTER_LOCK}
{SCENE_LOCK}
Premium Animistry-class painted 3D cartoon still, PORTRAIT 9:16 tall frame.
{scene_note}

EXACT LETTERING — spell letter-by-letter, ALL CAPITALS, zero typos, zero extra letters:
Line 1 ({L1[1]}, large chunky ALL-CAPS): {L1[0]}
Line 2 ({L2[1]}, smaller chunky teal ALL-CAPS like live BEFORE / IN THE / TABLE): {L2[0]}
Line 3 ({L3[1]}, BIGGEST gold punch ALL-CAPS): {L3[0]}

Confirm spelling (ALL CAPS): {" / ".join(t for t, _ in lines)}
Silent still. Single frame.
{HARD_REJECT}"""


COVERS = {
    "s01": {
        "out": "hos_004_s01_how_small_cover_live_v06.jpg",
        "scene": SCENES / "s01_scene.jpg",
        "expect": ["HOW", "SO", "SMALL?"],
        "lines": [("HOW", "cream"), ("SO", "teal"), ("SMALL?", "gold")],
        "scene_note": (
            "Victorian library desk: giant gold coin under a knife; Explorer small in "
            "lower third reacting amazed."
        ),
    },
    "s02": {
        "out": "hos_004_s02_every_eighth_cover_live_v06.jpg",
        "scene": SCENES / "s02_scene.jpg",
        "expect": ["EVERY", "EIGHTH", "ELEMENT?"],
        "lines": [("EVERY", "cream"), ("EIGHTH", "teal"), ("ELEMENT?", "gold")],
        "scene_note": (
            "Scholar desk with a row of eight blank cream cards; eighth card soft gold "
            "glow; Explorer small lower right reacting."
        ),
    },
    "s06": {
        "out": "hos_001_s06_carbolic_spray_cover_live_v06.jpg",
        "scene": SCENES / "s06_scene.jpg",
        "expect": ["THE", "CARBOLIC", "SPRAY"],
        "lines": [("THE", "cream"), ("CARBOLIC", "teal"), ("SPRAY", "gold")],
        "scene_note": (
            "1860s operating theatre: carbolic mist spraying over a wooden table with "
            "instruments; white cloth — NO open wounds, NO blood; period surgeon at the "
            "spray. Portrait crop focusing on spray mist and table."
        ),
    },
}


def spell_ok(path: Path, expect: list[str]) -> tuple[bool, str]:
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


def scene_ok(path: Path, key: str) -> tuple[bool, str]:
    """Reject wrong-scene grabs (Gallium droplet, coin desk on s06, etc.)."""
    from PIL import Image

    im = Image.open(path).convert("RGB")
    w, h = im.size
    bot = im.crop((0, int(h * 0.45), w, h)).resize((90, 60))
    px = list(bot.getdata())
    n = len(px)
    silver = sum(1 for r, g, b in px if abs(r - g) < 25 and abs(g - b) < 25 and 130 < r < 230) / n
    white = sum(1 for r, g, b in pix_white(px)) / n
    warm_gold = sum(1 for r, g, b in px if r > 160 and 100 < g < 210 and b < 100 and r > b + 50) / n
    # Fingerprint vs style refs
    fp = _fingerprint(path)
    banned = _BANNED_FPS or _load_banned_fps()
    if fp in banned:
        return False, f"banned_fp={fp[:10]}"
    if key == "s02":
        # Cards row scene — reject liquid-metal silver blob (Gallium)
        if silver > 0.08:
            return False, f"s02 looks like gallium silver={silver:.3f}"
        return True, f"s02 silver={silver:.3f} ok"
    if key == "s06":
        # Mist/theatre — reject coin-desk (high warm gold, low white mist)
        if warm_gold > 0.12 and white < 0.02:
            return False, f"s06 looks like coin desk gold={warm_gold:.3f} white={white:.3f}"
        return True, f"s06 gold={warm_gold:.3f} white={white:.3f}"
    if key == "s01":
        return True, f"s01 gold={warm_gold:.3f}"
    return True, "ok"


def pix_white(px):
    for r, g, b in px:
        if r > 200 and g > 200 and b > 200:
            yield r, g, b


def _fingerprint(path: Path) -> str:
    from PIL import Image
    import hashlib

    im = Image.open(path).convert("RGB").resize((48, 48))
    return hashlib.md5(im.tobytes()).hexdigest()


# Known wrong-asset fingerprints (style refs + prior keeps we must not re-grab)
_BANNED_FPS: set[str] = set()


def _load_banned_fps() -> set[str]:
    fps: set[str] = set()
    for p in (GALLIUM, TELLURIUM, OTHER_TABLE):
        if p.exists():
            fps.add(_fingerprint(p))
    # Also ban already-kept s01 so s06 cannot steal it
    s01 = OUT_DIR / "hos_004_s01_how_small_cover_live_v06.jpg"
    if s01.exists():
        fps.add(_fingerprint(s01))
    return fps


def fetch_cdn_portrait(page, dest: Path, before_srcs: set[str]) -> bool:
    """Click newest portrait tile and pull THAT tile's CDN URL (not style-ref leftovers)."""
    hit = page.evaluate(
        """(beforeList) => {
          const before = new Set(beforeList || []);
          const imgs=[...document.querySelectorAll('img')].map(i=>{
            const r=i.getBoundingClientRect();
            const src=i.currentSrc||i.src||'';
            return {src,w:r.width,h:r.height,y:r.y,x:r.x,area:r.width*r.height,
                    portrait:r.height>r.width*1.05, neu: !!(src && !before.has(src))};
          }).filter(i => i.w>90 && i.h>120 && i.y>70 && i.y<780 && i.portrait);
          const neu = imgs.filter(i => i.neu);
          // HARD: only NEW tiles — never fall back to old style-ref portraits
          if (!neu.length) return null;
          neu.sort((a,b)=>b.area-a.area);
          return neu[0];
        }""",
        list(before_srcs),
    )
    if not hit:
        print("  CDN: no NEW portrait tile yet", flush=True)
        return False
    try:
        page.mouse.click(hit["x"] + hit["w"] / 2, hit["y"] + hit["h"] / 2)
        page.wait_for_timeout(1100)
    except Exception:
        pass

    # Re-read NEW portrait srcs after click (lightbox often upgrades to full CDN)
    after = page.evaluate(
        """(beforeList) => {
          const before = new Set(beforeList || []);
          const out = [];
          for (const i of document.querySelectorAll('img')) {
            const r = i.getBoundingClientRect();
            const src = i.currentSrc || i.src || '';
            if (!src || src.length < 30) continue;
            if (r.width < 90 || r.height < 120) continue;
            if (!(r.height > r.width * 1.05)) continue;
            const neu = !before.has(src);
            out.push({src, w:r.width, h:r.height, area:r.width*r.height, neu,
                      y:r.y, big:r.width>400});
          }
          // Prefer NEW + largest on screen (lightbox)
          out.sort((a,b) => Number(b.neu)-Number(a.neu) || Number(b.big)-Number(a.big) || b.area-a.area);
          return out.slice(0, 8);
        }""",
        list(before_srcs),
    ) or []

    # Seed with the clicked tile src first
    seed = [hit.get("src")] if hit.get("src") else []
    urls = []
    for u in seed + [x["src"] for x in after if x.get("neu")]:
        if u and u not in urls:
            urls.append(u)
    if not urls:
        print("  CDN: no NEW urls after click", flush=True)
        return False

    dest.parent.mkdir(parents=True, exist_ok=True)
    from PIL import Image
    import io

    banned = _BANNED_FPS or _load_banned_fps()
    for i, url in enumerate(urls[:8]):
        try:
            fetch_url = url
            fetch_url = re.sub(r"=s\d+", "=s0", fetch_url)
            fetch_url = re.sub(r"=w\d+", "=w2048", fetch_url)
            if not re.search(
                r"googleusercontent|ggpht|flow-content|getMediaUrlRedirect|/asb/",
                fetch_url,
                re.I,
            ):
                # Still try — Flow sometimes uses other hosts
                pass
            resp = page.request.get(fetch_url, timeout=60000)
            if not resp.ok:
                continue
            body = resp.body()
            if len(body) < 40000:
                continue
            try:
                im = Image.open(io.BytesIO(body)).convert("RGB")
            except Exception:
                continue
            w, h = im.size
            if (w, h) == (1122, 1402):
                print(f"  CDN reject explorer-sheet {w}x{h}", flush=True)
                continue
            if h <= w * 1.05 or w < 500 or h < 700:
                print(f"  CDN skip {w}x{h} url#{i}", flush=True)
                continue
            # Fingerprint ban: style refs / already-kept wrong grabs
            tmp = dest.with_suffix(".cdn_try.png")
            im.save(tmp, format="PNG")
            fp = _fingerprint(tmp)
            if fp in banned:
                print(f"  CDN reject banned fingerprint url#{i} fp={fp[:10]}", flush=True)
                continue
            shutil.copy2(tmp, dest)
            print(
                f"  CDN fetch ok {w}x{h} bytes={len(body)} url#{i} fp={fp[:10]} neu_only",
                flush=True,
            )
            return True
        except Exception as e:
            print(f"  CDN fetch warn #{i}: {e}", flush=True)
    return False


def download_fullres(page, dest: Path, before_srcs: set[str], timeout_s: float = 300) -> Path:
    """Wait for NEW gen, then CDN-fetch full res (fallback to v02 tile/menu)."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    saw_progress = False
    while time.time() - t0 < timeout_s:
        try:
            flow.dismiss_soft_prompts(page)
        except Exception:
            pass
        pct = page.evaluate(
            """() => {
              const t = (document.body && document.body.innerText) || '';
              const m = t.match(/\\b(\\d{1,3})%/);
              return m ? Number(m[1]) : null;
            }"""
        )
        body_snip = v02.page_text(page, 2500)
        gen_hint = pct is not None or bool(
            re.search(
                r"\b\d{1,3}%\b|in the queue|generat(?:ing|e)|rendering|Creating your",
                body_snip,
                re.I,
            )
        )
        if gen_hint:
            saw_progress = True
        srcs = v02.gallery_media_srcs(page)
        new_srcs = [s for s in srcs if s not in before_srcs]
        print(
            f"  image poll new_srcs={len(new_srcs)} pct={pct} gen_hint={gen_hint} "
            f"saw_progress={saw_progress} elapsed={int(time.time()-t0)}s",
            flush=True,
        )
        # Flow sometimes sticks at 90% with the still already on the rail —
        # allow fetch once a NEW src exists and we've waited a bit.
        stuck_ready = bool(new_srcs) and (time.time() - t0 > 18)
        if gen_hint and (pct is None or pct < 100) and not stuck_ready:
            page.wait_for_timeout(2500)
            continue
        ready = saw_progress or (time.time() - t0 > 40) or stuck_ready
        if ready and new_srcs:
            if fetch_cdn_portrait(page, dest, before_srcs):
                from PIL import Image

                im = Image.open(dest)
                if im.size != (1122, 1402) and im.size[1] > im.size[0]:
                    # Scene/fingerprint check early
                    tmp_check = dest.with_suffix(".early.jpg")
                    im.convert("RGB").save(tmp_check, quality=90)
                    # key unknown here — only ban fingerprint
                    if _fingerprint(tmp_check) in (_BANNED_FPS or _load_banned_fps()):
                        print("  early reject banned fp — keep polling", flush=True)
                    else:
                        return dest
            # Fallback tile screenshot ONLY of NEW srcs
            if v02._screenshot_largest_new_portrait(page, dest, before_srcs):
                from PIL import Image

                im = Image.open(dest)
                if im.size != (1122, 1402) and im.size[1] > im.size[0] and im.size[0] >= 350:
                    return dest
        page.wait_for_timeout(3000)
    raise RuntimeError(f"Timed out waiting for NEW portrait Flow still → {dest}")


def mint_one(page, key: str, try_n: int, credits0) -> dict:
    spec_c = COVERS[key]
    prompt = letter_prompt(spec_c["lines"], spec_c["scene_note"])
    if try_n == 2:
        prompt += (
            "\nRETRY: previous try had lowercase or thin teal. Spell EXACTLY "
            f"{' / '.join(spec_c['expect'])} in ALL CAPITALS. Teal middle "
            f"'{spec_c['lines'][1][0]}' must be chunky bevelled ALL-CAPS like live "
            "BEFORE / IN THE / TABLE."
        )
    raw_path = QA_DIR / f"{key}_try{try_n}_raw.png"
    final_jpg = OUT_DIR / spec_c["out"]
    final_png = final_jpg.with_suffix(".png")
    print(f"\n=== LETTERED MINT v06 {key} try={try_n} → {final_jpg.name} ===", flush=True)

    v02.close_overlays(page)
    v02.select_image_9x16(page)
    credits_before, active = v02.read_credits(page)
    v02.close_overlays(page)

    # Clear leftover chips aggressively (wrong CDN grabs were style-ref leftovers)
    for _ in range(16):
        before = v02.ingredient_chip_count(page)
        v02.clear_prompt_attachments(page)
        page.wait_for_timeout(200)
        after = v02.ingredient_chip_count(page)
        if after == 0 or after >= before:
            break
    # Style refs first (lettering), then scene — keep to 3 so scene stays dominant
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

    download_fullres(page, raw_path, before_srcs=before_srcs, timeout_s=300)
    tmp_img = QA_DIR / f"{key}_try{try_n}_decoded.png"
    from PIL import Image

    Image.open(raw_path).convert("RGB").save(tmp_img)
    # If tile-small, upscale before geometry QA
    im = Image.open(tmp_img)
    if im.size[0] < 600 and im.size[0] >= 350 and im.size[1] > im.size[0]:
        up = im.resize((1080, 1920), Image.Resampling.LANCZOS)
        up.save(tmp_img)
        print(f"  upscaled tile {im.size} → 1080x1920", flush=True)

    verdict, reason, qa_meta = v02.qa_still(tmp_img)
    print(f"  QA geometry {verdict}: {reason}", flush=True)

    if verdict == "KEEP":
        v02.normalize_to_png(tmp_img, final_png)
        Image.open(final_png).convert("RGB").save(final_jpg, quality=92, optimize=True)
        ok_spell, spell_detail = spell_ok(final_jpg, spec_c["expect"])
        ok_scene, scene_detail = scene_ok(final_jpg, key)
        qa_meta["spell_heuristic"] = spell_detail
        qa_meta["scene_heuristic"] = scene_detail
        if not ok_spell:
            verdict, reason = "FAIL", f"lettering colours weak: {spell_detail}"
            REJECT_DIR.mkdir(parents=True, exist_ok=True)
            shutil.copy2(final_png, REJECT_DIR / f"{key}_try{try_n}_noletters.png")
            print(f"  SPELL/COLOUR FAIL {spell_detail}", flush=True)
        elif not ok_scene:
            verdict, reason = "FAIL", f"wrong scene: {scene_detail}"
            REJECT_DIR.mkdir(parents=True, exist_ok=True)
            shutil.copy2(final_png, REJECT_DIR / f"{key}_try{try_n}_wrongscene.png")
            print(f"  SCENE FAIL {scene_detail}", flush=True)
            try:
                final_jpg.unlink(missing_ok=True)
                final_png.unlink(missing_ok=True)
            except Exception:
                pass
        else:
            reason = f"{reason}; {spell_detail}; {scene_detail}"
            # Ban this keep so later slots cannot re-grab it
            _BANNED_FPS.add(_fingerprint(final_jpg))
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
    for p in (GALLIUM, TELLURIUM):
        if not p.exists():
            raise SystemExit(f"missing style ref {p}")
    # Quarantine prior s02/s06 outputs when reminting those keys (wrong CDN grabs)
    quarantine_map = {
        "s02": [
            "hos_004_s02_every_eighth_cover_live_v06.jpg",
            "hos_004_s02_every_eighth_cover_live_v06.png",
        ],
        "s06": [
            "hos_001_s06_carbolic_spray_cover_live_v06.jpg",
            "hos_001_s06_carbolic_spray_cover_live_v06.png",
        ],
    }
    for k, names in quarantine_map.items():
        if k not in keys:
            continue
        for bad_name in names:
            bad = OUT_DIR / bad_name
            if not bad.exists():
                continue
            REJECT_DIR.mkdir(parents=True, exist_ok=True)
            dest = REJECT_DIR / f"pre_remint_{bad.name}"
            shutil.move(str(bad), str(dest))
            print(f"quarantine {bad.name} → {dest.name}", flush=True)
    _BANNED_FPS.clear()
    _BANNED_FPS.update(_load_banned_fps())
    print(f"banned_fps={len(_BANNED_FPS)}", flush=True)

    from playwright.sync_api import sync_playwright

    log: dict = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "cdp": CDP,
        "engine": "Flow Image / Nano Banana / 9:16 lettered covers v06 ALLCAPS teal",
        "style_refs": [str(GALLIUM), str(TELLURIUM), str(OTHER_TABLE)],
        "covers": {},
        "note": "Ben Almost — teal middles ALL-CAPS chunky like live BEFORE/IN THE/TABLE",
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
