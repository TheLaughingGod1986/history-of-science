import copy,json,socket,unittest
from datetime import datetime,timezone,timedelta
from pathlib import Path
from unittest.mock import patch
import preflight as p
NOW=datetime(2026,11,5,8,tzinfo=timezone.utc)
AT=NOW.isoformat()
def evidence():
 return dict(credits=dict(at=AT,account=p.ACCOUNT,vertex_eligible=True,source='fixture',rows=[dict(id='monthly',status='Available',currency='GBP',eligible=True,type='CREDIT_TYPE_MONTHLY',remaining='69.48')]),
 price=dict(at=AT,model=p.MODEL,region=p.REGION,resolution='1080p',audio=False,currency='GBP',unit='second',rate='.20',sku='fixture-only',source='https://console.cloud.google.com/fixture'),
 usage=dict(at=AT,cutoff='2026-01-01T00:00:00Z',all_projects_checked=True,source='fixture-only',unlogged_upper_bound_gbp='0'),
 link=dict(at=AT,project=p.PROJECT,account=p.ACCOUNT,enabled=True),proposed_cap_gbp='20')
class GuardTests(unittest.TestCase):
 def setUp(self): self.e=evidence()
 def reject(self,rows=[]):
  with self.assertRaises(p.Stop): p.assess(self.e,rows,NOW)
 def test_budget(self): self.assertEqual(p.assess(self.e,[],NOW)['twelve_take_estimate_gbp'],'19.20')
 def test_unknown_credit(self): self.e['credits']['rows']=[];self.reject()
 def test_stale(self): self.e['credits']['at']=(NOW-timedelta(seconds=301)).isoformat();self.reject()
 def test_future(self): self.e['price']['at']=(NOW+timedelta(seconds=1)).isoformat();self.reject()
 def test_nonfinite(self): self.e['price']['rate']='NaN';self.reject()
 def test_wrong_unit(self): self.e['price']['unit']='count';self.reject()
 def test_wrong_model(self): self.e['price']['model']='veo-3.1-fast-generate-001';self.reject()
 def test_cap(self): self.e['proposed_cap_gbp']='19';self.reject()
 def test_floor(self): self.e['credits']['rows'][0]['remaining']='24';self.reject()
 def test_unpriced_historic(self): self.reject([dict(pool='vertex',kind='spend',at='2026-02-01T00:00:00Z',amount=0)])
 def test_pending(self): self.reject([dict(pool='vertex',kind='take_started',at=AT)])
 def test_bound(self):
  r=dict(pool='vertex',kind='spend',at=AT,amount=0)
  self.e['usage']['upper_bounds_gbp']={p.digest(r):'3'}
  self.assertEqual(p.assess(self.e,[r],NOW)['pending_gbp'],'3')
 def test_global(self):
  r=dict(pool='vertex',kind='spend',at=AT,amount=2,film='OWB:032')
  self.assertEqual(p.assess(self.e,[r],NOW)['pending_gbp'],'2')
 def test_replay(self): self.reject([dict(pool='vertex',kind='reserve',job='J2190',identity='J2190:Short_B S02:t1',input='Short_B S02',take=1,at=AT,amount=1)])
 def test_take_limit(self): self.reject([dict(pool='vertex',kind='reserve',job='J2190',identity='third',input='Short_B S02',take=3,at=AT,amount=1)])
 def test_cutoff(self): self.e['usage']['cutoff']='2027-01-01T00:00:00Z';self.reject()
 def test_no_network_no_writes(self):
  briefs=json.loads(Path(__file__).with_name('SIX_INPUT_BRIEFS.json').read_text())
  with patch.object(socket,'socket',side_effect=AssertionError('network')),patch.object(Path,'write_text',side_effect=AssertionError('write')):
   rows=p.requests(briefs,'v01');p.assess(self.e,[],NOW)
  self.assertEqual(len(rows),12)
  self.assertEqual(len({r['output'] for r in rows}),12)
  self.assertTrue(all(r['request']['config']==p.CONFIG and set(r['request']['source'])=={'prompt'} for r in rows))
 def test_lock_absent(self):
  with patch.dict('os.environ',{},clear=True):
   with self.assertRaises(p.Stop):p.check_lock()
 def test_duplicate_brief(self):
  b=json.loads(Path(__file__).with_name('SIX_INPUT_BRIEFS.json').read_text());b['briefs'][0]=b['briefs'][1]
  with self.assertRaises(p.Stop):p.requests(b,'v01')
if __name__=='__main__':unittest.main()
