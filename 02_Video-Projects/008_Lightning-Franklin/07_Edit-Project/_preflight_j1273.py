#!/usr/bin/env python3
"""J1273 candidate only. No master splice, publishing, or automatic approval."""
import importlib.util,json,subprocess as sp,sys,math,os
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import _build_rough_v09 as base
ROOT=Path(os.environ.get('J1273_OUT','/Users/benjaminoats/_desk/j1273-candidate-v08'))
V08=Path('/Volumes/data/mac-mini-archive/tmp-render-scratch/j1263-hos008-rough-v08/build_v08.py')
W,H=1920,1080

def load():
 s=importlib.util.spec_from_file_location('v08',V08);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def measure(gray,y,lo,hi):
 # Independent visible-shaft image measurement: darkest 5px-wide vertical band,
 # median across 11 rows rejects horizontal mortar lines.
 strip=np.median(gray[y-5:y+6,lo:hi],axis=0)
 scores=np.convolve(strip,np.ones(5)/5,mode='valid')
 return float(lo+np.argmin(scores)+2)

def controls(im):
 g=np.asarray(im.convert('L'),dtype=float)
 a=measure(g,100,1110,1220);b=measure(g,180,int(a-15),int(a+18))
 pts=[(a,100),(b,180)]
 # Hand and wall bracket dark edges are not rod measurements. Bridge them
 # with the local shaft direction from the exposed upper and lower sections.
 for y,lo,hi in [(520,1150,1210),(650,1160,1215),(800,1170,1220),(920,1175,1225)]:
  pts.append((measure(g,y,lo,hi),y))
 return pts

def xat(pts,y):return float(np.interp(y,[p[1] for p in pts],[p[0] for p in pts]))

def alpha(i,pts):
 t=i/24; im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
 path=[(xat(pts,280),280)]+[(x,y) for x,y in pts if y>280]
 base.draw_path(d,path,base.ease(t,0,.125),base.GOLD,12)
 for yy in range(320,900,64):
  x=xat(pts,yy); a=base.ease(t,0,.125)
  if a:d.ellipse((x-24,yy-12,x+24,yy+12),outline=(*base.CREAM[:3],round(255*a)),width=4)
 if t>=.30:
  base.draw_path(d,path,base.ease(t,.30,1.50),base.CREAM,5)
  if t>=.40:
   for k in range(16):
    y=280+640*((k/16+(t-.40)*.23)%1);x=xat(pts,y)
    d.ellipse((x-5,y-5,x+5,y+5),outline=base.GOLD,width=4)
 a=1 if t>=.48 else base.ease(t,.12,.48)
 base.stroke_text(d,(960,150),'METAL CONDUCTS',ImageFont.truetype(base.FONT,72,index=1),a,7)
 return im

def encode(frames,dest,rgba=False):
 cmd=['ffmpeg','-n','-v','error','-f','rawvideo','-pix_fmt','rgba' if rgba else 'rgb24','-s','1920x1080','-r','24','-i','pipe:0','-an']
 cmd+=['-c:v','prores_ks','-profile:v','4','-pix_fmt','yuva444p10le'] if rgba else ['-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p']
 p=sp.Popen(cmd+[str(dest)],stdin=sp.PIPE)
 for f in frames:p.stdin.write(f.tobytes())
 p.stdin.close();assert p.wait()==0

def build():
 (ROOT/'alpha_png').mkdir(exist_ok=False)
 entries=[]
 for i in range(42):
  im=Image.open(ROOT/'source'/f'{i:02}.png').convert('RGB');pts=controls(im)
  a=alpha(i,pts);a.save(ROOT/'alpha_png'/f'{i:02}.png')
  entries.append({'row_frame':i,'source_frame':109+i,'pts_s':i/24,'controls_xy':pts,'occluded_y_intervals':[[270,350],[420,480]]})
 (ROOT/'TRACKING.json').write_text(json.dumps(entries,indent=2)+'\n')
 encode((Image.open(ROOT/'alpha_png'/f'{i:02}.png') for i in range(42)),ROOT/'code_graphic_008_p5_10_metal_easy_v08.mov',True)
 # Composite the ENCODED alpha, not an unencoded stand-in, against exact extracted plate frames.
 sp.run(['ffmpeg','-n','-v','error','-framerate','24','-i',str(ROOT/'source/%02d.png'),'-i',str(ROOT/'code_graphic_008_p5_10_metal_easy_v08.mov'),'-filter_complex','[0:v]format=rgba[b];[b][1:v]overlay=0:0:format=auto,format=yuv420p[v]','-map','[v]','-frames:v','42','-an','-c:v','libx264','-preset','veryfast','-crf','17',str(ROOT/'composite_v08.mp4')],check=True)

def verify():
 v08=load();sys.path.insert(0,str(base.OWB_ROOT/'scripts'));import polish_gate as pg
 for name,src in [('decoded_alpha',ROOT/'code_graphic_008_p5_10_metal_easy_v08.mov'),('decoded_composite',ROOT/'composite_v08.mp4')]:
  (ROOT/name).mkdir(exist_ok=False)
  sp.run(['ffmpeg','-n','-v','error','-i',str(src),'-pix_fmt','rgba' if name=='decoded_alpha' else 'rgb24','-fps_mode','passthrough','-start_number','0',str(ROOT/name/'%02d.png')],check=True)
 entries=[]
 for i in range(42):
  # Exact index correspondence, same source PNG used for the composite.
  plate=Image.open(ROOT/'source'/f'{i:02}.png');g=np.asarray(plate.convert('L'),dtype=float)
  a=np.asarray(Image.open(ROOT/'decoded_alpha'/f'{i:02}.png').convert('RGBA'))
  # Measure the 12px gold callout's rendered centre at its start, excluding rings.
  xs=np.where(a[282,:,3]>200)[0]
  trace=float((xs.min()+xs.max())/2) if len(xs) else None
  tip=v08.tip_offset(g,trace_x=trace) if trace is not None else None
  shaft=[]
  for y,lo,hi in [(520,1150,1210),(650,1160,1215),(800,1170,1220),(920,1175,1225)]:
   rod=measure(g,y,lo,hi); xx=np.where(a[y,:,3]>200)[0]
   # select the opaque central line, not the surrounding cream rings
   runs=np.split(xx,np.where(np.diff(xx)>1)[0]+1) if len(xx) else []
   runs=[r for r in runs if len(r)>=5]
   chosen=max(runs,key=len) if runs else []
   rendered=float((chosen[0]+chosen[-1])/2) if len(chosen) else None
   shaft.append({'y':y,'rod_x':rod,'rendered_x':rendered,'offset_px':None if rendered is None else rod-rendered})
  entries.append({'row_frame':i,'source_frame':109+i,'trace_start_y':282,'tip':tip,'shaft':shaft})
 samples=[]
 for pct in [10,25,50,75,90]:
  # First display frame at or after requested percentile, explicitly logged.
  i=math.ceil(42*pct/100);e=entries[i];samples.append({'pct':pct,**e})
  Image.open(ROOT/'decoded_composite'/f'{i:02}.png').save(ROOT/f'p{pct}_frame{i:02}.png')
  gray=pg.frame_gray(ROOT/'composite_v08.mp4',i/24)
  samples[-1]['vertical_seams']=[h for h in pg.seams(gray) if 'vertical' in h.get('kind','')]
 report={'threshold_px':19.2,'detector_sha256':base.sha256_file(V08),'samples':samples,'all_frames':entries,'note':'Frame 0 has no overlay by original animation; early partial-callout lower-shaft measurements are unavailable, not zero.'}
 report['sample_alignment_ok']=all(e['tip'] and abs(e['tip']['offset_px'])<=19.2 for e in samples)
 (ROOT/'OFFSETS.json').write_text(json.dumps(report,indent=2)+'\n')
 # all 42 workman crops with frame labels, source and composite side by side
 for start in [0,14,28]:
  sheet=Image.new('RGB',(7*400,2*520),(30,30,30));d=ImageDraw.Draw(sheet)
  for j,i in enumerate(range(start,start+14)):
   x=(j%7)*400;y=(j//7)*520
   for k,folder in enumerate(['source','decoded_composite']):
    im=Image.open(ROOT/folder/f'{i:02}.png').crop((820,0,1260,1050));im.thumbnail((200,490));sheet.paste(im,(x+k*200,y+25))
   d.text((x+5,y+5),f'row {i} source {109+i} | candidate',fill='white')
  sheet.save(ROOT/f'all_frames_{start:02}.jpg')
 print(json.dumps({'sample_alignment_ok':report['sample_alignment_ok'],'samples':[(s['pct'],s['tip']) for s in samples]},indent=2))

if __name__=='__main__':
 if sys.argv[-1]=='extract':
  ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'source').mkdir(exist_ok=False)
  sp.run(['ffmpeg','-n','-v','error','-i',str(load().PLATE),'-vf','trim=start_frame=109:end_frame=151,setpts=PTS-STARTPTS,scale=1920:1080:flags=lanczos,eq=brightness=0.04:contrast=0.96','-fps_mode','passthrough','-start_number','0',str(ROOT/'source/%02d.png')],check=True)
 elif sys.argv[-1]=='build':build()
 elif sys.argv[-1]=='verify':verify()
 else:raise SystemExit('extract, build or verify')
