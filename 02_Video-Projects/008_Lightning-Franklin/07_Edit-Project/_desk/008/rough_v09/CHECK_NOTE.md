# J1267 rough v09 — check failed, parked for Chief

Built the same way as v08, from rough v04 e00bb897. New folders only. GBP0. No music bed, no upload.

## What matches
- Frame count 12923. Format 539.626s, video 539.500s, A/V end offset 0.0015s.
- polish_gate PASS (0 fail). picture_qa PASS (0 fail).
- Rod-top vs trace: worst 14.0 px, limit 19.2 px (1% of width). align_ok.
- Plate is source frames 109-150 (4.542-6.250s), 42 frames. Visual plate 459.292-461.042s.
- Unchanged frames outside this edit match v08 at mean abs 0 (checked 100, 200, 400, 450, 470, 500, 530s).

## What fails
Frame diff vs v08, mean abs, limit 1.0:

| t | mean abs |
|---|---|
| 462.3 | 44.311 |
| 464.0 | 1.531 |
| 466.0 | 1.070 |
| 468.7 | 1.001 |

At 462.3s v08 is still the METAL CONDUCTS plate. The plate picture in v08 runs to 463.125s: the 71-frame overlay ends near 462.25s, then the underlying v04 plate keeps the same label for about 22 frames, and the card starts at 463.167s. v09's 42-frame plate ends at 461.042s, so 462.3s is the SAFE PATH DOWN lead-in. Those are different pictures. The later samples are the settled card, just over 1.0 from the re-encode.

The brief's row clock (plate 459.297-461.047, match v08 from 462.256) cannot meet mean abs <= 1.0 at 462.3s, because v08's picture is still the plate there.

## Safe-path length
The v08 row holds 157 frames of the 168-frame asset. 29 + 157 = 186 keeps the row end (461.047-468.796) and the 12923-frame total. 29 + 168 = 197 would cover 11 frames of the next row.

## VO
Envelope match score 0.820, film = part + 409.875s.
- 459.30-461.05s: "apart. But a metal" (rod starts 461.14s)
- 461.05-462.26s: "rod is an easy" (path starts 462.44s)

Not forced. No other plate, no slow-mo, no freeze, no frame replay.
