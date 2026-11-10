# 074 script v01: notes for review (J0705)

Script: `lungs_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0705, Gemini Argon, 20 Oct 2026).** Built from `074_Hooke-Lower-Bohr-Krogh-Avery-Perutz-Lungs-Surfactant/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-19_J0682.md` (`evidence_2026-10-19_J0682/n_lungs_breathing.md` PASS — 5 education videos ≥ 1M views, ALL 5 strictly on lungs, breathing, gas exchange & haemoglobin: **TED-Ed ★ *How does asthma work? - Christopher E. Gaw* (`PzfLDi-sL3w`, 8.71M)**, **TED-Ed ★ *How do lungs work? - Emma Bryce* (`8NUxvJS-_0k`, 3.65M — exact subject match!)**, **TED-Ed ★ *Oxygen’s surprisingly complex journey through your body - Enda Butler* (`GVU_zANtroE`, 3.52M — exact haemoglobin & gas-exchange match!)**, **Khan Academy *The lungs and pulmonary system* (`SPGRkexI_cs`, 1.44M — exact subject match!)**, and **Khan Academy *Hemoglobin | Human anatomy and physiology* (`LWtXthfG9_M`, 1.03M — exact subject match!)**, plus **Amoeba Sisters (`3.90M`)**, **Nemours KidsHealth (`3.02M`)**, and **Science Sauce (`1.69M`)** in `public_search.md`, **TED-Ed ★ *How breathing works - Nirvair Kaur* (`Kl4cU9sG_08`, 492.8k)**, and **Cognito *The Lungs & Gas Exchange* (`Nn4ke02sW8Q`, 169.6k)**, alongside `public_search.md` & `public_search_titles.md` showing `"how do lungs work"` is an exact YouTube autocomplete match (`yes`), all 5 top GB search results for `"august krogh max perutz mary ellen avery surfactant"` under 41k views, and 4 of the top 5 GB slots for *How Your Lungs Breathe Without Collapsing Every Time You Exhale* under 416k views). The topic isn't locked yet: Chief locks `074` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed — haemoglobin is just a passive iron bucket that carries four oxygen molecules the way a shopping bag carries four apples! Wrong! On the thirteenth of February nineteen sixty, after twenty-two years of X-ray crystallography in Cambridge, Max Perutz proved that haemoglobin is a shape-shifting four-part machine — a molecular lung that physically clicks open when the first oxygen molecule sits down!" — where Max Perutz on 13 February 1960 in *Nature*, after solving the X-ray phase problem with mercury heavy-atom replacement in 1953, unveiled the 3D structure of `haemoglobin` and its `0.04 nm` iron-movement `T`-to-`R` cooperative switch) lands in Part 03; Kurt von Neergaard's 1929 saline-lung experiment, John Clements's 1957 surface balance, and Mary Ellen Avery & Jere Mead's May 1959 *AMA J. Dis. Child.* discovery of `pulmonary surfactant` deficiency in premature infants land in Part 04; the ending hands off directly to `075` (*How Do Your Cells Copy and Shuffle 46 Chromosomes — and How Did One White-Eyed Fruit Fly Map Our Genes (`Chromosomes, Mitosis, Meiosis & Thomas Hunt Morgan's Fly Room`)?*), with no goodbye and no subscribe ask. Five VO parts, matching 009–073.

## Marker count (v01)

Run on `lungs_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked alveolar gas-exchange, haemoglobin S-curve & surfactant surface-tension chart on period paper showing 300,000,000 alveoli (~70–100 m2 area, 0.5 µm barrier), Krogh's passive diffusion gradient (alveolar PO2 > capillary PO2), Bohr & Perutz's 4-subunit haemoglobin cooperative O2 curve, and Avery's pulmonary surfactant lowering surface tension from ~50 dyn/cm to near 0 dyn/cm on exhalation (0:34); 2) inked August & Marie Krogh (1910 Skand. Arch. Physiol. 23: 179–278) microtonometer alveolar vs arterial oxygen partial pressure table proving alveolar PO2 is always higher than arterial blood PO2 (0:52); 3) inked Christian Bohr, Hasselbalch & Krogh (1904 Skand. Arch. Physiol. 16: 402–412) CO2 Bohr-Effect oxygen dissociation shift & August and Marie Krogh (1910 Skand. Arch. Physiol. 23: 179–278 "Seven Little Devils") alveolar-to-arterial O2 diffusion curve on period paper (1:58); 4) inked Max Perutz et al. (13 February 1960 Nature 185: 416–422 & 1970 Nature 228: 726–734) 4-subunit haemoglobin T-state (deoxy) to R-state (oxy) conformational switch & hyperbolic myoglobin vs sigmoidal haemoglobin O2 binding curve on period paper (3:47); 5) inked Kurt von Neergaard (1929 Z. Gesamte Exp. Med. 66: 373–394) air vs saline lung pressure-volume hysteresis curve & Mary Ellen Avery and Jere Mead (May 1959 AMA J. Dis. Child. 97: 517–523) Langmuir trough minimum lung surface-tension table on period paper (5:32); 6) animated timeline building Oct 1667 & 1904 · 1910 · May 1959 & 13 Feb 1960 (6:48) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) your two lungs fold the surface area of an entire singles tennis court inside your ribcage — and every red blood cell races across that court in three-quarters of a second, snapping up oxygen through a wall fifty times thinner than tissue paper (0:34); 2) measuring the oxygen pressure of a single microscopic air bubble inside a hair-thin glass tube proved that your lungs don't need a single pump to push oxygen into your blood — oxygen flows downhill by itself like crowd-surfers pouring through an open stadium gate (0:52); 3) August and Marie Krogh proved that your lungs don't need an energy-burning oxygen pump because evolution folded a tennis court of membrane fifty times thinner than tissue paper inside your chest — letting oxygen pour into your blood by pure physical diffusion (1:58); 4) when the first oxygen molecule lands on haemoglobin, it tugs an iron atom by less than half the width of a single hydrogen atom — yet that tiny lever pull twists the entire ten-thousand-atom protein by fifteen degrees and throws open the doors for the next three oxygens (3:47); 5) without Mary Ellen Avery's phospholipid surfactant soap, inflating a newborn baby's wet microscopic lung bubbles on every breath is like trying to blow up three hundred million wet party balloons whose walls are glued together with superglue (5:32); 6) from fireplace bellows in seventeenth-century London to a microscopic gas bubble in Copenhagen, an X-ray beam in Cambridge, and a soap trough in Boston, scientists unlocked the tennis-court sponge that keeps us breathing (6:48) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **11** | Robert Hooke (0:34), Richard Lower (0:34), Christian Bohr (0:34), August Krogh (0:34), Marie Krogh (0:34), Mary Ellen Avery (0:34), Max Perutz (0:34), John C. Kendrew (3:13), Kurt von Neergaard (4:58), John A. Clements (4:58), Jere Mead (4:58) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **30** | Copenhagen, 1910 (0:00), October 1667 (0:34), 1904 (0:34), 1910 (0:34), 1929 (0:34), May 1959 (0:34), 13 February 1960 (0:34), 1661 (1:28), 24 October 1667 (1:28), 1669 (1:28), 1904 (1:28), 1910 (1:28), 1920 (1:28), 1862 (3:13), 1925 (3:13), 1937 (3:13), 1953 (3:13), 1958 (3:13), 13 February 1960 (3:13), 1962 (3:13), 1929 (4:58), 1957 (4:58), May 1959 (4:58), January 1980 (4:58), 1667–1980 (6:48), 1879 (7:45), 1902 (7:45), 1905 (7:45), May 1910 (7:45), January 1913 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **3** | Passive diffusion across a tennis court (1:28); Iron moves 0.04 nanometres (3:13); Soap film saves newborns (4:58) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (human chest breathing in as camera dives down bronchial tree into 300 million wet alveoli where O2 diffuses across a 0.5 µm barrier into 4-subunit haemoglobin while surfactant stops collapse), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Hooke & Lower's October 1667 scarlet blood, Bohr's 1904 `Bohr Effect`, August & Marie Krogh's 1910 passive diffusion proof, Neergaard 1929 & Avery May 1959 `pulmonary surfactant`, and Perutz's 13 February 1960 3D `haemoglobin` structure) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:08 (Part 04 coating two wet glass lung bubbles with glowing `DPPC SURFACTANT` so the smaller bubble stops snapping shut into the larger one).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why Christian Bohr and J. S. Haldane insisted the lungs actively pump oxygen into the blood and how August and Marie Krogh in 1910 proved their famous teacher wrong; Part 02 opens cold on Galen's 1,500-year heart-radiator myth, tells the story of Hooke & Lower (1667–1669), Christian Bohr (1904), and August & Marie Krogh's 1910 "Seven Little Devils" microtonometer proof, and ends on how `haemoglobin` packs 70 times more oxygen into blood than water and why Max Perutz spent 22 years shooting X-rays at horse blood crystals; Part 03 opens cold on the midpoint twist ("Case closed — haemoglobin is just a passive iron bucket that carries four oxygen molecules the way a shopping bag carries four apples! Wrong!"), tells the story of Hoppe-Seyler, Adair, Kendrew, and Max Perutz's 1937–13 February 1960 X-ray discovery of the `0.04 nm` `T`-to-`R` molecular lung, and ends on why Laplace surface tension inside 300 million wet air sacs should crush your lungs on every breath and how a 31-year-old Boston doctor in May 1959 solved the mystery; Part 04 opens cold on Harvard Medical School rejecting Mary Ellen Avery in 1948, explains Kurt von Neergaard (1929), John Clements (1957), and Avery & Mead's May 1959 *AMA J. Dis. Child.* `pulmonary surfactant` breakthrough, and ends on how your cells copy and shuffle the 46 chromosomes that encode those proteins; Part 05 opens cold on newborn surfactant therapy saving millions of lives and hands off to Walther Flemming (1879), Theodor Boveri & Walter Sutton (1902–1903), Nettie Stevens (1905), Thomas Hunt Morgan (May 1910), and Alfred Sturtevant (January 1913) (`075`).
- **Quirky anecdote before the hard idea:** August and Marie Krogh publishing seven back-to-back papers nicknamed "The Seven Little Devils" to prove August's own mentor Christian Bohr wrong; Mary Ellen Avery being rejected by Harvard Medical School because their women's quota was full, surviving tuberculosis, discovering newborn surfactant deficiency, and becoming Professor at Harvard Medical School!
- **Rivalry / tension:** Active oxygen secretion (`Christian Bohr & J. S. Haldane`) vs passive physical diffusion (`August & Marie Krogh's "Seven Little Devils"`); airway-blockage myth vs surface-tension collapse (`Mary Ellen Avery & Jere Mead`).
- **Misconception explained away:** "Do your lungs actively pump oxygen into your blood, and is breathing effort mostly stretching rubbery lung tissue?" — refuted by August & Marie Krogh's 1910 microtonometer proof of 100% passive diffusion and Kurt von Neergaard's 1929 / Mary Ellen Avery's 1959 proof that two-thirds of lung recoil is water surface tension tamed by `pulmonary surfactant` (Parts 02 & 04).

## For Chief to decide

1. Lock **074 = How Do Your Lungs Pull Oxygen Into Your Blood — and Why Don't 300 Million Wet Air Sacs Collapse Every Time You Exhale (`Lungs, Alveoli, Haemoglobin & Pulmonary Surfactant`)? Robert Hooke & Richard Lower's 1667 Scarlet-Blood Proof, Christian Bohr's 1904 `Bohr Effect` vs August & Marie Krogh's 1910 "Seven Little Devils" Diffusion Proof, Kurt von Neergaard's 1929 Surface-Tension Lung Experiment, Mary Ellen Avery's May 1959 Discovery of `Pulmonary Surfactant` in Premature Babies, and Max Perutz's 13 February 1960 3D X-Ray Structure of `Haemoglobin` (1667–1980)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *The Lungs: Why 300 Million Air Sacs Don't Collapse* (50 chars)
   - **B (Search question, §1 rule 2):** *How Your Lungs Breathe Without Collapsing Every Time You Exhale* (63 chars)
   - **Alt (Search / twist question):** *Why a Microscopic Soap Film Keeps Your Lungs From Snapping Shut* (63 chars)
2. Review `lungs_script_master_v01.md` (91.0/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# lungs_script_master_v01.md

**Decision:** PASS · **Score:** 91 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 7.2 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1788 · Est. min: 11.9 · Chapters: 4

## Cold open excerpt

> How do your lungs pull oxygen into your blood across three hundred million microscopic wet air bubbles ( alveoli ) ? Why doesn't water surface tension crush all three hundred million bubbles flat every single time you breathe out — and how did fireplace bellows in London in Octob

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91/100 — proceed to VO after production checklist.

Pass threshold: 90
```
