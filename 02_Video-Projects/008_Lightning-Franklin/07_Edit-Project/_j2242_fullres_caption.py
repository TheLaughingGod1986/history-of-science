"""Composite one caption row from a unique full-resolution source schedule.

The coarser low-resolution map may disagree. A frame that is not uniquely
identified stays unrendered, and the whole row stays out. This writes a
lossless intermediate only: no master, audio, or film approval.
"""
import argparse
import json
from pathlib import Path

import _build_rough_v13_recipe as recipe
from _j2242_ambiguous_fullres import accepted_fullres_indices
from _j2242_caption_composites import render

EVIDENCE = (
    'Full-resolution upper-band match. Every frame has per-pixel MSE at or below 9 '
    'and a runner-up margin of at least 0.1. Low-resolution disagreements are recorded '
    'and were not used as the schedule. Not a motion review, audio review, or film approval.'
)


def prepare_fullres_row(mapping_row, fullres_row):
    """Copy the inventory row and replace its schedule with the full-resolution one."""
    if mapping_row['row'] != fullres_row['row']:
        raise ValueError('Row names differ')
    if list(mapping_row['timeline_frames']) != list(fullres_row['timeline_frames']):
        raise ValueError('Timeline windows differ')
    if mapping_row['source_sha256'] != fullres_row['source_sha256']:
        raise ValueError('Source hashes differ')
    if fullres_row.get('role') != 'ambiguous':
        raise ValueError('Only an unresolved ambiguous row can use this schedule')
    indices = accepted_fullres_indices(fullres_row)
    row = dict(mapping_row)
    row['source_frame_indices'] = indices
    return row


def _load_checked(mapping_path, timeline_path):
    root = recipe.EDIT_DIR.parents[2] / 'jobs/reviews/J2242'
    evidence = json.loads((root / 'SOURCE_PREFLIGHT.json').read_text())
    clock_sha = evidence['evidence_files']['source_timeline.json']['sha256']
    recipe.require_hash(timeline_path, clock_sha)
    timeline = json.loads(timeline_path.read_text())
    mapping = json.loads(mapping_path.read_text())
    if mapping['master_sha256'] != recipe.MASTER_SHA:
        raise ValueError('Wrong mapped master')
    cuts_path = recipe.EDIT_DIR / '_desk/008/rough_v12/cuts_rough_v12.json'
    recipe.require_hash(cuts_path, mapping['cuts_sha256'])
    cuts = json.loads(cuts_path.read_text())
    labels = recipe.load_manifest()['caption_treatment']['labels']
    if len(mapping['rows']) != 27 or len({r['row'] for r in mapping['rows']}) != 27:
        raise ValueError('Incomplete or duplicated source mapping inventory')
    for row in mapping['rows']:
        if not any(lab['row'] == row['row'] and lab['master_frames'] == row['timeline_frames'] for lab in labels):
            raise ValueError('Mapped window differs from approved caption inventory')
        if not any(c['row'] == row['row'] and c['source_path'] == row['source_path']
                   and c['source_sha256'] == row['source_sha256'] for c in cuts):
            raise ValueError('Mapping source is absent from historical inventory')
    return timeline, mapping, clock_sha


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--row', required=True)
    ap.add_argument('--mapping', type=Path, required=True)
    ap.add_argument('--fullres', type=Path, required=True)
    ap.add_argument('--timeline', type=Path, required=True)
    ap.add_argument('--out-dir', type=Path, required=True)
    ap.add_argument('--evidence', type=Path, required=True)
    args = ap.parse_args()
    mapping_sha = recipe.sha256_file(args.mapping)
    fullres_sha = recipe.sha256_file(args.fullres)
    timeline, mapping, clock_sha = _load_checked(args.mapping, args.timeline)
    fullres = json.loads(args.fullres.read_text())
    if fullres.get('status') != 'FULLRES_UPPER_BAND_MAPPING_ONLY':
        raise ValueError('Full-resolution file is not the mapping evidence')
    item = next((row for row in fullres['rows'] if row['row'] == args.row), None)
    mapped = next((row for row in mapping['rows'] if row['row'] == args.row), None)
    if item is None or mapped is None:
        raise ValueError('Requested row is absent')
    prepared = prepare_fullres_row(mapped, item)
    root = recipe.EDIT_DIR.parents[2] / 'jobs/reviews/J2242'
    cards = json.loads((root / 'CAPTION_LAYERS.json').read_text())['cards']
    result = render(prepared, timeline, cards, args.out_dir, EVIDENCE)
    recipe.require_hash(args.mapping, mapping_sha)
    recipe.require_hash(args.fullres, fullres_sha)
    recipe.require_hash(args.timeline, clock_sha)
    disagreements = [
        {
            'local_index': frame['local_index'],
            'lowres_index': frame['lowres_index'],
            'fullres_best': frame['fullres_best'],
            'best_mse': frame['best_mse'],
            'margin': frame['margin'],
        }
        for frame in item['frames']
        if frame['lowres_index'] != frame['fullres_best']
    ]
    recipe.write_new(args.evidence, {
        'job': 'J2242',
        'status': 'FULLRES_UNIQUE_CAPTION_INTERMEDIATE',
        'row': args.row,
        'fullres_sha256': fullres_sha,
        'mapping_sha256': mapping_sha,
        'lowres_disagreement_count': len(disagreements),
        'lowres_disagreements': disagreements,
        'maximum_mse': item['maximum_mse'],
        'minimum_runner_up_mse_margin': item['minimum_runner_up_mse_margin'],
        'composite': result,
        'master_created': False,
        'final_film_approval': False,
    })
    print(args.row, 'full-resolution composite verified', flush=True)


if __name__ == '__main__':
    main()
