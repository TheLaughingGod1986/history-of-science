# J1267 rough v09 stopped before the splice

Chief h14 asked for source frames 109-150 and the same trace registration as alpha `bb821f40`. The 42-frame composite was built. The rod-top check then failed, so no master was spliced and nothing was overwritten.

Locked alpha left untouched: `bb821f402a2d1ca5a1536a6592e572b8a4d1653d6573ca733c2ae853db4c8056`
New alpha (v06, 42 frames, 24 fps): sha `dd2ab58280f0` (full hash in the render log)
New composite `overlay_10_metal_easy.mp4`: sha `56348a8e0254`

Rod-top vs trace x=1180.5, limit 1% of width (19.2 px):

| sample | plate time | offset |
|---|---|---|
| p10 | 4.717 s | +6.5 px (+0.34%) |
| p25 | 4.979 s | **-34.5 px (-1.80%)** |
| p50 | 5.417 s | -2.5 px (-0.13%) |
| p75 | 5.854 s | +17.5 px (+0.91%) |
| p90 | 6.117 s | +17.5 px (+0.91%) |

p25 is the only miss. The detector's dark pixel at the top of the frame (y=20) sits at x=1146; lower on the shaft (y=600) the same frame is x=1171, about 9 px off the trace. Trace was not moved. In-point was not moved. No slow-mo, freeze, or second plate.

Also measured, not built: the v08 safe-path row is 157 frames, not the 168-frame asset. A 29-frame lead-in plus those 157 frames is 186 and keeps 12,923 frames. 29+168=197 would cover 11 frames of the next row.
