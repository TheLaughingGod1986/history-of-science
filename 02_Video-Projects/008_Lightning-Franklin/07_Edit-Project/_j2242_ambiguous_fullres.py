"""Full-resolution upper-band check for caption rows the low-res map will not render.

A row stays rejected unless every full-resolution winner matches the low-resolution
index, per-pixel MSE stays within the existing map threshold, and the runner-up
margin clears that same threshold. This does not render, mux, or approve a film.
"""
import argparse
import json
import subprocess
from pathlib import Path

import numpy as np

import _build_rough_v13_recipe as recipe

W, H = 1920, 720
FILTER = f'scale=1920:1080:flags=lanczos,crop={W}:{H}:0:0,format=gray'
MAX_MSE = 9.0
MIN_MARGIN = 0.1
TARGET_ROWS = ('02_knuckle_spark', '14_royal_society', '07_giant_spark')
CONTROL_ROW = '12_steeple_fire'


def rank_upper_band(master, source):
    """Return best and runner-up source indices for each master frame.

    master is (N, P) and source is (M, P), both uint8. MSE is per pixel.
    """
    if master.ndim != 2 or source.ndim != 2 or master.shape[1] != source.shape[1]:
        raise ValueError('Upper-band arrays must share a pixel width')
    if len(master) == 0 or len(source) < 2:
        raise ValueError('Need master frames and at least two source frames')
    source_f = source.astype(np.float32)
    ranked = []
    for image in master:
        mse = np.mean((source_f - image.astype(np.float32)) ** 2, axis=1)
        order = np.argsort(mse, kind='stable')
        best, second = int(order[0]), int(order[1])
        ranked.append({
            'best': best,
            'second': second,
            'best_mse': float(mse[best]),
            'margin': float(mse[second] - mse[best]),
        })
    return ranked


def accepted_fullres_indices(row, max_mse=MAX_MSE, min_margin=MIN_MARGIN):
    """Return a full-resolution schedule when every frame is uniquely identified.

    Disagreement with the coarser low-resolution index is allowed. A frame whose
    best per-pixel MSE is above the threshold, or whose runner-up margin is
    below it, rejects the whole row. Nothing here renders or approves a film.
    """
    frames = row.get('frames') or []
    if not frames:
        raise ValueError('No full-resolution frames')
    lo, hi = row['timeline_frames']
    if hi - lo + 1 != len(frames):
        raise ValueError('Full-resolution count differs from its timeline window')
    indices = []
    for i, frame in enumerate(frames):
        if frame.get('local_index') != i or frame.get('master_frame') != lo + i:
            raise ValueError('Full-resolution frames are out of order')
        best = frame.get('fullres_best')
        if type(best) is not int or best < 0:
            raise ValueError('Invalid full-resolution index')
        if frame['best_mse'] > max_mse or frame['margin'] < min_margin:
            raise ValueError(f'{row.get("row", "row")} local {i} is not a unique full-resolution match')
        indices.append(best)
    if any(b < a for a, b in zip(indices, indices[1:])):
        raise ValueError('Backward full-resolution schedule')
    return indices


def judge_row(lowres_indices, ranked, max_mse=MAX_MSE, min_margin=MIN_MARGIN):
    """Accept a schedule only when full resolution confirms every low-res index."""
    if len(lowres_indices) != len(ranked) or not lowres_indices:
        raise ValueError('Full-resolution count differs from the low-resolution map')
    if any(type(i) is not int or i < 0 for i in lowres_indices):
        raise ValueError('Low-resolution indices must be non-negative ints')
    flips = [i for i, (low, item) in enumerate(zip(lowres_indices, ranked)) if low != item['best']]
    worst = max(item['best_mse'] for item in ranked)
    margin = min(item['margin'] for item in ranked)
    unique = not flips and worst <= max_mse and margin >= min_margin
    return {
        'frame_count': len(ranked),
        'maximum_mse': worst,
        'minimum_runner_up_mse_margin': margin,
        'winner_flip_count': len(flips),
        'winner_flip_local_frames': flips,
        'unique_match': unique,
        'reconstructed': False,
    }


def _decode(path, out_raw, count, selection=None):
    filters = (selection + ',' if selection else '') + FILTER
    subprocess.run(
        ['ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-i', str(path), '-an',
         '-vf', filters, '-fps_mode', 'passthrough', '-pix_fmt', 'gray',
         '-f', 'rawvideo', '-y', str(out_raw)],
        check=True)
    expected = count * W * H
    if out_raw.stat().st_size != expected:
        raise ValueError(f'{path.name} decoded {out_raw.stat().st_size} bytes, expected {expected}')
    return np.memmap(out_raw, dtype=np.uint8, mode='r', shape=(count, H * W))


def _windows(rows):
    windows = []
    for row in rows:
        lo, hi = row['timeline_frames']
        count = hi - lo + 1
        if count != len(row['source_frame_indices']):
            raise ValueError(f'{row["row"]} map length differs from its window')
        windows.append((lo, hi, count))
    if windows != sorted(windows):
        raise ValueError('Master windows must be decoded in timeline order')
    return windows


def measure(mapping, master, scratch):
    by_name = {row['row']: row for row in mapping['rows']}
    names = (CONTROL_ROW, *TARGET_ROWS)
    if any(name not in by_name for name in names):
        raise ValueError('Caption map is missing a measured row')
    rows = [by_name[name] for name in names]
    windows = _windows(rows)
    scratch = Path(scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    select = '+'.join(f'between(n,{lo},{hi})' for lo, hi, _ in windows)
    master_count = sum(count for _, _, count in windows)
    master_raw = scratch / 'master_upper.raw'
    decoded_master = _decode(master, master_raw, master_count, f"select='{select}'")
    offset = 0
    results = []
    for row, (lo, hi, count) in zip(rows, windows):
        source = Path(row['source_path'])
        recipe.require_hash(source, row['source_sha256'])
        source_raw = scratch / f'{row["row"]}_source.raw'
        decoded_source = _decode(source, source_raw, row['decoded_source_frames'])
        ranked = rank_upper_band(decoded_master[offset:offset + count], np.asarray(decoded_source))
        offset += count
        verdict = judge_row(row['source_frame_indices'], ranked)
        frames = []
        for local, (low, item) in enumerate(zip(row['source_frame_indices'], ranked)):
            frames.append({
                'local_index': local,
                'master_frame': lo + local,
                'lowres_index': low,
                'fullres_best': item['best'],
                'fullres_second': item['second'],
                'best_mse': item['best_mse'],
                'margin': item['margin'],
                'winner_matches_lowres': low == item['best'],
            })
        results.append({
            'row': row['row'],
            'role': 'control' if row['row'] == CONTROL_ROW else 'ambiguous',
            'timeline_frames': [lo, hi],
            'source_sha256': row['source_sha256'],
            'decoded_source_frames': row['decoded_source_frames'],
            'lowres_ambiguous_local_frames': row['ambiguous_local_frames'],
            **verdict,
            'frames': frames,
        })
        print(row['row'], 'max MSE', round(verdict['maximum_mse'], 3),
              'min margin', round(verdict['minimum_runner_up_mse_margin'], 4),
              'flips', verdict['winner_flip_count'],
              'unique', verdict['unique_match'], flush=True)
    if offset != master_count:
        raise ValueError('Master windows were not fully consumed')
    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--mapping', type=Path, required=True)
    ap.add_argument('--master', type=Path, default=recipe.DEFAULT_MASTER)
    ap.add_argument('--scratch', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    recipe.require_hash(args.master, recipe.MASTER_SHA, recipe.MASTER_BYTES)
    mapping = json.loads(args.mapping.read_text())
    if mapping.get('master_sha256') != recipe.MASTER_SHA:
        raise ValueError('Mapping was made against a different master')
    results = measure(mapping, args.master, args.scratch)
    recipe.require_hash(args.master, recipe.MASTER_SHA, recipe.MASTER_BYTES)
    recipe.write_new(args.out, {
        'job': 'J2242',
        'status': 'FULLRES_UPPER_BAND_MAPPING_ONLY',
        'comparison_filter': FILTER,
        'acceptance': {
            'maximum_per_pixel_mse': MAX_MSE,
            'minimum_runner_up_mse_margin': MIN_MARGIN,
            'winner_must_match_lowres_index': True,
        },
        'rows': results,
        'limitations': (
            'Full-resolution upper-band MSE against the graded master. '
            'Not a composite, motion review, audio review, or film approval.'
        ),
        'master_created': False,
        'final_film_approval': False,
    })


if __name__ == '__main__':
    main()
