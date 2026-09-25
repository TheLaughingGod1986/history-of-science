#!/usr/bin/env python3
"""Part 04 v15 HARD Ben-FAIL remint — crown · CLEAN LIGHT · sharp late desks.

Parent FAIL: hos_002_part04_rough_v14.mp4
  sha256 fa62ab22d0f7cbd4f208e5200c9b8b471c23595237b4d7d2dd18e6f47dabad4f

Remint plates:
  06_explorer_leaves_gap
  09b_risk_hold
  10_family_before_weight
  11_publish_gaps
  11b_wait_and_hunt

No PASS. Scores → CoS. No Ben ping.
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter

PROJ = Path(__file__).resolve().parents[1]
RAW_OUT = PROJ / "04_Generated-Clips/part04/raw/v15_fast"
QA = PROJ / "07_Edit-Project/_qa_part04_v15_hard"
STARTS = PROJ / "04_Generated-Clips/part04/refs/v15_start_frames"
SHEET = STARTS / "character_sheet.jpg"
if not SHEET.exists():
    SHEET = PROJ / "04_Generated-Clips/part04/refs/v11_dna/character_sheet.jpg"
OK_GLOW = PROJ / "07_Edit-Project/_qa_part04_v14_refs/ok_glow_102.jpg"

SOURCES = {
    "06_explorer_leaves_gap": PROJ
    / "04_Generated-Clips/part04/raw/v11_fast/06_explorer_leaves_gap_v11.mp4",
    "09b_risk_hold": PROJ / "04_Generated-Clips/part04/raw/v14_fast/09b_risk_hold_v14.mp4",
    "10_family_before_weight": PROJ
    / "04_Generated-Clips/part04/raw/v12_fast/10_family_before_weight_v12.mp4",
    "11_publish_gaps": PROJ / "04_Generated-Clips/part04/raw/v01_fast/11_publish_gaps_v01.mp4",
    "11b_wait_and_hunt": PROJ
    / "04_Generated-Clips/part04/raw/v01_fast/11b_wait_and_hunt_v01.mp4",
}

PARENT_SHA = "fa62ab22d0f7cbd4f208e5200c9b8b471c23595237b4d7d2dd18e6f47dabad4f"
W, H = 1920, 1080


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def is_lava(r: int, g: int, b: int) -> bool:
    if r < 165:
        return False
    if r >= 190 and g >= 70 and b <= 110 and (r - b) >= 90 and (r - g) <= 125:
        return True
    if r >= 205 and g >= 115 and b <= 120 and (r - b) >= 85:
        return True
    if r >= 230 and g >= 150 and b <= 145 and (r - b) >= 75 and g < 235:
        return True
    if r >= 195 and 85 <= g <= 185 and b <= 95 and (r - b) >= 110:
        return True
    # hot orange rim / molten pool
    if r > 200 and g > 130 and b < 140 and (r - b) > 75 and (r + g) > 360:
        return True
    return False


def lava_mask(im: Image.Image) -> Image.Image:
    rgb = im.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    m = Image.new("L", (w, h), 0)
    mp = m.load()
    for y in range(int(h * 0.04), int(h * 0.80)):
        for x in range(0, int(w * 0.75)):
            r, g, b = px[x, y]
            in_bulb = (
                y < int(h * 0.30)
                and x < int(w * 0.24)
                and r > 245
                and g > 235
                and b > 200
            )
            if (not in_bulb) and is_lava(r, g, b):
                mp[x, y] = 255
    m = m.filter(ImageFilter.MaxFilter(7))
    return m.filter(ImageFilter.GaussianBlur(4))


def wood_fill(im: Image.Image) -> Image.Image:
    rgb = im.convert("RGB")
    w, h = rgb.size
    patches = [
        rgb.crop((int(w * 0.45), int(h * 0.55), int(w * 0.68), int(h * 0.82))),
        rgb.crop((int(w * 0.55), int(h * 0.35), int(w * 0.75), int(h * 0.55))),
        rgb.crop((int(w * 0.30), int(h * 0.62), int(w * 0.50), int(h * 0.85))),
    ]
    base = patches[0].resize((w, h), Image.Resampling.BILINEAR)
    for p in patches[1:]:
        base = Image.blend(base, p.resize((w, h), Image.Resampling.BILINEAR), 0.35)
    px = base.load()
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            r, g, b = px[x, y]
            cool = (
                min(255, int(r * 0.72 + 32)),
                min(255, int(g * 0.78 + 26)),
                min(255, int(b * 0.88 + 22)),
            )
            px[x, y] = cool
            if x + 1 < w:
                px[x + 1, y] = cool
            if y + 1 < h:
                px[x, y + 1] = cool
                if x + 1 < w:
                    px[x + 1, y + 1] = cool
    return base.filter(ImageFilter.GaussianBlur(6))


def scrub_lava(im: Image.Image, strength: float = 0.95) -> Image.Image:
    rgb = im.convert("RGB")
    fill = wood_fill(rgb)
    mask = lava_mask(rgb)
    if strength < 1.0:
        mask = mask.point(lambda a: int(a * strength))
    out = Image.composite(fill, rgb, mask)
    mask2 = lava_mask(out)
    fill2 = wood_fill(out)
    return Image.composite(fill2, out, mask2.point(lambda a: int(a * 0.90)))


def soft_empty_chairs_panel(im: Image.Image) -> Image.Image:
    muted = scrub_lava(im.convert("RGB"), strength=0.85).convert("RGBA")
    w, h = muted.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    x0, y0 = int(w * 0.415), int(h * 0.255)
    x1, y1 = int(w * 0.585), int(h * 0.470)
    for pad, col in (
        (22, (255, 240, 215, 24)),
        (12, (255, 244, 222, 42)),
        (4, (255, 246, 228, 62)),
    ):
        d.rounded_rectangle(
            (x0 - pad, y0 - pad, x1 + pad, y1 + pad),
            radius=14 + pad // 4,
            fill=col,
        )
    d.rounded_rectangle(
        (x0, y0, x1, y1),
        radius=10,
        fill=(255, 248, 232, 70),
        outline=(255, 250, 235, 95),
        width=2,
    )
    overlay = overlay.filter(ImageFilter.GaussianBlur(2))
    return Image.alpha_composite(muted, overlay).convert("RGB")


def hard_lamp_region_clean(im: Image.Image) -> Image.Image:
    """Replace molten under-lamp pixels with soft cream light — no wood smear."""
    rgb = im.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    out = rgb.copy()
    op = out.load()
    # cream replacement color sampled from soft lit desk away from lava
    cream = (245, 228, 195)
    wood = (120, 82, 52)
    for y in range(int(h * 0.08), int(h * 0.70)):
        for x in range(0, int(w * 0.45)):
            r, g, b = px[x, y]
            # protect pure bulb core
            if y < int(h * 0.28) and x < int(w * 0.22) and r > 245 and g > 235 and b > 200:
                continue
            lava = is_lava(r, g, b)
            # also catch yellow-orange pools / drip shapes
            hot_pool = (
                r >= 200 and g >= 140 and b <= 150 and (r - b) >= 70 and (r + g) >= 360
            )
            if lava or hot_pool:
                # mix toward cream (light) not dark wood
                t = 0.82 if lava else 0.70
                op[x, y] = (
                    int((1 - t) * r + t * cream[0]),
                    int((1 - t) * g + t * cream[1]),
                    int((1 - t) * b + t * cream[2]),
                )
    # soften transitions
    out = Image.blend(rgb, out, 0.92)
    # second pass
    px2 = out.load()
    for y in range(int(h * 0.08), int(h * 0.68)):
        for x in range(0, int(w * 0.42)):
            r, g, b = px2[x, y]
            if is_lava(r, g, b) or (r > 210 and g > 150 and b < 140 and (r - b) > 80):
                if not (y < int(h * 0.28) and x < int(w * 0.22) and r > 245 and g > 230):
                    px2[x, y] = (
                        int(0.25 * r + 0.75 * cream[0]),
                        int(0.28 * g + 0.72 * cream[1]),
                        int(0.35 * b + 0.65 * cream[2]),
                    )
    return out.filter(ImageFilter.GaussianBlur(0.4))


def hard_chair_rim_clean(im: Image.Image) -> Image.Image:
    """Kill fiery chair rim; soft Empty-Chairs rectangular panel only."""
    rgb = hard_lamp_region_clean(im.convert("RGB"))
    w, h = rgb.size
    px = rgb.load()
    # neutralize hot rim around chair back
    for y in range(int(h * 0.18), int(h * 0.55)):
        for x in range(int(w * 0.34), int(w * 0.68)):
            r, g, b = px[x, y]
            if is_lava(r, g, b) or (r > 190 and g > 130 and b < 130 and (r - b) > 70):
                # wood-neutral
                px[x, y] = (
                    int(0.35 * r + 0.65 * 110),
                    int(0.35 * g + 0.65 * 78),
                    int(0.40 * b + 0.60 * 52),
                )
    return soft_empty_chairs_panel(rgb)



def sample_hair_colors(sheet: Image.Image) -> list[tuple[int, int, int]]:
    sw, sh = sheet.size
    crop = sheet.crop((int(sw * 0.12), int(sh * 0.02), int(sw * 0.28), int(sh * 0.13)))
    crop = crop.resize((64, 48), Image.Resampling.BILINEAR)
    px = crop.load()
    colors: list[tuple[int, int, int]] = []
    for y in range(crop.size[1]):
        for x in range(crop.size[0]):
            r, g, b = px[x, y][:3]
            if r > 60 and r < 190 and g < 140 and (r - b) > 15 and r > g:
                colors.append((r, g, b))
    if not colors:
        colors = [(120, 72, 42), (96, 55, 32), (140, 88, 52), (78, 44, 28)]
    return colors


def fill_crown(im: Image.Image, sheet: Image.Image) -> Image.Image:
    """Paint finished messy-wavy chestnut crown — no dark unfinished hole."""
    rgb = im.convert("RGBA")
    w, h = rgb.size
    local = rgb.convert("RGB")
    lp = local.load()
    samples = []
    for y in range(int(h * 0.26), int(h * 0.36)):
        for x in list(range(int(w * 0.45), int(w * 0.485))) + list(range(int(w * 0.545), int(w * 0.58))):
            r, g, b = lp[x, y]
            # prefer mid chestnut, skip very dark unfinished / very bright specular
            if 70 < r < 175 and g < 130 and (r - b) > 12 and r > g + 5 and (r + g + b) > 180:
                samples.append((r, g, b))
    colors = samples + sample_hair_colors(sheet.convert("RGB"))
    # brighten palette slightly so crown never reads as bald dark hole
    colors = [
        (min(255, int(r * 1.08 + 12)), min(255, int(g * 1.05 + 8)), min(255, int(b * 1.02 + 4)))
        for r, g, b in colors
    ]
    rng = random.Random(11)
    cx, cy = int(w * 0.505), int(h * 0.298)
    rw, rh = int(w * 0.092), int(h * 0.075)

    # base soft fill (opaque enough to hide hole)
    base = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    bd = ImageDraw.Draw(base)
    for _ in range(280):
        ang = rng.uniform(0, 2 * math.pi)
        rad = rng.uniform(0, 1) ** 0.45
        x = cx + int(math.cos(ang) * rw * rad)
        y = cy + int(math.sin(ang) * rh * rad * 0.88)
        col = colors[rng.randrange(len(colors))]
        r0 = rng.randint(4, 9)
        bd.ellipse((x - r0, y - r0, x + r0, y + r0), fill=(*col, 230))
    bmask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(bmask).ellipse((cx - rw, cy - rh, cx + rw, cy + int(rh * 0.95)), fill=255)
    bmask = bmask.filter(ImageFilter.GaussianBlur(6))
    base.putalpha(Image.composite(base.split()[-1], Image.new("L", (w, h), 0), bmask))
    out = Image.alpha_composite(rgb, base)

    # wavy tufts on top for finished messy crown
    hair = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(hair)
    for _ in range(160):
        col = colors[rng.randrange(len(colors))]
        x0 = cx + rng.randint(-rw + 4, rw - 4)
        y0 = cy + rng.randint(-rh + 2, int(rh * 0.35))
        x1 = x0 + rng.randint(-14, 14)
        y1 = y0 + rng.randint(-18, 3)
        d.line((x0, y0, x1, y1), fill=(*col, rng.randint(190, 245)), width=rng.randint(3, 6))
    for _ in range(220):
        ang = rng.uniform(-2.8, -0.4)
        rad = rng.uniform(0.2, 1.0) ** 0.55
        x = cx + int(math.cos(ang) * rw * rad)
        y = cy + int(math.sin(ang) * rh * rad * 0.9)
        col = colors[rng.randrange(len(colors))]
        r0 = rng.randint(2, 5)
        d.ellipse((x - r0, y - r0, x + r0, y + r0), fill=(*col, rng.randint(180, 240)))
    hair.putalpha(Image.composite(hair.split()[-1], Image.new("L", (w, h), 0), bmask))
    return Image.alpha_composite(out, hair).convert("RGB")



def deghost_sharpen(im: Image.Image) -> Image.Image:
    rgb = im.convert("RGB")
    w, h = rgb.size
    # temporal-ish: blur doubles then unsharp
    right = rgb.crop((int(w * 0.48), 0, w, h))
    soft = right.filter(ImageFilter.GaussianBlur(1.6))
    right = Image.blend(right, soft, 0.45)
    right = ImageEnhance.Sharpness(right).enhance(2.0)
    right = ImageEnhance.Contrast(right).enhance(1.12)
    out = rgb.copy()
    out.paste(right, (int(w * 0.48), 0))
    seam = Image.new("L", (w, h), 0)
    ImageDraw.Draw(seam).rectangle([int(w * 0.48), 0, w, h], fill=255)
    seam = seam.filter(ImageFilter.GaussianBlur(14))
    out = Image.composite(out, rgb, seam)
    # mild whole-frame unsharp
    blur = out.filter(ImageFilter.GaussianBlur(1.0))
    out = Image.blend(out, ImageChops.difference(out, blur).point(lambda v: min(255, v + 128)), 0.0)
    return ImageEnhance.Sharpness(out).enhance(1.35)


def upper_lock_mask(w: int, h: int) -> Image.Image:
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    d.rectangle([0, 0, int(w * 0.34), int(h * 0.70)], fill=255)
    d.rectangle([0, 0, w, int(h * 0.52)], fill=255)
    y0 = int(h * 0.52)
    band = int(h * 0.18)
    for i in range(band):
        a = int(255 * (1.0 - i / max(1, band - 1)))
        cur = mask.getpixel((w // 2, min(h - 1, y0 + i)))
        d.rectangle([0, y0 + i, w, y0 + i + 1], fill=max(cur, a))
    return mask.filter(ImageFilter.GaussianBlur(20))


def build_clean_still(pid: str, src_frame: Image.Image) -> Image.Image:
    im = src_frame.convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    if pid == "09b_risk_hold":
        if OK_GLOW.exists():
            dna = Image.open(OK_GLOW).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
            dna = hard_chair_rim_clean(hard_lamp_region_clean(dna))
            motion = hard_chair_rim_clean(hard_lamp_region_clean(im))
            im = Image.composite(dna, motion, upper_lock_mask(W, H))
        else:
            im = hard_chair_rim_clean(hard_lamp_region_clean(im))
        return ImageEnhance.Sharpness(im).enhance(1.15)
    if pid == "06_explorer_leaves_gap":
        im = hard_lamp_region_clean(im)
        im = fill_crown(im, Image.open(SHEET))
        return ImageEnhance.Sharpness(im).enhance(1.20)
    if pid == "10_family_before_weight":
        im = hard_chair_rim_clean(hard_lamp_region_clean(im))
        return deghost_sharpen(im)
    return deghost_sharpen(hard_lamp_region_clean(im))


def lava_pct(im: Image.Image) -> float:
    rgb = im.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    hot = n = 0
    for y in range(int(h * 0.05), int(h * 0.70), 2):
        for x in range(0, int(w * 0.55), 2):
            n += 1
            r, g, b = px[x, y]
            if is_lava(r, g, b):
                hot += 1
    return 100.0 * hot / max(n, 1)


def process_plate(pid: str) -> dict:
    src = SOURCES[pid]
    if not src.exists():
        raise SystemExit(f"missing source {src}")
    dest = RAW_OUT / f"{pid}_v15.mp4"
    RAW_OUT.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    rejected = RAW_OUT / "_rejected"
    rejected.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        shutil.move(
            str(dest),
            str(rejected / f"{pid}_v15_pre_hard_{dest.stat().st_mtime_ns}.mp4"),
        )

    with tempfile.TemporaryDirectory(prefix=f"hos_v15_hard_{pid}_") as td:
        tdir = Path(td)
        fin = tdir / "in"
        fout = tdir / "out"
        fin.mkdir()
        fout.mkdir()
        subprocess.check_call(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(src),
                "-vf", f"fps=24,scale={W}:{H}:flags=lanczos",
                str(fin / "f_%04d.jpg"),
            ]
        )
        frames = sorted(fin.glob("f_*.jpg"))
        if not frames:
            raise SystemExit(f"no frames from {src}")

        mid = Image.open(frames[len(frames) // 2]).convert("RGB")
        clean = build_clean_still(pid, mid)
        clean_path = QA / f"{pid}_clean_lock.jpg"
        clean.save(clean_path, quality=95)
        print(f"  clean_lock lava_pct={lava_pct(clean):.3f} → {clean_path.name}", flush=True)

        use_upper_lock = pid in {"09b_risk_hold", "10_family_before_weight"}
        mask = upper_lock_mask(W, H) if use_upper_lock else None
        sheet_im = Image.open(SHEET) if pid == "06_explorer_leaves_gap" else None

        for i, fp in enumerate(frames):
            motion = Image.open(fp).convert("RGB")
            if motion.size != (W, H):
                motion = motion.resize((W, H), Image.Resampling.LANCZOS)

            if mask is not None:
                if i % 5 == 0:
                    base = clean.point(lambda p: min(255, int(p * 1.003)))
                elif i % 5 == 2:
                    base = clean.point(lambda p: max(0, int(p * 0.998)))
                else:
                    base = clean
                frame = Image.composite(base, motion, mask)
            else:
                frame = motion

            frame = hard_lamp_region_clean(frame)
            if pid == "06_explorer_leaves_gap" and sheet_im is not None:
                frame = fill_crown(frame, sheet_im)
            if pid == "09b_risk_hold":
                frame = hard_chair_rim_clean(frame)
            if pid in {
                "10_family_before_weight",
                "11_publish_gaps",
                "11b_wait_and_hunt",
            }:
                frame = deghost_sharpen(frame)
            else:
                frame = ImageEnhance.Sharpness(frame).enhance(1.15)
            frame.save(fout / fp.name, quality=95)
            if i % 40 == 0:
                print(f"  {pid} frame {i}/{len(frames)} lava={lava_pct(frame):.3f}", flush=True)

        tmp = tdir / "out.mp4"
        subprocess.check_call(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-framerate", "24", "-i", str(fout / "f_%04d.jpg"),
                "-i", str(src),
                "-map", "0:v", "-map", "1:a?",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17",
                "-preset", "medium", "-c:a", "aac", "-b:a", "192k",
                "-shortest", str(tmp),
            ]
        )
        shutil.copy2(tmp, dest)

    qdir = QA / pid
    qdir.mkdir(parents=True, exist_ok=True)
    still_pcts = []
    for t in (0.5, 2.0, 4.0, 6.0, 7.5):
        sp = qdir / f"t{t:.1f}.jpg"
        subprocess.check_call(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-ss", str(t), "-i", str(dest), "-frames:v", "1", str(sp),
            ]
        )
        still_pcts.append(lava_pct(Image.open(sp)))

    info = {
        "plate": pid,
        "src": str(src),
        "out": str(dest),
        "sha256": sha256(dest),
        "bytes": dest.stat().st_size,
        "lava_pct_stills": still_pcts,
        "lava_pct_max": max(still_pcts) if still_pcts else None,
        "method": "hard_region_composite_v15",
    }
    (qdir / "meta.json").write_text(json.dumps(info, indent=2) + "\n")
    print(json.dumps(info), flush=True)
    return info


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", default=list(SOURCES.keys()))
    args = ap.parse_args()
    for pid, path in SOURCES.items():
        if not path.exists():
            raise SystemExit(f"missing source for {pid}: {path}")
    results = []
    for pid in args.only:
        if pid not in SOURCES:
            raise SystemExit(f"unknown plate {pid}")
        print(f"=== HARD remint {pid} ===", flush=True)
        results.append(process_plate(pid))
    summary = {
        "parent_v14_sha": PARENT_SHA,
        "results": results,
        "status": "HARD_REMINT_DONE — no PASS",
    }
    QA.mkdir(parents=True, exist_ok=True)
    (QA / "hard_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print("HARD REMINT OK", flush=True)


if __name__ == "__main__":
    main()
