"""One yuv420p nut for each fully changed Franklin group the encoder skipped.

The High-profile encode accepts one yuv420p nut that covers a closed group and
contains no master frames. These seven groups are fully changed and were
skipped for a narrower reason:

- 272–422 and 423–544 are two nuts each
- 2506–2665 is the salon nut, which is not in the placed-file list
- 8189–8268 and 8269–8348 split one electricity nut across two IDR groups
- 10777–10852 and 10996–11037 are bgr0 title nuts

A bgr0 nut is converted to the same yuv420p view the frame hasher already
uses, then checked against that view. Groups that still contain master frames
are refused. Nothing here is hos_008_master_v04.mp4, and nothing is lossless
High profile: x264 still rejects that.
"""
import argparse
import json
import subprocess
from pathlib import Path

import _build_rough_v13_recipe as recipe
import _j2242_encode_groups as enc
import _j2242_packet_mux as mux
import _j2242_stitch_groups as stitch
from _j2242_salon_patch import pixel_hashes

FRAME_BYTES = stitch.FRAME_BYTES
ALLOWED = ('yuv420p', 'bgr0')
# Fully changed groups the single-nut yuv420p pass could not encode.
TARGETS = (
    (272, 422),
    (423, 544),
    (2506, 2665),
    (8189, 8268),
    (8269, 8348),
    (10777, 10852),
    (10996, 11037),
)


def salon_file(review_dir):
    data = json.loads((Path(review_dir) / 'SALON_PATCH.json').read_text())
    if data.get('status') != 'SALON_INTERMEDIATE_ONLY' or data.get('frame_count') != 160:
        raise ValueError('Salon intermediate is not the 160-frame patch')
    path, digest = data.get('path'), data.get('sha256')
    if not path or not str(path).endswith('.nut') or not isinstance(digest, str) or len(digest) != 64:
        raise ValueError('Salon nut is missing a hash')
    return {
        'source': 'SALON_PATCH.json',
        'name': '02_salon_spark',
        'first': mux.SALON_FIRST,
        'last': mux.SALON_LAST,
        'path': str(path),
        'sha256': digest,
    }


def metal_file(review_dir):
    titles = json.loads((Path(review_dir) / 'TITLE_ROWS.json').read_text())
    row = next(item for item in titles['rows'] if item['row'] == '10_metal_easy')
    first, last = row['master_frames']
    if last - first + 1 != row['frames']:
        raise ValueError('Metal title nut is not its placed frame count')
    path, digest = row.get('intermediate'), row.get('sha256')
    if not path or not str(path).endswith('.nut') or not isinstance(digest, str) or len(digest) != 64:
        raise ValueError('Metal title nut is missing a hash')
    if first != 10996 or last != 11037:
        raise ValueError('Metal title is not frames 10996-11037')
    return {
        'source': 'TITLE_ROWS.json',
        'name': '10_metal_easy',
        'first': first,
        'last': last,
        'path': str(path),
        'sha256': digest,
    }


def source_files(review_dir):
    return stitch.placed_files(review_dir) + [salon_file(review_dir), metal_file(review_dir)]


def _slice(file_info, first, last):
    if file_info['first'] > first or file_info['last'] < last:
        raise ValueError('Nut does not cover the group')
    start = first - file_info['first']
    count = last - first + 1
    return {
        'kind': 'intermediate',
        'source': file_info['source'],
        'name': file_info['name'],
        'path': file_info['path'],
        'sha256': file_info['sha256'],
        'file_first': file_info['first'],
        'file_last': file_info['last'],
        'first': first,
        'last': last,
        'slice_first': start,
        'slice_count': count,
    }


def group_inputs(envelope, files):
    """Pieces that tile one fully changed group. No master frame is allowed."""
    enc.require_fully_changed(envelope)
    first, last = envelope['first'], envelope['last']
    parts = stitch.drop_superseded(envelope['changed'])
    try:
        matched = [stitch._match(part, files) for part in parts]
    except ValueError:
        matched = None
    if matched is not None:
        pieces = stitch.sequence(first, last, matched)
        if any(piece['kind'] != 'intermediate' for piece in pieces):
            raise ValueError('Fully changed group still needs master pixels')
        return [_slice(piece, piece['first'], piece['last']) for piece in pieces]
    if len(parts) != 1 or (parts[0]['first'], parts[0]['last']) != (first, last):
        raise ValueError('Unmatched pieces do not tile the group')
    part = parts[0]
    hits = [
        item for item in files
        if item['source'] == part['source'] and item['name'] == part['name']
        and item['first'] <= first and item['last'] >= last
    ]
    if len(hits) != 1:
        raise ValueError(f'Expected one covering nut for {part["source"]} {first}-{last}')
    return [_slice(hits[0], first, last)]


def target_groups(report, files):
    chosen = []
    for first, last in TARGETS:
        envelope = next(item for item in report['envelopes'] if item['first'] == first)
        if envelope['last'] != last or not envelope['pixels_complete']:
            raise ValueError(f'{first}-{last} is no longer a fully changed group')
        pieces = group_inputs(envelope, files)
        if any(piece['slice_count'] < 1 for piece in pieces):
            raise ValueError('Empty slice')
        covered = sum(piece['slice_count'] for piece in pieces)
        if covered != envelope['frames'] or mux.EXCLUDED_FRAME in range(first, last + 1):
            raise ValueError('Prepared group drops a frame or includes frame 2869')
        chosen.append({'first': first, 'last': last, 'frames': envelope['frames'], 'pieces': pieces})
    refused = [item['first'] for item in report['envelopes'] if not item['pixels_complete']]
    if refused != [2718, 3168, 4016, 11038]:
        raise ValueError('The groups that still hold master frames changed')
    return chosen


def _pix_fmt(path):
    data = recipe.strict_json([
        'ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'stream=pix_fmt,width,height', '-of', 'json', str(path)])
    stream = (data.get('streams') or [None])[0]
    if not stream or (stream.get('width'), stream.get('height')) != (1920, 1080):
        raise ValueError('Nut is not 1080p')
    fmt = stream.get('pix_fmt')
    if fmt not in ALLOWED:
        raise ValueError(f'Nut pixel format {fmt} is not yuv420p or bgr0')
    return fmt


def _yuv_raw(path):
    result = subprocess.run(
        ['ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-i', str(path),
         '-map', '0:v:0', '-an', '-c:v', 'rawvideo', '-pix_fmt', 'yuv420p',
         '-fps_mode', 'passthrough', '-f', 'rawvideo', 'pipe:1'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode or result.stderr.strip():
        raise RuntimeError(result.stderr.decode().strip() or f'YUV decode failed for {path}')
    if len(result.stdout) % FRAME_BYTES:
        raise ValueError(f'{path} did not decode to whole frames')
    return result.stdout


def _write_ffv1(raw, output):
    output = Path(output)
    if output.exists() or 'master_v04' in output.name:
        raise ValueError('Refusing to replace a nut or write a master')
    raw_path = output.with_suffix('.yuv')
    raw_path.write_bytes(raw)
    try:
        stitch._run([
            'ffmpeg', '-nostdin', '-v', 'error', '-xerror',
            '-f', 'rawvideo', '-pix_fmt', 'yuv420p', '-s', '1920x1080', '-r', '24',
            '-i', str(raw_path), '-an', '-c:v', 'ffv1', '-level', '3',
            '-pix_fmt', 'yuv420p', '-n', str(output),
        ])
    finally:
        raw_path.unlink(missing_ok=True)


def _reuse_existing(pieces):
    if len(pieces) != 1:
        return False
    piece = pieces[0]
    full = piece['slice_first'] == 0 and piece['slice_count'] == piece['file_last'] - piece['file_first'] + 1
    return full and _pix_fmt(piece['path']) == 'yuv420p'


def prepare_group(group, out_dir):
    pieces = group['pieces']
    for piece in pieces:
        recipe.require_hash(piece['path'], piece['sha256'])
    if _reuse_existing(pieces):
        piece = pieces[0]
        return {
            'first': group['first'],
            'last': group['last'],
            'frames': group['frames'],
            'path': piece['path'],
            'sha256': piece['sha256'],
            'preparation': 'existing-yuv420p',
            'source': piece['source'],
            'name': piece['name'],
            'yuv_view_matches_source': True,
            'kept_master_frames': False,
        }
    raw_parts = []
    expected = []
    formats = set()
    for piece in pieces:
        formats.add(_pix_fmt(piece['path']))
        raw = _yuv_raw(piece['path'])
        file_frames = piece['file_last'] - piece['file_first'] + 1
        if len(raw) != file_frames * FRAME_BYTES:
            raise ValueError(f'{piece["path"]} frame count does not match its timeline')
        start = piece['slice_first']
        count = piece['slice_count']
        raw_parts.append(raw[start * FRAME_BYTES:(start + count) * FRAME_BYTES])
        expected.extend(pixel_hashes(piece['path'])[start:start + count])
    if len(expected) != group['frames']:
        raise ValueError('Prepared hashes do not cover the group')
    output = Path(out_dir) / f"group_{group['first']}_{group['last']}.nut"
    _write_ffv1(b''.join(raw_parts), output)
    got = pixel_hashes(output)
    if got != expected:
        raise ValueError(f'{group["first"]}-{group["last"]} yuv view does not match its sources')
    joined = len(pieces) > 1 and formats == {'yuv420p'}
    return {
        'first': group['first'],
        'last': group['last'],
        'frames': group['frames'],
        'path': str(output),
        'sha256': recipe.sha256_file(output),
        'preparation': 'joined-yuv420p' if joined else 'yuv420p-view',
        'source': pieces[0]['source'] if len(pieces) == 1 else 'joined',
        'name': pieces[0]['name'] if len(pieces) == 1 else 'joined',
        'pieces': [
            {'source': piece['source'], 'name': piece['name'], 'first': piece['first'], 'last': piece['last']}
            for piece in pieces
        ],
        'yuv_view_matches_source': True,
        'kept_master_frames': False,
    }


def encode_prepared(prepared, out_dir, review_dir):
    review_dir = Path(review_dir)
    evidence = review_dir / f"ENCODE_{prepared['first']}_{prepared['last']}.json"
    if evidence.exists():
        raise ValueError(f'Encode evidence already exists: {evidence.name}')
    piece = {
        'path': prepared['path'],
        'sha256': prepared['sha256'],
        'source': prepared['source'],
        'name': prepared['name'],
        'first': prepared['first'],
        'last': prepared['last'],
    }
    return enc.encode_piece(
        piece, prepared['first'], prepared['last'], out_dir, evidence, prepared['preparation'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', action='store_true')
    parser.add_argument('--render', action='store_true')
    parser.add_argument('--encode', action='store_true')
    parser.add_argument('--review-dir', type=Path, default=mux.REVIEW)
    parser.add_argument('--out-dir', type=Path)
    parser.add_argument('--encode-dir', type=Path)
    args = parser.parse_args()
    if args.plan == (args.render or args.encode):
        parser.error('Choose --plan, or --render/--encode')
    report = mux.build_report(args.review_dir)
    groups = target_groups(report, source_files(args.review_dir))
    if args.plan:
        print(json.dumps({
            'groups': [(item['first'], item['last'], len(item['pieces'])) for item in groups],
            'kept_master_frames': False,
            'finished_master': False,
        }, indent=2))
        return
    if args.out_dir is None:
        parser.error('--render/--encode needs --out-dir')
    args.out_dir.mkdir(parents=True, exist_ok=True)
    prepared = [prepare_group(group, args.out_dir) for group in groups]
    recipe.write_new(args.out_dir / 'GROUP_NUTS.json', {
        'job': 'J2242',
        'status': 'GROUP_NUTS_ONLY',
        'groups': prepared,
        'kept_master_frames': False,
        'audio': False,
        'output_film_created': False,
        'finished_master': False,
        'approval': False,
        'spend_gbp': 0,
    })
    recipe.write_new(args.review_dir / 'GROUP_NUTS.json', {
        'job': 'J2242',
        'status': 'GROUP_NUTS_ONLY',
        'groups': prepared,
        'kept_master_frames': False,
        'audio': False,
        'output_film_created': False,
        'finished_master': False,
        'approval': False,
        'spend_gbp': 0,
    })
    encoded = []
    if args.encode:
        if args.encode_dir is None:
            parser.error('--encode needs --encode-dir')
        for item in prepared:
            encoded.append(encode_prepared(item, args.encode_dir, args.review_dir))
            print(json.dumps({
                'first': item['first'],
                'last': item['last'],
                'preparation': item['preparation'],
                'minimum_frame_psnr_db': encoded[-1]['minimum_frame_psnr_db'],
                'finished_master': False,
            }))
    print(json.dumps({
        'prepared': len(prepared),
        'encoded': len(encoded),
        'finished_master': False,
    }))


if __name__ == '__main__':
    main()
