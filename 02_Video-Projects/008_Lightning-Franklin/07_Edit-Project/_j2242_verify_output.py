"""Verify J2242 preservation against pinned source evidence; no approval or muxing.

The change contract declares inclusive modified frame ranges separately from
inclusive re-encoded GOP envelopes. Both are required, even if empty. Frames
outside modifications must decode identically, including within envelopes.
"""
import argparse
import json
import re
import subprocess
from pathlib import Path

import _build_rough_v13_recipe as recipe
from _j2242_source_preflight import probe_packets


def ranges(raw, count):
    result = set()
    previous = -1
    for pair in raw:
        if (not isinstance(pair, list) or len(pair) != 2 or
                any(type(n) is not int for n in pair)):
            raise ValueError('Ranges must be inclusive integer pairs')
        first, last = pair
        if not 0 <= first <= last < count or first <= previous:
            raise ValueError('Ranges must be sorted, disjoint and inside source')
        result.update(range(first, last + 1))
        previous = last
    return result


def parse_hashes(text):
    if '#tb 0: 1/12288' not in text.splitlines():
        raise ValueError('Decoded hashes must use original integer timebase')
    result = []
    for line in text.splitlines():
        if not line or line.startswith('#'):
            continue
        row = [s.strip() for s in line.split(',')]
        if len(row) != 6 or row[0] != '0' or not re.fullmatch(r'[0-9a-f]{64}', row[5]):
            raise ValueError('Invalid decoded hash row')
        result.append((int(row[2]), int(row[3]), int(row[4]), row[5]))
    if not result or len({r[0] for r in result}) != len(result):
        raise ValueError('Missing or duplicate decoded frames')
    return result


def stream(probe, kind):
    streams = [s for s in probe['streams'] if s['codec_type'] == kind]
    if len(streams) != 1:
        raise ValueError('Expected exactly one ' + kind + ' stream')
    return streams[0]


def packets(probe, kind):
    index = stream(probe, kind)['index']
    keys = ('pts', 'dts', 'duration', 'size', 'data_hash', 'flags', 'side_data_list')
    return [{k: p[k] for k in keys if k in p}
            for p in probe['packets'] if p['stream_index'] == index]


def verify(source_timeline, source_probe, source_hashes, output_timeline,
           output_probe, output_hashes, contract, idrs):
    frames = source_timeline['frames']
    count = len(frames)
    modified = ranges(contract['modified_frames'], count)
    encoded = ranges(contract['encoded_envelopes'], count)
    if not modified <= encoded:
        raise ValueError('Modified frame lies outside encoded envelopes')
    for first, last in contract['encoded_envelopes']:
        if first not in idrs or (last + 1 < count and last + 1 not in idrs):
            raise ValueError('Envelope does not meet source IDR boundaries')
    if (output_timeline['time_base'] != source_timeline['time_base'] or
            [(f['pts'], f['duration']) for f in output_timeline['frames']] !=
            [(f['pts'], f['duration']) for f in frames]):
        raise ValueError('Output changed original frame count, PTS or duration')
    if len(source_hashes) != count or len(output_hashes) != count:
        raise ValueError('Decoded hash count differs from source')
    for i, (a, b, frame) in enumerate(zip(source_hashes, output_hashes, frames)):
        clock = (frame['pts'], frame['duration'])
        if a[:2] != clock or b[:2] != clock:
            raise ValueError('Hash clock mismatch at frame ' + str(i))
        if i not in modified and a != b:
            raise ValueError('Unchanged decoded frame differs at ' + str(i))
    for kind in ('video', 'audio'):
        a, b = stream(source_probe, kind), stream(output_probe, kind)
        if (a['time_base'], a['codec_name']) != (b['time_base'], b['codec_name']):
            raise ValueError(kind + ' codec or timebase changed')
    if packets(source_probe, 'audio') != packets(output_probe, 'audio'):
        raise ValueError('Original compressed audio packets or timestamps changed')
    pts_index = {f['pts']: i for i, f in enumerate(frames)}
    def unchanged(probe):
        rows = packets(probe, 'video')
        if len(rows) != count or len({int(p['pts']) for p in rows}) != count:
            raise ValueError('Video packet count/PTS mismatch')
        result = []
        for packet in rows:
            index = pts_index.get(int(packet['pts']))
            if index is None:
                raise ValueError('Unmapped video packet')
            if index not in encoded:
                result.append(packet)
        return result
    if unchanged(source_probe) != unchanged(output_probe):
        raise ValueError('Copied GOP packet bytes or timestamps changed')
    return {'status': 'PRESERVATION_CHECKS_ONLY', 'frames': count,
            'unchanged_decoded_frames_verified': count - len(modified),
            'copied_video_packets_verified': count - len(encoded),
            'audio_packets_verified': len(packets(source_probe, 'audio')),
            'sync': 'UNMEASURED', 'loudness': 'UNMEASURED',
            'visual_review': 'OUTSTANDING', 'final_film_approval': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--contract', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True,
                        help='Pinned SOURCE_PREFLIGHT.json record')
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    evidence = json.loads(args.evidence.read_text())
    if evidence['master_sha256'] != recipe.MASTER_SHA:
        raise ValueError('Evidence is not for the approved source master')
    paths = {}
    for name, entry in evidence['evidence_files'].items():
        recipe.require_hash(entry['path'], entry['sha256'], entry['bytes'])
        paths[name] = Path(entry['path'])
    args.out.mkdir(parents=True, exist_ok=False)
    candidate_sha = recipe.sha256_file(args.candidate)
    contract_sha = recipe.sha256_file(args.contract)
    contract = json.loads(args.contract.read_text())
    timeline = recipe.probe_video(args.candidate, recipe.EXPECTED_FRAMES)
    probe = probe_packets(args.candidate)
    output_hashes = args.out / 'candidate.framehash'
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-copyts',
                    '-i', str(args.candidate), '-map', '0:v:0', '-an',
                    '-c:v', 'rawvideo', '-pix_fmt', 'yuv420p', '-fps_mode',
                    'passthrough', '-enc_time_base', '1/12288', '-f',
                    'framehash', '-hash', 'sha256', '-n', str(output_hashes)], check=True)
    result = verify(json.loads(paths['source_timeline.json'].read_text()),
                    json.loads(paths['source_packets.json'].read_text()),
                    parse_hashes(paths['source_decoded.framehash'].read_text()),
                    timeline, probe, parse_hashes(output_hashes.read_text()),
                    contract, evidence['idr_frame_indices'])
    if recipe.sha256_file(args.candidate) != candidate_sha:
        raise ValueError('Candidate changed during verification')
    if recipe.sha256_file(args.contract) != contract_sha:
        raise ValueError('Change contract changed during verification')
    result.update(identity_selfcheck=candidate_sha == recipe.MASTER_SHA,
                  candidate=str(args.candidate), candidate_sha256=candidate_sha,
                  source_master_sha256=recipe.MASTER_SHA,
                  contract_sha256=contract_sha,
                  candidate_framehash_sha256=recipe.sha256_file(output_hashes))
    recipe.write_new(args.out / 'RESULT.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
