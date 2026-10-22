#!/usr/bin/env python3
"""J0830: £0 HOS 007 original chamber score, house SFX and lossless-picture master.
Chief authority: OWB #99 comment 6347492456, 22 Oct 2026.
Runs detached; never uploads, spends, or grants approval.
"""
from pathlib import Path
import hashlib,json,subprocess as sp,sys,wave,re,math,shutil
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
FILM=Path(__file__).resolve().parents[1]
OWB=Path('/Users/benjaminoats/YouTube/orbit-with-ben')
sys.path.insert(0,str(OWB/'scripts'))
import sfx_kit
JOIN=FILM/'07_Edit-Project/_desk/007/full_join_v01'
META=json.loads((JOIN/'JOIN_META_v01.json').read_text())
SRC=Path(META['file']); TOTAL=META['duration_s']; SR=48000
WORK=Path('/private/tmp/j0830-audio-master-v01'); PACK=FILM/'07_Edit-Project/master_v01_pack'
MUSIC=FILM/'05_Music'; SFX=FILM/'06_Sound-Effects'; OUT=WORK/'hos_007_master_v01.mp4'
for p in [WORK,PACK,MUSIC,SFX]: p.mkdir(parents=True,exist_ok=True)
def run(args,log=None):
 print('RUN', ' '.join(map(str,args)),flush=True)
 if log:
  r=sp.run(list(map(str,args)),stdout=sp.PIPE,stderr=sp.STDOUT,text=True);(PACK/log).write_text(r.stdout);print(r.stdout[-1800:],flush=True);return r.returncode
 sp.run(list(map(str,args)),check=True);return 0
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def write(p,x):
 with wave.open(str(p),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(x,-1,1)*32767).astype('<i2').tobytes())
def read(p):
 with wave.open(str(p)) as w:return np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(np.float32).reshape(-1,w.getnchannels())/32768
assert sha(SRC)==META['sha256'],'Approved join changed'
VO=WORK/'stem_vo_v01.wav'
run(['ffmpeg','-y','-v','error','-i',SRC,'-vn','-af','loudnorm=I=-14:TP=-1.5:LRA=11','-ar',SR,'-ac',2,VO])
vo=read(VO); N=min(len(vo),round(TOTAL*SR));vo=vo[:N];write(VO,vo)
vm,vi=sfx_kit.ebur128(VO); vm=np.array(vm); grid=np.arange(len(vm))*.1
# Distinct original G-major/E-minor chamber harmony; 60 BPM, sustained warm strings,
# soft wooden plucks only in explanation chapters. No reused 029 notes/audio.
chapters=[(0,100.833,'awe'),(100.833,230.458,'explain'),(230.458,309.208,'awe'),(309.208,401.958,'explain'),(401.958,TOTAL,'awe')]
chords=[(43,55,59,62),(40,55,59,64),(48,55,60,64),(50,57,62,66),(43,55,59,67),(45,57,60,64)]
bed=np.zeros((N,2),np.float32)
# Smooth timbral transition over 3 seconds at actual part boundaries.
def explain(t):
 v=np.zeros_like(t)
 for a,b,m in chapters:
  if m=='explain':v=np.maximum(v,np.minimum(np.clip((t-a)/3,0,1),np.clip((b-t)/3,0,1)))
 return v
for k,a in enumerate(np.arange(0,TOTAL,12)):
 i=int(a*SR);j=min(N,int((a+14)*SR));t=np.arange(j-i,dtype=np.float32)/SR
 env=np.sin(np.minimum(t/2,1)*np.pi/2)*np.sin(np.clip((14-t)/2,0,1)*np.pi/2)
 for z,m in enumerate(chords[k%len(chords)]):
  hz=440*2**((m-69)/12);amp=.028/(1+z*.4)
  for c,det in enumerate([.9995,1.0005]):
   ph=2*np.pi*hz*det*t+z*.4
   bed[i:j,c]+=amp*env*(np.sin(ph)+.19*np.sin(2*ph)+.06*np.sin(3*ph))
for k in range(math.ceil(TOTAL)):
 i=k*SR;j=min(N,i+int(.8*SR))
 if j<=i:continue
 t=np.arange(j-i,dtype=np.float32)/SR; mix=float(explain(np.array([k],np.float32))[0]);m=chords[(k//12)%len(chords)][[1,2,3,2,1,3][k%6]]
 hz=440*2**((m-69)/12);tone=.035*mix*np.minimum(t/.012,1)*np.exp(-t/.19)*(np.sin(2*np.pi*hz*t)+.22*np.sin(4*np.pi*hz*t))
 bed[i:j,0]+=tone*.8;bed[i:j,1]+=tone*.65
# 100 ms envelope ducking targets 18 dB below voice, with conservative pause ceiling.
BW=WORK/'vaccine_score_bed_v01.wav';write(BW,bed)
bm,bi=sfx_kit.ebur128(BW);n=min(len(vm),len(bm));need=np.maximum(0,np.array(bm[:n])-np.minimum(vm[:n]-18,vi-20))
need=np.array([need[max(0,k-5):min(n,k+6)].max() for k in range(n)])
for i in range(0,N,SR):
 j=min(N,i+SR);env=np.interp(np.arange(i,j)/SR,grid[:n],need,left=need[0],right=need[-1]);bed[i:j]*=10**(-env[:,None]/20)
t=np.arange(N,dtype=np.float32)/SR;bed*= (np.minimum(t/1.5,1)*np.minimum((TOTAL-t)/2,1))[:,None];write(BW,bed)
BED=MUSIC/'vaccine_score_bed_v01.mp3'
run(['ffmpeg','-y','-v','error','-i',BW,'-c:a','libmp3lame','-b:a','192k',BED])
prompt='HOS 007 First Vaccine: warm restrained chamber strings and wooden harp, original G major / E minor harmony. Part 1 awe, part 2 explain, part 3 uneasy discovery, part 4 explain, part 5 warm resolution. Three-second timbral transitions at part boundaries. Pace: 58-64 BPM. NOT Betelgeuse cosmic pads, Saturn, Sun, Venus, Light Speed or any earlier HOS bed; no modern synth lead, drums, menace or fast arpeggio.'
(MUSIC/'vaccine_score_bed_v01_plan.json').write_text(json.dumps(dict(film=FILM.name,bed=BED.name,prompt=prompt,duration_s=TOTAL,source='Original numpy synthesis, J0830, £0',sha256=sha(BED),chapters=chapters),indent=2)+'\n')
(MUSIC/'BED_BRIEF_v01.md').write_text('# HOS 007 original chamber score\n\nChief authority: OWB #99 comment 6347492456 (22 Oct 2026). £0, no ElevenLabs.\n\n'+prompt+'\n\nSustained lower strings under wonder; wooden harp pulse at 60 BPM under explanation. Mood blends over three seconds at part boundaries. Fit remains for Chief to hear.\n')
sfx_kit.make(SFX/'kit_v01','hos',830)
kit=list((SFX/'kit_v01').glob('*tick*.wav'));tick=read(kit[0]);sfx=np.zeros_like(bed);cues=[]
cuts=json.loads((JOIN/'cuts_full_join_v01.json').read_text())
for c in cuts:
 if 'code_graphic' in str(c.get('source','')) or 'code_graphic' in str(c.get('file','')):
  start=c['timeline_in'];i=round(start*SR);j=min(N,i+len(tick));sfx[i:j]+=tick[:j-i]*.6;cues.append(dict(start=start,kind='tick',why=c['row']))
# No generic transition whooshes or invented environmental audio.
SF=SFX/'stem_sfx_v01.wav';write(SF,sfx)
(SFX/'sfx_cues_v01.json').write_text(json.dumps(dict(cues=cues,source='Own house HOS kit, no spend'),indent=2)+'\n')
rc=run([sys.executable,OWB/'scripts/sfx_kit.py','level','--vo',VO,'--sfx',SF,'--bed',BED,'--minutes',TOTAL/60,'--out',PACK/'sfx_level.json'],'sfx_level.txt')
if rc:raise RuntimeError('SFX/bed level gate failed; inspect before mixing')
# Two-pass normalization; picture bitstream is copied from the approved join.
fc='[0:a][1:a][2:a]amix=inputs=3:normalize=0:duration=first'
r=sp.run(['ffmpeg','-hide_banner','-i',str(VO),'-i',str(BED),'-i',str(SF),'-filter_complex',fc+',loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[a]','-map','[a]','-f','null','-'],capture_output=True,text=True,check=True)
st=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',r.stderr,re.S)[-1]);(PACK/'loudnorm_pass1.json').write_text(json.dumps(st,indent=2)+'\n')
norm=f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={st['input_i']}:measured_TP={st['input_tp']}:measured_LRA={st['input_lra']}:measured_thresh={st['input_thresh']}:offset={st['target_offset']}:linear=true"
AUDIO=WORK/'audio_master_v01.m4a'
run(['ffmpeg','-y','-v','error','-i',VO,'-i',BED,'-i',SF,'-filter_complex',fc+','+norm+'[a]','-map','[a]','-ar',SR,'-c:a','aac','-b:a','256k',AUDIO])
run(['ffmpeg','-y','-v','error','-i',SRC,'-i',AUDIO,'-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',OUT])
# Persist master and separate stems on mounted NAS, verify every copy; never delete NAS data.
NAS=Path('/Volumes/data/mac-mini-archive')
assert sp.check_output(['mount'],text=True).find(' on /Volumes/data ')>=0,'NAS not mounted'
DEST=NAS/'hos-007-vaccine/master_v01_J0830';DEST.mkdir(parents=True,exist_ok=True)
assets=[OUT,VO,BED,SF,AUDIO];records=[]
for src in assets:
 dst=DEST/src.name;shutil.copy2(src,dst);digest=sha(src);assert digest==sha(dst);records.append(dict(file=str(dst),sha256=digest))
(PACK/'MASTER_META_v01.json').write_text(json.dumps(dict(job='J0830',approved_join_sha256=META['sha256'],picture='video stream copy, no picture edits',duration_s=TOTAL,files=records,spend='£0',approval='pending Chief'),indent=2)+'\n')
# Full tools use existing Chief-reviewed exceptions only.
checks={}
others=[]
for repo in [OWB,Path('/Users/benjaminoats/YouTube/History Of Science')]:
 for md in (repo/'02_Video-Projects').glob('*/05_Music'):
  if md.parent.name != FILM.name:
   others.extend(p for p in md.iterdir() if p.suffix.lower() in {'.mp3','.wav','.m4a'})
checks['music_gate']=run([sys.executable,OWB/'scripts/music_gate.py',FILM,'--bed',BED,'--video',OUT,'--others',*others,'--out',PACK/'music_gate.json'],'music_gate.txt')
checks['polish_gate']=run([sys.executable,OWB/'scripts/polish_gate.py',OUT,'--cuts',JOIN/'cuts_full_join_v01.json','--reviewed-ok',JOIN/'reviewed_ok_full_join_v01.json','--out',PACK/'polish_gate.json'],'polish_gate.txt')
checks['picture_qa']=run([sys.executable,OWB/'scripts/picture_qa.py',OUT,'--cuts',JOIN/'cuts_full_join_v01.json','--pool',JOIN/'pool_full_join_v01.json','--reviewed-ok',JOIN/'reviewed_ok_full_join_v01.json','--out-dir',PACK],'picture_qa.txt')
# Use established main checkout dependencies, point the gate to this job's project.
checks['episode']=run(['npm','--prefix','/Users/benjaminoats/YouTube/History Of Science/07_Content-Ops','run','gate:episode','--','--project',FILM],'gate_episode.txt')
r=sp.run(['ffmpeg','-hide_banner','-i',str(OUT),'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True,check=True);(PACK/'master_loudness.txt').write_text(r.stderr[-1800:])
checks['loudness']={'integrated_lufs':float(re.findall(r'I:\s*([-\d.]+) LUFS',r.stderr)[-1]),'true_peak_dbtp':float(re.findall(r'Peak:\s*([-\d.]+) dBFS',r.stderr)[-1])}
(PACK/'CHECK_RESULTS.json').write_text(json.dumps(checks,indent=2)+'\n')
print('COMPLETE',json.dumps(checks),flush=True)
