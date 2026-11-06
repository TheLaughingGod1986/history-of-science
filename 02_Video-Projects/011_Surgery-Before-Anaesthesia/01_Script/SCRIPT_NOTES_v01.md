# 011 script v01: notes for review (J0183)

Script: `surgery_script_master_v01.md`.

**Draft only (J0183, Cursor on `claude-opus-5-5`, 12 Oct 2026).** Written from `opening_and_outline_v00.md` (J0180). The topic isn't locked yet: Chief locks 011 and the title spelling first, then Claude or Chief reviews and signs this script off. Every number, name, date and card is TO VERIFY in `SOURCES_v01.md` (rows 1–37) until the Gemini facts pass and Claude's quote check. No VO until then.

Structure (Reference lessons 1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Wrong.") lands at about 60%, at the end of Part 03; the scariest idea is raised and explained away in Part 05; the sign-off is the hand-off to 001, with no goodbye and no subscribe ask. Five VO parts, as on 009 and 010.

## Marker count (v01)

Run in this file: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---|---|---|
| DATA | 4: the stopwatch dial (0:10), the timeline starting (2:58), the timeline completing (7:20), the 1-in-100,000 counter (7:40) | 3 of them before 6:30; the timeline is one DATA moment, built across Parts 02–05 | 3 or more, one before any subscribe beat |
| SCALE | 2: boiling an egg (stopwatch), one in a stadium crowd (safety figure) | on the DATA numbers that are big or abstract | every big number gets a scale; the timeline needs none |
| WHO | 10: Liston, Davy, Long, Wells, Morton, Warren, Holmes, Jackson, Simpson, Snow | first mention only (Liston's card is at 0:10, not at 6:33) | one card per named person; Venable, Abbott and Prince Leopold are patients and get no card |
| WHEN | 11 | every spoken date or era; 1842 onward drop onto the one timeline | every date said |
| FACT | 3: used at parties first, a poet named it, the monument names nobody | Parts 02 and 04 | 2–4 |

## Craft checks (Reference lessons 1)

- **Line 1** is the claim with the mystery in it, not "Imagine…". The first concrete answer (ether, Boston, 1846) lands at about 0:22, and the questions the film answers are spoken by about 0:40.
- **Chapter ends:** Part 01 ends on the answer already written down; 02 on "who would show everyone?"; 03 on "Case closed? Wrong."; 04 on Liston about to try it; 05 hands off to Lister and germs (001).
- **Midpoint twist** at the end of Part 03 (~5:00 of ~8:20, about 60%).
- **Rivalry** told with back-and-forth portrait cuts (Part 04, 5:45).
- **Quirky anecdote before the hard idea:** the ether-frolic bruises nobody felt (Part 02), before Long's first operation.
- **Scariest idea explained away:** "Is it safe?" answered with the sourced figure, its scale, and the anaesthetist's watch (Part 05).
- **No gore.** Pain is told through speed, the watch, the straps and the cry in 1845, never shown on a body.

## For Chief to decide

1. Lock 011 (J0180's park) and the title spelling: *Anesthesia* (the neighbour and search word) in the title, *anaesthesia* (UK) in the spoken lines and cards, or one spelling throughout.
2. Warren's and Liston's quotes are spoken as "is said to have". If the Gemini pass finds a primary printed source with the URL, the hedge can go; if it finds nothing, cut the quote and keep the line without it.
3. The safety figure (about 1 in 100,000) and its stadium scale are unverified. If the Royal College of Anaesthetists' figure differs, the line, the counter and the scale change together; the line stays only with a sourced number.
4. The Liston speed: the script says "just a few minutes" and the dial stops short of three. The "28 seconds" figure is not used.

## Score

`npm run review:script`: **PASS 91.1 / 100** (1,246 words, about 8.3 min, structure gates 8/8). The scorer counts the claims table; the spoken lines alone are about 1,210 words.
