import sys, json
sys.path.insert(0, sys.argv[1])
from normalization_proposal import normalize_overage as n, EvidenceRefused
def t(label, p, s):
    try: print('ACCEPT', label, n(p, source=s))
    except EvidenceRefused as e: print('REFUSE', label, '->', e)
    except Exception as e: print('CRASH ', label, type(e).__name__, e)
N=lambda a='0',c='usd':{'current_overage':{'amount':a,'currency':c}}
F=lambda a='0',c='usd':{'current_overage_amount':a,'current_overage_currency':c}
t('raw nested int 0', N(0),'raw_api')
t('raw nested "00"', N('00'),'raw_api')
t('raw nested "000.000"', N('000.000'),'raw_api')
t('raw nested "0\\n"', N('0\n'),'raw_api')
t('raw nested fullwidth zero', N('０'),'raw_api')
t('raw nested arabic zero', N('٠'),'raw_api')
t('raw nested "+0"', N('+0'),'raw_api')
t('raw nested "0."', N('0.'),'raw_api')
t('raw nested huge int', N(10**400),'raw_api')
t('raw nested + flat (derived keys in "raw")', N()|F(),'raw_api')
t('raw nested gbp', N(c='gbp'),'raw_api')
t('hist nested only', N(),'historical_provenance')
t('hist flat only', F(),'historical_provenance')
t('hist flat int', F(0),'historical_provenance')
t('hist both differing currency', N()|F(c='eur'),'historical_provenance')
t('hist flat null currency', F(c=None),'historical_provenance')
t('hist empty', {},'historical_provenance')
t('source None', N(),None)
t('source list', N(),['raw_api'])
t('source bytes', N(),b'raw_api')
t('currency list', N(c=['usd']),'raw_api')
t('amount str subclass', N(type('S',(str,),{})('0')),'raw_api')
t('payload dict subclass', type('D',(dict,),{})(N()),'raw_api')
t('stale payload relabelled raw', N(),'raw_api')
dup='{"current_overage":{"amount":"5","currency":"usd"},"current_overage":{"amount":"0","currency":"usd"}}'
t('json duplicate key (5 then 0)', json.loads(dup),'raw_api')
dup2='{"current_overage":{"amount":"5","amount":"0","currency":"usd"}}'
t('json duplicate nested amount (5 then 0)', json.loads(dup2),'raw_api')
t('error envelope', {'detail':{'status':'x'}},'raw_api')
t('wrapped under subscription', {'subscription':N()},'raw_api')
