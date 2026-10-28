"""Mechanical coding, with OCR explicitly unverified; human subject/composition coding stays pending."""
import json,pathlib,subprocess,concurrent.futures,re
import numpy as np
from PIL import Image
P=pathlib.Path(__file__).parent;M=pathlib.Path('/Users/benjaminoats/_desk/J1107/competitors');s=json.load(open(P/'competitors.json'))['samples'];vs={v['id']:v for r in s for k in ['fast','slow'] for v in r[k]}
def code(v):
 p=M/(v['id']+'.jpg');row={'id':v['id'],'title':v['title'],'titleCharacters':len(v['title']),'titleShape':'question' if '?' in v['title'] else ('number' if re.search(r'\d',v['title']) else 'statement'),'thumbnailTextSource':'Tesseract OCR; not manually verified','subject':'PENDING human coding','composition':'PENDING human coding','curiosityGap':'PENDING human coding','hookWord':'PENDING human coding','textSizeColour':'PENDING human coding'}
 if p.exists():
  im=Image.open(p).convert('RGB');w,h=im.size
  if w/h<1.7:im=im.crop((0,(h-w*9/16)/2,w,(h+w*9/16)/2))
  a=np.asarray(im);lum=a.mean(axis=2);row.update({'meanLuma':round(float(lum.mean()),2),'lumaStd':round(float(lum.std()),2),'nearBlackPct':round(float((lum<30).mean()*100),2)})
  r=subprocess.run(['tesseract',str(p),'stdout','--psm','11'],capture_output=True,text=True,timeout=20);row['thumbnailWordsOCR']=r.stdout.strip()
 return row
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:rows=list(ex.map(code,vs.values()))
(P/'competitor_coding.json').write_text(json.dumps(rows,indent=2));print(len(rows),'mechanically coded; manual fields explicitly pending')
