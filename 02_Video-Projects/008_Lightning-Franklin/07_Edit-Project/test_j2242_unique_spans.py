import unittest
from _j2242_unique_spans import franklin_prefix, tower_roof


def _frames(count, weak):
    frames = []
    for i in range(count):
        margin = 0.05 if i in weak else 1.0
        frames.append({
            'local_index': i,
            'master_frame': 0,
            'fullres_best': i,
            'best_mse': 4.0,
            'margin': margin,
        })
    return frames


def franklin():
    return (
        {'row': '04_franklin_watches', 'timeline_frames': [2718, 2887],
         'source_sha256': 'abc', 'frames': _frames(170, {147})},
        {'row': '04_franklin_watches', 'timeline_frames': [2718, 2887],
         'source_sha256': 'abc', 'source_path': 'franklin.mp4', 'source_frame_indices': []},
    )


def tower():
    return (
        {'row': '02_tower_tilt', 'timeline_frames': [272, 422],
         'source_sha256': 'def', 'frames': _frames(151, {2, 3, 6})},
        {'row': '02_tower_tilt', 'timeline_frames': [272, 422],
         'source_sha256': 'def', 'source_path': 'tower.mp4', 'source_frame_indices': []},
    )


class UniqueSpans(unittest.TestCase):
    def test_franklin_prefix_is_source_0_through_146(self):
        row = franklin_prefix(*franklin())
        self.assertEqual(row['timeline_frames'], [2718, 2864])
        self.assertEqual(row['source_frame_indices'], list(range(147)))
        self.assertEqual(row['rejected_master_frames'], [2865, 2887])

    def test_tower_roof_is_source_75_through_150(self):
        row = tower_roof(*tower())
        self.assertEqual(row['timeline_frames'], [347, 422])
        self.assertEqual(row['source_frame_indices'], list(range(75, 151)))
        self.assertEqual(row['rejected_master_frames'], [272, 346])

    def test_a_near_tie_inside_the_span_is_rejected(self):
        measured, mapped = franklin()
        measured['frames'][10]['margin'] = 0.04
        with self.assertRaises(ValueError):
            franklin_prefix(measured, mapped)

    def test_a_fully_unique_tail_is_not_dropped(self):
        measured, mapped = franklin()
        for frame in measured['frames'][147:]:
            frame['margin'] = 2.0
        with self.assertRaises(ValueError):
            franklin_prefix(measured, mapped)

    def test_a_changed_source_schedule_is_rejected(self):
        measured, mapped = tower()
        measured['frames'][80]['fullres_best'] = 90
        with self.assertRaises(ValueError):
            tower_roof(measured, mapped)


if __name__ == '__main__':
    unittest.main()
