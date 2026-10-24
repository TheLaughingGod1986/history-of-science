# 075 script v01: notes for review (J0705)

Script: `chromosomes_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0705, Gemini Argon, 20 Oct 2026).** Built from `075_Flemming-Boveri-Sutton-Stevens-Morgan-Chromosomes-Mitosis/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-20_J0697.md` (`evidence_2026-10-20_J0697/n_chromosomes_mitosis.md` PASS — 9 education videos ≥ 1M views, ALL 9 strictly on mitosis, meiosis & chromosomes: **Amoeba Sisters *Mitosis: The Amazing Cell Process that Uses Division to Multiply!* (`f-ldPgEfAHI`, 15.32M — exact subject match!)**, **Amoeba Sisters *Mitosis vs. Meiosis: Side by Side Comparison* (`zrKdz93WlVk`, 9.13M — exact subject match!)**, **CrashCourse *Mitosis: Splitting Up is Complicated - Crash Course Biology #12* (`L0k-enzoeOM`, 7.20M — exact Flemming mitosis match!)**, **CrashCourse *Meiosis: Where the Sex Starts - Crash Course Biology #13* (`qCLmR9-YY7o`, 5.47M — exact meiosis & crossing-over match!)**, **Khan Academy *Comparing mitosis and meiosis* (`IQJ4DBkCnco`, 1.95M)**, **Khan Academy *Phases of Meiosis* (`ijLc52LmFQg`, 1.89M)**, **Khan Academy *Phases of Mitosis* (`LLKX_4DHE3I`, 1.69M)**, **Khan Academy *Chromosomes, Chromatids, Chromatin, etc.* (`s9HPNwXd9fk`, 1.64M)**, and **Khan Academy *Mitosis, Meiosis and Sexual Reproduction* (`kaSIjIzAtYA`, 1.21M)**, plus **CrashCourse (`731.8k` & `421.0k`)** and **FuseSchool (`427.7k`)**, alongside `public_search.md` & `public_search_titles.md` showing `"mitosis vs meiosis"` is an exact YouTube autocomplete match (`yes`), and all 5 top GB search results for `"walther flemming theodor boveri thomas hunt morgan fruit fly"` and *How One White-Eyed Fruit Fly Proved Genes Sit on Chromosomes* are under 452k views). The topic isn't locked yet: Chief locks `075` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed — Thomas Hunt Morgan is going to prove that chromosomes have nothing to do with Mendel's genes! Wrong! In May nineteen ten, inside a cramped sixteen-by-twenty-three-foot room at Columbia University stinking of fermented bananas, Morgan stared through a jeweller's lens at a single white-eyed male fruit fly — and proved the very chromosome theory he had spent years attacking!" — where Thomas Hunt Morgan on 22 July 1910 in *Science* discovered that all `782` white-eyed `F₂` fruit flies were male, proving X-chromosome linkage) lands in Part 03; Frans Janssens's 1909 `chiasmata` crossover discovery and 19-year-old Alfred Sturtevant's 1911 / January 1913 *J. Exp. Zool.* first linear genetic map (`confirmed in corn chromosomes by Harriet Creighton and Barbara McClintock in August 1931`) land in Part 04; the ending hands off directly to `076` (*Why Does Your Heart Beat 100,000 Times a Day (Even Outside Your Body) — and How Did a 600-Pound Salt-Bucket Machine & One Wrong Resistor Invent the ECG and Implantable Pacemaker?*), with no goodbye and no subscribe ask. Five VO parts, matching 009–074.

## Marker count (v01)

Run on `chromosomes_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked mitosis vs meiosis chromosome division & Sturtevant linear gene-map chart on period paper showing diploid mitosis (46 chromosomes → 2 identical cells of 46), meiosis (23 homologous pairs crossing over → 4 unique gametes of 23), XX vs XY sex determination, and Sturtevant's 1913 crossover recombination map (1% crossover = 1 map unit / centimorgan across 6 X-linked genes) (0:34); 2) inked Morgan (22 July 1910 Science 32: 120–122) F2 sex-linked cross (2,459 red-eyed females, 1,011 red-eyed males, 0 white-eyed females, 782 white-eyed males) & Sturtevant (January 1913 J. Exp. Zool. 14: 43–59) six-factor linear crossover map on period paper (0:52); 3) inked Walther Flemming (1882 Zellsubstanz, Kern und Zelltheilung) salamander mitosis phases vs Walter Sutton (1903 Biol. Bull. 4: 231–251) grasshopper meiosis reduction division & Nettie Stevens (1905 Carnegie Inst. Wash. Publ. 36) XX/XY sex chromosome karyotype chart on period paper (1:58); 4) inked Thomas Hunt Morgan (22 July 1910 Science 32: 120–122) X-linked white-eye Drosophila cross Punnett diagram & F2 count chart on period paper (3:47); 5) inked Frans Janssens (1909 La Cellule 25: 387–486) meiotic chiasma crossover diagram & Alfred Sturtevant (January 1913 J. Exp. Zool. 14: 43–59) additive linear map of 6 X-linked Drosophila genes on period paper (5:32); 6) animated timeline building 1879–1883 · 1902–1905 · May 1910 – Jan 1913 (6:48) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) packing two metres of DNA into forty-six microscopic chromosomes inside a cell nucleus six micrometres wide is like winding forty kilometres of ultra-fine sewing thread into forty-six neat bobbins inside a walnut shell — and then splitting every bobbin in half without a single knot (0:34); 2) Alfred Sturtevant realized that chromosomes swap pieces at random like two beaded necklaces tangling in a drawer — so if two beads get separated ten times more often than two others, they must sit ten times farther apart along the string (0:52); 3) mitosis is like photocopying a forty-six-volume encyclopaedia so two libraries get the exact same set — while meiosis shuffles your mother's twenty-three volumes with your father's twenty-three volumes to print a brand-new twenty-three-volume edition for every egg or sperm (1:58); 4) because a male only has one X chromosome with no backup copy on his tiny Y chromosome, a recessive mutation on the X chromosome is like flying a single-engine plane — if that one engine sputters, you see it straight away, whereas a female flies with twin X engines (3:47); 5) Alfred Sturtevant mapped invisible genes the way you could map stations on an underground train line with your eyes closed — just by counting how often a random power cut stops the train between any two stations (5:32); 6) from aniline fabric dye on salamander gills in Germany to rotting bananas in New York milk bottles, scientists proved that our entire hereditary blueprint rides on forty-six microscopic threads (6:48) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **9** | Walther Flemming (0:34), Theodor Boveri (0:34), Walter Stanborough Sutton (0:34), Nettie Maria Stevens (0:34), Thomas Hunt Morgan (0:34), Alfred Henry Sturtevant (0:34), Edouard van Beneden (1:28), Frans Alfons Janssens (4:58), Barbara McClintock (4:58) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **28** | New York, May 1910 (0:00), 1879 (0:34), 1902 (0:34), 1903 (0:34), 1905 (0:34), May 1910 (0:34), January 1913 (0:34), 1879 (1:28), 1882 (1:28), 1883 (1:28), 1888 (1:28), 1902 (1:28), 1903 (1:28), 1905 (1:28), 1909 (3:13), May 1910 (3:13), 22 July 1910 (3:13), 1909 (4:58), 1911 (4:58), January 1913 (4:58), August 1931 (4:58), 1933 (4:58), 1879–1933 (6:48), 1956 (7:20), 1882 (7:45), 1901 (7:45), 1906 (7:45), 1958 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **3** | 46 chromosomes in 23 pairs (1:28); All 782 white-eyed flies were male (3:13); First gene map by a 19-year-old (4:58) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (46 crimson-stained chromosomes lining up along a mitotic spindle and zipping into two daughter cells beside one white-eyed male fruit fly in a Columbia milk bottle), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Flemming's 1879 `mitosis`, Boveri & Sutton's 1902–1903 `Chromosome Theory`, Nettie Stevens's 1905 `X` and `Y` sex chromosomes, Morgan's May 1910 white-eyed fly, and Sturtevant's January 1913 first chromosome map) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:08 (Part 04 adding the `1.0%` Yellow–White crossover distance to the `32.7%` White–Miniature distance on a ruler to snap onto `33.7%`).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on how Walther Flemming in 1879 first spotted invisible threads inside a dividing cell and why Thomas Hunt Morgan thought the chromosome theory was wrong; Part 02 opens cold on the transparent cell nucleus mystery, tells the story of Flemming's 1879–1882 dyed salamander mitosis, van Beneden's 1883 meiosis, Boveri & Sutton's 1902–1903 chromosome theory, and Nettie Stevens's 1905 `X` and `Y` chromosomes, and ends on why Morgan started breeding fruit flies in stolen milk bottles to disprove the theory; Part 03 opens cold on the midpoint twist ("Case closed — Thomas Hunt Morgan is going to prove that chromosomes have nothing to do with Mendel's genes! Wrong!"), tells the story of Morgan's May 1910 white-eyed male fruit fly and all `782` white-eyed `F₂` grandchildren turning out male, and ends on why genes on the same chromosome sometimes separated during meiosis and how a 19-year-old undergraduate in 1911 used that clue to draw the first chromosome map; Part 04 opens cold on 19-year-old Alfred Sturtevant pushing his college homework aside in 1911, explains Frans Janssens's 1909 `chiasmata` and Sturtevant's January 1913 *J. Exp. Zool.* linear map (`plus Barbara McClintock's August 1931 maize confirmation`), and ends on why the embryonic heart those genes build beats 100,000 times a day even outside the body; Part 05 opens cold on Tjio & Levan's 1956 human 46-chromosome count and the Human Genome Project, and hands off to Sidney Ringer (1882), Willem Einthoven (1901), Arthur Keith & Martin Flack (1906), and Wilson Greatbatch (1958) (`076`).
- **Quirky anecdote before the hard idea:** Thomas Hunt Morgan breeding fruit flies on mashed bananas in stolen glass milk bottles in a smelly 16-by-23-foot room to *disprove* the chromosome theory; 19-year-old undergraduate Alfred Sturtevant blowing off his homework one night in 1911 to invent genetic mapping!
- **Rivalry / tension:** Sceptic Thomas Hunt Morgan vs the Boveri-Sutton Chromosome Theory (`until his own white-eyed fly converted him into its champion and won him the 1933 Nobel Prize`).
- **Misconception explained away:** "Why aren't all traits on the same chromosome permanently stuck together for ever?" — explained by Frans Janssens's 1909 meiotic `chiasmata` (`crossing over`) and Alfred Sturtevant's 1913 proof that crossover frequency measures linear distance along the chromosome (Part 04).

## For Chief to decide

1. Lock **075 = How Do Your Cells Copy and Shuffle 46 Chromosomes — and How Did One White-Eyed Fruit Fly Map Our Genes (`Chromosomes, Mitosis, Meiosis & Thomas Hunt Morgan's Fly Room`)? Walther Flemming's 1879 Stained Salamander `Mitosis`, Theodor Boveri & Walter Sutton's 1902–1903 `Chromosome Theory of Inheritance`, Nettie Stevens's 1905 `X` and `Y` Sex Chromosomes, Thomas Hunt Morgan's May 1910 White-Eyed Fruit Fly, and 19-Year-Old Alfred Sturtevant's January 1913 First Genetic Map (1879–1933)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Chromosomes: How One White-Eyed Fly Mapped DNA* (46 chars)
   - **B (Search question, §1 rule 2):** *How One White-Eyed Fruit Fly Proved Genes Sit on Chromosomes* (60 chars)
   - **Alt (Search / twist question):** *How Your Cells Copy 46 Chromosomes and Why One Fly Changed Biology* (66 chars)
2. Review `chromosomes_script_master_v01.md` (91.9/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# chromosomes_script_master_v01.md

**Decision:** PASS · **Score:** 91.9 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 8.1 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1739 · Est. min: 11.6 · Chapters: 4

## Cold open excerpt

> How does a single microscopic cell copy two metres of DNA coiled into forty-six chromosomes without tangling a single thread ( mitosis )? How does it shuffle your parents' genes like a deck of cards so you look like a mix of your mother and father yet never identical to your brot

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91.9/100 — proceed to VO after production checklist.

Pass threshold: 90
```
