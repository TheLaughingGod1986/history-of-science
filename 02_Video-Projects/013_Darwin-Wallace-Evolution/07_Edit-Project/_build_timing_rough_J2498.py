#!/usr/bin/env python3
"""Free diagnostic assembly; preserves merged v02 timings and never generates picture.

Run from any directory. Outputs media to scratch, then verifies a NAS copy.
Deliberately reports failed timing checks; this is not a delivery or QA approval.
"""
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import textwrap
from PIL import Image, ImageDraw, ImageFont

EDIT = Path(__file__).resolve().parent
FILM = EDIT.parent
NAS = Path('/Volumes/data/studio-live/History Of Science/02_Video-Projects') / FILM.name
OUT = EDIT / 'timing_rough_J2498'
SCRATCH = Path(os.environ.get('STUDIO_SCRATCH', '/Volumes/MiniWork/scratch')) / 'J2498-render'
FPS = 30
FONT = '/System/Library/Fonts/Supplemental/Arial.ttf'


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def save(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def run(args):
    subprocess.run(args, check=True)


def main():
    OUT.mkdir(exist_ok=True)
    SCRATCH.mkdir(parents=True, exist_ok=True)
    plan = json.loads((EDIT / 'PICTURE_PLAN_v02.json').read_text())
    transcript = json.loads((FILM / '02_Voiceover/stt/hos_013_vo_v03a/words_fw_small_en.json').read_text())
    words = transcript['words']
    vo = NAS / '02_Voiceover/hos_013_vo_v03a.wav'
    vo_hash = sha(vo)
    assert vo_hash == transcript['sha256'], 'VO does not match the word-timing input'
    # VO_STATUS J1310 is the lock; plan carries a different, erroneous hash.
    assert vo_hash == '837178125a72fb250d255f1039c5cb7f8630bbb313cf23801a1155f257d796e0'
    manifest = json.loads((EDIT / 'code_graphics_v01/CODE_GRAPHICS_v01.json').read_text())
    media = {r['id']: r for r in manifest['rendered_clips']}
    rows = []
    for part in sorted((EDIT / 'parts').glob('part-*_plates_v02.json')):
        d = json.loads(part.read_text())
        for r in d['plates']:
            r = dict(r)
            r['row'] = f"P{int(d['part'])}:{r['id']}"
            rows.append(r)
    assert len(rows) == 94
    assert all(not r.get('generation_authorized') for r in rows)
    assert all(r.get('quality') != 'Fast' for r in rows)
    cut_rows, inventory, issues, overlays = [], [], [], []
    for i, r in enumerate(rows):
        rid, start, end = r['row'], r['t_s'], r['t_end_s']
        if i:
            assert abs(rows[i-1]['t_end_s'] - start) < .001
        ws = [w for w in words if start <= (w['start'] + w['end']) / 2 < end]
        text = ''.join(w['word'] for w in ws).strip()
        kind = (r.get('teach_overlay') or {}).get('kind')
        cut_rows.append(dict(row=rid, source='CARD' if kind in ('CHAPTER', 'END_CARD') else r['source_kind'],
                             vo_in=start, vo_out=end, vo_text=text))
        if end-start > 8:
            issues.append(dict(row=rid, type='row_over_8s', start=start, end=end, duration=round(end-start, 3)))
        if i < len(rows)-1:
            prev = [w for w in words if (w['start']+w['end'])/2 < end]
            nxt = [w for w in words if (w['start']+w['end'])/2 >= end]
            crossing = [w for w in words if w['start']+.025 < end < w['end']-.025]
            if crossing:
                issues.append(dict(row=rid, type='cut_inside_word', cut=end, words=crossing))
            if prev and nxt and not re.search(r'[.!?]["\u201d\u2019\']?$', prev[-1]['word'].strip()):
                after = next((w['end'] for w in nxt if re.search(r'[.!?]["\u201d\u2019\']?$', w['word'].strip())), None)
                issues.append(dict(row=rid, type='cut_inside_sentence', cut=end,
                                   preceding_word=prev[-1]['word'].strip(), next_sentence_end=after,
                                   context=''.join(w['word'] for w in (prev[-7:]+nxt[:7])).strip()))
        overlay = r.get('teach_overlay') or {}
        if kind in ('WHO', 'WHEN', 'LABEL', 'FACT', 'DATA', 'EXPLAINER'):
            cue = dict(row=rid, kind=kind, planned_start=start, overlay=overlay,
                       status='NEEDS_EDITORIAL_ANCHOR', note='Plan has no explicit word-level overlay onset; row start is not verified sync.')
            if kind == 'WHO':
                name = overlay.get('line_1', '').split()
                candidates = []
                for j, w in enumerate(words):
                    excerpt = ''.join(x['word'] for x in words[j:j+len(name)])
                    if ' '.join(name).lower() in excerpt.lower():
                        candidates.append(w['start'])
                if candidates:
                    cue['nearest_name_onset'] = min(candidates, key=lambda t: abs(t-start))
                    cue['row_start_minus_name_s'] = round(start-cue['nearest_name_onset'], 3)
                    cue['status'] = 'MISALIGNED' if abs(cue['row_start_minus_name_s']) > .1 else 'ROW_START_ALIGNS'
            overlays.append(cue)
        record = media.get(rid)
        source = Path(record['nas_path']) if record else None
        if source and source.exists():
            assert sha(source) == record['sha256_mp4'], f'Changed existing render: {rid}'
            status = 'existing_render'
        else:
            source = None
            status = 'unminted_quality' if r['source_kind'].startswith('new_mint') else 'unavailable_free_or_reuse'
        inventory.append(dict(row=rid, start=start, end=end, status=status,
                              source=str(source) if source else None,
                              source_sha256=record['sha256_mp4'] if source else None))
    with open(OUT / 'cuts_v01.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['row', 'source', 'vo_in', 'vo_out', 'vo_text'], lineterminator='\n')
        writer.writeheader()
        writer.writerows(cut_rows)
    save('asset_inventory_v01.json', inventory)
    save('timing_issues_v01.json', issues)
    save('overlay_audit_v01.json', overlays)
    save('input_provenance_v01.json', dict(plan='PICTURE_PLAN_v02.json', plan_sha256=sha(EDIT/'PICTURE_PLAN_v02.json'),
        plan_vo_sha256=plan['vo_sha256'], actual_vo_sha256=vo_hash, transcript_sha256=transcript['sha256'],
        lock='02_Voiceover/VO_STATUS.md J1310', timings_changed=False,
        note='Diagnostic rough retains planned boundaries. Sentence-safe retiming requires Chief resolution of picture cadence and asset-length conflicts.'))
    checker = Path('/Users/benjaminoats/YouTube/orbit-with-ben/00_Brand/Channel-Setup/tools/clip_check.py')
    result = subprocess.run(['python3', str(checker), str(OUT/'cuts_v01.csv'), '--words',
        str(FILM/'02_Voiceover/stt/hos_013_vo_v03a/words_fw_small_en.json'), '--vo-end', '512.48', '--json'],
        text=True, capture_output=True)
    (OUT/'clip_check_v01.json').write_text(result.stdout)
    save('clip_check_exit_v01.json', dict(exit_code=result.returncode, stderr=result.stderr))
    for i, (r, asset) in enumerate(zip(rows, inventory)):
        target = SCRATCH / f'row_{i:03d}.mp4'
        frames = round(r['t_end_s']*FPS)-round(r['t_s']*FPS)
        if target.exists() and target.stat().st_size > 1000:
            continue
        if asset['source']:
            inputs = ['-i', asset['source']]
            vf = 'scale=960:540:flags=lanczos,setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=0.04'
        else:
            slate = SCRATCH / f'row_{i:03d}.png'
            content = f"{r['row']}\n{r['t_s']:.2f} - {r['t_end_s']:.2f} s\n"
            content += ('Veo 3.1 Quality - NOT MINTED' if asset['status']=='unminted_quality' else 'UNAVAILABLE FREE / REUSE SOURCE') + '\n\n'
            content += '\n'.join(textwrap.wrap(r['shot_description'], 72))
            im = Image.new('RGB', (960, 540), '#293340')
            draw = ImageDraw.Draw(im)
            draw.text((20, 16), 'J2498 TIMING ROUGH / SLATES / NOT FOR BEN', fill='white', font=ImageFont.truetype(FONT, 16))
            draw.multiline_text((40, 70), content, fill='white', font=ImageFont.truetype(FONT, 22), spacing=8)
            im.save(slate)
            inputs = ['-loop', '1', '-framerate', '30', '-i', str(slate)]
            vf = 'setsar=1,fps=30'
        run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', *inputs, '-vf', vf, '-frames:v', str(frames),
             '-an', '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '25', '-pix_fmt', 'yuv420p', '-threads', '2', str(target)])
        print(f'{i+1}/94 {r["row"]} {asset["status"]}', flush=True)
    concat = SCRATCH / 'concat.txt'
    concat.write_text(''.join(f"file 'row_{i:03d}.mp4'\n" for i in range(len(rows))))
    master = SCRATCH/'hos_013_timing_rough_J2498_v01.mp4'
    run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(concat),
         '-i', str(vo), '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
         '-af', 'apad', '-t', '515', '-movflags', '+faststart', str(master)])
    probe = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(master)]))
    assert abs(float(probe['format']['duration'])-515) < .1
    assert any(s['codec_type']=='audio' for s in probe['streams'])
    destination = NAS/'07_Edit-Project/timing_rough_J2498'/master.name
    destination.parent.mkdir(parents=True, exist_ok=True)
    assert not destination.exists(), 'Refusing to overwrite NAS rough'
    shutil.copy2(master, destination)
    digest = sha(master)
    assert sha(destination) == digest
    save('ROUGH_MANIFEST_v01.json', dict(path=str(destination), sha256=digest, duration_s=515,
        width=960, height=540, fps=FPS, existing_renders=sum(x['status']=='existing_render' for x in inventory),
        slates=sum(x['status']!='existing_render' for x in inventory), vo_sha256=vo_hash,
        audio='Locked VO only; no score or SFX; not a delivery mix.', credits_spent=0, gbp_spent=0,
        timings_changed=False, clip_check_exit=result.returncode, approved=False,
        limitations='Diagnostic only. Original plan timing faults preserved; overlays audited, not newly composited. No direct listening or motion review claimed.'))
    save('ffprobe_v01.json', probe)
    print(f'NAS COPY VERIFIED {destination} {digest}', flush=True)


if __name__ == '__main__':
    main()
