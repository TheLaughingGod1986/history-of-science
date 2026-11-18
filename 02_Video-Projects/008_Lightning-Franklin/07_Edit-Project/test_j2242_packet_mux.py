import unittest

import _j2242_packet_mux as mux


class PacketPlan(unittest.TestCase):
    def test_a_change_that_crosses_an_idr_becomes_two_envelopes(self):
        envelopes = mux.plan_envelopes([0, 10, 20], [
            {'name': 'cut', 'first': 8, 'last': 15}], frame_count=30)
        self.assertEqual([(e['first'], e['last']) for e in envelopes], [(0, 9), (10, 19)])
        self.assertEqual(envelopes[0]['stitch_source_frames'], [[0, 7]])
        self.assertEqual(envelopes[1]['stitch_source_frames'], [[16, 19]])
        self.assertFalse(any(e['pixels_complete'] for e in envelopes))
        counts = mux.assignment(envelopes, 30)
        self.assertEqual(counts['replaced_frames'], 20)
        self.assertEqual(counts['copied_frames'], 10)

    def test_the_night_street_and_frame_2869_cannot_be_changed(self):
        idrs = [0, 1000, 2000, 3000]
        with self.assertRaises(ValueError):
            mux.plan_envelopes(idrs, [{'name': 'night', 'first': 1129, 'last': 1231}])
        with self.assertRaises(ValueError):
            mux.plan_envelopes(idrs, [{'name': 'gap', 'first': 2860, 'last': 2869}])

    def test_replacement_keeps_the_source_clock(self):
        scheduled = mux.schedule_replacement([
            {'pts': 1536, 'duration': 512},
            {'pts': 2048, 'duration': 1024},
        ])
        self.assertEqual(scheduled, [
            {'pts': 1536, 'dts': 512, 'duration': 512},
            {'pts': 2048, 'dts': 1024, 'duration': 1024},
        ])
        with self.assertRaises(ValueError):
            mux.schedule_replacement([{'pts': 1, 'duration': 0}])
        with self.assertRaises(ValueError):
            mux.schedule_replacement([{'pts': 1, 'duration': 512}], delay=0)

    def test_overlapping_envelopes_are_refused(self):
        with self.assertRaises(ValueError):
            mux.assignment([{'first': 0, 'last': 5, 'frames': 6},
                            {'first': 5, 'last': 8, 'frames': 4}], 10)

    def test_the_real_intermediates_plan_without_a_master(self):
        report = mux.build_report()
        self.assertEqual(report['status'], 'PACKET_PLAN_ONLY')
        self.assertEqual(report['copied_frames'] + report['replaced_frames'], mux.FRAME_COUNT)
        self.assertFalse(report['output_film_created'])
        self.assertFalse(report['finished_master'])
        self.assertFalse(report['approval'])
        self.assertEqual(report['spend_gbp'], 0)
        self.assertNotIn('JAR_PATCH_V01_REJECTED.json',
                         {part['source'] for env in report['envelopes'] for part in env['changed']})
        self.assertEqual(report['foil_frame_3353'], 'packet_copy')
        self.assertIn(report['frame_2869'], ('packet_copy', 'keep_inside_reencode'))
        self.assertNotEqual(report['frame_2869'], 'changed')
        jar = next(env for env in report['envelopes'] if env['first'] == 3168)
        self.assertEqual(jar['last'], 3343)
        self.assertIn([3168, 3259], jar['stitch_source_frames'])
        self.assertTrue(report['job_envelopes_are_closed_idr_groups'])
        self.assertEqual(report['night_street'], 'packet_copy')
        self.assertEqual(report['unplaced_title_rows'], [])
        self.assertEqual(report['placed_title_rows'], list(mux.PLACED_TITLES))
        for name, first, last in (
            ('15_likeness_fire', 4016, 4129),
            ('06_same_thing', 8189, 8348),
            ('08_looking_path', 10777, 10852),
        ):
            parts = [part for env in report['envelopes'] for part in env['changed']
                     if part['name'] == name]
            self.assertEqual(min(part['first'] for part in parts), first)
            self.assertEqual(max(part['last'] for part in parts), last)


if __name__ == '__main__':
    unittest.main()
