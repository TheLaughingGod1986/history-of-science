import json,pathlib,urllib.request,concurrent.futures,hashlib,math
from PIL import Image,ImageOps,ImageDraw,ImageFont
P=pathlib.Path(__file__).parent;M=pathlib.Path('/Users/benjaminoats/_desk/J1107/competitors');M.mkdir(parents=True,exist_ok=True)
s=json.load(open(P/'competitors.json'))['samples'];vs={v['id']:v for r in s for k in ['fast','slow'] for v in r[k]}
def dl(v):
 p=M/(v['id']+'.jpg');t=v['thumbnails'];u=next(t[k]['url'] for k in ['high','medium','default'] if k in t)
 try:
  with urllib.request.urlopen(u,timeout=20) as r:b=r.read()
  p.write_bytes(b);return {'id':v['id'],'path':str(p),'url':u,'sha256':hashlib.sha256(b).hexdigest()}
 except Exception as e:return {'id':v['id'],'error':type(e).__name__}
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:manifest=list(ex.map(dl,vs.values()))
(P/'competitor_thumbnail_manifest.json').write_text(json.dumps(manifest,indent=2))
f=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',12)
for r in s:
 for group in ['fast','slow']:
  rows=r[group]
  if not rows:continue
  im=Image.new('RGB',(5*220,math.ceil(len(rows)/5)*175),'#eeeeee');d=ImageDraw.Draw(im)
  for i,v in enumerate(rows):
   x=i%5*220;y=i//5*175;p=M/(v['id']+'.jpg')
   if p.exists():
    pic=Image.open(p);w,h=pic.size
    # high thumbnail has 4:3 letterboxing; show the central 16:9 area.
    if w/h<1.7:pic=pic.crop((0,(h-w*9/16)/2,w,(h+w*9/16)/2))
    im.paste(ImageOps.fit(pic,(168,94)),(x,y))
   d.text((x,y+96),v['id']+' '+str(int(v['viewsPerDay']))+'/day',font=f,fill='black')
   for n in range(3):d.text((x,y+113+15*n),v['title'][n*30:(n+1)*30],font=f,fill='black')
  im.save(M/f"{r['channel']}_{r['format']}_{group}.jpg")
print('Saved',len(manifest),'competitor thumbnails and sheets')
