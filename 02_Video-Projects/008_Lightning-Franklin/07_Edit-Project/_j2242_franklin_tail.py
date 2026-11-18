"""Franklin clear-tail frames after the rendered unique prefix.

A near-tie repeats the nearest earlier unique source frame when that frame is
neither candidate. It never looks forward: looking forward makes this row
backward, and the existing outside-hold rule then refuses the whole row. A
backward hold is refused. Unique frames keep their winner. Frames 2868 and
2869 stay out. This does not make a master or approve the film.
"""
import argparse
import json
import subprocess
from fractions import Fraction
from pathlib import Path

import _build_rough_v13_recipe as recipe
from _j2242_caption_composites import source_graph, source_runs
from _j2242_caption_layers import clock_expression
from _j2242_salon_patch import pixel_hashes

MAX_MSE = 9.0
MIN_MARGIN = 0.1
PREFIX_LAST = 146
REFUSED_LOCALS = [150, 151]


def _unique(frame):
    return frame.get('best_mse', MAX_MSE + 1) <= MAX_MSE and frame.get('margin', 0) >= MIN_MARGIN


def _index(frame, key):
    value = frame.get(key)
    if type(value) is not int or isinstance(value, bool) or value < 0:
        raise ValueError(f'Invalid {key}')
    return value


def _nearest_earlier_outside(frames, index, winner, runner):
    """Nearest earlier unique source, or None when that source is a candidate.

    Does not walk past a unique candidate, and does not look forward.
    """
    cursor = index - 1
    while cursor >= 0:
        if _unique(frames[cursor]):
            candidate = _index(frames[cursor], 'fullres_best')
            if candidate != winner and candidate != runner:
                return candidate
            return None
        cursor -= 1
    return None


def forward_spans(frames):
    """Contiguous monotonic spans, and the local indices left unrendered."""
    if not frames or any(frame.get('local_index') != i for i, frame in enumerate(frames)):
        raise ValueError('Measured frames are out of order')
    accepted = []
    refused = []
    last = None
    for i, frame in enumerate(frames):
        winner = _index(frame, 'fullres_best')
        runner = _index(frame, 'fullres_second')
        if _unique(frame):
            chosen = winner
            held = False
        else:
            chosen = _nearest_earlier_outside(frames, i, winner, runner)
            held = chosen is not None
            if chosen in (winner, runner):
                raise ValueError(f'Local {i} adopted a near-tie candidate')
        if chosen is not None and last is not None and chosen < last:
            chosen = None
            held = False
        if chosen is None:
            refused.append(i)
            continue
        last = chosen
        accepted.append((i, chosen, held))
    spans = []
    current = []
    for item in accepted:
        if current and item[0] != current[-1][0] + 1:
            spans.append(_span(current))
            current = []
        current.append(item)
    if current:
        spans.append(_span(current))
    return spans, refused


def _span(items):
    return {
        'local_in': items[0][0],
        'local_last': items[-1][0],
        'source_frame_indices': [source for _, source, _ in items],
        'holds': {local: source for local, source, held in items if held},
    }


def franklin_tail(fullres_row):
    """Two clear-plate spans. Master frames 2868 and 2869 stay out."""
    if fullres_row.get('row') != '04_franklin_watches':
        raise ValueError('Wrong Franklin row')
    if fullres_row.get('timeline_frames') != [2718, 2887]:
        raise ValueError('Franklin window changed')
    frames = fullres_row.get('frames') or []
    if len(frames) != 170:
        raise ValueError('Franklin frame count changed')
    for i in range(PREFIX_LAST + 1):
        if not _unique(frames[i]) or _index(frames[i], 'fullres_best') != i:
            raise ValueError('Franklin prefix no longer matches the rendered unique span')
    spans, refused = forward_spans(frames)
    if refused != REFUSED_LOCALS:
        raise ValueError('Franklin refusal set changed')
    tail_items = []
    for span in spans:
        for offset, source in enumerate(span['source_frame_indices']):
            local = span['local_in'] + offset
            if local > PREFIX_LAST:
                tail_items.append((local, source, local in span['holds']))
    tail = []
    current = []
    for item in tail_items:
        if current and item[0] != current[-1][0] + 1:
            tail.append(_span(current))
            current = []
        current.append(item)
    if current:
        tail.append(_span(current))
    expected = [
        ([2865, 2867], [146, 148, 148], {147: 146}),
        ([2870, 2887],
         [148, 148, 148, 148, 148, 148, 158, 159, 160, 161, 162, 163, 164, 165, 166, 176, 177, 178],
         {152: 148, 153: 148, 154: 148, 155: 148, 156: 148, 157: 148}),
    ]
    if len(tail) != len(expected):
        raise ValueError('Franklin tail span count changed')
    for span, (timeline, indices, holds) in zip(tail, expected):
        span['timeline_frames'] = [2718 + span['local_in'], 2718 + span['local_last']]
        if span['timeline_frames'] != timeline or span['source_frame_indices'] != indices or span['holds'] != holds:
            raise ValueError('Franklin tail schedule changed')
        if span['timeline_frames'][0] <= 2864:
            raise ValueError('Tail overlaps the rendered prefix')
        for local, source in holds.items():
            frame = frames[local]
            if source in (frame['fullres_best'], frame['fullres_second']):
                raise ValueError(f'Local {local} adopted a near-tie candidate')
    return tail, [2718 + local for local in refused]


def render_clean(span, mapping_row, timeline, out):
    """Lossless clean plate. No caption is composited onto these frames."""
    lo, hi = span['timeline_frames']
    frames = timeline['frames'][lo:hi + 1]
    indices = span['source_frame_indices']
    if timeline['time_base'] != '1/12288' or len(frames) != hi - lo + 1 or len(indices) != len(frames):
        raise ValueError('Missing original tail clock')
    if any(frame['index'] != lo + i for i, frame in enumerate(frames)):
        raise ValueError('Original frame indices changed')
    source = Path(mapping_row['source_path'])
    recipe.require_hash(source, mapping_row['source_sha256'])
    native = recipe.probe_video(source)
    tb = Fraction(native['time_base'])
    if max(indices) >= len(native['frames']):
        raise ValueError('Source map exceeds decoded source')
    selected = [native['frames'][i] for i in indices]
    if any(frame['pts'] * tb != Fraction(i, 24) or frame['duration'] * tb != Fraction(1, 24)
           for i, frame in zip(indices, selected)):
        raise ValueError('Selected source is not native 24fps')
    source_runs(indices)
    out.mkdir(exist_ok=False)
    video = out / 'clean_plate.nut'
    base = 'scale=1920:1080:flags=lanczos,setsar=1,format=yuv420p'
    graph = source_graph(indices) + f";[ordered]{base},settb=1/12288,setpts='{clock_expression(frames)}'[base]"
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-i', str(source),
                    '-filter_complex', graph, '-map', '[base]', '-an',
                    '-c:v', 'ffv1', '-level', '3', '-threads', '4', '-fps_mode', 'passthrough',
                    '-enc_time_base', '1/12288', '-avoid_negative_ts', 'disabled', '-n', str(video)],
                   check=True)
    actual = recipe.probe_video(video, len(frames))
    ratio = Fraction(actual['time_base']) / Fraction('1/12288')
    if [frame['pts'] * ratio for frame in actual['frames']] != [frame['pts'] for frame in frames]:
        raise ValueError('Clean plate changed original PTS')
    duration_match = [frame['duration'] * ratio for frame in actual['frames']] == [frame['duration'] for frame in frames]
    expected = [pixel_hashes(source, base)[i] for i in indices]
    measured = pixel_hashes(video)
    if measured != expected:
        raise ValueError('Clean plate differs from the selected source')
    recipe.require_hash(source, mapping_row['source_sha256'])
    clock = out / 'original_clock.json'
    recipe.write_new(clock, {'time_base': '1/12288', 'frames': frames})
    result = {
        'row': '04_franklin_watches',
        'path': str(video),
        'sha256': recipe.sha256_file(video),
        'timeline_frames': span['timeline_frames'],
        'source_frame_indices': indices,
        'source_runs': source_runs(indices),
        'holds': [[local, source] for local, source in sorted(span['holds'].items())],
        'source_sha256': mapping_row['source_sha256'],
        'frame_count': len(frames),
        'caption_count': 0,
        'original_pts_match': True,
        'original_durations_preserved_in_intermediate': duration_match,
        'original_clock_path': str(clock),
        'original_clock_sha256': recipe.sha256_file(clock),
        'full_frame_pixel_hashes_match': True,
        'final_film_approval': False,
    }
    recipe.write_new(out / 'RESULT.json', result)
    print(span['timeline_frames'], len(frames), 'clean frames verified', flush=True)
    return result


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
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    evidence_sha = recipe.sha256_file(args.evidence)
    mapping_sha = recipe.sha256_file(args.mapping)
    root = recipe.EDIT_DIR.parents[2] / 'jobs/reviews/J2242'
    preflight = json.loads((root / 'SOURCE_PREFLIGHT.json').read_text())
    clock_sha = preflight['evidence_files']['source_timeline.json']['sha256']
    recipe.require_hash(args.timeline, clock_sha)
    evidence = json.loads(args.evidence.read_text())
    mapping = json.loads(args.mapping.read_text())
    if evidence.get('status') != 'FULLRES_UPPER_BAND_MAPPING_ONLY':
        raise ValueError('Franklin evidence is not full-resolution mapping')
    if mapping.get('master_sha256') != recipe.MASTER_SHA:
        raise ValueError('Mapping was made against a different master')
    measured = _load_row(evidence, '04_franklin_watches')
    mapped = _load_row(mapping, '04_franklin_watches')
    if measured.get('source_sha256') != mapped.get('source_sha256'):
        raise ValueError('Franklin source hash differs')
    cards = json.loads((root / 'CAPTION_LAYERS.json').read_text())['cards']
    card = [item for item in cards if item['row'] == '04_franklin_watches' and item['frame_last'] == 2813]
    if len(card) != 1:
        raise ValueError('Franklin caption card changed')
    tail, refused = franklin_tail(measured)
    if any(span['timeline_frames'][0] <= card[0]['frame_last'] for span in tail):
        raise ValueError('Tail overlaps the caption card')
    timeline = json.loads(args.timeline.read_text())
    args.out_dir.mkdir(exist_ok=False)
    results = []
    for span in tail:
        lo, hi = span['timeline_frames']
        results.append(render_clean(span, mapped, timeline, args.out_dir / f'{lo}-{hi}'))
    recipe.require_hash(args.evidence, evidence_sha)
    recipe.require_hash(args.mapping, mapping_sha)
    recipe.require_hash(args.timeline, clock_sha)
    recipe.write_new(args.report, {
        'job': 'J2242',
        'status': 'FRANKLIN_FORWARD_HOLD_CLEAR_TAIL',
        'rule': (
            'Repeat the nearest earlier unique source frame when it is neither '
            'near-tie candidate. Never look forward. Refuse a backward hold.'
        ),
        'evidence_sha256': evidence_sha,
        'mapping_sha256': mapping_sha,
        'rows': results,
        'refused_master_frames': refused,
        'caption_on_these_frames': False,
        'master_created': False,
        'final_film_approval': False,
    })
    print('franklin tail verified', flush=True)


if __name__ == '__main__':
    main()
