# HOS 004 — launch plan

Rules: `HOS_STRATEGY.md` → The week.

| When (UK) | What | Promotes |
|---|---|---|
| Thu 15 Oct 18:00 | Long **What's Really Inside an Atom?** — **normal publish, no Premiere**. Private until `publishAt` 2026-10-15T17:00:00Z. Mix: `hos_004_full_v02.mp4` (**music PASS** sha `ed870939…`). Package dry-run STOP — no upload until Ben yes. | — |
| Fri 16 Oct 11:30 | Lead Short: gold coin · caption **HOW SMALL?** · ~60 words. Scripts: `10_Shorts/SHORTS_PUNCH_SCRIPTS_v02.md` | 004 (this film) |
| Sun 18 Oct 11:30 | Short: Newlands’ octaves (not empty chairs/gallium) | 002 `AL_-qlWko_g` |
| Tue 20 Oct 11:30 | Short: Bertha’s hand only (not cardboard accident) | 003 `frP_YrNShsU` |

- Each Short's Studio Related points at the film it promotes. One Short a day at most; none before the 004 long is public.
- **At 18:05 on 15 Oct:** Fri Related → 004; add 004 to playlist **How Did We Discover…? | History of Science** (001–003 already in). Full checklist: `Schedule/LAUNCH_DAY_15_OCT_1805.md`.
- **Title (Ben):** main *What's Really Inside an Atom?*; T&C *Why Is the Periodic Table in This Order?* · *How Small Can You Cut Gold?*
- **Test & Compare pairs (title + thumbnail) — Ben PASS A/B v04; C v06 for look. Nothing to Studio until upload go:**

  | # | Title | Thumbnail |
  |---|---|---|
  | **1 (main)** | What's Really Inside an Atom? | **A** `hos_004_thumb_A_atom_live_v04.jpg` |
  | 2 | Why Is the Periodic Table in This Order? | **C** `hos_004_thumb_C_hidden_number_live_v06.jpg` — painted **52**/**53** · big **Te**/**I** |
  | 3 | How Small Can You Cut Gold? | **B** `hos_004_thumb_B_cut_gold_live_v04.jpg` |

  Letters **reassigned** vs v01–v03 (A=atom, B=coin, C=Te/I). Family sheet: `hos_004_thumbs_v06_family_vs_002_live.jpg`.
- Long thumbs in `08_Thumbnail/Selected/` (A/B v04 + C v06). Index: `THUMBS_INDEX_v06.json`.
- **Package:** Ben yes to upload when dry-run clean — **blocked**: HOS `07_Content-Ops/.env` absent. No video id. See `Schedule/UPLOAD_BLOCKED_ENV_ABSENT_2026-09-29.json`. `full_v03` parked unused.
- **Content Ops env (HOS only):** `npm run youtube:package` must run under `History Of Science/07_Content-Ops/` and load **`/Users/benjaminoats/YouTube/History Of Science/07_Content-Ops/.env`**. Do **not** use `orbit-with-ben/07_Content-Ops/.env`. Do **not** print `.env`.
- **Channel split:** every 004 record, status line, deliverable, and UAT file lives in the **history-of-science** repo and **`HOS UAT/004_Whats-Really-Inside-An-Atom/`** only. Never write HOS 004 into Orbit/OWB project, agent store, schedule file, `OWB UAT`, or the orbit-with-ben repo.
- Before 15 Oct there is no new long. Weeks without one run on three back-catalogue Shorts (HOS_STRATEGY.md → The week).
- Fallback: Thu 22 Oct, same pattern moved one week.
- Gates: Ben script review → `review:script` ≥90 and `gate:episode` PASS → VO → plate-first mint by part → rough KEEPs → join → UAT → thumbs → upload.
- **Never:** Premiere · `/go/` · touch 002's package or A/B test · print `.env` · Orbit branding / links / picture rules on HOS.
