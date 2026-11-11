"""Render J2631 and verify geometry; does not splice or approve the film."""
import importlib.util,json,math,subprocess,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import argparse
ap=argparse.ArgumentParser()
ap.add_argument('--out', type=Path, required=True)
ap.add_argument('--review', type=Path, required=True)
args=ap.parse_args()
edit=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('g',edit/'_build_code_graphics_v01.py'); g=importlib.util.module_from_spec(s); s.loader.exec_module(g)
out=args.out
out.mkdir(parents=True, exist_ok=True)
review=args.review; review.mkdir(parents=True, exist_ok=True)
# Pad to the next frame so the planned 13.51-second edit never runs out of source.
spec=dict(g.MINUTE_SECOND_SPEC); spec['dur']=math.ceil(spec['dur']*g.FPS)/g.FPS
assert not (out/spec['file']).exists(), 'Do not overwrite a prior candidate'
rec=g.render_one(g.make_paper(),spec,out)
rec.update(nominal_edit_duration_s=13.51,film_start_s=319.63,internal_cut_s=326.39,film_end_s=333.14,labels=[{'text':x,'start_s':a,'end_s':b} for x,a,b in g.MINUTE_SECOND_LABELS],review_status='pending Chief sheet review and Gemini narration timing',source_path=str(out/spec['file']),no_splice=True)
# Every rendered frame: one drop, no reverse, no label overlap, clean cut.
positions=[g.minute_second_positions(i/g.FPS) for i in range(406)]
assert all(b[0][1]>=a[0][1] and b[1][1]>=a[1][1] and b[1][0]>a[1][0] for a,b in zip(positions,positions[1:]))
assert all(p[0][1]==630 for p in positions[44:])
for i in range(406):
 t=i/g.FPS
 alphas=[g.minute_second_label_alpha(t,a,b) for _,a,b in g.MINUTE_SECOND_LABELS]
 assert sum(a>0 for a in alphas)<=1
 if t>=6.4: assert max(alphas)==0
assert g.minute_second_positions(13.51)[1][1]==630
rec['geometry_checks']={'all_406_frames_monotone':True,'left_landed_once':True,'bracket_y_px':[330,630],'one_label_at_a_time':True,'all_labels_off_at_s':6.4,'illustrative_time_scales':True}
# 12 distributed samples plus both source frames around internal cut and endpoints.
frames=sorted(set([0,24,43,65,90,112,135,166,191,240,300,360,405,202,203]))
thumbs=[]
for k in frames:
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(out/spec['file']),'-vf',f'select=eq(n\\,{k})','-frames:v','1','-f','image2pipe','-vcodec','png','-'])
 import io
 im=Image.open(io.BytesIO(raw)).convert('RGB'); thumbs.append((k,im))
cols=3; tw,th=640,360
sheet=Image.new('RGB',(cols*tw,math.ceil(len(thumbs)/cols)*(th+40)),(44,29,16)); d=ImageDraw.Draw(sheet); font=ImageFont.truetype(g.FONT,24,index=1)
for i,(k,im) in enumerate(thumbs):
 x=(i%cols)*tw; y=(i//cols)*(th+40); sheet.paste(im.resize((tw,th)),(x,y)); d.text((x+10,y+th+5),f'f{k:03d}  local {k/30:.3f}s  film {319.63+k/30:.3f}s',font=font,fill=g.CREAM[:3])
sheet.save(review/'CONTACT_SHEET.jpg',quality=92)
rec['sheet_frames']=frames
(review/'MANIFEST.json').write_text(json.dumps(rec,indent=2)+'\n')
print(json.dumps(rec,indent=2))
