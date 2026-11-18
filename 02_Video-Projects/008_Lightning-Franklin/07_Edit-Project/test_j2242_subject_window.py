import unittest

from _j2242_subject_window import confirm_subject_window, royal_schedule


def _frames():
    frames = []
    for i in range(127):
        margin = 0.05 if i in (1, 29) else 1.0
        best = 0 if i < 2 else (28 if i in (28, 29) else i - 1)
        frames.append({
            'local_index': i,
            'master_frame': 9303 + i,
            'fullres_best': best,
            'fullres_second': best + 1,
            'best_mse': 5.0,
            'margin': margin,
        })
    return frames


def _measured(confirm=True):
    runner = 5.2 if confirm else 5.05
    return [
        {'row': '14_royal_society', 'local_index': 1, 'master_frame': 9304,
         'fullres_best': 0, 'fullres_second': 1,
         'window_best_mse': 5.0, 'window_runner_mse': runner},
        {'row': '14_royal_society', 'local_index': 29, 'master_frame': 9332,
         'fullres_best': 28, 'fullres_second': 29,
         'window_best_mse': 5.0, 'window_runner_mse': runner},
    ]


def _rows():
    frames = _frames()
    fullres = {'row': '14_royal_society', 'timeline_frames': [9303, 9429],
               'source_sha256': 'abc', 'frames': frames}
    mapped = {'row': '14_royal_society', 'timeline_frames': [9303, 9429],
              'source_sha256': 'abc', 'source_path': 'royal.mp4', 'source_frame_indices': []}
    return fullres, mapped


class SubjectWindow(unittest.TestCase):
    def test_a_clear_centre_window_confirms_the_existing_winner(self):
        self.assertTrue(confirm_subject_window(5.0, 5.2))

    def test_a_window_that_prefers_the_runner_up_does_not_switch(self):
        self.assertFalse(confirm_subject_window(6.0, 5.0))

    def test_a_margin_under_0_1_stays_out(self):
        self.assertFalse(confirm_subject_window(5.0, 5.05))

    def test_error_above_9_stays_out(self):
        self.assertFalse(confirm_subject_window(9.1, 12.0))

    def test_royal_schedule_keeps_the_recorded_winners(self):
        row = royal_schedule(*_rows(), _measured())
        self.assertEqual(row['source_frame_indices'][1], 0)
        self.assertEqual(row['source_frame_indices'][29], 28)
        self.assertEqual(row['subject_window_confirmed_local_frames'], [1, 29])

    def test_one_unconfirmed_royal_frame_rejects_the_row(self):
        measured = _measured()
        measured[1]['window_runner_mse'] = 5.05
        with self.assertRaises(ValueError):
            royal_schedule(*_rows(), measured)

    def test_a_changed_weak_frame_is_rejected(self):
        fullres, mapped = _rows()
        fullres['frames'][4]['margin'] = 0.02
        with self.assertRaises(ValueError):
            royal_schedule(fullres, mapped, _measured())


if __name__ == '__main__':
    unittest.main()
