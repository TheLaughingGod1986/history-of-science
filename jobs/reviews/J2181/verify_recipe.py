"""J2181 read-only source evidence, not an assembler or a gate waiver.

Run from this HOS worktree; writes JSON here and stills under _desk only.
No media is modified. Native crop coordinates precede all scaling.
"""
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
DESK = Path('/Users/benjaminoats/_desk/handoff/J2181')
ROOT = HERE.parents[2]
FILM = ROOT / '02_Video-Projects/006_Trees-Are-Made-Of-Air'
RULE = json.loads((FILM / '10_Shorts/BUILD_RULE_v02.json').read_text())
MEDIA = Path(RULE['media_root']) / '04_Generated-Clips'
CANDIDATES = json.loads((HERE / 'CANDIDATE_PROBES.json').read_text())
by_id = {r['id']: r for r in CANDIDATES}
inventory = {}


def write(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2) + '\n')


def probe(path):
    if path not in inventory:
        p = Path(path)
        data = json.loads(subprocess.check_output([
            'ffprobe', '-v', 'error', '-show_entries',
            'format=duration:stream=codec_name,width,height,r_frame_rate',
            '-of', 'json', path]))
        v = next(s for s in data['streams'] if s.get('width'))
        inventory[path] = dict(path=path, sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                               bytes=p.stat().st_size, duration=float(data['format']['duration']),
                               width=v['width'], height=v['height'], probe=data)
    return inventory[path]


# (candidate id, native x/y/width/height, source in). Not KEEP.
changes = {
    ('Short_B', 'S01'): ('03_pot_jar_leaf', [700, 190, 460, 818], 1.0),
    ('Short_B', 'S02'): ('15_quill_vegetable', [0, 0, 608, 1080], 0.0),
    ('Short_B', 'S07'): ('01_soil_to_sky', [600, 0, 608, 1080], 0.0),
    ('Short_B', 'loop_tail'): ('03_pot_jar_leaf', [700, 190, 460, 818], 0.0),
    ('Short_C', 'S05'): ('03_pot_jar_leaf', [1120, 0, 608, 1080], 0.0),
}
all_checks = []
for sid in ['Short_B', 'Short_C']:
    original = next(s for s in RULE['shorts'] if s['id'] == sid)
    cuts = json.loads((HERE / f'{sid}_baseline_cuts.json').read_text())
    for c in cuts:
        row = c['row']
        duration = round(c['timeline_out'] - c['timeline_in'], 6)
        origin = next(r for r in original['rows'] if r['id'] == row)
        change = changes.get((sid, row))
        if change:
            candidate, crop, start = change
            c['source'] = by_id[candidate]['path']
        else:
            start = 1.0 if sid == 'Short_C' and row == 'S01' else 0.0
            a = probe(c['source'])
            # Full-height portrait crop; no intermediate 1920 normalization.
            width = 608 if a['height'] == 1080 else 404
            crop = [(a['width'] - width) // 2, 0, width, a['height']]
        a = probe(c['source'])
        x, y, w, h = crop
        end = round(start + duration, 6)
        upscale = max(1080 / w, 1920 / h)
        c.update(source_sha256=a['sha256'], source_in=start, source_out=end,
                 source_duration=a['duration'], source_dimensions=[a['width'], a['height']],
                 framing=dict(offset=start, crop_native_xywh=crop, output=[1080, 1920],
                              scale='lanczos', setsar=1, speed=1.0),
                 upscale=upscale, role='loop_tail' if row == 'loop_tail' else 'body',
                 qualification='proposal_requires_review' if change else 'inherited_requires_render_review')
        c.pop('offset_note', None)
        check = dict(short=sid, row=row, bounds_ok=0 <= start < end <= a['duration'],
                     crop_in_bounds=0 <= x and 0 <= y and x+w <= a['width'] and y+h <= a['height'],
                     upscale=upscale, upscale_ok=upscale <= 2.35)
        # Decode/hash every native cropped frame in the proposed interval.
        vf = f'crop={w}:{h}:{x}:{y}'
        proc = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(start), '-i', c['source'],
                               '-t', str(duration), '-an', '-vf', vf,
                               '-f', 'framemd5', '-'], text=True, capture_output=True)
        lines = [line for line in proc.stdout.splitlines() if line and not line.startswith('#')]
        hashes = [line.split(',')[-1].strip() for line in lines]
        check.update(decode_exit=proc.returncode, decode_stderr=proc.stderr,
                     decoded_frames=len(hashes), unique_frames=len(set(hashes)),
                     identical_adjacent_frames=sum(a == b for a, b in zip(hashes, hashes[1:])),
                     framehash_sha256=hashlib.sha256(proc.stdout.encode()).hexdigest(),
                     perceptual_motion_review=False)
        all_checks.append(check)
        # Selected replacement + opening/loop samples, not finished-cut frames.
        if change:
            times = [start, round(start + duration/2, 4), max(start, end-1/24)]
            for i, t in enumerate(times):
                dest = DESK / f'{sid}_{row}_{i}_native_crop.png'
                subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', c['source'],
                                '-frames:v', '1', '-vf', vf+',scale=270:480', '-y', str(dest)], check=True)
    write(f'{sid}_cuts.json', cuts)
    write(f'{sid}_pool.json', [dict(source=src, sha256=probe(src)['sha256'],
          title='Existing generated HOS006 KEEP long plate; new interval/crop unapproved',
          provenance='Original approved long plate, not archive footage',
          source_dimensions=[probe(src)['width'], probe(src)['height']])
          for src in dict.fromkeys(c['source'] for c in cuts)])
    write(f'{sid}_loop_proposal.json', dict(status='UNAPPROVED; contract pending J2179/J2182',
          opening_row='S01', terminal_row='loop_tail',
          source_sha256=cuts[0]['source_sha256'], source=cuts[0]['source'],
          opening_interval=[cuts[0]['source_in'], cuts[0]['source_out']],
          terminal_interval=[cuts[-1]['source_in'], cuts[-1]['source_out']],
          framing=cuts[0]['framing'],
          last_vo_word_s=23.08 if sid == 'Short_B' else 24.16,
          total_duration_s=original['total_duration_s'],
          note='Terminal 0–1s precedes opening source at1s. Same native crop. No declaration is passed to old checker; rendered correspondence/seam not verified.'))

write('SOURCE_INVENTORY.json', list(inventory.values()))
write('MACHINE_CHECKS.json', dict(job='J2181', source_only=True, rendered=False,
      note='Frame differences prove changing pixels, not perceived natural motion, anatomy or seamless loops.',
      rows=all_checks))
proposal = dict(job='J2181', status='PARTIAL_PROPOSAL_NOT_BUILD_READY', gbp=0,
    build_rule_sha256=hashlib.sha256((FILM/'10_Shorts/BUILD_RULE_v02.json').read_bytes()).hexdigest(),
    canonical_vo_sha256=dict(Short_B='0f1099262037b62ea2b2a003ce86e196458fa983e9ca97877afb5600e97c7479',
                            Short_C='5b5d84e560d51ed9ad6f9bf5588f458802620f48f008b9409c532f8a1ea4e269'),
    unchanged='All spoken lines and row times; original BUILD_RULE, exclusions, S7 planned-only and long/live stage unchanged.',
    rows=[dict(short=sid,row=row,candidate=cid,crop_native_xywh=crop,source_in=start,
               source_sha256=by_id[cid]['sha256']) for (sid,row),(cid,crop,start) in changes.items()],
    body_assignment=dict(Short_B_S04='Original 10_mint_jar_t1 now unique at S04; S01/loop change to pot_jar_leaf',
                         Short_B_S05='11_candle_tall_t1 now unique at S05'),
    blockers=[dict(short=r['short'],row=r['row'],reason='Native 720-high source requires >=2.6667x to fill 1920-high portrait, above2.35x')
              for r in all_checks if not r['upscale_ok']],
    system_dependency='J2180 FIX on PR512 be2c980ffa; J2179 corrections and J2182 re-review still required. No reopen of J2169.')
write('BUILD_RULE_J2181_REPAIR_PROPOSAL.json', proposal)
print(json.dumps(dict(sources=len(inventory), rows=len(all_checks),
                     bad_bounds=[r for r in all_checks if not r['bounds_ok']],
                     upscale_fail=[(r['short'],r['row'],r['upscale']) for r in all_checks if not r['upscale_ok']],
                     decode_fail=[(r['short'],r['row'],r['decode_stderr']) for r in all_checks if r['decode_exit']]),indent=2))
