# Topic Opportunity Score — `HOS:108` (`108_Faraday-Thomson-Joly-Somorjai-Why-Ice-Is-Slippery`)

> **Rule-E Topic Review Verdict (`J2917`, 16 Nov 2026):** **GO (`9.40 / 10` · `94 / 100` Opportunity Score)** — Pre-cleared in `jobs/WIP.json` `next_hos` under Rule G.
> **Unverified Claims Guard:** All historical and scientific claims in `TOPIC.md` §4–§5 and `PRE_BUILD_VIDIQ_AUDIT.md` remain **UNVERIFIED** working notes and are **NOT CLEARED FOR NARRATION OR SHORT OPENS** until an active HOS WIP slot opens, exact primary-source quotes are recorded in `SOURCES.md`, and the `facts` lane (`gemini-agy`) verifies every claim.

**Candidate topic:** Why Is Ice Slippery? (The 150-Year Textbook Myth) — Michael Faraday's 1850 two-ice-cube demonstration and intrinsic surface film hypothesis vs. James & William Thomson's (Lord Kelvin's) 1849–1850 pressure-melting piston, John Joly's 1886 ice-skate pressure calculation that fooled physics textbooks for a century, Bowden & Hughes's 1939 Jungfraujoch Alpine ice-cave and cold-lab friction experiments, and Gabor Somorjai's modern surface spectroscopy proof (`HOS:108`)
**Primary search phrase:** `"why is ice slippery"` / `"how does ice skating work"` / `"melting point of ice"` / `"how do crystals work"` (signed-out YouTube GB `public_search.py` & `neighbours.py` autocomplete = **yes** on all four, retrieved `2026-11-15` / `2026-11-16`)
**Date:** `2026-11-16` (`J2891` topic proposal · `J2917` Rule-E review by `macbook-2`)

---

## 1. Weighted Rubric (`00_Brand/Channel-Setup/templates/TOPIC_OPPORTUNITY_SCORE.md`)

| Dimension | Weight | Score (1–10) | Weighted | Evidence & Rationale |
|-----------|--------|--------------|----------|----------------------|
| **1. Evergreen search intent** | 25% | **9.5** | **2.375** | `"why is ice slippery"` (`3` suggestions including `why is ice slippery feynman`), `"how does ice skating work"` (`6` suggestions), `"melting point of ice"` (`10` suggestions), and `"how do crystals work"` (`10` suggestions) all autocomplete (`suggest = yes`) in signed-out YouTube GB. Top on-topic education videos carry **`5,991,243` views** (`SmarterEveryDay` `qd4CVvItJlo`), **`3,735,948` views** (`TED-Ed` `PgSRAsgrKmg`), **`3,046,453` views** (`Veritasium` `gM3zP72-rJE` *Does Pressure Melt Ice?*), **`2,513,630` views** (`minutephysics` `_bcfxty39Cw`), **`2,049,194` views** (`TED-Ed` `UukRgqzk-KE` *Why does ice float in water?*), **`1,158,527` views** (`Be Smart` `yjSf7Yh9UZc` *The Strange and Unexpected Reason Ice is Slippery*), **`810,742` views** (`Dr Ben Miles` `20zyW0qoSTE`), and **`806,131` views** (`Veritasium` `Stx6kLd9dYI`). |
| **2. Competition gap (wonder / clarity vs dry or crowding)** | 20% | **9.0** | **1.800** | `Veritasium` (`Stx6kLd9dYI`, `806k`, `2:54`) and `SciShow` (`WZV8gM2_MFQ`, `218k`, `2:46`) are brief 3-minute talking-head summaries; `Be Smart` (`yjSf7Yh9UZc`, `1.16M`, `8:27`) and `Dr Ben Miles` (`20zyW0qoSTE`, `811k`, `13:43`) are studio/stock-footage explainers; and recent small-channel uploads (`1–135` views) are generic AI slide essays. None brings to life the 4-room chronological 3D detective story (Faraday's 1850 Royal Institution lecture theatre vs. Kelvin's Glasgow pressure cylinder → Joly's 1886 Dublin skate-blade calculation → Bowden & Hughes's 1939 Jungfraujoch Alpine ice cave → Somorjai's Berkeley LEED/AFM molecular surface probe). |
| **3. Narrative & visual arc (3D world + diagram clarity)** | 20% | **9.5** | **1.900** | Ideal for HOS's painted-3D house look and *Teach on screen* graphics: (1) `0:00–0:05` Faraday pressing two glistening moist ice blocks together until they weld solid, cutting at `0:05–0:15` to a steel skate blade on `-20 °C` ice beside a brass pressure gauge, (2) William Thomson's heavy glass pressure cylinder (`DATA + SCALE`: `0.0075 °C` per atmosphere), (3) Joly's `466 atm` hairline blade myth vs. the real `100–150 atm` contact patch and `-22 °C` triple-point limit on an inked phase chart, (4) Bowden & Hughes's brass vs. ebonite sliders in a Swiss Alpine ice cave, and (5) an inked crystal-lattice diagram showing dangling surface $\text{H}_2\text{O}$ bonds rolling like marbles below `0 °C`. |
| **4. Brand & guardrail fit** | 20% | **10.0** | **2.000** | Pure History of Science discovery story with two giants of 19th-century physics (Michael Faraday vs. Lord Kelvin) on opposite sides of an everyday kitchen experiment, a 150-year textbook error traced to a single 1886 paper, and modern vindication of Faraday's intuition. Zero fearbait, zero `Made for Kids` risk, zero overlap with `000–107`, `109`, or `ideas/`. |
| **5. Series / cluster potential** | 15% | **8.8** | **1.320** | Anchors the **Everyday Physics & Thermodynamics Myths Cluster** alongside `029_Kelvin-Rutherford-Age-of-the-Earth` (Lord Kelvin's cooling-Earth calculation vs. Rutherford's radium), `033_Joule-Mayer-Helmholtz-Mechanical-Equivalent-of-Heat` (Joule's paddle-wheel), `085_Agassiz-Croll-Milankovitch-Ice-Ages` (glacier flow & ice physics), and `104_Romer-Fizeau-Foucault-Speed-of-Light`. |
| **Total** | **100%** | — | **`9.40 / 10` (`94 / 100`)** | **GO (`≥ 7.5` threshold exceeded by `+1.90` points)** |

**Rule:** Proceed (`GO`) if **Total ≥ 7.5** and **Brand fit ≥ 8**. Both pass (`9.40 / 10` total, `10.0 / 10` brand fit).

---

## 2. Education Neighbour Gate (`neighbours.py` + `public_search.py`, Retrieved `2026-11-15` / `2026-11-16`)

Saved in [`evidence_2026-11-15_neighbours.json`](evidence_2026-11-15_neighbours.json) (`bigCount = 9`, `hasTed = true`, `gate = PASS`) and [`evidence_2026-11-15_public_search.json`](evidence_2026-11-15_public_search.json):

| # | Channel | Views (`2026-11-15` / `16`) | Video ID & URL | Title | Source File |
|---:|---|---:|---|---|---|
| 1 | **SmarterEveryDay** | `5,991,243` | [`qd4CVvItJlo`](https://youtu.be/qd4CVvItJlo) | *COLD HARD SCIENCE.The Physics of Skating on Ice (With SlowMo) - Smarter Every Day 110* | `public_search.json` |
| 2 | **TED-Ed ★** | `3,735,948` | [`PgSRAsgrKmg`](https://youtu.be/PgSRAsgrKmg) | *How do crystals work? - Graham Baird* | `public_search.json` (Tier 1) |
| 3 | **Veritasium** | `3,046,453` | [`gM3zP72-rJE`](https://youtu.be/gM3zP72-rJE) | *Does Pressure Melt Ice?* | `public_search.json` (Tier 2) |
| 4 | **minutephysics** | `2,513,630` | [`_bcfxty39Cw`](https://youtu.be/_bcfxty39Cw) | *Freezing water expands. What if you don't let it?* | `public_search.json` (Tier 2) |
| 5 | **TED-Ed ★** | `2,049,194` | [`UukRgqzk-KE`](https://youtu.be/UukRgqzk-KE) | *Why does ice float in water? - George Zaidan and Charles Morton* | `neighbours.json` (Tier 1) |
| 6 | **FuseSchool** | `1,867,278` | [`xYU7RSoOZ0U`](https://youtu.be/xYU7RSoOZ0U) | *Changes of State \| Matter \| Physics \| FuseSchool* | `neighbours.json` (Tier 2) |
| 7 | **TED-Ed ★** | `1,342,673` | [`ASLUY2U1M-8`](https://youtu.be/ASLUY2U1M-8) | *How polarity makes water behave strangely - Christina Kleinberg* | `neighbours.json` (Tier 1) |
| 8 | **Veritasium** | `1,329,655` | [`KCL8zqjXbME`](https://youtu.be/KCL8zqjXbME) | *States of Matter* | `neighbours.json` (Tier 2) |
| 9 | **FuseSchool** | `1,203,396` | [`21CR01rlmv4`](https://youtu.be/21CR01rlmv4) | *States Of Matter - Solids, Liquids & Gases \| Properties of Matter \| Chemistry \| FuseSchool* | `neighbours.json` (Tier 2) |
| 10 | **Be Smart** | `1,158,527` | [`yjSf7Yh9UZc`](https://youtu.be/yjSf7Yh9UZc) | *The Strange and Unexpected Reason Ice is Slippery* | `neighbours.json` (Tier 2) + `public_search.json` |
| 11 | **Cognito** | `1,017,499` | [`hkBrw2fG75U`](https://youtu.be/hkBrw2fG75U) | *GCSE Chemistry - States of Matter & Changing State* | `neighbours.json` (Tier 2) |
| 12 | **Dr Ben Miles** | `810,742` | [`20zyW0qoSTE`](https://youtu.be/20zyW0qoSTE) | *We FINALLY Proved Why Ice Is Slippery* | `public_search.json` |
| 13 | **Veritasium** | `806,131` | [`Stx6kLd9dYI`](https://youtu.be/Stx6kLd9dYI) | *Why Is Ice Slippery?* | `neighbours.json` (Tier 2) + `public_search.json` |

---

## 3. Cluster Sketch (3 Adjacent Episodes)

1. **`HOS:108` (This Episode):** *Why Is Ice Slippery? (The 150-Year Textbook Myth)* — Faraday's 1850 two-ice-cube demonstration vs. James & William Thomson's pressure-melting piston, Joly's 1886 skate-blade calculation, Bowden & Hughes's 1939 Jungfraujoch Alpine ice-cave friction tests, and Somorjai's surface premelting proof.
2. **`HOS:029` (`029_Kelvin-Rutherford-Age-of-the-Earth`, in `ideas/`):** *How Old Is the Earth?* — Lord Kelvin's thermodynamic cooling-iron-sphere calculation vs. Ernest Rutherford's 1904 Royal Institution lecture with a piece of pitchblende in his pocket.
3. **`HOS:033` (`033_Joule-Mayer-Helmholtz-Mechanical-Equivalent-of-Heat`, in `ideas/`):** *What Is Heat?* — Count Rumford's cannon-boring water boil and James Prescott Joule's falling-weight paddle-wheel thermometer.
4. **`HOS:085` (`085_Agassiz-Croll-Milankovitch-Ice-Ages`, in `ideas/`):** *How Did We Discover Ice Ages?* — Louis Agassiz's Alpine erratic boulders, glacier motion (where Tyndall & Huxley first applied Faraday's regelation), and Milutin Milankovitch's orbital cycles.
