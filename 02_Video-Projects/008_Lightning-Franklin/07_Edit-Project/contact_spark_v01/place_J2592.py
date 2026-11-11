"""Place the approved #523 spark without changing its renderer or source take."""
import argparse
import json
from pathlib import Path
import subprocess
from PIL import Image, ImageChops
from render import spark, sha
from review_take4 import EXPECTED, FLASH

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--take', type=Path, required=True)
p.add_argument('--out', type=Path, required=True)
a = p.parse_args()
assert sha(a.take) == EXPECTED, 'Wrong source take'
a.out.mkdir(parents=True, exist_ok=False)
subprocess.run(['ffmpeg','-v','error','-i',str(a.take),'-frames:v','61','-fps_mode','passthrough',str(a.out/'source_%03d.png')],check=True)
rod, knuckle = (945.,333.), (933.,340.5)
changed=[]
actual_changed=[]
for f in range(61):
    bg=Image.open(a.out/f'source_{f+1:03}.png').convert('RGBA')
    assert bg.size == (1280,720)
    bg=bg.resize((1920,1080),Image.Resampling.LANCZOS)
    overlay=Image.new('RGBA',bg.size)
    if f in FLASH:
        s=FLASH[f]
        overlay=spark(bg.size,rod,knuckle,s['phase'],frames=2,bloom_scale=s['bloom_scale'],core=s['core'])
        overlay.save(a.out/f'overlay_f{f:03}.png')
        changed.append(f)
    im=Image.alpha_composite(bg,overlay).convert('RGB')
    if ImageChops.difference(bg.convert('RGB'), im).getbbox():
        actual_changed.append(f)
    im.save(a.out/f'frame_{f:03}.png')
assert changed == actual_changed == [29,30,31]
subprocess.run(['ffmpeg','-v','error','-n','-framerate','24','-i',str(a.out/'frame_%03d.png'),'-frames:v','61','-an','-c:v','libx264','-preset','slow','-crf','12','-pix_fmt','yuv420p','-movflags','+faststart',str(a.out/'02_salon_spark_j2241_t4_J2592_v01.mp4')],check=True)
subprocess.run(['ffmpeg','-v','error','-n','-framerate','24','-start_number','29','-i',str(a.out/'overlay_f%03d.png'),'-frames:v','3','-c:v','qtrle','-pix_fmt','argb',str(a.out/'spark_J2592_f029_f031.mov')],check=True)
# Actual encoded composite, two normal-speed loops, phone size. Silent picture only.
subprocess.run(['ffmpeg','-v','error','-n','-stream_loop','1','-i',str(a.out/'02_salon_spark_j2241_t4_J2592_v01.mp4'),'-vf','scale=390:-2','-an','-c:v','libx264','-crf','14',str(a.out/'phone390_two_loops.mp4')],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(a.out/'02_salon_spark_j2241_t4_J2592_v01.mp4'),'-f','null','-'],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(a.out/'02_salon_spark_j2241_t4_J2592_v01.mp4')]))
v=probe['streams'][0]
assert int(v['nb_read_frames']) == 61 and v['r_frame_rate']=='24/1'
assert sha(a.take)==EXPECTED
files=['02_salon_spark_j2241_t4_J2592_v01.mp4','spark_J2592_f029_f031.mov','phone390_two_loops.mp4']
m=dict(job='J2592',source=str(a.take),source_sha256=EXPECTED,renderer_revision='84a974b1',renderer_sha256=sha(Path(__file__).with_name('render.py')),approval_comments=[6797825254,6797878286],source_frames_inclusive=[0,60],fps=24,frame_count=61,duration_s=61/24,contact_frame=30,contact_time_s=1.25,rod_1080=rod,knuckle_1080=knuckle,rod_720=[630,222],knuckle_720=[622,227],overlay_frames=[29,30,31],overlay_png_sha256={f:sha(a.out/f'overlay_f{f:03}.png') for f in changed},files={f:sha(a.out/f) for f in files},checks={'source_unchanged':True,'full_decode':True,'no_frame_after_f060':True,'only_three_preencode_frames_changed':True},handoff='J2593: judge actual moving phone390_two_loops.mp4 at normal speed, at least two loops; no worker motion or audio approval. No audio added, final SFX/mix remains assembly work.')
(a.out/'MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps(m,indent=2))
