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

`npm run review:script`: **PASS 91.1 / 100** (1,246 words on v01; **1,259 words on locked `surgery_script_master_v02.md`**, about 8.4 min, structure gates 8/8). The scorer counts the claims table; the spoken lines alone are about 1,210 words.

## Nov 2026 `HOS-2026-11-E2` (`J2204`) First-30s Proof-First + Early DATA/SCALE Verification (`J2239`, 5 Nov 2026)

Checked `surgery_script_master_v02.md` against Chief h47 experiment `HOS-2026-11-E2` (`J2204`) with **zero spoken word changes** (preserving `J0224` Claude primary-source quote check lock at `91.1/100 PASS`):

1. **Locked first-minute milestones preserved:**
   - **Answer image (`<=0:05`):** `0:00` steep wooden operating theatre in London, surgeon in dark frock coat checking brass pocket watch (`WHEN: London, 1840s · LABEL: THE FASTEST KNIFE`).
   - **Title question (`<=0:08`):** *"Before eighteen forty-six, the best surgeon in the world was simply the fastest one. Why?"* (`~0:06`).
   - **Promise (`<=0:15`):** *"Because the patient was awake for every second of it, and in Europe and America, nobody knew how to stop the pain."* (`~0:14.5`).
   - **Stakes (`<=0:25`) & First real fact (`<0:45`):** *"In London, one surgeon was famous for his speed. His students timed him with their pocket watches, and he could take off a leg in just a few minutes."* (`~0:14.5–0:26.0`, followed by Boston Ether Dome on 16 October 1846 at `~0:26.0–0:39.0`).
2. **Rule 1 — Sub-4.5s visual cuts across `0:00–0:30` (`>=7` distinct moving plates; zero holds `>4.5s`):**
   - **Cut 1 (`0:00.0–0:03.5`, `3.5 s`):** Steep wooden London operating theatre lit by tall windows; surgeon in dark frock coat checks brass pocket watch and looks up (`ANSWER IMAGE by 0:03 · WHEN: London, 1840s · LABEL: THE FASTEST KNIFE`).
   - **Cut 2 (`0:03.5–0:07.5`, `4.0 s`):** Immediate physical apparatus — macro close-up on the surgeon's open brass pocket watch ticking beside the instrument tray (`title question by 0:06`).
   - **Cut 3 (`0:07.5–0:11.5`, `4.0 s`):** Immediate physical apparatus — close on the wooden operating chair in window light, leather straps hanging from the armrests (`no exterior hospital shot`).
   - **Cut 4 (`0:11.5–0:15.5`, `4.0 s`):** Immediate physical proof apparatus — two-necked glass ether inhaler globe glinting on a mahogany table beside its glass stopper (`promise by 0:15`).
   - **Cut 5 (`0:15.5–0:19.5`, `4.0 s`):** Robert Liston striding to the wooden table in his dark frock coat (`WHO: Robert Liston (1794–1847) — London surgeon`).
   - **Cut 6 (`0:19.5–0:23.5`, `4.0 s`):** Close on a row of medical students leaning over the gallery rail clicking open pocket watches one after another (`stakes by 0:23`).
   - **Cut 7 (`0:23.5–0:27.5`, `4.0 s`):** First animated `DATA` + `SCALE` graphic (`0:25–0:40` window): animated brass stopwatch dial on period paper sweeping round once and stopping short of three minutes (`DATA: a brass stopwatch dial that sweeps round once and stops short of three minutes · SCALE: about as long as boiling an egg`).
   - **Cut 8 (`0:27.5–0:31.5`, `4.0 s`):** Boston Ether Dome under the skylight; dentist William Morton holding the glass ether globe to young Edward Abbott's mouth as his eyes close (`FIRST CONCRETE ANSWER by 0:30 · WHEN: Boston, 16 October 1846 · LABEL: ETHER`).
3. **Rule 2 — Immediate physical proof/apparatus at `0:05–0:15` (not exterior establishing):** PASS — Cuts 2–4 (`0:03.5–0:15.5`) show the open brass pocket watch, the strapped wooden operating chair, and the two-necked glass ether inhaler globe inside the theatre; zero exterior building shots.
4. **Rule 3 — First animated `DATA` + `SCALE` graphic between `0:25–0:40`:** PASS — Cut 7 (`0:23.5–0:27.5` / `0:25–0:31` on the VO clock) animates the brass stopwatch dial (`DATA`) + `"about as long as boiling an egg"` (`SCALE`, verified in `FACT_NOTES_v01.md` rows 16 & 37).
