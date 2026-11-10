# 093 script v01: notes for review (J0803)

Script: `echolocation_ultrasound_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0803, Gemini Argon, 21 Oct 2026).** Built from `093_Spallanzani-Curie-Griffin-Donald-Echolocation-Ultrasound/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-21_J0790.md` (`evidence_2026-10-21_J0790/n_echolocation_ultrasound.md` PASS — 4 education videos ≥ 1M views, ALL 4 strictly on bats and dolphins: **MinuteEarth *Why Do Bats Carry So Many Diseases?* (`Ao0dqJvH4a0`, 7.57M)**, **TED-Ed ★ *How smart are dolphins? - Lori Marino* (`05PpTqtGhGU`, 3.44M — exact dolphin echolocation & cognition match!)**, **TED-Ed ★ *The truth about bats - Amy Wray* (`Z8wLQ3NCBgg`, 1.86M — exact bat echolocation match!)**, and **TED-Ed ★ *Why bats don't get sick - Arinjay Banerjee* (`XiBXhCr_Jpw`, 1.51M)**, plus **TED ★ *Could we speak the language of dolphins? | Denise Herzing* (`CQ5dRyyHwfM`, 528.1k)**, **SciShow Kids *How Do Bats See with Sound? | Echolocation* (`fSIFU8OTwrg`, 469.7k)**, **TED-Ed ★ *Are vampire bats dangerous?* (`H5DhD5Nwl_0`, 202.5k)**, and **National Geographic *Echolocation | Brain Games* (`mGgtRG2da1c`, 85.4k)**, alongside `public_search.md` & `public_search_titles.md` showing `"how does echolocation work"` is an exact YouTube autocomplete match (`yes`), all 5 top GB search results for `"how does echolocation work"` under 470k views, all 5 top GB slots for `"donald griffin bat echolocation ian donald ultrasound"` under 1,000 views, and all 5 top GB slots for *How Blindfolded Bats and Submarine Sonar Unlocked Medical Ultrasound* under 24k views). The topic isn't locked yet: Chief locks `093` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; Lazzaro Spallanzani (1793) and Charles Jurine's (1794) blinded vs ear-plugged bat experiments, Georges Cuvier's 1795 mockery, and Jacques & Pierre Curie's 2 August 1880 discovery of `piezoelectricity` (`plus Paul Langevin's 1917 submarine sonar`) land in Part 02; the midpoint twist ("Case closed — bats fly in pitch darkness without making a sound, feeling the air with their delicate wings! Wrong!") with Donald Griffin, Robert Galambos, and George Washington Pierce's 1938–1941 `50,000-Hz` bat microphone experiments and Griffin's 29 December 1944 coining of `echolocation` lands in Part 03; Ian Donald's 21 July 1955 Glasgow boilermaker metal-flaw detector test and Ian Donald, John MacVicar, and Tom Brown's 21 June 1958 *Lancet* diagnostic obstetric ultrasound land in Part 04; the ending hands off directly to `094` (*How Can a Gecko Walk Upside Down on Polished Glass With Zero Glue — and Why Is a Spider's Silk Five Times Stronger by Weight Than Steel?*), with no goodbye and no subscribe ask. Five VO parts, matching 009–092.

## Marker count (v01)

Run on `echolocation_ultrasound_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked acoustic frequency & wavelength scale (human hearing 20 Hz–20 kHz vs bat/dolphin echolocation 30–150 kHz vs Ian Donald 1958 medical ultrasound 1.5–2.5 MHz) & Spallanzani/Griffin wire-avoidance chart (0:34); 2) inked Donald Griffin & Robert Galambos (1941 *J. Exp. Zool.* 86: 481–506) pulse-repetition rate curve (`10–20` to `200 clicks/s` feeding buzz) (0:52); 3) inked Spallanzani & Jurine (1793–1794) open vs plugged brass ear-tube obstacle flight table & Jacques and Pierre Curie (2 Aug 1880 *C. R. Acad. Sci.*) quartz piezoelectric diagram (1:58); 4) inked Griffin & Galambos (1941 *J. Exp. Zool.*) wire-obstacle hit rate bar chart (blindfolded 24%–30% hits; deafened 66% hits; gagged 65% hits) (3:47); 5) inked Ian Donald, John MacVicar & Tom Brown (21 June 1958 *The Lancet* 271: 1188–1195) 2.5-MHz pulsed ultrasound A-scan vs 2D compound B-mode contact scanner diagram (5:32); 6) animated timeline 1793–1958 (6:48) | ≥ 3 per long, including the timeline |
| `SCALE` | **6** | 1) low-pitched human speech has a 1-m wavelength that washes past a mosquito, whereas a 50-kHz click has a 7-mm wavelength that bounces off a mosquito's wing (0:34); 2) a swooping bat fires up to 200 clicks/s, timing echoes <1 ms apart to judge distance within the thickness of a fingernail (0:52); 3) a quartz wafer inside an ultrasonic probe vibrates millions of times per second, expanding/shrinking by <1 nm (1:58); 4) in water, sound travels at 1,500 m/s (>4× faster than air), letting dolphins spot buried fish or tell brass from steel a football field away (3:47); 5) medical ultrasound uses ~2.5 MHz sound (>100× higher than human hearing), reflecting where tissue acoustic impedance shifts by even 1% (5:32); 6) from silk threads in an 18th-century Italian room to a boilermaker's flaw-detector on the River Clyde, echoes beyond human hearing opened a safe window into the womb (6:48) | `SCALE:` on every `DATA:` (`grep -c` matches) |
| `WHO` | **10** | Lazzaro Spallanzani (1729–1799) — Italian priest, biologist and physiologist; Louis Jurine (1751–1819) — Swiss surgeon and naturalist; Pierre Curie (1859–1906) — French physicist; Donald Redfield Griffin (1915–2003) — American zoologist and biophysicist; Ian Donald (1910–1987) — Scottish obstetrician and physician; Jacques Curie (1856–1941) — French physicist and mineralogist; Paul Langevin (1872–1946) — French physicist; George Washington Pierce (1872–1956) — American physicist and inventor; Robert Galambos (1914–2010) — American neurophysiologist; Tom Brown (1933–2019) — Scottish engineer and inventor | Every named person at first mention, role right for the scene's year |
| `WHEN` | **24** | Harvard, 1938 & Glasgow, 21 June 1958 (0:00); August 1793, February 1794, 2 August 1880, 1917, 1938, 29 December 1944, 21 June 1958 (0:34); August 1793, February 1794, 1795, 2 August 1880, 1917 (1:28); 1938, 1941, 29 December 1944, 1960 (3:13); 21 July 1955, 1957, 21 June 1958 (4:58); 1793–1958 timeline marker (6:48); 1873, 8 June 2000, 27 August 2002 (7:45) | Every spoken date or era |
| `FACT` | **3** | `Blinded bats steer by ear` (1:28); `Gagged bats crash like deaf bats` (3:13); `Shipyard sonar scanned the womb` (4:58) | 2–4 per long, ≤ 4 words per card |

## Craft lessons check (*Reference lessons* §1)

- **Cold opens & cliffhanger hand-offs:** Part 01 opens cold on how a bat zips through a pitch-black room dodging fine silk threads yet crashes the instant you plug its ears with wax and how a Scottish shipyard flaw-detector on 21 June 1958 turned ultrasonic echoes into a window on the unborn baby, and ends on how Spallanzani and Jurine discovered the sixth sense of bats in 1793 and why Georges Cuvier buried it until two brothers in Paris squeezed a quartz crystal in 1880; Part 02 opens cold on Spallanzani's owl-vs-bat candle experiment in Pavia in August 1793, tells the story of Jurine's wax earplugs, Spallanzani's brass ear-tubes, Cuvier's 1795 mockery, and Jacques & Pierre Curie's 2 August 1880 piezoelectric quartz (`plus Langevin's 1917 submarine sonar`), and ends on what happened in Spring 1938 when 22-year-old Harvard student Donald Griffin carried a cage of bats to G. W. Pierce's ultrasonic detector; Part 03 opens cold on the midpoint twist ("Case closed — bats fly in pitch darkness without making a sound, feeling the air with their delicate wings! Wrong!"), tells the story of Griffin, Pierce, and Galambos's 1938–1941 `50,000-Hz` bat microphone and wire-obstacle experiments (`blindfolded vs deafened vs gagged`) and Griffin's 1944 coining of `echolocation`, and ends on how Ian Donald walked into a Glasgow boilermaker factory on 21 July 1955 with tumours and a raw beefsteak in his car boot; Part 04 opens cold on how a machine built to hunt cracks in nuclear boiler steel saved a woman diagnosed with terminal cancer and imaged the first unborn baby, tells the story of Ian Donald and Tom Brown's 1957–21 June 1958 *Lancet* 2D compound contact scanner, and ends on how geckos walk upside down on polished glass with zero glue and why spider silk beats steel; Part 05 opens cold on expectant parents meeting their unborn baby on ultrasound screens worldwide, and hands off to Johannes Diderik van der Waals (1873), Kellar Autumn (2000–2002), and Fritz Vollrath (`Gecko Adhesion & Spider Silk`, `094`).
- **Quirky anecdote before the hard idea:** Spallanzani blowing out a candle to compare an owl and a bat; Griffin holding "silent" bats in front of Pierce's insect-song detector and hearing the loudspeaker roar like a machine gun; Ian Donald driving to a Scottish boilermaker works with ovarian cysts and a raw beefsteak in the boot of his car!
- **Rivalry / tension:** Georges Cuvier's authority burying Spallanzani and Jurine's bat ear experiments for 140 years vs Griffin and Galambos's 1938–1941 proof; medical skepticism of industrial flaw-detector spikes vs Donald and Brown's 2D compound scanner saving a patient misdiagnosed with inoperable cancer.
- **Misconception explained away:** "Don't bats see in the dark or feel air currents with their wings, and isn't ultrasound a kind of radiation like X-rays?" — refuted by Spallanzani/Jurine/Griffin's ear-plug and gag tests and Curie/Donald's mechanical quartz sound echoes (Parts 01–04).

## For Chief to decide

1. Lock **093 = How Do Bats Fly in Pitch Darkness and Dolphins Hunt in Muddy Water Using Sound — and How Did Submarine Sonar Birth the Medical Ultrasound That Sees Unborn Babies (`Echolocation, Lazzaro Spallanzani & Charles Jurine's 1793–1794 Bat Experiments, Pierre Curie's 1880 Piezoelectric Quartz, Donald Griffin's 1938–1944 Ultrasonic Bat Microphone & Ian Donald's 1958 Medical Ultrasound`)? Lazzaro Spallanzani (1793) & Charles Jurine's (1794) Blinded vs Ear-Plugged Bat Proof, Pierre & Jacques Curie (1880 `Piezoelectricity`) & Paul Langevin's (1917) Submarine Sonar, Donald Griffin & Robert Galambos's 1938–1944 Discovery of `Echolocation`, and Ian Donald & Tom Brown's 21 June 1958 *Lancet* Glasgow Shipyard Flaw-Detector Obstetric Ultrasound (1793–1958)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Echolocation: How Blinded Bats Unlocked Medical Ultrasound* (58 chars)
   - **B (Search question, §1 rule 2):** *How Blindfolded Bats and Submarine Sonar Unlocked Medical Ultrasound* (68 chars)
   - **Alt (Search / twist question):** *How Bats See With Sound and How Shipyard Sonar Saw Unborn Babies* (64 chars)
2. Review `echolocation_ultrasound_script_master_v01.md` (90.8/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# echolocation_ultrasound_script_master_v01.md

**Decision:** PASS · **Score:** 90.8 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.1 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 7.4 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1438 · Est. min: 9.6 · Chapters: 4

## Cold open excerpt

> How can a bat zip through a pitch-black room and dodge fine silk threads without brushing a single one — yet crash into the wall the instant you plug its ears with a drop of wax? And how did a steel-plate flaw detector from a Scottish shipyard on twenty-one June nineteen fifty-ei

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 90.8/100 — proceed to VO after production checklist.

Pass threshold: 90
```
