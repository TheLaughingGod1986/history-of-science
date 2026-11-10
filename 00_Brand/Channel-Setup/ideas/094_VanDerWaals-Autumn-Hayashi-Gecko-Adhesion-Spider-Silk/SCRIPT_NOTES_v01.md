# 094 script v01: notes for review (J0803)

Script: `gecko_spider_silk_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0803, Gemini Argon, 21 Oct 2026).** Built from `094_VanDerWaals-Autumn-Hayashi-Gecko-Adhesion-Spider-Silk/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-21_J0790.md` (`evidence_2026-10-21_J0790/n_spider_silk_gecko.md` PASS — 4 education videos ≥ 1M views, ALL 4 strictly on spider silk and gecko adhesion: **Veritasium *Is spider web really stronger than steel?* (`wt4p2oalmRY`, 9.80M — exact spider dragline silk tensile strength match!)**, **TED-Ed ★ *Can you solve the giant spider riddle? - Dan Finkel* (`0l5ftgEQUjM`, 3.58M)**, **Be Smart *20 MILLION Year-Old Spider and the Science of Spider Silk* (`QQOxB_ylkvs`, 3.45M — exact spider silk evolution & spidroin protein match!)**, and **TED-Ed ★ *How do geckos defy gravity? - Eleanor Nelsen* (`YeSuQm7KfaE`, 1.66M — exact Kellar Autumn gecko setae, spatulae & van der Waals forces match!)**, plus **TED-Ed ★ `6nWba9Ii5Lo` (`987.0k`)**, **FuseSchool *What Are Intermolecular Forces* (`9YwdeEDrfPI`, 715.2k)**, **Khan Academy `hA5jddDYcyg` (`672.2k`)**, **SciShow *Why Can't We Make Spider Silk?* (`UX2LHcLxjio`, 521.0k)**, **SciShow *We Finally Made Synthetic Spider Silk* (`rLtOcr6gMaQ`, 440.5k)**, **Be Smart *Why Geckos Are Sticky Without Being Sticky* (`p6QmV1EbVnI`, 413.7k)**, and **TED ★ *Cheryl Hayashi: The magnificence of spider silk* (`xossR6eHv3I`, 163.9k)**, alongside `public_search.md` & `public_search_titles.md` showing `"how can geckos climb walls"` is an exact YouTube autocomplete match (`yes`), all 5 top GB search results for `"kellar autumn gecko van der waals spider silk"` under 414k views, and 4 of the top 5 GB slots for *How Spider Silk and Gecko Toes Unlocked Nature's Strongest Forces* under 330 views). The topic isn't locked yet: Chief locks `094` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; Johannes Diderik van der Waals's 14 June 1873 intermolecular force equation (`a/V²`) and Fritz London's 1930 quantum dispersion force (`1/r⁶`) land in Part 02; the midpoint twist ("Case closed — geckos stick to walls using glue, suction cups, or microscopic water droplets! Wrong!") with Walter Dellit (1934), Rodolfo Ruibal & Valerie Ernst (1965), and Kellar Autumn, Robert Full, and Ronald Fearing's 8 June 2000 (*Nature*) single-gecko-seta force measurement (`200 µN`, `30°` release) and 27 August 2002 (*PNAS*) hydrophobic vs hydrophilic proof of `van der Waals` adhesion lands in Part 03; Randall Lewis (1990), John Gosline (1999), Cheryl Hayashi, and Fritz Vollrath & David Knight's 29 March 2001 (*Nature*) liquid-crystal `spidroin` spinneret and `beta-sheet` nanocrystal proof lands in Part 04; the ending hands off directly to `095` (*How Does a Caterpillar Dissolve Into Soup Inside a Chrysalis and Rebuild Itself as a Butterfly — and Why Does the Butterfly Still Remember What It Learned as a Caterpillar?*), with no goodbye and no subscribe ask. Five VO parts, matching 009–093.

## Marker count (v01)

Run on `gecko_spider_silk_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked Kellar Autumn et al. (2000 *Nature* 405: 681–685 & 2002 *PNAS* 99: 12252–12256) single-seta adhesive force chart (`200 µN`, `30°` release) & spider dragline silk vs steel and Kevlar comparison (0:34); 2) inked Vollrath & Knight (2001) and Gosline et al. (1999 *J. Exp. Biol.* 202: 3295–3303) mechanical properties table (`1.1 GPa` tensile strength, `160 MJ/m³` toughness) (0:52); 3) inked Johannes Diderik van der Waals (14 June 1873 Leiden thesis) gas-liquid continuity equation & Fritz London (1930 *Z. Phys.*) `1/r⁶` quantum induced-dipole curve (1:58); 4) inked Kellar Autumn et al. (8 June 2000 *Nature*) single-seta preload-and-drag activation curve & (27 Aug 2002 *PNAS*) hydrophobic GaAs vs hydrophilic SiO₂ equal-shear bar chart (3:47); 5) inked Randall Lewis (1990 *PNAS*) & Fritz Vollrath and David Knight (29 March 2001 *Nature*) spider spinneret pH-gradient (`6.9 → 6.3`) & `beta-sheet` nanocrystal stress-strain curve (5:32); 6) animated timeline 1873–2002 (6:48) | ≥ 3 per long, including the timeline |
| `SCALE` | **6** | 1) if all 6.5 million bristles on a single 70-g tokay gecko gripped a ceiling at once, they could hold up 130 kg — two grown adults (0:34); 2) each gecko bristle splits into up to 1,000 flat spatulae just 200 nm wide — 500× thinner than a human hair (0:52); 3) a single van der Waals bond is 50× weaker than a chemical bond, yet across 2 billion nano-tips it holds two adults (1:58); 4) a gecko attaches its toe in 5 ms and peels it off in 15 ms, running up glass at 20 body lengths/s with zero residue (3:47); 5) making Kevlar requires boiling petroleum chemicals in concentrated sulfuric acid, whereas a spider spins a fibre 3× tougher at room temperature using water and flies (5:32); 6) the weakest attraction in chemistry (<2 nm) lets geckos walk on glass and gives spider silk the strength to beat steel (6:48) | `SCALE:` on every `DATA:` (`grep -c` matches) |
| `WHO` | **9** | Johannes Diderik van der Waals (1837–1923) — Dutch theoretical physicist; Fritz Wolfgang London (1900–1954) — German-American theoretical physicist; Kellar Autumn (born 1965) — American biomechanist and biologist; Robert J. Full (born 1953) — American integrative biologist; Rodolfo Ruibal (1927–2021) — American herpetologist and zoologist; Ronald S. Fearing (born 1959) — American electrical engineer and roboticist; Randall V. Lewis (born 1947) — American molecular biochemist; Cheryl Y. Hayashi (born 1967) — American evolutionary biologist; Fritz Vollrath (born 1946) — German-British evolutionary biologist | Every named person at first mention, role right for the scene's year |
| `WHEN` | **23** | Leiden, 1873 & Berkeley/Stanford, 8 June 2000 (0:00); 14 June 1873, 1930, 1965, 8 June 2000, 29 March 2001, 27 August 2002 (0:34); 14 June 1873, 1910, 1930 (1:28); 1934, 1965, 8 June 2000, 27 August 2002 (3:13); 1990, 1999, 29 March 2001 (4:58); 1873–2002 timeline marker (6:48); 1669, 1864, 1934, 1954, 5 March 2008 (7:45) | Every spoken date or era |
| `FACT` | **3** | `Neutral atoms pull at 1 nm` (1:28); `Curling past 30° releases grip` (3:13); `Acid locks liquid silk into crystal` (4:58) | 2–4 per long, ≤ 4 words per card |

## Craft lessons check (*Reference lessons* §1)

- **Cold opens & cliffhanger hand-offs:** Part 01 opens cold on how a tokay gecko sprints upside down across polished glass with zero glue and zero suction and how the same quantum attraction (`van der Waals forces`) makes spider silk 5× stronger by weight than steel, and ends on how a Dutch schoolteacher in 1873 proved neutral atoms attract one another and how Kellar Autumn's team in 2000 measured a single gecko toe-hair; Part 02 opens cold on 19th-century billiard-ball gas dogma, tells the story of Van der Waals's 14 June 1873 Leiden thesis and Fritz London's 1930 quantum dispersion force, and ends on how Walter Dellit (1934), Rodolfo Ruibal (1965), and Kellar Autumn (2000) proved geckos climb glass using van der Waals forces; Part 03 opens cold on the midpoint twist ("Case closed — geckos stick to walls using glue, suction cups, or microscopic water droplets! Wrong!"), tells the story of Dellit's vacuum chamber, Ruibal & Ernst's electron microscopy, and Autumn, Full & Fearing's 2000–2002 single-seta (`200 µN`, `30°` release) and hydrophobic GaAs vs hydrophilic SiO₂ proof, and ends on how an orb-weaver spider weaves nanoscale intermolecular forces inside liquid-crystal silk; Part 04 opens cold on why spider dragline silk beats steel and Kevlar yet spiders can't be farmed like silkworms because they eat each other, tells the story of Randall Lewis (1990), Cheryl Hayashi, and Fritz Vollrath & David Knight's 29 March 2001 *Nature* liquid-crystal spinneret (`pH 6.9 → 6.3`), and ends on how a caterpillar dissolves into soup inside a chrysalis, rebuilds itself as a butterfly, and still remembers what it learned as a caterpillar; Part 05 opens cold on dry gecko space grippers and synthetic `spidroin` fibres, and hands off to Jan Swammerdam (1669), August Weismann (1864), Vincent Wigglesworth (1934), Peter Karlson (1954), and Martha Weiss (`Butterfly Metamorphosis & Caterpillar Memory`, `095`).
- **Quirky anecdote before the hard idea:** James Clerk Maxwell learning Dutch just to read Van der Waals's 1873 thesis; Walter Dellit pumping the air out of a vacuum chamber to see if a gecko falls off the glass; spiders eating each other whenever humans try to farm them like silkworms!
- **Rivalry / tension:** Five competing 2,000-year-old theories of gecko climbing (glue, suction, friction, micro-hooks, capillary water bridges) vs Autumn's 2000–2002 single-seta MEMS sensor and hydrophobic GaAs semiconductor test.
- **Misconception explained away:** "Don't geckos have suction cups or sticky glue on their feet?" — refuted by Dellit's 1934 vacuum test and Autumn's 2000–2002 dry van der Waals proof (Parts 01, 03).

## For Chief to decide

1. Lock **094 = How Can a Gecko Walk Upside Down on Polished Glass With Zero Glue — and Why Is a Spider's Silk Five Times Stronger by Weight Than Steel (`Van der Waals Intermolecular Forces, Kellar Autumn's 2000–2002 Single-Gecko-Seta Force Measurement & Spider Dragline Silk Spidroin Nanocrystals`)? Johannes Diderik van der Waals's 1873 Intermolecular Force Equation (`1910 Nobel Prize`), Ruibal & Ernst (1965) & Kellar Autumn, Robert Full & Ronald Fearing's 8 June 2000 (*Nature*) & 27 August 2002 (*PNAS*) Single-Seta Micro-Force Sensor Proof of `Van der Waals` Gecko Adhesion, and Cheryl Hayashi, Randy Lewis & Fritz Vollrath's Liquid-Crystal `Spidroin` Spider Silk Proof (1873–2002)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Gecko Toes and Spider Silk: How Weak Forces Beat Steel* (54 chars)
   - **B (Search question, §1 rule 2):** *How Spider Silk and Gecko Toes Unlocked Nature's Strongest Forces* (65 chars)
   - **Alt (Search / twist question):** *How Geckos Walk on Glass With Zero Glue and Why Spider Silk Beats Steel* (71 chars)
2. Review `gecko_spider_silk_script_master_v01.md` (91.9/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# gecko_spider_silk_script_master_v01.md

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

Words: 1379 · Est. min: 9.2 · Chapters: 4

## Cold open excerpt

> How can a tokay gecko sprint upside down across a ceiling of polished glass with zero glue, zero slime, and zero suction ? And how does the exact same ultra-short-range quantum attraction between neutral molecules ( van der Waals forces ) make a strand of spider silk five times s

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91.9/100 — proceed to VO after production checklist.

Pass threshold: 90
```
