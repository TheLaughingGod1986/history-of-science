#!/usr/bin/env python3
"""Original ~80s ominous D-minor ward cue. Not a pad. Not a rip."""
from __future__ import annotations

import struct
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "05_Music/hos_001_part01_ominous_ward_v12.mid"
PPQ = 480
BPM = 60  # 1 beat = 1s — easy to score 80s


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


def track(events: list[tuple[int, bytes]]) -> bytes:
    events = sorted(events, key=lambda x: (x[0], x[1][0] if x[1] else 0))
    body = b""
    last = 0
    for t, payload in events:
        body += ev(t - last, payload)
        last = t
    body += ev(0, bytes([0xFF, 0x2F, 0x00]))
    return b"MTrk" + struct.pack(">I", len(body)) + body


def beats(b: float) -> int:
    return int(b * PPQ)


def main() -> None:
    # ch0 cello melody, ch1 string choir, ch2 dark piano
    evs: list[tuple[int, bytes]] = [
        (0, bytes([0xFF, 0x51, 0x03]) + struct.pack(">I", 60000000 // BPM)[1:]),
        (0, prog(0, 42)),   # cello
        (0, prog(1, 48)),   # string ensemble
        (0, prog(2, 0)),    # piano
    ]

    # Harmony: i–VI–iii–V  (Dm Bb F A) 2 bars each, four cycles ~ 64s, then hold
    roots = [
        (50, 53, 57),  # Dm
        (46, 50, 53),  # Bb
        (53, 57, 60),  # F
        (45, 49, 52),  # A (major V — death-ward tension)
    ]
    t = 0.0
    cycle = 0
    while t < 76:
        chord = roots[cycle % 4]
        hold = 8.0  # 2 bars
        # strings: two whole-note swells via re-strike at mid
        for strike, vel in ((0.0, 48), (4.0, 44)):
            start = beats(t + strike)
            end = beats(min(t + hold, 80))
            for n in chord:
                evs.append((start, note_on(1, n - 12, vel)))
                evs.append((end, note_off(1, n - 12)))
                evs.append((start, note_on(1, n, vel - 8)))
                evs.append((end, note_off(1, n)))
        # cello melody — stepwise, not a drone
        if cycle % 4 == 0:
            line = [50, 53, 52, 50, 57, 55, 53, 52]
        elif cycle % 4 == 1:
            line = [53, 55, 57, 58, 57, 55, 53, 50]
        elif cycle % 4 == 2:
            line = [57, 60, 58, 57, 55, 53, 52, 50]
        else:
            line = [57, 55, 53, 52, 50, 49, 50, 52]
        for i, n in enumerate(line):
            s = beats(t + i)
            e = beats(t + i + 0.92)
            evs.append((s, note_on(0, n, 62)))
            evs.append((e, note_off(0, n)))
        # dark piano: low fifth + falling answer
        bass = chord[0] - 12
        for off, n, v, dur in (
            (0.0, bass, 54, 1.8),
            (0.0, bass + 7, 40, 1.8),
            (2.0, bass, 50, 1.6),
            (3.0, chord[2], 46, 0.7),
            (4.0, bass, 52, 1.8),
            (6.0, bass - 2, 48, 0.9),
            (7.0, bass, 50, 0.9),
        ):
            s = beats(t + off)
            e = beats(min(t + off + dur, 80))
            evs.append((s, note_on(2, n, v)))
            evs.append((e, note_off(2, n)))
        t += hold
        cycle += 1

    # last 4s: cello settles on D, piano octave, strings hold Dm
    s = beats(76)
    e = beats(80)
    evs += [
        (s, note_on(0, 50, 50)),
        (e, note_off(0, 50)),
        (s, note_on(1, 38, 40)),
        (s, note_on(1, 50, 36)),
        (e, note_off(1, 38)),
        (e, note_off(1, 50)),
        (s, note_on(2, 38, 40)),
        (e, note_off(2, 38)),
    ]

    hdr = b"MThd" + struct.pack(">IHHH", 6, 0, 1, PPQ)
    OUT.write_bytes(hdr + track(evs))
    print(f"WROTE {OUT} events={len(evs)}")


if __name__ == "__main__":
    main()
