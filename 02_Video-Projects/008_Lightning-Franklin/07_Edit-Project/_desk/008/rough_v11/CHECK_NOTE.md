# J1267 rough v11

Chief h20. Built from rough v08 by replacing one GOP. J1273 alpha 53454827126b copied into code_graphics_v07. render_alpha() was not called. GBP0. No UAT copy.

## Durations
format 539.626479 video 539.5 start 0.125 frames 12923 A/V end offset 0.0014790000000175496

## Composite vs f8453cc7
worst mean abs 0.834 limit 1.0 pass True

## Frame diff vs v08 at 463.2/464/466/468.7
worst 0.0 limit 1.0 pass True
indexes: [(463.2, 11090, 11090), (464.0, 11109, 11109), (466.0, 11157, 11157), (468.7, 11222, 11222)]

## Old plate gone (frames 11067-11088)
min mean abs 44.427 need above 1.0 pass True

## Join last lead-in vs first card at 463.167s
mean abs 1.747 limit 1.0 pass False
frames 11088 -> 11089

## Tip
worst 10.5 px limit 19.2 pass True

## Audio
streamhash match True

## Gates
polish_rc 0 picture_rc 0

## Safe path
51-frame lead-in (29 fade + 22 hold) plus 135 v08 card frames. 51+135=186. Total frames 12923.
Frames 11067-11088 are the lead-in hold, not the old plate. From the 463.166667s keyframe the packets are stream-copied from v08.
