import argparse,sys,json,subprocess as sp
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--owb',type=Path,required=True);args=ap.parse_args()
sys.path.insert(0,str(args.owb/'scripts'))
import polish_gate
root=args.out
manifest=json.loads((root/'GRAPHICS_MANIFEST_v01.json').read_text()); reports=[]
for item in manifest:
 p=root/item['file'];probe=json.loads(sp.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));v=probe['streams'][0]
 assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'30/1')
 assert abs(float(probe['format']['duration'])-item['duration'])<.04
 assert all(b-a>=.5 for a,b in zip(item['tick_ink_seconds'],item['tick_ink_seconds'][1:]))
 cuts=[dict(row=1,source=item['file'],timeline_in=0,timeline_out=item['duration'],framing={'offset':item['background_offset']})]
 report=polish_gate.judge(p,cuts)
 reports.append(dict(file=item['file'],format_check='PASS',polish=report))
(root/'POLISH_GATE_v01.json').write_text(json.dumps(reports,indent=2)+'\n')
print([(r['file'],r['polish']['verdict']) for r in reports])
