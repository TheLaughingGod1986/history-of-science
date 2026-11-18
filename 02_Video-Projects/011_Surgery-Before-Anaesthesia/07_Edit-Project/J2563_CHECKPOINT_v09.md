# J2563 cue schedule v02 — 13 November 2026

Cursor covering. Continued PR #560 from 244eb7e5. This run writes the word-timed overlay schedule. It does not download the five remaining pictures, render the rough, spend anything, or approve the film.

## What was written

`07_Edit-Project/OVERLAY_CUE_SCHEDULE_v02.json` (SHA-256 `0bff2f8e81eda41ddb3bbb738cb51018d20f85bc1a7cd2906681becba474bb64`).

38 cards are scheduled from the locked Scribe words. Each card starts when the last word of its phrase starts. No two cards share the frame. A name card keeps the frame: the London date card ends at 371.80 s so Robert Liston's card can start on his surname. 12 planned lines stay held because the narration does not say them, or because another card is already up.

Held, and not to be drawn:

- Under 3 minutes, the three-minute stopwatch, and the egg comparison.
- The opening "Boston, 16 October 1846". The date itself is scheduled at 225.14 s, when it is spoken.
- Early 1800s, Jefferson, 30 March, the 42-year span, and the two-dollar price.
- December 1844, because it falls inside the Horace Wells name card. Hartford is scheduled on its own.
- January 1845, 12 November 1846, and patent number 4,848. The spoken word "Patent" is scheduled.
- Nitrous oxide, because it falls inside the Humphry Davy name card.
- 1868, 4 November 1847, 7 April, and Wembley. The spoken lines "Public garden", "Next year, Edinburgh", "1853", and "90,000 people" are scheduled instead.

Corner credits use the approved source lines. The Morton inhaler credit and the Snow book credit stay held because a name card crosses those pictures. Liston, Davy, and Long portrait lines ride on their name cards. Seven portraits still have no approved credit line in the source manifest.

## Still open

Do not request the five remaining pictures before 2026-11-13T05:30:00Z: Squire inhaler, Liston operating, Simpson pamphlet, Snow inhaler, and Lister spray. The joined rough is not built. P5:16b stays a slate. The four-milestone plan stays at 1/4.

No moving-picture review and no listening review was done. This is not a film-stage pass and it is not Ben's watch copy.

## Checks

`python3 -m unittest test_overlay_schedule_v02.py test_prepare_assembly_v01.py` — 8 tests, OK. Nothing for Ben.
