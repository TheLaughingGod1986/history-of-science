#!/usr/bin/env python3
"""HOS 008 salon tapered contact streak. J2613 geometry, size revision 6796829044. No video-take input or placement."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess

import numpy as np
from PIL import Image

WARM = (255, 246, 224)
# Desk 6796829044. The 2px core was a hairline at phone width.
# Peak frame: about 3.8px FWHM through the middle at 1080p, plus one soft bloom.
# FWHM = 2*sqrt(2*ln2)*sigma. Ends stay tapered. The half-strength frame has no bloom.
CORE_SIGMA_END = 0.50
CORE_SIGMA_MID = 1.61
BLOOM_PEAK = 80.0
BLOOM_SIGMA = 10.5


def spark(size, rod, knuckle, phase, frames=4):
    """Straight-alpha RGBA; phase 0 is the supplied contact frame (zero-based)."""
    w, h = size
    if frames not in (2, 3, 4) or w < 16 or h < 16:
        raise ValueError('Use 2, 3 or 4 frames and a valid canvas')
    for p in (rod, knuckle):
        if len(p) != 2 or not all(math.isfinite(v) for v in p):
            raise ValueError('Points must be finite x,y pairs')
        if not (0 <= p[0] < w and 0 <= p[1] < h):
            raise ValueError('Point outside canvas')
    scale = h / 1080
    gap = math.dist(rod, knuckle)
    if not 2 * scale <= gap <= 24 * scale:
        raise ValueError('Use visible gap edges 2–24 px apart at 1080p; do not bridge a distant hand')
    out = np.zeros((h, w, 4), dtype=np.uint8)
    if phase not in range(frames):
        return Image.fromarray(out)
    # Integrate a continuous Gaussian profile over each pixel at 8x sampling.
    # Work only in the local support, so a 1080p canvas stays inexpensive.
    rod, knuckle = np.array(rod, dtype=float), np.array(knuckle, dtype=float)
    axis = (rod - knuckle) / gap
    # Bloom radius is about 25px at 1080p, so the support is wider than the streak.
    pad = 36 * scale + 2
    x0 = max(0, int(min(rod[0], knuckle[0]) - pad))
    x1 = min(w, int(max(rod[0], knuckle[0]) + pad) + 1)
    y0 = max(0, int(min(rod[1], knuckle[1]) - pad))
    y1 = min(h, int(max(rod[1], knuckle[1]) + pad) + 1)
    ss = 8
    yy, xx = np.meshgrid(y0 + (np.arange((y1-y0)*ss)+.5)/ss - .5,
                         x0 + (np.arange((x1-x0)*ss)+.5)/ss - .5, indexing='ij')
    along = (xx-knuckle[0])*axis[0] + (yy-knuckle[1])*axis[1]
    across = -(xx-knuckle[0])*axis[1] + (yy-knuckle[1])*axis[0]
    if phase < 2:
        start, end = (0., gap) if phase == 0 else (.1*gap, .9*gap)
        t = np.clip((along-start)/(end-start), 0, 1)
        # About 3.8px full-width at half maximum in the middle at 1080p,
        # tapering to rounded fine ends. No rectangle or hard clipping.
        sigma = scale * (CORE_SIGMA_END + (CORE_SIGMA_MID - CORE_SIGMA_END) * np.sin(np.pi*t))
        beyond = np.maximum(start-along, 0) + np.maximum(along-end, 0)
        core = np.exp(-.5*((across/sigma)**2 + (beyond/(.35*scale))**2))
        alpha = core * (245 if phase == 0 else 122.5)
        if phase == 0:
            mid = (rod + knuckle) / 2
            bloom_sigma = BLOOM_SIGMA * scale
            radius2 = (xx-mid[0])**2 + (yy-mid[1])**2
            bloom = BLOOM_PEAK * np.exp(-.5 * radius2 / bloom_sigma**2)
            alpha = np.maximum(alpha, bloom)
    else:
        # Optional generic +2/+3 tail stays at the knuckle, never mid-gap.
        radius2 = (xx-knuckle[0])**2 + (yy-knuckle[1])**2
        alpha = (55 if phase == 2 else 18)*np.exp(-radius2/(2*(.65*scale)**2))
    alpha = alpha.reshape(y1-y0, ss, x1-x0, ss).mean(axis=(1, 3))
    out[y0:y1, x0:x1, :3] = WARM
    out[y0:y1, x0:x1, 3] = np.rint(alpha).astype(np.uint8)
    out[out[:, :, 3] == 0] = 0
    return Image.fromarray(out)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--still', type=Path, required=True, help='Reference still, never a video take')
    p.add_argument('--contact-frame', type=int, required=True, help='Zero-based destination frame; metadata only')
    p.add_argument('--rod', type=float, nargs=2, required=True, metavar=('X', 'Y'))
    p.add_argument('--knuckle', type=float, nargs=2, required=True, metavar=('X', 'Y'))
    p.add_argument('--frames', type=int, choices=(2, 3, 4), default=4)
    p.add_argument('--fps', type=int, choices=(24, 25, 30), default=24)
    p.add_argument('--sfx', type=Path, required=True, help='Existing film pen-tap/crackle; no generation')
    p.add_argument('--demo', action='store_true', help='Coordinates are illustrative, not measured contact')
    p.add_argument('--out', type=Path, required=True, help='New output directory; never overwrites')
    a = p.parse_args()
    if a.contact_frame < 0:
        p.error('contact-frame must be nonnegative')
    bg = Image.open(a.still).convert('RGBA')
    overlays = [spark(bg.size, a.rod, a.knuckle, i, a.frames) for i in range(a.frames)]
    if not a.sfx.is_file():
        p.error('Existing SFX file missing')
    a.out.mkdir(parents=True, exist_ok=False)
    for i, overlay in enumerate(overlays):
        overlay.save(a.out / f'spark_{i:02}.png')
        Image.alpha_composite(bg, overlay).convert('RGB').save(a.out / f'preview_{i:02}.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-n', '-framerate', str(a.fps), '-i', str(a.out / 'spark_%02d.png'),
                    '-frames:v', str(a.frames), '-c:v', 'qtrle', '-pix_fmt', 'argb', str(a.out / 'spark_rgba.mov')], check=True)
    # Two-second still demonstration only, with one flick after 0.5 s and existing tick.
    demo_frame = a.fps // 2
    for i in range(a.fps * 2):
        phase = i - demo_frame
        frame = Image.alpha_composite(bg, overlays[phase]) if phase in range(a.frames) else bg
        frame.convert('RGB').save(a.out / f'demo_{i:03}.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-n', '-framerate', str(a.fps), '-i', str(a.out / 'demo_%03d.png'),
                    '-i', str(a.sfx), '-filter_complex', '[1:a]adelay=500:all=1,apad[a]', '-map', '0:v', '-map', '[a]',
                    '-t', '2', '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
                    str(a.out / 'still_demo_with_existing_tick.mp4')], check=True)
    manifest = dict(job='J2591', row='P2:02_salon_spark', kind='own_code_graphic',
                    preview_only=True, illustrative_coordinates=a.demo, size=list(bg.size), fps=a.fps,
                    contact_frame_zero_based=a.contact_frame, rod=a.rod, knuckle=a.knuckle,
                    frames=a.frames, rgba='straight alpha; PNG canonical; qtrle argb MOV convenience',
                    colour_rgb=WARM, bloom_frames=[0], source_still=str(a.still), source_sha256=sha(a.still),
                    sfx=str(a.sfx), sfx_sha256=sha(a.sfx), sfx_cue_frame_zero_based=a.contact_frame,
                    demo_contact_frame=demo_frame, placement_job='J2592', video_take_modified=False,
                    files={f.name: sha(f) for f in sorted(a.out.iterdir()) if f.is_file()})
    (a.out / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'Wrote {a.frames} RGBA frames and still-only preview: {a.out}')


if __name__ == '__main__':
    main()
