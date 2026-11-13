"""Four cached archive review rows. No network, generation, or stage approval.

Source imagery remains unaltered except fit-to-frame and translation. PDF
highlights use source-page coordinates. Output must be a new directory.
"""
import argparse, json, math, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from render_free_graphics_v02 import sha, anchor
HERE=Path(__file__).resolve().parent
FPS=30
SELECTED=['P1:09b','P2:04a_arch_davy_1800','P2:09b_arch_long_1849','P3:09a_arch_ether_dome_1847']
FONT='/System/Library/Fonts/Supplemental/Didot.ttc'

def write(path,data):path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--cache',type=Path,required=True);ap.add_argument('--pages',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False)
 recovery=json.loads((HERE/'ARCHIVE_RECOVERY_v05.json').read_text());sources={s['row_id']:s for s in recovery['sources']};pages={s['asset_id']:s for s in recovery['page_extracts'] if s['pdf_page_1based']!=712}
 plan=json.loads((HERE/'PICTURE_PLAN_v03.json').read_text());stt=HERE.parent/plan['vo_lock']['stt_raw'];raw=json.loads(stt.read_text());words=[dict(w,raw_index=i) for i,w in enumerate(raw['words']) if w['type']=='word']
 result={'job':'J2563','film_stage_approved':False,'motion_review':False,'audio_review':False,'spend_gbp':0,'credits_used':0,'plan_sha256':sha(HERE/'PICTURE_PLAN_v03.json'),'stt_sha256':sha(stt),'rows':[],'scope':'Four cached archive review rows only; eight other archive rows plus Morton composite, full cues and rough remain unfinished'}
 for r in plan['rows']:
  if r['row_id'] not in SELECTED:continue
  s=sources[r['row_id']];original=a.cache/s['file_name'];assert sha(original)==s['sha256']
  source=original;page=pages.get(s['asset_id']);highlights=[];cues=[]
  if page:
   source=a.pages/page['file_name'];assert sha(source)==page['sha256']
  if r['row_id'].startswith('P2:04'):
   c=anchor(words,'surgical operations',r['in_s'],r['out_s']);c.update(kind='source_highlight',out_s=r['out_s']);cues.append(c)
   # The full source paragraph, not an invented exact quote or OCR rewrite.
   import pymupdf
   doc=pymupdf.open(original);pg=doc[583];hits=pg.search_for('As nitrous oxide')+pg.search_for('of blood takes place.')
   assert len(hits)>=2;highlights=[(hits[0].x0*3,hits[0].y0*3,pg.rect.width*3-35,hits[-1].y1*3)]
  if r['row_id'].startswith('P2:09'):
   c=anchor(words,'seven years',r['in_s'],r['out_s']);c.update(kind='when',text='7 years later',out_s=min(r['out_s'],c['in_s']+2));cues.append(c)
   import pymupdf
   doc=pymupdf.open(original);pg=doc[710]
   highlights=[tuple(v*3 for v in h) for phrase in ['1849.','1842,'] for h in pg.search_for(phrase)];assert len(highlights)==2
  im=Image.open(source).convert('RGB');crop=None
  if r['row_id'].startswith('P2:04'):
   crop=(120,720,1020,1030);im=im.crop(crop);highlights=[(x0-crop[0],y0-crop[1],x1-crop[0],y1-crop[1]) for x0,y0,x1,y1 in highlights]
  source_width=im.width;im.thumbnail((1540,850),Image.Resampling.LANCZOS);iw,ih=im.size
  frames=round(r['duration_s']*FPS);target=a.out/(r['row_id'].replace(':','_')+'.mp4');proc=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',str(target)],stdin=subprocess.PIPE)
  credit_intervals=[(r['in_s'],r['out_s'])]
  if cues and cues[0].get('text'):credit_intervals=[(r['in_s'],cues[0]['in_s']),(cues[0]['out_s'],r['out_s'])]
  for n in range(frames):
   t=n/FPS;absolute=r['in_s']+t;canvas=Image.new('RGB',(1920,1080),(53,34,24));d=ImageDraw.Draw(canvas)
   # Approved archive movement: small lateral translation on a fixed mount,
   # no zoom, source repaint, heavy blur or generated scene substitution.
   x=round((1920-iw)/2+10*math.sin(t*.25));y=round((980-ih)/2)
   d.rectangle((x-16,y-16,x+iw+16,y+ih+16),fill=(220,204,169));canvas.paste(im,(x,y))
   if highlights and absolute>=cues[0]['in_s']:
    p=min(1,(absolute-cues[0]['in_s'])/.7);scale=iw/source_width
    for x0,y0,x1,y1 in highlights:
     d.line((x+x0*scale,y+y1*scale,x+(x0+(x1-x0)*p)*scale,y+y1*scale),fill=(187,135,47),width=4)
   active=next((c for c in cues if c.get('text') and c['in_s']<=absolute<c['out_s']),None)
   if active:d.text((80,970),active['text'],font=ImageFont.truetype(FONT,54,index=1),fill=(245,234,209))
   elif any(b<=absolute<e for b,e in credit_intervals):d.text((60,1005),s['credit'],font=ImageFont.truetype(FONT,32,index=1),fill=(245,234,209))
   if n==frames//2:canvas.save(a.out/(target.stem+'_layout.jpg'))
   proc.stdin.write(canvas.tobytes())
  proc.stdin.close();assert proc.wait()==0
  probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(target)]));v=probe['streams'][0];assert (v['width'],v['height'],v['avg_frame_rate'],int(v['nb_frames']))==(1920,1080,'30/1',frames)
  assert abs(float(v['duration'])-r['duration_s'])<=1/60+.00001
  credits=[{'kind':'archive_credit','text':s['credit'],'in_s':b,'out_s':e,'word_indices':[],'reason':'Source attribution, deferred while another label is visible'} for b,e in credit_intervals if e>b]
  rec={'row_id':r['row_id'],'path':str(target),'sha256':sha(target),'source':s,'page_extract':page,'source_crop_xyxy':crop,'plan_in_s':r['in_s'],'plan_out_s':r['out_s'],'frames':frames,'duration_s':float(v['duration']),'quantization_error_s':frames/FPS-r['duration_s'],'cues':cues,'credit_cues':credits,'review_status':'preliminary_requires_capable_motion_and_editorial_review','recipe':'Source fit on warm mount, lateral 10px sine drift; original pages with source-coordinate ink underlines; no narration change'}
  for c in cues:
   assert r['in_s']<=c['in_s']<c['out_s']<=r['out_s']
   assert c['in_s']==words[c['word_indices'][-1]]['start']
   if c.get('text'):assert all(c['out_s']<=z['in_s'] or c['in_s']>=z['out_s'] for z in credits)
  result['rows'].append(rec);write(a.out/'ARCHIVE_COMPOSITES_v06.json',result);print(r['row_id'],'rendered and mechanically checked',flush=True)
if __name__=='__main__':main()
