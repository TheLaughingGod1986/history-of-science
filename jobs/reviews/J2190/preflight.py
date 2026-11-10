#!/usr/bin/env python3
"""J2190 offline request/guard preflight. Deliberately has NO submission path.

A later explicit priced scope must implement submission under the canonical
vertex desk lock, reserve globally before the call, record uncertain failures,
and never retry automatically. This module cannot authorise or spend credit.
"""
import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from decimal import Decimal, ROUND_CEILING
from pathlib import Path

PROJECT = 'gen-lang-client-0538779324'
REGION = 'us-central1'
MODEL = 'veo-3.1-generate-001'
ACCOUNT = '0124D1-E6EFD6-40F6DA'
INPUTS = ('Short_B S02', 'Short_B S06', 'Short_C S01', 'Short_C S06', 'Short_C S07', 'Short_C S08')
CONFIG = dict(number_of_videos=1, duration_seconds=8, resolution='1080p', aspect_ratio='9:16', generate_audio=False)

class Stop(ValueError):
    pass

def money(v):
    try:
        d = Decimal(str(v))
        if not d.is_finite() or d < 0:
            raise ValueError()
        return d
    except Exception as exc:
        raise Stop('unknown/invalid nonnegative money') from exc

def stamp(v):
    try:
        d = datetime.fromisoformat(v.replace('Z', '+00:00'))
        if d.utcoffset() is None:
            raise ValueError()
        return d
    except Exception as exc:
        raise Stop('unknown/invalid timestamp') from exc

def digest(v):
    return hashlib.sha256(json.dumps(v, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def fresh(row, now):
    if not 0 <= (now - stamp(row['at'])).total_seconds() <= 300:
        raise Stop('evidence stale or future')

def check_lock():
    """Later producer must call while canonical desk-lock wrapper owns the lock."""
    canonical = Path.home() / '_desk/locks/vertex.lock'
    held = Path(os.environ.get('DESK_LOCK_HELD_DIR','/nonexistent'))
    if held.resolve() != canonical.resolve():
        raise Stop('canonical vertex desk-lock required')
    try:
        owner = dict(x.split('=',1) for x in (held/'owner.txt').read_text().splitlines() if '=' in x)
        pid = int(owner['pid'])
        if pid not in (os.getpid(),os.getppid()):
            raise Stop('vertex desk-lock belongs to another process')
        os.kill(pid,0)
    except (OSError,KeyError,ValueError) as exc:
        raise Stop('live owned vertex desk-lock required') from exc


def requests(briefs, version):
    if not version.startswith('v') or not version[1:].isdigit() or int(version[1:]) < 1:
        raise Stop('unique numeric version required')
    rows = briefs['briefs']
    if len(rows) != 6 or set(r['input'] for r in rows) != set(INPUTS):
        raise Stop('exact six distinct inputs required')
    result = []
    for name in INPUTS:
        row = next(r for r in rows if r['input'] == name)
        if row['duration_setting_s'] != 8 or row['outputs'] != 1 or not row['prompt'].strip():
            raise Stop('brief does not match fixed route')
        for take in (1, 2):
            req = dict(project=PROJECT, location=REGION, model=MODEL,
                       source={'prompt': row['prompt']}, config=dict(CONFIG))
            result.append(dict(input=name, take=take, request=req, request_sha256=digest(req),
                identity=f'J2190:{name}:t{take}',
                output=f'04_Generated-Clips/shorts_J2190/{version}/{name.replace(" ", "_")}_t{take}.mp4',
                operation=None, output_sha256=None, status='PREPARATION_ONLY'))
    return result

def assess(e, ledger, now=None):
    """Fail closed. All-project liability needs authoritative evidence, not age.

    usage.cutoff is a proved settlement boundary, NOT latest balance timestamp.
    Explicit upper_bounds must cover every unknown row by canonical row hash;
    unlogged_upper_bound covers otherwise absent usage across all projects.
    Pending reservations remain liabilities irrespective of the cutoff.
    """
    try:
        return _assess(e, ledger, now or datetime.now(timezone.utc))
    except Stop:
        raise
    except (KeyError, ValueError, TypeError, ArithmeticError) as exc:
        raise Stop('missing/malformed evidence or ledger') from exc

def _assess(e, ledger, now):
    for key in ('credits', 'price', 'usage', 'link'):
        fresh(e[key], now)
    c,p,u,l = (e[k] for k in ('credits','price','usage','link'))
    if (l['project'],l['account'],l['enabled']) != (PROJECT,ACCOUNT,True):
        raise Stop('billing linkage unresolved')
    if c['account'] != ACCOUNT or c['vertex_eligible'] is not True or not c['source']:
        raise Stop('monthly entitlement unresolved')
    active = [r for r in c['rows'] if r['status'] == 'Available']
    if not active or len({r['id'] for r in active}) != len(active):
        raise Stop('unknown or duplicated Available credits')
    if any(r['currency'] != 'GBP' or not r['eligible'] for r in active):
        raise Stop('unknown promo currency/eligibility')
    available = sum((money(r['remaining']) for r in active), Decimal(0))
    if not any(r['type']=='CREDIT_TYPE_MONTHLY' for r in active):
        raise Stop('live monthly entitlement missing')
    if (p['model'],p['region'],p['resolution'],p['audio'],p['currency'],p['unit']) != (MODEL,REGION,'1080p',False,'GBP','second'):
        raise Stop('current exact GBP price/unit unresolved')
    if not p['sku'] or not p['source'].startswith(('https://cloud.google.com/','https://console.cloud.google.com/')):
        raise Stop('official GBP SKU source missing')
    rate = money(p['rate'])
    if rate <= 0:
        raise Stop('positive GBP price required')
    per_take = (rate * 8).quantize(Decimal('.01'), rounding=ROUND_CEILING)
    # All twelve potential takes are budgeted, never implicitly authorised.
    full = per_take * 12
    if full > money(e['proposed_cap_gbp']):
        raise Stop('full twelve-take estimate exceeds proposed cap')
    cutoff = stamp(u['cutoff'])
    if cutoff > min(stamp(u['at']),stamp(c['at'])) or u['all_projects_checked'] is not True or not u['source']:
        raise Stop('global pending-charge coverage unresolved')
    pending = money(u['unlogged_upper_bound_gbp'])
    seen = set()
    takes = {}
    for r in ledger:
        if r.get('pool') != 'vertex':
            continue
        kind = r['kind']
        if kind == 'record':
            continue
        if kind not in ('spend','reserve','take_started'):
            raise Stop('unknown Vertex event')
        if r.get('job') == 'J2190':
            identity = r['identity']
            if identity in seen:
                raise Stop('repeated request identity')
            seen.add(identity)
            name,take = r['input'],r['take']
            if name not in INPUTS or type(take) is not int or take not in (1,2):
                raise Stop('unscoped input/take')
            takes.setdefault(name,set()).add(take)
            # Existing requests must be reconciled before preparing a fresh full batch.
            raise Stop('prior J2190 request/reservation exists; reconcile, never replay')
        when = stamp(r['at'])
        if kind in ('reserve','take_started') or when >= cutoff:
            h = digest(r)
            bound = u.get('upper_bounds_gbp',{}).get(h)
            if kind != 'spend' or 'amount' not in r or money(r['amount']) == 0:
                if bound is None:
                    raise Stop('unpriced/pending Vertex event without proved bound')
                pending += money(bound)
            else:
                pending += money(r['amount'])
    if available-pending-full < Decimal(5):
        raise Stop('GBP5 floor would be breached')
    return dict(available_gbp=str(available), pending_gbp=str(pending), per_take_gbp=str(per_take),
                twelve_take_estimate_gbp=str(full), after_gbp=str(available-pending-full),
                ledger_sha256=digest(ledger), spend_authorised=False)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--briefs',type=Path,required=True)
    ap.add_argument('--version',required=True)
    ap.add_argument('--evidence',type=Path)
    ap.add_argument('--ledger',type=Path)
    ap.add_argument('--require-lock',action='store_true')
    ap.add_argument('--output-root',type=Path)
    a=ap.parse_args()
    if a.require_lock:
        check_lock()
    plan=requests(json.loads(a.briefs.read_text()),a.version)
    if a.output_root and any((a.output_root/r['output']).exists() for r in plan):
        raise Stop('output version already exists; never overwrite')
    out={'mode':'NO_NETWORK_DRY_RUN','spend_authorised':False,'requests':plan}
    if a.evidence or a.ledger:
        if not (a.evidence and a.ledger):
            ap.error('evidence and global ledger required together')
        raw=a.ledger.read_text()
        if raw and not raw.endswith('\n'):
            raise Stop('incomplete global ledger')
        out['guard']=assess(json.loads(a.evidence.read_text()),[json.loads(x) for x in raw.splitlines() if x.strip()])
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    main()
