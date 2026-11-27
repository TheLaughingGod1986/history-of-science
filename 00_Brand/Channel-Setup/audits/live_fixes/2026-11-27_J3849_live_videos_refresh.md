# HOS `LIVE_VIDEOS.json` Inventory Refresh (`J3849`, 27 Nov 2026)

Follow-up to `J3847` (PR `#808`, merge commit `5f3c0a837587be4ca7aaa2b09c36cdd47725de5b`). Refreshed `00_Brand/Channel-Setup/audits/LIVE_VIDEOS.json` in an isolated worktree using the merged `07_Content-Ops/scripts/channel-audit.ts --write-live` (read-only YouTube Data API token path).

**No YouTube, Studio, privacy, schedule, Buffer, Test & Compare, or title writes were made.** This is a repository inventory refresh only, not a video restore.

## Live Audit Result (`2026-11-27T03:29:47.729Z`)

- **Exit code:** `0` (`0` channel findings, `0` video contract errors across all `80` audited HOS videos).
- **Audited inventory (`80` total):**
  - **44 public:** `8` longs + `36` Shorts
  - **7 private scheduled:** `2` longs + `5` Shorts
  - **29 private unscheduled:** `1` long + `28` Shorts (excluded from `LIVE_VIDEOS.json` per filter `privacy !== "private" || scheduled`)
- **`qOZgess30h0` confirmed Public:** directly returned via `videos.list` on `UCXp7HkBIl1LgaznXuZHJyRg` as `kind: "Short"`, `privacy: "public"`, `scheduled: ""`, `title: "Invisible life is still everywhere"`, `0` contract errors (`ai-disclosure` API-omission notice only).

## Coverage Notices & Unresolved IDs

- **Exact coverage notices emitted by `formatCoverageWarnings(coverage)`:**
  - `Coverage notice: playlistItems.list returned 80 raw rows across 2 page(s) (totalResults=80) with 4 duplicate ID(s) (clV6E10NLPw, TbMMJSRKC3U, 29bpGAI0wb8, GHZDsiH7L7A) -> 76 unique playlist IDs.`
  - `Direct videos.list recovery: 4 known HOS ID(s) omitted from playlistItems.list confirmed on channel via direct lookup: qOZgess30h0 (public), mTY67qet7cM (private), K0TQHg4XCHY (private), KIWJRl0dzjw (private).`
  - `Coverage totals: 80 audited HOS video(s) (44 public; channel statistics.videoCount=44).`
- **Known source IDs checked:** `69` repo IDs (`omittedKnownIdsChecked`: `4` — `qOZgess30h0`, `mTY67qet7cM`, `K0TQHg4XCHY`, `KIWJRl0dzjw`).
- **Recovered via direct lookup:** `4/4` confirmed on `UCXp7HkBIl1LgaznXuZHJyRg` (`1` public, `3` private unscheduled).
- **Unresolved IDs (`notReturnedByDirectLookup`):** `0` (`[]`).
- **Reconciliation totals:** `auditedTotal = 80` matches `playlistTotalResults = 80`; `auditedPublicCount = 44` matches `channelVideoCount = 44`.

## Persisted Row Verification

- `00_Brand/Channel-Setup/audits/LIVE_VIDEOS.json` contains **51 rows** (`44` public + `7` scheduled), generated directly from the live API response without forcing row counts.
- Independent verification confirmed all **51/51** persisted rows match the live API `rows` filter output 1:1 (`id`, `kind`, `title`, `privacy`, `scheduled`) with **0** duplicate IDs.
- Diff against `5f3c0a83`: only `pulledAt` (`2026-11-26T21:58:11.586Z` → `2026-11-27T03:29:47.729Z`) and the addition of the confirmed-public Short `qOZgess30h0` (*Invisible life is still everywhere*). All 50 previously persisted active rows remain unchanged and match current live API state.

## Checks Run

- `00_Brand/Channel-Setup/tools/check_all.sh` (includes durable desk handoffs, email ratchet, no media, status board, ElevenLabs guard tests, `vo_check` tests, `atempo` tests, contract tests `31/31`, and `package-lint`).
