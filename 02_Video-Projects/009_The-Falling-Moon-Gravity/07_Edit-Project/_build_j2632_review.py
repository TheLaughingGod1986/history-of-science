"""Build J2632 candidate and still evidence; never splice or approve."""
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
superseded = None
if video.exists():
    superseded = hashlib.sha256(video.read_bytes()).hexdigest()
    video.unlink()
    still = video.with_suffix('.jpg')
    if still.exists():
        still.unlink()
rec = g.render_one(g.make_paper(), spec, a.out)
if superseded:
    rec['superseded_sha256'] = superseded
    rec['revision'] = 'J2632 phone strokes, continent outlines, f116 at 390 on the sheet'
positions = [g.falling_moon_position(k / g.FPS) for k in range(158)]
assert all(b[0] > c[0] and b[1] > c[1] for c, b in zip(positions, positions[1:]))
cx, cy = g.FALLING_MOON_EARTH
assert all(abs(math.hypot(x-cx,y-cy)-720) < 1e-8 for x,y in positions)
assert all(57 < x < 1920-57 and 57 < y < 1080-57 for x,y in positions)
assert g.FALLING_MOON_ANGLE < math.pi/2
assert all(math.hypot(x-cx,y-cy)-150-57 > 500 for x,y in positions)
# Full stream validation, including actual encoded frame count and audio absence.
probe = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(video)]))
assert len(probe['streams']) == 1
stream = probe['streams'][0]
assert (stream['width'],stream['height'],stream['r_frame_rate'],int(stream['nb_frames'])) == (1920,1080,'30/1',158)
subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(video),'-f','null','-'], check=True)
rec.update(source_path=str(video),nominal_edit_duration_s=5.26,encoded_duration_s=float(stream['duration']),frame_count=158,film_start_s=183.94,film_end_s=189.20,angular_travel_degrees=70,earth_center_px=[cx,cy],orbit_radius_px=720,earth_radius_px=150,moon_radius_px=57,min_surface_clearance_px=513,arc_stroke_px=g.FALLING_MOON_ARC_PX,tangent_stroke_px=g.FALLING_MOON_DASH_PX,tangent_dash_on_px=g.FALLING_MOON_DASH_ON,tangent_dash_gap_px=g.FALLING_MOON_DASH_GAP,earth_marks='continent outlines',review_status='revised for phone weight and Earth coastlines; sheet for Grok',no_splice=True,geometry_checks='158 frames: increasing x and y, constant radius, inside frame, less than quarter turn; no freeze padding')
rec['timing_samples'] = [{'local_s':t,'moon_center_px':g.falling_moon_position(t),'gap_below_tangent_px':g.falling_moon_position(t)[1]-160} for t in (0,.58,1.4,1.92,2.56,3.38,3.88,157/30)]
def frame(path, k):
    raw = subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vf',f'select=eq(n\\,{k})','-frames:v','1','-f','image2pipe','-vcodec','png','-'])
    return Image.open(io.BytesIO(raw)).convert('RGB')
font = ImageFont.truetype(g.FONT,24,index=1)
def sheet(rows, dest, cols=2):
    im=Image.new('RGB',(640*cols,400*math.ceil(len(rows)/cols)),(44,29,16)); d=ImageDraw.Draw(im)
    for i,(pic,label) in enumerate(rows):
        x=(i%cols)*640; y=(i//cols)*400
        im.paste(pic.resize((640,360),Image.Resampling.LANCZOS),(x,y))
        d.text((x+10,y+365),label,font=font,fill=g.CREAM[:3])
    im.save(dest,quality=92)
frames = [0,17,42,58,77,101,116,157]
thumbs = [(frame(video,k),f'f{k:03d} | local {k/30:.3f}s | film {183.94+k/30:.3f}s') for k in frames]
phone = frame(video,116).resize((390,219),Image.Resampling.LANCZOS)
phone.save(a.review/'PHONE_390.jpg',quality=95)
# The 390-wide frame sits on the sheet at 1:1, so the phone check is not shrunk again.
sheet_im = Image.new('RGB',(1280, 400*4 + 280),(44,29,16))
d = ImageDraw.Draw(sheet_im)
for i,(pic,label) in enumerate(thumbs):
    x=(i%2)*640; y=(i//2)*400
    sheet_im.paste(pic.resize((640,360),Image.Resampling.LANCZOS),(x,y))
    d.text((x+10,y+365),label,font=font,fill=g.CREAM[:3])
sheet_im.paste(phone,(20, 400*4 + 36))
d.text((430, 400*4 + 80),'f116 at 390 px wide, 1:1',font=font,fill=g.CREAM[:3])
d.text((430, 400*4 + 120),'phone check of the gap, the dashes and the Earth',font=font,fill=g.CREAM[:3])
sheet_im.save(a.review/'CONTACT_SHEET.jpg',quality=92)
# Proposed parent head 0..5.26 and next head 0; assembler verifies at splice.
# The sources are both recorded KEEP in FLOW_MINT_LOG_v04_tranche1.json.
parent=a.parents/'01_really_falling_t1.mp4'; following=a.parents/'02_cannon_world_t1.mp4'
# 24 fps parent. Frame 94 (3.917s) is the last sampled frame whose trail still
# meets the Moon from above. By frame 96 (4.000s) the trail has passed the
# Moon and curls down its right side. The planned out, 5.26s, is inside that hook.
earlier = 94/24
boundaries=[]
for path,t,label,frame_n in [
    (parent,earlier,'Parent earlier out f94, trail still up',94),
    (parent,5.26-1/24,'Parent planned out, trail has curled',125),
    (video,0,'Candidate first frame',0),
    (video,157/30,'Candidate final frame',157),
    (following,0,'Next KEEP first frame',0),
]:
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vf',f'select=eq(n\\,{frame_n})','-frames:v','1','-f','image2pipe','-vcodec','png','-'])
    pic=Image.open(io.BytesIO(raw)).convert('RGB')
    boundaries.append((pic,label))
    rec.setdefault('boundaries',[]).append({'source':str(path),'source_time_s':t,'label':label,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
sheet(boundaries,a.review/'CUT_BOUNDARIES.jpg')
rec['parent_out'] = {
    'fps': 24,
    'planned_out_s': 5.26 - 1/24,
    'hook_visible_from_frame': 96,
    'hook_visible_from_s': 96/24,
    'earlier_out_frame': 94,
    'earlier_out_s': earlier,
    'delta_s': (5.26 - 1/24) - earlier,
    'instruction': 'Cut the parent at frame 94. Hold the graphic first frame for the 1.30s difference, crossfade 0.20s, so the cannon stays at 189.20 and the word timings stay on the moving gap.',
}
rec['boundary_note']='Parent KEEP is the whole 8s clip. Planned use is the first 5.26s, and that out shows the curled trail. Earlier out is frame 94. Not an assembled join.'
(a.review/'MANIFEST.json').write_text(json.dumps(rec,indent=2)+'\n')
print('J2632 geometry, stream, silence and full decode checks passed; review remains pending.')
