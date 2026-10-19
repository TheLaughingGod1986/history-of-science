# 067 script v01: notes for review (J0660)

Script: `embryo_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0660, Gemini Argon, 19 Oct 2026).** Built from `067_Driesch-Mangold-Spemann-Lewis-Gehring-Embryo-Hox-Genes/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-19_J0652.md` (`evidence_2026-10-19_J0652/n_embryo_hox_genes.md` PASS — 4+ education videos ≥ 1M views: **TED-Ed ★ *The genes you don't get from your parents (but can't live without) - Devin Shuman* (`0obYR-nf45I`, 2.49M)**, **TED-Ed ★ *What are stem cells? - Craig A. Kohn* (`evH0I7Coc54`, 2.33M)**, **Amoeba Sisters *How Cells Become Specialized [Featuring Stem Cells]* (`t3g26p9Mh_k`, 1.38M — exact cell differentiation match!)**, and **TED-Ed ★ *Where do genes come from? - Carl Zimmer* (`z9HIYjRRaDE`, 1.06M)**, plus **CrashCourse *Evolutionary Development: Chicken Teeth - Crash Course Biology #17* (`9sjwlxQ_6LI`, 935.2k — exact Hox genes & embryonic development match!)** and **SciShow *Hilde Mangold and the Organizer of Life | Great Minds* (`00L05Aqh7_0`, 110.2k — exact Hilde Mangold & Spemann Organizer match!)**, alongside `public_search.md` & `public_search_titles.md` showing `"hox genes embryonic development"` and `"hilde mangold hans spemann homeobox hox genes"` both triggering YouTube autocomplete, all 5 top GB search results for `"hox genes embryonic development"` under 92k views, and all 5 top GB slots for *How One Single Cell Knows Where to Build Your Head and Hands* under 29k views). The topic isn't locked yet: Chief locks `067` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed — building a body is so complicated that thousands of architect genes must be scattered randomly across every chromosome! Wrong! A tiny team of master architect genes sits lined up along the chromosome in the exact head-to-tail order of the body itself!" — where Edward B. Lewis on 7 December 1978 in *Nature* mapped the four-winged `Ultrabithorax` fly and chromosomal colinearity, followed on 30 October 1980 by Christiane Nüsslein-Volhard and Eric Wieschaus's 15 segmentation genes) lands in Part 03; Matthew Scott, Amy Weiner, William McGinnis, Michael Levine, and Walter Gehring's March–July 1984 discovery of the conserved 180-base-pair `Homeobox` (`8 fly Hox genes` vs `39 human HOX genes`) and Halder, Callaerts & Gehring's 24 March 1995 mouse `Pax6` ectopic fly-eye experiment land in Part 04; why our five fingers aren't five identical thumbs is raised and explained in Part 05 via Clifford Tabin's December 1993 `Sonic hedgehog` limb-bud morphogen gradient across nested `HOXD` genes; the ending hands off directly to `068` (*Why Do Identical Twins With 100% Identical DNA Grow Up Different (`Epigenetics, X-Chromosome Inactivation & DNA Methylation`)?*), with no goodbye and no subscribe ask. Five VO parts, matching 009–066.

## Marker count (v01)

Run on `embryo_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked chromosomal colinearity chart on period paper comparing the 8 fruit-fly homeotic genes (lab, pb, Dfd, Scr, Antp, Ubx, abd-A, Abd-B) and the 39 mammalian/human HOX genes (4 clusters), all sharing the conserved 180-base-pair homeobox (60-amino-acid DNA-binding homeodomain) and arranged along the chromosome in the exact head-to-tail order of the body segments they build (0:34); 2) inked Spemann-Mangold (May 1921 / 1924 Arch. Mikr. Anat. Entw. 100: 599–638) chimera cross-section showing unpigmented donor organizer cells (dorsal blastopore lip) recruiting >80% pigmented host ventral ectoderm cells into a secondary brain and spinal cord (0:52); 3) inked Roux (1888 hot-needle half-embryo) vs Driesch (1891 shaken 2-cell and 4-cell sea-urchin blastomere separation yielding 100% complete miniature pluteus larvae) and Spemann & Mangold (May 1921 / 1924 embryo Um 132) chimeric neural tube cell-origin chart on period paper (1:58); 4) inked Nüsslein-Volhard & Wieschaus (30 October 1980, Nature 287: 795–801) and Lewis (7 December 1978, Nature 276: 565–570) Drosophila segmentation hierarchy chart on period paper showing Maternal gradient (Bicoid anterior-to-posterior concentration curve) -> Gap genes -> Pair-rule 7-stripe genes -> 14 Segment-polarity stripes -> 8 Colinear Homeotic (Hox) selector genes (3:47); 5) inked McGinnis, Garber, Wirz, Kuroiwa & Gehring (July 1984, Cell 38: 675–680) cross-species Southern blot & Halder, Callaerts & Gehring (24 March 1995, Science 267: 1788–1792) Pax6/eyeless ectopic eye-induction chart on period paper showing the 180-bp homeobox and mouse Pax6 cDNA inducing compound eyes on Drosophila legs, wings, and antennae (5:32); 6) animated timeline building 1891 & May 1921 · 7 Dec 1978 & 30 Oct 1980 · Mar–Jul 1984 & 24 Mar 1995 (6:48) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) your body's master architect genes are lined up along your chromosome like stations on a railway line — the genes at the front of the DNA strand build your head and neck, the middle genes build your chest and ribs, and the genes at the end build your lower back and limbs (0:34); 2) transplanting a speck of organizer tissue smaller than a pinhead onto an embryo's belly is like dropping a conductor onto a building site — it orders the surrounding skin cells to stop making belly skin and build a second brain and spine instead (0:52); 3) Hilde Mangold's two-colour newt transplant worked like building a house out of white and black bricks — when the new twin spine appeared, over four-fifths of its bricks were black belly bricks that the tiny white organizer patch had recruited on the spot (1:58); 4) building a body from a single round egg is like painting a map on a blank globe — first a smooth gradient of maternal ink marks the North Pole as the head, then three waves of stencil genes divide the globe into fourteen numbered stripes, and finally each stripe reads its own Hox address code (3:47); 5) swapping the mouse Pax6 gene into a fruit fly is like unplugging the "Turn on the headlights" dashboard switch from a lorry and plugging it into a motorbike — the switch itself is identical, and the motorbike turns on its own headlight (5:32); 6) from a loop of baby hair in 1921 to a mouse gene inside a fruit fly in 1995, scientists proved that every animal with a head and a heart is built from the same half-billion-year-old genetic blueprint (6:48) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **10** | Hans Driesch (0:34), Hilde Mangold (0:34), Hans Spemann (0:34), Edward B. Lewis (0:34), Christiane Nüsslein-Volhard (0:34), Eric F. Wieschaus (0:34), Matthew P. Scott (0:34), Walter J. Gehring (0:34), Wilhelm Roux (1:28), William McGinnis (4:58) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **26** | Naples, 1891 (0:00), 1891 (0:34), May 1921 (0:34), 7 December 1978 (0:34), 30 October 1980 (0:34), 1984 (0:34), 1888 (1:28), 1891 (1:28), May 1921 (1:28), September 1924 (1:28), 1935 (1:28), 1894 (3:13), 1915 (3:13), 7 December 1978 (3:13), 30 October 1980 (3:13), 1995 (3:13), 29 March 1984 (4:58), July 1984 (4:58), 24 March 1995 (4:58), 1891–1995 (6:48), December 1993 (7:20), 22 April 1961 (7:45), May 1964 (7:45), January 1975 (7:45), August 2003 (7:45), July 2005 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **3** | Belly skin becomes a brain (1:28); Legs growing on a fly's head (3:13); Mouse gene builds a fly eye (4:58) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (single fertilised egg cell dividing into a striped embryo as colour-coded Hox genes light up in head-to-tail order along the chromosome and body), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Driesch's 1891 sea-urchin twins, Mangold & Spemann's May 1921 Organizer, Lewis's 7 December 1978 Bithorax colinearity, Nüsslein-Volhard & Wieschaus's 30 October 1980 segmentation screen, and Scott & Gehring's 1984 180-bp Homeobox) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:08 (Part 04 plugging the mouse `Pax6` master switch into a fruit fly's knee).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on what happened in Naples in 1891 when Hans Driesch shook a two-cell sea-urchin embryo and what Hilde Mangold discovered with a loop of baby hair; Part 02 opens cold on the 200-year homunculus myth and Wilhelm Roux's 1888 hot-needle frog experiment, tells the story of Driesch's 1891 shaken sea-urchin twins and Hilde Mangold and Hans Spemann's May 1921 dorsal blastopore lip transplant (`The Organizer`, `embryo 1921 Um 132`), and ends on who finally cracked the genetic code by breeding mutant flies with four wings and legs on their heads; Part 03 opens cold on the midpoint twist ("Case closed — building a body is so complicated that thousands of architect genes must be scattered randomly across every chromosome! Wrong!"), tells the story of Edward Lewis's 7 December 1978 four-winged `Ultrabithorax` fly and chromosomal colinearity and Christiane Nüsslein-Volhard and Eric Wieschaus's 30 October 1980 27,000-fly Heidelberg screen, and ends on what happened in 1984 when scientists searched for those fly sequences inside frogs, mice, and humans; Part 04 opens cold on Scott, Weiner, McGinnis, Levine, and Gehring's March–July 1984 discovery of the conserved 180-letter `Homeobox` (`39 human HOX genes`), explains Walter Gehring's 24 March 1995 mouse `Pax6` ectopic fly-eye experiment, and ends on why identical twins with 100% identical DNA grow up different and why almost every calico cat is female; Part 05 opens cold on `Sonic hedgehog` (`December 1993`) patterning our five fingers, and hands off to Mary Lyon (22 April 1961), Vincent Allfrey (May 1964), Holliday & Riggs (January 1975), Randy Jirtle (August 2003), and Manel Esteller (July 2005) (`068`).
- **Quirky anecdote before the hard idea:** Hilde Mangold using a loop of fine blond hair from Hans Spemann's infant daughter as a microscopic lasso; Walter Gehring switching on a mouse eye gene inside a fruit fly's leg so the fly sprouted a compound insect eye on its knee!
- **Rivalry / tension:** Wilhelm Roux's 1888 mosaic half-embryo dogma vs Hans Driesch's 1891 shaken totipotent twins; "insect-only genes" scepticism vs the 1984 cross-species `Homeobox` shock and 1995 `Pax6` deep-homology proof.
- **Misconception explained away:** "Why aren't your five fingers five identical copies when every cell in your hand carries the exact same genes?" — explained via the `Sonic hedgehog` morphogen gradient across nested `HOXD` genes (Part 05, 6:48).

## For Chief to decide

1. Lock **067 = How Does a Single Fertilised Egg Know Where to Put Your Head, Heart & Hands (`Embryology, the Spemann-Mangold Organizer & Homeobox / Hox Genes`)? Hans Driesch's 1891 Shaken Sea-Urchin Twin Embryos, Hilde Mangold & Hans Spemann's May 1921 Two-Headed Newt Embryo (`The Organizer`), Edward B. Lewis's 7 December 1978 Four-Winged Fruit Fly (`Ultrabithorax`), and Christiane Nüsslein-Volhard, Eric Wieschaus & Walter Gehring's 1980–1984 Discovery of the `Homeobox` (`Hox` Body-Plan Genes) (1891–1995)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Hox Genes: The Hidden Map That Built Your Body* (46 chars)
   - **B (Search question, §1 rule 2):** *How One Single Cell Knows Where to Build Your Head and Hands* (60 chars)
   - **Alt (Search / twist question):** *Why a Mouse Gene Made a Fruit Fly Grow an Eye on Its Leg* (56 chars)
2. Review `embryo_script_master_v01.md` (91.4/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# embryo_script_master_v01.md

**Decision:** PASS · **Score:** 91.4 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 7.6 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1583 · Est. min: 10.6 · Chapters: 4

## Cold open excerpt

> How does one microscopic, round fertilised egg cell know which end is your head, which end is your tail, and where to sprout arms instead of legs ? And how did a baby's blond hair in May nineteen twenty-one , a four-winged fruit fly in December nineteen seventy-eight , and a hund

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91.4/100 — proceed to VO after production checklist.

Pass threshold: 90
```
