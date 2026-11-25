# Pre-Build Search & Neighbour Audit — `126_Higgs-Englert-CERN-What-Is-The-Higgs-Boson` (`HOS:126` · Rule-E GO in `next_hos`)

> **RULE-E GO STATUS (`J3263`, `2026-11-21` — `96.1 / 100`):** Proposed in `J3245` and pre-cleared by `J3263` Rule-E topic go/no-go review (**GO**, `9.61 / 10` Opportunity Score; see [`TOPIC_GO_NO_GO_SHEET.md`](TOPIC_GO_NO_GO_SHEET.md) and [`TOPIC_OPPORTUNITY_SCORE.md`](TOPIC_OPPORTUNITY_SCORE.md)). Stays in `jobs/WIP.json` `next_hos` (Rule G; `4 / 4` active HOS slots full). Independently passes all currently in-force HOS topic gates and aligns with the **proposed** `hos-search-2027-01` Cluster 2 (`J3224`, currently `needsBen` in `studio/plan.json`, not yet approved by Ben). All historical and scientific claims below are **UNVERIFIED** working notes and must be sourced in `SOURCES.md` and checked by the `facts` lane (`gemini-agy`) when an active HOS WIP slot opens, before any script lock, VO, or picture spend.

## 1. The Discovery Story (Person, Date & Twist — UNVERIFIED)

- **Familiar phenomenon:** Why physical matter has weight and holds together as atoms — and why physicists spent 48 years hunting a particle nicknamed "the God particle" that doesn't actually create 99% of your body's mass.
- **Person, place & date:**
  - **François Englert & Robert Brout** (Brussels, **August 1964**), **Peter Higgs** (University of Edinburgh, **October 1964**), and **Gerald Guralnik, Carl Hagen & Tom Kibble** (Imperial College London, **November 1964**): independently solve the mass paradox in quantum field theory by proposing an invisible all-space field; *Physics Letters* rejects Higgs's paper as having *"no obvious relevance to physics"*, prompting him to add the explicit prediction of a massive spin-0 boson for *Physical Review Letters*.
  - **Leon Lederman** (**1993**, *The God Particle*): coins the censored nickname after his publisher refuses *"The Goddamn Particle"*.
  - **Fabiola Gianotti (ATLAS) & Joe Incandela (CMS) at CERN's Large Hadron Collider** (Geneva, **4 July 2012**): announce the discovery of a `~125 GeV` Higgs-like boson at `5-sigma` inside the 27-kilometre superconducting collider, ending a 48-year hunt and earning Higgs and Englert the **2013 Nobel Prize in Physics**.
  - **The Mass Twist:** While the Higgs field gives fundamental electrons and quarks their mass (without which atoms could never form), roughly `99%` of your body's mass actually comes from the strong-force binding energy ($E=mc^2$) of quarks and gluons inside protons and neutrons.

---

## 2. Search-First Demand Check (`LEARNINGS.md` Rule 26 + `J3224`, Retrieved `2026-11-21`)

- **`J3224` vidIQ demand (`2026-11-20`):** `the god particle` = **`19,705` est. monthly searches**, competition **`42`**, **`+89.8%` growth**, **`9/10` US signed-out SERP gap**, US/UK/CA/AU adult evergreen intent, sub-50k US breakouts (`Science Retold` 3.4K US → `61.9K` 13×; `Cosmo Explains` 37K US → `239.7K` 65×).
- **Exact signed-out YouTube autocomplete phrases (`autocomplete = yes`, `2026-11-21`):** `"what is the higgs boson"`, `"the god particle"`, `"why is it called the god particle"` (plus `"why is the higgs boson called the god particle"`).
  - **Ranking Video 1:** [`RIg1Vh7uPyw`](https://youtu.be/RIg1Vh7uPyw) — *What is a Higgs Boson?* (`Fermilab`, **`3,503,595` views**, retrieved `2026-11-21`)
  - **Ranking Video 2:** [`IElHgJG5Fe4`](https://youtu.be/IElHgJG5Fe4) — *The basics of the Higgs boson - Dave Barney and Steve Goldfarb* (`TED-Ed`, **`2,380,303` views**, retrieved `2026-11-21`)
- **Decision:** Candidate primary title = `What Is the Higgs Boson? (The 48-Year Hunt)` (Title A, `43 chars ≤ 50`, `0` collisions) / `The God Particle: The 1964 Paper They Rejected` (Title B, `46 chars ≤ 50`, `0` collisions).
- **Candidate description first 100 chars (unverified until `SOURCES.md` check):** `What is the Higgs boson? How a rejected 1964 paper triggered a 48-year hunt beneath Geneva at CERN.`

---

## 2b. Neighbour pass (blocking · `STUDIO_PLAYBOOK.md` §2 Step 4, Retrieved `2026-11-21`)

Saved in [`evidence_2026-11-21_neighbours.json`](evidence_2026-11-21_neighbours.json) (`bigCount = 11` strictly on-topic education videos `≥1M` views, `hasTed = true`, `gate = PASS`, `0` off-topic rows) and [`evidence_2026-11-21_public_search.json`](evidence_2026-11-21_public_search.json) (`10` queries, `0` exact title collisions):

| # | Views (`2026-11-21`) | Channel (internal) | id & URL | Title | Subject words we reuse |
|---:|------:|--------------------|----------|-------|------------------------|
| 1 | `3,503,595` | Fermilab (`public_search.py`) | [`RIg1Vh7uPyw`](https://youtu.be/RIg1Vh7uPyw) | *What is a Higgs Boson?* | `what is the higgs boson`, `higgs field`, `mass` |
| 2 | `3,372,242` | Veritasium (`neighbours.py`) | [`Ztc6QPNUqls`](https://youtu.be/Ztc6QPNUqls) | *Your Mass is NOT From the Higgs Boson* | `higgs boson`, `mass`, `quarks`, `binding energy` |
| 3 | `2,718,704` | PBS Space Time (`neighbours.py`) | [`kixAljyfdqU`](https://youtu.be/kixAljyfdqU) | *The Higgs Mechanism Explained* | `higgs mechanism`, `higgs field`, `particle` |
| 4 | `2,571,633` | minutephysics (`neighbours.py`) | [`9Uh5mTxRQcg`](https://youtu.be/9Uh5mTxRQcg) | *The Higgs Boson, Part I* | `higgs boson`, `field`, `quantum` |
| 5 | `2,380,303` | TED-Ed ★ (`neighbours.py`) | [`IElHgJG5Fe4`](https://youtu.be/IElHgJG5Fe4) | *The basics of the Higgs boson - Dave Barney and Steve Goldfarb* | `higgs boson`, `CERN`, `Large Hadron Collider` |
| 6 | `1,905,645` | PBS Space Time (`neighbours.py`) | [`G0Q4UAiKacw`](https://youtu.be/G0Q4UAiKacw) | *How the Higgs Mechanism Give Things Mass* | `higgs mechanism`, `mass`, `electrons` |
| 7 | `1,516,607` | minutephysics (`neighbours.py`) | [`ASRpIym_jFM`](https://youtu.be/ASRpIym_jFM) | *The Higgs Boson, Part II: What is Mass?* | `higgs boson`, `what is mass`, `energy` |
| 8 | `1,508,804` | PBS Space Time (`neighbours.py`) | [`GjkqedrTwZo`](https://youtu.be/GjkqedrTwZo) | *The Crisis in Physics: Why the Higgs Boson Should NOT Exist!* | `higgs boson`, `standard model` |
| 9 | `1,352,059` | Veritasium (`neighbours.py`) | [`649iUqrOKuE`](https://youtu.be/649iUqrOKuE) | *What Now For The Higgs Boson?* | `higgs boson`, `CERN`, `discovery` |
| 10 | `1,290,571` | SciShow (`neighbours.py`) | [`WUnDsNL_5nk`](https://youtu.be/WUnDsNL_5nk) | *So what IS the Higgs boson?* | `what is the higgs boson`, `particle physics` |
| 11 | `1,135,744` | minutephysics (`neighbours.py`) | [`6guXMfg88Z8`](https://youtu.be/6guXMfg88Z8) | *Higgs Boson Part III: How to Discover a Particle* | `higgs boson`, `collider`, `discovery` |
| 12 | `1,098,547` | TED-Ed ★ (`neighbours.py`) | [`joTKd5j3mzk`](https://youtu.be/joTKd5j3mzk) | *The Higgs Field, explained - Don Lincoln* | `higgs field`, `quantum field`, `mass` |

**Proposed subject-only tags (8 tags, zero channel names):**  
`what is the higgs boson, the god particle explained, higgs field mass, peter higgs 1964 paper, cern large hadron collider 2012, why is it called the god particle, where does mass come from, history of physics discoveries`

---

## 3. Title ABC (score before VO)

| | Title | Chars | Collisions (`2026-11-21`) | Role & Notes | Keep? |
|---|-------|------:|-----------:|--------------|-------|
| A | `What Is the Higgs Boson? (The 48-Year Hunt)` | 43 | 0 | **Main (`Rules 1, 15, 23, 26`):** Compact `≤50 chars`, exact autocomplete question `"what is the higgs boson"` first + concrete 48-year stakes tail | **Keep (Primary Proposal)** |
| B | `The God Particle: The 1964 Paper They Rejected` | 46 | 0 | **Test & Compare (`J3224`, `Rules 15, 23`):** Compact `≤50 chars`, exact `+89.8%` growth query `"the god particle"` + rejected-paper twist | **Keep (T&C Arm 2)** |
| C | `What Is the Higgs Boson? (The 1964 Paper CERN Proved)` | 53 | 0 | **Rule 26 Variant (`≤70 chars`):** Exact autocomplete phrase + 1964 paper & CERN proof | **Keep (T&C Arm 3)** |
| Reject | `Electroweak Symmetry Breaking in Quantum Field Theory \| HOS` | 60 | — | Academic jargon + forbidden series suffix | **Reject** |

---

## 3b. Script reviewer (blocking before VO — not run; proposal only)

- [ ] `SOURCES.md` exact quotes + `facts` lane verification completed (required before script lock)
- [ ] Score ≥ **90 / 100** (`npm run review:script`)
