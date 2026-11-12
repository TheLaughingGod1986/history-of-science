"""Verify delivered J2563 five-row checkpoint, not aesthetic or motion approval."""
import hashlib,json,pathlib,subprocess,sys
root=pathlib.Path(sys.argv[1]);d=json.loads((root/'FREE_GRAPHICS_MANIFEST_v03.json').read_text());here=pathlib.Path(__file__).resolve().parent
plan=json.loads((here/'PICTURE_PLAN_v03.json').read_text());stt=json.loads((here.parent/plan['vo_lock']['stt_raw']).read_text());words=[dict(w,raw_index=i) for i,w in enumerate(stt['words']) if w['type']=='word']
assert len(d['rows'])==5
for r in d['rows']:
 p=root/pathlib.Path(r['path']).name;assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
 v=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(p)]))['streams'][0]
 assert (v['width'],v['height'],v['avg_frame_rate'],int(v['nb_frames']))==(1920,1080,'30/1',r['frames'])
 assert abs(float(v['duration'])-r['plan_duration_s'])<=1/60+.00001
 previous=r['plan_in_s']
 for c in r['cues']:
  assert previous<=c['in_s']<c['out_s']<=r['plan_out_s'];previous=c['out_s']
  if c['word_indices']:
   assert c['in_s']==words[c['word_indices'][-1]]['start']
   assert c['raw_stt_indices']==[words[i]['raw_index'] for i in c['word_indices']]
  assert c['out_s']-c['in_s']<=4
print('PASS: five delivered graphic files match SHA-256, 1920x1080, 30 fps, planned durations within half a frame; cue word indices and raw indices agree, no label overlap or premature full-phrase reveal.')
print('Partial checkpoint only: 21 free rows, full overlays and timing rough remain unfinished; no moving-video or audio review, no film-stage approval.')
