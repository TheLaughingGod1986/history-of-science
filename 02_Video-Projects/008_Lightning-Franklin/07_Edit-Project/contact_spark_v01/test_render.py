import unittest
import numpy as np
from render import BLOOM_PEAK, BLOOM_RADIUS, spark


class ContactSparkTests(unittest.TestCase):
    def test_warm_single_flick(self):
        for count in (2, 3, 4):
            for phase in range(-1, count + 1):
                rgba = np.array(spark((320, 180), (94, 80), (90, 80), phase, count))
                mask = rgba[:, :, 3] > 0
                if phase < 0 or phase >= count:
                    self.assertFalse(mask.any())
                else:
                    self.assertTrue(mask.any())
                    self.assertTrue((rgba[:, :, :3][mask] == (255, 246, 224)).all())

    def test_guards(self):
        for rod, knuckle in (((0, 0), (100, 100)), ((-1, 0), (2, 0)), ((10, 10), (10, 10)), ((float('nan'), 0), (2, 0))):
            with self.assertRaises(ValueError):
                spark((1920, 1080), rod, knuckle, 0)

    def test_streak_and_knuckle_tail(self):
        a = [np.array(spark((1920, 1080), (970, 540), (950, 540), n))[:, :, 3] for n in range(4)]
        # Whole visible gap lights up, and a two-pixel core has soft shoulders.
        self.assertTrue((a[0][540, 950:971] > 100).all())
        self.assertGreater(a[0][540, 960], a[0][541, 960])
        self.assertGreater(a[0][541, 960], a[0][542, 960])
        self.assertGreater(a[0][541, 960], a[0][541, 952])
        self.assertAlmostEqual(a[1][540, 960]/a[0][540, 960], .5, delta=.03)
        self.assertLess(a[1][540, 950], a[0][540, 950])
        for n in (2, 3):
            y, x = np.unravel_index(a[n].argmax(), a[n].shape)
            self.assertEqual((x, y), (950, 540))
            self.assertEqual(a[n][540, 960], 0)
        self.assertTrue(all(a[i].sum() > a[i+1].sum() for i in range(3)))

    def test_rotates_and_stays_local(self):
        a = np.array(spark((1080, 1080), (550, 540), (530, 540), 0))[:, :, 3]
        b = np.array(spark((1080, 1080), (540, 550), (540, 530), 0))[:, :, 3]
        np.testing.assert_array_equal(a.T, b)
        y, x = np.where(a)
        # Bloom stays on the gap: about 60px radius, not a frame-wide glow.
        self.assertGreaterEqual(x.min(), 450)
        self.assertLessEqual(x.max(), 630)
        self.assertGreaterEqual(y.min(), 450)
        self.assertLessEqual(y.max(), 630)
        self.assertLess(x.max() - x.min(), 170)
        self.assertLess(y.max() - y.min(), 170)
        self.assertGreater(x.max() - x.min(), 90)

    def test_peak_core_width_and_gap_bloom(self):
        core = np.array(spark((1920, 1080), (970, 540), (950, 540), 0, frames=2, bloom_scale=0))[:, :, 3]
        a = np.array(spark((1920, 1080), (970, 540), (950, 540), 0, frames=2))[:, :, 3]
        b = np.array(spark((1920, 1080), (970, 540), (950, 540), 1, frames=2))[:, :, 3]
        pre = np.array(spark((1920, 1080), (970, 540), (950, 540), 0, frames=2, core=False, bloom_scale=0.25))[:, :, 3]
        peak = int(core[540, 960])
        self.assertGreaterEqual(peak, 220)
        half = peak / 2
        lit = np.where(core[:, 960] >= half)[0]
        width = int(lit.max() - lit.min() + 1)
        self.assertTrue(3 <= width <= 5)
        # Streak stops at the skin edge (knuckle x=950). One pixel onto the finger is empty.
        self.assertEqual(int(core[540, 949]), 0)
        self.assertGreater(int(core[540, 951]), 100)
        # Warm bloom centred on the gap. About 2 counts at 60px, gone by ~75px.
        # 20px off the gap the glow is bright enough to survive a phone downscale.
        self.assertGreaterEqual(int(a[520, 960]), 80)
        self.assertLessEqual(int(a[520, 960]), 160)
        radius = int(round(BLOOM_RADIUS))
        self.assertGreaterEqual(int(a[540 - radius, 960]), 1)
        self.assertLessEqual(int(a[540 - radius, 960]), 6)
        self.assertEqual(int(a[540 - radius - 18, 960]), 0)
        self.assertLess(a.max() - core.max(), 5)
        # Half-strength frame carries the same bloom at half. Pre-glow is about a quarter, with no core.
        self.assertAlmostEqual(int(b[520, 960]) / int(a[520, 960]), 0.5, delta=0.08)
        self.assertAlmostEqual(int(pre[520, 960]) / int(a[520, 960]), 0.25, delta=0.08)
        self.assertEqual(int(pre[540, 960]) < int(a[540, 960]), True)
        self.assertLess(int(pre.max()), BLOOM_PEAK * 0.25 + 2)

if __name__ == '__main__':
    unittest.main()
