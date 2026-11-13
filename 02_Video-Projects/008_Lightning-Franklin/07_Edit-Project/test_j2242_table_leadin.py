import unittest
from _j2242_table_leadin import accept_tower_leadin, leadin_schedule, table_stays_out


def _hit(best, mse=2.0, margin=4.0, second=None):
    return {'best': best, 'second': 0 if second is None else second, 'best_mse': mse, 'margin': margin}


def tower():
    return {
        'row': '02_tower_tilt',
        'timeline_frames': [272, 422],
        'source_frame_indices': list(range(151)),
        'decoded_source_frames': 192,
        'source_path': 'tower.mp4',
        'source_sha256': 'tower',
    }


def table():
    return {
        'row': '03_table_three',
        'timeline_frames': [423, 544],
        'poor_match_local_frames': [0, 1, 2, 3],
        'source_frame_indices': [52, 52, 52, 52, *range(118)],
    }


def tower_ranked():
    return [_hit(170), _hit(171), _hit(172), _hit(173)]


def table_ranked():
    return [_hit(52, mse=3300, margin=1), _hit(52, mse=3300, margin=1),
            _hit(52, mse=3300, margin=1), _hit(52, mse=3300, margin=1)]


class TableLeadIn(unittest.TestCase):
    def test_accepts_the_tower_continuation_only(self):
        schedule = leadin_schedule(tower(), tower_ranked(), table(), table_ranked())
        self.assertEqual(schedule['timeline_frames'], [423, 426])
        self.assertEqual(schedule['source_frame_indices'], [170, 171, 172, 173])
        self.assertEqual(schedule['frame_2869'], 'out')
        self.assertEqual(table_stays_out(table_ranked()), [423, 426])

    def test_rejects_a_different_or_weak_tower_frame(self):
        for ranked in (
            [_hit(170), _hit(171), _hit(172), _hit(174)],
            [_hit(151), _hit(152), _hit(153), _hit(154)],
            [_hit(170, margin=0.05), _hit(171), _hit(172), _hit(173)],
            [_hit(170, mse=12), _hit(171), _hit(172), _hit(173)],
            tower_ranked()[:3],
        ):
            with self.subTest(ranked=ranked):
                with self.assertRaises(ValueError):
                    accept_tower_leadin(ranked)

    def test_refuses_when_the_table_plate_is_close(self):
        close = table_ranked()
        close[2] = _hit(0, mse=8, margin=2)
        with self.assertRaises(ValueError):
            leadin_schedule(tower(), tower_ranked(), table(), close)

    def test_refuses_a_changed_tower_tail(self):
        changed = tower()
        changed['source_frame_indices'] = list(range(150))
        with self.assertRaises(ValueError):
            leadin_schedule(changed, tower_ranked(), table(), table_ranked())


if __name__ == '__main__':
    unittest.main()
