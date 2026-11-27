# HOS Channel Audit Uploads Coverage Investigation (`J3847`, 27 Nov 2026)

Follow-up to `J3844` (PR `#806`). Read-only investigation of why `npm run channel:audit` on `@HistoryOfScienceYT` (`UCXp7HkBIl1LgaznXuZHJyRg`) returned 76 rows and omitted the confirmed-public Germs Short `qOZgess30h0` (*Invisible life is still everywhere*).

**No YouTube, schedule, privacy, Buffer, or Test & Compare writes were made.** Only bounded read-only YouTube Data API requests (`channels.list`, `playlistItems.list`, `videos.list`) were executed using the read-only token path. No tokens, account details, email addresses, or raw credential data are stored.

## Summary

1. **Primary cause — upstream YouTube Data API `playlistItems.list` page-boundary omission:**
   - Authenticated `channels.list` (`mine=true`) for `UCXp7HkBIl1LgaznXuZHJyRg` returns uploads playlist `UUXp7HkBIl1LgaznXuZHJyRg` and `statistics.videoCount = 44`.
   - Authenticated `playlistItems.list` on `UUXp7HkBIl1LgaznXuZHJyRg` (`maxResults=50`) returns **80 raw items** across 2 pages (`50 + 30`), matching `pageInfo.totalResults = 80`, but **repeats 4 public video IDs across the page 1 → page 2 boundary** and **omits 4 real HOS videos** from the chronological gap between position 49 (`2026-10-14T20:48:00Z`) and position 54 (`2026-10-02T12:53:40Z`), yielding only **76 unique IDs**.
   - Direct authenticated `videos.list` confirmed all 4 omitted IDs exist on `UCXp7HkBIl1LgaznXuZHJyRg` with `uploadStatus: processed`: **1 public** (`qOZgess30h0`) and **3 private unscheduled** (`mTY67qet7cM`, `K0TQHg4XCHY`, `KIWJRl0dzjw`).
   - Re-running `playlistItems.list` with `maxResults=25` reproduced the same boundary-linked omission behavior: 80 raw rows across 4 pages (`25 + 25 + 25 + 5`), **6 cross-page duplicates**, **74 unique IDs**, additionally omitting 2 more confirmed-public Shorts (`xHnIi9GqOsM`, `qW2OsD4mujc`) at the position 24 → 25 boundary.
   - The internal YouTube backend reason for the `playlistItems.list` boundary overlap is opaque to the API client and is not speculated on here. Empirically, the omission shifts with page boundaries (and therefore surfaced for `qOZgess30h0` when new uploads such as `f_-BsKZf8X0` on 26 Nov shifted earlier videos past index 49).
2. **Code defect / coverage gap in `07_Content-Ops/scripts/channel-audit.ts`:**
   - The pagination loop (`do { ... } while (page)`) and `dedupeVideoIds` / `dedupeVideosById` functioned as written and did not drop unique playlist IDs.
   - However, `channel-audit.ts` relied solely on `playlistItems.list(uploads)` for ID discovery. Unlike Orbit's `analytics-snapshot.ts` (`catalogIds`), it did not cross-check known HOS repo video IDs via direct `videos.list`, nor did it report duplicate/coverage discrepancies (`playlistUniqueCount < pageInfo.totalResults` or `auditedPublicCount < statistics.videoCount`).
   - As a result, `--write-live` silently removed `qOZgess30h0` from `00_Brand/Channel-Setup/audits/LIVE_VIDEOS.json` on 26 Nov (`4b88ba36`), which led the `J3844` draft to misinfer Private status from absence.

## Safe Read-Only Reproduction Evidence (27 Nov 2026, ~02:52–02:58Z)

### 1. Channel baseline (`channels.list?part=id,contentDetails,statistics&mine=true`)
- `id`: `UCXp7HkBIl1LgaznXuZHJyRg`
- `uploads`: `UUXp7HkBIl1LgaznXuZHJyRg`
- `statistics.videoCount`: `44`

### 2. Uploads playlist enumeration (`playlistItems.list`)

| `maxResults` | Pages | `pageInfo.totalResults` | Raw rows | Duplicate IDs (cross-page) | Unique IDs | Known HOS IDs omitted from playlist |
|---:|---:|---:|---:|---:|---:|---|
| `50` | 2 (`50 + 30`) | `80` | `80` | `4`: `clV6E10NLPw`, `TbMMJSRKC3U`, `29bpGAI0wb8`, `GHZDsiH7L7A` | `76` | `qOZgess30h0` (public), `mTY67qet7cM` (private), `K0TQHg4XCHY` (private), `KIWJRl0dzjw` (private) |
| `25` | 4 (`25 + 25 + 25 + 5`) | `80` | `80` | `6`: `ETynHpIYLeY`, `VbPubYd6Fbs`, plus the 4 above | `74` | Same 4 above + `xHnIi9GqOsM` (public), `qW2OsD4mujc` (public) |

Observed boundary positions on `maxResults=50`:
- Page 1 ends at `pos 49`: `5n7xFQRBUvI` (`private`, `2026-10-14T20:48:00Z`).
- Page 2 starts at `pos 50..53` by repeating four Page 1 public videos:
  - `clV6E10NLPw`: page 1 `pos 41` and page 2 `pos 50` (`2026-10-20T10:30:31Z`)
  - `TbMMJSRKC3U`: page 1 `pos 43` and page 2 `pos 51` (`2026-10-18T10:30:11Z`)
  - `29bpGAI0wb8`: page 1 `pos 44` and page 2 `pos 52` (`2026-10-16T10:30:15Z`)
  - `GHZDsiH7L7A`: page 1 `pos 46` and page 2 `pos 53` (`2026-10-15T17:00:24Z`)
- Page 2 resumes new items at `pos 54`: `JI2ewIT1KSM` (`private`, `2026-10-02T12:53:40Z`).

### 3. Direct authenticated `videos.list` verification of omitted IDs

All four HOS repo IDs absent from `playlistItems.list(maxResults=50)` (and the two additional public IDs omitted only at `maxResults=25`) were checked directly via `videos.list?part=snippet,status,contentDetails`:

| ID | Channel match | `privacyStatus` | `publishAt` | `uploadStatus` | `publishedAt` | Duration | Title | Repo source(s) |
|---|---|---|---|---|---|---|---|---|
| `qOZgess30h0` | `UCXp7HkBIl1LgaznXuZHJyRg` | `public` | `null` | `processed` | `2026-10-13T10:30:06Z` | `PT24S` | *Invisible life is still everywhere* | `SHORTS_LOG.md` (and prior `LIVE_VIDEOS.json` / OWB snapshot) |
| `mTY67qet7cM` | `UCXp7HkBIl1LgaznXuZHJyRg` | `private` | `null` | `processed` | `2026-10-03T21:50:56Z` | `PT27S` | *One Tight Band Proved Your Blood Goes Round* | `SHORTS_LOG.md` |
| `KIWJRl0dzjw` | `UCXp7HkBIl1LgaznXuZHJyRg` | `private` | `null` | `processed` | `2026-10-03T21:49:32Z` | `PT27S` | *One Tight Band Proved Your Blood Goes Round (duplicate)* | `SHORTS_LOG.md` |
| `K0TQHg4XCHY` | `UCXp7HkBIl1LgaznXuZHJyRg` | `private` | `null` | `processed` | `2026-10-02T12:54:21Z` | `PT26S` | *The Four Elements Were Wrong (duplicate)* | `SHORTS_LOG.md` |
| `xHnIi9GqOsM` (`maxResults=25` only) | `UCXp7HkBIl1LgaznXuZHJyRg` | `public` | `null` | `processed` | `2026-11-05T11:30:14Z` | `PT23S` | *Why Do Veins Have Valves?* | `LIVE_VIDEOS.json`, `SHORTS_LOG.md` |
| `qW2OsD4mujc` (`maxResults=25` only) | `UCXp7HkBIl1LgaznXuZHJyRg` | `public` | `null` | `processed` | `2026-11-03T11:30:05Z` | `PT24S` | *The Four Elements Were Wrong* | `LIVE_VIDEOS.json`, `SHORTS_LOG.md` |

## Targeted Fix Implemented

- Added `07_Content-Ops/src/lib/hos-contract/audit-coverage.ts`:
  - `collectKnownHosVideoIds(repoRoot)` gathers valid 11-character IDs from `LIVE_VIDEOS.json`, `SHORTS_LOG.md` (column 2 `Id` only), `02_Video-Projects/*/10_Shorts/SHORTS_RELEASE.json`, and `02_Video-Projects/*/11_Upload-Package/PACKAGE_MANIFEST.json`.
  - `planDirectLookupIds(playlistUniqueIds, knownIds)` computes known IDs absent from `playlistItems.list`.
  - `reconcileChannelUploads(...)` merges only direct `videos.list` responses confirmed to belong to `HOS_CHANNEL_ID`, tracks `recoveredViaDirectLookup` and `notReturnedByDirectLookup` (never inferring Private from absence and never forcing totals), and reports duplicate/coverage anomalies.
  - `formatCoverageWarnings(coverage)` emits factual coverage notices in text output.
- Updated `07_Content-Ops/scripts/channel-audit.ts`:
  - Requests `statistics` on `channels.list` (no extra API call), records `playlistItems.list` page count, raw IDs, and `pageInfo.totalResults`.
  - Performs a bounded direct `videos.list` lookup for any known repo IDs (plus optional `--check-ids`) omitted from `playlistItems.list`.
  - Reconciles and audits all confirmed HOS videos, exposes `coverage` in `--json`, prints factual coverage notices in text mode, and keeps `--write-live` from silently dropping public/scheduled videos omitted by playlist pagination.
- Added regression tests in `07_Content-Ops/tests/hos-contract.test.ts` covering cross-page duplicate/omission recovery, foreign-channel filtering, unresolved known IDs without Private inference, and HOS repo source parsing.

## Verification

- `npx vitest run tests/hos-contract.test.ts`: **31 passed (31)**.
- `npx tsc --noEmit`: **PASS** (0 errors).
- `npx eslint src/lib/hos-contract/audit-coverage.ts`: **PASS** (0 warnings, 0 errors).
- Patched read-only live audit (`npx tsx --env-file=.env scripts/channel-audit.ts`, without `--write-live`):
  - **80 videos, 0 errors** (`44` public + `7` scheduled + `29` private unscheduled).
  - Recovered all 4 omitted HOS IDs (`qOZgess30h0` public; `mTY67qet7cM`, `K0TQHg4XCHY`, `KIWJRl0dzjw` private), all 4 passing contract rules with 0 errors.
  - Audited public count (`44`) matches `channels.list` `statistics.videoCount` (`44`); audited total (`80`) matches `playlistItems.list` `pageInfo.totalResults` (`80`).
- `00_Brand/Channel-Setup/tools/check_all.sh`: run before push (see PR check summary).

## Next Step (for Chief Review)

- Review and merge this code/evidence PR.
- After merge, running `npm run channel:audit -- --write-live` will refresh `00_Brand/Channel-Setup/audits/LIVE_VIDEOS.json` to restore public `qOZgess30h0` (51 active rows: 44 public + 7 scheduled). `LIVE_VIDEOS.json` was intentionally left untouched in this code PR to avoid merge conflicts.
