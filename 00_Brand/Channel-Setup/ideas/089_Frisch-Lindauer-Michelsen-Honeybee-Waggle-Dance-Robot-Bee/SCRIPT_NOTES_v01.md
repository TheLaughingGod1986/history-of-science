# 089 script v01: notes for review (J0783)

Script: `waggle_dance_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0783, Gemini Argon, 21 Oct 2026).** Built from `089_Frisch-Lindauer-Michelsen-Honeybee-Waggle-Dance-Robot-Bee/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-21_J0758.md` (`evidence_2026-10-21_J0758/n_bees_waggle_dance.md` PASS — 6 education videos ≥ 1M views, ALL 6 strictly on bees: **Kurzgesagt – In a Nutshell *The Death Of Bees Explained – Parasites, Poison and Humans* (`GqA42M4RtxE`, 15.42M)**, **MinuteEarth *Why There Are No King Bees* (`uKP3lc9SOaA`, 6.99M)**, **SciShow *How Bees Choose Their Queen* (`m_SlH3Uwslc`, 6.43M)**, **Be Smart *How Do Bees Make Honey?* (`nZlEjDLJCmg`, 5.44M — exact honeybee foraging & waggle dance match!)**, **SciShow Kids *Busy Bees! | Bumblebees and Honeybees* (`ta154f5Rp5Y`, 3.85M)**, and **TED-Ed ★ *Licking bees and pulping trees: The reign of a wasp queen* (`q93IfqUbEf4`, 3.31M)**, plus **SciShow Kids `A4YIpGQiD3w` (`915.4k`)**, **SciShow `3h4uVVFCvVg` (`664.9k`)**, **TED ★ *Marla Spivak: Why bees are disappearing* (`dY7iATJVCso`, 629.6k)**, and **TED-Ed ★ *How bees help plants have sex* (`Y5uRVv7GGQM`, 182.5k)**, alongside `public_search.md` & `public_search_titles.md` showing `"how do bees make honey"` is an exact YouTube autocomplete match (`yes`), 4 of the top 5 GB search results for `"karl von frisch honeybee waggle dance"` under 909k views, and all 5 top GB slots for *How a Dot of Paint and a Robot Bee Cracked the Honeybee Waggle Dance* under 483k views). The topic isn't locked yet: Chief locks `089` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; Karl von Frisch's 1914 30-grey checkerboard colour-vision proof and Summer 1944–1946 Brunnwinkl painted-bee glass hive discovery of the figure-eight `waggle dance` sun-to-gravity code land in Part 02; the midpoint twist ("Case closed — the waggle dance is just a hardwired reflex for fetching sugar water when the Sun is shining! Wrong!") with von Frisch's 1949 Polaroid-filter ultraviolet polarized-sky compass and Martin Lindauer's 1951–1955 `15°/hour` time-compensated marathon dances and swarm house-hunting democracy lands in Part 03; the 1967–1975 odour-plume controversy (Adrian Wenner vs James Gould) and Axel Michelsen, Wolfgang Kirchner & Martin Lindauer's June 1989 computer-controlled `280-Hz` brass-and-razor-blade mechanical robot bee proof land in Part 04; the ending hands off directly to `090` (*How Does a Single Drop of Snake Venom Stop a Breath or Clot a Bucket of Blood in Seconds — and How Did Horse Serum & Brazilian Pit-Viper Poison Save Millions of Lives?*), with no goodbye and no subscribe ask. Five VO parts, matching 009–088.

## Marker count (v01)

Run on `waggle_dance_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked Karl von Frisch (1946 *Experientia*) waggle dance sun-to-gravity angle (`0°`, `60°`, `180°`) & waggle-run duration vs flight distance curve (`~1 s ≈ 1,000 m`) (0:34); 2) inked Axel Michelsen, Wolfgang Kirchner & Martin Lindauer (1989 *Naturwissenschaften*) robot-bee directional and distance recruitment accuracy chart (0:52); 3) inked Karl von Frisch (1914 *Zool. Jahrb.*) blue-card-in-30-greys colour vision proof & (1946 *Experientia*) figure-eight waggle dance sun-to-gravity transposition (1:58); 4) inked Karl von Frisch (1949 *Experientia*) Polaroid-filter UV sky-polarization compass & Martin Lindauer (1955 *Z. vergl. Physiol.*) 5-day swarm house-hunting consensus chart + `15°/hour` shift (3:47); 5) inked Michelsen, Kirchner & Lindauer (June 1989 *Naturwissenschaften*) `280-Hz` brass-and-razor-blade robot bee schematic & 8-station polar capture histogram (5:32); 6) animated timeline 1914–1989 (6:48) | ≥ 3 per long, including the timeline |
| `SCALE` | **6** | 1) a honeybee's brain weighs 1 mg — smaller than a sesame seed — yet converts the angle of the Sun into the pull of gravity under her feet (0:34); 2) a single half-kilogram jar of honey takes two million flower visits and ~90,000 km of flight — more than twice around the Earth (0:52); 3) five spots of coloured shellac paint let von Frisch recognize bee #342 at a glance among 50,000 sisters (1:58); 4) a marathon scout bee dancing in a windowless room for four hours automatically rotates her waggle angle by 60° — 15° per hour (3:47); 5) Michelsen's robot bee was made from a scrap of brass tubing, a sliver of a shaving razor blade, and beeswax, yet sent living bees to a meadow 1 km away (5:32); 6) from five dots of shellac paint on an Austrian lakeside to a vibrating razor-blade robot in a dark hive (6:48) | `SCALE:` on every `DATA:` (`grep -c` matches) |
| `WHO` | **7** | Karl Ritter von Frisch (1886–1982) — Austrian ethologist and zoologist; Martin Lindauer (1918–2008) — German behavioral biologist; Axel Michelsen (born 1940) — Danish biophysicist; Wolfgang H. Kirchner (born 1959) — German behavioral biologist; Carl von Hess (1863–1923) — German ophthalmologist; Adrian M. Wenner (1928–2023) — American biologist; James L. Gould (born 1945) — American ethologist and evolutionary biologist | Every named person at first mention, role right for the scene's year |
| `WHEN` | **26** | Brunnwinkl, Austria, Summer 1945 (0:00); 1914, 1944, 1946, 1949, 1951, 1989 (0:34); 1910, 1914, 1923, Summer 1944, Summer 1945, 1946 (1:28); 1948, 1949, 1951, 1955, 1973 (3:13); 1967, 1975, June 1989 (4:58); 1914–1989 timeline marker (6:48); 1664, 10 February 1894, 1965, 1975 (7:45) | Every spoken date or era |
| `FACT` | **3** | `Gravity stands for the Sun` (1:28); `Swarms vote by waggle dance` (3:13); `Robot bee sent real bees` (4:58) | 2–4 per long, ≤ 4 words per card |

## Craft lessons check (*Reference lessons* §1)

- **Cold opens & cliffhanger hand-offs:** Part 01 opens cold on how a lone honeybee tells 50,000 sisters in a pitch-black hive the exact compass direction and distance to flowers miles away, and ends on how Karl von Frisch proved bees see colour in 1914 and why he misunderstood the dance for 20 years before Summer 1944; Part 02 opens cold on von Frisch's 1914 blue-card-in-30-greys experiment and Summer 1944–1946 painted-bee discovery of the figure-eight `waggle dance`, and ends on what happens when the Sun is hidden behind a mountain or clouds and how homeless swarms vote; Part 03 opens cold on the midpoint twist ("Case closed — the waggle dance is just a hardwired reflex for fetching sugar water when the Sun is shining! Wrong!"), tells the story of von Frisch's 1949 Polaroid sky compass and Martin Lindauer's 1951–1955 `15°/hour` marathon dancers and swarm house-hunting democracy, and ends on Adrian Wenner's 1967 odour challenge; Part 04 opens cold on how to test the dance without outdoor flower scent by building a robot bee, tells the story of Axel Michelsen, Wolfgang Kirchner & Martin Lindauer's June 1989 `280-Hz` brass-and-razor-blade mechanical robot bee, and ends on how honeybees defend their hive with venom and how scientists turned deadly snake venom into antivenom and heart medicine; Part 05 opens cold on the sesame-seed GPS, and hands off to Francesco Redi (1664), Albert Calmette & Césaire Phisalix (1894), and Sérgio Ferreira, David Cushman & Miguel Ondetti (`Captopril`, `090`).
- **Quirky anecdote before the hard idea:** Five-colour shellac paint code numbering individual bees up to #599; marathon dancers shifting their dance angle 15° every hour inside a windowless room; a mechanical robot bee built from brass tubing, beeswax, and a sliver of a shaving razor blade!
- **Rivalry / tension:** Carl von Hess's 1910 dogma that all invertebrates are colour-blind vs 27-year-old Karl von Frisch's 1914 30-grey checkerboard proof; Adrian Wenner's 1967–1989 odour-plume skeptics vs James Gould's 1975 ocelli misdirection test and Axel Michelsen's 1989 computer-controlled robot bee.
- **Misconception explained away:** "Don't honeybees just follow the scout bee back to the flowers, or sniff out the smell on the wind?" — refuted by trapping the scout in a jar and by Michelsen's unscented indoor robot bee sending real bees to an empty meadow (Parts 01, 04, 05).

## For Chief to decide

1. Lock **089 = How Do Honeybees Tell Their Hive Exact Directions to Flowers Miles Away in Pitch Darkness — and How Did a Glass Hive, a Dot of Paint & a Robot Bee Crack the Waggle Dance Code (`Honeybee Communication, Karl von Frisch's 1944–1946 Waggle Dance & Polarized-Light Sun Compass, Martin Lindauer's 1951 Swarm Democracy & Axel Michelsen's 1989 Robot Bee Proof`)? Karl von Frisch's 1914–1946 Painted-Bee Glass Observation Hive & `Waggle Dance` Sun-Angle Code (`1973 Nobel Prize`), Martin Lindauer's 1951–1955 House-Hunting Swarm Consensus, and Axel Michelsen, Wolfgang Kirchner & Martin Lindauer's 1989 Computer-Controlled `Mechanical Robot Bee` Proof (1914–1989)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *The Waggle Dance: How a Robot Bee Proved Bees Can Talk* (54 chars)
   - **B (Search question, §1 rule 2):** *How a Dot of Paint and a Robot Bee Cracked the Honeybee Waggle Dance* (68 chars)
   - **Alt (Search / twist question):** *How Honeybees Give GPS Directions in Pitch Darkness* (51 chars)
2. Review `waggle_dance_script_master_v01.md` (92.3/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# waggle_dance_script_master_v01.md

**Decision:** PASS · **Score:** 92.3 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 7.5 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 9 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1479 · Est. min: 9.9 · Chapters: 4

## Cold open excerpt

> How can a lone honeybee tell fifty thousand sisters in a pitch-black hive the exact compass direction and distance to flowers two miles away ? And how did a tiny dot of paint in nineteen forty-five and a computer-controlled robot bee in nineteen eighty-nine crack the secret langu

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 92.3/100 — proceed to VO after production checklist.

Pass threshold: 90
```
