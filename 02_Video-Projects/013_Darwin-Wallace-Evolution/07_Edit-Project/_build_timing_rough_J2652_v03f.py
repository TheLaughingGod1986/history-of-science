#!/usr/bin/env python3
"""Render an explicitly diagnostic v03f rough and 390px sheets, at zero spend.

Unavailable/short sources and unbuilt revised graphics become labelled slates.
Never stretches, loops, freezes or silently substitutes a missing source.
"""
import collections
from functools import lru_cache
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
SCRATCH=Path(os.environ.get('STUDIO_SCRATCH','/private/tmp'))/'J2652-render-v03f'
NAS=Path('/Volumes/data/studio-live/History Of Science/02_Video-Projects')/FILM.name
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'


@lru_cache(maxsize=None)
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
    plan=json.loads((EDIT/'PICTURE_PLAN_v03f.json').read_text())
    vo=NAS/'02_Voiceover/hos_013_vo_v03a.wav'
    assert sha(vo)==plan['vo_sha256']
    old=json.loads((EDIT/'timing_rough_J2498/asset_inventory_v01.json').read_text())
    assets={x['row']:x for x in old}
    # Archive inputs are diagnostic raw takes, not a claim that a take is KEEP.
    for r in plan['rows']:
        if r['source_kind'] not in ('new_mint_quality', 'existing_plate_reuse'):
            continue
        key = 'P1:01_study_beaks' if r['source_kind']=='existing_plate_reuse' else r['source_row_v02']
        part, rid = key.split(':')
        raw = NAS/'04_Generated-Clips/archive_v01_pass1'/f'P{int(part[1:]):02d}_{rid}_t1.mp4'
        receipt = Path(str(raw)+'.sha256.json')
        if raw.exists() and receipt.exists():
            expected = json.loads(receipt.read_text())['sha256']
            assert sha(raw)==expected, f'Archive receipt mismatch: {raw.name}'
            assets[r['source_row_v02']] = dict(source=str(raw), source_sha256=expected)
    # Current evidence directory is created only by this version's run.
    assert not (OUT/'ROUGH_MANIFEST_v03f.json').exists(), 'Completed version already exists'

    groups=collections.defaultdict(list)
    for r in plan['rows']:groups[r['source_row_v02']].append(r)
    watermark=SCRATCH/'diagnostic_watermark.png'
    wi=Image.new('RGBA',(960,540),(0,0,0,0));wd=ImageDraw.Draw(wi)
    wd.rectangle((8,502,490,534),fill=(0,0,0,190))
    wd.text((12,507),'TIMING ONLY - RAW TAKE - NOT KEEP',font=ImageFont.truetype(FONT,18),fill=(255,235,0,255))
    wi.save(watermark)
    inventory=[]; sheets=[]
    for i,r in enumerate(plan['rows']):
        duration=round(r['t_end_s']-r['t_s'],2)
        source=assets.get(r['source_row_v02'],{}).get('source')
        group=groups[r['source_row_v02']]
        offset=r['source_window_s'][0]
        reason='No hash-verified source for this timing beat'
        if r['source_kind'] in ('code_graphic','free_archive'):
            source=None
            reason='Revised graphic or archive composition remains unbuilt; prior baked art cannot verify this version'
        if source:
            assert sha(source)==assets[r['source_row_v02']]['source_sha256']
            available=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',source]))
            if offset+duration>available+.001:
                reason=f'Source too short: needs {offset+duration:.2f}s; has {available:.2f}s';source=None
            elif len(group)>1 and r['source_kind']=='code_graphic':
                reason='Split graphic needs distinct v03f render / moving background';source=None
        target=SCRATCH/f'row_{i:03d}.mp4'
        if source:
            args=['-ss',str(offset),'-i',source]
            crop = 'crop=trunc(iw*0.88/2)*2:trunc(ih*0.88/2)*2,' if ('_beat2' in r['id'] or r['id'].endswith('_detail')) else ''
            vf=crop+'scale=960:540:flags=lanczos,setsar=1,fps=50'
            args += ['-i',str(watermark)]
            filters=['-filter_complex',f'[0:v]{vf}[base];[base][1:v]overlay=0:0']
        else:
            im=Image.new('RGB',(960,540),'#293340');d=ImageDraw.Draw(im)
            lines=[f'J2652 DIAGNOSTIC — NOT A FINISHED CUT',f'P{r["part"]}:{r["id"]}',
                   f'{r["t_s"]:.2f}–{r["t_end_s"]:.2f} s',reason,'',*textwrap.wrap(r['shot_description'],65)]
            d.multiline_text((28,25),'\n'.join(lines),font=ImageFont.truetype(FONT,22),fill='white',spacing=7)
            slate=SCRATCH/f'row_{i:03d}.png';im.save(slate)
            args=['-loop','1','-framerate','50','-i',str(slate)];vf='setsar=1,fps=50'
            filters=['-vf',vf]
        run(['ffmpeg','-v','error','-y',*args,*filters,'-frames:v',str(round(duration*50)),
             '-an','-c:v','libx264','-preset','ultrafast','-crf','27','-pix_fmt','yuv420p','-threads','2',str(target)])
        frame=SCRATCH/f'frame_{i:03d}.jpg'
        run(['ffmpeg','-v','error','-y','-ss',str(duration/2),'-i',str(target),'-frames:v','1',str(frame)])
        record=dict(row=f'P{r["part"]}:{r["id"]}',start_s=r['t_s'],end_s=r['t_end_s'],
                    status='existing_render' if source else 'diagnostic_slate',source=source,
                    source_offset_s=offset if source else None,source_sha256=sha(source) if source else None,
                    crop='centred 88 percent diagnostic detail' if source and ('_beat2' in r['id'] or r['id'].endswith('_detail')) else None,
                    reason='Raw first take only; no KEEP or subject-framing acceptance' if source else reason)
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
        events.append(f'Dialogue: 0,{stamp(c["display_start_s"])},{stamp(c["display_end_s"])},Default,,0,0,0,,PLANNED CUE: {label}')
    ass.write_text(header+'\n'.join(events)+'\n')
    master=SCRATCH/'hos_013_timing_rough_J2652_v03f.mp4'
    run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(concat),'-i',str(vo),
         '-i',str(ass),'-map','0:v','-map','1:a','-map','2:s','-c:v','copy','-c:s','mov_text',
         '-threads','2','-c:a','aac','-b:a','192k','-af','apad','-t','515','-movflags','+faststart',str(master)])
    for page in range(math_ceil(len(sheets)/20)):
        im=Image.new('RGB',(390*4,260*5),'#202733');d=ImageDraw.Draw(im)
        for k,(path,r) in enumerate(sheets[page*20:(page+1)*20]):
            x=(k%4)*390;y=(k//4)*260
            thumb=Image.open(path).resize((390,219));im.paste(thumb,(x,y))
            d.text((x+4,y+221),f'{r["row"]}\n{r["start_s"]:.2f}–{r["end_s"]:.2f}',font=ImageFont.truetype(FONT,12),fill='white')
        dest=SCRATCH/f'phone_contact_v03f_{page+1:02d}.jpg';im.save(dest,quality=92)
    destdir=NAS/'07_Edit-Project/timing_rough_J2652';destdir.mkdir(parents=True,exist_ok=True)
    copies=[]
    for source in [master,*sorted(SCRATCH.glob('phone_contact_v03f_*.jpg'))]:
        dest=destdir/source.name
        assert not dest.exists(),f'Refusing overwrite: {dest}'
        shutil.copy2(source,dest);assert sha(source)==sha(dest)
        copies.append(dict(path=str(dest),sha256=sha(dest)))
    dump('asset_inventory_v03f.json',inventory)
    dump('ROUGH_MANIFEST_v03f.json',dict(files=copies,vo_sha256=sha(vo),plan_sha256=sha(EDIT/'PICTURE_PLAN_v03f.json'),
         duration_s=515,fps=50,credits_spent=0,gbp_spent=0,approved=False,
         slates=sum(r['status']=='diagnostic_slate' for r in inventory),
         limitations='Raw first takes with centred detail crops, not KEEP footage or approved framing. Selectable cue subtitles use display intervals. No music/SFX. All revised graphics and archive compositions are explicit slates. No audio or motion perception claimed.'))
    print('NAS COPY HASH VERIFIED',flush=True)


def math_ceil(x):
    return int(x) if int(x)==x else int(x)+1


if __name__=='__main__':main()
