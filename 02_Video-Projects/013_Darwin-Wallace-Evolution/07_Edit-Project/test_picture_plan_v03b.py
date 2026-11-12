"""Independent regression checks for the cue repair (no audio/media changes)."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

EDIT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('cue_audit', EDIT/'_audit_picture_plan_v03b.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class CueSchedule(unittest.TestCase):
    def setUp(self):
        self.original = json.loads((EDIT/'PICTURE_PLAN_v03.json').read_text())['overlay_cues']
        self.cues, self.removed = audit.schedule(self.original)

    def test_input_untouched_and_names_held_at_exact_onset(self):
        before = copy.deepcopy(self.original)
        audit.schedule(self.original)
        self.assertEqual(self.original, before)
        names = {audit.label(c): c for c in self.original if c['overlay']['kind']=='WHO'}
        for c in self.cues:
            if c['overlay']['kind']=='WHO':
                self.assertEqual(c['display_start_s'], names[audit.label(c)]['onset_s'])
                self.assertGreaterEqual(c['display_duration_s'], 3)
                self.assertLessEqual(c['display_duration_s'], 4)

    def test_all_overlaps_resolved_without_outliving_anchor_word(self):
        for a, b in zip(self.cues, self.cues[1:]):
            self.assertLessEqual(a['display_end_s'], b['display_start_s'])
        for c in self.cues:
            self.assertLessEqual(c['display_start_s'], c['word_end_s'])
        self.assertEqual(len(self.cues), 43)
        self.assertEqual(len(self.removed), 2)

    def test_barnacle_merge_keeps_data_and_fact(self):
        c = next(c for c in self.cues if audit.label(c)=='EIGHT YEARS ON BARNACLES')
        self.assertEqual(c['satisfies'], ['FACT', 'DATA'])
        self.assertEqual(len(c['merged_source_rows']), 2)
        self.assertIn('counter', c['overlay']['detail'])

    def test_impossible_name_collision_is_rejected(self):
        c = copy.deepcopy(next(c for c in self.original if c['overlay']['kind']=='WHO'))
        b = copy.deepcopy(c)
        b['onset_s'] += 1
        b['word_end_s'] += 1
        with self.assertRaisesRegex(AssertionError, 'Never postpone a name'):
            audit.schedule([c,b])


if __name__ == '__main__':
    unittest.main()
