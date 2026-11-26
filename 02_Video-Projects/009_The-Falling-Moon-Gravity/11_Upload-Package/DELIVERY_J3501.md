# Gravity delivery — J3501 — 24 November 2026

Ben approved long v03 (744f32b7f2f95e75fabf039a345aee6c7c01ab6f304a932ebe7172bd3b3ede55) at 24 November 08:42 UTC and both Shorts v01 at 23 November 09:57 UTC, as recorded by Claude in the J3501 brief. No renewed watch is required.

| Cut | YouTube id | Private until (London = UTC) | Thumbnail |
|---|---|---|---|
| Long v03 | wiyfRnsTfTY | 3 December 18:00 | A set by API |
| Moon stopped moving v01 | OhdDVA9kWBk | 4 December 11:30 | Frame 0 set by API |
| Newton gravity v01 | 9ETHUOUH5-A | 5 December 11:30 | Frame 0 set by API |

Before this job none had a YouTube id. All three are now private with the publishAt values above, explicitly authorised by the J3501 upload brief. No public release took place during this job.

Local and NAS long SHA-256 match the approved master. Both uploaded Shorts match the approved delivery manifest. Episode gate, package lint, both Shorts opening gates and upload dry runs pass. The older approved Shorts retain their 25.4/25.5-second runtime (duration warnings only). No film was re-rendered. Final channel audit reports zero errors. Full check_all passes.

British English, Education category, not made for kids and the schedules read back correctly. Long en-GB captions are serving; en-GB caption uploads for both Shorts succeeded. The long was added to the existing series playlist. No comment was posted on a Short. All three thumbnails were set, not refused.

Both Shorts were registered for the daily HOS Buffer mirror with verified hashes, parent wiyfRnsTfTY and social copy. Buffer posts are deferred to the normal seven-day scheduling window. Registration PR: Orbit #1294.

## Pre-public Studio finish (26 November 2026, J3501, CDP 9460, £0)

Completed on existing video ids only (no re-upload, no reschedule):

- **Long `wiyfRnsTfTY` (Private, scheduled Thu 3 Dec 2026 18:00 UK/UTC):**
  - End screen saved: Playlist `How Did We Discover…?` (`PLEbpfUzWzcXU`) + Subscribe (`History of Science`), `8:18:28`–`8:38:28` (exact final 20 s to Studio frame boundary `8:38:28`, zero overlap).
  - 2-way Title + Thumbnail Test & Compare armed & saved (no prior test existed): Arm 1 *How Isaac Newton Proved Gravity Using the Moon* + Thumb A (`IT MISSES`, `cd44f056…`) vs Arm 2 *Why Doesn't the Moon Fall to Earth?* + Thumb B (`ONE APPLE`, `3d116433…`). Reload read-back confirms `A/B testing titles: Ineligible` while Private/Scheduled. Logged as `T045` in OWB PR #1350 (`05_Analytics/tests/THUMB_LEDGER.json`).
  - Two Info cards saved (both past 1:00): Playlist `PLEbpfUzWzcXU` at `2:39:18` and public Franklin long `YqCWYlv_LCY` (*Benjamin Franklin's Kite Experiment Explained*) at `4:26:13`.
  - Metadata verified on reload: `No, it's not Made for Kids`, `Altered content: Yes`, `Paid promotion: No`, `Allow automatic places: Off`, `Category: Education` (`Type: Concept overview`, `Academic system: England`), `en-GB`, Playlist `PLEbpfUzWzcXU`, `Visibility: Scheduled`.
- **Short A `OhdDVA9kWBk` (Private, Fri 4 Dec 11:30 UK) & Short B `9ETHUOUH5-A` (Private, Sat 5 Dec 11:30 UK):**
  - Studio covers replaced auto-generated mid-frames (`sd2.jpg`) with exact 9:16 Frame-0 covers (`IT'S FALLING` on `OhdDVA9kWBk`, `1 MINUTE = 1 SECOND` on `9ETHUOUH5-A`), saved and visually verified on reload.
  - Both verified on reload: `No, it's not Made for Kids`, `Altered content: Yes`, `Paid promotion: No`, `Allow automatic places: Off`, `Education / Concept overview / England`, `Visibility: Scheduled`, `Related video: None`.
- **Post-Studio channel audit (`npm run channel:audit -- --write-live`):** `75 videos, 0 errors.`

## Remaining post-public work (wait check-at `2026-12-03T18:05:00Z`)

Once `wiyfRnsTfTY` is Public (Thu 3 Dec 2026 18:00 UK/UTC):
- Set `Related video → wiyfRnsTfTY` on `OhdDVA9kWBk` and `9ETHUOUH5-A` (before Fri 4 Dec 11:30 UK) and read back.
- Verify `T045` Title+Thumbnail Test & Compare transitions from `Ineligible` to `Running` on `wiyfRnsTfTY`.
- Post and pin the long's open question comment on `wiyfRnsTfTY`.

API receipts and readbacks sit beside this note and in each Short's package. Raw upload logs remain in the Mini job logs. £0; no generation or credit spend.
