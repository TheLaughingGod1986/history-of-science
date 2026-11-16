# Pre-Build vidIQ & Public Search Audit — `108_Faraday-Thomson-Joly-Somorjai-Why-Ice-Is-Slippery` (`HOS:108` Proposal)

> **PROPOSAL & VERIFICATION STATUS (`J2891`, `2026-11-15`):**
> - **Backlog Proposal Only (`next_hos`):** This audit accompanies the topic proposal for `HOS:108` (`108_Faraday-Thomson-Joly-Somorjai-Why-Ice-Is-Slippery`) waiting in `jobs/WIP.json` `next_hos` under Rule G (`active_hos` has 3 active films).
> - **All Claims Unverified:** Every historical and scientific claim below (Faraday's 7 June 1850 Royal Institution lecture on wet ice regelation and an intrinsic liquid-like surface film, James Thomson and William Thomson / Lord Kelvin's 1849–1850 pressure-melting thermodynamic argument, John Joly's 1886 skate-blade pressure calculation, Frank Philip Bowden and T. P. Hughes's 1939 Jungfraujoch Alpine ice-cave friction experiments, and Gabor Somorjai's 1996–2002 LEED/AFM surface premelting proof) is **UNVERIFIED** and **must not be locked into a script or recorded in VO** until verified with exact quotes in `SOURCES.md` and cleared by the `facts` lane (`gemini-agy`).

---

## 1. Angle & Contract Check (`studio/RULES.md` + `LEARNINGS.md` Rules 1, 22, 23, 26)

| Check | Result |
|---|---|
| Channel | `@HistoryOfScienceYT` (`history-of-science`) |
| Film Number & Slug | `108_Faraday-Thomson-Joly-Somorjai-Why-Ice-Is-Slippery` (`HOS:108`) |
| Core Everyday Question | *Why is ice slippery — and why did physics textbooks print the wrong pressure-melting explanation for more than a century after Michael Faraday had already demonstrated the real answer with two ice cubes in 1850?* |
| Rule 26 Autocomplete Phrase | `"why is ice slippery"` (`autocomplete = yes`, 6 suggestions in signed-out YouTube autocomplete on `2026-11-15`) and `"how does ice skating work"` (`autocomplete = yes`, 4 suggestions on `2026-11-15`) |
| Rule 26(a) Two Ranking Videos (`≥10,000` views) | 1. **Be Smart** — [`yjSf7Yh9UZc`](https://youtu.be/yjSf7Yh9UZc) *The Strange and Unexpected Reason Ice is Slippery* (**`1,158,527` views**, retrieved `2026-11-15`)<br>2. **Veritasium** — [`Stx6kLd9dYI`](https://youtu.be/Stx6kLd9dYI) *Why Is Ice Slippery?* (**`806,131` views**, retrieved `2026-11-15`; plus **Dr Ben Miles** [`fzhT-hB8w0w`](https://youtu.be/fzhT-hB8w0w) *Why Nobody Can Agree Why Ice Is Slippery* **`810,742` views** and **SmarterEveryDay** [`N7rR82Zk17U`](https://youtu.be/N7rR82Zk17U) *How Ice Skates Work (Slow Motion)* **`5,991,243` views**) |
| Neighbour Gate (`neighbours.py`) | **PASS (`2026-11-15`)** — **`9` education videos `≥1,000,000` views** (`TED-Ed/TED: yes`, topped by `TED-Ed` `23.95M` `9iMGFqMmUFs`, `TED-Ed` `2.05M` `UukRgqzk-KE`, `FuseSchool` `1.87M` `xYU7RSoOZ0U`, `TED-Ed` `1.34M` `ASLUY2U1M-8`, `Veritasium` `1.33M` `KCL8zqjXbME`, `FuseSchool` `1.20M` `21CR01rlmv4`, `Be Smart` `1.16M` `yjSf7Yh9UZc`, `TED-Ed` `1.12M` `OCzYdNSJF-k`, `Cognito` `1.02M` `hkBrw2fG75U`). Raw output saved at [`evidence_2026-11-15_neighbours.json`](evidence_2026-11-15_neighbours.json). |

---

## 2. Keyword & Public Search Table (`public_search.py`, Retrieved `2026-11-15`)

Saved in [`evidence_2026-11-15_public_search.json`](evidence_2026-11-15_public_search.json):

| Query / Candidate Title | Autocomplete (`2026-11-15`) | Top Public Results & Views (`2026-11-15`) | Role | Decision |
|---|---|---|---|---|
| `why is ice slippery` | **yes** (6 suggestions: `why is ice slippery`, `why is ice slippery veritasium`, `why is ice slippery physics`, `why is ice slippery sci show`, `why is ice slippery Hank green`, `why is ice slippery explained`) | `Be Smart` [`yjSf7Yh9UZc`](https://youtu.be/yjSf7Yh9UZc) **`1,158,527`** · `Dr Ben Miles` [`fzhT-hB8w0w`](https://youtu.be/fzhT-hB8w0w) **`810,742`** · `Veritasium` [`Stx6kLd9dYI`](https://youtu.be/Stx6kLd9dYI) **`806,131`** | Primary search phrase (Rule 26) | **Lock as primary keyword** |
| `how does ice skating work` | **yes** (4 suggestions: `how does ice skating work`, `how does figure skating work in the olympics`, `how does figure skating work`, `how does speed skating work`) | `SmarterEveryDay` [`N7rR82Zk17U`](https://youtu.be/N7rR82Zk17U) **`5,991,243`** · `Vox` **`4,734,881`** · `Olympics` **`1,250,023`** | Secondary everyday search phrase | **Keep in description & tags** |
| `Why Is Ice Slippery? (The 150-Year Textbook Myth)` | — (Title A candidate, `49 chars`) | `Be Smart` `1,158,527` · `Dr Ben Miles` `810,742` · `Veritasium` `806,131` | Long Title A (`0` exact collisions) | **Keep (Primary Proposal)** |
| `The 150-Year Textbook Myth About Why Ice Is Slippery` | — (Title B candidate, `52 chars`) | `Be Smart` `1,158,527` · `Dr Ben Miles` `810,742` · `Veritasium` `806,131` | Long Title B (`0` exact collisions, T&C Arm 2) | **Keep (T&C Arm 2)** |
| `Why Is Ice Slippery? How Faraday Beat a 150-Year Myth` | — (Title C candidate, `53 chars`) | `Be Smart` `1,158,527` · `Dr Ben Miles` `810,742` · `Veritasium` `806,131` | Long Title C (`0` exact collisions, exact phrase first) | **Keep (T&C Arm 3)** |
| `Why Do Two Ice Cubes Freeze Together When Pressed?` | — (Short `S01` candidate, `50 chars`) | `Action Lab` / physics demos (`0` exact collisions) | Short `S01` candidate question title (`0` exact collisions) | **Keep** |
| `Can Skate Pressure Really Melt Ice at Minus 20 Degrees?` | — (Short `S02` candidate, `55 chars`) | `Be Smart` `1,158,527` · `Veritasium` `806,131` | Short `S02` candidate question title (`0` exact collisions) | **Keep** |

- **Rule 26(a) Exact Phrase & Two Ranking Videos (`2026-11-15`):**
  - **Phrase:** `"why is ice slippery"` / `"how does ice skating work"`
  - **Ranking Video 1:** `yjSf7Yh9UZc` — *The Strange and Unexpected Reason Ice is Slippery* (`Be Smart`, **`1,158,527` views**, retrieved `2026-11-15`)
  - **Ranking Video 2:** `Stx6kLd9dYI` — *Why Is Ice Slippery?* (`Veritasium`, **`806,131` views**, retrieved `2026-11-15`; plus `Dr Ben Miles` `fzhT-hB8w0w` **`810,742` views** and `SmarterEveryDay` `N7rR82Zk17U` **`5,991,243` views**)
- **Decision:** Candidate primary title = `Why Is Ice Slippery? (The 150-Year Textbook Myth)` (Title A, `49 chars`) / `Why Is Ice Slippery? How Faraday Beat a 150-Year Myth` (Title C, `53 chars`, exact phrase first)
- **Candidate description first 100 chars (unverified until `SOURCES.md` check):** `Why is ice slippery, and why did physics textbooks teach the wrong pressure-melting answer for 150 years?`

---

## 2b. Neighbour pass (blocking · `STUDIO_PLAYBOOK.md` §2 Step 4, Retrieved `2026-11-15`)

Saved in [`evidence_2026-11-15_neighbours.json`](evidence_2026-11-15_neighbours.json) and [`evidence_2026-11-15_public_search.json`](evidence_2026-11-15_public_search.json):

| # | Views (`2026-11-15`) | Channel (internal) | id & URL | Title | Subject words we reuse |
|---:|------:|--------------------|----------|-------|------------------------|
| 1 | `23,950,623` | TED-Ed ★ (`neighbours.py`) | [`9iMGFqMmUFs`](https://youtu.be/9iMGFqMmUFs) | *What would happen if you didn't drink water? - Mia Nacamulli* | `water`, `molecules` |
| 2 | `5,991,243` | SmarterEveryDay (`public_search.py`) | [`N7rR82Zk17U`](https://youtu.be/N7rR82Zk17U) | *How Ice Skates Work (Slow Motion)* | `ice`, `ice skates`, `blade`, `melting` |
| 3 | `2,053,167` | TED-Ed ★ (`neighbours.py`) | [`UukRgqzk-KE`](https://youtu.be/UukRgqzk-KE) | *Why does ice float in water? - George Zaidan and Charles Morton* | `ice`, `water`, `hydrogen bonds`, `crystal lattice` |
| 4 | `1,867,406` | FuseSchool (`neighbours.py`) | [`xYU7RSoOZ0U`](https://youtu.be/xYU7RSoOZ0U) | *Changes of State \| Matter \| Physics \| FuseSchool* | `melting`, `freezing`, `states of matter` |
| 5 | `1,338,064` | TED-Ed ★ (`neighbours.py`) | [`ASLUY2U1M-8`](https://youtu.be/ASLUY2U1M-8) | *How polarity makes water behave strangely - Christina Kleinberg* | `water`, `polarity`, `ice`, `surface` |
| 6 | `1,326,829` | Veritasium (`neighbours.py`) | [`KCL8zqjXbME`](https://youtu.be/KCL8zqjXbME) | *States of Matter* | `solid`, `liquid`, `phase transition`, `ice` |
| 7 | `1,197,225` | FuseSchool (`neighbours.py`) | [`21CR01rlmv4`](https://youtu.be/21CR01rlmv4) | *Specific Latent Heat \| Matter \| Physics \| FuseSchool* | `melting`, `ice`, `latent heat` |
| 8 | `1,158,527` | Be Smart (`neighbours.py`) | [`yjSf7Yh9UZc`](https://youtu.be/yjSf7Yh9UZc) | *The Strange and Unexpected Reason Ice is Slippery* | `why is ice slippery`, `pressure melting`, `faraday`, `friction`, `premelting` |
| 9 | `1,123,773` | TED-Ed ★ (`neighbours.py`) | [`OCzYdNSJF-k`](https://youtu.be/OCzYdNSJF-k) | *How do crystals work? - Graham Baird* | `crystal`, `lattice`, `surface` |
| 10 | `1,021,477` | Cognito (`neighbours.py`) | [`hkBrw2fG75U`](https://youtu.be/hkBrw2fG75U) | *GCSE Physics - Particle Theory & States of Matter #25* | `particles`, `solid`, `liquid`, `melting` |

**Proposed subject-only tags (8 tags, zero channel names):**  
`why is ice slippery, how does ice skating work, michael faraday regelation ice, pressure melting ice myth, john joly ice skating, surface premelting ice, history of physics experiments, lord kelvin james thomson ice`

---

## 3. Title ABC (score before VO)

| | Title | Chars | Collisions (`2026-11-15`) | Role & Notes | Keep? |
|---|-------|------:|-----------:|--------------|-------|
| A | `Why Is Ice Slippery? (The 150-Year Textbook Myth)` | 49 | 0 | **Main (`LEARNINGS.md` Rules 1, 23, 26):** Starts verbatim with exact autocomplete question `"why is ice slippery"` + concrete textbook-myth stakes | **Keep (Primary Proposal)** |
| B | `The 150-Year Textbook Myth About Why Ice Is Slippery` | 52 | 0 | **Test & Compare (`Rule 23`):** Leads with the 150-year textbook error + exact search phrase | **Keep (T&C Arm 2)** |
| C | `Why Is Ice Slippery? How Faraday Beat a 150-Year Myth` | 53 | 0 | **Rule 26 Variant (`≤70 chars`):** Starts verbatim with exact autocomplete phrase `"why is ice slippery"` + Faraday discovery | **Keep (T&C Arm 3)** |
| Reject | `Surface Premelting and Regelation of Crystalline Ice \| History of Science` | 73 | — | Academic jargon + forbidden series suffix | **Reject** |

---

## 3b. Script reviewer (blocking before VO — not run; proposal only)

- [ ] `SOURCES.md` exact quotes + `facts` lane verification completed (required before script lock)
- [ ] Score ≥ **90 / 100** (`npm run review:script`)
