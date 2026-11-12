#!/usr/bin/env python3
"""Extract immutable, unapproved assembly inputs from the locked Vaccine master.

No generation, upload, or changes to originals. These are NOT finished Shorts.
"""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path('/Volumes/data/mac-mini-archive/hos-007-vaccine/master_v04_J0925/hos_007_master_v04.mp4')
EXPECTED = 'c7f62adbb241bf3fbfaa3a17929f05768eedcf89044cb2cc5ebd2971c163e810'
OUT = Path('/Users/benjaminoats/_desk/renders/J2230/vaccine_inputs_v01')
SRT = ROOT / '02_Video-Projects/007_The-First-Vaccine/11_Upload-Package/Captions/hos_007_master_v04.en.srt'

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(4 * 1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    assert sha(SOURCE) == EXPECTED, 'Wrong master: stop'
    blocks = {}
    for block in SRT.read_text().strip().split('\n\n'):
        lines = block.splitlines()
        blocks[int(lines[0])] = ' '.join(lines[2:])
    plans = [
        dict(id='variolation', title_draft='What Was Variolation?', air_draft='2026-11-25T11:30:00Z',
             intervals=[[67.66, 92.16]],
             text=' '.join(blocks[i] for i in range(16, 23))),
        dict(id='eradication', title_draft='How Was Smallpox Eradicated?', air_draft='2026-11-28T11:30:00Z',
             # Open with the outcome, then explain how; remove only the era clause.
             # 434.99 = Part05 start 409.59 + locked word start 25.40 (health).
             intervals=[[450.93, 458.69], [434.95, 444.09], [444.75, 449.89]],
             text=' '.join(blocks[i] for i in [117, 118]) + ' ' +
                  ' '.join(blocks[i] for i in [112, 113, 114]).split('century, ', 1)[1].capitalize() + ' ' +
                  ' '.join(blocks[i] for i in [115, 116])),
    ]
    for plan in plans:
        plan['word_count'] = len(plan['text'].split())
        assert 55 <= plan['word_count'] <= 65, plan
        plan['duration_s'] = round(sum(b-a for a,b in plan['intervals']), 3)
        assert 22 <= plan['duration_s'] <= 27, plan
        target = OUT / (plan['id'] + '_assembly_input_v01.mp4')
        # Preserve the native 1920x1080 picture and existing mix for edit reference.
        # This is not a crop/loop/caption/level-approved delivery file.
        if not target.exists():
            filters = []
            for i, (a,b) in enumerate(plan['intervals']):
                filters += [f'[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS[v{i}]',
                            f'[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS[a{i}]']
            inputs = ''.join(f'[v{i}][a{i}]' for i in range(len(plan['intervals'])))
            filters.append(inputs + f'concat=n={len(plan["intervals"])}:v=1:a=1[v][a]')
            subprocess.run(['ffmpeg','-nostdin','-n','-hide_banner','-loglevel','error','-i',str(SOURCE),
                            '-filter_complex',';'.join(filters),'-map','[v]','-map','[a]',
                            '-c:v','libx264','-preset','fast','-crf','20','-c:a','aac','-b:a','192k',
                            '-movflags','+faststart',str(target)],check=True)
        subprocess.run(['ffmpeg','-nostdin','-v','error','-i',str(target),'-f','null','-'],check=True)
        plan.update(file=str(target),sha256=sha(target),decode='PASS',
                    status='ASSEMBLY_INPUT_ONLY: not a finished Short; all Short gates and review pending')
    report = dict(job='J2230',source=str(SOURCE),source_sha256=EXPECTED,
                  timing_source='Locked master SRT; VO_RETIME_v01 locked word start for health; no obsolete character alignment',
                  spend=0,approval='NONE',plans=plans,
                  remaining=['Check exact splice boundaries with current word ends; ASR may mis-tokenize dates',
                             'Signed-out autocomplete and duplicate/retirement check',
                             'Native-motion vertical picture edit, distinct frame 0, 4-second terminal loop',
                             'Hook, word captions, exact live long title at 9-14 seconds and ending',
                             'Separate stems and current loudness/music/SFX/picture/polish/open gates',
                             'Independent review and durable verified final copies before awaits'])
    (OUT/'ASSEMBLY_INPUTS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__ == '__main__':
    main()
