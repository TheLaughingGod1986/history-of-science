# Pre-Build Search & Neighbour Audit — `114_Bruecke-Milinkovitch-How-Do-Chameleons-Change-Colour` (`HOS:114` Proposal)

> **PROPOSAL STATUS (`J2944`, `2026-11-16`):** Waiting in `jobs/WIP.json` `next_hos` (Rule G). All historical and scientific claims below are **UNVERIFIED** working notes and must be sourced in `SOURCES.md` and checked by the `facts` lane before script lock.

## 1. The Discovery Story (Person, Date & Twist — UNVERIFIED)

- **Familiar phenomenon:** How and why chameleons change colour across the visible spectrum.
- **Person, place & date:**
  - **Ernst Wilhelm von Brücke** (1819–1892, Vienna, **1851**): investigates chameleon skin under the microscope (*Untersuchungen über den Farbenwechsel des afrikanischen Chamäleons*) and describes layered chromatophores and interference effects, though textbook accounts for the next 160 years reduce colour change to background camouflage via dark pigment dispersion.
  - **Devon Stuart-Fox & Adnan Moussalli** (University of Melbourne, **January 2008**, *PLoS Biology*): use field reflectance spectrometry on 21 lineages of dwarf chameleons (*Bradypodion*) to prove dramatic colour shifts evolved primarily for **conspicuous social signalling** (male dominance contests and courtship) and **thermoregulation**, not background matching.
  - **Michel C. Milinkovitch & Jérémie Teyssier** (University of Geneva, **March 2015**, *Nature Communications*): discover that panther chameleons (*Furcifer pardalis*) have **zero green or blue pigment** and instead actively tune the spacing (`~30%` expansion) of a 3D **guanine-nanocrystal photonic lattice** inside upper S-iridophore cells (above a passive infrared-reflecting D-iridophore thermal shield), proved by shrinking an excised patch of skin in hypertonic salt water so it shifts backwards from red through yellow and green to blue.

---

## 2. Search-First Demand Check (`LEARNINGS.md` Rule 26, Retrieved `2026-11-16`)

- **Exact signed-out YouTube autocomplete phrase (`autocomplete = yes`):** `"how do chameleons change color"` (plus `"why do chameleons change color"`)
  - **Ranking Video 1:** `SQggDnScsvI` — *How Do Chameleons Change Color?* (`Veritasium`, **`3,475,292` views**, retrieved `2026-11-16`)
  - **Ranking Video 2:** `Dd7UVLkuxC4` — *The REAL Reason Chameleons Change Color* (`Odd Animal Specimens`, **`2,255,388` views**, retrieved `2026-11-16`; plus `Peekaboo Kidz` `y9mr02mE5XE` **`1,488,401` views**, `Happy Learning English` `aZuxerppygM` **`1,104,536` views**, and `Colossal Cranium` `mGijLaiVqsU` **`429,445` views**)
- **Decision:** Candidate primary title = `How Do Chameleons Change Colour? (The Nanocrystal Twist)` (Title A, `56 chars`) / `How Do Chameleons Change Colour? The Skin-Crystal Discovery` (Title C, `59 chars`, exact phrase first)
- **Candidate description first 100 chars (unverified until `SOURCES.md` check):** `How do chameleons change colour without green pigment? A 2015 Geneva test found tunable skin crystals.`

---

## 2b. Neighbour pass (blocking · `STUDIO_PLAYBOOK.md` §2 Step 4, Retrieved `2026-11-16`)

Saved in [`evidence_2026-11-16_neighbours.json`](evidence_2026-11-16_neighbours.json) and [`evidence_2026-11-16_public_search.json`](evidence_2026-11-16_public_search.json):

| # | Views (`2026-11-16`) | Channel (internal) | id & URL | Title | Subject words we reuse |
|---:|------:|--------------------|----------|-------|------------------------|
| 1 | `8,462,776` | TED-Ed ★ (`neighbours.py`) | [`gKfjHTk8KrY`](https://youtu.be/gKfjHTk8KrY) | *History’s deadliest colors - J. V. Maranto* | `color`, `pigment`, `green`, `history` |
| 2 | `5,014,768` | TED-Ed ★ (`neighbours.py`) | [`IxndOd3kmSs`](https://youtu.be/IxndOd3kmSs) | *Meet the tardigrade, the toughest animal on Earth - Thomas Boothby* | `animal`, `microscopic`, `survival`, `biology` |
| 3 | `3,540,205` | TED-Ed ★ (`neighbours.py`) | [`_r4c2NT4naQ`](https://youtu.be/_r4c2NT4naQ) | *The science of skin color - Angela Koine Flynn* | `skin color`, `melanin`, `pigment`, `light` |
| 4 | `3,475,292` | Veritasium (`public_search.py`) | [`SQggDnScsvI`](https://youtu.be/SQggDnScsvI) | *How Do Chameleons Change Color?* | `how do chameleons change color`, `nanocrystals`, `iridophores` |
| 5 | `2,255,388` | Odd Animal Specimens (`public_search.py`) | [`Dd7UVLkuxC4`](https://youtu.be/Dd7UVLkuxC4) | *The REAL Reason Chameleons Change Color* | `why chameleons change color`, `camouflage myth`, `rivals` |
| 6 | `1,906,840` | TED-Ed ★ (`neighbours.py`) | [`rkRbebvoYqI`](https://youtu.be/rkRbebvoYqI) | *What color is Tuesday? Exploring synesthesia - Richard E. Cytowic* | `color`, `perception`, `wavelength` |
| 7 | `1,742,391` | TED-Ed ★ (`neighbours.py`) | [`fSaHVHTqDY0`](https://youtu.be/fSaHVHTqDY0) | *These animals are also plants … wait, what? - Luka Seamus Wright* | `animals`, `cells`, `sunlight` |
| 8 | `1,672,051` | TED-Ed ★ (`neighbours.py`) | [`l8_fZPHasdo`](https://youtu.be/l8_fZPHasdo) | *How we see color - Colm Kelleher* | `how we see color`, `light wavelengths`, `reflection` |
| 9 | `1,326,018` | TED-Ed ★ (`neighbours.py`) | [`yRwoReHd7XU`](https://youtu.be/yRwoReHd7XU) | *What is the rarest color in nature? - Victoria Hwang* | `structural color`, `nanocrystals`, `pigment vs crystal` |
| 10 | `1,110,172` | TED-Ed ★ (`neighbours.py`) | [`UZ5UGnU7oOI`](https://youtu.be/UZ5UGnU7oOI) | *What is color? - Colm Kelleher* | `visible spectrum`, `wavelengths`, `light` |

**Proposed subject-only tags (8 tags, zero channel names):**  
`how do chameleons change color, why do chameleons change color, chameleon nanocrystals, structural color in nature, michel milinkovitch chameleon, iridophores guanine crystals, animal camouflage myth, history of science experiments`

---

## 3. Title ABC (score before VO)

| | Title | Chars | Collisions (`2026-11-16`) | Role & Notes | Keep? |
|---|-------|------:|-----------:|--------------|-------|
| A | `How Do Chameleons Change Colour? (The Nanocrystal Twist)` | 56 | 0 | **Main (`LEARNINGS.md` Rules 1, 23, 26):** Starts verbatim with exact autocomplete question `"how do chameleons change colour"` + nanocrystal experimental twist | **Keep (Primary Proposal)** |
| B | `Chameleons Have No Green Pigment (The 2015 Crystal Proof)` | 57 | 0 | **Test & Compare (`Rule 23`):** Leads with the zero-green-pigment surprise + 2015 Geneva proof | **Keep (T&C Arm 2)** |
| C | `How Do Chameleons Change Colour? The Skin-Crystal Discovery` | 59 | 0 | **Rule 26 Variant (`≤70 chars`):** Starts verbatim with exact autocomplete phrase + skin-crystal discovery story | **Keep (T&C Arm 3)** |
| Reject | `Photonic Guanine Lattices in Furcifer pardalis \| History of Science` | 67 | — | Academic jargon + forbidden series suffix | **Reject** |

---

## 3b. Script reviewer (blocking before VO — not run; proposal only)

- [ ] `SOURCES.md` exact quotes + `facts` lane verification completed (required before script lock)
- [ ] Score ≥ **90 / 100** (`npm run review:script`)
