"""One-job evidence audit; --apply calls only the existing runner accounting API."""
import sys, json, hashlib, importlib.util
from pathlib import Path
from datetime import datetime
ROOT=Path('/Users/benjaminoats/YouTube/orbit-with-ben')
ACCOUNT=Path('/Users/benjaminoats/_desk/state/flow/shared/account.jsonl')
SPEND=ROOT/'05_Analytics/ai_spend/ledger.jsonl'
RUNNER=Path('/Volumes/MiniWork/scratch/J2642-hos/02_Video-Projects/013_Darwin-Wallace-Evolution/07_Edit-Project/_mint_flow_v01_pass1.py')
spec=importlib.util.spec_from_file_location('runner',RUNNER); mod=importlib.util.module_from_spec(spec); sys.modules['runner']=mod; spec.loader.exec_module(mod)
def dt(s): return datetime.fromisoformat(s.replace('Z','+00:00'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def clean(e): return {k:v for k,v in e.items() if k!='evidence'}
spend=[dict(json.loads(l),line=n) for n,l in enumerate(SPEND.read_text().splitlines(),1)]
reads=sorted([e for e in spend if e.get('pool')=='flow' and e.get('kind')=='record' and ('Configured UI before Create' in e.get('note','') or e.get('by')=='mini-daily')],key=lambda e:dt(e['at']))
with mod.SharedFlowAccounting(ACCOUNT.parent) as account:
 before=account.snapshot(); original=[json.loads(l) for l in ACCOUNT.read_text().splitlines()]; out=[]
 for key,c in before['charges'].items():
  if not key.startswith(('HOS:008:','HOS:009:')) or c['posted'] or c['status']!='CHARGED': continue
  charge=next(e for e in original if e['kind']=='charged' and e['id']==key)
  r=next(e for e in reads if e.get('charge')==key)
  nxt=next(e for e in reads if dt(e['at'])>dt(r['at']) and e.get('charge')!=key)
  between=[clean(e) for e in original if dt(charge['at'])<dt(e['at'])<=dt(nxt['at']) and e['kind'] in ('reserve','release','charged','policy_refused','refund','reversal') and not(e['kind']=='charged' and e['id']==nxt.get('charge'))]
  ev={'before':r['left'],'after':nxt['left'],'before_read_at':r['at'],'after_read_at':nxt['at'],'source':str(SPEND),'before_line':r['line'],'after_line':nxt['line'],'next_charge':nxt.get('charge'),'intervening_events':between,'authority':'HOS desk 6806439304 / 6806623496; J2642'}
  ok=r['left']-nxt['left']==100 and not between and charge['evidence']['ui']['balances']==[r['left']] and dt(nxt['at'])>dt(r['at'])
  reason='qualifies' if ok else ('unchanged balance; existing reversal API is policy-refusal only, not a generic failed-take refund' if 'rods_spread:J2241:t1' in key else 'test 2: intervening ledger events' if between else 'test 1: delta is not 100')
  if ok and '--apply' in sys.argv: account.reconcile_posted(key,evidence=ev)
  out.append(dict(charge_id=key,eligible=ok,posted=ok and '--apply' in sys.argv,reason=reason,**ev))
 after=account.snapshot()
 result={'apply':'--apply' in sys.argv,'unposted_before':before['unposted'],'unposted_after':after['unposted'],'liability_after':after['liability'],'account_sha256_after':sha(ACCOUNT),'spend_sha256':sha(SPEND),'runner_sha256':sha(RUNNER),'charges':out,'clay_account_events':[clean(e) for e in original if dt('2026-11-11T15:19:39Z')<=dt(e['at'])<=dt('2026-11-11T15:31:18Z')],'clay_spend_events':[e for e in spend if dt('2026-11-11T15:19:39Z')<=dt(e['at'])<=dt('2026-11-11T15:31:18Z')]}
 Path(__file__).with_name('CHAINED_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ('charges','clay_account_events','clay_spend_events')})); print('eligible',sum(e['eligible'] for e in out)); print([(e['charge_id'],e['reason']) for e in out if not e['eligible']])
