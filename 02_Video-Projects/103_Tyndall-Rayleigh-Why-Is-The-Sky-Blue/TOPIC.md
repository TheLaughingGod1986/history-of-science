# HOS 103 — Topic brief and data learnings (J2748, 13 Nov 2026)

| Field | Value |
|---|---|
| ID / folder | `HOS:103` — `02_Video-Projects/103_Tyndall-Rayleigh-Why-Is-The-Sky-Blue` |
| Working title (search phrase first, rule 26) | **Why Is the Sky Blue? (And Why It Isn't Violet)** (46 chars) |
| Title B | **Why Is the Sky Blue? (The Glass Tube That Solved It)** (52 chars) |
| Search phrase to verify | "why is the sky blue", "rayleigh scattering", "why are sunsets red" |
| Status | `backlog`, waiting in `jobs/WIP.json` `next_hos` (rule G). Rule-E topic review **not yet passed**. |
| Spend | £0 |

**Not done in this job, and the rule-E review must do it:** the neighbour pass with view counts, the YouTube autocomplete check and the title collision check ("Why Is the Sky Blue?" alone will collide; the bracketed tail is there to make it ours). `neighbours.py`, `public_search.py`, web search and vidIQ were all refused in the unattended MacBook run, so no view number for another channel is given here.

## 1. What our own data says

The full ranking from the 2026-11-12 snapshot is in `../102_Molina-Rowland-Farman-Ozone-Hole/TOPIC.md` §1 (same job, same read). The lines this topic leans on:

- **Longs are only shown when the title is a plain question on a searched noun.** Periodic Table `AL_-qlWko_g`: 1,141 impressions, 3.4% CTR, 161 views. Atom `GHZDsiH7L7A`: 816 impressions, 32 views. The story-titled longs got 14 (Tied Arm) and 22 (Willow Tree) impressions.
- **Search is what keeps paying.** 22% of Shorts views and 23% of long views in the last 28 days came from YouTube search. Our best stayed-to-watch Short is a pure search question: *What Is the Pasteur Swan Neck Flask Experiment?* `-3L6HzJ_d_4`, 76.5% stayed on 122 views.
- **Light already works for us.** *Who Discovered Infrared Light?* `c2q7w0pgcn8`: 138 views, 43.5% stayed, 105% average viewed (loops).
- **Worst three Shorts** (*What other table has empty chairs?* 4 views, *The first X-ray showed a wedding ring* 9, *Gallium sat where the table said* 16) all hide the subject. This title cannot: the question is the subject.

## 2. The film

**One-line hook:** In 1869 John Tyndall filled a glass tube with vapour, shone a lamp through it and made a piece of blue sky on a laboratory bench, and then a 28-year-old lord worked out why the same sums say the sky should be violet.

**Person, date, twist** (from memory; every date and number below needs a `SOURCES.md` row with an exact quote before any script uses it):

1. **Horace-Bénédict de Saussure, 1789.** Carries a "cyanometer", a ring of numbered blue shades, up the Alps to measure how blue the sky is. He can measure it; nobody can explain it.
2. **John Tyndall, Royal Institution, 1869.** Shines a beam through a glass tube of fine particles. From the side the beam glows blue; the light coming out of the far end turns red. Sky and sunset in one tube.
3. **Lord Rayleigh (John William Strutt), 1871.** Gives the law: the shorter the wavelength, the stronger the scattering, as one over the wavelength to the fourth power. Blue light scatters several times more than red. In 1899 he shows the air's own molecules do it; no dust is needed.
4. **The twist.** By Rayleigh's law violet scatters most of all, so the sky "should" be violet. It is not, because the Sun sends less violet, the upper air absorbs some of it, and our eyes are weak at it. The sky's colour is partly made in the eye.

**Teach on screen:** DATA + SCALE: bars for how strongly red, green, blue and violet scatter; DATA: the longer path of sunlight at sunset; WHEN timeline 1789, 1869, 1871, 1899; WHO cards for Saussure, Tyndall, Rayleigh; FACT: "Mars has blue sunsets".

**Why it should work, from our data:**
- It is the most-typed science question we have not answered, and rule 26 says a long on a channel this small is found by search or not at all. Same title shape as the only two longs that passed 800 impressions.
- One apparatus, shown in the first 15 seconds (Tyndall's glowing tube), as in Periodic Table (71% still watching at 0:15) and the rule 30 proof-first test.
- A sibling of our infrared Short (105% viewed): invisible physics of light, a named person, a date.
- Everyone has seen the subject from the ground, the hunch under test in rule 31.

**Neighbours to verify (views NOT checked):** the reviewer runs `neighbours.py "why is the sky blue" "rayleigh scattering"` and needs three education videos at 1M+ for a go. Expect many large answers to this exact question, which is the demand and also the competition: our angle is the discovery story (the tube, the cyanometer, the violet problem), which the short explainers skip.

**No repeat:** not in `02_Video-Projects` (000–013, 099–101), not among idea folders 011–095, not in `WIP.json`. Tyndall also appears in idea 034 (greenhouse effect) for his heat work, a different experiment; 018 and 025 cover invisible light and the wave-particle story, not scattering. It is ground-level physics, not an Orbit With Ben space topic.

## 3. Two Short angles (22–27 s, question titles, rule 24 open)

| Short | Title | Frame 0 and first line | Payoff (after 70%) |
|---|---|---|---|
| S01 | **Why Isn't the Sky Violet?** | A deep blue sky fading to violet at the top of frame, clouds moving. "The sky should be violet." | Violet scatters most, but the Sun sends less of it and your eyes barely see it. |
| S02 | **Why Are Sunsets Red?** | A red sun on the horizon, moving. "Sunsets are red because the blue is gone." | At sunset the light crosses far more air, the blue is scattered out on the way, and red is what is left: Tyndall saw it at the end of his tube in 1869. |

Each Short's numbers are sourced with the long's. Both are curriculum search questions (rule 28).
