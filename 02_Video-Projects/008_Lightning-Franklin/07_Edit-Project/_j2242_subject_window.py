"""Confirm a near-tie only when a pre-declared centre window agrees.

The window is the central half of the 1920×720 upper band: x=480, y=180,
960×360. It was fixed before these scores were read. A near-tie is confirmed
only when that window's error on the existing full-band winner is at most 9
and beats the recorded runner-up by at least 0.1. The runner-up is never
adopted. One caption row renders only when every one of its weak frames
confirms. This does not make a master or approve the film.
"""
import argparse
import json
from pathlib import Path

import numpy as np

import _build_rough_v13_recipe as recipe
from _j2242_caption_composites import render

W, H = 1920, 720
WINDOW = (480, 180, 960, 360)
MAX_MSE = 9.0
MIN_MARGIN = 0.1


def confirm_subject_window(best_mse, runner_mse, max_mse=MAX_MSE, min_margin=MIN_MARGIN):
    """True only when the existing winner still wins on the centre window.

    A window that prefers the runner-up returns False. The caller must not
    switch to that other source frame.
    """
    if type(best_mse) not in (int, float) or type(runner_mse) not in (int, float):
        raise ValueError('Window MSE must be a number')
    if isinstance(best_mse, bool) or isinstance(runner_mse, bool):
        raise ValueError('Window MSE must be a number')
    if best_mse < 0 or runner_mse < 0:
        raise ValueError('Window MSE cannot be negative')
    if best_mse > max_mse or best_mse > runner_mse:
        return False
    return (runner_mse - best_mse) >= min_margin


def _weak(frames, max_mse=MAX_MSE, min_margin=MIN_MARGIN):
    weak = []
    for i, frame in enumerate(frames):
        if frame.get('local_index') != i:
            raise ValueError('Measured frames are out of order')
        if frame.get('best_mse', max_mse + 1) > max_mse or frame.get('margin', 0) < min_margin:
            weak.append(i)
    return weak


def royal_schedule(fullres_row, mapping_row, measurements):
    """Royal Society source indices, only when both weak frames confirm."""
    if fullres_row.get('row') != '14_royal_society' or mapping_row.get('row') != '14_royal_society':
        raise ValueError('Wrong row')
    if fullres_row.get('timeline_frames') != [9303, 9429] or mapping_row.get('timeline_frames') != [9303, 9429]:
        raise ValueError('Royal window changed')
    if fullres_row.get('source_sha256') != mapping_row.get('source_sha256'):
        raise ValueError('Royal source hash differs')
    frames = fullres_row.get('frames') or []
    if len(frames) != 127 or _weak(frames) != [1, 29]:
        raise ValueError('Royal weak frames changed')
    by_local = {}
    for item in measurements:
        if item.get('row') != '14_royal_society':
            continue
        local = item.get('local_index')
        if type(local) is not int or isinstance(local, bool) or local in by_local:
            raise ValueError('Duplicate or invalid royal window measurement')
        by_local[local] = item
    if set(by_local) != {1, 29}:
        raise ValueError('Royal window measurements must be exactly the two weak frames')
    for local in (1, 29):
        frame = frames[local]
        item = by_local[local]
        if item.get('fullres_best') != frame.get('fullres_best') or item.get('fullres_second') != frame.get('fullres_second'):
            raise ValueError('Window measurement does not name the recorded candidates')
        if item.get('master_frame') != frame.get('master_frame'):
            raise ValueError('Window measurement is on a different master frame')
        if not confirm_subject_window(item['window_best_mse'], item['window_runner_mse']):
            raise ValueError(f'Royal local {local} is not confirmed')
    indices = []
    for frame in frames:
        best = frame.get('fullres_best')
        if type(best) is not int or isinstance(best, bool) or best < 0:
            raise ValueError('Invalid full-resolution index')
        indices.append(best)
    if any(b < a for a, b in zip(indices, indices[1:])):
        raise ValueError('Backward royal schedule')
    row = dict(mapping_row)
    row['source_frame_indices'] = indices
    row['subject_window_confirmed_local_frames'] = [1, 29]
    return row


def _band_mse(master, source):
    return float(np.mean((master.astype(np.float32) - source.astype(np.float32)) ** 2))


def _window_mse(master, source):
    x, y, w, h = WINDOW
    return _band_mse(master[y:y + h, x:x + w], source[y:y + h, x:x + w])


def _memmap(path, count):
    path = Path(path)
    expected = count * H * W
    if path.stat().st_size != expected:
        raise ValueError(f'{path.name} has {path.stat().st_size} bytes, expected {expected}')
    return np.memmap(path, dtype=np.uint8, mode='r', shape=(count, H, W))


def _master_offsets(document):
    offset = 0
    offsets = {}
    for row in document['rows']:
        lo, hi = row['timeline_frames']
        count = hi - lo + 1
        if count != len(row.get('frames') or []):
            raise ValueError(f'{row["row"]} frame count differs from its window')
        offsets[row['row']] = offset
        offset += count
    return offsets, offset


def measure_document(document, scratch):
    """Score every near-tie whose full-band error is already within 9."""
    scratch = Path(scratch)
    offsets, total = _master_offsets(document)
    master = _memmap(scratch / 'master_upper.raw', total)
    sources = {}
    measured = []
    for row in document['rows']:
        frames = row['frames']
        near = [frame for frame in frames if frame['best_mse'] <= MAX_MSE and frame['margin'] < MIN_MARGIN]
        if not near:
            continue
        source_path = scratch / f'{row["row"]}_source.raw'
        count = source_path.stat().st_size // (H * W)
        source = _memmap(source_path, count)
        sources[row['row']] = count
        base = offsets[row['row']]
        for frame in near:
            local = frame['local_index']
            if frame['master_frame'] != row['timeline_frames'][0] + local:
                raise ValueError('Near-tie master frame is out of order')
            best = frame['fullres_best']
            second = frame['fullres_second']
            if best >= count or second >= count:
                raise ValueError('Near-tie source index is outside the decoded plate')
            image = master[base + local]
            full = _band_mse(image, source[best])
            if abs(full - frame['best_mse']) > 1e-3:
                raise ValueError(f'{row["row"]} local {local} does not match the recorded full-band error')
            window_best = _window_mse(image, source[best])
            window_runner = _window_mse(image, source[second])
            measured.append({
                'row': row['row'],
                'master_frame': frame['master_frame'],
                'local_index': local,
                'fullres_best': best,
                'fullres_second': second,
                'full_band_best_mse': full,
                'window_best_mse': window_best,
                'window_runner_mse': window_runner,
                'confirmed': confirm_subject_window(window_best, window_runner),
            })
    return measured


def _load_row(document, name):
    found = [row for row in document['rows'] if row['row'] == name]
    if len(found) != 1:
        raise ValueError(f'Missing row {name}')
    return found[0]


def _evidence(measurements):
    confirmed = [item for item in measurements if item['confirmed']]
    return {
        'job': 'J2242',
        'status': 'SUBJECT_WINDOW_NEAR_TIE_CHECK',
        'window': {'x': WINDOW[0], 'y': WINDOW[1], 'width': WINDOW[2], 'height': WINDOW[3]},
        'rule': (
            'Confirm the existing full-band winner only. Centre-window per-pixel MSE '
            'must be at most 9 and at least 0.1 under the runner-up. Never switch candidates.'
        ),
        'pair_count': len(measurements),
        'confirmed_count': len(confirmed),
        'pairs': measurements,
        'eligible_rows': ['14_royal_society'] if _royal_ready(measurements) else [],
        'master_created': False,
        'final_film_approval': False,
    }


def _royal_ready(measurements):
    royal = [item for item in measurements if item['row'] == '14_royal_society']
    return len(royal) == 2 and all(item['confirmed'] for item in royal)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--three', type=Path, required=True)
    parser.add_argument('--ambiguous', type=Path, required=True)
    parser.add_argument('--three-scratch', type=Path, required=True)
    parser.add_argument('--ambiguous-scratch', type=Path, required=True)
    parser.add_argument('--mapping', type=Path, required=True)
    parser.add_argument('--timeline', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--out-dir', type=Path)
    args = parser.parse_args()
    three = json.loads(args.three.read_text())
    ambiguous = json.loads(args.ambiguous.read_text())
    if three.get('status') != 'FULLRES_UPPER_BAND_MAPPING_ONLY':
        raise ValueError('Three-row file is not full-resolution mapping evidence')
    if ambiguous.get('status') != 'FULLRES_UPPER_BAND_MAPPING_ONLY':
        raise ValueError('Ambiguous file is not full-resolution mapping evidence')
    measurements = measure_document(three, args.three_scratch)
    measurements += measure_document(ambiguous, args.ambiguous_scratch)
    payload = _evidence(measurements)
    recipe.write_new(args.evidence, payload)
    print('near-ties', payload['pair_count'], 'confirmed', payload['confirmed_count'], flush=True)
    if args.out_dir is None:
        return
    if payload['eligible_rows'] != ['14_royal_society']:
        raise ValueError('Royal Society did not confirm; nothing is rendered')
    mapping = json.loads(args.mapping.read_text())
    if mapping.get('master_sha256') != recipe.MASTER_SHA:
        raise ValueError('Mapping was made against a different master')
    root = recipe.EDIT_DIR.parents[2] / 'jobs/reviews/J2242'
    preflight = json.loads((root / 'SOURCE_PREFLIGHT.json').read_text())
    clock_sha = preflight['evidence_files']['source_timeline.json']['sha256']
    recipe.require_hash(args.timeline, clock_sha)
    timeline = json.loads(args.timeline.read_text())
    prepared = royal_schedule(_load_row(ambiguous, '14_royal_society'), _load_row(mapping, '14_royal_society'), measurements)
    cards = json.loads((root / 'CAPTION_LAYERS.json').read_text())['cards']
    result = render(
        prepared, timeline, cards, args.out_dir,
        'Centre-window confirmation of the two Royal Society near-ties. '
        'The existing full-band winner is kept. Not a motion review, audio review, or film approval.')
    recipe.require_hash(args.timeline, clock_sha)
    print(result['row'], result['sha256'], flush=True)


if __name__ == '__main__':
    main()
