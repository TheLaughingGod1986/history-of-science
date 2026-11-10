# 016 script v01: notes for review (J0396)

Script: `franklin_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0396, Gemini Argon, 16 Oct 2026).** Built from `016_Franklin-DNA-Photo51/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-16_J0388.md` (`evidence_2026-10-16_J0388/n_dna.md` PASS — 11 big education videos ≥ 1M views led by **TED-Ed ★ *Rosalind Franklin: DNA's unsung hero* 1.94M**, TED-Ed ★ *What happens when your DNA is damaged?* 2.75M, TED-Ed ★ *How CRISPR lets you edit DNA* 2.09M, TED ★ *How CRISPR lets us edit our DNA | Jennifer Doudna* 1.94M, TED-Ed ★ *What can DNA tests really tell us about our ancestry?* 1.40M, and CrashCourse *DNA Structure and Replication* 10.66M — plus `public_search.md` & `public_search_titles.md` showing open top-5 GB search on `"rosalind franklin photo 51"` and `"how dna structure was discovered"`). The topic isn't locked yet: Chief locks `016` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–18) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Wrong." — Maurice Wilkins showing Photograph 51 from a drawer on 30 January 1953 without Franklin's permission, followed by Max Perutz handing over the December 1952 MRC report containing Franklin's $C2$ monoclinic crystal symmetry and Jerry Donohue's 27–28 February 1953 keto base-pairing breakthrough) lands in Part 04; the popular misconception ("Was Rosalind Franklin really so opposed to helices that she couldn't read her own photograph?") is raised and explained away in Part 05 with her unpublished manuscript dated 17 March 1953; the ending hands off directly to `017` (*Oxygen & the Phlogiston Myth: Priestley's Bell Jar & Lavoisier's Balance*), with no goodbye and no subscribe ask. Five VO parts, matching 009–015.

## Marker count (v01)

Run on `franklin_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **5** | 1) inked diagram of Photograph 51's X-cross showing 10 rungs per turn, 3.4 Å step rise, 34 Å helix pitch, and 20 Å diameter (0:34); 2) inked comparison of 2 metres of DNA per human cell nucleus vs tens of billions of km across trillions of body cells (0:52); 3) inked two-state humidity diagram showing dry A-DNA (75% relative humidity) stretching by ~25% into wet B-DNA (92% relative humidity) under a 1.54 Å X-ray beam (2:18); 4) inked crystal-symmetry diagram of Franklin's $C2$ monoclinic space group showing two antiparallel backbones running in opposite directions with 3.4 Å rung spacing (5:26); 5) animated timeline building 1869 · 1944 · May 1952 · 30 Jan 1953 · 28 Feb 1953 · 25 Apr 1953 (7:12) | 3 or more per long, including the animated timeline |
| `SCALE` | **5** | 1) 20 ångströms wide — 50,000 times thinner than a human hair (0:34); 2) tens of billions of km of DNA in you — enough to stretch past Pluto and back (0:52); 3) 1.54-ångström X-rays — 3,500 times shorter than green visible light (2:18); 4) 3.4 ångströms between rungs — 3 million rungs stacked in a single millimetre (5:26); 5) 6 billion base-pair letters copied every time one of your cells divides (7:12) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **10** | Rosalind Franklin (0:34), Raymond Gosling (0:34), Maurice Wilkins (1:52), James Watson (3:08), Francis Crick (3:08), Lawrence Bragg (4:02), Linus Pauling (4:28), Max Perutz (5:26), Erwin Chargaff (5:58), Jerry Donohue (5:58) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **18** | London May 1952 (0:00), 1951 (0:21), 2–6 May 1952 (0:34), Paris 1947–1950 (1:28), London January 1951 (1:52), Cambridge November 1951 (3:08), 21 November 1951 (3:35), 28 November 1951 (3:35), January 1953 (4:28), London 30 January 1953 (4:58), February 1953 (5:26), 1950 (5:58), 27–28 February 1953 (5:58), 17 March 1953 (6:43), 25 April 1953 (6:43), 1869–1953 (7:12), 16 April 1958 (7:42), December 1962 (7:42) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | Studied coal before DNA (1:28); Bragg banned their model-building (4:02); Shown without Franklin's permission (4:58); Solved with cardboard cut-outs (5:58) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (X-ray beam passing through a wet DNA fibre in King's College basement to burn Photograph 51's black X beside an uncoiling 3D double helix), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Rosalind Franklin and Raymond Gosling, 2–6 May 1952, Photograph 51, 20 Å wide, 10 rungs per turn) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 5:58 (Part 04 sliding the cardboard Adenine and Thymine cut-outs together on Watson's desk).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why earlier X-ray pictures of DNA were blurry and how two researchers in Cambridge built the molecule backwards; Part 02 opens cold on Rosalind Franklin's 1947–1950 Paris coal research before explaining A-DNA vs B-DNA humidity and ends on why she put Photograph 51 aside; Part 03 opens cold in Cambridge in November 1951 with Watson and Crick's three-stranded inside-out blunder and Linus Pauling's identical January 1953 error, ending on Watson's train trip to London on 30 January 1953; Part 04 opens cold on the midpoint twist ("Case closed? Wrong." — Wilkins opening the drawer on 30 January 1953, Perutz handing over the December 1952 MRC report, and Donohue + Chargaff + cardboard cut-outs on 27–28 February 1953) and ends on why the world thought Franklin had merely confirmed someone else's work; Part 05 opens cold on the "Franklin was anti-helix" myth and her 17 March 1953 manuscript, then hands off to Joseph Priestley's 1774 bell jar and oxygen (`017`).
- **Quirky anecdote before the hard idea:** Franklin spending 1947–1950 in Paris X-raying burnt coal and gas-mask charcoal pores before the 1.54 Å X-ray diffraction and 75% vs 92% relative-humidity A/B-DNA transition.
- **Rivalry / debate:** back-and-forth portrait cuts between Rosalind Franklin at King's College London and James Watson & Francis Crick at the Cavendish Laboratory on 21 and 28 November 1951 (3:35).
- **Misconception explained away:** "Was Rosalind Franklin really so opposed to helices that she couldn't read her own photograph?" — refuted by her unpublished draft manuscript dated 17 March 1953 proving she had independently deduced a two-chain coaxial helix with outer phosphates and 10 units per turn (Part 05, 6:43).

## For Chief to decide

1. Lock **016 = DNA & Photo 51: Rosalind Franklin's 100-hour X-ray & the double helix (May 1952 → April 1953)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *DNA: The 100-Hour X-Ray That Solved the Secret of Life* (54 chars)
   - **B (Search question, §1 rule 2):** *How a Single X-Ray Photograph Revealed the Shape of DNA* (55 chars)
   - **Alt:** *Why Rosalind Franklin Missed the Nobel Prize for DNA* (52 chars)
2. Review `franklin_script_master_v01.md` (92.2/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–18) before VO.

## Score (`npm run review:script`)

```text
# franklin_script_master_v01.md

**Decision:** PASS · **Score:** 92.2 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 8.4 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1504 · Est. min: 10 · Chapters: 4

## Cold open excerpt

> Why did the sharpest minds of the twentieth century have no idea how life copies itself? And how did a single X-ray photograph — exposed for one hundred hours in a damp London basement — reveal the twisted ladder inside every cell of your body? By the end of this film, you'll see

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 92.2/100 — proceed to VO after production checklist.

Pass threshold: 90
```
