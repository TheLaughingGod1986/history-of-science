"""Build J2632 r4 evidence under Chief ruling 6807936928; no splice."""
import argparse, hashlib, importlib.util, io, json, math, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument('--out', type=Path, required=True)
ap.add_argument('--review', type=Path, required=True)
ap.add_argument('--parents', type=Path, required=True)
a = ap.parse_args()
edit = Path(__file__).resolve().parent
mod = importlib.util.spec_from_file_location('graphics', edit / '_build_code_graphics_v01.py')
g = importlib.util.module_from_spec(mod); mod.loader.exec_module(g)
a.out.mkdir(parents=True, exist_ok=True); a.review.mkdir(parents=True, exist_ok=True)
spec = dict(g.FALLING_MOON_SPEC)
video = a.out / spec['file']
if video.exists():
    raise SystemExit('Use a new output directory; preserve previous render evidence.')
rec = g.render_one(g.make_paper(), spec, a.out)
head = g.FALLING_MOON_HEAD_FRAMES
n = head + 158
positions = [g.falling_moon_position(max(0,(k-head)/g.FPS)) for k in range(n)]
assert positions[:head+1] == [(560.0,160.0)]*(head+1)
assert all(b[0] > c[0] and b[1] > c[1] for c,b in zip(positions[head:],positions[head+1:]))
cx,cy = g.FALLING_MOON_EARTH
assert all(abs(math.hypot(x-cx,y-cy)-720)<1e-8 for x,y in positions)
assert all(57<x<1920-57 and 57<y<1080-57 for x,y in positions)
assert g.FALLING_MOON_ANGLE < math.pi/2
probe = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(video)]))
assert len(probe['streams']) == 1
stream = probe['streams'][0]
assert (stream['width'],stream['height'],stream['r_frame_rate'],int(stream['nb_frames'])) == (1920,1080,'30/1',n)
subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(video),'-f','null','-'],check=True)
md5 = subprocess.check_output(['ffmpeg','-v','error','-i',str(video),'-f','framemd5','-']).decode()
hashes = [line.split(',')[-1].strip() for line in md5.splitlines() if line and not line.startswith('#')]
assert len(hashes)==n and len(set(hashes))==n
# Preserve former motion on its film timestamps: frame32 maps to183.94.
start = 183.94-head/30
rec.update(source_path=str(video),superseded_sha256='cb8051bb9d6b46d014be46977522d089e19262fa7fd7fd90dfee3099fb13c2f7',revision='32 new head frames; accepted artwork unchanged; parent out104',nominal_edit_duration_s=5.26+head/30,encoded_duration_s=float(stream['duration']),frame_count=n,unique_decoded_frames=len(set(hashes)),head_frames=head,head_duration_s=head/30,film_start_s=start,film_motion_start_s=183.94,film_end_s=189.20,angular_travel_degrees=70,earth_center_px=[cx,cy],orbit_radius_px=720,earth_radius_px=150,moon_radius_px=57,min_surface_clearance_px=513,arc_stroke_px=5,tangent_stroke_px=4,tangent_dash_on_px=36,tangent_dash_gap_px=28,earth_marks='unchanged continent outlines',moon_rings={'count':2,'stroke_px':4,'outer_diameter_px':30,'inner_hole_px':22,'offsets_px':[[-19,-13],[18,18]],'fill':'unchanged moon wash'},review_status='candidate only; Claude sheet read and Chief KEEP required',no_splice=True,splice_authorized=False,geometry_checks='190 unique decoded frames;32 tangent-draw head frames;158 unchanged motion positions;constant radius;inside frame;less than quarter turn')
rec['timing_samples']=[{'motion_local_s':t,'render_local_s':t+head/30,'film_s':183.94+t,'moon_center_px':g.falling_moon_position(t),'gap_below_tangent_px':g.falling_moon_position(t)[1]-160} for t in (0,.58,1.4,1.92,2.56,3.38,3.88,157/30)]
rec['timing_reconciliation']={'chief_ruling':'https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6807936928','parent_frame_delta':21,'parent_fps':24,'parent_delta_s':21/24,'new_head_frames':head,'new_head_fps':30,'new_head_s':head/30,'fade_graphic_frames':[0,1,2,3,4,5],'fade_duration_s':.2,'fade_start_film_s':start,'fade_end_film_s':start+.2,'graphic_only_lead_s':head/30-.2,'parent_out_target_film_s':183.94-21/24,'parent_out_residual_s':start+.2-(183.94-21/24),'encoded_end_film_s':start+n/30,'status':'Prior 0.175 s mismatch superseded by 32-frame head and overlapping fade; residual under 10 ms, nearest-frame snap in assembly. Not a splice approval.'}
assert abs(rec['timing_reconciliation']['parent_out_residual_s']) < .01

def frame(path,k):
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vf',f'select=eq(n\\,{k})','-frames:v','1','-f','image2pipe','-vcodec','png','-'])
    return Image.open(io.BytesIO(raw)).convert('RGB')
font=ImageFont.truetype(g.FONT,24,index=1)
def sheet(rows,dest,cols=2,phone_rows=()):
    base=400*math.ceil(len(rows)/cols)
    im=Image.new('RGB',(640*cols,base+270*len(phone_rows)),(44,29,16)); d=ImageDraw.Draw(im)
    for i,(pic,label) in enumerate(rows):
        x=i%cols*640; y=i//cols*400
        im.paste(pic.resize((640,360),Image.Resampling.LANCZOS),(x,y))
        d.text((x+10,y+365),label,font=font,fill=g.CREAM[:3])
    for i,(pic,label) in enumerate(phone_rows):
        y=base+i*270
        im.paste(pic,(20,y+20))
        d.text((430,y+60),label,font=font,fill=g.CREAM[:3])
    im.save(dest,quality=95)
frames=[0,5,10,31,32,49,74,137,188,189]
phones=[(frame(video,k).resize((390,219),Image.Resampling.LANCZOS),f'f{k}:390px wide at1:1') for k in (10,137,188)]
sheet([(frame(video,k),f'f{k:03d} | local{k/30:.3f}s | film{start+k/30:.3f}s') for k in frames],a.review/'CONTACT_SHEET.jpg',phone_rows=phones)
# No enlargement: three phone frames at their native 390px review width.
phone_sheet=Image.new('RGB',(390,3*255),(44,29,16)); pd=ImageDraw.Draw(phone_sheet)
for i,(pic,label) in enumerate(phones):
    phone_sheet.paste(pic,(0,i*255)); pd.text((8,i*255+223),label,font=font,fill=g.CREAM[:3])
phone_sheet.save(a.review/'PHONE_390.jpg',quality=98)
parent=a.parents/'01_really_falling_t1.mp4'; following=a.parents/'02_cannon_world_t1.mp4'
rows=[]
for path,k,fps,label in [(parent,k,24,f'Parent f{k}: '+('fade range' if k<104 else 'OUT' if k==104 else 'EXCLUDED')) for k in [99,100,101,102,103,104,108,125]]+[(video,0,30,'Graphic first'),(video,n-1,30,'Graphic last'),(following,0,24,'Cannon first')]:
    rows.append((frame(path,k),label))
    rec.setdefault('boundaries',[]).append({'source':str(path),'frame':k,'source_time_s':k/fps,'label':label,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
sheet(rows,a.review/'CUT_BOUNDARIES.jpg')
rec['parent_out']={'fps':24,'earlier_out_frame':104,'earlier_out_s':104/24,'planned_out_frame':125,'delta_s':21/24,'crossfade_frames':[99,100,101,102,103,104],'crossfade_requested_s':.20,'excluded_frames':[108,112,125],'instruction':'Chief requires out104 and fade99-104. Review evidence only. Fade graphic f0-f5 at182.873333-183.073333; nearest-frame assembly snap per ruling6807936928. Never hold or splice this candidate before KEEP.'}
rec['boundary_note']='Source boundary samples only; no assembled join. Later rows and VO unchanged.'
(a.review/'MANIFEST.json').write_text(json.dumps(rec,indent=2)+'\n')
print('J2632 geometry, stream, silence, 190 unique decoded frames and full decode checks passed; r4 timing residual under 10 ms; review pending.')
