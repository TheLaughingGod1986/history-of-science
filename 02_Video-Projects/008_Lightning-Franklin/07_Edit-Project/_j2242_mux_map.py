"""Assembly order for the Franklin mux. Does not write a film.

Every master frame is one of three pieces: an original packet, a High qp 1
encode, or a High I_PCM picture. The jar keep 3168-3258 stays the original
packets. Frame 3259 is the exact picture, not that copy. Timestamps stay
the source PTS and duration, including every 1024-tick step. Nothing here
is hos_008_master_v04.mp4.
"""
import argparse
import json
from pathlib import Path

import _j2242_exact_pcm as exact
import _j2242_jar_copy as jar
import _j2242_packet_mux as mux

MASTER_NAME = 'hos_008_master_v04.mp4'
NIGHT = mux.NIGHT_STREET
FOIL = 3353
SALON = (mux.SALON_FIRST, mux.SALON_LAST)


def refuse_master(path):
    name = Path(path).name
    if name == MASTER_NAME or 'master_v04' in name:
        raise ValueError('This map cannot be written as the v04 master')
    return Path(path)


def clock_summary(frames):
    """Copy the source clock. A zero duration or a rebuilt index is refused."""
    if not frames:
        raise ValueError('The source clock is empty')
    scheduled = mux.schedule_replacement(frames)
    if [(row['pts'], row['duration']) for row in scheduled] != [
            (int(frame['pts']), int(frame['duration'])) for frame in frames]:
        raise ValueError('The replacement clock changed a source timestamp')
    counts = {}
    gaps = 0
    previous = None
    for index, frame in enumerate(frames):
        if int(frame.get('index', index)) != index:
            raise ValueError('Source clock frames are not in order')
        pts, dur = int(frame['pts']), int(frame['duration'])
        if previous is not None and pts != previous:
            gaps += 1
        previous = pts + dur
        counts[dur] = counts.get(dur, 0) + 1
    if 1024 not in counts:
        raise ValueError('The 1024-tick step is missing from the source clock')
    return {
        'time_base': '1/12288',
        'frames': len(frames),
        'start_pts': scheduled[0]['pts'],
        'end_pts': scheduled[-1]['pts'] + scheduled[-1]['duration'],
        'duration_ticks': {str(key): counts[key] for key in sorted(counts)},
        'ticks_1024': counts[1024],
        'gaps': gaps,
        'policy': 'copy original PTS and duration, including a gap; never setpts=N/24',
    }


def _ranges(changed):
    """Turn inclusive changed parts into a set of frame numbers."""
    frames = set()
    for part in changed:
        frames.update(range(part['first'], part['last'] + 1))
    return frames


def _load_json(path):
    data = json.loads(path.read_text())
    if data.get('finished_master') or data.get('approval') or data.get('spend_gbp'):
        raise ValueError(f'{path.name} is not an unfinished zero-spend piece')
    return data


def load_pieces(review_dir):
    review_dir = Path(review_dir)
    encodes = {}
    for path in sorted(review_dir.glob('ENCODE_*.json')):
        data = _load_json(path)
        key = (int(data['first']), int(data['last']))
        if key in encodes or key[0] > key[1]:
            raise ValueError(f'Encode range {key} is duplicated or backwards')
        if data.get('profile') != 'High' or data.get('bframes') != 0 or data.get('audio'):
            raise ValueError(f'{path.name} is not a silent High encode without B frames')
        if data.get('lossless') is not False:
            raise ValueError(f'{path.name} claims a lossless High encode')
        encodes[key] = data
    exact_doc = _load_json(review_dir / 'EXACT_PCM.json')
    exact_runs = {}
    for run in exact_doc['runs']:
        key = (int(run['first']), int(run['last']))
        if key in exact_runs:
            raise ValueError(f'Two exact pictures for {key}')
        exact_runs[key] = run
    if tuple(exact_runs) != exact.BLOCKED:
        raise ValueError('Exact pictures are not the four blocked runs')
    jar_doc = _load_json(review_dir / 'JAR_COPY.json')
    if (int(jar_doc['first']), int(jar_doc['last'])) != (jar.JAR_FIRST, jar.JAR_LAST):
        raise ValueError('Jar copy is not frames 3168-3258')
    if int(jar_doc['blocked_frame']) != jar.JAR_BLOCKED or jar_doc.get('audio'):
        raise ValueError('Jar copy includes frame 3259 or audio')
    return encodes, exact_runs, jar_doc


def _owner(frame, table):
    hits = [key for key in table if key[0] <= frame <= key[1]]
    if len(hits) != 1:
        raise ValueError(f'Frame {frame} belongs to {len(hits)} clips')
    return hits[0]


def assign(envelopes, encodes, exact_runs, frame_count=mux.FRAME_COUNT):
    changed = set()
    inside = set()
    for env in envelopes:
        inside.update(range(env['first'], env['last'] + 1))
        changed.update(_ranges(env['changed']))
    owners = []
    for frame in range(frame_count):
        is_exact = any(a <= frame <= b for a, b in exact.BLOCKED)
        is_jar = jar.JAR_FIRST <= frame <= jar.JAR_LAST
        if is_exact and frame in changed:
            raise ValueError(f'Exact frame {frame} was also marked changed')
        if is_jar and frame in changed:
            raise ValueError(f'Jar keep frame {frame} was also marked changed')
        if is_exact:
            if frame not in inside:
                raise ValueError(f'Exact frame {frame} is outside a rebuilt group')
            owners.append(('exact_pcm', _owner(frame, exact_runs)))
        elif frame in changed:
            owners.append(('high_encode', _owner(frame, encodes)))
        elif is_jar:
            if frame not in inside:
                raise ValueError('Jar keep fell outside its group')
            owners.append(('packet_copy', 'jar_keep'))
        elif frame in inside:
            raise ValueError(f'Frame {frame} is kept inside a rebuilt group with no exact picture')
        else:
            owners.append(('packet_copy', 'master_packets'))
    for key in encodes:
        for frame in range(key[0], key[1] + 1):
            if owners[frame] != ('high_encode', key):
                raise ValueError(f'Encode {key} does not cover frame {frame}')
    for key in exact_runs:
        for frame in range(key[0], key[1] + 1):
            if owners[frame] != ('exact_pcm', key):
                raise ValueError(f'Exact picture {key} does not cover frame {frame}')
    return owners


def collapse(owners):
    runs = []
    start = 0
    for index, owner in enumerate(owners):
        if owner != owners[start]:
            runs.append(_run(start, index - 1, owners[start]))
            start = index
    runs.append(_run(start, len(owners) - 1, owners[start]))
    covered = sum(run['frames'] for run in runs)
    if covered != len(owners):
        raise ValueError('Assembly runs dropped or repeated a frame')
    cursor = 0
    for run in runs:
        if run['first'] != cursor:
            raise ValueError('Assembly runs leave a gap')
        cursor = run['last'] + 1
    return runs


def _run(first, last, owner):
    role, key = owner
    return {
        'role': role,
        'first': first,
        'last': last,
        'frames': last - first + 1,
        'clip': list(key) if isinstance(key, tuple) else key,
    }


def _check_known(runs):
    by_role = {}
    for run in runs:
        for frame in range(run['first'], run['last'] + 1):
            by_role[frame] = (run['role'], tuple(run['clip']) if isinstance(run['clip'], list) else run['clip'])
    for frame in range(NIGHT[0], NIGHT[1] + 1):
        if by_role[frame] != ('packet_copy', 'master_packets'):
            raise ValueError('Night street is not an original packet')
    if by_role[FOIL] != ('packet_copy', 'master_packets'):
        raise ValueError('Frame 3353 is not an original packet')
    if by_role[mux.EXCLUDED_FRAME][0] != 'exact_pcm':
        raise ValueError('Frame 2869 is not an exact picture')
    if by_role[jar.JAR_BLOCKED][0] != 'exact_pcm':
        raise ValueError('Frame 3259 is not an exact picture')
    for frame in range(jar.JAR_FIRST, jar.JAR_LAST + 1):
        if by_role[frame] != ('packet_copy', 'jar_keep'):
            raise ValueError(f'Jar frame {frame} is not the packet copy')
    salon = [run for run in runs if run['first'] <= SALON[0] and run['last'] >= SALON[1]]
    if salon != [{'role': 'high_encode', 'first': SALON[0], 'last': SALON[1],
                  'frames': SALON[1] - SALON[0] + 1, 'clip': list(SALON)}]:
        raise ValueError('The salon row is not one 160-frame High encode')
    return by_role


def check_files(runs, encodes, exact_runs, jar_doc):
    """Sizes only. A missing file stays on disk as a failed check, not a master."""
    pieces = []
    for run in runs:
        if run['role'] == 'packet_copy' and run['clip'] == 'master_packets':
            continue
        if run['clip'] == 'jar_keep':
            record = jar_doc
            path = Path(record['clip'])
            expect = int(record['clip_bytes'])
        elif run['role'] == 'high_encode':
            record = encodes[tuple(run['clip'])]
            path = Path(record['encoded'])
            expect = int(record['encoded_bytes'])
        else:
            record = exact_runs[tuple(run['clip'])]
            path = Path(record['path'])
            expect = int(record['bytes'])
        if not path.is_file() or path.stat().st_size != expect:
            raise ValueError(f'{path} is missing or a different size from its record')
        pieces.append(str(path))
    return pieces


def build_map(review_dir=mux.REVIEW, timeline=None, check_media=False):
    review_dir = Path(review_dir)
    report = mux.build_report(review_dir)
    encodes, exact_runs, jar_doc = load_pieces(review_dir)
    owners = assign(report['envelopes'], encodes, exact_runs)
    runs = collapse(owners)
    _check_known(runs)
    counts = {role: 0 for role in ('packet_copy', 'high_encode', 'exact_pcm')}
    for run in runs:
        counts[run['role']] += run['frames']
    if sum(counts.values()) != mux.FRAME_COUNT:
        raise ValueError('Roles do not cover the master')
    if counts['exact_pcm'] != 139 or counts['packet_copy'] < 1:
        raise ValueError('Exact pictures are not the 139 blocked frames')
    clock = clock_summary(timeline) if timeline is not None else None
    if clock is not None and clock['frames'] != mux.FRAME_COUNT:
        raise ValueError('Source clock length is not the master frame count')
    media = check_files(runs, encodes, exact_runs, jar_doc) if check_media else []
    return {
        'job': 'J2242',
        'status': 'MUX_MAP_ONLY',
        'frames': mux.FRAME_COUNT,
        'runs': len(runs),
        'order': runs,
        'packet_copy_frames': counts['packet_copy'],
        'high_encode_frames': counts['high_encode'],
        'exact_pcm_frames': counts['exact_pcm'],
        'jar_keep': [jar.JAR_FIRST, jar.JAR_LAST],
        'frame_2869': 'exact_pcm',
        'frame_3259': 'exact_pcm',
        'frame_3353': 'packet_copy',
        'night_street': 'packet_copy',
        'salon_frames': [SALON[0], SALON[1]],
        'clock': clock,
        'media_files_checked': len(media),
        'timestamp_policy': 'copy original PTS and duration, including a gap; never setpts=N/24',
        'audio': 'OUTSTANDING',
        'output_film_created': False,
        'finished_master': False,
        'approval': False,
        'spend_gbp': 0,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', action='store_true')
    parser.add_argument('--review-dir', type=Path, default=mux.REVIEW)
    parser.add_argument('--timeline', type=Path)
    parser.add_argument('--check-media', action='store_true')
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    if not args.plan:
        parser.error('--plan is required; this tool does not mux')
    timeline = None
    if args.timeline:
        data = json.loads(args.timeline.read_text())
        if data.get('time_base') != '1/12288':
            raise ValueError('Source clock is not 1/12288')
        timeline = data['frames']
    report = build_map(args.review_dir, timeline, args.check_media)
    if args.out:
        refuse_master(args.out)
        mux.recipe.write_new(args.out, report)
    summary = {key: report[key] for key in (
        'status', 'frames', 'runs', 'packet_copy_frames', 'high_encode_frames',
        'exact_pcm_frames', 'frame_2869', 'frame_3259', 'frame_3353',
        'media_files_checked', 'output_film_created', 'finished_master')}
    if report['clock']:
        summary['ticks_1024'] = report['clock']['ticks_1024']
        summary['duration_ticks'] = report['clock']['duration_ticks']
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
