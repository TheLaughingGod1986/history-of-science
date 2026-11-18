import sys, json
sys.path.insert(0, sys.argv[1])
from normalization_proposal import normalize_overage as n, EvidenceRefused
def t(label, p, s):
    try: print('ACCEPT', label, n(p, source=s))
    except EvidenceRefused as e: print('REFUSE', label, '->', e)
    except Exception as e: print('CRASH ', label, type(e).__name__, e)
N=lambda a='0',c='usd':{'current_overage':{'amount':a,'currency':c}}
F=lambda a='0',c='usd':{'current_overage_amount':a,'current_overage_currency':c}
for a in ('0.0','0.000000000000000000000000','0.00000000000000000001','0,0','0_0','0x0','.0','0.0.0',' 0','0\x00','0\r',b'0',bytearray(b'0'),0j,float('nan')):
    t('raw amount %r'%(a,), N(a),'raw_api')
t('raw flat amount only + nested', N()|{'current_overage_amount':'0'},'raw_api')
t('raw flat currency only + nested', N()|{'current_overage_currency':'usd'},'raw_api')
t('raw flat key null + nested', N()|{'current_overage_amount':None},'raw_api')
t('hist nested 0.00 + flat 0', N('0.00')|F(),'historical_provenance')
t('hist nested + flat 0.01', N()|F('0.01'),'historical_provenance')
t('hist nested + one flat key', N()|{'current_overage_currency':'usd'},'historical_provenance')
t('hist nested malformed + flat ok', {'current_overage':{'amount':'0'}}|F(),'historical_provenance')
t('hist nested extra field + flat ok', {'current_overage':{'amount':'0','currency':'usd','x':1}}|F(),'historical_provenance')
t('hist nested dict subclass', {'current_overage':type('D',(dict,),{})(amount='0',currency='usd')},'historical_provenance')
t('nested non-str key', {'current_overage':{'amount':'0','currency':'usd',1:2}},'raw_api')
t('currency bool', N(c=True),'raw_api')
t('currency " usd"', N(c=' usd'),'raw_api')
t('currency unhashable dict', N(c={}),'raw_api')
t('source "RAW_API"', N(),'RAW_API')
t('source ""', N(),'')
t('source unhashable', N(),{})
t('other fields ignored (extension true)', N()|{'can_extend_character_limit':True,'status':'past_due'},'raw_api')
for s in ('raw_api','historical_provenance'):
    r=n(N(),source=s); assert r['authorizes_generation'] is False and r['freshness_assessed'] is False
try: n(N())
except TypeError as e: print('source is required keyword:', e)
print('duplicate-rejecting loader demo:')
def nodup(pairs):
    d={}
    for k,v in pairs:
        if k in d: raise ValueError('duplicate key '+k)
        d[k]=v
    return d
for body in ('{"current_overage":{"amount":"5","currency":"usd"},"current_overage":{"amount":"0","currency":"usd"}}','{"current_overage":{"amount":"5","amount":"0","currency":"usd"}}'):
    try: json.loads(body, object_pairs_hook=nodup); print(' loaded')
    except ValueError as e: print(' refused:', e)
