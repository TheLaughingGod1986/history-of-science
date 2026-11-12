#!/usr/bin/env python3
"""Repair cue scheduling and prove timing feasibility before another render.

Preserves v02, v03, their roughs, and the locked audio. Does not generate media.
Script punctuation evidence is paired with transcript word indices. A script
comma qualifies a boundary, but never authorizes cutting inside a spoken word.
"""
import copy
import hashlib
import json
from pathlib import Path

EDIT = Path(__file__).resolve().parent
OUT = EDIT / 'timing_rough_J2652'
WORDS = EDIT.parent / '02_Voiceover/stt/hos_013_vo_v03a/words_fw_small_en.json'


def write(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def label(cue):
    return cue['overlay'].get('line_1', cue['overlay'].get('label', ''))


def schedule(cues):
    """Keep named-person onsets; delayed labels must still start in their word."""
    cues = copy.deepcopy(cues)
    removed = []
    retained = []
    for c in cues:
        if label(c) == 'THE MISSING PIECE':
            removed.append(dict(cue=c, reason='Optional label removed to retain the mandatory Malthus WHO card for 3–4 seconds.'))
            continue
        if label(c) == 'EIGHT YEARS AT MICROSCOPE':
            removed.append(dict(cue=c, reason='Merged into the single barnacle fact/data cue at the same word onset.'))
            continue
        if label(c) == 'EIGHT YEARS ON BARNACLES':
            data = next(x for x in cues if label(x) == 'EIGHT YEARS AT MICROSCOPE')
            c['overlay'].update(kind='DATA', detail=data['overlay']['detail'], scale=data['overlay']['scale'])
            c['satisfies'] = ['FACT', 'DATA']
            c['merged_source_rows'] = [c['source_row_v02'], data['source_row_v02']]
        retained.append(c)
    retained.sort(key=lambda c: c['onset_s'])
    for i, c in enumerate(retained):
        o = c['overlay']
        # onset_s remains the exact transcript anchor; display_start_s is a
        # separate editorial field, never passed off as a different word time.
        start = c['onset_s']
        if i:
            start = max(start, retained[i-1]['display_end_s'])
        if o['kind'] == 'WHO':
            assert abs(start-c['onset_s']) < 1e-7, 'Never postpone a name'
        assert start <= c['word_end_s'] + 1e-7, ('Label would start after its word', label(c))
        hold = min(o.get('hold_s', 3), 4)
        if i+1 < len(retained):
            room = retained[i+1]['onset_s'] - start
            hold = min(hold, max(3 if o['kind'] == 'WHO' else 2.5, room))
        c.update(display_start_s=round(start, 3), display_end_s=round(start+hold, 3),
                 display_duration_s=round(hold, 3),
                 display_delay_s=round(start-c['onset_s'], 3))
        o['hold_s'] = round(hold, 3)
        if start > c['onset_s']:
            c['display_reason'] = 'Previous WHO card finishes first; this cue still begins while its anchored word is spoken.'
    return retained, removed


def main():
    src = EDIT / 'PICTURE_PLAN_v03.json'
    original_bytes = src.read_bytes()
    plan = json.loads(original_bytes)
    transcript = json.loads(WORDS.read_text())
    assert transcript['sha256'] == plan['vo_sha256']
    words = transcript['words']
    boundaries = json.loads((OUT / 'script_boundaries_v03b.json').read_text())
    pause_report = json.loads((OUT / 'measured_pauses_v03b.json').read_text())
    assert pause_report['vo_sha256'] == plan['vo_sha256']
    assert pause_report['threshold_db'] <= -45 and pause_report['minimum_s'] >= .12
    qualified = []
    for i, (a, b) in enumerate(zip(words, words[1:])):
        gap = b['start'] - a['end']
        if gap < -1e-7:
            continue
        pauses = [p for p in pause_report['intervals']
                  if p['start_s'] <= a['end'] <= b['start'] <= p['end_s']
                  and p['duration_s'] >= .12]
        if gap >= .12-1e-7 or str(i) in boundaries or pauses:
            qualified.append(dict(start_s=a['end'], end_s=b['start'], word_index=i,
                                  gap_s=round(gap, 3), script=boundaries.get(str(i)),
                                  measured_pause=pauses[0] if pauses else None))
    qualified.append(dict(start_s=words[-1]['end'], end_s=515.0,
                          word_index=len(words)-1, gap_s=round(515-words[-1]['end'], 3),
                          script={'context': 'End of locked narration; trailing silence.'}))
    blocked_spans = []
    for a, b in zip(qualified, qualified[1:]):
        duration = round(b['start_s']-a['end_s'], 3)
        if duration > 7:
            blocked_spans.append(dict(start_s=a['end_s'], end_s=b['start_s'], duration_s=duration,
                words=''.join(w['word'] for w in words[a['word_index']+1:b['word_index']+1]).strip(),
                first_word_index=a['word_index']+1, last_word_index=b['word_index'],
                reason='No transcript gap >=120 ms, measured pause at a word boundary, or verified script punctuation inside this span. No unsupported clause boundary is inferred.'))
    unsupported = []
    for r in plan['rows'][:-1]:
        t = r['t_end_s']
        if not any(q['start_s']-1e-7 <= t <= q['end_s']+1e-7 for q in qualified):
            unsupported.append(dict(row=f'P{r["part"]}:{r["id"]}', cut_s=t,
                prior_evidence=r['cut_out_evidence'],
                nearest_verified_boundaries=sorted(qualified, key=lambda q: abs(q['start_s']-t))[:2]))
    cues, removed = schedule(plan['overlay_cues'])
    for r in plan['rows']:
        r.pop('word_onsets', None)
    for c in cues:
        host = next(r for r in plan['rows'] if r['t_s'] <= c['display_start_s'] < r['t_end_s'])
        c['display_host_row'] = f'P{host["part"]}:{host["id"]}'
        host.setdefault('word_onsets', []).append(copy.deepcopy(c))
    plan.update(version='v03b-cue-scope', overlay_cues=cues, removed_or_merged_cues=removed,
                timing_status='FIX: inherited v03 cuts are not approved',
                render_authorized=False,
                parent_plan_sha256=hashlib.sha256(original_bytes).hexdigest())
    (EDIT / 'PICTURE_PLAN_v03b.json').write_text(json.dumps(plan, indent=2, ensure_ascii=False)+'\n')
    overlaps = [dict(first=label(a), second=label(b)) for a,b in zip(cues,cues[1:])
                if a['display_end_s'] > b['display_start_s']+1e-7]
    assert not overlaps
    assert all(c['onset_s'] == words[c['word_index']]['start'] for c in cues)
    assert all(3 <= c['display_duration_s'] <= 4 and c['display_delay_s'] == 0
               for c in cues if c['overlay']['kind']=='WHO')
    assert src.read_bytes() == original_bytes
    for name, sha in plan['source_v02_sha256'].items():
        assert hashlib.sha256((EDIT/name).read_bytes()).hexdigest() == sha
    audit = dict(approved=False, render_authorized=False, qualified_boundary_count=len(qualified),
                 unsupported_cuts=unsupported, unbridgeable_spans=blocked_spans,
                 cue_count=len(cues), cue_overlaps=overlaps, all_word_anchors_preserved=True,
                 all_name_onsets_preserved=True, all_name_holds_3_to_4_s=True,
                 delayed_cues=[dict(label=label(c), anchor_s=c['onset_s'], display_s=c['display_start_s'],
                                    word_end_s=c['word_end_s']) for c in cues if c['display_delay_s']],
                 measured_pause_boundary_count=sum(bool(q.get('measured_pause')) for q in qualified),
                 measured_pause_note='Numerical low-energy intervals only; no listening or motion perception claimed. A pause authorizes only an existing transcript word boundary, never a point inside a word.',
                 v02_and_v03_unchanged=True)
    write('qualified_boundaries_v03b.json', qualified)
    write('acceptance_audit_v03b.json', audit)
    write('overlay_audit_v03b.json', cues)
    print(f'CUE SCHEDULE PASS: {len(cues)} cues, zero collisions; names remain at their word onset for 3–4 s.')
    print(f'TIMING FIX: {len(unsupported)} unsupported existing cuts; {len(blocked_spans)} spans exceed 7 s without a verified boundary.')


if __name__ == '__main__':
    main()
