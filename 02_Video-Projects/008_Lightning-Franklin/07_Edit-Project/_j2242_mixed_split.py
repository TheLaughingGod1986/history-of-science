"""Split the four mixed Franklin groups. Never a v04 master.

Each of these IDR groups holds replacement pictures and master frames
together. x264 will not make a lossless High-profile encode, and the source
master uses B-frames, so a kept frame can reference a frame this job
replaces. A High qp 1 encode of the whole group would give up the source
hash of those master frames. A 4:4:4 lossless patch already broke later
copied packets.

Changed runs are encoded with the existing High recipe, one closed GOP, no
B-frames, no audio. Master runs are not encoded. With B-frames in the
source they are not a safe packet copy either. Nothing here is
hos_008_master_v04.mp4.
"""
import argparse
import json
import subprocess
from pathlib import Path

import _build_rough_v13_recipe as recipe
import _j2242_encode_groups as enc
import _j2242_packet_mux as mux
from _j2242_salon_patch import pixel_hashes

MIXED = (
    (2718, 2887),
    (3168, 3343),
    (4016, 4138),
    (11038, 11245),
)
CHANGED = (
    (2718, 2868),
    (2870, 2887),
    (3260, 3343),
    (4016, 4129),
    (11038, 11117),
)
MASTER = (
    (2869, 2869),
    (3168, 3259),
    (4130, 4138),
    (11118, 11245),
)


def _run(pieces, kind):
    """Merge touching pieces of one kind. A master frame stays a break."""
    merged = []
    for piece in pieces:
        if piece['kind'] != kind:
            continue
        if piece['last'] < piece['first']:
            raise ValueError('Stitch piece runs backwards')
        if merged and piece['first'] == merged[-1]['last'] + 1:
            merged[-1]['last'] = piece['last']
        elif merged and piece['first'] <= merged[-1]['last']:
            raise ValueError('Stitch pieces overlap')
        else:
            merged.append({'first': piece['first'], 'last': piece['last']})
    for run in merged:
        run['frames'] = run['last'] - run['first'] + 1
    return merged


def partition(group):
    """Changed and master runs that tile one mixed group exactly."""
    pieces = group['pieces']
    if not pieces:
        raise ValueError('Mixed group has no stitch pieces')
    cursor = group['first']
    for piece in pieces:
        if piece['kind'] not in ('intermediate', 'master'):
            raise ValueError('Unknown stitch piece')
        if piece['first'] != cursor:
            raise ValueError('Stitch pieces leave a gap or overlap')
        cursor = piece['last'] + 1
    if cursor != group['last'] + 1:
        raise ValueError('Stitch pieces do not cover the group')
    changed = _run(pieces, 'intermediate')
    master = _run(pieces, 'master')
    covered = sum(item['frames'] for item in changed) + sum(item['frames'] for item in master)
    if covered != group['frames']:
        raise ValueError('Split dropped or repeated a frame')
    if any(item['first'] <= mux.EXCLUDED_FRAME <= item['last'] for item in changed):
        raise ValueError('Frame 2869 was put in a changed run')
    return changed, master


def load_groups(review_dir):
    data = json.loads((Path(review_dir) / 'STITCH_GROUPS.json').read_text())
    if data.get('status') != 'STITCH_INTERMEDIATE_ONLY' or data.get('finished_master'):
        raise ValueError('Stitch record is not an intermediate')
    groups = data['groups']
    found = [(item['first'], item['last']) for item in groups]
    if found != list(MIXED):
        raise ValueError('The four mixed groups changed')
    for group in groups:
        changed, master = partition(group)
        if [(item['first'], item['last']) for item in changed] != [
                pair for pair in CHANGED if group['first'] <= pair[0] <= group['last']]:
            raise ValueError(f"Changed runs drifted in {group['first']}")
        if [(item['first'], item['last']) for item in master] != [
                pair for pair in MASTER if group['first'] <= pair[0] <= group['last']]:
            raise ValueError(f"Master runs drifted in {group['first']}")
    return groups


def changed_envelope(run):
    frames = run['frames']
    return {
        'pixels_complete': True,
        'stitch_source_frames': [],
        'changed_frames': frames,
        'frames': frames,
    }


def master_envelope(run):
    return {
        'pixels_complete': False,
        'stitch_source_frames': [[run['first'], run['last']]],
        'changed_frames': 0,
        'frames': run['frames'],
    }


def master_disposition(run, group_first, has_b_frames):
    """Master frames stay out of the High encode.

    Packet copy is only even a candidate when the source has no B-frames and
    the run starts on the group's IDR, so nothing in it has to look forward
    into a replaced frame. This source has B-frames, and the other three
    runs do not start on the IDR. Neither case is encoded here.
    """
    if not isinstance(has_b_frames, int) or has_b_frames < 0:
        raise ValueError('B-frame count is missing')
    if has_b_frames:
        return 'blocked_by_b_frames'
    if run['first'] == group_first:
        return 'packet_copy'
    return 'needs_new_idr'


def source_b_frames(path):
    data = recipe.strict_json([
        'ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'stream=has_b_frames,profile', '-of', 'json', str(path)])
    stream = (data.get('streams') or [None])[0]
    if not stream or stream.get('profile') != 'High':
        raise ValueError('Source master is not H264 High')
    count = stream.get('has_b_frames')
    if not isinstance(count, int) or count < 0:
        raise ValueError('Source B-frame count is missing')
    return count


def plan(groups, has_b_frames):
    rows = []
    for group in groups:
        changed, master = partition(group)
        for run in changed:
            enc.require_fully_changed(changed_envelope(run))
            rows.append({
                'role': 'changed',
                'first': run['first'],
                'last': run['last'],
                'frames': run['frames'],
                'group': group['first'],
                'slice_first': run['first'] - group['first'],
                'nut': group['path'],
                'nut_sha256': group['sha256'],
                'disposition': 'high_qp1',
            })
        for run in master:
            with _raises(ValueError):
                enc.require_fully_changed(master_envelope(run))
            rows.append({
                'role': 'master',
                'first': run['first'],
                'last': run['last'],
                'frames': run['frames'],
                'group': group['first'],
                'disposition': master_disposition(run, group['first'], has_b_frames),
            })
    changed_rows = [row for row in rows if row['role'] == 'changed']
    if [(row['first'], row['last']) for row in changed_rows] != list(CHANGED):
        raise ValueError('Changed encode list drifted')
    if [(row['first'], row['last']) for row in rows if row['role'] == 'master'] != list(MASTER):
        raise ValueError('Master list drifted')
    if any(row['disposition'] == 'high_qp1' and row['role'] != 'changed' for row in rows):
        raise ValueError('A master run was marked for the High encode')
    return rows


class _raises:
    def __init__(self, kind):
        self.kind = kind

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            raise ValueError('Master run was accepted by the High encode')
        if not issubclass(exc_type, self.kind):
            return False
        return True


def slice_nut(source, start, count, output):
    output = Path(output)
    if output.exists() or 'master_v04' in output.name or output.suffix != '.nut':
        raise ValueError('Refusing to replace a nut or write a master')
    if start < 0 or count < 1:
        raise ValueError('Slice is empty')
    filt = f'trim=start_frame={start}:end_frame={start + count},setpts=PTS-STARTPTS'
    result = subprocess.run(
        ['ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-i', str(source),
         '-map', '0:v:0', '-an', '-vf', filt, '-frames:v', str(count),
         '-c:v', 'ffv1', '-level', '3', '-pix_fmt', 'yuv420p', '-n', str(output)],
        stderr=subprocess.PIPE)
    if result.returncode:
        output.unlink(missing_ok=True)
        raise RuntimeError(result.stderr.decode().strip() or 'Slice failed')
    expected = pixel_hashes(source, filters=filt)
    got = pixel_hashes(output)
    if got != expected or len(got) != count:
        output.unlink(missing_ok=True)
        raise ValueError(f'Slice does not match nut frames {start}..{start + count - 1}')
    return got


def encode_changed(rows, out_dir, encode_dir, review_dir):
    out_dir = Path(out_dir)
    encode_dir = Path(encode_dir)
    review_dir = Path(review_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for row in rows:
        if row['role'] != 'changed' or row['disposition'] != 'high_qp1':
            raise ValueError('Refusing to encode a master run')
        if row['first'] <= mux.EXCLUDED_FRAME <= row['last']:
            raise ValueError('Frame 2869 was put in a changed run')
        recipe.require_hash(row['nut'], row['nut_sha256'])
        nut = out_dir / f"group_{row['first']}_{row['last']}.nut"
        slice_nut(row['nut'], row['slice_first'], row['frames'], nut)
        piece = {
            'path': str(nut),
            'sha256': recipe.sha256_file(nut),
            'source': 'STITCH_GROUPS.json',
            'name': f"mixed_{row['first']}_{row['last']}",
            'first': row['first'],
            'last': row['last'],
        }
        evidence = review_dir / f"ENCODE_{row['first']}_{row['last']}.json"
        report = enc.encode_piece(
            piece, row['first'], row['last'], encode_dir, evidence, 'yuv420p-view')
        if report.get('kept_master_frames') or report.get('finished_master'):
            raise ValueError('Encode report claims a master')
        written.append(report)
    return written


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', action='store_true')
    parser.add_argument('--encode', action='store_true')
    parser.add_argument('--review-dir', type=Path, default=mux.REVIEW)
    parser.add_argument('--master', type=Path, default=recipe.DEFAULT_MASTER)
    parser.add_argument('--out-dir', type=Path)
    parser.add_argument('--encode-dir', type=Path)
    args = parser.parse_args()
    if args.plan == args.encode:
        parser.error('Choose exactly one of --plan or --encode')
    groups = load_groups(args.review_dir)
    has_b_frames = source_b_frames(args.master)
    rows = plan(groups, has_b_frames)
    if args.plan:
        recipe.write_new(args.review_dir / 'MIXED_SPLIT.json', {
            'job': 'J2242',
            'status': 'MIXED_SPLIT_PLAN',
            'source_has_b_frames': has_b_frames,
            'rows': rows,
            'encoded_master_frames': False,
            'audio': False,
            'output_film_created': False,
            'finished_master': False,
            'approval': False,
            'spend_gbp': 0,
        })
        print(json.dumps({
            'changed': [(row['first'], row['last']) for row in rows if row['role'] == 'changed'],
            'master': [(row['first'], row['last'], row['disposition'])
                       for row in rows if row['role'] == 'master'],
            'finished_master': False,
        }, indent=2))
        return
    if args.out_dir is None or args.encode_dir is None:
        parser.error('--encode needs --out-dir and --encode-dir')
    written = encode_changed(
        [row for row in rows if row['role'] == 'changed'],
        args.out_dir, args.encode_dir, args.review_dir)
    print(json.dumps({
        'encoded': [(item['first'], item['last'], item['minimum_frame_psnr_db']) for item in written],
        'master_frames_encoded': False,
        'finished_master': False,
    }))


if __name__ == '__main__':
    main()
