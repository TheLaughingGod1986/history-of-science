import importlib.util,json,pathlib,tempfile,unittest,urllib.error
from unittest.mock import patch
HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('prepare',HERE/'prepare_assembly_v01.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class AssemblySourceChecks(unittest.TestCase):
 def test_scope_and_source_precedence(self):
  m=mod.manifest();assets={x['asset_id']:x for x in m['assets']}
  self.assertEqual(len(assets),23);self.assertEqual(len(m['rows']),93)
  self.assertEqual(sum(r['build_type']=='dependency_slate' for r in m['rows']),67)
  for k,identity in [('archive_P1_09b','L0041135'),('portrait_P2_02a','V0006497'),('portrait_P2_07a','M0003193'),('archive_P3_05b','L0018234'),('archive_P3_09a_arch_ether_dome_1847','Google_Art_Project')]:self.assertIn(identity,assets[k]['page_url'])
  self.assertFalse(m['generation_authorized']);self.assertIn('L0058154',assets['archive_P5_07a_arch_snow_chloroform_1858']['alternate_url'])
 def test_rate_limit_stops_all_later_requests(self):
  with tempfile.TemporaryDirectory() as td:
   p=pathlib.Path(td);m=mod.manifest()
   with patch.object(mod.urllib.request,'urlopen',side_effect=urllib.error.HTTPError('url',429,'rate limit',{},None)) as request:
    mod.fetch(m,p)
   self.assertEqual(request.call_count,1);self.assertIn('429',m['network_hold']);self.assertEqual(m['assets'][1]['status'],'not_fetched')
 def test_candidates_match_actual_word_indices(self):
  c=json.loads((HERE/'OVERLAY_CANDIDATES_v01.json').read_text());p=json.loads((HERE/'PICTURE_PLAN_v03.json').read_text());raw=json.loads((HERE.parent/p['vo_lock']['stt_raw']).read_text());words=[w for w in raw['words'] if w['type']=='word']
  for cue in c['candidates']:
   self.assertEqual(cue['in_s'],words[cue['word_indices'][0]]['start']);self.assertEqual(cue['anchor_text'],' '.join(words[i]['text'] for i in cue['word_indices']))
   self.assertEqual(cue['anchor_text'],' '.join(raw['words'][i]['text'] for i in cue['raw_stt_indices']))
  for a,b in zip(c['candidates'],c['candidates'][1:]):self.assertLessEqual(a['out_s'],b['in_s'])
  self.assertFalse(c['checks']['film_stage_pass']);self.assertGreater(len(c['held']),0)
if __name__=='__main__':unittest.main()
