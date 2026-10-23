from pathlib import Path
import hashlib,json,subprocess as sp,sys
ROOT=Path('/Users/benjaminoats/YouTube/History Of Science'); EP=ROOT/'02_Video-Projects/006_Trees-Are-Made-Of-Air';OWB=Path('/Users/benjaminoats/YouTube/orbit-with-ben');PACK=EP/'07_Edit-Project/master_v01';OLD=EP/'07_Edit-Project/full_join_v02_teach'
def run(args,name,cwd=None):
 r=sp.run([str(x) for x in args],stdout=sp.PIPE,stderr=sp.STDOUT,text=True,cwd=cwd);(PACK/name).write_text(r.stdout);print(r.stdout[-1500:],flush=True)
 if r.returncode: raise RuntimeError(f'{name} failed: {r.returncode}')
source=OLD/'hos_006_full_join_v03_teach.mp4';master=PACK/'hos_006_master_v01.mp4'
if '--gates-only' not in sys.argv:
 run(['ffmpeg','-y','-v','error','-i',source,'-i',PACK/'audio_master_v01.m4a','-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',master],'mux.txt')
# Verify identical compressed picture packets, not merely a copy-codec command.
for p,name in [(source,'source_video_sha256.txt'),(master,'master_video_sha256.txt')]:
 run(['ffmpeg','-v','error','-i',p,'-map','0:v:0','-c','copy','-f','hash','-hash','sha256','-'],name)
assert (PACK/'source_video_sha256.txt').read_text()==(PACK/'master_video_sha256.txt').read_text()
run([sys.executable,OWB/'scripts/music_gate.py',EP,'--bed',EP/'05_Music/trees006_score_bed_v01.mp3','--video',master,'--out',PACK/'music_gate.json','--others',*[p for root in [ROOT,OWB] for p in root.glob('02_Video-Projects/*/05_Music/*') if p.suffix.lower() in ('.mp3','.wav','.m4a') and p.parent.parent!=EP]],'music_gate.txt')
run([sys.executable,OWB/'scripts/picture_qa.py',master,'--cuts',OLD/'cuts_full_join_v02.json','--pool',OLD/'pool_full_join_v02.json','--out-dir',PACK,'--reviewed-ok',OLD/'picture_qa_reviewed_ok_v02_teach.json'], 'picture_qa.txt')
run([sys.executable,OWB/'scripts/polish_gate.py',master,'--cuts',OLD/'cuts_full_join_v02.json','--out',PACK/'polish_gate.json','--reviewed-ok',OLD/'picture_qa_reviewed_ok_v02_teach.json'],'polish_gate.txt')
run(['npm','run','gate:episode','--','--project',EP], 'episode_gate.txt',ROOT/'07_Content-Ops')
run(['ffmpeg','-hide_banner','-i',master,'-af','ebur128=peak=true','-f','null','-'],'master_loudness.txt')
manifest={str(p.relative_to(EP)):hashlib.file_digest(p.open('rb'),'sha256').hexdigest() for p in [master,PACK/'stem_vo_v01.wav',EP/'05_Music/trees006_score_bed_v01.mp3',EP/'06_Sound-Effects/stem_sfx_v01.wav']}
(PACK/'SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('ALL MASTER GATES COMPLETED',flush=True)
