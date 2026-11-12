import unittest

import numpy as np

from _j2242_ambiguous_fullres import judge_row, rank_upper_band


def plate(value, pixels=8):
    return np.full(pixels, value, dtype=np.uint8)


class FullResCaptionMap(unittest.TestCase):
    def test_exact_plate_beats_its_neighbour(self):
        source = np.stack([plate(10), plate(40), plate(80)])
        master = np.stack([plate(10), plate(80)])
        ranked = rank_upper_band(master, source)
        self.assertEqual([item['best'] for item in ranked], [0, 2])
        self.assertGreater(ranked[0]['margin'], 1)

    def test_closer_neighbour_wins_when_the_lowres_guess_is_wrong(self):
        source = np.stack([plate(0), plate(30), plate(90)])
        master = np.stack([plate(28)])
        ranked = rank_upper_band(master, source)
        self.assertEqual(ranked[0]['best'], 1)
        verdict = judge_row([0], ranked)
        self.assertFalse(verdict['unique_match'])
        self.assertEqual(verdict['winner_flip_local_frames'], [0])

    def test_high_error_stays_rejected_even_when_the_winner_matches(self):
        source = np.stack([plate(0), plate(255)])
        master = np.stack([plate(40)])
        ranked = rank_upper_band(master, source)
        verdict = judge_row([0], ranked)
        self.assertEqual(ranked[0]['best'], 0)
        self.assertFalse(verdict['unique_match'])
        self.assertEqual(verdict['winner_flip_count'], 0)
        self.assertGreater(verdict['maximum_mse'], 9)

    def test_confirmed_schedule_is_unique_and_still_unreconstructed(self):
        source = np.stack([plate(0), plate(20), plate(200)])
        master = np.stack([plate(0), plate(20)])
        verdict = judge_row([0, 1], rank_upper_band(master, source))
        self.assertTrue(verdict['unique_match'])
        self.assertFalse(verdict['reconstructed'])
        self.assertEqual(verdict['winner_flip_count'], 0)

    def test_count_mismatch_is_rejected(self):
        with self.assertRaises(ValueError):
            judge_row([0], [])


if __name__ == '__main__':
    unittest.main()
