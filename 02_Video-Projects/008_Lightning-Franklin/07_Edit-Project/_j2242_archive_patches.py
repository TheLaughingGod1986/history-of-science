"""Render bounded storm/jar source intermediates; never assemble or approve a master."""
import argparse
import json
import subprocess
from fractions import Fraction
from pathlib import Path
import _build_rough_v13_recipe as recipe
from _j2242_salon_patch import pixel_hashes

SPECS = {
    'storm': dict(first=744, last=839, first_pts=382976, overlap=745,
                  sha256='e1b2de5d8cd4bbc8ace98d6d5c17af3c75651f8949d54e062fe91fbe6ee31271',
                  filename='04_storm_mystery_t1.mp4'),
    'jar': dict(first=3260, last=3343, first_pts=1672704, overlap=None,
                sha256='7629a5dfdc5b649535c9816ece5bf0acf250a13133bf294bf43cfb1f21588270',
                filename='11_jar_crack_t1.mp4'),
}

def patch_clock(timeline, kind):
    spec = SPECS[kind]
    frames = timeline['frames'][spec['first']:spec['last'] + 1]
    count = spec['last'] - spec['first'] + 1
    if timeline['time_base'] != '1/12288' or len(frames) != count:
        raise ValueError('Missing or rescaled original clock')
    for i, frame in enumerate(frames):
        index = spec['first'] + i
        if (frame['index'] != index or frame['pts'] != spec['first_pts'] + i * 512
                or frame['duration'] != (1024 if index == spec['overlap'] else 512)):
            raise ValueError('Original index, PTS or duration changed')
    return frames

def validate_native_source(clock, count):
    frames = clock['frames'][:count]
    tb = Fraction(clock['time_base'])
    if len(frames) != count or any(
            f['pts'] * tb != Fraction(i, 24) or
            f['duration'] * tb != Fraction(1, 24) for i, f in enumerate(frames)):
        raise ValueError('Source does not supply the selected native 24fps frames')

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--kind', choices=SPECS, required=True)
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--timeline', type=Path, required=True)
    ap.add_argument('--out-dir', type=Path, required=True)
    args = ap.parse_args()
    spec = SPECS[args.kind]
    if args.source.name != spec['filename']:
        raise ValueError('Unexpected source identity')
    recipe.require_hash(args.source, spec['sha256'])
    evidence = json.loads((recipe.EDIT_DIR.parents[2] / 'jobs/reviews/J2242/SOURCE_PREFLIGHT.json').read_text())
    clock_hash = evidence['evidence_files']['source_timeline.json']['sha256']
    recipe.require_hash(args.timeline, clock_hash)
    frames = patch_clock(json.loads(args.timeline.read_text()), args.kind)
    count = len(frames)
    validate_native_source(recipe.probe_video(args.source), count)
    args.out_dir.mkdir(parents=True, exist_ok=False)
    filters = (f'trim=start_frame=0:end_frame={count},scale=1920:1080:flags=lanczos,'
               'setsar=1,format=yuv420p')
    graph = filters + f",settb=1/12288,setpts={spec['first_pts']}+N*512"
    output = args.out_dir / f'{args.kind}_patch.nut'
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-xerror',
                    '-i', str(args.source), '-map', '0:v:0', '-an', '-vf', graph,
                    '-c:v', 'ffv1', '-level', '3', '-threads', '4',
                    '-fps_mode', 'passthrough', '-enc_time_base', '1/12288',
                    '-avoid_negative_ts', 'disabled', '-n', str(output)], check=True)
    measured = recipe.probe_video(output, count)
    ratio = Fraction(measured['time_base']) / Fraction('1/12288')
    if [f['pts'] * ratio for f in measured['frames']] != [f['pts'] for f in frames]:
        raise ValueError('Intermediate presentation timestamps differ')
    expected = pixel_hashes(args.source, filters)
    if len(expected) != count or pixel_hashes(output) != expected:
        raise ValueError('Intermediate source pixels differ')
    clock_path = args.out_dir / 'original_clock.json'
    recipe.write_new(clock_path, dict(time_base='1/12288', frames=frames))
    duration_match = [f['duration'] * ratio for f in measured['frames']] == [f['duration'] for f in frames]
    recipe.require_hash(args.source, spec['sha256'])
    recipe.require_hash(args.timeline, clock_hash)
    result = dict(job='J2242', status='SOURCE_INTERMEDIATE_ONLY', kind=args.kind,
                  path=str(output), sha256=recipe.sha256_file(output),
                  source_sha256=spec['sha256'], source_frames=[0, count - 1],
                  timeline_frames=[spec['first'], spec['last']], frame_count=count,
                  original_pts_match=True, source_frame_pixel_hashes_match=True,
                  original_durations_preserved_in_intermediate=duration_match,
                  original_clock_path=str(clock_path),
                  original_clock_sha256=recipe.sha256_file(clock_path),
                  intermediate_time_base=measured['time_base'],
                  rescale_to_master_ticks=str(ratio),
                  final_mux_duration_verification='OUTSTANDING',
                  boundary_unchanged_frame_verification='OUTSTANDING',
                  audio='Absent; original master untouched',
                  visual_review='OUTSTANDING', speech_alignment='OUTSTANDING',
                  captions_rendered=False, master_created=False, final_film_approval=False)
    recipe.write_new(args.out_dir / 'RESULT.json', result)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
