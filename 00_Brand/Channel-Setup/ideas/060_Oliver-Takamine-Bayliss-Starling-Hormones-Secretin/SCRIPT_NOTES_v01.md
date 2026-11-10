# 060 script v01: notes for review (J0629)

Script: `hormones_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0629, Gemini Argon, 19 Oct 2026).** Built from `060_Oliver-Takamine-Bayliss-Starling-Hormones-Secretin/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-19_J0621.md` (`evidence_2026-10-19_J0621/n_hormones_endocrine.md` PASS — 6+ education videos ≥ 1M views: **CrashCourse *Endocrine System, Part 1 - Glands & Hormones: Crash Course Anatomy & Physiology #23* (`eWHH9je2zG4`, 7.58M — exact subject match!)**, **TED-Ed ★ *How does your immune system work? - Emma Bryce* (`PSRJfaAYkW4`, 5.20M)**, **TED-Ed ★ *How your muscular system works - Emma Bryce* (`VVL-8zr2hk4`, 3.23M)**, **CrashCourse *Endocrine System, Part 2 - Hormone Cascades: Crash Course Anatomy & Physiology #24* (`SCV_m91mN-Q`, 3.23M — exact subject match!)**, **TED-Ed ★ *How do your hormones work? - Emma Bryce* (`-SPRPkLoKp8`, 2.70M — exact subject match!)**, **Amoeba Sisters *Endocrine System* (`emvHaBiRY8Q`, 2.51M — exact subject match!)**, and **CrashCourse *Great Glands - Your Endocrine System* (`WVrlHH14q3o`, 2.04M)**, plus **Khan Academy *Intro to the endocrine system* (`f_Z1zsR9lFM`, 975.3k)**, alongside `public_search.md` & `public_search_titles.md` showing `"how hormones work"` triggering exact YouTube autocomplete, all 5 top GB search results for `"william bayliss ernest starling secretin hormones"` under 360 views, and 4 of the top 5 GB slots for *How Secret Chemical Messages in Your Blood Control Your Body* under 549k views). The topic isn't locked yet: Chief locks `060` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed — when acidic food leaves your stomach, electrical nerve wires telegraph your pancreas to pour out digestive juice! Wrong! Even when you cut every single nerve wire in the gut, the pancreas still fires right on schedule!" — where William Bayliss and Ernest Starling at University College London on the afternoon of Thursday, 16 January 1902 severed every nerve to an intestinal loop, dripped 0.4% HCl inside, and watched the pancreas pour out juice after 2 minutes before grinding gut mucosa with sand and acid to discover `secretin`) lands in Part 03; Ernest Starling's 20 June 1905 Croonian Lecture coining the word "hormone" (`from Greek hormōn, "to set in motion"`), Edward Kendall's Christmas Day 1914 isolation of `thyroxine`, and Rosalyn Yalow's 1959 radioimmunoassay (`1977 Nobel Prize`) land in Part 04; the nerves-vs-hormones misconception ("Many people still picture the nervous system and the hormone system as two separate worlds") is raised and explained away in Part 05 via the hypothalamus-pituitary neuroendocrine link; the ending hands off directly to `061` (*How Does Every Cell in Your Body Tell Time in Pitch Darkness (`The Circadian Clock & Period Gene`)? Jean-Jacques d'Ortous de Mairan's 1729 Cupboard Plant, Jürgen Aschoff's 1962 Underground Bunker Volunteers, Seymour Benzer & Ronald Konopka's September 1971 Mutant Fruit Flies & Jeffrey Hall, Michael Rosbash and Michael Young's 1984–1994 `PER/TIM` Molecular Hourglass*), with no goodbye and no subscribe ask. Five VO parts, matching 009–059.

## Marker count (v01)

Run on `hormones_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked comparison chart on period paper showing electrical nerve reflexes (wired point-to-point in milliseconds) vs blood-borne endocrine hormones (wireless broadcast through 5 litres of blood in seconds to minutes, active at picomolar-to-nanomolar concentrations, ~1 part per billion) (0:34); 2) inked pancreatic secretion rate chart (drops per minute vs time) from Bayliss & Starling (1902, J. Physiol. 28: 325–353) showing zero secretion at baseline, followed by a sharp surge of pancreatic flow ~2 minutes after either instilling acid into the denervated intestinal loop or injecting acid-extracted intestinal mucosa (`secretin`) into the jugular vein (0:52); 3) inked Oliver & Schäfer (March 1894, J. Physiol. 16: i–iv & 1895 J. Physiol. 18: 230–276) arterial blood-pressure kymograph tracing & Takamine (1901) crystalline adrenaline (`C9H13NO3`) potency chart on period paper showing intravenous suprarenal extract driving arterial pressure from ~100 mmHg to >240 mmHg within seconds via arteriolar vasoconstriction (1:58); 4) inked Bayliss & Starling (1902, Proc. R. Soc. Lond. 69: 352–353 & J. Physiol. 28: 325–353) four-step experimental proof chart on period paper comparing (1) acid in intact duodenum -> secretion, (2) acid in completely denervated jejunum loop -> full secretion after ~2 min, (3) acid injected directly into blood vein -> 0 secretion, and (4) acid-ground jejunal mucosa extract (`secretin`) injected into vein -> massive pancreatic secretion (3:42); 5) inked human endocrine network & radioimmunoassay sensitivity chart on period paper from Starling (August 1905, Lancet 166: 339–341), Kendall (1915, JAMA / 1950 Nobel), and Yalow & Berson (1959–1960, Nature / J. Clin. Invest.) mapping the hypothalamus-pituitary master axis, thyroid (thyroxine), adrenal (adrenaline, cortisol), pancreas (secretin, insulin), and gonads, detected at picogram-per-millilitre (`10^-12 g/mL`) levels (5:28); 6) animated timeline building Mar 1894 & 1901 · 16 Jan 1902 · 20 Jun 1905 · 1914–1977 (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) a single hormone in your blood is so potent that it works at one part per billion — like dissolving a single pinch of salt inside an Olympic swimming pool and having every cell in the pool taste it (0:34); 2) even with every nerve wire severed by a scalpel, it took just one hundred and twenty seconds for a chemical letter posted in the gut to ride the bloodstream and unlock the pancreas (0:52); 3) Takamine's adrenaline crystals were so powerful that injecting a single millionth of a gram — a speck far too small for the human eye to see — made blood pressure surge inside seconds (1:58); 4) when Pavlov's lab in St. Petersburg repeated Bayliss and Starling's nerve-cut experiment and saw the pancreas pour out juice with every wire cut, Pavlov stepped out of his office, shook his head, and said: "Of course they are right — we cannot claim a monopoly on truth" (3:42); 5) Rosalyn Yalow's 1959 hormone detector was so sensitive it could spot a single lump of sugar dissolved in a lake sixty miles long (5:28); 6) from a single afternoon nerve-cutting experiment in London to over fifty known human hormones, Bayliss and Starling revealed the wireless chemical postal service that runs your body (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **11** | George Oliver (0:34), Edward Sharpey-Schäfer (0:34), Jokichi Takamine (0:34), Keizo Uenaka (0:34), William M. Bayliss (0:34), Ernest H. Starling (0:34), Thomas Addison (1:28), John Jacob Abel (1:28), Ivan P. Pavlov (3:08), Edward C. Kendall (4:53), Rosalyn S. Yalow (4:53) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **17** | London, 16 January 1902 (0:00), March 1894 (0:34), 1900–1901 (0:34), 16 January 1902 (0:34), 20 June 1905 (0:34), 1855 (1:28), March 1894 (1:28), 21 July 1900 (1:28), 1901 (1:28), 16 January 1902 (3:08), 20 June 1905 (4:53), 25 December 1914 (4:53), 1959 (4:53), 1977 (4:53), 1894–1977 (6:43), 1729 (7:45), September 1971 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **3** | First pure hormone: adrenaline (1901) (1:28); Cut every nerve; gut still talked (3:08); "Hormone" means "to set in motion" (4:53) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (William Bayliss and Ernest Starling at UCL on 16 January 1902 severing every electrical nerve wire to a loop of small intestine, dripping dilute acid inside, and watching glowing `secretin` molecules enter the bloodstream and trigger the pancreas), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (George Oliver & Edward Schäfer's March 1894 adrenal blood-pressure surge, Jokichi Takamine & Keizo Uenaka's 1900–1901 crystalline `adrenaline`, and Bayliss & Starling's 16 January 1902 discovery of `secretin` and June 1905 coining of "hormone") by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:05 (Part 04 dispatching colour-coded chemical couriers from the hypothalamus and pituitary master switchboard into a glass blood tube).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why almost every scientist in 1894 believed nerve wires ran the entire body and what happened when a country doctor walked into a London lab with a vial of adrenal extract; Part 02 opens cold on the 300-year mystery of the tiny triangular adrenal glands atop the kidneys, tells the story of Thomas Addison (1855), George Oliver and Edward Schäfer's March 1894 mercury manometer shock, and Jokichi Takamine and Keizo Uenaka's 21 July 1900 – 1901 crystallization of pure `adrenaline`, and ends on what happened on 16 January 1902 when two brothers-in-law in London tested Ivan Pavlov's nerve-only rule; Part 03 opens cold on the midpoint twist ("Case closed — when acidic food leaves your stomach, electrical nerve wires telegraph your pancreas to pour out digestive juice! Wrong!"), tells the story of William Bayliss and Ernest Starling's 16 January 1902 nerve-cut jejunum and mortar-and-sand `secretin` experiment, and ends on how a dinner in Cambridge in 1905 gave us the word "hormone"; Part 04 opens cold on how to name a discovery that rewrites physiology, explains William Hardy, W. T. Vesey, and Ernest Starling coining "hormone" on 20 June 1905, Edward Kendall isolating `thyroxine` on Christmas Day 1914, and Rosalyn Yalow inventing radioimmunoassay in 1959, and ends on how your body knows what time of day to release cortisol and melatonin even inside a pitch-black underground bunker; Part 05 opens cold on the nerves-vs-hormones misconception, explains how the hypothalamus links both systems, and hands off to Jean-Jacques d'Ortous de Mairan (1729), Jürgen Aschoff (1962), Seymour Benzer & Ronald Konopka (September 1971), and Jeffrey Hall, Michael Rosbash & Michael Young's discovery of the **`PER/TIM` circadian clock** (`061`).
- **Quirky anecdote before the hard idea:** Edward Schäfer injecting George Oliver's adrenal extract only to humour his guest and watching the mercury float shoot almost out the top of the glass tube; Ernest Starling grinding gut lining with sand and weak acid in a mortar on the spot; coining "hormone" over college dinner in Cambridge!
- **Rivalry / tension:** Ivan Pavlov's St. Petersburg nerve-reflex dogma (`nervism`) vs Bayliss and Starling's blood-borne chemical messengers (`secretin`).
- **Misconception explained away:** "Many people still picture the nervous system and the hormone system as two separate worlds" — explained via high-speed nerve cables and blood-borne hormone broadcasts united by the brain's hypothalamus (Part 05, 6:43).

## For Chief to decide

1. Lock **060 = How Do Secret Chemical Messages in Your Blood Control Your Body (`Hormones & the Birth of Endocrinology`)? George Oliver & Edward Schäfer's March 1894 Adrenal Blood-Pressure Shock, Jokichi Takamine's 1901 Adrenaline Crystals, and William Bayliss & Ernest Starling's 16 January 1902 Denervated Loop Experiment That Discovered `Secretin` and Coined the Word "Hormone" (1894–1977)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Hormones: The Secret Messages in Your Blood* (43 chars)
   - **B (Search question, §1 rule 2):** *How Secret Chemical Messages in Your Blood Control Your Body* (60 chars)
   - **Alt (Search / twist question):** *How Cutting Every Nerve Proved Your Organs Talk Through Your Blood* (66 chars)
2. Review `hormones_script_master_v01.md` (91.2/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# hormones_script_master_v01.md

**Decision:** PASS · **Score:** 91.2 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 7.4 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1426 · Est. min: 9.5 · Chapters: 4

## Cold open excerpt

> How do your organs talk to each other when every single nerve wire between them has been cut ? And how did a nerve-cutting experiment in a London laboratory on the sixteenth of January nineteen oh-two prove that your body is run by secret chemical letters floating through your bl

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91.2/100 — proceed to VO after production checklist.

Pass threshold: 90
```
