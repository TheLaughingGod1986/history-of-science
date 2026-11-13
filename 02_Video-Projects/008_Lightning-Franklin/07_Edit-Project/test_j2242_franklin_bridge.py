import json
import unittest
from pathlib import Path

from _j2242_franklin_bridge import gap_bridge
from _j2242_franklin_tail import franklin_tail
from _j2242_subject_window import confirm_subject_window

ROOT = Path(__file__).resolve().parents[3] / 'jobs/reviews/J2242'


class FranklinBridge(unittest.TestCase):
    def setUp(self):
        evidence = json.loads((ROOT / 'THREE_ROW_FULLRES.json').read_text())
        window = json.loads((ROOT / 'SUBJECT_WINDOW.json').read_text())
        self.row = next(item for item in evidence['rows'] if item['row'] == '04_franklin_watches')
        self.tail, self.refused = franklin_tail(self.row)
        self.measurements = window['pairs']

    def test_only_the_confirmed_shared_neighbour_is_filled(self):
        filled, still_out = gap_bridge(self.row['frames'], self.tail, self.refused, self.measurements)
        self.assertEqual(self.refused, [2868, 2869])
        self.assertEqual(still_out, [2869])
        self.assertEqual(len(filled), 1)
        bridge = filled[0]
        self.assertEqual(bridge['timeline_frames'], [2868, 2868])
        self.assertEqual(bridge['source_frame_indices'], [148])
        self.assertEqual(bridge['holds'], {})
        self.assertEqual(bridge['runner_not_used'], 150)
        self.assertGreaterEqual(bridge['window_margin'], 0.1)
        frame = self.row['frames'][150]
        self.assertEqual(frame['master_frame'], 2868)
        self.assertEqual(frame['fullres_best'], 148)
        self.assertEqual(frame['fullres_second'], 150)
        self.assertNotEqual(bridge['source_frame_indices'][0], frame['fullres_second'])

    def test_frame_2869_is_not_switched_to_the_runner(self):
        pair = next(item for item in self.measurements
                    if item['row'] == '04_franklin_watches' and item['master_frame'] == 2869)
        self.assertFalse(pair['confirmed'])
        self.assertFalse(confirm_subject_window(pair['window_best_mse'], pair['window_runner_mse']))
        self.assertLess(pair['window_runner_mse'], pair['window_best_mse'])
        filled, still_out = gap_bridge(self.row['frames'], self.tail, self.refused, self.measurements)
        self.assertNotIn(150, filled[0]['source_frame_indices'])
        self.assertEqual(still_out, [2869])

    def test_a_confirmed_winner_with_different_flanks_stays_out(self):
        tail = [
            {'timeline_frames': [2867, 2867], 'source_frame_indices': [146]},
            {'timeline_frames': [2869, 2869], 'source_frame_indices': [150]},
        ]
        filled, still_out = gap_bridge(self.row['frames'], tail, [2868], self.measurements)
        self.assertEqual(filled, [])
        self.assertEqual(still_out, [2868])

    def test_an_already_accepted_frame_is_rejected(self):
        with self.assertRaises(ValueError):
            gap_bridge(self.row['frames'], self.tail, [2867], self.measurements)


if __name__ == '__main__':
    unittest.main()
