#!/usr/bin/env python3
"""J1241: code graphics v03 — £0 Pillow/ffmpeg FIX of 4 Chief rows from v02.

Writes to a fresh --out directory (never overwrite v02). Changes ONLY:
P2:15 likeness_fire, P3:03 rod_cloud, P3:04 letter_crosses, P3:15 wet_dry
(Acting Chief Claude ruling J1218, 30 Oct). Word beats from locked STT records.
Other rows stay byte-identical copies of v02. No generation, downloads, paid APIs.
"""
from pathlib import Path
import argparse, hashlib, json, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
W,H,FPS=1920,1080,30
CREAM=(244,228,195,255); GOLD=(211,167,88,255); BLUE=(149,194,214,255)
FONT='/System/Library/Fonts/Supplemental/Didot.ttc'
ROOT=Path(__file__).resolve().parent

def ease(t,a,b):
    p=max(0,min(1,(t-a)/(b-a)));return p*p*(3-2*p)

def path(draw, pts, p=1, color=CREAM, width=5):
    if p<=0:return
    lengths=[math.dist(a,b) for a,b in zip(pts,pts[1:])];left=sum(lengths)*min(p,1)
    for a,b,L in zip(pts,pts[1:],lengths):
        if left<=0:break
        q=min(1,left/max(L,.001));draw.line([a,(a[0]+q*(b[0]-a[0]),a[1]+q*(b[1]-a[1]))],fill=color,width=width);left-=L

def oval(d,box,color=CREAM,width=5):d.ellipse(box,outline=color,width=width)
def cloud(d,x,y,t):
    pts=[(x+i*5,y-28*math.sin(i*.085)-19*math.sin(i*.19)) for i in range(100)]
    path(d,pts);path(d,[(x,y),(x+40,y+55),(x+450,y+55),(x+495,y)])
def key(d,x,y):
    oval(d,(x-38,y-38,x+38,y+38),GOLD,9)
    path(d,[(x,y+38),(x,y+145),(x+55,y+145),(x+55,y+125)],color=GOLD,width=10)
def roof(d,x,y,s=1,p=1):
    path(d,[(x-180*s,y+120*s),(x,y-80*s),(x+180*s,y+120*s),(x-180*s,y+120*s)],p,GOLD,7)
    for z in [-100,-50,0,50,100]:path(d,[(x+z*s,y+120*s),(x,y-60*s)],p,CREAM,3)
def tower(d,p=1):
    path(d,[(760,870),(760,550),(900,300),(1040,550),(1040,870),(760,870)],p)
    path(d,[(760,550),(1040,550)],p,GOLD)
    for y in range(590,860,48):
        path(d,[(765,y),(1035,y)],p,(161,131,94,255),2)
        for x in range(790+(24 if y%96 else 0),1030,72):path(d,[(x,y),(x,y+45)],p,(161,131,94,255),2)
    path(d,[(840,865),(840,730),(960,730),(960,865)],p)
def dots(d,pts,t,start=0,end=100):
    if not start<=t<=end:return
    for i in range(16):
        q=((i/16+(t-start)*.23)%1);j=q*(len(pts)-1);k=min(int(j),len(pts)-2);u=j-k
        x=pts[k][0]*(1-u)+pts[k+1][0]*u;y=pts[k][1]*(1-u)+pts[k+1][1]*u
        oval(d,(x-5,y-5,x+5,y+5),GOLD,4)

def stroke_text(d, xy, label, font, alpha, stroke_w=4):
    fill=(*CREAM[:3], round(255*alpha))
    sc=(* (36,22,12), round(230*alpha))
    d.text(xy, label, font=font, fill=fill, anchor='mm', stroke_width=stroke_w, stroke_fill=sc)

def graphic(name,t,duration,label, alpha_layer=False):
    """alpha_layer=True omits opaque scene scaffolding that blocks KEEP plates."""
    im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
    p=ease(t,0,1.2)
    if name=='likeness_pairs':
        # J1193: colour beat first, crooked traces on spoken crooked-lines beat.
        path(d,[(960,330),(960,875)],ease(t,0,.4),GOLD,3)
        oval(d,(340,520,590,565),GOLD,8);path(d,[(340,540),(340,790),(590,790),(590,540)],p,CREAM,6);oval(d,(340,765,590,810),GOLD,7);path(d,[(465,540),(465,420)],p,GOLD,8);path(d,[(355,640),(575,640),(575,770),(355,770),(355,640)],p,GOLD,4)
        cloud(d,1190,420,t)
        # colour glow rings on jar & cloud ~0.4–1.8s
        if 0.4 <= t <= 1.8:
            a=ease(t,.4,.7)*(1-ease(t,1.5,1.8))
            for r_ring in (40,70,100):
                oval(d,(465-r_ring,540-r_ring,465+r_ring,540+r_ring),BLUE,4)
                oval(d,(1400-r_ring,450-r_ring,1400+r_ring,450+r_ring),BLUE,4)
        spark=[(0,0),(65,55),(20,110),(90,170),(50,220)]
        # crooked traces timed to "moved in crooked lines" (~2.9–3.9s)
        for x,start in [(465,2.90),(1400,3.10)]:
            path(d,[(x+a,430+b) for a,b in spark],ease(t,start,start+.55),BLUE,9)
            if t>start:
                dots(d,[(x,430),(x+20,500),(x+50,560)],t,start,start+1.2)
    elif name=='likeness_fire':
        # Chief J1218 FIX 30 Oct: jagged crack / flicker flame / tipped animal.
        # Locked STT: crack@0.80, fire@2.40, kill@3.40, animals@3.66.
        if not alpha_layer:
            path(d,[(250,360),(1670,360),(1670,900),(250,900),(250,360)],ease(t,.35,.7),GOLD,3)
        oval(d,(420,720,650,790),GOLD);path(d,[(530,720),(530,660)],p)
        if not alpha_layer:
            roof(d,1330,650)
        if t >= 0.80:
            crack=[(480,780),(505,705),(455,645),(515,560),(470,490),(530,420)]
            path(d,crack,ease(t,0.80,1.15),GOLD,9)
            path(d,[(505,705),(555,675),(575,610),(600,545)],ease(t,0.90,1.25),CREAM,5)
        if t >= 2.40:
            x=1330; flick=10*math.sin(t*12)
            flame=[(x-45,730),(x-60+flick,650),(x-18,585),(x+flick,495),(x+28,555),(x+55+flick,650),(x+40,730),(x-45,730)]
            path(d,flame,ease(t,2.40,2.75),GOLD,7)
            path(d,[(x,705),(x+flick*0.7,605),(x-6,535)],color=CREAM,width=6)
            path(d,[(x-18,690),(x-35+flick,615),(x-8,555)],ease(t,2.50,2.90),GOLD,4)
        if t >= 3.40:
            ax,ay=960,780; tip=ease(t,3.40,3.70)*40
            animal=[(ax-55,ay-tip),(ax-15,ay-35-tip),(ax+45,ay-18-tip),(ax+60,ay+12-tip),(ax+15,ay+28-tip),(ax-40,ay+22-tip),(ax-55,ay-tip)]
            path(d,animal,1.0,GOLD,5)
            path(d,[(ax-28,ay+22-tip),(ax-48,ay+58-tip)],1.0,GOLD,4)
            path(d,[(ax+12,ay+28-tip),(ax+30,ay+62-tip)],1.0,GOLD,4)
            path(d,[(ax-90,ay-70),(ax-10,ay-125),(ax+50,ay-85)],ease(t,3.40,3.75),BLUE,6)
            oval(d,(ax-14,ay-138,ax+14,ay-110),GOLD,5)
    elif name=='rod_cloud':
        # Chief FIX: thin pointed iron rod on roof; stream to tip; spark on pull sparks.
        # Locked STT: rod@2.84, pull@3.34, sparks@3.68.
        if not alpha_layer:
            tower(d,p)
            path(d,[(1040,405),(1130,365),(1220,405)],p,GOLD,5)
        tip_y=248
        path(d,[(1130,385),(1130,tip_y)],ease(t,2.50,2.95),GOLD,6)
        if t >= 2.70:
            path(d,[(1118,tip_y+28),(1130,tip_y),(1142,tip_y+28)],ease(t,2.70,3.00),CREAM,4)
        if not alpha_layer:
            cloud(d,650+16*math.sin(t*.3),218,t)
        dots(d,[(780,245),(890,275),(1000,265),(1130,tip_y)],t,3.20,6.5)
        if t >= 3.34:
            for ang in range(0,360,40):
                rad=math.radians(ang+t*50)
                path(d,[(1130,tip_y),(1130+30*math.cos(rad),tip_y+30*math.sin(rad))],ease(t,3.34,3.75),BLUE,4)
            oval(d,(1116,tip_y-14,1144,tip_y+14),GOLD,5)
    elif name=='letter_crosses':
        # ILLUSTRATIVE only (source correction stands). Chief FIX: filled land + place labels.
        # Locked STT: crossed@1.90, ocean@2.44.
        LAND=(120,88,55,210)
        west_poly=[(250,370),(340,395),(410,450),(470,505),(490,565),(455,635),(400,715),(355,795),(425,870),(530,910),(270,930),(210,800),(190,600),(215,450),(250,370)]
        britain_poly=[(1375,255),(1485,245),(1525,305),(1490,365),(1415,375),(1375,320),(1375,255)]
        france_poly=[(1395,395),(1530,385),(1590,455),(1565,565),(1480,625),(1410,585),(1375,500),(1395,395)]
        fa=ease(t,.25,.75)
        if fa>0:
            d.polygon(west_poly, fill=(*LAND[:3], round(LAND[3]*fa)))
            d.polygon(britain_poly, fill=(*LAND[:3], round(LAND[3]*fa)))
            d.polygon(france_poly, fill=(*LAND[:3], round(LAND[3]*fa)))
        path(d,west_poly+[west_poly[0]],ease(t,.25,.85),GOLD,4)
        path(d,britain_poly,ease(t,.3,.9),GOLD,4)
        path(d,france_poly+[france_poly[0]],ease(t,.3,.9),GOLD,4)
        phil=(455,545); paris=(1465,470)
        oval(d,(phil[0]-12,phil[1]-12,phil[0]+12,phil[1]+12),GOLD,6)
        lab=ImageFont.truetype(FONT,28,index=1)
        if t>=0.55:
            stroke_text(d,(phil[0],phil[1]-38),'PHILADELPHIA',lab,ease(t,.55,.95)*(1-ease(t,3.35,3.65)), stroke_w=2)
        route=[phil,(700,470),(980,430),(1200,470),paris]
        for i in range(50):
            q=i/49
            if q<=ease(t,1.90,2.90):
                j=q*4;k=min(int(j),3);u=j-k;x=route[k][0]*(1-u)+route[k+1][0]*u;y=route[k][1]*(1-u)+route[k+1][1]*u
                oval(d,(x-3,y-3,x+3,y+3),GOLD,4)
        if t>=2.50:
            oval(d,(paris[0]-12,paris[1]-12,paris[0]+12,paris[1]+12),GOLD,6)
            stroke_text(d,(paris[0],paris[1]-38),'PARIS',lab,ease(t,2.50,2.85)*(1-ease(t,3.35,3.65)), stroke_w=2)
    elif name=='wet_dry':
        # Chief FIX: wet twine one colour with flowing charge; dry silk different; dots stop at silk.
        # Locked STT: Wet@-0.08/0.00, dry@2.72, silk@3.16, would not@3.66/3.90.
        WET=(149,194,214,255); DRY=(211,167,88,255)
        if not alpha_layer:
            cloud(d,710,240,t)
        for rx in range(740,1180,55):
            for ry in (320,420,520,620):
                phase=(t*40+rx*0.1+ry*0.05)%70
                path(d,[(rx,ry+phase),(rx-12,ry+32+phase)],1.0,BLUE,3)
        path(d,[(640,300),(640,740)],ease(t,0,.8),(161,131,94,255),6)
        for yy in range(340,720,36):
            path(d,[(622,yy),(658,yy+16)],ease(t,.1,.8),(161,131,94,255),3)
        path(d,[(960,300),(960,590)],ease(t,0,.8),WET,11);key(d,960,625)
        for yy in range(320,580,28):
            oval(d,(944,yy-6,976,yy+6),WET,3)
        silk=[(960,700),(1045,745),(1025,825),(935,865),(870,800),(915,740),(960,700)]
        path(d,silk,ease(t,0,.8),DRY,10)
        if t>0.45:
            d.polygon(silk, fill=(*DRY[:3], 95))
        if t < 2.72:
            dots(d,[(960,300),(960,600),(960,690)],t,0.8,5.3)
        else:
            dots(d,[(960,300),(960,600)],t,0.8,5.3)
            path(d,[(900,720),(1020,720)],ease(t,2.72,3.05),DRY,8)
            if 3.66 <= t <= 4.40:
                oval(d,(930,700,990,760),GOLD,6)
    elif name=='same_thing':
        for seg_y in range(320,880,48):
            path(d,[(960,seg_y),(960,seg_y+28)],ease(t,.2,.7),GOLD,5)
        oval(d,(360,520,610,565),GOLD,8);path(d,[(360,540),(360,790),(610,790),(610,540)],p,CREAM,6);oval(d,(360,765,610,810),GOLD,7)
        path(d,[(485,540),(485,410)],p,GOLD,8);oval(d,(465,375,505,415),GOLD,6)
        for yy in range(600,760,28):
            path(d,[(380,yy),(590,yy)],p,(161,131,94,255),3)
        cloud(d,1180,410,t)
        roof(d,1420,780,0.75,p)
        spark=[(0,0),(55,48),(15,98),(75,150),(35,205)]
        path(d,[(485+a,415+b) for a,b in spark],ease(t,.5,1.2),BLUE,8)
        path(d,[(1380+a,430+b) for a,b in spark],ease(t,.8,1.5),BLUE,8)
        for r_ring in (45,85,125):
            oval(d,(960-r_ring,580-r_ring,960+r_ring,580+r_ring),GOLD,4)
    elif name=='teach_charge':
        if not alpha_layer:
            cloud(d,380,280,t)
        kite=[(720,450),(815,535),(720,620),(650,535),(720,450)]
        path(d,kite,p);path(d,[(720,450),(720,620)],p);path(d,[(650,535),(815,535)],p)
        if not alpha_layer:
            roof(d,1350,740,.8,p);path(d,[(1206,836),(1206,960),(1494,960),(1494,836)],p)
        path(d,[(720,620),(1140,830)],p);key(d,1140,850)
        dots(d,[(720,620),(930,725),(1140,830)],t,1.2,7.1)
        # ghost bolt cancellation on "never struck"
        if 1.2 <= t <= 2.0:
            a=ease(t,1.2,1.4)*(1-ease(t,1.8,2.0))
            bolt=[(900,200),(860,320),(920,400),(880,520)]
            path(d,bolt,1.0,BLUE,5)
            # X mark
            path(d,[(820,280),(980,480)],1.0,GOLD,6)
            path(d,[(980,280),(820,480)],1.0,GOLD,6)
        # continuous light rain
        for rx in range(300,1600,70):
            phase=(t*35+rx)%90
            path(d,[(rx,200+phase),(rx-10,240+phase)],1.0,BLUE,2)
    elif name=='looking_path':
        # Alpha: leaders only (no baked roof/tower/cloud over KEEP plate).
        if not alpha_layer:
            cloud(d,710,250,t)
            roof(d,520,780,0.85,p);tower(d,p);roof(d,1380,790,0.8,p)
        # All leaders step downward (y increasing) — fix upward (1000,660)->(900,300).
        for pts,delay in [
            ([(960,290),(920,410),(1010,475),(955,570),(1000,660),(980,780)],0),
            ([(920,410),(790,480),(820,560),(730,650),(640,720)],.35),
            ([(1010,475),(1140,530),(1100,630),(1220,735),(1310,790)],.55),
            ([(790,480),(660,540),(580,630),(520,715)],.7),
            ([(1140,530),(1280,580),(1350,660)],.85),
        ]:
            path(d,pts,ease(t,.2+delay,2.4),GOLD,8)
            path(d,pts,ease(t,.3+delay,2.6),CREAM,4)
    elif name=='wood_vs_metal':
        if not alpha_layer:
            roof(d,490,600,1.2,p);tower(d,p)
        else:
            # light roof/tower outlines only
            roof(d,490,600,1.2,ease(t,0,0.9));tower(d,ease(t,0.9,1.9))
        # terrible path choke
        if 2.2 <= t <= 3.8:
            path(d,[(490,300),(460,370),(510,440),(490,530)],ease(t,2.2,2.8),BLUE,7)
        # flame on "bursts into flame" (~4.24–4.86)
        if t >= 4.2:
            x=490
            path(d,[(x-55,520),(x-75,450),(x-25,390),(x,330),(x+30,405),(x+65,450),(x+55,520),(x-55,520)],ease(t,4.2,4.7),GOLD,6)
            path(d,[(x,500),(x+12*math.sin(t*3),420),(x-5,385)],color=CREAM,width=5)
        # cracks on "cracks apart" (~5.2+)
        if t >= 5.2:
            for a in range(0,360,50):
                rad=math.radians(a);x,y=900,580
                pts=[(x,y),(x+60*math.cos(rad),y+60*math.sin(rad)),(x+90*math.cos(rad+.2),y+90*math.sin(rad+.2)),(x+140*math.cos(rad),y+140*math.sin(rad))]
                path(d,pts,ease(t,5.2,6.5),GOLD,6)
    elif name=='metal_easy':
        # Alpha: rod + current only — omit roof/tower/wall that blocked KEEP plate.
        if not alpha_layer:
            roof(d,540,620,0.9,p);tower(d,p)
            path(d,[(640,330),(520,330),(520,890),(640,890),(640,330)],ease(t,.15,.6),CREAM,5)
            for yy in range(360,880,32):
                path(d,[(530,yy),(580,yy+14),(630,yy-6)],ease(t,.2,.7),(161,131,94,255),3)
        path(d,[(1180,280),(1180,920)],ease(t,.25,1.6),GOLD,12)
        for yy in range(320,900,64):
            oval(d,(1156,yy-12,1204,yy+12),CREAM,4)
        if t>.3:
            path(d,[(1180,280),(1180,280+640*ease(t,.3,2.4))],color=CREAM,width=5)
            dots(d,[(1180,280),(1180,600),(1180,920)],t,.4,2.9)
    elif name=='safe_path':
        if not alpha_layer:
            tower(d,ease(t,0,1.3));path(d,[(580,890),(1320,890)],p,GOLD,3)
        conductor=[(900,250),(900,290),(1070,550),(1085,890),(1085,995)]
        path(d,conductor,p,GOLD,6)
        for y in range(920,1010,25):path(d,[(650,y),(1000,y)],p,(155,125,87,255),2)
        path(d,[(810,760),(900,585),(995,760),(810,760)],p,CREAM,4)
        path(d,conductor,ease(t,1.5,6.5),CREAM,10);dots(d,conductor,t,1.5,6.98)
    else:raise ValueError(name)
    # Label windows — same_thing holds ELECTRICITY through spoken word (+5.14s).
    if name=='same_thing':
        start,end=4.80, min(duration-0.15, 7.10)
    elif name=='rod_cloud':
        start,end=1.20, 5.20
    elif name in ('safe_path','teach_charge'):
        start,end=.6, 4.4
    else:
        start=.5; end=min(duration-.15,start+4)
    alpha=ease(t,start,start+.4)*(1-ease(t,max(start+.4,end-.4),end))
    font=ImageFont.truetype(FONT,66 if len(label)<29 else 58,index=1)
    stroke_text(d,(W/2,150),label,font,alpha, stroke_w=4)
    if name=='likeness_fire':im.putalpha(im.getchannel('A').point(lambda a:round(a*(1-ease(t,4.5,4.8)))))
    return im


def paper():
    rng=np.random.default_rng(8329);y,x=np.mgrid[:H,:W];v=np.clip(((x-W/2)/(W/2))**2+((y-H/2)/(H/2))**2,0,1.4)
    a=np.zeros((H,W,3));noise=rng.normal(0,1.2,(H,W))
    for c,base in enumerate((136,100,66)):a[:,:,c]=base-42*v+noise
    return Image.fromarray(np.uint8(np.clip(a,0,255))).convert('RGBA')

def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def writer(p,alpha):
    cmd=['ffmpeg','-v','error','-nostdin','-n','-f','rawvideo','-pix_fmt','rgba','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-an']
    cmd+=['-c:v','prores_ks','-profile:v','4','-pix_fmt','yuva444p10le','-threads','2'] if alpha else ['-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-threads','2']
    return subprocess.Popen(cmd+[str(p)],stdin=subprocess.PIPE)

def lock_label(keyid, spec):
    """Chief FIX, 16 Oct 2026: P5:11 is three words. A longer label must not render."""
    if not keyid.startswith('P5:11'):
        return spec
    spec=dict(spec)
    spec['label']='SAFE PATH DOWN'
    spec['animation']=spec['animation'].replace('A SAFE PATH TO THE GROUND','SAFE PATH DOWN')
    words=spec['label'].split()
    if len(words)>4:
        raise SystemExit(f'P5:11 label has {len(words)} words: {spec["label"]}')
    return spec

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--stills-only',action='store_true')
    ap.add_argument('--only',default='',help='render just this row prefix, e.g. P5:11')
    ap.add_argument('--replace',action='store_true',help='replace existing files')
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    specs=json.loads((ROOT/'PICTURE_PLAN_v03.json').read_text())['code_graphics'];bg=paper();records=[];thumbs=[]
    for part in range(2,6):
        boardpath=ROOT/f'parts/part-{part:02}_plates_v03.json';board=json.loads(boardpath.read_text())
        for row in board['plates']:
            keyid=f"P{part}:{row['id']}"
            if keyid not in specs:continue
            spec=lock_label(keyid, specs[keyid]);name=row['id'].split('_',1)[1];duration=row['use_s'];frames=math.ceil(duration*FPS);overlay=spec['layout_mode']=='moving_plate_overlay'
            preview=args.out/spec['file'];alpha=preview.with_suffix('.mov');jpg=preview.with_suffix('.jpg');mid=min(2.7,duration*.75)
            selected=not args.only or keyid.startswith(args.only)
            if not selected:
                if not jpg.exists():
                    raise SystemExit(f'--only needs the existing still {jpg.name}')
                thumbs.append((keyid, Image.open(jpg).convert('RGB')));continue
            still=Image.alpha_composite(bg,graphic(name,mid,duration,spec['label'], alpha_layer=False)).convert('RGB');still.save(jpg);thumbs.append((keyid,still.copy()))
            record=dict(row=keyid,film_start_s=row['t_s'],part_start_s=round(row['t_s']-board['vo_film_start_s'],3),use_s=duration,encoded_s=frames/FPS,vo_land=row['vo_land'],vo_file=board['vo_file'],vo_sha256=board['vo_sha256'],spec=spec,preview=preview.name,alpha=alpha.name if overlay else None,composite_pending=overlay,board_sha256=digest(boardpath))
            if not args.stills_only:
                if preview.exists() or (overlay and alpha.exists()):
                    if not args.replace:
                        raise RuntimeError(f'Refusing overwrite: {preview}')
                    preview.unlink(missing_ok=True)
                    if overlay:alpha.unlink(missing_ok=True)
                proc=writer(preview,False);aproc=writer(alpha,True) if overlay else None
                for frame in range(frames):
                    layer_paper=graphic(name,frame/FPS,duration,spec['label'], alpha_layer=False)
                    proc.stdin.write(Image.alpha_composite(bg,layer_paper).tobytes())
                    if aproc:
                        layer_a=graphic(name,frame/FPS,duration,spec['label'], alpha_layer=True)
                        aproc.stdin.write(layer_a.tobytes())
                for p in (proc,aproc):
                    if p:p.stdin.close();assert p.wait()==0
                probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(preview)]));v=probe['streams'][0]
                assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(W,H,'30/1',frames)
                assert not any(s.get('codec_type')=='audio' for s in probe['streams'])
                record['technical_check']='1920x1080 / 30fps / expected frame count / no audio verified'
                record['label_words']=len(spec['label'].split())
            records.append(record);print(keyid, spec['label'], 'rendered' if not args.stills_only else 'still', flush=True)
    if args.only:
        manifest_path=args.out/'MANIFEST.json'
        existing=json.loads(manifest_path.read_text()) if manifest_path.exists() else []
        by={r['row']:r for r in records}
        merged=[]
        seen=set()
        for old in existing:
            merged.append(by.get(old['row'], old));seen.add(old['row'])
        merged.extend(r for r in records if r['row'] not in seen)
        records=merged
    sheet=Image.new('RGB',(1440,math.ceil(len(thumbs)/3)*310),(45,33,23));d=ImageDraw.Draw(sheet)
    for i,(label,img) in enumerate(thumbs):
        x=(i%3)*480;y=(i//3)*310;sheet.paste(img.resize((480,270)),(x,y));d.text((x+12,y+278),label,fill='white',font=ImageFont.truetype(FONT,22,index=1))
    sheet.save(args.out/'CONTACT_SHEET.jpg');(args.out/'MANIFEST.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
    files=sorted(p for p in args.out.iterdir() if p.is_file() and p.name!='SHA256SUMS.txt');(args.out/'SHA256SUMS.txt').write_text(''.join(f'{digest(p)}  {p.name}\n' for p in files))

if __name__=='__main__':main()
