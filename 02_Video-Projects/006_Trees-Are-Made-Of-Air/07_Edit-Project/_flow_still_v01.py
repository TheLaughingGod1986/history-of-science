#!/usr/bin/env python3
"""HOS 006: one Flow Image (Nano Banana 2) 16:9 start still per plate, on CDP :9222.

Chief style call J0140 (desk #180 6134444292, option 1): Flow text-to-video came
out near-photoreal, so each plate gets an Animistry 3D cartoon start still made in
Flow Image first (0 credits on Ultra), then Veo 3.1 image-to-video from it.
Parts 03-04 Vertex stills ride along as style ingredients.

Reuses the HOS 004 Flow Image helpers (`_mint_covers_live_v02_stills_cdp.py`):
image-mode pill, ingredient attach, Start generation, gallery srcs. Only the
ratio (16:9, not 9:16) and the landscape grab differ.

The caller checks credits before and after: a still that costs anything stops
the batch (the Chief's pass priced stills at 0).
"""
from __future__ import annotations

import hashlib
import importlib.util
import io
import re
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
V02 = REPO / "02_Video-Projects/004_Whats-Really-Inside-An-Atom/10_Shorts/_mint_covers_live_v02_stills_cdp.py"
_spec = importlib.util.spec_from_file_location("hos004_flow_stills", V02)
v02 = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(v02)

MEDIA_CLIPS = Path.home() / "YouTube/hos-006-trees/02_Video-Projects/006_Trees-Are-Made-Of-Air/04_Generated-Clips"
STYLE_REFS = [
    MEDIA_CLIPS / "part04/refs/v01_vertex_stills/04_sunny_window_v01.jpg",
    MEDIA_CLIPS / "part03/refs/v01_vertex_stills/10_mint_jar_v01.jpg",
]

STYLE_LOCK = (
    "STYLE LOCK from the attached stills: the same premium Animistry-class 3D cartoon "
    "look, rounded stylised shapes, soft finished materials, warm sunlit cinematic light. "
    "Use them for look only; do not copy their objects or layout."
)
HARD_REJECT = (
    "HARD REJECT: photoreal photo, live-action, flat 2D, letterbox bars, watermark, text, "
    "captions, signs, UI, logos, Orbit orange robot, DNA helix."
)


def still_prompt(look: str, core: str) -> str:
    return (f"{STYLE_LOCK}\nLANDSCAPE 16:9 wide single still frame, the opening frame of a shot.\n"
            f"{look}\n{core}\n{HARD_REJECT}")


def _pill_is_image_wide(pill: str) -> bool:
    if not pill or not re.search(r"Nano Banana|Banana|\bImage\b", pill, re.I):
        return False
    return bool(re.search(r"16:9|crop_16_9|16\s*[:×x]\s*9|crop_landscape", pill, re.I))


def select_image_16x9(page) -> str:
    pill0 = v02.pill_text(page)
    print(f"  pill before={pill0!r}", flush=True)
    if _pill_is_image_wide(pill0):
        return pill0
    import orbit_flow_veo_ui as flow
    flow._open_prompt_settings_pill(page)
    page.wait_for_timeout(900)
    page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button[role=radio],button[role=tab],[role=radio]')) {
            const t = ((b.innerText||'')+' '+(b.getAttribute('aria-label')||'')).trim();
            if ((/\\bimage\\b/i.test(t) || /banana/i.test(t)) && !/video|veo|omni/i.test(t)) {
              const r = b.getBoundingClientRect();
              if (r.width > 20 && r.height > 16) { b.click(); return t; }
            }
          }
          return null;
        }""")
    page.wait_for_timeout(600)
    clicked = page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button,[role=radio],[role=option]')) {
            const t = ((b.innerText||'')+' '+(b.getAttribute('aria-label')||'')).trim();
            if (/crop_16_9|\\b16:9\\b|crop_landscape/.test(t)) { b.click(); return t.slice(0,60); }
          }
          return null;
        }""")
    print(f"  ratio click={clicked!r}", flush=True)
    page.evaluate(
        """() => { for (const b of document.querySelectorAll('button'))
                     if ((b.innerText||'').trim() === 'x1') { b.click(); return true; } return false; }""")
    page.keyboard.press("Escape")
    page.wait_for_timeout(400)
    pill = v02.pill_text(page)
    print(f"  image-mode pill={pill!r}", flush=True)
    if not _pill_is_image_wide(pill):
        raise RuntimeError(f"Flow Image 16:9 not selected: {pill!r}")
    return pill


def canonical_src(src: str) -> str:
    """Flow may resize old gallery URLs; a new size is not a new image."""
    return re.sub(r"=s\d+[^?]*", "=s0", src)


def assert_unique_still(dest: Path, refs_root: Path) -> str:
    """Refuse another plate's saved still before any paid i2v submission."""
    digest = hashlib.sha256(dest.read_bytes()).hexdigest()
    plate = re.sub(r"_t\d+$", "", dest.stem.removesuffix(".candidate"))
    for other in refs_root.rglob("*.png"):
        if other.resolve() == dest.resolve() or other.stem.endswith(".armed"):
            continue
        if other.parent == dest.parent and re.sub(r"_t\d+$", "", other.stem) == plate:
            continue
        if hashlib.sha256(other.read_bytes()).hexdigest() == digest:
            raise RuntimeError(f"stale still matches another plate: {other}")
    return digest


def _fetch_new_landscape(page, dest: Path, before: set[str]) -> bool:
    from PIL import Image

    urls = page.evaluate(
        """(beforeList) => {
          const before = new Set(beforeList || []);
          return [...document.querySelectorAll('img')].map(i => {
            const r = i.getBoundingClientRect(); const src = i.currentSrc || i.src || '';
            return {src, area: r.width*r.height, wide: r.width > r.height*1.3, w: r.width};
          }).filter(i => i.src && !before.has(i.src) && i.wide && i.w > 120)
            .sort((a,b) => b.area - a.area).map(i => i.src);
        }""", list(before)) or []
    old_sources = {canonical_src(src) for src in before}
    for url in urls[:6]:
        if canonical_src(url) in old_sources:
            continue
        try:
            resp = page.request.get(re.sub(r"=s\d+", "=s0", url), timeout=60_000)
            if not resp.ok or len(resp.body()) < 40_000:
                continue
            im = Image.open(io.BytesIO(resp.body())).convert("RGB")
            w, h = im.size
            if w < 1000 or abs(w / h - 16 / 9) > 0.08:
                print(f"  skip {w}x{h}", flush=True)
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            candidate = dest.with_suffix(".candidate.png")
            im.save(candidate, format="PNG")
            try:
                assert_unique_still(candidate, MEDIA_CLIPS)
            except RuntimeError:
                candidate.unlink()
                raise
            candidate.replace(dest)
            print(f"  still ok {w}x{h} -> {dest.name}", flush=True)
            return True
        except Exception as e:
            print(f"  fetch warn: {e}", flush=True)
    return False


def all_img_srcs(page) -> set[str]:
    """Every img src on the page: v02.gallery_media_srcs skips tiles above y=80, the top row in a small viewport."""
    return set(page.evaluate("() => [...document.querySelectorAll('img')].map(i => i.currentSrc || i.src || '').filter(s => s.length >= 20)") or [])


def safe_close_overlays(page) -> None:
    """Close menus/modals with Escape and exit gallery image-edit mode without clicking gallery tiles."""
    for _ in range(3):
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        page.wait_for_timeout(120)
    try:
        done = page.locator('button[aria-label="Finished editing"]')
        if done.count() and done.first.is_visible():
            done.first.click(timeout=2000)
            page.wait_for_timeout(400)
    except Exception:
        pass


def prompt_pill_text(page) -> str:
    """Read the prompt-bar Settings trigger pill, ignoring the left sidebar 'image Images' tab."""
    return page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button')) {
            const aria = (b.getAttribute('aria-label') || '').trim();
            const t = (b.innerText || '').trim().replace(/\\n+/g, ' ');
            const r = b.getBoundingClientRect();
            if (r.width <= 40 || r.height <= 16) continue;
            if (/Settings trigger/i.test(aria)) return t.slice(0, 160);
            if (r.y > 400 && /Nano Banana|Video ·|Omni Flash|Omni 1|Veo 3|crop_/i.test(t)) return t.slice(0, 160);
          }
          return '';
        }"""
    ) or ""


def safe_open_ingredients_panel(page) -> None:
    """Open the Add-ingredients menu without toggling it closed if already open."""
    loc = page.locator('button[aria-label*="Add ingredients" i]')
    if loc.count():
        txt = (loc.first.inner_text() or "").strip().lower()
        if "close" in txt:
            return
        loc.first.click(force=True, timeout=5000)
        page.wait_for_timeout(800)
        return
    v02.open_ingredients_panel(page)


def prompt_chip_count(page) -> int:
    """Count only real attached prompt-bar ingredient chips (alt='Ingredient image' or y > 0.65*h),
    never the 40x40 asset rows inside the open Ingredients modal."""
    return int(page.evaluate(
        """() => [...document.querySelectorAll('img')].filter(i => {
          const r = i.getBoundingClientRect();
          if (r.width < 24 || r.height < 24 || r.width > 160 || r.height > 160) return false;
          return /ingredient image/i.test(i.alt || '') || r.y > (window.innerHeight || 900) * 0.65;
        }).length"""
    ) or 0)


v02.close_overlays = safe_close_overlays
v02.pill_text = prompt_pill_text
v02.open_ingredients_panel = safe_open_ingredients_panel
v02.ingredient_chip_count = prompt_chip_count


def attach_completed_style_ref(page, ref: Path, timeout_s: float = 120) -> bool:
    """Upload once if needed, then select the completed library asset-item (role=option) and Add to prompt."""
    safe_close_overlays(page)
    page.wait_for_timeout(400)
    before = prompt_chip_count(page)
    deadline = time.monotonic() + timeout_s
    uploaded = False
    while time.monotonic() < deadline:
        if prompt_chip_count(page) > before:
            safe_close_overlays(page)
            page.wait_for_timeout(400)
            return True
        safe_open_ingredients_panel(page)
        tile = page.locator(
            'button.asset-item, button[role="option"]',
            has_text=re.compile(re.escape(ref.name), re.I),
        )
        if tile.count() >= 1 and tile.first.is_visible():
            tile.first.click(timeout=3000)
            page.wait_for_timeout(500)
            if v02.click_add_to_prompt(page):
                page.wait_for_timeout(900)
                if prompt_chip_count(page) > before:
                    safe_close_overlays(page)
                    page.wait_for_timeout(400)
                    return True
        elif not uploaded:
            if v02.attach_style_ref_image_mode(page, ref) and prompt_chip_count(page) > before:
                safe_close_overlays(page)
                page.wait_for_timeout(400)
                return True
            uploaded = True
        page.wait_for_timeout(2000)
    safe_close_overlays(page)
    page.wait_for_timeout(400)
    return False


def make_still(page, prompt: str, dest: Path, timeout_s: float = 300) -> Path:
    """Arm Flow Image 16:9 with the style refs and prompt, Create once, save the new still."""
    import orbit_flow_veo_ui as flow

    if "/project/" not in (page.url or ""):
        flow.ensure_project(page)
        page.wait_for_timeout(2000)
        flow.dismiss_banners(page)
    v02.close_overlays(page)
    for _ in range(10):
        if v02.pill_text(page):
            break
        page.wait_for_timeout(500)
    select_image_16x9(page)
    v02.clear_prompt_attachments(page)
    attached = sum(1 for ref in STYLE_REFS if ref.exists() and attach_completed_style_ref(page, ref))
    chips = v02.ingredient_chip_count(page)
    print(f"  style refs attached={attached} chips={chips}", flush=True)
    if attached != len(STYLE_REFS) or chips < len(STYLE_REFS):
        raise RuntimeError("style refs not attached; refusing Create before upload/selection completes")
    make_still.refs_attached = chips
    box = flow.editor_box(page)
    if not box:
        raise RuntimeError("prompt editor missing")
    page.mouse.click(box["x"] + min(box["w"] - 40, 200), box["y"] + max(8, box["h"] / 2))
    page.keyboard.press("End")
    page.keyboard.insert_text(prompt)
    page.wait_for_timeout(400)
    if len(flow._editor_prompt_text(page) or "") < 80:
        raise RuntimeError("still prompt not armed")
    before = all_img_srcs(page)
    dest.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(dest.with_suffix(".armed.png")))
    v02.submit_create(page)
    page.wait_for_timeout(900)
    flow.confirm_generation_spend(page, timeout_s=12.0)
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        page.wait_for_timeout(4000)
        new = all_img_srcs(page) - before
        print(f"  still poll new={len(new)} elapsed={int(time.time() - t0)}s", flush=True)
        if new and time.time() - t0 > 15 and _fetch_new_landscape(page, dest, before):
            return dest
    raise RuntimeError(f"timed out waiting for a new 16:9 still -> {dest}")
