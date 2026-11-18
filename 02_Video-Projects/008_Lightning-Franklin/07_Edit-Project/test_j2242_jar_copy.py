import unittest

import _j2242_jar_copy as jar


def row(index, dts, pts=None):
    return {'index': index, 'dts': dts, 'pts': pts if pts is not None else dts + 1024, 'duration': 512}


class JarCopy(unittest.TestCase):
    def test_kept_frames_are_a_decode_prefix(self):
        kept = [row(index, 1000 + index) for index in range(jar.JAR_FIRST, jar.JAR_LAST + 1)]
        blocked = row(jar.JAR_BLOCKED, 1000 + jar.JAR_BLOCKED + 10)
        ordered = jar.assert_decode_prefix(kept, blocked)
        self.assertEqual(ordered[0]['index'], jar.JAR_FIRST)
        self.assertEqual(ordered[-1]['index'], jar.JAR_LAST)
        self.assertEqual(len(ordered), 91)

    def test_frame_3259_cannot_sit_inside_the_copy(self):
        kept = [row(index, 1000 + index) for index in range(jar.JAR_FIRST, jar.JAR_LAST + 1)]
        blocked = row(jar.JAR_BLOCKED, kept[-1]['dts'])
        with self.assertRaises(ValueError):
            jar.assert_decode_prefix(kept, blocked)

    def test_a_short_range_is_refused(self):
        kept = [row(index, 1000 + index) for index in range(jar.JAR_FIRST, jar.JAR_LAST)]
        blocked = row(jar.JAR_BLOCKED, 9000)
        with self.assertRaises(ValueError):
            jar.assert_decode_prefix(kept, blocked)

    def test_decoded_hashes_have_to_match_the_same_pts(self):
        frames = [{'index': index, 'pts': 10_000 + index} for index in range(jar.JAR_FIRST, jar.JAR_LAST + 1)]
        source = [{
            'pts': frame['pts'], 'duration': 512, 'size': 1920 * 1080 * 3 // 2, 'hash': f"h{frame['index']}",
        } for frame in frames]
        clip = [dict(row) for row in source]
        self.assertEqual(jar.match_hashes(source, clip, frames), 91)
        clip[0]['hash'] = 'different'
        with self.assertRaises(ValueError):
            jar.match_hashes(source, clip, frames)


if __name__ == '__main__':
    unittest.main()
