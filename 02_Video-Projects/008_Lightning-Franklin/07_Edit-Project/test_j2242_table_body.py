import unittest
from _j2242_table_body import table_body_schedule


def row():
    return dict(row='03_table_three', timeline_frames=[423, 544],
                source_frame_indices=[52, 52, 52, 52, *range(118)],
                poor_match_local_frames=[0, 1, 2, 3], ambiguous_local_frames=[],
                nonmonotonic_steps=[4], per_frame_mse=[3000, 3000, 3000, 3000, *([2.0] * 118)],
                source_path='table.mp4', source_sha256='abc')


class TableBody(unittest.TestCase):
    def test_accepts_measured_split_only(self):
        body = table_body_schedule(row())
        self.assertEqual(body['timeline_frames'], [427, 544])
        self.assertEqual(body['source_frame_indices'], list(range(118)))
        self.assertEqual(body['rejected_master_frames'], [423, 426])

    def test_rejects_a_changed_boundary(self):
        for change in (
            dict(poor_match_local_frames=[0, 1, 2]),
            dict(ambiguous_local_frames=[4]),
            dict(nonmonotonic_steps=[]),
            dict(source_frame_indices=[52, 52, 52, 52, *range(1, 119)]),
            dict(per_frame_mse=[3, 3, 3, 3, *([2.0] * 118)]),
            dict(per_frame_mse=[3000, 3000, 3000, 3000, *([2.0] * 117), 40]),
            dict(row='02_tower_tilt'),
            dict(timeline_frames=[423, 543]),
        ):
            with self.subTest(change=change):
                bad = row()
                bad.update(change)
                with self.assertRaises(ValueError):
                    table_body_schedule(bad)


if __name__ == '__main__':
    unittest.main()
