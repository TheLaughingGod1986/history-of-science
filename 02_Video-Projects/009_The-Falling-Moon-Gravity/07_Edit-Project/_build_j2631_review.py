"""Render J2631 and verify geometry; does not splice or approve the film."""
import importlib.util,json,math,subprocess,hashlib,io
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
assert all(p[0][1]==690 for p in positions[44:])
for i in range(406):
 t=i/g.FPS
 alphas=[g.minute_second_label_alpha(t,a,b) for _,a,b in g.MINUTE_SECOND_LABELS]
 assert sum(a>0 for a in alphas)<=1
 if t>=10.4 or i in (0,202,203): assert max(alphas)==0
assert g.minute_second_positions(13.51)[1][1]==690
assert g.prog(202/30,6.85,7.25)==g.prog(203/30,6.85,7.25)==0
assert g.minute_second_positions(13.51)[1][0]+57 < 1840  # clear bracket cap
assert g.minute_second_positions(0)[1][0]-57 > 960  # clear divider
assert all(a < b for _,a,b in g.MINUTE_SECOND_LABELS)
rec['geometry_checks']={'all_406_frames_monotone':True,'left_landed_once':True,'bracket_y_px':[300,690],'one_label_at_a_time':True,'all_labels_off_at_s':10.4,'illustrative_time_scales':True}
# 12 distributed samples plus both source frames around internal cut and endpoints.
frames=sorted(set([0,24,43,96,111,163,202,203,218,240,282,312,360,405]))
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
next(im for k,im in thumbs if k==240).resize((390,219),Image.Resampling.LANCZOS).save(review/'PHONE_390.jpg',quality=95)
rec.update(diagram_scale=1.3,moon_disc_scale=1.5,stroke_px=5,tangent_stroke_px=4,bracket_draw_s=[6.85,7.25],superseded_sha256='c33a45a5048e0f4615933ffd9bc11b2ffcace03f9468d446fff6d395fa3b988e')
(review/'MANIFEST.json').write_text(json.dumps(rec,indent=2)+'\n')
print(json.dumps(rec,indent=2))

# Existing KEEP sources provide the two outer boundaries; no assembled film is made.
boundaries=json.loads((edit/'J2631_review/CUT_BOUNDARIES.json').read_text())
boundaries['note']='Chief 6801512032 confirms parent source 0–6.75 and next source from 0. Candidate only; assembler rechecks at splice.'
bsheet=Image.new('RGB',(1280,3*400),(44,29,16)); bd=ImageDraw.Draw(bsheet)
for i,row in enumerate(boundaries['frames']):
    source=Path(row['source'])
    if 'code_graphic_009_p4_05_minute_second.mp4' in str(source):
        source=out/spec['file']
        row['source']=str(source)
    row['sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
    raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(row['source_time_s']),'-i',str(source),'-frames:v','1','-f','image2pipe','-vcodec','png','-'])
    im=Image.open(io.BytesIO(raw)).convert('RGB').resize((640,360))
    x=(i%2)*640; y=(i//2)*400
    bsheet.paste(im,(x,y)); bd.text((x+10,y+365),row['label'],font=font,fill=g.CREAM[:3])
bsheet.save(review/'CUT_BOUNDARIES.jpg',quality=92)
(review/'CUT_BOUNDARIES.json').write_text(json.dumps(boundaries,indent=2)+'\n')
