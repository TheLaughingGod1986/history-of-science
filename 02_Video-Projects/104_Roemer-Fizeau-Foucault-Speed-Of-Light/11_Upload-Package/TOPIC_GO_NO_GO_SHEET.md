# Rule-E Topic Go/No-Go Review Sheet — `HOS:104` (`104_Roemer-Fizeau-Foucault-Speed-Of-Light`)

| Field | Value |
|---|---|
| **Film ID & Slug** | `HOS:104` · `02_Video-Projects/104_Roemer-Fizeau-Foucault-Speed-Of-Light` |
| **Job ID & Reviewer** | `J2810` (`macbook` on `gemini-argon` / `gemini-agy`, `review` lane) |
| **Reviewed PRs** | HOS PR [`#581`](https://github.com/TheLaughingGod1986/history-of-science/pull/581) (`gemini/J2809-hos-topics-104-105`) · OWB PR [`#916`](https://github.com/TheLaughingGod1986/orbit-with-ben/pull/916) (`gemini/J2809-hos-topics-104-105`) |
| **Date** | `2026-11-14` |
| **Rule-E Verdict** | **GO (`96 / 100` · `9.60 / 10` Opportunity Score) — Pre-cleared in `jobs/WIP.json` `next_hos` under Rule G** |
| **Production & Claim Status** | **NOT CLEARED FOR SCRIPT LOCK, VO, OR PICTURE SPEND.** All historical and scientific claims in `TOPIC.md` §2–§3 and `PRE_BUILD_VIDIQ_AUDIT.md` remain **UNVERIFIED** working notes until an active HOS WIP slot opens (`len(WIP.json["hos"]) < 6`) and exact primary-source quotes are verified in `SOURCES.md` via the `facts` lane (`gemini-agy`). |

---

## 1. Rule-E Gate-by-Gate Audit

| # | Rule-E Gate (`AGENTS.md` / `STUDIO_PLAYBOOK.md` §2 / `LEARNINGS.md`) | Threshold / Requirement | Measured Evidence (`104_Roemer-Fizeau-Foucault-Speed-Of-Light`) | Status |
|---:|---|---|---|---|
| **1** | **Learn from our data first (`AGENTS.md` / `J2748` Ruling #2–#4)** | Compare top 3 and bottom 3 longs & Shorts by a single consistent primary metric (`views/day`) with exact snapshot timestamps, numerators, and elapsed-day denominators; separate rankings by other metrics; `UNKNOWN` where views are too few; patterns framed as hypotheses | `TOPIC.md` §1 cites `2026-11-12T06:40:28.196Z` and `2026-11-13T06:40:29.166Z` snapshots + `2026-11-12T07:07:54.728116+00:00` lifetime `studio_ctr.json`; ranks all `7` public longs and `28` public Shorts by `views/day` (`PFj6172YU4Q` `215v / 4d = 53.8/d` on `12 Nov`, `216v / 5d = 43.2/d` on `13 Nov`); separates impressions, CTR, stayed-to-watch (`-3L6HzJ_d_4` `76.47%`), and avg % viewed (`pWySvZsneZg` `112.43%`, `c2q7w0pgcn8` `105.30%`); marks `<10`-view curves `UNKNOWN` | **PASS** |
| **2** | **Signed-out YouTube autocomplete (`LEARNINGS.md` Rule 26)** | Primary search phrase must autocomplete (`suggest = yes`) in signed-out YouTube GB (`public_search.py`) | `"how did we measure the speed of light"` = **yes** (`10` suggestions incl. `"how did we measure the speed of light"`, `"how we first measured the speed of light"`) · `"speed of light"` = **yes** (`10` suggestions incl. `"speed of light"`, `"speed of light explained"`, `"speed of light experiment"`) · `"fizeau"` = **yes** (`"fizeau experiment speed of light"`, `"fizeau's method to determine speed of light"`) in `11_Upload-Package/evidence_2026-11-14_public_search.json` & `evidence_2026-11-14_neighbours.json` | **PASS** |
| **3** | **Two ranking videos named (`LEARNINGS.md` Rule 26a)** | Name 2 live ranking videos on the phrase with IDs and view counts | 1) **Veritasium** [`pTn6Ewhb27k`](https://youtu.be/pTn6Ewhb27k) (*Why No One Has Measured The Speed Of Light*, **`24,352,264` views**) · 2) **Rational Thinker** [`Jl1I4MA-TaU`](https://youtu.be/Jl1I4MA-TaU) (*How the Speed of Light Was First Measured*, **`2,001,964` views**), plus **Susskind Speaks** [`QqcLRZdVBIg`](https://youtu.be/QqcLRZdVBIg) (**`1,130,896` views**), **Carter Studios - Physics** [`8z1WR4b0hJY`](https://youtu.be/8z1WR4b0hJY) (**`799,836` views**), and **ayuta** [`a6gl8KZM0PM`](https://youtu.be/a6gl8KZM0PM) (*How to find the speed of light (Fizeau experiment)*, **`512,454` views**) | **PASS** |
| **4** | **Education neighbour gate (`STUDIO_PLAYBOOK.md` §2 Step 4)** | `neighbours.py` must return `≥ 3` education videos with `≥ 1,000,000` views (`gate: PASS`) and TED/TED-Ed presence | **`11` education videos `≥ 1,000,000` views (`gate = PASS`, `hasTed = true`)** in `11_Upload-Package/evidence_2026-11-14_neighbours.json`: Veritasium `pTn6Ewhb27k` (`24.35M`), Veritasium `NIk_0AW5hFU` (`17.60M`), Vsauce `ACUuFg9Y9dY` (`10.05M`), Kurzgesagt `IXxZRZxafEQ` (`9.99M`), PBS Space Time `msVuCEs8Ydo` (`7.13M`), minutephysics `lR4tJr7sMPM` (`4.30M`), TED-Ed ★ `Op3AYaJc0Xw` (`3.70M`), Veritasium `vVKFBaaL4uM` (`2.29M`), TED-Ed ★ `J1yIApZtLos` (`1.82M`), TED-Ed ★ `O0PawPSdk28` (`1.28M`), TED-Ed ★ `g12bxfYVhMk` (`1.02M`), plus 3Blue1Brown `KTzGBJPuJwM` (`2.90M`), Rational Thinker `Jl1I4MA-TaU` (`2.00M`), and Fermilab `CUjt36SD3h8` (`1.31M`) in `public_search.py` | **PASS** |
| **5** | **Exact title collision check (`public_search.py`)** | `0` exact title collisions on Long Titles A, B, C and Short Titles `S01`, `S02` | **Title A:** `How Did We Measure the Speed of Light? (A 720-Tooth Wheel)` (`58 chars`, `0` collisions; disambiguated from bare `How Did We Measure the Speed of Light?` on `Exploded View` `jMyuc5-1QF8`) · **Title B:** `The 720-Tooth Wheel That Measured the Speed of Light` (`52 chars`, `0` collisions) · **Title C:** `Speed of Light: How a 720-Tooth Wheel Measured It in 1849` (`57 chars`, `0` collisions) · **S01:** `How Did Jupiter's Moons Measure the Speed of Light?` (`51 chars`, `0` collisions) · **S02:** `Why Does Light Slow Down in Water? (Foucault's 1850 Test)` (`57 chars`, `0` collisions; disambiguated from bare `Why does light slow down in water?` on `Fermilab` `CUjt36SD3h8`) | **PASS** |
| **6** | **Non-duplication check (`AGENTS.md`)** | Zero overlap with `02_Video-Projects/`, `00_Brand/Channel-Setup/ideas/`, `VIDEO_BACKLOG.json`, and `jobs/WIP.json` (`hos` + `next_hos` + `owb`) | Verified across `02_Video-Projects/000–105`, `ideas/011–097`, `VIDEO_BACKLOG.json`, and `WIP.json`. (`018` covers Herschel IR / Ritter UV wavelengths; `021` covers Maxwell's `1865` electromagnetic equations; `025` covers Young's double-slit & Einstein's photoelectric effect; `032` covers Michelson–Morley's `1887` aether interferometer null result; `038` covers Buys Ballot's `1845` acoustic Doppler train test; `103` covers Rayleigh blue-sky scattering; `OWB:024` covers near-$c$ relativistic time dilation / muons / twin paradox with zero mention of Galileo, Rømer, Fizeau, or Foucault) | **PASS** |
| **7** | **Visual proof-first hook (`0:05–0:15`, `LEARNINGS.md` Rule 10 & Rule 30 `HOS-2026-11-E2`)** | Concrete physical experiment / mechanism in first `15 s`; zero *"By the end of this film..."* agenda line | Cold open on Hippolyte Fizeau's spinning **720-tooth brass cogwheel** in a Paris tower slicing a lantern beam aimed at a distant mirror on Montmartre (`0:05–0:15` mechanical eclipse of the returning flash), followed by `4` chronological acts (`1638 -> 1676 -> 1849 -> 1850/1862`) and `SCALE/DATA/WHEN` overlays | **PASS** |
| **8** | **Two search-titled Shorts (`LEARNINGS.md` Rules 1, 2, 24, 27, 28)** | `2` question-titled Shorts (`22–27 s`), `0%` Explorer & `0%` bars on Frame 0, `0.0 s` 2–3 word hook text (`#FFE000` key word), payoff `≥70%` runtime, `<1.0 s` loop tail, zero CTA | `S01` (*How Did Jupiter's Moons Measure the Speed of Light?*, `51 chars`, Frame 0 `1676 ECLIPSE` on Io entering Jupiter's shadow cone) and `S02` (*Why Does Light Slow Down in Water? (Foucault's 1850 Test)*, `57 chars`, Frame 0 `SLOWER IN WATER` on Foucault's rotating mirror and water tube) | **PASS** |
| **9** | **Unverified claims guard (`J2748` Ruling #4 / `J2810` brief)** | All historical & scientific claims marked **UNVERIFIED**; `01_Script/episode_script_draft_v01.md` untouched template until `SOURCES.md` + `facts` lane | Confirmed in `TOPIC.md` notice + §2–§3, `PRE_BUILD_VIDIQ_AUDIT.md` notice, `production-status.md`, `README.md`, and `01_Script/episode_script_draft_v01.md` (untouched template) | **PASS** |
| **10** | **WIP cap & spend guard (`AGENTS.md` Rule G)** | `£0.00` / `0` credits spent; `status.json` all stages `"todo"` while in `jobs/WIP.json` `next_hos` | `£0.00` spent; all `12` stages in `status.json` remain `"state": "todo"` (`status_board.py --check` PASS) | **PASS** |

---

## 2. Opportunity Score Summary (`9.60 / 10` = `96 / 100`)

See [`TOPIC_OPPORTUNITY_SCORE.md`](TOPIC_OPPORTUNITY_SCORE.md) for the full 5-dimension rubric breakdown:

| Dimension | Weight | Score (1–10) | Weighted |
|---|---:|---:|---:|
| 1. Evergreen search intent | 25% | `10.0` | `2.50` |
| 2. Competition gap (wonder / clarity vs dry or crowding) | 20% | `9.0` | `1.80` |
| 3. Narrative & visual arc (3D world + diagram clarity) | 20% | `10.0` | `2.00` |
| 4. Brand & guardrail fit | 20% | `10.0` | `2.00` |
| 5. Series / cluster potential | 15% | `8.7` | `1.30` |
| **Total Opportunity Score** | **100%** | — | **`9.60 / 10` (`96 / 100`)** |

---

## 3. Mandatory Gate Before Any Script Lock or VO (`Rule G` + `facts` Lane)

1. **Wait for an open active HOS WIP slot (`jobs/WIP.json`):** Active `hos` has `6 / 6` slots full (`007`, `008`, `009`, `010`, `011`, `013`). `HOS:104` stays in `next_hos` with all `status.json` stages `"todo"` until a slot opens.
2. **Primary-source verification (`SOURCES.md` + `facts` lane `gemini-agy`):**
   - **Galileo Galilei (`1638`, *Discorsi e Dimostrazioni Matematiche intorno a due nuove scienze*, First Day):** Exact quote for the two-observer covered-lantern proposal and Sagredo/Salviati dialogue conclusion.
   - **Ole Rømer (`7 December 1676`, *Journal des Sçavans*, *"Démonstration touchant le mouvement de la lumière trouvé par M. Römer"*) & Christiaan Huygens (`1690`, *Traité de la Lumière*):** Exact quotes for Io's `42.5`-hour period, cumulative eclipse delay across Earth's orbit, and Huygens's diameter/speed calculation.
   - **Hippolyte Fizeau (`23 July 1849`, *Comptes Rendus de l'Académie des Sciences*, vol. 29, pp. 90–92, *"Sur une expérience relative à la vitesse de propagation de la lumière"*):** Exact quote for the Suresnes–Montmartre path length (`8,633 m`), `720`-tooth brass wheel, rotation speed (`12.6 rev/s`), and calculated velocity.
   - **Léon Foucault (`6 May 1850` & `1862`, *Comptes Rendus*, vol. 30, pp. 551–560 & vol. 55, pp. 501–503 / 792–796):** Exact quotes for the steam/air-driven rotating mirror, the water-tube retardation proof (`1850`), and the `298,000 km/s` determination (`1862`).
