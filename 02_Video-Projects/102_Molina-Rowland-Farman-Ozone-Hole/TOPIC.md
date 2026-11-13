# HOS 102 — Topic brief and data learnings (J2748, 13 Nov 2026)

| Field | Value |
|---|---|
| ID / folder | `HOS:102` — `02_Video-Projects/102_Molina-Rowland-Farman-Ozone-Hole` |
| Working title (search phrase first, rule 26) | **How Did We Find the Hole in the Ozone Layer?** (43 chars) |
| Title B (story + stakes, rule 23) | **The Ozone Hole (Found by an Instrument From the 1950s)** (54 chars) |
| Search phrase to verify | "ozone layer", "ozone hole", "hole in the ozone layer" |
| Status | `backlog`, waiting in `jobs/WIP.json` `next_hos` (rule G). Rule-E topic review **not yet passed**. |
| Spend | £0 |

**Not done in this job, and the rule-E review must do it:** the neighbour pass with view counts, the YouTube autocomplete check and the title collision check. `neighbours.py`, `public_search.py`, web search and vidIQ were all refused in the unattended MacBook run, so no view number below the data section is measured. Nothing here is invented to fill the gap.

## 1. What our own data says (snapshot 2026-11-12, `REPORT.md`, `studio_ctr.json` read 12 Nov)

Channel: 6 subscribers, 3,852 views, 34 videos. Last 28 days: Shorts get 77% of their views from the Shorts feed and 22% from search; longs get 45% from Suggested and 23% from search.

### Longs, ranked by views per day

| Long | Views | Views/day | Impressions | CTR | Avg % viewed |
|---|---:|---:|---:|---:|---:|
| How Did We Discover the Periodic Table? `AL_-qlWko_g` | 161 | 2.9 | 1,141 | 3.4% | 21.6% |
| What's Inside an Atom? Mostly Empty Space `GHZDsiH7L7A` | 32 | 1.1 | 816 | 1.2% | 20.9% |
| The Willow Tree That Was Made of Air `VbPubYd6Fbs` | 4 | 0.6 | 22 | 0.0% | too few |
| The Tied Arm That Proved Your Blood Circulates `wwcjcFfC-5M` | 5 | 0.4 | 14 | 21.4% (3 clicks) | 9.2% |
| How Did We Discover X-rays? `frP_YrNShsU` | 5 | 0.1 | 41 | 2.4% | 26.7% |
| How Did We Discover Germs? `_C92tIJCk8A` | 7 | 0.1 | 44 | 6.8% | 48.1% |

- **Best three:** Periodic Table (161 views, 1,141 impressions, 71% still watching at 0:15), Atom (32 views, 816 impressions), Germs (best hold, 48.1%, on 7 views). **What they share:** a plain question built on the noun a student types (periodic table, atom, germs), a big education neighbour (Periodic Table gets most of its views from Suggested), and a physical object in the first seconds.
- **Worst three:** Willow Tree (22 impressions), Tied Arm (14 impressions, 9.2% viewed), X-rays (41 impressions). **What they share:** YouTube barely showed them. Two have story titles with no search phrase in them (rule 26's evidence), and Tied Arm opens on setup before the proof.

### Shorts

- **Best three by views per day:** *One Tight Band Proved Your Blood Goes Round* `PFj6172YU4Q` 53.8/day (215 views in 3 days, but only 15.2% stayed); *What happens if you keep cutting gold in half?* `29bpGAI0wb8` 45.4/day (1,226 views, 40.8% stayed); *Are Marie Curie's Notebooks Still Radioactive?* `AMSriTQ-lcQ` 18.3/day (274 views, 76.9% viewed).
- **Best on stayed-to-watch (100+ views):** *What Is the Pasteur Swan Neck Flask Experiment?* `-3L6HzJ_d_4` 76.5% stayed, 122 views, mostly from search; *Who Discovered Infrared Light?* `c2q7w0pgcn8` 43.5% stayed, 105% viewed; *How Was Phosphorus Discovered?* `oKqmnJNGiHg` 40.3% stayed, 87% viewed.
- **Worst three:** *What other table has empty chairs?* `LanTHJckYx8` 4 views; *The first X-ray showed a wedding ring* `zI_eD3vFWmE` 9 views; *Gallium sat where the table said* `CnHwX1L9XHg` 16 views.
- **What the winners share:** a positive question naming a thing you can picture (gold, notebooks, a flask), and a "what happens if / is it still" hook. **What the losers share:** riddle or statement titles that leave out the subject (LEARNINGS rules 1 and 28).

## 2. The film

**One-line hook:** In 1985 three British scientists with a 1950s instrument on the Antarctic ice found that a third of the ozone over their heads was gone each spring, and the satellites built to watch it had not raised the alarm.

**Person, date, twist** (from memory; every date and number below needs a `SOURCES.md` row with an exact quote before any script uses it):

1. **Thomas Midgley, about 1930.** Invents CFCs as the safe, non-toxic fridge gas. They go into fridges and spray cans worldwide.
2. **Mario Molina and Sherwood Rowland, *Nature*, June 1974.** They work out on paper that CFCs drift up to the stratosphere, sunlight breaks them, and one chlorine atom destroys many thousands of ozone molecules. Industry attacks the idea for a decade.
3. **Joe Farman, Brian Gardiner and Jonathan Shanklin, *Nature*, May 1985.** At Halley Bay the British Antarctic Survey's Dobson instrument shows spring ozone falling by about a third since the 1970s. **Twist:** NASA's satellite had recorded the low values too, but its processing flagged them as suspect, so nobody had looked.
4. **Montreal Protocol, September 1987.** Signed two years after the paper; later ratified by every UN member. Molina and Rowland share the 1995 Nobel Prize in Chemistry. The hole is forecast to close around the 2060s.

**Teach on screen:** DATA: Halley Bay October ozone by year, the line falling; DATA + SCALE: one chlorine atom against the ozone molecules it destroys; WHEN timeline 1930, 1974, 1985, 1987; WHO cards for Midgley, Molina, Rowland, Farman.

**Why it should work, from our data:**
- Same shape as our two longs that were actually shown: a plain "How did we…" question on a curriculum noun (Periodic Table 1,141 impressions and 3.4% CTR; Atom 816 impressions). "Ozone layer" is taught in school science, as those are (rules 1, 15, 26).
- It is an invisible thing proved by one instrument, like Germs (48.1% average viewed, our best hold) and Periodic Table (71% at 0:15). The Dobson instrument and the falling line give rule 10 and rule 30 their physical proof in the first 15 seconds.
- The "satellite missed it" twist is a "wait, really?" beat of the kind that carried the gold Short (1,226 views) and the Curie notebooks Short (274 views).

**Neighbours to verify (titles from memory, views NOT checked):** Vox, *Why you don't hear about the ozone layer anymore*; TED-Ed, *Whatever happened to the hole in the ozone layer?*; Veritasium's film on Thomas Midgley. The reviewer runs `neighbours.py "ozone layer" "ozone hole"` and needs three education videos at 1M+ for a go.

**No repeat:** not in `02_Video-Projects` (000–013, 099–101), not among idea folders 011–095, not in `WIP.json`. Nearest is idea 034 (greenhouse effect), a different gas, mechanism and cast.

## 3. Two Short angles (22–27 s, question titles, rule 24 open)

| Short | Title | Frame 0 and first line | Payoff (after 70%) |
|---|---|---|---|
| S01 | **Is the Hole in the Ozone Layer Still There?** | Satellite map of the hole over Antarctica, moving. "The ozone hole is still there." | It opens every spring, and it is shrinking: forecast to close around the 2060s. |
| S02 | **Why Did a Satellite Miss the Ozone Hole?** | The hole map with the low values blanked out. "A satellite saw the ozone hole first." | Its software marked the readings as errors; three men with a ground instrument published first, in 1985. |

Each Short's numbers are sourced with the long's. S01 follows the *Are Marie Curie's Notebooks Still Radioactive?* shape ("is it still…", 274 views, 76.9% viewed).
