"""Original-clock caption scheduling and house-style guards."""
import json
import unittest
from pathlib import Path
import _j2242_caption_layers as captions

EDIT = Path(__file__).resolve().parent


class CaptionTests(unittest.TestCase):
    def setUp(self):
        self.timeline = json.loads((EDIT / 'J2163_MASTER_FRAME_PTS.json').read_text())
        self.timeline['frames'] = captions.recipe.as_frame_dicts(self.timeline['frames'])
        self.manifest = json.loads((EDIT / 'J2163_CORRECTION_MANIFEST.json').read_text())
        self.notes = (EDIT.parent / '01_Script/FACT_NOTES_v01.md').read_text()

    def schedule(self):
        return captions.caption_schedule(self.timeline, self.manifest, self.notes)

    def test_exact_33_layers_and_safe_path(self):
        cards = self.schedule()
        self.assertEqual(len(cards), 33)
        safe = next(c for c in cards if c['row'] == '11_safe_path')
        self.assertEqual(safe['hold_ticks'], 40960)
        self.assertEqual(safe['frame_in'], 11038)
        self.assertEqual(len(safe['clock']), 80)
        self.assertTrue(all(c['word_count'] <= 4 and c['hold_ticks'] <= 49152 for c in cards))

    def test_remainder_is_clear(self):
        first = self.schedule()[0]
        self.assertEqual(first['frame_last'], 95)
        self.assertEqual(first['window_remainder_ticks'], 23552)
        self.assertEqual(first['clock'][-1]['index'], 95)

    def test_rescaled_master_clock_rejected(self):
        self.timeline['time_base'] = '1/24'
        with self.assertRaises(ValueError):
            self.schedule()

    def test_missing_caption_rejected(self):
        self.manifest['caption_treatment']['labels'].pop()
        with self.assertRaises(ValueError):
            self.schedule()

    def test_pts_expression_preserves_gaps(self):
        frames = [{'pts': x} for x in [1536, 2048, 3072, 3584]]
        self.assertEqual(captions.clock_expression(frames), '1536+N*512+(512)*gte(N,2)')

    def test_duplicate_pts_rejected(self):
        with self.assertRaises(ValueError):
            captions.clock_expression([{'pts': 1536}, {'pts': 1536}])


if __name__ == '__main__':
    unittest.main()
