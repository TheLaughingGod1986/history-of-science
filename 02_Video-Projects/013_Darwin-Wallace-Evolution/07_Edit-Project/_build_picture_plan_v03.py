#!/usr/bin/env python3
"""J2652: reproducible, no-spend timing scope. Never writes v02 or audio.

Times are seconds on the unchanged J1310 WAV. A global shortest-path search
keeps each picture near its original spoken passage while using only audited
word boundaries. Rendering and editorial acceptance remain separate checks.
"""
import copy
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess

EDIT = Path(__file__).resolve().parent
FILM = EDIT.parent
OUT = EDIT / 'timing_rough_J2652'
WORDS = FILM / '02_Voiceover/stt/hos_013_vo_v03a/words_fw_small_en.json'
LOCK = '837178125a72fb250d255f1039c5cb7f8630bbb313cf23801a1155f257d796e0'
# Proposed editorial boundaries where ASR has no punctuation/pause.
# These need the independent clause review recorded in REVIEW_v03.md; a
# boundary between words alone does not prove that it meets the Chief rule.
# Index is the last word before the break, not a guessed timestamp.
CLAUSES = {
    137: 'temporal clause: then in June 1858 / a letter arrived',
    741: 'coordinated clause: thought about Malthus / and like Darwin',
    986: 'coordinated clause: came out on 24 November 1859 / and booksellers',
    611: 'parenthetical clause ends: the story goes / that one of his children',
    38: 'list item: eight years of barnacles / and one letter',
    47: 'relative clause ends: other side of the world / forced',
    61: 'subject ends: most naturalists / believed',
    72: 'coordinated predicate: made once / and never changed',
    98: 'object ends: drew a little tree / in a private notebook',
    173: 'relative clause ends: who did not label his birds properly / stumble onto',
    189: 'subordinate clause ends: on the Galapagos Islands / they imagine',
    211: 'coordinated predicate: collected birds there / and thought',
    377: 'relative clause: one kind of finch / long ago and changed',
    423: 'attribution: human populations / by Thomas Malthus',
    563: 'coordinated predicate: sealed it / and left Emma a letter',
    636: 'conditional clause ends: waited too long / someone else',
    802: 'coordinated predicate: read Wallace paper / and wrote',
    872: 'subject ends: Charles Lyell and Joseph Hooker / had both works read',
    1051: 'coordinated clause: rest of his life / and the answer',
    1128: 'subject ends: a friar called Gregor Mendel / had published',
    1200: 'imperative clause ends: together with Mendel beads and / you have',
}


def dump(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def sentence(w):
    return bool(re.search(r'[.!?][\"\u201d\u2019\x27]?$', w['word'].strip()))


def candidates(words):
    result = {0.0: {'kind': 'start'}, 515.0: {'kind': 'end'}}
    for i, (a, b) in enumerate(zip(words, words[1:])):
        gap = round(b['start']-a['end'], 6)
        if gap < 0:
            continue
        kind = ('sentence' if sentence(a) else 'comma' if re.search(r'[,;:][\"\u201d\u2019\x27]?$', a['word'].strip())
                else 'gap_120ms' if gap >= .12-1e-6 else 'clause' if i in CLAUSES else None)
        if kind is None:
            continue
        # Every frame-grid point in the gap: avoids rounding into spoken words.
        for n in range(math.ceil((a['end']-1e-8)*50), math.floor((b['start']+1e-8)*50)+1):
            t = round(n/50, 2)
            if any(w['start']+1e-7 < t < w['end']-1e-7 for w in words):
                continue
            result[t] = dict(kind=kind, previous_word_index=i, next_word_index=i+1,
                             previous_word=a['word'].strip(), next_word=b['word'].strip(),
                             gap_s=gap, after_word_s=round(t-a['end'], 3),
                             clause_reason=CLAUSES.get(i) if kind=='clause' else None)
    result[512.74] = dict(kind='sentence', previous_word_index=len(words)-1,
                         after_word_s=.50, gap_s=2.76)
    return result


def main():
    OUT.mkdir(exist_ok=True)
    plan = json.loads((EDIT/'PICTURE_PLAN_v02.json').read_text())
    transcript = json.loads(WORDS.read_text())
    assert transcript['sha256'] == LOCK
    words = transcript['words']
    original = sorted((EDIT/'parts').glob('part-*_plates_v02.json'))
    hashes = {str(p.relative_to(EDIT)): digest(p) for p in original+[EDIT/'PICTURE_PLAN_v02.json']}
    parts = [json.loads(p.read_text()) for p in original]
    rows = []
    for part in parts:
        for source in part['plates']:
            # Split long visual passages into separately rendered beats. For long
            # diagrams, the second beat must be composited over moving picture.
            count = math.ceil((source['t_end_s']-source['t_s'])/7)
            for k in range(count):
                r = copy.deepcopy(source)
                r['part'] = int(part['part'])
                r['source_row_v02'] = f"P{int(part['part'])}:{source['id']}"
                r['id'] += f'_beat{k+1}' if count>1 else ''
                r['target_start_s'] = source['t_s']+(source['t_end_s']-source['t_s'])*k/count
                r['target_end_s'] = source['t_s']+(source['t_end_s']-source['t_s'])*(k+1)/count
                r['v02_window_s'] = [source['t_s'], source['t_end_s']]
                r['generation_authorized'] = False
                if count>1:
                    r['render_requirement'] = 'Distinct timed beat; contiguous source interval, no looping or duplicated frames.'
                    if source['source_kind']=='code_graphic':
                        r['composition'] = 'full_frame' if k%2==0 else 'overlay_on_moving_plate'
                        if k%2:
                            r['render_requirement'] = 'Re-render graphic as animated overlay on a matching moving Quality plate; no consecutive full-frame diagrams.'
                rows.append(r)
    allowed = candidates(words)
    # DP state: end time -> (cost, chosen boundaries). Hard caps are constraints,
    # not penalties. Sentence preference dominates normal proximity differences.
    states = {0.0: (0.0, [])}
    for idx, r in enumerate(rows):
        overlay = r.get('teach_overlay') or {}
        kind = overlay.get('kind')
        next_kind = (rows[idx+1].get('teach_overlay') or {}).get('kind') if idx+1<len(rows) else None
        ends = [515.] if idx==len(rows)-1 else [t for t in allowed if abs(t-r['target_end_s'])<=4.5]
        future = {}
        for start, (cost, path) in states.items():
            lo, hi = (.28, 3.0) if kind in ('CHAPTER','END_CARD') else (1.5, 7.0)
            if kind=='REUSE':
                hi = min(4.20, 8.0-path[0])
            feasible = [t for t in ends if lo-1e-7 <= t-start <= hi+1e-7]
            if kind in ('CHAPTER','END_CARD'):
                feasible = [t for t in feasible if not any(start<=w['start']<t for w in words)]
            if next_kind in ('CHAPTER','END_CARD'):
                feasible = [t for t in feasible if allowed[t]['kind']=='sentence' and .5-1e-7<=allowed[t].get('after_word_s',0)<=.8+1e-7]
            sentence_options = [t for t in feasible if allowed[t]['kind']=='sentence' and 3<=t-start<=7]
            group_first = next(j for j in range(idx+1) if rows[j]['source_row_v02']==r['source_row_v02'])
            group_start = path[group_first-1] if group_first else 0.0
            for end in feasible:
                # Keep split beats short, keep original semantic passage nearby.
                score = cost + (end-r['target_end_s'])**2 + .08*((end-start)-5)**2
                if sentence_options and end not in sentence_options and kind not in ('CHAPTER','END_CARD','REUSE'):
                    score += 100
                if end not in future or score<future[end][0]:
                    future[end] = score, path+[end]
        if not future:
            raise RuntimeError(f'No legal timing path at {idx} {r["source_row_v02"]}; do not relax constraints')
        states = future
    boundaries = states[515.][1]
    start = 0.
    cut_audit = []
    for i, (r, end) in enumerate(zip(rows, boundaries)):
        r.update(t_s=start, t_end_s=end, use_s=round(end-start,2),
                 t=f'{int(start//60)}:{start%60:05.2f}', t_end=f'{int(end//60)}:{end%60:05.2f}')
        r['vo_land'] = [''.join(w['word'] for w in words if start<=w['start']<end).strip()]
        r['cut_out_evidence'] = allowed[end]
        if r['source_kind']=='existing_plate_reuse':
            r['source_window_s']=[boundaries[0],round(boundaries[0]+end-start,2)]
        cut_audit.append(dict(row=f'P{r["part"]}:{r["id"]}', start=start, end=end, evidence=allowed[end]))
        start=end
    # Onsets are explicit word records, independent of row boundaries. Each
    # cue names its actual host row, so a late name is never painted early.
    cues=[]
    overrides = {'Charles Darwin': 2, 'Alfred Russel Wallace':647, 'Nicholas Lawson':259,
                 'John Gould':296, 'Thomas Malthus':425, 'Emma Darwin':548,
                 'Charles Lyell':808, 'Joseph Hooker':871, 'Fleeming Jenkin':1066,
                 'Gregor Mendel':1127, 'Herbert Spencer':1160}
    anchors = {
        'LOCKED AWAY':13, 'ONE LETTER':39, 'LONDON · 1830S':59, 'FIXED FOREVER?':74,
        'TWENTY YEARS IN A DRAWER':132, 'OTHER SIDE OF WORLD':145,
        'GALÁPAGOS · SEPTEMBER 1835':205, 'FORGOT TO LABEL FINCHES':228,
        'ONE SHELL PER ISLAND':268, 'WHOLE TOOLBOX OF BEAKS':327,
        'THE MISSING PIECE':429, 'MOST NEVER SURVIVE':444, 'NATURAL SELECTION':None,
        'CONFESSING A MURDER':542, 'JULY 1844':553, '230 PAGES · IF I DIE':560,
        'OCTOBER 1844':580, 'EIGHT YEARS ON BARNACLES':602,
        'EIGHT YEARS AT MICROSCOPE':602, 'AUGUST 1852':None,
        'HIS COLLECTION SANK':685, '125,660 SPECIMENS':723, 'FEBRUARY 1858':727,
        'THE SAME IDEA':None, 'ORIGINALITY SMASHED':812, 'TWO EMPTY CHAIRS':None,
        'NO STRIKING DISCOVERY':None, '24 NOVEMBER 1859':None,
        '1,250 COPIES PRE-SOLD':990, 'DARWINISM · 1889':1040,
        'BLENDED AWAY?':1075, 'WASHED AWAY BY BLENDING':1107,
        'WHOLE LIKE BEADS':1144, 'FIT MEANS FITS':1183,
    }
    # Remaining phrase anchors are located explicitly within their source row,
    # then saved as indices/quoted words for independent review.
    keywords = {'NATURAL SELECTION':'selection', 'EIGHT YEARS ON BARNACLES':'eight',
                'EIGHT YEARS AT MICROSCOPE':'years', 'AUGUST 1852':'1852',
                'HIS COLLECTION SANK':'lost', 'THE SAME IDEA':'malthus',
                'TWO EMPTY CHAIRS':'neither', 'NO STRIKING DISCOVERY':'striking',
                '24 NOVEMBER 1859':'1859', '1,250 COPIES PRE-SOLD':'250', 'OCTOBER 1844':'vestiges'}
    for part in parts:
        for source in part['plates']:
            o=copy.deepcopy(source.get('teach_overlay') or {})
            if o.get('kind') not in ('WHO','WHEN','LABEL','FACT','DATA','EXPLAINER','ARCHIVE'):
                continue
            key=o.get('line_1',o.get('label',''))
            if not key:
                continue
            wi=overrides.get(key, anchors.get(key))
            if wi is None and key in keywords:
                hits=[i for i,w in enumerate(words) if keywords[key] in w['word'].lower() and source['t_s']-3<=w['start']<=source['t_end_s']+3]
                wi=hits[0] if hits else None
            cue=dict(source_row_v02=f'P{int(part["part"])}:{source["id"]}', overlay=o)
            if wi is None:
                cue.update(status='UNRESOLVED', reason='No unambiguous matching phrase in the local transcript; no onset invented.')
            else:
                onset=words[wi]['start']
                host=next(r for r in rows if r['t_s']<=onset<r['t_end_s'])
                cue.update(status='ANCHORED', word_index=wi, word=words[wi]['word'].strip(), onset_s=onset,
                           word_end_s=words[wi]['end'], host_row=f'P{host["part"]}:{host["id"]}',
                           offset_in_host_s=round(onset-host['t_s'],3), transcript=str(WORDS.relative_to(FILM)))
                host.setdefault('word_onsets',[]).append(copy.deepcopy(cue))
            cues.append(cue)
    for part in parts:
        selected=[r for r in rows if r['part']==int(part['part'])]
        part.update(version='v03',task='J2652 word-safe scope; not picture approval',vo_sha256=LOCK,
                    vo_film_start_s=selected[0]['t_s'],part_end_film_s=selected[-1]['t_end_s'],plates=selected,
                    status='review',mint=False)
        for r in selected:
            r['local_s']=round(r['t_s']-selected[0]['t_s'],2)
            r.pop('teach_overlay',None)  # scheduled word_onsets are authoritative
        dump(EDIT/f'parts/part-{int(part["part"]):02d}_plates_v03.json',part)
    plan.update(version='v03',written='2026-11-12',task='J2652: word-safe picture scope; review required',
                vo_sha256=LOCK,word_timings_sha256=digest(WORDS),fps=50,
                ruling='https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6808560760',
                rows=rows,overlay_cues=cues,source_v02_sha256=hashes,
                callback=dict(max_duration_s=4.20,source_window_s=[boundaries[0],8.0],
                              policy='Trim only; no stretch or loop. Verify no overlap with retimed opener before KEEP.'),
                optional_replacements=dict(adopted=[],reason='No 390 px proof for these three replacements. Retain v02 Quality sources; no savings claimed.'),
                generation_authorized=False)
    plan['v02_reference_totals']=plan.pop('totals')
    plan['totals']=dict(edit_beats=len(rows),unique_source_rows=len({r['source_row_v02'] for r in rows}),new_generation_authorized=0)
    plan['v02_reference_per_part']=plan.pop('per_part')
    plan['v02_reference_open']=plan.pop('hos_2026_11_e2_open')
    dump(EDIT/'PICTURE_PLAN_v03.json',plan)
    dump(OUT/'cut_audit_v03.json',cut_audit)
    dump(OUT/'overlay_audit_v03.json',cues)
    with (OUT/'cuts_v03.csv').open('w',newline='') as f:
        out=csv.DictWriter(f,fieldnames=['row','source','vo_in','vo_out','vo_text'],lineterminator='\n');out.writeheader()
        for r in rows:
            card='card_p' in r['id'] or 'cream_end_card' in r['id']
            out.writerow(dict(row=f'P{r["part"]}:{r["id"]}',source='CARD' if card else r['source_kind'],
                              vo_in=r['t_s'],vo_out=r['t_end_s'],vo_text=r['vo_land'][0]))
    checker=Path('/Users/benjaminoats/YouTube/orbit-with-ben/00_Brand/Channel-Setup/tools/clip_check.py')
    check=subprocess.run(['python3',str(checker),str(OUT/'cuts_v03.csv'),'--words',str(WORDS),'--vo-end','512.48','--json'],text=True,capture_output=True)
    (OUT/'clip_check_v03.json').write_text(check.stdout)
    assert all(digest(EDIT/p)==h for p,h in hashes.items()),'v02 modified'
    print(f'{len(rows)} rows; clip_check exit {check.returncode}; {sum(c["status"]=="UNRESOLVED" for c in cues)} unresolved cues')


if __name__=='__main__':
    main()
