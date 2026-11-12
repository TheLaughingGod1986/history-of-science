"""Mechanical verification only; no film-stage, audio or motion approval."""
import hashlib,json,pathlib,subprocess,sys,math
root=pathlib.Path(sys.argv[1]);here=pathlib.Path(__file__).resolve().parent
d=json.loads((root/'REMAINING_GRAPHICS_MANIFEST_v04.json').read_text())
plan_path=here/'PICTURE_PLAN_v03.json';plan=json.loads(plan_path.read_text());raw=here.parent/plan['vo_lock']['stt_raw']
assert hashlib.sha256(plan_path.read_bytes()).hexdigest()==d['plan_sha256']
assert hashlib.sha256(raw.read_bytes()).hexdigest()==d['stt_sha256']
words=[dict(w,raw_index=i) for i,w in enumerate(json.loads(raw.read_text())['words']) if w['type']=='word']
rows={r['row_id']:r for r in plan['rows']};assert len(d['rows'])==8
assert len({r['row_id'] for r in d['rows']})==8
for r in d['rows']:
    p=root/pathlib.Path(r['path']).name
    assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
    v=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(p)]))['streams'][0]
    assert (v['width'],v['height'],v['avg_frame_rate'],int(v['nb_frames']))==(1920,1080,'30/1',r['frames'])
    assert abs(float(v['duration'])-r['plan_duration_s'])<=1/60+.00001
    source=rows[r['row_id']]
    assert (r['plan_in_s'],r['plan_out_s'])==(source['in_s'],source['out_s'])
    subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],check=True,stdout=subprocess.DEVNULL)
    previous=r['plan_in_s']
    for c in r['cues']:
        assert previous<=c['in_s']<c['out_s']<=r['plan_out_s'];previous=c['out_s']
        assert c['out_s']-c['in_s']<=4
        if c['word_indices']:
            assert c['in_s']>=words[c['word_indices'][-1]]['start']
            assert c['raw_stt_indices']==[words[i]['raw_index'] for i in c['word_indices']]
            assert ' '.join(words[i]['text'].strip('.,!?').lower() for i in c['word_indices'])==c['phrase'].lower()
        else:
            assert c['kind']=='chapter_heading'
            assert c['out_s']==next(w['start'] for w in words if r['plan_in_s']<=w['start']<r['plan_out_s'])
        # The renderer evaluates absolute time at frame starts; first visible frame cannot precede cue.
        first=math.ceil((c['in_s']-r['plan_in_s'])*30-1e-8)
        assert r['plan_in_s']+first/30>=c['in_s']-1e-7
print('PASS: eight additional preliminary graphic files match SHA-256, decode completely, are 1920x1080 at 30 fps, and match v03 durations within half a frame; source/raw word indices agree, cues do not overlap or reveal before their final anchor word, and chapter headings clear at the next spoken word.')
print('Partial checkpoint only. Editorial simplifications and brief chapter readability need Chief review. Thirteen archive rows, full cues and rough remain; no film-stage approval, audio assessment or moving-video review.')
