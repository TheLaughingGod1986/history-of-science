"""Stitch master pixels into the three incomplete Franklin picture groups.

A changed frame forces its whole IDR group to be re-encoded. Thirty-two groups
already have a picture for every frame. These three do not:

- 2718–2887, where frame 2869 stays the master picture
- 3168–3343, where 3168–3259 stay the master picture ahead of the jar patch
- 11038–11245, where the one-title safe path covers 11038–11117 and
  11118–11245 stay the master picture

The earlier safe-path intermediate still has two titles, so it is not used.
This writes lossless picture groups only. It does not mux, copy audio, or
make hos_008_master_v04.mp4.
"""
import argparse
import json
import subprocess
from pathlib import Path

import _build_rough_v13_recipe as recipe
import _j2242_packet_mux as mux
from _j2242_salon_patch import pixel_hashes

FRAMEHASH = Path('/Users/benjaminoats/_desk/state/J2242/source-preflight-v01/source_decoded.framehash')
FRAMEHASH_SHA = '7efa1f043cdf1ba83c87eef97a4e60e24904ac6d606336f17663d8054b150b65'
# The first safe-path render still shows the card's own title as well as the
# bottom card. The title fix replaces that exact window.
SUPERSEDED = {
    ('SAFE_PATH.json', 11038, 11117): ('SAFE_PATH_TITLE.json', 11038, 11117),
}


def _key(part):
    return (part['source'], part['first'], part['last'])


def drop_superseded(parts):
    """Remove an earlier intermediate only when its replacement is present."""
    present = {_key(part) for part in parts}
    drop = set()
    for old, new in SUPERSEDED.items():
        if old in present and new not in present:
            raise ValueError('The one-title safe path is missing')
        if old in present and new in present:
            drop.add(old)
    return [part for part in parts if _key(part) not in drop]


def sequence(first, last, parts):
    """Order intermediates and fill every gap with master frames."""
    if not isinstance(first, int) or not isinstance(last, int) or last < first:
        raise ValueError('Group bounds are not a frame range')
    kept = drop_superseded(parts)
    ordered = sorted(kept, key=lambda part: (part['first'], part['last'], part['source']))
    pieces = []
    cursor = first
    for part in ordered:
        lo, hi = part['first'], part['last']
        if not isinstance(lo, int) or not isinstance(hi, int) or hi < lo:
            raise ValueError('Intermediate is not a frame range')
        if lo < cursor or hi > last:
            raise ValueError('Intermediate overlaps or leaves the group')
        if lo > cursor:
            pieces.append({'kind': 'master', 'first': cursor, 'last': lo - 1})
        piece = {
            'kind': 'intermediate',
            'first': lo,
            'last': hi,
            'source': part['source'],
        }
        for field in ('path', 'sha256', 'name'):
            if field in part:
                piece[field] = part[field]
        pieces.append(piece)
        cursor = hi + 1
    if cursor <= last:
        pieces.append({'kind': 'master', 'first': cursor, 'last': last})
        cursor = last + 1
    if cursor != last + 1:
        raise ValueError('Group was not filled')
    covered = 0
    for piece in pieces:
        covered += piece['last'] - piece['first'] + 1
        if mux.EXCLUDED_FRAME >= piece['first'] and mux.EXCLUDED_FRAME <= piece['last']:
            if piece['kind'] != 'master':
                raise ValueError('Frame 2869 must stay the master picture')
        if _overlaps_night(piece):
            raise ValueError('0:51 night street stays a copied packet')
    if covered != last - first + 1:
        raise ValueError('Stitch counted a frame twice or dropped one')
    return pieces


def _overlaps_night(piece):
    return mux._overlaps(piece['first'], piece['last'], *mux.NIGHT_STREET)


def _files(data, source):
    found = []

    def walk(obj):
        if isinstance(obj, dict):
            frames = obj.get('timeline_frames')
            path = obj.get('path')
            status = str(obj.get('status', ''))
            if (path and str(path).endswith('.nut') and 'REJECTED' not in status
                    and isinstance(frames, list) and len(frames) == 2
                    and all(isinstance(n, int) for n in frames)):
                digest = obj.get('sha256')
                if not isinstance(digest, str) or len(digest) != 64:
                    raise ValueError(f'Missing hash for {path}')
                found.append({
                    'source': source,
                    'name': obj.get('row') or status or source,
                    'first': frames[0],
                    'last': frames[1],
                    'path': str(path),
                    'sha256': digest,
                })
            for value in obj.values():
                walk(value)
        elif isinstance(obj, list):
            for value in obj:
                walk(value)

    walk(data)
    return found


def placed_files(review_dir):
    review_dir = Path(review_dir)
    found = []
    for name in mux.SPAN_FILES:
        found.extend(_files(json.loads((review_dir / name).read_text()), name))
    return found


def _match(part, files):
    hits = [item for item in files if _key(item) == _key(part)]
    if len(hits) != 1:
        raise ValueError(f'Expected one file for {part["source"]} {part["first"]}-{part["last"]}')
    return hits[0]


def partial_groups(report, review_dir):
    files = placed_files(review_dir)
    groups = []
    for env in report['envelopes']:
        if env['pixels_complete']:
            continue
        matched = [_match(part, files) for part in drop_superseded(env['changed'])]
        pieces = sequence(env['first'], env['last'], matched)
        groups.append({
            'first': env['first'],
            'last': env['last'],
            'frames': env['frames'],
            'pieces': pieces,
        })
    return groups


def load_source_rows(path=FRAMEHASH):
    recipe.require_hash(path, FRAMEHASH_SHA)
    rows = []
    for line in Path(path).read_text().splitlines():
        if not line or line.startswith('#'):
            continue
        parts = [item.strip() for item in line.split(',')]
        if len(parts) != 6:
            raise ValueError('Unexpected source framehash row')
        rows.append({'pts': int(parts[2]), 'duration': int(parts[3]), 'hash': parts[5]})
    if len(rows) != mux.FRAME_COUNT:
        raise ValueError('Source framehash is not the master frame count')
    return rows


def _run(command):
    result = subprocess.run(command, check=False, text=True, stderr=subprocess.PIPE)
    if result.returncode or result.stderr.strip():
        raise RuntimeError(result.stderr.strip() or f'ffmpeg exited {result.returncode}')


def extract_master(master, ranges, outputs):
    """Decode the named master ranges once and write one lossless file each."""
    if len(ranges) != len(outputs) or not ranges:
        raise ValueError('Master extract ranges do not match the outputs')
    labels = ''.join(f'[s{i}]' for i in range(len(ranges)))
    filters = [f'[0:v]split={len(ranges)}{labels}']
    for i, (first, last) in enumerate(ranges):
        if first == last:
            choice = f'eq(n\\,{first})'
        else:
            choice = f'between(n\\,{first}\\,{last})'
        filters.append(f"[s{i}]select='{choice}',format=yuv420p,setpts=N/24/TB[o{i}]")
    command = [
        'ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-i', str(master),
        '-filter_complex', ';'.join(filters),
    ]
    for i, output in enumerate(outputs):
        command += [
            '-map', f'[o{i}]', '-an', '-c:v', 'ffv1', '-level', '3',
            '-pix_fmt', 'yuv420p', '-n', str(output),
        ]
    _run(command)


FRAME_BYTES = 1920 * 1080 * 3 // 2


def _decode_raw(path):
    """Decoded YUV420P bytes. A timestamp join dropped a frame, so this does not use one."""
    result = subprocess.run(
        ['ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-i', str(path),
         '-map', '0:v:0', '-an', '-f', 'rawvideo', '-pix_fmt', 'yuv420p', 'pipe:1'],
        check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode or result.stderr.strip():
        raise RuntimeError(result.stderr.decode().strip() or f'Raw decode failed for {path}')
    if len(result.stdout) % FRAME_BYTES:
        raise ValueError(f'{path} did not decode to whole frames')
    return result.stdout


def concat_pieces(paths, output):
    """Join pictures in order by raw frames. Source durations cannot drop one."""
    if len(paths) < 2:
        raise ValueError('A stitch needs the master frames and the replacement')
    raw_path = Path(str(output) + '.yuv')
    frames = 0
    with raw_path.open('wb') as raw:
        for path in paths:
            chunk = _decode_raw(path)
            frames += len(chunk) // FRAME_BYTES
            raw.write(chunk)
    if raw_path.stat().st_size != frames * FRAME_BYTES:
        raise ValueError('Raw stitch changed size while it was written')
    try:
        _run([
            'ffmpeg', '-nostdin', '-v', 'error', '-xerror',
            '-f', 'rawvideo', '-pix_fmt', 'yuv420p', '-s', '1920x1080', '-r', '24',
            '-i', str(raw_path), '-an', '-c:v', 'ffv1', '-level', '3',
            '-pix_fmt', 'yuv420p', '-n', str(output),
        ])
    finally:
        if output.exists() and raw_path.exists():
            raw_path.unlink()


def _master_ranges(groups):
    ranges = []
    for group in groups:
        for piece in group['pieces']:
            if piece['kind'] == 'master':
                ranges.append((piece['first'], piece['last']))
    if ranges != sorted(ranges):
        raise ValueError('Master ranges are not in timeline order')
    return ranges


def _check_hashes(measured, expected, label):
    if measured != expected:
        raise ValueError(f'{label} pixels do not match ({len(measured)} frames, expected {len(expected)})')


def render(groups, out_dir, master=recipe.DEFAULT_MASTER):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=False)
    recipe.require_hash(master, recipe.MASTER_SHA, recipe.MASTER_BYTES)
    rows = load_source_rows()
    ranges = _master_ranges(groups)
    extracts = [out_dir / f'master_{lo}-{hi}.nut' for lo, hi in ranges]
    extract_master(master, ranges, extracts)
    extract_hashes = {}
    for (lo, hi), path in zip(ranges, extracts):
        measured = pixel_hashes(path)
        expected = [rows[i]['hash'] for i in range(lo, hi + 1)]
        _check_hashes(measured, expected, f'Master {lo}-{hi}')
        extract_hashes[(lo, hi)] = measured
    rendered = []
    for group in groups:
        inputs = []
        expected = []
        for piece in group['pieces']:
            if piece['kind'] == 'master':
                key = (piece['first'], piece['last'])
                inputs.append(extracts[ranges.index(key)])
                expected.extend(extract_hashes[key])
            else:
                recipe.require_hash(piece['path'], piece['sha256'])
                inputs.append(piece['path'])
                expected.extend(pixel_hashes(piece['path']))
        if len(expected) != group['frames']:
            raise ValueError('Piece hashes do not cover the group')
        video = out_dir / f"group_{group['first']}-{group['last']}.nut"
        concat_pieces(inputs, video)
        measured = pixel_hashes(video)
        _check_hashes(measured, expected, f"Group {group['first']}-{group['last']}")
        clock_frames = [
            {'index': i, 'pts': rows[i]['pts'], 'duration': rows[i]['duration']}
            for i in range(group['first'], group['last'] + 1)
        ]
        clock = out_dir / f"group_{group['first']}-{group['last']}_clock.json"
        recipe.write_new(clock, {'time_base': '1/12288', 'frames': clock_frames})
        rendered.append({
            'first': group['first'],
            'last': group['last'],
            'frames': group['frames'],
            'path': str(video),
            'sha256': recipe.sha256_file(video),
            'clock': str(clock),
            'clock_sha256': recipe.sha256_file(clock),
            'pieces': [
                {key: piece[key] for key in ('kind', 'first', 'last', 'source') if key in piece}
                for piece in group['pieces']
            ],
            'master_pixels_match': True,
            'replacement_pixels_kept': True,
        })
        for piece in group['pieces']:
            if piece['kind'] != 'intermediate':
                continue
            recipe.require_hash(piece['path'], piece['sha256'])
    recipe.require_hash(master, recipe.MASTER_SHA, recipe.MASTER_BYTES)
    return rendered


def build_report(review_dir=mux.REVIEW):
    report = mux.build_report(review_dir)
    groups = partial_groups(report, review_dir)
    expected = [(2718, 2887), (3168, 3343), (11038, 11245)]
    if [(g['first'], g['last']) for g in groups] != expected:
        raise ValueError('The incomplete groups changed')
    master = next(piece for piece in groups[0]['pieces'] if piece['first'] <= 2869 <= piece['last'])
    if (master['kind'], master['first'], master['last']) != ('master', 2869, 2869):
        raise ValueError('Frame 2869 is not the master stitch')
    if groups[2]['pieces'][0].get('source') != 'SAFE_PATH_TITLE.json':
        raise ValueError('Safe path is not the one-title intermediate')
    return {
        'job': 'J2242',
        'status': 'STITCH_PLAN_ONLY',
        'groups': groups,
        'frame_2869': 'master pixels inside 2718-2887',
        'safe_path': 'SAFE_PATH_TITLE.json',
        'superseded': 'SAFE_PATH.json',
        'night_street': report['night_street'],
        'foil_frame_3353': report['foil_frame_3353'],
        'h264_packets': 'OUTSTANDING',
        'output_film_created': False,
        'finished_master': False,
        'approval': False,
        'spend_gbp': 0,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', action='store_true')
    parser.add_argument('--render', action='store_true')
    parser.add_argument('--review-dir', type=Path, default=mux.REVIEW)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    if args.plan == args.render:
        parser.error('Choose either --plan or --render')
    if args.render:
        if args.out is None:
            parser.error('--render needs --out')
        groups = partial_groups(mux.build_report(args.review_dir), args.review_dir)
        rendered = render(groups, args.out)
        recipe.write_new(args.out / 'STITCH_GROUPS.json', {
            'job': 'J2242',
            'status': 'STITCH_INTERMEDIATE_ONLY',
            'groups': rendered,
            'frame_2869': 'master pixels',
            'safe_path': 'SAFE_PATH_TITLE.json',
            'superseded': 'SAFE_PATH.json',
            'audio': False,
            'h264_packets': 'OUTSTANDING',
            'output_film_created': False,
            'finished_master': False,
            'approval': False,
            'spend_gbp': 0,
        })
        print(json.dumps({
            'status': 'STITCH_INTERMEDIATE_ONLY',
            'groups': len(rendered),
            'output_film_created': False,
        }, indent=2))
        return
    report = build_report(args.review_dir)
    if args.out:
        recipe.write_new(args.out, report)
    print(json.dumps({
        'status': report['status'],
        'groups': [(g['first'], g['last']) for g in report['groups']],
        'frame_2869': report['frame_2869'],
        'safe_path': report['safe_path'],
        'output_film_created': False,
    }, indent=2))


if __name__ == '__main__':
    main()
