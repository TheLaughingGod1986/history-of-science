# Shorts punch scripts — HOS 004 release week v03 (Ben PASS + edits)

**Status:** Ben passes all three scripts (2026-09-29) with the line edits below.  
**Cadence (UK):** after the 004 long is public (Thu 15 Oct 18:00). Never schedule a Short before that.  
**Length target:** ~55–65 spoken words → **22–27 s** at VO speed **1.04**. Punch-first. Captions the whole way. Zero `/go/`.  
**VO:** HOS house voice — ElevenLabs **Ben Orbit Narrator** (`kDch6ACCIpqgQ0NsU9kk`) · speed **1.04**. Same British IVC as the long; HOS channel only — no Orbit branding, links, or picture rules.  
**Related:** Studio Related → the film each Short promotes (exact live title).

No KEEP/LOCKED labels. No Premiere. No upload until Ben says the HOS `.env` is in place (and after phone UAT).

Word-count method: spoken words only (no stage directions). Est. seconds = words ÷ 156 × 60 (≈150 wpm × 1.04). Actual duration = VO take + last-4s open loop (fit into 22–27).

---

## Ben PASS edits (verbatim)

| Short | Slot | Edit |
|---|---|---|
| S02 | Sun → 002 | Replace *The repeating pattern was real; only the ruler for atoms was still wrong.* with **Twenty-two years later, the Royal Society gave him the Davy Medal.** |
| S03 | Tue → 003 | Replace *Wonder, not dread. A new kind of seeing.* with **She held still for fifteen minutes, in December eighteen ninety-five.** |
| S01 | Fri → 004 | As written. **Picture: coin, atom, nucleus only. NO stadium plates.** (VO may still say “pea in a stadium”; picture never shows a stadium.) |

---

## S01 — Fri 16 Oct 11:30 · promotes **004** · *What's Really Inside an Atom?*

**Frame 0:** gold coin mid-cut (knife already in the cut).  
**Frame-0 caption:** **HOW SMALL?**  
**Parent on screen ~9–14s:** What's Really Inside an Atom?  
**Related ▶** 004 (once the long listing exists).  
**Picture:** coin → atom → nucleus only. **No stadium plates.**  
**SHORTS_LOG check:** no prior Short titled like this; gold-coin punch is new for 004. Does **not** collide with 002 empty-chairs / gallium / tellurium rows.

Cut a gold coin in half. Then again.
How small can you go before it stops being gold?
A gold atom is mostly empty — its nucleus is like a pea in a stadium.
Keep going and you find what everything is made of —
and why the periodic table is in the order it is.
Watch What's Really Inside an Atom?

| | |
|---|---|
| Word count | **60** |
| Est. seconds @ 1.04 | **~23.1 s** (do not stretch holds) |

---

## S02 — Sun 18 Oct 11:30 · promotes **002** · *How Did We Discover the Periodic Table?*

**NEW idea** — not empty chairs / predictions / gallium (already live).  
**Frame 0:** Newlands’ octave cards / piano-note repeat (built from **002 plates**).  
**Frame-0 caption:** **EVERY EIGHTH?**  
**Parent on screen ~9–14s:** How Did We Discover the Periodic Table?  
**Related ▶** `AL_-qlWko_g`.  
**SHORTS_LOG check:** avoids live titles *The periodic table's empty chairs*, *He predicted a metal before it was found*, *Gallium sat where the table said*, *Why tellurium sat before iodine*, *What other table has empty chairs?*.

Before Mendeleev, John Newlands lined the elements up like notes on a piano.
He said every eighth element repeats — the law of octaves.
Other chemists laughed at him for comparing chemistry to music.
He was nearly right. Twenty-two years later, the Royal Society gave him the Davy Medal.
Watch How Did We Discover the Periodic Table?

| | |
|---|---|
| Word count | **56** |
| Est. seconds @ 1.04 | **~21.5 s** spoken; cut fits **22–27 s** with last-4s open loop (breath on the laugh; do not pad scenery) |

---

## S03 — Tue 20 Oct 11:30 · promotes **003** · *How Did We Discover X-rays?*

**Only Bertha’s hand** — drop the glowing cardboard (live Short *How X-rays Were Discovered by Accident*).  
**Frame 0:** Bertha Röntgen’s hand — bones and wedding ring (wonder, not fear).  
**Frame-0 caption:** **HER RING**  
**Parent on screen ~9–14s:** How Did We Discover X-rays?  
**Related ▶** `frP_YrNShsU`.  
**SHORTS_LOG check:** avoids `oowAOWTBoq0` *How X-rays Were Discovered by Accident* (cardboard accident). This Short is the person-proof beat only.

The first X-ray of a person was his wife's hand.
Bertha Röntgen held still while the plate recorded her bones —
and her wedding ring sat clear around the living bone.
That single plate proved you could see inside a living body without a knife.
She held still for fifteen minutes, in December eighteen ninety-five.
Watch How Did We Discover X-rays?

| | |
|---|---|
| Word count | **60** |
| Est. seconds @ 1.04 | **~23.1 s** (pause on the ring; do not stretch holds) |

---

## After VO / cut / gate

1. VO (Ben Orbit Narrator · 1.04) → `vo_check.py` each → cut 1080×1920 → `gate_shorts_open.py check` PASS → **HOS UAT** iCloud only. **STOP:** Ben watches all three on the phone.
2. Upload: wait for Ben's **"HOS .env is in place"** before any package dry-run. Never use the Orbit `.env`. Then PRIVATE + schedule each slot (**after** Thu 15 Oct 18:00) on **@HistoryOfScienceYT** only. Set Studio Related. Register with `gate_shorts_open.py add`.
3. Never Premiere. Never publish immediately. Never `/go/`. Never write Shorts into Orbit/OWB.
