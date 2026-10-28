import json,pathlib,re,math
from PIL import Image,ImageDraw,ImageFont,ImageOps
OUT=pathlib.Path(__file__).parent;MEDIA=pathlib.Path('/Users/benjaminoats/_desk/J1107/2026-10-28')
vs=[v for v in json.load(open(OUT/'inventory_api.json'))['videos'] if v['status']['privacyStatus']=='public' or v['status'].get('publishAt')]
f=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',12)
for kind in ['long','short']:
 rows=[v for v in vs if ('short' if not re.search(r'[HM]',v['contentDetails']['duration'][2:]) or (re.search(r'PT(\d+)M',v['contentDetails']['duration']) and int(re.search(r'PT(\d+)M',v['contentDetails']['duration'])[1])<3) else 'long')==kind]
 # This channel's Shorts are all under 40 seconds; longs over 3 min.
 rows.sort(key=lambda x:x['snippet']['publishedAt'])
 for part in range(0,len(rows),12):
  group=rows[part:part+12];sheet=Image.new('RGB',(4*260,math.ceil(len(group)/4)*205),(238,238,238));d=ImageDraw.Draw(sheet)
  for i,v in enumerate(group):
   x=(i%4)*260;y=(i//4)*205;p=MEDIA/(v['id']+'.jpg')
   im=Image.open(p);im=ImageOps.fit(im,(168,94));sheet.paste(im,(x,y))
   d.text((x,y+98),v['id'],font=f,fill='black');title=v['snippet']['title']
   for j in range(3): d.text((x,y+115+j*15),title[j*32:(j+1)*32],font=f,fill='black')
   d.text((x,y+163),v['status'].get('publishAt',v['status']['privacyStatus'])[:22],font=f,fill='black')
  sheet.save(MEDIA/f'{kind}_sheet_{part//12+1}.jpg')
 print(kind,len(rows))
