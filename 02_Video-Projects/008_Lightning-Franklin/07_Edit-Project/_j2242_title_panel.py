"""Put an unbordered umber panel behind the picture titles that stay.

Five code-graphic titles sit on a moving picture with no panel. The letter
row is the cream-letter replacement, which has no banner and no boxes, so
it is not painted here. The other four keep their words. The panel is the
caption umber, with no border, gold rule or pill. Frame 2869 stays out.
These are stills of the panel behind the existing words. No master is written.
"""
import argparse
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

import _build_rough_v13_recipe as recipe

W, H = 1920, 1080
UMBER = (48, 30, 20)
PAD = 28
TITLE_Y_MAX = 320
ROW_MIN = 80
MIN_BAND = 36
MAX_BAND = 80
ALIGN_MAE_MAX = 30.0

# The letter row is absent on purpose: its replacement removes the banner.
PAINT_ROWS = (
    '15_likeness_fire',
    '06_same_thing',
    '08_looking_path',
    '10_metal_easy',
)
LABELS = {
    '15_likeness_fire': 'CRACK · FIRE · SHOCK',
    '06_same_thing': 'ELECTRICITY',
    '08_looking_path': 'EASIEST PATH DOWN',
    '10_metal_easy': 'METAL CONDUCTS',
}
ALPHA = Path('/Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/code_graphics_v05')
SOURCES = {
    '15_likeness_fire': {
        'picture': Path('/Volumes/data/mac-mini-archive/tmp-render-scratch/j1248-hos008-rough-v05/special_assets/overlay_15_likeness_fire.mp4'),
        'picture_sha256': 'a18a51228c1f197a06336eeed096d38d24f775851093281086ee19bb443d8f92',
        'picture_bytes': 2818747,
        'alpha': ALPHA / 'code_graphic_008_p2_15_likeness_fire.mov',
        'alpha_sha256': 'f190e3e60ba03807ca7b4bc1dd823ea4e51a92b2455d5dd481cbf3122d67b596',
        'alpha_bytes': 56847531,
        'seek': '2.2',
    },
    '06_same_thing': {
        'picture': Path('/Volumes/data/mac-mini-archive/tmp-render-scratch/j1248-hos008-rough-v05/special_assets/overlay_06_same_thing.mp4'),
        'picture_sha256': '49c687ef5f6e862048d38fedbf6b3245d578e1311897ca02d8d002162a26bc54',
        'picture_bytes': 5614711,
        'alpha': ALPHA / 'code_graphic_008_p4_06_same_thing.mov',
        'alpha_sha256': 'd770bb34b46921c4c80b4b170bdfe5e5625765677c374b9a7fa91bc420466715',
        'alpha_bytes': 93444791,
        'seek': '5.6',
    },
    '08_looking_path': {
        'picture': Path('/Volumes/data/mac-mini-archive/tmp-render-scratch/j1218-hos008-rough-v03/special_assets/overlay_08_looking_path.mp4'),
        'picture_sha256': '80e37778e0e164c01532457ca8daaf30fa72dc306cc739170e40c44f2621be11',
        'picture_bytes': 1992880,
        'alpha': ALPHA / 'code_graphic_008_p5_08_looking_path.mov',
        'alpha_sha256': '7a16e548251c9c59337666a2a034f995955d6b16b3560efe02652829ceb3928e',
        'alpha_bytes': 23593579,
        'seek': '2.0',
    },
    '10_metal_easy': {
        'picture': recipe.DEFAULT_MASTER,
        'picture_sha256': recipe.MASTER_SHA,
        'picture_bytes': recipe.MASTER_BYTES,
        'master_frame': 11017,
        'alpha': ALPHA / 'code_graphic_008_p5_10_metal_easy.mov',
        'alpha_sha256': 'bb821f402a2d1ca5a1536a6592e572b8a4d1653d6573ca733c2ae853db4c8056',
        'alpha_bytes': 20257295,
        'seek': '1.5',
    },
}


def label_words(text):
    words = text.replace('·', ' ').split()
    if not words or len(words) > 4:
        raise ValueError(f'Title must be one to four words: {text}')
    return words


def title_box(alpha):
    """Return the padded box of the one dense title line. A diagram is not a title."""
    if getattr(alpha, 'shape', None) != (H, W, 4):
        raise ValueError('Expected one 1920x1080 alpha frame')
    opaque = alpha[:, :, 3] > 0
    rows = opaque[:TITLE_Y_MAX].sum(axis=1)
    hot = np.where(rows > ROW_MIN)[0]
    if len(hot) == 0:
        raise ValueError('No title band')
    splits = np.where(np.diff(hot) > 1)[0]
    starts = [int(hot[0])] + [int(hot[i + 1]) for i in splits]
    ends = [int(hot[i]) for i in splits] + [int(hot[-1])]
    candidates = []
    for start, end in zip(starts, ends):
        height = end - start + 1
        if MIN_BAND <= height <= MAX_BAND:
            candidates.append((int(opaque[start:end + 1].sum()), start, end))
    if len(candidates) != 1:
        raise ValueError(f'Expected one title line, found {len(candidates)}')
    _, start, end = candidates[0]
    xs = np.where(opaque[start:end + 1].any(axis=0))[0]
    if len(xs) == 0:
        raise ValueError('Title line has no pixels')
    return (
        max(0, int(xs.min()) - PAD),
        max(0, start - PAD),
        min(W - 1, int(xs.max()) + PAD),
        min(H - 1, end + PAD),
    )


def panel_behind(picture, box, glyphs):
    """Paint umber inside the box wherever the title is not. The words stay."""
    if getattr(picture, 'shape', None) != (H, W, 3) or getattr(glyphs, 'shape', None) != (H, W):
        raise ValueError('Expected a 1920x1080 picture and a full-frame glyph mask')
    if glyphs.dtype != np.bool_:
        raise ValueError('Glyph mask must be boolean')
    x0, y0, x1, y1 = (int(v) for v in box)
    if not (0 <= x0 < x1 < W and 0 <= y0 < y1 < H):
        raise ValueError('Title box is outside the frame')
    mask = glyphs[y0:y1 + 1, x0:x1 + 1]
    if not mask.any():
        raise ValueError('Title box has no glyphs')
    if mask.all():
        raise ValueError('Title box has no room for a panel')
    out = np.array(picture, copy=True)
    region = out[y0:y1 + 1, x0:x1 + 1]
    region[~mask] = UMBER
    changed = np.any(out != picture, axis=2)
    if changed.any() and not np.all(out[changed] == UMBER):
        raise ValueError('Panel drew a colour other than umber')
    outside = np.ones((H, W), dtype=bool)
    outside[y0:y1 + 1, x0:x1 + 1] = False
    if np.any(out[outside] != picture[outside]):
        raise ValueError('Panel changed the picture outside the title box')
    if np.any(out[glyphs] != picture[glyphs]):
        raise ValueError('Panel changed the title glyphs')
    return out


def decode_rgba(path, seek=None, frame=None):
    command = ['ffmpeg', '-nostdin', '-v', 'error', '-xerror']
    if seek is not None:
        command += ['-ss', str(seek)]
    command += ['-i', str(path)]
    if frame is not None:
        command += ['-vf', f'select=eq(n\\,{int(frame)})']
    command += ['-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-']
    raw = subprocess.check_output(command)
    expected = W * H * 4
    if len(raw) != expected:
        raise ValueError(f'Decoded {len(raw)} bytes from {path}, expected {expected}')
    return np.frombuffer(raw, dtype=np.uint8).reshape(H, W, 4)


def alignment_mae(picture, alpha, glyphs):
    solid = glyphs & (alpha[:, :, 3] > 200)
    if int(solid.sum()) < 100:
        raise ValueError('Too few solid title pixels to check alignment')
    diff = np.abs(picture.astype(np.int16) - alpha[:, :, :3].astype(np.int16))
    return float(diff[solid].mean())


def paint_row(name, source):
    recipe.require_hash(source['picture'], source['picture_sha256'], source['picture_bytes'])
    recipe.require_hash(source['alpha'], source['alpha_sha256'], source['alpha_bytes'])
    if 'master_frame' in source:
        picture = decode_rgba(source['picture'], frame=source['master_frame'])[:, :, :3]
    else:
        picture = decode_rgba(source['picture'], seek=source['seek'])[:, :, :3]
    alpha = decode_rgba(source['alpha'], seek=source['seek'])
    box = title_box(alpha)
    glyphs = alpha[:, :, 3] > 0
    mae = alignment_mae(picture, alpha, glyphs)
    if mae > ALIGN_MAE_MAX:
        raise ValueError(f'{name} title is not on this frame (MAE {mae:.2f})')
    painted = panel_behind(picture, box, glyphs)
    recipe.require_hash(source['picture'], source['picture_sha256'], source['picture_bytes'])
    recipe.require_hash(source['alpha'], source['alpha_sha256'], source['alpha_bytes'])
    return {
        'row': name,
        'label': LABELS[name],
        'words': label_words(LABELS[name]),
        'box': list(box),
        'alignment_mae': round(mae, 3),
        'glyph_pixels': int(glyphs[box[1]:box[3] + 1, box[0]:box[2] + 1].sum()),
        'panel_pixels': int((~glyphs[box[1]:box[3] + 1, box[0]:box[2] + 1]).sum()),
        'picture': painted,
    }


def save_still(image, path, phone):
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(image, 'RGB').save(path, quality=92)
    subprocess.run(
        ['ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-i', str(path),
         '-vf', 'scale=168:94', '-frames:v', '1', '-y', str(phone)],
        check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    args = parser.parse_args()
    if tuple(LABELS) != PAINT_ROWS or '04_letter_crosses' in PAINT_ROWS:
        raise ValueError('The letter banner is not a panel row')
    painted = []
    images = []
    for name in PAINT_ROWS:
        row = paint_row(name, SOURCES[name])
        images.append(row.pop('picture'))
        still = args.out_dir / f'{name}.jpg'
        phone = args.out_dir / f'{name}_168.jpg'
        save_still(images[-1], still, phone)
        row['still'] = str(still)
        row['phone_still'] = str(phone)
        painted.append(row)
        print(f'{name}: panel behind {row["label"]} mae {row["alignment_mae"]}', flush=True)
    recipe.write_new(args.evidence, {
        'job': 'J2242',
        'status': 'TITLE_PANELS_ON_STILLS',
        'note_resolved': False,
        'frame_2869': 'out',
        'letter_row': '04_letter_crosses stays the cream-letter replacement, which has no banner',
        'rows': painted,
        'umber': list(UMBER),
        'border': False,
        'gold_rule': False,
        'pill_chrome': False,
        'master_created': False,
        'final_film_approval': False,
        'still_check': 'one still per title, including 168x94; not a motion review or an audio review',
        'packet_mux': 'OUTSTANDING',
    })


if __name__ == '__main__':
    main()
