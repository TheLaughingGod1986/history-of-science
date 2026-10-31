# HOS 008 master v02 — review for Chief (J1287)

Cursor, 31 Oct 2026. Not a finished-film PASS. No Ben watch, no UAT, no upload. No new ElevenLabs take.

Chief h29: the v01 loop at 8:00 joined the take's fade-out to its opening theme. This cut replaces that join only. The picture is still locked rough v12.

## Picture

Video-stream MD5 of v12 and this master is `1ab08ec6b7bb7dbb7b44d272710474dd`. 12,923 video packets, video start 0.125 s, video duration 539.500 s. Rough v02–v12 and master v01 were not written.

| | v12 | master v02 |
|---|---|---|
| format duration | 539.626479 s | 539.626479 s |
| video packets | 12923 | 12923 |
| audio end | 539.626479 s | 539.626479 s |
| A/V end offset | 0.001479 s | 0.001479 s |

VO lag against the v12 decode is −1.0 ms (the mix against the aligned VO stem is 0.0 ms). Offset is inside one frame, and inside the ±1 ms bar.

Master sha256 `b43185edd215a68f876d28d5a19ef1482d713ce1dcfd1e888473047371484fe3`

- Local precheck: `07_Edit-Project/_precheck/master_v02/hos_008_master_v02.mp4`
- NAS desk: `/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_desk/008/master_v02/hos_008_master_v02.mp4` (same sha256)

## Music — same take, one new seam

Source is `lightning008_score_bed_v01_take.mp3`, song `XV6uI76yzdLON8PmTVwC`. Credits spent on this pass: 0.

The take is silent until 50.70 s. Film 0:00 plays the take from there. One mid-body repeat, 15 bars (54.0 s) on the 66.7 BPM grid (0.9 s beats, 3.6 s bars), joins with a 3.0 s equal-power crossfade. The repeat is take 370.45–424.45 s, not the opening theme at 50.7–110 s. The take's fade-out is at the film end. The unused file tail after 539.326 s is −89 dBFS.

Seam centre 372.25 s (fade 370.75–373.75), under running VO, more than 2 s from the long pauses and from the chapter cards at 319.00 and 408.96.

| Check | Result |
|---|---|
| 2 s RMS each side | −42.57 and −43.26 dB, delta 0.69 dB |
| Short-term LUFS ±2 s | −40.3 and −40.7, delta 0.4 LU |
| 2nd-diff click | seam 0.00158, body max 0.00375 |
| Spectral flux | seam 5.23, body p99.9 14.51 |
| Quiet stretch ≥6 s and >6 LU under the median | none outside the final ending |

Ducked bed, speech: mean 20.22 LU under the VO, 0 breach runs of 0.3 s. Pauses of 0.8 s or longer sit 16.18 LU under the VO's integrated loudness, 4.04 LU above the speech level. A few single 100 ms frames dip under 10 LU (the worst is 3.1 LU, two frames). `sfx_kit.py level --bed` PASS, 0 fails.

## SFX

House kit, no new render. Chapter 2 whoosh moved from 100.05 s to 99.67 s so its loud body ends at 100.36 s, 0.10 s before "In" at 100.46 s. Chapter 3 whoosh already ended at 188.44 s, 0.10 s before 188.54 s, so it stayed at 187.75 s. The other 19 cues are sample-identical.

## Mix

Integrated **−14.3 LUFS**. True peak **−1.3 dBFS**. LRA 3.8 LU.

## Chapters

Stamps in `lightning_long_description_v01.txt` were not moved. They still sit on the locked part starts (0:00, 1:40, 3:08, 5:19, 6:49).

## Gates

| Gate | Result |
|---|---|
| polish_gate | PASS, 0 of 112 failed. One low-detail warn on `13_ring_the_bells_c1`, same class as v01. |
| picture_qa | PASS, 0 of 112 cuts fail, 7 warns |
| music_gate | PASS, 66.7 BPM, 0 fails, 0 warns. 54 readable beds compared (127 iCloud placeholders skipped). Top similarity 0.394, nearest-star bed. |
| gate:episode | PASS, script 92.1/90 |
| package-lint | PASS. One captions warning: no captionsFile. Chapters unchanged. |

Top five music similarities: 0.394 nearest-star, 0.289 Venus, 0.286 HOS 005 part 03, 0.251 HOS 004 part 03, 0.244 HOS 005 part 05. Fail line is 0.8. This film's own v01 arrangement of the same take scores 0.605, under that line. It was left out of the other-film list.

## Not done here

PR #385 is not merged. No UAT copy and no upload until Chief passes this master.
