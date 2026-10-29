# Production status — 008 Lightning (Franklin)

| Field | Value |
|---|---|
| Slug | `008_Lightning-Franklin` |
| Channel | `@HistoryOfScienceYT` only |
| Topic | **Lightning** — Franklin's kite (June 1752 tradition) + lightning rod / pointed conductors (1750 proposal; French verification May 1752; Philadelphia how-to Oct 1752) |
| Stage | **FACT_NOTES sourced** (4 Oct 2026). Script master on main (PR #203 merged). FACT_NOTES_v01 covers every new-claims row (Claude 5982184384). |
| Neighbour gate | **PASS** (4 Oct 2026): 6 education ≥1M; TED-Ed yes. Evidence `11_Upload-Package/evidence_2026-10-04_neighbours.json` |
| Script review | script on main (`lightning_script_master_v01.md`); review 92.1 PASS; FACT_NOTES confirmed by Claude |
| Episode gate | **PASS** (4 Oct 2026) |
| VO | **allowed** (Claude confirmed FACT_NOTES 4 Oct 2026; Fischer line softened) |
| Picture | **All 101/101 Flow rows of boards v03 minted and KEEP (J1191, 29 Oct 2026):** 6/6 priority overlay moving plates (`P2:12`, `P3:07`, `P2:08`, `P4:02`, `P1:16`, `P5:06`) minted first · P1 22/22 · P2 17/17 · P3 25/25 · P4 16/16 · P5 21/21 = **101/101 Flow rows** (15 Quality + 86 Fast = **2,320 cr** vs 5,605 expected / 6,500 cap; live Flow `20,870 → 18,550 >= 3,000` buffer) + 11 £0 code graphics (`J0329`) = **112/112 rows**. Synced to NAS (`/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/`). Parked for Chief picture PASS. |
| Runtime target | 7–9 min, 5 parts (house default) |
| Air | TBD after 007 calendar |
| Shorts | not outlined yet |

## STOP

- No Vertex/Veo/Flow minting on this film.
- No ElevenLabs VO until Claude confirms sourced FACT_NOTES + script.
- Do not merge or close desk PR #180 or #202 from this work.


## 16 October 2026 — J0329 code graphics (codex)

Eleven v01 code graphics rendered from the Chief-kept v03 boards; five moving-plate rows also have alpha MOVs and provisional paper MP4 previews. See `07_Edit-Project/CODE_GRAPHICS_v01_REVIEW.md` for paths, timing manifest, technical checks and review limitations. No stage PASS or final OK issued. Picture remains blocked for Chief review and the unchanged mint gate.

Repository check output (automated checks only):
```text
-- no media: PASS
-- status board in sync: PASS
-- ElevenLabs guard tests: PASS
-- vo_check word tests: PASS
-- contract tests: PASS
-- package-lint: PASS
ALL CHECKS PASS
```

Full decode, 1080p/30fps and native alpha checks succeeded for all eleven rows. Review includes the seven-word P5:11 label against the four-word rule and schematic Atlantic geometry. No Flow/Vertex/ElevenLabs spend, YouTube changes or deletion.

NAS mirror pending: detached session `j0329-mirror-v2` is blocked in filesystem mkdir. No verified NAS copy yet; all local outputs retained. Resume from its log and exit marker listed in the review note.

## 24 October 2026 — J0909 (`J0899` Change 3): Pause-trim notes (`0:15–0:45` & `1:00–2:30`), 5 moving-plate overlay composite note & end-screen/description links to `GHZDsiH7L7A` + `AL_-qlWko_g` (Gemini covering)

- **Authority:** Chief PASS on `J0899` (`02_Video-Projects/_analytics/HOS_2026-10-24.md` §4 #3) and queue job `J0909`. `£0` spend, no live YouTube changes.
- **Applied to `11_Upload-Package/` and `07_Edit-Project/SHOT_LIST_v01.md`:**
  1. **Inter-sentence pause-trim notes (`0:15–0:45` and `1:00–2:30`) + 5 moving-plate alpha overlays (`J0329`):** Recorded in `07_Edit-Project/SHOT_LIST_v01.md`, `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`, `11_Upload-Package/LAUNCH_PLAN.md`, and `11_Upload-Package/PACKAGE_MANIFEST.json` (`note`) to address `004`'s `51%→30%` and `002`'s `45%→23%` early retention drops and composite the 5 `J0329` alpha overlays once `J0329` passes.
  2. **Links to `004` (`GHZDsiH7L7A`) + `002` (`AL_-qlWko_g`):** Set `"relatedVideoId": "GHZDsiH7L7A"` in `PACKAGE_MANIFEST.json`, added `Watch next:` links (`https://youtu.be/GHZDsiH7L7A` and `https://youtu.be/AL_-qlWko_g`) in `Descriptions/lightning_long_description_v01.txt`, and documented the end-screen pairing (`GHZDsiH7L7A` + `AL_-qlWko_g` + Subscribe) in `LAUNCH_PLAN.md`.
- **Package lint (`npm run lint:package -- --film 008`):** `PASS  02_Video-Projects/008_Lightning-Franklin/11_Upload-Package/PACKAGE_MANIFEST.json`.

## 29 October 2026 — J1191 Flow v03 minting complete (101/101 rows KEEP, £0, Gemini covering)

- **Authority:** Acting Chief (Claude) price pass `J0863` PASS and queue job `J1191`.
- **Flow balance & spend gate:** Live Flow read before session `20,870` (`ai_spend.py` logged before and after every batch). All 101 Flow rows of `PICTURE_PLAN_v03.json` (15 Quality @ 100 cr + 86 Fast @ 10 cr) minted in 1st-try I2V from Nano Banana 2 16:9 start stills (`0 cr` per still, one un-charged retry on `12_notebook_list` and 50 cr UI re-sync between batches; total UI balance drop `20,870 → 18,550` = `2,320` credits vs `5,605` expected / `6,500` cap, leaving `18,550 >= 3,000` buffer).
- **Priority overlay moving plates minted first (6/6 KEEP):**
  - `P2:12_notebook_list` (`sha256: 35164fd4319c...`, 8.0 s, 0 freeze events)
  - `P3:07_slow_news` (`sha256: 775e6d72eeb9...`, 8.0 s, 0 freeze events)
  - `P2:08_jar_spark` (`sha256: 6a24bb548744...`, 8.0 s, 0 freeze events)
  - `P4:02_knuckle_spark` (`sha256: a4328f1bd850...`, 8.0 s, 0 freeze events)
  - `P1:16_question_sky` (`sha256: ab8b5da574dc...`, 8.0 s, 0 freeze events)
  - `P5:06_rod_fitting` (`sha256: d55e01ab2879...`, 8.0 s, 0 freeze events)
- **All 5 parts complete (101/101 Flow rows KEEP + 11 £0 code graphics from J0329 = 112/112 board rows):**
  - Part 01: `22/22` Flow rows KEEP (+ 2 code graphics = 24 rows)
  - Part 02: `17/17` Flow rows KEEP (+ 2 code graphics = 19 rows)
  - Part 03: `25/25` Flow rows KEEP (+ 1 code graphic = 26 rows)
  - Part 04: `16/16` Flow rows KEEP (+ 2 code graphics = 18 rows)
  - Part 05: `21/21` Flow rows KEEP (+ 4 code graphics = 25 rows)
- **Evidence & NAS backup (copy only):**
  - Full take ledger, SHA-256s, UAT notes, motion checks (`freeze_events_0p8s: 0` across all 101 clips), and balance reads recorded in `07_Edit-Project/FLOW_MINT_LOG_v03.json`.
  - Local clips, start stills, and UAT contact sheets in `/Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin/04_Generated-Clips/` (including composite part sheets `uat_summary/PART01..05_ALL_*_REVIEW_SHEETS.jpg`) copied to NAS `/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/04_Generated-Clips/` and `07_Edit-Project/FLOW_MINT_LOG_v03.json`.
- **Status:** Parked for Chief `picture` PASS (`J1191`). No upload, no ElevenLabs, £0.
- **Repository check output (`check_all.sh 02_Video-Projects/008_Lightning-Franklin`):**
```text
-- no media: PASS
-- status board in sync: PASS
-- ElevenLabs guard tests: PASS
-- vo_check word tests: PASS
-- contract tests: PASS
-- package-lint: PASS
-- review:script lightning_script_master_v01.md: PASS
-- gate:episode: PASS
ALL CHECKS PASS
```


