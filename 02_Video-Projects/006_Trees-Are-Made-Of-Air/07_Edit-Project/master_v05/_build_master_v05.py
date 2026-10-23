#!/usr/bin/env python3
"""J0886: replace exactly four existing shot windows; retain v04 audio verbatim.
Run only AFTER motion review writes MOTION_REVIEW_v05.json with accepted=true
and matching hashes for all four clips. No automated visual approval.
"""
import json,subprocess as sp,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
OLD=Path('/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/master_v04')
ITEMS={2:'02_balance_trunk_v05',17:'05_pure_water_v05',50:'17_notebook_tick_v05',61:'10_only_green_v05'}
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def main():
 review=json.loads((HERE/'MOTION_REVIEW_v05.json').read_text())
 cuts=json.loads((OLD/'cuts_full_join_v04.json').read_text())
 cmd=['ffmpeg','-y','-v','warning','-i',str(OLD/'hos_006_master_v04.mp4')]
 filters=['[0:v]setpts=PTS-STARTPTS[v0]']
 for k,(num,sid) in enumerate(ITEMS.items(),1):
  src=HERE/'clips'/f'{sid}.mp4';h=sha(src)
  assert review[sid]['accepted'] is True and review[sid]['sha256']==h,'Motion review required'
  row=cuts[num-1];start=round(row['timeline_in']*24);end=round(row['timeline_out']*24)
  cmd+=['-i',str(src)]
  filters += [f'[{k}:v]fps=24,scale=1920:1080:flags=lanczos,setsar=1,trim=end_frame={end-start},setpts=PTS-STARTPTS+{start}/(24*TB)[r{k}]',f"[v{k-1}][r{k}]overlay=eof_action=pass:repeatlast=0:enable='between(n,{start},{end-1})'[v{k}]"]
  row.update(source=src.name,source_path=str(src),source_sha256=h,framing={'offset':0.0},upscale=1.0,disposition=f'J0886 fresh Flow motion replacement, visual evidence in MOTION_REVIEW_v05.json')
 out=HERE/'hos_006_master_v05.mp4'
 cmd+=['-filter_complex',';'.join(filters),'-map','[v4]','-map','0:a:0','-c:a','copy','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-frames:v','12764','-r','24','-movflags','+faststart',str(out)]
 sp.run(cmd,check=True)
 (HERE/'cuts_full_join_v05.json').write_text(json.dumps(cuts,indent=2)+'\n')
 pool=json.loads((OLD/'pool_full_join_v04.json').read_text())
 for num,sid in ITEMS.items():pool.append({'file':sid+'.mp4','part':cuts[num-1]['part'],'title':'HOS 006 J0886 fresh 3D cartoon replacement; pending Chief review'})
 (HERE/'pool_full_join_v05.json').write_text(json.dumps(pool,indent=2)+'\n')
 # Inherit only existing waivers; no new waivers or PASS decisions.
 (HERE/'picture_qa_reviewed_ok_v05.json').write_bytes((OLD/'picture_qa_reviewed_ok_v04.json').read_bytes())
 (HERE/'SHA256_master_v05.txt').write_text(sha(out)+'  '+out.name+'\n')
 # Prove the encoded audio payload is identical to v04, with no VO/music/SFX alteration.
 hashes=[]
 for p in [OLD/'hos_006_master_v04.mp4',out]:
  hashes.append(sp.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-'],text=True).strip())
 assert hashes[0]==hashes[1],'Audio stream changed'
 (HERE/'AUDIO_IDENTITY_v05.txt').write_text('\n'.join(hashes)+'\n')
 print('Built v05: original audio identical; four picture windows replaced. Gates still required.')
if __name__=='__main__':main()
