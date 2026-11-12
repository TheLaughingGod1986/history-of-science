"""Render transparent caption layers only; clean plate reconstruction is separate."""
import argparse
import json
import subprocess
from fractions import Fraction
from pathlib import Path

import _build_rough_v13_recipe as recipe

FONT = Path('/System/Library/Fonts/Supplemental/Didot.ttc')
WIDTH, HEIGHT, TOP = 1920, 300, 720
FADE = Fraction(3, 8)


def caption_schedule(timeline, manifest, notes):
    if timeline['time_base'] != '1/12288':
        raise ValueError('Original master clock required')
    plan = recipe.plan_captions(timeline['frames'], timeline['time_base'],
                                manifest['caption_treatment']['labels'], notes)
    if len(plan['cards']) != 32:
        raise ValueError('Expected exactly 32 planned captions')
    cards = plan['cards'] + [recipe.plan_safe_path(timeline['frames'], timeline['time_base'])]
    cards.sort(key=lambda c: c['pts_in'])
    for i, card in enumerate(cards):
        if not 1 <= card['word_count'] <= 4 or not 0 < card['hold_ticks'] <= 49152:
            raise ValueError('Caption word/hold limit failed')
        if i and cards[i-1]['pts_end'] > card['pts_in']:
            raise ValueError('Overlapping caption cards')
        clock = [f for f in timeline['frames']
                 if card['pts_in'] <= f['pts'] < card['pts_end']]
        if not clock or clock[0]['pts'] != card['pts_in']:
            raise ValueError('Caption does not start on original frame')
        if clock[-1]['pts'] + clock[-1]['duration'] != card['pts_end']:
            raise ValueError('Caption end differs from original clock')
        card['clock'] = clock
    return cards


def clock_expression(frames):
    """Preserve every irregular original PTS instead of rebuilding a CFR clock."""
    if not frames or any(b['pts'] <= a['pts'] for a, b in zip(frames, frames[1:])):
        raise ValueError('Missing or nonmonotonic clock')
    expression = f"{frames[0]['pts']}+N*512"
    for i in range(1, len(frames)):
        delta = frames[i]['pts'] - frames[i-1]['pts'] - 512
        if delta:
            expression += f'+({delta})*gte(N,{i})'
    return expression


def verify_alpha(video, card, panel_bounds):
    """Decode a panel pixel on every frame, checking both fades and the hold."""
    x = panel_bounds[0] + 4
    values = subprocess.check_output([
        'ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-i', str(video),
        '-vf', f'alphaextract,crop=1:1:{x}:{panel_bounds[1]+4}', '-an',
        '-fps_mode', 'passthrough', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'])
    clock = card['clock']
    if len(values) != len(clock):
        raise ValueError('Alpha decode count differs')
    duration = Fraction(card['hold_ticks'], 12288)
    errors = []
    for frame, actual in zip(clock, values):
        elapsed = Fraction(frame['pts'] - card['pts_in'], 12288)
        opacity = max(Fraction(0), min(Fraction(1), elapsed / FADE,
                                       (duration - elapsed) / FADE))
        errors.append(abs(actual - round(232 * opacity)))
    if max(errors) > 2 or values[0] != 0 or max(values) != 232:
        raise ValueError('Decoded panel opacity does not follow original-clock fades')
    return dict(decoded_frames=len(values), first_alpha=values[0],
                peak_alpha=max(values), last_alpha=values[-1],
                maximum_alpha_error=max(errors), passed=True)


def draw_layer(text, output):
    from PIL import Image, ImageDraw, ImageFont
    font = ImageFont.truetype(str(FONT), 128, index=1)
    if font.getname() != ('Didot', 'Italic'):
        raise ValueError('House Didot italic unavailable')
    image = Image.new('RGBA', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    def width(line):
        box = draw.textbbox((0, 0), line, font=font)
        return box[2] - box[0]
    lines = [text]
    if width(text) > WIDTH - 280:
        words = text.split()
        choices = [(words[:i], words[i:]) for i in range(1, len(words))]
        if not choices:
            raise ValueError('Unbreakable caption exceeds readable size')
        best = min(choices, key=lambda pair: max(width(' '.join(part)) for part in pair))
        lines = [' '.join(part) for part in best]
    text_width = max(map(width, lines))
    if text_width > WIDTH - 240:
        raise ValueError('Caption does not fit at phone-readable house size')
    # Plain unbordered umber rectangle; no pill, gold rule or outline.
    left = (WIDTH - text_width) // 2 - 48
    half_height = (104 + (len(lines)-1)*132) // 2 + 24
    panel = [left, HEIGHT//2-half_height, WIDTH-left, HEIGHT//2+half_height]
    draw.rectangle(panel, fill=(48, 30, 20, 232))
    for i, line in enumerate(lines):
        box = draw.textbbox((0, 0), line, font=font)
        center_y = HEIGHT/2 + (i-(len(lines)-1)/2)*132
        draw.text(((WIDTH-width(line))/2-box[0], center_y-(box[1]+box[3])/2),
                  line, font=font, fill=(255, 255, 255, 255))
    image.save(output)
    return dict(font='Didot Italic', font_size=128, lines=lines, panel_rgba=[48, 30, 20, 232],
                text_rgba=[255, 255, 255, 255], panel_bounds=panel,
                border=False, gold_rule=False, pill_chrome=False)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--timeline', type=Path, required=True)
    ap.add_argument('--out-dir', type=Path, required=True)
    args = ap.parse_args()
    evidence = json.loads((recipe.EDIT_DIR.parents[2] / 'jobs/reviews/J2242/SOURCE_PREFLIGHT.json').read_text())
    clock_hash = evidence['evidence_files']['source_timeline.json']['sha256']
    recipe.require_hash(args.timeline, clock_hash)
    manifest_path = recipe.EDIT_DIR / 'J2163_CORRECTION_MANIFEST.json'
    notes_path = recipe.EDIT_DIR.parent / '01_Script/FACT_NOTES_v01.md'
    input_hashes = {str(p): recipe.sha256_file(p) for p in (manifest_path, notes_path, FONT)}
    cards = caption_schedule(json.loads(args.timeline.read_text()),
                             json.loads(manifest_path.read_text()), notes_path.read_text())
    args.out_dir.mkdir(parents=True, exist_ok=False)
    rendered = []
    for i, card in enumerate(cards):
        stem = f'{i+1:02d}_{card["row"]}_{card.get("sequence", 1)}'
        png, video = args.out_dir / f'{stem}.png', args.out_dir / f'{stem}.nut'
        style = draw_layer(card['label'], png)
        frames = card['clock']
        duration = Fraction(card['hold_ticks'], 12288)
        fade_out = duration - FADE
        graph = (f"format=bgra,settb=1/12288,setpts='{clock_expression(frames)}-{frames[0]['pts']}',"
                 f'fade=t=in:st=0:d={float(FADE)}:alpha=1,'
                 f'fade=t=out:st={float(fade_out)}:d={float(FADE)}:alpha=1,'
                 f"setpts=PTS+{frames[0]['pts']}")
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-xerror',
                        '-loop', '1', '-framerate', '24', '-i', str(png),
                        '-vf', graph, '-frames:v', str(len(frames)), '-an',
                        '-c:v', 'ffv1', '-level', '3', '-pix_fmt', 'bgra', '-threads', '2',
                        '-fps_mode', 'passthrough', '-enc_time_base', '1/12288',
                        '-avoid_negative_ts', 'disabled', '-n', str(video)], check=True)
        measured = recipe.probe_video(video, len(frames))
        ratio = Fraction(measured['time_base']) / Fraction('1/12288')
        if [f['pts'] * ratio for f in measured['frames']] != [f['pts'] for f in frames]:
            raise ValueError('Rendered caption timestamps differ')
        alpha = verify_alpha(video, card, style['panel_bounds'])
        clock_path = args.out_dir / f'{stem}_clock.json'
        recipe.write_new(clock_path, dict(time_base='1/12288', frames=frames))
        item = {k: v for k, v in card.items() if k != 'clock'}
        item.update(layer_path=str(video), layer_sha256=recipe.sha256_file(video),
                    png_path=str(png), png_sha256=recipe.sha256_file(png),
                    frame_count=len(frames), original_pts_match=True,
                    original_clock_path=str(clock_path), original_clock_sha256=recipe.sha256_file(clock_path),
                    original_durations_preserved_in_intermediate=
                    [f['duration'] * ratio for f in measured['frames']] == [f['duration'] for f in frames],
                    overlay_position=[0, TOP], layer_size=[WIDTH, HEIGHT],
                    fade_in_s=str(FADE), fade_out_s=str(FADE), style=style, alpha_verification=alpha,
                    rendered=True, composited_over_clean_plate=False)
        rendered.append(item)
        recipe.write_new(args.out_dir / f'{stem}_RESULT.json', item)
        print(f'{i+1}/33 {card["label"]}: alpha layer rendered; original PTS verified', flush=True)
    recipe.require_hash(args.timeline, clock_hash)
    for path, expected in input_hashes.items():
        recipe.require_hash(path, expected)
    result = dict(job='J2242', status='TRANSPARENT_CAPTION_LAYERS_ONLY',
                  count=len(rendered), caption_count=32, safe_path_count=1,
                  input_hashes=input_hashes, timeline_sha256=clock_hash, cards=rendered,
                  baked_label_removal='OUTSTANDING: reconstruct moving source plates; do not overlay on baked text',
                  code_graphic_readability='OUTSTANDING: ten rows require separate review',
                  phone_readability='OUTSTANDING: final composite contact sheet required',
                  master_created=False, final_film_approval=False)
    recipe.write_new(args.out_dir / 'RESULT.json', result)


if __name__ == '__main__':
    main()
