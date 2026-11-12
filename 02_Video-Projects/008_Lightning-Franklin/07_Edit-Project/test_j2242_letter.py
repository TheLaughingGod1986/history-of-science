import json
import unittest
from pathlib import Path
import _j2242_letter_patch as letter


class LetterTests(unittest.TestCase):
    def setUp(self):
        self.timeline = json.loads((Path(__file__).parent / 'J2163_MASTER_FRAME_PTS.json').read_text())
        self.timeline['frames'] = letter.recipe.as_frame_dicts(self.timeline['frames'])

    def test_original_gap_preserved(self):
        frames = letter.patch_clock(self.timeline)
        self.assertEqual(frames[92]['pts']-frames[91]['pts'], 1536)

    def test_collapsed_gap_rejected(self):
        self.timeline['frames'][5069]['pts'] -= 1024
        with self.assertRaises(ValueError):
            letter.patch_clock(self.timeline)

    def test_letter_stays_in_left_sky_and_moves(self):
        positions = [letter.letter_geometry(i) for i in range(101)]
        self.assertTrue(all(x+132 < 580 and y+84 < 330 for x,y,a in positions))
        self.assertTrue(all(b[0] > a[0] for a,b in zip(positions,positions[1:])))
        self.assertEqual(positions[0][2], 0)
        self.assertEqual(positions[-1][2], 0)

    def test_out_of_window_rejected(self):
        with self.assertRaises(ValueError):
            letter.letter_geometry(101)
