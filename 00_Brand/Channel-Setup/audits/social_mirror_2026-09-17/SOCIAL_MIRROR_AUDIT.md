# HOS social mirror audit — 17 Sep 2026 22:00 Europe/London

**Channel:** [@HistoryOfScienceYT](https://www.youtube.com/@HistoryOfScienceYT) only  
**Do not:** TikTok · Orbit (@orbitwithben) · Wellesley (@historyofscience) · Oppti

## Verdict

**YouTube is live. Social is not mirrored.**

Public HOS YouTube (7 videos) has **zero** matching posts on Instagram `@historyofscienceyt`, Threads `@historyofscienceyt`, or the HOS Facebook Page `61593586420124`. Ledgers (`META_POSTED.json`, `THREADS_POSTED.json`) still only list August Orbit/aliens leftovers.

Did **not** post the catch-up from this pass: Mini Chrome CDP 9222/9223 is logged into **Orbit with Ben**, not HOS. Posting from those sessions would have shipped Germs / Periodic Table onto `@orbitwithben`. TikTok stays paused.

## Live YouTube (due for social)

| Kind | ID | Title | Social |
|---|---|---|---|
| Long | `AL_-qlWko_g` | How Did We Discover the Periodic Table? | **missing** (public ~2h) |
| Long | `_C92tIJCk8A` | How Did We Discover Germs? | **missing** (public 2 weeks) |
| Short | `H1y0DXFVmw8` | Germs don't cast a shadow | **missing** (78 views) |
| Short | `iqToagXnjX0` | Microbes in a drop of pond water | **missing** (110 views) |
| Short | `8_Edn_HCi1s` | Germs hitch a ride on you | **missing** (26 views) |
| Short | `sILtQxgYQk8` | A flask that proved germs come from outside | **missing** (24 views) |
| Short | `93fPUG-hW0A` | Invisible life is still everywhere | **missing** (6 views) |

Germs Shorts were reminted after the Sep 2 schedule. Old ids (`8uBR-9oxeWs`, `YX2UR1u-JCQ`, `Fnb3p81u-wY`, `vpuRgKXtFlY`, `Lcmh5y2KMQM`) are historical duplicates — uniqueness still forbids a second social post of the same title/file.

## Not due yet (do not dump)

| Short | ID | YouTube | Social |
|---|---|---|---|
| The periodic table's empty chairs | `uU12JA5rMWg` | Scheduled Fri 18 Sep 11:30 London | wait |
| He predicted a metal before it was found | `nFQRWmpulTQ` | Sat 19 Sep 11:30 | wait |
| Gallium sat where the table said | `CnHwX1L9XHg` | Sun 20 Sep 11:30 | wait |
| Why tellurium sat before iodine | `nba0-f7PPeU` | Mon 21 Sep 11:30 | wait |
| What other table has empty chairs? | `LanTHJckYx8` | Tue 22 Sep 11:30 | wait |

Never social-post a Short before it is public on YouTube. Never social-post 002 Shorts before Friday.

## Destinations (locked)

| Surface | Handle / id | State 17 Sep |
|---|---|---|
| Instagram | [@historyofscienceyt](https://www.instagram.com/historyofscienceyt/) | 1 follower · grid empty · login wall |
| Threads | [@historyofscienceyt](https://www.threads.com/@historyofscienceyt) | 0 followers · **No threads yet** |
| Facebook | Page [61593586420124](https://www.facebook.com/profile.php?id=61593586420124) | 26 followers · profile picture only · no Reels |
| TikTok | paused | `TIKTOK_UPLOAD_BLOCK.json` |

`facebook.com/HistoryOfScienceYT` is **not** a public slug (login sees “content isn't available”). Use the numeric Page id.

## Why the watcher never fired

1. No `10_Shorts/SHORTS_UPLOAD_INDEX.json` on 001 / 002 (discover only reads that file).
2. `Meta/auto/discover.py` and `Threads/auto/discover.py` still pointed at `/Users/ben/code/Orbit-YouTube`.
3. `suite_ids.pin_suite_creds` fell back to Orbit Page `61592833318203` when HOS `page_id` was null.
4. Threads CDP default username was `@historyofscience` (Wellesley).
5. Mini ports 9222/9223 are Orbit sessions (`@orbitwithben` / Orbit Facebook). Instagram on 9223 is logged **out**.

## Unblock (Ben / next agent)

1. Dedicated Chrome profile logged into **@historyofscienceyt** (IG + Threads). Do not switch the Orbit CDP profile.
2. Add HOS Page `61593586420124` to a HOS Business Suite (not the Orbit-with-Ben portfolio) **or** Graph tokens for that Page + IG pro id.
3. Link `@historyofscienceyt` to that Page so Reels can cross-post.
4. Then `live_shorts_to_meta.py --once` and `live_shorts_to_threads.py --once` from this repo — destination guard now aborts Orbit/Wellesley.
5. Longs: soft YouTube link on Threads + HOS Facebook only (not IG Reels, not Orbit).
6. 002 Shorts: mirror **after** each YouTube air (Fri–Tue 11:30), one unique post per platform.

TikTok stays paused until Ben lifts `TIKTOK_UPLOAD_BLOCK.json`.
