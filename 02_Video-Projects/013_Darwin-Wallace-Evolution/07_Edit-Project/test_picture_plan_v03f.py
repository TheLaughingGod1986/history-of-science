"""Independent interval, source and cue checks for the sentence revision."""
import hashlib
import json
import unittest
from test_picture_plan_v03d import Retiming as PreviousChecks, EDIT


class SentenceRevision(PreviousChecks):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.plan=json.loads((EDIT/'PICTURE_PLAN_v03f.json').read_text())

    def test_no_flash_beats_and_paint_matches_analogy(self):
        for row in self.plan['rows']:
            if 'card' not in row['id']:
                self.assertGreaterEqual(row['use_s'],2.5-1e-7)
        rows={r['id']:r for r in self.plan['rows']}
        paint=rows['02b_paint_pots_mix']
        self.assertEqual((paint['t_s'],paint['t_end_s']),(453.,458.14))
        self.assertIn('blended',paint['vo_land'][0])
        self.assertIn('mixing paint',paint['vo_land'][0])
        self.assertEqual(rows['06_padlock_shut']['t_end_s'],32.70)
        self.assertEqual(rows['01_card_p02']['t_end_s'],81.22)

    def test_inputs_and_no_authorization(self):
        for name,digest in self.plan['source_v02_sha256'].items():
            self.assertEqual(hashlib.sha256((EDIT/name).read_bytes()).hexdigest(),digest)
        self.assertEqual(hashlib.sha256((EDIT/'PICTURE_PLAN_v03d.json').read_bytes()).hexdigest(),self.plan['parent_plan_sha256'])
        self.assertFalse(self.plan['render_authorized'])
        self.assertFalse(self.plan['generation_authorized'])
        self.assertEqual(len(self.plan['rows']),self.plan['totals']['edit_beats'])

    def test_sentence_preference_independently(self):
        unresolved=[]
        for row in self.plan['rows'][:-1]:
            sentences=[q for q in self.qualified if (q.get('script') or {}).get('token','').rstrip('\"”’\'').endswith(('.', '?', '!'))]
            fitting=[q for q in sentences if max(q['start_s'],row['t_s']+3)<=min(q['end_s'],row['t_s']+7)]
            is_sentence=any(q['start_s']-1e-7<=row['t_end_s']<=q['end_s']+1e-7 for q in sentences)
            if fitting and not is_sentence:
                unresolved.append(row['id'])
        self.assertEqual(unresolved,['01_study_beaks'])


# Do not execute the imported base class twice in this module.
del PreviousChecks
if __name__=='__main__': unittest.main()
