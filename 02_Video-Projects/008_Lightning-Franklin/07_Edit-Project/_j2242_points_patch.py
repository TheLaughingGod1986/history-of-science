"""Render the approved points take as a lossless, PTS-verified intermediate with original duration sidecar."""
import argparse
import json
import subprocess
from fractions import Fraction
from pathlib import Path
import _build_rough_v13_recipe as recipe
from _j2242_salon_patch import pixel_hashes

POINTS_SHA = '950a2b34dee038becf1738ab797358e9dd7a0040d8a1c50e840b3886d59a93e3'
FIRST, LAST = 4511, 4670

def patch_clock(timeline):
    frames = timeline['frames'][FIRST:LAST + 1]
    if timeline['time_base'] != '1/12288' or len(frames) != 160:
        raise ValueError('Unexpected points clock or frame count')
    for i, frame in enumerate(frames):
        if (frame['index'] != FIRST + i or frame['duration'] != (1024 if frame['index'] == 4513 else 512) or
                frame['pts'] != frames[0]['pts'] + i * 512):
            raise ValueError('Points window differs from pinned source clock (including the overlapping duration)')
    return frames

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--timeline', type=Path, required=True)
    ap.add_argument('--out-dir', type=Path, required=True)
    args = ap.parse_args()
    recipe.require_hash(args.source, POINTS_SHA)
    # Pin the clock file to the independently measured source evidence.
    evidence = json.loads((recipe.EDIT_DIR.parents[2] / 'jobs/reviews/J2242/SOURCE_PREFLIGHT.json').read_text())
    clock_evidence = evidence['evidence_files']['source_timeline.json']
    recipe.require_hash(args.timeline, clock_evidence['sha256'])
    frames = patch_clock(json.loads(args.timeline.read_text()))
    source_clock = recipe.probe_video(args.source, 190)
    selected = source_clock['frames'][:160]
    tb = Fraction(source_clock['time_base'])
    if any(Fraction(f['pts']) * tb != Fraction(i, 24) or
           Fraction(f['duration']) * tb != Fraction(1, 24)
           for i, f in enumerate(selected)):
        raise ValueError('Retake native frame schedule changed')
    args.out_dir.mkdir(parents=True, exist_ok=False)
    filters = ('trim=start_frame=0:end_frame=160,scale=1920:1080:flags=lanczos,'
               'setsar=1,format=yuv420p')
    graph = filters + f",settb=1/12288,setpts={frames[0]['pts']}+N*512"
    output = args.out_dir / 'points_patch.nut'
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-xerror',
                    '-i', str(args.source), '-map', '0:v:0', '-an', '-vf', graph,
                    '-c:v', 'ffv1', '-level', '3', '-threads', '4',
                    '-fps_mode', 'passthrough', '-enc_time_base', '1/12288',
                    '-avoid_negative_ts', 'disabled', '-n', str(output)], check=True)
    measured = recipe.probe_video(output, 160)
    ratio = Fraction(measured['time_base']) / Fraction('1/12288')
    if [f['pts'] * ratio for f in measured['frames']] != [f['pts'] for f in frames]:
        raise ValueError('Intermediate changed original presentation timestamps')
    # NUT reconstructs durations from PTS; preserve overlapping original durations
    # explicitly for the future packet mux rather than claiming they survived here.
    clock_path = args.out_dir / 'original_clock.json'
    recipe.write_new(clock_path, {'time_base': '1/12288', 'frames': frames})
    expected = pixel_hashes(args.source, filters)
    if len(expected) != 160 or pixel_hashes(output) != expected:
        raise ValueError('Intermediate pixels differ from selected source frames')
    recipe.require_hash(args.source, POINTS_SHA)
    recipe.require_hash(args.timeline, clock_evidence['sha256'])
    result = {'job': 'J2242', 'status': 'POINTS_INTERMEDIATE_ONLY',
              'path': str(output), 'sha256': recipe.sha256_file(output),
              'source_sha256': POINTS_SHA, 'source_frames': [0, 159],
              'timeline_frames': [FIRST, LAST], 'frame_count': 160,
              'original_pts_match': True,
              'original_durations_preserved_in_intermediate': False,
              'original_clock_path': str(clock_path),
              'original_clock_sha256': recipe.sha256_file(clock_path),
              'final_mux_duration_verification': 'OUTSTANDING',
              'source_frame_pixel_hashes_match': True,
              'intermediate_time_base': measured['time_base'],
              'rescale_to_master_ticks': str(ratio),
              'lossless_intermediate': True, 'master_created': False,
              'audio': 'Absent; original master untouched',
              'visual_review': 'OUTSTANDING', 'final_film_approval': False}
    recipe.write_new(args.out_dir / 'RESULT.json', result)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
