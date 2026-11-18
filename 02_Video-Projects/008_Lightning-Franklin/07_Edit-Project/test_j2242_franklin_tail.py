import json
import unittest
from pathlib import Path

from _j2242_franklin_tail import forward_spans, franklin_tail
from _j2242_outside_hold import outside_hold

ROOT = Path(__file__).resolve().parents[3] / 'jobs/reviews/J2242'


def _frame(local, best, second, margin, mse=4.5):
    return {
        'local_index': local,
        'fullres_best': best,
        'fullres_second': second,
        'best_mse': mse,
        'margin': margin,
    }


class FranklinTail(unittest.TestCase):
    def test_a_forward_hold_repeats_the_earlier_outside_frame(self):
        frames = [
            _frame(0, 10, 11, 1.0),
            _frame(1, 12, 13, 0.01),
            _frame(2, 14, 15, 1.0),
        ]
        spans, refused = forward_spans(frames)
        self.assertEqual(refused, [])
        self.assertEqual(spans[0]['source_frame_indices'], [10, 10, 14])
        self.assertEqual(spans[0]['holds'], {1: 10})
        self.assertNotIn(12, spans[0]['source_frame_indices'])
        self.assertNotIn(13, spans[0]['source_frame_indices'])

    def test_a_blocked_near_tie_does_not_look_forward(self):
        frames = [
            _frame(0, 0, 1, 1.0),
            _frame(1, 0, 2, 0.01),
            _frame(2, 9, 8, 1.0),
        ]
        spans, refused = forward_spans(frames)
        self.assertEqual(refused, [1])
        self.assertEqual([span['source_frame_indices'] for span in spans], [[0], [9]])

    def test_a_backward_hold_is_left_out(self):
        frames = [
            _frame(0, 5, 4, 1.0),
            _frame(1, 1, 2, 0.01),
            _frame(2, 3, 4, 1.0),
        ]
        spans, refused = forward_spans(frames)
        self.assertEqual(spans[0]['source_frame_indices'], [5, 5])
        self.assertEqual(refused, [2])
        self.assertNotIn(1, spans[0]['source_frame_indices'])
        self.assertNotIn(2, spans[0]['source_frame_indices'])

    def test_recorded_tail_keeps_two_spans_and_two_refusals(self):
        evidence = json.loads((ROOT / 'THREE_ROW_FULLRES.json').read_text())
        row = next(item for item in evidence['rows'] if item['row'] == '04_franklin_watches')
        with self.assertRaises(ValueError):
            outside_hold(row['frames'])
        tail, refused = franklin_tail(row)
        self.assertEqual(refused, [2868, 2869])
        self.assertEqual(tail[0]['timeline_frames'], [2865, 2867])
        self.assertEqual(tail[0]['source_frame_indices'], [146, 148, 148])
        self.assertEqual(tail[0]['holds'], {147: 146})
        self.assertEqual(tail[1]['timeline_frames'], [2870, 2887])
        self.assertEqual(tail[1]['holds'], {152: 148, 153: 148, 154: 148, 155: 148, 156: 148, 157: 148})
        self.assertEqual(tail[1]['source_frame_indices'][:6], [148] * 6)
        self.assertEqual(tail[1]['source_frame_indices'][6:],
                         [158, 159, 160, 161, 162, 163, 164, 165, 166, 176, 177, 178])
        for span in tail:
            for local, source in span['holds'].items():
                frame = row['frames'][local]
                self.assertNotIn(source, (frame['fullres_best'], frame['fullres_second']))


if __name__ == '__main__':
    unittest.main()
