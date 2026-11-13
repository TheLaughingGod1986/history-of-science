"""Closed-IDR packet plan for the Franklin master. Does not write a film.

SOURCE_PREFLIGHT proved each random-access sample is an IDR, so a changed
frame forces that whole IDR interval to be re-encoded. Every other frame
stays a copied source packet. Original PTS and durations are copied onto the
replacement. Nothing here is a master, a preservation proof, or an approval.
"""
import argparse
import json
from pathlib import Path

import _build_rough_v13_recipe as recipe
from _j2242_salon_splice import FIRST as SALON_FIRST, LAST as SALON_LAST

REVIEW = Path(__file__).resolve().parents[3] / 'jobs' / 'reviews' / 'J2242'
FRAME_COUNT = recipe.EXPECTED_FRAMES
NIGHT_STREET = (1129, 1231)
EXCLUDED_FRAME = 2869
DECODE_DELAY = 1024
JOB_ENVELOPES = (
    (423, 544),
    (744, 839),
    (2506, 2665),
    (3168, 3343),
    (4511, 4670),
    (4977, 5077),
    (11358, 11492),
)
UNPLACED_TITLES = ('15_likeness_fire', '06_same_thing', '08_looking_path')
SPAN_FILES = (
    'CAPTION_COMPOSITES.json',
    'REPEAT_CAPTION_COMPOSITES.json',
    'OPENING_COMPOSITE.json',
    'TABLE_BODY.json',
    'TABLE_LEADIN.json',
    'STORM_PATCH.json',
    'JAR_PATCH.json',
    'POINTS_PATCH.json',
    'LETTER_PATCH.json',
    'RODS_PATCH.json',
    'FRANKLIN_BRIDGE.json',
    'FRANKLIN_TAIL.json',
    'UNIQUE_SPANS.json',
    'OUTSIDE_HOLD.json',
    'ROYAL_SUBJECT.json',
    'GIANT_SPARK_FULLRES.json',
    'SAFE_PATH.json',
    'SAFE_PATH_TITLE.json',
)


def idr_bounds(idrs, frame_count):
    if not idrs or idrs[0] != 0 or list(idrs) != sorted(set(idrs)):
        raise ValueError('IDR list is not a sorted random-access map')
    if idrs[-1] >= frame_count:
        raise ValueError('IDR past the last frame')
    points = list(idrs) + [frame_count]
    return [(a, b - 1) for a, b in zip(points, points[1:])]


def _overlaps(a0, a1, b0, b1):
    return not (a1 < b0 or b1 < a0)


def _split(bounds, first, last):
    parts = [(max(first, a), min(last, b)) for a, b in bounds]
    parts = [(lo, hi) for lo, hi in parts if lo <= hi]
    if not parts or parts[0][0] != first or parts[-1][1] != last:
        raise ValueError('Change sits outside the film')
    covered = first
    for lo, hi in parts:
        if lo != covered:
            raise ValueError('Change split left a gap')
        covered = hi + 1
    return parts


def _union_ranges(parts):
    points = []
    for part in parts:
        points.append((part['first'], 1))
        points.append((part['last'] + 1, -1))
    depth = count = 0
    start = None
    ranges = []
    for frame, delta in sorted(points):
        if depth and start is not None and frame > start:
            count += frame - start
        depth += delta
        start = frame
    return count


def _missing_ranges(first, last, parts):
    covered = []
    for part in parts:
        covered.append((part['first'], 1))
        covered.append((part['last'] + 1, -1))
    depth = 0
    ranges = []
    open_at = None
    cursor = first
    for frame, delta in sorted(covered):
        if frame > last + 1:
            break
        if depth == 0 and frame > cursor:
            ranges.append([cursor, frame - 1])
        depth += delta
        cursor = frame
    if cursor <= last:
        ranges.append([cursor, last])
    return ranges


def plan_envelopes(idrs, changes, frame_count=FRAME_COUNT):
    bounds = idr_bounds(idrs, frame_count)
    bound_of = {item: item for item in bounds}
    grouped = {item: [] for item in bounds}
    for change in changes:
        first, last = change['first'], change['last']
        if not isinstance(first, int) or not isinstance(last, int):
            raise ValueError('Frame numbers must be integers')
        if _overlaps(first, last, *NIGHT_STREET):
            raise ValueError('0:51 night street stays untouched')
        if first <= EXCLUDED_FRAME <= last:
            raise ValueError('Frame 2869 stays out')
        for lo, hi in _split(bounds, first, last):
            env = next(item for item in bound_of if item[0] <= lo <= hi <= item[1])
            grouped[env].append({
                'name': change['name'], 'first': lo, 'last': hi,
                'frames': hi - lo + 1, 'source': change.get('source', ''),
            })
    envelopes = []
    for first, last in bounds:
        parts = grouped[(first, last)]
        if not parts:
            continue
        changed = _union_ranges(parts)
        keep = _missing_ranges(first, last, parts)
        keep_frames = sum(b - a + 1 for a, b in keep)
        if changed + keep_frames != last - first + 1:
            raise ValueError('Envelope frames were counted twice or dropped')
        envelopes.append({
            'first': first,
            'last': last,
            'frames': last - first + 1,
            'changed_frames': changed,
            'changed': parts,
            'stitch_source_frames': keep,
            'pixels_complete': keep == [],
            'h264_packets': 'OUTSTANDING',
        })
    return envelopes


def assignment(envelopes, frame_count=FRAME_COUNT):
    cursor = -1
    replaced = 0
    for env in envelopes:
        if env['first'] <= cursor or env['last'] < env['first']:
            raise ValueError('Envelopes overlap or run backwards')
        cursor = env['last']
        replaced += env['frames']
    if replaced > frame_count:
        raise ValueError('Replacements exceed the film')
    return {'frame_count': frame_count, 'copied_frames': frame_count - replaced,
            'replaced_frames': replaced}


def schedule_replacement(frames, delay=DECODE_DELAY):
    """Copy each source PTS and duration. DTS keeps the source decode delay."""
    if delay != DECODE_DELAY:
        raise ValueError('Unexpected source decode delay')
    scheduled = []
    for frame in frames:
        pts, dur = int(frame['pts']), int(frame['duration'])
        if dur <= 0:
            raise ValueError('Duration must stay a positive source tick count')
        scheduled.append({'pts': pts, 'dts': pts - delay, 'duration': dur})
    return scheduled


def _iter_spans(data, source):
    found = []

    def walk(obj):
        if isinstance(obj, dict):
            frames = obj.get('timeline_frames')
            status = str(obj.get('status', ''))
            if (obj.get('path') and 'REJECTED' not in status
                    and isinstance(frames, list) and len(frames) == 2
                    and all(isinstance(n, int) for n in frames)):
                found.append({'name': obj.get('row') or status or source,
                              'first': frames[0], 'last': frames[1], 'source': source})
            for value in obj.values():
                walk(value)
        elif isinstance(obj, list):
            for value in obj:
                walk(value)

    walk(data)
    return found


def load_changes(review_dir=REVIEW):
    review_dir = Path(review_dir)
    changes = []
    for name in SPAN_FILES:
        data = json.loads((review_dir / name).read_text())
        found = _iter_spans(data, name)
        if not found:
            raise ValueError(f'No placed intermediate in {name}')
        changes.extend(found)
    salon = json.loads((review_dir / 'SALON_PATCH.json').read_text())
    if salon.get('status') != 'SALON_INTERMEDIATE_ONLY' or salon.get('frame_count') != 160:
        raise ValueError('Salon intermediate is not the 160-frame patch')
    changes.append({'name': '02_salon_spark', 'first': SALON_FIRST, 'last': SALON_LAST,
                    'source': 'SALON_PATCH.json'})
    titles = json.loads((review_dir / 'TITLE_ROWS.json').read_text())
    metal = next(row for row in titles['rows'] if row['row'] == '10_metal_easy')
    first, last = metal['master_frames']
    changes.append({'name': '10_metal_easy', 'first': first, 'last': last,
                    'source': 'TITLE_ROWS.json'})
    unplaced = [row['row'] for row in titles['rows'] if 'master_frames' not in row]
    if tuple(unplaced) != UNPLACED_TITLES:
        raise ValueError('Unplaced title rows changed')
    seen = set()
    unique = []
    for change in changes:
        key = (change['name'], change['first'], change['last'], change['source'])
        if key in seen:
            continue
        seen.add(key)
        unique.append(change)
    return unique


def _covers(envelopes, frame):
    return any(env['first'] <= frame <= env['last'] for env in envelopes)


def _changed(envelopes, frame):
    return any(part['first'] <= frame <= part['last']
               for env in envelopes for part in env['changed'])


def build_report(review_dir=REVIEW):
    review_dir = Path(review_dir)
    pre = json.loads((review_dir / 'SOURCE_PREFLIGHT.json').read_text())
    if pre.get('all_random_access_samples_are_idr') is not True:
        raise ValueError('IDR proof is missing')
    if pre.get('video_packets') != FRAME_COUNT:
        raise ValueError('Video packet count is not the master frame count')
    changes = load_changes(review_dir)
    envelopes = plan_envelopes(pre['idr_frame_indices'], changes)
    counts = assignment(envelopes)
    for first, last in JOB_ENVELOPES:
        match = [env for env in envelopes if env['first'] == first and env['last'] == last]
        if len(match) != 1:
            raise ValueError(f'Job envelope {first}-{last} is not one closed IDR group')
    night_inside = _covers(envelopes, NIGHT_STREET[0]) or _covers(envelopes, NIGHT_STREET[1])
    if any(_changed(envelopes, frame) for frame in range(NIGHT_STREET[0], NIGHT_STREET[1] + 1)):
        raise ValueError('Night street was marked changed')
    if _changed(envelopes, EXCLUDED_FRAME):
        raise ValueError('Frame 2869 was marked changed')
    safe = [part for env in envelopes for part in env['changed']
            if part['first'] == 11038]
    safe_end = max(part['last'] for part in safe) if safe else None
    return {
        'job': 'J2242',
        'status': 'PACKET_PLAN_ONLY',
        'idr_samples': len(pre['idr_frame_indices']),
        'idr_proof': 'actual IDR NALs in SOURCE_PREFLIGHT',
        'changes': len(changes),
        'envelopes': envelopes,
        **counts,
        'job_envelopes_are_closed_idr_groups': True,
        'night_street_frames': list(NIGHT_STREET),
        'night_street': 'lossless_keep_inside_reencode' if night_inside else 'packet_copy',
        'frame_2869': 'keep_inside_reencode' if _covers(envelopes, EXCLUDED_FRAME) else 'packet_copy',
        'foil_frame_3353': 'packet_copy' if not _covers(envelopes, 3353) else 'inside_reencode',
        'safe_path_intermediate_last': safe_end,
        'safe_path_frame_11118': 'not_in_intermediate' if safe_end != 11118 else 'included',
        'unplaced_title_rows': list(UNPLACED_TITLES),
        'decode_delay_ticks': DECODE_DELAY,
        'timestamp_policy': 'copy original PTS and duration; never setpts=N/24',
        'h264_packets': 'OUTSTANDING',
        'output_preservation': 'OUTSTANDING',
        'vo_sync': 'UNMEASURED',
        'output_film_created': False,
        'finished_master': False,
        'approval': False,
        'spend_gbp': 0,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', action='store_true')
    parser.add_argument('--review-dir', type=Path, default=REVIEW)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    if not args.plan:
        parser.error('--plan is required; this tool does not mux')
    report = build_report(args.review_dir)
    if args.out:
        recipe.write_new(args.out, report)
    summary = {key: report[key] for key in (
        'status', 'idr_samples', 'changes', 'copied_frames', 'replaced_frames',
        'night_street', 'frame_2869', 'foil_frame_3353', 'safe_path_intermediate_last',
        'output_film_created', 'finished_master')}
    summary['envelopes'] = len(report['envelopes'])
    summary['pixels_complete'] = sum(env['pixels_complete'] for env in report['envelopes'])
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
