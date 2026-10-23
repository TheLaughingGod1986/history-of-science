# 087 script v01: notes for review (J0766)

Script: `soap_micelles_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0766, Gemini Argon, 21 Oct 2026).** Built from `087_Chevreul-Pockels-McBain-Langmuir-Soap-Surface-Tension-Micelles/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-21_J0758.md` (`evidence_2026-10-21_J0758/n_soap_surface_tension.md` PASS — 3 education videos ≥ 1M views: **Physics Girl *7 Science Tricks with Surface Tension* (`WsksFbFZeeU`, 12.30M — exact surface tension & surfactant match!)**, **TED-Ed ★ *Which is better: Soap or hand sanitizer? - Alex Rosenthal and Pall Thordarson* (`x7KKkElpyKQ`, 5.57M — exact amphiphilic soap micelles ripping apart grease & viral lipid envelopes match!)**, and **TED-Ed ★ *Why does ice float in water? - George Zaidan and Charles Morton* (`UukRgqzk-KE`, 2.04M)**, plus **Khan Academy *Surface tension | States of matter and intermolecular forces* (`_RTF0DAHBBM`, 421.9k)**, **SciShow Kids *How Do Soap and Water Make Us Clean?* (`XntinCBEC9U`, 318.7k)**, and **TED ★ *The fascinating science of bubbles, from soap to champagne | Li Wei Tan* (`ez7HOFKTtH0`, 110.0k)**, alongside `public_search.md` & `public_search_titles.md` showing `"how does soap work"` is an exact YouTube autocomplete match (`yes`), all 5 top GB search results for `"how does soap work"` under 515k views, all 5 top GB search results for `"agnes pockels surface tension soap micelles"` under 15k views, and 3 of the top 4 GB slots for *How a Kitchen Sink Experiment Unlocked Why Soap Destroys Grease and Viruses* under 54k views). The topic isn't locked yet: Chief locks `087` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; Michel Eugène Chevreul's 1823 `saponification` proof and Agnes Pockels's 1881–12 March 1891 (*Nature*, with Lord Rayleigh) kitchen-sink `surface tension` trough and porcelain button balance land in Part 02; the midpoint twist ("Case closed — soap washes away grease simply because soap dissolves into loose molecules in water and makes the water slippery! Wrong!") with James William McBain's 1913 discovery of amphiphilic soap `micelles` (`"McBain's nonsense!"`, confirmed as spherical by G. S. Hartley in 1936) lands in Part 03; Irving Langmuir's 1917 and Katharine Blodgett's 1935 single-molecule `monolayers` (`~2.5 nm`) and how soap tails wedge open viral lipid envelopes in 20 seconds land in Part 04; the ending hands off directly to `088` (*What Happens When You Remove One Predator From an Ecosystem — and Why Are Fierce Predators Always Rare?*), with no goodbye and no subscribe ask. Five VO parts, matching 009–086.

## Marker count (v01)

Run on `soap_micelles_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked Agnes Pockels (1891) water surface tension drop (`72.8 mN/m` vs `~25 mN/m`) & Irving Langmuir (1917) `~2.5-nm` single-molecule fatty-acid monolayer chart (0:34); 2) inked James McBain (1913) Critical Micelle Concentration (CMC) conductivity curve & `50–100` soap molecules per `~5-nm` spherical micelle (0:52); 3) inked Chevreul (1823) triglyceride + `3 NaOH` saponification equation & Pockels (1891 *Nature*) `70-cm` tin trough & `6-mm` button balance compression curve (1:58); 4) inked McBain (1913 *Trans. Faraday Soc.*) soapy water conductivity vs osmotic pressure anomaly & spherical micelle diagram (3:47); 5) inked Langmuir (1917 *J. Am. Chem. Soc.*) Langmuir-Pockels trough pressure-area isotherm (`~0.21 nm²/molecule`, `~2.5 nm` height) & 20-second viral lipid envelope disruption (5:32); 6) animated timeline 1823–1935 (6:48) | ≥ 3 per long, including the timeline |
| `SCALE` | **6** | 1) a single soap film standing on water is 2.5 nm tall — 30,000× thinner than kitchen foil — yet cuts water's surface tension by nearly two-thirds (0:34); 2) a single drop of soapy water contains >10 quadrillion microscopic micelles, each a 5-nm cage with an oily inside and a water-loving outside (0:52); 3) Agnes Pockels had no lab, no salary, and no instruments — just a 70-cm tin pan, a 6-mm coat button, and a kitchen sink — yet Nobel laureates used her trough design for a century (1:58); 4) each soap molecule is like a magnet with two opposite personalities — an oil-loving tail and a water-loving head — teaming up by 50–100 to hide grease inside a water-friendly sphere (3:47); 5) spreading a drop of oil across Pockels's trough and measuring the rectangle with a ruler let Langmuir measure a single molecule's height to within a billionth of a metre (5:32); 6) from a Paris soap kettle and a German kitchen sink to single-molecule camera coatings and 20-second virus-shattering handwashing (6:48) | `SCALE:` on every `DATA:` (`grep -c` matches) |
| `WHO` | **8** | Michel Eugène Chevreul (1786–1889) — French chemist; Agnes Luise Wilhelmine Pockels (1862–1935) — German pioneer of surface science; John William Strutt, Lord Rayleigh (1842–1919) — British physicist; James William McBain (1882–1953) — Canadian-American physical chemist; Irving Langmuir (1881–1957) — American chemist and physicist; Katharine Burr Blodgett (1898–1979) — American physicist and chemist; Nicolas Leblanc (1742–1806) — French chemist and surgeon; George Stafford Hartley (1909–1997) — British physical chemist | Every named person at first mention, role right for the scene's year |
| `WHEN` | **22** | Brunswick, 12 March 1891 (0:00); 1823, 12 March 1891, 1913, 1917, 1935 (0:34); 1791, 1813, 1823, 1881, 10 January 1891, 12 March 1891 (1:28); 1913, 1936 (3:13); 1917, 1931, 1935 (4:58); 1823–1935 timeline marker (6:48); 1927, 1942, 1962, June 1963 (7:45) | Every spoken date or era |
| `FACT` | **3** | `Kitchen sink measured films` (1:28); `"McBain's nonsense" proved true` (3:13); `Soap crowbars rupture viruses` (4:58) | 2–4 per long, ≤ 4 words per card |

## Craft lessons check (*Reference lessons* §1)

- **Cold opens & cliffhanger hand-offs:** Part 01 opens cold on why plain water can't wash cooking grease off your hands while soap removes both grease and viruses in 20 seconds, and how 19-year-old Agnes Pockels unlocked surface tension at her kitchen sink, and ends on how Michel Eugène Chevreul took animal fat apart in Paris in 1823; Part 02 opens cold on Chevreul's 1823 `saponification` proof and Agnes Pockels's 1881–12 March 1891 kitchen-sink tin trough and button balance (published in *Nature* with Lord Rayleigh), and ends on why Britain's top chemists laughed at James William McBain in 1913 and called his discovery `"McBain's nonsense"`; Part 03 opens cold on the midpoint twist ("Case closed — soap washes away grease simply because soap dissolves into loose molecules in water and makes the water slippery! Wrong!"), explains McBain's 1913 amphiphilic soap `micelles`, and ends on how Irving Langmuir measured a single molecule with a ruler and why 20 seconds of soap rips viruses apart; Part 04 opens cold on Langmuir (1917) and Katharine Blodgett (1935) proving surface films are one molecule thick (`~2.5 nm`) and how soap tails rupture viral lipid envelopes, and ends on why fierce predators are rare in nature's food webs and what happened when Robert Paine threw every starfish off a Washington shore in June 1963; Part 05 opens cold on kitchen-sink chemistry and single molecules, and hands off to Elton (1927), Lindeman (1942), Carson (1962), and Robert Paine (1963) (`088`).
- **Quirky anecdote before the hard idea:** A bar of soap made out of fat washing fat off your fingers; 19-year-old Agnes Pockels using a 70-cm tin dishpan and a 6-mm porcelain coat button from her sewing box at the kitchen sink to outperform university physics labs; a Royal Society chairman shouting `"Nonsense, McBain!"` at the discovery of micelles!
- **Rivalry / tension:** 19th-century German university ban on women vs Agnes Pockels's kitchen-sink precision (`championed by Lord Rayleigh and Irving Langmuir`); Royal Society establishment (`"McBain's nonsense!"`) vs McBain's 1913 colloidal electrolyte / micelle proof.
- **Misconception explained away:** "Does soap just make water slippery so grease slides off?" — refuted by Chevreul, Pockels, McBain, and Langmuir (Parts 01–04).

## For Chief to decide

1. Lock **087 = Why Can't Plain Water Wash Off Grease — and How Did a German Woman at Her Kitchen Sink Unlock How Soap Rips Apart Dirt and Viruses (`Soap, Saponification, Surface Tension, Agnes Pockels's 1891 Kitchen-Sink Trough & James McBain's 1913 Micelles`)? Michel Eugène Chevreul's 1823 Fat-and-Alkali `Saponification` Proof, Agnes Pockels's 12 March 1891 Kitchen-Sink Button-and-Tin-Trough Discovery of `Surface Tension` Films (with Lord Rayleigh), James William McBain's 1913 Discovery of Soap `Micelles`, and Irving Langmuir's 1917 Single-Molecule Monolayers (1823–1935)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Soap: How a Kitchen Sink Unlocked Surface Tension* (49 chars)
   - **B (Search question, §1 rule 2):** *How a Kitchen Sink Experiment Unlocked Why Soap Destroys Grease and Viruses* (75 chars)
   - **Alt (Search / twist question):** *Why Plain Water Can't Wash Grease and How Soap Rips Viruses Apart* (65 chars)
2. Review `soap_micelles_script_master_v01.md` (91.4/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# soap_micelles_script_master_v01.md

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

Words: 1362 · Est. min: 9.1 · Chapters: 4

## Cold open excerpt

> Why can't plain water wash cooking grease off your hands — yet a single drop of soap makes both grease and deadly viruses vanish in twenty seconds ? Even stranger: how did a nineteen-year-old German woman barred from university unlock the secret of surface tension at her kitchen 

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91.4/100 — proceed to VO after production checklist.

Pass threshold: 90
```
