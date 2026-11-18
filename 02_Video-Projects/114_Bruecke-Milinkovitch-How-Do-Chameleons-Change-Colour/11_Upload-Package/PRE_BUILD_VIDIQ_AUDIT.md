# Pre-Build Search & Neighbour Audit — `114_Bruecke-Milinkovitch-How-Do-Chameleons-Change-Colour` (`HOS:114` Proposal)

> **RULE-E GO & RULE G STATUS (`J2944` / `J2945`, `2026-11-16`):**
> - **Rule-E Verdict (`J2945`):** **GO (`95.5 / 100` · `9.55 / 10` Opportunity Score)** — Pre-cleared in `jobs/WIP.json` `next_hos` under **Rule G** (`4 / 4` active HOS slots full: `008`, `009`, `010`, `013`).
> - **Claims Verification Guard:** All historical and scientific claims below are **UNVERIFIED** working notes and must be sourced with verbatim primary-source quotes in `SOURCES.md` and checked by the `facts` lane (`gemini-agy`) when an active HOS WIP slot opens, before any script lock, VO, or picture spend.

## 1. The Discovery Story (Person, Date & Twist — UNVERIFIED)

- **Familiar phenomenon:** How and why chameleons change colour across the visible spectrum.
- **Person, place & date:**
  - **Ernst Wilhelm von Brücke** (1819–1892, Vienna, **1851/1852**): investigates chameleon skin under the microscope (*Untersuchungen über den Farbenwechsel des afrikanischen Chamäleons*, *Denkschriften der Kaiserlichen Akademie der Wissenschaften* `4:179–210`) and describes layered chromatophores and interference effects (`Interferenzfarben`), though textbook accounts for the next 160 years reduce colour change to background camouflage via dark pigment dispersion.
  - **Devon Stuart-Fox & Adnan Moussalli** (University of Melbourne, **January 2008**, *PLoS Biology* `6(1):e25`): use field reflectance spectrometry (`300–700 nm`) on `21` lineages of dwarf chameleons (*Bradypodion*) to prove dramatic colour shifts evolved primarily for **conspicuous social signalling** (male dominance contests and courtship) and **thermoregulation**, not background matching.
  - **Michel C. Milinkovitch & Jérémie Teyssier** (with Sofia V. Saenko & Dirk van der Marel, University of Geneva, **10 March 2015**, *Nature Communications* `6:6368`): discover that panther chameleons (*Furcifer pardalis*) have **zero green or blue pigment** and instead actively tune the lattice spacing (`~30%` expansion) of a 3D **guanine-nanocrystal photonic lattice** (`~127.4 ± 17.8 nm` crystal diameter) inside upper S-iridophore cells (above a passive near-infrared-reflecting D-iridophore thermal shield reflecting `~45%` of direct sunlight energy), proved by shrinking an excised patch of skin in hypertonic salt water so it shifts backwards from red through yellow and green to blue.

---

## 2. Search-First Demand Check (`LEARNINGS.md` Rule 26, Retrieved `2026-11-16`)

- **Exact signed-out YouTube autocomplete phrases (`autocomplete = yes`):** `"how do chameleons change color"`, `"how do chameleons change colour"`, `"why do chameleons change color"`, `"why do chameleons change colour"`
  - **Ranking Video 1:** `SQggDnScsvI` — *How Do Chameleons Change Color?* (`Veritasium`, **`3,475,292` views**, retrieved `2026-11-16`)
  - **Ranking Video 2:** `Dd7UVLkuxC4` — *The REAL Reason Chameleons Change Color* (`Odd Animal Specimens`, **`2,255,381` views**, retrieved `2026-11-16`; plus `The Animal Box Office` `ioblgpA5eTo` **`21,524,829` views**, `Peekaboo Kidz` `y9mr02mE5XE` **`1,488,401` views**, `Deep Look` `Kp9W-_W8rCM` **`1,296,335` views**, `Happy Learning English` `aZuxerppygM` **`1,104,566` views**, `Colossal Cranium` `mGijLaiVqsU` **`429,445` views**, `Seeker` `xWwgOIHSc1o` **`166,206` views**, and `National Geographic` `1xVttpwEREs` **`92,446` views**)
- **Decision:** Candidate primary title = `How Do Chameleons Change Colour? (The Nanocrystal Twist)` (Title A, `56 chars ≤ 70`) / compact `Rule 15` (`≤50 chars`) option `How Do Chameleons Change Colour? (Crystal Proof)` (Title A1, `48 chars`) / `How Do Chameleons Change Colour? The Skin-Crystal Discovery` (Title C, `59 chars`, exact phrase first)
- **Candidate description first 100 chars (unverified until `SOURCES.md` check):** `How do chameleons change colour without green pigment? A 2015 Geneva test found tunable skin crystals.`

---

## 2b. Neighbour pass (blocking · `STUDIO_PLAYBOOK.md` §2 Step 4, Retrieved `2026-11-16`)

Saved in [`evidence_2026-11-16_neighbours.json`](evidence_2026-11-16_neighbours.json) (`bigCount = 9` strictly on-topic education videos `≥1M` views, `hasTed = true`, `gate = PASS`, `0` off-topic rows) and [`evidence_2026-11-16_public_search.json`](evidence_2026-11-16_public_search.json):

| # | Views (`2026-11-16`) | Channel (internal) | id & URL | Title | Subject words we reuse |
|---:|------:|--------------------|----------|-------|------------------------|
| 1 | `8,462,817` | TED-Ed ★ (`neighbours.py`) | [`gKfjHTk8KrY`](https://youtu.be/gKfjHTk8KrY) | *History’s deadliest colors - J. V. Maranto* | `color`, `pigment`, `green`, `history` |
| 2 | `3,540,205` | TED-Ed ★ (`neighbours.py`) | [`_r4c2NT4naQ`](https://youtu.be/_r4c2NT4naQ) | *The science of skin color - Angela Koine Flynn* | `skin color`, `melanin`, `pigment`, `light` |
| 3 | `3,475,292` | Veritasium (`neighbours.py` & `public_search.py`) | [`SQggDnScsvI`](https://youtu.be/SQggDnScsvI) | *How Do Chameleons Change Color?* | `how do chameleons change color`, `nanocrystals`, `iridophores` |
| 4 | `3,307,937` | Tom Scott (`neighbours.py`) | [`rApTzWboLrA`](https://youtu.be/rApTzWboLrA) | *The library of rare colors* | `rare colors`, `pigment`, `color` |
| 5 | `2,255,381` | Odd Animal Specimens (`public_search.py`) | [`Dd7UVLkuxC4`](https://youtu.be/Dd7UVLkuxC4) | *The REAL Reason Chameleons Change Color* | `why chameleons change color`, `camouflage myth`, `rivals` |
| 6 | `1,906,840` | TED-Ed ★ (`neighbours.py`) | [`rkRbebvoYqI`](https://youtu.be/rkRbebvoYqI) | *What color is Tuesday? Exploring synesthesia - Richard E. Cytowic* | `color`, `perception`, `wavelength` |
| 7 | `1,672,051` | TED-Ed ★ (`neighbours.py`) | [`l8_fZPHasdo`](https://youtu.be/l8_fZPHasdo) | *How we see color - Colm Kelleher* | `how we see color`, `light wavelengths`, `reflection` |
| 8 | `1,488,401` | Peekaboo Kidz (`public_search.py`) | [`y9mr02mE5XE`](https://youtu.be/y9mr02mE5XE) | *Why does a Chameleon change colors? \| The Dr. Binocs Show* | `why does a chameleon change colors`, `camouflage`, `skin` |
| 9 | `1,326,018` | TED-Ed ★ (`neighbours.py`) | [`yRwoReHd7XU`](https://youtu.be/yRwoReHd7XU) | *What is the rarest color in nature? - Victoria Hwang* | `structural color`, `nanocrystals`, `pigment vs crystal` |
| 10 | `1,296,335` | Deep Look (`public_search.py`) | [`Kp9W-_W8rCM`](https://youtu.be/Kp9W-_W8rCM) | *Nature's Mood Rings: How Chameleons Really Change Color \| Deep Look* | `how chameleons really change color`, `crystals`, `skin` |
| 11 | `1,156,372` | SciShow Kids (`neighbours.py`) | [`YOIRci0CKzg`](https://youtu.be/YOIRci0CKzg) | *Camouflage: Animal Hide & Seek* | `camouflage`, `color`, `animals` |
| 12 | `1,110,173` | TED-Ed ★ (`neighbours.py`) | [`UZ5UGnU7oOI`](https://youtu.be/UZ5UGnU7oOI) | *What is color? - Colm Kelleher* | `visible spectrum`, `wavelengths`, `light` |

**Proposed subject-only tags (8 tags, zero channel names):**  
`how do chameleons change color, why do chameleons change color, chameleon nanocrystals, structural color in nature, michel milinkovitch chameleon, iridophores guanine crystals, animal camouflage myth, history of science experiments`

---

## 3. Title ABC (score before VO)

| | Title | Chars | Collisions (`2026-11-16`) | Role & Notes | Keep? |
|---|-------|------:|-----------:|--------------|-------|
| A | `How Do Chameleons Change Colour? (The Nanocrystal Twist)` | 56 | 0 | **Main (`LEARNINGS.md` Rules 1, 23, 26):** Starts verbatim with exact autocomplete question `"how do chameleons change colour"` + nanocrystal experimental twist | **Keep (Primary Proposal)** |
| A1 | `How Do Chameleons Change Colour? (Crystal Proof)` | 48 | 0 | **Compact `Rule 15` (`≤50 chars`) & `Rule 26` Option:** Exact autocomplete phrase first + `48 chars ≤ 50` | **Keep (Compact Option)** |
| B | `Chameleons Have No Green Pigment (The 2015 Crystal Proof)` | 57 | 0 | **Test & Compare (`Rule 23`):** Leads with the zero-green-pigment surprise + 2015 Geneva proof | **Keep (T&C Arm 2)** |
| B1 | `Chameleons Have No Green Pigment (Crystal Proof)` | 48 | 0 | **Compact `Rule 15` (`≤50 chars`) T&C Option:** Zero-green-pigment surprise in `48 chars ≤ 50` | **Keep (Compact T&C Option)** |
| C | `How Do Chameleons Change Colour? The Skin-Crystal Discovery` | 59 | 0 | **Rule 26 Variant (`≤70 chars`):** Starts verbatim with exact autocomplete phrase + skin-crystal discovery story | **Keep (T&C Arm 3)** |
| Reject | `Photonic Guanine Lattices in Furcifer pardalis \| History of Science` | 67 | — | Academic jargon + forbidden series suffix | **Reject** |

---

## 3b. Script reviewer (blocking before VO — not run; proposal only)

- [x] Rule-E topic go/no-go review passed (`J2945`, **GO `95.5 / 100`**, [`TOPIC_GO_NO_GO_SHEET.md`](TOPIC_GO_NO_GO_SHEET.md) & [`TOPIC_OPPORTUNITY_SCORE.md`](TOPIC_OPPORTUNITY_SCORE.md))
- [ ] `SOURCES.md` exact quotes + `facts` lane verification completed (required before script lock when an active HOS WIP slot opens)
- [ ] Score ≥ **90 / 100** (`npm run review:script`)
