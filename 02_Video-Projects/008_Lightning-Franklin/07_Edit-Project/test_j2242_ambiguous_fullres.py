import unittest

import numpy as np

import json
from pathlib import Path

from _j2242_ambiguous_fullres import (
    accepted_fullres_indices, judge_row, rank_upper_band, resolve_near_tie, same_picture,
)
from _j2242_fullres_caption import prepare_fullres_row


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

    def _measured(self, best, low, mse=4.0, margin=1.0, local=0, master=100):
        return {
            'local_index': local,
            'master_frame': master,
            'lowres_index': low,
            'fullres_best': best,
            'fullres_second': best + 1,
            'best_mse': mse,
            'margin': margin,
            'winner_matches_lowres': low == best,
        }

    def test_unique_fullres_schedule_may_disagree_with_lowres(self):
        frames = [self._measured(0, 1, local=0, master=100), self._measured(1, 1, local=1, master=101)]
        row = {'row': 'example', 'timeline_frames': [100, 101], 'frames': frames}
        self.assertEqual(accepted_fullres_indices(row), [0, 1])

    def test_weak_margin_rejects_the_whole_row(self):
        frames = [self._measured(0, 0, margin=0.07, local=0, master=10)]
        row = {'row': 'example', 'timeline_frames': [10, 10], 'frames': frames}
        with self.assertRaises(ValueError):
            accepted_fullres_indices(row)

    def test_high_error_and_backward_schedule_are_rejected(self):
        high = {'row': 'example', 'timeline_frames': [10, 10],
                'frames': [self._measured(0, 0, mse=9.1, local=0, master=10)]}
        with self.assertRaises(ValueError):
            accepted_fullres_indices(high)
        backward = {
            'row': 'example',
            'timeline_frames': [10, 11],
            'frames': [
                self._measured(2, 2, local=0, master=10),
                self._measured(1, 1, local=1, master=11),
            ],
        }
        with self.assertRaises(ValueError):
            accepted_fullres_indices(backward)

    def test_recorded_giant_spark_is_unique_and_the_other_two_are_not(self):
        path = Path(__file__).resolve().parents[3] / 'jobs/reviews/J2242/AMBIGUOUS_FULLRES.json'
        data = json.loads(path.read_text())
        by_name = {row['row']: row for row in data['rows']}
        giant = by_name['07_giant_spark']
        self.assertEqual(accepted_fullres_indices(giant), list(range(151)))
        mapped = {
            'row': giant['row'],
            'timeline_frames': giant['timeline_frames'],
            'source_sha256': giant['source_sha256'],
            'source_frame_indices': [frame['lowres_index'] for frame in giant['frames']],
        }
        prepared = prepare_fullres_row(mapped, giant)
        self.assertEqual(prepared['source_frame_indices'], list(range(151)))
        self.assertNotEqual(prepared['source_frame_indices'], mapped['source_frame_indices'])
        for name in ('02_knuckle_spark', '14_royal_society'):
            with self.assertRaises(ValueError):
                accepted_fullres_indices(by_name[name])
        with self.assertRaises(ValueError):
            prepare_fullres_row(mapped, by_name['12_steeple_fire'])

    def test_near_tie_resolves_only_when_the_source_frames_match(self):
        self.assertTrue(same_picture(0.05))
        self.assertFalse(same_picture(0.1))
        self.assertFalse(resolve_near_tie(0.04, 1.39))
        with self.assertRaises(ValueError):
            resolve_near_tie(0.2, 0.01)
        with self.assertRaises(ValueError):
            same_picture(-0.1)

    def test_measured_near_ties_are_different_pictures(self):
        path = Path(__file__).resolve().parents[3] / 'jobs/reviews/J2242/NEAR_TIE_SOURCE_PAIRS.json'
        data = json.loads(path.read_text())
        self.assertEqual(data['status'], 'NEAR_TIE_SOURCE_PAIRS_DIFFER')
        self.assertGreaterEqual(len(data['pairs']), 16)
        for pair in data['pairs']:
            self.assertLess(pair['margin'], 0.1)
            self.assertFalse(resolve_near_tie(pair['margin'], pair['source_pair_mse']))
            self.assertGreaterEqual(pair['source_pair_mse'], 0.1)


if __name__ == '__main__':
    unittest.main()
