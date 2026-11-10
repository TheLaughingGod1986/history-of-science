#!/usr/bin/env python3
"""Prepare immutable VO-only inputs. No generation, approval, upload or final edit."""
import hashlib
import json
import argparse
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MEDIA = Path('/Volumes/data/mac-mini-archive/2026-11-05/YouTube/History Of Science/02_Video-Projects/007_The-First-Vaccine/02_Voiceover')
BASE = Path('/Users/benjaminoats/_desk/renders/J2230')
SOURCES = {
    'variolation': ('part01_the_speckled_monster_v03.mp3', '3881da7b96b4efaadde58287c4151b31c1dd39d337af4fd5dae0c6925ab5fb83', 1, 0),
    'eradication': ('part05_the_word_that_saved_millions_v01b.mp3', '18b725326c0b40e6bba2250be9f25a2581366a2ff76a2121fa889191f727557f', 5, 409.59),
}


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--version', choices=['v01', 'v02'], default='v01')
    version = ap.parse_args().version
    OUT = BASE / f'vaccine_stems_{version}'
    if OUT.exists():
        raise SystemExit(f'Refusing to overwrite existing inputs: {OUT}')
    plans = json.loads((HERE / 'VACCINE_ASSEMBLY_INPUTS_v01.json').read_text())['plans']
    retime = json.loads((ROOT / '02_Video-Projects/007_The-First-Vaccine/07_Edit-Project/VO_RETIME_v01.json').read_text())
    # Validate every source before making any output.
    for name, expected, _, _ in SOURCES.values():
        if sha(MEDIA / name) != expected:
            raise SystemExit(f'Source hash mismatch: {name}')
    OUT.mkdir(parents=True)
    results = []
    for plan in plans:
        sid = plan['id']
        if version == 'v02' and sid != 'eradication':
            continue
        name, expected, part_no, master_offset = SOURCES[sid]
        spans = [[round(a-master_offset, 3), round(b-master_offset, 3)] for a, b in plan['intervals']]
        # v01 inherited a master-reference trim ending at raw 40.30 s, inside
        # "gone" (start 40.24, sentence end 40.60 in VO_RETIME). Keep v01;
        # v02 preserves that sentence through 40.72 s, before next at 41.38.
        if version == 'v02':
            spans[-1][1] = 40.72
        fc = [f'[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo[a{i}]' for i, (a, b) in enumerate(spans)]
        fc.append(''.join(f'[a{i}]' for i in range(len(spans))) + f'concat=n={len(spans)}:v=0:a=1[out]')
        wav = OUT / f'{sid}_vo_input_{version}.wav'
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-n', '-i', str(MEDIA/name), '-filter_complex', ';'.join(fc), '-map', '[out]', '-c:a', 'pcm_s16le', str(wav)], check=True)
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-i', str(wav), '-f', 'null', '-'], check=True)
        (OUT / f'{sid}.txt').write_text(plan['text'] + '\n')
        words = next(p['words'] for p in retime['parts'] if p['part'] == part_no)
        mapped = []
        clock = 0
        for a, b in spans:
            for t, word in words:
                if a <= t < b:
                    mapped.append({'text': word, 'start_s': round(clock+t-a, 3), 'source_start_s': t})
            clock += b-a
        result = {'id': sid, 'status': 'ASSEMBLY INPUT ONLY; opening FIX and all final gates/review pending', 'source': str(MEDIA/name), 'source_sha256': expected, 'source_part': part_no, 'master_offset_s': master_offset, 'source_intervals_s': spans, 'file': str(wav), 'sha256': sha(wav), 'duration_s': round(clock, 3), 'decode_exit': 0, 'expected_text': plan['text'], 'timing_words': mapped, 'timing_warning': 'VO_RETIME word starts are ASR estimates, not word-end proof. Preserve the canonical expected text; check splice consonants by ear. No fade, tempo or gain applied.', 'approval': 'NONE', 'spend': 0}
        (OUT / f'{sid}_timing.json').write_text(json.dumps(result, indent=2)+'\n')
        results.append(result)
    (OUT / 'STEM_INPUTS.json').write_text(json.dumps(results, indent=2)+'\n')
    (HERE / f'VACCINE_STEM_INPUTS_{version}.json').write_text(json.dumps(results, indent=2)+'\n')
    print(json.dumps([{'id': r['id'], 'duration_s': r['duration_s'], 'sha256': r['sha256'], 'decode_exit': r['decode_exit']} for r in results], indent=2))


if __name__ == '__main__':
    main()
