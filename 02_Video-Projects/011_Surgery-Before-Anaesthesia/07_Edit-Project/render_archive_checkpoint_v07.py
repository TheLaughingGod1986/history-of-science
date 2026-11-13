"""Two additional cached archive composites; preliminary, no network or spend."""
import argparse,json,math,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from render_free_graphics_v02 import sha,anchor
HERE=Path(__file__).resolve().parent
FONT='/System/Library/Fonts/Supplemental/Didot.ttc'
SELECTED=['P2:05a_arch_laughing_gas_broadside','P3:05b']
def save(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def arrow(d,pts,phase):
 # A moving ink trace; direction follows the schematic inlet, sponge, outlet.
 lengths=[math.dist(a,b) for a,b in zip(pts,pts[1:])];total=sum(lengths);distance=phase*total
 for (a,b),length in zip(zip(pts,pts[1:]),lengths):
  if distance<=length:
   x=a[0]+(b[0]-a[0])*distance/length;y=a[1]+(b[1]-a[1])*distance/length
   d.ellipse((x-9,y-9,x+9,y+9),fill=(195,146,60));break
  distance-=length
 for a,b in zip(pts,pts[1:]):d.line((*a,*b),fill=(195,146,60),width=4)
 x,y=pts[-1];d.polygon([(x,y),(x-20,y-10),(x-20,y+10)],fill=(195,146,60))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--cache',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False)
 plan=json.loads((HERE/'PICTURE_PLAN_v03.json').read_text());raw=json.loads((HERE.parent/plan['vo_lock']['stt_raw']).read_text());words=[dict(w,raw_index=i) for i,w in enumerate(raw['words']) if w['type']=='word'];recovery=json.loads((HERE/'ARCHIVE_RECOVERY_v05.json').read_text());sources={s['row_id']:s for s in recovery['sources']}
 result={'job':'J2563','film_stage_approved':False,'motion_review':False,'audio_review':False,'spend_gbp':0,'credits_used':0,'plan_sha256':sha(HERE/'PICTURE_PLAN_v03.json'),'rows':[]}
 for r in plan['rows']:
  if r['row_id'] not in SELECTED:continue
  s=sources[r['row_id']];src=a.cache/s['file_name'];assert sha(src)==s['sha256'];im=Image.open(src).convert('RGB');crop=None;cues=[];mort=r['row_id']=='P3:05b'
  if mort:
   im.thumbnail((1020,790));cue=anchor(words,'ether',r['in_s'],r['out_s']);cue.update(text='ETHER',kind='label',out_s=min(cue['in_s']+1.5,r['out_s']));cues.append(cue)
  else:
   # Remove only scan calibration bars and margins, preserving the etching.
   crop=(105,98,923,678);im=im.crop(crop);im.thumbnail((1170,800))
  frames=round(r['duration_s']*30);target=a.out/(r['row_id'].replace(':','_')+'.mp4');proc=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',str(target)],stdin=subprocess.PIPE)
  intervals=[(r['in_s'],r['out_s'])]
  if cues:intervals=[(r['in_s'],cues[0]['in_s']),(cues[0]['out_s'],r['out_s'])]
  for n in range(frames):
   t=n/30;absolute=r['in_s']+t;canvas=Image.new('RGB',(1920,1080),(53,34,24));d=ImageDraw.Draw(canvas);x=80+round(8*math.sin(t*.3));y=round((980-im.height)/2)
   d.rectangle((x-12,y-12,x+im.width+12,y+im.height+12),fill=(224,207,173));canvas.paste(im,(x,y))
   if mort:
    # Own diagram kept separate from the replica photograph; no invented anatomy.
    d.arc((1280,345,1650,715),0,360,fill=(240,226,194),width=5)
    d.line((1370,365,1370,245,1420,245),fill=(240,226,194),width=5)
    d.line((1625,490,1750,490),fill=(240,226,194),width=5)
    for i in range(18):
     xx=1350+(i%6)*37;yy=595+(i//6)*25;d.ellipse((xx,yy,xx+25,yy+19),outline=(195,146,60),width=2)
    arrow(d,[(1390,260),(1390,480),(1460,625),(1575,490),(1750,490)],(t*.5)%1)
   else:
    # Approved own-drawn broadside fragment, distinct from Gillray's 1802 print.
    # It is a reconstruction, never presented as a photographed 1844 artefact.
    d.rectangle((1330,245,1830,795),fill=(235,217,177),outline=(177,139,78),width=4)
    for yy in (290,750):d.line((1370,yy,1790,yy),fill=(74,48,29),width=3)
    for text,yy,size in [('A GRAND',340,52),('EXHIBITION',420,54),('LAUGHING',535,55),('GAS',615,70)]:
     f=ImageFont.truetype(FONT,size,index=1);box=d.textbbox((0,0),text,font=f);d.text(((3160-box[2])/2,yy),text,font=f,fill=(64,41,26))
    # Animated underline, no still zoom or fabricated additional historical detail.
    d.line((1380,710,1380+380*min(1,t/1.5),710),fill=(177,139,78),width=3)
   active=next((c for c in cues if c['in_s']<=absolute<c['out_s']),None)
   if active:d.text((1260,850),active['text'],font=ImageFont.truetype(FONT,58,index=1),fill=(245,234,209))
   elif any(b<=absolute<e for b,e in intervals):d.text((60,1005),s['credit'] if mort else 'Gillray (1802), Library of Congress / Commons; broadside: own drawing',font=ImageFont.truetype(FONT,30,index=1),fill=(245,234,209))
   if n==frames//2:canvas.save(a.out/(target.stem+'_layout.jpg'))
   proc.stdin.write(canvas.tobytes())
  proc.stdin.close();assert proc.wait()==0
  v=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(target)]))['streams'][0];assert (v['width'],v['height'],v['avg_frame_rate'],int(v['nb_frames']))==(1920,1080,'30/1',frames);assert abs(float(v['duration'])-r['duration_s'])<1/60+.00001
  subprocess.run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'],check=True)
  credits=[{'kind':'archive_credit','text':s['credit'] if mort else 'Gillray (1802), Library of Congress / Commons; broadside: own drawing','in_s':b,'out_s':e,'word_indices':[],'reason':'Source credit deferred while spoken label appears'} for b,e in intervals if e>b]
  for c in cues:
   assert c['in_s']==words[c['word_indices'][-1]]['start'];assert all(c['out_s']<=z['in_s'] or z['out_s']<=c['in_s'] for z in credits)
  result['rows'].append({'row_id':r['row_id'],'path':str(target),'sha256':sha(target),'source':s,'source_crop_xyxy':crop,'frames':frames,'duration_s':float(v['duration']),'plan_in_s':r['in_s'],'plan_out_s':r['out_s'],'cues':cues,'credit_cues':credits,'review_status':'preliminary: static layout inspected; capable motion and editorial review required','reconciliation':'Replica circa 1945, not an 1846 engraving; separate schematic airflow, no new claims or date labels' if mort else 'Gillray 1802 source plus own-drawn fragment of approved broadside; no 1844 date shown. Reconstruction wording/readability requires editorial review.'});save(a.out/'ARCHIVE_COMPOSITES_v07.json',result);print(r['row_id'],'rendered; hash, decode, dimensions, duration and local cue checks passed',flush=True)
if __name__=='__main__':main()
