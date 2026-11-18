"""Rebuild master frames 423–426 from the tower plate, not the table.

Master frame 422 is tower source 150. These next four master frames are a
forward jump to tower source 170–173: unique at about 3 MSE, with a runner-up
margin of about 17. Sources 151–169 do not appear here. The table plate stays
above 3500 MSE and is unused. A KITE starts on this tower tail. Frame 2869
is not part of this rebuild.
"""
import argparse
import json
import subprocess
from fractions import Fraction
from pathlib import Path

import numpy as np

import _build_rough_v13_recipe as recipe
from _j2242_ambiguous_fullres import _decode, rank_upper_band
from _j2242_caption_composites import source_graph
from _j2242_caption_layers import clock_expression
from _j2242_salon_patch import pixel_hashes

LEAD_FRAMES = (423, 424, 425, 426)
TOWER_TAIL = 150
TOWER_INDICES = (170, 171, 172, 173)
MAX_MSE = 9.0
MIN_MARGIN = 0.1
TABLE_POOR_MSE = 1000.0


def accept_tower_leadin(ranked):
    """Return 170–173 only when each frame is that unique tower picture."""
    if len(ranked) != 4:
        raise ValueError('Lead-in is four frames')
    indices = []
    for i, item in enumerate(ranked):
        best = item.get('best')
        if type(best) is not int or isinstance(best, bool) or best < 0:
            raise ValueError('Invalid tower index')
        if item['best_mse'] > MAX_MSE or item['margin'] < MIN_MARGIN:
            raise ValueError(f'Lead-in local {i} is not a unique tower match')
        if best != TOWER_INDICES[i]:
            raise ValueError(f'Lead-in local {i} is not tower source {TOWER_INDICES[i]}')
        indices.append(best)
    if any(b != a + 1 for a, b in zip(indices, indices[1:])):
        raise ValueError('Lead-in tower schedule is not contiguous')
    return indices


def table_stays_out(ranked):
    """The table plate must stay a poor match. A close frame is not rebuilt."""
    if len(ranked) != 4:
        raise ValueError('Lead-in is four frames')
    if any(item.get('best_mse', 0) <= TABLE_POOR_MSE for item in ranked):
        raise ValueError('Table plate is close enough to refuse the tower lead-in')
    return [423, 426]


def leadin_schedule(tower_row, tower_ranked, table_row, table_ranked):
    """Accept the continuation only when both plates still say what they said."""
    if tower_row.get('row') != '02_tower_tilt' or tower_row.get('timeline_frames') != [272, 422]:
        raise ValueError('Tower window changed')
    idx = tower_row.get('source_frame_indices') or []
    if not idx or idx[-1] != TOWER_TAIL or tower_row.get('decoded_source_frames', 0) <= TOWER_INDICES[-1]:
        raise ValueError('Tower tail is not source 150 with frames 170-173 available')
    if table_row.get('row') != '03_table_three' or table_row.get('timeline_frames') != [423, 544]:
        raise ValueError('Table window changed')
    if table_row.get('poor_match_local_frames') != [0, 1, 2, 3]:
        raise ValueError('Table lead-in flags changed')
    if (table_row.get('source_frame_indices') or [])[:4] != [52, 52, 52, 52]:
        raise ValueError('Table lead-in index changed')
    rejected = table_stays_out(table_ranked)
    indices = accept_tower_leadin(tower_ranked)
    if indices[0] <= TOWER_TAIL:
        raise ValueError('Lead-in does not move forward from tower source 150')
    return {
        'timeline_frames': [423, 426],
        'source_frame_indices': indices,
        'rejected_table_frames': rejected,
        'source_path': tower_row['source_path'],
        'source_sha256': tower_row['source_sha256'],
        'frame_2869': 'out',
    }


def _ranked_record(ranked):
    return [{
        'best': item['best'],
        'second': item['second'],
        'best_mse': item['best_mse'],
        'margin': item['margin'],
    } for item in ranked]


def measure(master, tower_row, table_row, scratch):
    """Score the four master frames against the whole tower and table plates."""
    scratch = Path(scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    tower = Path(tower_row['source_path'])
    table = Path(table_row['source_path'])
    recipe.require_hash(master, recipe.MASTER_SHA, recipe.MASTER_BYTES)
    recipe.require_hash(tower, tower_row['source_sha256'])
    recipe.require_hash(table, table_row['source_sha256'])
    tower_count = tower_row['decoded_source_frames']
    table_count = table_row['decoded_source_frames']
    master_raw = _decode(master, scratch / 'master_upper.raw', 4, "select='between(n,423,426)'")
    tower_raw = _decode(tower, scratch / 'tower_upper.raw', tower_count)
    table_raw = _decode(table, scratch / 'table_upper.raw', table_count)
    tower_ranked = rank_upper_band(np.asarray(master_raw), np.asarray(tower_raw))
    table_ranked = rank_upper_band(np.asarray(master_raw), np.asarray(table_raw))
    recipe.require_hash(master, recipe.MASTER_SHA, recipe.MASTER_BYTES)
    recipe.require_hash(tower, tower_row['source_sha256'])
    recipe.require_hash(table, table_row['source_sha256'])
    return tower_ranked, table_ranked


def _kite_card(cards):
    selected = [card for card in cards
                if card.get('row') == '03_table_three' and card.get('label') == 'A KITE'
                and card.get('frame_in') == 423 and card.get('frame_last') == 462]
    if len(selected) != 1:
        raise ValueError('A KITE card changed')
    return selected[0]


def _visible_caption(layer, count):
    """Frames whose panel alpha is above zero. The fade starts at zero."""
    values = subprocess.check_output([
        'ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-i', str(layer),
        '-frames:v', str(count), '-vf', 'alphaextract,crop=1:1:800:80',
        '-an', '-fps_mode', 'passthrough', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'])
    if len(values) != count:
        raise ValueError('A KITE alpha count differs')
    return [bool(value) for value in values]


def render_leadin(schedule, timeline, card, out):
    """Composite A KITE onto the four tower frames. No master is written."""
    frames = timeline['frames'][423:427]
    if timeline.get('time_base') != '1/12288' or len(frames) != 4:
        raise ValueError('Lead-in clock missing')
    if any(frame['index'] != 423 + i for i, frame in enumerate(frames)):
        raise ValueError('Lead-in clock is out of order')
    if schedule['timeline_frames'] != [423, 426] or schedule['source_frame_indices'] != list(TOWER_INDICES):
        raise ValueError('Lead-in schedule changed')
    if schedule.get('frame_2869') != 'out':
        raise ValueError('Frame 2869 is not part of this lead-in')
    source = Path(schedule['source_path'])
    recipe.require_hash(source, schedule['source_sha256'])
    recipe.require_hash(card['layer_path'], card['layer_sha256'])
    recipe.require_hash(card['original_clock_path'], card['original_clock_sha256'])
    native = recipe.probe_video(source)
    if max(TOWER_INDICES) >= len(native['frames']):
        raise ValueError('Tower source is shorter than frames 170-173')
    visible = _visible_caption(card['layer_path'], 4)
    if visible[0] or not any(visible[1:]):
        raise ValueError('A KITE fade does not start clear and then appear')
    out.mkdir(exist_ok=False)
    base = 'scale=1920:1080:flags=lanczos,setsar=1,format=yuv420p'
    graph = [
        source_graph(list(TOWER_INDICES)),
        f"[ordered]{base},settb=1/12288,setpts='{clock_expression(frames)}'[base]",
        '[base][1:v]overlay=x=0:y=720:eof_action=pass:repeatlast=0:shortest=1:format=yuv420[out]',
    ]
    video = out / 'table_leadin.nut'
    subprocess.run([
        'ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-copyts',
        '-i', str(source), '-i', card['layer_path'],
        '-filter_complex', ';'.join(graph), '-map', '[out]', '-an',
        '-c:v', 'ffv1', '-level', '3', '-threads', '4', '-fps_mode', 'passthrough',
        '-enc_time_base', '1/12288', '-avoid_negative_ts', 'disabled', '-n', str(video),
    ], check=True)
    actual = recipe.probe_video(video, 4)
    ratio = Fraction(actual['time_base']) / Fraction('1/12288')
    if [frame['pts'] * ratio for frame in actual['frames']] != [frame['pts'] for frame in frames]:
        raise ValueError('Lead-in changed original PTS')
    duration_match = [frame['duration'] * ratio for frame in actual['frames']] == [frame['duration'] for frame in frames]
    clean = pixel_hashes(source, base)
    expected = [clean[i] for i in TOWER_INDICES]
    measured = pixel_hashes(video)
    if len(measured) != 4:
        raise ValueError('Lead-in frame count differs')
    upper = pixel_hashes(source, base + ',crop=1920:720:0:0')
    if pixel_hashes(video, 'crop=1920:720:0:0') != [upper[i] for i in TOWER_INDICES]:
        raise ValueError('Picture above the lead-in caption differs')
    for i, shown in enumerate(visible):
        if shown and measured[i] == expected[i]:
            raise ValueError(f'A KITE is missing on lead-in frame {i}')
        if not shown and measured[i] != expected[i]:
            raise ValueError(f'A KITE changes a still-clear lead-in frame {i}')
    recipe.require_hash(source, schedule['source_sha256'])
    recipe.require_hash(card['layer_path'], card['layer_sha256'])
    clock = out / 'original_clock.json'
    recipe.write_new(clock, {'time_base': '1/12288', 'frames': frames})
    result = {
        'job': 'J2242',
        'status': 'TABLE_LEADIN_INTERMEDIATE_ONLY',
        'path': str(video),
        'sha256': recipe.sha256_file(video),
        'timeline_frames': [423, 426],
        'source_frame_indices': list(TOWER_INDICES),
        'source_sha256': schedule['source_sha256'],
        'frame_count': 4,
        'label': 'A KITE',
        'visible_caption_local_frames': [i for i, shown in enumerate(visible) if shown],
        'original_pts_match': True,
        'original_durations_preserved_in_intermediate': duration_match,
        'original_clock_path': str(clock),
        'original_clock_sha256': recipe.sha256_file(clock),
        'above_caption_band_pixel_hashes_match': True,
        'table_source_used': False,
        'frame_2869': 'out',
        'master_created': False,
        'final_film_approval': False,
    }
    recipe.write_new(out / 'RESULT.json', result)
    print('table lead-in', 4, 'frames verified', flush=True)
    return result


def _row(mapping, name):
    found = [row for row in mapping['rows'] if row['row'] == name]
    if len(found) != 1:
        raise ValueError(f'Missing {name}')
    return found[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mapping', type=Path, required=True)
    parser.add_argument('--timeline', type=Path, required=True)
    parser.add_argument('--master', type=Path, default=recipe.DEFAULT_MASTER)
    parser.add_argument('--scratch', type=Path, required=True)
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    args = parser.parse_args()
    mapping = json.loads(args.mapping.read_text())
    if mapping.get('master_sha256') != recipe.MASTER_SHA:
        raise ValueError('Mapping was made against a different master')
    tower_row = _row(mapping, '02_tower_tilt')
    table_row = _row(mapping, '03_table_three')
    tower_ranked, table_ranked = measure(args.master, tower_row, table_row, args.scratch)
    print('tower', _ranked_record(tower_ranked), flush=True)
    print('table', _ranked_record(table_ranked), flush=True)
    schedule = leadin_schedule(tower_row, tower_ranked, table_row, table_ranked)
    root = recipe.EDIT_DIR.parents[2] / 'jobs/reviews/J2242'
    preflight = json.loads((root / 'SOURCE_PREFLIGHT.json').read_text())
    clock_sha = preflight['evidence_files']['source_timeline.json']['sha256']
    recipe.require_hash(args.timeline, clock_sha)
    timeline = json.loads(args.timeline.read_text())
    card = _kite_card(json.loads((root / 'CAPTION_LAYERS.json').read_text())['cards'])
    result = render_leadin(schedule, timeline, card, args.out_dir)
    recipe.require_hash(args.timeline, clock_sha)
    recipe.write_new(args.evidence, {
        'job': 'J2242',
        'status': 'TABLE_LEADIN_TOWER_CONTINUATION',
        'comparison': 'full-resolution upper 1920x720 after lanczos scale',
        'acceptance': {
            'maximum_per_pixel_mse': MAX_MSE,
            'minimum_runner_up_mse_margin': MIN_MARGIN,
            'tower_source_frames': list(TOWER_INDICES),
            'table_plate': 'unused; best MSE stays above 1000',
        },
        'tower': _ranked_record(tower_ranked),
        'table': _ranked_record(table_ranked),
        'render': result,
        'frame_2869': 'out',
        'safe_path': 'outstanding',
        'foil_frame_3353': 'outstanding',
        'master_created': False,
        'final_film_approval': False,
    })
    print(json.dumps({'status': result['status'], 'sha256': result['sha256']}))


if __name__ == '__main__':
    main()
