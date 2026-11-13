# HOS 103 — Topic Proposal & Data Learnings (`J2748`, Corrected 13 Nov 2026)

| Field | Value |
|---|---|
| **ID / Folder** | `HOS:103` — `02_Video-Projects/103_Tyndall-Rayleigh-Why-Is-The-Sky-Blue` |
| **Rule-E Topic Review Status (`J2776`, 13 Nov 2026)** | **`GO` (`95 / 100` Opportunity Score) — PRE-CLEARED IN BACKLOG `next_hos` UNDER RULE G (Recorded for Chief Review; Not Yet in Active Production).** Waiting in `jobs/WIP.json` `next_hos` on OWB PR `#881`. See [`11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md`](11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md), [`11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md`](11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md), and `orbit-with-ben` `jobs/reviews/J2776/REVIEW.md`. |
| **Working Title A (Rule 26 Exact Search Phrase First + Stakes, `46 chars`, `0` exact collisions)** | **Why Is the Sky Blue? (And Why It Isn't Violet)** |
| **Title B (Rule 26 Exact Search Phrase First + Apparatus, `52 chars`, `0` exact collisions)** | **Why Is the Sky Blue? (The Glass Tube That Solved It)** |
| **Title C (Story + Apparatus Hook, `49 chars`, `0` exact collisions)** | **The 1869 Glass Tube That Put Blue Sky in a Bottle** |
| **Verified Plain Search Phrases (`public_search.py`, retrieved `2026-11-13`)** | `"why is the sky blue"` (`autocomplete = yes`), `"rayleigh scattering"` (`autocomplete = yes`), `"why are sunsets red"` (`autocomplete = yes`), `"why isn't the sky violet"` (`related autocomplete = "why isn't the sky purple", "why is the sky purple"`), `"Why Is the Sky Blue? (And Why It Isn't Violet)"` (`related autocomplete = "why is the sky blue and not violet"`) |
| **Two Ranking Videos for Plain Search Phrase (`"why is the sky blue"`, retrieved `2026-11-13`)** | 1. **StarTalk** — *Neil deGrasse Tyson Explains Why The Sky Is Blue* (`https://youtu.be/UvmWxm3nR6E`, **`3,394,689` views**, retrieved `2026-11-13`)<br>2. **Netflix Jr.** — *Why is the Sky Blue \| Ask the Storybots \| Netflix Jr* (`https://youtu.be/Ldm_9LsKblU`, **`1,050,550` views**, retrieved `2026-11-13`; alongside **NASA Space Place** *Why Is the Sky Blue?* `https://youtu.be/ehUIlhKhzDA`, **`937,900` views**, and **Veritasium** *Why the Sky ISN'T Blue* `https://youtu.be/ro2MmmdARrs`, **`1,536,981` views**) |
| **Saved Tool Evidence (`2026-11-13`)** | `11_Upload-Package/evidence_2026-11-13_neighbours.json` (`neighbours.py`)<br>`11_Upload-Package/evidence_2026-11-13_public_search.json` (`public_search.py`) |
| **Facts & Script Status** | **UNVERIFIED — NOT CLEARED FOR NARRATION OR SHORT OPENS.** No spoken draft is approved. All historical and scientific claims (including Saussure's cyanometer dates, Tyndall's 1869 vapour-tube reagents, Rayleigh's $\lambda^{-4}$ scattering ratio, and the solar-spectrum / ocular-cone explanation for why the sky is not violet) must be sourced with exact quotes in `SOURCES.md` and checked through the `facts` lane before any script lock. |
| **Spend** | **£0** (no paid API, TTS, or picture generation; no Studio or publish change) |

---

## 0. Mandatory Public-Search Probe (`J2748` Routing Preflight, 13 Nov 2026)

Per `J2748` routing instructions (`desk 6853484674`), `public_search.py` was probed from the Mac mini before making any corrections:

```text
$ python3 00_Brand/Channel-Setup/tools/public_search.py "why is the sky blue"
| Phrase | Autocomplete? | Top results (GB) |
|---|---|---|
| why is the sky blue | yes | NASA Space Place 937,917 · Nick Cope 614,123 · SciShow Kids 530,954 · StarTalk 3,394,689 · Netflix Jr. 1,050,542 |
```

---

## 1. Learn From Our Data First (Corrected Analytics Comparison — `2026-11-12` & `2026-11-13` Snapshots vs Lifetime Studio Read)

The full per-video tables for all eligible public longs (`6` settled + `007` newly public on `12 Nov 18:00Z`) and all `28` public Shorts are in [`../102_Molina-Rowland-Farman-Ozone-Hole/TOPIC.md` §1](../102_Molina-Rowland-Farman-Ozone-Hole/TOPIC.md). Key methodology and rankings summary:

### 1.1 Data Sources, Timestamps, Numerators & Elapsed-Day Convention
- **Snapshots:** `05_Analytics/hos/snapshots/2026-11-12.json` (`takenAt: 2026-11-12T06:40:28.196Z`, `last28`/`last7` settled through `2026-11-10`) and `2026-11-13.json` (`takenAt: 2026-11-13T06:40:29.166Z`, `last28`/`last7` settled through `2026-11-11`).
- **Views/day convention (`channel-tracker.ts:596,611`):** Numerator = snapshot `video.views`; denominator = `ageDays = max(daysBetween(publishedAt.slice(0, 10), snapshot.date), 1)` (UTC calendar-day difference, floored at `1` day); `views/day = round((views / ageDays) * 10) / 10`.
- **Lifetime Studio Scrape (`05_Analytics/hos/studio_ctr.json`):** Read at `2026-11-12T07:07:54.728116+00:00` (`period: "lifetime"`). Kept strictly separate from rolling 28-day YouTube Analytics (`YTA`) windows.

### 1.2 Top 3 and Bottom 3 Public HOS Longs by `Views/Day` (Consistent Metric Ranking)
- **Top 3 Longs by `Views/Day` (`12 Nov` and `13 Nov` snapshots):**
  1. **`AL_-qlWko_g` (`002`, *How Did We Discover the Periodic Table?*, `541 s`):** `2.9/day` on `12 Nov` (`161v / 56d`) and `2.8/day` on `13 Nov` (`161v / 57d`); lifetime Studio (`12 Nov`): `1,141` impressions, `3.42%` CTR, `21.59%` avg viewed (`1:56`), stayed `not applicable`; YTA retention curve (`161` views): `75.0%` at `0:11`, `70–71%` at `0:15`, `51%` at `0:30`, `43%` at `1:00`.
  2. **`GHZDsiH7L7A` (`004`, *What's Inside an Atom? Mostly Empty Space*, `525 s`):** `1.1/day` on `12 Nov` (`32v / 28d`, `#2`) and `1.1/day` on `13 Nov` (`33v / 29d`, `#3`); lifetime Studio (`12 Nov`): `816` impressions, `1.23%` CTR, `20.89%` avg viewed (`1:49`), stayed `not applicable`; YTA retention curve (`31` views): `61%` at `0:15`, `41%` at `0:30`, `32%` at `1:00`.
  3. **`VbPubYd6Fbs` (`006`, *The Willow Tree That Was Made of Air*, `532 s`):** `0.6/day` on `12 Nov` (`4v / 7d`, `#3`) and `1.3/day` on `13 Nov` (`10v / 8d`, `#2`); lifetime Studio (`12 Nov` on `2` Studio views): `22` impressions, `0.0%` CTR, `99.99%` avg viewed (`8:51` on `n=2` views — sample too small to interpret), YTA curve `UNKNOWN` (`too few views`), stayed `not applicable`.
- **Bottom 3 Settled Longs by `Views/Day` (`≥7` days public):**
  1. **`frP_YrNShsU` (`003`, *How Did We Discover X-rays?*, `426 s`):** `0.1/day` (`5v / 49d` on `12 Nov`; `5v / 50d` on `13 Nov`); lifetime Studio: `41` impressions, `2.44%` CTR, `26.65%` avg viewed (`1:53` on `5` views), curve `UNKNOWN`, stayed `not applicable`.
  2. **`_C92tIJCk8A` (`001`, *How Did We Discover Germs?*, `365 s`):** `0.1/day` (`7v / 70d` on `12 Nov`; `7v / 71d` on `13 Nov`); lifetime Studio: `44` impressions, `6.82%` CTR, `48.08%` avg viewed (`2:55` on `7` views), curve `UNKNOWN`, stayed `not applicable`.
  3. **`wwcjcFfC-5M` (`005`, *The Tied Arm That Proved Your Blood Circulates*, `529 s`):** `0.4/day` on `12 Nov` (`5v / 14d`) and `0.3/day` on `13 Nov` (`5v / 15d`); lifetime Studio: `14` impressions, `21.43%` CTR (`n=14` impr), `9.24%` avg viewed (`0:48` on `5` views), curve `UNKNOWN`, stayed `not applicable`. *(Newly public `007` `ETynHpIYLeY` has `0.0/day` [`0v / 1d`] on `13 Nov`, all Studio metrics `UNKNOWN`.)*
- **Separate Long Rankings by Other Metrics:** By **Lifetime Studio Impressions**: `002` (`1,141`) → `004` (`816`) → `001` (`44`) → `003` (`41`) → `006` (`22`) → `005` (`14`). By **Lifetime Studio Avg % Viewed** (`≥30` views): `002` (`21.59%` on `161` v) → `004` (`20.89%` on `31` v); all `<10`-view averages (`006` `99.99%` on `2` v, `001` `48.08%` on `7` v, `003` `26.65%` on `5` v, `005` `9.24%` on `5` v) have too few views to establish a winning or losing retention format.

### 1.3 Top 3 and Bottom 3 Public HOS Shorts by `Views/Day` (Plus Separate Retention Rankings)
- **Top 3 Shorts by `Views/Day`:**
  1. **`PFj6172YU4Q` (`005`, *One Tight Band Proved Your Blood Goes Round*, `27 s`):** `53.8/day` on `12 Nov` (`215` views across **`4` elapsed days**, `2026-11-08` to `2026-11-12`) and `43.2/day` on `13 Nov` (`216` views across **`5` elapsed days**, `#2` on `13 Nov`); lifetime Studio: `218` views, `15.21%` stayed (`MISS`), `61.08%` avg viewed (`0:16`), CTR `not applicable`.
  2. **`29bpGAI0wb8` (`004`, *What happens if you keep cutting gold in half?*, `25 s`):** `45.4/day` on `12 Nov` (`1,226v / 27d`, `#2`) and `43.8/day` on `13 Nov` (`1,226v / 28d`, `#1`); lifetime Studio: `1,226` views, `40.78%` stayed (`MISS`), `44.12%` avg viewed (`0:11`), CTR `not applicable`.
  3. **`AMSriTQ-lcQ` (`004`, *Are Marie Curie's Notebooks Still Radioactive?*, `22 s`):** `18.3/day` on `12 Nov` (`274v / 15d`) and `17.1/day` on `13 Nov` (`274v / 16d`); lifetime Studio: `274` views, `22.66%` stayed (`MISS`), `76.94%` avg viewed (`0:16`, `PASS`), CTR `not applicable`.
- **Bottom 3 Shorts by `Views/Day`:**
  1. **`LanTHJckYx8` (`002`, *What other table has empty chairs?*, `26 s`):** `0.1/day` (`4v / 51d` on `12 Nov`, `52d` on `13 Nov`); lifetime Studio (`n=4`): `33.33%` stayed, `23.08%` avg viewed (`0:06`), CTR `not applicable`.
  2. **`zI_eD3vFWmE` (`003`, *The first X-ray showed a wedding ring*, `25 s`):** `0.2/day` (`9v / 46d` on `12 Nov`, `47d` on `13 Nov`); lifetime Studio (`n=9`): `50.00%` stayed, `64.00%` avg viewed (`0:16`), CTR `not applicable`.
  3. **`CnHwX1L9XHg` (`002`, *Gallium sat where the table said*, `26 s`):** `0.3/day` (`16v / 53d` on `12 Nov`, `54d` on `13 Nov`); lifetime Studio (`n=16`): `30.43%` stayed, `33.45%` avg viewed (`0:08`), CTR `not applicable`.
- **Separate Short Rankings (`≥100` Studio Views):**
  - **By Stayed-to-Watch:** `#1` `-3L6HzJ_d_4` (*What Is the Pasteur Swan Neck Flask Experiment?*, `19 s`, `122` v: **`76.47%` stayed**, `74.54%` avg viewed, `92%` of 28d views from `YT_SEARCH`) → `#2` `c2q7w0pgcn8` (*Who Discovered Infrared Light?*, `23 s`, `138` v: **`43.52%` stayed**, `105.30%` avg viewed) → `#3` `29bpGAI0wb8` (`1,226` v: **`40.78%` stayed**) → `#4` `oKqmnJNGiHg` (`183` v: **`40.30%` stayed**, `87.29%` avg viewed).
  - **By Avg % Viewed:** `#1` `pWySvZsneZg` (`137` v: **`112.43%`**) → `#2` `c2q7w0pgcn8` (`138` v: **`105.30%`**) → `#3` `oKqmnJNGiHg` (`183` v: **`87.29%`**) → `#4` `AMSriTQ-lcQ` (`274` v: **`76.94%`**) → `#5` `-3L6HzJ_d_4` (`122` v: **`74.54%`**). *(Note: `>100%` avg viewed on `pWySvZsneZg` and `c2q7w0pgcn8` is consistent with viewer replay/rewatching alongside short `0.30–1.00 s` tails and late payoffs, not proof of an intentional seamless loop alone.)*

---

## 2. Topic Proposal — `HOS:103` (*Why Is the Sky Blue? (And Why It Isn't Violet)*)

> **UNVERIFIED HISTORICAL & SCIENTIFIC CLAIMS NOTICE (Correction 4):**
> Every date, person, apparatus detail, and scientific number in §2 and §3 below — including Horace-Bénédict de Saussure's cyanometer dates, John Tyndall's 1869 vapour-tube reagents, Lord Rayleigh's 1871 and 1899 scattering papers ($\propto \lambda^{-4}$), and the three-part explanation for why the sky looks blue rather than violet (solar spectrum peak, atmospheric absorption, and human cone-cell sensitivity) — is **UNVERIFIED** and **NOT CLEARED FOR NARRATION OR SHORT OPENS**. No spoken script draft is approved (`01_Script/episode_script_draft_v01.md` remains the blank template). Before any script lock, every claim must be backed by an exact quote in `SOURCES.md` and verified through the `facts` lane (`gemini-agy`).

### 2.1 One-Line Hook & Candidate Discovery Outline (Unverified Working Notes)
- **One-line hook (unverified):** In 1869 John Tyndall shone a laboratory lamp through a glass tube of fine vapour to create an artificial blue sky and a red sunset on a bench at the Royal Institution — setting up Lord Rayleigh's scattering law and the puzzle of why our sky looks blue rather than violet.
- **Candidate 4-act outline to verify in `SOURCES.md` before scripting:**
  1. **Horace-Bénédict de Saussure (c. 1789, *UNVERIFIED*):** Invents the **cyanometer** (a ring of graduated Prussian-blue paper shades) and carries it up Alpine peaks (Mont Blanc / Col du Géant) to measure sky blueness against altitude. *(Requires exact primary/secondary source quote on year, number of shades, and altitude observation.)*
  2. **John Tyndall at the Royal Institution (January 1869, *UNVERIFIED*):** Passes a beam of white light through a long glass tube containing trace vapour (e.g. butyl nitrite + hydrochloric acid — verify exact reagent in Tyndall's *Proc. R. Soc. Lond.* 1869 paper). As sub-microscopic particles form, the tube glows deep azure blue from the side (polarised at $90^\circ$) while the transmitted beam at the far end turns orange-red.
  3. **Lord Rayleigh / John William Strutt (1871 & 1899, *UNVERIFIED*):** Derives that particles much smaller than the wavelength of light scatter intensity inversely with the fourth power of wavelength ($I \propto \lambda^{-4}$), and later (`1899`) shows that air molecules ($N_2, O_2$) themselves suffice without dust or water droplets. *(Requires exact quotes from Strutt's Feb/Apr 1871 and Apr 1899 *Phil. Mag.* papers, including the exact blue-vs-red scattering ratio.)*
  4. **The Violet Puzzle (*UNVERIFIED*):** Because violet light (`~400 nm`) has a shorter wavelength than blue (`~470 nm`), Rayleigh's $\lambda^{-4}$ law scatters violet even more strongly than blue. Verify in `SOURCES.md` (e.g. Smith 2005 *Am. J. Phys.* `73(7):590–597` or equivalent peer-reviewed optics source) the exact combination of solar spectrum irradiance and human photopic cone response (`S`, `M`, `L` cones) that makes the scattered spectrum register as pale blue rather than violet.
- **Planned Teach-on-Screen Visuals (Once Sourced):** `DATA + SCALE`: relative $\lambda^{-4}$ scattering strength across red, green, blue, and violet wavelengths; `DATA`: optical path length through the atmosphere at noon vs sunset; `WHEN`: timeline (`1789 -> 1869 -> 1871 -> 1899`); `WHO` cards for Saussure, Tyndall, and Rayleigh; `FACT`: sourced planetary comparison (e.g. Mars dust-scattered sunsets, only if verified in `SOURCES.md`).
- **3-Way Thumbnail Concept Plan (Rule 12 / Rule 14 — Concepts Only, Zero Spend):**
  - **Thumb A (Apparatus Proof):** Painted 3D house style: John Tyndall's darkened 1869 Royal Institution bench with a glass tube glowing brilliant azure blue along its barrel and casting a red sunset disc onto a screen at the end; Explorer small lower-left; serif text on left band: `SKY IN A TUBE` (`4 words` or `BLUE IN A TUBE` `4 words` -> `MADE IN A TUBE` `4 words`; house 2–3 word version: `SKY IN GLASS` `3 words`).
  - **Thumb B (Rule 14 Bright High-Contrast Variant):** Split daylight sky: left side familiar azure blue, right side deep ultraviolet/violet with a glowing `400 nm` vs `470 nm` prism beam; serif text: `WHY NOT VIOLET?` (`3 words`).
  - **Thumb C (Instrument):** Saussure's circular numbered **cyanometer** wheel held up against a deep Alpine sky over snow-capped peaks; serif text: `53 SHADES` (`2 words`, exact number to be verified in `SOURCES.md`).

### 2.2 Why Our Data Suggests Testing This Topic (Hypotheses, Not Guarantees)
1. **Plain Search Question + Bracketed Twist (Rule 26 Hypothesis):** `"why is the sky blue"` is a verified YouTube GB autocomplete phrase (`suggest = yes`, retrieved `2026-11-13`), and our full candidate title `Why Is the Sky Blue? (And Why It Isn't Violet)` triggers the related YouTube autocomplete `"why is the sky blue and not violet"` while having `0` exact title collisions. On our channel, our two highest-impression longs (`002` Periodic Table `1,141` impr, `2.8–2.9/d`; `004` Atom `816` impr, `1.1/d`) use plain question leads on core physical-science subjects — though as `003` (*How Did We Discover X-rays?*, `41` impr, `0.1/d`) and `001` (*How Did We Discover Germs?*, `44` impr, `0.1/d`) show, a plain question title is a **hypothesis**, not an automatic guarantee of impressions.
2. **Physical Bench Apparatus in `0:05–0:15` (Rule 10 & Rule 30 `HOS-2026-11-E2` Hypothesis):** Tyndall's glowing glass tube at the Royal Institution gives a tangible benchtop apparatus for the `0:05–0:15` proof window (testing whether a physical optics experiment holds early viewers similarly to `002`'s `70–71%` at `0:15` and `004`'s `61%` at `0:15`).
3. **Optics & Light Sibling Hypothesis:** Among our Shorts with `≥100` views, `c2q7w0pgcn8` (*Who Discovered Infrared Light?*, `23 s`, `138` Studio views, `5.6–5.8/d`) reached `43.52%` stayed-to-watch (`#2` among `≥100`-view Shorts) and `105.30%` avg viewed (`#2`, consistent with viewer replay). Testing another classic Royal Institution / British optics discovery (`Tyndall 1869` / `Rayleigh 1871`, one generation after Herschel's `1800` prism) tests whether hands-on light experiments continue to hold viewers.

---

### 2.3 Complete Neighbour & Public-Search Evidence (`2026-11-13`)

#### A. Eight Actual On-Topic Education Videos (`≥1,000,000` Views) with URLs, View Counts & Retrieval Date
Retrieved `2026-11-13` via `neighbours.py` and `public_search.py` (saved in `11_Upload-Package/evidence_2026-11-13_neighbours.json` and `11_Upload-Package/evidence_2026-11-13_public_search.json`):

| # | Channel | Video Title & URL | View Count (Retrieved `2026-11-13`) | Length & Age | Relevance to `HOS:103` | Tool Source |
|---:|---|---|---:|---|---|---|
| **1** | **Be Smart** (`Tier 2` in `neighbours.py`) | [*Why Is Blue So Rare In Nature?*](https://youtu.be/3g246c6Bv58) | **`26,613,295` views** | `8:21` · 8 yr ago | Physics of structural blue and short-wavelength light scattering (`foundBy: "why the sky isn't blue"`) | `neighbours.py` (`#5` in table) |
| **2** | **Kurzgesagt – In a Nutshell** (`Tier 2` in `neighbours.py`) | [*What Is Light?*](https://youtu.be/IXxZRZxafEQ) | **`9,990,176` views** | `4:39` · 11 yr ago | Electromagnetic spectrum, visible wavelengths (`400–700 nm`), and why human eyes evolved for the Sun's visible window | `neighbours.py` (`#6` in table) |
| **3** | **StarTalk** (Science explainer via `public_search.py`) | [*Neil deGrasse Tyson Explains Why The Sky Is Blue*](https://youtu.be/UvmWxm3nR6E) | **`3,394,689` views** | `13:12` · 6 yr ago | Direct explainer on Rayleigh scattering, blue sky, and red sunsets (`#4`/`#5` GB result for `"why is the sky blue"`) | `public_search.py` (`"why is the sky blue"`) |
| **4** | **3Blue1Brown** (`Tier 2` in `neighbours.py`) | [*How wiggling charges give rise to light*](https://youtu.be/aXRTczANuIs) | **`1,900,703` views** | `21:33` · 3 yr ago | Dipole radiation and frequency-dependent light scattering | `neighbours.py` (`#7` in table) |
| **5** | **TED-Ed ★** (`Tier 1` in `neighbours.py`) | [*Is light a particle or a wave? - Colm Kelleher*](https://youtu.be/J1yIApZtLos) | **`1,816,004` views** | `4:24` · 13 yr ago | Wave optics foundation for wavelength-dependent scattering | `neighbours.py` (`#1` in table) |
| **6** | **Veritasium** (`Tier 2` in `neighbours.py`) | [*Why the Sky ISN'T Blue*](https://youtu.be/ro2MmmdARrs) | **`1,536,981` views** | `7:53` · 13 yr ago | Direct explainer on Rayleigh scattering and why the sky's scattered spectrum is not pure blue/violet | `neighbours.py` (`#8` in table) |
| **7** | **minutephysics** (`Tier 2` in `neighbours.py`) | [*Why Isn't The Sky Purple?*](https://youtu.be/R5P6O0pDyMU) | **`1,382,559` views** | `3:10` · 12 yr ago | Direct explainer on the exact twist of `HOS:103` (Rayleigh scattering + solar spectrum + human cone cells) | `neighbours.py` (`#9` in table) |
| **8** | **minutephysics** (`Tier 2` in `neighbours.py`) | [*Why is the Sun Yellow and the Sky Blue?*](https://youtu.be/NafbGOQBlQs) | **`1,363,672` views** | `1:59` · 12 yr ago | Direct explainer on Rayleigh scattering removing short wavelengths from direct sunlight | `neighbours.py` (`#10` in table) |
| **9** | **TED-Ed ★** (`Tier 1` in `neighbours.py`) | [*Light waves, visible and invisible - Lucianne Walkowicz*](https://youtu.be/O0PawPSdk28) | **`1,275,823` views** | `5:58` · 13 yr ago | Electromagnetic spectrum and atmospheric transmission/scattering | `neighbours.py` (`#2` in table) |
| **10** | **Netflix Jr.** (Education via `public_search.py`) | [*Why is the Sky Blue \| Ask the Storybots \| Netflix Jr*](https://youtu.be/Ldm_9LsKblU) | **`1,050,550` views** | `1:40` · 9 yr ago | Direct `"why is the sky blue"` explainer (`#4` GB result) | `public_search.py` (`"why is the sky blue"`) |
| **11** | **NASA Space Place** (Official agency explainer via `public_search.py`) | [*Why Is the Sky Blue?*](https://youtu.be/ehUIlhKhzDA) | **`937,900` views** | `2:49` · 6 yr ago | Direct `"why is the sky blue"` explainer (`#1`/`#2` GB result) | `public_search.py` (`"why is the sky blue"`) |

#### B. Pasted `neighbours.py` Output (`PASS`, `8` Big Neighbours `≥1M` Views, Including `3` Direct Blue-Sky/Purple-Sky Explainers on `Veritasium` & `minutephysics` + `2` `1M+` `TED-Ed` Light Lessons)

```text
$ python3 00_Brand/Channel-Setup/tools/neighbours.py "why is the sky blue" "why the sky isn't blue" "why isn't the sky purple" "rayleigh scattering" "light scattering" --out 02_Video-Projects/103_Tyndall-Rayleigh-Why-Is-The-Sky-Blue/11_Upload-Package/evidence_2026-11-13_neighbours.json
| # | Channel | Views | Title | Found by |
|---|---|---|---|---|
| 1 | TED-Ed ★ | 1,816,004 views | [Is light a particle or a wave? - Colm Kelleher](https://youtu.be/J1yIApZtLos) | ted-ed light scattering |
| 2 | TED-Ed ★ | 1,275,823 views | [Light waves, visible and invisible](https://youtu.be/O0PawPSdk28) | ted-ed light scattering |
| 3 | TED-Ed ★ | 509,601 views | [Are the Northern Lights dangerous? - Fabio Pacucci](https://youtu.be/8PCHd5banhE) | ted-ed light scattering |
| 4 | TED-Ed ★ | 332,526 views | [What light can teach us about the universe - Pete Edwards](https://youtu.be/HZ7hwUduMoU) | ted-ed light scattering |
| 5 | Be Smart | 26,613,295 views | [Why Is Blue So Rare In Nature?](https://youtu.be/3g246c6Bv58) | why the sky isn't blue |
| 6 | Kurzgesagt – In a Nutshell | 9,990,176 views | [What Is Light?](https://youtu.be/IXxZRZxafEQ) | light scattering ted |
| 7 | 3Blue1Brown | 1,900,703 views | [How wiggling charges give rise to light](https://youtu.be/aXRTczANuIs) | light scattering ted |
| 8 | Veritasium | 1,536,981 views | [Why the Sky ISN'T Blue](https://youtu.be/ro2MmmdARrs) | ted-ed why is the sky blue |
| 9 | minutephysics | 1,382,559 views | [Why Isn't The Sky Purple?](https://youtu.be/R5P6O0pDyMU) | why the sky isn't blue |
| 10 | minutephysics | 1,363,672 views | [Why is the Sun Yellow and the Sky Blue?](https://youtu.be/NafbGOQBlQs) | why is the sky blue |
| 11 | minutephysics | 671,083 views | [Why the Sky is Blue explained in ten seconds](https://youtu.be/doSR9Mq_taw) | ted-ed why is the sky blue |
| 12 | SciShow | 617,274 views | [World's Most Asked Questions: Why is the Sky Blue?](https://youtu.be/_Yli-yvNy-k) | why is the sky blue |

Words the top neighbours share: the sky, is light, why is
TED-Ed/TED neighbour: yes
Big neighbours (≥ 1,000,000 views): 8 (need 3)
Neighbour gate (≥ 3 education videos with 1,000,000+ views): PASS
Raw pull: 02_Video-Projects/103_Tyndall-Rayleigh-Why-Is-The-Sky-Blue/11_Upload-Package/evidence_2026-11-13_neighbours.json
```

#### C. Pasted `public_search.py` Output & Title Collision Check (`2026-11-13`)

```text
$ python3 00_Brand/Channel-Setup/tools/public_search.py "why is the sky blue" "rayleigh scattering" "why are sunsets red" "why isn't the sky violet" "Why Is the Sky Blue? (And Why It Isn't Violet)" "Why Is the Sky Blue? (The Glass Tube That Solved It)" "Why Isn't the Sky Violet? (Rayleigh's Puzzle)" "Why Are Sunsets Red? (Tyndall's 1869 Glass Tube)" --out 02_Video-Projects/103_Tyndall-Rayleigh-Why-Is-The-Sky-Blue/11_Upload-Package/evidence_2026-11-13_public_search.json
| Phrase | Autocomplete? | Top results (GB) |
|---|---|---|
| why is the sky blue | yes | Nick Cope 614,119 · NASA Space Place 937,900 · SciShow Kids 530,954 · Netflix Jr. 1,050,550 · Fermilab 97,566 |
| rayleigh scattering | yes | Science ABC 32,535 · The Science Asylum 306,702 · SciencePrimer 52,939 · LIB LAB 32,132 · Scientificprotocols 26,294 |
| why are sunsets red | yes | Astronomic 200,584 · It's AumSum Time 559,993 · Mind Trivia 337 · BBC Earth Science 62,760 · Science Workshop 9,320 |
| why isn't the sky violet | related: why isn't the sky purple; why is the sky purple | minutephysics 1,382,559 · My Pilot Projects 13 · Plain Cause 174 · Physics Lore 239 · Unconventional Wisdom 24 |
| Why Is the Sky Blue? (And Why It Isn't Violet) | related: why is the sky blue and not violet | minutephysics 1,382,559 · Why Is It 7 · thecuriousengineer 393,697 · NASA Space Place 937,917 · StarTalk 3,394,689 |
| Why Is the Sky Blue? (The Glass Tube That Solved It) | related: why is the sky blue experiment | Nick Cope 614,123 · Stickyman 1 view · BBC Earth Science 52,339 · NASA Space Place 937,917 · SciShow 617,274 |
| Why Isn't the Sky Violet? (Rayleigh's Puzzle) | no | Morsels 42 · Why Originals 1,241 · Physics Lore 239 · minutephysics 1,382,559 · Clear Science Lab 60 |
| Why Are Sunsets Red? (Tyndall's 1869 Glass Tube) | related: why are sunsets red | Mind Trivia 337 · Kaleidaxis 43 · Board of Why 5 · Kids Fun Science (Kids Fun Science) 26,690 · Education Maya No |

Raw pull: 02_Video-Projects/103_Tyndall-Rayleigh-Why-Is-The-Sky-Blue/11_Upload-Package/evidence_2026-11-13_public_search.json
```

- **Title Collision Check (`evidence_2026-11-13_public_search.json`):**
  - **Bare `"Why Is the Sky Blue?"`:** Collides with `NASA Space Place` (`ehUIlhKhzDA`, `937,900` views), `National Space Centre` (`DiF64N8C0fs`, `33,168` views), `Fermilab` (`9mnlJdABRns`, `97,566` views), and `Nick Cope` (`enKeTKon9NI`, `614,119` views) — so bare `"Why Is the Sky Blue?"` is **rejected** under `studio/RULES.md` Never list (*"a title that copies a live video"*).
  - **Title A (`Why Is the Sky Blue? (And Why It Isn't Violet)`):** **`0` exact collisions** (nearest are `MGlbtz3QjrA` *Why Is the Sky Blue? The Real Science and Why It Isn't Violet* [`7` views], `0b1fqodmZJ0` *Why is the Sky Blue and not Violet?* [`393,697` views], and `1k8zD-a5x98` *Why Is the Sky Blue? (And Why Isn't It Purple?)* [`8` views]).
  - **Title B (`Why Is the Sky Blue? (The Glass Tube That Solved It)`):** **`0` exact collisions**.
  - **Bare Short titles `"Why Isn't the Sky Violet?"` and `"Why Are Sunsets Red?"`:** Bare `"Why Isn't the Sky Violet?"` collides with `ChkF5oVeX6c` (`239` views), `XzCi6GthoJk` (`174` views), and `0eK0pDs76Hw` (`13` views); bare `"Why Are Sunsets Red?"` collides with `fxRzHYhgi4s` (`Cosmoknowledge`, `6,121` views). Therefore both candidate Short titles include a disambiguating historical tail and have **`0` exact collisions**:
    - **Short S01:** `Why Isn't the Sky Violet? (Rayleigh's Puzzle)` (`45 chars`, `0` exact collisions)
    - **Short S02:** `Why Are Sunsets Red? (Tyndall's 1869 Glass Tube)` (`48 chars`, `0` exact collisions; triggers `related: why are sunsets red`)

---

### 2.4 Overlap Check Across Projects, Ideas, Backlog & WIP (Correction 5)
Rechecked on `2026-11-13`:
- **`02_Video-Projects/` (`000`–`013`, `099`–`102`):** None covers Tyndall's 1869 scattering tube, Rayleigh scattering, or why the sky is blue.
- **`00_Brand/Channel-Setup/ideas/` (`011`–`095` & `IDEAS_*.md`):**
  - Idea `034_Foote-Tyndall-Arrhenius-Greenhouse` covers Eunice Foote (`1856`), John Tyndall (`1859` infrared absorption by $CO_2$ and water vapour in his ratio spectrophotometer), and Svante Arrhenius (`1896`) — thermal infrared absorption / greenhouse warming, a different physical phenomenon, apparatus, and decade from Tyndall's `1869` visible-light nephelometer/scattering tube and Rayleigh's `1871`/`1899` $\lambda^{-4}$ scattering law.
  - Idea `018_Herschel-Ritter-Invisible-Light` covers Herschel's `1800` infrared thermometer and Ritter's `1801` ultraviolet silver-chloride paper.
  - Idea `025_Young-Einstein-Double-Slit` covers Young's `1801` interference slits and Einstein's `1905` photoelectric effect.
  - None covers Rayleigh scattering or why the sky is blue.
- **`00_Brand/Channel-Setup/VIDEO_BACKLOG.json` & `orbit-with-ben/jobs/WIP.json`:** Not in active `hos` (`007`–`011`, `013`) and not in `next_hos` (`012`, `014`–`017`, `100`, `101` prior to this PR). Ground-level atmospheric optics / history of physics (not an Orbit With Ben space topic).

---

## 3. Two Candidate Short Angles (22–27 s, Question Titles — UNVERIFIED CONCEPTS ONLY)

> **Important:** Neither Short below is cleared for VO or production. Every historical and scientific claim — especially the violet-vs-blue solar spectrum and human cone-sensitivity explanation in S01 and Tyndall's 1869 tube details in S02 — must be verified with exact quotes in `SOURCES.md` through the `facts` lane before any Short script is locked.

| Short | Candidate Title (`0` exact collisions) | Frame-0 Visual Concept & Candidate Opening Idea (*UNVERIFIED*) | Candidate Payoff Idea (`≥70%` of runtime, *UNVERIFIED*) |
|---|---|---|---|
| **S01** | **Why Isn't the Sky Violet? (Rayleigh's Puzzle)** *(45 chars; `0` exact collisions; pairs with `"why isn't the sky purple"` autocomplete)* | **Frame 0 (`mode: "cover"`):** Full-bleed moving sky shifting from azure blue to deep violet above sunlit clouds with a prism bar (`0%` Explorer, `0%` bars); `0.0 s` hook text: `WHY NOT VIOLET?` (`#FFE000` on `VIOLET?`). Candidate opening concept: by Lord Rayleigh's scattering law, air scatters violet light even more strongly than blue. | **Payoff (`≥70%` runtime, `<1.0 s` loop tail, zero CTA):** Verify in `SOURCES.md` (e.g. Smith 2005 *Am. J. Phys.*) how the Sun's spectrum sends less violet than blue and how human red/green/blue cone cells respond to the combined scattered spectrum as pale blue. |
| **S02** | **Why Are Sunsets Red? (Tyndall's 1869 Glass Tube)** *(48 chars; `0` exact collisions; triggers `"why are sunsets red"` autocomplete)* | **Frame 0 (`mode: "cover"`):** Close moving shot of John Tyndall's 1869 glass tube glowing blue along its side while projecting a deep red disc out of its far end (`0%` Explorer, `0%` bars); `0.0 s` hook text: `SUNSET IN A TUBE` (`#FFE000` on `SUNSET`). Candidate opening concept: in 1869 John Tyndall made both a blue sky and a red sunset inside a single glass tube. | **Payoff (`≥70%` runtime, `<1.0 s` loop tail, zero CTA):** Verify in `SOURCES.md` how low-angle sunset light passes through a much longer path of air, scattering blue wavelengths out to the sides and leaving red light on the straight path to your eyes. |
