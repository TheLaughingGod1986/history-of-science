"""Eight preliminary graphics; proposed retime reconciliation, not stage approval.

No network, generation or narration changes. Run with owb-cg Python, outside-git output.
Source v03 stays immutable. Chapter titles are editorial headings, not spoken labels.
"""
import argparse, json, math, pathlib, subprocess
import render_free_graphics_v02 as base
from PIL import ImageDraw
HERE=pathlib.Path(__file__).resolve().parent
CHAPTERS={2:('II','A Gas That Made People Laugh'),3:('III','This Is No Humbug'),4:('IV','The Fight Over Who Was First'),5:('V','Across the Ocean')}
SELECTED=['P1:04b_cg_stopwatch_scale','P1:07a_cg_three_chapters_map','P2:01_card_p02','P2:07b_cg_timeline_42yr','P3:01_card_p03','P4:01_card_p04','P4:06a_cg_master_timeline','P5:01_card_p05']

def cues_for(r,words):
    a,b=r['in_s'],r['out_s'];rid=r['row_id'];out=[]
    if '_card_' in rid:
        first=next(w['start'] for w in words if a<=w['start']<b)
        # Use the measured breath; never the stale hard-coded 0.70 s prose.
        out.append(dict(text=CHAPTERS[r['part']][1],in_s=a,out_s=first,word_indices=[],raw_stt_indices=[],reason='Editorial chapter heading in measured interchapter breath',kind='chapter_heading'))
        return out
    specs={
      SELECTED[0]:[('changed','changed',b)],
      SELECTED[1]:[('party trick','party trick',51.66),('country doctor','country doctor',b)],
      SELECTED[3]:[('March 1842','March 1842',152.5)],
      SELECTED[6]:[('two years earlier','two years earlier',329.44),('Crawford Long','Crawford Long',b)]}
    for phrase,text,end in specs.get(rid,[]):
        c=base.anchor(words,phrase,a,b);c.update(text=text,out_s=min(end,b),kind='spoken_label')
        if rid==SELECTED[3]:
            c['in_s']=max(c['in_s'],149.10) # previous Long WHO candidate ends here
            c['reconciliation']='Wait until preceding Long WHO clears at 149.10 s.'
        out.append(c)
    return out

def desk(im,t):
    d=ImageDraw.Draw(im)
    # Inked case folder on a perspective walnut desk; no camera zoom or fake archive.
    d.polygon([(140,300),(1600,250),(1830,940),(50,980)],fill=(68,42,27),outline=base.GOLD,width=3)
    d.polygon([(400,400),(1180,350),(1390,800),(430,870)],fill=(115,83,49),outline=base.CREAM,width=3)
    d.polygon([(400,400),(440,355),(720,335),(760,380)],fill=(115,83,49),outline=base.CREAM,width=3)
    # Animated ink stroke across the folder, never a still push.
    p=min(1,t/.65);d.line((520,730,520+660*p,700-20*p),fill=base.GOLD,width=4)
    d.ellipse((1460,400,1570,450),fill=(22,17,14),outline=base.GOLD,width=3)
    d.line((1500,415,1650,285),fill=base.CREAM,width=5)

def frame(r,t,cues):
    im=base.background(t);d=ImageDraw.Draw(im);a=r['in_s']+t
    active=next((c for c in cues if c['in_s']<=a<c['out_s']),None)
    if '_card_' in r['row_id']:
        desk(im,t)
        if active:
            # One grouped heading; 0.15 s fade within the short measured breath.
            alpha=min(1,(a-active['in_s'])/.15,(active['out_s']-a)/.15)
            base.label(im,CHAPTERS[r['part']][0],430,74,alpha)
            title=active['text'];size=64 if len(title)<27 else 54
            base.label(im,title,570,size,alpha)
    elif r['row_id']==SELECTED[0]:
        # No unspoken 3-minute/zero-pain claim in the retimed changed-only row.
        d.ellipse((710,290,1210,790),outline=base.GOLD,width=8)
        d.rounded_rectangle((890,230,1030,285),15,outline=base.CREAM,width=5)
        for i in range(12):
            q=i*math.pi/6;d.line((960+220*math.sin(q),540-220*math.cos(q),960+235*math.sin(q),540-235*math.cos(q)),fill=base.CREAM,width=3)
        q=min(1,t/1.5)*math.pi*1.5
        d.line((960,540,960+190*math.sin(q),540-190*math.cos(q)),fill=base.CREAM,width=6)
    elif r['row_id']==SELECTED[1]:
        # Only two promise stops occur inside this row; Boston is not revealed early.
        p=max(0,min(1,(a-50.52)/2));d.arc((420,330,1500,760),190,190+140*p,fill=base.GOLD,width=5)
        if active:
            x=610 if active['text']=='party trick' else 1320
            d.ellipse((x-38,520,x+38,596),outline=base.CREAM,width=5)
            if active['text']=='party trick':
                d.polygon([(x-50,385),(x+50,385),(x+65,470),(x-65,470)],outline=base.GOLD,width=4)
            else:
                d.line((x-30,400,x+30,460),fill=base.GOLD,width=5);d.line((x+30,400,x-30,460),fill=base.GOLD,width=5)
    else:
        # Drawing is a neutral time span. Dates/claims absent from this line are omitted.
        p=min(1,t/1.0);d.line((400,560,400+1120*p,560),fill=base.GOLD,width=5)
        for x in (400,1520):d.line((x,520,x,600),fill=base.CREAM,width=5)
        if r['row_id']==SELECTED[3] and a>=149.10:
            q=min(1,(a-149.1)/.6);d.arc((1415,455,1625,665),0,360*q,fill=base.GOLD,width=4)
        if r['row_id']==SELECTED[6] and active and active['text']=='Crawford Long':
            q=min(1,(a-active['in_s'])/.5);d.line((1520,560,1520-700*q,560),fill=base.CREAM,width=8)
    if active and '_card_' not in r['row_id']:
        base.label(im,active['text'],130,78,min(1,(a-active['in_s'])/.3))
    return im.convert('RGB')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=pathlib.Path,required=True);args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    plan=json.loads((HERE/'PICTURE_PLAN_v03.json').read_text());raw=HERE.parent/plan['vo_lock']['stt_raw'];stt=json.loads(raw.read_text());words=[dict(w,raw_index=i) for i,w in enumerate(stt['words']) if w['type']=='word']
    result=dict(job='J2563',scope='eight remaining preliminary code graphics; no archives or rough',plan_sha256=base.sha(HERE/'PICTURE_PLAN_v03.json'),stt_sha256=base.sha(raw),film_stage_approved=False,motion_review=False,audio_review=False,fps=30,rows=[],editorial_holds=['Four teaching graphics simplify inherited visual prose to fit actual words. Chief review required; these are not final DATA/SCALE compliance.', 'Chapter headings occupy only the actual 0.8–0.86 s breaths. Readability needs editorial review; no breathing time added.', 'No E2 opening approval claimed. Full overlay schedule still unfinished.'])
    for r in plan['rows']:
        if r['row_id'] not in SELECTED:continue
        cues=cues_for(r,words);frames=round(r['duration_s']*30);out=args.out/(r['row_id'].replace(':','_')+'.mp4')
        if out.exists():raise RuntimeError('Refusing overwrite '+str(out))
        proc=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size','1920x1080','-framerate','30','-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
        print('Rendering',r['row_id'],frames,flush=True)
        try:
            for n in range(frames):proc.stdin.write(frame(r,n/30,cues).tobytes())
            proc.stdin.close();assert proc.wait()==0
        except BaseException:proc.kill();raise
        sample=(cues[-1]['in_s']-r['in_s']+.15) if cues else .5
        if '_card_' in r['row_id']:sample=.35
        frame(r,min(r['duration_s']-.04,sample),cues).save(out.with_name(out.stem+'_layout.jpg'))
        result['rows'].append(dict(row_id=r['row_id'],path=str(out),sha256=base.sha(out),frames=frames,plan_in_s=r['in_s'],plan_out_s=r['out_s'],plan_duration_s=r['duration_s'],cues=cues,status='preliminary_requires_Chief_editorial_and_motion_review'))
        base.dump(args.out/'REMAINING_GRAPHICS_MANIFEST_v04.json',result)
    print('Eight preliminary graphics rendered; verification and editorial review remain.',flush=True)
if __name__=='__main__':main()
