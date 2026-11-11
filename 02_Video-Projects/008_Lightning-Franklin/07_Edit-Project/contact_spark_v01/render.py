#!/usr/bin/env python3
"""HOS 008 salon contact point; J2591. No video-take input or placement."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess

import numpy as np
from PIL import Image

WARM = (255, 246, 224)


def spark(size, rod, knuckle, phase, frames=4):
    """Straight-alpha RGBA; phase 0 is the supplied contact frame (zero-based)."""
    w, h = size
    if frames not in (3, 4) or w < 16 or h < 16:
        raise ValueError('Use 3 or 4 frames and a valid canvas')
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
    # Circular point only: its entire support fits inside the gap's diameter.
    cx, cy = (np.array(rod) + np.array(knuckle)) / 2
    yy, xx = np.ogrid[:h, :w]
    distance = np.sqrt((xx - cx)**2 + (yy - cy)**2)
    radius = min(2.8 * scale, gap / 2)
    envelope = (1.0, .58, .23, .08)[:frames]
    alpha = np.clip((radius - distance) / max(.65 * scale, .2), 0, 1) * 255 * envelope[phase]
    if phase == 0:
        bloom_radius = min(6 * scale, gap / 2)
        bloom = np.clip(1 - distance / bloom_radius, 0, 1)**2 * 24
        alpha = np.maximum(alpha, bloom)
    out[:, :, :3] = WARM
    out[:, :, 3] = np.rint(alpha).astype(np.uint8)
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
    p.add_argument('--frames', type=int, choices=(3, 4), default=4)
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
