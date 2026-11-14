# Pre-build vidIQ audit — History of Science (`HOS:107` · Proposal Only)

> **UNVERIFIED CLAIMS GUARD (`J2837`, 14 Nov 2026):** All historical dates, names, quotes, and numbers below are **UNVERIFIED** working notes from `J2835` and are **NOT CLEARED FOR SCRIPT LOCK, VO, OR PICTURE SPEND** until `HOS:107` enters an active HOS WIP slot (`jobs/WIP.json`) and every claim is verified from primary sources in `SOURCES.md` by the `facts` lane (`gemini-agy`).

---

## Episode

| Field | Value |
|-------|-------|
| ID / slug | `HOS:107` · `02_Video-Projects/107_Tswett-Willstatter-Autumn-Leaves-Chlorophyll` |
| Working title (`0` collisions) | `Why Do Leaves Change Colour? (A Chalk Tube Showed Why)` (`54` chars; `≤50`-char Rule 15 variant: `Why Do Leaves Change Colour? (The 1903 Chalk Tube)`, `50` chars) |
| Date pulled | `2026-11-14` (`neighbours.py` in `J2835` · `public_search.py` in `J2836` & `J2837`) |
| Credits used (approx) | `£0.00` / `0` credits (public signed-out YouTube GB search; vidIQ waived per standing rule) |
| Brand guardrails | Wonder over fearbait · no conspiracy · adult historical science tone (never `Made for Kids`) · HOS lane (a familiar seasonal change on the ground, and the 1903 glass chalk tube in Warsaw that revealed the yellow was there all summer) |

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Opportunity Score (`TOPIC_OPPORTUNITY_SCORE.md`) | **`9.00 / 10` (`90 / 100`, `GO`, placed behind `HOS:106` in `next_hos`)** |
| Primary keyword (`Rule 26`) | `"why do leaves change colour"` / `"why do leaves change color in the fall"` (`autocomplete = yes`, top education results `SciShow Kids` `1.85M` & `MinuteEarth` `1.56M`) + `"what is chromatography"` (`autocomplete = yes`, `Cognito` `1.53M` & `Khan Academy` `1.33M`) |
| Hook promise | Every green summer leaf is already full of bright yellow and orange pigments — and in 1903 a Russian-Italian botanist in Warsaw proved it by pouring green leaf juice through a glass tube of powdered chalk, inventing chromatography |
| Retention design | Proof-first `0:05–0:15` on Tswett's 1903 glass chalk column separating green leaf juice into emerald, yellow-green, and golden-orange rings + 5 chronological acts (`1817 Pelletier & Caventou -> 1903 Tswett's Warsaw chalk tube -> 1906-1915 Willstätter's magnesium & Nobel rivalry -> Autumn leaf unmasking vs red anthocyanins -> 1931 Kuhn/Lederer vindication`) |
| Packaging | 3-way Thumbnail Test & Compare concept (`ALWAYS YELLOW` split green/gold leaf beside Tswett's banded chalk column vs `CHALK TUBE` emerald-and-gold rings in glass column vs `3 COLOURS` leaf pigment separation; readable at `168×94`) |

---

## 2. Keyword research (Signed-Out YouTube Autocomplete & Competition Check · Rule 26, Retrieved `2026-11-14`)

Saved in `11_Upload-Package/evidence_2026-11-14_public_search.json`:

| Keyword / Candidate Title | Autocomplete (`suggest()`) | GB Top-5 Competition (`public_search.py`, `2026-11-14`) | Role (title / desc / chapter / Shorts) | Keep? |
|---------|---------------------------|----------------------------------------------------------|----------------------------------------|-------|
| `why do leaves change colour` | **yes** (`10` suggestions) | `Super Simple Songs` `1,991,366` · `SciShow Kids` `1,850,236` · `MinuteEarth` `1,558,957` · `Peekaboo Kidz` `346,918` · `SciShow` `269,611` | Primary UK search phrase (Title A/B/C + Desc line 1 + tags) | **Keep** |
| `why do leaves change color in the fall` | **yes** (`6` suggestions) | `SciShow Kids` `1,850,236` · `Peekaboo Kidz` `346,918` · `Super Simple Songs` `1,991,366` · `MinuteEarth` `1,558,957` · `Free School` `388,111` | Primary US search phrase (Desc + tags) | **Keep** |
| `what is chromatography` | **yes** (`10` suggestions) | `Chemistry Student` `131,446` · `Cognito` `1,532,858` · `Chemistorian` `319,708` · `Freesciencelessons` `242,321` · `It's AumSum Time` `2,116,418` | Year-round GCSE/AP/MCAT curriculum phrase (Short `S02` + Desc + chapters + tags) | **Keep** |
| `chlorophyll` | **yes** (`10` suggestions) | `WonderKids Academy` `2,260` · `thedailyECO` `198,943` · `Dr. Eric Berg DC` `567,457` · `Guess Who's Vegan` `58,203` · `I Never Knew Tv` `44,500` | Core pigment term (Desc + chapters + tags) | **Keep** |
| `Why Do Leaves Turn Yellow in Autumn?` | related (`3` suggestions) | `MinuteEarth` `1,558,962` · `SciShow Kids` `1,850,236` · `Peekaboo Kidz` `346,918` · `Sheffield Made Plants` `106,876` · `Curiously Kids` `1,808` | Short `S01` question title (`0` collisions) | **Keep** |
| `What Is Chromatography? (Tswett's 1903 Leaf-Chalk Tube)` | related | `Cognito` `1,532,866` · `StudyIB` `23` · `NC State S.M.A.R.T. Lab` `324,857` · `Chemistorian` `319,712` · `STEM Spark Zone` `359` | Disambiguated Short `S02` question title (`0` collisions; replaces verbatim collision `rTFlBVcwewI`) | **Keep** |

- **Rule 26(a) Exact Phrase & Two Ranking Videos (`2026-11-14`):**
  - **Phrase 1:** `"why do leaves change colour"` / `"why do leaves change color in the fall"` → **SciShow Kids** [`Xk4-6II8l5Q`](https://youtu.be/Xk4-6II8l5Q) (*Why Do Leaves Change Colors in the Fall? | Biology for Kids*, **`1,850,236` views**) and **MinuteEarth** [`JWva5AaDkXw`](https://youtu.be/JWva5AaDkXw) (*The Real Reason Leaves Change Color In the Fall*, **`1,558,957` views**)
  - **Phrase 2:** `"what is chromatography"` → **Cognito** [`TdJ57SQ6GAQ`](https://youtu.be/TdJ57SQ6GAQ) (*GCSE Chemistry - Paper Chromatography*, **`1,532,858` views**) and **Khan Academy** [`SnbXQTTHGs4`](https://youtu.be/SnbXQTTHGs4) (*Basics of chromatography | Chemical processes | MCAT | Khan Academy*, **`1,328,589` views**)
- **Decision:** Primary title lead = `Why Do Leaves Change Colour? (A Chalk Tube Showed Why)` (`54` chars, `0` collisions)
- **Description first 100 chars must include:** `Why do leaves change colour in autumn — and how did Mikhail Tswett's 1903 chalk tube prove the yellow was always there?`

---

## 3. Title ABC (score before VO)

| | Title | Chars | Collision Check (`public_search.py`, `2026-11-14`) | Keep? |
|---|-------|------:|----------------------------------------------------|-------|
| **A (Primary, Rule 26)** | `Why Do Leaves Change Colour? (A Chalk Tube Showed Why)` | `54` | **`0` exact collisions** | **Keep (Side A)** |
| **B (Test & Compare, Rule 26 + Rule 23)** | `Why Do Leaves Change Colour in Autumn? (Tswett's 1903 Chalk Tube)` | `65` | **`0` exact collisions** | **Keep (Side B)** |
| **C (`≤50`-char Rule 15 Variant)** | `Why Do Leaves Change Colour? (The 1903 Chalk Tube)` | `50` | **`0` exact collisions** | **Keep (Alt)** |
| **Disambiguated from (`J2835` drafts)** | *Why Do Leaves Change Colour in Autumn? (The Yellow Was Always There)* / *The Hidden Colours Inside Every Green Leaf* | `68` / `42` | Near-collisions with `tlhm2c7bhic` (`10`v), `PfgRu-0WTts` (`2`v), `hthQp2wvPJY` (`4`v), and `DrcdawG3cAs` (`70,498`v) | **Replaced by A, B & C** |

---

## 4. Outlier / competitive patterns (on-brand only)

| Outlier / pattern | Views | Steal (structure) | Do **not** copy |
|-------------------|------:|-------------------|-----------------|
| `MinuteEarth` *The Real Reason Leaves Change Color In the Fall* (`JWva5AaDkXw`) | `1,558,957` | Contrast between yellow carotenoids (always present) and red anthocyanins (newly synthesised in autumn) | 2-minute stick-figure format with zero history of science |
| `SciShow Kids` *Why Do Leaves Change Colors in the Fall?* (`Xk4-6II8l5Q`) | `1,850,236` | Clear visual reveal of green chlorophyll fading to unmask yellow underneath | Young children's tone (`Made for Kids` audience risk) |
| `Cognito` *GCSE Chemistry - Paper Chromatography* (`TdJ57SQ6GAQ`) | `1,532,858` | Clear step-by-step visual of mobile phase carrying pigments at different speeds up/down stationary phase | Exam-board whiteboard lecture without Tswett's 1903 story |

**Patterns we will use in this script (once active WIP slot opens and `SOURCES.md` passes):**

- [x] Assumption-flip / open-loop title (`Why Do Leaves Change Colour? (A Chalk Tube Showed Why)`)
- [x] Numbered chronological layers (`1817 Paris -> 1903 Warsaw -> 1906-1915 Zurich/Berlin -> 1931 Heidelberg`)
- [x] Body-scale / everyday anchor (a single green summer leaf hiding four distinct colour rings inside a tube of chalk)
- [x] Slow reveal / midpoint twist (Nobel laureate Richard Willstätter's school dismissed Tswett's chalk column, delaying chromatography for 25 years; plus red leaves are *not* unmasked — they are manufactured new as the leaf dies)

---

## 5. Incorporate into the build (required before script lock)

**Chapter list after audit** (5 acts, each with a teach-point — UNVERIFIED working outline until `SOURCES.md` pass):

1. **Part 01 — The Green Mask (Paris, 1817 & Warsaw, 1903):** Cold open on Mikhail Tswett pouring green leaf extract into a glass tube packed with powdered chalk (`0:05–0:15`), and how Pelletier & Caventou named *chlorophylle* in 1817 thinking green was a single substance.
2. **Part 02 — Colour Writing in a Tube of Chalk (Warsaw, 1903–1906):** How Tswett discovered that washing colourless solvent down the chalk column split "pure" green leaf extract into distinct emerald, yellow-green, and golden-yellow bands (`chlorophyll a`, `chlorophyll b`, `xanthophylls`, `carotenes`), proving autumn's yellows were inside the summer leaf all along.
3. **Part 03 — The Nobel Chemist Who Missed the Tube (Zurich & Berlin, 1906–1919):** Midpoint twist — Richard Willstätter wins the 1915 Nobel Prize for proving magnesium sits at the heart of chlorophyll, yet his laboratory distrusts Tswett's chalk column, and Tswett dies in 1919 before seeing his method adopted.
4. **Part 04 — Why Yellow Was Always There, and Why Red Is Made New:** How trees dismantle chlorophyll in autumn to salvage nitrogen and magnesium, unmasking summer's yellow carotenoids while manufacturing fresh red anthocyanins in the fading leaf.
5. **Part 05 — The Tube in Every Lab on Earth (1931–Present):** Kuhn, Winterstein, and Lederer revive Tswett's column in 1931, turning "colour writing" into modern chromatography — handing off to the next film.

---

## 6. Retention plan (whole-video watch)

| Minute zone | Job | Picture / VO note |
|-------------|-----|-------------------|
| `0–0:05` | Answer image / proof | Close-up of Tswett's glass tube packed with white chalk as dark green leaf extract separates into bright emerald and golden-yellow rings |
| `0:05–0:15` | Title question & apparatus | Tswett's hands pouring solvent into the Warsaw chalk column; title question by `0:08`, promise by `0:15` |
| `0:15–0:40` | Stakes + Early `DATA+SCALE` | Animated ink pigment band chart (`1` green drop → `2` chlorophylls + `4+` yellow/orange carotenoids) before `0:40` |
| Chapter starts | Case-file desk card + cold open | Period quote or question; each chapter ends on the question the next chapter answers |
| Mid (`~60%`) | Midpoint twist | "Case closed — every chemist adopted Tswett's tube? Wrong." Willstätter's circle rejected it for 25 years, and red autumn leaves work completely differently from yellow ones |
| Final chapter | Payoff + hand-off | 1931 revival of chromatography across modern science; hand-off to next film (no goodbye, no subscribe ask) |

---

## 7. Sign-off (block production until checked)

- [x] Keywords pulled (`public_search.py` & `neighbours.py`, `2026-11-14`) and `0`-collision primary title locked (`Why Do Leaves Change Colour? (A Chalk Tube Showed Why)`)
- [x] Rule-E topic review `GO` (`90 / 100`, `J2837`, placed behind `HOS:106` in `next_hos`)
- [ ] Active HOS WIP slot open (`jobs/WIP.json`)
- [ ] Primary sources & exact quotes verified in `SOURCES.md` (`facts` lane)
- [ ] Script reviewer ≥ 90 & `gate:episode` PASS

**Rule-E Reviewer:** `macbook` (`gemini-argon`, `J2837`)  
**Date:** `2026-11-14`
