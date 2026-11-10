#!/usr/bin/env python3
"""Chief-directed J0184 price proposal. No API calls; never authorizes minting."""
import json
import math
from pathlib import Path

EDIT = Path(__file__).resolve().parent
# Draft hero selection: title opening, Shorts covers, pivotal physical proof,
# and the two character beats. Chief reviews this list; it is not a KEEP decision.
HEROES = {
    'P1:01_kite_open': 'Long title opening',
    'P1:13_ring_the_bells': 'Short B cover',
    'P1:17_globe_spark': 'Bench electricity proof and later callback',
    'P2:08_jar_spark': 'Leyden jar discharge proof',
    'P2:13_explorer_jar': 'Explorer hero beat',
    'P3:06_marly_spark': 'First physical lightning proof',
    'P3:19_kite_climb': 'Short A cover',
    'P3:25_fibres_rise': 'First visible charge evidence',
    'P4:02_knuckle_spark': 'Kite experiment proof',
    'P4:04_fill_the_jar': 'Stored lightning proof',
    'P4:05_jar_spark_field': 'Stored-charge discharge proof',
    'P4:09_charge_string': 'Core charge mechanism',
    'P5:14_safe_towers': 'Lightning rod protection proof',
    'P5:16_explorer_rooftop': 'Explorer hero beat',
    'P5:19_skyline_strike': 'Short C cover / modern title payoff',
}
PRICE_FIELDS = ('flow_credits_try1','flow_credits_expected','vertex_try1_gbp','vertex_expected_gbp')
source_plan = json.loads((EDIT/'PICTURE_PLAN_v01.json').read_text())
rates = source_plan['rates']
boards = []
rows = {}
for path in sorted((EDIT/'parts').glob('part-??_plates_v01.json')):
    board = json.loads(path.read_text())
    n = int(board['part'])
    for row in board['plates']:
        key = f"P{n}:{row['id']}"
        row['v01_quality'] = row['quality']
        row['generation_authorized'] = False
        row['review_required'] = []
        if row.get('added'):
            source = row['id'].rsplit('_c',1)[0]
            row.update(quality='reuse',reuse_of=f'P{n}:{source}',route='reuse',
                       engine_reason='Chief 12 Oct: continuation hold becomes reuse, no new mint.',
                       reuse_window='TBD: unused moving KEEP frames only; no loop, freeze or replay',
                       reuse_feasibility='unverified until source KEEP is measured')
            for field in ('prompt','i2v_from','flow_model','flow_clip_s','vertex_model','clip_in_s'):
                row.pop(field,None)
            row['review_required'].append('An 8 s source may not contain enough unused motion for both windows. If it does not, select a distinct compatible KEEP cutaway and reprice any longer source; do not replay frames.')
        elif row['quality'] != 'reuse':
            if key in HEROES:
                row.update(quality='Quality',hero_reason=HEROES[key],engine_reason='Quality: proposed hero/cover plate; Chief price review required.')
            else:
                row.update(quality='Fast',engine_reason='Chief 12 Oct: non-hero plate proposed as Fast.')
                if row['v01_quality']=='Quality':
                    row['review_required'].append('Prompt/framing review required before Fast generation: preserve the spoken subject, remove fragile light from garnish or substitute a reviewed compatible KEEP. Never run Fast on fragile light. Price assumes an eligible Fast prompt, not the unchanged v01 prompt.')
            if 'parchment' in row.get('prompt','').lower() or 'diagram' in row.get('prompt','').lower() or 'Split frame:' in row.get('prompt',''):
                row['review_required'].append('Existing explanatory image requires own per-row code graphic/overlay treatment, not a generated flat card; review separately. Current video price is conservative, not permission to mint this prompt.')
        rows[key]=row
    board.update(status='BOARD_V02_PRICE_PROPOSAL',mint=False,
                 quality_note='Chief 12 Oct revision: Quality only for proposed hero/cover plates. Fast remains forbidden on fragile light; flagged prompts are not generation-ready.',
                 house='J0184 v02 price proposal by codex, 14 Oct 2026, applying Chief FIX on PR #296. Timing, VO text, reference and original prompts retained for review. No mint; no final OK or PASS.',
                 continuation_lock='Continuation holds are proposed reuses. Select unused moving KEEP frames or a distinct compatible cutaway; never loop, freeze-pad or replay. No reuse is assumed feasible without measuring its source.')
    boards.append(board)

# Keep source clip lengths from v01: longer unused windows might require a
# revised source/route, which remains an explicit uncertainty in this proposal.
cum_flow=0;cum_vertex=0
per_part=[]
for board in boards:
    for row in board['plates']:
        if row['quality']=='reuse':
            row.update({field:0 for field in PRICE_FIELDS})
            row.update(vertex_clip_s=0,route='reuse')
        else:
            q=row['quality'];clip=row['vertex_clip_s']
            cost=rates['vertex_usd_per_s'][q]*clip*rates['gbp_per_usd_planning']
            expected=cost*rates['takes_per_keep_005'][q]+rates['stills_per_plate_005']*rates['usd_per_still']*rates['gbp_per_usd_planning']
            row.update(flow_model=f'Veo 3.1 {q}',vertex_model='veo-3.1-generate-001' if q=='Quality' else 'veo-3.1-fast-generate-001',
                       flow_credits_try1=rates['flow_credits_per_take'][q],
                       flow_credits_expected=math.ceil(rates['flow_credits_per_take'][q]*rates['takes_per_keep_005'][q]),
                       vertex_try1_gbp=round(cost,2),vertex_expected_gbp=round(expected,2))
        cum_flow+=row['flow_credits_expected'];cum_vertex+=row['vertex_expected_gbp']
        row.update(cum_flow_credits_expected=cum_flow,cum_vertex_expected_gbp=round(cum_vertex,2))
    plate_rows=board['plates']
    counts={q:sum(r['quality']==q for r in plate_rows) for q in ('Quality','Fast','reuse')}
    board['counts']=dict(rows=len(plate_rows),mints=counts['Quality']+counts['Fast'],added=sum(bool(r.get('added')) for r in plate_rows),**counts)
    pp=dict(part=int(board['part']),**board['counts'])
    pp.update({f:round(sum(r[f] for r in plate_rows),2) for f in PRICE_FIELDS})
    per_part.append(pp)
    (EDIT/'parts'/f"part-{board['part']}_plates_v02.json").write_text(json.dumps(board,indent=2,ensure_ascii=False)+'\n')
totals={k:round(sum(p[k] for p in per_part),2) for k in per_part[0] if k!='part'}
plan=dict(source_plan)
plan.update(written='2026-10-14',status='PARKED_FOR_CHIEF_PRICE_PASS',mint=False,
            readings_as_of='2026-10-12; historical planning inputs, not live spend authority',
            totals=totals,per_part=per_part,hero_candidates=HEROES,
            all_on_flow_credits_expected=totals['flow_credits_expected'],
            all_on_vertex_gbp_expected=totals['vertex_expected_gbp'],
            fits_now={'flow':None,'vertex':None},
            price_pass_questions=[
                'Chief reviews proposed hero/cover list and conditional Fast prices; flagged non-hero prompts cannot mint unchanged on Fast.',
                'Measure unused KEEP motion for all continuation reuses; no repeat, loop or freeze permitted. Distinct cutaways or longer sources may alter price.',
                'Own code-graphic treatment for inherited explainer/card prompts remains a shot-list review item.',
                'Flow/Vertex split waits for Ultra refill and live balance check. Historical 12 Oct balances are not a current credit reading.',
            ],
            changes={'continuations_to_reuse':sum(bool(r.get('added')) for r in rows.values()),
                     'quality_to_fast':sum(r['v01_quality']=='Quality' and r['quality']=='Fast' for r in rows.values())},
            estimate_scope='Conditional video estimate using unchanged v01 clip lengths and empirical take multipliers. Reuse availability and eligible Fast framing unverified; no spend authorization.')
(EDIT/'PICTURE_PLAN_v02.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'totals':totals,'changes':plan['changes']},indent=2))
