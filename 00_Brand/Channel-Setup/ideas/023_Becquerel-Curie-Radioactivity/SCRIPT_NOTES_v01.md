# 023 script v01: notes for review (J0447)

Script: `curie_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0447, Gemini Argon, 17 Oct 2026).** Built from `023_Becquerel-Curie-Radioactivity/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-17_J0438.md` (`evidence_2026-10-17_J0438/n_curie.md` PASS — 5 education videos ≥ 1M views including **three TED-Ed videos ≥ 1M** led by **TED-Ed ★ *The genius of Marie Curie - Shohini Ghose* (`w6JFRi0Qm_s`, 4.14M — exact Marie Curie discovery match)**, **TED-Ed ★ *Is radiation dangerous? - Matt Anticole* (3.00M)**, **FuseSchool *Stable and Unstable Nuclei | Radioactivity* (1.04M)**, and **TED-Ed ★ *Radioactivity: Expect the unexpected - Steve Weatherall* (1.01M)**, plus `public_search.md` showing `"henri becquerel radioactivity"` autocompleting in GB search with all 5 top GB slots under 144k views). The topic isn't locked yet: Chief locks `023` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–5) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Wrong." — after Marie and Pierre Curie discovered polonium on 18 July 1898 and radium on 26 December 1898, orthodox chemists refused to believe radium existed until Marie boiled tonnes of brown pitchblende waste in a leaky Rue Lhomond dissecting shed for 45 months to isolate 0.1 gram of pure radium chloride in July 1902, and then four French Academy members secretly nominated only Becquerel and Pierre Curie for the 1903 Physics Nobel until Gösta Mittag-Leffler warned Pierre, making Marie the first woman Nobel laureate in 1903 and the only two-science Nobel laureate in 1911) lands in Part 04; the popular misconception ("Many people picture pure radium glowing bright cartoon green, or wonder how a cold rock can pour out energy for centuries without breaking the laws of physics") is raised and explained away in Part 05 via pale blue-violet nitrogen ionization, Ernest Rutherford and Frederick Soddy's 1902–1903 nuclear transmutation proof, and Radium-226's 1,600-year half-life keeping Marie Curie's notebooks inside lead-lined boxes at the Bibliothèque Nationale in Paris; the ending hands off directly to `024` (*Thermodynamics & Conservation of Energy: Count Rumford's Boiled Cannon & James Prescott Joule's Falling-Weight Paddle Wheel*, January 1798 & June 1845), with no goodbye and no subscribe ask. Five VO parts, matching 009–022.

## Marker count (v01)

Run on `curie_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **5** | 1) inked radioactivity comparison on period paper comparing pure Uranium (1x), raw Joachimsthal Pitchblende ore (4x uranium), and pure Radium (over 1,000,000x uranium) (0:34); 2) inked yield comparison showing several tonnes (1,000,000+ grams) of pitchblende residue refined down to 0.1 gram of pure radium chloride in July 1902 (0:52); 3) inked exposure comparison on period paper showing Becquerel's expectation (0 hours of sunlight = 0 exposure in the dark drawer) vs the 1 March 1896 result (96 hours in a pitch-dark drawer = full-strength blackening across the Maltese cross) (2:28); 4) inked electrometer current bar chart on period paper from Marie Curie's 12 April 1898 Academy note: Metallic Uranium = 24 picocoulombs/s (24 × 10⁻¹² A), Natural Chalcolite = 52 picocoulombs/s (~2x uranium), Joachimsthal Pitchblende = 83 picocoulombs/s (~3.5–4x uranium) (3:42); 5) animated timeline building 1 Mar 1896 · 12 Apr 1898 · 18 Jul & 26 Dec 1898 · Jul 1902 · Dec 1903 · 1911 · 3500 AD alongside an inked Radium-226 nuclear transmutation and 1,600-year half-life decay curve (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **5** | 1) one million times more active than uranium — a single pinch of radium pouring out as many rays as an entire freight-train car of uranium rock (0:34); 2) ten million parts of rock for one part of radium — like hunting for a single grain of salt hidden inside a swimming pool of sand (0:52); 3) four days locked in a pitch-black drawer with zero sunlight — and the rock burned an image as strong as midday sun (2:28); 4) 83 trillionths of an ampere — an electric current a hundred billion times smaller than a household lightbulb, measured with a stretched crystal of quartz and a stopwatch (3:42); 5) a half-life of 1,600 years — if a Roman emperor had spilled radium in 400 AD, half of those exact atoms would still be firing radiation today (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **9** | Henri Becquerel (0:34), Marie Skłodowska Curie (0:34), Pierre Curie (0:34), Henri Poincaré (1:28), Jacques Curie (3:08), Gustave Bémont (4:58), Eugène-Anatole Demarçay (4:58), Gösta Mittag-Leffler (6:00), Frederick Soddy (6:43) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **25** | Paris 1 March 1896 (0:00), February 1896 (0:21), 26 February 1896 (0:34), 1 March 1896 (0:34), December 1898 (0:34), Paris 20 January 1896 (1:28), 24 February 1896 (1:28), 26 February 1896 (1:58), 1 March 1896 (1:58), 2 March 1896 (1:58), Paris 1891 (3:08), Late 1897 (3:08), 12 April 1898 (3:42), 18 July 1898 (4:58), 26 December 1898 (4:58), July 1902 (5:30), March 1903 (5:30), December 1903 (6:00), 1911 (6:00), 1902–1903 (6:43), 4 July 1934 (6:43), 3500 AD (6:43), 1896–3500 AD (6:43), January 1798 (7:45), June 1845 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | No sunlight needed at all (1:58); Studied at secret university (3:08); 2 Nobels in 2 sciences (6:00); Notebooks need lead for 1,600 yr (6:43) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (Henri Becquerel pulling a paper-wrapped glass plate out of a dark wooden desk drawer on 1 March 1896 as the jet-black silhouette of a copper Maltese cross burns into view beside a glowing vial of Marie Curie's radium), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Becquerel's 26 February–1 March 1896 drawer discovery and Marie & Pierre Curie's 1898 discovery of polonium and radium over a million times more active than uranium) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:00 (Part 04 holding a thermometer against a glowing radium tube in the freezing shed and warming its hands in amazement).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why Becquerel put a copper cross and uranium into a dark drawer and why he developed the plate when the sun had never come out; Part 02 opens cold on Henri Poincaré showing Röntgen's X-rays on 20 January 1896, Becquerel's wrong sunlight hypothesis on 24 February 1896, and the cloudy week of 26 February–1 March 1896 when the Maltese cross burned jet-black in a pitch-dark drawer, ending on why physicists walked away and how a 30-year-old Polish student measured the rays without a photographic plate; Part 03 opens cold on Maria Skłodowska's underground "Floating University" in Warsaw, Pierre and Jacques Curie's piezoelectric quartz electrometer, and the 12 April 1898 shock that raw pitchblende ore is nearly four times more active than pure uranium, ending on why they found two new elements instead of one and why chemists still refused to believe them; Part 04 opens cold on Polonium (18 July 1898) and Radium (26 December 1898) and lands the midpoint twist ("Case closed? Wrong." — 45 months boiling tonnes of waste in a freezing dissecting shed to isolate 0.1 g of pure radium chloride in July 1902, and the 1903 French Academy nomination letter omitting Marie that Gösta Mittag-Leffler and Pierre Curie stopped), ending on why radium pours out heat for years and why visitors to Paris today must open a lead box to read Marie Curie's notebooks; Part 05 opens cold on the neon-green and energy-creation misconceptions, explains Rutherford and Soddy's 1902–1903 nuclear transmutation and Radium-226's 1,600-year half-life, and hands off to Count Rumford's January 1798 Munich cannon and James Prescott Joule's June 1845 paddle wheel (`024`).
- **Quirky anecdote before the hard idea:** Becquerel's experiment ruined by four days of cloudy Paris winter weather in February 1896; Maria Skłodowska studying by candlelight in Warsaw's secret underground "Floating University" and stirring boiling 20 kg cauldrons of waste slag with an iron rod nearly as tall as herself.
- **Rivalry / tension:** back-and-forth portrait cuts between the four French Academy nominators excluding Marie Curie and Gösta Mittag-Leffler alerting Pierre Curie in 1903 (6:00).
- **Misconception explained away:** "Many people picture pure radium glowing bright cartoon green, or wonder how a cold rock can pour out energy for centuries without breaking the laws of physics" — explained via pale blue-violet nitrogen ionization (vs zinc-sulfide watch paint) and Rutherford & Soddy's 1902–1903 spontaneous nuclear transmutation (Part 05, 6:43).

## For Chief to decide

1. Lock **023 = Radioactivity: Henri Becquerel's Cloudy-Day Drawer & Marie Curie's Freezing Shed (1896–1902)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Radioactivity: Why Marie Curie's Notebooks Still Glow* (53 chars)
   - **B (Search question, §1 rule 2):** *How a Dark Desk Drawer and a Freezing Shed Found Radium* (55 chars)
   - **Alt (Search / twist question):** *Why Cloudy Weather in Paris Revealed That Atoms Explode* (55 chars)
2. Review `curie_script_master_v01.md` (91.6/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–5) before VO.

## Score (`npm run review:script`)

```text
# curie_script_master_v01.md

**Decision:** PASS · **Score:** 91.6 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 7.8 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1542 · Est. min: 10.3 · Chapters: 4

## Cold open excerpt

> How did a week of cloudy weather in Paris — and a pitch-dark wooden desk drawer — reveal that atoms can pour out invisible energy for thousands of years without any fuel at all? By the end of this film, you'll see why a ruined sunlight experiment accidentally caught atoms breakin

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91.6/100 — proceed to VO after production checklist.

Pass threshold: 90
```
