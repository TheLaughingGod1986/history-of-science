"""Caption rows whose near-ties are different pictures.

The full-band winner and the runner-up stay unused on a near-tie. The frame
repeats the nearest unique source frame that is outside that pair: the
previous one when it qualifies, otherwise the next one. A pair with no such
neighbour is refused. This does not make a master or approve the film.
"""
import argparse
import json
from pathlib import Path

import _build_rough_v13_recipe as recipe
from _j2242_caption_composites import render

MAX_MSE = 9.0
MIN_MARGIN = 0.1


def _unique(frame):
    return frame.get('best_mse', MAX_MSE + 1) <= MAX_MSE and frame.get('margin', 0) >= MIN_MARGIN


def _index(frame, key):
    value = frame.get(key)
    if type(value) is not int or isinstance(value, bool) or value < 0:
        raise ValueError(f'Invalid {key}')
    return value


def _outside_neighbour(frames, index, winner, runner):
    """Nearest unique source index that is neither candidate, or None."""
    for step in (-1, 1):
        cursor = index + step
        while 0 <= cursor < len(frames):
            if _unique(frames[cursor]):
                candidate = _index(frames[cursor], 'fullres_best')
                if candidate != winner and candidate != runner:
                    return candidate
                break
            cursor += step
    return None


def outside_hold(frames):
    """Return source indices and the local frames that repeat an outside picture.

    Unique frames keep their full-resolution winner. A near-tie repeats an
    adjacent unique frame from outside its own pair. The schedule must stay
    monotonic.
    """
    if not frames:
        raise ValueError('No frames')
    indices = []
    holds = {}
    for i, frame in enumerate(frames):
        if frame.get('local_index') != i:
            raise ValueError('Measured frames are out of order')
        winner = _index(frame, 'fullres_best')
        runner = _index(frame, 'fullres_second')
        if _unique(frame):
            indices.append(winner)
            continue
        held = _outside_neighbour(frames, i, winner, runner)
        if held is None:
            raise ValueError(f'Local {i} has no unique source frame outside the near-tie pair')
        indices.append(held)
        holds[i] = held
    if any(b < a for a, b in zip(indices, indices[1:])):
        raise ValueError('Outside hold is backward')
    return indices, holds


def _prepare(fullres, mapping, name, timeline, expected_holds):
    if fullres.get('row') != name or mapping.get('row') != name:
        raise ValueError(f'Wrong {name} row')
    if fullres.get('timeline_frames') != timeline or mapping.get('timeline_frames') != timeline:
        raise ValueError(f'{name} window changed')
    if fullres.get('source_sha256') != mapping.get('source_sha256'):
        raise ValueError(f'{name} source hash differs')
    frames = fullres.get('frames') or []
    lo, hi = timeline
    if len(frames) != hi - lo + 1:
        raise ValueError(f'{name} frame count changed')
    indices, holds = outside_hold(frames)
    if holds != expected_holds:
        raise ValueError(f'{name} outside holds changed')
    for local, held in holds.items():
        frame = frames[local]
        if held in (frame['fullres_best'], frame['fullres_second']):
            raise ValueError(f'{name} local {local} adopted a near-tie candidate')
    row = dict(mapping)
    row['source_frame_indices'] = indices
    row['outside_hold_local_frames'] = holds
    row['poor_match_local_frames'] = []
    row['ambiguous_local_frames'] = []
    row['nonmonotonic_steps'] = []
    return row


def sentry_row(fullres, mapping):
    """Whole sentry row. Local 2 repeats source 0, not source 2 or 1."""
    return _prepare(fullres, mapping, '02_sentry_box', [4671, 4820], {2: 0})


def knuckle_row(fullres, mapping):
    """Whole knuckle row. Local 29 repeats source 30, not source 29 or 28."""
    return _prepare(fullres, mapping, '02_knuckle_spark', [7748, 7836], {29: 30})


def tower_opening(fullres, mapping):
    """THE ANSWER IS only. The ON THE ROOF span is already a separate intermediate."""
    row = _prepare(fullres, mapping, '02_tower_tilt', [272, 422], {2: 0, 3: 0, 6: 4})
    indices = row['source_frame_indices']
    if indices[74] != 74 or indices[75] != 75:
        raise ValueError('Tower opening does not meet the rendered roof span')
    row['timeline_frames'] = [272, 346]
    row['source_frame_indices'] = indices[:75]
    row['outside_hold_local_frames'] = {2: 0, 3: 0, 6: 4}
    return row


def _load(document, name):
    found = [row for row in document['rows'] if row['row'] == name]
    if len(found) != 1:
        raise ValueError(f'Missing row {name}')
    return found[0]


def _one_card(cards, name, lo, hi, label):
    selected = [card for card in cards
                if card['row'] == name and card['frame_in'] == lo and card['frame_last'] == hi
                and card['label'] == label]
    if len(selected) != 1:
        raise ValueError(f'Missing caption card {label}')
    return selected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--three', type=Path, required=True)
    parser.add_argument('--ambiguous', type=Path, required=True)
    parser.add_argument('--mapping', type=Path, required=True)
    parser.add_argument('--timeline', type=Path, required=True)
    parser.add_argument('--out-dir', type=Path, required=True)
    args = parser.parse_args()
    three = json.loads(args.three.read_text())
    ambiguous = json.loads(args.ambiguous.read_text())
    mapping = json.loads(args.mapping.read_text())
    if three.get('status') != 'FULLRES_UPPER_BAND_MAPPING_ONLY':
        raise ValueError('Three-row file is not full-resolution mapping evidence')
    if ambiguous.get('status') != 'FULLRES_UPPER_BAND_MAPPING_ONLY':
        raise ValueError('Ambiguous file is not full-resolution mapping evidence')
    if mapping.get('master_sha256') != recipe.MASTER_SHA:
        raise ValueError('Mapping was made against a different master')
    root = recipe.EDIT_DIR.parents[2] / 'jobs/reviews/J2242'
    preflight = json.loads((root / 'SOURCE_PREFLIGHT.json').read_text())
    clock_sha = preflight['evidence_files']['source_timeline.json']['sha256']
    recipe.require_hash(args.timeline, clock_sha)
    timeline = json.loads(args.timeline.read_text())
    cards = json.loads((root / 'CAPTION_LAYERS.json').read_text())['cards']
    prepared = [
        (sentry_row(_load(three, '02_sentry_box'), _load(mapping, '02_sentry_box')),
         _one_card(cards, '02_sentry_box', 4671, 4766, 'THE SENTRY-BOX'),
         'Local 2 repeats source 0. Sources 1 and 2 stay unused.'),
        (knuckle_row(_load(ambiguous, '02_knuckle_spark'), _load(mapping, '02_knuckle_spark')),
         _one_card(cards, '02_knuckle_spark', 7748, 7836, 'A SPARK'),
         'Local 29 repeats source 30. Sources 28 and 29 stay unused.'),
        (tower_opening(_load(three, '02_tower_tilt'), _load(mapping, '02_tower_tilt')),
         _one_card(cards, '02_tower_tilt', 272, 346, 'THE ANSWER IS'),
         'Locals 2, 3 and 6 repeat source 0 or 4. The contested source frames stay unused.'),
    ]
    args.out_dir.mkdir(exist_ok=False)
    results = []
    for row, selected, note in prepared:
        results.append(render(row, timeline, selected, args.out_dir / row['row'], note))
    recipe.require_hash(args.timeline, clock_sha)
    recipe.write_new(args.out_dir / 'RESULT.json', {
        'job': 'J2242',
        'status': 'OUTSIDE_HOLD_CAPTION_INTERMEDIATES',
        'rule': (
            'On a near-tie, repeat the nearest unique source frame that is neither '
            'the full-band winner nor the runner-up. Never adopt either candidate.'
        ),
        'rows': results,
        'still_out': [
            '04_franklin_watches frames 2865-2887',
            'table lead-in frames 423-426',
            'SAFE PATH DOWN',
            'foil check at frame 3353',
        ],
        'master_created': False,
        'final_film_approval': False,
    })
    print('outside-hold captions verified', flush=True)


if __name__ == '__main__':
    main()
