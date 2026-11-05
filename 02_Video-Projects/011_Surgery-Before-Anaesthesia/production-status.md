# Production status — Anesthesia (Ether Day, 1846 and surgery before anesthesia)

| Field | Value |
|---|---|
| Slug | `011_Surgery-Before-Anaesthesia` |
| Channel | `@HistoryOfScienceYT` only |
| Topic | **Anesthesia** — Surgery before anesthesia, Davy's 1800 laughing gas, Long's 1842 ether towel, Wells's 1845 Boston trial, Morton & Warren's 16 Oct 1846 Ether Dome, Simpson's 1847 chloroform, Snow & Queen Victoria 1853 |
| Air (slotted) | **Thu 10 Dec 2026** 18:00 UK (`2026-12-10T18:00:00.000Z`) — locked in `J2231` |
| Ready for Ben's OK | **Sun 6 Dec 2026** |
| Stage | **Package scaffold & Shorts scripts v02 done; Long VO queued (`J2245`)** (`J0180` / `J0183` / `J0198` / `J0224` / `J2231` / `J2239`). |
| Neighbour gate | **PASS** (12 Oct 2026 `J0180` & 5 Nov 2026 `J2231`): 6 education ≥1M; TED-Ed/TED yes (TED-Ed *How does anesthesia work?* 19.73M, TED-Ed *What did people do before anesthesia?* 2.66M, TED-Ed *How aspirin was discovered* 3.08M, SciShow *What Does Anesthesia Do to Your Brain?* 1.38M). Evidence `11_Upload-Package/evidence_2026-11-05_neighbours.json` |
| Public search | **PASS** (`11_Upload-Package/evidence_2026-11-05_public_search.json` + `evidence_2026-11-05_shorts_public_search.json`): `"What Surgery Was Like Before Anesthesia"`, `"who invented anesthesia"`, `"surgery before anesthesia"`, `"How Was Surgery Done Before Anesthesia?"`, and `"Who Invented Anesthesia?"` all autocomplete (`yes` / exact `related`). |
| Script review | `01_Script/surgery_script_master_v02.md` (**91.1/100 PASS**, 1,259 words / ~1,210 spoken, 8/8 structure gates; verified against Nov 2026 `HOS-2026-11-E2` / `J2204` first-30s proof-first + early DATA/SCALE rules in `01_Script/SCRIPT_NOTES_v01.md`) |
| FACT_NOTES | `01_Script/SOURCES_v01.md` / `01_Script/FACT_NOTES_v01.md` (`J0198` Gemini facts PASS: 35 OK, 1 PARTIAL hedged, 0 FLAG) + `01_Script/CLAUDE_QUOTE_CHECK_v01.md` (`J0224` Claude primary-source quote check PASS) |
| Shorts scripts | `10_Shorts/SHORTS_SCRIPTS_v02.md` (**done**, `J2239`: 2 Test B search-titled Shorts — *How Was Surgery Done Before Anesthesia?* 61w and *Who Invented Anesthesia?* 60w, payoffs withheld past 15 s) |
| Upload package | `11_Upload-Package/PACKAGE_MANIFEST.json`, `PRODUCTION_CHECKLIST_V2.md`, `Descriptions/surgery_long_description_v01.txt`, `Tags/surgery_long_tags_v01.txt` (`npm run lint:package -- --film 011` **PASS**, `J2239`) |
| VO | **queued (`J2245`, `--kind vo`, `--needs mini`)** — 5 parts, Ben Orbit Narrator `eleven_v3`, from locked `surgery_script_master_v02.md` |
| Picture | **not started, no mint** |
| Runtime target | 7–9 min, 5 parts (~1,210 spoken words) |

## 5 Nov 2026 — Topic lock for Thu 10 Dec & Episode Gate (`J2231`)

### `neighbours.py` & `public_search.py` output

```text
| # | Channel | Views | Title | Found by |
|---|---|---|---|---|
| 1 | TED-Ed ★ | 19,734,385 views | [How does anesthesia work? - Steven Zheng](https://youtu.be/B_tTymvDWXk) | surgery before anesthesia |
| 2 | TED-Ed ★ | 6,830,607 views | [How does laser eye surgery work? - Dan Reinstein](https://youtu.be/XPDVmBg5DeE) | ted-ed how anesthesia was discovered |
| 3 | TED-Ed ★ | 4,584,699 views | [How does heart transplant surgery work? - Roni Shanoada](https://youtu.be/o1z2DfFZBS4) | ted-ed surgery before anesthesia |
| 4 | TED-Ed ★ | 3,078,948 views | [How aspirin was discovered - Krishna Sudhir](https://youtu.be/uRhkDN2WjzI) | ted-ed how anesthesia was discovered |
| 5 | TED-Ed ★ | 2,659,053 views | [What did people do before anesthesia? - Sally Frampton](https://youtu.be/FBlcU4GdxCc) | surgery before anesthesia |
| 6 | TED-Ed ★ | 280,618 views | [How to perform brain surgery without making a single cut - Hyunsoo Joshua No](https://youtu.be/6d_dtVTs4CM) | ted-ed surgery before anesthesia |
| 7 | SciShow | 1,381,676 views | [What Does Anesthesia Do to Your Brain?](https://youtu.be/43z7NovmlHk) | ted-ed how anesthesia was discovered |
| 8 | SciShow | 444,291 views | [We Finally Know How Anesthesia Works](https://youtu.be/ZSsYjQeK0qg) | how anesthesia was discovered |
| 9 | SciShow | 281,274 views | [The Con Man Who Invented Anesthesia](https://youtu.be/YHuet6imDWI) | ted-ed how anesthesia was discovered |

Words the top neighbours share: how does, does anesthesia, surgery work
TED-Ed/TED neighbour: yes
Big neighbours (≥ 1,000,000 views): 6 (need 3)
Neighbour gate (≥ 3 education videos with 1,000,000+ views): PASS
Raw pull: 02_Video-Projects/011_Surgery-Before-Anaesthesia/11_Upload-Package/evidence_2026-11-05_neighbours.json
| Phrase | Autocomplete? | Top results (GB) |
|---|---|---|
| What Surgery Was Like Before Anesthesia | yes | Zenn 29,011 · TED-Ed 2,659,051 · Medical Secrets 995,905 · TED-Ed 19,734,385 · Medical Secrets 2,436,471 |
| Anesthesia: The Day Surgery Stopped Hurting | no | TED-Ed 19,734,385 · Medical Secrets 1,581,730 · Medical Secrets 1,840,484 · Nomi khattak 42 · Doctor Myro 3,895,150 |
| who invented anesthesia | yes | Patrick Kelly 147,776 · TED-Ed 19,734,385 · TED-Ed 2,659,053 · SciShow 281,274 · Suho Pulse 480 |
| surgery before anesthesia | yes | TED-Ed 2,659,053 · Medical Secrets 2,436,471 · Zenn 29,010 · Medical Secrets 35,835 · TED-Ed 19,734,385 |

Raw pull: 02_Video-Projects/011_Surgery-Before-Anaesthesia/11_Upload-Package/evidence_2026-11-05_public_search.json
```

### `npm run review:script` output

```text
# surgery_script_master_v02.md

**Decision:** PASS · **Score:** 91.1 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 7.9 |
| storytelling | 8 |
| scientificAccuracy | 8.9 |
| emotion | 9.6 |
| escalation | 10 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1259 · Est. min: 8.4 · Chapters: 4

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91.1/100 — proceed to VO after production checklist.

Pass threshold: 90
```

### `npm run gate:episode` output

```text
# Episode gate — 011_Surgery-Before-Anaesthesia

**Decision:** PASS — VO / Gemini Veo allowed

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/ben/_desk/worker/history-of-science/02_Video-Projects/011_Surgery-Before-Anaesthesia |
| prebuild_vidiq | OK | Pre-build vidIQ audit present and looks signed off. |
| script_file | OK | Script: 01_Script/surgery_script_master_v02.md |
| script_review | OK | Script reviewer PASS 91.1/90 (need ≥90). |
| explorer_acts | OK | [EXPLORER ACTS] beats 2 (need ≥1). |
| visual_must | OK | [VISUAL MUST] count 26 (need ≥4). |
| teach | OK | [TEACH] count 5 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 4 (aim 4–6 film acts). |
| production_checklist | WARN | No PRODUCTION_CHECKLIST_V2.md yet — add before publish. |
| gemini_env | WARN | No 07_Edit-Project/.env.example — ensure GEMINI_API_KEY before Veo spend. |

Script score: **91.1/100** · PASS
```

## Next four HOS topics proposed to mid-January (`J2231`, `jobs/WIP.json` `next_hos`)

1. **Thu 24 Dec 2026 (`HOS:012` · `012_Mendel-Pea-Plants`):** *Genetics: The Monk Who Counted 28,000 Pea Plants* — how Augustinian friar Gregor Mendel hand-pollinated 28,000 pea plants in Brünn (1856–1863) to discover dominant and recessive traits, only to be ignored for 35 years until three botanists rediscovered his paper in spring 1900 (neighbour gate PASS: 8 education videos ≥1M incl. TED-Ed 5.02M; script v01 93.5 PASS in `00_Brand/Channel-Setup/ideas/012_Mendel-Pea-Plants/`).
2. **Thu 31 Dec 2026 (`HOS:014` · `014_Anning-Fossils-Extinction`):** *Extinction: The 12-Year-Old Who Dug Up a Sea Dragon* — how twelve-year-old Mary Anning chipped out a 17-foot *Ichthyosaurus* (1811–1812) and the first complete *Plesiosaurus* (1823) on the Lyme Regis cliffs, convincing Georges Cuvier in Paris that entire kinds of animals could go extinct (neighbour gate PASS: 4 education videos ≥1M incl. NHM 5.22M & TED-Ed 1.78M; script v01 93.8 PASS in `00_Brand/Channel-Setup/ideas/014_Anning-Fossils-Extinction/`).
3. **Thu 7 Jan 2027 (`HOS:015` · `015_Hooke-Cell-Theory`):** *Cell Theory: How Cork, a Microscope and a Stolen Idea Revealed Our Cells* — how Robert Hooke coined the word "cell" under his 1665 leather microscope in *Micrographia* and Robert Remak proved in 1852 that every living cell divides from an existing cell before Rudolf Virchow published the motto as his own (neighbour gate PASS: 12 education videos ≥1M incl. TED-Ed *The wacky history of cell theory* 8.35M; script v01 93.8 PASS in `00_Brand/Channel-Setup/ideas/015_Hooke-Cell-Theory/`).
4. **Thu 14 Jan 2027 (`HOS:018` · `018_Herschel-Ritter-Invisible-Light`):** *Invisible Light: How a Thermometer Past the Rainbow Found Infrared* — how William Herschel placed a control thermometer in the dark shadow just beyond the red end of a prism rainbow on 11 February 1800 to discover infrared light, prompting Johann Wilhelm Ritter to find ultraviolet with silver chloride in 1801 (neighbour gate PASS: 5 education videos ≥1M incl. Kurzgesagt 9.97M & TED-Ed *Light waves, visible and invisible* 1.26M; script v01 94.8 PASS in `00_Brand/Channel-Setup/ideas/018_Herschel-Ritter-Invisible-Light/`).

## 5 Nov 2026 — Shorts Scripts v02, Upload Package Scaffold & Long VO Queued (`J2239`)

### 1. Nov 2026 `HOS-2026-11-E2` (`J2204`) First-30s Proof-First + Early DATA/SCALE Check

Verified `01_Script/surgery_script_master_v02.md` against `J2204` (`01_Script/SCRIPT_NOTES_v01.md`) with zero spoken word changes:
- **Sub-4.5s visual cuts across `0:00–0:30`:** 8 distinct moving plates (`3.5–4.0 s` each, zero holds `>4.5 s`).
- **Immediate physical proof/apparatus (`0:05–0:15`):** Open brass pocket watch ticking on the surgical tray, strapped wooden operating chair, and two-necked glass ether inhaler globe inside the theatre (no exterior hospital establishing shot).
- **First animated `DATA` + `SCALE` graphic (`0:25–0:40`):** Brass stopwatch dial sweeping round once and stopping short of three minutes + `SCALE: about as long as boiling an egg` (`FACT_NOTES_v01.md` rows 16 & 37).

### 2. Shorts `public_search.py` autocomplete check (`10_Shorts/SHORTS_SCRIPTS_v02.md`)

```text
| Phrase | Autocomplete? | Top results (GB) |
|---|---|---|
| How Was Surgery Done Before Anesthesia? | related: how was surgery done before anesthesia | TED-Ed 2,659,051 · TED-Ed 19,734,424 · Zenn 29,011 · Medical Secrets 995,928 · Michael J. Denk, MD, FACS 2,170,428 |
| Who Invented Anesthesia? | related: who invented anesthesia | Patrick Kelly 147,776 · TED-Ed 19,734,424 · TED-Ed 2,659,053 · SciShow 281,302 · Suho Pulse 480 |
| Why Is Nitrous Oxide Called Laughing Gas? | no | Teeth Talk Girl 259,973 · Violin MD 280,053 · Dr George Olstein 5,773 · Big Manny 993,076 · Peekaboo Kidz 844,307 |
| How Was Anesthesia Discovered? | related: how was anesthesia discovered | Patrick Kelly 147,776 · TED-Ed 19,734,424 · TED-Ed 2,659,051 · SciShow 444,291 · Into the Shadows 166,324 |

Raw pull: 02_Video-Projects/011_Surgery-Before-Anaesthesia/11_Upload-Package/evidence_2026-11-05_shorts_public_search.json
```

### 3. `npm run lint:package -- --film 011` & `npm run gate:episode` output

```text
> content-ops@0.1.0 lint:package
> tsx scripts/package-lint.ts --film 011

PASS  02_Video-Projects/011_Surgery-Before-Anaesthesia/11_Upload-Package/PACKAGE_MANIFEST.json
   warn  [captions] no captionsFile (captions from the script)

# Episode gate — 011_Surgery-Before-Anaesthesia

**Decision:** PASS — VO / Gemini Veo allowed

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/ben/_desk/worker/slot2/history-of-science/02_Video-Projects/011_Surgery-Before-Anaesthesia |
| prebuild_vidiq | OK | Pre-build vidIQ audit present and looks signed off. |
| script_file | OK | Script: 01_Script/surgery_script_master_v02.md |
| script_review | OK | Script reviewer PASS 91.1/90 (need ≥90). |
| explorer_acts | OK | [EXPLORER ACTS] beats 2 (need ≥1). |
| visual_must | OK | [VISUAL MUST] count 26 (need ≥4). |
| teach | OK | [TEACH] count 5 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 4 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |
| gemini_env | WARN | No 07_Edit-Project/.env.example — ensure GEMINI_API_KEY before Veo spend. |

Script score: **91.1/100** · PASS
```

### 4. Long VO queued (`J2245`)

Queued `J2245` (`--repo hos --film 011 --stage vo --needs mini --kind vo --after J2239`) to record all 5 parts of `01_Script/surgery_script_master_v02.md` in Ben Orbit Narrator (`eleven_v3`) on the Mac Mini via `el_client.py` / `vo_take.py`.

## STOP

- No Vertex/Veo/Flow minting on this film.
- Do not merge or close desk PR #180 from this work.
