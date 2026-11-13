"""Independent checks of timing, footage accounting, and cue preservation."""
import hashlib
import json
from pathlib import Path
import unittest

EDIT=Path(__file__).resolve().parent


class Retiming(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan=json.loads((EDIT/'PICTURE_PLAN_v03d.json').read_text())
        cls.words=json.loads((EDIT.parent/'02_Voiceover/stt/hos_013_vo_v03a/words_fw_small_en.json').read_text())['words']
        cls.qualified=json.loads((EDIT/'timing_rough_J2652/qualified_boundaries_v03d.json').read_text())

    def test_continuous_frame_aligned_word_safe_coverage(self):
        end=0
        for r in self.plan['rows']:
            self.assertAlmostEqual(r['t_s'],end)
            end=r['t_end_s']
            self.assertAlmostEqual(end*50,round(end*50))
            self.assertLessEqual(r['use_s'],7)
            self.assertFalse(any(w['start']+1e-7<end<w['end']-1e-7 for w in self.words))
            self.assertTrue(any(q['start_s']-1e-7<=end<=q['end_s']+1e-7 for q in self.qualified))
        self.assertEqual(end,515)

    def test_source_accounting_and_unused_callback(self):
        groups={}
        for r in self.plan['rows']:
            groups.setdefault(r['source_row_v02'],[]).append(r)
        for group in groups.values():
            if group[0]['source_kind']=='new_mint_quality':
                self.assertLessEqual(sum(r['use_s'] for r in group),8+1e-7)
                for a,b in zip(group,group[1:]):
                    self.assertEqual(a['source_window_s'][1],b['source_window_s'][0])
        c=next(r for r in self.plan['rows'] if r['source_kind']=='existing_plate_reuse')
        self.assertGreaterEqual(c['source_window_s'][0],self.plan['rows'][0]['use_s'])
        self.assertLessEqual(c['source_window_s'][1],8)
        self.assertLessEqual(c['use_s'],4.2)
        self.assertAlmostEqual(c['use_s'],c['source_window_s'][1]-c['source_window_s'][0])

    def test_cues_and_chapter_titles_do_not_collide(self):
        old=json.loads((EDIT/'PICTURE_PLAN_v03b.json').read_text())['overlay_cues']
        spans=[]
        for a,b in zip(old,self.plan['overlay_cues']):
            for key in ('word_index','onset_s','display_start_s','display_end_s'):
                self.assertEqual(a[key],b[key])
            spans.append((b['display_start_s'],b['display_end_s']))
        for r in self.plan['rows']:
            if 'chapter_title_window_s' in r:
                start,end=r['chapter_title_window_s'];spans.append((start,end))
                self.assertGreaterEqual(end-start,2.5-1e-7)
                q=next(q for q in self.qualified if q['start_s']-1e-7<=start<=q['end_s']+1e-7)
                self.assertGreaterEqual(start-q['start_s'],.5-1e-7)
                self.assertLessEqual(start-q['start_s'],.8+1e-7)
        for a,b in zip(sorted(spans),sorted(spans)[1:]):
            self.assertLessEqual(a[1],b[0]+1e-7)

    def test_no_flash_beats_and_paint_matches_analogy(self):
        for r in self.plan['rows']:
            if 'card' not in r['id']:
                self.assertGreaterEqual(r['use_s'], 2.5-1e-7)
        paint=next(r for r in self.plan['rows'] if r['id']=='02b_paint_pots_mix')
        self.assertEqual(paint['t_end_s'],459.64)
        self.assertLessEqual(paint['t_s'],456.88)
        cabin=next(r for r in self.plan['rows'] if r['id']=='11_beagle_cabin_explorer_beat1')
        self.assertEqual(cabin['t_end_s'],71.22)
        self.assertIn('editorial_clause',cabin['cut_out_evidence'])
        self.assertEqual(cabin['cut_out_evidence']['gap_s'],0)

    def test_inputs_and_no_authorization(self):
        for name,digest in self.plan['source_v02_sha256'].items():
            self.assertEqual(hashlib.sha256((EDIT/name).read_bytes()).hexdigest(),digest)
        self.assertEqual(hashlib.sha256((EDIT/'PICTURE_PLAN_v03b.json').read_bytes()).hexdigest(),self.plan['parent_plan_sha256'])
        self.assertFalse(self.plan['render_authorized'])
        self.assertFalse(self.plan['generation_authorized'])
        self.assertEqual(len(self.plan['rows']),self.plan['totals']['edit_beats'])


if __name__=='__main__': unittest.main()
