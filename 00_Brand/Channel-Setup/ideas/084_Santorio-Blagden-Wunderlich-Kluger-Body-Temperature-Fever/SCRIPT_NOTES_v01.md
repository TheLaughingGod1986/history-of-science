# 084 script v01: notes for review (J0751)

Script: `body_temp_fever_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0751, Gemini Argon, 20 Oct 2026).** Built from `084_Santorio-Blagden-Wunderlich-Kluger-Body-Temperature-Fever/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-20_J0743.md` (`evidence_2026-10-20_J0743/n_body_temp_fever.md` PASS — 4 education videos ≥ 1M views, ALL 4 strictly on fever and sweating: **Kurzgesagt – In a Nutshell *Fever Feels Horrible, but is Actually Awesome!* (`cRZOUcpiOxY`, 11.47M — exact hypothalamic fever set-point & immune survival match!)**, **TED-Ed ★ *Why do you get a fever when you're sick? - Christian Moro* (`jRvxnpfCDSo`, 1.62M — exact subject match!)**, **TED-Ed ★ *Why do we sweat? - John Murnan* (`fctH_1NuqCQ`, 1.46M — exact subject match!)**, and **MinuteEarth *How Fevers REALLY Work* (`qDSc2RkVWAQ`, 1.20M — exact subject match!)**, plus **SciShow *Why Do Fevers Get Worse at Night?* (`aVi-zF0Yr8I`, 491.0k)**, **SciShow *Why Do I Sweat So Much?* (`MAUvnCsV6C4`, 440.7k)**, **SciShow Kids *Why Do We Sweat?* (`c2_aN98p0RM`, 294.4k)**, and **The Royal Institution *How To Sweat Less - The Science of Sweating* (`FLFd85y7MUM`, 268.3k)**, alongside `public_search.md` & `public_search_titles.md` showing `"why do we get a fever"` is an exact YouTube autocomplete match (`yes`), all 5 top GB search results for `"charles blagden carl wunderlich body temperature fever"` under 100k views, and all 5 top GB slots for *How a 126 Degree Room and 1 Million Readings Unlocked Human Body Temperature* under 571k views). The topic isn't locked yet: Chief locks `084` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; Santorio Santorio's 1612–1614 clinical mouth thermometer and weighing chair and Charles Blagden's 23 January 1775 `126 °C` (`260 °F`) heated-room beefsteak experiment proving evaporative sweat cooling land in Part 02; the midpoint twist ("Case closed — thirty-seven degrees Celsius (`98.6 °F`) is a flat, unchanging number stamped into every human body, and a fever happens when an infection overheats your blood like a car engine with a broken radiator! Wrong on both counts!") with Carl Wunderlich's 1868 1,000,000 armpit readings across 25,000 patients and Henry Barbour's 1912 `anterior hypothalamus` thermostat proof lands in Part 03; Paul Beeson's 1948 leukocyte `endogenous pyrogens` (`Interleukin-1 → prostaglandin E₂`) and Matthew Kluger's 1975 desert iguana behavioural fever survival proof (`75% vs 25%`) land in Part 04; the ending hands off directly to `085` (*How Do Your Taste Buds Detect Sweet, Salty, Sour, Bitter & Umami — and Why Was Every School Textbook's "Tongue Map" Wrong for 100 Years?*), with no goodbye and no subscribe ask. Five VO parts, matching 009–083.

## Marker count (v01)

Run on `body_temp_fever_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked Charles Blagden (1775) `126 °C` (`260 °F`) room vs `37.8 °C` (`100 °F`) core temperature & evaporative cooling latent heat (`2,428 J / 580 cal` per gram) chart (0:34); 2) inked Wunderlich (1868) & Barbour/Beeson (1912–1948) hypothalamic set-point (`37.0 °C → 39.0 °C`) vs core temperature chills/crisis curve (0:52); 3) inked Santorio (1614 *De Statica Medicina*) weighing-chair water-loss balance & Blagden (1775 *Phil. Trans.*) oiled-vs-open water flask evaporation chart (1:58); 4) inked Carl Wunderlich (1868) 25,000-patient circadian temperature range (`36.2–37.5 °C` around `37.0 °C`) & Henry Barbour (1912) anterior hypothalamic thermode warming-vs-cooling response chart (3:47); 5) inked Paul Beeson (1948) & Matthew Kluger (1975 *Science*) desert iguana (*Dipsosaurus dorsalis*) behavioural fever survival curve (`75% vs 25%`) (5:32); 6) animated timeline 1612–1975 (6:48) | ≥ 3 per long, including the timeline |
| `SCALE` | **6** | 1) evaporating 1 litre of sweat off your skin carries away 580 kcal — enough heat to bring >5 large mugs of ice-cold water to a rolling boil (0:34); 2) Wunderlich's foot-long thermometer took 20 minutes per armpit reading — 1,000,000 measurements took >300,000 hours of waiting (0:52); 3) inside Blagden's 126 °C room a dead beefsteak cooked in 33 minutes because dead meat cannot sweat, while living scientists stood unharmed inside a self-cooling sweat shield (1:58); 4) the thermostat controlling all 37 trillion cells in your body sits in the preoptic hypothalamus and is no bigger than a garden pea (3:47); 5) raising body temperature by 2 °C in a fever burns ~25% more energy — like jogging several miles in bed, to supercharge immune cells and starve bacteria of iron (5:32); 6) from a 126 °C brick oven in Georgian London to 1,000,000 readings in Leipzig and fever-seeking lizards in Michigan (6:48) | `SCALE:` on every `DATA:` (`grep -c` matches) |
| `WHO` | **9** | Santorio Santorio (1561–1636) — Venetian physician and physiologist; Charles Blagden (1748–1820) — British physician and physicist; Carl Reinhold August Wunderlich (1815–1877) — German physician and professor; Henry Gray Barbour (1886–1943) — American pharmacologist and physiologist; Paul Bruce Beeson (1908–2006) — American physician and researcher; Matthew Jay Kluger (born 1945) — American physiologist; George Fordyce (1736–1802) — Scottish physician and chemist; Joseph Banks (1743–1820) — British naturalist and botanist; Thomas Clifford Allbutt (1836–1925) — British physician | Every named person at first mention, role right for the scene's year |
| `WHEN` | **21** | London, 23 January 1775 (0:00); 1612, 23 January 1775, 1868, 1912, 1948, 1975 (0:34); 1612, 1614, 23 January 1775 (1:28); 1866, 1868, 1912 (3:13); 1948, 1975 (4:58); 1612–1975 timeline marker (6:48); 1901, 25 July 1908, 1942, 1974, 2002 (7:45) | Every spoken date or era |
| `FACT` | **3** | `Sweat cooled a 126°C room` (1:28); `1 million readings set 37°C` (3:13); `Lizards seek fever to live` (4:58) | 2–4 per long, ≤ 4 words per card |

## Craft lessons check (*Reference lessons* §1)

- **Cold opens & cliffhanger hand-offs:** Part 01 opens cold on how your body stays locked at `37 °C` in snow or desert heat, why your brain gives you a fever, and how Charles Blagden stood inside a `126 °C` room beside a cooking beefsteak, and ends on Santorio's 30-year weighing chair and Blagden's `126 °C` oven; Part 02 opens cold on Santorio's 1612 mouth thermometer and weighing chair and Blagden's 23 January 1775 `126 °C` room with open vs oiled flasks proving evaporative sweat cooling, and ends on how Carl Wunderlich in Leipzig in 1868 took 1,000,000 armpit measurements to define `37.0 °C`; Part 03 opens cold on the midpoint twist ("Case closed — thirty-seven degrees Celsius (`98.6 °F`) is a flat, unchanging number stamped into every human body, and a fever happens when an infection overheats your blood like a car engine with a broken radiator! Wrong on both counts!"), tells the story of Allbutt's 1866 pocket thermometer, Wunderlich's 1868 1,000,000 readings, and Barbour's 1912 `anterior hypothalamus` silver water-tube thermostat proof, and ends on why your brain makes you shiver under blankets to reach `39 °C` and how Paul Beeson (1948) and Matthew Kluger's desert lizards (1975) proved fever saves lives; Part 04 opens cold on Beeson's 1948 leukocyte `endogenous pyrogens` (`chills` vs `crisis sweat`) and Kluger's 1975 desert iguana behavioural fever experiment (`75% vs 25%` survival), and ends on how 10,000 taste buds test fuel for that furnace and why every biology textbook's "Tongue Map" was wrong for 100 years; Part 05 opens cold on the living thermostat, and hands off to Hänig (1901), Ikeda (1908 `umami`), Boring (1942), Collings (1974), and Zuker (2002) (`085`).
- **Quirky anecdote before the hard idea:** Santorio Santorio eating and sleeping on a hanging steelyard chair for 30 years; Charles Blagden cooking a raw beefsteak with a bellows inside a `126 °C` room while his own breath cooled the wall thermometer; Carl Wunderlich waiting 20 minutes per armpit reading a million times; infected desert iguanas walking under a heat lamp to give themselves a life-saving fever!
- **Rivalry / tension:** Boerhaave's dogma that air above blood heat kills vs Blagden's `126 °C` evaporative cooling proof; fever as a "broken radiator / disease" vs Barbour, Beeson & Kluger's regulated hypothalamic defence weapon.
- **Misconception explained away:** "Do you shiver at the start of a fever because your body is cold, and is a fever just your body overheating out of control?" — refuted by Barbour & Beeson's hypothalamic set-point jump from `37 °C` to `39 °C` and Kluger's survival proof (Parts 01, 03 & 04).

## For Chief to decide

1. Lock **084 = How Does Your Body Keep Its Temperature at Exactly 37 °C in Freezing Snow or Desert Heat — and Why Does Your Brain Give You a Fever When You're Sick (`Thermoregulation, Evaporating Sweat, the Hypothalamic Thermostat, Carl Wunderlich's 1868 1-Million-Reading 37 °C Thermometer & Fever`)? Santorio Santorio's 1612 Clinical Mouth Thermometer & Weighing Chair, Charles Blagden's 23 January 1775 `126 °C` (`260 °F`) Heated-Room Beefsteak Experiment (`Evaporating Sweat`), Carl Reinhold August Wunderlich's 1868 `1,000,000-Reading` Discovery of `37.0 °C` (`98.6 °F`) & Fever Curves, and Henry Barbour (1912), Paul Beeson (1948) & Matthew Kluger's (1975) Discovery of the `Hypothalamic Thermostat` and Why Fever Saves Lives (1612–1975)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Fever: Why Your Brain Heats Your Blood to 39°C* (46 chars)
   - **B (Search question, §1 rule 2):** *How a 126 Degree Room and 1 Million Readings Unlocked Human Body Temperature* (76 chars)
   - **Alt (Search / twist question):** *How Your Body Locks at 37°C and Why Your Brain Gives You a Fever* (64 chars)
2. Review `body_temp_fever_script_master_v01.md` (91.4/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# body_temp_fever_script_master_v01.md

**Decision:** PASS · **Score:** 91.4 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 7.6 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1561 · Est. min: 10.4 · Chapters: 4

## Cold open excerpt

> How does your body stay locked at thirty-seven degrees Celsius ( 98.6 °F ) in freezing snow or desert heat — and why does your own brain give you a fever when you get sick? On twenty-three January seventeen seventy-five , a British doctor stood inside a room heated to one hundred

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91.4/100 — proceed to VO after production checklist.

Pass threshold: 90
```
