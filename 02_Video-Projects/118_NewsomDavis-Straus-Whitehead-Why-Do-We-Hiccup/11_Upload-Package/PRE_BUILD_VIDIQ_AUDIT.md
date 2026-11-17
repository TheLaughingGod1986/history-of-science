# Pre-Build Search & Neighbour Audit — `118_NewsomDavis-Straus-Whitehead-Why-Do-We-Hiccup` (`HOS:118` · Rule-E GO in `next_hos`)

> **RULE-E GO STATUS (`J2970` / `J2971`, `2026-11-17`):** Pre-cleared (`95.5 / 100` · `9.55 / 10` Opportunity Score) in `jobs/WIP.json` `next_hos` (Rule G; `4 / 4` active HOS slots full). All historical and scientific claims below are **UNVERIFIED** working notes and must be sourced in `SOURCES.md` and checked by the `facts` lane (`gemini-agy`) when an active HOS WIP slot opens, before any script lock, VO, or picture spend.

## 1. The Discovery Story (Person, Date & Twist — UNVERIFIED)

- **Familiar phenomenon:** Why our chest suddenly jerks with an involuntary `"hic"` that serves no obvious breathing purpose—and why unborn human babies spend up to 15 minutes a day hiccuping inside the womb before they ever take a breath of air.
- **Person, place & date:**
  - **John Newsom Davis** (National Hospital, Queen Square, London, **August 1970**, *Brain* `93(4):851–872`, `"An experimental study of hiccup"`): wires electromyography (EMG) and airflow transducers to patients with intractable hiccups, overturning the old textbook idea of a simple stomach or diaphragm twitch by proving a hiccup is a highly coordinated **brainstem motor pattern** where the diaphragm and external intercostal inspiratory muscles fire together and the **glottis snaps shut ~35 milliseconds later** (blocking airflow and creating the *"hic"* sound), and showing high arterial $\text{CO}_2$ suppresses hiccup frequency.
  - **Johanna I. P. de Vries, Gerard H. A. Visser & Heinz F. R. Prechtl** (University Hospital Groningen, **1982**, *Early Human Development* `7(4):301–322`): use real-time obstetric ultrasound to discover that human fetuses begin regular bouts of hiccuping as early as **8–9 weeks of gestation**—before breathing movements even mature—spending roughly **1–2% of their day** (`~15 minutes`) hiccuping in amniotic fluid.
  - **Christian Straus & William A. Whitelaw** (Pitié-Salpêtrière Hospital, Paris & University of Calgary, **February 2003**, *BioEssays* `25(2):182–188`): solve the evolutionary paradox by showing that the human hiccup motor pattern is homologous to the **370-million-year-old amphibian gill-ventilation CPG (central pattern generator)** in air-breathing tadpoles, which compress the oral cavity to pump water across their gills while slamming the glottis shut so water cannot flood their primitive lungs.
  - **Kimberley Whitehead & Lorenzo Fabrizi** (University College London, **November 2019**, *Clinical Neurophysiology* `130(11):2216–2221`): record newborn EEG brainwaves during hiccup bouts and discover that each diaphragm contraction triggers a large **three-wave cortical response** in the baby's somatosensory cortex, teaching the newborn brain to map and regulate its own breathing muscles before and right after birth.

---

## 2. Search-First Demand Check (`LEARNINGS.md` Rule 26, Retrieved `2026-11-17`)

- **Exact signed-out YouTube autocomplete phrases (`autocomplete = yes`):** `"why do we hiccup"`, `"why do you hiccup"`, `"why do we get hiccups"`, `"what causes hiccups"`, and `"why do babies hiccup in the womb"` (plus `"cured hiccups"`, `"diaphragm"`, `"respiratory"`, and `"lungs anatomy"`)
  - **Ranking Video 1:** [`-AdQLkUkui8`](https://youtu.be/-AdQLkUkui8) — *Why do we hiccup? - John Cameron* (`TED-Ed`, **`3,344,659` views**, retrieved `2026-11-17`)
  - **Ranking Video 2:** [`ylWgmSNBYtg`](https://youtu.be/ylWgmSNBYtg) — *Why has no one cured hiccups yet?* (`Be Smart`, **`1,693,978` views**, retrieved `2026-11-17`; plus `Zack D. Films` [`xSie-M8xVp4`](https://youtu.be/xSie-M8xVp4) **`8,844,060` views**, `Peekaboo Kidz` [`UZy2Wlh97SU`](https://youtu.be/UZy2Wlh97SU) **`2,902,625` views**, `Institute of Human Anatomy` [`MAsRkRK-S2E`](https://youtu.be/MAsRkRK-S2E) **`1,820,635` views**, `T-Series Kids Hut` [`UTLz-wHH2Pc`](https://youtu.be/UTLz-wHH2Pc) **`1,453,078` views**, `Doctor Mike` [`bDD-oM0FHko`](https://youtu.be/bDD-oM0FHko) **`1,341,797` views**, `It's AumSum Time` [`Ux9SEPRMF5Y`](https://youtu.be/Ux9SEPRMF5Y) **`1,167,955` views**, and `SciShow Kids` [`9e5lcQycf2M`](https://youtu.be/9e5lcQycf2M) **`316,189` views**)
- **Decision:** Candidate primary title = `Why Do We Hiccup? (The Tadpole Gill Twist)` (Title A, `42 chars`, `≤50 chars`) / `Why Do We Hiccup? The Ancient Tadpole Brain Reflex` (Title C, `50 chars`, exact phrase first)
- **Candidate description first 100 chars (unverified until `SOURCES.md` check):** `Why do we hiccup? A 2003 gill study and 2019 baby brain scan traced hiccups to a tadpole reflex.`

---

## 2b. Neighbour pass (blocking · `STUDIO_PLAYBOOK.md` §2 Step 4, Retrieved `2026-11-17`)

Saved in [`evidence_2026-11-17_neighbours.json`](evidence_2026-11-17_neighbours.json) (`bigCount = 7` strictly on-topic education videos `≥1M` views, `hasTed = true`, `gate = PASS`, `0` off-topic rows) and [`evidence_2026-11-17_public_search.json`](evidence_2026-11-17_public_search.json) (`11` queries, `78` search results, `0` exact title collisions):

| # | Views (`2026-11-17`) | Channel (internal) | id & URL | Title | Subject words we reuse |
|---:|------:|--------------------|----------|-------|------------------------|
| 1 | `8,844,060` | Zack D. Films (`public_search.py`) | [`xSie-M8xVp4`](https://youtu.be/xSie-M8xVp4) | *Why Do We Hiccup? 🤔* | `why do we hiccup`, `diaphragm`, `vocal cords` |
| 2 | `5,923,036` | CrashCourse (`neighbours.py`) | [`bHZsvBdUC2I`](https://youtu.be/bHZsvBdUC2I) | *Respiratory System, Part 1: Crash Course Anatomy & Physiology #31* | `respiratory system`, `lungs`, `breathing` |
| 3 | `4,023,356` | Amoeba Sisters (`neighbours.py`) | [`v_j-LD2YEqg`](https://youtu.be/v_j-LD2YEqg) | *Respiratory System* | `respiratory system`, `lungs`, `diaphragm` |
| 4 | `3,686,170` | TED-Ed ★ (`neighbours.py`) | [`8NUxvJS-_0k`](https://youtu.be/8NUxvJS-_0k) | *How do lungs work? - Emma Bryce* | `lungs`, `diaphragm`, `breathing` |
| 5 | `3,344,659` | TED-Ed ★ (`neighbours.py`) | [`-AdQLkUkui8`](https://youtu.be/-AdQLkUkui8) | *Why do we hiccup? - John Cameron* | `why do we hiccup`, `diaphragm`, `glottis`, `amphibian` |
| 6 | `3,130,640` | CrashCourse (`neighbours.py`) | [`Cqt4LjHnMEA`](https://youtu.be/Cqt4LjHnMEA) | *Respiratory System, Part 2: Crash Course Anatomy & Physiology #32* | `respiratory system`, `breathing`, `carbon dioxide` |
| 7 | `2,902,625` | Peekaboo Kidz (`public_search.py`) | [`UZy2Wlh97SU`](https://youtu.be/UZy2Wlh97SU) | *Why Do We Hiccup? \| The Dr. Binocs Show \| BEST LEARNING VIDEOS For Kids* | `why do we hiccup`, `what causes hiccups`, `vocal cords` |
| 8 | `1,820,635` | Institute of Human Anatomy (`public_search.py`) | [`MAsRkRK-S2E`](https://youtu.be/MAsRkRK-S2E) | *What Are Hiccups, and Why Do We Get Them??* | `hiccup`, `phrenic nerve`, `diaphragm`, `glottis` |
| 9 | `1,693,978` | Be Smart (`neighbours.py`) | [`ylWgmSNBYtg`](https://youtu.be/ylWgmSNBYtg) | *Why has no one cured hiccups yet?* | `hiccups`, `reflex`, `tadpole gills` |
| 10 | `1,446,998` | Khan Academy (`neighbours.py`) | [`SPGRkexI_cs`](https://youtu.be/SPGRkexI_cs) | *The lungs and pulmonary system \| Health & Medicine \| Khan Academy* | `lungs`, `pulmonary`, `diaphragm` |
| 11 | `1,341,797` | Doctor Mike (`public_search.py`) | [`bDD-oM0FHko`](https://youtu.be/bDD-oM0FHko) | *Why Do We Get Hiccups & How To Stop Them \| RTC* | `why do we get hiccups`, `diaphragm`, `reflex` |
| 12 | `316,189` | SciShow Kids (`neighbours.py`) | [`9e5lcQycf2M`](https://youtu.be/9e5lcQycf2M) | *Why Do We Get Hiccups? \| Body Science for Kids* | `why do we get hiccups`, `diaphragm` |

**Proposed subject-only tags (8 tags, zero channel names):**  
`why do we hiccup, what causes hiccups, tadpole gill reflex hiccups, john newsom davis hiccup, christian straus hiccup, why do babies hiccup in the womb, diaphragm glottis reflex, history of science experiments`

---

## 3. Title ABC (score before VO)

| | Title | Chars | Collisions (`2026-11-17`) | Role & Notes | Keep? |
|---|-------|------:|-----------:|--------------|-------|
| A | `Why Do We Hiccup? (The Tadpole Gill Twist)` | 42 | 0 | **Main (`LEARNINGS.md` Rules 1, 15, 23, 26):** Compact `≤50 chars`, starts verbatim with exact autocomplete question `"why do we hiccup"` + 2003 tadpole gill twist | **Keep (Primary Proposal)** |
| B | `Hiccups Aren't a Mistake (The 370M-Year Reflex)` | 47 | 0 | **Test & Compare (`Rules 15, 23`):** Compact `≤50 chars`, leads with the "useless spasm" myth reversal + 370M-year evolutionary reflex | **Keep (T&C Arm 2)** |
| C | `Why Do We Hiccup? The Ancient Tadpole Brain Reflex` | 50 | 0 | **Rule 26 Variant (`≤50 chars`):** Starts verbatim with exact autocomplete phrase + ancient tadpole brain reflex | **Keep (T&C Arm 3)** |
| Reject | `Phylogenetic Hypothesis of the Mammalian Hiccup Reflex \| HOS` | 60 | — | Academic jargon + forbidden series suffix | **Reject** |

---

## 3b. Script reviewer (blocking before VO — not run; proposal only)

- [ ] `SOURCES.md` exact quotes + `facts` lane verification completed (required before script lock)
- [ ] Score ≥ **90 / 100** (`npm run review:script`)
