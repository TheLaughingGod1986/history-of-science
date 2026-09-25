# Merge conflict report — `main` × `cursor/history-of-science-rebrand-ab63`

Fetched `origin/main` (includes `d8f37c5` — parallel rebrand on main). Merge started; **simple conflicts resolved**; **11 files still conflicted** pending Ben’s intent call.

## Simple — resolved

| File | Resolution |
|---|---|
| TikTok CDP fill scripts (×3) | `main` — “History of Science Content Ops” |
| Brand channel-ID one-liners (`BRAND_OPTIMISATION`, `FINAL_BRAND_REFINEMENT`, `CHANNEL_BUILD_SYSTEM`) | `main` — clearer “do not use Orbit channel ID” |
| `VERIFY_RESULT.json` | **ours** — keep TBD Studio URL (main still pointed at Orbit `UC_es…`) |
| Content Ops README / layout / login titles | `main` |
| Hashtags (`seed.ts`, TikTok callback, `generate-platform-copy`) | `main` — `#Science` / `#History` not Space/Astronomy |
| `social-copy-rules.ts` | `main` — allow `*.vercel.app` |
| `ORBIT_GROWTH_PLAYBOOK` promise | `main` — discovery framing |
| `ORBIT_MONETISATION_MASTER_PLAN` primary repo | `main` — `history-of-science` |
| `ORBIT_BRAND_SNAPSHOT` handle note | `main` — “claim at create — not live yet” |
| README Growth System link line | ours (CHANNEL_READY already linked above; avoid duplicate) |

Plus clean auto-merges from `main` (affiliate docs, AppShell, package-lock, etc.).

## Complicated — still conflicted (need a decision)

### A. Brand / visual intent (cartoon-new vs Orbit-mascot)

| Ours (this PR) | `main` |
|---|---|
| Cartoon / stylised / upbeat; Orbit = **legacy seed** until new HOS character | Orbit **stays the mascot**; channel name = History of Science |
| Tagline: “Science stories. Bright questions.” / “Curious. Cartoon. Upbeat science.” | “How we discovered what we know.” / “Discovery. Wonder. Proof.” |
| About copy = cartoon-bright, no Orbit first-person | About copy = “with Orbit” / “I'm Orbit…” Pixar-warm |

**Files:** `README.md`, `CHANNEL_READY.md`, `CHANNEL_META.json`, `CHANNEL_VISION.md` (ours-only), `channel_description.txt`, `channel_keywords.txt`, `ORBIT_BRAND_SNAPSHOT.md` (wordmark/IP hunk)

Your chat direction matched **ours**. Main’s rebrand kept Orbit as mascot.

### B. Social / Meta / TikTok account wiring

| Ours | `main` |
|---|---|
| Renames Orbit’s live Meta/Threads/TikTok IDs + handles to History of Science | **Nulls** IDs; create **new** accounts; do not publish to Orbit’s Page |

**Files:** `Meta/META_ACCOUNTS.json`, `Threads/THREADS_ACCOUNTS.json`, `TikTok/TIKTOK_META.json`

`main` is safer ops-wise (avoids posting to Orbit’s portfolio by accident). Ours assumes reusing Orbit social assets under a new name.

### C. Hosting / affiliate base URL

| Ours | `main` |
|---|---|
| Keep `https://orbit-content-ops.vercel.app` | New host `history-of-science-content-ops.vercel.app` / localhost for `.env.example` |

**Files:** `.cursor/rules/orbit-affiliate-named-in-film.mdc`, `07_Content-Ops/.env.example`

## Status

Merge **in progress** on `cursor/history-of-science-rebrand-ab63` with conflict markers left in the 11 complicated files. No merge commit until A/B/C are decided.
