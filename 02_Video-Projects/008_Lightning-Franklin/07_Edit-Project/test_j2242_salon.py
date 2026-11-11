"""Guard the restricted take window, spark placement and master clock."""
import copy
import unittest

from _j2242_salon_patch import patch_clock, source_schedule


class SalonTests(unittest.TestCase):
    def clock(self):
        return {'time_base': '1/12288', 'frames': [
            {'index': i, 'pts': 1536 + 512*i, 'duration': 512}
            for i in range(2666)]}

    def test_approved_source_schedule(self):
        sequence = source_schedule()
        self.assertEqual(len(sequence), 80)
        self.assertEqual(sequence[:19], [0]*19)
        self.assertEqual(sequence[19:], list(range(61)))
        self.assertEqual(sequence[2635-2586], 30)
        self.assertEqual(max(sequence), 60)

    def test_clock_retains_offset(self):
        clock = self.clock()
        self.assertEqual(patch_clock(clock), clock['frames'][2506:2666])

    def test_gap_is_never_collapsed(self):
        for field in ('pts', 'duration', 'index'):
            clock = copy.deepcopy(self.clock())
            clock['frames'][2600][field] += 512
            with self.subTest(field=field), self.assertRaises(ValueError):
                patch_clock(clock)

    def test_rejects_short_or_wrong_timebase(self):
        clock = self.clock()
        clock['frames'].pop()
        with self.assertRaises(ValueError):
            patch_clock(clock)
        clock = self.clock()
        clock['time_base'] = '1/24'
        with self.assertRaises(ValueError):
            patch_clock(clock)


if __name__ == '__main__':
    unittest.main()
