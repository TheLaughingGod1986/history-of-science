#!/usr/bin/env python3
"""Resolve sentence preferences without changing locked audio or earlier plans."""
import copy
import csv
import hashlib
import json
from pathlib import Path

EDIT = Path(__file__).resolve().parent
OUT = EDIT / 'timing_rough_J2652'


def main():
    source = EDIT / 'PICTURE_PLAN_v03d.json'
    plan = json.loads(source.read_text())
    rows = plan['rows']
    by_id = {r['id']: r for r in rows}
    # The 8-second desk source can supply two different compositions. This
    # retains the 1837 image while cutting first on the preceding sentence.
    by_id['06_padlock_shut']['t_end_s'] = 32.70
    desk = by_id['07_darwin_1837_desk']
    detail = copy.deepcopy(desk)
    desk.update(id='07_darwin_1837_desk_wide', t_s=32.70, t_end_s=35.42)
    detail.update(id='07_darwin_1837_desk_detail', t_s=35.42)
    for r, framing in ((desk, 'wide'), (detail, 'notebook detail')):
        r['render_requirement'] = f'Distinct {framing} composition from the same native 8-second source; subject-safe crop must be reviewed. No looping or stretching.'
    rows.insert(rows.index(desk)+1, detail)
    # A single beach shot follows the full first sentence on the chapter scene.
    by_id['01_card_p02']['t_end_s'] = 81.22
    rows.remove(by_id['02_galapagos_beach_myth_beat1'])
    beach = by_id['02_galapagos_beach_myth_beat2']
    beach['id'] = '02_galapagos_beach_myth'
    # Show the blending analogy throughout its whole sentence, not as a flash
    # after Jenkin's portrait. His original WHO remains over the chapter scene.
    rows.remove(by_id['02a_jenkin_study'])
    paint = by_id['02b_paint_pots_mix']
    paint.update(t_s=453.0, t_end_s=458.14)
    by_id['03_cg_blending_beaks_beat1']['t_s'] = 458.14
    qualified = json.loads((OUT/'qualified_boundaries_v03d.json').read_text())
    words = json.loads((EDIT.parent/'02_Voiceover/stt/hos_013_vo_v03a/words_fw_small_en.json').read_text())['words']
    groups = {}
    for r in rows:
        r['use_s'] = round(r['t_end_s']-r['t_s'], 2)
        group = groups.setdefault(r['source_row_v02'], [])
        group.append(r)
        r['source_window_s'] = [round(r['t_s']-group[0]['t_s'], 2), round(r['t_end_s']-group[0]['t_s'], 2)]
        r['vo_land'] = [''.join(w['word'] for w in words if r['t_s'] <= w['start'] < r['t_end_s']).strip()]
        for key, value in [('t',r['t_s']),('t_end',r['t_end_s'])]:
            r[key] = f'{int(value//60)}:{value%60:05.2f}'
        r['local_s'] = round(r['t_s']-next(x['t_s'] for x in rows if x['part']==r['part']),2)
        r.pop('word_onsets', None)
        matches = [q for q in qualified if q['start_s']-1e-7 <= r['t_end_s'] <= q['end_s']+1e-7]
        if matches:
            q = matches[0]
            token = (q.get('script') or {}).get('token','').rstrip('\"”’\'')
            r['cut_out_evidence'] = dict(kind='sentence' if token.endswith(('.', '?', '!')) else 'qualified_gap', **q)
    callback = next(r for r in rows if r['source_kind']=='existing_plate_reuse')
    callback['source_window_s'] = [rows[0]['use_s'], round(rows[0]['use_s']+callback['use_s'],2)]
    for cue in plan['overlay_cues']:
        host = next(r for r in rows if r['t_s'] <= cue['display_start_s'] < r['t_end_s'])
        cue['display_host_row'] = cue['host_row'] = f'P{host["part"]}:{host["id"]}'
        cue['offset_in_host_s'] = round(cue['onset_s']-host['t_s'],3)
        host.setdefault('word_onsets',[]).append(copy.deepcopy(cue))
    exceptions = []
    for r in rows[:-1]:
        sentences = [q for q in qualified if (q.get('script') or {}).get('token','').rstrip('\"”’\'').endswith(('.', '?', '!'))
                     and max(q['start_s'],r['t_s']+3) <= min(q['end_s'],r['t_s']+7)]
        if sentences and r['cut_out_evidence']['kind'] != 'sentence':
            exceptions.append(dict(row=r['id'],start_s=r['t_s'],cut_s=r['t_end_s'],sentence_windows=[[q['start_s'],q['end_s']] for q in sentences]))
    plan.update(version='v03f-timing-scope',parent_plan_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                timing_status='Sentence preferences resolved except the explicit opening example in Chief ruling 6808560760; compositions still require review',render_authorized=False)
    plan['totals'].update(edit_beats=len(rows),unique_source_rows=len(groups))
    plan['callback'].update(source_window_s=callback['source_window_s'],duration_s=callback['use_s'])
    (EDIT/'PICTURE_PLAN_v03f.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False)+'\n')
    (OUT/'sentence_preference_v03f.json').write_text(json.dumps(dict(approved=False,remaining_choices=exceptions),indent=2)+'\n')
    with (OUT/'cuts_v03f.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['row','source','vo_in','vo_out','vo_text'],lineterminator='\n')
        writer.writeheader()
        for r in rows:
            writer.writerow(dict(row=f'P{r["part"]}:{r["id"]}',source='CARD' if 'card_p' in r['id'] or 'cream_end_card' in r['id'] else r['source_kind'],vo_in=r['t_s'],vo_out=r['t_end_s'],vo_text=r['vo_land'][0]))
    print(json.dumps(dict(rows=len(rows),sentence_choices=exceptions),indent=2))


if __name__ == '__main__':
    main()
