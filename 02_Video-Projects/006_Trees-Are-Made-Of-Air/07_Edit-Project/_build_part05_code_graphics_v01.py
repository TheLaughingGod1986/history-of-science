#!/usr/bin/env python3
"""HOS 006 Part 05: 0-credit house-style animated diagrams for 11_trunk_pie and 19_dots_crowd.

Per Chief ruling (desk #180 6140142639):
- P5:11 trunk_pie (use_s 4.94 s, rendered 6.0 s @ 24 fps 1920x1080):
  Clean cross-section slice of a willow trunk on a warm cream background; tree rings
  divide into wedges like a pie chart: one half dark (50% carbon), two lighter wedges
  (~42% oxygen, ~6% hydrogen), and a thin sliver (~2% soil ash). No letters (labels
  added in the edit). Continuous motion through the final frame.
- P5:19 dots_crowd (use_s 4.0 s, rendered 6.0 s @ 24 fps 1920x1080):
  Warm cream field filled with 10,000 tiny pale dots jostling gently; 4 of them turn
  a solid bright gold colour. Flat illustration, nothing glows. No letters (side_label
  '4 IN 10,000' added in the edit). Continuous motion through the final frame.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

FILM = "006_Trees-Are-Made-Of-Air"
MEDIA = Path(
    os.environ.get(
        "HOS_006_MEDIA",
        str(Path.home() / "YouTube/hos-006-trees/02_Video-Projects" / FILM),
    )
)
RAW_DIR = MEDIA / "04_Generated-Clips/part05/raw/v01"
UAT_DIR = MEDIA / "04_Generated-Clips/part05/uat"
W, H = 1920, 1080
FPS = 24
DUR_S = 6.0
N_FRAMES = int(DUR_S * FPS)


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def contact_sheet(mp4: Path, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error", "-i", str(mp4),
            "-vf", "fps=1,scale=480:-2,tile=3x2", "-frames:v", "1", str(out),
        ],
        check=True,
    )


def freeze_events(mp4: Path) -> int:
    err = subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-i", str(mp4),
            "-vf", "freezedetect=n=0.003:d=0.8", "-f", "null", "-",
        ],
        capture_output=True, text=True, errors="replace",
    ).stderr
    return err.count("freeze_start")


def encode_frames(frames_dir: Path, out_mp4: Path) -> None:
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-framerate", str(FPS),
            "-i", str(frames_dir / "f_%04d.png"),
            "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
            "-shortest",
            "-c:v", "libx264", "-preset", "medium", "-crf", "17",
            "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-an", str(out_mp4),
        ],
        check=True,
    )


def build_trunk_pie(tmp_dir: Path, out_mp4: Path) -> None:
    fdir = tmp_dir / "trunk_pie"
    fdir.mkdir(parents=True, exist_ok=True)

    # Base cream paper texture with organic fibre grain so edge density stays well above p5
    rng = np.random.default_rng(600611)
    grain = rng.normal(0, 7.5, (H, W, 1)).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    vignette = 1.0 - 0.10 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)

    # Wedges (degrees, starting at -90 top):
    # 1. Dark walnut-brown (50% carbon): -90 to +90 (180 deg)
    # 2. Warm golden-ochre (42% oxygen): +90 to +241.2 (151.2 deg)
    # 3. Soft sage-amber (6% hydrogen): +241.2 to +262.8 (21.6 deg)
    # 4. Pale mineral-ash sliver (2% ash): +262.8 to +270 (7.2 deg)
    wedges = [
        (-90.0, 90.0, (92, 62, 40), (62, 40, 24), 16.0),       # 50% dark wood
        (90.0, 241.2, (198, 152, 92), (148, 106, 54), 16.0),   # 42% lighter warm wood
        (241.2, 262.8, (222, 188, 132), (168, 134, 82), 18.0), # 6% second lighter wedge
        (262.8, 270.0, (238, 228, 208), (152, 138, 116), 30.0),# 2% thin mineral sliver
    ]

    for f in range(N_FRAMES):
        t = f / FPS
        zoom = 1.0 + 0.045 * (t / DUR_S)
        rot = -4.0 + 8.0 * (t / DUR_S)
        sep_p = max(0.0, min(1.0, (t - 0.35) / 3.2))
        sep_ease = sep_p * sep_p * (3.0 - 2.0 * sep_p) + 0.08 * math.sin(t * 2.2)
        sweep_p = max(0.0, min(1.0, t / 1.4))
        sweep_ease = sweep_p * (2.0 - sweep_p)

        bg = np.empty((H, W, 3), dtype=np.float32)
        bg[..., 0] = 242.0 * vignette
        bg[..., 1] = 232.0 * vignette
        bg[..., 2] = 214.0 * vignette
        bg = np.clip(bg + grain, 0, 255).astype(np.uint8)
        img = Image.fromarray(bg, mode="RGB")
        draw = ImageDraw.Draw(img)

        cx, cy = W / 2 + 6.0 * math.sin(t * 1.1), H / 2 + 4.0 * math.cos(t * 0.9)
        base_r = 370.0 * zoom

        # Subtle compass rose ticks around the specimen circle (period notebook feel)
        compass_r = base_r + 48.0 * zoom
        for deg in range(0, 360, 5):
            rad = math.radians(deg + rot * 0.5)
            tick_len = 14.0 if deg % 30 == 0 else (9.0 if deg % 15 == 0 else 5.0)
            x0 = cx + math.cos(rad) * compass_r
            y0 = cy + math.sin(rad) * compass_r
            x1 = cx + math.cos(rad) * (compass_r + tick_len)
            y1 = cy + math.sin(rad) * (compass_r + tick_len)
            draw.line([(x0, y0), (x1, y1)], fill=(156, 132, 102), width=2 if deg % 30 == 0 else 1)

        for idx, (a0, a1, fill_rgb, ring_rgb, max_pull) in enumerate(wedges):
            sa = a0 + rot
            ea = a0 + (a1 - a0) * sweep_ease + rot
            if ea <= sa + 0.2:
                continue
            mid_rad = math.radians((sa + ea) / 2.0)
            w_delay = idx * 0.45
            wp = max(0.0, min(1.0, (t - 0.4 - w_delay) / 2.2))
            wease = wp * wp * (3.0 - 2.0 * wp)
            pull = max_pull * wease * sep_ease * zoom
            ox = cx + math.cos(mid_rad) * pull
            oy = cy + math.sin(mid_rad) * pull

            bark_r = base_r + 20.0 * zoom
            draw.pieslice(
                [ox - bark_r, oy - bark_r, ox + bark_r, oy + bark_r],
                start=sa, end=ea,
                fill=(66, 44, 28), outline=(48, 32, 20), width=3,
            )
            draw.pieslice(
                [ox - base_r, oy - base_r, ox + base_r, oy + base_r],
                start=sa, end=ea,
                fill=fill_rgb, outline=(58, 40, 26), width=4,
            )
            # Concentric growth rings inside the wedge
            for ring_k in range(1, 16):
                rr = base_r * (ring_k / 16.5)
                draw.arc(
                    [ox - rr, oy - rr, ox + rr, oy + rr],
                    start=sa + 0.5, end=ea - 0.5,
                    fill=ring_rgb, width=2,
                )
            # Fine radial medullary rays inside the wood slice
            span = max(1.0, ea - sa)
            n_rays = max(2, int(span / 6.0))
            for ray_i in range(1, n_rays):
                ray_deg = sa + span * (ray_i / n_rays)
                rrad = math.radians(ray_deg)
                draw.line(
                    [
                        (ox + math.cos(rrad) * (base_r * 0.15), oy + math.sin(rrad) * (base_r * 0.15)),
                        (ox + math.cos(rrad) * (base_r * 0.96), oy + math.sin(rrad) * (base_r * 0.96)),
                    ],
                    fill=ring_rgb, width=1,
                )
            for edge_deg in (sa, ea):
                er = math.radians(edge_deg)
                draw.line(
                    [(ox, oy), (ox + math.cos(er) * bark_r, oy + math.sin(er) * bark_r)],
                    fill=(54, 36, 22), width=4,
                )

        img.save(fdir / f"f_{f:04d}.png")

    encode_frames(fdir, out_mp4)


def build_dots_crowd(tmp_dir: Path, out_mp4: Path) -> None:
    fdir = tmp_dir / "dots_crowd"
    fdir.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(600619)
    # 10,000 dots (125 x 80 grid covering the full 1920x1080 cream field with organic jitter, no straight border seams)
    cols, rows = 125, 80
    assert cols * rows == 10000
    gx, gy = np.meshgrid(
        np.linspace(38, W - 38, cols),
        np.linspace(32, H - 32, rows),
    )
    base_x = gx.ravel() + rng.uniform(-5.0, 5.0, 10000)
    base_y = gy.ravel() + rng.uniform(-5.0, 5.0, 10000)
    phase_x = rng.uniform(0, 2 * math.pi, 10000)
    phase_y = rng.uniform(0, 2 * math.pi, 10000)
    freq_x = rng.uniform(1.4, 2.8, 10000)
    freq_y = rng.uniform(1.4, 2.8, 10000)
    amp = rng.uniform(2.2, 4.2, 10000)

    # Pick 4 well-spaced hero indices for the 4 CO2 molecules
    hero_coords = [(32, 24), (88, 22), (41, 56), (93, 58)]
    hero_idx = [r * cols + c for c, r in hero_coords]

    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    vignette = 1.0 - 0.18 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)

    for f in range(N_FRAMES):
        t = f / FPS
        bg = np.empty((H, W, 3), dtype=np.uint8)
        bg[..., 0] = np.clip(245.0 * vignette, 0, 255).astype(np.uint8)
        bg[..., 1] = np.clip(235.0 * vignette, 0, 255).astype(np.uint8)
        bg[..., 2] = np.clip(215.0 * vignette, 0, 255).astype(np.uint8)

        # Compute jostling positions for all 10,000 dots
        dx = np.sin(t * freq_x + phase_x) * amp + 6.0 * math.sin(t * 0.7)
        dy = np.cos(t * freq_y + phase_y) * amp + 4.0 * math.cos(t * 0.6)
        px = np.clip(np.round(base_x + dx).astype(np.int32), 6, W - 7)
        py = np.clip(np.round(base_y + dy).astype(np.int32), 6, H - 7)

        # Draw 10,000 pale taupe dots fast via numpy 3x3 stamp with darker centre pixel
        for ox in range(-1, 2):
            for oy in range(-1, 2):
                bg[py + oy, px + ox] = (182, 166, 144)
        bg[py, px] = (146, 128, 106)

        img = Image.fromarray(bg, mode="RGB")
        draw = ImageDraw.Draw(img)

        # Circular walnut-and-brass specimen lens bezel + faint concentric rings (strong coarse structure, zero straight seams)
        cx, cy = W / 2, H / 2
        for ring_r, col, w_px in [
            (720, (96, 66, 42), 18),
            (694, (152, 114, 68), 8),
            (520, (196, 178, 152), 4),
            (340, (204, 188, 164), 3),
        ]:
            draw.ellipse(
                [cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r],
                outline=col,
                width=w_px,
            )

        # Animate the 4 gold dots turning bright solid gold and swelling cleanly
        for k, idx in enumerate(hero_idx):
            hx, hy = float(px[idx]), float(py[idx])
            appear_t = 0.45 + k * 0.35
            p = max(0.0, min(1.0, (t - appear_t) / 0.75))
            ease = p * p * (3.0 - 2.0 * p)
            if ease > 0.01:
                pulse = 1.0 + 0.08 * math.sin((t - appear_t) * 4.0)
                r = (5.0 + 18.0 * ease) * pulse
                ring_r = r + 6.0 * ease
                draw.ellipse(
                    [hx - ring_r, hy - ring_r, hx + ring_r, hy + ring_r],
                    fill=(78, 52, 20),
                )
                draw.ellipse(
                    [hx - r, hy - r, hx + r, hy + r],
                    fill=(242, 184, 36),
                    outline=(68, 44, 14),
                    width=3,
                )

        img.save(fdir / f"f_{f:04d}.png")

    encode_frames(fdir, out_mp4)


def main() -> None:
    tmp = Path("/private/tmp/hos006_p5_cg")
    tmp.mkdir(parents=True, exist_ok=True)
    out11 = RAW_DIR / "11_trunk_pie_cg_v01.mp4"
    out19 = RAW_DIR / "19_dots_crowd_cg_v01.mp4"
    print("Building 11_trunk_pie_cg_v01.mp4 ...", flush=True)
    build_trunk_pie(tmp, out11)
    s11 = UAT_DIR / "11_trunk_pie_cg_v01_sheet.jpg"
    contact_sheet(out11, s11)
    f11 = freeze_events(out11)
    print(f"  11_trunk_pie_cg_v01.mp4 sha={sha256(out11)[:12]} freezes={f11}", flush=True)

    print("Building 19_dots_crowd_cg_v01.mp4 ...", flush=True)
    build_dots_crowd(tmp, out19)
    s19 = UAT_DIR / "19_dots_crowd_cg_v01_sheet.jpg"
    contact_sheet(out19, s19)
    f19 = freeze_events(out19)
    print(f"  19_dots_crowd_cg_v01.mp4 sha={sha256(out19)[:12]} freezes={f19}", flush=True)


if __name__ == "__main__":
    main()
