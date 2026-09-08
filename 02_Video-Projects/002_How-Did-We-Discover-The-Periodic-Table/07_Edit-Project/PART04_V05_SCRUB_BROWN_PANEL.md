# HOS 002 Part 04 — v05 scrub (unblended brown scrub panel)

**Gate:** UAT FAIL on v04 — single blocker ~18–21s **unblended brown scrub/panel** still covers the book stack. House silhouettes CLEARED; late window town CLEARED. Gate = sil/scrub **gone** (panel itself fails).  
**Parent:** `hos_002_part04_rough_v04.mp4`  
  sha256 `fda60b04bd3785b1f01b61c5c76b786a841d21152df29ed398ce5b5e4490554d` · 76318531 B · 127.760s  
**Export:** `hos_002_part04_rough_v05.mp4`  
**Flow:** `benoats@googlemail.com`. Create dies → STOP (no Ken Burns).  
**Scores → CoS only.** No P05 until PASS. **P01–P03 FROZEN** (P03 `30060612…`).

---

## Root cause (do not repeat)

v04 used hard rectangular fills (brown leather panel + sky boxes). They killed houses but left **visible unblended overlays** that UAT rejects.

**v05: FULL Veo 3.1 Fast remint of `02b_cards_sixty_three` only.**  
No hard fills. No brown panels. No flat sky rectangles over the desk. Scene must look like one continuous desk shot.

---

## KEEP (do not remint)

| Keep | Note |
|------|------|
| Late window ~91–97 | CLEARED on `09`/`09b` — KEEP |
| Night-sky ~38–44 / ~40 | KEEP on `05`/`06` |
| Explorer teal ~49 | KEEP |
| Empty Chairs / Seats | KEEP |
| MAD | KEEP |

---

## Remint REQUIRED — `02b_cards_sixty_three` only (~18–21)

**Prompt / picture:**
- 1869 desk DNA: honey wood, soft lamp, cream blank cards flipping/stack, leather books **without** house props or house silhouettes.
- Window (if in frame): natural night sky + moon through real window panes — **in-camera**, not a pasted rectangle.
- Continuous Veo Fast motion.

**HARD REJECT:**
- Unblended brown scrub panels / flat leather overlays / hard rectangular fills of any colour
- House silhouettes, peaked roofs, chimneys, yellow house glow, house-icon tokens
- Flat blue sky boxes cutting across desk/cards
- Ken Burns-only, Orbit, photoreal

**If Create dies or gallery download fails → STOP and report.** Do not heal with hard fills again.

---

## Assemble

1. Remint **02b only** → swap into **v04** pack (keep v04’s cleared 09/09b + 05/06).  
2. Still QA ~18–21: no brown panel, no houses, desk reads continuous.  
3. Spot-confirm ~91–97 and ~40 still clean.  
4. Export `hos_002_part04_rough_v05.mp4` + sha + iCloud HOS UAT + `PART04_V05_COS_SCORES.md` + `WATCH_part04_v05.txt`.  
5. Scores → CoS only. Do not declare PASS. Do not ping Ben.

## Report
path · bytes · duration · sha256 · plates · method=Veo Fast (confirm no hard fill) · Flow · P03 · QA ~18–21 · confirm KEEP zones.
