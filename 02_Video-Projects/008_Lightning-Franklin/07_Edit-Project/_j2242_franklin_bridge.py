"""Fill one refused Franklin frame when the centre window confirms the neighbour.

Master frame 2868 is a full-band near-tie. Its winner is source 148, the same
source already accepted on both sides of the gap, and the pre-declared centre
window confirms that winner. The runner-up is not used. Master frame 2869
stays out: its winner is the other source, and the window prefers that other
source, which this rule does not switch to. This does not make a master or
approve the film.
"""
import argparse
import json
from pathlib import Path

import _build_rough_v13_recipe as recipe
from _j2242_franklin_tail import franklin_tail, render_clean
from _j2242_subject_window import (
    _master_offsets,
    _memmap,
    _window_mse,
    confirm_subject_window,
)

ORIGIN = 2718
BRIDGE_FRAMES = (2868, 2869)


def _accepted(tail):
    accepted = {}
    for span in tail:
        lo, hi = span['timeline_frames']
        indices = span['source_frame_indices']
        if hi < lo or hi - lo + 1 != len(indices):
            raise ValueError('Tail span length changed')
        for offset, source in enumerate(indices):
            master = lo + offset
            if master < ORIGIN or master in accepted:
                raise ValueError('Tail span overlaps or leaves the Franklin window')
            if type(source) is not int or isinstance(source, bool) or source < 0:
                raise ValueError('Invalid accepted source')
            accepted[master] = source
    if not accepted:
        raise ValueError('Franklin tail is empty')
    return accepted


def gap_bridge(frames, tail, refused_masters, measurements):
    """Return one-frame bridges, and the refused frames that stay out.

    A refused frame is filled only when the nearest accepted sources on both
    sides are the same index, that index is the full-band winner, and the
    centre window confirms the winner. The runner-up is never adopted. A new
    fill is not itself a flank for another refused frame.
    """
    accepted = _accepted(tail)
    by_master = {}
    for item in measurements:
        if item.get('row') != '04_franklin_watches':
            continue
        master = item.get('master_frame')
        if type(master) is not int or isinstance(master, bool) or master in by_master:
            raise ValueError('Duplicate Franklin window measurement')
        by_master[master] = item
    filled = []
    still_out = []
    for master in refused_masters:
        if type(master) is not int or isinstance(master, bool):
            raise ValueError('Invalid refused frame')
        if master in accepted:
            raise ValueError(f'Master {master} is already accepted')
        left = [frame for frame in accepted if frame < master]
        right = [frame for frame in accepted if frame > master]
        if not left or not right:
            still_out.append(master)
            continue
        flank = accepted[max(left)]
        if accepted[min(right)] != flank:
            still_out.append(master)
            continue
        local = master - ORIGIN
        if local < 0 or local >= len(frames):
            raise ValueError('Refused frame is outside the Franklin row')
        frame = frames[local]
        if frame.get('master_frame') != master or frame.get('local_index') != local:
            raise ValueError('Refused frame is not the measured Franklin frame')
        winner = frame.get('fullres_best')
        runner = frame.get('fullres_second')
        if type(winner) is not int or type(runner) is not int or isinstance(winner, bool) or isinstance(runner, bool):
            raise ValueError('Invalid near-tie candidates')
        item = by_master.get(master)
        if item is None:
            raise ValueError(f'No centre-window measurement for {master}')
        if item.get('local_index') != local or item.get('fullres_best') != winner or item.get('fullres_second') != runner:
            raise ValueError('Window measurement names different candidates')
        confirmed = confirm_subject_window(item['window_best_mse'], item['window_runner_mse'])
        if confirmed != item.get('confirmed'):
            raise ValueError('Recorded confirmation does not match the window scores')
        if not confirmed or winner != flank or winner == runner:
            still_out.append(master)
            continue
        filled.append({
            'timeline_frames': [master, master],
            'source_frame_indices': [winner],
            'holds': {},
            'local_index': local,
            'runner_not_used': runner,
            'window_margin': item['window_runner_mse'] - item['window_best_mse'],
        })
    return filled, still_out


def verify_window(document, scratch, recorded):
    """Re-score frames 2868 and 2869 from the raw upper band."""
    offsets, total = _master_offsets(document)
    master = _memmap(Path(scratch) / 'master_upper.raw', total)
    source_path = Path(scratch) / '04_franklin_watches_source.raw'
    count = source_path.stat().st_size // (720 * 1920)
    source = _memmap(source_path, count)
    base = offsets['04_franklin_watches']
    checked = []
    for master_frame in BRIDGE_FRAMES:
        found = [item for item in recorded
                 if item.get('row') == '04_franklin_watches' and item.get('master_frame') == master_frame]
        if len(found) != 1:
            raise ValueError(f'Missing recorded window for {master_frame}')
        item = found[0]
        local = item['local_index']
        image = master[base + local]
        best = _window_mse(image, source[item['fullres_best']])
        runner = _window_mse(image, source[item['fullres_second']])
        if abs(best - item['window_best_mse']) > 1e-3 or abs(runner - item['window_runner_mse']) > 1e-3:
            raise ValueError(f'Centre window no longer matches the record at {master_frame}')
        if confirm_subject_window(best, runner) != item['confirmed']:
            raise ValueError(f'Fresh window score disagrees at {master_frame}')
        checked.append(master_frame)
    return checked


def _load_row(document, name):
    found = [row for row in document['rows'] if row['row'] == name]
    if len(found) != 1:
        raise ValueError(f'Missing row {name}')
    return found[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--mapping', type=Path, required=True)
    parser.add_argument('--timeline', type=Path, required=True)
    parser.add_argument('--window', type=Path, required=True)
    parser.add_argument('--three-scratch', type=Path, required=True)
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    evidence_sha = recipe.sha256_file(args.evidence)
    mapping_sha = recipe.sha256_file(args.mapping)
    window_sha = recipe.sha256_file(args.window)
    root = recipe.EDIT_DIR.parents[2] / 'jobs/reviews/J2242'
    preflight = json.loads((root / 'SOURCE_PREFLIGHT.json').read_text())
    clock_sha = preflight['evidence_files']['source_timeline.json']['sha256']
    recipe.require_hash(args.timeline, clock_sha)
    evidence = json.loads(args.evidence.read_text())
    mapping = json.loads(args.mapping.read_text())
    window = json.loads(args.window.read_text())
    if evidence.get('status') != 'FULLRES_UPPER_BAND_MAPPING_ONLY':
        raise ValueError('Franklin evidence is not full-resolution mapping')
    if mapping.get('master_sha256') != recipe.MASTER_SHA:
        raise ValueError('Mapping was made against a different master')
    if window.get('status') != 'SUBJECT_WINDOW_NEAR_TIE_CHECK':
        raise ValueError('Window file is not the centre-window check')
    measured = _load_row(evidence, '04_franklin_watches')
    mapped = _load_row(mapping, '04_franklin_watches')
    if measured.get('source_sha256') != mapped.get('source_sha256'):
        raise ValueError('Franklin source hash differs')
    tail, refused = franklin_tail(measured)
    if refused != list(BRIDGE_FRAMES):
        raise ValueError('Franklin refusal set changed')
    checked = verify_window(evidence, args.three_scratch, window['pairs'])
    if checked != list(BRIDGE_FRAMES):
        raise ValueError('Franklin bridge frames were not remeasured')
    filled, still_out = gap_bridge(measured['frames'], tail, refused, window['pairs'])
    if [item['timeline_frames'][0] for item in filled] != [2868] or still_out != [2869]:
        raise ValueError('Franklin bridge decision changed')
    if filled[0]['source_frame_indices'] != [148] or filled[0]['runner_not_used'] != 150:
        raise ValueError('Frame 2868 adopted something other than the confirmed neighbour')
    cards = json.loads((root / 'CAPTION_LAYERS.json').read_text())['cards']
    card = [item for item in cards if item['row'] == '04_franklin_watches' and item['frame_last'] == 2813]
    if len(card) != 1 or filled[0]['timeline_frames'][0] <= card[0]['frame_last']:
        raise ValueError('Bridge overlaps the Franklin caption')
    timeline = json.loads(args.timeline.read_text())
    args.out_dir.mkdir(exist_ok=False)
    lo, hi = filled[0]['timeline_frames']
    result = render_clean(filled[0], mapped, timeline, args.out_dir / f'{lo}-{hi}')
    recipe.require_hash(args.evidence, evidence_sha)
    recipe.require_hash(args.mapping, mapping_sha)
    recipe.require_hash(args.window, window_sha)
    recipe.require_hash(args.timeline, clock_sha)
    recipe.write_new(args.report, {
        'job': 'J2242',
        'status': 'FRANKLIN_CONFIRMED_NEIGHBOUR_BRIDGE',
        'rule': (
            'Fill a refused frame only when both neighbouring accepted sources '
            'are the full-band winner and the centre window confirms that winner. '
            'Never adopt the runner-up.'
        ),
        'evidence_sha256': evidence_sha,
        'mapping_sha256': mapping_sha,
        'window_sha256': window_sha,
        'remeasured_master_frames': checked,
        'rows': [result],
        'filled_master_frames': [2868],
        'refused_master_frames': still_out,
        'refusal_reason': (
            'Frame 2869 keeps full-band winner 150. The centre window prefers '
            'source 148, and this rule does not switch to the runner-up. Source '
            '150 is not the accepted neighbour on both sides.'
        ),
        'caption_on_these_frames': False,
        'master_created': False,
        'final_film_approval': False,
    })
    print('franklin bridge verified', flush=True)


if __name__ == '__main__':
    main()
