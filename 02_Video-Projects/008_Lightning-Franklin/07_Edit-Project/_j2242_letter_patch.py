"""Bounded cream ink letter over the approved moving sea plate; no new claims."""
import argparse
import json
import math
import subprocess
from fractions import Fraction
from pathlib import Path
import _build_rough_v13_recipe as recipe
from _j2242_caption_layers import clock_expression
from _j2242_salon_patch import pixel_hashes

SOURCE_SHA = '775e6d72eeb9bcec1ba61a72ee2fab14669620a23626bb5c1b0b5c80d7b5d749'


def letter_geometry(index, count=101):
    if not 0 <= index < count or count != 101:
        raise ValueError('Only the approved 101-frame crossing is supported')
    q = index / (count - 1)
    x = round(100 + 340 * q)
    y = round(235 - 70 * math.sin(math.pi * q))
    opacity = max(0, min(1, index / 9, (count - 1 - index) / 9))
    return x, y, round(opacity * 255)


def patch_clock(timeline):
    if timeline['time_base'] != '1/12288':
        raise ValueError('Original time base required')
    frames = timeline['frames'][4977:5078]
    if len(frames) != 101:
        raise ValueError('Missing crossing frames')
    for i, frame in enumerate(frames):
        expected = 2553856 + i * 512 + (1024 if i >= 92 else 0)
        duration = 1536 if i == 91 else 512
        if frame['index'] != 4977 + i or frame['pts'] != expected or frame['duration'] != duration:
            raise ValueError('Original crossing frame/PTS/duration differs')
    return frames


def verify_background(source, output):
    results = {}
    for name, crop in [('ship_and_right', 'crop=1340:1080:580:0'),
                       ('sea_and_lower_frame', 'crop=1920:740:0:340'),
                       ('upper_sky', 'crop=1920:140:0:0')]:
        expected = pixel_hashes(source, 'trim=start_frame=0:end_frame=101,'
                                'scale=1920:1080:flags=lanczos,setsar=1,format=yuv420p,'+crop)
        actual = pixel_hashes(output, crop)
        if len(expected) != 101 or actual != expected:
            raise ValueError(f'{name} background changed outside ink animation')
        results[name] = dict(compared_frames=101, exact_decoded_pixel_hashes_match=True)
    return results


def main():
    from PIL import Image, ImageDraw
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--timeline', type=Path, required=True)
    ap.add_argument('--out-dir', type=Path, required=True)
    args = ap.parse_args()
    if args.source.name != '07_slow_news_t1.mp4':
        raise ValueError('Wrong sea plate')
    recipe.require_hash(args.source, SOURCE_SHA)
    evidence = json.loads((recipe.EDIT_DIR.parents[2] / 'jobs/reviews/J2242/SOURCE_PREFLIGHT.json').read_text())
    clock_hash = evidence['evidence_files']['source_timeline.json']['sha256']
    recipe.require_hash(args.timeline, clock_hash)
    frames = patch_clock(json.loads(args.timeline.read_text()))
    source = recipe.probe_video(args.source)
    if len(source['frames']) < 101 or any(Fraction(f['pts']) * Fraction(source['time_base']) != Fraction(i, 24)
                                          for i, f in enumerate(source['frames'][:101])):
        raise ValueError('Sea plate does not supply native source f000..f100')
    args.out_dir.mkdir(parents=True, exist_ok=False)
    layers = args.out_dir / 'alpha'
    layers.mkdir()
    bounds = []
    for i in range(101):
        image = Image.new('RGBA', (1920, 1080))
        draw = ImageDraw.Draw(image)
        x, y, alpha = letter_geometry(i)
        cream = (255, 245, 221, alpha)
        # One inked folded letter; no map, trail, banner, box or written claim.
        draw.line([(x, y), (x+132, y), (x+132, y+84), (x, y+84), (x, y)], fill=cream, width=7)
        draw.line([(x, y), (x+66, y+48), (x+132, y)], fill=cream, width=7)
        draw.line([(x, y+84), (x+45, y+42)], fill=cream, width=5)
        draw.line([(x+132, y+84), (x+87, y+42)], fill=cream, width=5)
        image.save(layers / f'{i:03d}.png')
        bounds.append([x, y, x+132, y+84])
    graph = ('[0:v]trim=start_frame=0:end_frame=101,setpts=PTS-STARTPTS,'
             'scale=1920:1080:flags=lanczos,setsar=1,format=yuv420p[base];'
             '[1:v]format=rgba[ink];'
             '[base][ink]overlay=shortest=1:eof_action=endall,format=yuv420p,'
             f"settb=1/12288,setpts='{clock_expression(frames)}'[v]")
    output = args.out_dir / 'letter_patch.nut'
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-xerror',
                    '-i', str(args.source), '-framerate', '24', '-i', str(layers / '%03d.png'),
                    '-filter_complex', graph, '-map', '[v]', '-frames:v', '101', '-an',
                    '-c:v', 'ffv1', '-level', '3', '-threads', '4',
                    '-fps_mode', 'passthrough', '-enc_time_base', '1/12288',
                    '-avoid_negative_ts', 'disabled', '-n', str(output)], check=True)
    measured = recipe.probe_video(output, 101)
    ratio = Fraction(measured['time_base']) / Fraction('1/12288')
    if [f['pts'] * ratio for f in measured['frames']] != [f['pts'] for f in frames]:
        raise ValueError('Crossing PTS changed')
    background = verify_background(args.source, output)
    clock_path = args.out_dir / 'original_clock.json'
    recipe.write_new(clock_path, dict(time_base='1/12288', frames=frames))
    recipe.require_hash(args.source, SOURCE_SHA)
    recipe.require_hash(args.timeline, clock_hash)
    result = dict(job='J2242', status='LETTER_INTERMEDIATE_ONLY', path=str(output),
                  sha256=recipe.sha256_file(output), source_sha256=SOURCE_SHA,
                  source_frames=[0, 100], timeline_frames=[4977, 5077], frame_count=101,
                  original_pts_match=True, original_clock_path=str(clock_path),
                  original_clock_sha256=recipe.sha256_file(clock_path),
                  original_durations_preserved_in_intermediate=
                  [f['duration'] * ratio for f in measured['frames']] == [f['duration'] for f in frames],
                  alpha_frame_bounds=bounds, background_verification=background, moving_ink_letter_count=1,
                  brown_boxes=0, geography_labels=0, distance_labels=0,
                  final_mux_verification='OUTSTANDING', phone_readability='OUTSTANDING',
                  visual_review='OUTSTANDING', master_created=False, final_film_approval=False)
    recipe.write_new(args.out_dir / 'RESULT.json', result)
    print(json.dumps({k:v for k,v in result.items() if k != 'alpha_frame_bounds'}, indent=2))


if __name__ == '__main__':
    main()
