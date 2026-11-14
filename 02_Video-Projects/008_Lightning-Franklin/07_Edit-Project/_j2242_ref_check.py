"""Which kept Franklin frames look at a picture this job replaces.

The four mixed groups still hold master frames. The source is H.264 High
with B-frames, so a kept packet can only stay exact when every picture it
uses is also an original packet. This reads the slice headers and builds
the reference lists. It does not mux a master and it does not encode the
kept frames.
"""
import argparse
import json
from pathlib import Path

import _build_rough_v13_recipe as recipe
import _j2242_mixed_split as split
import _j2242_packet_mux as mux

MAX_FRAME_NUM = 16
MAX_POC_LSB = 64
MAX_REF = 4
SLICE = {0: 'P', 1: 'B', 2: 'I', 5: 'P', 6: 'B', 7: 'I'}


class Bits:
    def __init__(self, data):
        self.data = data
        self.bit = 0
        self.n = len(data) * 8

    def one(self):
        if self.bit >= self.n:
            raise ValueError('Truncated H.264 header')
        value = (self.data[self.bit // 8] >> (7 - self.bit % 8)) & 1
        self.bit += 1
        return value

    def u(self, count):
        value = 0
        for _ in range(count):
            value = (value << 1) | self.one()
        return value

    def ue(self):
        zeros = 0
        while self.one() == 0:
            zeros += 1
            if zeros > 31:
                raise ValueError('Exp-Golomb value is too long')
        return ((1 << zeros) - 1) + (self.u(zeros) if zeros else 0)

    def se(self):
        value = self.ue()
        return (value + 1) // 2 if value % 2 else -(value // 2)


def nal_payloads(data, length_size=4):
    payloads = []
    offset = 0
    while offset < len(data):
        if len(data) - offset < length_size:
            raise ValueError('Truncated NAL length')
        size = int.from_bytes(data[offset:offset + length_size], 'big')
        offset += length_size
        if size < 1 or offset + size > len(data):
            raise ValueError('Invalid NAL payload length')
        payloads.append(data[offset:offset + size])
        offset += size
    return payloads


def _mod_commands(bits):
    commands = []
    while True:
        command = bits.ue()
        if command == 3:
            commands.append((3, None))
            return commands
        if command in (0, 1):
            commands.append((command, bits.ue()))
        elif command == 2:
            raise ValueError('Long-term reference reorder is not used')
        else:
            raise ValueError('Unknown reference-list command')
        if len(commands) > 16:
            raise ValueError('Reference-list command does not end')


def _skip_weights(bits, kind, num_l0, num_l1, chroma):
    bits.ue()
    if chroma:
        bits.ue()

    def one_list(count):
        for _ in range(count):
            if bits.u(1):
                bits.se()
                bits.se()
            if chroma and bits.u(1):
                for _plane in range(2):
                    bits.se()
                    bits.se()

    one_list(num_l0)
    if kind == 'B':
        one_list(num_l1)


def parse_slice(rbsp, pps):
    """Slice fields the reference list needs. Weights are skipped, not used."""
    if not rbsp:
        raise ValueError('Empty slice')
    nal_ref = (rbsp[0] >> 5) & 3
    nal_type = rbsp[0] & 31
    if nal_type not in (1, 5):
        raise ValueError('Not a coded slice')
    bits = Bits(rbsp[1:])
    bits.ue()
    kind = SLICE.get(bits.ue())
    if kind is None:
        raise ValueError('Unsupported slice type')
    if bits.ue() != pps['pps_id']:
        raise ValueError('Slice uses a different picture parameter set')
    frame_num = bits.u(4)
    if nal_type == 5:
        bits.ue()
    poc_lsb = bits.u(6)
    if kind == 'B':
        bits.u(1)
    num_l0 = pps['l0'] + 1
    num_l1 = pps['l1'] + 1
    if kind in ('P', 'B') and bits.u(1):
        num_l0 = bits.ue() + 1
        if kind == 'B':
            num_l1 = bits.ue() + 1
    mods_l0 = []
    mods_l1 = []
    if kind != 'I':
        if bits.u(1):
            mods_l0 = _mod_commands(bits)
        if kind == 'B' and bits.u(1):
            mods_l1 = _mod_commands(bits)
    if (pps['wpred'] and kind == 'P') or (pps['wbipred'] == 1 and kind == 'B'):
        _skip_weights(bits, kind, num_l0, num_l1, chroma=1)
    adaptive = 0
    long_term = 0
    mmco = []
    if nal_ref:
        if nal_type == 5:
            bits.u(1)
            long_term = bits.u(1)
        else:
            adaptive = bits.u(1)
            if adaptive:
                while True:
                    operation = bits.ue()
                    if operation == 0:
                        mmco.append((0,))
                        break
                    if operation == 1:
                        mmco.append((1, bits.ue()))
                    else:
                        raise ValueError(f'Unsupported reference-marking operation {operation}')
                    if len(mmco) > 8:
                        raise ValueError('Reference-marking commands do not end')
    if long_term:
        raise ValueError('Long-term IDR reference is not used')
    return {
        'nal_ref': nal_ref,
        'idr': nal_type == 5,
        'kind': kind,
        'frame_num': frame_num,
        'poc_lsb': poc_lsb,
        'l0': 0 if kind == 'I' else num_l0,
        'l1': num_l1 if kind == 'B' else 0,
        'mods_l0': mods_l0,
        'mods_l1': mods_l1,
        'adaptive': adaptive,
        'mmco': mmco,
    }


def assign_poc(pictures):
    """POC in decode order. An IDR starts a new count."""
    prev_msb = 0
    prev_lsb = 0
    half = MAX_POC_LSB // 2
    for pic in pictures:
        lsb = pic['poc_lsb']
        if pic['idr']:
            msb = 0
        elif lsb < prev_lsb and prev_lsb - lsb >= half:
            msb = prev_msb + MAX_POC_LSB
        elif lsb > prev_lsb and lsb - prev_lsb > half:
            msb = prev_msb - MAX_POC_LSB
        else:
            msb = prev_msb
        pic['poc'] = msb + lsb
        if pic['nal_ref']:
            prev_msb = 0 if pic['idr'] else msb
            prev_lsb = lsb
    return pictures


def _pic_num(ref, curr_frame_num):
    frame_num = ref['frame_num']
    if frame_num > curr_frame_num:
        frame_num -= MAX_FRAME_NUM
    return frame_num


def _default_lists(pic, dpb):
    if pic['kind'] == 'I':
        return [], []
    if pic['kind'] == 'P':
        ordered = sorted(dpb, key=lambda item: _pic_num(item, pic['frame_num']), reverse=True)
        return ordered, []
    past = [item for item in dpb if item['poc'] < pic['poc']]
    future = [item for item in dpb if item['poc'] > pic['poc']]
    past.sort(key=lambda item: item['poc'], reverse=True)
    future.sort(key=lambda item: item['poc'])
    return past + future, future + past


def _reorder(default, mods, pic, dpb):
    if not mods:
        return default
    output = list(default)
    pred = pic['frame_num']
    index = 0
    for command, argument in mods:
        if command == 3:
            break
        gap = argument + 1
        if command == 0:
            wrapped = pred - gap
            if wrapped < 0:
                wrapped += MAX_FRAME_NUM
        else:
            wrapped = pred + gap
            if wrapped >= MAX_FRAME_NUM:
                wrapped -= MAX_FRAME_NUM
        pred = wrapped
        target = wrapped - MAX_FRAME_NUM if wrapped > pic['frame_num'] else wrapped
        chosen = next(
            (item for item in dpb if _pic_num(item, pic['frame_num']) == target), None)
        if chosen is None:
            raise ValueError(f"Reordered reference {target} is not in the buffer")
        output = [item for item in output if item is not chosen]
        output.insert(index, chosen)
        index += 1
    return output


def _slide(dpb, pic):
    dpb.append(pic)
    while len(dpb) > MAX_REF:
        oldest = min(dpb, key=lambda item: _pic_num(item, pic['frame_num']))
        if oldest is pic and len(dpb) > 1:
            oldest = min(
                (item for item in dpb if item is not pic),
                key=lambda item: _pic_num(item, pic['frame_num']))
        dpb.remove(oldest)


def _mark(dpb, pic):
    """Apply decoded-reference marking, then keep this picture if it is a reference."""
    if not pic['nal_ref']:
        return
    if pic.get('mmco'):
        for command in pic['mmco']:
            if command[0] == 0:
                break
            target = pic['frame_num'] - (command[1] + 1)
            victim = next(
                (item for item in dpb if _pic_num(item, pic['frame_num']) == target), None)
            if victim is None:
                raise ValueError(
                    f'Frame {pic["index"]} drops missing reference {target}')
            dpb.remove(victim)
        dpb.append(pic)
        if len(dpb) > MAX_REF:
            raise ValueError(f'Frame {pic["index"]} leaves too many references')
        return
    _slide(dpb, pic)


def assign_refs(pictures):
    """Fill each picture's used reference indices. Decode order, one closed GOP."""
    if not pictures or not pictures[0]['idr']:
        raise ValueError('Reference walk must start on an IDR')
    dpb = []
    for pic in pictures:
        if pic['idr']:
            dpb = []
        list0, list1 = _default_lists(pic, dpb)
        if pic['mods_l0']:
            list0 = _reorder(list0, pic['mods_l0'], pic, dpb)
        if pic['mods_l1']:
            list1 = _reorder(list1, pic['mods_l1'], pic, dpb)
        used = []
        for item in list0[:pic['l0']] + list1[:pic['l1']]:
            if item['index'] not in used:
                used.append(item['index'])
        pic['refs'] = used
        _mark(dpb, pic)
    return pictures


def taint(pictures, changed):
    """A frame is exact only when its whole reference chain avoids changed frames."""
    by_index = {pic['index']: pic for pic in pictures}
    changed = set(changed)
    state = {}

    def walk(index, stack):
        if index in state:
            return state[index]
        if index in stack:
            raise ValueError('Reference list refers to itself')
        if index not in by_index:
            state[index] = True
            return True
        if index in changed:
            state[index] = True
            return True
        stack.add(index)
        hit = any(walk(ref, stack) for ref in by_index[index]['refs'])
        stack.remove(index)
        state[index] = hit
        return hit

    for pic in pictures:
        pic['tainted'] = walk(pic['index'], set())
    return pictures


def exact_runs(pictures, master_runs):
    """Inclusive master ranges whose packets do not need a replaced picture."""
    exact = {pic['index'] for pic in pictures if not pic['tainted']}
    runs = []
    for first, last in master_runs:
        cursor = None
        for index in range(first, last + 1):
            if index in exact:
                cursor = index if cursor is None else cursor
                end = index
            elif cursor is not None:
                runs.append((cursor, end))
                cursor = None
        if cursor is not None:
            runs.append((cursor, end))
    return runs


def blocked_runs(pictures, master_runs):
    blocked = {pic['index'] for pic in pictures if pic['tainted']}
    runs = []
    for first, last in master_runs:
        cursor = None
        for index in range(first, last + 1):
            if index in blocked:
                if cursor is None:
                    cursor = index
                end = index
            elif cursor is not None:
                runs.append((cursor, end))
                cursor = None
        if cursor is not None:
            runs.append((cursor, end))
    return runs


def opening_ok(pictures):
    """The first GOP's first three pictures are the x264 pattern this parser claims."""
    by_index = {pic['index']: pic for pic in pictures}
    needed = (0, 1, 2)
    if any(index not in by_index for index in needed):
        return False
    return (
        by_index[0]['kind'] == 'I' and by_index[0]['idr']
        and by_index[2]['refs'] == [0]
        and by_index[1]['refs'] == [0, 2]
        and [pic['poc'] for pic in pictures[:6]] == [0, 4, 2, 8, 6, 12]
    )


def _assert_closed(pictures, first, last):
    order = sorted(pictures, key=lambda pic: pic['poc'])
    if [pic['index'] for pic in order] != list(range(first, last + 1)):
        raise ValueError(f'POC order does not match display order in {first}-{last}')
    last_ref = None
    ref_pics = [pic for pic in pictures if pic['nal_ref']]
    for pic in pictures:
        for ref in pic['refs']:
            if ref < first or ref > last:
                raise ValueError(f'Frame {pic["index"]} references {ref} outside its IDR group')
            if ref == pic['index']:
                raise ValueError(f'Frame {pic["index"]} references itself')
        if pic['kind'] == 'P' and pic['l0'] == 1 and not pic['mods_l0']:
            if pic['refs'] != [last_ref]:
                raise ValueError(
                    f'P frame {pic["index"]} references {pic["refs"]}, not {last_ref}')
        if pic['kind'] == 'B' and pic['l0'] == 1 and pic['l1'] == 1 and not pic['mods_l0'] and not pic['mods_l1']:
            past = [item for item in ref_pics if item['poc'] < pic['poc'] and item is not pic]
            future = [item for item in ref_pics if item['poc'] > pic['poc'] and item is not pic]
            expect = []
            if past:
                expect.append(max(past, key=lambda item: item['poc'])['index'])
            if future:
                expect.append(min(future, key=lambda item: item['poc'])['index'])
            if pic['refs'] != expect:
                raise ValueError(
                    f'B frame {pic["index"]} references {pic["refs"]}, not {expect}')
        if pic['nal_ref']:
            last_ref = pic['index']


def load_packets(master, packets, timeline):
    by_pts = {frame['pts']: frame for frame in timeline['frames']}
    video = {}
    for packet in packets:
        if packet['stream_index'] != 0:
            continue
        frame = by_pts[int(packet['pts'])]
        video[frame['index']] = packet
    if len(video) != recipe.EXPECTED_FRAMES:
        raise ValueError('Video packet map is short')
    return video


def read_group(master_bytes, packets, first, last, pps):
    selected = []
    for index in range(first, last + 1):
        packet = packets[index]
        payload = master_bytes[int(packet['pos']):int(packet['pos']) + int(packet['size'])]
        if 'SHA256:' not in packet.get('data_hash', ''):
            raise ValueError('Packet hash is missing')
        vcl = next(item for item in nal_payloads(payload) if (item[0] & 31) in (1, 5))
        row = parse_slice(vcl, pps)
        row.update({
            'index': index,
            'dts': int(packet['dts']),
            'pts': int(packet['pts']),
        })
        selected.append(row)
    selected.sort(key=lambda item: item['dts'])
    if not selected[0]['idr'] or selected[0]['index'] != first:
        raise ValueError(f'Group {first} does not decode from its IDR')
    assign_poc(selected)
    assign_refs(selected)
    _assert_closed(selected, first, last)
    return selected


def classify_group(pictures, master_runs, changed_runs):
    changed = []
    for first, last in changed_runs:
        changed.extend(range(first, last + 1))
    taint(pictures, changed)
    master_frames = []
    for first, last in master_runs:
        for pic in pictures:
            if first <= pic['index'] <= last:
                master_frames.append({
                    'index': pic['index'],
                    'kind': pic['kind'],
                    'refs': pic['refs'],
                    'exact': not pic['tainted'],
                })
    return {
        'exact_runs': exact_runs(pictures, master_runs),
        'blocked_runs': blocked_runs(pictures, master_runs),
        'master_frames': master_frames,
        'reordered': sum(bool(pic['mods_l0'] or pic['mods_l1']) for pic in pictures),
    }


def group_report(master_bytes, packets, groups, pps):
    rows = []
    for group in groups:
        first, last = group['first'], group['last']
        changed, master = split.partition(group)
        pictures = read_group(master_bytes, packets, first, last, pps)
        result = classify_group(
            pictures,
            [(item['first'], item['last']) for item in master],
            [(item['first'], item['last']) for item in changed])
        rows.append({
            'first': first,
            'last': last,
            'frames': last - first + 1,
            'exact_runs': result['exact_runs'],
            'blocked_runs': result['blocked_runs'],
            'blocked_frames': [
                frame for frame in result['master_frames'] if not frame['exact']],
            'exact_frames': sum(frame['exact'] for frame in result['master_frames']),
            'reordered_slices': result['reordered'],
        })
    return rows


PPS = {'pps_id': 0, 'l0': 0, 'l1': 0, 'wpred': 1, 'wbipred': 2}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--master', type=Path, default=recipe.DEFAULT_MASTER)
    parser.add_argument('--review-dir', type=Path, default=mux.REVIEW)
    parser.add_argument('--packets', type=Path, default=Path(
        '/Users/benjaminoats/_desk/state/J2242/source-preflight-v01/source_packets.json'))
    parser.add_argument('--timeline', type=Path, default=Path(
        '/Users/benjaminoats/_desk/state/J2242/source-preflight-v01/source_timeline.json'))
    args = parser.parse_args()
    recipe.require_hash(args.master, recipe.MASTER_SHA, recipe.MASTER_BYTES)
    groups = split.load_groups(args.review_dir)
    packet_json = json.loads(args.packets.read_text())
    timeline = json.loads(args.timeline.read_text())
    video = load_packets(args.master, packet_json['packets'], timeline)
    master_bytes = args.master.read_bytes()
    if len(master_bytes) != recipe.MASTER_BYTES:
        raise ValueError('Master size changed while reading')
    opening = read_group(master_bytes, video, 0, 141, PPS)
    if not opening_ok(opening):
        raise ValueError('Opening GOP does not match the x264 reference pattern')
    rows = group_report(master_bytes, video, groups, PPS)
    blocked = [run for row in rows for run in row['blocked_runs']]
    exact = [run for row in rows for run in row['exact_runs']]
    recipe.write_new(args.review_dir / 'REF_CHECK.json', {
        'job': 'J2242',
        'status': 'REFERENCE_CHECK',
        'source': 'slice headers of hos_008_master_v03.mp4',
        'opening_pattern_ok': True,
        'groups': rows,
        'exact_runs': exact,
        'blocked_runs': blocked,
        'encoded_master_frames': False,
        'audio': False,
        'output_film_created': False,
        'finished_master': False,
        'approval': False,
        'spend_gbp': 0,
        'note': (
            'A kept frame is exact only when every picture it references is '
            'also kept. Blocked frames look into a replaced picture, so their '
            'original packets cannot be copied beside the new High encode.'
        ),
    })
    print(json.dumps({
        'exact_runs': exact,
        'blocked_runs': blocked,
        'finished_master': False,
    }, indent=2))


if __name__ == '__main__':
    main()
