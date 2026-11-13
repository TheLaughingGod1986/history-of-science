"""Remove the baked SAFE PATH title so the bottom card is the only label.

The v12 card draws SAFE PATH DOWN in x 640–1280, y 115–182. Frame 0 of
body.mp4 is that field before the title fades in. Later frames keep the same
field in the corners of the box and put the title in the centre. The steeple
stays outside the box. The box is widened by one luma row so a 4:2:0 sample
does not change the row above it. No master is written.
"""
import argparse
import json
import subprocess
from fractions import Fraction
from pathlib import Path

import numpy as np

import _build_rough_v13_recipe as recipe
from _j2242_caption_layers import clock_expression
from _j2242_safe_path import (
    BODY_INDICES, BODY_SHA, FRAME_COUNT, FRAME_IN, _card, _visible_caption,
)
from _j2242_salon_patch import pixel_hashes

W, H = 1920, 1080
# v12 ink is y 115–182. y 114 keeps the chroma samples inside this rectangle.
TITLE_BOX = (640, 1280, 114, 182)
INK_BOX = (640, 1280, 115, 182)
HELD_TITLE_FRAME = 28
MAX_CORNER_MSE = 4.0
MIN_TITLE_MSE = 500.0
Y_BYTES = W * H
C_BYTES = (W // 2) * (H // 2)
FRAME_BYTES = Y_BYTES + 2 * C_BYTES


def chroma_box(box):
    """Return the 4:2:0 rectangle that covers an even luma box and nothing past it."""
    x0, x1, y0, y1 = box
    if any(type(n) is not int or isinstance(n, bool) or n % 2 or n < 0 for n in box):
        raise ValueError('Title box is not a chroma-aligned rectangle')
    if x0 >= x1 or y0 >= y1:
        raise ValueError('Title box is empty')
    return (x0 // 2, x1 // 2, y0 // 2, y1 // 2)


def clear_title_box(y, u, v, donor_y, donor_u, donor_v, box=TITLE_BOX):
    """Copy the clear field into the title box. Pixels outside the box stay put."""
    x0, x1, y0, y1 = box
    cx0, cx1, cy0, cy1 = chroma_box(box)
    if y.shape != donor_y.shape or u.shape != donor_u.shape or v.shape != donor_v.shape:
        raise ValueError('Frame size changed')
    if y1 > y.shape[0] or x1 > y.shape[1] or cy1 > u.shape[0] or cx1 > u.shape[1]:
        raise ValueError('Title box is outside the frame')
    out_y, out_u, out_v = y.copy(), u.copy(), v.copy()
    out_y[y0:y1, x0:x1] = donor_y[y0:y1, x0:x1]
    out_u[cy0:cy1, cx0:cx1] = donor_u[cy0:cy1, cx0:cx1]
    out_v[cy0:cy1, cx0:cx1] = donor_v[cy0:cy1, cx0:cx1]
    return out_y, out_u, out_v


def _box_view(y, box, inset):
    x0, x1, y0, y1 = box
    view = y[y0 + inset[0]:y1 - inset[1], x0 + inset[2]:x1 - inset[3]]
    if view.size == 0:
        raise ValueError('Title sample is empty')
    return view


def field_corners(y, box=TITLE_BOX, n=8):
    view = _box_view(y, box, (0, 0, 0, 0))
    if view.shape[0] <= 2 * n or view.shape[1] <= 2 * n:
        raise ValueError('Title box is smaller than its corners')
    return np.concatenate([
        view[:n, :n].reshape(-1), view[:n, -n:].reshape(-1),
        view[-n:, :n].reshape(-1), view[-n:, -n:].reshape(-1),
    ])


def field_center(y, box=TITLE_BOX):
    """The ink sits in the middle of the box, clear of the field corners."""
    return _box_view(y, box, (16, 16, 220, 220))


def _mse(a, b):
    return float(np.mean((a.astype(np.float32) - b.astype(np.float32)) ** 2))


def same_field(donor, frames, indices, box=TITLE_BOX):
    """Accept the clear field only when the title is ink and the corners are the field."""
    if not frames or len(frames) != len(indices) or indices[0] != 0:
        raise ValueError('Clear field is body frame 0')
    donor_corners = field_corners(donor, box)
    donor_center = field_center(donor, box)
    corners, centers = [], []
    for i, (frame, source) in enumerate(zip(frames, indices)):
        corner_mse = _mse(field_corners(frame, box), donor_corners)
        center_mse = _mse(field_center(frame, box), donor_center)
        if corner_mse > MAX_CORNER_MSE:
            raise ValueError(f'Title box covers a different picture on frame {i}')
        corners.append(corner_mse)
        centers.append(center_mse)
        if source >= HELD_TITLE_FRAME and center_mse < MIN_TITLE_MSE:
            raise ValueError(f'Held frame {source} has no baked title')
    return {
        'corner_mse_max': max(corners),
        'held_title_center_mse_min': min(
            c for c, source in zip(centers, indices) if source >= HELD_TITLE_FRAME),
    }


def _planes(raw):
    if len(raw) != FRAME_BYTES:
        raise ValueError('Frame is not 1920x1080 yuv420')
    y = np.frombuffer(raw[:Y_BYTES], dtype=np.uint8).reshape(H, W).copy()
    u = np.frombuffer(raw[Y_BYTES:Y_BYTES + C_BYTES], dtype=np.uint8).reshape(H // 2, W // 2).copy()
    v = np.frombuffer(raw[Y_BYTES + C_BYTES:], dtype=np.uint8).reshape(H // 2, W // 2).copy()
    return y, u, v


def _pack(y, u, v):
    return y.tobytes() + u.tobytes() + v.tobytes()


def _outside_same(a, b, box, chroma=False):
    if chroma:
        box = chroma_box(box)
    x0, x1, y0, y1 = box
    keep = np.ones(a.shape, dtype=bool)
    keep[y0:y1, x0:x1] = False
    return np.array_equal(a[keep], b[keep])


def clear_selected(prefix, indices):
    """Return packed frames with the baked title replaced by body frame 0."""
    if len(prefix) != (max(indices) + 1) * FRAME_BYTES:
        raise ValueError('Body prefix does not cover the schedule')
    frames = [_planes(prefix[i * FRAME_BYTES:(i + 1) * FRAME_BYTES]) for i in indices]
    donor = _planes(prefix[:FRAME_BYTES])
    measured = same_field(donor[0], [frame[0] for frame in frames], indices)
    cleared = []
    for y, u, v in frames:
        out_y, out_u, out_v = clear_title_box(y, u, v, *donor)
        x0, x1, y0, y1 = TITLE_BOX
        if not (_outside_same(out_y, y, TITLE_BOX) and _outside_same(out_u, u, TITLE_BOX, True)
                and _outside_same(out_v, v, TITLE_BOX, True)):
            raise ValueError('Title clear changed the picture outside the box')
        if not np.array_equal(out_y[y0:y1, x0:x1], donor[0][y0:y1, x0:x1]):
            raise ValueError('Title box is not the clear field')
        cleared.append(_pack(out_y, out_u, out_v))
    return b''.join(cleared), measured


def _decode_prefix(path, count):
    raw = subprocess.check_output([
        'ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-i', str(path),
        '-frames:v', str(count), '-an', '-f', 'rawvideo', '-pix_fmt', 'yuv420p', 'pipe:1'])
    if len(raw) != count * FRAME_BYTES:
        raise ValueError('Body decode is short')
    return raw


def render_single_title(indices, timeline, card, body, out):
    """Composite the bottom card onto frames whose baked title has been removed."""
    frames = recipe.as_frame_dicts(timeline['frames'])[FRAME_IN:FRAME_IN + FRAME_COUNT]
    if timeline.get('time_base') != '1/12288' or list(indices) != list(BODY_INDICES):
        raise ValueError('SAFE PATH schedule changed')
    if any(frame['index'] != FRAME_IN + i for i, frame in enumerate(frames)):
        raise ValueError('SAFE PATH clock is out of order')
    recipe.require_hash(body, BODY_SHA)
    recipe.require_hash(card['layer_path'], card['layer_sha256'])
    recipe.require_hash(card['original_clock_path'], card['original_clock_sha256'])
    clock = json.loads(Path(card['original_clock_path']).read_text())
    if clock.get('frames') != frames:
        raise ValueError('SAFE PATH layer clock differs from the master timeline')
    visible = _visible_caption(card['layer_path'], FRAME_COUNT)
    if visible[0] or not any(visible[1:]):
        raise ValueError('SAFE PATH fade does not start clear and then appear')
    prefix = _decode_prefix(body, max(indices) + 1)
    cleared, measured = clear_selected(prefix, list(indices))
    out.mkdir(exist_ok=False)
    bare = out / 'title_cleared.nut'
    subprocess.run([
        'ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-f', 'rawvideo', '-pix_fmt', 'yuv420p',
        '-s', f'{W}x{H}', '-r', '24', '-i', 'pipe:0', '-frames:v', str(FRAME_COUNT), '-an',
        '-c:v', 'ffv1', '-level', '3', '-threads', '4', '-n', str(bare),
    ], input=cleared, check=True)
    if pixel_hashes(bare) != pixel_hashes_raw(cleared):
        raise ValueError('Title-cleared encode is not lossless')
    video = out / 'safe_path.nut'
    graph = (
        f"[0:v]setsar=1,format=yuv420p,settb=1/12288,setpts='{clock_expression(frames)}'[base];"
        '[base][1:v]overlay=x=0:y=720:eof_action=pass:repeatlast=0:shortest=1:format=yuv420[out]'
    )
    subprocess.run([
        'ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-copyts',
        '-i', str(bare), '-i', card['layer_path'],
        '-filter_complex', graph, '-map', '[out]', '-an',
        '-c:v', 'ffv1', '-level', '3', '-threads', '4', '-fps_mode', 'passthrough',
        '-enc_time_base', '1/12288', '-avoid_negative_ts', 'disabled', '-n', str(video),
    ], check=True)
    actual = recipe.probe_video(video, FRAME_COUNT)
    ratio = Fraction(actual['time_base']) / Fraction('1/12288')
    if [frame['pts'] * ratio for frame in actual['frames']] != [frame['pts'] for frame in frames]:
        raise ValueError('SAFE PATH changed original PTS')
    duration_match = [frame['duration'] * ratio for frame in actual['frames']] == [
        frame['duration'] for frame in frames]
    bare_upper = pixel_hashes(bare, 'crop=1920:720:0:0')
    if pixel_hashes(video, 'crop=1920:720:0:0') != bare_upper:
        raise ValueError('Bottom card changed the picture above it')
    bare_full = pixel_hashes(bare)
    full = pixel_hashes(video)
    for i, shown in enumerate(visible):
        if shown and full[i] == bare_full[i]:
            raise ValueError(f'SAFE PATH is missing on frame {i}')
        if not shown and full[i] != bare_full[i]:
            raise ValueError(f'SAFE PATH changes a still-clear frame {i}')
    recipe.require_hash(body, BODY_SHA)
    clock_path = out / 'original_clock.json'
    recipe.write_new(clock_path, {'time_base': '1/12288', 'frames': frames})
    return {
        'job': 'J2242',
        'status': 'SAFE_PATH_ONE_TITLE',
        'path': str(video),
        'sha256': recipe.sha256_file(video),
        'cleared_path': str(bare),
        'cleared_sha256': recipe.sha256_file(bare),
        'timeline_frames': [FRAME_IN, FRAME_IN + FRAME_COUNT - 1],
        'source_frame_indices': list(indices),
        'title_box': list(TITLE_BOX),
        'ink_box': list(INK_BOX),
        'field': measured,
        'label': 'SAFE PATH DOWN',
        'labels_on_screen': 1,
        'baked_title': 'removed',
        'bottom_card': 'kept',
        'visible_caption_local_frames': [i for i, shown in enumerate(visible) if shown],
        'original_pts_match': True,
        'original_durations_preserved_in_intermediate': duration_match,
        'original_clock_path': str(clock_path),
        'original_clock_sha256': recipe.sha256_file(clock_path),
        'above_caption_band_matches_cleared_field': True,
        'frame_2869': 'out',
        'master_created': False,
        'final_film_approval': False,
    }


def pixel_hashes_raw(raw):
    """Hash packed yuv420 frames without writing them, for the lossless check."""
    command = [
        'ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-f', 'rawvideo', '-pix_fmt', 'yuv420p',
        '-s', f'{W}x{H}', '-i', 'pipe:0', '-frames:v', str(len(raw) // FRAME_BYTES),
        '-an', '-c:v', 'rawvideo', '-pix_fmt', 'yuv420p', '-f', 'framehash', '-hash', 'sha256', '-',
    ]
    output = subprocess.run(command, input=raw, check=True, capture_output=True).stdout.decode()
    return [line.split(',')[-1].strip() for line in output.splitlines() if line and not line.startswith('#')]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--body', type=Path, required=True)
    parser.add_argument('--timeline', type=Path, required=True)
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    args = parser.parse_args()
    root = recipe.EDIT_DIR.parents[2] / 'jobs/reviews/J2242'
    preflight = json.loads((root / 'SOURCE_PREFLIGHT.json').read_text())
    clock_sha = preflight['evidence_files']['source_timeline.json']['sha256']
    recipe.require_hash(args.timeline, clock_sha)
    timeline = json.loads(args.timeline.read_text())
    card = _card(json.loads((root / 'CAPTION_LAYERS.json').read_text())['cards'])
    result = render_single_title(BODY_INDICES, timeline, card, args.body, args.out_dir)
    recipe.require_hash(args.timeline, clock_sha)
    recipe.write_new(args.evidence, {
        'job': 'J2242',
        'status': 'SAFE_PATH_ONE_TITLE',
        'title_box': {
            'luma': list(TITLE_BOX),
            'ink': list(INK_BOX),
            'source': 'v12 title paste, replaced with body frame 0',
            'max_corner_mse': MAX_CORNER_MSE,
            'min_held_title_mse': MIN_TITLE_MSE,
        },
        'field': result['field'],
        'render': result,
        'frame_2869': 'out',
        'foil_frame_3353': 'outstanding',
        'still_check': 'stills only; not a motion review or an audio review',
        'master_created': False,
        'final_film_approval': False,
    })
    print(json.dumps({'status': result['status'], 'sha256': result['sha256']}))


if __name__ == '__main__':
    main()
