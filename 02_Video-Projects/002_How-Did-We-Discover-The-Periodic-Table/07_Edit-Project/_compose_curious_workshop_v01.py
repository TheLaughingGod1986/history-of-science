#!/usr/bin/env python3
"""Curious workshop underscore for HOS 002 Part 01 — wonder, not death-ward.

G major · flute + strings + harp. Matches zoo-of-stuff chemistry, sits under VO.
"""
from __future__ import annotations

import struct
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "05_Music/hos_002_part01_curious_workshop_v01.mid"
PPQ = 480
BPM = 72


def vlq(n: int) -> bytes:
    buf = [n & 0x7F]
    n >>= 7
    while n:
        buf.append((n & 0x7F) | 0x80)
        n >>= 7
    return bytes(reversed(buf))


def ev(dt: int, payload: bytes) -> bytes:
    return vlq(dt) + payload


def note_on(ch: int, n: int, v: int) -> bytes:
    return bytes([0x90 | ch, n, v])


def note_off(ch: int, n: int) -> bytes:
    return bytes([0x80 | ch, n, 0])


def prog(ch: int, p: int) -> bytes:
    return bytes([0xC0 | ch, p])


def beats(b: float) -> int:
    return int(b * PPQ)


def track(events: list[tuple[int, bytes]]) -> bytes:
    events = sorted(events, key=lambda x: (x[0], x[1][0] if x[1] else 0))
    body = b""
    last = 0
    for t, payload in events:
        body += ev(t - last, payload)
        last = t
    body += ev(0, bytes([0xFF, 0x2F, 0x00]))
    return b"MTrk" + struct.pack(">I", len(body)) + body


def main() -> None:
    # ch0 flute melody · ch1 warm strings · ch2 harp arpeggios
    evs: list[tuple[int, bytes]] = [
        (0, bytes([0xFF, 0x51, 0x03]) + struct.pack(">I", 60000000 // BPM)[1:]),
        (0, prog(0, 73)),  # flute
        (0, prog(1, 48)),  # strings
        (0, prog(2, 46)),  # harp
    ]
    # G – Em – C – D  (wonder / curiosity, not ominous i–VI)
    roots = [
        (55, 59, 62),  # G
        (52, 55, 59),  # Em
        (48, 52, 55),  # C
        (50, 54, 57),  # D
    ]
    flute_lines = [
        [67, 69, 71, 72, 71, 69, 67, 64],
        [64, 67, 69, 71, 69, 67, 64, 62],
        [72, 71, 69, 67, 64, 62, 60, 59],
        [62, 64, 66, 67, 69, 67, 66, 64],
    ]
    t = 0.0
    cycle = 0
    # 72 BPM: 120 beats ≈ 100s wall-clock so the bed covers 85.68s VO + pad
    while t < 120:
        chord = roots[cycle % 4]
        hold = 8.0
        for strike, vel in ((0.0, 42), (4.0, 38)):
            start = beats(t + strike)
            end = beats(min(t + hold, 92))
            for n in chord:
                evs.append((start, note_on(1, n - 12, vel)))
                evs.append((end, note_off(1, n - 12)))
                evs.append((start, note_on(1, n, vel - 6)))
                evs.append((end, note_off(1, n)))
        line = flute_lines[cycle % 4]
        for i, n in enumerate(line):
            s = beats(t + i)
            e = beats(t + i + 0.88)
            evs.append((s, note_on(0, n, 58)))
            evs.append((e, note_off(0, n)))
        bass = chord[0] - 12
        arp = [chord[0], chord[1], chord[2], chord[1] + 12]
        for i, n in enumerate(arp * 2):
            s = beats(t + i)
            e = beats(t + i + 0.9)
            evs.append((s, note_on(2, n, 40)))
            evs.append((e, note_off(2, n)))
        evs.append((beats(t), note_on(2, bass, 36)))
        evs.append((beats(t + hold), note_off(2, bass)))
        t += hold
        cycle += 1

    s = beats(120)
    e = beats(126)
    evs += [
        (s, note_on(0, 67, 46)),
        (e, note_off(0, 67)),
        (s, note_on(1, 43, 34)),
        (s, note_on(1, 55, 32)),
        (e, note_off(1, 43)),
        (e, note_off(1, 55)),
        (s, note_on(2, 55, 30)),
        (e, note_off(2, 55)),
    ]
    # All notes off so fluidsynth does not hold hanging voices past EOF.
    for ch in (0, 1, 2):
        evs.append((e + 10, bytes([0xB0 | ch, 123, 0])))
    hdr = b"MThd" + struct.pack(">IHHH", 6, 0, 1, PPQ)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(hdr + track(evs))
    print(f"WROTE {OUT} events={len(evs)}")


if __name__ == "__main__":
    main()
