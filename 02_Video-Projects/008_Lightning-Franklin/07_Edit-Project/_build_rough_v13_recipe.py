#!/usr/bin/env python3
"""J2217 read-only correction planner. J2163's measured-PTS repair is kept.
Eight defect rows plus a film-wide caption panel. Execution stays refused until
J1881 re-reviews this amend. Original J1880 code remains at bd530249.
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

def clock_frame(frames, time_base, seconds):
    """Return the one decoded frame whose PTS interval contains this clock time."""
    tb = Fraction(time_base)
    t = Fraction(str(seconds))
    hits = []
    for f in frames:
        if isinstance(f, dict):
            idx, pts, dur = f['index'], f['pts'], f['duration']
        else:
            idx, pts, dur = f[0], f[1], f[2]
        start = Fraction(pts) * tb
        end = start + Fraction(dur) * tb
        if start <= t < end:
            hits.append(idx)
    if len(hits) != 1:
        raise PlanError(f'Clock {seconds}s matched {hits}')
    return hits[0]

# Keyframe alignment is not GOP closure. J2242 has to prove dependencies.
RETAKE_MIN_FRAMES = {'p2_02': 160, 'p5_13': 135, 'p3_01': 160}
MAX_STATIC_HOLD_S = 4
LABEL_SPLITS = {
    'THE ANSWER IS ON THE ROOF': ('THE ANSWER IS', 'ON THE ROOF'),
    'A KITE · A KEY · A JAR': ('A KITE', 'A KEY', 'A JAR'),
    'LET THE EXPERIMENT BE MADE': ('LET THE EXPERIMENT', 'BE MADE'),
    'PENNSYLVANIA GAZETTE · 19 OCTOBER 1752': ('PENNSYLVANIA GAZETTE', '19 OCTOBER 1752'),
}
AI_SPEND_CMDS = ('record', 'spend', 'report', 'doc')
BOUNDARY_POLICY = (
    'UNAPPROVED: candidate keyframe envelope only. Keyframe flags do not prove a closed GOP; '
    'dependency validation is outstanding. J2242 must prove dependencies and unchanged-frame/'
    'audio preservation before accepting output. Lossless only outside changed frames; no global re-encode.'
)

def label_words(text):
    return [w for w in str(text).replace('·', ' ').split() if w]

def sequential_labels(text):
    parts = LABEL_SPLITS.get(text)
    if parts is None:
        words = label_words(text)
        parts = tuple(' '.join(words[i:i + 4]) for i in range(0, len(words), 4)) or ('',)
    flat = []
    for part in parts:
        words = label_words(part)
        if not words or len(words) > 4:
            raise PlanError(f'Caption chunk exceeds four words: {part}')
        flat.extend(words)
    if flat != label_words(text):
        raise PlanError(f'Caption split changed the locked words: {text}')
    return parts

def as_frame_dicts(frames):
    out = []
    for f in frames:
        if isinstance(f, dict):
            out.append(f)
        else:
            out.append({'index': f[0], 'pts': f[1], 'duration': f[2], 'key_frame': f[3]})
    return out

def plan_captions(frames, time_base, labels, notes_text):
    """Planned cards only. No pixels. Timing comes from master PTS ticks."""
    frames = as_frame_dicts(frames)
    tb = Fraction(time_base)
    four = Fraction(MAX_STATIC_HOLD_S) / tb
    if four.denominator != 1:
        raise PlanError('4s hold is not an integer tick count')
    four = int(four)
    by_index = {f['index']: f for f in frames}
    cards = []
    windows = []

    def card_bounds(first, last, hi):
        start = by_index[first]['pts']
        if last < hi:
            end = by_index[last + 1]['pts']
        else:
            end = by_index[last]['pts'] + by_index[last]['duration']
        return start, end, end - start

    for lab in labels:
        lo, hi = lab['master_frames']
        if hi not in by_index or lo not in by_index:
            raise PlanError(f'Caption window is off the master: {lab["row"]}')
        start, end, span = card_bounds(lo, hi, hi)
        if span <= 0:
            raise PlanError(f'Empty caption window: {lab["row"]}')
        parts = sequential_labels(lab['label'])
        pending = list(range(lo, hi + 1))
        window_cards = []
        for i, text in enumerate(parts):
            if not pending:
                raise PlanError(f'No frames left for {lab["row"]}')
            left_parts = len(parts) - i
            target = max(1, len(pending) // left_parts)
            group = [pending.pop(0)]
            while pending and len(group) < target:
                _, _, hold = card_bounds(group[0], pending[0], hi)
                if hold > four:
                    break
                group.append(pending.pop(0))
            while len(group) > 1:
                _, _, hold = card_bounds(group[0], group[-1], hi)
                if hold <= four:
                    break
                pending.insert(0, group.pop())
            pts_in, pts_end, hold = card_bounds(group[0], group[-1], hi)
            if hold <= 0 or hold > four:
                raise PlanError(f'Caption hold out of range: {lab["row"]} {hold}')
            words = label_words(text)
            window_cards.append({
                'row': lab['row'],
                'source_label': lab['label'],
                'label': text,
                'words': words,
                'word_count': len(words),
                'sequence': i + 1,
                'sequence_of': len(parts),
                'pts_in': pts_in,
                'pts_end': pts_end,
                'hold_ticks': hold,
                'static_hold_s': str(Fraction(hold) * tb),
                'frame_in': group[0],
                'frame_last': group[-1],
                'background': 'unbordered umber',
                'border': False,
                'gold_rule': False,
                'pill_chrome': False,
                'over': 'moving plate',
                'one_at_a_time': True,
                'rendered': False,
                'new_claims': False,
                'splice': False,
            })
        remainder = by_index[pending[-1]]['pts'] + by_index[pending[-1]]['duration'] - by_index[pending[0]]['pts'] if pending else 0
        for card in window_cards:
            card['window_remainder_ticks'] = remainder
        windows.append({'row': lab['row'], 'pts_in': start, 'pts_end': end, 'remainder_ticks': remainder, 'cards': len(window_cards)})
        cards.extend(window_cards)
    for a, b in zip(cards, cards[1:]):
        if b['pts_in'] < a['pts_end']:
            raise PlanError(f'Caption cards overlap: {a["row"]} and {b["row"]}')
        if Fraction(a['hold_ticks']) * tb > MAX_STATIC_HOLD_S or a['word_count'] > 4:
            raise PlanError('Caption card breaks the 4-word or 4-second rule')
    if cards and (Fraction(cards[-1]['hold_ticks']) * tb > MAX_STATIC_HOLD_S or cards[-1]['word_count'] > 4):
        raise PlanError('Caption card breaks the 4-word or 4-second rule')
    for card in cards:
        for word in card['words']:
            if len(word) == 4 and word.isdigit() and word not in notes_text:
                raise PlanError(f'Year {word} is not in FACT_NOTES')
    return {'cards': cards, 'windows': windows, 'rendered': False, 'max_words': 4, 'max_static_hold_s': '4'}

def reconcile_bottom_text(cuts, labels):
    side = [(c['row'], c.get('side_label')) for c in cuts if c.get('side_label')]
    inv = [(lab['row'], lab['label']) for lab in labels]
    others = []
    for c in cuts:
        if c.get('side_label'):
            continue
        disp = c.get('disposition') or ''
        if 'SAFE PATH DOWN' in disp:
            kind = 'title_outside_side_label'
        elif c.get('quality') == 'code_graphic' or 'Code graphic' in disp or 'overlay_' in disp:
            kind = 'code_graphic_or_overlay'
        else:
            continue
        others.append({
            'row': c['row'],
            'kind': kind,
            'timeline_in': c.get('timeline_in'),
            'timeline_out': c.get('timeline_out'),
            'disposition': disp,
            'covered_by_side_label_inventory': False,
        })
    return {
        'side_label_count': len(side),
        'inventory_count': len(inv),
        'side_label_inventory_matches_cut_list': side == inv,
        'side_label_inventory_proves_film_wide_coverage': False,
        'missing_from_inventory': [list(s) for s in side if s not in inv],
        'inventory_not_in_cuts': [list(i) for i in inv if i not in side],
        'other_onscreen_text': others,
    }

def plan_safe_path(frames, time_base):
    """The rough-v12 safe-path title is bottom text the side_label list does not name."""
    frames = as_frame_dicts(frames)
    start = clock_frame(frames, time_base, '461.0473')
    hold_end = clock_frame(frames, time_base, '464.375')
    tb = Fraction(time_base)
    pts_in = frames[start]['pts']
    pts_limit = frames[hold_end]['pts']
    if pts_limit < pts_in:
        raise PlanError('Safe-path hold ends before it starts')
    four = int(Fraction(MAX_STATIC_HOLD_S) / tb)
    hold = min(four, pts_limit - pts_in)
    if hold <= 0:
        raise PlanError('Safe-path hold collapsed')
    text = 'SAFE PATH DOWN'
    return {
        'row': '11_safe_path',
        'source': 'rough_v12 disposition, not side_label',
        'label': text,
        'words': label_words(text),
        'word_count': len(label_words(text)),
        'pts_in': pts_in,
        'pts_end': pts_in + hold,
        'hold_ticks': hold,
        'static_hold_s': str(Fraction(hold) * tb),
        'frame_in': start,
        'disposition_hold_end_s': '464.375',
        'disposition_hold_end_frame': hold_end,
        'background': 'unbordered umber',
        'border': False,
        'rendered': False,
        'new_claims': False,
        'in_side_label_inventory': False,
        'note_resolved': False,
    }

def spend_preflight(ai_spend_py=None):
    spec = {
        'authorized': False,
        'gbp': 0,
        'no_top_up': True,
        'no_overage': True,
        'no_prepaid_ai_studio': True,
        'takes_max_per_plate': 3,
        'subscription_credits_max_per_plate': 300,
        'subscription_credits_max_total': 900,
        'plates': ['p2_02 salon spark', 'p3_01 points desk', 'p5_13 rods'],
        'ai_spend_cli': 'python3 scripts/ai_spend.py',
        'ai_spend_subcommands': list(AI_SPEND_CMDS),
        'ai_spend_check': 'not a subcommand; do not call it',
        'unposted_spends': 'Subtract ai_spend.py spends logged since the balance reading before judging headroom.',
        'live_balance': (
            'Read the Flow account with read_account() in '
            '02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/_mint_flow_cdp_v01.py '
            'on CDP ORBIT_FLOW_CDP (default http://127.0.0.1:9222), account the studio Ultra account. '
            'That is the route _mint_flow_v03.py already uses. Log it with '
            'ai_spend.py record --pool flow --left N.'
        ),
        'quality_price': (
            'Read the credit count on the Flow confirm dialog for Veo 3.1 Quality '
            "(orbit_flow_veo_ui.py matches 'Use N credits') before any Create. "
            'The historical TRY1 Quality=100 table is not the live price.'
        ),
        'log_spend': 'A future authorized take logs ai_spend.py spend --pool flow --amount N --film HOS:008. This FIX authorizes none.',
    }
    if ai_spend_py:
        text = Path(ai_spend_py).read_text()
        if 'add_parser("check"' in text or "add_parser('check'" in text:
            raise PlanError('ai_spend.py check is present; preflight text is stale')
        for cmd in AI_SPEND_CMDS:
            if f'add_parser("{cmd}"' not in text and f"add_parser('{cmd}'" not in text:
                raise PlanError(f'ai_spend.py is missing subcommand {cmd}')
        spec['ai_spend_py_checked'] = str(ai_spend_py)
    return spec

def load_manifest():
    manifest = json.loads((EDIT_DIR / 'J2163_CORRECTION_MANIFEST.json').read_text())
    if 'eight_rows' not in manifest:
        raise PlanError('J2217 eight-row amend missing; refusing to plan the six-row list')
    rows = manifest['eight_rows']
    if len(rows) != 8:
        raise PlanError('Expected eight defect rows')
    cap = manifest['caption_treatment']
    if cap.get('scope') != 'every_bottom_onscreen_text_over_moving_footage':
        raise PlanError('Caption treatment must be film-wide')
    if cap.get('background_panel') is not True or cap.get('bordered_ui_chrome') is not False or cap.get('border') is not False:
        raise PlanError('Caption treatment must be an unbordered background panel')
    if cap.get('inventory_is_splice_list') is not False:
        raise PlanError('Caption inventory is not a splice list')
    if cap.get('max_words') != 4 or cap.get('max_static_hold_s') != '4' or cap.get('one_label_at_a_time') is not True:
        raise PlanError('Caption plan must be four words, four seconds, one label at a time')
    if cap.get('side_label_inventory_proves_film_wide_coverage') is not False:
        raise PlanError('The side_label list does not by itself prove film-wide coverage')
    if cap.get('rendered') is not False:
        raise PlanError('Caption plan is not a render')
    by_ts = {row['timestamp']: row for row in rows}
    if set(by_ts) != {'00:20', '0:30', '0:51', '1:49', '2:20', '3:13', '3:31', '7:58'}:
        raise PlanError('Eight-row timestamps drifted')
    for row in rows:
        if not str(row.get('status', '')).startswith('UNRESOLVED'):
            raise PlanError('Notes stay unresolved')
    hair, salon = by_ts['0:51']['candidate_frames'], by_ts['1:49']['candidate_frames']
    if not (hair[1] < salon[0] or salon[1] < hair[0]):
        raise PlanError('0:51 overlaps the 1:49 hair source')
    if by_ts['0:51'].get('same_source_as_1_49') is not False:
        raise PlanError('0:51 stays off the 1:49 salon source until a watched confirmation')
    hair = by_ts['0:51']
    disp = hair.get('disposition') or {}
    if hair.get('splice') is not False or disp.get('night_street') != 'leave_untouched':
        raise PlanError('0:51 night street stays untouched and is not a splice')
    if disp.get('distinct_hot_night_rebuild') is not False:
        raise PlanError('0:51 is not a distinct hot-night rebuild')
    if disp.get('proposed_salon_retarget') != 'inference_pending_capable_in_context_confirmation':
        raise PlanError('Salon retarget stays an unconfirmed inference')
    if disp.get('native_perception') is not False or disp.get('evidence_level') != 'source_map_only':
        raise PlanError('0:51 evidence is the source map, not a watched picture')
    if disp.get('note_resolved') is not False or hair['verbatim_note'] != 'still have hair flying out the tube, this needs rebuilt':
        raise PlanError('Ben\'s 0:51 wording stays, and the note stays open')
    foil = by_ts['2:20']
    ev = foil['jar_flip_2_18']
    lo, hi = foil['candidate_frames']
    if not (lo <= ev['master_frame'] <= hi) or ev['inside_replace_3260_3343'] is not True or ev['inside_keep_3168_3259'] is not False:
        raise PlanError('2:18 must sit in the foil replace zone and outside the kept frames')
    spark = foil['foil_next_spark_2_20']
    if spark.get('distinct_from_jar_flip') is not True or spark.get('beyond_replacement_ending_139_625s') is not True:
        raise PlanError('2:20 foil check stays distinct and past the replacement end')
    if spark.get('inside_replace_3260_3343') is not False or not (spark['master_frame'] > hi):
        raise PlanError('140s foil frame lies outside the jar replacement')
    if spark.get('note_resolved') is not False:
        raise PlanError('2:20 foil note stays open')
    if by_ts['7:58']['clock_7_59']['inside_candidate_11358_11492'] is not True:
        raise PlanError('7:59 must stay inside the existing rods row')
    return manifest

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
                        'candidate_keyframe_envelope': [left, right-1],
                        'gop_closure_proven': False,
                        'dependency_validation': 'OUTSTANDING',
                        'preservation': 'Keep original PTS and durations. Unchanged decoded frames and audio stay identical. J2242 must prove both.',
                        'boundary_policy': BOUNDARY_POLICY,
                        'pts_reconciled': False})
    return patches

def splice_rows(rows):
    kept = []
    for row in rows:
        if row.get('splice') is False:
            continue
        if (row.get('disposition') or {}).get('night_street') == 'leave_untouched':
            continue
        kept.append(row)
    return kept

def verify_plan(master=DEFAULT_MASTER, retakes=None):
    manifest = load_manifest()
    retakes = retakes or {}
    for name, item in retakes.items():
        # Explicitly requested missing/short retakes never fall back to another plate.
        require_hash(item['path'], item['sha256'])
        retake = probe_video(item['path'])
        minimum = RETAKE_MIN_FRAMES.get(name)
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
    # Caption labels are a panel policy. They are not splice intervals.
    # 0:51 is evidence of where the clock lands. It is not a night-street splice.
    patches = build_plan(timeline, splice_rows(manifest['eight_rows']))
    notes = (EDIT_DIR.parent / '01_Script' / 'FACT_NOTES_v01.md').read_text()
    captions = plan_captions(timeline['frames'], timeline['time_base'], manifest['caption_treatment']['labels'], notes)
    cuts = json.loads((EDIT_DIR / '_desk/008/rough_v12/cuts_rough_v12.json').read_text())
    bottom = reconcile_bottom_text(cuts, manifest['caption_treatment']['labels'])
    bottom['planned_safe_path'] = plan_safe_path(timeline['frames'], timeline['time_base'])
    ai_spend = Path('/Users/benjaminoats/YouTube/orbit-with-ben/scripts/ai_spend.py')
    return {'status': 'PLANNED_NOT_EXECUTABLE', 'master': str(master), 'master_sha256': MASTER_SHA,
            'timeline': timeline, 'patches': patches, 'inputs': inputs,
            'caption_plan': captions, 'bottom_text': bottom,
            'spend_preflight': spend_preflight(ai_spend if ai_spend.is_file() else None),
            'frame_count_delta': 'UNMEASURED', 'vo_sync_lag_ms': 'UNMEASURED',
            'unchanged_frame_identity': 'UNMEASURED', 'audio_packet_identity_and_timestamps': 'UNMEASURED',
            'holds': manifest['holds'], 'spend_gbp': 0, 'media_rendered': False}

def extract_unchanged_range(*args, **kwargs):
    raise PlanError('Removed unsafe CFR/re-encode path. Future scoped packet/GOP splicer required.')

def execute_recipe(*args, **kwargs):
    raise PlanError('Execution refused until J1881 re-reviews the J2217 eight-item amend. No splice, replacement render, spend, upload, or YouTube change.')

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--execute', action='store_true')
    ap.add_argument('--master', type=Path, default=DEFAULT_MASTER)
    ap.add_argument('--report', type=Path)
    ap.add_argument('--retake-p2-02', type=Path)
    ap.add_argument('--retake-p3-01', type=Path)
    ap.add_argument('--retake-p5-13', type=Path)
    ap.add_argument('--retake-p2-02-sha256')
    ap.add_argument('--retake-p3-01-sha256')
    ap.add_argument('--retake-p5-13-sha256')
    args = ap.parse_args()
    if args.execute:
        ap.exit(2, 'Execution refused until J1881 re-reviews the J2217 eight-item amend.\n')
    if args.report and args.report.exists():
        ap.exit(2, 'Refusing to overwrite report.\n')
    retakes = {}
    for name in ('p2_02', 'p3_01', 'p5_13'):
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
    printed = {k: v for k, v in report.items() if k not in ('timeline', 'patches')}
    # The card list is the planned treatment. Frame schedules stay out of the summary.
    if 'caption_plan' in printed:
        printed['caption_plan'] = {
            'card_count': len(printed['caption_plan']['cards']),
            'rendered': False,
            'cards': [{k: c[k] for k in ('row', 'label', 'word_count', 'pts_in', 'pts_end', 'static_hold_s', 'window_remainder_ticks')}
                      for c in printed['caption_plan']['cards']],
        }
    print(json.dumps(printed, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
