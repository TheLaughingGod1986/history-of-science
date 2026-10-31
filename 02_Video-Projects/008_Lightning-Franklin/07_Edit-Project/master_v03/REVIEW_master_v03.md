# HOS 008 master v03 — review for Chief (J1287)

Cursor, 31 Oct 2026. Not a finished-film PASS. No Ben watch, no UAT, no upload. No new ElevenLabs take.

Chief h33: the v02 voice was 19.667 ms early because `align_vo()` trimmed 944 samples from a stem that was already at 0, and the chapter 3 whoosh body ended 0.08 s before "Franklin". This cut fixes those two things. The picture is still locked rough v12. The arranged bed is still `stem_bed_v02_arranged.wav` (sha `142b7d41bb5aaf3403ec0c09f73af875c40b3f3f9953bde3361d18cd91c17355`), seam centre 372.25 s.

## Picture

Video-stream MD5 of v12 and this master is `1ab08ec6b7bb7dbb7b44d272710474dd`. 12,923 video packets, video start 0.125 s, video duration 539.500 s. Rough v02–v12 and masters v01 and v02 were not written.

| | v12 | master v03 |
|---|---|---|
| format duration | 539.626479 s | 539.626479 s |
| video packets | 12923 | 12923 |
| audio end | 539.626479 s | 539.626479 s |
| A/V end offset | 0.001479 s | 0.001479 s |

The offset is the video end (0.125 + 539.500) against the audio end. It is inside one frame.

Master sha256 `cf1561c218bace7bc14ed3d625b0790a457027a90f392262f45ca7172723099b`

- Local precheck: `07_Edit-Project/_precheck/master_v03/hos_008_master_v03.mp4`
- NAS desk: `/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_desk/008/master_v03/hos_008_master_v03.mp4` (same sha256)

## Voice

`stem_vo_v12.wav` from sample 0, cut to 25,902,071 samples. Nothing trimmed off the front. The mix chain is latency-neutral: `amix` with normalize off, a static +7.1 dB, then `alimiter` at −1.5 dB with attack 0.1 ms and delay compensation. No `loudnorm`. `normalization_type` is linear.

Full-file decodes, no input seek and no decimation. Lag of the master against v12:

| t | ffmpeg | afconvert |
|---|---|---|
| 5 s | 0.000 ms | 0.000 ms |
| 100 s | 0.000 ms | 0.000 ms |
| 300 s | 0.000 ms | 0.000 ms |
| 500 s | 0.000 ms | 0.000 ms |

The unshifted stem alone, before the mix, measured 0.000 ms at the same four points.

## Music — same arranged bed, re-ducked

Source arrangement unchanged. Credits spent on this pass: 0. Seam centre 372.25 s (fade 370.75–373.75), source 370.45–424.45 s, take ending at the film end.

| Check | Result |
|---|---|
| 2 s RMS each side | −42.54 and −43.28 dB, delta 0.74 dB |
| Short-term LUFS ±2 s | −40.3 and −40.7, delta 0.4 LU |
| 2nd-diff click | seam 0.00159, body max 0.00375 |
| Spectral flux | seam 5.25, body p99.9 14.53 |
| Quiet stretch ≥6 s and >6 LU under the median | none |

Ducked bed, speech: mean 20.25 LU under the VO, 0 breach runs of 0.3 s. Pauses of 0.8 s or longer sit 16.26 LU under the VO's integrated loudness, 3.99 LU above the speech level. A few single 100 ms frames dip under 10 LU (the worst is 4.2 LU, two frames).

`sfx_kit.py level --bed` PASS, 0 fails:

```
SFX level PASS: VO -20.5 LUFS, SFX -35.7 LUFS, 20 hits
{"verdict": "PASS", "vo_integrated": -20.5, "sfx_integrated": -35.7, "hits": 20, "fails": [], "warns": []}
```

## SFX

House kit, no new render. Chapter 2 stays at 99.67 s. Its 20 dB body ends at 100.51 s, 0.11 s before the energy onset of "In" at 100.62 s. Chapter 3 moves from 187.75 s to 187.65 s. Its 20 dB body ends at 188.41 s, 0.20 s before the energy onset of "Franklin" at 188.61 s (first 10 ms above −45 dBFS). Every other sample, including the other 19 cues and the chapter 2 whoosh, is unchanged.

## Mix

Integrated **−14.1 LUFS**. True peak **−1.2 dBFS**. LRA 4.1 LU. The wav before the AAC encode measured the same −14.1 / −1.2.

## Chapters

Stamps in `lightning_long_description_v01.txt` were not moved. They still sit on the locked part starts (0:00, 1:40, 3:08, 5:19, 6:49). The voice is back on the v12 clock, so those stamps did not move.

## Gates

All five exited 0. Unmodified tools.

| Gate | Result |
|---|---|
| polish_gate | PASS, 0 of 112 failed. Five low-detail warns (edge density just under the film's own p5), including `18_rod_closeup`. |
| picture_qa | PASS, 0 of 112 cuts fail, 7 warns. Same seven as v02: four low-detail rows, plus `10_metal_easy` and `11_safe_path` untitled in the pool. |
| music_gate | PASS, 66.7 BPM (not null), 0 fails. 127 warns, every one an unreadable iCloud placeholder. No other-film similarity reached the 0.8 fail line. The bed file was not rewritten (sha `40937135976eeb99fe33acedc5924b0bd41f89b20244b81a2759da7792f4404c`), so the v02 top similarity of 0.394 still describes it. |
| gate:episode | PASS, script 92.1/90 |
| package-lint | PASS. One captions warning: no captionsFile. Chapters unchanged. |

## Not done here

No UAT copy and no upload. Parked for Chief. PR #385 was already merged (38c5cdc, h29).
