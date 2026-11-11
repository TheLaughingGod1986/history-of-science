"""Read-only source evidence for J2242. Does not assemble or approve a film."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import _build_rough_v13_recipe as recipe


def nal_types(data, length_size):
    """Parse actual MP4 AVC sample lengths; reject truncated samples."""
    result = []
    offset = 0
    while offset < len(data):
        if len(data) - offset < length_size:
            raise ValueError('Truncated NAL length')
        size = int.from_bytes(data[offset:offset + length_size], 'big')
        offset += length_size
        if size < 1 or offset + size > len(data):
            raise ValueError('Invalid NAL payload length')
        result.append(data[offset] & 31)
        offset += size
    return result


def probe_packets(master):
    return recipe.strict_json([
        'ffprobe', '-v', 'error', '-show_packets', '-show_streams',
        '-show_data_hash', 'sha256', '-show_entries',
        'stream=index,codec_type,codec_name,time_base,nal_length_size,is_avc:'
        'packet=stream_index,pts,dts,duration,size,pos,flags,data_hash,side_data_list',
        '-of', 'json', str(master)])


def inspect_packets(master, probe, timeline):
    streams = probe['streams']
    video = [s for s in streams if s['codec_type'] == 'video']
    audio = [s for s in streams if s['codec_type'] == 'audio']
    if len(video) != 1 or len(audio) != 1:
        raise ValueError('Expected one video and one original audio stream')
    video, audio = video[0], audio[0]
    if video['codec_name'] != 'h264' or video['is_avc'] != 'true':
        raise ValueError('Only length-prefixed H.264 is supported')
    if video['time_base'] != timeline['time_base']:
        raise ValueError('Packet/frame timebase differs')
    frame_by_pts = {f['pts']: f for f in timeline['frames']}
    seen = set()
    idrs = []
    with Path(master).open('rb') as source:
        for packet in probe['packets']:
            if packet['stream_index'] != video['index']:
                continue
            pts = int(packet['pts'])
            if pts in seen or pts not in frame_by_pts:
                raise ValueError('Duplicate or unmapped video packet PTS')
            seen.add(pts)
            source.seek(int(packet['pos']))
            payload = source.read(int(packet['size']))
            if 'SHA256:' + hashlib.sha256(payload).hexdigest() != packet['data_hash']:
                raise ValueError('Actual packet bytes differ from probe hash')
            types = nal_types(payload, int(video['nal_length_size']))
            slices = set(types) & {1, 2, 3, 4, 5}
            if not slices:
                raise ValueError('Video sample contains no VCL slice')
            idr = slices == {5}
            key = bool(frame_by_pts[pts]['key_frame'])
            if idr != key or ('K' in packet['flags']) != key:
                raise ValueError('Keyframe flag is not an actual all-IDR sample')
            if idr:
                idrs.append(frame_by_pts[pts]['index'])
    if len(seen) != recipe.EXPECTED_FRAMES:
        raise ValueError('Packet/frame count mismatch')
    # IDR flushes prior reference pictures. Every start of an unchanged run
    # must be IDR; key flags alone never establish this property.
    if set(idrs) != {f['index'] for f in timeline['frames'] if f['key_frame']}:
        raise ValueError('Random-access points do not match decoded frame map')
    return {'video_packets': len(seen), 'idr_frame_indices': sorted(idrs),
            'all_random_access_samples_are_idr': True,
            'audio_packets': sum(p['stream_index'] == audio['index'] for p in probe['packets']),
            'note': 'Source reference reset proven by actual IDR NALs. Future splice decode, unchanged-frame equality, audio equality and sync remain required.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--master', type=Path, default=recipe.DEFAULT_MASTER)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    recipe.require_hash(args.master, recipe.MASTER_SHA, recipe.MASTER_BYTES)
    timeline = recipe.probe_video(args.master, recipe.EXPECTED_FRAMES)
    probe = probe_packets(args.master)
    result = inspect_packets(args.master, probe, timeline)
    recipe.write_new(args.out / 'source_packets.json', probe)
    recipe.write_new(args.out / 'source_timeline.json', timeline)
    # Raw decoded YUV420P hashes, at original integer PTS/duration. No fps filter,
    # timestamp reconstruction, output film, or changes to the source.
    subprocess.run([
        'ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-copyts', '-i', str(args.master),
        '-map', '0:v:0', '-an', '-c:v', 'rawvideo', '-pix_fmt', 'yuv420p',
        '-fps_mode', 'passthrough', '-enc_time_base', timeline['time_base'],
        '-f', 'framehash', '-hash', 'sha256', '-n',
        str(args.out / 'source_decoded.framehash')], check=True)
    lines = (args.out / 'source_decoded.framehash').read_text().splitlines()
    rows = [[part.strip() for part in line.split(',')]
            for line in lines if line and not line.startswith('#')]
    if len(rows) != len(timeline['frames']):
        raise ValueError('Decoded hash frame count mismatch')
    for row, frame in zip(rows, timeline['frames']):
        if int(row[2]) != frame['pts'] or int(row[3]) != frame['duration']:
            raise ValueError('Decoded hash PTS/duration differs from original')
    result.update(master_sha256=recipe.MASTER_SHA, source_decoded_hashes=len(rows),
                  source_integer_pts_and_durations_verified=True,
                  output_film_created=False, output_preservation='UNMEASURED',
                  output_vo_sync='UNMEASURED', media_perception=False)
    recipe.write_new(args.out / 'RESULT.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
