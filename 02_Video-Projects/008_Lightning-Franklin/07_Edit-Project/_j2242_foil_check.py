"""Confirm the 140s foil frame sits past the jar replacement.

Frame 3305 (138s) is the jar flip inside replacement 3260-3343, which ends
at 139.625s. Frame 3353 (140s) is the next keyframe envelope, 3344-3404.
Replacing the jar tail does not cover 3353. This check does not splice that
envelope, does not resolve the note, and does not make a master.
"""
import argparse
import json
import subprocess
from fractions import Fraction
from pathlib import Path

import numpy as np

import _build_rough_v13_recipe as recipe

REPLACE = (3260, 3343)
JAR_FLIP = 3305
FOIL_FRAME = 3353
ENVELOPE = (3344, 3404)
NEXT_KEY = 3405
REPLACEMENT_END = Fraction('139.625')
MAX_MSE = 9.0
MIN_MARGIN = 0.1
W, H = 1920, 720
FILTER = f'scale=1920:1080:flags=lanczos,crop={W}:{H}:0:0,format=gray'
PLATES = {
    '07_foil_jar': {
        'path': Path('/Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin/04_Generated-Clips/part02/raw/v01/07_foil_jar_t1.mp4'),
        'sha256': '8e28cc24ed747a60f6a305f3f1014a65ead7bde964a682bcb4939c527b59ec11',
    },
    '08_jar_spark': {
        'path': Path('/Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin/04_Generated-Clips/part02/raw/v01/08_jar_spark_t1.mp4'),
        'sha256': '6a24bb5487447e000f2041833f9ef8ef575f678a82ffc10c8ddbb513fa585b4c',
    },
}
MASTER_FRAMES = (3343, 3344, 3353)


def _index(frame):
    return frame['index'] if isinstance(frame, dict) else frame[0]


def _pts(frame):
    return frame['pts'] if isinstance(frame, dict) else frame[1]


def _duration(frame):
    return frame['duration'] if isinstance(frame, dict) else frame[2]


def _key(frame):
    return frame['key_frame'] if isinstance(frame, dict) else frame[3]


def frame_end(frames, index, time_base):
    """Return the exclusive end of one frame on the original clock."""
    row = next((frame for frame in frames if _index(frame) == index), None)
    if row is None:
        raise ValueError(f'Missing frame {index}')
    return Fraction(_pts(row) + _duration(row)) * Fraction(time_base)


def spark_envelope(frames):
    """Return 3344-3404 only when those are the real keyframe bounds."""
    keys = [_index(frame) for frame in frames if _key(frame)]
    if ENVELOPE[0] not in keys:
        raise ValueError('Frame 3344 is not a keyframe')
    nxt = next((key for key in keys if key > ENVELOPE[0]), None)
    if nxt != NEXT_KEY:
        raise ValueError(f'Next keyframe is {nxt}, expected {NEXT_KEY}')
    return ENVELOPE


def classify(row, frames, time_base):
    """Return the two Row 5 checks when they stay distinct and unresolved."""
    flip = row['jar_flip_2_18']
    spark = row['foil_next_spark_2_20']
    if spark.get('note_resolved') is not False:
        raise ValueError('2:20 note stays open')
    if spark.get('splice') is not False:
        raise ValueError('140s foil frame is not a splice')
    if spark.get('distinct_from_jar_flip') is not True or spark.get('beyond_replacement_ending_139_625s') is not True:
        raise ValueError('140s check must stay distinct and past the replacement')
    if spark.get('inside_replace_3260_3343') is not False:
        raise ValueError('140s frame is marked inside the jar replacement')
    flip_frame = recipe.clock_frame(frames, time_base, 138)
    foil_frame = recipe.clock_frame(frames, time_base, 140)
    if flip_frame != flip['master_frame'] or flip_frame != JAR_FLIP:
        raise ValueError('138s jar flip moved')
    if foil_frame != spark['master_frame'] or foil_frame != FOIL_FRAME:
        raise ValueError('140s foil frame moved')
    if not (REPLACE[0] <= flip_frame <= REPLACE[1]) or flip.get('inside_replace_3260_3343') is not True:
        raise ValueError('Jar flip left the replacement')
    if REPLACE[0] <= foil_frame <= REPLACE[1]:
        raise ValueError('140s frame fell inside the jar replacement')
    if frame_end(frames, REPLACE[1], time_base) != REPLACEMENT_END:
        raise ValueError('Replacement no longer ends at 139.625s')
    envelope = spark_envelope(frames)
    if not envelope[0] <= foil_frame <= envelope[1]:
        raise ValueError('140s frame left the spark envelope')
    if list(spark['candidate_keyframe_envelope']) != list(envelope):
        raise ValueError('Manifest envelope drifted')
    return {
        'jar_flip_frame': flip_frame,
        'foil_frame': foil_frame,
        'replacement': list(REPLACE),
        'replacement_end_s': '139.625',
        'spark_envelope': list(envelope),
        'jar_flip_inside_replacement': True,
        'foil_inside_replacement': False,
        'distinct': True,
        'note_resolved': False,
        'splice': False,
        'frame_2869': 'out',
    }


def plate_match(frame, plates, max_mse=MAX_MSE, min_margin=MIN_MARGIN):
    """Name the plate whose best frame matches, without picking a near-tie index."""
    if getattr(frame, 'ndim', None) != 1:
        raise ValueError('Master frame must be one upper-band row')
    if len(plates) < 2:
        raise ValueError('Need both the foil jar and the jar spark')
    scores = []
    image = frame.astype(np.float32)
    for name in sorted(plates):
        source = plates[name]
        if getattr(source, 'ndim', None) != 2 or source.shape[1] != frame.shape[0] or len(source) < 2:
            raise ValueError(f'{name} is not a comparable plate')
        mse = np.mean((source.astype(np.float32) - image) ** 2, axis=1)
        order = np.argsort(mse, kind='stable')
        best, second = int(order[0]), int(order[1])
        scores.append({
            'plate': name,
            'best': best,
            'second': second,
            'best_mse': float(mse[best]),
            'frame_margin': float(mse[second] - mse[best]),
        })
    scores.sort(key=lambda item: (item['best_mse'], item['plate']))
    winner, runner = scores[0], scores[1]
    plate_margin = float(runner['best_mse'] - winner['best_mse'])
    identified = winner['best_mse'] <= max_mse and plate_margin >= min_margin
    return {
        'plate': winner['plate'] if identified else None,
        'source_frame': winner['best'] if identified else None,
        'source_frame_unique': bool(identified and winner['frame_margin'] >= min_margin),
        'best_mse': winner['best_mse'],
        'plate_margin': plate_margin,
        'scores': scores,
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


def _frame_count(path):
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames',
         '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', str(path)],
        check=True, capture_output=True, text=True)
    count = int(result.stdout.strip())
    if count < 2:
        raise ValueError(f'{path.name} has {count} frames')
    return count


def measure(master, plates, scratch):
    """Compare master frames 3343, 3344 and 3353 with the two pinned plates."""
    scratch = Path(scratch)
    scratch.mkdir(parents=True)
    recipe.require_hash(master, recipe.MASTER_SHA, recipe.MASTER_BYTES)
    decoded = {}
    for name, plate in plates.items():
        recipe.require_hash(plate['path'], plate['sha256'])
        count = _frame_count(plate['path'])
        decoded[name] = _decode(plate['path'], scratch / f'{name}.raw', count)
    select = '+'.join(f'eq(n,{index})' for index in MASTER_FRAMES)
    master_frames = _decode(master, scratch / 'master.raw', len(MASTER_FRAMES), f"select='{select}'")
    recipe.require_hash(master, recipe.MASTER_SHA, recipe.MASTER_BYTES)
    compared = {}
    for index, image in zip(MASTER_FRAMES, master_frames):
        match = plate_match(image, decoded)
        compared[str(index)] = match
    foil = compared[str(FOIL_FRAME)]
    tail = compared[str(REPLACE[1])]
    if foil['plate'] != '08_jar_spark':
        raise ValueError('Frame 3353 is not the jar-spark plate')
    if tail['plate'] != '07_foil_jar':
        raise ValueError('Frame 3343 is not the foil-jar plate')
    if foil['plate'] == tail['plate']:
        raise ValueError('The 140s frame is the same plate as the jar tail')
    for raw in scratch.glob('*.raw'):
        raw.unlink()
    return compared


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--timeline', type=Path, required=True)
    parser.add_argument('--master', type=Path, default=recipe.DEFAULT_MASTER)
    parser.add_argument('--scratch', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads((recipe.EDIT_DIR / 'J2163_CORRECTION_MANIFEST.json').read_text())
    row = next(item for item in manifest['eight_rows'] if item.get('timestamp') == '2:20')
    timeline = json.loads(args.timeline.read_text())
    clock = classify(row, timeline['frames'], timeline['time_base'])
    compared = measure(args.master, PLATES, args.scratch)
    recipe.write_new(args.evidence, {
        'job': 'J2242',
        'status': 'FOIL_CHECK_DISTINCT',
        'clock': clock,
        'frames': compared,
        'still_check': 'pixel match only; not a motion review or an audio review',
        'note_resolved': False,
        'splice': False,
        'frame_2869': 'out',
        'master_created': False,
        'final_film_approval': False,
    })
    print(json.dumps({
        'status': 'FOIL_CHECK_DISTINCT',
        'foil_plate': compared[str(FOIL_FRAME)]['plate'],
        'foil_source_frame': compared[str(FOIL_FRAME)]['source_frame'],
        'tail_plate': compared[str(REPLACE[1])]['plate'],
    }))


if __name__ == '__main__':
    main()
