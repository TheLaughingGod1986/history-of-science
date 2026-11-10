# 061 script v01: notes for review (J0629)

Script: `circadian_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0629, Gemini Argon, 19 Oct 2026).** Built from `061_deMairan-Aschoff-Benzer-Hall-Rosbash-Young-Circadian-Clock/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-19_J0621.md` (`evidence_2026-10-19_J0621/n_circadian_clock.md` PASS — 19 education videos ≥ 1M views: **TED ★ *Sleep Is Your Superpower | Matt Walker* (`5MuIMqhT8DM`, 17.49M)**, **TED-Ed ★ *What would happen if you didn't sleep? - Claudia Aguirre* (`dqONk48l5vY`, 15.01M)**, **TED-Ed ★ *How stress affects your body* (`v-t1Z5-oPtU`, 9.05M)**, **TED-Ed ★ *The benefits of a good night's sleep* (`gedoSfZvBgE`, 7.47M)**, **TED-Ed ★ *What staying up all night does to your brain* (`idrbwnWLJ7w`, 7.21M)**, **TED ★ *Do You Really Need 8 Hours of Sleep Every Night?* (`fQUeDdaVoWo`, 4.58M)**, **TED-Ed ★ *Can you change your sleep schedule?* (`Amkg1cdDCpM`, 2.68M — exact circadian clock match!)**, **SciShow *Circadian Rhythm and Your Brain's Clock* (`UbQ0RxQu2gM`, 1.15M — exact subject match!)**, and **TED-Ed ★ *How does your body know what time it is? - Marco A. Sotomayor* (`Y8ZXOfWUbms`, 1.05M — exact Period/PER/TIM circadian clock match!)**, alongside `public_search.md` & `public_search_titles.md` showing `"circadian rhythm body clock"` triggering YouTube autocomplete, all 5 top GB search results for `"jeffrey hall michael rosbash michael young circadian rhythm"` under 32k views, and 3 of the top 5 GB slots for *How Every Cell in Your Body Tells Time in Pitch Darkness* under 227k views). The topic isn't locked yet: Chief locks `061` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed — a twenty-four-hour body clock must require hundreds of brain nerves wired together; no single gene could ever set the length of a day! Wrong! Mutate one single gene on the X chromosome, and you can speed the day up to nineteen hours, slow it down to twenty-eight hours, or stop the clock dead!" — where Seymour Benzer and Ronald Konopka at Caltech in September 1971 isolated three single-gene circadian mutants in *Drosophila* all mapping to the X-linked `Period` gene) lands in Part 03; Jeffrey Hall, Michael Rosbash, and Michael Young's 1984–1994 discovery of the `PER/TIM` transcription-translation negative-feedback hourglass (`2017 Nobel Prize`) and David Berson's 8 February 2002 discovery of `480-nm` blue-light melanopsin retinal ganglion cells (`ipRGCs`) land in Part 04; the "only one clock in the brain" misconception ("Many people still assume you have only one body clock inside your head") is raised and explained away in Part 05 via multi-organ `PER/TIM` clocks and jet-lag desynchrony; the ending hands off directly to `062` (*How Do Your Muscles Turn Food Into Motion (and Why Do You Recycle Your Entire Body Weight in `ATP` Every Single Day — `Muscles, ATP & the Sliding Filament Motor`)? Karl Lohmann, Cyrus Fiske & Yellapragada SubbaRow's 1929 Discovery of `ATP`, Albert Szent-Györgyi's 1942 Contracting Rabbit Muscle Threads & Hugh Huxley and Andrew Huxley's Back-to-Back 22 May 1954 Sliding-Filament Proof*), with no goodbye and no subscribe ask. Five VO parts, matching 009–060.

## Marker count (v01)

Run on `circadian_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked circadian period comparison chart on period paper showing wild-type 24-hour rhythm, human free-running bunker period (24 h 11 min average, drifting ~11 minutes later every day without morning sunlight), and Konopka & Benzer's September 1971 single-gene Period (`per`) mutants running at 19 hours (`perS`), 28 hours (`perL`), or losing all rhythm (`per0`) (0:34); 2) inked 24-hour PER/TIM protein & mRNA oscillation curve across a day-night cycle showing `per` mRNA peaking in early evening followed ~4–6 hours later by nuclear PER/TIM protein complex peaking late at night to repress transcription (0:52); 3) inked Aschoff (15 June 1962, Science 136: 963–966), Siffre (July–September 1962 Scarasson cave log), and Czeisler et al. (25 June 1999, Science 284: 2177–2181) human free-running actogram & body-temperature rhythm chart on period paper showing sleep-wake and core temperature cycles drifting slightly later each day in constant conditions with an intrinsic human period of 24.18 hours (24 h 11 min) (1:58); 4) inked Konopka & Benzer (September 1971, PNAS 68: 2112–2116) Drosophila eclosion & locomotor activity rhythm chart on period paper comparing wild-type (24.0 h period), per^01 (arrhythmic), per^S (19.0 h period), and per^L1 (28.0 h period) all mapping to a single locus on the X chromosome (3:42); 5) inked PER/TIM/DBT feedback loop & melanopsin 480-nm blue-light phase-resetting chart on period paper from Bargiello, Jackson & Young (October 1984, Nature 312: 752–754), Zehring et al., Rosbash & Hall (December 1984, Cell 39: 369–376), Hardin, Hall & Rosbash (8 February 1990, Nature 343: 536–540), Vosshall, Price, Sehgal & Young (18 March 1994, Science 263: 1606–1609), and Berson, Dunn & Takao (8 February 2002, Science 295: 1070–1073) showing the 24-hour PER/TIM nuclear negative feedback loop and ~480-nm melanopsin ipRGC signaling to the 20,000-neuron SCN (5:28); 6) animated timeline building 1729 · Jun–Sep 1962 · Sep 1971 · 1984–1994 & 2002 (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) without morning sunlight to reset your eyes, the natural clock inside a human body runs about twenty-four hours and eleven minutes long — drifting eleven minutes later every single day like a pocket watch that runs slightly slow (0:34); 2) every cell in your body tells time like an old sand hourglass — spending twelve hours trickling `PER` and `TIM` protein grains into a pile until at midnight the pile tips over, shuts off the tap, and takes twelve hours to drain away (0:52); 3) when Michel Siffre climbed out of his pitch-black alpine cave on the fourteenth of September nineteen sixty-two after fifty-eight days without a watch, his internal body clock had drifted so steadily that he thought it was still the twentieth of August (1:58); 4) changing a single genetic letter inside the Period gene was like turning the regulating screw on the back of a grandfather clock — speeding a fly's entire day up to nineteen hours or slowing it down to twenty-eight (3:42); 5) staring at a bright blue phone screen at midnight hits your retina with four-hundred-and-eighty-nanometre sky-blue light — fooling the twenty thousand clock neurons at the base of your brain into thinking dawn has just broken (5:28); 6) from a sensitive houseplant locked in a dark Paris cupboard to a twenty-four-hour protein hourglass inside every cell, three centuries of science revealed how living things keep time with the turning Earth (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **10** | Jean-Jacques d'Ortous de Mairan (0:34), Jürgen Aschoff (0:34), Seymour Benzer (0:34), Ronald J. Konopka (0:34), Jeffrey C. Hall (0:34), Michael Rosbash (0:34), Michael W. Young (0:34), Franz Halberg (1:28), Michel Siffre (1:28), David M. Berson (4:53) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **21** | Paris, 1729 (0:00), 1729 (0:34), 15 June 1962 (0:34), September 1971 (0:34), October 1984 (0:34), 1994 (0:34), 1729 (1:28), 1832 (1:28), 1959 (1:28), 15 June 1962 (1:28), 16 July 1962 (1:28), September 1971 (3:08), October 1984 (4:53), February 1990 (4:53), March 1994 (4:53), 8 February 2002 (4:53), 2017 (4:53), 1729–2017 (6:43), August 1929 (7:45), 1942 (7:45), 22 May 1954 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **3** | Human clock: 24 hours, 11 minutes (1:28); One gene sets the 24-hour day (3:08); Blue light (480 nm) resets your clock (4:53) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (Jean-Jacques d'Ortous de Mairan's 1729 *Mimosa* plant unfolding its leaves inside a pitch-black Paris cupboard, zooming into a human cell where glowing `PER` and `TIM` clock proteins accumulate until midnight to switch off their own genes), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (de Mairan's 1729 dark cupboard, Jürgen Aschoff's June 1962 underground bunker, Seymour Benzer & Ronald Konopka's September 1971 `Period` gene, and Hall, Rosbash & Young's 1984–1994 `PER/TIM` molecular hourglass) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:05 (Part 04 shining a 480-nm blue lantern at a retinal melanopsin sensor to reset the 20,000-neuron SCN clock dial).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why a French astronomer in 1729 locked a sensitive houseplant inside a dark cupboard and why sceptics refused to believe him for over 200 years; Part 02 opens cold on gardeners watching *Mimosa pudica* open at dawn, tells the story of de Mairan (1729), de Candolle (1832), Franz Halberg coining "circadian" (1959), and Jürgen Aschoff's June 1962 bunker + Michel Siffre's July–September 1962 alpine glacier cave (`24 h 11 min` human period), and ends on how two scientists in California proved a single gene sets the 24-hour clock; Part 03 opens cold on the midpoint twist ("Case closed — a twenty-four-hour body clock must require hundreds of brain nerves wired together; no single gene could ever set the length of a day! Wrong!"), tells the story of Seymour Benzer and Ronald Konopka's September 1971 *PNAS* discovery of the `19-hour`, `28-hour`, and arrhythmic `Period` (`per`) mutants on the X chromosome, and ends on how a tiny molecule of DNA and protein can count out 24 hours; Part 04 opens cold on how a single gene builds a 24-hour timer, explains Jeffrey Hall, Michael Rosbash, and Michael Young's 1984–1994 `PER/TIM` negative-feedback hourglass (`2017 Nobel Prize`) and David Berson's 8 February 2002 `480-nm` blue-light melanopsin retinal cells, and ends on how your muscles turn breakfast into physical motion; Part 05 opens cold on the "one clock in the brain" misconception, explains jet lag across brain vs liver/gut clocks, and hands off to Karl Lohmann and Fiske & SubbaRow (1929 `ATP`), Albert Szent-Györgyi (1942 rabbit threads), and Hugh Huxley & Andrew Huxley's 22 May 1954 *Nature* **Sliding Filament Theory** (`062`).
- **Quirky anecdote before the hard idea:** De Mairan locking a houseplant inside a Paris cupboard; Michel Siffre emerging from a freezing glacier cave on 14 September 1962 convinced it was still 20 August!
- **Rivalry / tension:** "Factor X" external-cue sceptics vs internal circadian clocks; multi-gene behaviour dogma vs Benzer & Konopka's single `Period` gene; friendly race between Brandeis (Hall & Rosbash) and Rockefeller (Young).
- **Misconception explained away:** "Many people still assume you have only one body clock inside your head" — explained via light-reset SCN master clock vs meal-reset liver and gut `PER/TIM` clocks causing jet lag (Part 05, 6:43).

## For Chief to decide

1. Lock **061 = How Does Every Cell in Your Body Tell Time in Pitch Darkness (`The Circadian Clock & Period Gene`)? Jean-Jacques d'Ortous de Mairan's 1729 Cupboard Plant, Jürgen Aschoff's 1962 Underground Bunker Volunteers, Seymour Benzer & Ronald Konopka's September 1971 Mutant Fruit Flies, and Jeffrey Hall, Michael Rosbash & Michael Young's 1984–1994 `PER/TIM` Molecular Hourglass (1729–2017)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *The Circadian Clock: The 24-Hour Timer Inside Your Cells* (56 chars)
   - **B (Search question, §1 rule 2):** *How Every Cell in Your Body Tells Time in Pitch Darkness* (56 chars)
   - **Alt (Search / twist question):** *How a Plant in a Dark Cupboard Revealed Your Body's 24-Hour Clock* (65 chars)
2. Review `circadian_script_master_v01.md` (91.9/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# circadian_script_master_v01.md

**Decision:** PASS · **Score:** 91.9 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 8.1 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1469 · Est. min: 9.8 · Chapters: 4

## Cold open excerpt

> How does your body know what time it is when you are locked in pitch darkness with no windows and no clocks? And how did a French astronomer's dark cupboard in seventeen twenty-nine , a Bavarian underground bunker , and three mutant fruit flies in nineteen seventy-one reveal the 

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91.9/100 — proceed to VO after production checklist.

Pass threshold: 90
```
