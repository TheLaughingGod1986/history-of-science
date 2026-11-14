import unittest

import _j2242_group_nuts as nuts
import _j2242_packet_mux as mux


class GroupNuts(unittest.TestCase):
    def test_seven_fully_changed_groups_and_no_master_frame(self):
        files = nuts.source_files(mux.REVIEW)
        groups = nuts.target_groups(mux.build_report(), files)
        self.assertEqual(
            [(item['first'], item['last'], len(item['pieces'])) for item in groups],
            [
                (272, 422, 2),
                (423, 544, 2),
                (2506, 2665, 1),
                (8189, 8268, 1),
                (8269, 8348, 1),
                (10777, 10852, 1),
                (10996, 11037, 1),
            ])
        salon = groups[2]['pieces'][0]
        self.assertEqual(salon['slice_first'], 0)
        self.assertEqual(salon['slice_count'], 160)
        self.assertEqual(salon['source'], 'SALON_PATCH.json')
        early, late = groups[3]['pieces'][0], groups[4]['pieces'][0]
        self.assertEqual((early['slice_first'], early['slice_count']), (0, 80))
        self.assertEqual((late['slice_first'], late['slice_count']), (80, 80))
        self.assertEqual(early['path'], late['path'])
        self.assertNotIn(2869, [frame for item in groups for frame in range(item['first'], item['last'] + 1)])

    def test_a_group_that_keeps_master_frames_is_refused(self):
        report = mux.build_report()
        jar = next(item for item in report['envelopes'] if item['first'] == 3168)
        with self.assertRaises(ValueError):
            nuts.group_inputs(jar, nuts.source_files(mux.REVIEW))


if __name__ == '__main__':
    unittest.main()
