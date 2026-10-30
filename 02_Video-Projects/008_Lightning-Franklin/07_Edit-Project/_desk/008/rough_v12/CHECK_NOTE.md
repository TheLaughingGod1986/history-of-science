# J1267 rough v12

Chief h21. One title: the card's own SAFE PATH DOWN pixels from v08 frame 11114 (464.208 s), pasted onto the opening field. Not a separately drawn title. Alpha 53454827126b copied into code_graphics_v07. render_alpha() was not called. GBP0. No UAT copy.

## Durations
format 539.626479 video 539.5 start 0.125 frames 12923 A/V end offset 0.0014790000000175496

## Title box vs v08 at 464.208 s, frames 11067-11118
worst 0.952 limit 1.0 pass True over []

## Join 11088 vs 11089
mean abs 0.001 limit 1.0 pass True

## Body vs v08 at 464.2/466/468.7/469.6, and stream copy at 469.708
body worst 0.409 limit 1.0 pass True

## Old plate gone (frames 11067-11088)
min mean abs 44.408 need above 1.0 pass True

## Composite vs f8453cc7
worst 0.866 limit 1.0 pass True

## Tip
worst 10.5 px limit 19.2 pass True

## Audio
streamhash match True

## Gates
polish_rc 0 picture_rc 0

## Safe path
51-frame lead-in (29 fade + 22 hold) plus 157 re-encoded card frames. The full title is held through 464.375 s. From 469.708 s the packets are stream-copied. Total frames 12923.
