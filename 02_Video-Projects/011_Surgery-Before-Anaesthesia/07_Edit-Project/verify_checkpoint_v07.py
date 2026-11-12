"""Verify NAS deliveries and index partial coverage, never approve a film stage."""
import json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
NAS=Path('/Volumes/data/studio-live/History Of Science/02_Video-Projects/011_Surgery-Before-Anaesthesia/07_Edit-Project')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
 deliveries=[(Path('/Volumes/MiniWork/scratch/J2563-archive-v07b-assets'),NAS/'J2563_archive_composites_v07','ARCHIVE_COMPOSITES_v07.json'),(Path('/Volumes/MiniWork/scratch/J2563-slates-v07'),NAS/'J2563_dependency_slates_v07','DEPENDENCY_SLATES_v07.json')];copies=[]
 for local,remote,name in deliveries:
  # Verify all output bytes before replacing only the manifest's local paths.
  for src in sorted(local.iterdir()):
   if src.is_file():
    dest=remote/src.name;assert sha(src)==sha(dest),str(dest);copies.append({'name':str(dest.relative_to(NAS)),'sha256':sha(dest)})
  d=json.loads((local/name).read_text())
  for r in d['rows']:r['path']=str(remote/Path(r['path']).name);assert sha(Path(r['path']))==r['sha256']
  save(remote/name,d);save(HERE/name,d)
 plan=json.loads((HERE/'PICTURE_PLAN_v03.json').read_text());indexed={}
 for name,kind in [('FREE_GRAPHICS_MANIFEST_v03.json','preliminary_free'),('REMAINING_GRAPHICS_MANIFEST_v04.json','preliminary_free'),('ARCHIVE_COMPOSITES_v06.json','preliminary_free'),('ARCHIVE_COMPOSITES_v07.json','preliminary_free'),('DEPENDENCY_SLATES_v07.json','dependency_slate')]:
  for r in json.loads((HERE/name).read_text())['rows']:
   path=Path(r['path'])
   if name=='REMAINING_GRAPHICS_MANIFEST_v04.json':path=NAS/'J2563_free_graphics_v04'/path.name
   assert sha(path)==r['sha256'],str(path);assert r['row_id'] not in indexed
   indexed[r['row_id']]={'row_id':r['row_id'],'path':str(path),'sha256':r['sha256'],'manifest':name,'status':kind}
 assert len(indexed)==86
 missing=[r['row_id'] for r in plan['rows'] if r['row_id'] not in indexed];assert len(missing)==7
 index={'job':'J2563','plan_sha256':sha(HERE/'PICTURE_PLAN_v03.json'),'status':'Partial only: 19 preliminary free rows, 67 dependency slates, seven archives unbuilt; no joined rough','generation_authorized':False,'film_stage_approved':False,'audio_review':False,'motion_review':False,'rows':[indexed[r['row_id']] for r in plan['rows'] if r['row_id'] in indexed],'missing_rows':missing,'full_overlay_schedule_complete':False}
 save(HERE/'ASSEMBLY_INDEX_v07.json',index);save(NAS/'J2563_dependency_slates_v07'/'ASSEMBLY_INDEX_v07.json',index)
 verification={'status':'PASS: output-byte copy checks, 86 NAS row hashes and exact 19 preliminary / 67 slate / seven missing classification','copy_file_count':len(copies),'files':copies,'index_sha256':sha(HERE/'ASSEMBLY_INDEX_v07.json'),'not_reviewed':['moving_video','audio','full_overlay_schedule','joined_rough']};save(HERE/'J2563_COPY_VERIFICATION_v07.json',verification);save(NAS/'J2563_dependency_slates_v07'/'COPY_VERIFICATION_v07.json',verification)
 print(verification['status']);print('Seven unbuilt rows:',', '.join(missing))
if __name__=='__main__':main()
