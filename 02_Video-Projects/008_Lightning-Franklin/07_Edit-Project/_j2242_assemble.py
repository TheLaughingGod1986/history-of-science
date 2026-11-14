"""Mux the Franklin assembly order onto the source clock. Does not name a master.

Packet-copy runs keep the original packet bytes and timestamps. Each rebuild
cluster that sits between those packets in decode order is written in display
order, so a High encode stays one closed run. Each decode time is the previous
one plus that frame's duration, which is how the source clock is stored.
Audio packets are
copied with their original timestamps. Nothing here is hos_008_master_v04.mp4.
"""
import argparse
import json
from fractions import Fraction
from pathlib import Path

import _build_rough_v13_recipe as recipe
import _j2242_mux_map as plan
import _j2242_packet_mux as mux
from _j2242_source_preflight import nal_types

MASTER_NAME = plan.MASTER_NAME
TIMELINE = Path('/Users/benjaminoats/_desk/state/J2242/source-preflight-v01/source_timeline.json')


def refuse_output(path):
    path = Path(path)
    if path.name == MASTER_NAME or 'master_v04' in path.name:
        raise ValueError('This assembly cannot be written as the v04 master')
    return path


def schedule(demux, frames, source_dts, is_anchor):
    """Return one event per frame in mux order.

    An anchor keeps its source decode time. Rebuild frames between anchors are
    emitted in display order. Their decode times are prev+1, prev+2, ... and
    must stay below the next anchor and at or before each frame's own PTS.
    """
    if len(demux) != len(frames) or len(source_dts) != len(frames):
        raise ValueError('Schedule inputs are different lengths')
    if len(set(demux)) != len(demux):
        raise ValueError('Demux order repeats a frame')
    order = []
    cursor = 0
    while cursor < len(demux):
        index = demux[cursor]
        if is_anchor(index):
            order.append(index)
            cursor += 1
            continue
        end = cursor
        while end < len(demux) and not is_anchor(demux[end]):
            end += 1
        order.extend(sorted(demux[cursor:end]))
        cursor = end
    if len(order) != len(frames) or set(order) != set(range(len(frames))):
        raise ValueError('Schedule dropped or repeated a frame')
    # The muxer stores duration as the gap to the next decode time. Copied
    # packets keep their original decode times, so the gaps have to be the
    # source durations, including across a rebuilt run.
    dts = int(source_dts[order[0]])
    events = []
    for place, index in enumerate(order):
        frame = frames[index]
        pts = int(frame['pts'])
        duration = int(frame['duration'])
        anchor = bool(is_anchor(index))
        if duration <= 0 or dts > pts:
            raise ValueError(f'Frame {index} has no legal decode time')
        if anchor and dts != int(source_dts[index]):
            raise ValueError(f'Copied frame {index} cannot keep its decode time')
        events.append({
            'index': index,
            'pts': pts,
            'dts': dts,
            'duration': duration,
            'anchor': anchor,
        })
        if place + 1 < len(order):
            nxt = dts + duration
            if nxt <= dts:
                raise ValueError('Decode time does not advance')
            dts = nxt
    return events


def annexb_nals(data):
    """Split an annex B byte string into NAL payloads, without start codes."""
    positions = []
    cursor = 0
    while True:
        found = data.find(b'\x00\x00\x01', cursor)
        if found < 0:
            break
        start = found - 1 if found > 0 and data[found - 1] == 0 else found
        positions.append(start)
        cursor = found + 3
    if not positions:
        raise ValueError('Exact picture has no annex B start codes')
    nals = []
    for start, nxt in zip(positions, positions[1:] + [len(data)]):
        if data[start:start + 4] == b'\x00\x00\x00\x01':
            payload = data[start + 4:nxt]
        elif data[start:start + 3] == b'\x00\x00\x01':
            payload = data[start + 3:nxt]
        else:
            raise ValueError('Exact picture has a broken start code')
        if not payload:
            raise ValueError('Exact picture has an empty NAL')
        nals.append(payload)
    return nals


def access_units(data):
    """Group NALs into access units. Each exact frame starts with its own SPS."""
    units = []
    current = []
    for nal in annexb_nals(data):
        if (nal[0] & 31) == 7 and current:
            units.append(current)
            current = []
        current.append(nal)
    if current:
        units.append(current)
    if not units:
        raise ValueError('Exact picture has no access units')
    return units


def to_avcc(nals):
    return b''.join(len(nal).to_bytes(4, 'big') + nal for nal in nals)


def idr_headers(payload):
    types = set(nal_types(payload, 4))
    if not {7, 8, 5} <= types:
        raise ValueError('Boundary packet is missing in-band SPS, PPS or IDR')
    return types


def high_runs_contiguous(events, runs):
    position = {row['index']: place for place, row in enumerate(events)}
    for run in runs:
        if run['role'] == 'packet_copy':
            continue
        places = [position[frame] for frame in range(run['first'], run['last'] + 1)]
        if places != list(range(places[0], places[0] + len(places))):
            raise ValueError(f"Replacement {run['first']}-{run['last']} is not one run")
        if [events[place]['index'] for place in places] != list(range(run['first'], run['last'] + 1)):
            raise ValueError(f"Replacement {run['first']}-{run['last']} is out of display order")


def clock_ok(events, frames):
    if [(row['pts'], row['duration']) for row in sorted(events, key=lambda item: item['index'])] != [
            (int(frame['pts']), int(frame['duration'])) for frame in frames]:
        raise ValueError('Assembly clock changed a source timestamp')
    counts = {}
    for row in events:
        counts[row['duration']] = counts.get(row['duration'], 0) + 1
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', action='store_true')
    parser.add_argument('--master', type=Path, default=recipe.DEFAULT_MASTER)
    parser.add_argument('--timeline', type=Path, default=TIMELINE)
    parser.add_argument('--review-dir', type=Path, default=mux.REVIEW)
    parser.add_argument('--out-dir', type=Path, required=True)
    args = parser.parse_args()
    if not args.plan:
        parser.error('--plan is required; this tool does not run from an import')
    out_dir = refuse_output(args.out_dir)
    candidate = refuse_output(out_dir / 'franklin_assembly.mp4')
    if candidate.resolve() == Path(args.master).resolve():
        raise ValueError('Refusing to write over the source master')
    recipe.require_hash(args.master, recipe.MASTER_SHA, recipe.MASTER_BYTES)
    timeline = json.loads(args.timeline.read_text())
    if timeline.get('time_base') != '1/12288' or len(timeline['frames']) != mux.FRAME_COUNT:
        raise ValueError('Source clock is not the 12923-frame 1/12288 master')
    report = plan.build_map(args.review_dir, timeline['frames'], check_media=True)
    if report['audio'] != 'OUTSTANDING' or report['finished_master']:
        raise ValueError('Assembly map is not an unfinished zero-audio order')
    import av
    frames = timeline['frames']
    by_pts = {int(frame['pts']): frame['index'] for frame in frames}
    role = {}
    for run in report['order']:
        for index in range(run['first'], run['last'] + 1):
            role[index] = run['role']
    with av.open(str(args.master)) as source:
        video = source.streams.video[0]
        audio = source.streams.audio[0]
        if video.time_base != Fraction(1, 12288):
            raise ValueError('Source video is not on the 1/12288 clock')
        video_packets = {}
        audio_packets = []
        demux = []
        source_dts = [None] * mux.FRAME_COUNT
        for packet in source.demux(video, audio):
            if not packet.size:
                continue
            if packet.stream.index == audio.index:
                audio_packets.append(packet)
                continue
            index = by_pts.get(int(packet.pts))
            if index is None or index in video_packets or source_dts[index] is not None:
                raise ValueError('Source video packet does not map onto one frame')
            source_dts[index] = int(packet.dts)
            if int(packet.pts) != int(frames[index]['pts']) or int(packet.duration) != int(frames[index]['duration']):
                raise ValueError(f'Frame {index} packet clock differs from the timeline')
            if role[index] == 'packet_copy':
                video_packets[index] = packet
            demux.append(index)
    if len(demux) != mux.FRAME_COUNT or len(audio_packets) != 25296:
        raise ValueError('Source packet counts are not the pinned master')
    if any(item is None for item in source_dts):
        raise ValueError('A source frame has no decode time')
    events = schedule(demux, frames, source_dts, lambda index: role[index] == 'packet_copy')
    high_runs_contiguous(events, report['order'])
    counts = clock_ok(events, frames)
    if counts.get(1024) != 23:
        raise ValueError('Assembly clock lost a 1024-tick step')
    for event in events:
        if event['anchor'] and event['dts'] != source_dts[event['index']]:
            raise ValueError(f"Copied frame {event['index']} changed its decode time")
    for run in report['order']:
        if run['role'] == 'packet_copy' and not video_packets[run['first']].is_keyframe:
            raise ValueError(f"Packet copy {run['first']} does not start on an IDR")
    envelopes = encoded_envelopes(report['order'], mux.build_report(args.review_dir)['envelopes'])
    print('schedule ok; hashing replacement pictures', flush=True)
    specs = _replacement_specs(report, args.review_dir)
    print(f'hashed {len(specs)} replacement runs; muxing', flush=True)
    out_dir.mkdir(parents=True, exist_ok=False)
    written = _mux(args.master, candidate, events, video_packets, audio_packets, specs, role)
    recipe.require_hash(args.master, recipe.MASTER_SHA, recipe.MASTER_BYTES)
    result = {
        'job': 'J2242',
        'status': 'UNVERIFIED_ASSEMBLY',
        'candidate': str(candidate),
        'candidate_sha256': recipe.sha256_file(candidate),
        'candidate_bytes': candidate.stat().st_size,
        'frames': written['frames'],
        'packet_copy_frames': report['packet_copy_frames'],
        'high_encode_frames': report['high_encode_frames'],
        'exact_pcm_frames': report['exact_pcm_frames'],
        'copied_audio_packets': written['audio'],
        'duration_ticks': {str(key): counts[key] for key in sorted(counts)},
        'ticks_1024': counts[1024],
        'timestamp_policy': 'copy original PTS and duration; decode time advances by that duration',
        'audio': 'COPIED_UNMEASURED',
        'output_preservation': 'OUTSTANDING',
        'loudness': 'UNMEASURED',
        'vo_sync': 'UNMEASURED',
        'output_film_created': True,
        'finished_master': False,
        'approval': False,
        'spend_gbp': 0,
        'source_master_sha256': recipe.MASTER_SHA,
    }
    recipe.write_new(out_dir / 'ASSEMBLE.json', result)
    recipe.write_new(out_dir / 'contract.json', {
        'modified_frames': _ranges(report['order'], 'high_encode'),
        'encoded_envelopes': envelopes,
    })
    print(json.dumps({
        'status': result['status'],
        'frames': result['frames'],
        'audio': result['copied_audio_packets'],
        'ticks_1024': result['ticks_1024'],
        'finished_master': False,
    }, indent=2))


def _ranges(order, role):
    return [[run['first'], run['last']] for run in order if run['role'] == role]


def encoded_envelopes(order, envelopes):
    """Keep the closed IDR groups. Every rebuilt frame has to sit inside one."""
    pairs = []
    covered = set()
    previous = -1
    for env in envelopes:
        first, last = int(env['first']), int(env['last'])
        if first <= previous or first > last:
            raise ValueError('IDR envelopes are overlapping or backwards')
        pairs.append([first, last])
        covered.update(range(first, last + 1))
        previous = last
    for run in order:
        if run['role'] == 'packet_copy':
            continue
        for frame in range(run['first'], run['last'] + 1):
            if frame not in covered:
                raise ValueError(f'Frame {frame} is rebuilt outside an IDR envelope')
    return pairs


def _replacement_specs(report, review_dir):
    """Hash the pieces and remember where they are. The bytes stay on disk."""
    encodes, exact_runs, _jar = plan.load_pieces(review_dir)
    specs = {}
    for run in report['order']:
        if run['role'] == 'packet_copy':
            continue
        key = (run['first'], run['last'])
        if run['role'] == 'high_encode':
            record = encodes[tuple(run['clip'])]
            path = Path(record['encoded'])
            recipe.require_hash(path, record['encoded_sha256'], int(record['encoded_bytes']))
            kind = 'high_encode'
        else:
            record = exact_runs[tuple(run['clip'])]
            path = Path(record['path'])
            recipe.require_hash(path, record['sha256'], int(record['bytes']))
            kind = 'exact_pcm'
        specs[key] = {'kind': kind, 'path': path, 'frames': run['frames']}
    return specs


def _load_spec(spec):
    if spec['kind'] == 'high_encode':
        packets = _mp4_packets(spec['path'], spec['frames'])
        idr_headers(packets[0])
        return packets
    packets = [to_avcc(unit) for unit in access_units(spec['path'].read_bytes())]
    if len(packets) != spec['frames']:
        raise ValueError(f"{spec['path'].name} has {len(packets)} pictures, not {spec['frames']}")
    for packet in packets:
        idr_headers(packet)
    return packets


def _mp4_packets(path, count):
    import av
    with av.open(str(path)) as container:
        stream = container.streams.video[0]
        if stream.codec_context.profile != 'High':
            raise ValueError(f'{path.name} is not High profile')
        rows = [(bytes(packet), bool(packet.is_keyframe))
                for packet in container.demux(stream) if packet.size]
    if len(rows) != count or not rows[0][1] or any(flag for _payload, flag in rows[1:]):
        raise ValueError(f'{path.name} is not one IDR followed by {count - 1} other pictures')
    return [payload for payload, _flag in rows]


def _video_batch(cluster, video_packets, specs, role):
    import av
    if cluster[0]['anchor']:
        if len(cluster) != 1:
            raise ValueError('Copied frames must be muxed one at a time')
        event = cluster[0]
        packet = video_packets.pop(event['index'])
        if int(packet.pts) != event['pts'] or int(packet.dts) != event['dts']:
            raise ValueError(f"Anchor {event['index']} timestamps drifted")
        return [packet]
    owners = {}
    for key in specs:
        for index in range(key[0], key[1] + 1):
            owners[index] = key
    loaded = {}
    cursors = {}
    packets = []
    for event in cluster:
        key = owners[event['index']]
        if key not in loaded:
            loaded[key] = _load_spec(specs[key])
            cursors[key] = 0
        payload = loaded[key][cursors[key]]
        cursors[key] += 1
        packet = av.Packet(payload)
        packet.pts = event['pts']
        packet.dts = event['dts']
        packet.duration = event['duration']
        packet.time_base = Fraction(1, 12288)
        packet.is_keyframe = role[event['index']] == 'exact_pcm' or cursors[key] == 1
        packets.append(packet)
    for key, rows in loaded.items():
        if cursors[key] != len(rows):
            raise ValueError(f'Replacement {key} was only partly used')
    return packets


def _mux(master, candidate, events, video_packets, audio_packets, specs, role):
    import av
    with av.open(str(master)) as source, av.open(
            str(candidate), 'w', options={'avoid_negative_ts': 'disabled',
                                          'video_track_timescale': '12288'}) as out:
        ov = out.add_stream_from_template(source.streams.video[0])
        oa = out.add_stream_from_template(source.streams.audio[0])
        audio_at = 0
        frames = 0
        last_video = None
        last_audio = None
        cursor = 0
        while cursor < len(events):
            if events[cursor]['anchor']:
                batch = _video_batch(events[cursor:cursor + 1], video_packets, specs, role)
                cursor += 1
            else:
                end = cursor
                while end < len(events) and not events[end]['anchor']:
                    end += 1
                batch = _video_batch(events[cursor:end], video_packets, specs, role)
                cursor = end
            limit = int(batch[-1].dts)
            ready = [(int(packet.dts), 1, packet) for packet in batch]
            while audio_at < len(audio_packets) and int(audio_packets[audio_at].dts) <= limit:
                ready.append((int(audio_packets[audio_at].dts), 0, audio_packets[audio_at]))
                audio_at += 1
            for _dts, kind, packet in sorted(ready, key=lambda item: (item[0], item[1])):
                if kind == 1:
                    if last_video is not None and int(packet.dts) <= last_video:
                        raise ValueError('Video decode times went backwards while muxing')
                    last_video = int(packet.dts)
                    packet.stream = ov
                    frames += 1
                else:
                    if last_audio is not None and int(packet.dts) <= last_audio:
                        raise ValueError('Audio decode times went backwards while muxing')
                    last_audio = int(packet.dts)
                    packet.stream = oa
                out.mux(packet)
            del batch, ready
        while audio_at < len(audio_packets):
            packet = audio_packets[audio_at]
            audio_at += 1
            if last_audio is not None and int(packet.dts) <= last_audio:
                raise ValueError('Audio decode times went backwards while muxing')
            last_audio = int(packet.dts)
            packet.stream = oa
            out.mux(packet)
    if frames != len(events) or audio_at != len(audio_packets):
        raise ValueError('Mux did not write every frame and audio packet')
    return {'frames': frames, 'audio': audio_at}


if __name__ == '__main__':
    main()
