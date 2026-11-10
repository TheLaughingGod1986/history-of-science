# 070 script v01: notes for review (J0675)

Script: `enzymes_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0675, Gemini Argon, 19 Oct 2026).** Built from `070_Fischer-Buchner-Sumner-Phillips-Enzymes-Catalysts/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-19_J0667.md` (`evidence_2026-10-19_J0667/n_enzymes_catalysts.md` PASS — 6 education videos ≥ 1M views: **Amoeba Sisters *Enzymes (Updated)* (`qgVFkRn8f10`, 7.12M — exact subject match!)**, **TED-Ed ★ *How to speed up chemical reactions (and get a date) - Aaron Sams* (`OttRV5ykP7A`, 2.46M — exact subject match!)**, **RCSB Protein Data Bank (`1.62M` in `public_search.md`)**, **TED-Ed ★ (`SEDabz-hyKo`, 1.52M)**, **FuseSchool *Enzymes | Cells | Biology* (`rlH1ym916Fo`, 1.14M — exact subject match!)**, and **TED-Ed ★ *What triggers a chemical reaction? - Kareem Jarrah* (`8m6RtOpqvtU`, 1.06M — exact subject match!)**, plus **TED-Ed ★ *The chemical reaction that feeds the world* (`o1_D4FscMnU`, 841.1k)**, **Cognito *What are Enzymes?* (`gUncqL1ul8Q`, 685.5k)**, **FuseSchool *Digestive enzymes* (`a0yGDipKWlo`, 529.2k)**, **Khan Academy *Enzymes* (`A90HKrgUOg0`, 332.3k)**, and **TED-Ed ★ *Activation energy: Kickstarting chemical reactions* (`D0ZyjpAin_Y`, 265.2k)**, alongside `public_search.md` & `public_search_titles.md` showing `"how do enzymes work"` as an exact YouTube autocomplete match (`yes`), all 5 top GB search results for `"eduard buchner emil fischer james sumner enzymes"` under 8k views, and both top GB slots for *How Crushed Yeast Proved Life Is Powered by Molecular Locks* under 5k views). The topic isn't locked yet: Chief locks `070` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed — proteins are just passive structural jelly like egg white, so enzymes must be mysterious non-protein chemicals! Wrong! In August nineteen twenty-six, a one-armed chemist who had been told he could never work in a laboratory crystallised the first enzyme in history — and proved it was one hundred percent pure protein!" — where James B. Sumner in August 1926 in *J. Biol. Chem.* crystallised jack-bean `urease` and John Howard Northrop on 20 July 1930 crystallised stomach `pepsin`, defeating Nobel laureate Richard Willstätter's non-protein enzyme dogma) lands in Part 03; Linus Pauling's 1946 transition-state stabilization principle, Daniel Koshland's February 1958 *PNAS* `Induced-Fit Theory`, and David Phillips, Colin Blake, and Louise Johnson's 22 May 1965 *Nature* `2-angstrom` 3D X-ray structure of hen egg-white `lysozyme` land in Part 04; how medicines and poisons work as custom-cut keys (`enzyme inhibitors`) that jam target active sites is explained in Part 05; the ending hands off directly to `071` (*How Does a Soap-Bubble Skin Just Two Molecules Thick Keep Your Cells Alive (`Cell Membranes, the Phospholipid Bilayer, the Sodium-Potassium Pump & Aquaporin Water Channels`)?*), with no goodbye and no subscribe ask. Five VO parts, matching 009–069.

## Marker count (v01)

Run on `enzymes_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked activation-energy & catalytic rate-acceleration chart on period paper comparing uncatalysed vs enzyme-catalysed transition-state barrier (Delta G‡) and showing urease speeding up urea hydrolysis by ~10^14-fold (from ~3,000,000 years uncatalysed to milliseconds) and catalase decomposing 40,000,000 H2O2 molecules per second (0:34); 2) inked Buchner (11 January 1897 Ber. Dtsch. Chem. Ges. 30: 117–124) cell-free yeast press-juice protocol and CO2 evolution table showing 1 kg yeast + 1 kg quartz sand + 200 g kieselguhr pressed at 300 atm -> 500 mL cell-free juice producing grams of CO2 and ethanol with 0 living cells (0:52); 3) inked Fischer (1894 Ber. Dtsch. Chem. Ges. 27: 2985–2993) alpha- vs beta-methyl glucoside stereospecificity chart & Buchner (11 January 1897 Ber. Dtsch. Chem. Ges. 30: 117–124) 300-atmosphere cell-free yeast press-juice CO2/ethanol yield chart on period paper (1:58); 4) inked Sumner (August 1926 J. Biol. Chem. 69: 435–441) octahedral jack-bean urease crystal activity table & Northrop (20 July 1930 J. Gen. Physiol. 13: 739–766) crystalline pepsin solubility/activity proof on period paper showing constant specific enzymatic activity across repeated protein recrystallisations and urease's 10^14-fold catalytic rate acceleration (3:47); 5) inked Koshland (February 1958 PNAS 44: 98–104) Induced-Fit conformational alignment diagram & Blake, Koenig, Mair, North, Phillips & Sarma (22 May 1965 Nature 206: 757–761) 2-angstrom hen egg-white lysozyme 129-amino-acid active-site cleft chart on period paper showing subsites A–F distorting bacterial peptidoglycan sugar ring D into a half-chair transition state between Glu35 and Asp52 (5:32); 6) animated timeline building 1857, 1894 & 11 Jan 1897 · Aug 1926 & 20 Jul 1930 · Feb 1958 & 22 May 1965 (6:48) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) an enzyme lowers the energy mountain a chemical reaction has to climb — like blasting a flat railway tunnel straight through the base of Mount Everest so molecules can zip across in milliseconds instead of waiting millions of years (0:34); 2) squeezing yeast at three hundred atmospheres with sharp quartz sand shreds every living cell wall like glass in a blender — yet when sugar hits the dead juice, the invisible protein machines inside keep right on brewing alcohol and carbon dioxide (0:52); 3) Emil Fischer's lock-and-key discovery showed that a yeast enzyme is as picky as a front-door Yale lock — a right-handed sugar key slides straight in and turns, while its left-handed mirror image can't even enter the keyhole (1:58); 4) Willstätter missed the protein in his diluted enzyme solutions because enzymes are so powerful that a pinch of enzyme too small for a 1920s protein test to spot could still chew through millions of molecules a second (3:47); 5) breaking a sugar chain with lysozyme is like snapping a green stick over your knee — the enzyme's cleft grabs both ends and bends the middle ring into a tight curve until the two chemical claws clip the strained bond with effortless ease (5:32); 6) from a 300-atmosphere yeast press in Munich to an X-ray beam in London, scientists proved that life's chemistry needs no magic vital force — only folded protein machines that bend molecules across the finish line (6:48) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **10** | Hermann Emil Fischer (0:34), Eduard Buchner (0:34), James B. Sumner (0:34), Daniel E. Koshland Jr. (0:34), David C. Phillips (0:34), Wilhelm Kühne (1:28), Richard Willstätter (3:13), John Howard Northrop (3:13), Linus Pauling (4:58), Louise N. Johnson (4:58) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **27** | Munich, 11 January 1897 (0:00), 1894 (0:34), 11 January 1897 (0:34), August 1926 (0:34), February 1958 (0:34), 22 May 1965 (0:34), 1833 (1:28), 1857 (1:28), 1877 (1:28), 1894 (1:28), 11 January 1897 (1:28), 1907 (1:28), 1917 (3:13), August 1926 (3:13), 20 July 1930 (3:13), 1932 (3:13), 1946 (3:13), 1922 (4:58), 1946 (4:58), February 1958 (4:58), 22 May 1965 (4:58), 1857–1965 (6:48), 1895 (7:45), 1 April 1925 (7:45), February 1957 (7:45), 18 February 1972 (7:45), 17 April 1992 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **3** | Dead yeast juice brews alcohol (1:28); Enzymes are pure folded proteins (3:13); Bends sugar rings until they snap (4:58) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (300-atmosphere hydraulic press in Munich crushing yeast and quartz sand into cell-free liquid that bubbles with `CO₂` as a 3D lysozyme cleft snaps a sugar chain), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Fischer's 1894 lock-and-key model, Buchner's 11 January 1897 cell-free `Zymase`, Sumner's August 1926 jack-bean `urease` crystals, Koshland's February 1958 Induced-Fit, and Phillips's 22 May 1965 2-angstrom `lysozyme` structure) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:08 (Part 04 pulling the jaws of the 129-amino-acid lysozyme cleft inward to bend ring D and tap the `Glu35` and `Asp52` wire-cutters).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why Louis Pasteur insisted fermentation could never happen outside a living cell and how Eduard Buchner's attempt to preserve dead yeast juice with kitchen sugar proved Pasteur wrong by accident; Part 02 opens cold on Payen & Persoz (1833), Pasteur's 1857 "living vital force" dogma, and Wilhelm Kühne's 1877 word `enzyme`, tells the story of Emil Fischer's 1894 *Ber. Dtsch. Chem. Ges.* `Lock-and-Key` (*wie Schloss und Schlüssel*) and Eduard Buchner's 11 January 1897 300-atmosphere cell-free yeast press (`Zymase`), and ends on why Germany's most powerful Nobel laureate mocked a one-armed American professor at Cornell in August 1926 when he crystallised an enzyme and found it was 100% pure protein; Part 03 opens cold on the midpoint twist ("Case closed — proteins are just passive structural jelly like egg white, so enzymes must be mysterious non-protein chemicals! Wrong!"), tells the story of one-armed James Sumner's August 1926 *J. Biol. Chem.* octahedral jack-bean `urease` crystals, Richard Willstätter's dilution fallacy, and John Howard Northrop's 20 July 1930 crystalline `pepsin` proof, and ends on why a molecule doesn't just sit inside a rigid keyhole forever and how an enzyme actually breaks a chemical bond; Part 04 opens cold on Linus Pauling's 1946 transition-state principle, explains Daniel Koshland's February 1958 *PNAS* `Induced-Fit` flexible glove model and David Phillips, Colin Blake, and Louise Johnson's 22 May 1965 *Nature* `2-angstrom` X-ray structure of `lysozyme` (`Glu35` and `Asp52` snapping strained sugar ring D), and ends on how a soap-bubble skin just two molecules (`5 nanometres`) thick (`the cell membrane`) keeps all those enzymes inside the cell; Part 05 opens cold on how medicines (`aspirin`, `penicillin`) work by jamming enzyme active sites, and hands off to Ernest Overton (1895), Evert Gorter and François Grendel (1 April 1925), Jens Christian Skou (February 1957), Jonathan Singer and Garth Nicolson (18 February 1972), and Peter Agre (17 April 1992) (`071`).
- **Quirky anecdote before the hard idea:** Eduard Buchner adding kitchen sugar (`sucrose`) as a jam preservative to dead, sand-crushed yeast extract and watching it erupt into fizzy alcohol; James Sumner losing his left arm at 17, being told he could never work in a lab, and crystallising the first enzyme in history with one hand!
- **Rivalry / tension:** Louis Pasteur's "living vital force" vs Eduard Buchner's cell-free `Zymase`; Nobel laureate Richard Willstätter's non-protein catalyst dogma vs one-armed James Sumner's `urease` crystals; rigid keyhole (`Fischer`) vs flexible transition-state vice (`Pauling, Koshland, Phillips`).
- **Misconception explained away:** "Does an enzyme fit its starting molecule like a rigid, comfortable armchair?" — explained via Pauling's transition-state strain, Koshland's Induced-Fit, and Phillips's 2-angstrom `lysozyme` cleft bending sugar ring D to breaking point, plus how drugs act as jamming keys (Part 04 & Part 05).

## For Chief to decide

1. Lock **070 = How Do Enzymes Speed Up the Chemistry of Life a Billion Times (and How Did Crushed Yeast With Zero Living Cells Birth Modern Biochemistry — `Enzymes, Fermentation & the Lock-and-Key Active Site`)? Louis Pasteur's 1857 "Vital Force" Yeast Theory, Emil Fischer's 1894 Lock-and-Key Model, Eduard Buchner's 11 January 1897 Cell-Free Hydraulic Yeast Press (`Zymase`), James B. Sumner's August 1926 Jack-Bean Urease Crystals, and Daniel Koshland & David C. Phillips's 1958–1965 Induced-Fit & X-Ray Lysozyme Structure (1857–1965)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Enzymes: The Molecular Locks That Speed Up Life* (47 chars)
   - **B (Search question, §1 rule 2):** *How Crushed Yeast Proved Life Is Powered by Molecular Locks* (59 chars)
   - **Alt (Search / twist question):** *How Your Cells Speed Up Chemical Reactions a Billion Times* (58 chars)
2. Review `enzymes_script_master_v01.md` (91.6/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# enzymes_script_master_v01.md

**Decision:** PASS · **Score:** 91.6 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 8.7 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 8.6 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1565 · Est. min: 10.4 · Chapters: 4

## Cold open excerpt

> How do your cells speed up chemical reactions a billion times at cool body temperature ? Why do reactions that take milliseconds inside your body take millions of years in a glass beaker — and how did a three-hundred-atmosphere hydraulic press in Munich in January eighteen ninety

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91.6/100 — proceed to VO after production checklist.

Pass threshold: 90
```
