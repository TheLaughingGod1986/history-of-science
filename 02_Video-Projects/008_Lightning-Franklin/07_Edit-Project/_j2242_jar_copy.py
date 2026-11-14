"""Copy jar frames 3168-3258 as original master packets.

Frame 3259 is a B frame. It uses kept frame 3258 and replaced frame 3260,
so its original packet stays out. The 91 kept frames have to be a
decode-order prefix of their IDR group: they start on the in-band
SPS/PPS/IDR and they end before frame 3260. This writes a silent clip,
not hos_008_master_v04.mp4, and it does not touch the master.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import _build_rough_v13_recipe as recipe
import _j2242_ref_check as ref
from _j2242_salon_splice import check_headers

JAR_FIRST = 3168
JAR_LAST = 3258
JAR_BLOCKED = 3259
JAR_GROUP = (3168, 3343)
JAR_CHANGED = (3260, 3343)
JAR_MASTER = (3168, 3259)
PACKETS = Path('/Users/benjaminoats/_desk/state/J2242/source-preflight-v01/source_packets.json')
TIMELINE = Path('/Users/benjaminoats/_desk/state/J2242/source-preflight-v01/source_timeline.json')
FRAMEHASH = Path('/Users/benjaminoats/_desk/state/J2242/source-preflight-v01/source_decoded.framehash')


def assert_decode_prefix(kept, blocked):
    """Kept packets must be frames 3168-3258 and must end before frame 3259."""
    ordered = sorted(kept, key=lambda row: (row['dts'], row['index']))
    indexes = sorted(row['index'] for row in ordered)
    expect = list(range(JAR_FIRST, JAR_LAST + 1))
    if indexes != expect:
        raise ValueError('Jar copy is not exactly frames 3168-3258')
    if ordered[0]['index'] != JAR_FIRST:
        raise ValueError('Jar copy does not start at the IDR')
    for earlier, later in zip(ordered, ordered[1:]):
        if later['dts'] <= earlier['dts']:
            raise ValueError('Jar copy decode times are not increasing')
    if blocked['index'] != JAR_BLOCKED:
        raise ValueError('The blocked jar frame is not 3259')
    if any(row['index'] == JAR_BLOCKED for row in ordered):
        raise ValueError('Blocked frame 3259 was included')
    if blocked['dts'] <= ordered[-1]['dts']:
        raise ValueError('Blocked frame 3259 sits inside the jar copy')
    return ordered


def classify_jar(pictures):
    """The reference check has to agree before any packet is copied."""
    result = ref.classify_group(pictures, [JAR_MASTER], [JAR_CHANGED])
    if result['exact_runs'] != [(JAR_FIRST, JAR_LAST)]:
        raise ValueError(f"Jar exact run changed: {result['exact_runs']}")
    if result['blocked_runs'] != [(JAR_BLOCKED, JAR_BLOCKED)]:
        raise ValueError(f"Jar blocked run changed: {result['blocked_runs']}")
    return result


def parse_framehash(text):
    rows = []
    for line in text.splitlines():
        if not line or line.startswith('#'):
            continue
        stream, dts, pts, duration, size, digest = [part.strip() for part in line.split(',')]
        rows.append({
            'stream': int(stream),
            'dts': int(dts),
            'pts': int(pts),
            'duration': int(duration),
            'size': int(size),
            'hash': digest,
        })
    return rows


def match_hashes(source_rows, clip_rows, frames):
    """Every decoded clip frame must equal the master frame at the same PTS."""
    by_pts = {frame['pts']: frame for frame in frames}
    source = {row['pts']: row for row in source_rows}
    if len(clip_rows) != JAR_LAST - JAR_FIRST + 1:
        raise ValueError('Clip decoded the wrong number of frames')
    seen = set()
    for clip in clip_rows:
        frame = by_pts.get(clip['pts'])
        if frame is None or not (JAR_FIRST <= frame['index'] <= JAR_LAST):
            raise ValueError(f"Clip PTS {clip['pts']} is outside the jar keep")
        original = source.get(clip['pts'])
        if original is None:
            raise ValueError(f"No master hash at PTS {clip['pts']}")
        if clip['hash'] != original['hash'] or clip['duration'] != original['duration']:
            raise ValueError(f"Frame {frame['index']} does not match the master")
        if clip['size'] != original['size'] or clip['size'] != 1920 * 1080 * 3 // 2:
            raise ValueError(f"Frame {frame['index']} is not 1080p yuv420p")
        seen.add(frame['index'])
    if seen != set(range(JAR_FIRST, JAR_LAST + 1)):
        raise ValueError('A jar frame was missing from the decoded clip')
    return len(seen)


def _packet_row(index, packet):
    return {
        'index': index,
        'pts': int(packet['pts']),
        'dts': int(packet['dts']),
        'duration': int(packet['duration']),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--master', type=Path, default=recipe.DEFAULT_MASTER)
    parser.add_argument('--packets', type=Path, default=PACKETS)
    parser.add_argument('--timeline', type=Path, default=TIMELINE)
    parser.add_argument('--framehash', type=Path, default=FRAMEHASH)
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--review-dir', type=Path, default=ref.mux.REVIEW)
    args = parser.parse_args()
    import av
    from fractions import Fraction

    recipe.require_hash(args.master, recipe.MASTER_SHA, recipe.MASTER_BYTES)
    packet_json = json.loads(args.packets.read_text())
    timeline = json.loads(args.timeline.read_text())
    video = ref.load_packets(args.master, packet_json['packets'], timeline)
    master_bytes = args.master.read_bytes()
    if len(master_bytes) != recipe.MASTER_BYTES:
        raise ValueError('Master size changed while reading')
    pictures = ref.read_group(master_bytes, video, JAR_GROUP[0], JAR_GROUP[1], ref.PPS)
    classify_jar(pictures)
    kept = assert_decode_prefix(
        [_packet_row(index, video[index]) for index in range(JAR_FIRST, JAR_LAST + 1)],
        _packet_row(JAR_BLOCKED, video[JAR_BLOCKED]))
    opening = master_bytes[int(video[JAR_FIRST]['pos']):
                           int(video[JAR_FIRST]['pos']) + int(video[JAR_FIRST]['size'])]
    check_headers(opening, 4)
    if hashlib.sha256(opening).hexdigest() != video[JAR_FIRST]['data_hash'].split('SHA256:', 1)[1]:
        raise ValueError('IDR packet bytes do not match the probe hash')

    args.out_dir.mkdir(parents=True, exist_ok=False)
    clip = args.out_dir / 'jar_keep_3168_3258.mp4'
    by_pts = {frame['pts']: frame['index'] for frame in timeline['frames']}
    wanted = {row['index'] for row in kept}
    copied = []
    with av.open(str(args.master)) as source, av.open(
            str(clip), 'w', options={'avoid_negative_ts': 'disabled',
                                     'video_track_timescale': '12288'}) as out:
        stream = source.streams.video[0]
        if stream.time_base != Fraction(1, 12288):
            raise ValueError('Unexpected master timebase')
        target = out.add_stream_from_template(stream)
        for packet in source.demux(stream):
            if not packet.size:
                continue
            index = by_pts.get(int(packet.pts))
            if index not in wanted:
                continue
            payload = bytes(packet)
            if index == JAR_FIRST:
                check_headers(payload, 4)
            copied.append({
                'index': index,
                'pts': int(packet.pts),
                'dts': int(packet.dts),
                'duration': int(packet.duration),
                'sha256': hashlib.sha256(payload).hexdigest(),
            })
            packet.stream = target
            out.mux(packet)
    if [row['index'] for row in copied] != [row['index'] for row in kept]:
        raise ValueError('Mux order is not the master decode order')
    for row, original in zip(copied, kept):
        if (row['pts'], row['dts'], row['duration']) != (original['pts'], original['dts'], original['duration']):
            raise ValueError(f"Frame {row['index']} timestamp changed before mux")
        probed = video[row['index']]
        if row['sha256'] != probed['data_hash'].split('SHA256:', 1)[1]:
            raise ValueError(f"Frame {row['index']} packet bytes differ from the master")

    framehash = args.out_dir / 'jar_keep.framehash'
    subprocess.run([
        'ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-copyts', '-i', str(clip),
        '-map', '0:v:0', '-an', '-c:v', 'rawvideo', '-pix_fmt', 'yuv420p',
        '-fps_mode', 'passthrough', '-enc_time_base', '1/12288',
        '-f', 'framehash', '-hash', 'sha256', '-n', str(framehash),
    ], check=True)
    matched = match_hashes(
        parse_framehash(args.framehash.read_text()),
        parse_framehash(framehash.read_text()),
        timeline['frames'])
    recipe.require_hash(args.master, recipe.MASTER_SHA, recipe.MASTER_BYTES)
    report = {
        'job': 'J2242',
        'status': 'JAR_KEEP_PACKET_COPY',
        'clip': str(clip),
        'clip_sha256': recipe.sha256_file(clip),
        'clip_bytes': clip.stat().st_size,
        'frames': matched,
        'first': JAR_FIRST,
        'last': JAR_LAST,
        'blocked_frame': JAR_BLOCKED,
        'blocked_reason': 'Frame 3259 references kept frame 3258 and replaced frame 3260',
        'idr_in_band_sps_pps': True,
        'decoded_hashes_match_master': True,
        'audio': False,
        'finished_master': False,
        'approval': False,
        'spend_gbp': 0,
        'source_master_sha256': recipe.MASTER_SHA,
    }
    recipe.write_new(args.out_dir / 'JAR_COPY.json', report)
    recipe.write_new(args.review_dir / 'JAR_COPY.json', report)
    print(json.dumps({
        'frames': matched,
        'clip_sha256': report['clip_sha256'],
        'blocked_frame': JAR_BLOCKED,
        'finished_master': False,
    }, indent=2))


if __name__ == '__main__':
    main()
