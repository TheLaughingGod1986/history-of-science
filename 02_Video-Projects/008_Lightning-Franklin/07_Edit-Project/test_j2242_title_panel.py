import unittest

import numpy as np

from _j2242_title_panel import (
    LABELS,
    METAL_CHECK_FRAME,
    METAL_FRAME_STOP,
    PAINT_ROWS,
    UMBER,
    alpha_frame_for_picture,
    label_words,
    metal_frames,
    paint_matched,
    panel_behind,
    summarize_frames,
    title_box,
)


def alpha_frame():
    frame = np.zeros((1080, 1920, 4), np.uint8)
    frame[120:176, 600:1300, :3] = (210, 170, 90)
    frame[120:176, 600:1300, 3] = 255
    frame[400:620, 200:1700, 3] = 255
    return frame


class TitlePanel(unittest.TestCase):
    def test_the_letter_banner_is_not_painted(self):
        self.assertNotIn('04_letter_crosses', PAINT_ROWS)
        self.assertEqual(PAINT_ROWS, tuple(LABELS))
        for label in LABELS.values():
            self.assertLessEqual(len(label_words(label)), 4)

    def test_the_title_line_is_the_box_and_the_diagram_is_not(self):
        box = title_box(alpha_frame())
        self.assertLessEqual(box[1], 120)
        self.assertGreaterEqual(box[3], 175)
        self.assertLess(box[3], 250)

    def test_a_tall_band_and_a_speck_are_refused(self):
        tall = np.zeros((1080, 1920, 4), np.uint8)
        tall[100:300, 100:1800, 3] = 255
        speck = np.zeros((1080, 1920, 4), np.uint8)
        speck[10:14, 10:40, 3] = 255
        with self.assertRaises(ValueError):
            title_box(tall)
        with self.assertRaises(ValueError):
            title_box(speck)

    def test_the_panel_is_umber_behind_the_words_only(self):
        alpha = alpha_frame()
        glyphs = alpha[:, :, 3] > 0
        picture = np.full((1080, 1920, 3), 180, np.uint8)
        picture[glyphs] = alpha[:, :, :3][glyphs]
        box = title_box(alpha)
        out = panel_behind(picture, box, glyphs)
        changed = np.any(out != picture, axis=2)
        self.assertTrue(changed.any())
        self.assertTrue(np.all(out[changed] == UMBER))
        self.assertTrue(np.all(out[glyphs] == picture[glyphs]))
        x0, y0, x1, y1 = box
        outside = np.ones((1080, 1920), dtype=bool)
        outside[y0:y1 + 1, x0:x1 + 1] = False
        self.assertTrue(np.all(out[outside] == picture[outside]))
        self.assertTrue(np.all(out[y0, x0] == UMBER))
        self.assertTrue(np.all(out[y0 + 4, x0 + 4] == UMBER))

    def test_an_empty_box_and_a_full_box_are_refused(self):
        picture = np.full((1080, 1920, 3), 180, np.uint8)
        empty = np.zeros((1080, 1920), dtype=bool)
        full = np.ones((1080, 1920), dtype=bool)
        with self.assertRaises(ValueError):
            panel_behind(picture, (100, 100, 400, 180), empty)
        with self.assertRaises(ValueError):
            panel_behind(picture, (100, 100, 400, 180), full)

    def test_five_words_are_refused(self):
        with self.assertRaises(ValueError):
            label_words('ONE TWO THREE FOUR FIVE')

    def test_the_metal_window_stops_before_the_safe_path(self):
        frames = metal_frames()
        self.assertEqual(len(frames), 42)
        self.assertEqual(frames[21], METAL_CHECK_FRAME)
        self.assertNotIn(METAL_FRAME_STOP, frames)
        self.assertNotIn(2869, frames)

    def test_alpha_frames_match_the_checked_timestamps(self):
        self.assertEqual(alpha_frame_for_picture(53, 114, 159), 66)
        self.assertEqual(alpha_frame_for_picture(134, 160, 219), 168)
        self.assertEqual(alpha_frame_for_picture(48, 76, 95), 60)
        with self.assertRaises(ValueError):
            alpha_frame_for_picture(113, 114, 100)

    def test_a_frame_without_a_title_is_kept_and_an_aligned_title_is_painted(self):
        alpha = alpha_frame()
        blank = np.zeros((1080, 1920, 4), np.uint8)
        picture = np.full((1080, 1920, 3), 180, np.uint8)
        picture[alpha[:, :, 3] > 0] = alpha[:, :, :3][alpha[:, :, 3] > 0]
        kept, kept_status = paint_matched(picture, blank)
        self.assertIs(kept, picture)
        self.assertEqual(kept_status['status'], 'kept')
        painted, painted_status = paint_matched(picture, alpha)
        self.assertEqual(painted_status['status'], 'painted')
        changed = np.any(painted != picture, axis=2)
        self.assertTrue(np.all(painted[changed] == UMBER))
        title_only = np.zeros((1080, 1920, 4), np.uint8)
        title_only[120:176, 600:1300, :3] = (210, 170, 90)
        title_only[120:176, 600:1300, 3] = 255
        mismatched = np.zeros((1080, 1920, 3), np.uint8)
        untouched, status = paint_matched(mismatched, title_only)
        self.assertEqual(status['status'], 'kept')
        self.assertEqual(status['why'], 'unaligned')
        self.assertTrue(np.array_equal(untouched, mismatched))

    def test_a_row_needs_one_stable_title_box(self):
        with self.assertRaises(ValueError):
            summarize_frames([{'status': 'kept', 'why': 'no title'}])
        summary = summarize_frames([
            {'status': 'kept', 'why': 'no title'},
            {'status': 'painted', 'box': [1, 2, 3, 4], 'alignment_mae': 4.0},
            {'status': 'painted', 'box': [1, 2, 3, 4], 'alignment_mae': 6.0},
        ])
        self.assertEqual(summary['painted'], 2)
        self.assertEqual(summary['kept'], 1)
        self.assertEqual(summary['box'], [1, 2, 3, 4])
        with self.assertRaises(ValueError):
            summarize_frames([
                {'status': 'painted', 'box': [1, 2, 3, 4], 'alignment_mae': 4.0},
                {'status': 'painted', 'box': [2, 2, 3, 4], 'alignment_mae': 4.0},
            ])


if __name__ == '__main__':
    unittest.main()
