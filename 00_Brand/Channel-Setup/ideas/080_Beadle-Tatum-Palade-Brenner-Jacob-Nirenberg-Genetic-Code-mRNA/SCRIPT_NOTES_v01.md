# 080 script v01: notes for review (J0736)

Script: `genetic_code_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0736, Gemini Argon, 20 Oct 2026).** Built from `080_Beadle-Tatum-Palade-Brenner-Jacob-Nirenberg-Genetic-Code-mRNA/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-20_J0713.md` (`evidence_2026-10-20_J0713/n_genetic_code_mrna.md` PASS — 5 education videos ≥ 1M views, ALL 5 strictly on protein synthesis, mRNA, transcription & translation: **Amoeba Sisters *Protein Synthesis: Transcription and Translation (Updated)* (`oefAI2x2CQM`, 11.55M — exact subject match!)**, **Khan Academy *DNA replication and RNA transcription and translation* (`6gUY5NoX1Lk`, 3.17M — exact subject match!)**, **Khan Academy *Transcription and mRNA processing | Biomolecules | MCAT* (`JQIwwJqF5D0`, 1.90M — exact subject match!)**, **Cognito *How are Proteins Made? Transcription & Translation* (`ubdoUqmNF98`, 1.90M — exact subject match!)**, and **Khan Academy *Translation (mRNA to protein) | Biomolecules | MCAT* (`ocAAkB32Hqs`, 1.42M — exact subject match!)**, plus **FuseSchool *Protein Synthesis* (`x5ZXQo-xeMo`, 642.8k)**, **TED ★ *How mRNA Medicine Will Change the World | Melissa J. Moore* (`h5D3mv8ewCY`, 356.9k)**, and **CrashCourse *Transcription: How mRNA Helped Save Lives: Crash Course Biology #34* (`j6YaOqKORYY`, 268.3k)**, alongside `public_search.md` & `public_search_titles.md` showing `"transcription and translation"` is an exact YouTube autocomplete match (`yes`), all 5 top GB search results for `"marshall nirenberg sydney brenner mrna genetic code"` under 40k views, and all 3 top GB slots for *How an Unknown Scientist at 3 AM Cracked the 4-Letter Genetic Code* under 181k views). The topic isn't locked yet: Chief locks `080` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; Archibald Garrod's 1902 "inborn errors of metabolism", George Beadle & Edward Tatum's 1941 irradiated *Neurospora* bread mould Tube #299 proving `One Gene–One Enzyme`, and George Palade's January 1955 discovery of `ribosomes` land in Part 02; the midpoint twist ("Case closed — since Palade's ribosomes are made of RNA, every ribosome must be custom-built in the nucleus as a permanent mould for one specific protein! Wrong! On Good Friday, fifteen April nineteen sixty inside a Cambridge college room, François Jacob and Sydney Brenner realized that ribosomes are neutral tape-players — and that cells run on a self-destructing photocopy tape called `messenger RNA`!" — where Brenner, Jacob & Matthew Meselson proved `mRNA` and Francis Crick & Brenner proved 3-letter `triplet codons`) lands in Part 03; Marshall Nirenberg & Heinrich Matthaei's 3:00 a.m. 27 May 1961 `poly-U` (`UUU = Phenylalanine`) breakthrough and Har Gobind Khorana's completion of the 64-codon genetic code land in Part 04; the ending hands off directly to `081` (*How Do Plants See Light, Feel Gravity & Ripen Fruit Without Eyes, Nerves or Brains?*), with no goodbye and no subscribe ask. Five VO parts, matching 009–079.

## Marker count (v01)

Run on `genetic_code_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked Central Dogma (`DNA → mRNA → ribosome → protein`) & 64-triplet genetic code table on period paper showing 4 bases read in 1-letter (4), 2-letter (16), vs 3-letter (`4³ = 64`) words for 20 amino acids, and Nirenberg & Matthaei's 27 May 1961 `poly-U` experiment (`39,800 cpm` vs `70 cpm`) (0:34); 2) inked Nirenberg & Matthaei (Oct 1961 *PNAS* Table 1) cell-free `poly-U` radioactive amino acid incorporation chart (`39,800 cpm` `¹⁴C-L-phenylalanine` vs `70 cpm` control) (0:52); 3) inked Beadle & Tatum (15 Nov 1941 *PNAS*) *Neurospora crassa* X-ray mutant Tube #299 pyridoxine growth chart + George Palade (Jan 1955) EM ribosome distribution chart (1:58); 4) inked Brenner, Jacob & Meselson (13 May 1961 *Nature*) heavy-isotope (`¹⁵N`/`¹³C`) ribosome density-gradient chart + Crick & Brenner (30 Dec 1961 *Nature*) `+1/+2` vs `+3` triplet reading-frame restoration chart (3:47); 5) inked Nirenberg, Matthaei, Leder & Khorana (1961–1966) complete 64-codon genetic code dictionary chart (5:32); 6) animated timeline 1902–1968 (6:48) | ≥ 3 per long, including the timeline |
| `SCALE` | **6** | 1) 1-letter (4) vs 2-letter (16) vs 3-letter (`4³ = 64`) triplet math for 20 amino acids (0:34); 2) feeding pure `U-U-U-U-U` into crushed bacteria as the Rosetta Stone of biology (0:52); 3) 10 million ribosomes packed into a single human cell like 10 million microscopic 3D printers (1:58); 4) DNA master blueprint in the nucleus vault vs disposable `mRNA` photocopies sent to the ribosome construction crew (3:47); 5) every living thing on Earth from grass and gut bacteria to human brain neurons reading the exact same 64-word dictionary (5:32); 6) Stanford bread mould to Cambridge Good Friday to Bethesda 3 a.m. Geiger counter cracking life's operating system (6:48) | `SCALE:` on every `DATA:` (`grep -c` matches) |
| `WHO` | **12** | George Wells Beadle (1903–1989) — American geneticist; Edward Lawrie Tatum (1909–1975) — American biochemist and geneticist; George Emil Palade (1912–2008) — Romanian-American cell biologist; Sydney Brenner (1927–2019) — South African molecular biologist; François Jacob (1920–2013) — French geneticist and biologist; Matthew Meselson (born 1930) — American molecular biologist; Marshall Warren Nirenberg (1927–2010) — American biochemist; J. Heinrich Matthaei (born 1929) — German biochemist; Archibald Garrod (1857–1936) — British physician; Francis Crick (1916–2004) — British molecular biologist and biophysicist; Jacques Monod (1910–1976) — French biochemist and geneticist; Har Gobind Khorana (1922–2011) — Indian-American biochemist | Every named person at first mention, role right for the scene's year |
| `WHEN` | **26** | Bethesda, 27 May 1961 (0:00); 1941, 1955, 15 April 1960, 13 May 1961, 27 May 1961 (0:34); 1902, 15 November 1941, January 1955, 1958 (1:28); 1957, 1959, 15 April 1960, 13 May 1961, 30 December 1961 (3:13); 1954, 27 May 1961, August 1961, October 1961, 1966, 1968 (4:58); 1941–1968 timeline marker (6:48); November 1880, 1901, 17 April 1926, 1934 (7:45) | Every spoken date or era |
| `FACT` | **3** | `299th tube proved gene law` (1:28); `mRNA is a disposable tape` (3:13); `UUU spelled first life word` (4:58) | 2–4 per long, ≤ 4 words per card |

## Craft lessons check (*Reference lessons* §1)

- **Cold opens & cliffhanger hand-offs:** Part 01 opens cold on the 4-letter DNA alphabet question (`A, T, C, G` → 20 amino acids) and ends on how Beadle and Tatum in 1941 used pink bread mould and an X-ray tube to prove what a gene builds; Part 02 opens cold on Garrod's 1902 black-urine clue and Beadle & Tatum's 1941 *Neurospora* Tube #299 + Palade's 1955 ribosomes, and ends on how the recipe gets from the locked DNA vault in the nucleus to the ribosomes out in the cytoplasm on Good Friday, 15 April 1960; Part 03 opens cold on the midpoint twist ("Case closed — since Palade's ribosomes are made of RNA, every ribosome must be custom-built in the nucleus as a permanent mould for one specific protein! Wrong!"), tells the story of Brenner, Jacob & Meselson's `messenger RNA` and Crick & Brenner's 3-letter `triplet codons`, and ends on how two unknown scientists in Bethesda beat the elite "RNA Tie Club" at 3:00 a.m. on 27 May 1961; Part 04 opens cold on the 20-member RNA Tie Club vs Nirenberg and Matthaei's cell-free mortar and pestle, explains the 3:00 a.m. `poly-U` (`UUU = Phenylalanine`) spike to 39,800 cpm, the Moscow surprise, and Khorana's full 64-codon dictionary, and ends on how plants read that same genetic code to see light, feel gravity, and ripen fruit without eyes or brains; Part 05 opens cold on the universal 64-word dictionary across all life on Earth, and hands off to Charles & Francis Darwin (Nov 1880), Frits Went (17 Apr 1926), and Dmitry Neljubow & Richard Gane (1901–1934) (`081`).
- **Quirky anecdote before the hard idea:** George Gamow and Francis Crick's 20-member `RNA Tie Club` with custom embroidered woollen neckties; Beadle and Tatum testing 299 tubes of X-rayed bread mould; Nirenberg speaking to 30 people in a tiny Moscow room before Crick moved him to the 1,000-seat hall!
- **Rivalry / tension:** "One Gene–One Ribosome" dogma vs Brenner, Jacob & Meselson's disposable `mRNA` tape; the superstar `RNA Tie Club` theorists vs unknown biochemical outsiders Marshall Nirenberg and Heinrich Matthaei.
- **Misconception explained away:** "Does DNA leave the nucleus to build proteins directly, or is each ribosome custom-built for one protein?" — refuted by Brenner, Jacob & Meselson's 1960–1961 proof of disposable `mRNA` transcripts feeding through neutral ribosomes (Part 03).

## For Chief to decide

1. Lock **080 = How Did Scientists Crack the 4-Letter Genetic Code — and How Did an Unknown Scientist at 3:00 a.m. Beat the World's Greatest Biologists to Read Life's First Word (`Transcription, Translation, Messenger RNA, Ribosomes & Marshall Nirenberg's 1961 Genetic Code`)? George Beadle & Edward Tatum's 1941 Irradiated Bread-Mould "One Gene–One Enzyme" Proof, George Palade's 1955 Discovery of `Ribosomes`, Sydney Brenner, François Jacob & Matthew Meselson's Good Friday 1960 Discovery of `Messenger RNA (mRNA)`, and Marshall Nirenberg & J. Heinrich Matthaei's 27 May 1961 3:00 a.m. `Poly-U` (`UUU = Phenylalanine`) Experiment (1941–1968)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *The Genetic Code: Cracked by an Outsider at 3 AM* (48 chars)
   - **B (Search question, §1 rule 2):** *How an Unknown Scientist at 3 AM Cracked the 4-Letter Genetic Code* (66 chars)
   - **Alt (Search / twist question):** *How Your Cells Read DNA to Build Proteins Through Messenger RNA* (63 chars)
2. Review `genetic_code_script_master_v01.md` (90.3/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# genetic_code_script_master_v01.md

**Decision:** PASS · **Score:** 90.3 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 7.5 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 7 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1553 · Est. min: 10.4 · Chapters: 4

## Cold open excerpt

> How do your cells read a four-letter DNA alphabet ( A, T, C, G ) locked inside the nucleus? Right now, your cells translate those four chemical letters into twenty different amino acids to build every protein in your body — so how did an unknown thirty-four-year-old scientist wor

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 90.3/100 — proceed to VO after production checklist.

Pass threshold: 90
```
