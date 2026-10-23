#!/usr/bin/env python3
"""J0886: bounded Flow motion batch. One submission per plate; never blindly retry."""
import json,os,sys,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
SHARED=Path('/Users/benjaminoats/YouTube/History Of Science')
sys.path[:0]=[str(SHARED/'04_Audio/tools'),str(SHARED/'02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project')]
import orbit_flow_veo_ui as flow
import _mint_flow_cdp_v01 as helper
from playwright.sync_api import sync_playwright
ITEMS=[
 ('02_balance_trunk_v05',10,'Veo 3.1 - Fast','The balance beam gently rocks by a tiny amount while willow leaves flutter naturally. The entire willow and its compact root ball remain firmly supported INSIDE the LEFT brass weighing pan at every frame. Roots never float or leave the pan. Soil stays settled in the right pan. Static camera, no morphing, no falling soil.'),
 ('05_pure_water_v05',10,'Veo 3.1 - Fast','Jan Baptist van Helmont gently waters the small willow growing from soil in the CENTER of this terracotta pot. Keep trunk planted in the pot, continuous connection from trunk to soil inside the pot. Very small realistic water trickle through lid holes. Both arms attached to the visible man. Gentle leaf movement, stable camera, no tree motion or morphing.'),
 ('17_notebook_tick_v05',10,'Veo 3.1 - Fast','Joseph Priestley sits at his desk and makes one simple tick with his quill in the notebook. His head, torso, shoulder, elbow, forearm and wrist remain visibly connected throughout, both arms attached to the body. Natural small breathing and hand movement. Stable medium wide framing. No floating or detached hands. No new writing other than a small tick.'),
 ('10_only_green_v05',100,'Veo 3.1 - Quality','Static camera. Tiny oxygen bubbles slowly rise ONLY UNDERWATER from the submerged green leaf in the RIGHT glass jar. Each bubble disappears immediately AT THE WATER SURFACE, well below the jar rim. The air above the water and outside all jars remains completely empty at every frame. No bubbles above water, no droplets, spray, steam or particles. Left root and middle flower remain submerged and produce no bubbles. Very gentle water shimmer, retain the exact three jars and objects.')
]
LOG=HERE/'FLOW_MOTION_LOG_v05.json'
def save(doc):LOG.write_text(json.dumps(doc,indent=2)+'\n')
def main():
 doc=json.loads(LOG.read_text()) if LOG.exists() else {'job':'J0886','cap_credits':400,'takes':{},'balance_reads':[]}
 (HERE/'clips').mkdir(exist_ok=True)
 with sync_playwright() as pw:
  browser=pw.chromium.connect_over_cdp(helper.CDP);page=helper.flow_page(browser,flow)
  for sid,cost,model,action in ITEMS:
   if sid in doc['takes']:
    if doc['takes'][sid]['status']!='PENDING_VISUAL_REVIEW':raise SystemExit('STOP recover uncertain prior generation: '+sid)
    print('SKIP downloaded prior take',sid,flush=True);continue
   balance,account=helper.read_account(page)
   if account!=helper.REQUIRED or balance is None:raise SystemExit('STOP account/balance gate')
   reserved=sum(t['cost_reserved'] for t in doc['takes'].values())
   if reserved+cost>400 or balance<cost:raise SystemExit('STOP credit cap or live balance')
   if helper.UNPAID_RE.search(helper.body_text(page)):raise SystemExit('STOP billing banner')
   still=HERE/'stills'/f'{sid}.png';assert still.exists()
   dest=HERE/'clips'/f'{sid}.mp4'
   entry={'cost_reserved':cost,'credits_before':balance,'model':model,'prompt':helper.LOOK+' '+action,'start_frame':str(still),'start_frame_sha256':helper.sha256(still),'submitted_at':helper.now(),'status':'SUBMITTING_DO_NOT_RETRY'}
   doc['takes'][sid]=entry;save(doc)
   os.environ['ORBIT_FLOW_VEO_MODEL']=model
   os.environ['OWB_FLOW_FILM']='HOS:006'
   print('SUBMIT',sid,model,'reserved',reserved+cost,flush=True)
   try:
    info=flow.generate_clip(page,entry['prompt'],dest,model=model,start_frame=still,timeout_s=600,reuse_project=False,attempts=1) or {}
    entry['info']=info
    if not dest.exists():raise RuntimeError('No downloaded clip; recover existing generation before any new take')
    import orbit_gemini_veo as veo
    veo.strip_audio(dest)
    helper.contact_sheet(dest,HERE/f'{sid}_motion_sheet.jpg')
    entry.update(status='PENDING_VISUAL_REVIEW',file=str(dest),sha256=helper.sha256(dest),duration_s=helper.duration(dest),freeze_events_0p8s=helper.freeze_events(dest))
   except Exception as e:
    entry.update(status='STOP_RECOVER_EXISTING_GENERATION',error=str(e));save(doc);raise
   after,account=helper.read_account(page);entry['credits_after']=after
   doc['balance_reads'].append({'at':helper.now(),'credits':after,'after':sid});save(doc)
   if after is None or balance-after>cost:raise SystemExit('STOP unexpected credit charge')
 print('ALL FOUR MOTION TAKES READY FOR REVIEW',flush=True)
if __name__=='__main__':main()
