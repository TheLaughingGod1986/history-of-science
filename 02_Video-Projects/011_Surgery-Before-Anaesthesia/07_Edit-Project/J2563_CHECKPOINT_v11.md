# J2563 archive rows and timing rough v11 — 13 November 2026

Cursor covering. Continued PR #560 from 5dde86f6 after the Chief released the Wikimedia hold (J2759). No generation, credits, narration edits, publishing, stage approval or UAT. Nothing needed from Ben.

## What was built

Five archive rows, from files downloaded with a descriptive contact and at least two seconds between requests. Each file matched the probed size. Media is on studio-live under `J2563_archive_sources_v09/` and `J2563_archive_composites_v09/`.

- P5:03a: Wellcome L0057829, a photograph of a Squire-type copy, CC BY 4.0. Not an 1846 engraving. Credit on screen for 3.5 s: Squire Ether Inhaler (1846), Wellcome / CC BY 4.0. SHA-256 `749ef816af10cd35a5e43b84fa179f3ab150dcbbb075dfb167e635a61dbc52a5`, 520,680 bytes.
- P5:04a: Wellcome M0005603, Ernest Board, CC BY 4.0. Credit: E. Board, Liston Operating (1846), Wellcome / CC BY 4.0. SHA-256 `42d39d9e60ff1c397bea880df75b1054fcfc32ca4a4077a48aa569b61df9da01`, 7,519,367 bytes.
- P5:06a: public-domain NLM scan of Simpson's account. The title page in the file is the 1848 New York third American edition, and it prints the Edinburgh communication of 10 November 1847. A gold line grows under the title. Credit: Simpson, Account of a New Anaesthetic Agent (1847). SHA-256 `3102d1217309a2f8b825292a5afb88d52509149cf6db509fe217e7b691ac467c`, 1,640,119 bytes.
- P5:07a: Wellcome L0058154, the Snow-type inhaler photograph, CC BY 4.0. The book PDF was not used. The corner credit stays off because the John Snow name card occupies this row. Description credit: Snow-type chloroform inhaler (1848-1870), Wellcome L0058154 / CC BY 4.0. SHA-256 `4d21dcede9257f4f3240dc69acfe90a54145b4e14dafaa056df4a355371d11eb`, 1,503,513 bytes.
- P5:14a: Wellcome M0003436, CC BY 4.0. The frame holds the operating scene. Credit: Cheyne, Antiseptic Surgery (1882), Wellcome / CC BY 4.0. SHA-256 `cd842561e025c5d45a8972991ec1a2783272ede4b9dc07a0d9bb3c39e4b4da94`, 5,169,472 bytes.

The internal rough is `J2563_timing_rough_v11/hos_011_timing_rough_v11.mp4`. SHA-256 `0903b729ef9de8bfbb8952e5791a9bc4f6d1401f18e10d9601eda051179a9cf7`. 1920×1080, 30 fps, 16,059 frames, 535.300 s. The locked narration is the same WAV (SHA-256 `d873f1d0c9158087fd61ce0b9f53de985055d778cd58b8df70c67c0701300ae2`, 532.720 s). A level meter reads mean −23.1 dB and max −3.6 dB. That is a measurement, not a listening review.

The picture is 21 earlier free rows, these 5 archive composites, and 67 dependency slates. No download-hold card remains. P5:16b stays a slate.

## Reuse finding for the Chief

P1:07b has no generated file, so its actual duration, in point and out point are empty. The plan gives P1:07b 6.61 s and P5:16b 4.52 s. A disjoint tail would need 11.13 s. An eight-second source used from the start would overlap by 3.13 s. No unused tail was invented, and nothing was stretched, frozen or generated. The slate stays until a real source exists.

## Still open

A reviewer who can watch moving picture still has to look at the rough. No listening review was done. This is not a film-stage pass and it is not Ben's watch copy. The four-milestone plan can leave 1/4: the free rows and the internal rough now exist, and picture approval does not.

## Checks

`python3 -m unittest test_join_timing_rough_v11.py test_join_timing_rough_v10.py test_overlay_schedule_v02.py test_prepare_assembly_v01.py` — 10 tests, OK. The rough covers 93 rows with no gaps and no row over 8.00 s. The joined file was fully decoded. Nothing for Ben.
