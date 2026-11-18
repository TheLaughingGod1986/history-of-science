import json
import unittest
from pathlib import Path

import numpy as np

import _build_rough_v13_recipe as recipe
from _j2242_bottom_text import EXPECTED_ROWS, STILL_NOTES, code_rows, field_kind, midpoint_frame


class BottomText(unittest.TestCase):
    def test_ten_rows_stay_outside_the_side_labels(self):
        manifest = recipe.load_manifest()
        cuts = json.loads((Path(recipe.__file__).parent / '_desk/008/rough_v12/cuts_rough_v12.json').read_text())
        rows = code_rows(cuts, manifest['caption_treatment']['labels'])
        self.assertEqual(tuple(row['row'] for row in rows), EXPECTED_ROWS)
        self.assertTrue(all(row['kind'] == 'code_graphic_or_overlay' for row in rows))
        self.assertEqual(tuple(STILL_NOTES), EXPECTED_ROWS)

    def test_midpoints_land_on_the_measured_frames(self):
        manifest = recipe.load_manifest()
        cuts = json.loads((Path(recipe.__file__).parent / '_desk/008/rough_v12/cuts_rough_v12.json').read_text())
        timeline = json.loads((Path(recipe.__file__).parent / 'J2163_MASTER_FRAME_PTS.json').read_text())
        frames = [
            {'index': frame[0], 'pts': frame[1], 'duration': frame[2], 'key_frame': frame[3]}
            for frame in timeline['frames']
        ]
        expected = {
            '14_likeness_pairs': 3955,
            '15_likeness_fire': 4073,
            '03_rod_cloud': 4898,
            '04_letter_crosses': 5021,
            '15_wet_dry': 6410,
            '06_same_thing': 8268,
            '08_teach_charge': 8506,
            '08_looking_path': 10793,
            '09_wood_vs_metal': 10913,
            '10_metal_easy': 11017,
        }
        for row in code_rows(cuts, manifest['caption_treatment']['labels']):
            self.assertEqual(midpoint_frame(row, frames, timeline['time_base']), expected[row['row']])

    def test_a_side_label_on_a_code_row_is_refused(self):
        manifest = recipe.load_manifest()
        cuts = json.loads((Path(recipe.__file__).parent / '_desk/008/rough_v12/cuts_rough_v12.json').read_text())
        for cut in cuts:
            if cut['row'] == '14_likeness_pairs':
                cut['side_label'] = 'A LABEL'
        with self.assertRaises(ValueError):
            code_rows(cuts, manifest['caption_treatment']['labels'])

    def test_flat_field_is_not_a_caption_panel(self):
        flat = np.full((1080, 1920), 80, np.uint8)
        found = field_kind(flat)
        self.assertTrue(found['flat_field'])
        self.assertFalse(found['picture'])
        self.assertFalse(found['bottom_panel'])

    def test_a_picture_without_a_bar_has_no_panel(self):
        picture = np.tile(np.linspace(0, 255, 1920, dtype=np.uint8), (1080, 1))
        found = field_kind(picture)
        self.assertTrue(found['picture'])
        self.assertFalse(found['bottom_panel'])

    def test_a_dark_bar_on_a_picture_is_a_panel(self):
        picture = np.tile(np.linspace(0, 255, 1920, dtype=np.uint8), (1080, 1))
        picture[760:1000, :] = 55
        picture[820:900, 700:1100] = 220
        found = field_kind(picture)
        self.assertTrue(found['picture'])
        self.assertTrue(found['bottom_panel'])

    def test_the_wrong_frame_shape_is_refused(self):
        with self.assertRaises(ValueError):
            field_kind(np.zeros((720, 1920), np.uint8))


if __name__ == '__main__':
    unittest.main()
