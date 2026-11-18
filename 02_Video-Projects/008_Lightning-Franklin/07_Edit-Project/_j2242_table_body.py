"""Reconstruct only the clean table body, master frames 427–544.

Frames 423–426 match the table source at MSE about 3380 and are left
unreconstructed. No master, audio, or film approval.
"""
import argparse
import json
import subprocess
from fractions import Fraction
from pathlib import Path
import _build_rough_v13_recipe as recipe
from _j2242_caption_composites import row_clock, source_graph, source_runs
from _j2242_caption_layers import clock_expression
from _j2242_salon_patch import pixel_hashes


def table_body_schedule(row):
    """Accept only the measured table split. Anything else stays rejected."""
    idx = row['source_frame_indices']
    lo, hi = row['timeline_frames']
    if row.get('row') != '03_table_three' or [lo, hi] != [423, 544] or len(idx) != 122:
        raise ValueError('Table window changed')
    if row.get('poor_match_local_frames') != [0, 1, 2, 3] or row.get('ambiguous_local_frames') or row.get('nonmonotonic_steps') != [4]:
        raise ValueError('Table boundary flags changed')
    if idx[:4] != [52, 52, 52, 52] or idx[4:] != list(range(118)):
        raise ValueError('Table body is not source frames 0 through 117')
    mse = row.get('per_frame_mse')
    if mse is not None and (len(mse) != 122 or min(mse[:4]) <= 1000 or max(mse[4:]) > 9):
        raise ValueError('Table match quality changed')
    return dict(row='03_table_three', timeline_frames=[427, 544], source_frame_indices=list(range(118)),
                source_path=row['source_path'], source_sha256=row['source_sha256'],
                rejected_master_frames=[423, 426], rejected_source_index=52,
                poor_match_local_frames=[], ambiguous_local_frames=[], nonmonotonic_steps=[])


def render_table_body(row, timeline, cards, out):
    body = table_body_schedule(row)
    frames = row_clock(timeline, body)
    selected = [c for c in cards if c['row'] == '03_table_three']
    expected_cards = [('A KITE', 423, 462), ('A KEY', 463, 503), ('A JAR', 504, 544)]
    if [(c['label'], c['frame_in'], c['frame_last']) for c in selected] != expected_cards:
        raise ValueError('Table caption cards changed')
    source = Path(body['source_path'])
    recipe.require_hash(source, body['source_sha256'])
    native = recipe.probe_video(source)
    tb = Fraction(native['time_base'])
    if any(f['pts'] * tb != Fraction(i, 24) or f['duration'] * tb != Fraction(1, 24) for i, f in enumerate(native['frames'][:118])):
        raise ValueError('Table source is not native 24fps')
    out.mkdir(exist_ok=False)
    inputs = ['-i', str(source)]
    base = 'scale=1920:1080:flags=lanczos,setsar=1,format=yuv420p'
    graph = [source_graph(body['source_frame_indices']),
             f"[ordered]{base},settb=1/12288,setpts='{clock_expression(frames)}'[base]"]
    previous = 'base'
    for i, card in enumerate(selected, 1):
        # A KITE begins on the rejected preceding frames. Its later frames are in this body.
        if card['frame_in'] < 423 or card['frame_last'] > 544 or card['frame_last'] < 427:
            raise ValueError('Table card falls outside the known windows')
        recipe.require_hash(card['layer_path'], card['layer_sha256'])
        recipe.require_hash(card['original_clock_path'], card['original_clock_sha256'])
        inputs += ['-i', card['layer_path']]
        current = f'c{i}'
        graph.append(f'[{previous}][{i}:v]overlay=x=0:y=720:eof_action=pass:repeatlast=0:format=yuv420[{current}]')
        previous = current
    video = out / 'table_body.nut'
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-copyts', *inputs,
                    '-filter_complex', ';'.join(graph), '-map', f'[{previous}]', '-an',
                    '-c:v', 'ffv1', '-level', '3', '-threads', '4', '-fps_mode', 'passthrough',
                    '-enc_time_base', '1/12288', '-avoid_negative_ts', 'disabled', '-n', str(video)], check=True)
    actual = recipe.probe_video(video, 118)
    ratio = Fraction(actual['time_base']) / Fraction('1/12288')
    if [f['pts'] * ratio for f in actual['frames']] != [f['pts'] for f in frames]:
        raise ValueError('Table body changed original PTS')
    duration_match = [f['duration'] * ratio for f in actual['frames']] == [f['duration'] for f in frames]
    expected = pixel_hashes(source, base)[:118]
    measured = pixel_hashes(video)
    if len(expected) != 118 or len(measured) != 118:
        raise ValueError('Table body frame count differs')
    upper = pixel_hashes(source, base + ',crop=1920:720:0:0')[:118]
    if pixel_hashes(video, 'crop=1920:720:0:0') != upper:
        raise ValueError('Picture above the table caption differs')
    for card in selected:
        peak = (card['frame_in'] + card['frame_last']) // 2 - 427
        if peak < 0 or peak >= 118 or measured[peak] == expected[peak]:
            raise ValueError('Table caption missing inside the body')
        recipe.require_hash(card['layer_path'], card['layer_sha256'])
    # Frame 427 is already four frames into A KITE, so the first body frame carries the card.
    if measured[0] == expected[0]:
        raise ValueError('Opening table card is absent on the first body frame')
    recipe.require_hash(source, body['source_sha256'])
    clock = out / 'original_clock.json'
    recipe.write_new(clock, dict(time_base='1/12288', frames=frames))
    result = dict(job='J2242', status='TABLE_BODY_INTERMEDIATE_ONLY', path=str(video),
                  sha256=recipe.sha256_file(video), timeline_frames=[427, 544],
                  rejected_master_frames=[423, 426], rejected_reason='Low-resolution MSE about 3380 against table source frame 52. Not reconstructed.',
                  source_frame_indices=[0, 117], source_runs=source_runs(body['source_frame_indices']),
                  source_sha256=body['source_sha256'], frame_count=118, caption_count=3,
                  original_pts_match=True, original_durations_preserved_in_intermediate=duration_match,
                  original_clock_path=str(clock), original_clock_sha256=recipe.sha256_file(clock),
                  above_caption_band_pixel_hashes_match=True, caption_midpoints_present=True,
                  first_body_frame_has_caption=True, clear_tail_inside_body=0,
                  master_created=False, final_film_approval=False,
                  final_mux_duration_verification='OUTSTANDING')
    recipe.write_new(out / 'RESULT.json', result)
    print('03_table_three body', 118, 'frames verified', flush=True)
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--mapping', type=Path, required=True)
    ap.add_argument('--timeline', type=Path, required=True)
    ap.add_argument('--out-dir', type=Path, required=True)
    a = ap.parse_args()
    root = recipe.EDIT_DIR.parents[2] / 'jobs/reviews/J2242'
    evidence = json.loads((root / 'SOURCE_PREFLIGHT.json').read_text())
    clock_sha = evidence['evidence_files']['source_timeline.json']['sha256']
    recipe.require_hash(a.timeline, clock_sha)
    mapping = json.loads(a.mapping.read_text())
    mapping_sha = recipe.sha256_file(a.mapping)
    row = next(r for r in mapping['rows'] if r['row'] == '03_table_three')
    layers = json.loads((root / 'CAPTION_LAYERS.json').read_text())
    timeline = json.loads(a.timeline.read_text())
    result = render_table_body(row, timeline, layers['cards'], a.out_dir)
    recipe.require_hash(a.mapping, mapping_sha)
    recipe.require_hash(a.timeline, clock_sha)
    result['mapping_sha256'] = mapping_sha
    print(json.dumps({k: result[k] for k in ('status', 'sha256', 'frame_count', 'timeline_frames')}))


if __name__ == '__main__':
    main()
