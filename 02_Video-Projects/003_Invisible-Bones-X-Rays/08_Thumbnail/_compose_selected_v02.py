#!/usr/bin/env python3
"""HOS 003 Selected thumbs v02 — house lock remint. More text variants, TV-friendly."""
from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import hashlib, json, shutil

BASE = Path("/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/003_Invisible-Bones-X-Rays/08_Thumbnail")
FR = BASE / "_frames"
DRAFT = BASE / "Drafts_v02"
SEL = BASE / "Selected"
PILLS = SEL / "pills"
DRAFT.mkdir(parents=True, exist_ok=True)
PILLS.mkdir(parents=True, exist_ok=True)

def load_font(size: int):
    for p, idx in [
        ("/System/Library/Fonts/Supplemental/Didot.ttc", 0),
        ("/System/Library/Fonts/Supplemental/Times New Roman.ttf", 0),
        ("/System/Library/Fonts/Supplemental/Georgia.ttf", 0),
    ]:
        try:
            return ImageFont.truetype(p, size, index=idx)
        except Exception:
            continue
    return ImageFont.load_default()

def fit_cover(im: Image.Image, w: int, h: int) -> Image.Image:
    im = im.convert("RGB")
    scale = max(w / im.width, h / im.height)
    nw, nh = int(im.width * scale), int(im.height * scale)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - w) // 2
    top = max(0, (nh - h) // 2 - int(h * 0.02))  # slight upward bias = centre-safe
    return im.crop((left, top, left + w, top + h))

def darken_edges(im: Image.Image, strength=0.35) -> Image.Image:
    """Soft vignette so text + hero pop (TV)."""
    im = im.convert("RGB")
    w, h = im.size
    vignette = Image.new("L", (w, h), 0)
    vd = ImageDraw.Draw(vignette)
    # radial-ish via ellipse
    margin = int(min(w, h) * 0.08)
    vd.ellipse([margin, margin, w - margin, h - margin], fill=255)
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=min(w, h) // 8))
    base = ImageEnhance.Brightness(im).enhance(0.92)
    black = Image.new("RGB", (w, h), (8, 6, 10))
    # blend using vignette as mask: bright centre keeps base
    return Image.composite(base, Image.blend(base, black, strength), vignette)

def stamp(im: Image.Image, text: str, place: str = "tl") -> Image.Image:
    """Large TV-readable Didot stamp. place: tl|tr|bl|br|topc"""
    # size scales with width
    size = 78 if im.width >= 1200 else (70 if im.width >= 1000 else 56)
    if len(text) > 10:
        size = int(size * 0.82)
    font = load_font(size)
    draw = ImageDraw.Draw(im)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_x, pad_y = 22, 14
    margin = 48 if im.height > 1000 else 36
    if place == "tl":
        x, y = margin, margin
    elif place == "tr":
        x, y = im.width - tw - margin - pad_x * 2, margin
    elif place == "bl":
        x, y = margin, im.height - th - margin - pad_y * 2
    elif place == "br":
        x, y = im.width - tw - margin - pad_x * 2, im.height - th - margin - pad_y * 2
    else:  # topc
        x, y = (im.width - tw) // 2 - pad_x, margin
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rounded_rectangle(
        [x - 4, y - 4, x + tw + pad_x * 2 + 4, y + th + pad_y * 2 + 4],
        radius=10,
        fill=(0, 0, 0, 165),
    )
    out = Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(out)
    tx, ty = x + pad_x, y + pad_y - 2
    draw.text((tx + 2, ty + 2), text, font=font, fill=(0, 0, 0))
    draw.text((tx, ty), text, font=font, fill=(250, 245, 232))
    return out

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save_jpg(im: Image.Image, path: Path) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, "JPEG", quality=92, optimize=True)
    h = sha(path)
    print(f"JPG\t{path.name}\t{path.stat().st_size}\t{h}", flush=True)
    return h

def make_pill(title: str, out: Path, width=1080) -> str:
    """Didot title pill for Shorts packaging."""
    height = 220
    im = Image.new("RGB", (width, height), (18, 14, 22))
    font = load_font(42 if len(title) < 40 else 34)
    draw = ImageDraw.Draw(im)
    bbox = draw.textbbox((0, 0), title, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (width - tw) // 2
    y = (height - th) // 2 - 4
    # cream rule lines
    draw.rectangle([80, 40, width - 80, 42], fill=(200, 175, 120))
    draw.rectangle([80, height - 42, width - 80, height - 40], fill=(200, 175, 120))
    draw.text((x + 1, y + 1), title, font=font, fill=(0, 0, 0))
    draw.text((x, y), title, font=font, fill=(245, 238, 220))
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, "PNG", optimize=True)
    h = sha(out)
    print(f"PILL\t{out.name}\t{out.stat().st_size}\t{h}", flush=True)
    return h

# Frame picks (hero obvious, less clutter)
FRAMES = {
    "long": FR / "long_t35.jpg",           # Bertha ring plate
    "s1": FR / "s1_glow.jpg",              # cardboard/glow apparatus
    "s2": FR / "s2_skeleton.jpg",          # bones via ray
    "s3": FR / "long_t35.jpg",             # ring denser on plate
}

# Text variants — pick one Selected each
VARIANTS = {
    "long": [("1895", "tl"), ("X-RAYS", "tl"), ("FIRST PROOF", "tl")],
    "s1": [("GLOW?", "tl"), ("DARK?", "tl"), ("X", "tr")],
    "s2": [("NO KNIFE", "tl"), ("BONES", "tl"), ("SEE INSIDE", "tl")],
    "s3": [("RING", "tl"), ("BERTHA", "tl"), ("FIRST X-RAY", "bl")],
}

# Chosen for Selected (TV + emotion + match board)
PICK = {
    "long": ("1895", "tl"),
    "s1": ("GLOW?", "tl"),
    "s2": ("NO KNIFE", "tl"),
    "s3": ("RING", "tl"),
}

manifest = {"version": "v02", "picks": {}, "variants": {}, "covers": {}, "pills": {}}

print("compose v02 start", flush=True)
for key, src in FRAMES.items():
    base_im = darken_edges(fit_cover(Image.open(src), 1280, 720))
    for text, place in VARIANTS[key]:
        stamped = stamp(base_im.copy(), text, place)
        name = f"hos_003_thumb_{key}_{text.replace(' ', '_').replace('?', '').lower()}_v02.jpg"
        # normalize names for known assets
        h = save_jpg(stamped, DRAFT / name)
        manifest["variants"].setdefault(key, []).append({"file": name, "text": text, "sha256": h})

# Selected canonical filenames
selected_map = {
    "long": ("hos_003_thumb_long_bertha_ring_v02.jpg", FRAMES["long"], *PICK["long"]),
    "s1": ("hos_003_thumb_s1_cardboard_glow_v02.jpg", FRAMES["s1"], *PICK["s1"]),
    "s2": ("hos_003_thumb_s2_bones_no_knife_v02.jpg", FRAMES["s2"], *PICK["s2"]),
    "s3": ("hos_003_thumb_s3_bertha_ring_v02.jpg", FRAMES["s3"], *PICK["s3"]),
}
for key, (fname, src, text, place) in selected_map.items():
    im = stamp(darken_edges(fit_cover(Image.open(src), 1280, 720)), text, place)
    h = save_jpg(im, SEL / fname)
    manifest["picks"][key] = {"file": fname, "text": text, "sha256": h, "rationale": f"TV-large {text}; hero frame; board match"}

# 9:16 covers centre-safe
covers = [
    ("hos_003_s1_cover_v02.jpg", FRAMES["s1"], *PICK["s1"]),
    ("hos_003_s2_cover_v02.jpg", FRAMES["s2"], *PICK["s2"]),
    ("hos_003_s3_cover_v02.jpg", FRAMES["s3"], *PICK["s3"]),
]
for fname, src, text, place in covers:
    # for vertical: keep hero in centre — fit_cover already centre; stamp top
    place_v = "topc" if place != "bl" else "bl"
    im = stamp(darken_edges(fit_cover(Image.open(src), 1080, 1920)), text, place_v)
    h = save_jpg(im, SEL / fname)
    manifest["covers"][fname] = {"text": text, "sha256": h}

# Pills — exact KEEP Short titles
pills = [
    ("hos_003_s1_pill_v02.png", "Why Did This Cardboard Glow in the Dark?"),
    ("hos_003_s2_pill_v02.png", "How Can You See Bones Without a Knife?"),
    ("hos_003_s3_pill_v02.png", "Why Is There a Ring on the First X-ray?"),
    ("hos_003_long_pill_v02.png", "How Did We Discover X-rays?"),
]
for fname, title in pills:
    h = make_pill(title, PILLS / fname)
    manifest["pills"][fname] = {"title": title, "sha256": h}

md = SEL / "SELECTED_v02_MANIFEST.md"
lines = [
    "# HOS 003 Thumbnail Selected v02",
    "",
    "**Date:** 23 Sep 2026 Europe/London",
    "**House:** HOS_HOUSE_THUMBNAIL_LOCK — TV-friendly, question/emotion, clear hero, less clutter, more text variants.",
    "**v01:** archived in `_archive_v01_2026-09-22/`",
    "",
    "## Selected picks",
    "",
]
for key, info in manifest["picks"].items():
    lines.append(f"- **{key}** `{info['file']}` text `{info['text']}` sha `{info['sha256']}`")
lines += ["", "## Covers 9:16", ""]
for fname, info in manifest["covers"].items():
    lines.append(f"- `{fname}` text `{info['text']}` sha `{info['sha256']}`")
lines += ["", "## Pills", ""]
for fname, info in manifest["pills"].items():
    lines.append(f"- `{fname}` — {info['title']} — sha `{info['sha256']}`")
lines += ["", "## Draft variants", "See `Drafts_v02/` for alternate marks.", ""]
md.write_text("\n".join(lines) + "\n")
(SEL / "SELECTED_v02_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
print("DONE thumbs", flush=True)
