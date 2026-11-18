"""Place three picture-title overlays by a unique full-frame match.

The cut clock is the wrong map for two of them. The first clock frame of
06_same_thing is the previous picture, and 08_looking_path sits 22 frames
after its cut starts. A placement is the one shift whose postcard-sized
mean absolute error stays under the ceiling and clear of the runner-up.
Frame 2869 stays out. This does not write a master.
"""
import json
from pathlib import Path

import numpy as np

import _build_rough_v13_recipe as recipe

W, H = 96, 54
MATCH_MEAN_MAX = 0.5
# One fire frame carries a moving diagram, so its postcard error is 3.3
# while the sequence mean stays 0.21. A wrong alignment still fails the mean.
FRAME_MAE_MAX = 3.5
MARGIN_MIN = 0.9
PLACED_TITLES = ('15_likeness_fire', '06_same_thing', '08_looking_path')
# Cut-clock windows, kept so a pixel placement can be compared with them.
CLOCK_WINDOWS = {
    '15_likeness_fire': (4016, 4129),
    '06_same_thing': (8188, 8348),
    '08_looking_path': (10755, 10830),
}
# Locks the measurement already made on master v03. A later signature that
# lands somewhere else must stop, not silently move the splice.
PROVED_FRAMES = {
    '15_likeness_fire': (4016, 4129),
    '06_same_thing': (8189, 8348),
    '08_looking_path': (10777, 10852),
}
FULL_RES_SPOTS = {
    '15_likeness_fire': [
        {'master_frame': 4016, 'overlay_frame': 0, 'mae': 0.560, 'match': True},
        {'master_frame': 4069, 'overlay_frame': 53, 'mae': 0.949, 'match': True},
        {'master_frame': 4129, 'overlay_frame': 113, 'mae': 5.384, 'match': True},
    ],
    '06_same_thing': [
        {'master_frame': 8188, 'overlay_frame': 0, 'mae': 39.773, 'match': False},
        {'master_frame': 8189, 'overlay_frame': 0, 'mae': 0.554, 'match': True},
        {'master_frame': 8348, 'overlay_frame': 159, 'mae': 1.119, 'match': True},
    ],
    '08_looking_path': [
        {'master_frame': 10755, 'overlay_frame': 0, 'mae': 54.880, 'match': False},
        {'master_frame': 10777, 'overlay_frame': 0, 'mae': 1.387, 'match': True},
        {'master_frame': 10825, 'overlay_frame': 48, 'mae': 2.258, 'match': True},
        {'master_frame': 10852, 'overlay_frame': 75, 'mae': 2.316, 'match': True},
    ],
}


def slide_mae(master, overlay):
    """Mean absolute error of every alignment of overlay inside master."""
    if master.ndim != 3 or overlay.ndim != 3 or master.shape[1:] != overlay.shape[1:]:
        raise ValueError('Master and overlay must be frame stacks of one shape')
    if len(overlay) < 1 or len(master) < len(overlay):
        raise ValueError('Overlay must be at least one frame and fit in the master')
    scores = np.empty(len(master) - len(overlay) + 1, dtype=np.float64)
    flat_m = np.asarray(master, dtype=np.float64).reshape(len(master), -1)
    flat_o = np.asarray(overlay, dtype=np.float64).reshape(len(overlay), -1)
    step = 32
    for start in range(0, scores.size, step):
        stop = min(scores.size, start + step)
        windows = np.stack([flat_m[i:i + len(overlay)] for i in range(start, stop)])
        scores[start:stop] = np.abs(windows - flat_o).mean(axis=(1, 2))
    return scores


def choose_shift(master, overlay, mean_max=MATCH_MEAN_MAX, frame_max=FRAME_MAE_MAX,
                 margin_min=MARGIN_MIN):
    """Return the one safe shift, or refuse a weak or tied match."""
    scores = slide_mae(master, overlay)
    order = np.argsort(scores)
    best = int(order[0])
    mean = float(scores[best])
    margin = float(scores[order[1]] - mean) if scores.size > 1 else float('inf')
    per = np.abs(
        np.asarray(master[best:best + len(overlay)], dtype=np.float64)
        - np.asarray(overlay, dtype=np.float64)
    ).mean(axis=(1, 2))
    worst = float(per.max())
    if mean > mean_max or worst > frame_max or margin < margin_min:
        raise ValueError(
            f'No unique title match: mean {mean:.4f}, worst {worst:.4f}, margin {margin:.4f}')
    return {
        'first': best,
        'last': best + len(overlay) - 1,
        'frames': int(len(overlay)),
        'mean_mae': round(mean, 4),
        'worst_frame_mae': round(worst, 4),
        'margin': round(margin, 4),
    }


def load_raw(path, frames, width=W, height=H):
    data = np.fromfile(path, dtype=np.uint8)
    expected = frames * width * height
    if data.size != expected:
        raise ValueError(f'{path} has {data.size} bytes, expected {expected}')
    return data.reshape(frames, height, width)


def placement_report(master, overlays):
    """Place each named overlay. overlays maps a row name to its frame stack."""
    if tuple(overlays) != PLACED_TITLES:
        raise ValueError('Title overlays are not the three picture rows')
    rows = []
    for name in PLACED_TITLES:
        found = choose_shift(master, overlays[name])
        expect = PROVED_FRAMES[name]
        if (found['first'], found['last']) != expect:
            raise ValueError(f'{name} landed on {found["first"]}-{found["last"]}, not {expect}')
        clock = CLOCK_WINDOWS[name]
        lead = [clock[0], found['first'] - 1] if found['first'] > clock[0] else None
        past = [clock[1] + 1, found['last']] if found['last'] > clock[1] else None
        rows.append({
            'row': name,
            'status': 'PLACED',
            'master_frames': [found['first'], found['last']],
            'frames': found['frames'],
            'clock_frames': list(clock),
            'clock_matches_pixels': list(clock) == [found['first'], found['last']],
            'clock_frames_before_picture': lead,
            'frames_past_the_cut': past,
            'mean_mae': found['mean_mae'],
            'worst_frame_mae': found['worst_frame_mae'],
            'margin': found['margin'],
            'scale': f'{W}x{H} gray',
            'full_resolution_spots': FULL_RES_SPOTS[name],
        })
    return {
        'job': 'J2242',
        'status': 'TITLE_ROWS_PLACED',
        'rows': rows,
        'match_mean_max': MATCH_MEAN_MAX,
        'frame_mae_max': FRAME_MAE_MAX,
        'margin_min': MARGIN_MIN,
        'frame_2869': 'out',
        'master_created': False,
        'final_film_approval': False,
        'motion_review': False,
        'audio_review': False,
        'postcard_match': '96x54 gray mean absolute error; not a motion review',
    }


def read_placement(path):
    """Return splice ranges from a placement record that still meets its ceiling."""
    data = json.loads(Path(path).read_text())
    if data.get('status') != 'TITLE_ROWS_PLACED' or data.get('master_created') is not False:
        raise ValueError('Title placement is not a proved no-master record')
    rows = data.get('rows') or []
    if tuple(row.get('row') for row in rows) != PLACED_TITLES:
        raise ValueError('Placed title rows changed')
    changes = []
    for row in rows:
        if row.get('status') != 'PLACED':
            raise ValueError(f'{row.get("row")} is not placed')
        first, last = row['master_frames']
        if not isinstance(first, int) or not isinstance(last, int):
            raise ValueError('Placed frames must be integers')
        if last - first + 1 != row['frames']:
            raise ValueError(f'{row["row"]} frame count does not match its span')
        if row['mean_mae'] > data['match_mean_max'] or row['margin'] < data['margin_min']:
            raise ValueError(f'{row["row"]} is weaker than the recorded ceiling')
        if row['worst_frame_mae'] > data['frame_mae_max']:
            raise ValueError(f'{row["row"]} has a frame over the match ceiling')
        if (first, last) != PROVED_FRAMES[row['row']]:
            raise ValueError(f'{row["row"]} no longer matches the proved frames')
        changes.append({
            'name': row['row'],
            'first': first,
            'last': last,
            'source': 'TITLE_PLACE.json',
        })
    return changes


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--signature-dir', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--master-frames', type=int, default=12923)
    args = parser.parse_args()
    master = load_raw(args.signature_dir / 'master_full.raw', args.master_frames)
    overlays = {}
    counts = {'15_likeness_fire': 114, '06_same_thing': 160, '08_looking_path': 76}
    files = {
        '15_likeness_fire': 'overlay_fire.raw',
        '06_same_thing': 'overlay_same.raw',
        '08_looking_path': 'overlay_path.raw',
    }
    for name, count in counts.items():
        overlays[name] = load_raw(args.signature_dir / files[name], count)
    recipe.write_new(args.evidence, placement_report(master, overlays))


if __name__ == '__main__':
    main()
