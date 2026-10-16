# 014 script v01: notes for review (J0364)

Script: `anning_script_master_v01.md` (with `opening_and_outline_v00.md` and `SOURCES_v01.md`).

**Draft only (J0364, Gemini Argon, 16 Oct 2026).** Built from the #1 recommended `014` candidate in today's weekly growth audit (`02_Video-Projects/_analytics/HOS_2026-10-16.md` §5), the neighbour and search evidence in `IDEAS_2026-10-15_J0295.md` (`evidence_2026-10-15_J0295/n_anning.md` PASS — 4 big education videos ≥ 1M views: Natural History Museum *How do dinosaur fossils form?* 5.22M, Be Smart *Are We Living In the Sixth Extinction?* 4.42M, TED-Ed ★ *When will the next mass extinction occur?* 1.78M, Extra History *Mary Anning - Princess of Paleontology* 1.16M — plus `public_search.md` & `public_search_titles.md`), and `VIDEO_BACKLOG.json` (`idea-fossils`). The topic isn't locked yet: Chief locks `014` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–28) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Wrong." — Cuvier suspecting the 35-vertebra *Plesiosaurus* is a forged monster, followed by the 20 February 1824 Geological Society triumph from which Anning herself is barred) lands in Part 04; the popular misconception ("Were Mary Anning's sea dragons swimming dinosaurs?") is raised and explained away in Part 05; the ending hands off directly to `010` (*What Killed the Dinosaurs Was Hidden in a Line of Clay*) / `013` (*Darwin & Wallace*), with no goodbye and no subscribe ask. Five VO parts, matching 009–012.

## Marker count (v01)

Run on `anning_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **5** | 1) 17-foot (5.2 m) ichthyosaur skeleton and 4-foot skull compared against a wooden rowing boat (0:34); 2) inked bone-count comparison of 35 neck vertebrae in *Plesiosaurus* vs 7 in a giraffe (0:52); 3) animated timeline building 1796 · 1800 · 1810 · 1811–1812 beside a £23 coin stack (2:38); 4) inked anatomy diagram of *Ichthyosaurus* (dolphin snout, crocodile teeth, bony eye ring, fish spine, 4 paddles) (3:38); 5) inked Jurassic food chain (belemnite → fish → small ichthyosaur → large ichthyosaur) and completed 1796 → 1847 timeline (7:25) | 3 or more per long, including the animated timeline |
| `SCALE` | **5** | 1) seventeen feet long — longer than a family rowing boat (0:34); 2) five times as many neck bones as a giraffe (0:52); 3) twenty-three pounds — half a year's labourer wages (2:38); 4) eye rings as wide as dinner plates (3:38); 5) 200-million-year-old ink still dark enough to draw with (7:25) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **9** | Mary Anning (0:34), Joseph Anning (0:34), Georges Cuvier (1:28), Richard Anning (2:10), Henry Hoste Henley (4:10), Sir Everard Home (4:10), Thomas Birch (4:38), William Conybeare (5:25), William Buckland (5:25) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **13** | Lyme Regis 1811–1812 (0:00), Late 1700s (0:21), Lyme Regis 1811–1812 (0:34), Paris 1796 (1:28), Lyme Regis 19 August 1800 (1:48), November 1810 (2:38), 1811–1812 (3:08), London 1814 (4:10), 15 May 1820 (4:38), 10 December 1823 (4:58), London 20 February 1824 (5:58), 1824–1829 (6:43), 9 March 1847 (7:25) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | Survived a lightning strike (1:48); Not named in the paper (4:10); Cuvier suspected a forgery (5:25); Fossil ink still wrote (7:05) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (twelve-year-old girl brushing wet shale from a giant stone jawbone and bony eye ring on the Lyme Regis beach), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Mary and Joseph Anning, Lyme Regis 1811–1812, 17-foot skeleton) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:43 (Part 05 coprolite discovery).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on how a Sunday-school reader found what London and Paris professors missed; Part 02 opens cold on Cuvier in Paris (1796) and the 1800 lightning strike, ending on Joseph spotting the 4-foot skull in 1811; Part 03 opens cold on chipping out the 17-foot *Ichthyosaurus* and ends on the 1823 skeleton Cuvier thought was faked; Part 04 opens cold on 10 December 1823 (*Plesiosaurus*) and ends on how Anning worked out what those creatures ate; Part 05 opens cold on cracking open the "bezoar stones" (coprolites) and hands off to the dinosaur extinction mystery (`010`).
- **Quirky anecdote before the hard idea:** baby Mary surviving the 1800 lightning strike that killed three women under an elm tree, and tourists buying "snake-stones" and "devil's fingers", before the comparative anatomy of *Ichthyosaurus* and *Plesiosaurus*.
- **Rivalry / debate:** told with back-and-forth portrait cuts between Georges Cuvier in Paris and William Conybeare & William Buckland in England over whether the 35-vertebra *Plesiosaurus* neck was a fake (Part 04, 5:25).
- **Misconception explained away:** why ichthyosaurs and plesiosaurs were marine reptiles, not swimming dinosaurs (erect pillar legs beneath the hips vs marine flippers, Part 05, 7:50).

## For Chief to decide

1. Lock **014 = Extinction & Fossils: Mary Anning's 17-foot sea dragon at Lyme Regis (1811–1824)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Extinction: The 12-Year-Old Who Dug Up a Sea Dragon* (51 chars)
   - **B (Search question + twist, §1 rule 2):** *How a 12-Year-Old Girl Proved Extinction Is Real* (48 chars)
   - **Alt:** *Fossils: The Sea Monsters That Proved Extinction Is Real* (56 chars)
2. Review `anning_script_master_v01.md` (93.8/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–28) before VO.

## Score (`npm run review:script`)

```text
# anning_script_master_v01.md

**Decision:** PASS · **Score:** 93.8 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 10 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1301 · Est. min: 8.7 · Chapters: 4

## Cold open excerpt

> Why did scientists two hundred years ago believe it was impossible for any kind of animal to go extinct? And what if the secret that proved whole worlds of creatures had vanished forever was chipped out of a crumbling beach cliff by a twelve-year-old girl? By the end of this film

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 93.8/100 — proceed to VO after production checklist.

Pass threshold: 90
```
