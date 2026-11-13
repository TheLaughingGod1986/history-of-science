"""Caption spans where every full-resolution frame has one winning source frame.

Per-pixel MSE must be at most 9 and the runner-up margin at least 0.1, the
same rule as the earlier unique rows. A nearer tie stays out. This does not
lower that rule, and it does not make a master or approve the film.
"""
import json
from pathlib import Path

import _build_rough_v13_recipe as recipe
from _j2242_caption_composites import render

MAX_MSE = 9.0
MIN_MARGIN = 0.1


def _index(frame):
    """Return the winning source index, or reject a frame that is not unique."""
    best = frame.get('fullres_best')
    if type(best) is not int or isinstance(best, bool) or best < 0:
        raise ValueError('Invalid full-resolution index')
    if frame.get('best_mse', MAX_MSE + 1) > MAX_MSE or frame.get('margin', 0) < MIN_MARGIN:
        raise ValueError('Frame is not a unique full-resolution match')
    return best


def _span(frames, start, end):
    """Inclusive local indices. Every selected frame must already be unique."""
    chosen = frames[start:end + 1]
    if not chosen or len(chosen) != end - start + 1:
        raise ValueError('Span is outside the measured frames')
    if any(frame.get('local_index') != start + i for i, frame in enumerate(chosen)):
        raise ValueError('Measured frames are out of order')
    indices = [_index(frame) for frame in chosen]
    if any(b < a for a, b in zip(indices, indices[1:])):
        raise ValueError('Backward full-resolution span')
    return indices


def _near_tie(frames):
    return any(frame.get('best_mse', 0) > MAX_MSE or frame.get('margin', MIN_MARGIN) < MIN_MARGIN
               for frame in frames)


def franklin_prefix(fullres_row, mapping_row):
    """Master frames 2718–2864, source frames 0–146. The near-tie tail stays out."""
    if fullres_row.get('row') != '04_franklin_watches' or mapping_row.get('row') != '04_franklin_watches':
        raise ValueError('Wrong Franklin row')
    if fullres_row.get('timeline_frames') != [2718, 2887] or mapping_row.get('timeline_frames') != [2718, 2887]:
        raise ValueError('Franklin window changed')
    if fullres_row.get('source_sha256') != mapping_row.get('source_sha256'):
        raise ValueError('Franklin source hash differs')
    frames = fullres_row.get('frames') or []
    if len(frames) != 170:
        raise ValueError('Franklin frame count changed')
    indices = _span(frames, 0, 146)
    if indices != list(range(147)):
        raise ValueError('Franklin prefix is not source frames 0 through 146')
    if not _near_tie(frames[147:]):
        raise ValueError('Franklin tail is unique and must not be dropped silently')
    row = dict(mapping_row)
    row['timeline_frames'] = [2718, 2864]
    row['source_frame_indices'] = indices
    row['rejected_master_frames'] = [2865, 2887]
    return row


def tower_roof(fullres_row, mapping_row):
    """The ON THE ROOF card, master frames 347–422. The opening card stays out."""
    if fullres_row.get('row') != '02_tower_tilt' or mapping_row.get('row') != '02_tower_tilt':
        raise ValueError('Wrong tower row')
    if fullres_row.get('timeline_frames') != [272, 422] or mapping_row.get('timeline_frames') != [272, 422]:
        raise ValueError('Tower window changed')
    if fullres_row.get('source_sha256') != mapping_row.get('source_sha256'):
        raise ValueError('Tower source hash differs')
    frames = fullres_row.get('frames') or []
    if len(frames) != 151:
        raise ValueError('Tower frame count changed')
    indices = _span(frames, 75, 150)
    if indices != list(range(75, 151)):
        raise ValueError('Roof card is not source frames 75 through 150')
    if not _near_tie(frames[:75]):
        raise ValueError('Tower opening is unique and must not be dropped silently')
    row = dict(mapping_row)
    row['timeline_frames'] = [347, 422]
    row['source_frame_indices'] = indices
    row['rejected_master_frames'] = [272, 346]
    return row


def _load(mapping_path, timeline_path, evidence_path):
    root = recipe.EDIT_DIR.parents[2] / 'jobs/reviews/J2242'
    preflight = json.loads((root / 'SOURCE_PREFLIGHT.json').read_text())
    clock_sha = preflight['evidence_files']['source_timeline.json']['sha256']
    recipe.require_hash(timeline_path, clock_sha)
    timeline = json.loads(timeline_path.read_text())
    mapping = json.loads(mapping_path.read_text())
    if mapping.get('master_sha256') != recipe.MASTER_SHA:
        raise ValueError('Mapping was made against a different master')
    evidence = json.loads(evidence_path.read_text())
    if evidence.get('status') != 'FULLRES_UPPER_BAND_MAPPING_ONLY':
        raise ValueError('Full-resolution evidence is not a mapping')
    return timeline, mapping, evidence, clock_sha


def _row(mapping, name):
    found = [row for row in mapping['rows'] if row['row'] == name]
    if len(found) != 1:
        raise ValueError(f'Missing mapped row {name}')
    return found[0]


def _measured(evidence, name):
    found = [row for row in evidence['rows'] if row['row'] == name]
    if len(found) != 1:
        raise ValueError(f'Missing measured row {name}')
    return found[0]


def _cards_inside(cards, row_name, lo, hi):
    selected = [card for card in cards
                if card['row'] == row_name and lo <= card['frame_in'] and card['frame_last'] <= hi]
    if not selected:
        raise ValueError('No complete caption card inside the unique span')
    return selected


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--mapping', type=Path, required=True)
    ap.add_argument('--timeline', type=Path, required=True)
    ap.add_argument('--evidence', type=Path, required=True)
    ap.add_argument('--out-dir', type=Path, required=True)
    args = ap.parse_args()
    mapping_sha = recipe.sha256_file(args.mapping)
    evidence_sha = recipe.sha256_file(args.evidence)
    timeline, mapping, evidence, clock_sha = _load(args.mapping, args.timeline, args.evidence)
    root = recipe.EDIT_DIR.parents[2] / 'jobs/reviews/J2242'
    cards = json.loads((root / 'CAPTION_LAYERS.json').read_text())['cards']
    franklin = franklin_prefix(_measured(evidence, '04_franklin_watches'), _row(mapping, '04_franklin_watches'))
    tower = tower_roof(_measured(evidence, '02_tower_tilt'), _row(mapping, '02_tower_tilt'))
    args.out_dir.mkdir(exist_ok=False)
    results = [
        render(franklin, timeline, _cards_inside(cards, '04_franklin_watches', 2718, 2864),
               args.out_dir / '04_franklin_watches',
               'Full-resolution unique prefix, source frames 0-146. Tail 2865-2887 stays out.'),
        render(tower, timeline, _cards_inside(cards, '02_tower_tilt', 347, 422),
               args.out_dir / '02_tower_tilt',
               'Full-resolution unique ON THE ROOF card, source frames 75-150. Opening card stays out.'),
    ]
    recipe.require_hash(args.mapping, mapping_sha)
    recipe.require_hash(args.evidence, evidence_sha)
    recipe.require_hash(args.timeline, clock_sha)
    recipe.write_new(args.out_dir / 'RESULT.json', {
        'job': 'J2242',
        'status': 'UNIQUE_FULLRES_SPANS_ONLY',
        'evidence_sha256': evidence_sha,
        'mapping_sha256': mapping_sha,
        'rows': results,
        'rejected': {
            '04_franklin_watches': [2865, 2887],
            '02_tower_tilt': [272, 346],
            '02_sentry_box': 'one near-tie inside THE SENTRY-BOX; whole card stays out',
            '02_knuckle_spark': 'one near-tie inside A SPARK; whole card stays out',
            '14_royal_society': 'two near-ties inside THE ROYAL SOCIETY; whole card stays out',
        },
        'master_created': False,
        'final_film_approval': False,
    })
    print('unique spans verified', flush=True)


if __name__ == '__main__':
    main()
