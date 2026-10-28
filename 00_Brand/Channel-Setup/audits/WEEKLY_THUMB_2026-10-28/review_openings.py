import json
from pathlib import Path
r=Path(__file__).resolve().parent
obs={
'-3L6HzJ_d_4':('FLASK STAYS','Flask clearly visible; caption sits at top rather than vertically centred (§3.3).'),
'-I_GHK-GcFs':('THE FIRST TEST','Centred readable caption; no gold/yellow hook word visible (§3.3).'),
'4WUs0beKn0A':('NOT THE FIRST','Cow visible and centred readable caption; no gold/yellow hook word visible (§3.3).'),
'AMSriTQ-lcQ':('STILL RADIOACTIVE','Caption at top rather than centred; pictured vessels do not clearly show the titled notebooks (§3.1,3.3).'),
'BW_CFAX-mxc':('NOT A PUMP','Torso/furnace visible, centred readable cream/yellow hook; static frame checks consistent.'),
'PFj6172YU4Q':('ONE TIGHT BAND','Arm/band visible, centred readable cream/yellow hook; static frame checks consistent.'),
'Rl2uZ-KOTl8':('MORE THAN YOU HAVE','Torso visible, four-word centred cream/yellow hook; static frame checks consistent.'),
'oKqmnJNGiHg':('BOILING URINE FOR GOLD','Vessel visible, four-word cream/yellow hook; top placement differs from centred rule (§3.3).'),
'pWySvZsneZg':('IT CAME BACK','Gold foil visible, centred cream/yellow hook; generic words do not name gold but match spoken event.'),
'qW2OsD4mujc':('NOT ELEMENTS','Earth/fire/air/water scene, centred cream/yellow hook; static frame checks consistent.'),
'xHnIi9GqOsM':('ONE WAY','Valve illustration visible, centred cream/yellow hook; static frame checks consistent.')}
rows=json.load(open(r/'recovered/frame0_manifest.json'))
for x in rows:
 x['overall_opening_status']='UNVERIFIED: motion, VO and opening-repeat checks not performed in this still audit'
 if x.get('registryHashMatches'):
  x['caption'],x['static_observation']=obs[x['id']]
 else:x['static_observation']='Not accepted as current uploaded opening: missing source or upload hash mismatch.'
(r/'opening_still_review.json').write_text(json.dumps(rows,indent=2)+'\n')
