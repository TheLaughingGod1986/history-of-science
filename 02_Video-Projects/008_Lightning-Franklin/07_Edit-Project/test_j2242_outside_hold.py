import json
import unittest
from pathlib import Path

from _j2242_outside_hold import knuckle_row, outside_hold, sentry_row, tower_opening

ROOT = Path(__file__).resolve().parents[3] / 'jobs/reviews/J2242'


def _frame(local, best, second, margin, mse=5.0):
    return {
        'local_index': local,
        'fullres_best': best,
        'fullres_second': second,
        'best_mse': mse,
        'margin': margin,
    }


class OutsideHold(unittest.TestCase):
    def test_a_previous_outside_frame_is_repeated(self):
        frames = [
            _frame(0, 0, 1, 1.0),
            _frame(1, 0, 1, 0.4),
            _frame(2, 2, 1, 0.08),
            _frame(3, 3, 2, 0.4),
        ]
        indices, holds = outside_hold(frames)
        self.assertEqual(indices, [0, 0, 0, 3])
        self.assertEqual(holds, {2: 0})

    def test_the_next_outside_frame_is_used_when_the_previous_is_a_candidate(self):
        frames = [
            _frame(0, 28, 27, 0.2),
            _frame(1, 29, 28, 0.07),
            _frame(2, 30, 31, 1.0),
        ]
        indices, holds = outside_hold(frames)
        self.assertEqual(indices, [28, 30, 30])
        self.assertEqual(holds, {1: 30})
        self.assertNotIn(29, indices)
        self.assertNotIn(holds[1], (29, 28))

    def test_a_run_of_near_ties_holds_the_same_outside_frame(self):
        frames = [
            _frame(0, 0, 1, 0.2),
            _frame(1, 1, 2, 0.01),
            _frame(2, 3, 2, 0.07),
            _frame(3, 4, 3, 0.2),
        ]
        indices, holds = outside_hold(frames)
        self.assertEqual(indices, [0, 0, 0, 4])
        self.assertEqual(holds, {1: 0, 2: 0})

    def test_no_outside_neighbour_is_refused(self):
        frames = [
            _frame(0, 1, 0, 0.05),
            _frame(1, 1, 0, 1.0),
        ]
        with self.assertRaises(ValueError):
            outside_hold(frames)

    def test_a_backward_hold_is_refused(self):
        frames = [
            _frame(0, 5, 4, 1.0),
            _frame(1, 5, 6, 0.05),
            _frame(2, 4, 3, 1.0),
        ]
        with self.assertRaises(ValueError):
            outside_hold(frames)

    def test_recorded_rows_keep_the_pinned_holds(self):
        three = json.loads((ROOT / 'THREE_ROW_FULLRES.json').read_text())
        ambiguous = json.loads((ROOT / 'AMBIGUOUS_FULLRES.json').read_text())
        mapping = json.loads((ROOT / 'CAPTION_SOURCE_MAP.json').read_text())

        def row(document, name):
            found = [item for item in document['rows'] if item['row'] == name]
            self.assertEqual(len(found), 1)
            return found[0]

        sentry = sentry_row(row(three, '02_sentry_box'), row(mapping, '02_sentry_box'))
        knuckle = knuckle_row(row(ambiguous, '02_knuckle_spark'), row(mapping, '02_knuckle_spark'))
        tower = tower_opening(row(three, '02_tower_tilt'), row(mapping, '02_tower_tilt'))
        self.assertEqual(sentry['outside_hold_local_frames'], {2: 0})
        self.assertEqual(sentry['source_frame_indices'][2], 0)
        self.assertEqual(knuckle['outside_hold_local_frames'], {29: 30})
        self.assertEqual(knuckle['source_frame_indices'][29], 30)
        self.assertEqual(tower['timeline_frames'], [272, 346])
        self.assertEqual(len(tower['source_frame_indices']), 75)
        self.assertEqual(tower['outside_hold_local_frames'], {2: 0, 3: 0, 6: 4})
        self.assertEqual(tower['source_frame_indices'][74], 74)


if __name__ == '__main__':
    unittest.main()
