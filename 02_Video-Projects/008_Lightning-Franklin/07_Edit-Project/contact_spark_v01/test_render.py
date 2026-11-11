import unittest
import numpy as np
from render import spark


class ContactSparkTests(unittest.TestCase):
    def test_bounded_warm_single_flick(self):
        for count in (3, 4):
            for rod, knuckle in (((90, 80), (94, 80)), ((90, 78), (90, 82))):
                for phase in range(-1, count + 1):
                    rgba = np.array(spark((320, 180), rod, knuckle, phase, count))
                    mask = rgba[:, :, 3] > 0
                    if phase < 0 or phase >= count:
                        self.assertFalse(mask.any())
                        continue
                    self.assertTrue(mask.any())
                    colours = rgba[:, :, :3][mask]
                    self.assertTrue((colours[:, 0] >= colours[:, 1]).all())
                    self.assertTrue((colours[:, 1] >= colours[:, 2]).all())
                    y, x = np.where(mask)
                    centre = (np.array(rod) + knuckle) / 2
                    self.assertTrue((((x-centre[0])**2 + (y-centre[1])**2) <= (np.linalg.norm(np.array(rod)-knuckle)/2)**2).all())

    def test_guards(self):
        for rod, knuckle in (((0, 0), (100, 100)), ((-1, 0), (2, 0)), ((10, 10), (10, 10)), ((float('nan'), 0), (2, 0))):
            with self.assertRaises(ValueError):
                spark((1920, 1080), rod, knuckle, 0)

    def test_bloom_only_on_contact(self):
        a = [np.array(spark((1920, 1080), (950, 540), (970, 540), n))[:, :, 3] for n in range(4)]
        self.assertGreater(np.count_nonzero(a[0]), np.count_nonzero(a[1]))
        self.assertTrue(all(a[i].sum() > a[i+1].sum() for i in range(3)))


if __name__ == '__main__':
    unittest.main()
