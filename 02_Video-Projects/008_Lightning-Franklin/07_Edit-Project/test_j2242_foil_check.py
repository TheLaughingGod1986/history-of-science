import unittest
from fractions import Fraction

import numpy as np

from _j2242_foil_check import FOIL_FRAME, JAR_FLIP, REPLACE, classify, plate_match


def _frames():
    frames = []
    origin = 1695744 - (3305 - 3260) * 512
    for index in range(3260, 3410):
        key = 1 if index in (3344, 3405) else 0
        frames.append([index, origin + (index - 3260) * 512, 512, key])
    return frames


def _row():
    return {
        'jar_flip_2_18': {'master_frame': JAR_FLIP, 'inside_replace_3260_3343': True},
        'foil_next_spark_2_20': {
            'master_frame': FOIL_FRAME,
            'note_resolved': False,
            'splice': False,
            'distinct_from_jar_flip': True,
            'beyond_replacement_ending_139_625s': True,
            'inside_replace_3260_3343': False,
            'candidate_keyframe_envelope': [3344, 3404],
        },
    }


class FoilCheck(unittest.TestCase):
    def test_clock_keeps_the_two_checks_apart(self):
        found = classify(_row(), _frames(), '1/12288')
        self.assertEqual(found['jar_flip_frame'], 3305)
        self.assertEqual(found['foil_frame'], 3353)
        self.assertEqual(found['replacement'], list(REPLACE))
        self.assertEqual(found['replacement_end_s'], '139.625')
        self.assertEqual(found['spark_envelope'], [3344, 3404])
        self.assertTrue(found['jar_flip_inside_replacement'])
        self.assertFalse(found['foil_inside_replacement'])
        self.assertFalse(found['note_resolved'])
        self.assertFalse(found['splice'])
        self.assertEqual(found['frame_2869'], 'out')

    def test_resolved_or_spliced_note_is_refused(self):
        resolved = _row()
        resolved['foil_next_spark_2_20']['note_resolved'] = True
        with self.assertRaises(ValueError):
            classify(resolved, _frames(), '1/12288')
        spliced = _row()
        spliced['foil_next_spark_2_20']['splice'] = True
        with self.assertRaises(ValueError):
            classify(spliced, _frames(), '1/12288')

    def test_shifted_envelope_is_refused(self):
        frames = _frames()
        for frame in frames:
            if frame[0] == 3405:
                frame[3] = 0
            if frame[0] == 3406:
                frame[3] = 1
        with self.assertRaises(ValueError):
            classify(_row(), frames, '1/12288')

    def test_plate_match_names_the_spark_and_refuses_a_tie(self):
        spark = np.zeros((3, 4), np.uint8)
        spark[1] = (10, 20, 30, 40)
        foil = np.full((3, 4), 200, np.uint8)
        found = plate_match(spark[1], {'08_jar_spark': spark, '07_foil_jar': foil})
        self.assertEqual(found['plate'], '08_jar_spark')
        self.assertEqual(found['source_frame'], 1)
        self.assertTrue(found['source_frame_unique'])
        near = spark.copy()
        near[2] = spark[1]
        tied = plate_match(spark[1], {'08_jar_spark': near, '07_foil_jar': foil})
        self.assertEqual(tied['plate'], '08_jar_spark')
        self.assertFalse(tied['source_frame_unique'])
        ambiguous = plate_match(spark[1], {'08_jar_spark': spark, '07_foil_jar': spark})
        self.assertIsNone(ambiguous['plate'])
        self.assertLess(ambiguous['plate_margin'], 0.1)

    def test_replacement_end_is_the_real_fraction(self):
        self.assertEqual(Fraction(1695744 + 38 * 512 + 512, 12288), Fraction('139.625'))


if __name__ == '__main__':
    unittest.main()
