# HOS 137 — `v02` Fix Verification & Acting Chief `KEEP` / Script Lock Ruling (`J3687`)

- **Job:** `J3687` (`kind: review`, ref `J3565`)
- **Acting Chief:** `gemini` (elected Acting Chief under `Claude -> Codex -> Gemini -> Grok` per Ben's 24 Nov 2026 order; verified via live `chief_relay.py status` = `Chief: Gemini` at `08:40Z` and `08:43Z`; `claude` down until `12:50Z`, `codex` down on usage limit until Nov 27)
- **Date:** `2026-11-25` (UTC)
- **Film:** `HOS:137` — *Accidental Inventions: 5 Mistakes That Worked* (Cluster 3 Film 3, target air Thu 24 Dec 2026 18:00 London; Ben's watch Mon 21 Dec; script lock due Tue 8 Dec)
- **Audited PRs:**
  - HOS PR `#772` (`macbook/J3685`, head `be99dffe0e4b5f6441604c6de2a0008c126d09fc`) — `v02` script, `SOURCES.md`, `FACT_NOTES_v02.md`, `SHORTS_SCRIPTS_v02.md`, `LAUNCH_PLAN.md`, `production-status.md`, `status.json`
  - HOS PR `#775` (`gemini/J3686-hos137-facts-v02`, head `b7871857e390bdc5c93708aa8c699210a246c99d`, stacked cleanly on PR `#772`, `MERGEABLE`, `7/7` GitHub CI checks green) — independent `v02` facts audit (`01_Script/GEMINI_FACTS_CHECK_v02.md`: `18 OK / 10 PARTIAL / 0 FLAG`)
- **Ruling:** **`KEEP` & SCRIPT LOCKED**
- **Protected Actions Executed by Elected Acting Chief (`gemini`):**
  - Merged HOS PR `#775` into `main` as **`b4622600888c536da1cc894344daca30a4eae4b2`** (automatically merging/superseding stacked PRs `#747`, `#754`, `#769`, and `#772`, all verified `MERGED`).
  - Recorded this `jobs/reviews/J3687/REVIEW.md` and locked `status.json` (`script`: `done`, `facts`: `done`, `shorts_scripts`: `done`) + `production-status.md` via clean PR to HOS `main`.
  - Closed parent **`J3565`** as `done` in `orbit-with-ben/jobs/QUEUE.json` (script lock achieved).
  - **Rule G WIP Guard (`orbit-with-ben/jobs/WIP.json` checked `2026-11-25`):** HOS currently occupies **5 of 5** active WIP places (`HOS:009`, `HOS:010`, `HOS:013`, `HOS:128`, `HOS:136`). Therefore `HOS:137` long VO and Shorts `S01`/`S02` VO are **NOT queued yet** and remain cleanly held (`vo: todo`, `shorts_vo: todo`) pending an open HOS WIP slot release (once `HOS:009` clears Ben's watch / schedules).
  - **Spend / Scheduling:** **£0.00 / 0 credits spent**; nothing uploaded, scheduled, or altered on YouTube.
  - **Schedule & contingency preserved:** Tue 8 Dec lock achieved 13 days early; Mon 21 Dec Ben watch and Thu 24 Dec 2026 18:00 London target air preserved (normal publish, no Premiere; Shorts `S02` Fri 25 Dec & `S01` Sat 26 Dec 11:30 London; standing 1-week slip contingency if not ready).
  - **Packaging caveat preserved:** Confirmed working direction only — draft thumbnail concepts (`NEARLY TRASHED`, `WRONG RESISTOR`, §2.6 hand-verified ink, plus 3rd T&C variant post-VO per §2.9) remain **unrendered drafts (NOT rendered packaging PASS)**; picture and rendered thumbnails wait for Chief VO PASS.

---

## 1. Exact Locked `v02` SHA-256 Hashes (Independently Verified on `b7871857` / Merged `b4622600`)

Confirmed byte-for-byte that PR `#775` (`J3686`) did not modify any of the four core `v02` deliverables from PR `#772` (`J3685`):

```text
d2a359c4cb30b707b9ac723693372c6faba1d65ca1d32d8241a2b9a3c25caecb  02_Video-Projects/137_Accidental-Inventions-That-Changed-The-World/01_Script/accidental_inventions_script_master_v02.md
bc755590b3f7df7894f03fc2a202f60b92641aac9bc657107771e65d8bfbdb0c  02_Video-Projects/137_Accidental-Inventions-That-Changed-The-World/01_Script/SOURCES.md
7f5020911bbc8dd5e2f9c2911095c8fd7657ef8b029575fb071e1bcccc6df4b4  02_Video-Projects/137_Accidental-Inventions-That-Changed-The-World/01_Script/FACT_NOTES_v02.md
1fd7a797be0ae74292f9c00e753800c61d2fac40b1689dbb486827e60ddd01da  02_Video-Projects/137_Accidental-Inventions-That-Changed-The-World/01_Script/GEMINI_FACTS_CHECK_v02.md
62ff7c99d88c0416f0b6a23191b8fb60e1915776c91fc67e2d5fb67163f0da94  02_Video-Projects/137_Accidental-Inventions-That-Changed-The-World/10_Shorts/SHORTS_SCRIPTS_v02.md
da131a4346bb9c05bc545a347b5053c32f3ba7350dc7ff3e914c42aa35296de8  02_Video-Projects/137_Accidental-Inventions-That-Changed-The-World/11_Upload-Package/PACKAGE_FIRST_SCORING_v01.md
e7c89ba2d19dc6c45096cbaec4b1c2c4d385ca0c361c3cc6d9c1d0e0cc58bf13  02_Video-Projects/137_Accidental-Inventions-That-Changed-The-World/11_Upload-Package/LAUNCH_PLAN.md
d84b917ec0a4106253dd4ba31afa68c6a4176a6b5d8eb77e241018af3a60cbf9  02_Video-Projects/137_Accidental-Inventions-That-Changed-The-World/11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md
```

---

## 2. Independent Verification Matrix — All 9 `J3565` Blocking Fixes (`FIX-1`–`FIX-9`)

| Fix | Requirement (`J3565` PR `#770`) | Independent Chief Verification (`2026-11-25`, direct live checks on `v02`) | Status |
|---|---|---|---|
| **`FIX-1`** | Bénédictus `FR 405,881` filing date (`1909-08-10`, not Nov 1909); add `FR405881A` to `SOURCES.md` & `FACT_NOTES` | Part 03 line 85 speaks *"filed his French patent in August nineteen oh-nine"* (zero occurrences of `"November nineteen oh-nine"`). Direct live `HTTP 200` on `https://patents.google.com/patent/FR405881A/en` confirmed `1909-08-10`, `1910-01-15`, `Benedictus`. Present in `SOURCES.md` & `FACT_NOTES_v02.md`. | **PASS** |
| **`FIX-2`** | Chardack-Greatbatch 1960 two-stage implant (`June 1960`) & `two years` survival | Part 01 line 34 speaks *"in June nineteen sixty, Chardack and Gage completed the implant ... in a human patient who lived another two years"*; visual line 31 reads `Buffalo June 1960` (`April nineteen sixty` & `eighteen months` absent). Direct live `HTTP 200` on both `PMC3232561` (`June 1960`, `2 years`) and `department.va.gov` (`two years`); secondary Wikipedia variance documented in Row 7. | **PASS** |
| **`FIX-3`** | Remove dead `HTTP 521` `heartrhythm.com`, merge 8 primary upgrades, add 4 lifespan quotes (Chardack, Gage, Elmqvist, Senning), remove un-upheld v01 tally | `https://heartrhythm.com` absent from `SOURCES.md` & `FACT_NOTES_v02.md`; replaced with `PMC3232561` (`HTTP 200`). All 8 primary upgrades verified live (`FR405881A`, `PMC3232561`, `PMC5403050`, `US3633A`, NobelPrize.org Fleming/Florey/Chain/1945, NIHF Fry & Spencer, `US2495429A` all direct `HTTP 200`; 3M Post-it `"Boise Blitz"` / `"Ninety percent"` / `"Press 'n Peel"` verified via `J3686` `HTTP 200` + live search grounding on `post-it.com`/`3m.co.uk`). All 4 lifespan quotes verified live: Chardack `1914–2006` (`pesthaus.at` PDF p. 2 `HTTP 200` + Crossref DOI `10.1016/j.hrthm.2006.06.018` `HTTP 200`), Gage `1922–2024` (`amigone.com` `HTTP 200`), Elmqvist `1906–1996` & Senning `1915–2000` (Wikipedia `HTTP 200`). Un-upheld v01 tally removed. | **PASS** |
| **`FIX-4`** | Microsphere chemistry: replace `"low-tack"` with `"low-adhesion, pressure-sensitive adhesive"` matching `US3691140A` & NIHF | Part 05 line 122 speaks *"low-adhesion, pressure-sensitive adhesive"* (`"low-tack"` absent from script). Direct live `HTTP 200` on `US3691140A` (`"inherently tacky"`, `"low degree of adhesion"`) and NIHF Spencer Silver (`"high level of tack but a low degree of adhesion"`). | **PASS** |
| **`FIX-5`** | Part 01 opening milestones (`≤0:15` promise, `≤0:25` stakes, `0:25–0:40` `DATA+SCALE`, `<0:45` first fact) & replace `"camera flash"` | Programmatically measured at `150 wpm` (`2.5 w/s`): L05 (`14w`) `0:00.0–0:05.6` (`≤0:08` title question); L09 (`21w`) `0:05.6–0:14.0` (`≤0:15` promise); L13 (`18w`) `0:14.0–0:21.2` (`≤0:25` stakes); L17 (`36w`) `0:21.2–0:35.6` (Greatbatch 1956 `100×` error & early `DATA+SCALE` inside `0:25–0:40`, first real fact `<0:45`). `"camera flash"` absent; replaced by *"less than two thousandths of a second, a tiny fraction of a blink"* verified live `HTTP 200` at Harvard BioNumbers `BNID 100706` (`0.1-0.4 sec`) & `PMC4043155` (`70 to 215 ms`). | **PASS** |
| **`FIX-6`** | Speak Part 02 `270°F` / boiling water `DATA`+`SCALE`; align Part 05 & `S02` on Boise Blitz `90%`; remove secondary-only `"aerospace"` | Part 02 line 59 speaks *"two hundred and seventy degrees Fahrenheit, about one hundred and thirty-two Celsius, hotter than boiling water"*, verified live `HTTP 200` in primary `US3633A` (`270` Fahrenheit). Long Part 05 line 130 (`"Ninety percent ... nine out of every ten offices"`) and Short `S02` Row 4 (`"ninety percent wanted to buy more"`) aligned cleanly. `"aerospace"` absent from Long script and Short spoken lines. | **PASS** |
| **`FIX-7`** | Cap Part 03 `FACT:` card at `≤4` words | Part 03 line 80 updated to `FACT: Used in gas masks` (`4w`). Programmatic audit across full `v02` script confirms **100% `≤4` words**: `13/13 WHO` roles (`2–4w`, year-accurate), `4/4 FACT` cards (`3–4w`), and `18/18 LABEL` cards (`2–4w`). | **PASS** |
| **`FIX-8`** | Shorts `S01`/`S02` realistic `~150 wpm` row pacing (`16.0–19.0 s`), `≤4w` synced overlays clear of `0–2 s` & `9–14 s`, R7 loop cleanliness | Programmatic row audit on `SHORTS_SCRIPTS_v02.md`: `S01` (`42` spoken words = `16.8 s` + `0.4 s` = `17.2 s`; rows `150.0 / 150.0 / 150.0 / 150.0 / 131.2 wpm`; overlay `1.8 MS PULSE` `3w` at `6.0–8.8 s`); `S02` (`40` ws / `42` hyphen-split spoken words = `17.2 s`; rows `128.6–150.0 wpm` ws / `150.0 wpm` hyphen-split; overlay `1974 CHOIR BOOKMARK` `3w` at `5.6–8.8 s`). Both clear of `0–2 s` & `9–14 s`; R7 exact live title (*Accidental Inventions: 5 Mistakes That Worked*) specified cleanly at `9.0–14.0 s` banner + `14.0–16.9 s` lower-third tag fading at `16.9 s` ahead of `≤0.3 s` Frame-0 match-cut loop. | **PASS** |
| **`FIX-9`** | Single `v02` master filename in `01_Script/` & template-stub hygiene | `01_Script/` contains ONLY `accidental_inventions_script_master_v02.md` (`v01` removed); default `npm run gate:episode` (no `--script`) resolves `v02` and PASSes; `production-status.md` explicitly lists `part-01_plates_v01.json` as an unfilled `_template` stub starting post-VO. | **PASS** |

*Non-blocking `J3686` notes acknowledged (`10` explicitly labelled secondary Wikipedia dependencies / historical nuances in `GEMINI_FACTS_CHECK_v02.md`, plus minor Row 21 title+abstract string merge and OCR spelling quirks on 1844/1914 patents) — zero factual or spoken defects.*

---

## 3. Confirmed Packaging Working Direction (Unrendered Drafts Only)

- **Primary Title (Arm A):** `Accidental Inventions: 5 Mistakes That Worked` (`45c ≤ 50`, `0` exact collisions in `evidence_2026-11-24_public_search.json`). Confirmed manifest neighbour phrase `"inventions"` per `THUMBNAIL_AND_TITLE_RULES.md` §1.3 (while T&C Arms B/C and description line 1 also carry `"that changed the world"`).
- **T&C Arm B (Plan Title):** `Accidental Inventions That Changed the World (5 Mistakes That Worked)` (`69c ≤ 70`, `0` collisions).
- **T&C Arm C (Backup):** `Accidental Inventions: 5 Mistakes That Changed the World` (`56c`, `0` collisions).
- **Neighbours:** `evidence_2026-11-24_neighbours.json` `gate = PASS`, `bigCount = 4` (`3` strictly on-topic `≥1M` after excluding off-topic AI video + `SciShow` `1.48M`), `hasTed = True`, `failedQueries = []`. Low-RPM `"history of inventions"` (`PK 25%`) excluded.
- **Draft Thumbnails (Unrendered Drafts — NOT rendered packaging PASS):** Concept A (`NEARLY TRASHED`, gold on `TRASHED`) & Concept B (`WRONG RESISTOR`, gold on `WRONG`, §2.6 hand-verified resistor/oscilloscope ink). 3rd T&C variant (`§2.9`), `style_sheet.py`, `thumb_preview.py` (`168×94`), and HOOK/BAND/PHONE scoring wait until after Chief VO PASS.
- **Shorts Titles (Test B, `0` collisions):** `S01` *How Did One Wrong Resistor Invent the Pacemaker?* (`48c`, Sat 26 Dec 11:30 London) & `S02` *How Did Failed Glue Accidentally Invent Post-it Notes?* (`54c`, Fri 25 Dec 11:30 London).

---

## 4. Fresh Independent Gate Outputs (`b7871857` / Merged `b4622600`, `2026-11-25`)

- **Direct live HTTP exact-quote checks:** `35/36` URLs returned direct `HTTP 200` with exact quoted text verified in this session (`32/33` primary/secondary HTML pages + `FR Wikipedia` `HTTP 200` + `pesthaus.at` PDF p. 2 `HTTP 200` with `"William Chardack (1914–2006)"` + Crossref DOI `10.1016/j.hrthm.2006.06.018` `HTTP 200`); `post-it.com` returned Akamai `HTTP 403` to CLI curl and was verified via live web search grounding on `post-it.com`/`3m.co.uk` alongside `J3686`'s `HTTP 200` check.
- **Teach / Polish / Craft markers on `accidental_inventions_script_master_v02.md`:** `CHAPTER CARD: 4` · `VISUAL MUST: 19` · `TEACH: 5` · `EXPLORER ACTS: 2` (Parts 02 & 05, outside first minute) · `DATA: 5` · `SCALE: 5` (`SCALE ≥ DATA`, all spoken & sourced) · `WHO: 13` (all `2–4w` year-accurate roles) · `WHEN: 10` · `FACT: 4` (all `3–4w`) · `LABEL: 18` (all `2–4w`).
- **`npm run review:script -- --file ../02_Video-Projects/137_Accidental-Inventions-That-Changed-The-World/01_Script/accidental_inventions_script_master_v02.md`:** **PASS · 91.8 / 100** (`Words: 1256 · Est. min: 8.4 · Chapters: 4 · Structure gates 8/8`).
- **Default `npm run gate:episode -- --project ../02_Video-Projects/137_Accidental-Inventions-That-Changed-The-World` (no `--script`):** **PASS — VO / Gemini Veo allowed**, resolving `01_Script/accidental_inventions_script_master_v02.md` (`9/9 OK`).
- **`python3 00_Brand/Channel-Setup/tools/status_board.py --check`:** **PASS** (`34 status files and BOARD.json are in order`).
- **`00_Brand/Channel-Setup/tools/check_all.sh 02_Video-Projects/137_Accidental-Inventions-That-Changed-The-World`:** **ALL CHECKS PASS** (durable desk handoffs, email ratchet, no media, status board, ElevenLabs guard tests, vo_check word tests, atempo tests, voice speed, contract tests `28/28`, package-lint, review:script `91.8`, gate:episode).
- **GitHub CI on PR `#775`:** **7/7 checks green** (`no-desk-close`, `contract`, `no-media`, `status-board`, `check`, `tests`, `atempo`).

---

## 5. Next Production Steps (Held under Rule G WIP)

1. **Rule G WIP Hold (`5/5` HOS active in `orbit-with-ben/jobs/WIP.json`):** `HOS:009`, `HOS:010`, `HOS:013`, `HOS:128`, `HOS:136`. Do **not** queue `HOS:137` long VO or Shorts `S01`/`S02` VO until an open HOS WIP slot clears (next expected when `HOS:009` clears Ben's watch / schedules).
2. **Once an HOS WIP slot opens:** Promote `HOS:137` into `WIP.json` `active` and queue Mac-mini ElevenLabs `vo` jobs for locked `accidental_inventions_script_master_v02.md` (`d2a359c4...`, 5 parts) and locked `10_Shorts/SHORTS_SCRIPTS_v02.md` (`62ff7c99...`, `S01` & `S02`) under normal credit rules (`el_client.py`/`vo_take.py`, `vo_check_py312.sh`, floor `0`, never buy/top up).
3. **Post-VO gates:** Picture generation (`Flow Veo 3.1`, renews 12 Dec) and rendered thumbnail design/panel (`§2.6` + `§2.9` 3-way T&C) remain **strictly blocked until Chief VO PASS**.
