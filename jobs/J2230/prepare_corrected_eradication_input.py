#!/usr/bin/env python3
"""Repair J2230's obsolete master time mapping; preserve every old input."""
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MASTER = Path('/Volumes/data/mac-mini-archive/hos-007-vaccine/master_v04_J0925/hos_007_master_v04.mp4')
STEM = Path('/Volumes/data/mac-mini-archive/hos-007-vaccine/master_v03_J0887/stem_vo_v03.wav')
OUT = Path('/Users/benjaminoats/_desk/renders/J2230/eradication_corrected_inputs_v02')


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    if OUT.exists():
        raise SystemExit(f'Refusing overwrite: {OUT}')
    for path, expected in [(MASTER, 'c7f62adbb241bf3fbfaa3a17929f05768eedcf89044cb2cc5ebd2971c163e810'), (STEM, '289b543efd5d1e01975a75ab7b07e03f27fda0c0847bba75d532202f8917a8dd')]:
        assert sha(path) == expected, f'Hash mismatch: {path}'
    cuts = json.loads((ROOT/'02_Video-Projects/007_The-First-Vaccine/07_Edit-Project/master_v04_pack/cuts_full_join_v04.json').read_text())
    offsets = [r['timeline_in']-r['part_timeline_in'] for r in cuts if r.get('part') == 5]
    assert max(offsets)-min(offsets) < .001
    # Film Part 05 starts at frame 9647 / 24, not the obsolete VO_RETIME
    # planning offset 409.59. The actual v04 cuts agree to rounding precision.
    offset = 9647/24
    assert abs(offset-offsets[0]) < .001
    raw = [[41.34, 49.10], [25.36, 34.50], [35.16, 40.72]]
    spans = [[round(offset+a, 6), round(offset+b, 6)] for a,b in raw]
    OUT.mkdir(parents=True)
    clips=[]
    for i,(a,b) in enumerate(spans):
        dst=OUT/f'seg_{i:02}.mp4'
        subprocess.run(['ffmpeg','-nostdin','-v','error','-n','-ss',str(a),'-i',str(MASTER),'-t',str(b-a),'-c:v','libx264','-preset','fast','-crf','18','-c:a','aac','-b:a','192k',str(dst)],check=True)
        clips.append(dst)
    listing=OUT/'concat.txt'
    listing.write_text(''.join(f"file '{p.name}'\n" for p in clips))
    mp4=OUT/'eradication_assembly_input_v02.mp4'
    subprocess.run(['ffmpeg','-nostdin','-v','error','-n','-f','concat','-safe','0','-i',str(listing),'-c','copy',str(mp4)],check=True)
    fc=[f'[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS[a{i}]' for i,(a,b) in enumerate(spans)]
    fc.append('[a0][a1][a2]concat=n=3:v=0:a=1,volume=-7dB[out]')
    wav=OUT/'eradication_vo_from_master_v02.wav'
    subprocess.run(['ffmpeg','-nostdin','-v','error','-n','-i',str(STEM),'-filter_complex',';'.join(fc),'-map','[out]','-c:a','pcm_s16le',str(wav)],check=True)
    for path in [mp4,wav]:
        subprocess.run(['ffmpeg','-nostdin','-v','error','-i',str(path),'-f','null','-'],check=True)
    rec={'status':'ASSEMBLY INPUT ONLY; not a final Short or approval', 'master':str(MASTER),'master_sha256':sha(MASTER),'source_vo':str(STEM),'source_vo_sha256':sha(STEM),'part5_master_start_s':offset,'obsolete_part5_start_s':409.59,'raw_part5_intervals_s':raw,'master_intervals_s':spans,'file':str(mp4),'sha256':sha(mp4),'vo_file':str(wav),'vo_sha256':sha(wav),'vo_gain_db':-7,'duration_s':round(sum(b-a for a,b in raw),3),'decode_exit':0,'explanation':'Old input used obsolete planned film times and selects different narration. v02 follows actual master cut offsets. Last interval extends through raw 40.72 to preserve gone. Original v01 files remain untouched. Opening A disease still needs editorial FIX; had/have source flag requires actual listening. No new VO, music, picture, generation or publishing.'}
    (HERE/'ERADICATION_CORRECTED_INPUT_v02.json').write_text(json.dumps(rec,indent=2)+'\n')
    print(json.dumps(rec,indent=2))


if __name__=='__main__':
    main()
