import unittest

import numpy as np

from _j2242_safe_path_title import (
    HELD_TITLE_FRAME, INK_BOX, TITLE_BOX, chroma_box, clear_title_box, same_field,
)


def _field(title=False, corner=False):
    y = np.full((1080, 1920), 40, np.uint8)
    if title:
        y[130:165, 860:1060] = 220
    if corner:
        y[114:122, 640:648] = 0
    return y


class SafePathTitle(unittest.TestCase):
    def test_box_covers_the_v12_ink_and_stays_on_the_chroma_grid(self):
        x0, x1, y0, y1 = TITLE_BOX
        ix0, ix1, iy0, iy1 = INK_BOX
        self.assertTrue(x0 <= ix0 and x1 >= ix1 and y0 <= iy0 and y1 >= iy1)
        self.assertEqual(chroma_box(TITLE_BOX), (320, 640, 57, 91))
        with self.assertRaises(ValueError):
            chroma_box((640, 1280, 115, 182))

    def test_clear_copies_the_field_and_leaves_the_picture_outside(self):
        y = np.full((8, 8), 9, np.uint8)
        donor = np.ones((8, 8), np.uint8)
        u = np.full((4, 4), 3, np.uint8)
        v = np.full((4, 4), 4, np.uint8)
        du, dv = np.full((4, 4), 5, np.uint8), np.full((4, 4), 6, np.uint8)
        out_y, out_u, out_v = clear_title_box(y, u, v, donor, du, dv, (2, 6, 2, 6))
        self.assertTrue(np.array_equal(out_y[2:6, 2:6], donor[2:6, 2:6]))
        self.assertTrue(np.all(out_y[0, :] == 9) and np.all(out_y[:, 0] == 9))
        self.assertTrue(np.array_equal(out_u[1:3, 1:3], du[1:3, 1:3]))
        self.assertEqual(int(out_u[0, 0]), 3)
        self.assertEqual(int(out_v[0, 0]), 4)
        with self.assertRaises(ValueError):
            clear_title_box(y, u, v, donor, du, dv, (1, 6, 2, 6))

    def test_same_field_accepts_ink_on_the_clear_field_only(self):
        donor = _field()
        titled = _field(title=True)
        indices = [0, HELD_TITLE_FRAME]
        measured = same_field(donor, [donor, titled], indices)
        self.assertGreaterEqual(measured['held_title_center_mse_min'], 500)
        self.assertLessEqual(measured['corner_mse_max'], 4)
        with self.assertRaises(ValueError):
            same_field(donor, [donor, _field(title=True, corner=True)], indices)
        with self.assertRaises(ValueError):
            same_field(donor, [donor, donor], indices)


if __name__ == '__main__':
    unittest.main()
