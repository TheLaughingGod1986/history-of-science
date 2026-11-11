import unittest
import numpy as np
from render import spark


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
        # Soft bloom stays on the gap: about 25px, not a frame-wide glow.
        self.assertGreaterEqual(x.min(), 500)
        self.assertLessEqual(x.max(), 580)
        self.assertGreaterEqual(y.min(), 500)
        self.assertLessEqual(y.max(), 580)
        self.assertLess(x.max() - x.min(), 80)
        self.assertLess(y.max() - y.min(), 80)

    def test_peak_core_width_and_gap_bloom(self):
        a = np.array(spark((1920, 1080), (970, 540), (950, 540), 0, frames=2))[:, :, 3]
        b = np.array(spark((1920, 1080), (970, 540), (950, 540), 1, frames=2))[:, :, 3]
        peak = int(a[540, 960])
        self.assertGreaterEqual(peak, 220)
        half = peak / 2
        lit = np.where(a[:, 960] >= half)[0]
        width = int(lit.max() - lit.min() + 1)
        self.assertTrue(3 <= width <= 5)
        # Low-alpha bloom on the peak frame, centred on the gap, about 20–30px.
        self.assertGreaterEqual(int(a[520, 960]), 8)
        self.assertLessEqual(int(a[520, 960]), 28)
        self.assertGreater(int(a[515, 960]), 0)
        self.assertEqual(int(a[500, 960]), 0)
        # Half-strength frame keeps the shorter core and does not carry the bloom.
        self.assertEqual(int(b[520, 960]), 0)
        self.assertEqual(int(b[540, 980]), 0)
        self.assertGreater(int(a[540, 980]), 0)

if __name__ == '__main__':
    unittest.main()
