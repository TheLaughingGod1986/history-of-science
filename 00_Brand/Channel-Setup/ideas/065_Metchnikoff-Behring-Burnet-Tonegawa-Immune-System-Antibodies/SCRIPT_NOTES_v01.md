# 065 script v01: notes for review (J0660)

Script: `immune_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0660, Gemini Argon, 19 Oct 2026).** Built from `065_Metchnikoff-Behring-Burnet-Tonegawa-Immune-System-Antibodies/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-19_J0637.md` (`evidence_2026-10-19_J0637/n_immune_antibodies.md` PASS — 11 education videos ≥ 1M views, ALL 11 strictly on the immune system, antibodies, B-cells & T-cells: **Kurzgesagt – In a Nutshell *The Immune System Explained I – Bacteria Infection* (`zQGOcOUBi6s`, 54.64M — exact subject match!)**, **Kurzgesagt *How The Immune System ACTUALLY Works – IMMUNE* (`lXfEK8G8CUI`, 26.15M — exact subject match!)**, **CrashCourse *Immune System, Part 1: Crash Course Anatomy & Physiology #45* (`GIJK3dwCWCw`, 7.13M — exact subject match!)**, **TED-Ed ★ *How does your immune system work? - Emma Bryce* (`PSRJfaAYkW4`, 5.20M — exact subject match!)**, **CrashCourse *Immune System, Part 2: Crash Course Anatomy & Physiology #46* (`2DFN4IBZ3rI`, 4.28M — exact antibody/humoral match!)**, **TED-Ed ★ *How do vaccines work? - Kelwalin Dhanasarnsombut* (`rb7TVW77ZCs`, 3.54M)**, **CrashCourse *Immune System, Part 3: Crash Course Anatomy & Physiology #47* (`rd2cf5hValM`, 3.26M — exact T-cell match!)**, and **Khan Academy *Types of immune responses: Innate and adaptive, humoral vs. cell-mediated* (`rp7T4IItbtM`, 2.09M)**, alongside `public_search.md` & `public_search_titles.md` showing `"how does the immune system work"` triggering exact YouTube autocomplete, all 5 top GB search results for `"macfarlane burnet susumu tonegawa antibodies clonal selection"` under 45k views, and 3 of the top 5 GB slots for *How Your Immune System Recognises a Billion New Invaders* under 287k views). The topic isn't locked yet: Chief locks `065` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed — an antibody must be a soft lump of protein clay that wraps itself around an invader to take its shape! Wrong! Every single antibody lock is already built before the invader ever enters your body!" — where Frank Macfarlane Burnet in October 1957 proposed the Clonal Selection Theory, proven by Gustav Nossal and Joshua Lederberg on 17 May 1958 in *Nature* across 456 single-cell microdroplets) lands in Part 03; Susumu Tonegawa and Nobumichi Hozumi's October 1976 Basel restriction-enzyme proof that developing B-cells cut, shuffle, and splice modular `V`, `D`, and `J` gene segments (`V(D)J recombination`) to build >10 billion antibodies from ~20,000 genes lands in Part 04; the "why can you still catch a cold or the flu twice if memory cells last for life?" misconception is raised and explained away in Part 05 via RNA virus surface coat mutation (`antigenic drift`); the ending hands off directly to `066` (*How Did Scientists Discover That Cancer Comes From Our Own Genes With a Stuck Accelerator or Broken Brakes (`Oncogenes, Tumour Suppressors & p53`)? Peyton Rous's 21 January 1911 Chicken Sarcoma Virus, Alfred Knudson's April 1971 "Two-Hit" Retinoblastoma Equation, J. Michael Bishop & Harold Varmus's March 1976 Discovery of `src` Proto-Oncogenes Inside Normal DNA, and David Lane, Arnold Levine & Lloyd Old's May 1979 Discovery of `p53` ("The Guardian of the Genome")*), with no goodbye and no subscribe ask. Five VO parts, matching 009–064.

## Marker count (v01)

Run on `immune_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked human genome vs antibody diversity chart on period paper comparing ~20,000 total human protein-coding genes against >10,000,000,000 (10^10) unique B-cell antibody locks created by shuffling ~40 V, 23 D, and 6 J heavy-chain gene segments with light-chain V-J segments and random junctional nucleotides (0:34); 2) inked clonal selection & antibody titre curve showing a 5–10 day primary lag phase as 1 matching B-cell divides into thousands of plasma cells (~2,000 antibodies/cell/second) and memory B-cells that trigger an immediate, 100-fold higher IgG surge upon second exposure (0:52); 3) inked Metchnikoff cellular phagocytosis (1882–1884) vs Behring & Kitasato humoral antitoxin serum protection (4 December 1890) & Ehrlich side-chain lock-and-key chart on period paper comparing fast, non-specific innate phagocytes (hours) against specific adaptive serum antibodies (days to weeks, conferring lifelong immunity) (1:58); 4) inked Burnet (October 1957, Aust. J. Sci. 20: 67–69) and Nossal & Lederberg (17 May 1958, Nature 181: 1419–1420) single-cell microdroplet antibody chart on period paper comparing Pauling's 1940 instructional model vs Nossal & Lederberg's 456 single-cell microdroplets (100% monospecific) (3:42); 5) inked Hozumi & Tonegawa (October 1976, PNAS 73: 3628–3632) somatic V(D)J recombination chart on period paper showing embryonic germline DNA vs rearranged adult B-cell DNA, multiplying ~40 VH × 23 DH × 6 JH × light-chain Vκ/λ-Jκ/λ × junctional additions into >10^10 unique antibodies (5:28); 6) animated timeline building Dec 1882 & 4 Dec 1890 · Oct 1957 & May 1958 · Oct 1976 (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) if every one of your twenty thousand human genes were a single book, your immune system couldn't fill a small town library — yet by cutting and shuffling sentences from just a few dozen pages like a slot machine, your white blood cells print ten billion different security passcodes (0:34); 2) once the right B-cell meets its matching virus, it clones itself into an army of factories where each single cell fires out two thousand Y-shaped antibody missiles every single second (0:52); 3) your immune system fights with two armies at once — front-line phagocyte cells that swallow any stranger on sight within minutes, and custom-built antibody missiles that lock onto one exact target with pinpoint precision (1:58); 4) instead of waiting for a burglar to show up and moulding a lock around his key, your body pre-builds a hundred million different locks before you are even born and waits to see which door the burglar tries (3:42); 5) with just three modularity reels — V, D, and J — plus random letters inserted at the joints, your DNA works like a combination lock where a few dozen dials can dial up ten billion different numbers (5:28); 6) from a Christmas rose thorn in a Sicilian starfish to a genetic slot machine in Switzerland, a century of discovery explained how twenty thousand human genes guard you against a universe of unseen invaders (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **9** | Élie Metchnikoff (0:34), Emil von Behring (0:34), Shibasaburo Kitasato (0:34), Frank Macfarlane Burnet (0:34), Susumu Tonegawa (0:34), Nobumichi Hozumi (0:34), Paul Ehrlich (1:28), Gustav J. V. Nossal (3:08), Joshua Lederberg (3:08) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **23** | Messina, December 1882 (0:00), December 1882 (0:34), 4 December 1890 (0:34), October 1957 (0:34), October 1976 (0:34), December 1882 (1:28), 1884 (1:28), 4 December 1890 (1:28), 1900 (1:28), 1908 (1:28), 1917 (1:28), 1940 (3:08), 1955 (3:08), October 1957 (3:08), May 1958 (3:08), 1965 (4:53), October 1976 (4:53), 1987 (4:53), 1882–1976 (6:43), 21 January 1911 (7:45), April 1971 (7:45), March 1976 (7:45), May 1979 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **3** | Soldier cells vs liquid antibodies (1:28); One cell, one pre-made antibody (3:08); Immune cells shuffle their own DNA (4:53) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (millions of B-cells in a lymph node displaying unique Y-shaped antibody locks until a spiked virus hits matching B-cell #84,102,391, zooming inside its nucleus where modular V, D, and J gene segments shuffle like a three-reel slot machine), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Metchnikoff's December 1882 phagocytes, Behring & Kitasato's 4 December 1890 antitoxin antibodies, Burnet's October 1957 Clonal Selection Theory, and Tonegawa & Hozumi's October 1976 `V(D)J recombination` generating >10 billion locks from ~20,000 genes) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:05 (Part 04 snipping and clicking modular V-14, D-7, and J-3 gene cards together).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on what happened in Sicily at Christmas in 1882 when Élie Metchnikoff pushed a rose thorn into a transparent starfish larva; Part 02 opens cold on the 2,000-year mystery of plague immunity, tells the story of Metchnikoff's December 1882 rose-thorn phagocytes vs Behring and Kitasato's 4 December 1890 cell-free diphtheria antitoxin serum and Paul Ehrlich's 1900 lock-and-key receptors, and ends on Karl Landsteiner's 1917 synthetic-chemical puzzle and Linus Pauling's 1940 clay theory; Part 03 opens cold on the midpoint twist ("Case closed — an antibody must be a soft lump of protein clay that wraps itself around an invader to take its shape! Wrong!"), tells the story of Frank Macfarlane Burnet's October 1957 Clonal Selection Theory and Gustav Nossal and Joshua Lederberg's May 1958 456-single-cell microdroplet proof, and ends on how 20,000 human genes can pre-build 10 billion different antibody proteins; Part 04 opens cold on William Dreyer and Claude Bennett's 1965 two-gene heresy, explains Susumu Tonegawa and Nobumichi Hozumi's October 1976 Basel discovery of somatic `V(D)J recombination` (`1987 Nobel Prize`), and ends on why you can still catch a cold again next winter and what happens when your own cells refuse to stop dividing; Part 05 opens cold on why colds and flu return despite lifelong memory cells (`antigenic drift`), and hands off to Peyton Rous (21 January 1911), Alfred Knudson (April 1971), Michael Bishop & Harold Varmus (March 1976), and `p53` (May 1979) (`066`).
- **Quirky anecdote before the hard idea:** Élie Metchnikoff plucking a rose thorn from his children's Christmas tangerine tree while his family went to see performing apes at a circus in Messina; Gustav Nossal and Joshua Lederberg trapping 456 individual white blood cells inside microscopic oil droplets!
- **Rivalry / tension:** Metchnikoff's Russian/French cellular immunity school (`phagocytes`) vs Behring, Kitasato & Koch's German humoral school (`serum antibodies`); Linus Pauling's 1940 Instructional Template clay model vs Burnet's 1957 Clonal Selection Theory; invariant genome dogma vs Tonegawa's DNA-shuffling B-cells.
- **Misconception explained away:** "If memory cells remember every invader for life, why can you catch a cold or the flu again every winter?" — explained via rapid RNA virus surface-coat mutations (`antigenic drift`) vs stable measles coats (Part 05, 6:43).

## For Chief to decide

1. Lock **065 = How Does Your Immune System Recognise a Billion Invaders It Has Never Seen Before (`Phagocytes, Antibodies, Clonal Selection & V(D)J Recombination`)? Élie Metchnikoff's December 1882 Rose-Thorn Starfish Larva (`Phagocytes`), Emil von Behring & Shibasaburo Kitasato's 4 December 1890 Diphtheria Antitoxin (`Antibodies`), Frank Macfarlane Burnet's October 1957 Clonal Selection Theory, and Susumu Tonegawa's October 1976 Genetic Slot-Machine Proof (`V(D)J Recombination`) (1882–1976)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *The Immune System: How Your DNA Builds a Billion Locks* (54 chars)
   - **B (Search question, §1 rule 2):** *How Your Immune System Recognises a Billion New Invaders* (56 chars)
   - **Alt (Search / twist question):** *How 20,000 Human Genes Build 10 Billion Different Antibodies* (60 chars)
2. Review `immune_script_master_v01.md` (91.8/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# immune_script_master_v01.md

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

Words: 1543 · Est. min: 10.3 · Chapters: 4

## Cold open excerpt

> How can your immune system build ten billion different custom-fitted antibodies when your entire human genome contains only twenty thousand genes ? And how did a rose thorn in a starfish larva in December eighteen eighty-two , an Australian virologist in October nineteen fifty-se

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91.8/100 — proceed to VO after production checklist.

Pass threshold: 90
```
