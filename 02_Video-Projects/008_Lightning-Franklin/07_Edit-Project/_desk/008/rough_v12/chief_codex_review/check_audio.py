import json,hashlib,subprocess
from pathlib import Path
from faster_whisper import WhisperModel
out=Path('/Users/benjaminoats/_desk/chief/j1267-v12-review')
p=Path('/Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_precheck/rough_v12/hos_008_rough_v12.mp4')
sha=hashlib.sha256(p.read_bytes()).hexdigest();print('MASTER',sha,flush=True)
cmd=['ffmpeg','-v','error','-ss','455','-i',str(p),'-t','15','-vn','-ac','1','-ar','16000','-c:a','pcm_s16le',str(out/'window.wav')]
subprocess.run(cmd,check=True)
a=hashlib.sha256((out/'window.wav').read_bytes()).hexdigest()
for model in ['base.en','small.en']:
 m=WhisperModel(model,device='cpu',compute_type='int8',local_files_only=True)
 segs,info=m.transcribe(str(out/'window.wav'),language='en',word_timestamps=True,beam_size=5,vad_filter=False)
 words=[dict(word=w.word,start=round(455+w.start,3),end=round(455+w.end,3)) for s in segs for w in s.words]
 r=dict(master_sha256=sha,audio_sha256=a,extract_command=cmd,model=model,words=words)
 (out/(model+'.json')).write_text(json.dumps(r,indent=2))
 print(model,json.dumps(words),flush=True)
