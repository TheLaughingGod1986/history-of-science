# J1267 rough v10

Built from rough v08 by replacing one GOP. J1273 alpha 53454827126b copied into code_graphics_v07. render_alpha() was not called. GBP0. No UAT copy.

## Durations
format 539.626479 video 539.5 start 0.125 frames 12923 A/V end offset 0.0014790000000175496

## Composite vs f8453cc7
worst mean abs 0.834 limit 1.0 pass True

## Frame diff vs v08 at 463.2/464/466/468.7
worst 0.0 limit 1.0 pass True
indexes: [(463.2, 11090, 11090), (464.0, 11109, 11109), (466.0, 11157, 11157), (468.7, 11222, 11222)]

## Tip
worst 10.5 px limit 19.2 pass True

## Gates
polish_rc 0 picture_rc 0

## Safe path
29-frame lead-in plus the v08 body. 29+157=186. Total frames 12923.
The 22 frames from 462.250s to 463.167s are the v08 picture re-encoded inside the replaced GOP. From the 463.166667s keyframe onward the packets are stream-copied from v08.

## VO
Audio matches rough v08 (MD5 of 450-465s identical). STT at the v09 offset, film = part + 409.875s:
- 459.30-461.05s: apart. But a metal
- 461.05-462.26s: rod is an easy
A fresh correlator on this run scored 0.108 and did not re-lock; the words above are the v09 alignment on this same audio.
