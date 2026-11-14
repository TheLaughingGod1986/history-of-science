import unittest

import _j2242_encode_groups as enc
import _j2242_mixed_split as split
import _j2242_packet_mux as mux


class MixedSplit(unittest.TestCase):
    def setUp(self):
        self.groups = split.load_groups(mux.REVIEW)

    def test_changed_runs_skip_the_master_frames(self):
        rows = split.plan(self.groups, has_b_frames=2)
        changed = [(row['first'], row['last'], row['frames']) for row in rows if row['role'] == 'changed']
        master = [(row['first'], row['last'], row['disposition']) for row in rows if row['role'] == 'master']
        self.assertEqual(changed, [
            (2718, 2868, 151),
            (2870, 2887, 18),
            (3260, 3343, 84),
            (4016, 4129, 114),
            (11038, 11117, 80),
        ])
        self.assertEqual(master, [
            (2869, 2869, 'blocked_by_b_frames'),
            (3168, 3259, 'blocked_by_b_frames'),
            (4130, 4138, 'blocked_by_b_frames'),
            (11118, 11245, 'blocked_by_b_frames'),
        ])
        self.assertTrue(all(row['disposition'] == 'high_qp1' for row in rows if row['role'] == 'changed'))
        covered = []
        for first, last, _frames in changed:
            covered.extend(range(first, last + 1))
        self.assertNotIn(2869, covered)
        self.assertNotIn(4130, covered)
        self.assertNotIn(11118, covered)

    def test_the_high_encode_still_refuses_a_master_run(self):
        _changed, master = split.partition(self.groups[0])
        self.assertEqual((master[0]['first'], master[0]['last']), (2869, 2869))
        with self.assertRaises(ValueError):
            enc.require_fully_changed(split.master_envelope(master[0]))
        franklin = next(row for row in split.plan(self.groups, 0) if row['first'] == 2718)
        enc.require_fully_changed(split.changed_envelope(franklin))

    def test_packet_copy_needs_no_b_frames_and_an_idr_start(self):
        jar = next(group for group in self.groups if group['first'] == 3168)
        _changed, master = split.partition(jar)
        self.assertEqual(split.master_disposition(master[0], 3168, 0), 'packet_copy')
        self.assertEqual(split.master_disposition(master[0], 3168, 2), 'blocked_by_b_frames')
        fire = next(group for group in self.groups if group['first'] == 4016)
        _changed, tail = split.partition(fire)
        self.assertEqual(split.master_disposition(tail[0], 4016, 0), 'needs_new_idr')
        with self.assertRaises(ValueError):
            split.master_disposition(master[0], 3168, -1)


if __name__ == '__main__':
    unittest.main()
