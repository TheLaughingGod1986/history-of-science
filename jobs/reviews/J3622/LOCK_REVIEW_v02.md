# HOS 127 — `v02` Fix Verification & Acting Chief `KEEP` / Script Lock Ruling (`J3622`)

- **Job:** `J3622` (`kind: review`, ref `J3504`, reopened by `J3689` on `2026-11-25T09:44Z`)
- **Acting Chief:** `gemini` (elected Acting Chief under `Claude -> Codex -> Gemini -> Grok` per Ben's 24 Nov 2026 order; verified via live `chief_relay.py status` = `Chief: Gemini` at `09:47Z`, `09:51Z`, and `09:52Z`; `claude` down until `12:50Z`, `codex` down on usage limit until Nov 27)
- **Date:** `2026-11-25` (UTC)
- **Film:** `HOS:127` — *Wright Brothers First Flight: The 1901 Wind Tunnel* (Cluster 4 Lead Film 4 of `hos-search-2027-01`, target air **Thu 31 Dec 2026 18:00 London**; Ben's watch **Mon 28 Dec**; script lock due **Fri 11 Dec**)
- **Prior Ruling:** `jobs/reviews/J3622/REVIEW.md` (merged via HOS PR `#773` `75656f0a`, `FIX before lock` on `v01` with 8 mandatory items `FIX-1`–`FIX-8`)
- **Audited `v02` PRs:**
  - HOS PR `#774` (`macbook/J3688`, head `45953e56d7a41bca78d1985f451663246d47c649`) — `v02` script, `SOURCES.md`, `FACT_NOTES_v02.md`, `SHORTS_SCRIPTS_v02.md`, synced packaging docs (`PRE_BUILD_VIDIQ_AUDIT.md`, `LAUNCH_PLAN.md`, `PACKAGE_FIRST_SCORING_v01.md`), archived `v01`, `production-status.md`, `status.json`
  - HOS PR `#778` (`gemini/J3690-hos127-facts-v02`, head `09567d14`, stacked cleanly on PR `#774`, `MERGEABLE`, `7/7` GitHub CI checks green) — independent `v02` facts audit (`01_Script/GEMINI_FACTS_CHECK_v02.md`: `17 OK / 4 PARTIAL / 0 FLAG`)
- **Ruling:** **`KEEP` & SCRIPT LOCKED**
- **Protected Actions Executed by Elected Acting Chief (`gemini`):**
  - Merged HOS PR `#778` into `main` as **`d4186e333802cca592d012b5af56aa4779967471`** (automatically merging/superseding stacked PRs `#708`, `#756`, `#771`, and `#774`, all verified `MERGED` at `2026-11-25T09:53Z`).
  - Recorded this `jobs/reviews/J3622/LOCK_REVIEW_v02.md` and locked `status.json` (`script`: `done`, `facts`: `done`, `shorts_scripts`: `done`, `air`: `2026-12-31`, `ready_by`: `2026-12-28`) + `production-status.md` via clean PR to HOS `main`.
  - Closed **`J3622`** as `done` in `orbit-with-ben/jobs/QUEUE.json` (script lock achieved).
  - **Rule G WIP Guard (`orbit-with-ben/jobs/WIP.json` checked `2026-11-25`):** HOS currently occupies **5 of 5** active WIP places (`HOS:009`, `HOS:010`, `HOS:013`, `HOS:128`, `HOS:136`). Therefore `HOS:127` long VO and Shorts `S01`/`S02` VO are **NOT queued yet** and remain cleanly held (`vo: todo`, `shorts_vo: todo`) behind `HOS:137` until an open HOS WIP slot clears.
  - **Spend / Scheduling:** **£0.00 / 0 credits spent**; nothing uploaded, scheduled, or altered on YouTube.
  - **Schedule & contingency preserved:** Fri 11 Dec lock achieved 16 days early; Mon 28 Dec Ben watch and Thu 31 Dec 2026 18:00 London target air preserved (normal publish, no Premiere; Shorts `S02` Fri 1 Jan & `S01` Sat 2 Jan 11:30 London; standing 1-week slip contingency if not ready).
  - **Packaging caveat preserved:** Confirmed working direction only — draft thumbnail concepts (`50% TOO HIGH` with 20-gauge steel airfoil, `200 TINY WINGS` with miniature 20-gauge steel wings, §2.6 hand-verified ink, plus 3rd T&C variant post-VO per §2.9) remain **unrendered drafts (NOT rendered packaging PASS)**; picture and rendered thumbnails wait for Chief VO PASS.

---

## 1. Exact Locked `v02` SHA-256 Hashes (Independently Verified on `09567d14` / Merged `d4186e33`)

Confirmed byte-for-byte that PR `#778` (`J3690`) did not modify any of the seven core `v02` deliverables from PR `#774` (`J3688`):

```text
1488f59692ec624c9225b0d509d8dc47c7a1ded8e5b276514783d2fd5eddfdd4  02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel/01_Script/wright_brothers_wind_tunnel_script_master_v02.md
9f331ba20a6f221668c53084fd26dd3d71ff1d7b95e8b6cba606094233f1e8da  02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel/01_Script/SOURCES.md
7ad7cb465190e3d3bd1f32f8ccaf65e55e569ed7eb23afb10683c80c935f71b6  02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel/01_Script/FACT_NOTES_v02.md
e105927874f38f495e6a7deea3e31d735ac1c8c00337d13931032e88ed1a5d26  02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel/01_Script/GEMINI_FACTS_CHECK_v02.md
59e3005dee9df893d7c3c81f5bab2e9a5ffa8563e4cb97b4f0ab68721b174ef6  02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel/10_Shorts/SHORTS_SCRIPTS_v02.md
32fb501ae6a28b6c9a9729cd0650793786d5f746c3669cf45d6643950bbecd69  02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel/11_Upload-Package/PACKAGE_FIRST_SCORING_v01.md
3c9738a278fe902c7ce1af02f4ab431a20308bb18376b42858ad0ff3e3d1b989  02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel/11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md
5007dc56184f984cbe7dce9caba2d57d525e29f2904faef1fbd41f8d5788e62e  02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel/11_Upload-Package/LAUNCH_PLAN.md
```

---

## 2. Independent Verification Matrix — All 8 `J3621`/`J3622` Blocking Fixes (`FIX-1`–`FIX-8`)

| Fix | Requirement (`J3622` PR `#773`) | Independent Chief Verification (`2026-11-25`, direct live checks on `v02`) | Status |
|---|---|---|---|
| **`FIX-1`** | 1902 vs 1901 glide ratio (`622.5 ft` vs typical `300 ft` 1901 glides, removing `"almost double"`) | Part 04 L126 speaks *"more than double their typical three-hundred-foot glides of nineteen oh-one"* (`622.5 / 300 = 2.075×`); `SCALE:` L119 matches; Row 13 quotes NASA GRC `1901-wind-tunnel-tests/` verbatim (`"300 feet"` verified direct `HTTP 200`); `"almost double"` removed; `1.60×` vs `389 ft` record noted transparently. | **PASS** |
| **`FIX-2`** | Harrison `H4` (`1759`) handoff time gap (`"a century and a half earlier"`, not `"two centuries"`) + Row 18 RMG `ZAA0037` | Part 05 L160 speaks *"Yet a century and a half earlier — in the very same year Smeaton published his table — another workshop craftsman faced an even deadlier measurement mystery: building a brass watch..."*. Direct `HTTP 200` on RMG `ZAA0037` (`H4`, `1759`, `1755`, `Brass`) & RMG *Longitude found* (`1761`, `Jamaica`). | **PASS** |
| **`FIX-3`** | Soften Part 01 `1/3` lift causality to Smeaton `0.005` + flawed wing-lift curves; tighten `"century-old"`; align `S01` Caption Line 1 | Part 01 L09 reads *"an eighteenth-century flight formula"*; L21 & `[TEACH]` L40 attribute `1/3` lift to flawed wing-lift curves together with Smeaton's `1759` `0.005` (NASA GRC `1901-wind-tunnel-tests/` direct `HTTP 200` verified). `S01` Caption Line 1 (`Their 1901 glider lifted only a third of what tables promised.`) matches spoken VO cleanly; ambiguous `"50% wrong"` removed from caption. | **PASS** |
| **`FIX-4`** | Short `S02` adverse-yaw wording (`"spin the wrong way"`, never `"spin backward"`) | `"spin backward"` absent (`0` occurrences) across `SHORTS_SCRIPTS_v02.md`; replaced with `"spin the wrong way"` across VO, Caption Line 1, table Row 1, and loop check, matching Part 04 adverse-yaw `"well digging"` physics verified direct `HTTP 200` on Smithsonian NASM. | **PASS** |
| **`FIX-5`** | Sync `PRE_BUILD_VIDIQ_AUDIT.md`, `LAUNCH_PLAN.md`, `PACKAGE_FIRST_SCORING_v01.md` to Arm A (`50c`), `20-gauge steel` models, & Smeaton `1759` DOI | Programmatic sweep across all three docs confirms Arm A (`50c`) primary everywhere, `0` `"brass"` wing-model slips, `0` `"THE TABLES LIED"`, `0` stale `6-foot`/`16-inch`/`66%`/`cardboard`/`UNVERIFIED` leaks. Smeaton `1759` DOI `10.1098/rstl.1759.0019` added to `SOURCES.md` #8 & Row 4 and verified live via CrossRef API `HTTP 200` (`Smeaton`, `1759`, `100-174`). | **PASS** |
| **`FIX-6`** | Speak `1899–1905` 6-year timeline `SCALE`; separate `1900` tent vs `1901` shed chronology; cap all `WHEN:` stamps `≤4` words | Part 05 L158 speaks *"In just six years, they had gone from a five-foot kite to a thirty-nine-minute airplane."* Part 01 L15 (`WHEN: Kitty Hawk, 1900` canvas tent) & L39 (`WHEN: Kill Devil Hills, 1901` wooden camp shed & 1901 glider) separated cleanly. Programmatic check confirms `14/14` `WHEN:` stamps `1–4` words (`0` over 4w). | **PASS** |
| **`FIX-7`** | Rebalance `SHORTS_SCRIPTS_v02.md` row WPM (`16.0–19.0 s`, `atempo ≤ 1.06`), `≤4w` overlays clear of `0–2 s` & `9–14 s`, explicit R7 handling | `S01` (`43` tokens / `44` spoken ≈ `17.8 s`, `145–148 wpm` overall, overlay `1/3 PREDICTED LIFT` `3w` at `4.6–8.0 s`) & `S02` (`44` tokens / `46` spoken ≈ `18.0 s`, all rows `142–158 wpm`, overlay `KILL DEVIL HILLS, 1902` `4w` at `4.2–7.8 s`) both fit `16.0–19.0 s` (`atempo ≤ 1.06`) with R7 exact live long title cleanly at `9.0–14.0 s` fading well before `≤0.3 s` match-cut loop. | **PASS** |
| **`FIX-8`** | Archive `v01` out of `01_Script/`, exclude `_template` plate stub, fold `R04`/`R10`/`R14`/`R16` polishes | `01_Script/` contains ONLY `wright_brothers_wind_tunnel_script_master_v02.md` (`v01` archived to `_archive/`); default `npm run gate:episode` resolves `v02` directly (`9/9 OK`); `_template` stub `part-01_plates_v01.json` explicitly excluded from completed plate boards in `production-status.md`; `R04` full quote, `R10` `0.794 mm` vs `0.76 mm` wording, `R14` `"Ten responded"` quote + L133 `"By early nineteen oh-three"`, and `R16` `14 Dec` quotes all verified live. | **PASS** |

*Non-blocking `J3690` hygiene notes acknowledged cleanly:* (1) `S01` shot table rows 3–4 word-count labels (`12w`/`11w` labelled `13w`/`10w`, total `43` tokens / `44` spoken over `17.8 s` intact; edit cut can shift `0.4 s` with zero spoken change); (2) non-spoken parenthetical `389 ft` 1901 record note in `SOURCES.md`/`FACT_NOTES_v02.md` Row 13 (all spoken/on-screen `R13` figures verified verbatim on primary NASA/Smithsonian/NPS pages); (3) Royal Society `doi.org` redirects behind WAF `403` to CLI clients while CrossRef API returns `HTTP 200` with exact `1759` metadata.

---

## 3. Confirmed Packaging Working Direction (Unrendered Drafts Only)

- **Primary Title (Arm A):** `Wright Brothers First Flight: The 1901 Wind Tunnel` (`50c ≤ 50`, `0` exact collisions across `80` saved search rows in `evidence_2026-11-21_public_search.json` & `evidence_2026-11-24_plan_title_search.json`). Confirmed manifest neighbour phrase `"wright brothers"` per `THUMBNAIL_AND_TITLE_RULES.md` §1.3. Low-RPM `"aviation history"` (`PK 35%`, `VN 12%`) excluded everywhere.
- **T&C Arm B (Verbatim Plan Title):** `Wright Brothers First Flight: The 1901 Wind Tunnel That Solved Lift` (`67c ≤ 70`, `0` collisions).
- **T&C Arm C (Physics Lead):** `How Do Airplanes Fly? (The 1901 Wind Tunnel)` (`44c ≤ 50`, `0` collisions).
- **Neighbours:** `evidence_2026-11-21_neighbours.json` `gate = PASS`, `bigCount = 8` raw (`5` strictly on-topic `≥1M` led by `TED-Ed` ★ `2,568,211`), `hasTed = True`, `failedQueries = []`.
- **Draft Thumbnails (Unrendered Drafts — NOT rendered packaging PASS):** Concept A (`50% TOO HIGH`, gold on `50%`, 20-gauge steel airfoil) & Concept B (`200 TINY WINGS`, gold on `200`, miniature 20-gauge steel wings). 3rd T&C variant (`§2.9`), `§2.6` hand-verified lettering, `style_sheet.py`, `thumb_preview.py` (`168×94`), and HOOK/BAND/PHONE scoring wait until after Chief VO PASS.
- **Shorts Titles (Test B, `0` collisions):** `S01` *Why Did the Wright Brothers Build a Wind Tunnel?* (`48c`, Sat 2 Jan 2027 11:30 London) & `S02` *How Did the Wright Brothers Steer the First Plane?* (`50c`, Fri 1 Jan 2027 11:30 London).

---

## 4. Fresh Independent Gate Outputs (`09567d14` / Merged `d4186e33`, `2026-11-25`)

- **Direct live HTTP exact-quote checks (run in this Chief session):** **`15/15` primary institutional endpoints returned `HTTP 200` with `55/55` key quote substrings matched (`0` missing)** (`NASA_SMEATON`, `NASA_BERNOULLI`, `NASA_1901_TESTS`, `NASA_TUNNEL`, `NASA_MODELS`, `NASA_BALANCE`, `NASA_CONTROL`, `NASA_PROPELLERS`, `SI_RESEARCH`, `SI_FLYER`, `SI_KITTY_HAWK`, `NPS_FIRST_FLIGHT`, `CROSSREF_SMEATON`, `RMG_H4`, `RMG_LONGITUDE`), corroborating `J3690`'s `21/21` endpoint fetch (`77/77` verbatim quotes; `17 OK / 4 non-blocking secondary-lifespan PARTIAL / 0 FLAG`).
- **Part 01 spoken milestones (`@150 wpm`, programmatic):** L05 (`17w`, `0.0–6.8 s ≤ 0:08` title question), L09 (`17w`, `6.8–13.6 s ≤ 0:15` promise), L13 (`24w`, `13.6–23.2 s ≤ 0:25` stakes), L17 (`18w`, `23.2–30.4 s < 0:45` first real fact), L21 (`36w`, `30.4–44.8 s`, early `DATA+SCALE` Smeaton `0.005` vs `0.0033` landing inside `0:25–0:40`).
- **Teach / Polish / Craft markers on `wright_brothers_wind_tunnel_script_master_v02.md`:** `CHAPTER CARD: 4` · `VISUAL MUST: 29` · `TEACH: 5` · `EXPLORER ACTS: 2` (Parts 02 & 05, outside first minute) · `DATA: 7` · `SCALE: 7` (`SCALE ≥ DATA`, all 7 spoken & sourced) · `WHO: 5` (all `3w ≤ 4w` year-accurate roles) · `WHEN: 14` (all `≤4w`) · `FACT: 4` (all `≤4w`) · `LABEL: 27` (all `≤4w`).
- **`npm run review:script -- --file ../02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel/01_Script/wright_brothers_wind_tunnel_script_master_v02.md`:** **PASS · 93.6 / 100** (`Words: 1282 · Est. min: 8.5 · Chapters: 4 · Structure gates 8/8`).
- **Default `npm run gate:episode -- --project ../02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel` (no `--script`):** **PASS — VO / Gemini Veo allowed**, resolving `01_Script/wright_brothers_wind_tunnel_script_master_v02.md` (`9/9 OK`).
- **`python3 00_Brand/Channel-Setup/tools/status_board.py --check`:** **PASS** (`34 status files and BOARD.json are in order`).
- **`00_Brand/Channel-Setup/tools/check_all.sh 02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel`:** **ALL CHECKS PASS**.
- **GitHub CI on PR `#778`:** **7/7 checks green** (`no-desk-close`, `contract`, `no-media`, `status-board`, `check`, `tests`, `atempo`).

---

## 5. Next Production Steps (Held under Rule G WIP)

1. **Rule G WIP Hold (`5/5` HOS active in `orbit-with-ben/jobs/WIP.json`):** `HOS:009`, `HOS:010`, `HOS:013`, `HOS:128`, `HOS:136`. Do **not** queue `HOS:127` long VO or Shorts `S01`/`S02` VO until an open HOS WIP slot clears behind `HOS:137`.
2. **Once an HOS WIP slot opens for `HOS:127`:** Promote `HOS:127` into `WIP.json` `active` and queue Mac-mini ElevenLabs `vo` jobs for locked `wright_brothers_wind_tunnel_script_master_v02.md` (`1488f596...`, 5 parts) and locked `10_Shorts/SHORTS_SCRIPTS_v02.md` (`59e3005d...`, `S01` & `S02`) under normal credit rules (`el_client.py`/`vo_take.py`, `vo_check_py312.sh`, floor `0`, never buy/top up).
3. **Post-VO gates:** Picture generation (Google Flow — post-5 Dec `Veo 3.1 - Lite` / `Omni 1.2 Flash` rules per `studio/RULES.md`, Flow renews 12 Dec) and rendered thumbnail design/panel (`§2.6` + `§2.9` 3-way T&C) remain **strictly blocked until Chief VO PASS**.
