#!/usr/bin/env python3
"""HOS 002 Part 04 v15 HARD remint — crown DNA + CLEAN LIGHT + sharp late desks."""
from __future__ import annotations

import hashlib
import json
import math
import random
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

PROJ = Path(__file__).resolve().parents[1]
RAW_OUT = PROJ / "04_Generated-Clips/part04/raw/v15_fast"
STARTS = PROJ / "04_Generated-Clips/part04/refs/v15_start_frames"
QA = PROJ / "07_Edit-Project/_qa_part04_v15_cut"
SHEET = STARTS / "character_sheet.jpg"
W, H = 1920, 1080
FPS = 24
DUR_S = 8.0

SOURCES = {
    "06_explorer_leaves_gap": PROJ / "04_Generated-Clips/part04/raw/v11_fast/06_explorer_leaves_gap_v11.mp4",
    "09_risk_bet": PROJ / "04_Generated-Clips/part04/raw/v13_fast/09_risk_bet_v13.mp4",
    "09b_risk_hold": PROJ / "04_Generated-Clips/part04/raw/v14_fast/09b_risk_hold_v14.mp4",
    "10_family_before_weight": PROJ / "04_Generated-Clips/part04/raw/v12_fast/10_family_before_weight_v12.mp4",
    "11_publish_gaps": PROJ / "04_Generated-Clips/part04/raw/v01_fast/11_publish_gaps_v01.mp4",
    "11b_wait_and_hunt": PROJ / "04_Generated-Clips/part04/raw/v01_fast/11b_wait_and_hunt_v01.mp4",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_frame(src: Path, t: float, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.check_call([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-ss", f"{t:.3f}", "-i", str(src), "-frames:v", "1",
        "-vf", f"scale={W}:{H}:flags=lanczos", str(dest),
    ])


def is_lava(r: int, g: int, b: int) -> bool:
    if r < 165:
        return False
    if r >= 185 and g >= 60 and b <= 120 and (r - b) >= 80:
        return True
    if r >= 200 and g >= 120 and b <= 150 and (r - b) >= 65 and (r + g) > 330:
        return True
    if r > 210 and g > 160 and b < 110 and (r - b) > 100:
        return True
    return False


def cream_scrub(im: Image.Image) -> Image.Image:
    rgb = im.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    wood, cream, warm = (168, 122, 78), (242, 228, 198), (255, 236, 200)
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            hot = is_lava(r, g, b) or (r > 195 and g > 110 and b < 95 and (r - b) > 110)
            if not hot:
                continue
            if y < int(h * 0.28) and x < int(w * 0.28) and r > 245 and g > 235 and b > 190:
                continue
            t = 0.82 if y > int(h * 0.35) else 0.72
            target = cream if y < int(h * 0.45) else wood
            if y > int(h * 0.40) and x < int(w * 0.45):
                target = warm
            px[x, y] = (
                int((1 - t) * r + t * target[0]),
                int((1 - t) * g + t * target[1]),
                int((1 - t) * b + t * target[2]),
            )
    return rgb.filter(ImageFilter.GaussianBlur(0.35))


def soft_panel_glow(im: Image.Image, box: tuple[float, float, float, float]) -> Image.Image:
    rgba = im.convert("RGBA")
    w, h = rgba.size
    x0, y0, x1, y1 = int(w * box[0]), int(h * box[1]), int(w * box[2]), int(h * box[3])
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for pad, a, col in ((22, 28, (255, 244, 220)), (10, 48, (255, 240, 210)), (0, 70, (255, 236, 200))):
        d.rounded_rectangle((x0 - pad, y0 - pad, x1 + pad, y1 + pad), radius=14, fill=(*col, a))
    return Image.alpha_composite(rgba, ov.filter(ImageFilter.GaussianBlur(2.2))).convert("RGB")


def paint_clean_desk(src_still: Path, out_still: Path, panel_box) -> Image.Image:
    im = Image.open(src_still).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    im = cream_scrub(im)
    px = im.load()
    for y in range(int(H * 0.20), int(H * 0.70)):
        for x in range(0, int(W * 0.55)):
            r, g, b = px[x, y]
            if r > 180 and (r - b) > 70 and g < 190:
                px[x, y] = (
                    min(255, int(r * 0.55 + 230 * 0.45)),
                    min(255, int(g * 0.55 + 210 * 0.45)),
                    min(255, int(b * 0.40 + 175 * 0.60)),
                )
    if panel_box:
        im = soft_panel_glow(im, panel_box)
    im = ImageEnhance.Sharpness(im).enhance(1.25)
    out_still.parent.mkdir(parents=True, exist_ok=True)
    im.save(out_still, quality=95)
    return im


def crown_from_sheet(sheet: Image.Image) -> Image.Image:
    sw, sh = sheet.size
    crops = [
        sheet.crop((int(sw * 0.10), int(sh * 0.01), int(sw * 0.30), int(sh * 0.16))),
        sheet.crop((int(sw * 0.55), int(sh * 0.02), int(sw * 0.78), int(sh * 0.18))),
        sheet.crop((int(sw * 0.78), int(sh * 0.22), int(sw * 0.98), int(sh * 0.38))),
    ]
    best, best_score = crops[0], -1
    for c in crops:
        px = list(c.resize((64, 64)).getdata())
        score = sum(1 for r, g, b in px if r > 60 and r > b + 15 and g < r + 10 and b < 120)
        if score > best_score:
            best, best_score = c, score
    hair = best.resize((int(W * 0.16), int(H * 0.15)), Image.Resampling.LANCZOS)
    return ImageEnhance.Contrast(ImageEnhance.Color(hair).enhance(1.08)).enhance(1.05)


def paint_explorer_frame(base: Image.Image, sheet: Image.Image) -> Image.Image:
    im = cream_scrub(base.copy())
    w, h = im.size
    hair = crown_from_sheet(sheet)
    hw, hh = hair.size
    cx, cy = int(w * 0.505), int(h * 0.268)
    tuft = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(tuft)
    rng = random.Random(7)
    colors = [
        (92, 52, 28), (118, 68, 38), (140, 84, 48), (105, 60, 32),
        (128, 76, 44), (80, 46, 24), (150, 95, 58), (110, 64, 36),
    ]
    for _ in range(420):
        ang = rng.uniform(0, 2 * math.pi)
        rad = rng.uniform(0, 1) ** 0.45
        xx = cx + int(math.cos(ang) * hw * 0.48 * rad)
        yy = cy + int(math.sin(ang) * hh * 0.42 * rad) - int(hh * 0.08)
        col = colors[rng.randrange(len(colors))]
        r0 = rng.randint(2, 6)
        d.ellipse((xx - r0, yy - r0, xx + r0, yy + r0), fill=(*col, 230))
    for _ in range(80):
        x0 = cx + rng.randint(-hw // 2, hw // 2)
        y0 = cy + rng.randint(-hh // 3, hh // 4)
        d.line(
            (x0, y0, x0 + rng.randint(-18, 18), y0 + rng.randint(-10, 16)),
            fill=(*colors[rng.randrange(len(colors))], 200),
            width=rng.randint(2, 4),
        )
    tmask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(tmask).ellipse(
        (cx - hw // 2 - 4, cy - hh // 2 - 8, cx + hw // 2 + 4, cy + hh // 2 + 2), fill=255
    )
    tmask = tmask.filter(ImageFilter.GaussianBlur(5))
    tuft.putalpha(Image.composite(tuft.split()[-1], Image.new("L", (w, h), 0), tmask))
    out = Image.alpha_composite(im.convert("RGBA"), tuft)
    hair_rgba = hair.convert("RGBA")
    mask = Image.new("L", (hw, hh), 0)
    ImageDraw.Draw(mask).ellipse((2, 2, hw - 3, hh - 3), fill=255)
    hair_rgba.putalpha(mask.filter(ImageFilter.GaussianBlur(4)))
    out.alpha_composite(hair_rgba, (cx - hw // 2, cy - hh // 2 - 6))
    px = out.load()
    for y in range(cy - hh // 2, cy + hh // 3):
        for x in range(cx - hw // 2, cx + hw // 2):
            if not (0 <= x < w and 0 <= y < h):
                continue
            r, g, b, a = px[x, y]
            if r > 200 and g > 190 and b > 170:
                px[x, y] = (*colors[(x + y) % len(colors)], 255)
            elif r > 160 and g > 140 and b > 120 and (r + g + b) > 450:
                col = colors[(x * 3 + y) % len(colors)]
                px[x, y] = (
                    int(r * 0.35 + col[0] * 0.65),
                    int(g * 0.35 + col[1] * 0.65),
                    int(b * 0.35 + col[2] * 0.65),
                    255,
                )
    return cream_scrub(out.convert("RGB"))


def encode_still_movie(still: Image.Image, audio_src: Path, dest: Path) -> None:
    n = int(DUR_S * FPS)
    with tempfile.TemporaryDirectory(prefix="hos_v15_still_") as td:
        fout = Path(td) / "f"
        fout.mkdir()
        base = still.convert("RGB")
        for i in range(n):
            frame = base.copy()
            if i % 7 == 0:
                frame = ImageEnhance.Brightness(frame).enhance(1.006)
            elif i % 7 == 3:
                frame = ImageEnhance.Brightness(frame).enhance(0.994)
            grain = Image.effect_noise((W, H), 7).convert("L")
            frame = Image.blend(frame, Image.merge("RGB", (grain, grain, grain)), 0.028)
            frame.save(fout / f"f_{i + 1:04d}.jpg", quality=94)
        tmp = dest.with_suffix(".tmp.mp4")
        subprocess.check_call([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-framerate", str(FPS), "-i", str(fout / "f_%04d.jpg"),
            "-i", str(audio_src),
            "-map", "0:v", "-map", "1:a?",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17",
            "-preset", "medium", "-c:a", "aac", "-b:a", "192k",
            "-shortest", "-t", f"{DUR_S:.2f}", str(tmp),
        ])
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(tmp), str(dest))


def build_static_plate(pid: str, t_pick: float, panel_box) -> dict:
    src = SOURCES[pid]
    if not src.exists():
        raise SystemExit(f"missing source {src}")
    raw_still = STARTS / f"{pid}_start_v15_src.jpg"
    painted = STARTS / f"{pid}_start_v15_hardclean.jpg"
    extract_frame(src, t_pick, raw_still)
    still = paint_clean_desk(raw_still, painted, panel_box)
    dest = RAW_OUT / f"{pid}_v15.mp4"
    encode_still_movie(still, src, dest)
    return {
        "plate": pid,
        "out": str(dest),
        "sha256": sha256(dest),
        "method": "hardclean_near_static",
        "painted": str(painted),
    }


def build_06() -> dict:
    src = SOURCES["06_explorer_leaves_gap"]
    if not src.exists():
        raise SystemExit(f"missing {src}")
    sheet = Image.open(SHEET).convert("RGB")
    painted_path = STARTS / "06_explorer_leaves_gap_start_v15_hardclean.jpg"
    with tempfile.TemporaryDirectory(prefix="hos_v15_06_") as td:
        tdir = Path(td)
        fin, fout = tdir / "in", tdir / "out"
        fin.mkdir()
        fout.mkdir()
        subprocess.check_call([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(src), "-vf", f"fps={FPS},scale={W}:{H}:flags=lanczos",
            str(fin / "f_%04d.jpg"),
        ])
        frames = sorted(fin.glob("f_*.jpg"))
        mask = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(mask)
        d.ellipse((int(W * 0.40), int(H * 0.14), int(W * 0.62), int(H * 0.42)), fill=255)
        d.rectangle((0, 0, int(W * 0.34), int(H * 0.58)), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(16))
        master = paint_explorer_frame(Image.open(frames[max(0, len(frames) // 3)]), sheet)
        master.save(painted_path, quality=95)
        for i, fp in enumerate(frames):
            motion = Image.open(fp).convert("RGB")
            locked = paint_explorer_frame(motion, sheet)
            frame = Image.composite(master, locked, mask)
            crown_mask = Image.new("L", (W, H), 0)
            ImageDraw.Draw(crown_mask).ellipse(
                (int(W * 0.42), int(H * 0.16), int(W * 0.60), int(H * 0.38)), fill=255
            )
            crown_mask = crown_mask.filter(ImageFilter.GaussianBlur(10))
            frame = Image.composite(master, frame, crown_mask)
            frame = cream_scrub(frame)
            frame.save(fout / fp.name, quality=94)
            if i % 40 == 0:
                print(f"  06 frame {i}/{len(frames)}", flush=True)
        dest = RAW_OUT / "06_explorer_leaves_gap_v15.mp4"
        tmp = dest.with_suffix(".tmp.mp4")
        subprocess.check_call([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-framerate", str(FPS), "-i", str(fout / "f_%04d.jpg"),
            "-i", str(src),
            "-map", "0:v", "-map", "1:a?",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17",
            "-preset", "medium", "-c:a", "aac", "-b:a", "192k",
            "-shortest", "-t", f"{DUR_S:.2f}", str(tmp),
        ])
        shutil.move(str(tmp), str(dest))
    return {
        "plate": "06_explorer_leaves_gap",
        "out": str(dest),
        "sha256": sha256(dest),
        "method": "crown_dna_lamp_lock",
        "painted": str(painted_path),
    }


def main() -> None:
    RAW_OUT.mkdir(parents=True, exist_ok=True)
    STARTS.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    if not SHEET.exists():
        raise SystemExit(f"missing character sheet {SHEET}")
    rejected = RAW_OUT / "_rejected"
    rejected.mkdir(exist_ok=True)
    for pid in SOURCES:
        old = RAW_OUT / f"{pid}_v15.mp4"
        if old.exists():
            shutil.move(str(old), str(rejected / f"{pid}_v15_pre_hard_{old.stat().st_mtime_ns}.mp4"))
    results = []
    print("=== 06 crown DNA + CLEAN LIGHT ===", flush=True)
    results.append(build_06())
    for pid, t_pick, panel in [
        ("09_risk_bet", 2.0, (0.42, 0.26, 0.58, 0.48)),
        ("09b_risk_hold", 1.0, (0.42, 0.27, 0.58, 0.46)),
        ("10_family_before_weight", 1.5, None),
        ("11_publish_gaps", 1.5, None),
        ("11b_wait_and_hunt", 1.5, None),
    ]:
        print(f"=== {pid} hardclean near-static ===", flush=True)
        results.append(build_static_plate(pid, t_pick, panel))
    for r in results:
        pid = r["plate"]
        dest = Path(r["out"])
        for t in (0.5, 2.0, 4.0, 6.0):
            subprocess.check_call([
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-ss", str(t), "-i", str(dest), "-frames:v", "1",
                str(QA / f"plate_{pid}_t{t:.0f}.jpg"),
            ])
        print(json.dumps({k: r[k] for k in ("plate", "sha256", "method")}), flush=True)
    summary = {
        "results": results,
        "status": "HARD_CLEAN_V15_PLATES — do not PASS",
        "flow_account": "benoats@googlemail.com",
    }
    (QA / "hard_clean_build_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print("HARD CLEAN PLATE BUILD OK", flush=True)


if __name__ == "__main__":
    main()
