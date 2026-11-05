#!/usr/bin/env python3
"""J2163 read-only correction planner. Original J1880 code is preserved at bd530249.
No renderer is exposed: a separately scoped implementation must preserve source PTS,
packet-copy untouched closed GOPs and losslessly encode only recorded boundary GOPs.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess as sp
from fractions import Fraction
from pathlib import Path

EDIT_DIR = Path(__file__).resolve().parent
DEFAULT_MASTER = Path('/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_precheck/master_v03/hos_008_master_v03.mp4')
MASTER_SHA = 'cf1561c218bace7bc14ed3d625b0790a457027a90f392262f45ca7172723099b'
MASTER_BYTES = 393139693
EXPECTED_FRAMES = 12923

class PlanError(RuntimeError):
    pass

def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def require_hash(path, expected, size=None):
    path = Path(path)
    if not path.is_file():
        raise PlanError(f'Missing input: {path}')
    if size is not None and path.stat().st_size != size:
        raise PlanError(f'Size mismatch: {path}')
    actual = sha256_file(path)
    if actual != expected:
        raise PlanError(f'Hash mismatch: {path}: expected {expected}, actual {actual}')
    return actual

def write_new(path, data):
    # Exclusive creation: neither reports nor future outputs may replace evidence.
    with Path(path).open('x') as f:
        json.dump(data, f, indent=2)
        f.write('\n')

def strict_json(command):
    r = sp.run(command, capture_output=True, text=True, check=False)
    if r.returncode or r.stderr.strip():
        raise PlanError(f'Decode/probe failed: {r.stderr.strip()}')
    try:
        return json.loads(r.stdout)
    except ValueError as e:
        raise PlanError('Invalid probe output') from e

def validate_frames(raw, stream, expected_count=None):
    tb = Fraction(stream['time_base'])
    if not raw or (expected_count is not None and len(raw) != expected_count):
        raise PlanError(f'Short/missing decode: {len(raw)} frames; expected {expected_count}')
    frames = []
    for i, f in enumerate(raw):
        if 'pts' not in f or not ('duration' in f or 'pkt_duration' in f):
            raise PlanError(f'Missing actual PTS/duration at frame {i}')
        pts = int(f['pts']); duration = int(f.get('duration', f.get('pkt_duration')))
        if duration <= 0 or (frames and pts <= frames[-1]['pts']):
            raise PlanError(f'Invalid/nonmonotonic timestamp at frame {i}')
        frames.append({'index': i, 'pts': pts, 'duration': duration, 'key_frame': int(f['key_frame'])})
    start = Fraction(stream['start_pts']) * tb
    if Fraction(frames[0]['pts']) * tb != start:
        raise PlanError('Decoded start differs from stream start')
    # Gaps are evidence, never filled, collapsed, or converted to frame_index/24.
    gaps = []
    for a, b in zip(frames, frames[1:]):
        delta = b['pts'] - a['pts'] - a['duration']
        if delta:
            gaps.append({'after_frame': a['index'], 'delta_ticks': delta})
    end = frames[-1]['pts'] + frames[-1]['duration']
    if 'duration_ts' in stream and end != int(stream['start_pts']) + int(stream['duration_ts']):
        raise PlanError('Short decode or stream/decode end mismatch')
    return {'time_base': str(tb), 'start_pts': frames[0]['pts'], 'end_pts': end,
            'frames': frames, 'gaps': gaps, 'decoded_frames': len(frames)}

def probe_video(path, expected_count=None):
    data = strict_json(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                        '-show_streams', '-show_frames', '-show_entries',
                        'stream=time_base,start_pts,duration_ts,start_time,duration,nb_frames:frame=pts,duration,pkt_duration,key_frame',
                        '-of', 'json', str(path)])
    if len(data.get('streams', [])) != 1:
        raise PlanError('Expected one video stream')
    return validate_frames(data.get('frames', []), data['streams'][0], expected_count)

def build_plan(timeline, rows):
    frames = timeline['frames']; keys = [f['index'] for f in frames if f['key_frame']]
    if not keys or keys[0] != 0:
        raise PlanError('No initial random-access point')
    patches = []; previous = -1
    for row in rows:
        a, b = row['candidate_frames']
        if not 0 <= a <= b < len(frames) or a <= previous:
            raise PlanError('Invalid/overlapping patch interval')
        previous = b
        left = max(k for k in keys if k <= a)
        right = next((k for k in keys if k > b), len(frames))
        patches.append({**row, 'measured_pts_in': frames[a]['pts'],
                        'measured_pts_end': frames[b]['pts'] + frames[b]['duration'],
                        'source_frame_schedule': frames[a:b+1],
                        'candidate_boundary_gop_envelope': [left, right-1],
                        'boundary_policy': 'UNAPPROVED: closed-GOP dependency check required; lossless only outside changed frames; no global re-encode',
                        'pts_reconciled': False})
    return patches

def verify_plan(master=DEFAULT_MASTER, retakes=None):
    manifest = json.loads((EDIT_DIR / 'J2163_CORRECTION_MANIFEST.json').read_text())
    retakes = retakes or {}
    for name, item in retakes.items():
        # Explicitly requested missing/short retakes never fall back to another plate.
        require_hash(item['path'], item['sha256'])
        retake = probe_video(item['path'])
        minimum = {'p2_02': 160, 'p5_13': 135}.get(name)
        if minimum is None or retake['decoded_frames'] < minimum:
            raise PlanError(f'Short or unrecognized explicit retake: {name}')
    require_hash(master, MASTER_SHA, MASTER_BYTES)
    timeline = probe_video(master, EXPECTED_FRAMES)
    if Fraction(timeline['start_pts']) * Fraction(timeline['time_base']) != Fraction(1, 8):
        raise PlanError('Master start is not 0.125 s')
    if (timeline['end_pts'] - timeline['start_pts']) * Fraction(timeline['time_base']) != Fraction('539.5'):
        raise PlanError('Master video duration is not 539.500 s')
    inputs = []
    for item in manifest['required_inputs']:
        require_hash(item['path'], item['sha256'])
        source = probe_video(item['path'])
        tb = Fraction(source['time_base'])
        start, end = map(Fraction, item['required_seconds'])
        fs = source['frames']
        if fs[0]['pts'] * tb > start or source['end_pts'] * tb < end:
            raise PlanError(f'Short source interval: {item["path"]}')
        selected = [f for f in fs if start <= f['pts'] * tb < end]
        if len(selected) < item['minimum_frames']:
            raise PlanError(f'Insufficient actual frames: {item["path"]}')
        inputs.append({'path': item['path'], 'sha256': item['sha256'], 'available_frames': len(selected), 'decode': 'verified'})
    patches = build_plan(timeline, manifest['six_rows'])
    return {'status': 'PLANNED_NOT_EXECUTABLE', 'master': str(master), 'master_sha256': MASTER_SHA,
            'timeline': timeline, 'patches': patches, 'inputs': inputs,
            'frame_count_delta': 'UNMEASURED', 'vo_sync_lag_ms': 'UNMEASURED',
            'unchanged_frame_identity': 'UNMEASURED', 'audio_packet_identity_and_timestamps': 'UNMEASURED',
            'holds': manifest['holds'], 'spend_gbp': 0, 'media_rendered': False}

def extract_unchanged_range(*args, **kwargs):
    raise PlanError('Removed unsafe CFR/re-encode path. Future scoped packet/GOP splicer required.')

def execute_recipe(*args, **kwargs):
    raise PlanError('Execution refused: separate elected-Chief production scope and tested PTS/GOP splicer required.')

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--execute', action='store_true')
    ap.add_argument('--master', type=Path, default=DEFAULT_MASTER)
    ap.add_argument('--report', type=Path)
    ap.add_argument('--retake-p2-02', type=Path)
    ap.add_argument('--retake-p5-13', type=Path)
    ap.add_argument('--retake-p2-02-sha256')
    ap.add_argument('--retake-p5-13-sha256')
    args = ap.parse_args()
    if args.execute:
        ap.exit(2, 'Execution refused: J2163 permits code/evidence only.\n')
    if args.report and args.report.exists():
        ap.exit(2, 'Refusing to overwrite report.\n')
    retakes = {}
    for name in ('p2_02', 'p5_13'):
        path = getattr(args, 'retake_' + name)
        digest = getattr(args, 'retake_' + name + '_sha256')
        if path is not None:
            if not digest:
                ap.exit(2, 'Explicit retake requires expected SHA256.\n')
            retakes[name] = {'path': path, 'sha256': digest}
    try:
        report = verify_plan(args.master, retakes)
    except (OSError, PlanError, KeyError, ValueError) as e:
        print(json.dumps({'status': 'BLOCKED_INPUT_VALIDATION', 'error': str(e),
                          'frame_count_delta': 'UNMEASURED', 'vo_sync_lag_ms': 'UNMEASURED', 'media_rendered': False}))
        return 2
    if args.report:
        write_new(args.report, report)
    print(json.dumps({k: v for k, v in report.items() if k not in ('timeline', 'patches')}, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
