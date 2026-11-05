# Production checklist v2 — History of Science

**Episode:** 011 · Anesthesia (Ether Day, 1846 and surgery before anesthesia) · `011_Surgery-Before-Anaesthesia`  
**Date:** 5 Nov 2026 (scaffold, `J2239`)  
**Script review score:** **91.1** / 100 (must be ≥ 90) — PASS on `surgery_script_master_v02.md` (`J0183` / `J0224`)

Canonical: `STUDIO_PLAYBOOK.md`

---

## Story & open

- [x] Cold open: curiosity by **5s** (answer image by 0:03), question by **8s**, promise by **15s**, stakes by **25s**, first concrete answer by **30s**, first real fact before **45s**
- [x] **Nov 2026 `HOS-2026-11-E2` (`J2204`) first-30s proof-first + early DATA/SCALE check:**
  - Sub-4.5s visual cuts across `0:00–0:30` (`≥7` distinct moving plates planned in `01_Script/SCRIPT_NOTES_v01.md`, zero holds `>4.5s`)
  - Immediate physical proof/apparatus at `0:05–0:15` (close on students' brass pocket watches clicking open + leather operating-chair straps + two-necked glass ether globe; no exterior hospital establishing shot)
  - First animated `DATA` + `SCALE` graphic between `0:25–0:40` (brass stopwatch dial sweeping round and stopping short of three minutes · `SCALE: about as long as boiling an egg` on the Liston speed beat at `~0:24–0:31`)
- [x] No channel intro / history / textbook definition open
- [x] Immediate mystery — audience needs the answer
- [x] Structure: Question → Danger → Story → Explain-in-story → Escalation → Ending
- [x] Framework beats present: Hook → Question → Escalation → Discovery → Payoff → Bigger question
- [x] The proof is on screen early; the Explorer is in 2 beats only (`[EXPLORER ACTS]`, outside the first minute)
- [x] Emotional “you” stakes present without fearbait or gore
- [x] **5** film-act sections (`PART 01` cold open + 4 `[CHAPTER CARD]` acts)
- [x] Runtime target **7–9 min** (~1,210 spoken words, est. 8.0–8.4 min)

## Packaging

- [x] Title: one promise · ≤ 60 chars (*Anesthesia: The Day Surgery Stopped Hurting*, 43 chars; T&C B *What Surgery Was Like Before Anesthesia*, 39 chars) · **no series suffix**
- [ ] Thumbnail: one object · one emotion · minimal text (2–3 words that add to the title, never repeating it) · matches title promise
- [x] Description scaffold complete (`Descriptions/surgery_long_description_v01.txt`: hook · provisional chapters · verified sources from `FACT_NOTES_v01.md` · archive credits + AI disclosure line)
- [x] SEO / tags / neighbour phrases checked (`Tags/surgery_long_tags_v01.txt`, `PACKAGE_MANIFEST.json`, `lint:package -- --film 011` PASS)

## Funnel (no dead ends)

- [ ] End screen → the best related HOS long (`001_How-Did-We-Discover-Germs`, Joseph Lister hand-off) + Subscribe (normal publish, no Premiere)
- [ ] Cards configured (none in the first minute)
- [ ] Pinned comment (question + next / companion link)
- [ ] Related Shorts linked to this long (once public)
- [x] Shorts scripts v02 (`10_Shorts/SHORTS_SCRIPTS_v02.md`): **2 Test B search-titled Shorts** (*How Was Surgery Done Before Anesthesia?* and *Who Invented Anesthesia?*), autocomplete-checked (`evidence_2026-11-05_shorts_public_search.json`), payoffs withheld past 15 s (`J0899`/`J0909`)

## Gates signed

- [x] Pre-build vidIQ audit signed off (`11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`)
- [x] Script reviewer ≥ 90 (**91.1** on `surgery_script_master_v02.md`)
- [x] `FACT_NOTES_v01.md` (`J0198` Gemini facts PASS: 35 OK, 1 PARTIAL hedged, 0 FLAG) + `CLAUDE_QUOTE_CHECK_v01.md` (`J0224` Claude primary-source quote check PASS)
- [ ] VO (`vo_check.py` PASS across all 5 parts)
- [ ] VO–picture gate QA passed
- [ ] **UAT ALWAYS — CONSISTENCY:** Explorer scale + teal trenchcoat garnish / props / style match locked priors (`STUDIO_PLAYBOOK.md`)
- [ ] **UAT ALWAYS — VO VISUAL EXPLAINER:** picture matches and visually explains the spoken VO beat (not pretty B-roll)
- [ ] **UAT ALWAYS — EXPLORER ROUND GLASSES:** Explorer wears round glasses whenever visible (fail bare / no-glasses)
- [ ] **UAT ALWAYS — LAMP = CLEAN WARM GLOW:** lamps are clean warm glow only (fail fire spit / candle-flame / smoke artifacts)
- [ ] **UAT ALWAYS — READABLE CARDS:** cards show readable writing/symbols (all text added in edit, never by Veo)
- [ ] **UAT ALWAYS — EXPLORER FACE / HAIR — FINISHED:** full finished crown; fail sloppy / bald patch / face-cloud blot / black-hole scalp dots
- [ ] **UAT ALWAYS — NO LAMP LAVA DRIP:** no molten / orange leak under bulb onto chair / desk
- [ ] **UAT ALWAYS — LATE SHOTS SHARP + FINISHED:** final beats sharp; fail ANY horizontal ghost / double-exposure on lamp / flasks / grid
- [ ] **UAT ALWAYS — FINISHED 3D CARTOON QUALITY (NO UNFINISHED FLAT):** picture reads as finished premium 3D cartoon house; fail soft/flat/unfinished anim look
- [ ] Studio finish items done after API upload (ABC if long · Related+pin Shorts)

**Ship only when every box is checked.**

## STOP (this film)

- No Vertex/Veo/Flow minting until VO is recorded and passed for this film.
- Do not merge or close desk PR #180 from this work.
