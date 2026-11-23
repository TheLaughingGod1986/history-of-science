# Topic Opportunity Score — `HOS:133` (`How Was Quantum Physics Discovered? (The Lightbulb Problem)`)

- **Date:** `2026-11-23` (`J3410` Rule-E topic go/no-go review of `J3408` / HOS PR `#733` / OWB PR `#1208`)
- **Channel:** History of Science (`@HistoryOfScienceYT`)
- **Verdict:** **GO (`9.68 / 10` · `96.8 / 100`) — Pre-cleared in `jobs/WIP.json` `next_hos` under Rule G**

---

## 1. Weighted Opportunity Rubric (`9.680 / 10` · `96.8 / 100`)

| Dimension | Weight | Score (1–10) | Weighted | Evidence & Rationale |
|---|---:|---:|---:|---|
| 1. Evergreen search intent | 25% | `9.9` | `2.475` | Top-tier evergreen physics search demand: signed-out YouTube GB `autocomplete = yes` on **all 4 core queries** (`"how was quantum physics discovered"`, `"what is quantum mechanics"`, `"what is the ultraviolet catastrophe"`, `"max planck quantum theory"`). `neighbours.py` **PASS** with `13` raw / `11` on-topic quantum `≥1M` education videos (`9` core quantum-physics/origins + `2` adjacent quantum computing/biology TED talks; `2` off-topic excluded), including **`3` `TED-Ed` ★ `≥1M`** (`9.23M`, `2.17M`, `1.15M`), `Veritasium` (`21.55M` & `20.89M`), `The Royal Institution` (`4.69M`), and exact-match `PBS Space Time` (`2.05M` *Planck's Constant and The Origin of Quantum Mechanics*). Backed in `public_search.json` by `BBC News` (`9.67M`), `Big Think` (`4.73M`), `minutephysics` (`3.23M`), and `Physics Explained` (`2.71M`). |
| 2. Competition gap | 20% | `9.6` | `1.920` | Strong verified `<50k` US adult small-channel breakouts in `J3224` on this **exact** subject: `Science Retold` (`3.4K` US) → **`61.9K` (`13×`)** on *The Origin Of Planck's Constant* (`62,055` live on `2026-11-23`), `Math Everywhere` (`10.3K` US) → **`36.5K` (`10×`)** on *MAX PLANCK*, and `Cosmo Explains` (`37.0K` US) → **`239.7K` (`65×`)**. Ranking competition consists mostly of 25–120 minute lectures (`56:11`, `40:29`, `2:08:55`) or decade-old chalkboard clips (`10–14 yr`), leaving a clear lane for a `7–9 min` 3D cartoon discovery story. `0` exact and `0` near-exact title collisions across Titles A/A1/B/C and Shorts S01/S02. |
| 3. Narrative & visual arc | 20% | `9.7` | `1.940` | Compelling proof-first `0:05–0:15` apparatus (1900 Berlin PTR glowing ceramic blackbody oven + brass spectrometer vs classical infinity curve), grounded in an everyday industrial lightbulb race and peaking in Planck's Oct–Dec 1900 "act of desperation" ($E = h\nu$) and Bohr's 1913 atomic bridge to `HOS:004`. Minor `-0.3` for reconciling the 4-act sketch into HOS's 5-part (`7–9 min`) layout and enforcing strict Rayleigh–Jeans / infrared chronology. |
| 4. Brand & guardrail fit | 20% | `9.3` | `1.860` | Pure *Discovery · Wonder · Proof* HOS lane; zero overlap across `000–018`, `099–119`, open PRs `120–132`, and `ideas/011–095` (distinct from `ideas/025` wave-particle/photoelectric duality); `10_Shorts/README.md` complies with Ben's `19 Nov 2026` `16–19 s` house rules; all claims explicitly marked **UNVERIFIED**. `-0.7` for draft items caught and fixed in `J3410`: Thumb A `1900 POSTCARD` repeated Title B words (`§2.5`) → fixed to `IMPOSSIBLE GLOW`; blank `PRE_BUILD_VIDIQ_AUDIT.md` template populated at `£0`; 6 historical/physics precision guardrails logged (incl. von Jolly `1874` vs `1878`, Rayleigh–Jeans `1900/1905/1911` chronology, 1918/1919 Nobel). |
| 5. Series / cluster potential | 15% | `9.9` | `1.485` | Directly fills **Cluster 2 #6** (*Nuclear, Quantum & Modern Physics Breakthroughs* — Max Planck) in Ben's proposed `hos-search-2027-01` plan (`J3224`, `needsBen`), linking cleanly via end screens and playlists with live `HOS:004` (*What's Inside an Atom?*), `HOS:126` (Higgs Boson), `HOS:130` (Fermi Nuclear Reactor), `HOS:131` (Einstein Relativity), `ideas/022` (Meitner/Hahn Fission), and `ideas/025` (Young/Einstein Light). |
| **Total Opportunity Score** | **100%** | — | **`9.680 / 10` (`96.8 / 100`)** | **GO (Pre-cleared in `jobs/WIP.json` `next_hos` under Rule G)** |

---

## 2. Verified On-Topic Neighbour & Search Pool (`2026-11-23`, Signed-Out GB)

| # | Channel | Views | Video ID | Title | Evidence File |
|---:|---|---:|---|---|---|
| 1 | **Veritasium** | `21,553,339` | [`KfODG5REyss`](https://youtu.be/KfODG5REyss) | *I finally saw quantum physics with my own eyes... (It's spookier than I expected)* | `neighbours.json` (Tier 2) & `public_search.json` |
| 2 | **Veritasium** | `20,891,298` | [`qJZ1Ez28C-A`](https://youtu.be/qJZ1Ez28C-A) | *The Strangest Implication of Quantum Mechanics* | `neighbours.json` (Tier 2) & `public_search.json` |
| 3 | **BBC News** | `9,674,229` | [`fcfQkxwz4Oo`](https://youtu.be/fcfQkxwz4Oo) | *Brian Cox explains quantum mechanics in 60 seconds - BBC News* | `public_search.json` |
| 4 | **TED-Ed ★** | `9,228,160` | [`UjaAxUO6-Uw`](https://youtu.be/UjaAxUO6-Uw) | *Schrödinger's cat: A thought experiment in quantum mechanics - Chad Orzel* | `neighbours.json` (Tier 1) |
| 5 | **Big Think** | `4,727,044` | [`BHEhxPuMmQI`](https://youtu.be/BHEhxPuMmQI) | *Physicist Brian Cox explains quantum physics in 22 minutes* | `public_search.json` |
| 6 | **The Royal Institution** | `4,686,613` | [`5hVmeOCJjOU`](https://youtu.be/5hVmeOCJjOU) | *A Brief History of Quantum Mechanics - with Sean Carroll* | `neighbours.json` (Tier 2) & `public_search.json` |
| 7 | **TEDx Talks ★** | `3,813,226` | [`ARWBdfWpDyc`](https://youtu.be/ARWBdfWpDyc) | *Quantum Physics for 7 Year Olds \| Dominic Walliman \| TEDxEastVan* | `neighbours.json` (Tier 1) & `public_search.json` |
| 8 | **minutephysics** | `3,232,924` | [`i1TVZIBj7UA`](https://youtu.be/i1TVZIBj7UA) | *The Origin of Quantum Mechanics (feat. Neil Turok)* | `public_search.json` |
| 9 | **Physics Explained** | `2,714,822` | [`rCfPQLVzus4`](https://youtu.be/rCfPQLVzus4) | *What is the Ultraviolet Catastrophe?* | `public_search.json` |
| 10 | **PBS Space Time** | `2,514,160` | [`YSwRqNCeP9k`](https://youtu.be/YSwRqNCeP9k) | *So You Want to Understand Quantum Mechanics…* | `neighbours.json` (Tier 2) & `public_search.json` |
| 11 | **TED-Ed ★** | `2,168,361` | [`z1GCnycbMeA`](https://youtu.be/z1GCnycbMeA) | *What can Schrödinger's cat teach us about quantum mechanics? - Josh Samani* | `neighbours.json` (Tier 1) |
| 12 | **PBS Space Time** | `2,054,493` | [`tQSbms5MDvY`](https://youtu.be/tQSbms5MDvY) | *Planck's Constant and The Origin of Quantum Mechanics* | `neighbours.json` (Tier 2) & `public_search.json` |
| 13 | **Professor Dave Explains** | `1,273,903` | [`7BXvc9W97iU`](https://youtu.be/7BXvc9W97iU) | *Quantization of Energy Part 1: Blackbody Radiation and the Ultraviolet Catastrophe* | `public_search.json` |
| 14 | **Science ABC** | `1,199,963` | [`p9pPjASnnxw`](https://youtu.be/p9pPjASnnxw) | *Quantum Mechanics Explained in Ridiculously Simple Words* | `public_search.json` |
| 15 | **TED-Ed ★** | `1,153,323` | [`Hk3fgjHNQ2Q`](https://youtu.be/Hk3fgjHNQ2Q) | *Particles and waves: The central mystery of quantum mechanics - Chad Orzel* | `neighbours.json` (Tier 1) |
| 16 | **Abide By Reason** | `1,072,051` | [`BcNHTv7Rw3c`](https://youtu.be/BcNHTv7Rw3c) | *How Heisenberg Discovered Quantum Mechanics* | `public_search.json` |

*(Additional adjacent/sub-1M evidence: `TED` ★ `QuR969uMICM` `2,665,434` quantum computing & `_qgSz1UmcBM` `1,110,967` quantum biology; `Physics Girl` `FXfrncRey-4` `999,524` *The ULTRAVIOLET CATASTROPHE*; `The Royal Institution` `k-0pky806Fo` `735,223`; `Khan Academy` `OFwskHrtYQ4` `531,186`, `N0lBsW3ZzN8` `337,724` Atomic spectra, `DHG61XPuWyk` `257,384` Blackbody radiation; `Science Retold` `4L7guyXCl5M` `62,055` *The Origin Of Planck's Constant*. Two raw `≥1M` rows in `neighbours.json` transparently excluded: `TEDx Talks` `2RuCfTiCDjs` `3,866,931` manifestation talk and `Khan Academy` `uIojjqSm0m4` `1,511,742` 1D motion.)*

---

## 3. Cluster 2 Chain Sketch (Adjacent Episodes)

1. **`HOS:004` (Published — Direct Bridge):** *What's Inside an Atom? Mostly Empty Space* — Rutherford's 1911 nuclear atom, whose instability Bohr solved in 1913 using Planck's constant $h$.
2. **`HOS:133` (This Episode — Cluster 2 #6):** *How Was Quantum Physics Discovered? (The Lightbulb Problem)* — Berlin's 1887–1900 PTR blackbody oven → Planck's 1900 energy quanta ($E = h\nu$) → Bohr's 1913 stable atom.
3. **`ideas/025` (Distinct Wave-Particle Companion):** *Young / Fresnel / Einstein Light* — double-slit interference (1801–1803), Arago's bright spot (1819), and Einstein's 1905 photoelectric wave-particle proof.
4. **Cluster 2 Peers (`J3224`):** `HOS:131` (*What Is the Theory of Relativity? (1919 Eclipse)*), `HOS:130` (*How Does a Nuclear Reactor Work? (Under a Stadium)*), `HOS:126` (*What Is the Higgs Boson?*), and `ideas/022` (Meitner/Hahn nuclear fission).
