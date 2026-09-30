#!/usr/bin/env python3
"""Mint THREE HOS Short cover stills via Flow Image / Nano Banana 2 on CDP :9222.

HARD:
- Open NEW tab only. Never navigate/close other Flow tabs.
- Never touch HOS Studio Chrome on :9460.
- Max 2 tries per still.
- Portrait 9:16 (crop_9_16). Attach style refs as ingredients (Image mode).
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow  # noqa: E402

CDP = os.environ.get("ORBIT_FLOW_CDP", "http://127.0.0.1:9222")
REQUIRED = "benoats@googlemail.com"
CREDIT_RE = re.compile(r"([\d,]{1,7})\s*(?:Google\s+Flow\s+)?credits", re.I)
PINNED = os.environ.get(
    "HOS_FLOW_PROJECT_URL",
    "https://flow.google.com/project/30a34afb-8d9c-4eac-83ba-012d97f6b1b5",
)

PROJ = Path(__file__).resolve().parent
OUT_DIR = PROJ / "covers_live_v02" / "stills"
QA_DIR = OUT_DIR / "_qa_mint"
REJECT_DIR = OUT_DIR / "_rejected"
LOG_PATH = PROJ / "covers_live_v02" / "MINT_LOG.json"

STYLE_REFS = [
    REPO
    / "02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/08_Thumbnail/Shorts"
    / "hos_002_s04_tellurium_cover_live_v02.jpg",
    REPO
    / "02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/08_Thumbnail/Shorts"
    / "hos_002_s05_other_table_cover_live_v02.jpg",
    REPO / "01_Character/05_Generation-References/hos-explorer-reference-v01.jpg",
]
OPTIONAL_STYLE = (
    REPO
    / "02_Video-Projects/004_Whats-Really-Inside-An-Atom/08_Thumbnail/Selected"
    / "hos_004_thumb_B_cut_gold_live_v04.jpg"
)

HARD_REJECT = (
    "HARD REJECT: film-frame look, cinematic letterbox, UI, watermark, HUD, "
    "readable text or letters or numbers or symbols in the scene, see-through text boxes, "
    "Orbit orange robot, photoreal photo, live-action, flat 2D cel outlines."
)

STYLE_LOCK = (
    "STYLE LOCK from attached references: premium Animistry-class painted 3D cartoon "
    "(same warm painted polish as the attached HOS Short covers). Soft volumetric light, "
    "rich materials, finished feature-animation look — NOT photoreal, NOT film still. "
    "Match Explorer identity from the attached Explorer reference when he appears "
    "(messy brown hair, round gold glasses, teal overcoat, tan vest, brown bow tie, satchel). "
    "Use attached covers ONLY for paint style / lighting / depth — IGNORE any letters on them."
)

STILLS = {
    "s01": {
        "out": "s01_how_small_scene.png",
        "try1": f"""{STYLE_LOCK}
Premium Animistry-class painted 3D cartoon still, PORTRAIT 9:16 tall frame.
Warm Victorian library desk. HERO: a giant gold coin under a knife on the desk
(coin fills lower-mid frame, knife tip resting on coin edge). Soft warm lamp light.
Explorer (from attached ref) is SMALL in the LOWER third, reacting curious/amazed —
about 1/5 frame height, garnish only, not hero. CALM EMPTY UPPER third for later
title text (no objects, no bright glow, no characters up there).
No letters anywhere in the scene. Silent still. Single frame.
{HARD_REJECT}""",
        "try2": f"""{STYLE_LOCK}
Portrait 9:16 Animistry painted 3D cartoon. Close-medium on a warm oak desk:
oversized gleaming gold coin under a steel knife — clear hero objects in lower half.
Tiny Explorer in bottom corner reacting amazed (teal coat, gold glasses). Upper third
stays calm empty negative space for text. No readable text. Not photoreal. Not film.
{HARD_REJECT}""",
    },
    "s02": {
        "out": "s02_every_eighth_scene.png",
        "try1": f"""{STYLE_LOCK}
Premium Animistry-class painted 3D cartoon still, PORTRAIT 9:16 tall frame.
Newlands-era scholar desk. HERO: a neat row of EIGHT blank cream rectangular cards
as physical objects on the desk — the EIGHTH card has a soft warm gold glow rim
(octaves idea made physical). Cards have NO letters, NO numbers, NO symbols —
blank cream paper only. Soft warm desk lamp. Explorer SMALL in LOWER third reacting
curious (teal coat, gold glasses), garnish. CALM EMPTY UPPER third for title text.
No readable text anywhere. Silent still. Single frame.
{HARD_REJECT}""",
        "try2": f"""{STYLE_LOCK}
Portrait 9:16 Animistry painted 3D cartoon. Warm wood desk with eight blank cream
cards in a clear horizontal row; eighth card glowing softly. Tiny Explorer lower
reacting. Upper third empty and calm. Zero text on cards. Painted not photoreal.
{HARD_REJECT}""",
    },
    "s03": {
        "out": "s03_they_laughed_scene.png",
        "try1": f"""{STYLE_LOCK}
Premium Animistry-class painted 3D cartoon still, PORTRAIT 9:16 tall frame.
1840s hospital ward wood interior. HERO: stone/ceramic basin of water with a bar of soap
in the lower-mid foreground. Small background doctors in dark frocks turning away / scoffing
pose (tiny figures, not hero faces) OR Explorer SMALL in LOWER area reacting shocked/pleading
toward the basin. Warm wood ward light. CALM EMPTY UPPER third for later title text.
No letters, no UI. Silent still. Single frame. Semmelweis handwash beat as picture only.
{HARD_REJECT}""",
        "try2": f"""{STYLE_LOCK}
Portrait 9:16 Animistry painted 3D cartoon. 1840s wood ward: basin + soap hero in lower
half. Tiny scoffing doctors in soft background OR small Explorer pleading toward basin.
Upper third calm empty. No text. Painted cartoon polish, not photoreal film.
{HARD_REJECT}""",
    },
}


def page_text(page, n: int = 12000) -> str:
    try:
        return page.locator("body").inner_text(timeout=8000)[:n]
    except Exception:
        return ""


def open_account_menu(page) -> None:
    for sel in (
        '[aria-label*="Account details" i]',
        '[aria-label*="Google Account" i]',
        'button:has-text("ULTRA")',
        "text=ULTRA",
    ):
        try:
            loc = page.locator(sel).first
            if loc.count() == 0:
                continue
            loc.click(timeout=2500)
            time.sleep(1.4)
            return
        except Exception:
            continue


def close_overlays(page) -> None:
    for _ in range(4):
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        page.wait_for_timeout(120)
    try:
        page.mouse.click(640, 280)
    except Exception:
        pass
    page.wait_for_timeout(200)


def read_credits(page) -> tuple[int | None, str | None]:
    def parse(text: str) -> tuple[int | None, str | None]:
        emails = set(
            re.findall(r"[A-Za-z0-9._%+-]+@(?:gmail|googlemail)\.com", text, flags=re.I)
        )
        active = None
        if REQUIRED.lower() in {e.lower() for e in emails}:
            active = REQUIRED.lower()
        elif emails:
            active = sorted(emails)[0].lower()
        hits = [int(m.group(1).replace(",", "")) for m in CREDIT_RE.finditer(text)]
        credits = None
        if hits:
            near = [c for c in hits if 100 <= c <= 20000]
            credits = near[0] if near else max(hits)
        return credits, active

    credits, active = parse(page_text(page))
    if credits is None or active is None:
        open_account_menu(page)
        credits2, active2 = parse(page_text(page))
        credits = credits if credits is not None else credits2
        active = active or active2
        close_overlays(page)
    else:
        close_overlays(page)
    return credits, active


def pill_text(page) -> str:
    return (
        page.evaluate(
            """() => {
          for (const b of document.querySelectorAll('button')) {
            const t = (b.innerText || '').trim().replace(/\\n/g, ' ');
            if (/Nano Banana|Video ·|Omni Flash|Omni 1|Veo 3|crop_|\\bImage\\b/i.test(t)) {
              const r = b.getBoundingClientRect();
              if (r.width > 40 && r.height > 16) return t.slice(0, 160);
            }
          }
          return '';
        }"""
        )
        or ""
    )


def _pill_is_image_9x16(pill: str) -> bool:
    if not pill:
        return False
    image_ok = bool(re.search(r"Nano Banana|Banana|\bImage\b", pill, re.I))
    if re.search(r"\bVideo\b|Veo\s*3|Omni", pill, re.I) and not re.search(
        r"Banana|Nano", pill, re.I
    ):
        return False
    ratio_ok = bool(re.search(r"9:16|crop_9_16|9\s*[:×x]\s*16", pill, re.I))
    return image_ok and ratio_ok


def select_image_9x16(page) -> None:
    pill0 = ""
    for _ in range(8):
        pill0 = pill_text(page)
        if pill0:
            break
        page.wait_for_timeout(400)
    print(f"  pill before={pill0!r}", flush=True)
    if _pill_is_image_9x16(pill0):
        print("  already Image/Nano Banana 9:16 — skip settings", flush=True)
        return
    flow._open_prompt_settings_pill(page)
    page.wait_for_timeout(900)
    # Image radio
    page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button[role=radio],button[role=tab],[role=radio]')) {
            const t = ((b.innerText||'')+' '+(b.getAttribute('aria-label')||'')).trim();
            if ((/\\bimage\\b/i.test(t) || /banana/i.test(t)) && !/video|veo|omni/i.test(t)) {
              const r = b.getBoundingClientRect();
              if (r.width > 20 && r.height > 16) { b.click(); return t.slice(0,80); }
            }
          }
          return null;
        }"""
    )
    page.wait_for_timeout(600)
    # 9:16 ratio
    clicked = page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button,[role=radio],[role=option]')) {
            const t = ((b.innerText||'')+' '+(b.getAttribute('aria-label')||'')).trim();
            if (/crop_9_16|\\b9:16\\b/.test(t)) { b.click(); return t.slice(0,60); }
          }
          return null;
        }"""
    )
    print(f"  ratio click={clicked!r}", flush=True)
    page.wait_for_timeout(400)
    # x1 if visible
    page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button')) {
            const t = (b.innerText || '').trim();
            if (t === 'x1') { b.click(); return true; }
          }
          return false;
        }"""
    )
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    page.wait_for_timeout(400)
    pill = pill_text(page)
    print(f"  image-mode pill={pill!r}", flush=True)
    if pill and re.search(r"\bVideo\b", pill) and not re.search(r"Banana|Image", pill, re.I):
        raise RuntimeError(f"Failed to switch to Image mode: {pill!r}")
    if pill and not re.search(r"9:16|crop_9_16", pill, re.I):
        # Retry open + click 9:16 once
        flow._open_prompt_settings_pill(page)
        page.wait_for_timeout(700)
        page.evaluate(
            """() => {
              for (const b of document.querySelectorAll('button,[role=radio]')) {
                const t = ((b.innerText||'')+' '+(b.getAttribute('aria-label')||'')).trim();
                if (/crop_9_16|\\b9:16\\b/.test(t)) { b.click(); return true; }
              }
              return false;
            }"""
        )
        page.wait_for_timeout(400)
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        pill = pill_text(page)
        print(f"  image-mode pill retry={pill!r}", flush=True)


def _find_upload_control(page):
    for pattern in (
        r"^Upload media$",
        r"Upload media",
        r"^Upload$",
        r"From (device|computer)",
    ):
        loc = page.get_by_role("button", name=re.compile(pattern, re.I))
        if loc.count():
            return loc.last
    loc = page.locator(
        'button[aria-label*="Upload" i], button:has-text("Upload"), '
        'button:has-text("cloud_upload")'
    )
    if loc.count():
        return loc.last
    return None


def attach_style_ref_image_mode(page, ref: Path) -> bool:
    """Upload a style ref while staying in Image / Nano Banana (no Frames/Veo switch)."""
    ref = Path(ref).resolve()
    if not ref.exists():
        raise FileNotFoundError(ref)
    before = flow._prompt_attachment_count(page)
    print(f"  attach style ref: {ref.name} (before={before})", flush=True)
    flow.ensure_agent_session(page)
    flow._open_create_picker(page)
    page.wait_for_timeout(500)
    uploads_tab = page.locator('button:has-text("Uploads")')
    if uploads_tab.count():
        try:
            uploads_tab.first.click(timeout=3000)
            page.wait_for_timeout(400)
        except Exception:
            pass
    # Reveal Upload via Add if needed
    if _find_upload_control(page) is None:
        for pattern in (r"^Add$", r"Add (media|image|file|to prompt)", r"^Create$"):
            loc = page.get_by_role("button", name=re.compile(pattern, re.I))
            if loc.count():
                try:
                    loc.last.click(force=True, timeout=3000)
                    page.wait_for_timeout(600)
                except Exception:
                    pass
                if _find_upload_control(page) is not None:
                    break
    up = _find_upload_control(page)
    if up is None:
        fi = page.locator('input[type="file"]')
        if fi.count() == 0:
            raise RuntimeError(f"Upload control missing for {ref.name}")
        fi.last.set_input_files(str(ref))
    else:
        try:
            with page.expect_file_chooser(timeout=15_000) as fc:
                up.click(force=True)
            fc.value.set_files(str(ref))
        except Exception:
            fi = page.locator('input[type="file"]')
            if fi.count() == 0:
                raise RuntimeError(f"Could not upload {ref.name}")
            fi.last.set_input_files(str(ref))
    # Consent
    for _ in range(6):
        agree = page.get_by_role(
            "button", name=re.compile(r"^(I agree|Agree|Accept)$", re.I)
        )
        if agree.count() == 0:
            break
        try:
            agree.last.click(force=True, timeout=3000)
            page.wait_for_timeout(800)
        except Exception:
            break
    page.wait_for_timeout(2200)
    if flow._prompt_attachment_count(page) > before:
        print(f"  auto-attached {ref.name}", flush=True)
        return True
    # Select newest tile + Add to Prompt
    page.evaluate(
        """() => {
          const imgs = [...document.querySelectorAll('img')].filter(i => {
            const r = i.getBoundingClientRect();
            return r.width > 48 && r.height > 48 && r.y > 60;
          });
          if (!imgs.length) return false;
          imgs[imgs.length-1].click();
          return true;
        }"""
    )
    page.wait_for_timeout(600)
    enabled = False
    try:
        enabled = flow._wait_add_to_prompt_enabled(page, timeout_s=25)
    except Exception:
        pass
    add = page.locator('button:has-text("Add to Prompt")')
    if add.count() and enabled:
        try:
            add.last.click(force=True, timeout=4000)
            page.wait_for_timeout(1200)
        except Exception as e:
            print(f"  Add to Prompt warn: {e}", flush=True)
    after = flow._prompt_attachment_count(page)
    ok = after > before
    print(f"  attach result {ref.name}: {ok} (after={after})", flush=True)
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    page.wait_for_timeout(300)
    return ok


def clear_prompt_attachments(page) -> None:
    """Best-effort remove prior chips so each still starts clean."""
    for _ in range(8):
        removed = page.evaluate(
            """() => {
              const btns = [...document.querySelectorAll('button')].filter(b => {
                const t = ((b.innerText||'')+' '+(b.getAttribute('aria-label')||'')).trim();
                const r = b.getBoundingClientRect();
                return r.width > 10 && r.height > 10 && r.width < 48 &&
                  (/close|clear|remove|delete|cancel/i.test(t) || t === '×' || t === 'x');
              });
              // Prefer chips near the prompt bar (lower half)
              const near = btns.filter(b => b.getBoundingClientRect().y > 400);
              const target = near[0] || btns[0];
              if (!target) return false;
              try { target.click(); return true; } catch (e) { return false; }
            }"""
        )
        if not removed:
            break
        page.wait_for_timeout(250)


def download_newest_image(page, dest: Path, timeout_s: float = 220) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        try:
            flow.dismiss_soft_prompts(page)
        except Exception:
            pass
        hit = page.evaluate(
            """() => {
              const imgs=[...document.querySelectorAll('img')].map(i=>{
                const r=i.getBoundingClientRect();
                return {x:r.x+r.width/2,y:r.y+r.height/2,w:r.width,h:r.height,y0:r.y,
                        src:i.currentSrc||i.src||''};
              }).filter(i=>i.w>100&&i.h>120&&i.y0>60);  // portrait-friendly
              imgs.sort((a,b)=>b.y0-a.y0 || b.w*b.h-a.w*a.h);
              return imgs[0]||null;
            }"""
        )
        body_snip = page_text(page, 2500)
        gen_hint = bool(
            re.search(
                r"\b\d{1,3}%\b|in the queue|generat(?:ing|e)|rendering",
                body_snip,
                re.I,
            )
        ) and "Start creating or drop media" not in body_snip
        print(
            f"  image poll hit={'yes' if hit else 'no'} "
            f"gen_hint={gen_hint} elapsed={int(time.time()-t0)}s",
            flush=True,
        )
        if hit:
            page.mouse.click(hit["x"], hit["y"])
            page.wait_for_timeout(1100)
            for label in ("Download", "download", "Save"):
                btn = page.get_by_role("button", name=re.compile(label, re.I))
                if btn.count():
                    try:
                        with page.expect_download(timeout=20000) as dl:
                            btn.first.click(timeout=4000)
                        d = dl.value
                        d.save_as(str(dest))
                        if dest.exists() and dest.stat().st_size > 40000:
                            return dest
                    except Exception as e:
                        print(f"  download via {label} failed: {e}", flush=True)
            src = hit.get("src") or page.evaluate(
                """() => {
                  const imgs=[...document.querySelectorAll('img')].map(i=>{
                    const r=i.getBoundingClientRect();
                    return {src:i.currentSrc||i.src,w:r.width,h:r.height};
                  }).filter(i=>i.w>200&&i.h>240&&i.src);
                  imgs.sort((a,b)=>b.w*b.h-a.w*a.h);
                  return imgs[0]?.src||null;
                }"""
            )
            if src and str(src).startswith("http"):
                data = page.evaluate(
                    """async (url) => {
                      const r = await fetch(url); const b = await r.arrayBuffer();
                      const u = new Uint8Array(b); let s='';
                      for (let i=0;i<u.length;i++) s+=String.fromCharCode(u[i]);
                      return btoa(s);
                    }""",
                    src,
                )
                dest.write_bytes(base64.b64decode(data))
                if dest.stat().st_size > 40000:
                    return dest
            if src and str(src).startswith("data:image"):
                b64 = str(src).split(",", 1)[-1]
                dest.write_bytes(base64.b64decode(b64))
                if dest.stat().st_size > 40000:
                    return dest
        page.wait_for_timeout(4000)
    try:
        page.screenshot(path=str(QA_DIR / "download_timeout.png"), full_page=False)
    except Exception:
        pass
    raise RuntimeError(f"Timed out waiting for Flow image still → {dest}")


def qa_still(path: Path) -> tuple[str, str, dict]:
    from PIL import Image, ImageStat

    im = Image.open(path).convert("RGB")
    w, h = im.size
    ratio = w / h
    meta = {"w": w, "h": h, "ratio": round(ratio, 4)}
    # Accept 9:16 or tall 3:4 (crop later)
    ok_916 = abs(ratio - 9 / 16) <= 0.08
    ok_34 = abs(ratio - 3 / 4) <= 0.08
    if w < 600 or h < 800:
        return "FAIL", f"too small {w}x{h}", meta
    if not (ok_916 or ok_34):
        return "FAIL", f"not tall portrait ratio={ratio:.3f}", meta
    # Heuristic: film-frame often has very dark letterbox bars or ultra-smooth photo noise
    small = im.resize((54, 96))
    px = list(small.getdata())
    dark = sum(1 for r, g, b in px if r < 18 and g < 18 and b < 18)
    whiteish = sum(1 for r, g, b in px if r > 245 and g > 245 and b > 245)
    if dark > 0.35 * len(px):
        return "FAIL", "likely letterbox / film-frame dark bars", meta
    if whiteish > 0.40 * len(px):
        return "FAIL", "too much white / UI", meta
    # Painted warmth: average shouldn't be cold grey photo
    st = ImageStat.Stat(im.resize((64, 64)))
    avg = tuple(int(v) for v in st.mean[:3])
    meta["avg_rgb"] = avg
    look = "painted" if (avg[0] > avg[2] + 8 or avg[1] > 60) else "uncertain"
    meta["look_guess"] = look
    return "KEEP", f"{w}x{h} ratio={ratio:.3f} look={look}", meta


def normalize_to_png(src: Path, dest: Path) -> Path:
    """Ensure final is PNG; center-crop 3:4 → 9:16 when needed; target ~1080x1920."""
    from PIL import Image

    im = Image.open(src).convert("RGB")
    w, h = im.size
    ratio = w / h
    target_r = 9 / 16
    if abs(ratio - target_r) > 0.02:
        # crop to 9:16 from center
        if ratio > target_r:
            new_w = int(h * target_r)
            x0 = (w - new_w) // 2
            im = im.crop((x0, 0, x0 + new_w, h))
        else:
            new_h = int(w / target_r)
            y0 = (h - new_h) // 2
            im = im.crop((0, y0, w, y0 + new_h))
    # Upscale/downscale to 1080x1920 for cover pipeline
    if im.size != (1080, 1920):
        im = im.resize((1080, 1920), Image.Resampling.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, format="PNG", optimize=True)
    return dest


def submit_create(page) -> None:
    clicked = page.evaluate(
        """() => {
          const ranked = [];
          for (const b of document.querySelectorAll('button')) {
            const t = (b.innerText || '').trim().replace(/\\n/g, ' ');
            if (!/arrow_forward/i.test(t)) continue;
            if (b.disabled || b.getAttribute('aria-disabled') === 'true') continue;
            const r = b.getBoundingClientRect();
            if (r.width < 8 || r.height < 8) continue;
            ranked.push({b, y: r.y, t});
          }
          if (!ranked.length) return null;
          ranked.sort((a, c) => c.y - a.y);
          ranked[0].b.click();
          return ranked[0].t;
        }"""
    )
    if not clicked:
        flow.submit_create(page)
    else:
        print(f"  js-clicked send ({clicked!r})", flush=True)


def mint_one(page, key: str, try_n: int, credits_session_start: int | None) -> dict:
    spec = STILLS[key]
    prompt = spec["try1"] if try_n == 1 else spec["try2"]
    raw_path = QA_DIR / f"{key}_try{try_n}_raw.bin"
    final_path = OUT_DIR / spec["out"]
    print(f"\n=== MINT {key} try={try_n} → {final_path.name} ===", flush=True)

    close_overlays(page)
    select_image_9x16(page)
    try:
        flow.force_outputs_x1(page)
    except Exception as e:
        print(f"  force_outputs_x1 warn: {e}", flush=True)
    try:
        flow._ensure_create_prompt_mode(page)
    except Exception as e:
        print(f"  create-mode warn: {e}", flush=True)

    # Fresh attachments each try
    clear_prompt_attachments(page)
    refs = [p for p in STYLE_REFS if p.exists()]
    if OPTIONAL_STYLE.exists():
        refs.append(OPTIONAL_STYLE)
    attached = 0
    for ref in refs:
        try:
            if attach_style_ref_image_mode(page, ref):
                attached += 1
            # Re-assert Image 9:16 after attach (some uploads flip settings)
            select_image_9x16(page)
        except Exception as e:
            print(f"  attach fail {ref.name}: {e}", flush=True)

    credits_before, active = read_credits(page)
    print(
        f"  credits_before={credits_before} account={active} attached={attached}",
        flush=True,
    )

    armed = False
    last_err: Exception | None = None
    for attempt in range(1, 4):
        try:
            flow.ensure_agent_session(page)
            flow.set_prompt(page, prompt)
            armed = True
            break
        except Exception as e:
            last_err = e
            print(f"  set_prompt attempt {attempt}/3 failed: {e}", flush=True)
            page.wait_for_timeout(700)
    if not armed:
        raise RuntimeError(f"Could not arm prompt: {last_err}")

    for _ in range(3):
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        page.wait_for_timeout(150)

    page.screenshot(path=str(QA_DIR / f"{key}_try{try_n}_armed.png"), full_page=False)
    print("  submitting Image Create…", flush=True)
    submit_create(page)
    page.wait_for_timeout(800)
    confirmed = flow.confirm_generation_spend(page, timeout_s=20.0)
    print(f"  confirm_spend={confirmed}", flush=True)
    flow.dismiss_soft_prompts(page)
    page.wait_for_timeout(3000)

    download_newest_image(page, raw_path, timeout_s=220)
    # Convert whatever format Flow gave us
    tmp_img = QA_DIR / f"{key}_try{try_n}_decoded.png"
    from PIL import Image

    im = Image.open(raw_path)
    im.convert("RGB").save(tmp_img)
    verdict, reason, qa_meta = qa_still(tmp_img)
    print(f"  QA raw {verdict}: {reason}", flush=True)

    if verdict == "KEEP":
        normalize_to_png(tmp_img, final_path)
        v2, r2, m2 = qa_still(final_path)
        qa_meta.update(m2)
        verdict, reason = v2, r2 + " (normalized)"
    else:
        # Archive reject
        REJECT_DIR.mkdir(parents=True, exist_ok=True)
        rej = REJECT_DIR / f"{key}_try{try_n}_{int(time.time())}.png"
        normalize_to_png(tmp_img, rej)
        print(f"  archived reject → {rej}", flush=True)

    credits_after, _ = read_credits(page)
    used = None
    if credits_before is not None and credits_after is not None:
        used = max(0, credits_before - credits_after)

    entry = {
        "key": key,
        "try": try_n,
        "out": str(final_path) if verdict == "KEEP" else None,
        "raw": str(tmp_img),
        "bytes": final_path.stat().st_size if final_path.exists() and verdict == "KEEP" else None,
        "account": active,
        "credits_before": credits_before,
        "credits_after": credits_after,
        "credits_used": used,
        "credits_session_start": credits_session_start,
        "attached_refs": attached,
        "qa": verdict,
        "qa_reason": reason,
        "qa_meta": qa_meta,
        "pill": pill_text(page),
        "url": page.url,
        "pulled": datetime.now(timezone.utc).isoformat(),
    }
    (QA_DIR / f"{key}_try{try_n}.meta.json").write_text(json.dumps(entry, indent=2) + "\n")
    print(f"  RESULT {verdict} {reason}", flush=True)
    return entry


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=sorted(STILLS.keys()), action="append")
    ap.add_argument("--max-tries", type=int, default=2)
    args = ap.parse_args()
    keys = args.only or ["s01", "s02", "s03"]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    QA_DIR.mkdir(parents=True, exist_ok=True)
    REJECT_DIR.mkdir(parents=True, exist_ok=True)

    from playwright.sync_api import sync_playwright

    log: dict = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "cdp": CDP,
        "account_required": REQUIRED,
        "engine": "Flow Image / Nano Banana 2 / 9:16 / x1",
        "style_refs": [str(p) for p in STYLE_REFS],
        "optional_style": str(OPTIONAL_STYLE),
        "stills": {},
        "credits_before_batch": None,
        "credits_after_batch": None,
        "page_tabs_rule": "NEW tab only; never close other Flow tabs; never touch :9460",
    }

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        page = ctx.new_page()
        our_page = page
        try:
            page.goto(PINNED, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2800)
            flow.dismiss_banners(page)
            if "/project/" not in (page.url or ""):
                page.goto("https://flow.google.com/", wait_until="domcontentloaded", timeout=120_000)
                page.wait_for_timeout(2000)
                flow.dismiss_banners(page)
                for label in (r"New project", r"Create with Flow", r"^New$"):
                    try:
                        btn = page.get_by_role("button", name=re.compile(label, re.I))
                        if btn.count():
                            btn.first.click(timeout=3000)
                            page.wait_for_timeout(2500)
                            break
                    except Exception:
                        continue
            flow.dismiss_banners(page)
            credits0, active = read_credits(page)
            log["credits_before_batch"] = credits0
            log["account"] = active
            print(f"GATE account={active} credits_before={credits0} url={page.url}", flush=True)
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
                            path=str(QA_DIR / f"{key}_try{try_n}_error.png"),
                            full_page=False,
                        )
                log["stills"][key] = {
                    "kept": kept,
                    "attempts": attempts,
                    "status": "KEEP" if kept else "FAIL",
                }

            credits1, _ = read_credits(page)
            log["credits_after_batch"] = credits1
            if credits0 is not None and credits1 is not None:
                log["credits_used_batch"] = max(0, credits0 - credits1)
            log["finished_at"] = datetime.now(timezone.utc).isoformat()
            LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
            LOG_PATH.write_text(json.dumps(log, indent=2) + "\n")
            print(f"\nLOG → {LOG_PATH}", flush=True)
            print(json.dumps({k: v["status"] for k, v in log["stills"].items()}, indent=2))
            fails = [k for k, v in log["stills"].items() if v["status"] != "KEEP"]
            return 1 if fails else 0
        finally:
            try:
                our_page.close()
            except Exception:
                pass


if __name__ == "__main__":
    raise SystemExit(main())
