import copy
import unittest
from _j2242_points_patch import patch_clock, FIRST, LAST

class PointsClock(unittest.TestCase):
    def setUp(self):
        self.clock = {'time_base': '1/12288', 'frames': [
            {'index': i, 'pts': 1536 + i * 512, 'duration': 1024 if i == 4513 else 512}
            for i in range(LAST + 1)]}

    def test_exact_native_window(self):
        result = patch_clock(self.clock)
        self.assertEqual(len(result), 160)
        self.assertEqual((result[0]['index'], result[-1]['index']), (FIRST, LAST))

    def test_reject_clock_changes(self):
        for field, value in [('pts', 0), ('duration', 1024), ('index', 0)]:
            with self.subTest(field=field):
                clock = copy.deepcopy(self.clock)
                clock['frames'][FIRST + 20][field] = value
                with self.assertRaises(ValueError):
                    patch_clock(clock)

    def test_reject_normalized_overlap(self):
        clock = copy.deepcopy(self.clock)
        clock['frames'][4513]['duration'] = 512
        with self.assertRaises(ValueError):
            patch_clock(clock)

    def test_reject_short_or_rescaled_clock(self):
        for clock in [dict(self.clock, time_base='1/24'),
                      dict(self.clock, frames=self.clock['frames'][:-1])]:
            with self.assertRaises(ValueError):
                patch_clock(clock)

if __name__ == '__main__':
    unittest.main()
