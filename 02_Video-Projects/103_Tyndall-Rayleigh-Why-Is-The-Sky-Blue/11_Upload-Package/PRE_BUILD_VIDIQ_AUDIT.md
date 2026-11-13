# Pre-build vidIQ audit — History of Science (`HOS:103` — Rule-E `GO` in `next_hos`, Claims Unverified)

> **RULE-E `GO` & UNVERIFIED CLAIMS NOTICE (`J2748` / `J2776`, 13 Nov 2026):**
> This topic (`HOS:103`) scored **`95 / 100` (`GO`)** in its Rule-E topic review (`J2776`, [`TOPIC_OPPORTUNITY_SCORE.md`](TOPIC_OPPORTUNITY_SCORE.md) & [`TOPIC_GO_NO_GO_SHEET.md`](TOPIC_GO_NO_GO_SHEET.md)) and waits in `jobs/WIP.json` `next_hos` under Rule G (`4/4` active HOS slots currently full). **No production work, spend, script lock, VO, or Studio change starts from this review.** All historical and scientific claims below — including Saussure's cyanometer dates, Tyndall's 1869 vapour-tube reagents, Rayleigh's $\lambda^{-4}$ scattering ratio, and the solar-spectrum / human-cone explanation for why the sky is not violet — remain **explicitly unverified** and **not cleared for narration or Short opens** until backed by exact quotes in `SOURCES.md` and verified through the `facts` lane when `HOS:103` enters an active HOS WIP slot.

---

## Episode

| Field | Value |
|-------|-------|
| ID / slug | `103_Tyndall-Rayleigh-Why-Is-The-Sky-Blue` (`HOS:103`) |
| Working title (A) | `Why Is the Sky Blue? (And Why It Isn't Violet)` (`46 chars`, `0` exact collisions) |
| Title B (T&C) | `Why Is the Sky Blue? (The Glass Tube That Solved It)` (`52 chars`, `0` exact collisions) |
| Title C (Story) | `The 1869 Glass Tube That Put Blue Sky in a Bottle` (`49 chars`, `0` exact collisions) |
| Date pulled | `2026-11-13` (`J2748` correction on Mac mini) |
| Credits used (approx) | `£0.00` (signed-out YouTube GB public search + `neighbours.py`) |
| Brand guardrails | Wonder over fearbait · no conspiracy · HOS lane (a familiar thing — the blue sky and red sunset overhead — and the 1869 glass tube and 1871 scattering law that explained it) |

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**) |
| Primary keyword overall | `"why is the sky blue"` (`autocomplete = yes`), `"rayleigh scattering"` (`autocomplete = yes`), `"why are sunsets red"` (`autocomplete = yes`) |
| Hook promise | Candidate hook (unverified): In 1869 John Tyndall shone a laboratory lamp through a glass tube of fine vapour to make an artificial blue sky and a red sunset on a Royal Institution bench — setting up Lord Rayleigh's scattering law and the puzzle of why our sky looks blue rather than violet |
| Retention design | Proof-first `0:05–0:15` on Tyndall's glowing 1869 glass tube + 4 chronological acts (`1789 -> 1869 -> 1871/1899 -> The Violet Puzzle`) that earn the next minute |
| Packaging | 3-way Thumbnail Test & Compare concept (`SKY IN GLASS` Tyndall glowing tube vs Rule 14 bright `WHY NOT VIOLET?` prism sky split vs Saussure's Alpine cyanometer wheel; readable at `168×94`) |

---

## 2. Keyword research (Signed-Out YouTube Autocomplete & Competition Check · Rule 26, Retrieved `2026-11-13`)

Saved in `11_Upload-Package/evidence_2026-11-13_public_search.json`:

| Keyword | Autocomplete (`suggest()`) | GB Top-5 Competition (`public_search.py`, `2026-11-13`) | Role (title / desc / chapter / Shorts) | Keep? |
|---------|---------------------------|----------------------------------------------------------|----------------------------------------|-------|
| `why is the sky blue` | **yes** (`why is the sky blue`, `why is the sky blue and sunsets red`, `why is the sky blue but space is black`) | `Nick Cope` `614,119` · `NASA Space Place` `937,900` · `SciShow Kids` `530,954` · `Netflix Jr.` `1,050,550` · `Fermilab` `97,566` (`StarTalk` `3,394,689`) | Primary search phrase (Title A & Title B lead + Desc line 1 + tags) | **Keep** |
| `Why Is the Sky Blue? (And Why It Isn't Violet)` | **related:** `why is the sky blue and not violet` | `minutephysics` `1,382,559` · `Why Is It` `7` · `thecuriousengineer` `393,697` · `NASA Space Place` `937,917` · `StarTalk` `3,394,689` | Full candidate Title A (`0` exact collisions) | **Keep** |
| `rayleigh scattering` | **yes** (`rayleigh scattering`, `rayleigh scattering experiment`, `rayleigh scattering animation`) | `Science ABC` `32,535` · `The Science Asylum` `306,702` · `SciencePrimer` `52,939` · `LIB LAB` `32,132` · `Scientificprotocols` `26,294` | Secondary mechanism phrase (Desc + Ch 3 + tags) | **Keep** |
| `why are sunsets red` | **yes** (`why are sunsets red`) | `Astronomic` `200,584` · `It's AumSum Time` `559,993` · `Mind Trivia` `337` · `BBC Earth Science` `62,760` · `Science Workshop` `9,320` | Short `S02` lead (`Why Are Sunsets Red? (Tyndall's 1869 Glass Tube)`, `0` exact collisions) | **Keep** |
| `why isn't the sky violet` | **related:** `why isn't the sky purple`, `why is the sky purple` | `minutephysics` `1,382,559` · `My Pilot Projects` `13` · `Plain Cause` `174` · `Physics Lore` `239` · `Unconventional Wisdom` `24` | Short `S01` lead (`Why Isn't the Sky Violet? (Rayleigh's Puzzle)`, `0` exact collisions) | **Keep** |

- **Rule 26(a) Exact Phrase & Two Ranking Videos (`2026-11-13`):**
  - **Phrase:** `"why is the sky blue"`
  - **Ranking Video 1:** `UvmWxm3nR6E` — *Neil deGrasse Tyson Explains Why The Sky Is Blue* (`StarTalk`, **`3,394,689` views**, retrieved `2026-11-13`)
  - **Ranking Video 2:** `Ldm_9LsKblU` — *Why is the Sky Blue \| Ask the Storybots \| Netflix Jr* (`Netflix Jr.`, **`1,050,550` views**, retrieved `2026-11-13`; plus `ehUIlhKhzDA` `NASA Space Place` *Why Is the Sky Blue?* **`937,900` views** and `ro2MmmdARrs` `Veritasium` *Why the Sky ISN'T Blue* **`1,536,981` views**)
- **Decision:** Candidate primary title = `Why Is the Sky Blue? (And Why It Isn't Violet)` (Title A, `46 chars`, `0` exact collisions) / `Why Is the Sky Blue? (The Glass Tube That Solved It)` (Title B, `52 chars`, `0` exact collisions)
- **Candidate description first 100 chars (unverified until `SOURCES.md` check):** `Why is the sky blue—and why isn't it violet? In 1869 John Tyndall shone a lamp through a glass tube...`

---

## 2b. Neighbour pass (blocking · `STUDIO_PLAYBOOK.md` §2 Step 4, Retrieved `2026-11-13`)

Saved in `11_Upload-Package/evidence_2026-11-13_neighbours.json` (`8` big neighbours `≥1M` views, `PASS`):

| # | Views (`2026-11-13`) | Channel (internal) | id & URL | Title | Subject words we reuse |
|---:|------:|--------------------|----------|-------|------------------------|
| 1 | `26,613,295` | Be Smart (`neighbours.py`) | [`3g246c6Bv58`](https://youtu.be/3g246c6Bv58) | *Why Is Blue So Rare In Nature?* | `blue`, `light scattering`, `wavelength` |
| 2 | `9,990,176` | Kurzgesagt (`neighbours.py`) | [`IXxZRZxafEQ`](https://youtu.be/IXxZRZxafEQ) | *What Is Light?* | `light`, `wavelength`, `visible spectrum`, `sunlight` |
| 3 | `3,394,689` | StarTalk (`public_search.py`) | [`UvmWxm3nR6E`](https://youtu.be/UvmWxm3nR6E) | *Neil deGrasse Tyson Explains Why The Sky Is Blue* | `why is the sky blue`, `scatter`, `atmosphere`, `sunset` |
| 4 | `1,900,703` | 3Blue1Brown (`neighbours.py`) | [`aXRTczANuIs`](https://youtu.be/aXRTczANuIs) | *How wiggling charges give rise to light* | `light`, `charges`, `scattering`, `frequency` |
| 5 | `1,816,004` | TED-Ed ★ (`neighbours.py`) | [`J1yIApZtLos`](https://youtu.be/J1yIApZtLos) | *Is light a particle or a wave? - Colm Kelleher* | `light`, `wave`, `wavelength` |
| 6 | `1,536,981` | Veritasium (`neighbours.py`) | [`ro2MmmdARrs`](https://youtu.be/ro2MmmdARrs) | *Why the Sky ISN'T Blue* | `why is the sky blue`, `rayleigh scattering`, `spectrum` |
| 7 | `1,382,559` | minutephysics (`neighbours.py`) | [`R5P6O0pDyMU`](https://youtu.be/R5P6O0pDyMU) | *Why Isn't The Sky Purple?* | `why isn't the sky violet`, `purple`, `sunlight`, `eyes` |
| 8 | `1,363,672` | minutephysics (`neighbours.py`) | [`NafbGOQBlQs`](https://youtu.be/NafbGOQBlQs) | *Why is the Sun Yellow and the Sky Blue?* | `why is the sky blue`, `sun`, `scattering` |
| 9 | `1,275,823` | TED-Ed ★ (`neighbours.py`) | [`O0PawPSdk28`](https://youtu.be/O0PawPSdk28) | *Light waves, visible and invisible* | `light waves`, `ultraviolet`, `violet`, `atmosphere` |

**Proposed subject-only tags (8 tags, zero channel names):**  
`why is the sky blue, why isn't the sky violet, rayleigh scattering, why are sunsets red, john tyndall blue sky experiment, lord rayleigh scattering, light scattering, cyanometer saussure`

---

## 3. Title ABC (score before VO)

| | Title | Chars | Collisions (`2026-11-13`) | Role & Notes | Keep? |
|---|-------|------:|-----------:|--------------|-------|
| A | `Why Is the Sky Blue? (And Why It Isn't Violet)` | 46 | 0 | **Main (`Rule 26` + `Rule 15`):** Starts with exact autocomplete phrase `"Why Is the Sky Blue?"` + bracketed twist (`≤50` chars, `0` collisions) | **Keep (Primary Proposal)** |
| B | `Why Is the Sky Blue? (The Glass Tube That Solved It)` | 52 | 0 | **Test & Compare (`Rule 26` + `Rule 23`):** Exact search phrase first + 1869 bench apparatus tail (`0` collisions) | **Keep (T&C Arm 2)** |
| C | `The 1869 Glass Tube That Put Blue Sky in a Bottle` | 49 | 0 | **Story/Apparatus Variant:** Concrete Royal Institution instrument hook (`0` collisions) | **Keep (Alt)** |
| Reject | `Why Is the Sky Blue?` | 20 | 4+ | Collides verbatim with live videos on `NASA Space Place` (`ehUIlhKhzDA`), `Nick Cope` (`enKeTKon9NI`), `Fermilab` (`9mnlJdABRns`), and `National Space Centre` (`DiF64N8C0fs`) | **Reject (Collision)** |

---

## 3b. Script reviewer (blocking before VO — not run; proposal only)

- [ ] `SOURCES.md` exact quotes + `facts` lane verification completed (required before script lock)
- [ ] Score ≥ **90 / 100** (`npm run review:script`)

---

## 4. Outlier / competitive patterns (on-brand only)

| Outlier / pattern | Views (`2026-11-13`) | Steal (structure) | Do **not** copy |
|-------------------|------:|-------------------|-----------------|
| `R5P6O0pDyMU` (*Why Isn't The Sky Purple?*, minutephysics) & `ro2MmmdARrs` (*Why the Sky ISN'T Blue*, Veritasium) | `1.38M` & `1.54M` | The counter-intuitive turn: Rayleigh's $\lambda^{-4}$ law scatters violet more than blue, so explaining the sky's colour requires both the Sun's spectrum and human vision | Stick-figure whiteboard or street-interview format (we tell the `1789 -> 1869 -> 1871/1899` discovery story in 3D cartoon rooms) |
| `UvmWxm3nR6E` (*Neil deGrasse Tyson Explains Why The Sky Is Blue*, StarTalk) | `3.39M` | Connecting overhead blue sky and horizon red sunset as two ends of the same beam | Studio podcast conversation without Tyndall's 1869 glass tube or Saussure's cyanometer |

---

## 5. Incorporate into the build (once approved & sourced)

| Data finding | Change to script / chapters / visuals / packaging |
|--------------|-----------------------------------------------------|
| Primary search phrase (`why is the sky blue`) | Starts Title A and Title B verbatim, spoken in the first `8 s`, and in line 1 of the description (Rule 26) |
| Bare title collisions on `"Why Is the Sky Blue?"`, `"Why Isn't the Sky Violet?"`, and `"Why Are Sunsets Red?"` | Keep disambiguating tails on all long and Short titles (`Why Is the Sky Blue? (And Why It Isn't Violet)`, `Why Isn't the Sky Violet? (Rayleigh's Puzzle)`, `Why Are Sunsets Red? (Tyndall's 1869 Glass Tube)`) so exact collisions = `0` |
| Unverified historical & optics claims | Source Saussure (`1789`), Tyndall (`1869`), Rayleigh (`1871`, `1899`), and the violet-vs-blue solar/cone mechanism (`Smith 2005 Am. J. Phys.`) in `SOURCES.md` before writing any script |

**Candidate chapter list (unverified — requires `SOURCES.md` verification before scripting):**
1. **Measuring the Blue (c. 1789, *UNVERIFIED*):** Horace-Bénédict de Saussure's numbered cyanometer wheel in the Alps.
2. **Sky in a Glass Tube (1869, *UNVERIFIED*):** John Tyndall's Royal Institution vapour tube glows blue from the side and casts a red sunset from its end.
3. **The Fourth-Power Law (1871 & 1899, *UNVERIFIED*):** Lord Rayleigh derives $\lambda^{-4}$ scattering and shows air molecules themselves scatter sunlight.
4. **Why Blue Instead of Violet? (*UNVERIFIED*):** Combining Rayleigh scattering with the Sun's emission spectrum and human `S`/`M`/`L` cone sensitivity.

---

## 6. Retention plan (whole-video watch)

| Minute zone | Job | Picture / VO note |
|-------------|-----|-------------------|
| 0–0:05 | Curiosity spike | Moving 3D glass tube on Tyndall's darkened Royal Institution bench lighting up azure blue |
| 0:05–0:15 | Physical proof | White lamp beam entering the glass tube: blue glow out the sides, red sunset disc at the far end |
| ~0:25–0:40 | Early `DATA+SCALE` | First sourced relative scattering comparison across red vs blue/violet wavelengths (once verified in `SOURCES.md`) |
| Chapter starts | Re-hook + chapter card | Case-file desk transition (`1789 -> 1869 -> 1871 -> 1899`) |
| Mid | Teach while story continues | Inked wavelength scattering diagram on period paper |
| Final chapter | Payoff + hand-off | Sourced solar-spectrum + human-eye resolution of the violet puzzle + hand-off to next film |

---

## 7. Sign-off (block production until checked)

- [x] Keywords pulled and primary candidate identified (`2026-11-13`)
- [x] Neighbour gate (`≥3` education videos `≥1M` views) verified (`2026-11-13`)
- [x] Rule-E Topic Review (`GO` — `95 / 100` in [`TOPIC_OPPORTUNITY_SCORE.md`](TOPIC_OPPORTUNITY_SCORE.md) & [`TOPIC_GO_NO_GO_SHEET.md`](TOPIC_GO_NO_GO_SHEET.md); `J2776`, `2026-11-13`, recorded for Chief review; waits in `next_hos` under Rule G)
- [ ] `SOURCES.md` primary quotes + `facts` lane verification (`gemini-agy` — required when `HOS:103` enters an active HOS WIP slot before any script lock)
- [ ] Script reviewer ≥ 90 (`npm run review:script`)

**Signed off by:** `macbook` (`J2776` Rule-E Topic Review: `GO` `95/100` in `next_hos` for Chief review; historical/scientific claims remain **unverified** until `SOURCES.md` + `facts` lane)  
**Date:** `2026-11-13`
