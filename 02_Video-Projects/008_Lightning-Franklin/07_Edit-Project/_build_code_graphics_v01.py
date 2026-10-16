#!/usr/bin/env python3
"""J0329: deterministic £0 Pillow/ffmpeg period-ink graphics from KEEP v03 boards.

MP4s for overlays are REVIEW paper stand-ins, never finished composites.
Their ProRes 4444 MOV siblings carry straight alpha for the future moving plates.
No generation, downloads, audio, deletion, or network access. 30fps durations round
UP to the next frame; trim to board use_s on assembly. Tick cues remain separate.
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

def graphic(name,t,duration,label):
    im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
    p=ease(t,0,1.2)
    if name=='likeness_pairs':
        path(d,[(960,330),(960,875)],ease(t,0,.4),GOLD,3)
        oval(d,(340,520,590,565),GOLD,8);path(d,[(340,540),(340,790),(590,790),(590,540)],p,CREAM,6);oval(d,(340,765,590,810),GOLD,7);path(d,[(465,540),(465,420)],p,GOLD,8);path(d,[(355,640),(575,640),(575,770),(355,770),(355,640)],p,GOLD,4)
        cloud(d,1190,420,t)
        spark=[(0,0),(65,55),(20,110),(90,170),(50,220)]
        for x,start in [(465,.6),(1400,2.2)]:path(d,[(x+a,430+b) for a,b in spark],ease(t,start,start+.55),BLUE,9)
    elif name=='likeness_fire':
        path(d,[(250,360),(1670,360),(1670,900),(250,900),(250,360)],ease(t,.35,.7),GOLD,3)
        oval(d,(420,720,650,790),GOLD);path(d,[(530,720),(530,660)],p)
        roof(d,1330,650)
        for x,start in [(530,.7),(1330,2.3)]:
            path(d,[(x-55,680),(x-75,610),(x-25,550),(x,490),(x+30,565),(x+65,610),(x+55,680),(x-55,680)],ease(t,start,start+.4),GOLD,6)
            if t>start: path(d,[(x,650),(x+12*math.sin(t*3),570),(x-5,535)],color=CREAM,width=5)
    elif name=='rod_cloud':
        tower(d,p);path(d,[(1100,800),(1100,400),(1160,400),(1160,800),(1100,800)],p)
        path(d,[(1130,400),(1130,265)],p,GOLD,8)
        cloud(d,650+16*math.sin(t*.3),235,t)
        dots(d,[(780,285),(890,330),(1030,340),(1130,265)],t,1.5,6.5)
    elif name=='letter_crosses':
        # Schematic coastline contours, intentionally not a survey/map claim.
        west=[(340,300),(440,330),(490,390),(570,420),(600,480),(560,540),(510,610),(480,730),(540,830)]
        east=[(1480,310),(1380,360),(1420,420),(1340,470),(1320,530),(1390,590),(1350,640),(1430,720),(1500,840)]
        path(d,west,ease(t,.3,.65));path(d,east,ease(t,.3,.65));oval(d,(550,525,570,545),GOLD,6)
        route=[(560,535),(770,430),(1040,390),(1230,440),(1360,535)]
        for i in range(45):
            q=i/44
            if q<=ease(t,.6,3.4):
                j=q*4;k=min(int(j),3);u=j-k;x=route[k][0]*(1-u)+route[k+1][0]*u;y=route[k][1]*(1-u)+route[k+1][1]*u
                oval(d,(x-3,y-3,x+3,y+3),GOLD,4)
        if t>=3.1:oval(d,(1350,525,1370,545),GOLD,6)
    elif name=='wet_dry':
        path(d,[(960,300),(960,590)],ease(t,0,.8),CREAM,9);key(d,960,625)
        path(d,[(960,780),(1010,820),(940,920),(880,860),(960,780),(1040,865)],ease(t,0,.8),BLUE,10)
        dots(d,[(960,300),(960,600),(960,755)],t,1,5.3)
        if t>2.8:path(d,[(895,780),(1025,780)],ease(t,2.8,3.1),GOLD,8)
    elif name=='same_thing':path(d,[(960,300),(960,960)],ease(t,.3,.7),GOLD,5)
    elif name=='teach_charge':
        cloud(d,380,280,t)
        kite=[(720,450),(815,535),(720,620),(650,535),(720,450)]
        path(d,kite,p);path(d,[(720,450),(720,620)],p);path(d,[(650,535),(815,535)],p)
        roof(d,1350,740,.8,p);path(d,[(1206,836),(1206,960),(1494,960),(1494,836)],p)
        path(d,[(720,620),(1140,830)],p);key(d,1140,850)
        dots(d,[(720,620),(930,725),(1140,830)],t,1.2,7.1)
    elif name=='looking_path':
        for pts,delay in [([(960,310),(920,410),(1010,475),(955,570),(1000,660),(960,780)],0), ([(920,410),(790,480),(820,560),(730,650)],.45), ([(1010,475),(1140,530),(1100,630),(1220,735)],.8)]:
            path(d,pts,ease(t,.3+delay,2.8),GOLD,7)
    elif name=='wood_vs_metal':
        roof(d,490,600,1.2,p);tower(d,p)
        for a in range(0,360,50):
            rad=math.radians(a);x,y=900,580
            pts=[(x,y),(x+60*math.cos(rad),y+60*math.sin(rad)),(x+90*math.cos(rad+.2),y+90*math.sin(rad+.2)),(x+140*math.cos(rad),y+140*math.sin(rad))]
            path(d,pts,ease(t,1.8,6.8),GOLD,6)
        path(d,[(490,300),(460,370),(510,440),(490,530)],ease(t,1.2,1.8),BLUE,7)
    elif name=='metal_easy':
        path(d,[(850,330),(800,330),(800,890),(850,890)],ease(t,.25,.6),CREAM,4)
        path(d,[(960,300),(960,920)],ease(t,.4,2.8),GOLD,10)
        if t>.4: path(d,[(960,300),(960,300+620*ease(t,.4,2.8))],color=CREAM,width=3)
    elif name=='safe_path':
        tower(d,ease(t,0,1.3));path(d,[(580,890),(1320,890)],p,GOLD,3)
        conductor=[(900,250),(900,290),(1070,550),(1085,890),(1085,995)]
        path(d,conductor,p,GOLD,6)
        for y in range(920,1010,25):path(d,[(650,y),(1000,y)],p,(155,125,87,255),2)
        path(d,[(810,760),(900,585),(995,760),(810,760)],p,CREAM,4)
        path(d,conductor,ease(t,1.5,6.5),CREAM,10);dots(d,conductor,t,1.5,6.98)
    else:raise ValueError(name)
    # Single label in the approved wording, no text resampling / Ken Burns.
    start=1.2 if name=='same_thing' else .6 if name in ('safe_path','teach_charge') else .5
    end=5 if name=='same_thing' else 4.4 if name in ('safe_path','teach_charge') else min(duration-.15,start+4)
    alpha=ease(t,start,start+.4)*(1-ease(t,max(start+.4,end-.4),end))
    font=ImageFont.truetype(FONT,66 if len(label)<29 else 58,index=1)
    d.text((W/2,150),label,font=font,fill=(*CREAM[:3],round(255*alpha)),anchor='mm')
    if name=='likeness_fire':im.putalpha(im.getchannel('A').point(lambda a:round(a*(1-ease(t,4.5,4.8)))))
    return im

def paper():
    rng=np.random.default_rng(8329);y,x=np.mgrid[:H,:W];v=((x-W/2)/(W/2))**2+((y-H/2)/(H/2))**2
    a=np.zeros((H,W,3));noise=rng.normal(0,1.2,(H,W))
    for c,base in enumerate((100,73,49)):a[:,:,c]=base-12*v+noise
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
    ap.add_argument('--replace',action='store_true',help='with --only, replace that row’s existing files')
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    if args.replace and not args.only:
        raise SystemExit('--replace requires --only')
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
            still=Image.alpha_composite(bg,graphic(name,mid,duration,spec['label'])).convert('RGB');still.save(jpg);thumbs.append((keyid,still.copy()))
            record=dict(row=keyid,film_start_s=row['t_s'],part_start_s=round(row['t_s']-board['vo_film_start_s'],3),use_s=duration,encoded_s=frames/FPS,vo_land=row['vo_land'],vo_file=board['vo_file'],vo_sha256=board['vo_sha256'],spec=spec,preview=preview.name,alpha=alpha.name if overlay else None,composite_pending=overlay,board_sha256=digest(boardpath))
            if not args.stills_only:
                if preview.exists() or (overlay and alpha.exists()):
                    if not args.replace:
                        raise RuntimeError(f'Refusing overwrite: {preview}')
                    preview.unlink(missing_ok=True)
                    if overlay:alpha.unlink(missing_ok=True)
                proc=writer(preview,False);aproc=writer(alpha,True) if overlay else None
                for frame in range(frames):
                    layer=graphic(name,frame/FPS,duration,spec['label'])
                    proc.stdin.write(Image.alpha_composite(bg,layer).tobytes())
                    if aproc:aproc.stdin.write(layer.tobytes())
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
