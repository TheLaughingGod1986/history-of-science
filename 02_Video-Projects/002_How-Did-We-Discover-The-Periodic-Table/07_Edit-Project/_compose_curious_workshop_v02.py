#!/usr/bin/env python3
"""Curious workshop underscore v02 — denser continuous pad under VO.

v01 was too sparse/quiet to hear on phone. v02: continuous warm strings +
soft pad + flute + harp in G major (wonder, not Germs death-ward).
"""
from __future__ import annotations

import struct
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "05_Music/hos_002_part01_curious_workshop_v02.mid"
PPQ = 480
BPM = 70


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
    # ch0 flute · ch1 strings ensemble · ch2 harp · ch3 warm pad
    evs: list[tuple[int, bytes]] = [
        (0, bytes([0xFF, 0x51, 0x03]) + struct.pack(">I", 60000000 // BPM)[1:]),
        (0, prog(0, 73)),   # flute
        (0, prog(1, 48)),   # strings
        (0, prog(2, 46)),   # harp
        (0, prog(3, 89)),   # warm pad (New Age)
    ]
    # G – Em – C – D
    roots = [
        (55, 59, 62),
        (52, 55, 59),
        (48, 52, 55),
        (50, 54, 57),
    ]
    flute_lines = [
        [67, 69, 71, 72, 71, 69, 67, 64],
        [64, 67, 69, 71, 69, 67, 64, 62],
        [72, 71, 69, 67, 64, 62, 60, 59],
        [62, 64, 66, 67, 69, 67, 66, 64],
    ]
    t = 0.0
    cycle = 0
    # ~100s wall clock at 70 BPM
    while t < 118:
        chord = roots[cycle % 4]
        hold = 8.0
        start = beats(t)
        end = beats(t + hold)
        # Continuous pad + strings (no mid-bar dropouts)
        for n in chord:
            evs.append((start, note_on(3, n, 52)))
            evs.append((end, note_off(3, n)))
            evs.append((start, note_on(3, n + 12, 36)))
            evs.append((end, note_off(3, n + 12)))
            evs.append((start, note_on(1, n - 12, 50)))
            evs.append((end, note_off(1, n - 12)))
            evs.append((start, note_on(1, n, 44)))
            evs.append((end, note_off(1, n)))
        # Soft flute line
        line = flute_lines[cycle % 4]
        for i, n in enumerate(line):
            s = beats(t + i)
            e = beats(t + i + 0.92)
            evs.append((s, note_on(0, n, 52)))
            evs.append((e, note_off(0, n)))
        # Steady harp arpeggio (8ths so the bed never goes hollow)
        arp = [chord[0], chord[1], chord[2], chord[1] + 12,
               chord[0] + 12, chord[2], chord[1], chord[0]]
        for i, n in enumerate(arp):
            s = beats(t + i)
            e = beats(t + i + 0.95)
            evs.append((s, note_on(2, n, 46)))
            evs.append((e, note_off(2, n)))
        bass = chord[0] - 12
        evs.append((start, note_on(2, bass, 42)))
        evs.append((end, note_off(2, bass)))
        t += hold
        cycle += 1

    s = beats(118)
    e = beats(124)
    for n, v in ((55, 40), (59, 36), (62, 34), (67, 40)):
        evs.append((s, note_on(3, n, v)))
        evs.append((e, note_off(3, n)))
    evs.append((s, note_on(0, 67, 40)))
    evs.append((e, note_off(0, 67)))
    for ch in (0, 1, 2, 3):
        evs.append((e + 10, bytes([0xB0 | ch, 123, 0])))
    hdr = b"MThd" + struct.pack(">IHHH", 6, 0, 1, PPQ)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(hdr + track(evs))
    print(f"WROTE {OUT} events={len(evs)}")


if __name__ == "__main__":
    main()
