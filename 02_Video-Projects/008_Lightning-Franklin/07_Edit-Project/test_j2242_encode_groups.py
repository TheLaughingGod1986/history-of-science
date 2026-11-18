import unittest

import _j2242_encode_groups as enc
import _j2242_packet_mux as mux


class EncodeGroups(unittest.TestCase):
    def test_kept_master_frames_are_refused(self):
        report = mux.build_report()
        jar = next(env for env in report['envelopes'] if env['first'] == 3168)
        with self.assertRaises(ValueError):
            enc.require_fully_changed(jar)
        medal = next(env for env in report['envelopes'] if env['first'] == 9430)
        enc.require_fully_changed(medal)
        self.assertEqual(medal['stitch_source_frames'], [])

    def test_encode_command_matches_the_salon_high_profile_recipe(self):
        args = enc.encode_args('in.nut', 'group_9430_9486_high.mp4', 57)
        self.assertIn('libx264', args)
        self.assertIn('high', args)
        self.assertIn('1', args)
        self.assertIn('bframes=0:repeat-headers=1:keyint=57:min-keyint=57:scenecut=0', args)
        self.assertIn('-an', args)
        self.assertNotIn('setpts=N/24', ' '.join(args))
        with self.assertRaises(ValueError):
            enc.encode_args('in.nut', 'hos_008_master_v04.mp4', 57)
        with self.assertRaises(ValueError):
            enc.encode_args('in.nut', 'group_0.mp4', 0)

    def test_copley_is_one_nut_and_salon_is_not_in_the_placed_files(self):
        import _j2242_stitch_groups as stitch
        report = mux.build_report()
        files = stitch.placed_files(mux.REVIEW)
        medal = next(env for env in report['envelopes'] if env['first'] == 9430)
        piece = enc.single_nut(medal, files)
        self.assertEqual((piece['first'], piece['last']), (9430, 9486))
        self.assertTrue(piece['path'].endswith('.nut'))
        salon = next(env for env in report['envelopes'] if env['first'] == 2506)
        with self.assertRaises(ValueError):
            enc.single_nut(salon, files)


if __name__ == '__main__':
    unittest.main()
