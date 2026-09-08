# HOS 002 Part 04 — v06 scrub (02b window roofs)

**Gate:** UAT FAIL on v05 — single blocker ~18–21s (02b) in-camera roof/town silhouettes through window (peaked roofs + chimneys). Brown scrub CLEARED.  
**Parent:** `hos_002_part04_rough_v05.mp4`  
  sha256 `a7c9741c32f9689c019d5c8695b36a8e8d2bbbebfb19b93ee53b6d584b8a43fc` · 76043650 B · 127.760s  
**Export:** `hos_002_part04_rough_v06.mp4`  
**Flow:** `benoats@googlemail.com`. Create dies → STOP (no Ken Burns).  
**Scores → CoS only.** No P05 until PASS. **P01–P03 FROZEN** (P03 `30060612…`).

---

## KEEP (do not remint)

| Keep | Note |
|------|------|
| Brown scrub cleared | Books visible — KEEP that win |
| Late window ~91–97 | CLEARED KEEP |
| Night-sky ~40 | KEEP |
| Explorer teal ~49 | KEEP |
| Empty Chairs / Seats | KEEP |

---

## Remint REQUIRED — `02b_cards_sixty_three` only

**FULL Veo 3.1 Fast remint.** No hard fills. No brown panels. No pasted sky rectangles.

### Prompt locks (must be in the mint prompt)
- 1869 desk DNA: honey wood, soft lamp, cream blank cards in motion, leather books, opaque/lab vessels OK.
- Through the **real window panes**: deep night sky + full moon + soft clouds + stars **ONLY**.
- Explicit negatives: **no buildings, no houses, no peaked roofs, no chimneys, no town silhouette, no skyline, no rooftops on the sill, no model-town.**

### Accept / reject
- Generate → still-check every second ~0–8 of the plate (rough ~18–21).  
- **Reject and remint** if any peaked roof / chimney / town silhouette is readable.  
- Max 2 Creates; if still roofs → STOP and report (do not hard-fill).

### HARD REJECT
- Roof/town/chimney silhouettes through window  
- Hard fills / brown scrub panels / flat sky boxes  
- House props on books  
- Ken Burns-only, Orbit, photoreal

---

## Assemble

1. Remint 02b only → swap into **v05** pack.  
2. QA ~18–21: continuous desk, no brown panel, **n=0 roofs**.  
3. Spot-confirm KEEP zones.  
4. Export `hos_002_part04_rough_v06.mp4` + sha + iCloud HOS UAT + `PART04_V06_COS_SCORES.md` + `WATCH_part04_v06.txt`.  
5. Scores → CoS only. Do not declare PASS. Do not ping Ben.

## Report
path · bytes · duration · sha256 · method=Veo Fast · tries · Flow · P03 · roof n≈0 at ~18–21 · KEEP confirm.
