import json,pathlib,re,statistics
P=pathlib.Path(__file__).parent
vs=[v for v in json.load(open(P/'inventory_api.json'))['videos'] if v['status']['privacyStatus']=='public' or v['status'].get('publishAt')]
s=(P/'studio_advanced_28days.txt').read_text();s=s[s.rfind('Total\n2,297'):];parts=re.split(r'\n\d{1,2}:\d{2}\n',s)[1:];bytitle={v['snippet']['title']:v for v in vs};metrics={}
for block in parts:
 lines=block.strip().splitlines();title=lines[0];v=bytitle.get(title)
 if not v:raise ValueError('Unmatched Studio title: '+title)
 imp=int(lines[-2].replace(',',''));ctr=float(lines[-1].rstrip('%'));metrics[v['id']]={'impressions':imp,'ctrPct':ctr,'views':None if lines[1]=='—' else int(lines[1].replace(',','')),'engagedViewsFromImpressions':None}
for v in vs:
 id=v['id'];f=P/f'studio_{id}_28days.txt'
 if id in metrics and f.exists():
  m=re.search(r'Engaged views from impressions\n([\d,]+)',f.read_text())
  if m:metrics[id]['engagedViewsFromImpressions']=int(m[1].replace(',',''))
med={kind:statistics.median([metrics[v['id']]['ctrPct'] for v in vs if v['id'] in metrics and ('long' if 'M' in v['contentDetails']['duration'] else 'short')==kind]) for kind in ['long','short']}
(P/'metrics_28days.json').write_text(json.dumps({'period':'2026-09-30 to 2026-10-27','source':'Studio Advanced mode table; Reach funnel for long engaged views from impressions','medianCtrPct':med,'medianDefinition':'Unweighted per-video median among videos with observed impressions and numeric CTR; missing rows excluded, not zero. No inference of statistical significance.','metrics':metrics},indent=2))
longs={
'_C92tIJCk8A':('PASS','Approved reference family; legacy full-title text exempt under §2.5. Phone subject and gold GERMS readable.','running T009'),
'AL_-qlWko_g':('PASS','Approved reference family; legacy full-title text exempt under §2.5. PERIODIC TABLE is small at 168 px; improvement opportunity, not a CTR verdict.','finished 11 Oct; watch-time shares unavailable, A visible'),
'frP_YrNShsU':('FAIL','§2.2–3: Explorer occupies right hero area; hero X-ray object is small. Legacy title text itself is exempt. Preserve active test.','running T001; about 2h54 left at read-back'),
'GHZDsiH7L7A':('PASS','Approved reference family; legacy title text exempt. Atom silhouette and INSIDE AN ATOM readable.','running title/thumbnail test; about 23h14 left; absent from ledger'),
'wwcjcFfC-5M':('PASS','ONE TIGHT BAND readable; cream/gold serif left; hand and band right, small Explorer left.','prearmed/ineligible until public'),
'VbPubYd6Fbs':('FAIL','§2.2: tree hero too small relative to frame; WOOD FROM SKY readable but composition can emphasise the tree.','prearmed/ineligible title and thumbnail variants'),
'ETynHpIYLeY':('FAIL','§2.B.1: THE MILKMAIDS SECRET is a teaser rather than concrete subject/dare; cream top line tiny at 168 px.','prearmed/ineligible title and thumbnail variants'),
'uAomPaOBrM8':('FAIL','§2.2: multiple competing hero objects; 6 EXPERIMENTS is a catalogue label, weak concrete promise. Tiny text at 168 px.','no running badge seen; verify test UI before any arm')}
shortnotes={
'H1y0DXFVmw8':'§4.2: AN ENEMY WITH NO SHADOW is five words; readable family style.',
'iqToagXnjX0':'§4.2: A DROP IS NOT EMPTY is five words; readable family style.',
'8_Edn_HCi1s':'§4.1: YOU ARE THE VECTOR substitutes jargon for title hook germs/ride; reduce decoding.',
'sILtQxgYQk8':'§4.2: A FLASK LIKE A QUESTION MARK is six words; semantic riddle.',
'uU12JA5rMWg':'§4.1: empty chairs is an abstract table metaphor; title also lacks a concrete discovery question.',
'nFQRWmpulTQ':'Cover matches title hook; four words; readable family style.',
'CnHwX1L9XHg':'Cover matches title hook; four words; readable family style.',
'nba0-f7PPeU':'Cover matches title hook; three words; readable family style.',
'LanTHJckYx8':'§4.2 and §2.B.1: WHAT OTHER TABLE HAS GAPS? is five words and vague.',
'oowAOWTBoq0':'§4.2: HOW X-RAYS WERE DISCOVERED BY ACCIDENT is six words; no teal middle word (§4.4).',
'xvanpsLeADE':'§4.4: chunky letters but no teal middle word; hook itself readable.',
'zI_eD3vFWmE':'§4.2: THE FIRST X-RAY SHOWED A WEDDING RING is seven words; tiny top line.',
'x_3L_IdYgEc':'§4.4: thin serif film-frame lettering instead of chunky rounded gold/cream cover; vague HE NEVER SAW THIS.',
'qOZgess30h0':'§2.B.1: WHAT ELSE IS STILL INVISIBLE? is vague; five words (§4.2).',
'-sa2t7dAtCk':'§4.4: thin serif film-frame lettering; EACH ATOM omits the theory hook.',
'29bpGAI0wb8':'§2.B.1: HOW SO SMALL? does not name gold/atom; family style otherwise readable.',
'TbMMJSRKC3U':'Cover readable; four words and question; standard family.',
'c2q7w0pgcn8':'§4.1: HEAT beyond RED is a physical hook, but omits title subject infrared; family otherwise clear.',
'clV6E10NLPw':'Cover readable; three words; standard family.',
'oKqmnJNGiHg':'§4.1: GLOW not GOLD omits phosphorus named in title; family otherwise clear.',
'-I_GHK-GcFs':'§4.4: thin serif film frame; THE FIRST TEST omits Jenner/vaccine, vague.',
'LCZRHUyTiq0':'§4.4: thin serif film frame; THE BEAM BENT readable but not custom-cover style.',
'4WUs0beKn0A':'§4.4: thin serif film frame; NOT THE FIRST vague relative to vaccine title.',
'Rl2uZ-KOTl8':'§4.2: MORE THAN YOU HAVE is four words; readable but §2.B.1 vague, no blood/heart named.',
'BW_CFAX-mxc':'§4.2: IS THE HEART A PUMP? five words; otherwise readable question and clear subject.',
'pWySvZsneZg':'§4.2: GOLD THREW IT BACK four words; clear subject and family style.',
'qW2OsD4mujc':'§4.2: FOUR ELEMENTS WERE WRONG four words; clear family style.',
'PFj6172YU4Q':'Clear hook, three words, family style; title lacks question requested by brief.',
'xHnIi9GqOsM':'§4.4: thin serif film frame; DOORS IN VEINS is analogy, title names valves.',
'OnJ8MFu0Mi0':'Readable three-word REMOVE the HANDLE; subject pump visible. Colour/outline family retained.',
'-3L6HzJ_d_4':'§4.4: thin serif film frame; FLASK STAYS is incomplete hook.',
'AMSriTQ-lcQ':'Readable BOOKS behind LEAD, three words; subject matches title.'}
shortpass={'nFQRWmpulTQ','CnHwX1L9XHg','nba0-f7PPeU','TbMMJSRKC3U','clV6E10NLPw','pWySvZsneZg','qW2OsD4mujc','PFj6172YU4Q','OnJ8MFu0Mi0','AMSriTQ-lcQ'}
rows=[]
for v in vs:
 id=v['id'];kind='long' if 'M' in v['contentDetails']['duration'] else 'short';title=v['snippet']['title']
 if kind=='long':score,note,test=longs[id]
 else:score='PASS' if id in shortpass else 'FAIL';note=shortnotes[id];test='not applicable to Shorts'
 rows.append({'id':id,'title':title,'format':kind,'publishAt':v['status'].get('publishAt',v['snippet']['publishedAt']),'state':'scheduled' if v['status'].get('publishAt') else 'public','style':score,'styleNote':note,'briefQuestionTitle':'PASS' if title.endswith('?') else 'FAIL' if kind=='short' else 'N/A','test':test,'metrics':metrics.get(id),'ctrVsFormatMedian':round(metrics[id]['ctrPct']-med[kind],2) if id in metrics else None,'statisticallyRankable':metrics.get(id,{}).get('impressions',0)>=1000})

for row in rows:
 if row['format']=='short' and row['state']=='scheduled':
  row['authorizationContext']='J1113: all ten scheduled Shorts set to frame-0 hooks 28 Oct 17:09, awaiting Chief review in OWB PR #320. Rubric mismatch is informational; do not reverse/queue duplicate cover work. API-served image may be cached; confirm Studio saved frame.'
(P/'assessment.json').write_text(json.dumps({'reviewer':'codex; advisory rubric scores, not Chief approval','rows':rows},indent=2))
print('metrics',len(metrics),'medians',med,'assessment',len(rows))
