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

## 30 October 2026 — J1265 Long description Chapters + Sources block (Chief h13 on J1261, £0, Gemini covering)

- **Authority:** Chief (Grok) ruling `h13` on `J1261` (30 Oct 2026, HOS `#180` re `6521114044`) and queue job `J1265`. Records only, `£0`, no YouTube/Studio change, no upload.
- **Provisional chapters status:** **re-verify chapters against the locked master at picture lock** (any later trim moves stamps; the picture-lock job must re-check them).
- **Chapters added to `11_Upload-Package/Descriptions/lightning_long_description_v01.txt` from Chief-reviewed rough `v08` (`hos_008_rough_v08.mp4`, master `sha256: c1f952a714c8758f66bf284b578873a449eb9bdecdff1782672983834be4d382`, `539.626 s`, `cuts_rough_v08.json`):**

| Stamp | Chapter title | VO part (`02_Voiceover/`) | `cuts_rough_v08.json` first row & `timeline_in` (24 fps frame) | First VO word onset in `v08` (`c1f952a7`) |
|---|---|---|---|---|
| `0:00` | `Fire from the sky` | `part01_fire_from_the_sky` (`hos_008_part01_fire_from_the_sky_v01b.mp3`) | `01_kite_open` · `0.0000 s` (frame `0`) | `"In"` at `0.050 s` (`0:00.05`, frame `1`) |
| `1:40` | `The sparks in a jar` | `part02_the_sparks_in_a_jar` (`hos_008_part02_the_sparks_in_a_jar_v01.mp3`) | `01_salon_tube` · `100.2510 s` (`1:40.25`, frame `2406`) | `"In"` at `100.5665 s` (`1:40.57`, frame `2414`) |
| `3:08` | `A kite in the storm` | `part03_a_kite_in_the_storm` (`hos_008_part03_a_kite_in_the_storm_v01.mp3`) | `01_points_desk` · `187.9520 s` (`3:07.95`, frame `4511`) | `"Franklin"` at `188.5227 s` (`3:08.52`, frame `4525`) |
| `5:19` | `The spark from the key` | `part04_the_spark_from_the_key` (`hos_008_part04_the_spark_from_the_key_v01.mp3`) | `01_knuckle_close` · `319.0037 s` (`5:19.00`, frame `7656`) | `"Slowly"` at `319.7680 s` (`5:19.77`, frame `7674`) |
| `6:49` | `The rod on every roof` | `part05_the_rod_on_every_roof` (`hos_008_part05_the_rod_on_every_roof_v01b.mp3`) | `01_house_rod` · `408.9640 s` (`6:48.96`, frame `9815`) | `"In"` at `409.9576 s` (`6:49.96`, frame `9839`) |

- **Sources block added under `Chapters` (7 plain citations from `01_Script/FACT_NOTES_v01.md` source column only; Founders Online / *Poor Richard Improved* (1753) cited for almanac wording, not NOAA):**
  - `Benjamin Franklin, Pennsylvania Gazette (19 October 1752)`
  - `Benjamin Franklin, Poor Richard Improved (1753), Founders Online`
  - `Benjamin Franklin, Experiments and Observations on Electricity (London, 1751)`
  - `Benjamin Franklin, Autobiography, Founders Online`
  - `Joseph Priestley, The History and Present State of Electricity (1767)`
  - `E. Philip Krider, "Benjamin Franklin and Lightning Rods", Physics Today (2006)`
  - `NOAA / National Weather Service, "Lightning Myths and Facts"`
- **Rest of description (`lightning_long_description_v01.txt`) and `PACKAGE_MANIFEST.json`:** opener, bullet list, `Watch next:` links, and sign-off kept byte-identical to `#383`; `PACKAGE_MANIFEST.json` `chaptersFile` left `null` (no `Chapters/` file for `008`).
- **Repository check output (`00_Brand/Channel-Setup/tools/check_all.sh 02_Video-Projects/008_Lightning-Franklin`):**
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
- **Package lint on `main` and against PR `#387` (`origin/gemini/j1259-release-gate-chapters-sources` @ `592eaae7`, `checkChaptersAndSources`):**
```text
> content-ops@0.1.0 lint:package
> tsx scripts/package-lint.ts --film 008

PASS  02_Video-Projects/008_Lightning-Franklin/11_Upload-Package/PACKAGE_MANIFEST.json
   warn  [captions] no captionsFile (captions from the script)
```





## J1273 tracked-rod preflight — 30 Oct 2026, Codex worker

Candidate only, parked for Chief; no film/stage PASS. Evidence: `07_Edit-Project/_desk/008/J1273_tracked_preflight/REVIEW.md`. Durable media: `/Users/benjaminoats/_desk/j1273-candidate-v08/`. Alpha/composite 42 frames, 24 fps; source 109–150 exactly. Five required offsets: -4.5/-11/+3.5/+0.5/+1.5 px, limit 19.2 px. Retained source-hand/bracket occlusion and picture warning need Chief review.

Unmodified row tool output:
```
polish gate PASS: 0 of 1 rows failed, 0 to look at
picture QA PASS: 0 of 1 cuts fail, 1 to look at
WARN: kind of picture: no title in the pool, so nobody can tell what it is
```

J1267 remains held at 2/6; only Chief acceptance can resume it. No master splice, stage approval, spend, music, upload or Ben watch. Delivery code now uses verified copies and refuses conflicts instead of deleting folders.


## 3 November 2026 — J1868 Franklin v03 UAT triage (Codex acting Chief)

Live review confirmed six original notes at 2026-11-03T16:08:33.439Z. Exact notes and correction criteria: `07_Edit-Project/J1868_UAT_CORRECTIONS.md`; original JSON preserved beside it. J1880 owns no-spend source mapping and edit recipe; J1881 follows J1880 to review and scope correction assembly/media QA. Six notes remain unresolved. Historical h22/h35 approvals are retained, with no invented completion of undocumented stages. J1755 and open PR401 remain separate delivery work; its automatic-publication rejection stays intact. No media, credit, upload, scheduling or YouTube changes.

Repository validation (record-only; not corrected-media approval):

```text
-- durable desk handoffs: PASS
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


## J1881 — 4 November 2026

Recipe scope review: FIX, production held. J2163 queued to repair timing/preservation, truthful verification and teaching labels; J1881 resumes on that input. See `07_Edit-Project/J1881_SCOPE_REVIEW.md`. No media PASS, six notes unresolved, J1755 delivery hold separate.

Validation of review records (not media): `bash 00_Brand/Channel-Setup/tools/check_all.sh` output: **ALL CHECKS PASS**. `git diff --check` passed.



## 5 November 2026 — J2170 Short C paper hook resolution & conditional 2 Dec slot preflight (Gemini worker)

`£0` preparation only (`0` credits spent, no VO recording, no Flow/Vertex generation, no media modification, no upload/schedule/privacy/retitle or Buffer writes). Original `10_Shorts/SHORTS_SCRIPTS_v02.md`, `10_Shorts/SHORTS_PICTURE_PLAN_v02.json`, `10_Shorts/vo_v02/*`, and `J1004` / `J1273` / `J1868` / `J1881` / `J2163` rulings preserved unmodified.

- **Deliverables:**
  - `10_Shorts/J2170/SHORT_C_PAPER_PLAN.md`: complete paper plan, timing proof, source-checked 1-sentence hook options, whole-sentence re-indexing of unmodified `hos_008_short_C_v02.wav` (`w[13..61]`), and 8-cut approved Flow Veo plate mapping (`J1881`/`J2163` six-note overlap = 0).
  - `10_Shorts/J2170/INPUT_INVENTORY.json`: 47 verified local/NAS input rows with exact SHA-256 hashes (`all_rows_exist: true`).
- **Conditional 2 Dec 11:30Z slot status (`Ben watch by 29 Nov`):** **EXPLICITLY NOT ACHIEVABLE on existing audio alone; slot remains EMPTY / HELD.**
  - Re-confirmed `J1004` proof: `hos_008_short_C_v02.mp3` (`ba8ffec96f137ce14b71a192a49461a3c0332b010dfde5e4ddfb96985e5cf758`) Sentence 1 (`w[00..12]`, 13 words: *"That thin metal rod on top of tall buildings was Benjamin Franklin's idea."*) ends at `4.840 s` (`3.720 s` pure speech at `1.00x`, `3.509 s > 2.85 s` at `1.06x` cap with zero inter-word gaps). Excising `w[04..08]` (*"on top of tall buildings"*) leaves `3.240 s > 2.85 s` at `1.00x` and violates the `AGENTS.md` Never list.
  - Re-confirmed `02_Voiceover/hos_008_part05_the_rod_on_every_roof_v01b.mp3` (`e5e86140174f30164b9fd4856e982b0c2bfbb05b6d8858bf8d5c9bc491b4a6ae`): no contiguous `22–27 s` lightning-rod mechanism passage starts with a `<= 2.85 s` hook sentence naming both subject and surprise claim.
- **Paper hook resolution & source check (`01_Script/FACT_NOTES_v01.md` rows 25, 38, 39, 41, 42, 44):**
  - Primary 1-sentence pickup `C-Open-1` (7 words, 47 chars, 10 syllables): **`"That rooftop lightning rod was Franklin's idea."`** (est. `2.35–2.55 s <= 2.85 s` at `speed=1.04`, `1.00x`).
  - Alternative `C-Open-2` (6 words, 45 chars, 10 syllables): **`"Benjamin Franklin invented the lightning rod."`** (est. `2.15–2.35 s <= 2.85 s`).
  - Paired with unchanged `hos_008_short_C_v02.wav` (`0a25b6dab2ca193e9549c2463d5c03c05348b0e2eb2d28258749db3fbeb99f77`) slice `w[13..61]` (`5.720–24.400 s`, 49 words, `18.680 s`), total spoken words = `55–56` (`55–65` lock PASS) and total runtime = **`~22.35 s`** (`21.35 s` VO + `1.00 s` loop tail, `22–27 s` lock PASS). Both original sentence order (`Layout C-v03a`, scale payoff `w[52..61]` at `82.3% >= 70%`) and whole-sentence reordered `Layout C-v03b` (`w[52..61]` moved whole to `S02` so mechanism answer `w[40..51]` starts at `76.1% >= 70%`) are specified.
- **Plate inventory vs `J1881` / `J2163` six-note corrections:**
  - All 6 `J1881`/`J2163` UAT notes (`00:20` `P1:03_table_three`, `0:30` `P1:03b_town_safe -> P1:04_storm_mystery`, `1:49` `P2:02_salon_spark`, `2:20` `P2:07_foil_jar`, `3:31` `P3:04_letter_crosses`, `7:58` `P5:13_rods_spread`) are disjoint from `Short_C`. Defective `P5:13_rods_spread` (`d9fa5f13...`) is explicitly excluded.
  - `SHORTS_PICTURE_PLAN_v02.json` used 4 pre-labelled code graphics (`P5:08..P5:11`) that collide with the `9.0–14.0 s` promoted long title banner and violate the HOS Shorts 1-overlay cap, plus `P5:10` (`J1273` `composite_v08.mp4`, 42 clean frames / `1.75 s`) remains parked for Chief. Replaced on paper with 8 verified `J1191` KEEP moving Flow Veo plates (`P5:19_skyline_strike`, `P5:01_house_rod`, `P5:07_giant_spark`, `P1:12_steeple_fire`, `P5:18_rod_closeup`, `P5:06_rod_fitting_c1`, `P5:06_rod_fitting`, `P5:14_safe_towers`).
  - `Short_A` (`J0912`, target 24 Nov / watch 20 Nov) remains completely separate and untouched.
  - Separate bounded decision/pickup job queued for Chief/Claude (`J2023` does not authorize credit spend).

Repository check output (`bash 00_Brand/Channel-Setup/tools/check_all.sh 02_Video-Projects/008_Lightning-Franklin`):
```text
-- durable desk handoffs: PASS
-- no media: PASS
-- status board in sync: PASS
-- ElevenLabs guard tests: PASS
-- vo_check word tests: PASS
-- atempo check tests: PASS
-- voice speed (atempo <= 1.06): PASS
-- contract tests: PASS
-- package-lint: PASS
-- review:script lightning_script_master_v01.md: PASS
-- gate:episode: PASS
ALL CHECKS PASS
```
