import unittest

import _j2242_ref_check as ref


def picture(index, kind, poc, frame_num, nal_ref, idr=False, l0=1, l1=0):
    return {
        'index': index, 'kind': kind, 'poc': poc, 'frame_num': frame_num,
        'nal_ref': nal_ref, 'idr': idr, 'l0': 0 if kind == 'I' else l0,
        'l1': l1 if kind == 'B' else 0, 'mods_l0': [], 'mods_l1': [],
    }


class RefCheck(unittest.TestCase):
    def test_opening_b_frame_uses_the_idr_and_the_next_p(self):
        pictures = [
            picture(0, 'I', 0, 0, 3, idr=True),
            picture(2, 'P', 4, 1, 2),
            picture(1, 'B', 2, 2, 0, l1=1),
            picture(4, 'P', 8, 2, 2),
            picture(3, 'B', 6, 3, 0, l1=1),
        ]
        ref.assign_refs(pictures)
        by_index = {item['index']: item for item in pictures}
        self.assertEqual(by_index[2]['refs'], [0])
        self.assertEqual(by_index[1]['refs'], [0, 2])
        self.assertEqual(by_index[4]['refs'], [2])
        self.assertEqual(by_index[3]['refs'], [2, 4])

    def test_a_master_frame_that_looks_ahead_is_blocked(self):
        pictures = [
            picture(0, 'I', 0, 0, 3, idr=True),
            picture(2, 'P', 4, 1, 2),
            picture(1, 'B', 2, 2, 0, l1=1),
            picture(4, 'P', 8, 2, 2),
            picture(3, 'B', 6, 3, 0, l1=1),
        ]
        ref.assign_refs(pictures)
        ref.taint(pictures, changed=[4])
        by_index = {item['index']: item for item in pictures}
        self.assertFalse(by_index[0]['tainted'])
        self.assertFalse(by_index[1]['tainted'])
        self.assertFalse(by_index[2]['tainted'])
        self.assertTrue(by_index[4]['tainted'])
        self.assertTrue(by_index[3]['tainted'])
        self.assertEqual(ref.exact_runs(pictures, [(0, 3)]), [(0, 2)])
        self.assertEqual(ref.blocked_runs(pictures, [(0, 3)]), [(3, 3)])

    def test_a_kept_tail_and_a_middle_p_are_blocked(self):
        tail = [
            picture(0, 'I', 0, 0, 3, idr=True),
            picture(1, 'P', 2, 1, 2),
            picture(2, 'B', 4, 2, 0, l1=1),
        ]
        ref.assign_refs(tail)
        ref.taint(tail, changed=[0, 1])
        self.assertTrue(tail[-1]['tainted'])
        self.assertEqual(ref.exact_runs(tail, [(2, 2)]), [])
        middle = [
            picture(10, 'I', 0, 0, 3, idr=True),
            picture(11, 'P', 2, 1, 2),
        ]
        ref.assign_refs(middle)
        ref.taint(middle, changed=[10])
        self.assertTrue(middle[1]['tainted'])
        self.assertEqual(middle[1]['refs'], [10])

    def test_marking_drops_a_reference_after_the_list_is_built(self):
        pictures = [
            picture(0, 'I', 0, 0, 3, idr=True),
            picture(2, 'P', 4, 1, 2),
            picture(4, 'P', 8, 2, 2),
            picture(6, 'P', 12, 3, 2),
        ]
        pictures[3]['mmco'] = [(1, 2), (0,)]
        ref.assign_refs(pictures)
        self.assertEqual(pictures[3]['refs'], [4])

    def test_a_tainted_single_frame_is_not_copied(self):
        kept = picture(2869, 'P', 46, 8, 2)
        kept['tainted'] = True
        self.assertEqual(ref.exact_runs([kept], [(2869, 2869)]), [])
        self.assertEqual(ref.blocked_runs([kept], [(2869, 2869)]), [(2869, 2869)])


if __name__ == '__main__':
    unittest.main()
