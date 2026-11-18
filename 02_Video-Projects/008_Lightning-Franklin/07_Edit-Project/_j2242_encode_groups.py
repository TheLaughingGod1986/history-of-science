"""Encode fully changed Franklin groups to H264 High. Never a v04 master.

x264 rejects lossless High profile (`high profile doesn't support lossless`).
The source master is High, and a 4:4:4 lossless patch broke later copied
packets under a default decode. This path is the salon experiment's
near-lossless High encode: qp 1, no B frames, one IDR per group.

A group that still contains master frames is refused. Those frames have to
match the source hashes exactly, and this encode is not lossless. Audio is
not muxed. Nothing here is named hos_008_master_v04.mp4.
"""
import argparse
import json
import math
import subprocess
import tempfile
from pathlib import Path

import _build_rough_v13_recipe as recipe
import _j2242_packet_mux as mux
import _j2242_stitch_groups as stitch

QP = 1
PROFILE = 'high'


def require_fully_changed(envelope):
    kept = envelope.get('stitch_source_frames') or []
    if not envelope.get('pixels_complete') or kept:
        raise ValueError(
            'Kept master frames cannot use the High-profile near-lossless encode')
    if envelope.get('changed_frames') != envelope.get('frames'):
        raise ValueError('Group is not fully changed')
    return envelope


def encode_args(source, output, frames):
    frames = int(frames)
    if frames < 1:
        raise ValueError('Group has no frames')
    output = Path(output)
    if 'master_v04' in output.name or output.suffix.lower() != '.mp4':
        raise ValueError('Encode target must be a group mp4, not a master')
    return [
        'ffmpeg', '-nostdin', '-v', 'error', '-xerror',
        '-i', str(source),
        '-map', '0:v:0', '-an',
        '-c:v', 'libx264', '-preset', 'fast', '-qp', str(QP),
        '-profile:v', PROFILE, '-pix_fmt', 'yuv420p',
        '-x264-params',
        f'bframes=0:repeat-headers=1:keyint={frames}:min-keyint={frames}:scenecut=0',
        '-fps_mode', 'passthrough', '-enc_time_base', '1/12288',
        '-video_track_timescale', '12288',
        '-n', str(output),
    ]


def single_nut(envelope, files):
    """One verified nut that already covers the whole closed group."""
    require_fully_changed(envelope)
    parts = stitch.drop_superseded(envelope['changed'])
    matched = [stitch._match(part, files) for part in parts]
    pieces = stitch.sequence(envelope['first'], envelope['last'], matched)
    if len(pieces) != 1 or pieces[0]['kind'] != 'intermediate':
        raise ValueError('This encode takes one nut that already covers the group')
    piece = pieces[0]
    if piece['first'] != envelope['first'] or piece['last'] != envelope['last']:
        raise ValueError('Nut does not cover the closed group')
    if not str(piece['path']).endswith('.nut'):
        raise ValueError('Source must be a nut intermediate')
    return piece


def minimum_psnr(reference, encoded, frames):
    with tempfile.TemporaryDirectory(prefix='j2242-encode-psnr-') as tmp:
        stats = Path(tmp) / 'psnr.txt'
        subprocess.run(
            ['ffmpeg', '-nostdin', '-v', 'error', '-xerror',
             '-i', str(reference), '-i', str(encoded),
             '-filter_complex',
             '[0:v]settb=1/12288,setpts=PTS-STARTPTS[a];'
             '[1:v]settb=1/12288,setpts=PTS-STARTPTS[b];'
             f'[a][b]psnr=stats_file={stats}',
             '-an', '-f', 'null', '-'],
            check=True)
        rows = [dict(item.split(':', 1) for item in line.split())
                for line in stats.read_text().splitlines() if line.strip()]
    if len(rows) != frames:
        raise ValueError(f'Quality comparison covered {len(rows)} frames, not {frames}')
    values = [float(row['psnr_avg']) for row in rows]
    if any(math.isnan(value) or value < 60 for value in values):
        raise ValueError('High-profile encode is below 60 dB on a frame')
    return min(values)


def probe_silent_high(path, frames):
    data = recipe.strict_json(
        ['ffprobe', '-v', 'error', '-count_packets', '-show_streams', '-of', 'json', str(path)])
    streams = data.get('streams') or []
    video = [item for item in streams if item.get('codec_type') == 'video']
    audio = [item for item in streams if item.get('codec_type') == 'audio']
    if len(video) != 1 or audio:
        raise ValueError('Encode must be one silent video stream')
    stream = video[0]
    if stream.get('codec_name') != 'h264' or stream.get('profile') != 'High':
        raise ValueError('Encode must be H264 High')
    if stream.get('pix_fmt') != 'yuv420p' or (stream.get('width'), stream.get('height')) != (1920, 1080):
        raise ValueError('Encode must stay 1080p yuv420p')
    counted = int(stream.get('nb_read_packets') or 0)
    if counted != frames:
        raise ValueError(f'Encode has {counted} packets, not {frames}')
    return stream


def source_is_yuv420p(path):
    data = recipe.strict_json(
        ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
         'stream=codec_name,pix_fmt,width,height', '-of', 'json', str(path)])
    stream = (data.get('streams') or [None])[0]
    if not stream or stream.get('pix_fmt') != 'yuv420p':
        raise ValueError('Source nut is not yuv420p')
    if (stream.get('width'), stream.get('height')) != (1920, 1080):
        raise ValueError('Source nut is not 1080p')
    return stream


def encode_piece(piece, first, last, out_dir, evidence_path, preparation='single-nut'):
    """Encode one yuv420p nut that already covers this closed group."""
    frames = last - first + 1
    if piece['first'] != first or piece['last'] != last:
        raise ValueError('Nut does not cover the closed group')
    if piece['last'] - piece['first'] + 1 != frames:
        raise ValueError('Nut frame count does not match the group')
    if preparation not in ('single-nut', 'existing-yuv420p', 'joined-yuv420p', 'yuv420p-view'):
        raise ValueError('Unknown nut preparation')
    recipe.require_hash(piece['path'], piece['sha256'])
    source_is_yuv420p(piece['path'])
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    output = out_dir / f'group_{first}_{last}_high.mp4'
    if output.exists():
        raise ValueError(f'Encode already exists: {output}')
    partial = output.with_suffix('.partial.mp4')
    if partial.exists():
        partial.unlink()
    try:
        subprocess.run(encode_args(piece['path'], partial, frames), check=True)
        recipe.require_hash(piece['path'], piece['sha256'])
        probe_silent_high(partial, frames)
        lowest = minimum_psnr(piece['path'], partial, frames)
    except Exception:
        partial.unlink(missing_ok=True)
        raise
    partial.rename(output)
    report = {
        'job': 'J2242',
        'status': 'HIGH_PROFILE_GROUP_ONLY',
        'row': piece.get('name'),
        'source': piece['source'],
        'first': first,
        'last': last,
        'frames': frames,
        'nut': piece['path'],
        'nut_sha256': piece['sha256'],
        'preparation': preparation,
        'encoded': str(output),
        'encoded_sha256': recipe.sha256_file(output),
        'encoded_bytes': output.stat().st_size,
        'profile': 'High',
        'qp': QP,
        'bframes': 0,
        'minimum_frame_psnr_db': lowest,
        'lossless': False,
        'audio': False,
        'master_clock': 'not on this file; the later mux copies original PTS',
        'kept_master_frames': False,
        'output_film_created': False,
        'finished_master': False,
        'approval': False,
        'spend_gbp': 0,
    }
    recipe.write_new(evidence_path, report)
    return report


def encode_group(envelope, files, out_dir, evidence_path):
    piece = single_nut(envelope, files)
    return encode_piece(
        piece, envelope['first'], envelope['last'], out_dir, evidence_path, 'single-nut')


def selectable(report):
    return [env for env in report['envelopes'] if env.get('pixels_complete')]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--group', type=int, help='first frame of one closed group')
    parser.add_argument('--single-nuts', action='store_true',
                        help='encode every fully changed group that is already one yuv420p nut')
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--review-dir', type=Path, default=mux.REVIEW)
    args = parser.parse_args()
    if bool(args.group is not None) == bool(args.single_nuts):
        parser.error('Choose exactly one of --group or --single-nuts')
    report = mux.build_report(args.review_dir)
    files = stitch.placed_files(args.review_dir)
    chosen = selectable(report)
    if args.group is not None:
        chosen = [env for env in chosen if env['first'] == args.group]
        if len(chosen) != 1:
            raise SystemExit(f'No fully changed group starts at {args.group}')
    written = skipped = 0
    for envelope in chosen:
        evidence = args.review_dir / f"ENCODE_{envelope['first']}_{envelope['last']}.json"
        if evidence.exists():
            print(f"skip {envelope['first']}-{envelope['last']}: evidence exists")
            skipped += 1
            continue
        try:
            piece = single_nut(envelope, files)
            source_is_yuv420p(piece['path'])
        except ValueError as exc:
            print(f"skip {envelope['first']}-{envelope['last']}: {exc}")
            skipped += 1
            continue
        result = encode_group(envelope, files, args.out_dir, evidence)
        written += 1
        print(json.dumps({
            'status': result['status'],
            'frames': result['frames'],
            'first': result['first'],
            'last': result['last'],
            'minimum_frame_psnr_db': result['minimum_frame_psnr_db'],
            'finished_master': False,
        }))
    if args.group is not None and written != 1:
        raise SystemExit('The named group was not encoded')
    print(json.dumps({'encoded': written, 'skipped': skipped, 'finished_master': False}))


if __name__ == '__main__':
    main()
