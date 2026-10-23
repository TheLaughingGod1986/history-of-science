from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
im=Image.open(ROOT/'00_Brand/Channel-Setup/style/long/001_how_did_we_discover_germs.jpg').convert('RGB')
# Reuse the approved painted art and Explorer; replace the old title area only.
patch=im.crop((320,385,570,720)).resize((580,375)).filter(ImageFilter.GaussianBlur(14))
patch=ImageEnhance.Brightness(patch).enhance(0.55)
im.paste(patch,(0,0))
d=ImageDraw.Draw(im)
font='/System/Library/Fonts/Supplemental/Didot.ttc'
for word,y,colour in [('FLASK',70,'#f6e8c6'),('PROOF',200,'#e8b94c')]:
 f=ImageFont.truetype(font,112)
 box=d.textbbox((0,0),word,font=f)
 x=(560-(box[2]-box[0]))/2
 d.text((x+2,y+3),word,font=f,fill='#553919',stroke_width=2)
 d.text((x,y),word,font=f,fill=colour,stroke_width=1,stroke_fill='#aa8750')
d.line((65,55,505,55),fill='#ba944e',width=2)
d.line((65,350,505,350),fill='#ba944e',width=2)
im.save(OUT/'compilation_thumb_v01.jpg',quality=95)
