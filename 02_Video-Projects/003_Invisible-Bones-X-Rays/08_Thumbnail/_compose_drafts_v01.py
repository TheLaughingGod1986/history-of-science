from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import hashlib

BASE = Path("/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/003_Invisible-Bones-X-Rays/08_Thumbnail")
FR = BASE / "_frames"
OUT = BASE / "Drafts"
OUT.mkdir(parents=True, exist_ok=True)

def load_font(size):
    for p in [
        "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
        "/System/Library/Fonts/Supplemental/Georgia.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]:
        try:
            return ImageFont.truetype(p, size, index=0)
        except Exception:
            continue
    return ImageFont.load_default()

def fit_cover(im, w, h):
    im = im.convert("RGB")
    scale = max(w / im.width, h / im.height)
    nw, nh = int(im.width * scale), int(im.height * scale)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - w) // 2
    top = (nh - h) // 2
    return im.crop((left, top, left + w, top + h))

def stamp(im, text, corner="tl"):
    font = load_font(64 if im.width >= 1200 else 44)
    draw = ImageDraw.Draw(im)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad = 16
    if corner == "tl":
        x, y = 40, 40
    else:
        x = im.width - tw - 40
        y = im.height - th - 40
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle([x - pad, y - pad, x + tw + pad, y + th + pad], fill=(0, 0, 0, 150))
    im = Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(im)
    draw.text((x + 2, y + 2), text, font=font, fill=(0, 0, 0))
    draw.text((x, y), text, font=font, fill=(245, 240, 230))
    return im

def save_jpg(im, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, "JPEG", quality=90, optimize=True)
    h = hashlib.sha256(path.read_bytes()).hexdigest()
    print(f"{path.name}\t{path.stat().st_size}\t{h}", flush=True)
    return h

print("compose start", flush=True)
long = stamp(fit_cover(Image.open(FR / "long_t35.jpg"), 1280, 720), "1895")
save_jpg(long, OUT / "hos_003_thumb_long_bertha_ring_v01.jpg")

s3 = stamp(fit_cover(Image.open(FR / "long_t35.jpg"), 1280, 720), "RING")
save_jpg(s3, OUT / "hos_003_thumb_s3_bertha_ring_v01.jpg")

s1 = stamp(fit_cover(Image.open(FR / "s1_glow.jpg"), 1280, 720), "GLOW?")
save_jpg(s1, OUT / "hos_003_thumb_s1_cardboard_glow_v01.jpg")

s2src = FR / "s2_skeleton.jpg"
s2 = stamp(fit_cover(Image.open(s2src), 1280, 720), "NO KNIFE")
save_jpg(s2, OUT / "hos_003_thumb_s2_bones_no_knife_v01.jpg")

for name, src, mark in [
    ("hos_003_s1_cover_v01.jpg", FR / "s1_glow.jpg", "GLOW?"),
    ("hos_003_s2_cover_v01.jpg", FR / "s2_skeleton.jpg", "NO KNIFE"),
    ("hos_003_s3_cover_v01.jpg", FR / "long_t35.jpg", "RING"),
]:
    save_jpg(stamp(fit_cover(Image.open(src), 1080, 1920), mark), OUT / name)

print("DONE", flush=True)
