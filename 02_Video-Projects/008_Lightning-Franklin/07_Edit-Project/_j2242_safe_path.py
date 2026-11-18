"""Composite SAFE PATH DOWN onto the v12 card frames that are already on screen.

Master frames 11038–11117 match body.mp4 in the upper 1920×720 band with
per-pixel MSE 0. The schedule is monotonic. It holds body frame 44 once and
frame 48 twice, and it does not use body frames 45, 49 or 50. The original
code-graphic files are not this plate. No master is written.
"""
import argparse
import json
import subprocess
from fractions import Fraction
from pathlib import Path

import numpy as np

import _build_rough_v13_recipe as recipe
from _j2242_ambiguous_fullres import _decode, rank_upper_band, same_picture
from _j2242_caption_composites import source_graph
from _j2242_caption_layers import clock_expression
from _j2242_salon_patch import pixel_hashes

FRAME_IN = 11038
FRAME_COUNT = 80
BODY_SHA = '5a00e3dcaaadfe3bdcdce7a0851a12fdf45637e78055d86c481e460bc8a1af3c'
BODY_FRAMES = 208
# 0..44, a second 44, 46..48 with 48 held twice more, then 51..79.
BODY_INDICES = (*range(45), 44, 46, 47, 48, 48, 48, *range(51, 80))
UNUSED_BODY_FRAMES = (45, 49, 50)
MIN_MARGIN = 0.1


def accept_safe_path(ranked):
    """Return the pinned body schedule only when every frame is that exact picture."""
    if len(BODY_INDICES) != FRAME_COUNT:
        raise ValueError('Pinned SAFE PATH schedule is not 80 frames')
    if len(ranked) != FRAME_COUNT:
        raise ValueError('SAFE PATH is 80 frames')
    indices = []
    for i, item in enumerate(ranked):
        best = item.get('best')
        if type(best) is not int or isinstance(best, bool) or best < 0:
            raise ValueError('Invalid body index')
        if item.get('best_mse') != 0:
            raise ValueError(f'SAFE PATH local {i} is not an exact body match')
        if best != BODY_INDICES[i]:
            raise ValueError(f'SAFE PATH local {i} is not body source {BODY_INDICES[i]}')
        if best in UNUSED_BODY_FRAMES:
            raise ValueError(f'Body frame {best} stays unused')
        if item.get('margin', 0) < MIN_MARGIN and item.get('same_picture') is not True:
            raise ValueError(f'SAFE PATH local {i} near-tie is a different picture')
        indices.append(best)
    if any(b < a for a, b in zip(indices, indices[1:])):
        raise ValueError('SAFE PATH schedule goes backward')
    return indices


def _with_same_picture(ranked, body):
    """Mark a weak runner-up only when it is the same picture as the exact frame."""
    marked = []
    for item in ranked:
        row = dict(item)
        if row['margin'] < MIN_MARGIN:
            pair = float(np.mean(
                (body[row['best']].astype(np.float32) - body[row['second']].astype(np.float32)) ** 2))
            row['pair_mse'] = pair
            row['same_picture'] = same_picture(pair)
        marked.append(row)
    return marked


def measure(master, body, scratch):
    """Score the 80 caption frames against the whole v12 card."""
    scratch = Path(scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    recipe.require_hash(master, recipe.MASTER_SHA, recipe.MASTER_BYTES)
    recipe.require_hash(body, BODY_SHA)
    master_raw = _decode(
        master, scratch / 'master_upper.raw', FRAME_COUNT,
        f"select='between(n,{FRAME_IN},{FRAME_IN + FRAME_COUNT - 1})'")
    body_raw = _decode(body, scratch / 'body_upper.raw', BODY_FRAMES)
    ranked = rank_upper_band(np.asarray(master_raw), np.asarray(body_raw))
    recipe.require_hash(master, recipe.MASTER_SHA, recipe.MASTER_BYTES)
    recipe.require_hash(body, BODY_SHA)
    return _with_same_picture(ranked, np.asarray(body_raw))


def _card(cards):
    selected = [card for card in cards
                if card.get('row') == '11_safe_path' and card.get('label') == 'SAFE PATH DOWN'
                and card.get('frame_in') == FRAME_IN and card.get('frame_count') == FRAME_COUNT
                and card.get('word_count') == 3 and card.get('static_hold_s') == '10/3']
    if len(selected) != 1:
        raise ValueError('SAFE PATH DOWN card changed')
    return selected[0]


def _visible_caption(layer, count):
    values = subprocess.check_output([
        'ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-i', str(layer),
        '-frames:v', str(count), '-vf', 'alphaextract,crop=1:1:800:80',
        '-an', '-fps_mode', 'passthrough', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'])
    if len(values) != count:
        raise ValueError('SAFE PATH alpha count differs')
    return [bool(value) for value in values]


def render_safe_path(indices, timeline, card, body, out):
    """Composite the existing layer onto the measured body frames. No master is written."""
    frames = recipe.as_frame_dicts(timeline['frames'])[FRAME_IN:FRAME_IN + FRAME_COUNT]
    if timeline.get('time_base') != '1/12288' or len(frames) != FRAME_COUNT:
        raise ValueError('SAFE PATH clock missing')
    if any(frame['index'] != FRAME_IN + i for i, frame in enumerate(frames)):
        raise ValueError('SAFE PATH clock is out of order')
    if list(indices) != list(BODY_INDICES):
        raise ValueError('SAFE PATH schedule changed')
    recipe.require_hash(body, BODY_SHA)
    recipe.require_hash(card['layer_path'], card['layer_sha256'])
    recipe.require_hash(card['original_clock_path'], card['original_clock_sha256'])
    clock = json.loads(Path(card['original_clock_path']).read_text())
    if clock.get('time_base') != '1/12288' or clock.get('frames') != frames:
        raise ValueError('SAFE PATH layer clock differs from the master timeline')
    native = recipe.probe_video(body)
    if len(native['frames']) != BODY_FRAMES or max(indices) >= BODY_FRAMES:
        raise ValueError('Body card is not the measured 208-frame plate')
    tb = Fraction(native['time_base'])
    selected = [native['frames'][i] for i in indices]
    if any(frame['pts'] * tb != Fraction(i, 24) or frame['duration'] * tb != Fraction(1, 24)
           for i, frame in zip(indices, selected)):
        raise ValueError('Selected body frames are not native 24fps')
    visible = _visible_caption(card['layer_path'], FRAME_COUNT)
    if visible[0] or not any(visible[1:]):
        raise ValueError('SAFE PATH fade does not start clear and then appear')
    out.mkdir(exist_ok=False)
    base = 'scale=1920:1080:flags=lanczos,setsar=1,format=yuv420p'
    graph = [
        source_graph(list(indices)),
        f"[ordered]{base},settb=1/12288,setpts='{clock_expression(frames)}'[base]",
        '[base][1:v]overlay=x=0:y=720:eof_action=pass:repeatlast=0:shortest=1:format=yuv420[out]',
    ]
    video = out / 'safe_path.nut'
    subprocess.run([
        'ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-copyts',
        '-i', str(body), '-i', card['layer_path'],
        '-filter_complex', ';'.join(graph), '-map', '[out]', '-an',
        '-c:v', 'ffv1', '-level', '3', '-threads', '4', '-fps_mode', 'passthrough',
        '-enc_time_base', '1/12288', '-avoid_negative_ts', 'disabled', '-n', str(video),
    ], check=True)
    actual = recipe.probe_video(video, FRAME_COUNT)
    ratio = Fraction(actual['time_base']) / Fraction('1/12288')
    if [frame['pts'] * ratio for frame in actual['frames']] != [frame['pts'] for frame in frames]:
        raise ValueError('SAFE PATH changed original PTS')
    duration_match = [frame['duration'] * ratio for frame in actual['frames']] == [frame['duration'] for frame in frames]
    clean = pixel_hashes(body, base)
    expected = [clean[i] for i in indices]
    measured = pixel_hashes(video)
    if len(measured) != FRAME_COUNT:
        raise ValueError('SAFE PATH frame count differs')
    upper = pixel_hashes(body, base + ',crop=1920:720:0:0')
    if pixel_hashes(video, 'crop=1920:720:0:0') != [upper[i] for i in indices]:
        raise ValueError('Picture above the SAFE PATH caption differs')
    for i, shown in enumerate(visible):
        if shown and measured[i] == expected[i]:
            raise ValueError(f'SAFE PATH is missing on frame {i}')
        if not shown and measured[i] != expected[i]:
            raise ValueError(f'SAFE PATH changes a still-clear frame {i}')
    recipe.require_hash(body, BODY_SHA)
    recipe.require_hash(card['layer_path'], card['layer_sha256'])
    clock_path = out / 'original_clock.json'
    recipe.write_new(clock_path, {'time_base': '1/12288', 'frames': frames})
    result = {
        'job': 'J2242',
        'status': 'SAFE_PATH_INTERMEDIATE_ONLY',
        'path': str(video),
        'sha256': recipe.sha256_file(video),
        'timeline_frames': [FRAME_IN, FRAME_IN + FRAME_COUNT - 1],
        'source_frame_indices': list(indices),
        'unused_body_frames': list(UNUSED_BODY_FRAMES),
        'source_sha256': BODY_SHA,
        'frame_count': FRAME_COUNT,
        'label': 'SAFE PATH DOWN',
        'visible_caption_local_frames': [i for i, shown in enumerate(visible) if shown],
        'original_pts_match': True,
        'original_durations_preserved_in_intermediate': duration_match,
        'original_clock_path': str(clock_path),
        'original_clock_sha256': recipe.sha256_file(clock_path),
        'above_caption_band_pixel_hashes_match': True,
        'code_graphic_files_used': False,
        'frame_2869': 'out',
        'master_created': False,
        'final_film_approval': False,
    }
    recipe.write_new(out / 'RESULT.json', result)
    print('SAFE PATH DOWN', FRAME_COUNT, 'frames verified', flush=True)
    return result


def _ranked_record(ranked):
    return [{
        'best': item['best'],
        'second': item['second'],
        'best_mse': item['best_mse'],
        'margin': item['margin'],
        'same_picture': item.get('same_picture'),
    } for item in ranked]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--body', type=Path, required=True)
    parser.add_argument('--timeline', type=Path, required=True)
    parser.add_argument('--master', type=Path, default=recipe.DEFAULT_MASTER)
    parser.add_argument('--scratch', type=Path, required=True)
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    args = parser.parse_args()
    ranked = measure(args.master, args.body, args.scratch)
    indices = accept_safe_path(ranked)
    root = recipe.EDIT_DIR.parents[2] / 'jobs/reviews/J2242'
    preflight = json.loads((root / 'SOURCE_PREFLIGHT.json').read_text())
    clock_sha = preflight['evidence_files']['source_timeline.json']['sha256']
    recipe.require_hash(args.timeline, clock_sha)
    timeline = json.loads(args.timeline.read_text())
    card = _card(json.loads((root / 'CAPTION_LAYERS.json').read_text())['cards'])
    result = render_safe_path(indices, timeline, card, args.body, args.out_dir)
    recipe.require_hash(args.timeline, clock_sha)
    recipe.write_new(args.evidence, {
        'job': 'J2242',
        'status': 'SAFE_PATH_ON_V12_CARD',
        'comparison': 'full-resolution upper 1920x720 after lanczos scale',
        'acceptance': {
            'maximum_per_pixel_mse': 0,
            'weak_runner_up_must_be_the_same_picture': True,
            'body_sha256': BODY_SHA,
            'unused_body_frames': list(UNUSED_BODY_FRAMES),
            'code_graphic_files': 'unused',
        },
        'body': _ranked_record(ranked),
        'render': result,
        'frame_2869': 'out',
        'foil_frame_3353': 'outstanding',
        'master_created': False,
        'final_film_approval': False,
    })
    print(json.dumps({'status': result['status'], 'sha256': result['sha256']}))


if __name__ == '__main__':
    main()
