import json,hashlib
from pathlib import Path
r=Path(__file__).resolve().parent;m=json.load(open('/Users/benjaminoats/_desk/j1107/short_covers/manifest.json'))
# Observed in Studio Thumbnail-section captures, not inferred from Data API images.
obs='''-3L6HzJ_d_4|How Did We Discover Germs?|FAIL|Film frame with tiny serif title; lacks large 2–4-word rounded cover hook (§4.2,4.4).
-I_GHK-GcFs|THE FIRST TEST|FAIL|Serif film-frame caption, centred rather than rounded top-third cover; generic hook (§4.2,4.4,2.B.1).
-sa2t7dAtCk|EACH ATOM|FAIL|Serif film-frame caption over the object, not house cover typography (§4.2,4.4).
29bpGAI0wb8|HOW SO SMALL?|FAIL|Readable house-style cover, but question does not name its subject (§2.B.1).
4WUs0beKn0A|NOT THE FIRST|FAIL|Serif film-frame caption, generic hook, no rounded top-third cover (§4.2,4.4,2.B.1).
8_Edn_HCi1s|YOU ARE THE VECTOR|PASS|Readable chunky gold/cream/teal stack, pointing hand subject and small Explorer; audit advice only.
AMSriTQ-lcQ|1898 / Po / polonium|FAIL|Mid-film label frame; no readable title-hook cover (§4.1–4.4).
BW_CFAX-mxc|IS THE HEART A PUMP?|FAIL|Good house typography and clear torso, but 5-word hook exceeds 2–4 words (§4.2); preserve J1113.
CnHwX1L9XHg|GALLIUM IN THE GAP|PASS|House reference: clear top stack and isolated droplet; audit advice only.
H1y0DXFVmw8|AN ENEMY WITH NO SHADOW|FAIL|5-word hook exceeds 2–4 words (§4.2), although style and topic read clearly.
LCZRHUyTiq0|J. J. THOMSON / Cambridge, 1897|FAIL|Mid-film person card; no large rounded title-hook cover (§4.1–4.4).
LanTHJckYx8|WHAT OTHER TABLE HAS GAPS?|FAIL|5-word question; table/chairs riddle remains abstract (§4.2,1.5).
OnJ8MFu0Mi0|Still blamed bad air|FAIL|Film frame with tiny subtitle, no title-hook cover (§4.1–4.4).
PFj6172YU4Q|ONE TIGHT BAND|PASS|Clear band/arm hero and top-third house lettering; preserve J1113.
Rl2uZ-KOTl8|MORE THAN YOU HAVE|PASS|Four-word readable house stack matches title hook; preserve J1113.
TbMMJSRKC3U|EVERY EIGHTH ELEMENT?|PASS|Three-word subject question, clear top stack and small Explorer.
c2q7w0pgcn8|sunlight with a prism|FAIL|Film frame and tiny subtitle, not a title-hook cover (§4.1–4.4).
clV6E10NLPw|THE CARBOLIC SPRAY|PASS|House reference lettering, subject spray clear below top band.
iqToagXnjX0|A DROP IS NOT EMPTY|FAIL|5 words exceeds cover length (§4.2), though subject/house style clear.
nFQRWmpulTQ|HE PREDICTED A METAL|PASS|Four-word title hook, gold/cream/teal top stack and metal hero.
nba0-f7PPeU|TELLURIUM BEFORE IODINE|PASS|Three-word house reference cover with clear separate objects.
oKqmnJNGiHg|to a black sludge|FAIL|Film frame and tiny subtitle, no title-hook cover (§4.1–4.4).
oowAOWTBoq0|HOW X-RAYS WERE DISCOVERED BY ACCIDENT|FAIL|Six words and cramped small first line (§4.2).
pWySvZsneZg|GOLD THREW IT BACK|PASS|Four-word readable house stack, foil hero; preserve J1113.
qOZgess30h0|What else is still invisible?|FAIL|Five-word mid-frame plain subtitle and vague question (§4.2,4.4,2.B.1).
qW2OsD4mujc|FOUR ELEMENTS WERE WRONG|PASS|Four-word house stack matches title hook, clear painted scene; preserve J1113.
sILtQxgYQk8|A FLASK LIKE A QUESTION MARK|FAIL|Six-word cover exceeds length (§4.2), despite correct house family.
uU12JA5rMWg|THE EMPTY WERE THE CHAIRS|FAIL|Five-word malformed phrase does not make a clear title hook (§4.1,4.2).
xHnIi9GqOsM|DOORS IN VEINS|FAIL|Readable serif film-frame caption rather than rounded top-third cover (§4.2,4.4).
x_3L_IdYgEc|HE NEVER SAW THIS|FAIL|Generic teaser in serif film-frame caption (§2.B.1,4.2,4.4).
xvanpsLeADE|SEE BONES WITHOUT CUTTING|FAIL|Four readable words and clear subject, but plain gold lettering lacks the rounded cream/gold/teal house cover treatment (§4.4).
zI_eD3vFWmE|THE FIRST X-RAY SHOWED A WEDDING RING|FAIL|Seven-word cover with small first line (§4.2).'''
by={}
for line in obs.splitlines():
 id,words,score,note=line.split('|');by[id]={'words':words,'advisory_style':score,'style_note':note}
assert set(by)=={x['id'] for x in m}
for x in m:
 assert hashlib.sha256(Path(x['image']).read_bytes()).hexdigest()==x['sha256']
 x.update(by[x['id']]);x['authority']='Worker visual audit only; Chief approval not granted';x['frame0_verified']=False
(r/'short_cover_review.json').write_text(json.dumps(m,indent=2)+'\n')
for x in m:
 inv=json.load(open(r/'inventory.json'))
 # Saved inventory enriched only in this evidence branch; no live state changed.
 for v in inv['videos']:
  if v['id']==x['id']:v.update(advisory_style=x['advisory_style'],style_note=x['style_note'],studio_cover_image=x['image'],studio_cover_sha256=x['sha256'])
 (r/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
print('Reviewed',len(m),'Studio covers;',sum(x['advisory_style']=='PASS' for x in m),'advisory compliant,',sum(x['advisory_style']=='FAIL' for x in m),'style mismatches')
