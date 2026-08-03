# Social match to YouTube — 2026-08-03

## Source of truth

YouTube originally showed **6** public Shorts. Two were obsolete v01 duplicates and were privatized so socials mirror the current product set:

| YouTube ID | Short | Visibility |
|---|---|---|
| `1HuV8o3gOss` | Where Is Everybody? (v02) | **public** |
| `dPMJQp2gMNc` | Space Is Rude About Distance (v02) | **public** |
| `rFJoOdQAc9c` | What If Aliens Are Watching Us? (v02) | **public** |
| `KcKBixwmcV4` | First Alien Clue (v02) | **public** |
| `UWwNKYf_aU8` | old distance v01 | **private** |
| `MO19iXYCu0c` | old watching v01 | **private** |

**Target for socials = 4** (match current public YouTube).

## Live matrix

| Platform | Count | Match? | Notes |
|---|---:|---|---|
| YouTube | 4 | ✓ | Old v01s privatized |
| Instagram | 4 | ✓ | `Dbk9zWSyCE_`, `Dbk984KygUG_`, `Dbk-HKtSMx_`, `Dbk4wQMAkLM` |
| Facebook Page | 4 | ✓ | Page reels tab shows all four |
| Threads | 2 | ✗ | Watching + Clue exist as **YouTube link cards**, not native videos. Everybody + Distance video uploads reach “Posting…” then vanish / fail server-side |
| TikTok | 3 | ✗ | Everybody / Distance / Watching live. Clue blocked by Studio `check_limit` / temporary posting restriction (`status_code: 21`) |

## Blockers

1. **Threads native video** — composer can attach video (including re-encoded ~2–4 MB 720p files) and shows Post enabled / “Posting…”, but posts do not appear on `@orbitwithben`. Link-only posts with `youtu.be` unfurl do publish. IG “Share → Threads” only opens a text intent to the IG URL (no embedded reel video).
2. **TikTok Clue** — Studio upload reaches the form; Post returns content-check / community-guideline temporary block. Retry after the ban window (ledger: `TIKTOK_POSTED.json` → `platform_block`).

## Next actions

1. When TikTok ban lifts: post `aliens_short-04_hidden-clues_v02.mp4` via `TikTok/auto/studio_upload.py` (disable Content check lite).
2. Threads: retry native video later, or obtain Threads API token (`THREADS_CREDENTIALS.json` currently empty) and publish via Graph. Prefer captions **without** raw `youtu.be` URLs so media is not replaced by a link card.
3. Optional cleanup: delete Threads link-card posts for Watching / Clue once native video versions land.
