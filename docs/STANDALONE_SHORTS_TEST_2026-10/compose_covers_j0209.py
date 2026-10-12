#!/usr/bin/env python3
"""J0209: deterministic cover lettering over unchanged, approved plates.

Usage: python3 compose_covers_j0209.py --media-root '/path/to/HOS'
No network, generation, grading, background replacement or publishing.
"""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = Path('docs/STANDALONE_SHORTS_TEST_2026-10')
FONT = Path('/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf')
SPECS = [
    ('s1', 's1/01_beyond_red_v01.jpg', ['HEAT', 'beyond', 'RED'], 'Who Discovered Infrared Light?'),
    ('s2', 's2/01_glowing_flask_v01.jpg', ['GLOW', 'not', 'GOLD'], 'How Was Phosphorus Discovered?'),
    ('s3', 's3/05_handle_off_v03.jpg', ['REMOVE', 'the', 'HANDLE'], 'How Did John Snow Stop Cholera?'),
    ('s4', 's4/01_lead_box_v01.jpg', ['BOOKS', 'behind', 'LEAD'], "Are Marie Curie’s Notebooks Still Radioactive?"),
    ('s5', 's5/01_pigeons_horn_v01.jpg', ['BLAMED', 'the', 'PIGEONS'], 'How Was the Cosmic Microwave Background Discovered?'),
    ('s6', 's6/01_mouldy_dish_v01.jpg', ['SAVED', 'by', 'MOULD'], 'How Was Penicillin Discovered?'),
    ('s7', 's7/01_candle_jar_v01.jpg', ['MINT', 'fixed', 'AIR'], 'Who Discovered That Plants Produce Oxygen?'),
    ('s8', 's8/01_tall_tube_v01.jpg', ['BLOOD', 'eight feet', 'UP'], 'Who First Measured Blood Pressure?'),
]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def lettering(word, height, width, top, bottom):
    font = ImageFont.truetype(str(FONT), 300)
    bounds = font.getbbox(word)
    mask = Image.new('L', (bounds[2]-bounds[0]+24, bounds[3]-bounds[1]+24))
    ImageDraw.Draw(mask).text((12-bounds[0], 12-bounds[1]), word, font=font, fill=255)
    mask = mask.filter(ImageFilter.MaxFilter(15))
    # Per-line display lettering; width capped at the live cover's 85–90% span.
    natural = round(mask.width * height / mask.height)
    mask = mask.resize((width if height == 155 else min(width, natural), height), Image.Resampling.LANCZOS)
    pad = 20
    m = Image.new('L', (mask.width+2*pad, mask.height+2*pad))
    m.paste(mask, (pad, pad))
    layer = Image.new('RGBA', m.size)
    outline = m.filter(ImageFilter.MaxFilter(19))
    shadow = Image.new('L', m.size)
    shadow.paste(outline, (0, 7))
    layer.paste((28, 16, 10, 255), (0, 0), shadow)
    layer.paste((45, 26, 15, 255), (0, 0), outline)
    grad = Image.new('RGBA', m.size)
    d = ImageDraw.Draw(grad)
    for y in range(grad.height):
        t = max(0, min(1, (y-pad)/max(1,height-1)))
        colour = tuple(round(a+(b-a)*t) for a,b in zip(top,bottom))
        d.line((0,y,grad.width,y), fill=(*colour,255))
    layer.paste(grad, (0,0), m)
    return layer

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--media-root', type=Path, required=True)
    ap.add_argument('--manifest', type=Path, default=Path(__file__).with_name('COVERS_J0209_v01.json'))
    ap.add_argument('--only', nargs='+', choices=[row[0] for row in SPECS], default=['s1', 's2', 's3', 's4'])
    ap.add_argument('--job', default='J0209')
    ns = ap.parse_args()
    out = ns.media_root/BASE/'covers_j0209_v01'
    out.mkdir(parents=True, exist_ok=True)
    records=[]
    for sid, plate, words, title in SPECS:
        if sid not in ns.only:
            continue
        src=ns.media_root/BASE/'plates_v01'/plate
        original=Image.open(src).convert('RGB')
        assert original.size == (1080,1920), (src, original.size)
        canvas=original.convert('RGBA')
        # The entire letter stack is above y=520. Hero objects begin below it.
        entries=[]
        for word, y, height, maxwidth, top, bottom in [
            (words[0],55,155,920,(255,244,212),(228,200,143)),
            (words[1],245,65,430,(136,221,204),(61,152,150)),
            (words[2],345,145,920,(255,214,111),(201,134,40)),
        ]:
            # S8's tube mounting reaches the top band: keep the lower
            # two lines in its clear left edge, without altering the plate.
            if sid == 's8' and y > 55:
                maxwidth = 360
                height = 60 if y == 245 else 115
            if sid == 's5' and y == 345:
                y = 320
            layer=lettering(word,height,maxwidth,top,bottom)
            x=45 if sid == 's8' and y > 55 else (1080-layer.width)//2
            canvas.alpha_composite(layer,(x,y-20))
            entries.append({'word':word,'box':[x,y-20,x+layer.width,y-20+layer.height]})
        final=canvas.convert('RGB')
        assert final.crop((0,530,1080,1920)).tobytes() == original.crop((0,530,1080,1920)).tobytes()
        dest=out/f'hos_sa_{sid}_cover_v01.png'
        final.save(dest)
        records.append({'id':sid,'title':title,'draft_words':' '.join(words),'plate':str(src.relative_to(ns.media_root)), 'plate_sha256':sha(src),'cover':str(dest.relative_to(ns.media_root)), 'cover_sha256':sha(dest),'size':[1080,1920],'lettering':entries,'pixels_below_y530_unchanged':True,'approval':'pending Chief HOOK / BAND / PHONE'})
    ns.manifest.write_text(json.dumps({'job':ns.job,'status':'draft for Chief','font':str(FONT),'font_sha256':sha(FONT),'media_root':str(ns.media_root),'covers':records},indent=2)+'\n')
    print(f'Created {len(records)} drafts: {out}')

if __name__=='__main__':
    main()
