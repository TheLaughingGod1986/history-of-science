# Omni long-form playbook

**Locked:** 2026-08-14 after Europa (`006_Could-Life-Exist-Under-The-Ice-Of-Europa`) — best long to date.  
**Intent:** Build every future Orbit long in this format and style. Reiterate when QA teaches a better rule.

Cursor rules: `orbit-omni-longform-playbook.mdc` · `orbit-omni-section-qa.mdc` · `orbit-cutscene-no-reuse.mdc` · `orbit-shorts-punch-first.mdc` · `orbit-character-consistency.mdc`

## Why this format

- Minute-by-minute QA catches twins, env lies, and floaty Orbit before they compound.
- Omni Flash + native SFX under Ben Orbit Narrator reads as a character *in* the world.
- Soft A/V joins keep the soundtrack continuous; freeze-pad looks broken.

## End-to-end steps

### A. Gate (unchanged)

Growth System v2 · topic score · cluster plan · vidIQ audit · script ≥90 · `gate:episode` PASS.

### B. Part loop (~1 min each)

1. Write part script (VO-literal journey beats table).
2. TTS → `02_Voiceover/parts/` (Ben Orbit Narrator lock).
3. Plate plan JSON: ~8–10 unique ~8s Omni takes; tag `env: underwater|surface|space`.
4. Generate Omni Flash (Flow) with Orbit identity lock; archive rejects; bump `v0N`.
5. Assemble: paired `xfade` + `acrossfade`; Omni SFX under VO (~0.18–0.2); water bed only underwater.
6. Picture QA (start/mid/end twin + face spot-check). Approve → `PART0N_LESSONS.md` → next part.

### C. Broadcast polish

1. Brand intro (~1–2s still / sting).
2. Chapter cards (locked stills — **never** Ken Burns on text).
3. Soft-join approved part roughs in story order.
4. Like/subscribe outro hold + matching VO CTA in final part.
5. Export → `09_Final-Export/<slug>_broadcast_v01.mp4`. Verify intro/chapters/outro present; A/V locked.

### D. Shorts cluster (4–8)

1. Punch-first cuts **~22–28s** from locked **part roughs** (not chapter silence).
2. Strongest fact/question in 0–1.5s; captions reinforce; curiosity-gap end; soft CTA last ~3s.
3. Abort if any Short ≥40s.
4. Package `10_Shorts/` + `SHORTS_UPLOAD_INDEX.json` when scheduling.

## Hard rejects

| Reject | Why |
|--------|-----|
| Freeze-pad / scenery loop | Broken / against cutscene rules |
| Twin Orbit / second face / blank white eyes | Character break |
| Bubbles in vacuum/surface | Env lie |
| Clipper underwater | Identity/env break |
| Zoompan on title/chapter text | Glyph vibration |
| ≥40s Shorts | Retention evidence |

## Reference assets (Europa)

- Broadcast: `…/006_…/09_Final-Export/europa_broadcast_v01.mp4`
- Lessons: `…/006_…/07_Edit-Project/PART01_LESSONS.md` … `PART08_LESSONS.md`
- Brand: `002_…/04_Generated-Clips/03_Polished/brand/orbit_brand_intro_bold-v05_2s.mp4` + `orbit_brand_outro_subscribe_v02.png`

## Change control

When a future episode improves the bar: update this file + the matching `.mdc` rule in the same PR/commit, and note the episode ID + date. Do not fork a silent second standard.
