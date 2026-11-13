import unittest

import _j2242_packet_mux as mux
import _j2242_stitch_groups as stitch


def _part(source, first, last):
    return {'source': source, 'first': first, 'last': last, 'path': f'{source}.nut',
            'sha256': 'a' * 64}


class StitchGroups(unittest.TestCase):
    def test_gaps_at_both_ends_and_the_middle_stay_master_frames(self):
        pieces = stitch.sequence(0, 9, [
            _part('body', 2, 3),
            _part('tail', 7, 7),
        ])
        self.assertEqual([(p['kind'], p['first'], p['last']) for p in pieces], [
            ('master', 0, 1),
            ('intermediate', 2, 3),
            ('master', 4, 6),
            ('intermediate', 7, 7),
            ('master', 8, 9),
        ])

    def test_an_overlap_is_refused(self):
        with self.assertRaises(ValueError):
            stitch.sequence(0, 5, [_part('a', 0, 3), _part('b', 3, 5)])

    def test_frame_2869_cannot_be_a_replacement(self):
        with self.assertRaises(ValueError):
            stitch.sequence(2860, 2870, [_part('plate', 2860, 2870)])

    def test_the_old_safe_path_is_kept_only_with_its_title_fix(self):
        old = _part('SAFE_PATH.json', 11038, 11117)
        fixed = _part('SAFE_PATH_TITLE.json', 11038, 11117)
        with self.assertRaises(ValueError):
            stitch.drop_superseded([old])
        kept = stitch.drop_superseded([old, fixed])
        self.assertEqual([part['source'] for part in kept], ['SAFE_PATH_TITLE.json'])

    def test_the_three_real_groups_use_master_pixels_for_the_gaps(self):
        groups = stitch.partial_groups(mux.build_report(), mux.REVIEW)
        self.assertEqual([(g['first'], g['last']) for g in groups], [
            (2718, 2887), (3168, 3343), (11038, 11245),
        ])
        frank, jar, safe = groups
        self.assertEqual([(p['kind'], p['first'], p['last']) for p in frank['pieces']], [
            ('intermediate', 2718, 2864),
            ('intermediate', 2865, 2867),
            ('intermediate', 2868, 2868),
            ('master', 2869, 2869),
            ('intermediate', 2870, 2887),
        ])
        self.assertEqual([(p['kind'], p['first'], p['last']) for p in jar['pieces']], [
            ('master', 3168, 3259),
            ('intermediate', 3260, 3343),
        ])
        self.assertEqual([(p['kind'], p['first'], p['last'], p.get('source')) for p in safe['pieces']], [
            ('intermediate', 11038, 11117, 'SAFE_PATH_TITLE.json'),
            ('master', 11118, 11245, None),
        ])
        self.assertTrue(safe['pieces'][0]['path'].endswith('J2242-safe-path-v02/safe_path.nut'))
        report = stitch.build_report()
        self.assertEqual(report['status'], 'STITCH_PLAN_ONLY')
        self.assertFalse(report['output_film_created'])
        self.assertFalse(report['finished_master'])
        self.assertEqual(report['spend_gbp'], 0)


if __name__ == '__main__':
    unittest.main()
