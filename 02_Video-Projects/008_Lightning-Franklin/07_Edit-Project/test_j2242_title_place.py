import unittest

import numpy as np

import _j2242_title_place as place


def _stack(value, frames, shape=(4, 4)):
    return np.full((frames, *shape), value, dtype=np.uint8)


class TitlePlace(unittest.TestCase):
    def test_a_unique_shift_is_kept(self):
        master = _stack(0, 8)
        overlay = _stack(9, 3)
        master[4:7] = overlay
        found = place.choose_shift(master, overlay, mean_max=0.1, frame_max=0.1, margin_min=1)
        self.assertEqual((found['first'], found['last'], found['frames']), (4, 6, 3))
        self.assertEqual(found['mean_mae'], 0.0)

    def test_a_tie_is_refused(self):
        master = _stack(0, 8)
        overlay = _stack(0, 3)
        with self.assertRaises(ValueError):
            place.choose_shift(master, overlay, mean_max=0.1, frame_max=0.1, margin_min=0.5)

    def test_a_weak_match_is_refused(self):
        master = _stack(0, 4)
        overlay = _stack(40, 2)
        with self.assertRaises(ValueError):
            place.choose_shift(master, overlay, mean_max=1, frame_max=1, margin_min=0.1)

    def test_a_record_must_still_meet_its_ceiling(self):
        good = {
            'status': 'TITLE_ROWS_PLACED',
            'master_created': False,
            'match_mean_max': 0.5,
            'frame_mae_max': 3.5,
            'margin_min': 0.9,
            'rows': [
                {
                    'row': name,
                    'status': 'PLACED',
                    'master_frames': list(span),
                    'frames': span[1] - span[0] + 1,
                    'mean_mae': 0.3,
                    'worst_frame_mae': 0.8,
                    'margin': 1.0,
                }
                for name, span in place.PROVED_FRAMES.items()
            ],
        }
        import json
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'TITLE_PLACE.json'
            target.write_text(json.dumps(good))
            changes = place.read_placement(target)
        self.assertEqual(
            [(row['name'], row['first'], row['last']) for row in changes],
            [(name, span[0], span[1]) for name, span in place.PROVED_FRAMES.items()])
        good['rows'][0]['mean_mae'] = 9
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'TITLE_PLACE.json'
            target.write_text(json.dumps(good))
            with self.assertRaises(ValueError):
                place.read_placement(target)


if __name__ == '__main__':
    unittest.main()
