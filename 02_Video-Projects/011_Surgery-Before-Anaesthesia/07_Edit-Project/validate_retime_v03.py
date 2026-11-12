"""Validate the J2655 plan against immutable v02 and tracked Scribe intervals."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILM = HERE.parent

def read(name):
    return json.loads((HERE / name).read_text())

def main():
    old, new = read('PICTURE_PLAN_v02.json'), read('PICTURE_PLAN_v03.json')
    audit = read('RETIME_AUDIT_v03.json')
    words = [w for w in json.loads((FILM / old['vo_lock']['stt_raw']).read_text())['words'] if w['type'] == 'word']
    assert hashlib.sha256((HERE / 'PICTURE_PLAN_v02.json').read_bytes()).hexdigest() == new['retime_provenance']['source_plan_sha256']
    assert hashlib.sha256((FILM / old['vo_lock']['stt_raw']).read_bytes()).hexdigest() == new['retime_provenance']['word_timings_sha256']
    assert new['vo_lock'] == old['vo_lock']
    assert new['totals'] == old['totals'] and new['parts'] == old['parts']
    assert new['who_portraits'] == old['who_portraits']
    assert new['generation_authorized'] is False
    assert len(old['rows']) == len(new['rows']) == 93
    allowed = {'in', 'out', 'in_s', 'out_s', 'duration_s', 'vo_excerpt'}
    for before, after in zip(old['rows'], new['rows']):
        assert before['row_id'] == after['row_id']
        ignored = allowed | ({'visual', 'prompt'} if before['row_id'] == 'P4:08a' else set())
        assert {k: v for k, v in before.items() if k not in ignored} == {k: v for k, v in after.items() if k not in ignored}
        if before['row_id'] == 'P4:08a':
            for key in ('visual', 'prompt'):
                assert after[key] == before[key].replace('Victorian', 'mid-1840s')
        assert 0 < after['duration_s'] <= 8
        assert abs(after['out_s'] - after['in_s'] - after['duration_s']) < 1e-8
        for key, timestamp in (('in', after['in_s']), ('out', after['out_s'])):
            assert after[key] == f'{int(timestamp // 60)}:{timestamp % 60:05.2f}'
        assert after['vo_excerpt'] == ' '.join(w['text'] for w in words if after['in_s'] <= w['start'] < after['out_s'])
    rows = new['rows']
    assert rows[0]['in_s'] == 0 and rows[-1]['out_s'] == 535.3
    assert rows[-1]['in_s'] == 532.72 and rows[-1]['duration_s'] == 2.58
    for left, right, entry in zip(rows, rows[1:], audit['boundaries']):
        t = right['in_s']
        assert left['out_s'] == t
        assert not any(w['start'] < t < w['end'] for w in words), (right['row_id'], t)
        assert entry['next_row'] == right['row_id'] and entry['new_s'] == t
    assert len(audit['boundaries']) == 92
    assert sum(bool(x['old_crossed_words']) for x in audit['boundaries']) == 18
    assert sum(x['changed'] for x in audit['boundaries']) == 37
    sentences, current = [], []
    for w in words:
        current.append(w)
        if w['text'].rstrip('"').endswith(('.', '?', '!')):
            if current[-1]['end'] - current[0]['start'] > 8:
                sentences.append(current)
            current = []
    assert len(sentences) == len(audit['long_sentences']) == 11
    for sentence, entry in zip(sentences, audit['long_sentences']):
        assert entry['start_s'] == sentence[0]['start'] and entry['end_s'] == sentence[-1]['end']
        cuts = [r['in_s'] for r in rows[1:] if sentence[0]['start'] < r['in_s'] < sentence[-1]['end']]
        assert len(cuts) == 1 and cuts == [c['s'] for c in entry['cuts']]
    print('PASS: mechanical retime validation — 93 contiguous rows, 92 word-safe boundaries; 18 word crossings removed; all 11 long sentences split; maximum 8.00 s; v02 source, VO lock, row identities, budgets and generation locks preserved.')
    print('This is a data validation result, not film-stage approval or listening/motion QA.')

if __name__ == '__main__':
    main()
