# Part 05 plate 01 — CREATE v14 (locked CU / no pull-back)

**Status:** **MINT THIS TEXT** · supersedes v13 for Create  
**Plate:** `01_chapter_new_seeing` → target **01_v18**  
**Dated:** 22 Sep 2026 · Europe/London  
**Opener:** **BLANK** (or `Same Würzburg lab` only). Never DNA.  
**Assemble:** **CLOSED** until 01_v18 PASS  

## FAIL trail

| Ver | Invent |
|---|---|
| v07–v09 | Seeying / in-mint title letters |
| v10 Option A | Picture-only (title fixed in assemble) |
| v11 → 01_v14 | Spirals on bg desk + shelves + side benches (sha c2ff7426) |
| v12 → 01_v16 | Spirals + bg shelves/jars + dual tubes (sha e70d6c04) |
| v13 → 01_v17 | Early CU OK, then **pull-back** reveals shelves + spiral ~6–7s (sha 7ec59051) |

## Why v14

Framing at frame 0 was correct; the camera zoomed/pulled back and re-opened invent space. **Lock the extreme CU for the full duration** — tube fills frame entire clip; no pull-back, no zoom-out, no furniture reveal.

## Create prompt (paste)

```
Animistry 3D cartoon. MUTE-TEST VO-LITERAL (CRITICAL): chapter-open PICTURE ONLY — glow-only. EXTREME CLOSE-UP / HERO TUBE LOCKED FOR FULL DURATION: ONE Crookes/cathode-ray glass tube fills most of the frame for the ENTIRE clip (full ~8 seconds), resting on a narrow bare dark wood strip only. Soft green-violet glow from the tube. CAMERA LOCKED: continuous living settle / micro-motion only — NO pull-back, NO zoom-out, NO dolly-back, NO widen, NO reveal of anything beyond the tube and strip. Framing stays tube-fills-frame from first frame to last frame. BACKGROUND stays soft dark glow or plain void dark wall ONLY for the whole take — ZERO furniture ever enters frame: NO shelves, NO shelving units, NO cabinets, NO pillars, NO second desks, NO side benches, NO jars, NO bottles, NO glassware. ONE tube ONLY — never a second tube, never a purple sphere twin, never dual apparatus. Any wire coil may exist ONLY as part of that one Crookes tube — never as a freestanding spiral, corkscrew, spring, or coil stand. NO readable words anywhere: NO titles, NO CHAPTER cards, NO floating letters, NO chalkboard writing, NO labels. Title card comes later in assemble — do not mint letters into this plate. Tube glass clear or soft glow only. Silent. No Explorer. HARD REJECT: any pull-back or zoom-out that reveals shelves/pillars/furniture/spirals; freestanding corkscrew or spring or spiral stands; second tube or purple-sphere twin; shelves, jars, bottles, pillars, second desks; ball-and-stick molecule kits; any on-screen text or letters; Orbit robot; Ken Burns-only; late-clip widen.
```

## Mute-test

Extreme CU holds for **full** clip: one Crookes tube fills frame on bare wood strip; soft dark void BG; **no** pull-back/zoom-out/reveal of shelves/pillars/furniture; one tube only; coil only in tube; ZERO freestanding spiral; ZERO text.

## Locks

- Option A: ZERO on-screen text (assemble title card exact: `A New Kind of Seeing`)
- **Extreme CU locked full duration** — micro-motion OK; NO pull-back / zoom-out / reveal
- ONE tube; coil only as part of tube; void BG; bare wood strip only

## HARD FAIL (UAT humans)

- Pull-back / zoom-out / late widen that reveals shelves, pillars, furniture, or spirals
- Freestanding spiral / corkscrew / spring stands
- Second tube / purple-sphere twin
- In-picture CHAPTER/title letters

Board: `parts/part-05_plates_v01.json`  
Prior: `PART05_PLATE01_CREATE_v13.md` (superseded for Create)
