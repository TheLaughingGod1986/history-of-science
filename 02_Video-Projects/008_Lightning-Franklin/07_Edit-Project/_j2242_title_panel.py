"""Put an unbordered umber panel behind the picture titles that stay.

Five code-graphic titles sit on a moving picture with no panel. The letter
row is the cream-letter replacement, which has no banner and no boxes, so
it is not painted here. The other four keep their words. The panel is the
caption umber, with no border, gold rule or pill. Frame 2869 stays out.
`--every-frame` paints each frame of those four rows where the title is
actually aligned, and writes a lossless intermediate. It does not write a
master. The still path remains one frame per title.
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
PICTURE_FPS = 24
ALPHA_FPS = 30
# Master frames whose clock interval is inside 10_metal_easy. 11038 is the
# safe-path frame (clock 461.0473), so the window stops before it.
METAL_FRAME_FIRST = 10996
METAL_FRAME_STOP = 11038
METAL_CHECK_FRAME = 11017
METAL_ALPHA_SEEK = '1.5'
EXPECTED_PICTURE_FRAMES = {
    '15_likeness_fire': 114,
    '06_same_thing': 160,
    '08_looking_path': 76,
}
EXPECTED_ALPHA_FRAMES = {
    '15_likeness_fire': 159,
    '06_same_thing': 219,
    '08_looking_path': 95,
    '10_metal_easy': 90,
}
# Picture-frame index of the still that was already checked.
CHECK_INDEX = {
    '15_likeness_fire': 53,
    '06_same_thing': 134,
    '08_looking_path': 48,
    '10_metal_easy': METAL_CHECK_FRAME - METAL_FRAME_FIRST,
}

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


def metal_frames():
    """The 42 master frames of the metal row, excluding the safe-path frame."""
    frames = tuple(range(METAL_FRAME_FIRST, METAL_FRAME_STOP))
    if len(frames) != 42:
        raise ValueError(f'Metal row is {len(frames)} frames, expected 42')
    if METAL_CHECK_FRAME not in frames or METAL_FRAME_STOP in frames or 2869 in frames:
        raise ValueError('Metal window includes the safe path or frame 2869')
    if frames[CHECK_INDEX['10_metal_easy']] != METAL_CHECK_FRAME:
        raise ValueError('Metal check frame is not master frame 11017')
    return frames


def alpha_frame_for_picture(picture_index, picture_count, alpha_count,
                            picture_fps=PICTURE_FPS, alpha_fps=ALPHA_FPS):
    """Return the alpha frame nearest this picture frame's timestamp."""
    if picture_count < 1 or alpha_count < 1:
        raise ValueError('A row needs picture frames and alpha frames')
    if not 0 <= int(picture_index) < picture_count:
        raise ValueError(f'Picture frame {picture_index} is outside 0..{picture_count - 1}')
    index = int(round(int(picture_index) * alpha_fps / picture_fps))
    if not 0 <= index < alpha_count:
        raise ValueError(f'Alpha frame {index} is outside 0..{alpha_count - 1}')
    return index


def paint_matched(picture, alpha):
    """Paint when one title line is aligned. Otherwise keep the picture."""
    if getattr(picture, 'shape', None) != (H, W, 3) or getattr(alpha, 'shape', None) != (H, W, 4):
        raise ValueError('Expected a 1920x1080 picture and alpha frame')
    try:
        box = title_box(alpha)
    except ValueError:
        return picture, {'status': 'kept', 'why': 'no title'}
    glyphs = alpha[:, :, 3] > 0
    try:
        mae = alignment_mae(picture, alpha, glyphs)
    except ValueError as exc:
        return picture, {'status': 'kept', 'why': str(exc)}
    if mae > ALIGN_MAE_MAX:
        return picture, {'status': 'kept', 'why': 'unaligned', 'alignment_mae': round(float(mae), 3)}
    painted = panel_behind(picture, box, glyphs)
    return painted, {
        'status': 'painted',
        'box': [int(v) for v in box],
        'alignment_mae': round(float(mae), 3),
        'glyph_pixels': int(glyphs[box[1]:box[3] + 1, box[0]:box[2] + 1].sum()),
    }


def summarize_frames(statuses):
    """Require one stable title box and at least one painted frame."""
    if not statuses:
        raise ValueError('A row has no frames')
    painted = [row for row in statuses if row['status'] == 'painted']
    if not painted:
        raise ValueError('A picture row needs at least one painted frame')
    boxes = {tuple(row['box']) for row in painted}
    if len(boxes) != 1:
        raise ValueError(f'Title box moved across the row: {sorted(boxes)}')
    kept = [row for row in statuses if row['status'] != 'painted']
    if any(row['status'] not in ('painted', 'kept') for row in statuses):
        raise ValueError('Unknown frame status')
    return {
        'frames': len(statuses),
        'painted': len(painted),
        'kept': len(kept),
        'box': list(painted[0]['box']),
        'mae_min': min(row['alignment_mae'] for row in painted),
        'mae_max': max(row['alignment_mae'] for row in painted),
        'kept_reasons': {
            why: sum(1 for row in kept if row.get('why') == why)
            for why in sorted({row.get('why') for row in kept})
        },
    }


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


def decode_all(path, pix_fmt, channels, raw_path, select=None):
    """Decode every selected frame into a read-only array."""
    raw_path = Path(raw_path)
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    if raw_path.exists():
        raise FileExistsError(raw_path)
    command = ['ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-i', str(path), '-an']
    if select is not None:
        command += ['-vf', f"select='{select}',format={pix_fmt}", '-fps_mode', 'passthrough']
    command += ['-f', 'rawvideo', '-pix_fmt', pix_fmt, str(raw_path)]
    subprocess.run(command, check=True)
    frame_bytes = W * H * channels
    size = raw_path.stat().st_size
    if size < frame_bytes or size % frame_bytes:
        raise ValueError(f'{path} decoded to {size} bytes')
    count = size // frame_bytes
    return np.memmap(raw_path, dtype=np.uint8, mode='r', shape=(count, H, W, channels))


def close_map(array):
    mmap = getattr(array, '_mmap', None)
    if mmap is not None:
        mmap.close()


def write_ffv1(raw_path, dest, frame_count):
    """Write lossless RGB and prove the file decodes back to the same bytes."""
    dest = Path(dest)
    if dest.exists():
        raise FileExistsError(dest)
    subprocess.run(
        ['ffmpeg', '-nostdin', '-v', 'error', '-xerror',
         '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24',
         '-i', str(raw_path), '-frames:v', str(frame_count),
         '-c:v', 'ffv1', '-pix_fmt', 'gbrp', '-an', str(dest)],
        check=True)
    check = dest.with_suffix('.rgb')
    subprocess.run(
        ['ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-i', str(dest),
         '-f', 'rawvideo', '-pix_fmt', 'rgb24', str(check)],
        check=True)
    expected = frame_count * W * H * 3
    if check.stat().st_size != expected:
        raise ValueError(f'{dest.name} round trip is {check.stat().st_size} bytes, expected {expected}')
    if recipe.sha256_file(check) != recipe.sha256_file(raw_path):
        raise ValueError(f'{dest.name} did not round-trip')
    check.unlink()


def paint_sequence(pictures, alphas, check_index, dest):
    """Paint each picture frame from the alpha frame at the same timestamp."""
    count = int(pictures.shape[0])
    alpha_count = int(alphas.shape[0])
    if not 0 <= check_index < count:
        raise ValueError('Check frame is outside the picture')
    statuses = []
    check = None
    with Path(dest).open('wb') as handle:
        for index in range(count):
            alpha_index = alpha_frame_for_picture(index, count, alpha_count)
            image, status = paint_matched(pictures[index], alphas[alpha_index])
            status = dict(status)
            status['picture_frame'] = index
            status['alpha_frame'] = alpha_index
            if status['status'] == 'kept' and image is not pictures[index] and not np.array_equal(image, pictures[index]):
                raise ValueError(f'Frame {index} was marked kept but its pixels changed')
            if status['status'] == 'painted' and np.array_equal(image, pictures[index]):
                raise ValueError(f'Frame {index} was marked painted but its pixels did not change')
            handle.write(np.ascontiguousarray(image).tobytes())
            if index == check_index:
                check = (
                    np.array(pictures[index], copy=True),
                    np.array(image, copy=True),
                    np.array(alphas[alpha_index], copy=True),
                    status,
                )
            statuses.append(status)
    summary = summarize_frames(statuses)
    if check is None or check[3]['status'] != 'painted':
        raise ValueError('The previously checked title frame was not painted')
    source, output, alpha, status = check
    changed = np.any(output != source, axis=2)
    if not changed.any() or not np.all(output[changed] == UMBER):
        raise ValueError('The check frame changed a pixel to a colour other than umber')
    glyphs = alpha[:, :, 3] > 0
    if np.any(output[glyphs] != source[glyphs]):
        raise ValueError('The check frame changed the title glyphs')
    summary['check_frame'] = status['picture_frame']
    summary['check_alpha_frame'] = status['alpha_frame']
    summary['check_mae'] = status['alignment_mae']
    return summary, output


def paint_metal_sequence(pictures, alpha, dest):
    """Paint master frames that still match the one aligned metal title."""
    frames = metal_frames()
    if int(pictures.shape[0]) != len(frames):
        raise ValueError(f'Metal decode is {pictures.shape[0]} frames, expected {len(frames)}')
    check_index = CHECK_INDEX['10_metal_easy']
    statuses = []
    check = None
    with Path(dest).open('wb') as handle:
        for index, master_frame in enumerate(frames):
            image, status = paint_matched(pictures[index], alpha)
            status = dict(status)
            status['picture_frame'] = index
            status['master_frame'] = master_frame
            if status['status'] == 'kept' and not np.array_equal(image, pictures[index]):
                raise ValueError(f'Metal frame {master_frame} was marked kept but its pixels changed')
            if status['status'] == 'painted' and np.array_equal(image, pictures[index]):
                raise ValueError(f'Metal frame {master_frame} was marked painted but its pixels did not change')
            handle.write(np.ascontiguousarray(image).tobytes())
            if index == check_index:
                check = (np.array(pictures[index], copy=True), np.array(image, copy=True), status)
            statuses.append(status)
    if any(row.get('master_frame') == METAL_FRAME_STOP for row in statuses):
        raise ValueError('Safe-path frame 11038 was included')
    summary = summarize_frames(statuses)
    if check is None or check[2]['status'] != 'painted':
        raise ValueError('Master frame 11017 was not painted')
    source, output, status = check
    changed = np.any(output != source, axis=2)
    glyphs = alpha[:, :, 3] > 0
    if not changed.any() or not np.all(output[changed] == UMBER) or np.any(output[glyphs] != source[glyphs]):
        raise ValueError('Master frame 11017 panel is not umber behind the words')
    if abs(status['alignment_mae'] - 20.279) > 0.001:
        raise ValueError(f'Master frame 11017 MAE changed: {status["alignment_mae"]}')
    summary['check_frame'] = METAL_CHECK_FRAME
    summary['check_mae'] = status['alignment_mae']
    summary['master_frames'] = [METAL_FRAME_FIRST, METAL_FRAME_STOP - 1]
    summary['safe_path_frame_11038'] = 'out'
    return summary, output


def render_rows(out_dir, scratch, evidence):
    """Paint every aligned frame of the four picture rows. No master is written."""
    if tuple(LABELS) != PAINT_ROWS or '04_letter_crosses' in PAINT_ROWS:
        raise ValueError('The letter banner is not a panel row')
    out_dir = Path(out_dir)
    scratch = Path(scratch)
    out_dir.mkdir(parents=True, exist_ok=True)
    scratch.mkdir(parents=True, exist_ok=True)
    rows = []
    for name in PAINT_ROWS:
        if name == '10_metal_easy':
            summary = render_metal(out_dir, scratch)
        else:
            summary = render_overlay(name, out_dir, scratch)
        rows.append(summary)
        print(
            f'{name}: painted {summary["painted"]} of {summary["frames"]} '
            f'mae {summary["mae_min"]}..{summary["mae_max"]}',
            flush=True)
    recipe.write_new(evidence, {
        'job': 'J2242',
        'status': 'TITLE_PANELS_ON_EVERY_ALIGNED_FRAME',
        'note_resolved': False,
        'frame_2869': 'out',
        'letter_row': '04_letter_crosses stays the cream-letter replacement, which has no banner',
        'rows': rows,
        'umber': list(UMBER),
        'border': False,
        'gold_rule': False,
        'pill_chrome': False,
        'master_created': False,
        'final_film_approval': False,
        'motion_review': False,
        'audio_review': False,
        'packet_mux': 'OUTSTANDING',
    })


def render_overlay(name, out_dir, scratch):
    source = SOURCES[name]
    recipe.require_hash(source['picture'], source['picture_sha256'], source['picture_bytes'])
    recipe.require_hash(source['alpha'], source['alpha_sha256'], source['alpha_bytes'])
    work = scratch / name
    picture_raw = work / 'picture.raw'
    alpha_raw = work / 'alpha.raw'
    pictures = decode_all(source['picture'], 'rgb24', 3, picture_raw)
    alphas = decode_all(source['alpha'], 'rgba', 4, alpha_raw)
    try:
        if pictures.shape[0] != EXPECTED_PICTURE_FRAMES[name]:
            raise ValueError(f'{name} picture is {pictures.shape[0]} frames')
        if alphas.shape[0] != EXPECTED_ALPHA_FRAMES[name]:
            raise ValueError(f'{name} alpha is {alphas.shape[0]} frames')
        painted = work / 'painted.raw'
        summary, image = paint_sequence(pictures, alphas, CHECK_INDEX[name], painted)
    finally:
        close_map(pictures)
        close_map(alphas)
        del pictures, alphas
    dest = out_dir / f'{name}.nut'
    write_ffv1(painted, dest, summary['frames'])
    save_still(image, out_dir / f'{name}.jpg', out_dir / f'{name}_168.jpg')
    summary.update({
        'row': name,
        'label': LABELS[name],
        'words': label_words(LABELS[name]),
        'intermediate': str(dest),
        'sha256': recipe.sha256_file(dest),
        'bytes': dest.stat().st_size,
        'phone_still': str(out_dir / f'{name}_168.jpg'),
    })
    for path in (picture_raw, alpha_raw, painted):
        path.unlink(missing_ok=True)
    return summary


def render_metal(out_dir, scratch):
    source = SOURCES['10_metal_easy']
    recipe.require_hash(recipe.DEFAULT_MASTER, recipe.MASTER_SHA, recipe.MASTER_BYTES)
    recipe.require_hash(source['alpha'], source['alpha_sha256'], source['alpha_bytes'])
    alpha = decode_rgba(source['alpha'], seek=METAL_ALPHA_SEEK)
    if title_box(alpha) != (582, 87, 1331, 209):
        raise ValueError('The metal title box moved')
    work = scratch / '10_metal_easy'
    picture_raw = work / 'picture.raw'
    frames = metal_frames()
    select = '+'.join(f'eq(n,{frame})' for frame in frames)
    pictures = decode_all(recipe.DEFAULT_MASTER, 'rgb24', 3, picture_raw, select=select)
    try:
        if pictures.shape[0] != len(frames):
            raise ValueError(f'Metal master decode is {pictures.shape[0]} frames')
        painted = work / 'painted.raw'
        summary, image = paint_metal_sequence(pictures, alpha, painted)
    finally:
        close_map(pictures)
        del pictures
    dest = out_dir / '10_metal_easy.nut'
    write_ffv1(painted, dest, summary['frames'])
    save_still(image, out_dir / '10_metal_easy.jpg', out_dir / '10_metal_easy_168.jpg')
    summary.update({
        'row': '10_metal_easy',
        'label': LABELS['10_metal_easy'],
        'words': label_words(LABELS['10_metal_easy']),
        'intermediate': str(dest),
        'sha256': recipe.sha256_file(dest),
        'bytes': dest.stat().st_size,
        'phone_still': str(out_dir / '10_metal_easy_168.jpg'),
        'alpha_seek': METAL_ALPHA_SEEK,
    })
    for path in (picture_raw, painted):
        path.unlink(missing_ok=True)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--every-frame', action='store_true')
    parser.add_argument('--scratch', type=Path)
    args = parser.parse_args()
    if tuple(LABELS) != PAINT_ROWS or '04_letter_crosses' in PAINT_ROWS:
        raise ValueError('The letter banner is not a panel row')
    if args.every_frame:
        if args.scratch is None:
            parser.error('--every-frame requires --scratch')
        render_rows(args.out_dir, args.scratch, args.evidence)
        return
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
