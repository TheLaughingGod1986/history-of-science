# 015 script v01: notes for review (J0379)

Script: `hooke_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0379, Gemini Argon, 16 Oct 2026).** Built from `015_Hooke-Cell-Theory/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-16_J0371.md` (`evidence_2026-10-16_J0371/n_hooke.md` PASS — 5 big education videos ≥ 1M views led by **TED-Ed ★ *The wacky history of cell theory* 8.35M**, Amoeba Sisters *Introduction to Cells* 9.93M, Freesciencelessons *Microscopy* 1.38M, Ninja Nerd *Cell Structure and Function* 1.35M, CrashCourse *Eukaryopolis* 6.13M — plus `public_search.md` & `public_search_titles.md` showing wide-open top-5 GB search on `"robert hooke micrographia"` and `"how cells were discovered"`). The topic isn't locked yet: Chief locks `015` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–22) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Wrong." — Schleiden and Schwann's false "sugar crystals in fluid" model versus Robert Remak proving binary cell division in his Berlin Charité attic lab, followed by Rudolf Virchow's 1855 *"Omnis cellula e cellula"* omitting Remak) lands in Part 04; the popular misconception ("Does your body really replace every single cell every seven years?") is raised and explained away in Part 05; the ending hands off directly to `012` (*Gregor Mendel's 28,000 Pea Plants*), with no goodbye and no subscribe ask. Five VO parts, matching 009–014.

## Marker count (v01)

Run on `hooke_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **5** | 1) inked cubic-inch cork diagram showing 1,080 pores/inch and 1,259,712,000 cells/in³ beside a sugar lump (0:34); 2) inked scale comparison of 1.25B cork cells vs ~30 trillion living cells in an adult human body (0:52); 3) inked optical diagram of Hooke's oil-lamp + brine-filled glass globe condenser (~30×–50× magnification) (2:18); 4) inked two-panel explainer contrasting Schleiden & Schwann's false crystal-in-fluid model with Remak's 1→2→4→8→16 binary frog-egg cleavage (4:58); 5) animated timeline building 1665 · 1703 · 1831 · 1838–1839 · 1852 · 1855 (7:12) | 3 or more per long, including the animated timeline |
| `SCALE` | **5** | 1) 1.25 billion cells in a cube the size of a sugar lump (0:34); 2) 30 trillion cells in you — 3,700 times the number of people on Earth (0:52); 3) magnified 50 times — making a flea look as long as a cat (2:18); 4) one cell doubling 45 times — enough to build all 30 trillion cells in an adult human (4:58); 5) 190 years from Hooke's cork slice (1665) to Omnis cellula e cellula (1855) (7:12) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **10** | Robert Hooke (0:34), Samuel Pepys (1:28), Robert Boyle (1:52), Isaac Newton (3:08), Joseph Jackson Lister (4:00), Robert Brown (4:00), Matthias Schleiden (4:28), Theodor Schwann (4:28), Robert Remak (5:28), Rudolf Virchow (6:02) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **17** | London January 1665 (0:00), 1660s (0:21), January 1665 (0:34), London 21 January 1665 (1:28), London 1662 (1:52), 3 March 1703 (3:08), 30 November 1703 (3:08), London 1710 (3:35), 1830 (4:00), 1831 (4:00), Berlin October 1838 (4:28), 1839 (4:28), Berlin 1841–1852 (5:28), 1852 (5:28), April 1855 (6:02), 1858 (6:02), 1665–1855 (7:12) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | Pepys read until 2 a.m. (1:28); Portrait vanished around 1710 (3:35); Barred from a professorship (5:28); Left Remak's name out (6:02) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (penknife shaving a paper-thin slice of bottle cork under Hooke's red-leather microscope and water-globe lens), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Robert Hooke, January 1665, "cells", 1,259,712,000 per cubic inch) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 5:28 (Part 04 Remak's frog-egg cleavage).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why Hooke never realised humans are made of cells and why his portrait vanished; Part 02 opens cold on Samuel Pepys reading *Micrographia* until 2 a.m. on 21 January 1665 and ends on why it took 170 years to see inside living cells; Part 03 opens cold on Hooke's 30-year feud with Isaac Newton and the 1710 missing portrait, ending on how Schleiden and Schwann could be completely wrong about where new cells come from; Part 04 opens cold on the midpoint twist ("Case closed? Wrong." — false sugar-crystal model vs Remak's attic proof and Virchow's 1855 *"Omnis cellula e cellula"*) and ends on tracing the chain of cell divisions back; Part 05 opens cold on the 7-year cell-replacement myth and hands off to Gregor Mendel's 28,000 pea plants (`012`).
- **Quirky anecdote before the hard idea:** Samuel Pepys sitting up until 2 a.m. by candlelight on 21 January 1665 reading *Micrographia* before Hooke's water-globe optical condenser and cubic-inch cell calculation.
- **Rivalry / debate:** two back-and-forth portrait-cut rivalries: Hooke vs Newton in 1703–1710 (3:08), and Robert Remak vs Rudolf Virchow in 1852–1855 (6:02).
- **Misconception explained away:** "Does your body really replace every single cell every seven years?" — gut lining renews in 3–5 days, red blood cells last ~120 days, while cerebral cortex neurons and eye lens cells last for life (Part 05, 6:43).

## For Chief to decide

1. Lock **015 = Cell Theory: Robert Hooke's cork, Robert Remak & how cells divide (1665 → 1855)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Cells: The Slice of Cork That Changed Biology* (45 chars)
   - **B (Search question, §1 rule 2):** *How a Slice of Cork Revealed Every Cell in Your Body* (52 chars)
   - **Alt:** *Why History Forgot the Man Who Discovered How Cells Divide* (58 chars)
2. Review `hooke_script_master_v01.md` (91.4/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–22) before VO.

## Score (`npm run review:script`)

```text
# hooke_script_master_v01.md

**Decision:** PASS · **Score:** 91.4 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.1 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 8 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1411 · Est. min: 9.4 · Chapters: 4

## Cold open excerpt

> Why did scientists three hundred and sixty years ago have no idea what your skin, your blood, or a leaf is actually built out of? And how did a paper-thin shaving of wine-bottle cork reveal a secret shared by every living thing on Earth? By the end of this film, you'll see how a 

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91.4/100 — proceed to VO after production checklist.

Pass threshold: 90
```
