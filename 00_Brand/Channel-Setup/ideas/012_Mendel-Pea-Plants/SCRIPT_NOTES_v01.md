# 012 script v01: notes for review (J0260)

Script: `mendel_script_master_v01.md`.

**Draft only (J0260, Gemini `gemini-agy`, 15 Oct 2026).** Written from `opening_and_outline_v00.md` (J0252). The topic isn't locked yet: Chief locks 012 and the working title first, then Claude or Chief reviews and signs this script off. Every number, name, date, quote, scale and card is TO VERIFY in `SOURCES_v01.md` (rows 1–33) until the Gemini facts pass and Claude's quote check. No VO until then.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Wrong.") lands at about 60%, at the end of Part 03 (~5:00 of ~8:20); the baffling misconception ("Why doesn't everything in your family follow a 3-to-1 box?") is raised and explained away in Part 05; the sign-off hands off to Darwin & evolution (013 candidate), with no goodbye and no subscribe ask. Five VO parts, matching 009, 010 and 011.

## Marker count (v01)

Run on `mendel_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **5** | 1) 28,000 pea plants counter beside the 35×7 m abbey garden plan (0:34); 2) 7,324 seeds filling a 2-litre jar (0:52); 3) timeline starting 1843–1856 beside 34 seed packets (2:35); 4) inked bar chart of 5,474 : 1,850 smooth/wrinkled and 6,022 : 2,001 yellow/green (4:00); 5) timeline completing 1843–1905 with the 35-year gap bracket (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **5** | 1) more plants than a city park rose garden (0:34); 2) enough peas to fill a two-litre jar (0:52); 3) 34 seed packets — enough to line a garden shed shelf (2:35); 4) three smooth for every wrinkled one, a two-kilogram pile (4:00); 5) thirty-five years — longer than a human generation (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **9** | Darwin (0:21), Mendel (0:34), Napp (1:42), Doppler (1:58), Nägeli (5:25), de Vries (7:00), Correns (7:00), Tschermak (7:00), Bateson (7:18) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **17** | Brünn 1856 (0:00), 1850s (0:21), St Thomas's Abbey 1856–1863 (0:34), Vienna 1850 (1:28), Brünn 1843 (1:42), Vienna 1851–1853 (1:58), May 1856 (2:15), Brünn 1854–1856 (2:35), Spring 1856 (3:08), 8 Feb & 8 Mar 1865 (4:45), 1866 (4:45), Munich 1866–1873 (5:25), 1903 (5:45), March 1868 (6:12), 6 Jan 1884 (6:12), Spring 1900 (6:43), 1905 (7:18) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | Failed teacher exam twice (1:28); Tested 34 seed varieties (2:35); Coined "dominant" and "recessive" (4:22); Hawkweed clones its seeds (5:45) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (hand splitting open a pea pod showing 6 smooth golden and 2 wrinkled green peas), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Mendel, 1856–1863, 28,000 pea plants) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 4:22 (Part 03 discovery peak).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on how a farmer's son who failed his exam twice solved the puzzle; Part 02 opens cold in the 1850 Vienna exam room and ends on what happened when he crossed the seven traits; Part 03 opens cold in the spring 1856 garden and ends on the midpoint twist ("Case closed? Wrong."); Part 04 opens cold on the silent 1865 hall and ends on how the world ever found out after his papers were burned; Part 05 opens cold on the 35-year gap and hands off to Darwin in England.
- **Quirky anecdote before the hard idea:** the abbey mice rumour (hedged as "Rumour says") and the sealed tent-like pea flower before the 3:1 ratios and 2×2 grid.
- **Rivalry / debate:** told with back-and-forth portrait cuts between Mendel in Brünn and Carl von Nägeli in Munich (Part 04, 5:25).
- **Misconception explained away:** why human traits like height look blended instead of a neat 3:1 box — polygenic inheritance shown as a dozen small brass sliders adding tiny steps vs a single two-way switch in Mendel's peas (Part 05, 7:38).

## For Chief to decide

1. Lock **012 = Genetics: Gregor Mendel's 28,000 pea plants** (from J0252) and choose the working title:
   - *Genetics: The Monk Who Counted 28,000 Pea Plants* (subject + hook, §1 rule 11; 49 chars)
   - *How a Monk and 28,000 Pea Plants Solved Genetics* (search promise + exact number; 49 chars)
   - *How Mendel's Pea Plants Solved Heredity* (shares TED-Ed's exact words; 39 chars)
2. Review and sign off `mendel_script_master_v01.md` (or ask Claude to review/adjust), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` rows 1–33 and Claude's quote check (`CLAUDE_QUOTE_CHECK_v01.md`) before VO.
3. Confirm whether the after-act hand-off stays pointed at **013 = Evolution (Charles Darwin)** or switches to 006 (*The Willow Tree That Was Made of Air*) if 012 airs before 013 is in production.

## Score (`npm run review:script`)

```text
# mendel_script_master_v01.md

**Decision:** PASS · **Score:** 93.5 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 9 |
| scientificAccuracy | 9.9 |
| emotion | 9.6 |
| escalation | 8.8 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1311 · Est. min: 8.7 · Chapters: 4

## Cold open excerpt

> Why can you have your grandfather's red hair, or your grandmother's green eyes, when neither of your parents has them? And what if the answer to that mystery was found when a monk began to cross garden peas, and was then ignored for thirty-five years? By the end of this film, you

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 93.5/100 — proceed to VO after production checklist.

Pass threshold: 90
```
