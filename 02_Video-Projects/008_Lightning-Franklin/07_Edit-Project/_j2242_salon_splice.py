"""Bounded salon-only packet mux experiment; never a finished v04 master.

Requires PyAV. Copies original packets except the approved 160-frame salon GOP.
The pre-encoded replacement must be lossless H264 with no B frames and in-band
SPS/PPS. Existing source IDRs must carry their own SPS/PPS to restore the source
codec after the patch. Independent preservation verification is mandatory.
"""
import argparse
import json
from fractions import Fraction
from pathlib import Path

import _build_rough_v13_recipe as recipe
from _j2242_source_preflight import nal_types
from _j2242_salon_patch import pixel_hashes

FIRST, LAST = 2506, 2665


def validate_clock(timeline):
    frames = timeline['frames'][FIRST:LAST + 1]
    if timeline['time_base'] != '1/12288' or len(frames) != 160:
        raise ValueError('Unexpected salon clock')
    if any(f['pts'] != frames[0]['pts'] + i * 512 or f['duration'] != 512
           for i, f in enumerate(frames)):
        raise ValueError('Salon is not the approved uniform interval')
    if not frames[0]['key_frame'] or not timeline['frames'][LAST + 1]['key_frame']:
        raise ValueError('Salon boundaries are not random access')
    return frames


def check_headers(payload, length_size):
    types = nal_types(payload, length_size)
    if not {7, 8, 5} <= set(types):
        raise ValueError('Boundary requires in-band SPS, PPS and IDR')


def main():
    import av
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', type=Path, default=recipe.DEFAULT_MASTER)
    ap.add_argument('--encoded-patch', type=Path, required=True)
    ap.add_argument('--evidence', type=Path, required=True)
    ap.add_argument('--out-dir', type=Path, required=True)
    a = ap.parse_args()
    recipe.require_hash(a.source, recipe.MASTER_SHA, recipe.MASTER_BYTES)
    evidence = json.loads(a.evidence.read_text())
    paths = evidence['evidence_files']
    for entry in paths.values():
        recipe.require_hash(entry['path'], entry['sha256'], entry['bytes'])
    timeline = json.loads(Path(paths['source_timeline.json']['path']).read_text())
    frames = validate_clock(timeline)
    patch_sha = recipe.sha256_file(a.encoded_patch)
    intermediate = json.loads(Path('jobs/reviews/J2242/SALON_PATCH.json').read_text())
    recipe.require_hash(intermediate['path'], intermediate['sha256'])
    expected = pixel_hashes(intermediate['path'])
    if len(expected) != 160 or pixel_hashes(a.encoded_patch) != expected:
        raise ValueError('Encoded patch differs from verified salon intermediate')
    patch = av.open(str(a.encoded_patch))
    ps = patch.streams.video[0]
    if ps.codec_context.name != 'h264' or (ps.width, ps.height) != (1920, 1080):
        raise ValueError('Patch must be 1080p H264')
    if len(ps.codec_context.extradata) < 5 or ps.codec_context.extradata[4] & 3 != 3:
        raise ValueError('Patch must use four-byte NAL lengths')
    replacement = [p for p in patch.demux(ps) if p.size]
    if len(replacement) != len(frames):
        raise ValueError('Patch must contain exactly 160 packets')
    base = replacement[0].pts
    for i, p in enumerate(replacement):
        if p.pts != p.dts or Fraction(p.pts - base) * p.time_base != Fraction(i, 24):
            raise ValueError('Patch must have no B frames and native 24fps')
    check_headers(bytes(replacement[0]), 4)
    source = av.open(str(a.source))
    video, audio = source.streams.video[0], source.streams.audio[0]
    if video.time_base != Fraction(1, 12288):
        raise ValueError('Unexpected source timebase')
    a.out_dir.mkdir(parents=True, exist_ok=False)
    candidate = a.out_dir / 'salon_only_experiment.mp4'
    contract = {'modified_frames': [[FIRST, LAST]], 'encoded_envelopes': [[FIRST, LAST]]}
    (a.out_dir / 'contract.json').write_text(json.dumps(contract, indent=2) + '\n')
    n = copied = audios = 0
    inserted = restored = False
    with av.open(str(candidate), 'w', options={'avoid_negative_ts': 'disabled',
                 'video_track_timescale': '12288'}) as out:
        ov = out.add_stream_from_template(video)
        oa = out.add_stream_from_template(audio)
        for packet in source.demux(video, audio):
            if not packet.size:
                continue
            if packet.stream.index == audio.index:
                packet.stream = oa
                out.mux(packet)
                audios += 1
                continue
            if frames[0]['pts'] <= packet.pts <= frames[-1]['pts']:
                if not inserted:
                    # Source B-frame reorder delay is retained in DTS. The new
                    # patch has no B frames; all PTS remain exact master ticks.
                    delay = packet.pts - packet.dts
                    if delay != 1024:
                        raise ValueError('Unexpected source decode delay')
                    for i, p in enumerate(replacement):
                        p.pts = frames[i]['pts']
                        p.dts = p.pts - delay
                        p.duration = frames[i]['duration']
                        p.time_base = Fraction(1, 12288)
                        p.stream = ov
                        out.mux(p)
                    inserted = True
                n += 1
                continue
            if packet.pts == timeline['frames'][LAST + 1]['pts']:
                check_headers(bytes(packet), 4)
                restored = True
            packet.stream = ov
            out.mux(packet)
            copied += 1
    source.close()
    patch.close()
    recipe.require_hash(a.source, recipe.MASTER_SHA, recipe.MASTER_BYTES)
    if n != 160 or not restored or not inserted:
        raise ValueError('Incomplete salon replacement')
    if recipe.sha256_file(a.encoded_patch) != patch_sha:
        raise ValueError('Encoded patch changed during mux')
    result = {'status': 'UNVERIFIED_SALON_ONLY_EXPERIMENT',
              'candidate': str(candidate), 'candidate_sha256': recipe.sha256_file(candidate),
              'encoded_patch_sha256': patch_sha, 'source_sha256': recipe.MASTER_SHA,
              'replaced_packets': n, 'copied_video_packets': copied,
              'copied_audio_packets': audios, 'pyav_version': av.__version__,
              'output_preservation': 'OUTSTANDING', 'vo_sync': 'UNMEASURED',
              'finished_master': False, 'approval': False}
    recipe.write_new(a.out_dir / 'MUX_RESULT.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
