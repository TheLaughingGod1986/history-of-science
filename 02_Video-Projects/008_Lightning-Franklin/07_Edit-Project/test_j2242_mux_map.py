import unittest

import _j2242_mux_map as plan


class MuxMap(unittest.TestCase):
    def test_the_clock_copies_every_source_duration(self):
        frames = [
            {'index': 0, 'pts': 1536, 'duration': 512},
            {'index': 1, 'pts': 2048, 'duration': 1024},
            {'index': 2, 'pts': 3072, 'duration': 1536},
        ]
        clock = plan.clock_summary(frames)
        self.assertEqual(clock['start_pts'], 1536)
        self.assertEqual(clock['end_pts'], 4608)
        self.assertEqual(clock['ticks_1024'], 1)
        self.assertEqual(clock['duration_ticks'], {'512': 1, '1024': 1, '1536': 1})
        self.assertEqual(clock['gaps'], 0)
        self.assertIn('never setpts=N/24', clock['policy'])
        with self.assertRaises(ValueError):
            plan.clock_summary([{'index': 0, 'pts': 1, 'duration': 512}])
        gapped = plan.clock_summary([
            {'index': 0, 'pts': 0, 'duration': 512},
            {'index': 1, 'pts': 1024, 'duration': 1024},
        ])
        self.assertEqual(gapped['gaps'], 1)
        self.assertEqual(gapped['start_pts'], 0)

    def test_the_map_cannot_be_named_as_the_master(self):
        with self.assertRaises(ValueError):
            plan.refuse_master('hos_008_master_v04.mp4')
        self.assertTrue(str(plan.refuse_master('MUX_MAP.json')).endswith('MUX_MAP.json'))

    def test_the_real_pieces_cover_every_frame_without_a_film(self):
        report = plan.build_map()
        self.assertEqual(report['status'], 'MUX_MAP_ONLY')
        self.assertEqual(report['frames'], 12923)
        self.assertEqual(
            report['packet_copy_frames'] + report['high_encode_frames'] + report['exact_pcm_frames'],
            12923)
        self.assertEqual(report['exact_pcm_frames'], 139)
        self.assertEqual(report['frame_2869'], 'exact_pcm')
        self.assertEqual(report['frame_3259'], 'exact_pcm')
        self.assertEqual(report['frame_3353'], 'packet_copy')
        self.assertEqual(report['night_street'], 'packet_copy')
        self.assertEqual(report['jar_keep'], [3168, 3258])
        self.assertFalse(report['output_film_created'])
        self.assertFalse(report['finished_master'])
        self.assertFalse(report['approval'])
        self.assertEqual(report['spend_gbp'], 0)
        self.assertIsNone(report['clock'])
        order = report['order']
        self.assertEqual(order[0]['first'], 0)
        self.assertEqual(order[-1]['last'], 12922)
        self.assertEqual(sum(run['frames'] for run in order), 12923)
        jar_run = next(run for run in order if run['clip'] == 'jar_keep')
        self.assertEqual([jar_run['first'], jar_run['last'], jar_run['role']],
                         [3168, 3258, 'packet_copy'])
        salon = next(run for run in order if run['first'] == 2506)
        self.assertEqual([salon['last'], salon['role'], salon['frames']], [2665, 'high_encode', 160])


if __name__ == '__main__':
    unittest.main()
