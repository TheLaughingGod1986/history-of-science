# Production status — 130 How Does a Nuclear Reactor Work? (Under a Stadium)

| Field | Value |
|---|---|
| Slug | `130_Fermi-Szilard-Woods-How-Does-A-Nuclear-Reactor-Work` |
| Channel | `@HistoryOfScienceYT` only |
| Topic | **Rule-E pre-cleared GO (`96.6 / 100`, `J3350`, `2026-11-22`)** · stays in `jobs/WIP.json` `next_hos` under Rule G (`4/4` active HOS slots full) — [`11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md`](11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md) · [`11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md`](11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md) |
| Neighbour gate | **PASS** (`12` raw / `9` strictly on-topic education videos `≥1M`, `TED-Ed/TED: yes`; `6` tightly focused reactor-mechanism/build videos `≥1M`) — `11_Upload-Package/evidence_2026-11-22_neighbours.json` |
| Public search check | **PASS** (`11` queries / `80` rows, `autocomplete = yes` on `4` core phrases, `0` exact title collisions across all `5` candidate titles — refreshed in `J3350`) — `11_Upload-Package/evidence_2026-11-22_public_search.json` |
| Pre-build vidIQ audit | Draft pre-filled (`11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`, £0 spend; `J3224` Cluster 2 demand cited; live title scores wait on active WIP slot) |
| Script review | — / 90 (not started — waits on open HOS WIP slot, `SOURCES.md`, and `facts` lane) |
| Episode gate | not run |
| VO | pending (Ben Orbit Narrator — zero spend) |
| Picture | pending (Flow Veo 3.1, plate library — zero spend) |
| Runtime target | 7–9 min, 5 parts |
| Air | Proposal in `next_hos` — Thursday 18:00 UK, normal publish (no Premiere) |
| Shorts | 2 search-titled `16–19 s` Shorts proposed (`Ben 19 Nov 2026` house rules: `S01` *How Does a Nuclear Reactor Control a Chain Reaction?*, `S02` *Why Did Enrico Fermi Build a Reactor Under a Stadium?*), Related → this long |

## Topic Gate Evidence (`neighbours.py` & `public_search.py`, Retrieved `2026-11-22`)

### 1. Neighbour Gate (`neighbours.py "nuclear reactor" "nuclear power plant"`) — **PASS (`12` Raw / `9` Strictly On-Topic Education Videos `≥1M` Views, `TED-Ed/TED: yes`)**

| # | Views (`2026-11-22`) | Channel | Video ID | Title | Relevance |
|---:|---:|---|---|---|---|
| 1 | `10,888,517` | Kurzgesagt – In a Nutshell | [`Jzfpyo-q-RM`](https://youtu.be/Jzfpyo-q-RM) | *Worst Nuclear Accidents in History* | On-topic nuclear power |
| 2 | `9,916,883` | Kurzgesagt – In a Nutshell | [`EhAemz1v7dQ`](https://youtu.be/EhAemz1v7dQ) | *Do we Need Nuclear Energy to Stop Climate Change?* | On-topic nuclear power |
| 3 | `8,224,844` | Kurzgesagt – In a Nutshell | [`rcOFV4y5z8c`](https://youtu.be/rcOFV4y5z8c) | *Nuclear Energy Explained: How does it work? 1/3* | Strictly on-topic (mechanism) |
| 4 | `7,524,461` | SmarterEveryDay | [`v0afQ6w3Bjw`](https://youtu.be/v0afQ6w3Bjw) | *Refueling a NUCLEAR REACTOR - Smarter Every Day 311* | Strictly on-topic (reactor hardware) |
| 5 | `3,847,436` | SmarterEveryDay | [`JVROsxtjoCw`](https://youtu.be/JVROsxtjoCw) | *I Explored the World's First Nuclear Power Plant (and How It Works) - Smarter Every Day 306* | Strictly on-topic (first plant & mechanism) |
| 6 | `3,332,507` | TED-Ed ★ | [`R7WPEYGr1Vs`](https://youtu.be/R7WPEYGr1Vs) | *How do nuclear power plants work? - M. V. Ramana and Sajan Saini* | Strictly on-topic (mechanism) |
| 7 | `2,322,050` | TEDx Talks ★ | [`ciStnd9Y2ak`](https://youtu.be/ciStnd9Y2ak) | *Why I changed my mind about nuclear power \| Michael Shellenberger* | On-topic nuclear power |
| 8 | `1,576,494` | TEDx Talks ★ | [`-tAsHGFA-74`](https://youtu.be/-tAsHGFA-74) | *How I built a nuclear reactor at the age of 13 \| Jamie Edwards* | Strictly on-topic (building reactor) |
| 9 | `1,243,751` | TED ★ | [`5HL1BEC024g`](https://youtu.be/5HL1BEC024g) | *Taylor Wilson: My radical plan for small nuclear fission reactors* | Strictly on-topic (fission reactors) |

*(3 raw `≥1M` rows transparently excluded: `Kurzgesagt` `mZsaaturR6E` Fusion Power `15,253,905`, `TED-Ed` `GHBb25lzNVM` Nuclear Fallout `2,149,234`, and `TED-Ed` `dcZ0BXJYlUA` Three Gorges hydroelectric dam `1,352,160`.)*

```text
neighbours.py "nuclear reactor" "nuclear power plant"
Words the top neighbours share: nuclear power, michael shellenberger, i built, built a, a nuclear, taylor wilson, the world
TED-Ed/TED neighbour: yes
Big neighbours (≥ 1,000,000 views): 12 (need 3; 9 strictly on-topic nuclear reactor/power; 6 tightly focused on reactor mechanism/build)
Neighbour gate (≥ 3 education videos with 1,000,000+ views): PASS
Raw pull: 02_Video-Projects/130_Fermi-Szilard-Woods-How-Does-A-Nuclear-Reactor-Work/11_Upload-Package/evidence_2026-11-22_neighbours.json
```

### 2. Public Search & Autocomplete Gate (`public_search.py`) — **PASS (`11` Queries / `80` Rows, `0` Collisions)**

- `"how does a nuclear reactor work"` → **`autocomplete = yes`** (`7` suggestions; `Kurzgesagt` `rcOFV4y5z8c` `8,224,844`, `StarTalk` `boUqlyYfUuo` `5,655,988`, `Elearnin` `1U6Nzcv9Vws` `5,024,242`, `TED-Ed` ★ `R7WPEYGr1Vs` `3,332,507`, `Animagraffs` `PRWwXeRIvoI` `825,335`, `ENGIE Belgium` `jpDRfaWYk3I` `739,191`)
- `"chicago pile 1"` → **`autocomplete = yes`** (`4` suggestions; `SciShow` `MLJ1ebNcNLM` `457,251`, `uchicagoarts` `w_6K6arW3h4` `83,009`, `Argonne National Laboratory` `0tKf7R2XncM` `81,230` & `mTPiTJ2bKS0` `56,005`)
- `"enrico fermi nuclear reactor"` → **`autocomplete = yes`** (`Plainly Difficult` `Y0iwe8T-PTc` `607,158`, `SciShow` `MLJ1ebNcNLM` `457,251`, `University of Chicago` `JrOUuzCTnB0` `15,483`)
- `"nuclear chain reaction"` → **`autocomplete = yes`** (`9` suggestions; `StarTalk` `boUqlyYfUuo` `5,655,988`, `Elearnin` `1U6Nzcv9Vws` `5,024,242`, `PhysicsMadeFun` `6_8-U3TZtn0` `132,282`, `Higgsino physics` `ojkeBfOckIk` `128,392`)
- **Exact title collisions:** `0` across Titles A (`8` live rows), B (plain query `8` live rows), C (`8` live rows), and Shorts S01 (`8` live rows) & S02 (`8` live rows).

## Parts

| Part | Plate board | Latest cut | Status |
|---|---|---|---|
| 01 | `07_Edit-Project/parts/part-01_plates_v01.json` | — | todo |
| 02 | | | todo |
| 03 | | | todo |
| 04 | | | todo |
| 05 | | | todo |

Keep this file current on `main`. A STOP (quota, auth, missing VO) is a line here, not an open branch.
