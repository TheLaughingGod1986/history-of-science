"""Render the 67 authorized internal dependency slates. No generated pictures."""
import argparse,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from render_free_graphics_v02 import sha
HERE=Path(__file__).resolve().parent
FONT='/System/Library/Fonts/Supplemental/Didot.ttc'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False)
 plan=json.loads((HERE/'PICTURE_PLAN_v03.json').read_text());rows=[r for r in plan['rows'] if r['source_kind'].startswith('mint_') or r['source_kind']=='existing_plate_reuse'];assert len(rows)==67
 result={'job':'J2563','purpose':'Internal timing dependencies only; no picture generation or film-stage approval','plan_sha256':sha(HERE/'PICTURE_PLAN_v03.json'),'generation_authorized':False,'spend_gbp':0,'credits_used':0,'motion_review':False,'audio_review':False,'fps':30,'quantization':'Cumulative absolute 30fps boundaries; each boundary within half a frame','rows':[],'reuse_finding':{'row_id':'P5:16b','source_row':'P1:07b','actual_source_duration_s':None,'actual_source_in_out':None,'source_available':False,'required_first_use_s':6.61,'required_callback_s':4.52,'minimum_disjoint_duration_s':11.13,'hypothetical_8s_overlap_s':3.13,'decision':'Dependency slate remains; no actual source interval verified, no stretch or freeze'}}
 for r in rows:
  target=a.out/(r['row_id'].replace(':','_')+'.mp4');png=target.with_suffix('.png');im=Image.new('RGB',(1920,1080),(45,30,23));d=ImageDraw.Draw(im)
  lines=['INTERNAL TIMING ROUGH',r['row_id'],'DEPENDENCY: REUSE NOT VERIFIED' if r['source_kind']=='existing_plate_reuse' else 'DEPENDENCY: PICTURE NOT GENERATED',f"{r['in_s']:.2f}–{r['out_s']:.2f} s",'Not a finished film']
  for text,y,size in zip(lines,[170,345,520,680,870],[65,76,48,48,38]):
   font=ImageFont.truetype(FONT,size,index=1);box=d.textbbox((0,0),text,font=font);d.text(((1920-box[2])/2,y),text,font=font,fill=(239,222,184))
  im.save(png);start=round(r['in_s']*30);end=round(r['out_s']*30);frames=end-start
  subprocess.run(['ffmpeg','-v','error','-loop','1','-framerate','30','-i',str(png),'-frames:v',str(frames),'-an','-c:v','libx264','-preset','ultrafast','-crf','23','-pix_fmt','yuv420p',str(target)],check=True)
  v=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(target)]))['streams'][0];assert int(v['nb_frames'])==frames;assert (v['width'],v['height'],v['avg_frame_rate'])==(1920,1080,'30/1');assert abs(start/30-r['in_s'])<=1/60+.00001;assert abs(end/30-r['out_s'])<=1/60+.00001
  subprocess.run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'],check=True)
  result['rows'].append({'row_id':r['row_id'],'path':str(target),'sha256':sha(target),'plan_in_s':r['in_s'],'plan_out_s':r['out_s'],'start_frame':start,'end_frame_exclusive':end,'frames':frames,'duration_s':float(v['duration']),'type':'reuse_dependency' if r['source_kind']=='existing_plate_reuse' else 'generation_dependency'});(a.out/'DEPENDENCY_SLATES_v07.json').write_text(json.dumps(result,indent=2)+'\n');print(r['row_id'],flush=True)
 print('PASS: 67 labelled dependency slates; full decode, hashes, 1080p/30fps and cumulative-frame timing checked. Internal artifacts only.')
if __name__=='__main__':main()
