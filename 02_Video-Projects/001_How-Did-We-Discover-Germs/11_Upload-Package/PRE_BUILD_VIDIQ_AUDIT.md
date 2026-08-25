# Pre-build vidIQ audit — How Did We Discover Germs?

**Date pulled:** 2026-08-25  
**Episode:** 001 · `001_How-Did-We-Discover-Germs`  
**Credits used (approx):** 0 (VidIQ live pull deferred — packaging shaped for script lock)  
**Brand guardrails:** Wonder over fearbait · no conspiracy · History of Science / Explorer DNA · Animistry-class form

> Live VidIQ MCP may be unavailable in this cloud environment. Re-run `vidiq_keyword_research` / `vidiq_score_title` before YouTube package lock. **This audit is signed for script → VO gate only.**

---

## Episode

| Field | Value |
|-------|-------|
| ID / slug | 001_How-Did-We-Discover-Germs |
| Working title | How Did We Discover Germs? |
| Runtime target | 8–9 min |
| Cluster | `hos-germ-theory-001` |

---

## 1. Success targets

| Metric | Target |
|--------|--------|
| Title score | ≥ 90 (aim 95+) — re-score before upload |
| Primary keyword | how did we discover germs / germ theory |
| Hook promise | Invisible life was killing people in “clean” hospitals — until science proved germs were real |
| Retention | 5 acts · teach + turn each chapter |
| Packaging | One question thumb · microbes vs ward |

---

## 2. Keyword research (draft — confirm in VidIQ)

| Keyword | Role | Keep? |
|---------|------|-------|
| how did we discover germs | primary / title | Yes |
| germ theory | secondary / desc | Yes |
| Louis Pasteur | chapter / tags | Yes |
| Joseph Lister antiseptic | chapter / Shorts | Yes |
| microscope bacteria history | umbrella | Yes |
| what are germs | Shorts hooks | Yes |

**Decision:** Primary keyword for title lead = **how did we discover germs**  
**Description first 100 chars must include:** how we discovered germs / germ theory

---

## 3. Title ABC

| | Title | Score | Keep? |
|---|-------|------:|-------|
| A | How Did We Discover Germs? | TBD live | **Yes — locked for script** |
| B | The Day Doctors Realised Germs Were Real | TBD | Backup |
| C | How Invisible Creatures Changed Medicine Forever | TBD | Soft |
| Reject | Hospitals Are Hiding Deadly Germs Everywhere | — | **Reject** (fearbait) |

**Locked title:** How Did We Discover Germs?  
**Why:** Animistry-class curiosity question · one promise · no series suffix

---

## 3b. Script reviewer (blocking before VO)

```bash
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/001_How-Did-We-Discover-Germs/01_Script/germs_script_master_v01.md
```

- [x] Score ≥ **90 / 100** (fill after review run)
- Reject / rewrite if below threshold

---

## 4. Outlier / competitive patterns

| Pattern | Steal | Do not copy |
|---------|-------|-------------|
| Animistry immersion cold-open | Picture-first world · curiosity title | War/politics topics |
| Kurzgesagt “you” stakes | Lived “what would you…” | Flat-vector house style / shop close |
| Discovery journey structure | Assumption flip → proof → new medicine | Gore / dread essay |

**Patterns we will use:**

- [x] Assumption-flip / open-loop title  
- [x] Chapter journey  
- [x] Body-scale anchor (wards, hands, cuts, flasks)  
- [x] Slow reveal / delayed answer  

---

## 5. Incorporate into the build

| Data finding | Change |
|--------------|--------|
| Primary keyword | Title + early VO + desc lead |
| Pasteur / Lister | Mid chapters + Shorts punches |
| Animistry form | 8–9 min · immersion · upbeat discovery |
| Explorer sparse | Side character every few scenes only |

**Chapter list (5 acts):**

1. The invisible enemy  
2. Seeing the tiny world  
3. Bad air vs living seeds  
4. Proof in a flask  
5. Clean hands, clean cuts  

---

## 6. Retention plan

| Minute zone | Job | Note |
|-------------|-----|------|
| 0–0:05 | Curiosity | Microbes / ward air on frame 1 |
| ~0:15 | Stakes | People died where medicine “helped” |
| ~0:30 | Journey | We rewind to the discovery |
| Chapters | Re-hook | Card + new question |
| Mid | Teach in story | Explorer sparse |
| Final | Payoff + bigger question | Invisible life everywhere |
| Outro | Soft CTA | 10s last picture · Studio end screens |

- [x] No 30s+ stretch without teach/turn  
- [x] Every chapter earns the next  
- [x] Runtime target **8–9 min** (trust window)

---

## 7. Sign-off

- [x] Keywords pulled and primary locked (draft; confirm live VidIQ before upload)  
- [x] Title ≥90 locked intent (fearbait / series-suffix clutter rejected) — live score before upload  
- [x] Script reviewer ≥ 90  
- [x] Outlier patterns mapped into chapter arc  
- [x] Thumb concepts match title promise (one object · one emotion)  
- [x] Chapter teach-points listed (5 acts)  
- [x] Cold-open clock (5 / 15 / 30s) written  
- [x] Retention plan filled  
- [x] Production checklist path noted: `00_Brand/Channel-Setup/templates/PRODUCTION_CHECKLIST_V2.md`  

**Signed off by:** Cloud Agent (History of Science Episode 001 script lock)  
**Date:** 2026-08-25  

**Only then:** full script → ElevenLabs VO → Gemini Veo picture → edit.
