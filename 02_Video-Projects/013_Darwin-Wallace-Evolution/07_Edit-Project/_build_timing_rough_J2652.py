#!/usr/bin/env python3
"""Render an explicitly diagnostic v03 rough and 390px sheets, at zero spend.

Unavailable/short sources and unbuilt revised graphics become labelled slates.
Never stretches, loops, freezes or silently substitutes a missing source.
"""
import collections
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import textwrap
from PIL import Image, ImageDraw, ImageFont

EDIT=Path(__file__).resolve().parent
FILM=EDIT.parent
OUT=EDIT/'timing_rough_J2652'
SCRATCH=Path(os.environ.get('STUDIO_SCRATCH','/private/tmp'))/'J2652-render'
NAS=Path('/Volumes/data/studio-live/History Of Science/02_Video-Projects')/FILM.name
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'


def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()


def run(args):
    subprocess.run(args,check=True)


def dump(name,data):
    (OUT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')


def main():
    SCRATCH.mkdir(exist_ok=True,parents=True)
    plan=json.loads((EDIT/'PICTURE_PLAN_v03.json').read_text())
    vo=NAS/'02_Voiceover/hos_013_vo_v03a.wav'
    assert sha(vo)==plan['vo_sha256']
    old=json.loads((EDIT/'timing_rough_J2498/asset_inventory_v01.json').read_text())
    assets={x['row']:x for x in old}
    groups=collections.defaultdict(list)
    for r in plan['rows']:groups[r['source_row_v02']].append(r)
    inventory=[]; sheets=[]
    for i,r in enumerate(plan['rows']):
        duration=round(r['t_end_s']-r['t_s'],2)
        source=assets.get(r['source_row_v02'],{}).get('source')
        group=groups[r['source_row_v02']]
        offset=round(r['t_s']-group[0]['t_s'],2)
        reason='Source not in the verified J2498 render inventory'
        if source:
            assert sha(source)==assets[r['source_row_v02']]['source_sha256']
            available=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',source]))
            if offset+duration>available+.001:
                reason=f'Source too short: needs {offset+duration:.2f}s; has {available:.2f}s';source=None
            elif len(group)>1 and r['source_kind']=='code_graphic':
                reason='Split graphic needs distinct v03 render / moving background';source=None
        target=SCRATCH/f'row_{i:03d}.mp4'
        if source:
            args=['-ss',str(offset),'-i',source]
            vf='scale=960:540:flags=lanczos,setsar=1,fps=50'
        else:
            im=Image.new('RGB',(960,540),'#293340');d=ImageDraw.Draw(im)
            lines=[f'J2652 DIAGNOSTIC — NOT A FINISHED CUT',f'P{r["part"]}:{r["id"]}',
                   f'{r["t_s"]:.2f}–{r["t_end_s"]:.2f} s',reason,'',*textwrap.wrap(r['shot_description'],65)]
            d.multiline_text((28,25),'\n'.join(lines),font=ImageFont.truetype(FONT,22),fill='white',spacing=7)
            slate=SCRATCH/f'row_{i:03d}.png';im.save(slate)
            args=['-loop','1','-framerate','50','-i',str(slate)];vf='setsar=1,fps=50'
        run(['ffmpeg','-v','error','-y',*args,'-vf',vf,'-frames:v',str(round(duration*50)),
             '-an','-c:v','libx264','-preset','ultrafast','-crf','27','-pix_fmt','yuv420p','-threads','2',str(target)])
        frame=SCRATCH/f'frame_{i:03d}.jpg'
        run(['ffmpeg','-v','error','-y','-ss',str(duration/2),'-i',str(target),'-frames:v','1',str(frame)])
        record=dict(row=f'P{r["part"]}:{r["id"]}',start_s=r['t_s'],end_s=r['t_end_s'],
                    status='existing_render' if source else 'diagnostic_slate',source=source,
                    source_offset_s=offset if source else None,reason=None if source else reason)
        inventory.append(record)
        sheets.append((frame,record))
        print(f'{i+1}/{len(plan["rows"])} {record["row"]} {record["status"]}',flush=True)
    concat=SCRATCH/'concat.txt';concat.write_text(''.join(f"file 'row_{i:03d}.mp4'\n" for i in range(len(plan['rows']))))
    # Diagnostic cue subtitles display the planned onset; old art may retain its
    # old label. These are not represented as final composited teach graphics.
    ass=SCRATCH/'onsets.ass'
    def stamp(t):
        return f'{int(t//3600)}:{int(t//60)%60:02d}:{t%60:05.2f}'
    header='[Script Info]\nScriptType: v4.00+\nPlayResX: 960\nPlayResY: 540\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Default,Arial,20,&H0000FFFF,&H0000FFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,3,2,0,8,20,20,12,1\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
    events=[]
    for c in plan['overlay_cues']:
        if c['status']!='ANCHORED':continue
        label=c['overlay'].get('line_1',c['overlay'].get('label',''))
        events.append(f'Dialogue: 0,{stamp(c["onset_s"])},{stamp(c["onset_s"]+min(c["overlay"].get("hold_s",3),4))},Default,,0,0,0,,PLANNED CUE: {label}')
    ass.write_text(header+'\n'.join(events)+'\n')
    master=SCRATCH/'hos_013_timing_rough_J2652_v03.mp4'
    run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(concat),'-i',str(vo),
         '-i',str(ass),'-map','0:v','-map','1:a','-map','2:s','-c:v','copy','-c:s','mov_text',
         '-threads','2','-c:a','aac','-b:a','192k','-af','apad','-t','515','-movflags','+faststart',str(master)])
    for page in range(math_ceil(len(sheets)/20)):
        im=Image.new('RGB',(390*4,260*5),'#202733');d=ImageDraw.Draw(im)
        for k,(path,r) in enumerate(sheets[page*20:(page+1)*20]):
            x=(k%4)*390;y=(k//4)*260
            thumb=Image.open(path).resize((390,219));im.paste(thumb,(x,y))
            d.text((x+4,y+221),f'{r["row"]}\n{r["start_s"]:.2f}–{r["end_s"]:.2f}',font=ImageFont.truetype(FONT,12),fill='white')
        dest=SCRATCH/f'phone_contact_v03_{page+1:02d}.jpg';im.save(dest,quality=92)
    destdir=NAS/'07_Edit-Project/timing_rough_J2652';destdir.mkdir(parents=True,exist_ok=True)
    copies=[]
    for source in [master,*sorted(SCRATCH.glob('phone_contact_v03_*.jpg'))]:
        dest=destdir/source.name
        assert not dest.exists(),f'Refusing overwrite: {dest}'
        shutil.copy2(source,dest);assert sha(source)==sha(dest)
        copies.append(dict(path=str(dest),sha256=sha(dest)))
    dump('asset_inventory_v03.json',inventory)
    dump('ROUGH_MANIFEST_v03.json',dict(files=copies,vo_sha256=sha(vo),plan_sha256=sha(EDIT/'PICTURE_PLAN_v03.json'),
         duration_s=515,fps=50,credits_spent=0,gbp_spent=0,approved=False,
         slates=sum(r['status']=='diagnostic_slate' for r in inventory),
         limitations='Selectable diagnostic cue subtitles only; no music/SFX. Missing art and revised graphics are slates. No audio or motion perception claimed.'))
    print('NAS COPY HASH VERIFIED',flush=True)


def math_ceil(x):
    return int(x) if int(x)==x else int(x)+1


if __name__=='__main__':main()
