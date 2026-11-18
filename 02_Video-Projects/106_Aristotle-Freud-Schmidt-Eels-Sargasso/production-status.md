# Production status — 106 Where Do Eels Come From? (The Sargasso Sea Hunt) (Rule-E `GO` in `next_hos`)

| Field | Value |
|---|---|
| Slug | `106_Aristotle-Freud-Schmidt-Eels-Sargasso` |
| Channel | `@HistoryOfScienceYT` only |
| Topic | **Rule-E `GO` (`94 / 100` · `9.40 / 10` Opportunity Score, `J2836`, 14 Nov 2026)** — Pre-cleared in `jobs/WIP.json` `next_hos` under Rule G (`J2835`). **UNVERIFIED CLAIMS GUARD:** Every historical and scientific claim in `TOPIC.md` §2 and `PRE_BUILD_VIDIQ_AUDIT.md` remains **UNVERIFIED** until an active HOS WIP slot opens and `SOURCES.md` + the `facts` lane verify every claim. |
| Neighbour gate | **PASS** (`11_Upload-Package/evidence_2026-11-14_neighbours.json`: `bigCount = 3`, `hasTed = true`: `TED-Ed` `RFi6ISTjkR4` `2,751,342` views, `TED-Ed` `BR1enXROmgA` `1,157,611` views, `Thoughty2` `k61Bk63EvTM` `3,317,475` views; plus `Bizarre Beasts` `acEIGorImGs` `1,594,707` views & `Auralis` `LxNq8zOEbM8` `1,629,143` views in `public_search.py`) |
| Public search gate | **PASS** (`11_Upload-Package/evidence_2026-11-14_public_search.json`: `"where do eels come from"`, `"how do eels reproduce"`, `"eel migration"`, `"sargasso sea eels"` all `autocomplete = yes`; `0` exact title collisions on disambiguated Title A `Where Do Eels Come From? (The Sargasso Sea Hunt)`, Title B `How Do Eels Reproduce? (The 1922 Sargasso Sea Hunt)`, Title C `The Fish That Freud Dissected 400 Times`, Short `S01` `Why Did Sigmund Freud Dissect 400 Eels?`, and Short `S02` `Has Anyone Ever Seen an Eel Lay Eggs?`) |
| Pre-build vidIQ audit | Drafted as proposal in [`11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`](11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md) (unverified claims flagged for `facts` lane) |
| Script review | — / 90 (no script started; waits on active HOS WIP slot and `SOURCES.md` / `facts` lane) |
| Episode gate | not run |
| VO | pending (Ben Orbit Narrator) |
| Picture | pending (Flow Veo 3.1, plate library) |
| Runtime target | 7–9 min, 5 parts |
| Air | Proposal in `next_hos` — Thursday 18:00 UK, normal publish (no Premiere) |
| Shorts | 2 question-titled Shorts proposed (`S01`: *Why Did Sigmund Freud Dissect 400 Eels?*, `S02`: *Has Anyone Ever Seen an Eel Lay Eggs?* — unverified concepts only, not cleared for VO) |

## Topic Gate Evidence (`neighbours.py` & `public_search.py`, Retrieved `2026-11-14`)

```text
| # | Channel | Views | Title | Found by |
|---|---|---|---|---|
| 1 | TED-Ed ★ | 2,751,342 views | [No one can figure out how eels have sex - Lucy Cooke](https://youtu.be/RFi6ISTjkR4) | ted-ed eels |
| 2 | TED-Ed ★ | 1,157,611 views | [Eli the eel: A mysterious migration - James Prosek](https://youtu.be/BR1enXROmgA) | ted-ed eels |
| 3 | Thoughty2 | 3,317,475 views | [Why Nobody Knows How Eels Reproduce](https://youtu.be/k61Bk63EvTM) | eels ted |
| 4 | TEDx Talks ★ | 743 views | [Searching for the Eel Song | Performance Where Water Meets | TEDxHobart](https://youtu.be/pPXs0BAnD4Q) | eels ted |

Words the top neighbours share: how eels, the eel
TED-Ed/TED neighbour: yes
Big neighbours (≥ 1,000,000 views): 3 (need 3)
Neighbour gate (≥ 3 education videos with 1,000,000+ views): PASS
Raw pull: 02_Video-Projects/106_Aristotle-Freud-Schmidt-Eels-Sargasso/11_Upload-Package/evidence_2026-11-14_neighbours.json
```

```text
| Phrase | Autocomplete? | Top results (GB) |
|---|---|---|
| where do eels come from | yes | Bizarre Beasts 1,594,707 · Atomic Frontier 365,534 · TED-Ed 1,157,605 · Auralis 1,629,143 · MinuteEarth 569,775 |
| how do eels reproduce | yes | TED-Ed 2,751,342 · Bizarre Beasts 1,594,707 · जिज्ञासु बने रहें — TED-Ed 5,088 · OctoLab 1,366 · Thoughty2 3,317,475 |
| eel migration | yes | TED-Ed 1,157,608 · ironfalcon100 32,354 · Hidden Animal World 240 · Tim Olley 19,049 · Cormac Skinner 662 |
| sargasso sea eels | yes | acapellascience 175,206 · Discovery UK 114,189 · Search for the Truth Ministries 7,192 · Auralis 1,629,143 · Bizarre Beasts 1,594,707 |
| Where Do Eels Come From? (The 2,000-Year Mystery) | related: where do eels come from; mystery of eel reproduction | Creature Code 8 · Bizarre Beasts 1,594,707 · Riddle & Record 10 · TED-Ed 1,157,605 · Auralis 1,629,141 |
| Where Do Eels Come From? (The Sargasso Sea Hunt) | related: eel migration sargasso sea | Bizarre Beasts 1,594,709 · WowScience by TechSensia 66 · Untamed Animal Facts 1,209 · MinuteEarth 569,777 · TED-Ed 1,157,611 |
| How Do Eels Reproduce? (Nobody Has Ever Seen It) | related: how do eels reproduce mystery | TED-Ed 2,751,342 · Thoughty2 3,317,475 · OctoLab 1,366 · Bizarre Beasts 1,594,707 · Deep Sea Lab 668 |
| How Do Eels Reproduce? (The 1922 Sargasso Sea Hunt) | related: how do eels reproduce mystery | Bizarre Beasts 1,594,709 · Thoughty2 3,317,476 · The Earth and Alien 1 view · OctoLab 1,365 · Deep Sea Lab 668 |
| The Fish That Freud Dissected 400 Times | no | calvintheninja 47,374 · VILEMasterShake 13,938 · Animal Oddballs 81 · The Origin Vault 66,928 · Fish Journeys 255 |
| Why Did Sigmund Freud Dissect 400 Eels? | related: what did sigmund freud do | calvintheninja 47,374 · VILEMasterShake 13,938 · Animal Oddballs 80 · showselectordog 3,451,018 · Sketchy Details 31 |
| Has Anyone Ever Seen an Eel Lay Eggs? | no | Bizarre Beasts 1,594,707 · Never Filmed 57 · Pokato_1 9 · TED-Ed 2,751,342 · Nescium 382 |

Raw pull: 02_Video-Projects/106_Aristotle-Freud-Schmidt-Eels-Sargasso/11_Upload-Package/evidence_2026-11-14_public_search.json
```

## Parts

| Part | Plate board | Latest cut | Status |
|---|---|---|---|
| 01 | `07_Edit-Project/parts/part-01_plates_v01.json` | — | — |
| 02 | | | |
| 03 | | | |
| 04 | | | |
| 05 | | | |

Keep this file current on `main`. A STOP (quota, auth, missing VO) is a line here, not an open branch.
