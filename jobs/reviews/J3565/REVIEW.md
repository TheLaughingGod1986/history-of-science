# HOS 137 — independent draft review (J3565)

Reviewer: `macbook-2`, 25 November 2026. Advisory recommendation: **FIX before lock**.

Reviewed **HOS PR #754** (`gemini/J3513-hos137-script`, head `1ae0da81229a07c0fff5f8c0e74817a680b283da`, built on `origin/main` + `origin/macbook/J3503` PR `#747`) and the completed independent Gemini `facts` lane audit in **HOS PR #769** (`gemini/J3564-hos137-facts-audit`, head `7ae40acfc16eb67da7b812ef79230b02da110de6`, `01_Script/GEMINI_FACTS_CHECK_v01.md`). Confirmed byte-for-byte that PR `#769` left `accidental_inventions_script_master_v01.md`, `SHORTS_SCRIPTS_v01.md`, `FACT_NOTES_v01.md`, `SOURCES.md`, `PACKAGE_FIRST_SCORING_v01.md`, `PRE_BUILD_VIDIQ_AUDIT.md`, and `LAUNCH_PLAN.md` unchanged from PR `#754`.

This report changes no spoken script, grants no PASS or script lock, merges no PR, and authorises no VO or picture spend (`£0.00` / `0` credits). The elected Chief (Codex per fresh `chief_relay.py status` on 25 Nov 2026) owns the FIX ruling, any follow-on routing, merges, and final lock.

---

## 1. Packaging recommendation

- **Titles (confirm working direction; not final upload PASS):**
  - **Primary Arm A:** **`Accidental Inventions: 5 Mistakes That Worked`** (`45 chars ≤ 50`, `0` exact live collisions verified programmatically in `evidence_2026-11-24_public_search.json`). Query-first (`Accidental Inventions`), mobile-safe, wonder-and-proof framing, and excludes the low-RPM trap `history of inventions` (`PK 25%`).
  - **T&C Arm B (plan title):** `Accidental Inventions That Changed the World (5 Mistakes That Worked)` (`69 chars`, `0` collisions) — carries the full `+73.9%`-growth phrase and verbatim neighbour phrase (`that changed the world`).
  - **T&C Arm C:** `Accidental Inventions: 5 Mistakes That Changed the World` (`56 chars`, `0` collisions) — cleaner mobile fit while keeping `Changed the World`.
  - **Programmatic collision & neighbour check:** All 7 candidate Long & Short titles in `evidence_2026-11-24_public_search.json` return `0` exact collisions (retired `5 Accidental Inventions That Changed the World` confirmed colliding with `4` case-insensitive exact title matches in its top 8 results); `5/5` core phrases have live YouTube autocomplete (`suggest` counts `4, 5, 10, 10, 10`); `evidence_2026-11-24_neighbours.json` confirms `gate = PASS`, `bigCount = 4` (`3` strictly on-topic education videos `≥1M` after excluding off-topic AI video `RzkD_rTEBYs`, plus `SciShow` `1.48M` in `public_search.json`), `hasTed = True`, `failedQueries = []`.
  - **Manifest note for Chief (`THUMBNAIL_AND_TITLE_RULES.md` §1.3):** Because `neighbours.py` extracted shared words `"the world, that changed, changed the"`, Arm A (`Accidental Inventions: 5 Mistakes That Worked`) shares the subject noun `"inventions"` (used by `Thoughty2` and `TED-Ed` neighbours) rather than `"that changed the world"`. Confirm `"inventions"` as the manifest neighbour phrase for Arm A so `npm run lint:package` stays aligned with Arm A (while Arms B/C and the description first line also carry `"that changed the world"`).
  - Note: the `96 / 92 / 90` scores in `PACKAGE_FIRST_SCORING_v01.md` are draft judgements, not measured CTR.

- **Thumbnails (confirm concepts with §2.6 / §2.9 notes; unrendered):**
  - **Concept A (`NEARLY TRASHED`, gold on `TRASHED`):** Single giant 3D cartoon 1903 cracked-yet-intact safety-glass flask filling 2/3 right frame, Explorer small lower-left. Complies with §2.2 (single hero), §2.5 (zero word overlap with Titles A/B/C), and §2.B (lettering off hero). Note `NEARLY TRASHED` relies on the flask silhouette to name the object visually; keep the spiderweb fracture unmistakable at `168×94`.
  - **Concept B (`WRONG RESISTOR`, gold on `WRONG`):** Single oversized glowing 1956 wrong resistor + golden heartbeat oscilloscope trace on warm period workbench, Explorer small lower-left. Directly names the object (§2.B.1) and connects to Part 01's opening beat. Enforce §2.6 strictly: all resistor colour bands, oscilloscope grid/waveform, and serif lettering must be hand-verified or inked cleanly in edit (no AI-garbled numerals), and watch dark bakelite near-black balance.
  - **Pending before upload:** Neither concept is rendered yet — `style_sheet.py`, `thumb_preview.py` (`168×94`), HOOK/BAND/PHONE scoring, and a third Test & Compare thumbnail variant (`THUMBNAIL_AND_TITLE_RULES.md` §2.9: 3 variants on every long) remain required after script & VO lock.

---

## 2. Corrections required before lock (`FIX-1` through `FIX-9`)

### Factual & source blockers (all 4 `J3564` FLAGs independently corroborated on 25 Nov 2026)

1. **`FIX-1` — Bénédictus French Patent `FR 405,881` filing date (`Part 03`, line 85; `FACT_NOTES_v01.md` Row 14; `SOURCES.md` Item 3; `J3564` FLAG-1).**  
   Spoken v01 says *"He filed his French patent in November nineteen oh-nine and founded his company in nineteen eleven."* Independently opened primary patent `https://patents.google.com/patent/FR405881A/en` (`HTTP 200` on 25 Nov 2026): **filing/priority date is `1909-08-10` (10 August 1909)**, publication `1910-01-15`, inventor `Edouard Benedictus`. Change spoken line 85 to *"filed his French patent in August nineteen oh-nine"* or year-only *"filed his French patent in nineteen oh-nine"*, and add `FR405881A` to `SOURCES.md` and `FACT_NOTES`.

2. **`FIX-2` — Chardack-Greatbatch 1960 two-stage human implant & survival variance (`Part 01`, lines 31 & 34; `FACT_NOTES_v01.md` Row 7; `SOURCES.md` Item 1; `J3564` FLAG-2).**  
   Spoken line 34 attributes the self-contained mercury-battery pacemaker unqualified to *"April nineteen sixty"* with *"eighteen months"* survival, and visual line 31 reads `Buffalo Apr 1960`. Independently opened `https://pmc.ncbi.nlm.nih.gov/articles/PMC3232561/` (`HTTP 200`) and `https://department.va.gov/history/object-5-cardiac-pacemaker/` (`HTTP 200`): the first human procedure was **two-stage** (myocardial lead implanted first in April 1960; self-contained pulse generator implanted in **June 1960**), and both institutional sources report **2 years / two years** survival (vs Wikipedia's `18 months`). Update spoken line 34 to *"in nineteen sixty"* or *"in June nineteen sixty"* (and visual card to `Buffalo 1960` or `Buffalo June 1960`), and reconcile `"eighteen months"` with VA/`PMC3232561` `"two years"` (or have Chief document the literature variance explicitly).

3. **`FIX-3` — Dead sole URL (`HTTP 521`) & missing source quotes (`FACT_NOTES_v01.md` Rows 2, 5, 6, 8, 9, 24; `SOURCES.md`; inherited by `S01`; `J3564` FLAG-3).**  
   Independently confirmed `https://heartrhythm.com/40th-Anniversary/Wilson-Greatbatch` returns **`HTTP 521`**. Replace with live peer-reviewed `https://pmc.ncbi.nlm.nih.gov/articles/PMC3232561/` (`HTTP 200`, verbatim Greatbatch `10 KΩ` → `1 MΩ` quote). In `v02`, merge `J3564`'s 8 primary/institutional upgrades (`FR405881A`, `PMC3232561`, `PMC5403050`, `US3633A` `270°F`, NobelPrize.org Fleming/Florey/Chain/1945, NIHF Arthur L. Fry & Percy L. Spencer, 3M Post-it history, `US2495429A`), add explicit source quotes for the lifespans of Chardack (`1914–2006`), Gage (`1922–2024`), Elmqvist (`1906–1996`), and Senning (`1915–2000`), and remove the un-upheld `"24 OK · 0 PARTIAL · 0 FLAG"` claim from `FACT_NOTES`.

4. **`FIX-4` — Microsphere adhesive chemistry contradiction (`Part 05`, line 122; `FACT_NOTES_v01.md` Row 21; `SOURCES.md` Item 5; `J3564` FLAG-4).**  
   Spoken line 122 calls Spencer Silver's microspheres *"a low-tack, pressure-sensitive adhesive"*, directly contradicting primary `https://patents.google.com/patent/US3691140A/en` (`HTTP 200`: `"inherently tacky ... low degree of adhesion"`) and its own cited Row 21 quote from `https://www.invent.org/inductees/spencer-silver` (`HTTP 200`: `"high level of tack but a low degree of adhesion"`). Replace `"low-tack"` in Part 05 line 122, `SOURCES.md`, and `FACT_NOTES` with `"low-adhesion, pressure-sensitive adhesive"` or `"light-grip, pressure-sensitive adhesive"` (matching `S02`'s clean `"stuck lightly and peeled clean"`).

### Script opening, Teach/Polish & Shorts timing blockers (new catches in `J3565`)

5. **`FIX-5` — Part 01 opening timings & unsourced `"briefer than a camera flash"` comparison.**  
   Measured from the actual spoken text at `150 wpm` (`2.5 wps`):
   - Line 1 (`14w`): `0.0–5.6 s` (title question by `0:08` — OK).
   - Line 2 (`21w`): `5.6–14.0 s` (general thesis).
   - Line 3 (`41w`): `14.0–30.4 s` (*"By the end of this film, you'll see how a wrong resistor mimicked a living heart..."*) — a 41-word agenda preview that pushes the `0:15` promise and `0:25` stakes milestones past target, delays the first real historical story (Greatbatch 1956) to `30.4–46.8 s` (borderline past the `<0:45` first-fact milestone), and puts `[VISUAL MUST: 0:28 ... EARLY DATA+SCALE 0:25–0:40]` out of sync with the spoken `100×` error (`~40–47 s`) and `1.8 ms` pulse (`~56–63 s`). Trim the agenda sentence by ~20 words so the promise finishes by `0:15`, stakes land by `0:25`, and Greatbatch's 1956 `100×` error starts inside `0:25–0:40`.
   - **Physics/source catch on `"briefer than a camera flash"` (Part 01 line 27):** Standard electronic xenon camera flashes last roughly `0.2–1.0 ms`, which is *shorter* than `1.8 ms`, and no source for this comparison appears in `FACT_NOTES_v01.md`. Replace with an accurate, verifiable scale (e.g., `"less than two thousandths of a second — a tiny fraction of a blink"`, with a cited blink-duration reference in `FACT_NOTES`).
   - Note: `HOS-2026-11-E2` (7 moving plates in `0:00–0:30`) formally applies to films `008–010` only (`studio/RULES.md`), not `137`, though a tight proof-first opening remains desirable.

6. **`FIX-6` — Unspoken `DATA`/`SCALE` in Part 02 & alignment in Part 05 (Polish Pass Rule 4).**  
   `studio/RULES.md` → *Polish pass #4* requires every `DATA` number to have its `SCALE` comparison **spoken** in the same or next sentence and sourced in `FACT_NOTES`. In Part 02, `DATA: ~270°F (132°C)` and `SCALE: hotter than boiling water` exist **only inside `[VISUAL MUST]`** and are never spoken in VO. Either speak the `270°F` / `132°C` *"hotter than boiling water"* comparison in Part 02 VO (backed by primary `US3633A`'s `"heat of 270 of Fahrenheit's scale"`), or tie the `DATA`/`SCALE` marker to a number actually spoken in Part 02. In Part 05, align the spoken Boise Blitz figure with the `SCALE` card (`"nine out of ten"` / `"ninety percent"`) and reconcile Long (`"More than ninety percent"`, Wikipedia) vs Short `S02` (`"ninety percent"`, 3M official history). Also note Part 05 `"aerospace"` (Long & `S02`) is secondary-only (absent from `US3691140A` and NIHF) — qualify or cite explicitly.

7. **`FIX-7` — 5-word `FACT:` card exceeds `≤4`-word cap (`Part 03`, line 80).**  
   `FACT: First used in gas masks` is 5 words, violating `studio/RULES.md` → *Teach on screen* (`≤4` words). Tighten to `Used in gas masks` or `First in gas masks` (`4` words).

8. **`FIX-8` — Shorts `S01` & `S02` front-loaded unperformable row WPM, overlay timing/length & R7 end-card rule (`10_Shorts/SHORTS_SCRIPTS_v01.md`).**  
   Row-by-row pacing audit against `studio/RULES.md` → *Shorts house rules (Ben, 19 Nov 2026)* (`16–19 s`, subject + surprise within `~1.5 s`, overlay clear of `0–2 s` and `9–14 s`, `≤4` words per label, `atempo ≤ 1.06`):
   - **`S01` (`42` ws / `46` hyphen-split words):** Row 1 (`0.0–2.8 s`, `9–10w`) requires `193–214 wpm` and delays `"pacemaker"` to `~3.5 s` at `150 wpm` (past `~1.5 s`); Row 2 (`2.8–6.5 s`, `3.7 s`, `17` ws / `20` hyphen-split words) requires **`276–324 wpm`** (unperformable without illegal speedup); Row 3 (`6.5–9.5 s`, `11w`) requires `220 wpm`; meanwhile Row 4 (`9.5–14.5 s`, `5.0 s`) has only `3` words (`36 wpm`) and Row 5 (`14.5–17.9 s`, `3.4 s`) has `2` words (`35 wpm`).
   - **`S02` (`41` ws / `43` hyphen-split words):** Row 2 (`2.6–6.5 s`, `14–15w`) requires `215–231 wpm` and Row 3 (`6.5–9.5 s`, `11w`) requires `220 wpm`, while Row 4 (`9.5–14.5 s`, `7w`) drops to `84 wpm` and Row 5 (`14.5–16.8 s`, `2w`) drops to `52 wpm`.
   - **Overlay sync & word cap:** Because rows 1–3 actually consume `~13–15 s` at `150 wpm`, the `4.5–8.5 s` Teach overlays (`1.8 MS PULSE · 1 S PAUSE` in `S01`; `1968 SPHERES · 1974 BOOKMARK` in `S02`) fire well before their spoken lines and risk clashing with the `9–14 s` long title card. In addition, `1.8 MS PULSE · 1 S PAUSE` has `6` tokens / two separate facts (`>4`-word cap; tighten to `1.8 MS PULSE` or `100× WRONG RESISTOR`).
   - **R7 ending check:** Specify how the promoted long's exact live title (`Accidental Inventions: 5 Mistakes That Worked`) appears cleanly at `9–14 s` and satisfies `HOS_STRATEGY.md` R7 without breaking the `≤0.3 s` Frame-0 match-cut loop. Rebalance both Shorts' row timestamps to realistic `~150 wpm` speech so total runtime lands cleanly inside `16.0–19.0 s` on actual VO measurement.

9. **`FIX-9` — `v02` filename hygiene & template-stub awareness.**  
   Per the `HOS:128` (`J3630`) `gate:episode` finding, when `v02` is committed to `01_Script/`, do not leave a superseded `*_script_master_v01.md` alongside `v02` where default `npm run gate:episode` (without `--script`) would pick `v01` first — remove or archive `v01` out of `01_Script/` and verify default `gate:episode` resolves `v02`. Also note `07_Edit-Project/parts/part-01_plates_v01.json` in PR `#754` is still an unfilled `_template` placeholder (`"film": "NNN_Slug"`); do not list it in `production-status.md` as a completed Part 01 plate board until post-VO picture stage.

---

## 3. Teach on screen, Polish pass & Craft review

| Area | Audit result on `v01` | Notes for `v02` |
|---|---|---|
| **DATA + SCALE** | `5 DATA`, `5 SCALE` (`SCALE ≥ DATA`) | **FIX-5 & FIX-6:** Part 02 `270°F` / `boiling water` unspoken; Part 01 `"camera flash"` unsourced/inaccurate; align Part 05 spoken `90%` / `nine out of ten`. Timeline `1839–1974` (`135 years`) present and clean. |
| **WHO cards** | `13 WHO` (all 13 named people covered, `≤4`-word year-accurate roles, no premature Nobel titles) | **PASS on script cards**; add missing lifespan quotes for Chardack, Gage, Elmqvist, Senning in `FACT_NOTES` (`FIX-3`). |
| **WHEN stamps** | `10 WHEN` | Core era stamps present; minor gaps on spoken `Oct 1958`, `1911`, `1941`, `1945`, `1972`, `1980` (can drop onto timeline or sequential stamps in edit). Multi-year stamps (`1844, 1860 & 1898`; `Minnesota, 1974 & Boise, 1978`) must animate sequentially so one label shows at a time. |
| **FACT beats** | `4 FACT` | **FIX-7:** #3 `First used in gas masks` is 5 words (`>4`-word cap). |
| **LABELs** | `18 LABEL` (`2–4` words each) | **PASS.** |
| **Explorer & Craft** | `2 [EXPLORER ACTS]` (Parts 02 & 05, outside first minute); `4 [CHAPTER CARD]` (5 parts); midpoint twist (`"Case closed? Not yet."` at Part 03 end); clean curiosity-only handoff to `HOS:129` (Microwave excluded from 5 beats, no goodbye/subscribe ask) | **PASS on structure.** `LAUNCH_PLAN.md` chapter estimates (`0:00`, `1:35`, `3:10`, `4:40`, `6:25`) differ from script headers (`0:00`, `1:45`, `3:20`, `4:50`, `6:35`) and `@150 wpm` (`0:00`, `1:48`, `3:19`, `4:46`, `6:19`); re-time from locked VO. |
| **Shorts house rules (19 Nov)** | 3D cartoon Frame 0, 0% Explorer at Frame 0, concrete-fact line-1 captions, `0` collisions, seamless loop intent | **FIX-8:** Row timings/WPM, `S01` 6-token overlay, overlay/title overlap, R7 alignment. `gate_shorts_open.py` and rendered OPEN/LENGTH/LOOP checks wait for media. |
| **Polish / Picture / Audio gates** | Unverified (script stage only) | SFX (`sfx_kit.py level`), music by part, fine grain, crossfades, actual overlay motion, and `4–6 s` plate cuts remain unverified until media exists. |

---

## 4. Local verification & input hashes

Fresh local tool runs on a verbatim export of **HOS PR #754** (`1ae0da81229a07c0fff5f8c0e74817a680b283da`, 25 Nov 2026):

```text
review:script: Decision: PASS · Score: 92.6 / 100
hook: 9.5 | curiosity: 8.7 | storytelling: 9.5 | scientificAccuracy: 10 | emotion: 9.6
escalation: 8.1 | retentionPotential: 9 | searchPotential: 9.1 | visualOpportunities: 9.5 | narrationFlow: 9.6
Words: 1225 · Est. min: 8.2 · Chapters: 4
Findings: Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.

gate:episode: Decision: PASS — VO / Gemini Veo allowed
project_dir: OK | prebuild_vidiq: OK | script_file: OK | script_review: OK (92.6/90)
explorer_acts: OK (2) | visual_must: OK (19) | teach: OK (5) | chapters: OK (4) | production_checklist: OK
```

These are mechanical script-linter outputs only; they do not override the verified factual contradictions (`FIX-1`–`FIX-4`) or opening/Shorts timing and rule defects (`FIX-5`–`FIX-9`).

**Verified Input SHA-256 Hashes:**
- `01_Script/accidental_inventions_script_master_v01.md` (PR `#754` & `#769`): `aacd41b7965fd10f3c517f369069ff08f4350e4fa4c6cbd1281040916c842d59`
- `10_Shorts/SHORTS_SCRIPTS_v01.md` (PR `#754` & `#769`): `6ab9032f725f5a991f4cbf427b5dd350829904c6a265e5d967f9c68c645946c8`
- `01_Script/FACT_NOTES_v01.md` (PR `#754` & `#769`): `13bd05e3d9c3b88497cc712d0ec4a5d34b43873e9a1b5975f2957a020e12598f`
- `01_Script/SOURCES.md` (PR `#754` & `#769`): `b2fcc8c310361344a7f3601eeda221fc788f9b009c1ab5dd3bc18dc295da9c57`
- `11_Upload-Package/PACKAGE_FIRST_SCORING_v01.md` (PR `#754` & `#769`): `da131a4346bb9c05bc545a347b5053c32f3ba7350dc7ff3e914c42aa35296de8`
- `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md` (PR `#754` & `#769`): `d84b917ec0a4106253dd4ba31afa68c6a4176a6b5d8eb77e241018af3a60cbf9`
- `11_Upload-Package/LAUNCH_PLAN.md` (PR `#754` & `#769`): `79b64fcff8458cf572b7197f214f86107ec79a6656e69fcf83889b4de856a01d`
- `01_Script/GEMINI_FACTS_CHECK_v01.md` (PR `#769` `7ae40acf`): `3e570433908f89ee4ea8dacd5ba9c7ef8724169a9819c6506190d7eb88f30496`

---

## 5. Handoff & Rule G WIP guard

- **Next owner:** Elected Chief (Codex). Park `J3565` for Chief to issue the formal **FIX** ruling and queue:
  1. A `script` correction job producing **`v02`** (resolving `FIX-1` through `FIX-9` cleanly on top of PR `#769` / `#754` / `#747`).
  2. An independent `facts` re-verification pass against `v02`'s exact SHA-256 hash.
  3. Direct MUST QUOTE check & Chief lock/merge of `v02` (superseding PRs `#747`, `#754`, `#769`).
- **Rule G WIP note (`orbit-with-ben/jobs/WIP.json` checked 25 Nov 2026):** HOS currently occupies **5 of 5** active slots (`HOS:009`, `HOS:010`, `HOS:013`, `HOS:128`, `HOS:136`; `HOS:008` has already left active). Even after `v02` locks, `HOS:137` VO waits for an open HOS WIP slot to clear. Preserve the Tue 8 Dec lock due date, Mon 21 Dec Ben watch target, and Thu 24 Dec 18:00 London air target (with standing 1-week slip contingency if needed).
- **Spend:** `£0.00` / `0` credits. No merge, no script lock, no VO/picture spend, no YouTube or scheduling action.
