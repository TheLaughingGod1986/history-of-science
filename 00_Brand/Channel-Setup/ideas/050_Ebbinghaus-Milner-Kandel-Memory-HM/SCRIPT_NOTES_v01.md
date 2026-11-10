# 050 script v01: notes for review (J0584)

Script: `memory_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0584, Gemini Argon, 18 Oct 2026).** Built from `050_Ebbinghaus-Milner-Kandel-Memory-HM/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-18_J0561.md` (`evidence_2026-10-18_J0561/n_memory_hm.md` PASS — 5 strictly on-topic memory education videos ≥ 1M views: **TED-Ed ★ *What happens when you remove the hippocampus? - Sam Kean* (`KkaXNvzE4pk`, 5.11M — exact Patient H.M. match!)**, **CrashCourse *How We Make Memories: Crash Course Psychology #13* (`bSycdIx-C48`, 4.52M)**, **Kurzgesagt *How Are Memories Stored Inside Your Brain?* (`PqtggjVAi8M`, 3.40M)**, **TED-Ed ★ *How memories form and how we lose them - Catharine Young* (`yOgAbKJGrTA`, 3.24M — exact subject match!)**, and **TED-Ed ★ *Are all of your memories real? - Daniel L. Schacter* (`D-2p86FvqF4`, 2.21M)**, plus **SciShow *How Do You Make Memories?* (`Pq0aQAG0A3o`, 458.5k)**, alongside `public_search.md` showing 4 of the top 5 GB search results for `"patient hm henry molaison brenda milner memory"` under 163k views and 3 of the top 5 GB slots for *How a Man Who Forgot Every 30 Seconds Proved You Have Two Different Memories* under 570k views). The topic isn't locked yet: Chief locks `050` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed — had the surgery destroyed Henry's ability to learn anything new? Wrong! In nineteen fifty-five to nineteen fifty-seven, British-Canadian neuropsychologist Brenda Milner sat at Henry's table with a clever test, published in nineteen fifty-seven and nineteen sixty-two" — Patient H.M. reducing his mirror-star errors from ~30 to near zero over three days while swearing he had never seen the apparatus, proving conscious declarative memory in the hippocampus is separate from motor procedural memory in the basal ganglia and cerebellum) lands in Part 03; Tim Bliss and Terje Lømo's 1966–1973 hippocampal Long-Term Potentiation (`LTP`) and Eric Kandel and Craig Bailey's 1983–2000 discovery in *Aplysia* sea slugs that spaced training activates `CREB` to double physical synaptic terminals from ~1,300 to ~2,600 lands in Part 04; the all-night cramming misconception ("Many people still believe cramming for hours straight the night before an exam is the best way to lock facts into your head") is raised and explained away in Part 05 via short-term chemical facilitation vs spaced-repetition `CREB` structural synapse growth; the ending hands off directly to `051` (*Why Do Chilis Burn & Peppermints Feel Freezing Cold? Wilbur Scoville's 1912 Sugar-Water Taste Test & David Julius and Ardem Patapoutian's 1997–2002 Capsaicin `TRPV1` & Menthol `TRPM8` Ion Channels*), with no goodbye and no subscribe ask. Five VO parts, matching 009–049.

## Marker count (v01)

Run on `memory_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked Ebbinghaus forgetting curve & Milner 3-day mirror-drawing error chart on period paper showing nonsense-syllable retention dropping to 42% after 20 minutes, 33% after 24 hours, and 25% after 6 days (Ebbinghaus 1885), juxtaposed with Patient H.M.'s mirror-star errors plummeting from ~30 on Day 1 to <3 on Day 3 while declarative recall stayed at 0% (Scoville & Milner 1957; Milner 1962) (0:34); 2) inked synaptic plasticity bar chart comparing short-term memory (0 new terminals, temporary cyclic-AMP/glutamate boost lasting minutes) against long-term memory (CREB-driven gene expression doubling physical synaptic terminals from ~1,300 to ~2,600 per sensory neuron) (0:52); 3) inked Ebbinghaus forgetting vs spaced-repetition curve on period paper from Hermann Ebbinghaus (1885, Über das Gedächtnis) showing exponential memory decay (58% lost at 20 min, 66% at 1 day, 75% at 6 days, 79% at 31 days) vs step-wise relearning savings that flatten decay into permanent storage (1:58); 4) inked 3-day mirror-drawing learning curve on period paper from Brenda Milner (1962, Physiologie de l'Hippocampe, & Scoville & Milner 1957 J. Neurol. Neurosurg. Psychiatry 20: 11–21) showing Patient H.M.'s error score dropping across 30 trials over 3 days from ~30 line-crossings on Trial 1 to <3 on Day 3 while conscious recognition of the apparatus remained 0% (3:42); 5) inked short-term vs long-term synaptic architecture diagram on period paper from Eric Kandel & Craig Bailey (1983 Science 220: 91–93 & 2000 Nobel Lecture) showing 1 training pulse causing temporary cAMP/glutamate enhancement across 1,300 existing terminals (short-term memory, minutes) vs 4–5 spaced training pulses activating CREB gene transcription to grow ~2,600 physical terminals (long-term memory, weeks) (5:28); 6) animated timeline building 1885 · 25 Aug 1953 & 1957 · 1966–1973 · 1983–2000 alongside the short-term cramming chemical spike vs spaced-repetition CREB structural growth comparison (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) without review, your brain throws away more than half of a new list within the first hour — yet a motor skill learned by your hands can survive for decades even if your hippocampus is completely gone (0:34); 2) a sea slug has only twenty thousand nerve cells compared with your eighty-six billion — yet every time you turn a short-term thought into a lifelong memory, your brain cells physically sprout twice as many microscopic branches (0:52); 3) within twenty minutes of cramming a new list, more than half of it has already evaporated from your brain — unless you reset the curve with spaced review (1:58); 4) for fifty-five years, Henry Molaison lived inside a thirty-second sliding window of the present — yet his hands learned new skills as smoothly as yours (3:42); 5) learning something for the rest of your life literally changes the physical anatomy of your brain — sprouting twice as many microscopic bridges between the nerve cells that carry that memory (5:28); 6) by the time you finish watching this nine-minute film, the neurons inside your hippocampus have already begun firing the genetic switches to wire these stories into physical branches inside your brain (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **10** | Hermann Ebbinghaus (0:34), William Beecher Scoville (0:34), Brenda Milner (0:34), Henry Molaison (0:34), Tim Bliss (0:34), Terje Lømo (0:34), Eric Kandel (0:34), Karl Lashley (1:28), Donald Hebb (4:53), Craig H. Bailey (4:53) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **25** | Hartford Connecticut 1955–1957 (0:00), 1955–1957 (0:21), 1885 (0:34), 25 August 1953 (0:34), 1957 (0:34), 1966–1973 (0:34), 2000 (0:34), 1879–1885 (1:28), 1885 (1:28), 1920–1950 (1:28), 1950 (1:28), 25 August 1953 (3:08), 1955–1957 (3:08), 1957 (3:08), 1962 (3:08), 2008 (3:08), 1949 (4:53), 1966 (4:53), 1973 (4:53), 1983 (4:53), 2000 (4:53), 1885–2000 (6:43), May 1912 (7:45), 23 October 1997 (7:45), 2002 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **3** | 2,300 nonsense syllables (1:28); Swore he'd never seen it (3:08); 20,000 giant slug neurons (4:53) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (Brenda Milner holding a metal screen over Henry Molaison's hand as he traces a five-pointed star in a mirror alongside the missing hippocampus and giant sea-slug neurons doubling their synaptic terminals), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Hermann Ebbinghaus's 1885 Forgetting Curve from 2,300 nonsense syllables, William Scoville's 25 August 1953 surgery and Brenda Milner's 1957 Patient H.M. mirror-star proof of separate declarative and motor memories, and Bliss, Lømo, and Eric Kandel's 1966–2000 proof that long-term memory doubles synaptic connections) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:05 (Part 04 tapping the nuclear `CREB` genetic blueprint desk with five spaced beats to sprout a second bridge of glowing synaptic terminals from 1,300 to 2,600).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why a 30-year-old philosopher in Berlin locked himself in a room to memorise 2,300 gibberish words and why another scientist spent 30 years slicing rat brains without finding a single memory; Part 02 opens cold on why philosophers before 1879 claimed memory couldn't be measured, then tells the story of Hermann Ebbinghaus's 1879–1885 metronome tests on 2,300 nonsense syllables (`WID, ZOF, KAX`), the Forgetting Curve, spaced repetition, and Karl Lashley's 1920–1950 rat-maze hunt, ending on what happened on 25 August 1953 when a surgeon removed two seahorse-shaped ridges from Patient H.M.; Part 03 opens cold on Henry Molaison's 25 August 1953 operation and his 30-second sliding memory window, delivers the midpoint twist ("Case closed — had the surgery destroyed Henry's ability to learn anything new? Wrong!" — Brenda Milner's 1955–1957 three-day mirror-star test proving declarative hippocampus memory is separate from motor skill memory), and ends on how a fleeting electrical spark between two brain cells turns into a physical trace that lasts 80 years; Part 04 opens cold on Donald Hebb's 1949 rule and Tim Bliss and Terje Lømo's 1966–1973 hippocampal Long-Term Potentiation, then explains Eric Kandel and Craig Bailey's 1983–2000 *Aplysia* sea-slug experiments proving spaced training activates `CREB` to double physical synaptic terminals from 1,300 to 2,600, ending on why cramming all night before an exam fails; Part 05 opens cold on the all-night cramming misconception, explains short-term chemical facilitation vs spaced `CREB` structural growth, and hands off to Wilbur Scoville's May 1912 16,000,000-drop chili test and David Julius and Ardem Patapoutian's 1997–2002 `TRPV1` and `TRPM8` thermometer doors (`051`).
- **Quirky anecdote before the hard idea:** Hermann Ebbinghaus sitting alone in Berlin reciting 2,300 gibberish syllables (`WID, ZOF, KAX`) to a 150-bpm metronome for six years, and Henry Molaison looking at the mirror-star puzzle on Day 3, swearing he had never seen it in his life, and then tracing it almost flawlessly while saying *"Well, this is strange — I thought that would be difficult, but it looks as if I've done it well!"*
- **Rivalry / tension:** Karl Lashley's 1950 conclusion that no localized brain structure controls memory vs Scoville and Milner's 1953–1957 hippocampus proof; single-memory-system dogma vs Milner's dual declarative/procedural proof.
- **Misconception explained away:** "Many people still believe cramming for hours straight the night before an exam is the best way to lock facts into your head" — explained via short-term neurotransmitter facilitation vs spaced-repetition `CREB` protein synthesis and double-synapse growth (Part 05, 6:43).

## For Chief to decide

1. Lock **050 = How Do Memories Form & Why Do We Forget? Hermann Ebbinghaus's 1885 2,300 Nonsense Syllables (`The Forgetting Curve`), Brenda Milner & Patient H.M.'s 1953–1957 Mirror-Star Test (`Hippocampus`) & Eric Kandel's Sea-Slug Synapses (1885–2000)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Memory & Forgetting: The Man Who Lived in 30-Second Loops* (57 chars)
   - **B (Search question, §1 rule 2):** *How a Man Who Forgot Every 30 Seconds Proved You Have Two Different Memories* (76 chars)
   - **Alt (Search / twist question):** *Why Patient H.M. Could Master a Mirror Star He Swore He Had Never Seen* (70 chars)
2. Review `memory_script_master_v01.md` (92.2/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# memory_script_master_v01.md

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

Words: 1588 · Est. min: 10.6 · Chapters: 4

## Cold open excerpt

> Why can you still ride a bicycle after twenty years without thinking about it, yet forget a stranger's name thirty seconds after hearing it? And how did a twenty-seven-year-old man who lost the ability to form any new conscious memories on the twenty-fifth of August nineteen fift

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 92.2/100 — proceed to VO after production checklist.

Pass threshold: 90
```
