#!/usr/bin/env python3
"""Three scoped J2241 Quality first takes, with HOS009 shared account guards.
No automatic retry; existing submissions stop duplicate work. Never marks KEEP.
"""
import importlib.util,json,sys,os,subprocess,hashlib
from pathlib import Path
REPO=Path(__file__).resolve().parents[3]
EDIT=Path(__file__).resolve().parent
MEDIA=Path.home()/'YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin'
STATE=Path.home()/'_desk/state/flow/hos008-j2241'
OWB=Path.home()/'YouTube/orbit-with-ben'
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
g=load('j2241_guard',REPO/'02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project/_mint_flow_v05_tranche2.py')
ROWS=[
 ('02','02_salon_spark','aefd6338aded1037c11306a99fc580d1a62a66d9367409f01e0edd993cc8cc58',160,
  'In a warm eighteenth-century salon the lecturer rubs one solid sealed glass rod with silk, then draws one crisp spark to a guest’s knuckle. Fine hair tips lift gently in place on the guests’ heads. The rod remains solid glass, sealed and empty: nothing emerges from either end. No hair, smoke, cotton, fibres or material extruding from or detaching near the glass rod.'),
 ('03','01_points_desk','cc16a515a43e881c54a207eb2cb3f700ab9a4166bbb83a366dc09431db403e51',160,
  'At the eighteenth-century wooden laboratory desk the same mature grey-haired experimenter holds a pointed iron needle near the slowly spinning brass electrostatic globe. One single thin linen indicator thread hangs and deflects cleanly. The brass globe stays a solid rigid sphere. No paper strips, receipts, ribbons or material unrolling or emerging from the globe.'),
 ('05','13_rods_spread','84a92bf6ce1abd1a5780c37ac2e8ae50ea6099f5cff5c7f728a70060b394819c',135,
  'Eighteenth-century harbour with a church steeple, brick house roof and sailing ship mast. Straight rigid vertical iron lightning rods remain firmly anchored on the steeple, roof and ship mast. Gentle camera drift and small natural movement in water and sails. Every rod stays perfectly straight, upright, rigid and fixed throughout. No kinks, tilting, bending, detaching or falling rods.')]
def save(x):
 STATE.mkdir(parents=True,exist_ok=True);(STATE/'manifest.json').write_text(json.dumps(x,indent=2)+'\n')
def main():
 STATE.mkdir(parents=True,exist_ok=True)
 if (STATE/'manifest.json').exists():raise RuntimeError('Existing J2241 run: inspect manifest, never auto-repeat')
 sys.path.insert(0,str(REPO/'04_Audio/tools'));import orbit_flow_veo_ui as flow
 from playwright.sync_api import sync_playwright
 manifest={'job':'J2241','film':'HOS:008','status':'RUNNING','takes':[],'max_credits':900,'cash_gbp':0,'motion_review':'J2243 and Ben; no worker motion claim'}
 for part,pid,digest,minimum,prompt in ROWS:
  ref=MEDIA/f'04_Generated-Clips/part{part}/refs/v03_flow_stills/{pid}_t1.png'
  assert g.sha256_file(ref)==digest, f'Reference hash mismatch {pid}'
 save(manifest)
 with g.SharedFlowAccounting() as accounting:
  assert not accounting.snapshot()['pending'],'Shared pending submission blocks work'
  with sync_playwright() as pw:
   b=pw.chromium.connect_over_cdp('http://127.0.0.1:9222')
   page=g.open_flow_page(b,flow.FLOW_HOME,lambda p,u:p.goto(u,wait_until='domcontentloaded'))
   live=g.read_live_balance(page);accounting.reserve('J2241','HOS:008',900,live=live)
   manifest['preflight']={'live':live,'pending':False,'shared_liability':accounting.snapshot()['liability']};save(manifest)
   for part,pid,digest,minimum,prompt in ROWS:
    ref=MEDIA/f'04_Generated-Clips/part{part}/refs/v03_flow_stills/{pid}_t1.png'
    dest=MEDIA/f'04_Generated-Clips/part{part}/j2241/{pid}_j2241_t1.mp4';dest.parent.mkdir(parents=True,exist_ok=True)
    assert not dest.exists(),'Never overwrite output'
    entry={'part':part,'id':pid,'take':1,'reference_sha256':digest,'file':str(dest),'minimum_frames':minimum,'status':'PREPARING'};manifest['takes'].append(entry);save(manifest)
    charge=f'HOS:008:P{part}:{pid}:J2241:t1'
    def guard(p):
     bal=g.read_live_balance(p)
     g.read_live_evidence(p,balance=bal,open_overlay=True)
     record=g.guarded_create(p,accounting,reservation='J2241',charge=charge,evidence_path=STATE/f'{pid}_create.json',balance=bal)
     entry.update(status='SUBMITTED',credits=100,charge=charge);save(manifest)
     accounting.export_ai_spend(OWB/'05_Analytics/ai_spend/ledger.jsonl',by='codex')
    info=flow.generate_clip(page,'History of Science premium 3D cartoon, warm cinematic period light. Animate the attached reference with its exact look. '+prompt+' Silent picture only. Continuous subject and camera motion through the final frame. No text, captions, letters, numbers, logos or UI.',dest,model='Veo 3.1 - Quality',start_frame=ref,timeout_s=700,attempts=1,reuse_project=False,create_guard=guard)
    entry['generation']=info;save(manifest)
    if not dest.exists():
     entry['status']='HARVEST_REQUIRED';save(manifest);raise RuntimeError('Generated take needs gallery harvest; do not resubmit')
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(dest)]))
    stream=next(s for s in probe['streams'] if s['codec_type']=='video');frames=int(stream['nb_read_frames'])
    subprocess.run(['ffmpeg','-v','error','-i',str(dest),'-f','null','-'],check=True)
    sheet=dest.with_suffix('.jpg')
    subprocess.run(['ffmpeg','-v','error','-i',str(dest),'-vf','fps=1,scale=320:-1,tile=4x2','-frames:v','1',str(sheet)],check=True)
    entry.update(status='GENERATED_PENDING_REVIEW',sha256=g.sha256_file(dest),frames=frames,width=stream['width'],height=stream['height'],frame_rate=stream['r_frame_rate'],sheet=str(sheet),decode_ok=True)
    save(manifest);assert frames>=minimum,'Too few decoded frames'
   accounting._event({'kind':'release','id':'J2241'})
 manifest['status']='GENERATED_PENDING_REVIEW';save(manifest)
 print('J2241 complete: three first takes; 300 credits; pending review',flush=True)
if __name__=='__main__':main()
