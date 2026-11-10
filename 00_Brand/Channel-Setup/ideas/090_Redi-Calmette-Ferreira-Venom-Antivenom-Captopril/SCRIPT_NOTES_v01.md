# 090 script v01: notes for review (J0783)

Script: `venom_antivenom_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0783, Gemini Argon, 21 Oct 2026).** Built from `090_Redi-Calmette-Ferreira-Venom-Antivenom-Captopril/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-21_J0774.md` (`evidence_2026-10-21_J0774/n_venom_antivenom.md` PASS — 4 education videos ≥ 1M views, ALL 4 strictly on snakes & venom: **TED-Ed ★ *Poison vs. venom: What's the difference? - Rose Eveleth* (`KnJ4_xRfxpA`, 3.12M — exact injected protein venom vs swallowed poison match!)**, **TED-Ed ★ *Why don't poisonous animals poison themselves? - Rebecca D. Tarvin* (`-sEpBGF106k`, 2.64M)**, **TED-Ed ★ *Watch this if you're scared of snakes - Andrew Whitworth* (`s_Cs1nbbv_M`, 1.51M)**, and **MinuteEarth *Why Don't Snakes Poison Themselves?* (`EzoqvBZe_gI`, 1.15M — exact Francesco Redi 1664 swallowed-venom digestion match!)**, plus **SciShow *What Happens When a Venomous Snake Bites Itself?* (`fp1r40w_PtA`, 645.1k)**, **TED-Ed ★ *How do snakes swallow animals so much bigger than they are?* (`m2BE9GZJJbs`, 465.9k)**, **SciShow *Can You Drink Snake Venom?* (`AxS0m00jFOA`, 159.5k)**, and **TED ★ *The power of venom -- and how it could one day save your life | Mandë Holford* (`5LRhKegPCRY`, 39.3k)**, alongside `public_search.md` & `public_search_titles.md` showing `"how does snake venom work"` is an exact YouTube autocomplete match (`yes`), 4 of the top 5 GB search results for `"how does snake venom work"` under 615k views, and 4 of the top 5 GB slots for *How Horse Blood and Pit Viper Poison Unlocked Antivenom and Saved Millions* under 139k views). The topic isn't locked yet: Chief locks `090` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; Francesco Redi's 1664 Medici Court experiments refuting the gall-bladder myth, tracing hollow fangs to post-orbital venom glands, and proving with Jacopo Sozzi that swallowed protein venom is digested in the stomach land in Part 02; the midpoint twist ("Case closed — once snake venom enters your bloodstream, nothing can stop its enzymes from shutting down your lungs or clotting your blood! Wrong!") with the October 1891 Saigon cobra flood and Césaire Phisalix & Gabriel Bertrand and Albert Calmette's simultaneous 10 February 1894 Paris presentation of `antivenom` serum (plus horse-serum scaling and Vital Brazil's 1901 species-specific proof) lands in Part 03; Maurício Rocha e Silva's 1949 `bradykinin` discovery, Sérgio Ferreira's 1965 *Bothrops jararaca* `Bradykinin Potentiating Factor` (with John Vane in 1968), and David Cushman & Miguel Ondetti's 1975–1977 design of `Captopril` (`ACE inhibitors`) land in Part 04; the ending hands off directly to `091` (*How Do Trees Secretly Trade Food and Warning Signals Underground — and How Did a Lichen Scandal & Radioactive Forest Gas Unlock the "Wood Wide Web"?*), with no goodbye and no subscribe ask. Five VO parts, matching 009–089.

## Marker count (v01)

Run on `venom_antivenom_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked Redi (1664) injected vs swallowed protein venom comparison, Calmette (1894) horse-serum antivenom neutralization curve & Ferreira/Cushman/Ondetti (1965–1977) *Bothrops jararaca* BPF / Captopril ACE-inhibition potency chart (0:34); 2) inked Redi (1664) Florence Medici Court experimental survival table & hollow fang diagram (0:52); 3) inked Francesco Redi (1664 *Osservazioni intorno alle vipere*) hollow viper fang cross-section & Florence experimental matrix (1:58); 4) inked Albert Calmette & Césaire Phisalix / Gabriel Bertrand (10 Feb 1894 *C. R. Soc. Biol.* 46: 111–115) horse-serum antivenom immunization & survival chart (3:47); 5) inked Sérgio Ferreira (1965 *Br. J. Pharmacol.*) & David Cushman and Miguel Ondetti (1977 *Science*) *Bothrops jararaca* `BPP9a` / Teprotide to `Captopril` structure-activity chart (`IC50 = 23 nM`) (5:32); 6) animated timeline 1664–1977 (6:48) | ≥ 3 per long, including the timeline |
| `SCALE` | **6** | 1) a single bite injects less than 0.1 g of venom — the weight of two grains of rice — yet can clot or paralyze an adult human body a million times heavier (0:34); 2) venomous snakes bite >5 million people a year and kill >100,000, yet blood-pressure medicines designed from one Brazilian viper's venom protect >40 million hearts every day (0:52); 3) a viper's fang is a natural hypodermic needle with its exit hole just above the tip so the tooth never plugs with skin — injecting proteins lethal in blood yet digested like chicken soup in the stomach (1:58); 4) how we still make antivenom more than a century after 1894 — milking real snakes by hand, injecting harmless micro-doses into horses, and purifying antibodies from plasma (3:47); 5) replacing a 9-link viper peptide with a tiny two-part molecule carrying a sulfur hook for one zinc atom made a pill small enough to survive stomach acid (5:32); 6) over 313 years, a drop of yellow liquid from a viper's fang went from an ancient gall-bladder myth in Florence to a daily heart pill protecting tens of millions of lives (6:48) | `SCALE:` on every `DATA:` (`grep -c` matches) |
| `WHO` | **10** | Francesco Redi (1626–1697) — Italian physician and naturalist; Albert Calmette (1863–1933) — French physician and bacteriologist; Césaire Phisalix (1852–1906) — French physician and biologist; Sérgio Henrique Ferreira (1934–2016) — Brazilian pharmacologist and physician; Gabriel Bertrand (1867–1962) — French biochemist and bacteriologist; Vital Brazil Mineiro da Campanha (1865–1950) — Brazilian physician and immunologist; Maurício Rocha e Silva (1910–1983) — Brazilian pharmacologist and physician; John Robert Vane (1927–2004) — British pharmacologist; David W. Cushman (1939–2000) — American biochemist; Miguel A. Ondetti (1930–2004) — Argentine-American chemist | Every named person at first mention, role right for the scene's year |
| `WHEN` | **22** | Florence, Italy, 1664 (0:00); 1664, 10 February 1894, 1949, 1965, 1975, 1977 (0:34); 1664 (1:28); December 1890, October 1891, 10 February 1894, 1901 (3:13); 1949, 1965, 1968, 1975, 1977 (4:58); 1664–1977 timeline marker (6:48); 1867, 1879, 1885, August 1997 (7:45) | Every spoken date or era |
| `FACT` | **3** | `Stomach acid digests venom` (1:28); `Two teams on one day` (3:13); `Viper venom became heart pills` (4:58) | 2–4 per long, ≤ 4 words per card |

## Craft lessons check (*Reference lessons* §1)

- **Cold opens & cliffhanger hand-offs:** Part 01 opens cold on why a single drop of snake venom clots a beaker of blood into solid jelly in 20 seconds yet is digested harmlessly if swallowed, and ends on how Francesco Redi proved how fangs work in 1664 and how two rival French labs presented antivenom on the same afternoon in 1894; Part 02 opens cold on Redi's 1664 Medici Court experiments refuting the gall-bladder myth and Jacopo Sozzi drinking viper venom in wine, and ends on how an 1891 Saigon cobra flood sparked the birth of antivenom; Part 03 opens cold on the midpoint twist ("Case closed — once snake venom enters your bloodstream, nothing can stop its enzymes from shutting down your lungs or clotting your blood! Wrong!"), tells the story of Phisalix, Bertrand, and Calmette's simultaneous 10 February 1894 Paris discovery of `antivenom` serum and Vital Brazil's 1901 species-specific proof, and ends on why a bite from the Brazilian *jararaca* pit viper drops blood pressure to zero; Part 04 opens cold on Sérgio Ferreira's pocket vial of viper peptide in 1965 and tells the story of Rocha e Silva (`bradykinin`), Ferreira & John Vane (`BPF` blocking `ACE`), and Cushman & Ondetti's 1975–1977 `Captopril`, and ends on the underground fungal network beneath the forest floor; Part 05 opens cold on the Medici wineglass and 40 million hearts, and hands off to Simon Schwendener (1867), Heinrich Anton de Bary (1879), Albert Bernhard Frank (1885), and Suzanne Simard (`Wood Wide Web`, `091`).
- **Quirky anecdote before the hard idea:** Viper-catcher Jacopo Sozzi drinking a goblet of fresh viper venom at the Medici Court in 1664 with zero harm; a barrel of 40 live monocled cobras sent to Albert Calmette in Saigon after an October 1891 monsoon flood; Sérgio Ferreira carrying a freeze-dried vial of pit-viper poison in his coat pocket to London in 1965!
- **Rivalry / tension:** 2,000 years of Aristotle/Galen gall-bladder bile dogma vs Francesco Redi's 1664 experiments; Césaire Phisalix & Gabriel Bertrand vs Albert Calmette presenting back-to-back at the exact same Paris meeting on 10 February 1894; skepticism over oral peptide drugs vs Cushman and Ondetti's zinc-binding sulfur hook.
- **Misconception explained away:** "Aren't poison and venom the same thing — so drinking snake venom should kill you instantly?" — refuted by Francesco Redi in 1664 (protein venoms must be injected into blood and are digested into amino acids in a healthy stomach, Parts 01, 02, 04).

## For Chief to decide

1. Lock **090 = How Does a Single Drop of Snake Venom Stop a Breath or Clot a Bucket of Blood in Seconds — and How Did Horse Serum & Brazilian Pit-Viper Poison Save Millions of Lives (`Snake Venom, Francesco Redi's 1664 Swallowed-Venom Proof, Albert Calmette's 1894 Horse Antivenom & Sérgio Ferreira / David Cushman & Miguel Ondetti's 1965–1975 Viper-Venom ACE Inhibitor Blood-Pressure Medicine`)? Francesco Redi's 1664 Viper-Fang vs Swallowed-Venom Proof, Albert Calmette & Césaire Phisalix's 10 February 1894 First Horse-Serum `Antivenom`, Maurício Rocha e Silva (1949 `Bradykinin`) & Sérgio Henrique Ferreira's (1965) *Bothrops jararaca* Viper Peptide (`BPF`), and John Vane, David Cushman & Miguel Ondetti's 1968–1975 Design of `Captopril` (`ACE Inhibitors`) (1664–1977)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Snake Venom: How Pit Viper Poison Saved Millions of Hearts* (58 chars)
   - **B (Search question, §1 rule 2):** *How Horse Blood and Pit Viper Poison Unlocked Antivenom and Saved Millions* (74 chars)
   - **Alt (Search / twist question):** *Why You Can Drink Snake Venom and How Viper Poison Became Heart Medicine* (72 chars)
2. Review `venom_antivenom_script_master_v01.md` (91.6/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# venom_antivenom_script_master_v01.md

**Decision:** PASS · **Score:** 91.6 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 7.8 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1401 · Est. min: 9.3 · Chapters: 4

## Cold open excerpt

> Why can a single drop of snake venom clot a beaker of blood into solid jelly in twenty seconds ? Yet if you swallow that exact same drop of venom , why does your stomach digest it harmlessly like egg white — and how did horse blood in eighteen ninety-four and a deadly Brazilian p

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91.6/100 — proceed to VO after production checklist.

Pass threshold: 90
```
