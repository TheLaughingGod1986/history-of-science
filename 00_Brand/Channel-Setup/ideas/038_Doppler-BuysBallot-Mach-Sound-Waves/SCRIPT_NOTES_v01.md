# 038 script v01: notes for review (J0523)

Script: `doppler_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0523, Gemini Argon, 18 Oct 2026).** Built from `038_Doppler-BuysBallot-Mach-Sound-Waves/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-17_J0500.md` (`evidence_2026-10-17_J0500/n_doppler.md` PASS — 7 education videos ≥ 1M views: **Vsauce *What Is The Speed of Dark?* (`JTvcpdfGUtQ`, 25.38M)**, **CrashCourse *Sound: Crash Course Physics #18* (`qV4lR9EWGlY`, 2.03M)**, **TEDx Talks ★ *Music Medicine: Sound At A Cellular Level | Dr. Lee Bartel* (`wDZgzsQh0Dw`, 1.47M)**, **Khan Academy *Introduction to waves | Mechanical waves and sound* (`c38H6UKt3_I`, 1.27M)**, **TED-Ed ★ *Light waves, visible and invisible* (`O0PawPSdk28`, 1.26M)**, **TED-Ed ★ *Particles and waves: The central mystery of quantum mechanics* (`Hk3fgjHNQ2Q`, 1.15M)**, **Khan Academy *Amplitude, period, frequency and wavelength of periodic waves* (`tJW_a6JeXD8`, 1.02M)**, and **TED-Ed ★ *How fast is the speed of thought?* (`g12bxfYVhMk`, 1.01M)**, plus **Khan Academy *Introduction to the doppler effect* (`dc7l7Qqa8xk`, 611k)** and **TED-Ed ★ *How to see with sound - Jacques S. Abramowicz* (`4JLNb8-LOB0`, 518k)**, alongside `public_search.md` showing all 5 top GB search results for `"christian doppler train horn experiment"` under 98k views and 4 of the top 5 GB slots for *How a Steam Train Full of Trumpets Proved the Doppler Effect* under 129k views). The topic isn't locked yet: Chief locks `038` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Wrong!" — 27-year-old Dutch meteorologist Christophorus Buys Ballot hired a steam locomotive, an open flatbed car, professional horn players, and trained musicians with perfect pitch along the Utrecht–Maarssen railway on 3 and 5 June 1845 to debunk Christian Doppler's 1842 wave equation, only to hear the sustained G note shift nearly a semitone sharper approaching and plunge nearly a full tone lower receding, before Hippolyte Fizeau in 1848 and William Huggins in 1868 proved stellar spectral redshift) lands in Part 03; Ernst Mach and Peter Salcher's spring 1887 Fiume microsecond Leyden-jar spark shadowgraphs of a supersonic rifle bullet's Mach cone (alongside the supersonic crack of a leather bullwhip) land in Part 04; the popular misconception ("Many people think a supersonic jet creates a sonic boom only once — at the exact second it accelerates past Mach one to 'break' the sound barrier") is raised and explained away in Part 05 via a continuous conical shockwave wake sweeping across the ground, paired with 1957 medical Doppler ultrasound; the ending hands off directly to `039` (*Atmospheric Pressure, the Barometer & the Vacuum: Evangelista Torricelli's 1643 Mercury Tube, Blaise Pascal's 19 September 1648 Puy-de-Dôme Mountain Climb & Otto von Guericke's 8 May 1654 16-Horse Magdeburg Hemispheres*), with no goodbye and no subscribe ask. Five VO parts, matching 009–037.

## Marker count (v01)

Run on `doppler_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked wave-frequency & pitch chart on period paper showing sound travelling at 343 m/s (767 mph at 20 °C) and a train moving at ~18 m/s (40 mph) shifting a horn note by ~10% in frequency (~a musical whole tone from approaching to receding) (0:34); 2) inked speed bar comparing Buys Ballot's June 1845 steam train (~18 m/s / 40 mph = Mach 0.05) vs the speed of sound in air at 20 °C (343 m/s / 767 mph = Mach 1.0) vs Mach & Salcher's 1887 rifle bullet (~440–530 m/s = Mach 1.3–1.5) (0:52); 3) inked cannon-timing & wave diagram on period paper showing the 1738 French Academy cannon experiment (muzzle flash vs acoustic boom across ~29 km = 331 m/s at 0 °C / 343 m/s at 20 °C) alongside Christian Doppler's 25 May 1842 wave-bunching formula f_obs = f_src × v / (v ∓ v_s) (1:58); 4) inked musical-pitch & wavelength chart on period paper from Buys Ballot's June 1845 Utrecht–Maarssen train experiments showing a sustained G4 horn note (~392 Hz): approaching at ~18 m/s (~40 mph) shifts pitch up to ~414 Hz (~G#4, +1 semitone), then drops on passing to ~372 Hz (~F#4, −1 semitone) (3:42); 5) inked three-stage wave-front & Mach-cone diagram on period paper from Mach & Salcher's 1887 spark photographs comparing subsonic motion (v < 343 m/s, nested circles), transonic sound barrier (v = 343 m/s = Mach 1.0, wave fronts pile up into a single wall of pressure), and supersonic flight (v = 485 m/s = Mach 1.4, V-shaped Mach cone with sin θ = 1 / M) (5:28); 6) animated timeline building 1738 · 25 May 1842 · 3–5 Jun 1845 · 1868 · 1887 alongside a continuous supersonic Mach-cone pressure carpet (v = 686 m/s = Mach 2.0) and medical Doppler ultrasound blood-flow shift (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) a steam train chugging at just forty miles an hour — barely one-twentieth the speed of sound — squashes and stretches the sound waves enough to drop a trumpet's note by nearly a full piano key as it passes your ear (0:34); 2) sound races through mild air at 343 metres per second — the length of three and a half football pitches every single second (0:52); 3) light crosses twenty-nine kilometres in less than a ten-thousandth of a second — whereas the cannon's sound wave takes a full eighty-eight seconds to march across the same valley (1:58); 4) as the locomotive passed the station platform at forty miles an hour, the horn's note plunged by nearly a full piano step in a fraction of a second (3:42); 5) a Leyden-jar spark lasting less than one-millionth of a second froze a rifle bullet moving at five hundred metres per second into a crystal-clear shadow on glass (5:28); 6) a supersonic jet at Mach 2 drags a continuous cone of compressed air across the ground at nearly seven hundred metres per second — twice as fast as a rifle shot (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **5** | Christian Doppler (0:34), Christophorus Buys Ballot (0:34), Ernst Mach (0:34), William Huggins (3:08), Peter Salcher (4:53) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **22** | Utrecht 3 June 1845 (0:00), Prague 1887 (0:00), Prague 25 May 1842 (0:21), 25 May 1842 (0:34), 3 June 1845 (0:34), 1887 (0:34), 1630s (1:28), 1738 (1:28), 25 May 1842 (1:28), February 1845 (3:08), 3 June 1845 (3:08), 5 June 1845 (3:08), 1848 (3:08), 1868 (3:08), 1887 (4:53), 1929 (4:53), 14 October 1947 (4:53), 1957 (6:43), 1738–1887 (6:43), 1643 (7:45), 19 September 1648 (7:45), 8 May 1654 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | Spoke to just 6 people (1:28); Hired a train to debunk him (3:08); A whip crack is a sonic boom (4:53); Sonic booms never stop in flight (6:43) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (Buys Ballot's 3 June 1845 Utrecht steam train of horn players dissolving to Ernst Mach's 1887 microsecond spark photo of a supersonic bullet shockwave cone), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Doppler's 25 May 1842 wave-bunching equation proved by Buys Ballot's 3 June 1845 train horn experiment and Mach's 1887 Mach cone) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:05 (Part 04 cracking a miniature bullwhip past 343 m/s and magnifying a supersonic bullet's V-shaped Mach cone).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why 17th-century scientists fired cannons across France to clock sound and why Doppler's binary-star colour mistake made critics sure his wave equation was wrong; Part 02 opens cold on what travels across a room when you clap, the 1738 French Academy cannon flash-vs-boom experiment (331 m/s at 0 °C, 343 m/s at 20 °C), and Christian Doppler's 25 May 1842 Prague lecture to ~6 listeners, ending on how 27-year-old Dutch scientist Christophorus Buys Ballot set out in June 1845 to demolish Doppler's theory using a steam railway and brass horn players; Part 03 opens cold on the midpoint twist ("Case closed? Wrong!" — Buys Ballot's February and 3–5 June 1845 Utrecht–Maarssen train horn experiments proving the ~1-whole-tone pitch drop, plus Fizeau 1848 and Huggins 1868 stellar spectral redshift), ending on what happens when an object travels as fast as or faster than its own sound waves; Part 04 opens cold on a cracked leather bullwhip breaking the sound barrier by hand and Ernst Mach and Peter Salcher's spring 1887 Fiume Leyden-jar microsecond spark shadowgraphs of a supersonic bullet's V-shaped Mach cone, ending on why people think a supersonic jet makes a sonic boom only once; Part 05 opens cold on the sonic-boom misconception, explains continuous shockwave wakes and 1957 medical Doppler ultrasound, and hands off to Evangelista Torricelli's 1643–1644 mercury barometer tube, Blaise Pascal's 19 September 1648 Puy-de-Dôme mountain climb, and Otto von Guericke's 8 May 1654 16-horse Magdeburg hemispheres (`039`).
- **Quirky anecdote before the hard idea:** Christian Doppler lecturing to barely six listeners in Prague on 25 May 1842; Christophorus Buys Ballot hiring a Dutch steam train and a flatbed car of horn players to debunk Doppler and accidentally proving him right; a leather bullwhip cracking past Mach 1 by hand.
- **Rivalry / tension:** Doppler's critics seizing on his binary-star naked-eye colour mistake to reject his wave equation vs Buys Ballot's Utrecht railway test and William Huggins's 1868 Sirius spectral-line redshift.
- **Misconception explained away:** "Many people think a supersonic jet creates a sonic boom only once — at the exact second it accelerates past Mach one to 'break' the sound barrier" — explained via a continuous conical shockwave wake dragged across the ground for the entire supersonic flight (Part 05, 6:43).

## For Chief to decide

1. Lock **038 = Sound Waves, the Doppler Effect & the Sound Barrier — Christian Doppler's 25 May 1842 Wave Equation, Buys Ballot's June 1845 Steam Train of Horn Players & Ernst Mach's 1887 Supersonic Bullet Photo (1738–1887)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *The Doppler Effect: The 1845 Train of Trumpets That Proved It* (61 chars)
   - **B (Search question, §1 rule 2):** *How a Steam Train Full of Trumpets Proved the Doppler Effect* (60 chars)
   - **Alt (Search / twist question):** *Why Sirens Drop Pitch — and How an 1845 Train Experiment Proved It* (66 chars)
2. Review `doppler_script_master_v01.md` (94.1/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# doppler_script_master_v01.md

**Decision:** PASS · **Score:** 94.1 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 9.5 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 8.8 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1802 · Est. min: 12 · Chapters: 4

## Cold open excerpt

> Why does the pitch of every ambulance siren fall the instant it races past you? And why did a skeptical Dutch scientist in eighteen forty-five hire a steam locomotive and a flatbed car full of trumpet players to prove that secret equation wrong? By the end of this film, you'll se

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 94.1/100 — proceed to VO after production checklist.

Pass threshold: 90
```
