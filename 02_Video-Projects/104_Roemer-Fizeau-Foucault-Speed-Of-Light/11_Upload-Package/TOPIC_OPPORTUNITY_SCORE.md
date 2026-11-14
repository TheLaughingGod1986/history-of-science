# Topic Opportunity Score — `HOS:104` (`104_Roemer-Fizeau-Foucault-Speed-Of-Light`)

> **Rule-E Topic Review Verdict (`J2810`, 14 Nov 2026):** **GO (`9.60 / 10` · `96 / 100` Opportunity Score)** — Pre-cleared in `jobs/WIP.json` `next_hos` under Rule G.
> **Unverified Claims Guard:** All historical and scientific claims in `TOPIC.md` §2–§3 and `PRE_BUILD_VIDIQ_AUDIT.md` remain **UNVERIFIED** working notes and are **NOT CLEARED FOR NARRATION OR SHORT OPENS** until an active HOS WIP slot opens (`len(WIP.json["hos"]) < 6`), exact primary-source quotes are recorded in `SOURCES.md`, and the `facts` lane (`gemini-agy`) verifies every claim.

**Candidate topic:** How Did We Measure the Speed of Light? — Galileo's 1638 hilltop lanterns, Ole Rømer's 1676 eclipses of Jupiter's moon Io, Hippolyte Fizeau's 1849 720-tooth brass cogwheel across Paris, and Léon Foucault's 1850/1862 rotating mirror & water-tube test (`HOS:104`)
**Primary search phrase:** `"how did we measure the speed of light"` / `"speed of light"` (signed-out YouTube GB `public_search.py` autocomplete = **yes** on both, plus `"fizeau"` = **yes**, retrieved `2026-11-14`)
**Date:** `2026-11-14` (`J2809` evidence pull on Mac mini · `J2810` Rule-E review by `macbook`)

---

## 1.Weighted Rubric (`00_Brand/Channel-Setup/templates/TOPIC_OPPORTUNITY_SCORE.md`)

| Dimension | Weight | Score (1–10) | Weighted | Evidence & Rationale |
|-----------|--------|--------------|----------|----------------------|
| **1. Evergreen search intent** | 25% | **10.0** | **2.50** | `"how did we measure the speed of light"` (`10` autocomplete suggestions incl. `"how did we measure the speed of light"`, `"how we first measured the speed of light"`), `"speed of light"` (`10` suggestions incl. `"speed of light"`, `"speed of light explained"`, `"speed of light experiment"`), and `"fizeau"` (`"fizeau experiment speed of light"`, `"fizeau's method to determine speed of light"`) all autocomplete (`suggest = yes`) in signed-out YouTube GB (`evidence_2026-11-14_public_search.json`, `evidence_2026-11-14_neighbours.json`). Top ranking videos on the exact query carry **`24,352,264` views** (`Veritasium` `pTn6Ewhb27k`), **`2,001,964` views** (`Rational Thinker` `Jl1I4MA-TaU`), **`1,130,896` views** (`Susskind Speaks` `QqcLRZdVBIg`), and **`799,836` views** (`Carter Studios - Physics` `8z1WR4b0hJY`). |
| **2. Competition gap (wonder / clarity vs dry or crowding)** | 20% | **9.0** | **1.80** | `Veritasium`'s `24.35M` hit (`pTn6Ewhb27k`) focuses on the relativistic one-way vs two-way clock-synchronisation paradox; `PBS Space Time` (`7.13M`), `Vsauce` (`10.05M`), and `Kurzgesagt` (`9.99M`) focus on relativity or electromagnetic theory; `Rational Thinker` (`2.00M`) is a 16-minute slideshow overview; `ayuta` (`512k`, `4:07`) is a silent/minimalist 3D diagram of Fizeau's gear. There is a clear opening for an `8–9 min` painted-3D History of Science film that puts the viewer inside the physical instruments (`1638` hilltop lanterns → `1676` Paris Observatory telescope timing Io → `1849` Suresnes–Montmartre `720`-tooth brass cogwheel → `1850` Foucault rotating mirror & water tube) with zero exact title collisions on any of our 5 disambiguated long/Short titles. |
| **3. Narrative & visual arc (3D world + diagram clarity)** | 20% | **10.0** | **2.00** | Every act turns on a tactile, photogenic physical mechanism: (1) two covered lanterns flashing across dark Florentine hills (`1638`), (2) Jupiter's moon Io slipping into Jupiter's shadow cone as Earth moves across its orbit (`1676`, `SCALE + DATA`), (3) Fizeau's `720`-tooth brass wheel spinning faster until a brass tooth physically blocks the returning pinpoint of light from Montmartre (`1849`, `0:05–0:15` proof-first cold open + `DATA` RPM/brightness plot), and (4) Foucault's high-speed rotating mirror splitting beams through air and water (`1850/1862`, `DATA` deflection angle). |
| **4. Brand & guardrail fit** | 20% | **10.0** | **2.00** | Pure History of Science house lane: starts from a universal everyday question (*how do we time something that crosses a room in nanoseconds using only gears and mirrors?*) and answers it through four chronological human experiments. Zero fearbait, zero medical advice, zero conspiracy, and zero overlap with existing HOS projects (`000–105`), `ideas/011–097`, or OWB relativity videos (`OWB:024`). |
| **5. Series / cluster potential** | 15% | **8.7** | **1.30** | Forms a high-demand **Light & Optics Experimental Cluster** alongside `018_Herschel-Ritter-Infrared` (invisible IR/UV spectrum, in `next_hos`), `025_Young-Fresnel-Einstein-Light` (wave-particle duality & Poisson spot, in `ideas/`), `032_Michelson-Morley-Aether` (1887 interferometer, in `ideas/`), `038_Doppler-Buys-Ballot-Wave-Shift` (Doppler shift), and `103_Rayleigh-Einstein-Smoluchowski-Blue-Sky` (Rayleigh scattering, pre-cleared in `next_hos` by `J2776`). Also connects directly to HOS's `#2` Short by both stayed-to-watch (`43.52%`) and avg % viewed (`105.30%`), `c2q7w0pgcn8` (*Who Discovered Infrared Light?*). |
| **Total** | **100%** | — | **`9.60 / 10` (`96 / 100`)** | **GO (`≥ 7.5` threshold exceeded by `+2.10` points)** |

**Rule:** Proceed (`GO`) if **Total ≥ 7.5** and **Brand fit ≥ 8**. Both pass (`9.60 / 10` total, `10.0 / 10` brand fit).

---

## 2. Education Neighbour Gate (`neighbours.py` + `public_search.py`, Retrieved `2026-11-14`)

Saved in [`evidence_2026-11-14_neighbours.json`](evidence_2026-11-14_neighbours.json) (`bigCount = 11`, `hasTed = true`, `gate = PASS`) and [`evidence_2026-11-14_public_search.json`](evidence_2026-11-14_public_search.json):

| # | Channel | Views (`2026-11-14`) | Video ID & URL | Title | Source File |
|---:|---|---:|---|---|---|
| 1 | **Veritasium** | `24,352,264` | [`pTn6Ewhb27k`](https://youtu.be/pTn6Ewhb27k) | *Why No One Has Measured The Speed Of Light* | `neighbours.json` + `public_search.json` |
| 2 | **Veritasium** | `17,596,419` | [`NIk_0AW5hFU`](https://youtu.be/NIk_0AW5hFU) | *There Is Something Faster Than Light* | `neighbours.json` |
| 3 | **Vsauce** | `10,047,754` | [`ACUuFg9Y9dY`](https://youtu.be/ACUuFg9Y9dY) | *Would Headlights Work at Light Speed?* | `neighbours.json` |
| 4 | **Kurzgesagt – In a Nutshell** | `9,990,677` | [`IXxZRZxafEQ`](https://youtu.be/IXxZRZxafEQ) | *What Is Light?* | `neighbours.json` |
| 5 | **PBS Space Time** | `7,134,459` | [`msVuCEs8Ydo`](https://youtu.be/msVuCEs8Ydo) | *The Speed of Light is NOT About Light* | `neighbours.json` |
| 6 | **minutephysics** | `4,304,501` | [`lR4tJr7sMPM`](https://youtu.be/lR4tJr7sMPM) | *How to break the speed of light* | `neighbours.json` |
| 7 | **TED-Ed ★** | `3,695,293` | [`Op3AYaJc0Xw`](https://youtu.be/Op3AYaJc0Xw) | *Light seconds, light years, light centuries: How to measure extreme distances - Yuan-Sen Ting* | `neighbours.json` |
| 8 | **3Blue1Brown** | `2,896,005` | [`KTzGBJPuJwM`](https://youtu.be/KTzGBJPuJwM) | *But why would light "slow down"? \| Visualizing Feynman's lecture on the refractive index* | `public_search.json` |
| 9 | **Veritasium** | `2,289,873` | [`vVKFBaaL4uM`](https://youtu.be/vVKFBaaL4uM) | *Can You Go the Speed of Light?* | `neighbours.json` (11th `≥1M` neighbour in `neighbours.json`) |
| 10 | **Rational Thinker** | `2,001,964` | [`Jl1I4MA-TaU`](https://youtu.be/Jl1I4MA-TaU) | *How the Speed of Light Was First Measured* | `public_search.json` |
| 11 | **TED-Ed ★** | `1,816,164` | [`J1yIApZtLos`](https://youtu.be/J1yIApZtLos) | *Is light a particle or a wave? - Colm Kelleher* | `neighbours.json` |
| 12 | **Fermilab** | `1,309,684` | [`CUjt36SD3h8`](https://youtu.be/CUjt36SD3h8) | *Why does light slow down in water?* | `public_search.json` |
| 13 | **TED-Ed ★** | `1,276,309` | [`O0PawPSdk28`](https://youtu.be/O0PawPSdk28) | *Light waves, visible and invisible* | `neighbours.json` |
| 14 | **Susskind Speaks** | `1,130,896` | [`QqcLRZdVBIg`](https://youtu.be/QqcLRZdVBIg) | *Why the Speed of Light Is NOT a Speed - Leonard Susskind* | `public_search.json` |
| 15 | **TED-Ed ★** | `1,015,443` | [`g12bxfYVhMk`](https://youtu.be/g12bxfYVhMk) | *How fast is the speed of thought? - Seena Mathew* | `neighbours.json` |

---

## 3. Cluster Sketch (3 Adjacent Episodes)

1. **`HOS:104` (This Episode):** *How Did We Measure the Speed of Light? (A 720-Tooth Wheel)* — Galileo's 1638 hilltop lanterns, Rømer's 1676 Jupiter moon Io eclipses, Fizeau's 1849 720-tooth brass wheel across Paris, and Foucault's 1850/1862 rotating mirror & water tube.
2. **`HOS:018` (`018_Herschel-Ritter-Infrared`, in `next_hos`):** *How Did a Thermometer Discover Invisible Light?* — William Herschel's 1800 prism thermometer beyond red and Johann Ritter's 1801 silver-chloride paper beyond violet.
3. **`HOS:103` (`103_Rayleigh-Einstein-Smoluchowski-Blue-Sky`, Rule-E `GO` in `next_hos`):** *Why Is the Sky Blue? (Tyndall's 1869 Glass Tube)* — John Tyndall's artificial sky in a glass tube, Lord Rayleigh's $\lambda^{-4}$ scattering law, and Einstein/Smoluchowski's thermal density fluctuations.
4. **`HOS:025` (`025_Young-Fresnel-Einstein-Light`, in `ideas/`):** *Is Light a Wave or a Particle?* — Thomas Young's 1801 double slit, Arago's 1818 bright spot behind a circular disc, and Einstein's 1905 photoelectric quanta.
