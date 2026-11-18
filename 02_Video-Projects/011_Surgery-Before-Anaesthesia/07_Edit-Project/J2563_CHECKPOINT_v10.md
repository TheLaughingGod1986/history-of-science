# J2563 timing rough v10 — 13 November 2026

Cursor covering. Continued PR #560 from 0fbc15d5. This run joins the internal timing rough. It does not download the five remaining pictures, spend anything, or approve the film.

## What was built

`J2563_timing_rough_v10/hos_011_timing_rough_v10.mp4` on studio-live.

SHA-256 `20c813c341f42e07211b95d23b38aac7eefe40dce83d23f66c72cb3335eb5a48`. 1920×1080, 30 fps, 16,059 frames, 535.300 s. The locked narration `hos_011_vo_v01.wav` (SHA-256 `d873f1d0c9158087fd61ce0b9f53de985055d778cd58b8df70c67c0701300ae2`, 532.720 s) is carried as an AAC timing copy, with silence under the 2.58 s end hold. A level meter reads mean −23.1 dB and max −3.6 dB. That is a measurement, not a listening review.

The picture is the 21 delivered free rows, the 67 dependency slates, and five labelled hold cards. The hold cards say the download is still held. They are not the approved photographs. P5:16b stays the existing dependency slate. No unused tail was invented.

Three delivered rows were one frame off the v03 boundary. The rough fits them and leaves the source files unchanged:

- P3:01_card_p03: 73 frames fitted to 72
- P4:01_card_p04: 107 frames fitted to 108
- P4:03a_arch_letheon_patent: 142 frames fitted to 141

## Still open

Do not request the five remaining pictures before 2026-11-13T05:30:00Z: Squire inhaler, Liston operating, Simpson pamphlet, Snow inhaler, and Lister spray. When those pictures exist, this rough should be rebuilt so the hold cards come out. The four-milestone plan stays at 1/4.

No moving-picture review and no listening review was done. This is not a film-stage pass and it is not Ben's watch copy. A reviewer who can watch moving picture still has to look at it.

## Checks

`python3 -m unittest test_join_timing_rough_v10.py test_overlay_schedule_v02.py test_prepare_assembly_v01.py` — 9 tests, OK. The rough covers 93 rows with no gaps and no row over 8.00 s. The joined file was fully decoded. Nothing for Ben.
