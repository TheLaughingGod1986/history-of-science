import copy
import unittest
import _j2242_salon_splice as splice


def nal(t):
    return (1).to_bytes(4, 'big') + bytes([t])


class BoundaryTests(unittest.TestCase):
    def test_requires_parameter_restore_with_idr(self):
        splice.check_headers(nal(7) + nal(8) + nal(5), 4)
        for types in ([5], [7, 5], [8, 5], [7, 8, 1]):
            with self.assertRaises(ValueError):
                splice.check_headers(b''.join(nal(t) for t in types), 4)

    def test_clock_rejects_gap_or_wrong_boundaries(self):
        timeline = {'time_base': '1/12288', 'frames': [
            {'pts': 1536 + i * 512, 'duration': 512,
             'key_frame': int(i in (2506, 2666))} for i in range(2667)]}
        self.assertEqual(len(splice.validate_clock(timeline)), 160)
        for index, field, value in ((2520, 'pts', 0), (2520, 'duration', 1024),
                                     (2506, 'key_frame', 0), (2666, 'key_frame', 0)):
            bad = copy.deepcopy(timeline)
            bad['frames'][index][field] = value
            with self.assertRaises(ValueError):
                splice.validate_clock(bad)


if __name__ == '__main__':
    unittest.main()
