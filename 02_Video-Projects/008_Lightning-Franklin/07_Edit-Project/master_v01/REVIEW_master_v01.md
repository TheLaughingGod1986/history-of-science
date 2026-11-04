# HOS 008 master v01 — review for Chief (J1287)

Cursor, 30 Oct 2026. Not a finished-film PASS. No Ben watch, no UAT, no upload.

## Picture

Locked rough v12 is unchanged. Video-stream MD5 of v12 and this master is `1ab08ec6b7bb7dbb7b44d272710474dd`. 12,923 video packets, 1920×1080, 24 fps, video start 0.125 s, video duration 539.500 s. Rough v02–v12 were not written.

| | v12 | master v01 (gain) |
|---|---|---|
| format duration | 539.626479 s | 539.646875 s |
| video packets | 12923 | 12923 |
| audio end | 539.626479 s | 539.646875 s |
| A/V end offset | 0.001479 s | 0.021875 s |

Offset is under one frame (0.0417 s). The VO was not re-spoken and not edited. The mix uses a PCM decode of the v12 audio.

Master sha256 `0eced44bf65a5cb12567f085e5ca286f45f0adac2d727fb331840e58158d7877`

- Local: `07_Edit-Project/_precheck/master_v01/hos_008_master_v01_gain.mp4`
- NAS desk: `07_Edit-Project/_desk/008/master_v01/hos_008_master_v01.mp4` (same bytes after the copy in this job)

An earlier mix, sha256 `163c98676ed85e7331dc3a0226e8cb295b057868dc04de1b8fb1689290df0d8c`, stays on the NAS desk as `hos_008_master_v01_flatpause.mp4`. Its bed did not rise in pauses. It was not deleted.

## Music — one take

`05_Music/lightning008_score_bed_v01.mp3`, song `XV6uI76yzdLON8PmTVwC`. Dry-run first, then one generate. The balance read immediately before and after both showed 8,101 used and 113,013 remaining (delta 0 on that read). No second take. No top-up.

The take itself is silent for about 50 s from the start (`lightning008_score_bed_v01_take.mp3`, kept). The laid bed is that same take shifted 50 s, with the tail looped from the same file, so the opening has music. Tempo **66.7 BPM** (brief Pace 64–72). `music_gate` fail list empty.

The mix stem is `scratch/J1287/stem_bed_v01g.wav`, a gain pass on the shifted stem `stem_bed_v01c.wav`. Speech, bed under the VO: mean 20.75 LU, p10 14.93, min 11.6. Pauses of 0.8 s or longer sit 16.86 LU under the VO's integrated loudness, 3.9 LU louder than speech, so the bed rises there. Shorter gaps stay ducked (all-pause mean 20.0 LU under). Breach runs of 0.3 s under 10 LU: 0.

`sfx_kit.py level --bed` **PASS**, 0 fails:

```
SFX level PASS: VO -20.5 LUFS, SFX -35.7 LUFS, 20 hits
{"verdict": "PASS", "vo_integrated": -20.5, "sfx_integrated": -35.7, "hits": 20, "fails": [], "warns": []}
```

## SFX

House kit, seed 1287, no spend. Ink ticks on the Franklin WHO card, the date stamps and the data pills; a page-turn whoosh before each chapter card. Ticks sit off the first word of a line. Level PASS as above.

## Mix

Integrated **−14.12 LUFS**. True peak **−1.04 dBFS**. LRA 3.6 LU.

## Chapters

Stamps in `lightning_long_description_v01.txt` were not moved. They sit on the locked part starts:

| Stamp | Part start | First speech |
|---|---|---|
| 0:00 Fire from the sky | 0.00 | 0.10 |
| 1:40 The sparks in a jar | 100.25 | 100.60 |
| 3:08 A kite in the storm | 187.95 | 188.65 |
| 5:19 The spark from the key | 319.00 | 320.05 |
| 6:49 The rod on every roof | 408.96 | 408.95 |

Five stamps, 0:00 first, gaps 100 / 88 / 131 / 90 s. `package-lint --film 008` PASS (one captions warning: no captionsFile).

## Gates

Video bitstream is the v12 stream, so polish and picture from the 21:20 run apply to this file (same MD5). Fresh `music_gate` on this bed: PASS, 66.7 BPM, fail [].

| Gate | Result |
|---|---|
| polish_gate | 0 fail (rc 0). One low-detail warn on `13_ring_the_bells_c1`. |
| picture_qa | PASS, 0 of 112 cuts fail, 7 warns |
| music_gate | PASS, 66.7 BPM, fail [] |
| gate:episode | PASS, script 92.1/90 |

## Not done here

PR #385 (rough evidence) is open, mergeable, and its checks are green. A worker does not merge it. No UAT copy and no upload until Chief passes this master.
