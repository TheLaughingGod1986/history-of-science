"""J0204: deterministic, no-spend HOS compilation graphics over moving masters.
Requires ffmpeg, Pillow, numpy, and macOS Didot. Media stays outside git.
"""
import argparse, hashlib, json, subprocess as sp
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W,H,FPS=1920,1080,30
FONT='/System/Library/Fonts/Supplemental/Didot.ttc'
CREAM=(255,244,218,255)
DATES=['1628','1779','1860s','1869','1895','1911']
NAMES=['HARVEY','INGENHOUSZ','PASTEUR','MENDELEEV','RÖNTGEN','RUTHERFORD']
TITLES=['The Hidden Circle','Built From Air','The Invisible Enemy','The Empty Chairs','A Light Through Skin','Inside the Atom']
def font(n): return ImageFont.truetype(FONT,n,index=1)
def layer(): return Image.new('RGBA',(W,H))
def text(im,xy,s,size): ImageDraw.Draw(im).text(xy,s,font=font(size),fill=CREAM,anchor='mm',stroke_width=0)
def ease(x):
    x=max(0,min(1,x)); return x*x*(3-2*x)
def reveal(im,t,start,fade,ink=False):
    p=ease((t-start)/.5)*fade
    if p<=0:return layer()
    out=im.copy()
    a=np.array(out.getchannel('A'))
    if ink:
        # A soft left-to-right ink reveal, not a camera push on a card.
        ramp=np.clip((p*2100-np.arange(W))/180,0,1)
        a=(a*ramp[None,:]).astype('uint8')
    else:a=(a*p).astype('uint8')
    out.putalpha(Image.fromarray(a));return out

def render(out,scratch,spec):
    name,duration,film,offset,count,old,title=spec
    path=out/(name+'.mp4'); source=scratch/f'film_{film}_norm.mp4'
    layers=[]; ticks=[]
    if title:
        ink=layer(); d=ImageDraw.Draw(ink)
        text(ink,(960,430),'HISTORY OF SCIENCE',32)
        text(ink,(960,550),title,100)
        d.line((650,650,1270,650),fill=CREAM,width=2)
        layers=[(ink,.2,True)]; ticks=[.2]
    else:
        base=layer(); d=ImageDraw.Draw(base)
        text(base,(960,290),'Finding the invisible world',68)
        d.line((190,550,1730,550),fill=CREAM,width=3)
        layers=[(base,0,True)]
        for i in range(count):
            im=layer(); d=ImageDraw.Draw(im); x=230+i*292
            above=i%2==0
            d.line((x,550,x,480 if above else 620),fill=CREAM,width=3)
            d.ellipse((x-7,543,x+7,557),fill=CREAM)
            text(im,(x,420 if above else 680),DATES[i],62)
            text(im,(x,470 if above else 730),NAMES[i],32)
            start=.15 if i<old else .6+(i-old)*.65
            layers.append((im,start,False))
            if i>=old:ticks.append(start)
    # Blurred moving source supplies continuous motion; warm grade lifts shadows.
    filt='scale=1920:1080,boxblur=12:2,colorchannelmixer=rr=.34:rg=.33:rb=.16:gr=.23:gg=.28:gb=.12:br=.16:bg=.18:bb=.12,lutrgb=r=val+48:g=val+30:b=val+18,fps=30,format=rgb24'
    dec=sp.Popen(['ffmpeg','-v','error','-ss',str(offset),'-i',str(source),'-t',str(duration),'-vf',filt,'-f','rawvideo','-'],stdout=sp.PIPE)
    enc=sp.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate','30','-i','-','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(path)],stdin=sp.PIPE)
    minmean=999; minp95=999
    try:
        for k in range(round(duration*FPS)):
            raw=dec.stdout.read(W*H*3)
            if len(raw)!=W*H*3:raise RuntimeError('Background ended early')
            frame=Image.frombytes('RGB',(W,H),raw).convert('RGBA');t=k/FPS
            fade=1-ease((t-(duration-.5))/.5)
            for im,start,ink in layers:frame=Image.alpha_composite(frame,reveal(im,t,start,fade,ink))
            frame=frame.convert('RGB');enc.stdin.write(frame.tobytes())
            if k%15==0:
                g=np.array(frame.convert('L'));minmean=min(minmean,float(g.mean()));minp95=min(minp95,float(np.percentile(g,95)))
            if k==round((duration-.7)*FPS):frame.save(out/(name+'.jpg'),quality=92)
    finally:
        enc.stdin.close();dec.stdout.close()
    if enc.wait()!=0 or dec.wait()!=0:raise RuntimeError('ffmpeg failed')
    return dict(file=path.name,duration=duration,fps=FPS,width=W,height=H,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),background=str(source),background_offset=offset,tick_ink_seconds=ticks,minimum_sample_mean_luma=round(minmean,2),minimum_sample_p95=round(minp95,2),near_black='PASS' if minmean>=28 and minp95>=50 else 'FAIL',note='Tick cues relative to this clip; new markers only. No audio baked in. Ordinal milestones, not a linear year scale.')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--scratch',type=Path,default=Path('/private/tmp/hos_comp_v01'));args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    specs=[('code_graphic_comp_timeline_b1',3.5,'005',287.6,1,0,None),('code_graphic_comp_timeline_b3',4,'002',131.5,3,1,None),('code_graphic_comp_timeline_b5',4,'004',260,5,3,None),('code_graphic_comp_timeline_close',4,'004',310,6,5,None)]
    for i,(film,offset) in enumerate([('005',287.6),('002',134),('001',300),('002',162.3),('003',95.5),('004',252)]):specs.append((f'code_graphic_comp_card_{i+1:02}',3,film,offset,0,0,TITLES[i]))
    results=[]
    for spec in specs:
        print('Rendering',spec[0],flush=True);results.append(render(args.out,args.scratch,spec))
    (args.out/'GRAPHICS_MANIFEST_v01.json').write_text(json.dumps(results,indent=2)+'\n')
    sheet=Image.new('RGB',(1280,5*400),(35,28,23));d=ImageDraw.Draw(sheet)
    for i,r in enumerate(results):
        im=Image.open(args.out/r['file'].replace('.mp4','.jpg'));im.thumbnail((640,360));x=(i%2)*640;y=(i//2)*400;sheet.paste(im,(x,y));d.text((x+10,y+366),r['file'].replace('code_graphic_comp_',''),font=font(22),fill='white')
    sheet.save(args.out/'COMPILATION_GRAPHICS_STILLS_v01.jpg',quality=93)
    print('Rendered',len(results),'clips',flush=True)
if __name__=='__main__':main()
