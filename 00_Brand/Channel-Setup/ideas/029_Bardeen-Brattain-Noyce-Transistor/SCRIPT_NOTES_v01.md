# 029 script v01: notes for review (J0478)

Script: `transistor_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0478, Gemini Argon, 17 Oct 2026).** Built from `029_Bardeen-Brattain-Noyce-Transistor/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-17_J0454.md` (`evidence_2026-10-17_J0454/n_transistor.md` PASS — 5 strictly on-topic education videos ≥ 1M views: **TED-Ed ★ *How do solar panels work? - Richard Komp* (`xKxrkht7CpY`, 26.98M — silicon p-n junction)**, **Real Engineering *Transistors - The Invention That Changed The World* (`OwS9aTE2Go4`, 5.97M — exact 1947 Bell Labs transistor story)**, **Veritasium *How Does a Transistor Work?* (`IcrBqCFLHIY`, 4.55M)**, **TED-Ed ★ *How computer memory works - Kanawat Senanan* (`p3q5zWCw8J4`, 3.74M)**, and **TED-Ed ★ *How exactly does binary code work? - José Américo N L F de Freitas* (`wgbV6DLVezo`, 1.64M)**, plus **TED-Ed ★ *How transistors work - Gokul J. Krishnan* (`WhNyURBiJcU`, 977.8k)**, alongside `public_search.md` showing `"how does a transistor work"` autocompleting in GB search and 4 of the top 5 GB slots for `"bell labs transistor 1947"` under 723k views). The topic isn't locked yet: Chief locks `029` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Wrong." — even after silicon transistors replaced vacuum tubes in the mid-1950s, electronics hit the "Tyranny of Numbers" because advanced computers and rockets required tens of thousands of separate components soldered together by hand, until the "Traitorous Eight" walked out on William Shockley on 18 September 1957 to found Fairchild Semiconductor, Jack Kilby sat alone at Texas Instruments during the July 1958 factory summer holiday and demonstrated the first monolithic integrated circuit on 12 September 1958, and Robert Noyce used Jean Hoerni's planar silicon dioxide process on 23 January 1959 to print complete circuits flat onto a silicon wafer with light) lands in Part 04; the popular misconception ("Many people think silicon is a rare metal mined only in California, or that a microchip's billions of switches are wired together one by one under a microscope") is raised and explained away in Part 05 via silicon's 27.7% abundance in Earth's crust (ordinary sand), ultraviolet photolithography, and Gordon Moore's 19 April 1965 law (Moore's Law); the ending hands off directly to `030` (*Continental Drift & Plate Tectonics: Alfred Wegener's 6 January 1912 Jigsaw Map & Marie Tharp's 1952 Mid-Atlantic Ocean Rift*), with no goodbye and no subscribe ask. Five VO parts, matching 009–028.

## Marker count (v01)

Run on `transistor_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked schematic and scale comparison on period paper of the 16 December 1947 point-contact transistor (0.005 cm razor-slit gold gap on germanium crystal) vs 1946 ENIAC (17,468 vacuum tubes, 30 tonnes, 150 kW) and a modern smartphone chip (>15 billion silicon transistors on a fingernail) (0:34); 2) inked gap comparison showing 1/500th inch (~50 µm, thinner than tissue paper) between Brattain's two gold contacts vs a 10 cm glass vacuum tube (0:52); 3) inked physics diagram on period paper showing Bardeen's March 1946 surface-state electron trap on n-type germanium and Brattain's 16 December 1947 gold-foil plastic wedge injecting minority "holes" across a 1/500th-inch (50 µm) gap to amplify output current ~100× (1:58); 4) inked three-layer n-p-n junction transistor diagram on period paper showing how a tiny positive voltage on the thin p-type base lowers the potential barrier and unleashes a 100× electron current from n-type emitter to collector (3:42); 5) inked comparison diagram on period paper of the "Tyranny of Numbers" (thousands of hand-soldered discrete parts) vs Jack Kilby's 12 September 1958 monolithic germanium oscillator chip and Jean Hoerni & Robert Noyce's 23 January 1959 planar silicon integrated circuit with printed metal interconnects (5:28); 6) animated timeline building 16–23 Dec 1947 · 23 Jan 1948 · 18 Sep 1957 · 12 Sep 1958 & 23 Jan 1959 · 19 Apr 1965 & Jul 1968 · 2000–Today alongside an inked Moore's Law chart rising from 1 transistor (1947) and 4 components (1958) to >15 billion transistors on a fingernail-sized silicon chip (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) 17,468 glass tubes filling a room and gulping enough power for a hundred homes — replaced today by 15 billion crystal switches on a chip the size of your fingernail (0:34); 2) a gap one five-hundredth of an inch wide sliced by hand with a razor blade — thinner than a sheet of tissue paper (0:52); 3) instead of boiling electrons in a hot glass bulb the size of a fist, Bardeen and Brattain steered them through a solid crystal across a gap thinner than tissue paper (1:58); 4) a tiny trickle of electrons into the middle crystal layer opens the floodgate for a river of current a hundred times larger (3:42); 5) instead of soldering 100,000 separate parts together by hand, Noyce's planar chip printed the entire circuit flat onto a sliver of silicon like pages on a printing press (5:28); 6) from 1 hand-sliced transistor in 1947 to more than 15 billion transistors on a single phone chip today — with each gate just 15 silicon atoms wide (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **10** | Walter Brattain (0:34), John Bardeen (0:34), William Shockley (0:34), Jack Kilby (0:34), Robert Noyce (0:34), Lee De Forest (1:28), Julius Edgar Lilienfeld (3:08), Gordon Teal (3:42), Gordon Moore (4:53), Jean Hoerni (4:53) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **27** | Murray Hill 16 December 1947 (0:00), Philadelphia February 1946 (0:21), 16 December 1947 (0:34), 12 September 1958 (0:34), 23 January 1959 (0:34), 23 December 1947 (1:05), 1906 (1:28), April 1945 (1:28), March 1946 (1:28), 16 December 1947 (1:58), 23 December 1947 (2:32), 1930 (3:08), 23 January 1948 (3:08), May 1954 (3:42), 10 December 1956 (4:18), 1957 (4:18), 1972 (4:18), 18 September 1957 (4:53), July 1958 (4:53), Dallas 12 September 1958 (4:53), 23 January 1959 (5:28), 19 April 1965 (6:43), July 1968 (6:43), 2000 (6:43), 1947–2000 (6:43), 6 January 1912 (7:45), 1952 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | Gap cut with razor blade (1:28); Only 2× Physics Nobel winner (3:08); Invented during summer holiday (4:53); Made from ordinary sand (6:43) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (Walter Brattain and John Bardeen at Bell Labs on 16 December 1947 pressing a razor-slit gold-foil plastic wedge onto a germanium crystal as the oscilloscope signal leaps 100-fold and morphs into a 15-billion-transistor silicon microchip), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Brattain and Bardeen's 16 December 1947 1/500th-inch razor-slit gold-foil gap on germanium and Kilby & Noyce's 1958–1959 microchip) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:05 (Part 04 setting aside a tangled bird's nest of hand-soldered wires to shine light through a stencil onto a flat silicon wafer).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why William Shockley's first semiconductor design failed completely in 1945 and why his jealousy split the team apart; Part 02 opens cold on Lee De Forest's 1906 hot glass triode vacuum tube, ENIAC's 17,468 tubes, Bardeen's March 1946 surface-state discovery, and Brattain's 16–23 December 1947 razor-slit gold-foil wedge held by a paperclip spring, ending on why their boss William Shockley was furious and what happened when he locked himself alone in a Chicago hotel room over New Year's Eve; Part 03 opens cold on Julius Edgar Lilienfeld's 1930 patent blocking Shockley's name from the point-contact patent, Shockley's 23 January 1948 three-layer bipolar junction transistor, Gordon Teal's May 1954 pocketful of silicon transistors, and John Bardeen's 1956 and 1972 double Physics Nobel Prizes, ending on why the "Tyranny of Numbers" threatened to paralyse computing and how eight young engineers rebelling against Shockley solved it; Part 04 opens cold on the midpoint twist ("Case closed? Wrong." — the 18 September 1957 walkout of the "Traitorous Eight" to found Fairchild Semiconductor, Jack Kilby's lonely July 1958 summer-holiday epiphany and 12 September 1958 monolithic germanium microchip at Texas Instruments, and Robert Noyce's 23 January 1959 planar silicon integrated circuit using Jean Hoerni's silicon dioxide layer), ending on why Gordon Moore predicted in 1965 that components on a chip would double every year or two; Part 05 opens cold on the rare-metal / hand-wired misconception, explains silicon's 27.7% abundance in ordinary beach sand, photolithography, and Moore's Law, and hands off to Alfred Wegener's 6 January 1912 continental drift lecture and Marie Tharp's 1952 Mid-Atlantic Ridge rift valley (`030`).
- **Quirky anecdote before the hard idea:** Walter Brattain slicing a 1/500th-inch gap in gold foil with a razor blade and holding it down with a bent paperclip spring; Jack Kilby inventing the microchip because as a May 1958 new hire at Texas Instruments he had earned no summer vacation days and had the whole lab to himself in July 1958.
- **Rivalry / tension:** William Shockley's jealousy over Bardeen and Brattain's December 1947 triumph driving him to invent the junction transistor in a Chicago hotel room, driving John Bardeen out of Bell Labs (to win a second Physics Nobel), and driving the "Traitorous Eight" to walk out in September 1957 and launch Silicon Valley.
- **Misconception explained away:** "Many people think silicon is a rare metal mined only in California, or that a microchip's billions of switches are wired together one by one under a microscope" — explained via silicon's 27.7% abundance in Earth's crust (beach sand) and ultraviolet photolithography etching all 15+ billion switches simultaneously (Part 05, 6:43).

## For Chief to decide

1. Lock **029 = The Silicon Transistor & Microchip: John Bardeen, Walter Brattain & William Shockley's 1947 Gold-Foil Transistor at Bell Labs & Jack Kilby and Robert Noyce's 1958–1959 Integrated Circuit (1946–1965)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *The First Transistor: How a Paperclip and Gold Foil Shrunk Computers* (68 chars)
   - **B (Search question, §1 rule 2):** *How Two Strips of Gold Foil Replaced 17,000 Vacuum Tubes* (56 chars)
   - **Alt (Search / twist question):** *How a Jealous Boss in a Hotel Room Accidentally Created Silicon Valley* (70 chars)
2. Review `transistor_script_master_v01.md` (92.6/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# transistor_script_master_v01.md

**Decision:** PASS · **Score:** 92.6 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 9 |
| scientificAccuracy | 9.4 |
| emotion | 9.6 |
| escalation | 8.4 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1643 · Est. min: 11 · Chapters: 4

## Cold open excerpt

> How did pressing two strips of gold foil onto a grey crystal with a bent paperclip shrink a thirty-tonne computer into your phone? By the end of this film, you'll see why early computers filled whole rooms with seventeen thousand hot glass tubes that burned out in deadly danger o

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 92.6/100 — proceed to VO after production checklist.

Pass threshold: 90
```
