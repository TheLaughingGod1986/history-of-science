# Pre-Build Search & Neighbour Audit — `118_NewsomDavis-Straus-Whitehead-Why-Do-We-Hiccup` (`HOS:118` Proposal)

> **PROPOSAL STATUS (`J2970`, `2026-11-17`):** Waiting in `jobs/WIP.json` `next_hos` (Rule G). All historical and scientific claims below are **UNVERIFIED** working notes and must be sourced in `SOURCES.md` and checked by the `facts` lane before script lock.

## 1. The Discovery Story (Person, Date & Twist — UNVERIFIED)

- **Familiar phenomenon:** Why our chest suddenly jerks with an involuntary `"hic"` that serves no obvious breathing purpose—and why unborn human babies spend up to 15 minutes a day hiccuping inside the womb before they ever take a breath of air.
- **Person, place & date:**
  - **John Newsom Davis** (National Hospital, Queen Square, London, **August 1970**, *Brain*, `"An experimental study of hiccup"`): wires electromyography (EMG) and airflow transducers to patients with intractable hiccups, overturning the old textbook idea of a simple stomach or diaphragm twitch by proving a hiccup is a highly coordinated **brainstem motor pattern** where the diaphragm and external intercostal inspiratory muscles fire together and the **glottis snaps shut ~35 milliseconds later** (blocking airflow and creating the *"hic"* sound), and showing high arterial $\text{CO}_2$ suppresses hiccup frequency.
  - **Johanna I. P. de Vries, Gerard H. A. Visser & Heinz F. R. Prechtl** (University Hospital Groningen, **1982**, *Early Human Development*): use real-time obstetric ultrasound to discover that human fetuses begin regular bouts of hiccuping as early as **8–9 weeks of gestation**—before breathing movements even mature—spending roughly **1–2% of their day** hiccuping in amniotic fluid.
  - **Christian Straus & William A. Whitelaw** (Pitié-Salpêtrière Hospital, Paris & University of Calgary, **February 2003**, *BioEssays*): solve the evolutionary paradox by showing that the human hiccup motor pattern is homologous to the **370-million-year-old amphibian gill-ventilation CPG (central pattern generator)** in air-breathing tadpoles, which compress the oral cavity to pump water across their gills while slamming the glottis shut so water cannot flood their primitive lungs.
  - **Kimberley Whitehead & Lorenzo Fabrizi** (University College London, **November 2019**, *Clinical Neurophysiology*): record newborn EEG brainwaves during hiccup bouts and discover that each diaphragm contraction triggers a large **three-wave cortical response** in the baby's somatosensory cortex, teaching the newborn brain to map and regulate its own breathing muscles before and right after birth.

---

## 2. Search-First Demand Check (`LEARNINGS.md` Rule 26, Retrieved `2026-11-17`)

- **Exact signed-out YouTube autocomplete phrase (`autocomplete = yes`):** `"why do we hiccup"` (plus `"what causes hiccups"` and `"why do babies hiccup in the womb"`)
  - **Ranking Video 1:** `-AdQLkUkui8` — *Why do we hiccup? - John Cameron* (`TED-Ed`, **`3,344,637` views**, retrieved `2026-11-17`)
  - **Ranking Video 2:** `ylWgmSNBYtg` — *Why has no one cured hiccups yet?* (`Be Smart`, **`1,693,978` views**, retrieved `2026-11-17`; plus `Zack D. Films` **`8,843,896` views**, `Peekaboo Kidz` **`2,902,592` views**, `Institute of Human Anatomy` **`1,820,633` views**, and `SciShow Kids` `9e5lcQycf2M` **`316,185` views**)
- **Decision:** Candidate primary title = `Why Do We Hiccup? (The Tadpole Gill Twist)` (Title A, `42 chars`, `≤50 chars`) / `Why Do We Hiccup? The Ancient Tadpole Brain Reflex` (Title C, `50 chars`, exact phrase first)
- **Candidate description first 100 chars (unverified until `SOURCES.md` check):** `Why do we hiccup? A 2003 gill study and 2019 baby brain scan traced hiccups to a tadpole reflex.`

---

## 2b. Neighbour pass (blocking · `STUDIO_PLAYBOOK.md` §2 Step 4, Retrieved `2026-11-17`)

Saved in [`evidence_2026-11-17_neighbours.json`](evidence_2026-11-17_neighbours.json) and [`evidence_2026-11-17_public_search.json`](evidence_2026-11-17_public_search.json):

| # | Views (`2026-11-17`) | Channel (internal) | id & URL | Title | Subject words we reuse |
|---:|------:|--------------------|----------|-------|------------------------|
| 1 | `3,686,149` | TED-Ed ★ (`neighbours.py`) | [`8NUxvJS-_0k`](https://youtu.be/8NUxvJS-_0k) | *How do lungs work? - Emma Bryce* | `lungs`, `diaphragm`, `breathing` |
| 2 | `3,344,637` | TED-Ed ★ (`neighbours.py`) | [`-AdQLkUkui8`](https://youtu.be/-AdQLkUkui8) | *Why do we hiccup? - John Cameron* | `why do we hiccup`, `diaphragm`, `glottis`, `amphibian` |
| 3 | `2,902,592` | Peekaboo Kidz (`public_search.py`) | [`fb1p43M1s3w`](https://www.youtube.com/results?search_query=why+do+we+hiccup) | *Why Do We Get Hiccups? \| The Dr. Binocs Show* | `why do we hiccup`, `what causes hiccups`, `vocal cords` |
| 4 | `2,237,332` | MinuteEarth (`neighbours.py`) | [`Kd4ubaE_sT4`](https://youtu.be/Kd4ubaE_sT4) | *Our Lungs Have A Fatal Flaw* | `lungs`, `evolution`, `breathing` |
| 5 | `1,926,175` | TEDx Talks ★ (`neighbours.py`) | [`nM-ySWyID9o`](https://youtu.be/nM-ySWyID9o) | *How breathing and metabolism are interconnected \| Ruben Meerman \| TEDxBundaberg* | `breathing`, `carbon dioxide` |
| 6 | `1,820,633` | Institute of Human Anatomy (`public_search.py`) | [`why do we hiccup`](https://www.youtube.com/results?search_query=why+do+we+hiccup) | *What Really Happens When You Hiccup* | `hiccup`, `phrenic nerve`, `diaphragm`, `glottis` |
| 7 | `1,693,978` | Be Smart (`neighbours.py`) | [`ylWgmSNBYtg`](https://youtu.be/ylWgmSNBYtg) | *Why has no one cured hiccups yet?* | `hiccups`, `reflex`, `tadpole gills` |
| 8 | `1,446,995` | Khan Academy (`neighbours.py`) | [`SPGRkexI_cs`](https://youtu.be/SPGRkexI_cs) | *The lungs and pulmonary system \| Health & Medicine \| Khan Academy* | `lungs`, `pulmonary`, `diaphragm` |
| 9 | `732,881` | TED-Ed ★ (`neighbours.py`) | [`bH3O69BscYg`](https://youtu.be/bH3O69BscYg) | *Why fish are better at breathing than you are - Dan Kwartler* | `gills`, `breathing`, `evolution` |
| 10 | `316,185` | SciShow Kids (`neighbours.py`) | [`9e5lcQycf2M`](https://youtu.be/9e5lcQycf2M) | *Why Do We Get Hiccups? \| Body Science for Kids* | `why do we get hiccups`, `diaphragm` |

**Proposed subject-only tags (8 tags, zero channel names):**  
`why do we hiccup, what causes hiccups, tadpole gill reflex hiccups, john newsom davis hiccup, christian straus hiccup, why do babies hiccup in the womb, diaphragm glottis reflex, history of science experiments`

---

## 3. Title ABC (score before VO)

| | Title | Chars | Collisions (`2026-11-17`) | Role & Notes | Keep? |
|---|-------|------:|-----------:|--------------|-------|
| A | `Why Do We Hiccup? (The Tadpole Gill Twist)` | 42 | 0 | **Main (`LEARNINGS.md` Rules 1, 15, 23, 26):** Compact `≤50 chars`, starts verbatim with exact autocomplete question `"why do we hiccup"` + 2003 tadpole gill twist | **Keep (Primary Proposal)** |
| B | `Hiccups Aren't a Mistake (The 370M-Year Reflex)` | 47 | 0 | **Test & Compare (`Rule 23`):** Compact `≤50 chars`, leads with the "useless spasm" myth reversal + 370M-year evolutionary reflex | **Keep (T&C Arm 2)** |
| C | `Why Do We Hiccup? The Ancient Tadpole Brain Reflex` | 50 | 0 | **Rule 26 Variant (`≤50 chars`):** Starts verbatim with exact autocomplete phrase + ancient tadpole brain reflex | **Keep (T&C Arm 3)** |
| Reject | `Phylogenetic Hypothesis of the Mammalian Hiccup Reflex \| HOS` | 60 | — | Academic jargon + forbidden series suffix | **Reject** |

---

## 3b. Script reviewer (blocking before VO — not run; proposal only)

- [ ] `SOURCES.md` exact quotes + `facts` lane verification completed (required before script lock)
- [ ] Score ≥ **90 / 100** (`npm run review:script`)
