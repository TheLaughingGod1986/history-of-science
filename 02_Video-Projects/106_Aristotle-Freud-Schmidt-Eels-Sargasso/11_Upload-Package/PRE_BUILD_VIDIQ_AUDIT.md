# Pre-build vidIQ audit — History of Science (`HOS:106` · Proposal Only)

> **UNVERIFIED CLAIMS GUARD (`J2836`, 14 Nov 2026):** All historical dates, names, quotes, and numbers below are **UNVERIFIED** working notes from `J2835` and are **NOT CLEARED FOR SCRIPT LOCK, VO, OR PICTURE SPEND** until `HOS:106` enters an active HOS WIP slot (`jobs/WIP.json`) and every claim is verified from primary sources in `SOURCES.md` by the `facts` lane (`gemini-agy`).

---

## Episode

| Field | Value |
|-------|-------|
| ID / slug | `HOS:106` · `02_Video-Projects/106_Aristotle-Freud-Schmidt-Eels-Sargasso` |
| Working title (`0` collisions) | `Where Do Eels Come From? (The Sargasso Sea Hunt)` (`48` chars) |
| Date pulled | `2026-11-14` (`neighbours.py` in `J2835` · `public_search.py` in `J2836`) |
| Credits used (approx) | `£0.00` / `0` credits (public signed-out YouTube GB search; vidIQ waived per standing rule) |
| Brand guardrails | Wonder over fearbait · no conspiracy · no gore (clean anatomical ink sketches / specimen tray per `005` guardrail) · HOS lane (a familiar creature, and the 2,000-year hunt for where it is born) |

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Opportunity Score (`TOPIC_OPPORTUNITY_SCORE.md`) | **`9.40 / 10` (`94 / 100`, `GO`)** |
| Primary keyword (`Rule 26`) | `"where do eels come from"` (`autocomplete = yes`, top result `Bizarre Beasts` `1.59M` views & `TED-Ed` `1.16M` views) |
| Hook promise | For 2,000 years nobody could find an eel with eggs — not Aristotle, and not a 19-year-old Sigmund Freud cutting open 400 eels in Trieste — until Johannes Schmidt towed nets across the Atlantic for nearly 20 years, following ever-smaller transparent larvae to the Sargasso Sea |
| Retention design | Proof-first `0:05–0:15` on Freud's 1876 Trieste dissection tray and microscope + 5 chronological acts (`Aristotle -> Freud 1876 -> Grassi 1896 -> Schmidt 1904-1922 -> 2022 satellite tags`) |
| Packaging | 3-way Thumbnail Test & Compare concept (`400 EELS` Freud at microscope vs `ZERO EGGS` transparent willow-leaf larva vs Rule 14 bright Atlantic Sargasso map `6,000 KM`; readable at `168×94`) |

---

## 2. Keyword research (Signed-Out YouTube Autocomplete & Competition Check · Rule 26, Retrieved `2026-11-14`)

Saved in `11_Upload-Package/evidence_2026-11-14_public_search.json`:

| Keyword / Candidate Title | Autocomplete (`suggest()`) | GB Top-5 Competition (`public_search.py`, `2026-11-14`) | Role (title / desc / chapter / Shorts) | Keep? |
|---------|---------------------------|----------------------------------------------------------|----------------------------------------|-------|
| `where do eels come from` | **yes** (`5` suggestions) | `Bizarre Beasts` `1,594,707` · `Atomic Frontier` `365,534` · `TED-Ed` `1,157,605` · `Auralis` `1,629,143` · `MinuteEarth` `569,775` | Primary search phrase (Title A + Desc line 1 + tags) | **Keep** |
| `how do eels reproduce` | **yes** (`7` suggestions) | `TED-Ed` `2,751,342` · `Bizarre Beasts` `1,594,707` · `TED-Ed Hindi` `5,088` · `OctoLab` `1,366` · `Thoughty2` `3,317,475` | Secondary search phrase (Title B + Desc + tags) | **Keep** |
| `eel migration` | **yes** (`9` suggestions) | `TED-Ed` `1,157,608` · `Auralis` `1,629,141` · `Bizarre Beasts` `1,594,707` · `Discovery UK` `114,189` · `ZSL` `93,645` | Umbrella term (Desc + chapters + tags) | **Keep** |
| `sargasso sea eels` | **yes** (`1` suggestion) | `acapellascience` `175,206` · `Discovery UK` `114,189` · `Auralis` `1,629,143` · `Bizarre Beasts` `1,594,707` | Payoff location term (Title A/B tail + Act 4 + tags) | **Keep** |
| `Why Did Sigmund Freud Dissect 400 Eels?` | related (`what did sigmund freud do`) | `calvintheninja` `47,374` · `VILEMasterShake` `13,938` · `Animal Oddballs` `80` · `showselectordog` `3,451,018` · `Hannah Fry` `62,190` | Short `S01` question title (`0` collisions) | **Keep** |
| `Has Anyone Ever Seen an Eel Lay Eggs?` | **no** | `Bizarre Beasts` `1,594,707` · `Never Filmed` `57` · `Pokato_1` `9` · `TED-Ed` `2,751,342` · `Nescium` `382` | Short `S02` question title (`0` collisions) | **Keep** |

- **Rule 26(a) Exact Phrase & Two Ranking Videos (`2026-11-14`):**
  - **Phrase 1:** `"where do eels come from"` → **Bizarre Beasts** [`acEIGorImGs`](https://youtu.be/acEIGorImGs) (*We Finally Know Where Eels Come From*, **`1,594,707` views**) and **TED-Ed** [`BR1enXROmgA`](https://youtu.be/BR1enXROmgA) (*Eli the eel: A mysterious migration - James Prosek*, **`1,157,610` views**)
  - **Phrase 2:** `"how do eels reproduce"` → **TED-Ed** [`RFi6ISTjkR4`](https://youtu.be/RFi6ISTjkR4) (*No one can figure out how eels have sex - Lucy Cooke*, **`2,751,342` views**) and **Thoughty2** [`k61Bk63EvTM`](https://youtu.be/k61Bk63EvTM) (*Why Nobody Knows How Eels Reproduce*, **`3,317,475` views**)
- **Decision:** Primary title lead = `Where Do Eels Come From? (The Sargasso Sea Hunt)` (`48` chars, `0` collisions)
- **Description first 100 chars must include:** `Where do eels come from, and how do eels reproduce when nobody has ever seen a wild eel lay eggs?`

---

## 3. Title ABC (score before VO)

| | Title | Chars | Collision Check (`public_search.py`, `2026-11-14`) | Keep? |
|---|-------|------:|----------------------------------------------------|-------|
| **A (Primary, Rule 15 & Rule 26)** | `Where Do Eels Come From? (The Sargasso Sea Hunt)` | `48` | **`0` exact collisions** | **Keep (Side A)** |
| **B (Test & Compare, Rule 26 + Rule 23)** | `How Do Eels Reproduce? (The 1922 Sargasso Sea Hunt)` | `51` | **`0` exact collisions** | **Keep (Side B)** |
| **C (Story Variant)** | `The Fish That Freud Dissected 400 Times` | `39` | **`0` exact collisions** | **Keep (Alt)** |
| **Disambiguated from (`J2835` drafts)** | *Where Do Eels Come From? (The 2,000-Year Mystery)* / *How Do Eels Reproduce? (Nobody Has Ever Seen It)* | `49` / `48` | Punctuation collisions with `mgRlVeTSSMA` (`8`v) and `_BWQLJJ3GcM` (`2`v) | **Replaced by A & B** |

---

## 4. Outlier / competitive patterns (on-brand only)

| Outlier / pattern | Views | Steal (structure) | Do **not** copy |
|-------------------|------:|-------------------|-----------------|
| `TED-Ed` *No one can figure out how eels have sex* (`RFi6ISTjkR4`) | `2,751,342` | Chronological progression from Aristotle → Freud → Schmidt's Sargasso larvae | Do not copy TED-Ed's title wording ("have sex") or flat 2D look |
| `Thoughty2` *Why Nobody Knows How Eels Reproduce* (`k61Bk63EvTM`) | `3,317,475` | Highlighting the 19-year-old Sigmund Freud in Trieste as an early character hook | Talking-head studio monologue and 16-minute padding |
| `Bizarre Beasts` *We Finally Know Where Eels Come From* (`acEIGorImGs`) | `1,594,707` | Connecting the 5 metamorphic stages (leptocephalus → glass eel → elver → yellow eel → silver eel) to the 2022 satellite tags | Stock-photo slideshow format |

**Patterns we will use in this script (once active WIP slot opens and `SOURCES.md` passes):**

- [x] Assumption-flip / open-loop title (`Where Do Eels Come From? (The Sargasso Sea Hunt)`)
- [x] Numbered chronological layers (`4th c. BC -> 1876 Trieste -> 1896 Sicily -> 1904-1922 Atlantic -> 2022 Sargasso`)
- [x] Body-scale anchor (`<10 mm` willow-leaf larva crossing thousands of kilometres of open ocean)
- [x] Slow reveal / midpoint twist (the transparent leaf-fish *Leptocephalus* wasn't a separate species — it was the baby eel all along)

---

## 5. Incorporate into the build (required before script lock)

**Chapter list after audit** (5 acts, each with a teach-point — UNVERIFIED working outline until `SOURCES.md` pass):

1. **Part 01 — The Fish With No Eggs (Trieste, 1876 & Ancient Greece):** Cold open on 19-year-old Sigmund Freud in Trieste dissecting hundreds of eels looking for male organs, and why Aristotle concluded eels grew from mud.
2. **Part 02 — The Leaf in the Tank (Messina / Catania, 1896):** Giovanni Battista Grassi and Salvatore Calandruccio watch a transparent leaf-shaped marine fish (*Leptocephalus brevirostris*) shrink into a glass eel.
3. **Part 03 — Trailing a Millimetre Across the Atlantic (1904–1913):** Midpoint twist — Johannes Schmidt tows plankton nets across the Atlantic, plotting larval sizes (`45 mm → 25 mm`) westward away from Europe.
4. **Part 04 — The Sargasso Sea (1920–1922):** Aboard the *Dana*, Schmidt catches `<10 mm` newly hatched larvae in the Sargasso Sea, proving every European eel is born in one patch of ocean thousands of kilometres from European rivers.
5. **Part 05 — The Last Unseen Act (2022–Present):** 2022 pop-up satellite tags finally track adult European eels entering the Sargasso Sea, yet no human has ever seen wild eels spawn — handing off to the next film.

---

## 6. Retention plan (whole-video watch)

| Minute zone | Job | Picture / VO note |
|-------------|-----|-------------------|
| `0–0:05` | Answer image / proof | Freud's 1876 Trieste laboratory tray and microscope with an ink anatomical sketch showing zero eggs |
| `0:05–0:15` | Title question & apparatus | Hands adjusting the brass microscope over the specimen tray; title question by `0:08`, promise by `0:15` |
| `0:15–0:40` | Stakes + Early `DATA+SCALE` | Animated ink counter/scale (`~400` eels dissected vs `0` eggs found) before `0:40` |
| Chapter starts | Case-file desk card + cold open | Period quote or question; each chapter ends on the question the next chapter answers |
| Mid (`~60%`) | Midpoint twist | "Case closed — eels breed in the Mediterranean? Wrong." Schmidt finds smaller larvae out in the open Atlantic |
| Final chapter | Payoff + hand-off | 2022 satellite tracks into the Sargasso Sea; hand-off to next film (no goodbye, no subscribe ask) |

---

## 7. Sign-off (block production until checked)

- [x] Keywords pulled (`public_search.py` & `neighbours.py`, `2026-11-14`) and `0`-collision primary title locked (`Where Do Eels Come From? (The Sargasso Sea Hunt)`)
- [x] Rule-E topic review `GO` (`94 / 100`, `J2836`)
- [ ] Active HOS WIP slot open (`jobs/WIP.json`)
- [ ] Primary sources & exact quotes verified in `SOURCES.md` (`facts` lane)
- [ ] Script reviewer ≥ 90 & `gate:episode` PASS

**Rule-E Reviewer:** `macbook` (`gemini-argon`, `J2836`)  
**Date:** `2026-11-14`
