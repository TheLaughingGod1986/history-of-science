#!/usr/bin/env python3
"""J3871 repair of J3816 failed draft: only locked 009 narration and pictures; never uploads."""
import hashlib, importlib.util, json, subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
SHARED=Path('/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/009_The-Falling-Moon-Gravity')
NAS=Path('/Volumes/data/studio-live/History Of Science/02_Video-Projects/009_The-Falling-Moon-Gravity')
WORK=Path('/Volumes/MiniWork/scratch/J3871-build-v04'); WORK.mkdir(exist_ok=True)
SPEC=importlib.util.spec_from_file_location('house',HERE.parents[1]/'008_Lightning-Franklin/10_Shorts/_build_short_s04_no_patent_v01.py')
b=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(b)
MASTER=Path('/Volumes/MiniWork/scratch/J3314-assembly/hos009_long_master_v03.mp4')
assert b.sha256(MASTER)=='744f32b7f2f95e75fabf039a345aee6c7c01ab6f304a932ebe7172bd3b3ede55'
VO=SHARED/'02_Voiceover/hos_009_part02_an_apple_in_a_plague_year_v01.mp3'
assert b.sha256(VO)=='3685590755967b2267d209a2847821df7088d60b1fa602328b0025dfb017eadc'
STEM='hos_009_s03_apple_head_v04'; TOTAL=17.10
# Whole sentences: rebuttal first, then Newton's later account, ending in the falling apple.
SLICES=[(139.50,144.44),(127.82,138.76)]
words=[];offset=0
raw=json.loads((SHARED/'02_Voiceover/stt/hos_009_part02_an_apple_in_a_plague_year_v01/stt_raw.json').read_text())['words']
for i,(start,end) in enumerate(SLICES):
 ss=start-86.34;ee=end-86.34
 b.ff('-ss',str(ss),'-t',str(end-start),'-i',str(VO),'-ar','48000','-ac','2',str(WORK/f'vo{i}.wav'))
 for w in raw:
  if w.get('type')=='word' and w['start']>=ss-.02 and w['end']<=ee+.02:
   words.append({'word':w['text'],'start':round(w['start']-ss+offset,3),'end':round(w['end']-ss+offset,3)})
 offset+=end-start
(WORK/'voice.txt').write_text("file 'vo0.wav'\nfile 'vo1.wav'\n")
b.ff('-f','concat','-safe','0','-i',str(WORK/'voice.txt'),'-af',f'apad=whole_dur={TOTAL}','-t',str(TOTAL),str(WORK/'vo.wav'))
# Actual native source windows and portrait crop; terminal 0.9s is pre-roll into opening source time.
BEATS=[(0,0.8,139.50,1028),(0.8,4.94,144.41,1028),(4.94,8.24,127.82,950),(8.24,11.54,131.12,1040),(11.54,16.20,134.42,1028),(16.20,17.10,138.30,1028)]
ARCHIVE=Path('/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/009_The-Falling-Moon-Gravity/04_Generated-Clips/part02/raw/v01')
CLEAN=[(ARCHIVE/'08_the_apple_t1.mp4',0.9),(ARCHIVE/'06_old_newton_tells_t1.mp4',0),(ARCHIVE/'06_old_newton_tells_t1.mp4',4.14),(ARCHIVE/'07_orchard_bench_t1.mp4',0),(ARCHIVE/'07_orchard_bench_t1.mp4',3.3),(ARCHIVE/'08_the_apple_t1.mp4',0)]
for i,(a,z,s,cx) in enumerate(BEATS):
 src,ss=CLEAN[i]
 b.ff('-ss',str(ss),'-i',str(src),'-t',str(z-a),'-an','-vf',f'scale=3008:1692:flags=lanczos,crop=952:1692:{cx}:0,setsar=1,fps=30','-c:v','libx264','-preset','veryfast','-crf','18',str(WORK/f'seg{i}.mp4'))
(WORK/'pic.txt').write_text(''.join(f"file 'seg{i}.mp4'\n" for i in range(len(BEATS))))
b.ff('-f','concat','-safe','0','-i',str(WORK/'pic.txt'),'-c','copy',str(WORK/'picture.mp4'))
b.TOTAL=TOTAL;b.HOOK_OUT=1.65;b.HOOK_LINES=["The apple **didn't**",'hit him on','the head.']
b.LONG_TITLE='How Isaac Newton Proved Gravity Using the Moon';b.LONG_VIDEO_ID='wiyfRnsTfTY'
# Reuse house text rendering. WHO sourced in long FACT_NOTES, no added spoken claim.
card_source=Path(b.__file__).read_text();old=b.render_who_card
# Draw explicit house card with truthful identity and sourced years.
from PIL import Image,ImageDraw,ImageFont
im=Image.new('RGBA',(952,1692));dr=ImageDraw.Draw(im)
f=ImageFont.truetype(b.FONT,58,index=2)
b._draw_styled_lines(dr,[[('Isaac Newton',False)],[('1642–1727',True)]],f,880,bg=(28,22,18,175));im.save(WORK/'who.png')
overlays=[]
b.render_hook(WORK/'hook.png');overlays.append((WORK/'hook.png',0,1.65))
for i,c in enumerate(b.chunk_words(words)):
 p=WORK/f'cap{i}.png';b.render_caption(p,c['styled']);overlays.append((p,c['t0'],c['t1']))
b.render_long_title(WORK/'title.png');overlays.append((WORK/'title.png',9,13.8));overlays.append((WORK/'who.png',5,8))
b.ff('-i',str(WORK/'kit/sfx_hos_tick_ink_v01.wav'),'-af',f'volume=-9dB,adelay=5000|5000,apad=whole_dur={TOTAL}','-t',str(TOTAL),str(WORK/'sfx.wav'))
args=['-i',str(WORK/'picture.mp4'),'-i',str(WORK/'vo.wav'),'-ss','140','-i',str(SHARED/'05_Music/hos_009_score_v04_synth.wav')]
args+=['-i',str(WORK/'sfx.wav')]
for p,a,z in overlays:args+=['-loop','1','-i',str(p)]
fc=[];last='[0:v]'
for i,(p,a,z) in enumerate(overlays,4):
 inp=f'[{i}:v]'
 if p.name=='who.png':
  fc.append(f'[{i}:v]format=rgba,fade=t=in:st=5:d=0.35:alpha=1,fade=t=out:st=7.65:d=0.35:alpha=1[who]');inp='[who]'
 fc.append(f"{last}{inp}overlay=0:0:enable='gte(t,{a})*lt(t,{z})'[v{i}]");last=f'[v{i}]'
fc.append(f'[2:a]atrim=0:{TOTAL},volume=-24dB[b];[1:a][b][3:a]amix=inputs=3:normalize=0,loudnorm=I=-13.3:TP=-2:LRA=11[a]')
out=WORK/f'{STEM}.mp4'
b.ff(*args,'-filter_complex',';'.join(fc),'-map',last,'-map','[a]','-t',str(TOTAL),'-r','30','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(out))
qa=HERE/'J3871/v04';qa.mkdir(parents=True,exist_ok=True)
meta={'clean_sources':[{'path':str(p),'in':t,'sha256':b.sha256(p)} for p,t in CLEAN],'job':'J3871','film':'009','status':'DRAFT, NOT PASSED','title_draft':"Did Newton’s Apple Hit His Head?",'master_source':str(MASTER),'master_source_sha256':b.sha256(MASTER),'draft':str(out),'sha256':b.sha256(out),'duration_s':b.probe(out),'vo_slices_master_time':SLICES,'vo_source':str(VO),'spoken':' '.join(w['word'] for w in words),'words':words,'picture_plan':[{'timeline_in':a,'timeline_out':z,'crop_x':cx,'source':str(src),'source_in':ss,'source_sha256':b.sha256(src)} for (a,z,_,cx),(src,ss) in zip(BEATS,CLEAN)],'upscale_from_720p':2.35,'heard':False,'watched':False,'spend':0}
(qa/'BUILD.json').write_text(json.dumps(meta,indent=2)+'\n')
(qa/'words.json').write_text(json.dumps({'words':words},indent=2)+'\n')
(qa/'spoken.txt').write_text(meta['spoken']+'\n')
print(json.dumps({k:meta[k] for k in ['draft','duration_s','spoken','sha256']}))
