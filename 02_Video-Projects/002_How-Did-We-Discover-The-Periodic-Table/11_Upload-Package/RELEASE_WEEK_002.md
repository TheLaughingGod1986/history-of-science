# HOS 002 — Studio premiere + Shorts cluster

**Channel:** [@HistoryOfScienceYT](https://www.youtube.com/@HistoryOfScienceYT) only  
**Not:** Orbit · Oppti  
**Affiliate:** none · **zero `/go/`**

## Long (pillar)

| Field | Value |
|---|---|
| Title A | How Did We Discover the Periodic Table? |
| Cut | `hos_002_periodic_table_full_v02.mp4` |
| sha256 | `8a5b8dde713cd4d6d2834b49635443ebf5fda1a83de92688bf79ca91746de31f` |
| Premiere | **Thursday 17 Sep 2026 19:00 Europe/London** |
| Thumb A | live-lock gallium (`hos_002_thumb_A_gallium_live_v02.jpg`) |
| Made for kids | No |
| Subscribe | Studio end screens only |
| ABC | After Premiere ends (Premiere videos cannot A/B until then) |

## Shorts (after the long listing exists)

None before the Premiere. First Short **Friday 18 Sep 2026 11:30 Europe/London**. Related ▶ this long’s exact title / id.

| Slot | London | Title |
|---|---|---|
| s01 | Fri 18 Sep 11:30 | The periodic table's empty chairs |
| s02 | Sat 19 Sep 11:30 | He predicted a metal before it was found |
| s03 | Sun 20 Sep 11:30 | Gallium sat where the table said |
| s04 | Mon 21 Sep 11:30 | Why tellurium sat before iodine |
| s05 | Tue 22 Sep 11:30 | What other table has empty chairs? |

Uploader: `Schedule/_upload_hos_002_shorts_v01.py` · finish: `Schedule/_finish_hos_002_shorts_v01.py`

## Status 11 Sep 2026 10:20 London

Long is on **@HistoryOfScienceYT** as id `AL_-qlWko_g`.

- Title A, description, chapters, live-lock thumb A, not made for kids
- **Premiere Thursday 17 Sep 2026 19:00** (Studio Visibility: Premiere)
- Zero `/go/` · do not lead with a Short · ABC after Premiere ends
- Pinned comment not posted yet (no comments on a scheduled listing)

https://youtu.be/AL_-qlWko_g

Five punch Shorts are **Scheduled** at 11:30 Europe/London (never Public on finish). Covers are live_v02 illustrated 9:16. Descriptions already link the long. Studio Related ▶ picker did not save.

| Slot | London | Title | id |
|---|---|---|---|
| s01 | Fri 18 Sep 11:30 | The periodic table's empty chairs | `uU12JA5rMWg` |
| s02 | Sat 19 Sep 11:30 | He predicted a metal before it was found | `nFQRWmpulTQ` |
| s03 | Sun 20 Sep 11:30 | Gallium sat where the table said | `CnHwX1L9XHg` |
| s04 | Mon 21 Sep 11:30 | Why tellurium sat before iodine | `nba0-f7PPeU` |
| s05 | Tue 22 Sep 11:30 | What other table has empty chairs? | `LanTHJckYx8` |

One extra s02 draft (duplicate file) is left as **Draft** and is not scheduled.

## Status 11 Sep 2026 11:16 London — live_v02 covers on the Content list

Phone Studio still showed **film-frame** covers on s03, s04, and a cropped long row. Desktop Content list is the proof surface. Re-applied every `live_v02` still with click **Upload file** → image input (skip video-only) → **Save**. Helper: `Schedule/_force_hos_002_thumbs_live_v02.py`.

| Row | id | Cover on Content list |
|---|---|---|
| s01 | `uU12JA5rMWg` | THE EMPTY WERE THE CHAIRS |
| s02 | `nFQRWmpulTQ` | HE PREDICTED A METAL |
| s03 | `CnHwX1L9XHg` | GALLIUM IN THE GAP |
| s04 | `nba0-f7PPeU` | TELLURIUM BEFORE IODINE |
| s05 | `LanTHJckYx8` | WHAT OTHER TABLE HAS GAPS? |
| long | `AL_-qlWko_g` | gallium live_v02 + PREMIERE |

The leftover s02 **Draft** still uses a film frame — leave it unpublished. Phone app may cache old stills; pull-to-refresh Content → Scheduled. Do not click Public.

## Status 11 Sep 2026 12:10 London — s03 cover actually stuck

Phone Scheduled still showed a **film frame** on s03 (`CnHwX1L9XHg`) after the 11:16 pass. Edit page had empty Upload file / Select from video tiles — the earlier `set_input_files` path did not persist. Re-uploaded via Studio **Upload file** file-chooser (`accept=image/jpeg,image/png`) → Save → reload. Custom **GALLIUM IN THE GAP** still present after reload. Helper now prefers the file chooser.
