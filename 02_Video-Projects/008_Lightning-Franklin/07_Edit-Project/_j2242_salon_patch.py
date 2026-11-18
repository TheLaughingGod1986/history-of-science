"""Render only J2242's salon intermediate. No master mux, approval or publication."""
import argparse
import json
import subprocess
from fractions import Fraction
from pathlib import Path

import _build_rough_v13_recipe as recipe

# FLOW_MINT_LOG_v03 and rough_v12 cut[22] agree with the on-disk bytes.
# J1880's inventory carries a different, stale hash; do not use that as baseline.
TUBE_SHA = 'd3a0b24c996c9d388baaf4e764b7561f9144e50a6fe21d94e8a3d2f9f2c45170'
COMPOSITE_SHA = '1dd1c555e26658cfe019f68502be7949866a1913b6ad012bc0659ee202d6e704'


def patch_clock(timeline):
    frames = timeline['frames'][2506:2666]
    if timeline['time_base'] != '1/12288' or len(frames) != 160:
        raise ValueError('Unexpected master clock or frame count')
    if any(f['index'] != 2506 + i or f['duration'] != 512 or
           f['pts'] != frames[0]['pts'] + i * 512 for i, f in enumerate(frames)):
        raise ValueError('Salon window is not the verified uniform source interval')
    return frames


def source_schedule():
    schedule = [0] * 19 + list(range(61))
    assert len(schedule) == 80 and schedule[2635 - 2586] == 30
    return schedule


def pixel_hashes(path, filters=None):
    command = ['ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-i', str(path), '-map', '0:v:0', '-an']
    if filters:
        command += ['-vf', filters]
    command += ['-c:v', 'rawvideo', '-pix_fmt', 'yuv420p', '-fps_mode', 'passthrough', '-f', 'framehash', '-hash', 'sha256', '-']
    output = subprocess.check_output(command, text=True)
    return [line.split(',')[-1].strip() for line in output.splitlines() if line and not line.startswith('#')]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tube', type=Path, required=True)
    parser.add_argument('--composite', type=Path, required=True)
    parser.add_argument('--timeline', type=Path, required=True)
    parser.add_argument('--out-dir', type=Path, required=True)
    args = parser.parse_args()
    frames = patch_clock(json.loads(args.timeline.read_text()))
    recipe.require_hash(args.tube, TUBE_SHA)
    recipe.require_hash(args.composite, COMPOSITE_SHA)
    composite = recipe.probe_video(args.composite, 61)
    tube = recipe.probe_video(args.tube)
    for clock in (composite, tube):
        if any(b['pts'] - a['pts'] != 512 for a, b in zip(clock['frames'], clock['frames'][1:])):
            raise ValueError('Source must have 24fps native schedule')
    args.out_dir.mkdir(parents=True, exist_ok=False)
    # Select source frames, not approximate seek times. tpad adds exactly 19
    # leading copies; the native f000 follows, then f001..f060. Last frame hard
    # clipped before the composite is concatenated. No post-f060 input exists.
    graph = (
        '[0:v]trim=start_frame=99:end_frame=179,setpts=PTS-STARTPTS,'
        'crop=iw*0.89:ih*0.89:iw*0.08:ih*0.06,scale=1920:1080:flags=lanczos,'
        'setsar=1,format=yuv420p[a];'
        '[1:v]trim=start_frame=0:end_frame=61,setpts=PTS-STARTPTS,'
        'scale=1920:1080:flags=lanczos,setsar=1,format=yuv420p,'
        'tpad=start=19:start_mode=clone,trim=end_frame=80[b];'
        '[a][b]concat=n=2:v=1:a=0,settb=1/12288,'
        f'setpts={frames[0]["pts"]}+N*512[v]'
    )
    (args.out_dir / 'filter.txt').write_text(graph)
    output = args.out_dir / 'salon_patch.nut'
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-xerror',
                    '-i', str(args.tube), '-i', str(args.composite),
                    '-filter_complex', graph,
                    '-map', '[v]', '-an', '-c:v', 'ffv1', '-level', '3',
                    '-threads', '4', '-fps_mode', 'passthrough', '-enc_time_base',
                    '1/12288', '-avoid_negative_ts', 'disabled', '-n', str(output)], check=True)
    measured = recipe.probe_video(output, 160)
    ratio = Fraction(measured['time_base']) / Fraction('1/12288')
    if [(f['pts'] * ratio, f['duration'] * ratio) for f in measured['frames']] != [(f['pts'], f['duration']) for f in frames]:
        raise ValueError('Intermediate changed original timestamps/durations')
    tube_hashes = pixel_hashes(args.tube, 'trim=start_frame=99:end_frame=179,crop=iw*0.89:ih*0.89:iw*0.08:ih*0.06,scale=1920:1080:flags=lanczos,setsar=1,format=yuv420p')
    composite_hashes = pixel_hashes(args.composite, 'scale=1920:1080:flags=lanczos,setsar=1,format=yuv420p')
    expected_hashes = tube_hashes + [composite_hashes[i] for i in source_schedule()]
    actual_hashes = pixel_hashes(output)
    if len(tube_hashes) != 80 or len(composite_hashes) != 61 or actual_hashes != expected_hashes:
        raise ValueError('Lossless decode differs from exact source frame schedule')
    result = {'job': 'J2242', 'status': 'SALON_INTERMEDIATE_ONLY',
              'path': str(output), 'sha256': recipe.sha256_file(output),
              'frame_count': 160, 'original_pts_and_duration_match': True,
              'intermediate_time_base': measured['time_base'],
              'rescale_to_master_ticks': str(ratio),
              'source_frame_pixel_hashes_match': True,
              'tube_sha256': TUBE_SHA, 'composite_sha256': COMPOSITE_SHA,
              'tube_frames': [99, 178], 'composite_frame_schedule': source_schedule(),
              'spark_timeline_frame': 2635, 'last_composite_frame': 60,
              'lossless_intermediate': True, 'master_created': False,
              'visual_review': 'OUTSTANDING; 19-frame hold requires in-context review',
              'audio': 'Absent from intermediate; original master audio untouched'}
    recipe.write_new(args.out_dir / 'RESULT.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
