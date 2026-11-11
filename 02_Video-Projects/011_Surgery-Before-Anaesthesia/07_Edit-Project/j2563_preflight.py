"""Read-only plan audit: no rendering, generation, VO or timing mutations."""
import concurrent.futures
import datetime
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent
plan = json.loads((ROOT / 'PICTURE_PLAN_v02.json').read_text())
words = [w for w in json.loads((ROOT.parent / plan['vo_lock']['stt_raw']).read_text())['words'] if w['type'] == 'word']

def source_check(row):
    result = {'row_id': row['row_id'], 'url': row['archive_url'], 'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        request = urllib.request.Request(row['archive_url'], headers={'User-Agent': 'OrbitStudio/1.0 provenance check'})
        with urllib.request.urlopen(request, timeout=20) as response:
            result.update(http_status=response.status, final_url=response.url, bytes_read=len(response.read()), licence_verified=False)
    except Exception as error:
        result.update(http_status=getattr(error, 'code', None), error=str(error), licence_verified=False)
    return result

sentences = []
start = words[0]['start']
text = []
for word in words:
    text.append(word['text'])
    if word['text'].rstrip('\"\u201d\u2019').endswith(('.', '?', '!')):
        sentences.append({'start': start, 'end': word['end'], 'text': ' '.join(text)})
        start = None
        text = []
    if start is None:
        following = words.index(word) + 1
        if following < len(words):
            start = words[following]['start']

boundaries = []
for row in plan['rows'][1:]:
    cut = row['in_s']
    crossing_words = [w for w in words if w['start'] + .005 < cut < w['end'] - .005]
    crossing_sentence = [s for s in sentences if s['start'] + .005 < cut < s['end'] - .005]
    if crossing_words or crossing_sentence:
        boundaries.append({'next_row': row['row_id'], 'cut_s': cut, 'words_crossed': crossing_words, 'sentence_crossed': crossing_sentence})
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    sources = list(pool.map(source_check, [r for r in plan['rows'] if r['archive_url']]))
result = {
    'job': 'J2563', 'plan': 'PICTURE_PLAN_v02.json',
    'method': 'Text/timestamp audit only; punctuation is a conservative sentence-boundary proxy. No listening or motion review.',
    'source_checks': sources, 'boundary_flags': boundaries,
    'over_8s_rows': [r['row_id'] for r in plan['rows'] if r['duration_s'] > 8.005],
    'sentences_over_8s': [s for s in sentences if s['end'] - s['start'] > 8.005],
    'reuse_dependencies': [{'row_id': r['row_id'], 'requires': r['reuses_row'], 'source_kind': next(x['source_kind'] for x in plan['rows'] if x['row_id'] == r['reuses_row'])} for r in plan['rows'] if r['reuses_row']],
    'generation_authorized': False,
}
(ROOT / 'J2563_PREFLIGHT.json').write_text(json.dumps(result, indent=2) + '\n')
lines = ['# J2563 timing preflight', '', result['method'], '', f"{len(boundaries)} picture boundaries occur inside punctuation-delimited sentences; {sum(bool(x['words_crossed']) for x in boundaries)} also intersect a spoken word. {len(result['over_8s_rows'])} planned rows exceed 8 seconds.", '', 'These are findings, not automatic timing corrections. A sentence longer than 8 seconds cannot both remain in one picture row and meet the 8-second maximum. Chief must resolve that conflict before a render or v03 retime.', '', '## Boundaries to resolve', '', '| Next row | Cut seconds | Word crossed | Sentence |', '|---|---:|---|---|']
for item in boundaries:
    lines.append('| {} | {:.2f} | {} | {} |'.format(item['next_row'], item['cut_s'], ', '.join(w['text'] for w in item['words_crossed']) or 'none', ' / '.join(s['text'] for s in item['sentence_crossed']).replace('|', '/')))
lines += ['', '## Sentences longer than 8 seconds', '']
for item in result['sentences_over_8s']:
    lines.append(f"- {item['start']:.2f}–{item['end']:.2f} ({item['end']-item['start']:.2f}s): {item['text']}")
lines += ['', '## Overlay alignment', '', 'Not verified: markers in v02 specify row-level prose, not per-word overlay cue times. The rough and per-word reveal schedule remain unbuilt. No overlay timing PASS is claimed.', '', '## Chief wording note', '', 'P4:08a: replace “Victorian” with “mid-1840s” wherever present in its visual/prompt. This wording correction is accepted in the brief; no plan timing or generation permission has been changed.']
(ROOT / 'J2563_TIMING_AUDIT.md').write_text('\n'.join(lines) + '\n')
print(f"Source results: {[s.get('http_status') for s in sources]}")
print(f"Sentence boundary flags: {len(boundaries)}; word overlaps: {sum(bool(x['words_crossed']) for x in boundaries)}; long sentences: {len(result['sentences_over_8s'])}; rows over 8s: {result['over_8s_rows']}")
