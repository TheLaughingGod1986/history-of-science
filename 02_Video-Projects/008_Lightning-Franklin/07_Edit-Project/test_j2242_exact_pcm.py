import tempfile
import unittest
from pathlib import Path

import _j2242_exact_pcm as exact


class ExactPcm(unittest.TestCase):
    def test_only_the_four_blocked_runs_are_encoded(self):
        for first, last in exact.BLOCKED:
            self.assertEqual(exact.require_blocked(first, last), (first, last))
        for pair in ((2868, 2869), (3258, 3259), (4130, 4139), (3168, 3258), (11118, 11246)):
            with self.assertRaises(ValueError):
                exact.require_blocked(*pair)

    def test_the_clip_cannot_be_named_as_the_master(self):
        with self.assertRaises(ValueError):
            exact.refuse_master_name('hos_008_master_v04.mp4')
        with self.assertRaises(ValueError):
            exact.refuse_master_name('exact.nut')
        self.assertTrue(str(exact.refuse_master_name('exact_2869.h264')).endswith('.h264'))

    def test_deblocking_is_off_and_a_tiny_picture_roundtrips(self):
        width = height = 16
        y = bytes((index * 17 + 3) & 255 for index in range(width * height))
        u = bytes((index * 5 + 40) & 255 for index in range(width * height // 4))
        v = bytes((index * 9 + 90) & 255 for index in range(width * height // 4))
        frame = y + u + v
        other = bytes(255 - byte for byte in y) + u + v
        payload = exact.ipcm_idr(frame, width, height, height, 0, 0)
        self.assertTrue(exact.deblocking_disabled(payload))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'exact.h264'
            path.write_bytes(
                exact.access_unit(frame, width, height, height, exact.tiny_sps(), 0, 0)
                + exact.access_unit(other, width, height, height, exact.tiny_sps(), 0, 1))
            self.assertEqual(exact.decode_annexb(path, width, height), [frame, other])


if __name__ == '__main__':
    unittest.main()
