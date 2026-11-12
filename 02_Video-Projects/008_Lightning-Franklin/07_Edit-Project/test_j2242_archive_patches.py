import copy
import unittest
from _j2242_archive_patches import SPECS, patch_clock, validate_native_source

class ArchiveWindows(unittest.TestCase):
    def clock(self, kind):
        s = SPECS[kind]
        return dict(time_base='1/12288', frames=[dict(index=i,
            pts=s['first_pts'] + (i-s['first'])*512,
            duration=1024 if i == s['overlap'] else 512)
            for i in range(s['last']+1)])

    def test_selected_windows_and_absolute_pts(self):
        for kind, count in [('storm',96),('jar',84)]:
            f = patch_clock(self.clock(kind), kind)
            self.assertEqual(len(f), count)
            self.assertEqual(f[0]['pts'], SPECS[kind]['first_pts'])

    def test_reject_clock_mutations(self):
        for kind in SPECS:
            for field, value in [('pts',0),('index',0),('duration',1024)]:
                t = self.clock(kind)
                t['frames'][SPECS[kind]['first']][field] = value
                with self.assertRaises(ValueError): patch_clock(t, kind)

    def test_reject_normalized_storm_overlap(self):
        t=self.clock('storm'); t['frames'][745]['duration']=512
        with self.assertRaises(ValueError): patch_clock(t,'storm')

    def test_reject_truncation_and_timebase(self):
        for kind in SPECS:
            t=self.clock(kind)
            for bad in [dict(t,time_base='1/24'),dict(t,frames=t['frames'][:-1])]:
                with self.assertRaises(ValueError): patch_clock(bad,kind)

    def test_native_input_and_short_or_shifted_rejection(self):
        t=dict(time_base='1/24',frames=[dict(pts=i,duration=1) for i in range(96)])
        validate_native_source(t,96)
        for bad in [dict(t,frames=t['frames'][:-1]),copy.deepcopy(t)]:
            if len(bad['frames'])==96: bad['frames'][0]['pts']=1
            with self.assertRaises(ValueError): validate_native_source(bad,96)

if __name__ == '__main__': unittest.main()
