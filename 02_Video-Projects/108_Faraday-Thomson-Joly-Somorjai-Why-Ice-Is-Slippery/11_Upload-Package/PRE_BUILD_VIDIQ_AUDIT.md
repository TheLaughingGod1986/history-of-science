# Pre-Build vidIQ & Public Search Audit — `108_Faraday-Thomson-Joly-Somorjai-Why-Ice-Is-Slippery` (`HOS:108` — Rule-E GO in `next_hos`)

> **PROPOSAL, RULE-E GO & VERIFICATION STATUS (`J2891` / `J2917`, `2026-11-16`):**
> - **Rule-E Topic Go/No-Go Review (`J2917`): GO (`94 / 100` · `9.40 / 10` Opportunity Score).** Pre-cleared in `jobs/WIP.json` `next_hos` under Rule G (`active` has `4 / 4` HOS slots full: `HOS:008`, `HOS:009`, `HOS:010`, `HOS:013`). See [`TOPIC_GO_NO_GO_SHEET.md`](TOPIC_GO_NO_GO_SHEET.md) and [`TOPIC_OPPORTUNITY_SCORE.md`](TOPIC_OPPORTUNITY_SCORE.md).
> - **All Claims Unverified:** Every historical and scientific claim below (Faraday's 7 June 1850 Royal Institution lecture on two wet ice blocks welding together and an intrinsic liquid-like surface film, Tyndall & Huxley's 1857 coinage of *regelation*, James Thomson and William Thomson / Lord Kelvin's 1849–1850 pressure-melting thermodynamic argument, John Joly's December 1886 skate-blade pressure calculation, Frank Philip Bowden and T. P. Hughes's 1939 Jungfraujoch Alpine ice-cave and Cambridge cold-lab friction experiments, and Gabor Somorjai's 1996–2002 LEED/AFM/SFG surface premelting proof) is **UNVERIFIED** and **must not be locked into a script or recorded in VO** until verified with exact quotes in `SOURCES.md` and cleared by the `facts` lane (`gemini-agy`).

---

## 1. Angle & Contract Check (`studio/RULES.md` + `LEARNINGS.md` Rules 1, 22, 23, 26)

| Check | Result |
|---|---|
| Channel | `@HistoryOfScienceYT` (`history-of-science`) |
| Film Number & Slug | `108_Faraday-Thomson-Joly-Somorjai-Why-Ice-Is-Slippery` (`HOS:108`) |
| Core Everyday Question | *Why is ice slippery — and why did physics textbooks print the wrong pressure-melting explanation for more than a century after Michael Faraday had already demonstrated the real answer with two ice cubes in 1850?* |
| Rule 26 Autocomplete Phrase | `"why is ice slippery"` (`autocomplete = yes`, 3 suggestions in signed-out YouTube GB autocomplete: `why is ice slippery`, `why is ice slippery feynman`, `why is ice so slippery`) and `"how does ice skating work"` (`autocomplete = yes`, 6 suggestions in signed-out YouTube GB autocomplete: `how does ice skating work`, `how does figure skating work`, `how do ice rinks work`, `how does figure skating scoring work`, `how do figure skating competitions work`, `how ice skating works`) |
| Rule 26(a) Two Ranking Videos (`≥10,000` views) | 1. **Be Smart** — [`yjSf7Yh9UZc`](https://youtu.be/yjSf7Yh9UZc) *The Strange and Unexpected Reason Ice is Slippery* (**`1,158,527` views**, retrieved `2026-11-15`)<br>2. **Veritasium** — [`Stx6kLd9dYI`](https://youtu.be/Stx6kLd9dYI) *Why Is Ice Slippery?* (**`806,131` views**, retrieved `2026-11-15`; plus **Dr Ben Miles** [`20zyW0qoSTE`](https://youtu.be/20zyW0qoSTE) *We FINALLY Proved Why Ice Is Slippery* **`810,742` views**, **Veritasium** [`gM3zP72-rJE`](https://youtu.be/gM3zP72-rJE) *Does Pressure Melt Ice?* **`3,046,453` views**, and **SmarterEveryDay** [`qd4CVvItJlo`](https://youtu.be/qd4CVvItJlo) *COLD HARD SCIENCE.The Physics of Skating on Ice (With SlowMo) - Smarter Every Day 110* **`5,991,243` views**) |
| Neighbour Gate (`neighbours.py`) | **PASS (`2026-11-15` / `2026-11-16`)** — **`9` education videos `≥1,000,000` views in `neighbours.py`** (`TED-Ed/TED: yes`, `7` strictly on-topic ice/states-of-matter videos led by `TED-Ed` `2,049,194` `UukRgqzk-KE` *Why does ice float in water?*, `FuseSchool` `1,867,278` `xYU7RSoOZ0U` *Changes of State*, `TED-Ed` `1,342,673` `ASLUY2U1M-8` *How polarity makes water behave strangely*, `Veritasium` `1,329,655` `KCL8zqjXbME` *States of Matter*, `FuseSchool` `1,203,396` `21CR01rlmv4` *States Of Matter*, `Be Smart` `1,158,527` `yjSf7Yh9UZc` *The Strange and Unexpected Reason Ice is Slippery*, `Cognito` `1,017,499` `hkBrw2fG75U` *GCSE Chemistry - States of Matter & Changing State*, plus `4` additional `≥1M` on-topic education videos in `public_search.py`: `SmarterEveryDay` `5,991,243` `qd4CVvItJlo`, `TED-Ed` `3,735,948` `PgSRAsgrKmg` *How do crystals work? - Graham Baird*, `Veritasium` `3,046,453` `gM3zP72-rJE` *Does Pressure Melt Ice?*, `minutephysics` `2,513,630` `_bcfxty39Cw` *Freezing water expands. What if you don't let it?*). Raw outputs saved at [`evidence_2026-11-15_neighbours.json`](evidence_2026-11-15_neighbours.json) and [`evidence_2026-11-15_public_search.json`](evidence_2026-11-15_public_search.json). |

---

## 2. Keyword & Public Search Table (`public_search.py`, Retrieved `2026-11-15` / `2026-11-16`)

Saved in [`evidence_2026-11-15_public_search.json`](evidence_2026-11-15_public_search.json):

| Query / Candidate Title | Autocomplete (`2026-11-15` / `16`) | Top Public Results & Views (GB) | Role | Decision |
|---|---|---|---|---|
| `why is ice slippery` | **yes** (3 suggestions: `why is ice slippery`, `why is ice slippery feynman`, `why is ice so slippery`) | `Be Smart` [`yjSf7Yh9UZc`](https://youtu.be/yjSf7Yh9UZc) **`1,158,527`** · `Dr Ben Miles` [`20zyW0qoSTE`](https://youtu.be/20zyW0qoSTE) **`810,742`** · `Veritasium` [`Stx6kLd9dYI`](https://youtu.be/Stx6kLd9dYI) **`806,131`** · `SciShow` [`WZV8gM2_MFQ`](https://youtu.be/WZV8gM2_MFQ) **`217,761`** · `StarTalk` [`Zm3Ef-i-Mpk`](https://youtu.be/Zm3Ef-i-Mpk) **`142,621`** | Primary search phrase (Rule 26) | **Lock as primary keyword** |
| `how does ice skating work` | **yes** (6 suggestions: `how does ice skating work`, `how does figure skating work`, `how do ice rinks work`, `how does figure skating scoring work`, `how do figure skating competitions work`, `how ice skating works`) | `SmarterEveryDay` [`qd4CVvItJlo`](https://youtu.be/qd4CVvItJlo) **`5,991,243`** · `How To Inline Skate` [`-vKYvvJ_-Hg`](https://youtu.be/-vKYvvJ_-Hg) **`1,618,477`** · `Olympic Games` [`J1RC2p6UOq4`](https://youtu.be/J1RC2p6UOq4) **`562,311`** · `Cathy Ding` [`6s8zNzJ-BaU`](https://youtu.be/6s8zNzJ-BaU) **`90,920`** | Secondary everyday search phrase | **Keep in description & tags** |
| `does pressure melt ice` | no | `Veritasium` [`gM3zP72-rJE`](https://youtu.be/gM3zP72-rJE) **`3,046,453`** · `minutephysics` [`_bcfxty39Cw`](https://youtu.be/_bcfxty39Cw) **`2,513,630`** · `OSU Demo Lab` **`27,201`** | Core mechanism neighbour query | **Keep in description & tags** |
| `how do crystals work` | **yes** (10 suggestions) | `TED-Ed` [`PgSRAsgrKmg`](https://youtu.be/PgSRAsgrKmg) **`3,735,948`** (*How do crystals work? - Graham Baird*) | Crystal lattice neighbour query | **Keep subject words (`crystal`, `lattice`)** |
| `Why Is Ice Slippery? (The 150-Year Textbook Myth)` | no (Title A candidate, `49 chars`) | `The Mundane Lab` `12` · `Long Answer Lab` `4` · `Quantayo` `47` · `Watium` `76` · `Scio 3D` `95` | Long Title A (`0` exact collisions) | **Keep (Primary Proposal)** |
| `The 150-Year Textbook Myth About Why Ice Is Slippery` | no (Title B candidate, `52 chars`) | `The Mundane Lab` `12` · `Scio 3D` `95` · `Made Of Secrets` `1` · `Quantayo` `47` · `Long Answer Lab` `4` | Long Title B (`0` exact collisions, T&C Arm 2) | **Keep (T&C Arm 2)** |
| `Why Is Ice Slippery? How Faraday Beat a 150-Year Myth` | no (Title C candidate, `53 chars`) | `Clear Cut, Big Science` `10` · `Dr Ben Miles` `810,742` · `Curious Horizon` `81` · `Quark Street` `101` · `금경애` `135` | Long Title C (`0` exact collisions, exact phrase first) | **Keep (T&C Arm 3)** |
| `Why Do Two Ice Cubes Freeze Together When Pressed?` | no (Short `S01` candidate, `50 chars`) | `Flurida Appliances` `34,142` · `The Vetta Group` `80,743` · `Lawrence Jacobsen` `18,385` · `Blulines Plus One` `14` | Short `S01` candidate question title (`0` exact collisions) | **Keep** |
| `Can Skate Pressure Really Melt Ice at Minus 20 Degrees?` | no (Short `S02` candidate, `55 chars`) | `Dots & Dimensions` `0` · `Turns Out` `109` · `JRE Clips` `124,100` · `Veritasium` `3,046,449` · `Michel van Biezen` `9,167` | Short `S02` candidate question title (`0` exact collisions) | **Keep** |

- **Rule 26(a) Exact Phrase & Two Ranking Videos (`2026-11-15`):**
  - **Phrase:** `"why is ice slippery"` / `"how does ice skating work"`
  - **Ranking Video 1:** `yjSf7Yh9UZc` — *The Strange and Unexpected Reason Ice is Slippery* (`Be Smart`, **`1,158,527` views**, retrieved `2026-11-15`)
  - **Ranking Video 2:** `Stx6kLd9dYI` — *Why Is Ice Slippery?* (`Veritasium`, **`806,131` views**, retrieved `2026-11-15`; plus `Dr Ben Miles` `20zyW0qoSTE` **`810,742` views**, `Veritasium` `gM3zP72-rJE` **`3,046,453` views**, and `SmarterEveryDay` `qd4CVvItJlo` **`5,991,243` views**)
- **Decision:** Candidate primary title = `Why Is Ice Slippery? (The 150-Year Textbook Myth)` (Title A, `49 chars`) / `Why Is Ice Slippery? How Faraday Beat a 150-Year Myth` (Title C, `53 chars`, exact phrase first)
- **Candidate description first 100 chars (unverified until `SOURCES.md` check):** `Why is ice slippery, and why did physics textbooks teach the wrong pressure-melting answer for 150 years?`

---

## 2b. Neighbour pass (blocking · `STUDIO_PLAYBOOK.md` §2 Step 4, Retrieved `2026-11-15` / `2026-11-16`)

Saved in [`evidence_2026-11-15_neighbours.json`](evidence_2026-11-15_neighbours.json) and [`evidence_2026-11-15_public_search.json`](evidence_2026-11-15_public_search.json):

| # | Views (`2026-11-15` / `16`) | Channel (internal) | id & URL | Title | Subject words we reuse |
|---:|------:|--------------------|----------|-------|------------------------|
| 1 | `5,991,243` | SmarterEveryDay (`public_search.py`) | [`qd4CVvItJlo`](https://youtu.be/qd4CVvItJlo) | *COLD HARD SCIENCE.The Physics of Skating on Ice (With SlowMo) - Smarter Every Day 110* | `ice`, `skating on ice`, `physics`, `blade` |
| 2 | `3,735,948` | TED-Ed ★ (`public_search.py`) | [`PgSRAsgrKmg`](https://youtu.be/PgSRAsgrKmg) | *How do crystals work? - Graham Baird* | `crystal`, `lattice`, `surface`, `molecules` |
| 3 | `3,046,453` | Veritasium (`public_search.py`) | [`gM3zP72-rJE`](https://youtu.be/gM3zP72-rJE) | *Does Pressure Melt Ice?* | `pressure`, `melt ice`, `regelation`, `freezing point` |
| 4 | `2,513,630` | minutephysics (`public_search.py`) | [`_bcfxty39Cw`](https://youtu.be/_bcfxty39Cw) | *Freezing water expands. What if you don't let it?* | `freezing water`, `ice`, `pressure`, `phase diagram` |
| 5 | `2,049,194` | TED-Ed ★ (`neighbours.py`) | [`UukRgqzk-KE`](https://youtu.be/UukRgqzk-KE) | *Why does ice float in water? - George Zaidan and Charles Morton* | `ice`, `water`, `hydrogen bonds`, `crystal lattice` |
| 6 | `1,867,278` | FuseSchool (`neighbours.py`) | [`xYU7RSoOZ0U`](https://youtu.be/xYU7RSoOZ0U) | *Changes of State \| Matter \| Physics \| FuseSchool* | `melting`, `freezing`, `states of matter` |
| 7 | `1,342,673` | TED-Ed ★ (`neighbours.py`) | [`ASLUY2U1M-8`](https://youtu.be/ASLUY2U1M-8) | *How polarity makes water behave strangely - Christina Kleinberg* | `water`, `polarity`, `ice`, `surface` |
| 8 | `1,329,655` | Veritasium (`neighbours.py`) | [`KCL8zqjXbME`](https://youtu.be/KCL8zqjXbME) | *States of Matter* | `solid`, `liquid`, `phase transition`, `ice` |
| 9 | `1,203,396` | FuseSchool (`neighbours.py`) | [`21CR01rlmv4`](https://youtu.be/21CR01rlmv4) | *States Of Matter - Solids, Liquids & Gases \| Properties of Matter \| Chemistry \| FuseSchool* | `solids`, `liquids`, `melting`, `ice` |
| 10 | `1,158,527` | Be Smart (`neighbours.py`) | [`yjSf7Yh9UZc`](https://youtu.be/yjSf7Yh9UZc) | *The Strange and Unexpected Reason Ice is Slippery* | `why is ice slippery`, `pressure melting`, `faraday`, `friction`, `premelting` |
| 11 | `1,017,499` | Cognito (`neighbours.py`) | [`hkBrw2fG75U`](https://youtu.be/hkBrw2fG75U) | *GCSE Chemistry - States of Matter & Changing State* | `particles`, `solid`, `liquid`, `melting` |

*(Note: `evidence_2026-11-15_neighbours.json` also contains two general water-scarcity/hydration `TED-Ed` videos from the `"states of matter water"` query — `9iMGFqMmUFs` *What would happen if you didn't drink water?* `23,946,681` views and `OCzYdNSJF-k` *Are we running out of clean water?* `1,116,740` views — which are excluded from the numbered on-topic table above; the `7` remaining `≥1M` videos in `neighbours.json` plus the `4` `≥1M` videos in `public_search.json` give **`11` strictly on-topic education videos `≥1,000,000` views**.)*

**Proposed subject-only tags (8 tags, zero channel names):**  
`why is ice slippery, how does ice skating work, michael faraday regelation ice, pressure melting ice myth, john joly ice skating, surface premelting ice, history of physics experiments, lord kelvin james thomson ice`

---

## 3. Title ABC (score before VO)

| | Title | Chars | Collisions (`2026-11-15` / `16`) | Role & Notes | Keep? |
|---|-------|------:|-----------:|--------------|-------|
| A | `Why Is Ice Slippery? (The 150-Year Textbook Myth)` | 49 | 0 | **Main (`LEARNINGS.md` Rules 1, 15, 23, 26):** Starts verbatim with exact autocomplete question `"why is ice slippery"` + concrete textbook-myth stakes (`≤50 chars`) | **Keep (Primary Proposal)** |
| B | `The 150-Year Textbook Myth About Why Ice Is Slippery` | 52 | 0 | **Test & Compare (`Rule 23`):** Leads with the 150-year textbook error + exact search phrase | **Keep (T&C Arm 2)** |
| C | `Why Is Ice Slippery? How Faraday Beat a 150-Year Myth` | 53 | 0 | **Rule 26 Variant (`≤70 chars`):** Starts verbatim with exact autocomplete phrase `"why is ice slippery"` + Faraday discovery hook | **Keep (T&C Arm 3)** |
| Reject | `Surface Premelting and Regelation of Crystalline Ice \| History of Science` | 73 | — | Academic jargon + forbidden series suffix | **Reject** |

---

## 3b. Script reviewer (blocking before VO — not run; proposal only)

- [x] Rule-E topic go/no-go review passed (`J2917`, `94 / 100` · `9.40 / 10` Opportunity Score, pre-cleared in `next_hos`)
- [ ] `SOURCES.md` exact quotes + `facts` lane verification completed (required before script lock)
- [ ] Score ≥ **90 / 100** (`npm run review:script`)
