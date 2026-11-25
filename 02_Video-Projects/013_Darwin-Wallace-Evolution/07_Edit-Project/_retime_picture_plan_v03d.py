#!/usr/bin/env python3
"""Evidence-only timing allocation; never changes existing plans or audio."""
import copy
import csv
import hashlib
import json
import math
from pathlib import Path

EDIT = Path(__file__).resolve().parent
OUT = EDIT / 'timing_rough_J2652'


def solve(rows, qualified, cues):
    points = {0.0: {'kind': 'start'}, 515.0: {'kind': 'end'}}
    for q in qualified:
        token = (q.get('script') or {}).get('token', '')
        sentence = token.rstrip('\"”’\'').endswith(('.', '?', '!'))
        for tick in range(math.ceil((q['start_s']-1e-7)*50), math.floor((q['end_s']+1e-7)*50)+1):
            t = round(tick/50, 2)
            points[t] = dict(kind='sentence' if sentence else 'qualified_gap', **q)
    # State includes the start of the current source, so native footage length
    # is constrained across all beats rather than forgotten at each cut.
    states = {(0., 0.): (0., [])}
    for i, row in enumerate(rows):
        chapter = '_card_p' in row['id']
        endcard = 'cream_end_card' in row['id']
        next_chapter = i+1 < len(rows) and '_card_p' in rows[i+1]['id']
        same = i > 0 and rows[i-1]['source_row_v02'] == row['source_row_v02']
        ends = [515.] if i == len(rows)-1 else sorted(t for t in points if abs(t-row['t_end_s']) <= 6 and t < 515)
        if i == 0:
            ends = [t for t in ends if t <= 3.82]
        if row['id'] == '02b_paint_pots_mix':
            # Finish the paint analogy before the quantified beak mechanism.
            ends = [459.64]
        future = {}
        for (start, prev_group_start), (cost, path) in states.items():
            group_start = prev_group_start if same else start
            minimum = 2.0 if chapter or endcard else 2.5
            maximum = 4 if endcard else 7
            if row['source_kind'] == 'existing_plate_reuse':
                maximum = min(4.2, 8-path[0])
            feasible = [t for t in ends if minimum-1e-7 <= t-start <= maximum+1e-7]
            if i+1 < len(rows) and 'cream_end_card' in rows[i+1]['id']:
                feasible = [t for t in feasible if 512.74-1e-7 <= t <= 513.0]
            if next_chapter:
                feasible = [t for t in feasible if points[t]['kind']=='sentence'
                            and .5-1e-7 <= t-points[t]['start_s'] <= .8+1e-7]
            if chapter:
                # The title is one overlay, not the whole background shot.
                # Clear it before a mandatory WHO starts; the case-file scene
                # can continue beneath that independently timed portrait card.
                feasible = [t for t in feasible if t-start >= 2.5-1e-7 and not any(start < c['display_end_s']-1e-7 and start+2.5 > c['display_start_s']+1e-7 for c in cues)]
            if row['source_kind']=='new_mint_quality':
                feasible = [t for t in feasible if t-group_start <= 8+1e-7]
            sentences = [t for t in feasible if points[t]['kind']=='sentence' and 3 <= t-start <= 7]
            for end in feasible:
                score = cost + (end-row['t_end_s'])**2 + .1*(end-start-5)**2
                if sentences and end not in sentences and not chapter and not endcard:
                    score += 100
                if chapter and end-start < 2:
                    score += 300
                key = (end, group_start)
                if key not in future or score < future[key][0]:
                    future[key] = (score, path+[end])
        if not future:
            raise ValueError(f'No feasible path at {i}: {row["source_row_v02"]}; prior ends {sorted({k[0] for k in states})}; constraints remain in force')
        states = future
    return min(states.values(), key=lambda v:v[0])[1], points


def main():
    source = EDIT/'PICTURE_PLAN_v03b.json'
    plan = json.loads(source.read_text())
    # Drop redundant views rather than inventing punctuation to keep them.
    dropped = {'04a_packet_seal', '04b_drawer_unlock', '09_wallace_hut_split_beat2', '13a_lyell_warning', '10_darwin_worried_shelf_beat2', '03_unlabelled_bagging_beat2'}
    rows = [copy.deepcopy(r) for r in plan['rows'] if r['id'] not in dropped]
    # Extend the joint-reading archive coverage through the actual spoken
    # reading/extracts; two distinct compositions, no stretched footage.
    idx=next(i for i,r in enumerate(rows) if r['id']=='02b_joint_papers_lectern')
    second=copy.deepcopy(rows[idx])
    rows[idx]['id'] += '_wide'
    rows[idx]['t_end_s']=376.64
    second['id'] += '_detail'
    rows.insert(idx+1,second)
    for r in (rows[idx],rows[idx+1]):
        r['render_requirement']='New distinct archive composition for this beat; wide context then portrait detail, no repeated frames or length stretch.'
    qualified = json.loads((OUT/'qualified_boundaries_v03b.json').read_text())
    # The restrictive relative clause ends before the main verb "stumble".
    # This is syntax evidence allowed by ruling 6808560760, NOT a measured
    # breath, a 120 ms pause, or added punctuation in the locked script.
    qualified.append(dict(start_s=71.22, end_s=71.22, word_index=173,
        gap_s=0.0, script=None, measured_pause=None,
        editorial_clause=dict(kind='relative_clause_end',
            exact_clause="who didn't even label his birds properly",
            next_word='stumble',
            source='01_Script/darwin_script_master_v02.md:26',
            reason='End of the relative clause modifying young man; resumes main predicate stumble.')))
    qualified.sort(key=lambda q:q['start_s'])
    (OUT/'qualified_boundaries_v03d.json').write_text(json.dumps(qualified,indent=2)+'\n')
    ends, points = solve(rows, qualified, plan['overlay_cues'])
    start=0.
    for row,end in zip(rows,ends):
        row.update(t_s=start,t_end_s=end,use_s=round(end-start,2),cut_out_evidence=points[end])
        row.pop('word_onsets',None)
        start=end
    for cue in plan['overlay_cues']:
        host=next(r for r in rows if r['t_s'] <= cue['display_start_s'] < r['t_end_s'])
        cue['display_host_row']=f'P{host["part"]}:{host["id"]}'
        cue['host_row']=cue['display_host_row']
        cue['offset_in_host_s']=round(cue['onset_s']-host['t_s'],3)
        host.setdefault('word_onsets',[]).append(copy.deepcopy(cue))
    words=json.loads((EDIT.parent/'02_Voiceover/stt/hos_013_vo_v03a/words_fw_small_en.json').read_text())['words']
    groups={}
    for r in rows:
        group=groups.setdefault(r['source_row_v02'],[]);group.append(r)
        r['source_window_s']=[round(r['t_s']-group[0]['t_s'],2),round(r['t_end_s']-group[0]['t_s'],2)]
        r['vo_land']=[''.join(w['word'] for w in words if r['t_s']<=w['start']<r['t_end_s']).strip()]
        r['t']=f'{int(r["t_s"]//60)}:{r["t_s"]%60:05.2f}'
        r['t_end']=f'{int(r["t_end_s"]//60)}:{r["t_end_s"]%60:05.2f}'
        part_start=next(x['t_s'] for x in rows if x['part']==r['part'])
        r['local_s']=round(r['t_s']-part_start,2)
        if r['source_kind']=='existing_plate_reuse':
            r['source_window_s']=[ends[0],round(ends[0]+r['use_s'],2)]
    chapters=[dict(row=r['source_row_v02'],start_s=r['t_s'],end_s=r['t_end_s'],duration_s=r['use_s'],title_start_s=r['t_s'],title_end_s=round(r['t_s']+2.5,2)) for r in rows if '_card_p' in r['id']]
    for r in rows:
        if '_card_p' in r['id']:
            r['chapter_title_window_s']=[r['t_s'],round(r['t_s']+2.5,2)]
            r['render_requirement']='Case-file desk moving background; title fades in/out within the explicit 2.5-second window, then clears before any WHO. Never bake a title into the background.'
    unsupported=[r['id'] for r in rows[:-1] if not any(q['start_s']-1e-7<=r['t_end_s']<=q['end_s']+1e-7 for q in qualified)]
    crossings=[r['id'] for r in rows[:-1] if any(w['start']+1e-7<r['t_end_s']<w['end']-1e-7 for w in words)]
    overruns=[k for k,g in groups.items() if g[0]['source_kind']=='new_mint_quality' and sum(r['use_s'] for r in g)>8+1e-7]
    assert not unsupported and not crossings and not overruns
    plan.update(version='v03d-timing-scope',rows=rows,parent_plan_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                removed_redundant_views=sorted(dropped),timing_status='Candidate: qualified cuts and source caps pass; chapter/render review outstanding',render_authorized=False)
    callback=next(r for r in rows if r['source_kind']=='existing_plate_reuse')
    plan['callback'].update(source_window_s=callback['source_window_s'],duration_s=callback['use_s'])
    plan['totals']=dict(edit_beats=len(rows),unique_source_rows=len(groups),new_generation_authorized=0)
    audit=dict(approved=False,unsupported_cuts=unsupported,in_word_cuts=crossings,native_source_overruns=overruns,
               row_count=len(rows),max_row_s=max(r['use_s'] for r in rows),chapters=chapters,
               short_chapters=[c for c in chapters if c['duration_s']<2],
               sentence_preference='Search preference, not a claim of independent editorial acceptance',
               source_caps='8-second planned Quality inputs; actual accepted source windows still require media checks',
               callback=next(r['source_window_s'] for r in rows if r['source_kind']=='existing_plate_reuse'))
    audit['brief_picture_beats']=[dict(row=r['id'],start_s=r['t_s'],duration_s=r['use_s']) for r in rows if r['use_s']<2]
    audit['chapter_title_cue_overlaps']=[dict(chapter=c['row'],cue=x['word']) for c in chapters for x in plan['overlay_cues']
        if c['title_start_s'] < x['display_end_s']-1e-7 and c['title_end_s'] > x['display_start_s']+1e-7]
    assert not audit['chapter_title_cue_overlaps']
    assert abs(callback['source_window_s'][1]-callback['source_window_s'][0]-callback['use_s'])<1e-7
    assert callback['source_window_s'][0] >= rows[0]['use_s'] and callback['source_window_s'][1] <= 8
    for name,digest in plan['source_v02_sha256'].items():
        assert hashlib.sha256((EDIT/name).read_bytes()).hexdigest()==digest
    for dest,obj in [(EDIT/'PICTURE_PLAN_v03d.json',plan),(OUT/'acceptance_audit_v03d.json',audit)]:
        dest.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
    with (OUT/'cuts_v03d.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['row','source','vo_in','vo_out','vo_text'],lineterminator='\n')
        writer.writeheader()
        for r in rows:
            writer.writerow(dict(row=f'P{r["part"]}:{r["id"]}',source='CARD' if 'card_p' in r['id'] or 'cream_end_card' in r['id'] else r['source_kind'],vo_in=r['t_s'],vo_out=r['t_end_s'],vo_text=r['vo_land'][0]))
    print(json.dumps(audit,indent=2))


if __name__=='__main__':
    main()
