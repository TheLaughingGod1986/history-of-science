"""Bounded J2563 free-graphics checkpoint, not a film-stage approval.

Five reconciled rows only. Immutable v03 timing and narration are inputs.
Render at 1920x1080/30 CFR; store media outside git. No network or generation.
"""
import argparse, hashlib, json, math, pathlib, subprocess
from PIL import Image, ImageDraw, ImageFont
HERE = pathlib.Path(__file__).resolve().parent
FONT = '/System/Library/Fonts/Supplemental/Didot.ttc'
W,H,FPS = 1920,1080,30
CREAM=(241,226,192); GOLD=(203,161,83)
# Full phrase labels reveal at the last anchor word, never before its information.
SELECTED=['P4:04c_cg_anesthesia_etymology','P5:09b_cg_safety_stadium','P5:12a_cg_anesthetist_monitor','P5:16a','P5:17_cream_end_card']
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d): p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def font(size): return ImageFont.truetype(FONT,size,index=1)
def label(im,text,y,size=76,alpha=1):
    layer=Image.new('RGBA',im.size);d=ImageDraw.Draw(layer);f=font(size)
    box=d.textbbox((0,0),text,font=f);x=(W-box[2])/2
    d.text((x,y),text,font=f,fill=(*CREAM,int(255*max(0,min(1,alpha)))))
    im.alpha_composite(layer)
def background(t):
    im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
    # Continuous subtle wood grain, no faux archival distress or camera zoom.
    for y in range(H):
        k=int(3*math.sin(y*.018)+2*math.sin(y*.071+t*.1))
        d.line((0,y,W,y),fill=(51+k,31+k,22+k,255))
    return im

def anchor(words,phrase,start,end):
    import re
    norm=lambda s:re.sub('[^a-z0-9]','',s.lower())
    tokens=[norm(w['text']) for w in words];target=[norm(x) for x in phrase.split()]
    matches=[i for i in range(len(words)-len(target)+1) if tokens[i:i+len(target)]==target and start<=words[i]['start']<end]
    if len(matches)!=1:raise ValueError((phrase,matches))
    i=matches[0];j=i+len(target)-1
    return {'phrase':phrase,'word_indices':list(range(i,j+1)),'raw_stt_indices':[words[n]['raw_index'] for n in range(i,j+1)],'in_s':words[j]['start'],'evidence_end_s':words[j]['end']}

def make_cues(row,words):
    rid=row['row_id'];a,b=row['in_s'],row['out_s'];cues=[]
    specs={SELECTED[0]:[('anesthesia','ANAESTHESIA',313.10),('without feeling','Without feeling',b)],SELECTED[1]:[('one in every hundred thousand','1 in 100,000',462.20),('90,000','90,000 people',b)],SELECTED[2]:[('just asleep enough','Just asleep enough',b)],SELECTED[3]:[('gas','A gas',525.74),('bag','A bag',526.76),('globe','A globe',b)]}
    for phrase,text,end in specs.get(rid,[]):
        c=anchor(words,phrase,a,b);c.update(text=text,out_s=min(end,b));cues.append(c)
    if rid==SELECTED[-1]:cues=[{'text':'History of Science','in_s':a,'out_s':b,'word_indices':[],'raw_stt_indices':[],'reason':'Approved post-VO end card; no spoken anchor'}]
    for x,y in zip(cues,cues[1:]):assert x['out_s']<=y['in_s']
    return cues

def frame(row,t,cues):
    im=background(t);d=ImageDraw.Draw(im);rid=row['row_id'];absolute=row['in_s']+t
    active=next((c for c in cues if c['in_s']<=absolute<c['out_s']),None)
    if rid==SELECTED[0]:
        # Inked feather/quill metaphor rather than unsourced Greek spellings/date.
        progress=min(1,t/1.4);d.arc((540,300,1380,760),190,190+160*progress,fill=GOLD,width=5)
        if active:label(im,active['text'],470,86,min(1,(absolute-active['in_s'])/.3))
    elif rid==SELECTED[1]:
        # Architectural bowl, not a literal 90,000-dot census or a premature death claim.
        onset=next(c['in_s'] for c in cues if c['text']=='90,000 people')
        if absolute>=onset:
            progress=min(1,(absolute-onset)/.7)
            for i in range(12):
                box=(420-i*17,260-i*8,1500+i*17,820+i*8)
                d.arc(box,0,360*progress,fill=GOLD,width=2)
            d.ellipse((690,420,1230,660),outline=CREAM,width=3)
        if active:label(im,active['text'],115,80,min(1,(absolute-active['in_s'])/.3))
    elif rid==SELECTED[2]:
        # Symbolic medicine balance. No diagnostic pulse trace or invented dose scale.
        angle=.07*math.sin(t*2)*math.exp(-t)
        d.line((960,370,960,800),fill=GOLD,width=7);d.line((790,800,1130,800),fill=GOLD,width=7)
        dx=370;dy=math.sin(angle)*dx
        d.line((960-dx,470-dy,960+dx,470+dy),fill=CREAM,width=6)
        for x,y in [(590,470-dy),(1330,470+dy)]:
            d.line((x,y,x-85,y+160),fill=GOLD,width=3);d.line((x,y,x+85,y+160),fill=GOLD,width=3)
            d.arc((x-100,y+90,x+100,y+220),0,180,fill=CREAM,width=4)
        if active:label(im,active['text'],150,76,min(1,(absolute-active['in_s'])/.3))
    elif rid==SELECTED[3]:
        # Each object appears only when its own word starts; previous one clears.
        if active:
            p=min(1,(absolute-active['in_s'])/.35);x0,x1=720,1200
            if active['text']=='A gas':
                for i in range(11):
                    x=960+180*math.sin(i*2.3+t*.6);y=540+120*math.cos(i*1.7+t*.4)
                    d.ellipse((x-11,y-11,x+11,y+11),outline=GOLD,width=3)
            elif active['text']=='A bag':
                pts=[(760,430),(1160,430),(1220,650),(1150,710),(770,710),(700,650),(760,430)]
                d.line(pts[:max(2,int(len(pts)*p))],fill=GOLD,width=6)
            else:
                d.arc((770,370,1150,750),0,360*p,fill=GOLD,width=6)
                d.line((820,405,820,315,860,315),fill=CREAM,width=5)
                d.line((1080,405,1080,315,1120,315),fill=CREAM,width=5)
            label(im,active['text'],150,90,p)
    else:
        label(im,'History of Science',410,100,min(1,t/.4))
        label(im,'DISCOVERY. WONDER. PROOF.',570,48,min(1,t/.4))
    return im.convert('RGB')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=pathlib.Path,required=True);args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    plan=json.loads((HERE/'PICTURE_PLAN_v03.json').read_text());raw=HERE.parent/plan['vo_lock']['stt_raw'];stt=json.loads(raw.read_text());words=[dict(w,raw_index=i) for i,w in enumerate(stt['words']) if w['type']=='word']
    result={'job':'J2563','scope':'five free graphics only; remaining 21 free rows and all 67 slates unbuilt','film_stage_approved':False,'audio_review':False,'motion_review':False,'plan_sha256':sha(HERE/'PICTURE_PLAN_v03.json'),'stt_sha256':sha(raw),'fps':FPS,'frame_size':[W,H],'rows':[],'source':'Own code; approved v03 row identities; unsupported inherited labels omitted, not spoken-line changes.'}
    for row in plan['rows']:
        if row['row_id'] not in SELECTED:continue
        cues=make_cues(row,words);frames=round(row['duration_s']*FPS);out=args.out/(row['row_id'].replace(':','_')+'.mp4')
        if out.exists():raise RuntimeError('Refusing to overwrite existing render '+str(out))
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(out)]
        print('Rendering',row['row_id'],frames,flush=True);proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
        try:
            for n in range(frames):proc.stdin.write(frame(row,n/FPS,cues).tobytes())
            proc.stdin.close();code=proc.wait();assert code==0
        except BaseException:
            proc.kill();raise
        probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]));v=probe['streams'][0]
        assert v['width']==W and v['height']==H and v['avg_frame_rate']=='30/1' and int(v['nb_frames'])==frames
        record={'row_id':row['row_id'],'path':str(out),'sha256':sha(out),'plan_in_s':row['in_s'],'plan_out_s':row['out_s'],'plan_duration_s':row['duration_s'],'frames':frames,'actual_duration_s':float(v['duration']),'quantization_error_s':frames/FPS-row['duration_s'],'cues':cues,'status':'rendered_requires_motion_and_layout_review'}
        assert abs(record['quantization_error_s'])<=1/60+.00001
        # Save a representative still only for layout inspection; never motion QA.
        sample_t=min(row['duration_s']-.04,max(.6,((cues[0]['in_s']-row['in_s']+.5) if cues else .6)))
        frame(row,sample_t,cues).save(args.out/(row['row_id'].replace(':','_')+'_layout.jpg'))
        result['rows'].append(record);dump(args.out/'FREE_GRAPHICS_MANIFEST_v03.json',result)
    print('Five graphic rows rendered and mechanically verified; no film-stage PASS.',flush=True)
if __name__=='__main__':main()
