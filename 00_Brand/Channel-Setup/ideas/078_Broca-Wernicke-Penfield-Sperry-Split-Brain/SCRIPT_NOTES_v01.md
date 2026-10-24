# 078 script v01: notes for review (J0721)

Script: `split_brain_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0721, Gemini Argon, 20 Oct 2026).** Built from `078_Broca-Wernicke-Penfield-Sperry-Split-Brain/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-20_J0713.md` (`evidence_2026-10-20_J0713/n_split_brain.md` PASS — 25 education videos ≥ 1M views on brain structure, left/right hemispheres, language & neuroscience, led by **TEDx ★ *After watching this, your brain will not be the same | Lara Boyd* (`LNHBMFCzznE`, 46.16M)**, **TEDx ★ *83,000 brain scans* (`esPRsT-lmw8`, 24.36M)**, **TEDx ★ *How to Get Your Brain to Focus* (`Hu4Yvq-g7_Y`, 20.53M)**, **TED-Ed ★ *The benefits of a bilingual brain - Mia Nacamulli* (`MMmOLN5zBLY`, 18.32M — exact left/right hemisphere & Broca/Wernicke language match!)**, **TED-Ed ★ *How playing an instrument benefits your brain - Anita Collins* (`R0JKCYZ8hng`, 15.15M — exact corpus callosum bridge match!)**, **TED ★ *The Brain-Changing Benefits of Exercise | Wendy Suzuki* (`BHY0FxzoKZE`, 12.44M)**, **TED ★ *Your Brain Hallucinates Your Conscious Reality | Anil Seth* (`lyu7v7nWzfo`, 11.96M)**, **TED-Ed ★ *Why are some people left-handed? - Daniel M. Abrams* (`TGLYcYCm2FM`, 11.27M — exact cerebral lateralization match!)**, and **TED-Ed ★ *The left brain vs. right brain myth - Elizabeth Waters* (`ZMSbDwpIyF4`, 1.21M — exact subject match!)**, alongside `public_search.md` & `public_search_titles.md` showing `"left brain vs right brain"` is an exact YouTube autocomplete match (`yes`) and 4 of the top 5 GB search results for `"paul broca wilder penfield roger sperry split brain"` under 545k views). The topic isn't locked yet: Chief locks `078` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; Paul Broca's 18 April 1861 "Tan" discovery (`Broca's area`) and Carl Wernicke's 1874 comprehension area land in Part 02; Fritsch & Hitzig's 1870 contralateral motor cortex proof and Wilder Penfield's December 1937 awake cortical `homunculus` map land in Part 03; the midpoint twist ("Case closed — cutting the two-hundred-million-wire `corpus callosum` bridge between the left and right hemispheres does nothing at all, and psychologists even joked its only job was to stop the two halves of the brain from sagging! Wrong! In nineteen sixty-two at Caltech, Roger Sperry and twenty-two-year-old graduate student Michael Gazzaniga proved that severing that bridge leaves two independent minds inside one human skull!") lands in Part 04; the ending refutes the pop-psychology "left-brained vs right-brained" myth and hands off directly to `079` (*How Do Your Bones Dissolve and Rebuild Your Entire Skeleton Every 10 Years?*), with no goodbye and no subscribe ask. Five VO parts, matching 009–077.

## Marker count (v01)

Run on `split_brain_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked cerebral hemisphere lateralization, Penfield cortical homunculus & Sperry-Gazzaniga split-brain tachistoscope chart on period paper showing Broca's area (left inferior frontal gyrus, 1861), Wernicke's area (left superior temporal gyrus, 1874), the 200-million-axon corpus callosum, and 0.1-second left- vs right-visual-field tachistoscope responses (0:34); 2) inked Gazzaniga, Bogen & Sperry (1962 PNAS 48: 1765–1769) split-brain left vs right visual field verbal naming vs left-hand tactile selection table on period paper (0:52); 3) inked Paul Broca (18 April 1861 Bull. Soc. Anthropol. Paris 2: 235–238 & 1865 Bull. Soc. Anthropol. Paris 6: 377–393) and Carl Wernicke (1874 Der aphasische Symptomencomplex) left-hemisphere language network diagram on period paper (1:58); 4) inked Wilder Penfield & Edwin Boldrey (December 1937 Brain 60: 389–443) motor and sensory cortical homunculus chart on period paper (3:47); 5) inked Gazzaniga, Bogen & Sperry (1962 PNAS 48: 1765–1769 & 1965 Brain 88: 221–236) split-brain lateralized tachistoscope & Left-Brain Interpreter diagram on period paper (5:32); 6) animated timeline building 18 Apr 1861 & 1874 · 1870 & Dec 1937 · 1962–1981 (6:48) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) the corpus callosum bridge connecting the two halves of your brain packs two hundred million nerve fibres into a band the size of a folded thumb — more wiring than all the transatlantic internet cables on Earth combined (0:34); 2) flashing a picture for one-tenth of a second to the left side of a split-brain patient's gaze is like slipping a secret note into the right half of a house after the telephone line to the front door has been cut (0:52); 3) Paul Broca and Carl Wernicke proved that speaking a single sentence is like a two-room telegraph office in the left half of your brain — Wernicke's room writes the message in words, and Broca's room taps it out to your mouth (1:58); 4) on the sensory map inside your brain, your two thumbs and your lips take up more cortical real estate than your entire chest, back, and legs combined — because your brain allocates space by precision, not size (3:47); 5) flashing a secret command to the right half of a split-brain patient's brain and watching the left hand obey while the mouth invents an excuse proved that your left brain has a built-in press secretary that makes up a sensible story whenever it doesn't know why you did something (5:32); 6) from a Paris hospital patient who could only say "Tan" to numbered paper tickets on an awake brain and a 0.1-second flash screen at Caltech, scientists discovered how two hemispheres weave one human mind (6:48) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **10** | Pierre Paul Broca (0:34), Carl Wernicke (0:34), Wilder Graves Penfield (0:34), Roger Wolcott Sperry (0:34), Michael S. Gazzaniga (0:34), Pierre Flourens (1:28), Gustav Fritsch (3:13), Eduard Hitzig (3:13), Edwin Boldrey (3:13), Joseph E. Bogen (4:58) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **25** | Paris, 18 April 1861 (0:00), 18 April 1861 (0:34), 1874 (0:34), December 1937 (0:34), 1962 (0:34), 1967 (0:34), 12 April 1861 (1:28), 17 April 1861 (1:28), 18 April 1861 (1:28), 1865 (1:28), 1874 (1:28), 1870 (3:13), December 1937 (3:13), 1953 (4:58), 15 October 1962 (4:58), 1965 (4:58), 1967 (4:58), 8 December 1981 (4:58), 1861–1981 (6:48), 1736 (7:45), 1739 (7:45), 1866 (7:45), 1873 (7:45), 1892 (7:45), 1922 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **3** | Patient said only "Tan" (1:28); Brain feels zero direct pain (3:13); Left hand knew secret (4:58) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (glowing 1.4-kg human brain split into left and right hemispheres linked by the 200-million-axon corpus callosum beside Sperry and Gazzaniga's 1962 Caltech split-brain spoon test), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Broca 1861 & Wernicke 1874 left-hemisphere language lateralization, Penfield 1937 cortical `homunculus`, and Sperry & Gazzaniga 1962–1967 `split-brain` experiments) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:08 (Part 04 flashing snow and chicken cards across a split tachistoscope desk to trigger the Left-Brain Interpreter).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why 19th-century scientists insisted the two halves of the brain were identical twins and how patient "Tan" in April 1861 proved them wrong; Part 02 opens cold on Pierre Flourens's undivided-cortex dogma, tells the story of Paul Broca's 12–18 April 1861 patient Louis Victor Leborgne ("Tan") and Carl Wernicke's 1874 comprehension area, and ends on how Wilder Penfield in December 1937 mapped the human cortex while his patients were wide awake and chatting with him; Part 03 opens cold on why brain surgery can be performed on awake patients (zero pain receptors in brain tissue itself), explains Fritsch & Hitzig's 1870 bedroom-table motor cortex proof and Penfield & Boldrey's December 1937 `cortical homunculus`, and ends on how Roger Sperry and Michael Gazzaniga in 1962 proved that severing the 200-million-wire `corpus callosum` leaves two separate minds living side by side; Part 04 opens cold on the midpoint twist ("Case closed — cutting the two-hundred-million-wire `corpus callosum` bridge between the left and right hemispheres does nothing at all, and psychologists even joked its only job was to stop the two halves of the brain from sagging! Wrong!"), tells the story of Gazzaniga and Sperry's 0.1-second tachistoscope tests on Patient W.J. and the `Left-Brain Interpreter`, and ends on what this proves about the "left-brained vs right-brained" myth and how the living skeleton (`206 bones`) dissolves and rebuilds itself every 10 years; Part 05 opens cold on why healthy brains use all 200 million fibres of the corpus callosum to unite both hemispheres, and hands off to John Belchier (1736), Duhamel du Monceau (1739), Albert von Kölliker (1873), Karl Culmann & Julius Wolff (1866–1892), and Mellanby, McCollum & Harriette Chick (1919–1922) (`079`).
- **Quirky anecdote before the hard idea:** Leborgne only able to say `"Tan, tan"` for 21 years; Fritsch and Hitzig operating on a bedroom dressing table; Penfield dropping tiny numbered paper tickets onto an awake, talking brain; a split-brain patient's left hand picking up a spoon their mouth swore they never saw, and the left brain inventing a chicken-shed excuse!
- **Rivalry / tension:** Pierre Flourens's holistic cortex dogma vs Paul Broca's left-frontal localization; Karl Lashley's joke that the corpus callosum just stops the brain from sagging vs Roger Sperry and Michael Gazzaniga's 0.1-second tachistoscope proof.
- **Misconception explained away:** "Are some people 'left-brained' (logical) and others 'right-brained' (creative)?" — refuted by Sperry and Gazzaniga's proof that in any healthy brain, 200 million fibres of the corpus callosum integrate both hemispheres every millisecond (Part 05).

## For Chief to decide

1. Lock **078 = Why Does Your Brain Have Two Halves — and What Happened When Scientists Cut the Bridge Between the Left and Right Brain (`Cerebral Hemispheres, Broca's Speech Area, Penfield's Homunculus & Roger Sperry's Split-Brain Experiments`)? Paul Broca's 18 April 1861 "Tan" Patient (`Broca's Area`) & Carl Wernicke's 1874 Comprehension Area, Gustav Fritsch, Eduard Hitzig & Wilder Penfield's 1870–1937 Electrical Motor & Sensory `Homunculus` Map of the Living Human Cortex, and Roger Sperry & Michael Gazzaniga's 1962–1967 `Split-Brain` Corpus Callosum Experiments (1861–1981)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Split Brain: Two Minds Inside One Human Skull* (45 chars)
   - **B (Search question, §1 rule 2):** *What Happened When Scientists Cut the Bridge Between the Left and Right Brain* (77 chars)
   - **Alt (Search / twist question):** *Why Your Brain Has Two Halves and What Happens When They Are Split* (66 chars)
2. Review `split_brain_script_master_v01.md` (91.8/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# split_brain_script_master_v01.md

**Decision:** PASS · **Score:** 91.8 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 8 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1618 · Est. min: 10.8 · Chapters: 4

## Cold open excerpt

> Why is the one-point-four-kilogram brain inside your skull split cleanly down the middle into two halves ? How can your left brain control your right hand and speak your words while your right brain controls your left hand — and what happened in the nineteen sixties when neurosur

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91.8/100 — proceed to VO after production checklist.

Pass threshold: 90
```
