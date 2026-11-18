"""Create auditable overlay candidates; unresolved prose never becomes an active cue."""
import argparse, hashlib, json, pathlib, re
HERE=pathlib.Path(__file__).resolve().parent

def norm(t):return re.sub(r'[^a-z0-9]+','',t.lower())

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=pathlib.Path);args=ap.parse_args()
 p=json.loads((HERE/'PICTURE_PLAN_v03.json').read_text());raw=HERE.parent/p['vo_lock']['stt_raw'];stt=json.loads(raw.read_text())
 words=[dict(w,raw_index=i) for i,w in enumerate(stt['words']) if w['type']=='word'];tokens=[norm(w['text']) for w in words]
 # Anchors are exact Scribe token sequences, not inferred speech or listening.
 anchors={
 ('P1:01a','when'):'Before 1846',('P1:01b','label'):'fastest',('P1:02a','when'):'Europe and America',
 ('P1:03a','who'):'Robert Liston',('P1:04a','when'):'autumn of 1846',('P1:05a','label'):'glass globe',('P1:08a','when'):'1840',('P1:09c','when'):'nearly fifty years earlier',
 ('P2:02a','who'):'Humphry Davy',('P2:02a','when'):'1800 in Bristol',('P2:02b','label'):'nitrous oxide',('P2:06a','when'):'next morning',('P2:07a','who'):'Crawford Long',
 ('P2:09b_arch_long_1849','when'):'another seven years',('P3:02a','who'):'Horace Wells',('P3:02a','when'):'December 1844',('P3:03a','when'):'The next day',
 ('P3:05a','who'):'William Morton',('P3:05b','label'):'ether',('P3:08a','who'):'John Collins Warren',('P4:04a','who'):'Oliver Wendell Holmes',
 ('P4:04c_cg_anesthesia_etymology','label'):'anesthesia',('P4:05b','who'):'Charles Jackson',('P4:09a','fact'):"doesn't name a single one of them",('P5:02a','when'):'21st of December 1846 in London',
 ('P5:04b','who'):'James Young Simpson',('P5:05a','label'):'chloroform',('P5:06b','who'):'John Snow',('P5:09a','when'):'Today',('P5:11a','label'):'anesthetist'}
 # Text reductions use only supported spoken detail. Full sourced WHO biographies remain intact.
 text_overrides={('P1:01a','when'):'Before 1846',('P1:01b','label'):'FASTEST',('P1:04a','when'):'Autumn 1846',('P1:05a','label'):'GLASS GLOBE',('P1:09c','when'):'Nearly fifty years earlier',('P2:06a','when'):'The next morning',('P2:09b_arch_long_1849','when'):'Seven years later',('P3:02a','when'):'December 1844',('P3:03a','when'):'The next day',('P4:09a','fact'):'No claimant named',('P5:02a','when'):'London, 21 December 1846'}
 cues=[];held=[]
 for r in p['rows']:
  for kind,text in r['markers'].items():
   if kind not in ('who','when','data','fact','label'):continue
   item={'row_id':r['row_id'],'kind':kind,'planned_text':text,'row_window_s':[r['in_s'],r['out_s']]}
   anchor=anchors.get((r['row_id'],kind))
   if anchor is None:
    held.append(dict(item,status='held',reason='Visual prose needs supported word anchor and reconciliation; not scheduled.'));continue
   target=[norm(t) for t in anchor.split()];matches=[i for i in range(len(tokens)-len(target)+1) if tokens[i:i+len(target)]==target]
   if not matches:
    held.append(dict(item,status='held',reason='Exact Scribe anchor absent: '+anchor));continue
   # Prefer the closest occurrence to its planned row. Names at first mention use global first occurrence.
   i=matches[0] if kind=='who' else min(matches,key=lambda n:abs(words[n]['start']-r['in_s']))
   j=i+len(target)-1;start=words[i]['start'];end=round(min(start+(3.2 if kind=='who' else 2.0),p['vo_lock']['duration_s']),3)
   item.update(anchor_text=' '.join(w['text'] for w in words[i:j+1]),word_indices=list(range(i,j+1)),raw_stt_indices=[w['raw_index'] for w in words[i:j+1]],evidence_window_s=[start,words[j]['end']],in_s=start,out_s=end,text=text_overrides.get((r['row_id'],kind),text),status='candidate_requires_layout_review')
   item['actual_row_id']=next(x['row_id'] for x in p['rows'] if x['in_s']<=start<x['out_s'])
   if item['actual_row_id']!=r['row_id']:item['reconciliation']='Moved to actual spoken evidence; immutable plan unchanged.'
   cues.append(item)
 # Conflicts are held, never resolved by silently delaying spoken synchronization.
 cues.sort(key=lambda c:c['in_s']);active=[]
 for cue in cues:
  conflict=next((c for c in active if c['in_s']<cue['out_s'] and cue['in_s']<c['out_s']),None)
  if conflict:
   cue.update(status='held',reason='One-label conflict with '+conflict['row_id']+'/'+conflict['kind']);held.append(cue)
  else:active.append(cue)
 # Credits carry immutable source references. These intervals reserve the archive row;
 # actual credit placement is held if a WHO card crosses the row (notably Snow).
 manifest=json.loads((args.out/'ASSEMBLY_SOURCES_v01.json').read_text());credits=[]
 for asset in manifest['assets']:
  if asset['role']!='archive':continue
  r=next(x for x in p['rows'] if x['row_id']==asset['row_id'])
  conflicts=[c['row_id']+'/'+c['kind'] for c in active if c['in_s']<r['out_s'] and r['in_s']<c['out_s']]
  credits.append({'row_id':r['row_id'],'kind':'archive_credit','text':asset['credit'],'in_s':r['in_s'],'out_s':r['out_s'],'source_asset':asset['asset_id'],'page_url':asset['page_url'],'status':'held_layout_conflict' if conflicts else 'candidate_requires_source_review','conflicts':conflicts,'word_indices':[i for i,w in enumerate(words) if r['in_s']<=w['start']<r['out_s']]})
 result={'job':'J2563','status':'partial_candidates_not_render_ready','stt_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'word_index_basis':'zero-based filtered type=word list; raw_stt_indices also recorded','candidates':active,'held':held,'archive_credit_candidates':credits,'checks':{'active_candidate_overlaps':0,'no_candidate_precedes_anchor_word':all(c['in_s']==words[c['word_indices'][0]]['start'] for c in active),'unresolved_candidates':len(held),'film_stage_pass':False},'render_notes':['No E2 experiment approval for 011.','WHO Liston moves to first spoken name at 371.48 s, not 14.28 s.','WHO Snow moves from P5:06b to archive P5:07a; credit/WHO layout remains held.','P1:04b stopwatch, P2:07b timeline, master timeline and stadium need per-element reconciliation; inherited prose is not a cue schedule.','Never render held items or regard candidates as finished QA.']}
 (args.out/'OVERLAY_CANDIDATES_v01.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
 print(f"{len(active)} nonoverlapping anchored candidates; {len(held)} held; {len(credits)} archive credit intervals. Not render-ready.")
if __name__=='__main__':main()
