import json,pathlib,subprocess,concurrent.futures,hashlib
P=pathlib.Path(__file__).parent;R=pathlib.Path('/Users/benjaminoats/YouTube/History Of Science');M=pathlib.Path('/Users/benjaminoats/_desk/J1107/2026-10-28')
reg=json.load(open(R/'00_Brand/Channel-Setup/social/UPLOADS.json'))['videos'];vs=json.load(open(P/'inventory_api.json'))['videos']
def frame(v):
 if 'M' in v['contentDetails']['duration'] or (v['status']['privacyStatus']!='public' and not v['status'].get('publishAt')):return None
 vid=v['id'];r=reg.get(vid,{});f=r.get('file');src=(R/f if f else None)
 if not src or not src.exists():return {'id':vid,'status':'UNVERIFIED','reason':'registered media unavailable' if f else 'no registry entry','registeredPath':f}
 out=M/(vid+'_frame0.jpg');p=subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(src),'-frames:v','1','-q:v','2','-y',str(out)],capture_output=True,timeout=35)
 return {'id':vid,'status':'extracted' if p.returncode==0 else 'UNVERIFIED','source':str(src),'frame':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest() if out.exists() else None,'note':'Local registered media; live upload identity still requires hash matching to upload receipt'}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:r=[x for x in ex.map(frame,vs) if x]
(P/'frame0_manifest.json').write_text(json.dumps(r,indent=2));print('Frames:',sum(x['status']=='extracted' for x in r),'of',len(r))
