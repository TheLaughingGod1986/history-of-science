"""Review the ten code-graphic rows that are not side-label cards.

The cut list names ten rows whose on-screen words are outside the 32
caption cards. This measures one midpoint frame of the current master for
each row. A flat brown diagram is a field. A picture with no dark bar in
the caption band has no bottom panel. Neither result is a film approval,
and Ben's readability note stays open. Frame 2869 stays out. No master
is written.
"""
import argparse
import json
import subprocess
from fractions import Fraction
from pathlib import Path

import numpy as np

import _build_rough_v13_recipe as recipe

EXPECTED_ROWS = (
    '14_likeness_pairs',
    '15_likeness_fire',
    '03_rod_cloud',
    '04_letter_crosses',
    '15_wet_dry',
    '06_same_thing',
    '08_teach_charge',
    '08_looking_path',
    '09_wood_vs_metal',
    '10_metal_easy',
)
FLAT_STD_MAX = 26.0
FLAT_MEAN = (70.0, 95.0)
W, H = 1920, 1080

# Words read from the saved midpoint stills. Not OCR, and not a motion review.
STILL_NOTES = {
    '14_likeness_pairs': {
        'words': 'SAME COLOUR · CROOKED LINES',
        'word_count': 4,
        'seat': 'top of the flat field',
        'bottom_panel': False,
    },
    '15_likeness_fire': {
        'words': 'CRACK · FIRE · SHOCK',
        'word_count': 3,
        'seat': 'upper area, over the picture',
        'bottom_panel': False,
    },
    '03_rod_cloud': {
        'words': 'DRAWING CHARGE FROM CLOUD',
        'word_count': 4,
        'seat': 'bottom of the flat field',
        'bottom_panel': False,
    },
    '04_letter_crosses': {
        'words': 'PHILADELPHIA TO PARIS',
        'word_count': 3,
        'seat': 'upper area, over the picture, with two box labels',
        'bottom_panel': False,
        'extra_labels': ['PHILADELPHIA', 'PARIS'],
    },
    '15_wet_dry': {
        'words': 'WET TWINE · DRY SILK',
        'word_count': 4,
        'seat': 'upper area of the flat field',
        'bottom_panel': False,
    },
    '06_same_thing': {
        'words': '',
        'word_count': 0,
        'seat': 'midpoint has line diagrams and no title; a later still reads ELECTRICITY over the picture',
        'bottom_panel': False,
    },
    '08_teach_charge': {
        'words': 'NO BOLT, JUST CHARGE',
        'word_count': 4,
        'seat': 'upper area of the flat field',
        'bottom_panel': False,
    },
    '08_looking_path': {
        'words': 'EASIEST PATH DOWN',
        'word_count': 3,
        'seat': 'upper area, over cloud',
        'bottom_panel': False,
    },
    '09_wood_vs_metal': {
        'words': 'WOOD AND STONE RESIST',
        'word_count': 4,
        'seat': 'upper area of the flat field',
        'bottom_panel': False,
    },
    '10_metal_easy': {
        'words': 'METAL CONDUCTS',
        'word_count': 2,
        'seat': 'upper area, over brick',
        'bottom_panel': False,
    },
}


def code_rows(cuts, labels):
    """Return the ten code-graphic rows, and keep the safe-path title separate."""
    bottom = recipe.reconcile_bottom_text(cuts, labels)
    rows = [row for row in bottom['other_onscreen_text'] if row['kind'] == 'code_graphic_or_overlay']
    names = tuple(row['row'] for row in rows)
    if names != EXPECTED_ROWS:
        raise ValueError(f'Code-graphic rows changed: {names}')
    safe = [row['row'] for row in bottom['other_onscreen_text'] if row['kind'] == 'title_outside_side_label']
    if safe != ['11_safe_path']:
        raise ValueError(f'Safe path is no longer its own title row: {safe}')
    by_name = {cut['row']: cut for cut in cuts}
    for name in names:
        if by_name[name].get('side_label'):
            raise ValueError(f'{name} now has a side label')
    if len(STILL_NOTES) != len(EXPECTED_ROWS) or tuple(STILL_NOTES) != EXPECTED_ROWS:
        raise ValueError('Still notes do not match the ten rows')
    for name, note in STILL_NOTES.items():
        if note['word_count'] > 4:
            raise ValueError(f'{name} still note is over four words')
        if note['bottom_panel'] is not False:
            raise ValueError(f'{name} still note claims a caption panel')
    return rows


def midpoint_frame(row, frames, time_base):
    """Return the master frame that contains the middle of this row."""
    start = Fraction(str(row['timeline_in']))
    end = Fraction(str(row['timeline_out']))
    if end <= start:
        raise ValueError(f'{row["row"]} ends before it starts')
    return recipe.clock_frame(frames, time_base, (start + end) / 2)


def field_kind(gray):
    """Classify one full frame. A flat diagram is not a caption panel."""
    if getattr(gray, 'shape', None) != (H, W):
        raise ValueError('Expected one 1920x1080 gray frame')
    image = gray.astype(np.float32)
    mean = float(image.mean())
    std = float(image.std())
    flat = std <= FLAT_STD_MAX and FLAT_MEAN[0] <= mean <= FLAT_MEAN[1]
    band = image[760:1000]
    median = float(np.median(band))
    # A caption panel is a flat fill. A dark street or a roof is not.
    fill = float(np.mean(np.abs(band - median) <= 12))
    center = band[:, 480:1440]
    contrast = float(np.percentile(center, 95) - np.median(center))
    panel = not flat and fill >= 0.72 and 35 <= median <= 110 and contrast >= 40
    return {
        'flat_field': bool(flat),
        'picture': not bool(flat),
        'bottom_panel': bool(panel),
        'frame_mean': round(mean, 3),
        'frame_std': round(std, 3),
        'bottom_fill': round(fill, 3),
        'bottom_contrast': round(contrast, 3),
    }


def decode_frames(master, indices, scratch):
    """Decode the named master frames in one forward pass."""
    indices = [int(index) for index in indices]
    if indices != sorted(indices) or len(set(indices)) != len(indices):
        raise ValueError('Frame indices must be unique and in order')
    select = '+'.join(f'eq(n,{index})' for index in indices)
    out = Path(scratch) / 'frames.raw'
    subprocess.run(
        ['ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-i', str(master), '-an',
         '-vf', f"select='{select}',format=gray", '-fps_mode', 'passthrough',
         '-pix_fmt', 'gray', '-f', 'rawvideo', '-y', str(out)],
        check=True)
    expected = len(indices) * W * H
    if out.stat().st_size != expected:
        raise ValueError(f'Decoded {out.stat().st_size} bytes, expected {expected}')
    data = np.fromfile(out, dtype=np.uint8).reshape(len(indices), H, W)
    out.unlink()
    return data


def measure(master, rows, frames, time_base, scratch):
    """Classify the midpoint of each code-graphic row on the current master."""
    scratch = Path(scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    recipe.require_hash(master, recipe.MASTER_SHA, recipe.MASTER_BYTES)
    indexed = [(row, midpoint_frame(row, frames, time_base)) for row in rows]
    decoded = decode_frames(master, [index for _, index in indexed], scratch)
    found = []
    for (row, index), gray in zip(indexed, decoded):
        kind = field_kind(gray)
        note = STILL_NOTES[row['row']]
        found.append({
            'row': row['row'],
            'master_frame': index,
            'timeline_in': row['timeline_in'],
            'timeline_out': row['timeline_out'],
            **kind,
            'still_words': note['words'],
            'still_word_count': note['word_count'],
            'still_seat': note['seat'],
            'still_bottom_panel': note['bottom_panel'],
        })
    recipe.require_hash(master, recipe.MASTER_SHA, recipe.MASTER_BYTES)
    pictures = [item['row'] for item in found if item['picture']]
    flats = [item['row'] for item in found if item['flat_field']]
    if any(item['bottom_panel'] for item in found):
        raise ValueError('A midpoint grew a bottom panel; review that frame before recording it')
    return {'rows': found, 'flat_fields': flats, 'pictures_without_panel': pictures}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--master', type=Path, default=recipe.DEFAULT_MASTER)
    parser.add_argument('--scratch', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    args = parser.parse_args()
    manifest = recipe.load_manifest()
    cuts = json.loads((recipe.EDIT_DIR / '_desk/008/rough_v12/cuts_rough_v12.json').read_text())
    timeline = json.loads((recipe.EDIT_DIR / 'J2163_MASTER_FRAME_PTS.json').read_text())
    frames = [
        {'index': frame[0], 'pts': frame[1], 'duration': frame[2], 'key_frame': frame[3]}
        for frame in timeline['frames']
    ]
    rows = code_rows(cuts, manifest['caption_treatment']['labels'])
    measured = measure(args.master, rows, frames, timeline['time_base'], args.scratch)
    recipe.write_new(args.evidence, {
        'job': 'J2242',
        'status': 'BOTTOM_TEXT_REVIEWED',
        'note_resolved': False,
        'frame_2869': 'out',
        'master_created': False,
        'final_film_approval': False,
        'still_check': 'midpoint stills plus one later still on 06_same_thing; not a motion review or an audio review',
        'ocr': False,
        **measured,
    })
    print(json.dumps({
        'status': 'BOTTOM_TEXT_REVIEWED',
        'flat_fields': measured['flat_fields'],
        'pictures_without_panel': measured['pictures_without_panel'],
    }))


if __name__ == '__main__':
    main()
