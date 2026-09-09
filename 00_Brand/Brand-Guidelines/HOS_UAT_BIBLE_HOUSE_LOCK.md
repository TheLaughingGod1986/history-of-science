# HOS UAT bible — house lock (8 Sep 2026)

**Source:** Ben → CoS, 8 Sep 2026. HOS UAT already notified.  
**Hardened:** Ben, 8 Sep 2026 — standing ALWAYS fails (glasses · lamp glow · readable cards) after P04 v10 UAT PASS then Ben FAIL remint on basics.  
**Hardened again:** Ben, 9 Sep 2026 — standing ALWAYS fails (Explorer hair · no lamp lava drip · late-shot finish) after P04 v14 UAT PASS then Ben FAIL. Keep all prior ALWAYS.  
**Channel:** [@HistoryOfScienceYT](https://www.youtube.com/@HistoryOfScienceYT) **only**  
**Cursor rule:** `.cursor/rules/hos-uat-bible-house-lock.mdc` (always apply)  
**Scope:** **Standing ALWAYS** on every HOS cut — film **001**, **002**, and every later film. Not film-002-only.

Docs / rules only. No remint · no mint · no upload · no Mini · no Flow · no Studio · no Orbit / Oppti from this file.

## Standing ALWAYS checks (every cut)

Score every rough / lock / ship gate against **all eight**. Fail any → **UAT FAIL** (stills when picture fails).

| # | Check | Pass bar |
|---|---|---|
| 1 | **CONSISTENCY** | Matches locked prior parts and house: Explorer **scale** + **teal trenchcoat** garnish language, props, period world, 3D-cartoon style. Off-model = fail. |
| 2 | **VO VISUAL EXPLAINER** | Picture **matches** and **visually explains** the spoken VO beat — not pretty B-roll under clever narration. |
| 3 | **EXPLORER ROUND GLASSES** | Whenever Explorer is visible, he wears **round glasses** (sheet DNA). Bare / no-glasses Explorer = fail. |
| 4 | **LAMP = CLEAN WARM GLOW** | Lamps read as a **clean warm glow** only. Fire spit / candle-flame lamp artifacts = fail. |
| 5 | **READABLE CARDS** | Cards show **readable writing or symbols**. Blank stacks / blank hero cards = fail. |
| 6 | **EXPLORER HAIR — FULL FINISHED CROWN** | Explorer hair is a **full finished crown**. Sloppy / unfinished mid-scalp / bald patch = fail. |
| 7 | **NO LAMP LAVA DRIP** | No molten / orange leak under the bulb onto chair / desk. Extends clean light — lava drip = fail. |
| 8 | **LATE SHOTS SHARP + FINISHED** | Final beats stay **sharp and finished**. Heavy motion blur / ghost doubles / unfinished desks on late shots = fail. |

Mute test: with VO off, you should still follow the beat. If the plate could swap with generic scenery under the same line, rewrite or remint the picture.

## 1 — CONSISTENCY (house continuity)

- Match **locked prior parts** in the same film and the channel house look (Part 01 style baseline · Explorer character · microbe / prop locks where they apply).
- **Explorer** when present: side-character garnish only; **teal trenchcoat boy** silhouette and **scale** that reads with locked plates — not a redesign, not a second mascot, not Orbit orange.
- Props, wardrobe, ward / lab / hall materials, and lighting grammar stay continuous with the KEEP / LOCK cuts already passed.
- Reject off-model Explorers, wrong coat colour, twin Explorers, style jumps mid-minute, or props that break a prior lock for that film.

Canonical character / style: `.cursor/rules/hos-explorer-character.mdc` · `01_Character/CHARACTER_BIBLE.md` · `.cursor/rules/hos-part01-style-baseline.mdc` · `00_Brand/Channel-Setup/HOS_PART01_STYLE_BASELINE_LOCKED.md`.

## 2 — VO VISUAL EXPLAINER

- When VO names a thing, the frame shows **that** thing in the same window (hero prop / action / label).
- Picture must **explain** the line: a newcomer should see what the VO is teaching, not only atmosphere.
- Reinforces house VO/teach: picture lands **with** the VO beat (`HOS_HOUSE_VO_AND_TEACH_LOCK.md`). Does **not** replace script clarity or teach-why rules — it is the UAT picture half of that bar.
- Animistry / side labels still cue with spoken terms when the beat uses them.

## 3 — EXPLORER ROUND GLASSES (sheet DNA)

- **Whenever Explorer is on screen**, round glasses are on. Sheet DNA — not optional garnish.
- Fail bare face / no-glasses Explorer, even if coat and scale otherwise match.
- Reinforces Explorer identity lock (`.cursor/rules/hos-explorer-character.mdc` · character sheet). Does not replace scale / teal trenchcoat consistency — it is an additional ALWAYS fail.

## 4 — LAMP = CLEAN WARM GLOW

- Period lamps / desk lights read as a **clean warm glow** only.
- Fail fire spit, candle-flame tongues, ember spit, or other flame-artifact lamps when the beat is a lamp.
- Lighting grammar still stays continuous with KEEP / LOCK plates (see Consistency).
- **Also see §7** — molten / orange lava drip under the bulb is a separate ALWAYS fail that extends this clean-light bar.

## 5 — READABLE CARDS

- When cards / sheets / placards are hero or stack props, they show **readable writing or symbols** (letters, numbers, or clear marks a viewer can parse).
- Fail blank stacks and blank hero cards.
- Film-specific lessons may add extra card rules for that minute; this ALWAYS fail still runs on top.

## 6 — EXPLORER HAIR — FULL FINISHED CROWN

- Whenever Explorer is visible, the scalp reads as a **full finished crown** of hair — complete, on-model, no unfinished hole.
- Fail sloppy / unfinished mid-scalp, bald patch, sparse crown hole, or half-built hair volume.
- Does not replace glasses / scale / teal trenchcoat consistency — it is an additional ALWAYS fail on Explorer finish.

## 7 — NO LAMP LAVA DRIP

- Extends **§4 clean warm glow**: light stays light — not liquid.
- Fail molten / orange leak dripping from under the bulb onto chair, desk, papers, or floor.
- Fail lava-blob underside glow, syrupy orange run, or pooled melt under a lamp that should only glow.
- Fire-spit / candle-flame artifacts still fail under §4; lava drip fails here even when the upper glow looks clean.

## 8 — LATE SHOTS SHARP + FINISHED

- Final beats / closing shots in a cut stay **sharp and finished** — readable desks, complete props, stable subject.
- Fail heavy motion blur on late hero beats, ghost doubles / smear twins, or unfinished desks / half-built props on the closing plates.
- Early-shot energy blur does not excuse a soft or incomplete finish; the last beats hold the highest finish bar.

## How this sits with other locks

| Lock | Relationship |
|---|---|
| `HOS_HOUSE_VO_AND_TEACH_LOCK.md` | VO/teach = clearer scripts + picture-with-beat + teach why. This bible’s **VO visual explainer** is the standing UAT score for the picture-with-beat half. Do not weaken VO/teach. |
| Explorer / Part 01 style / microbe locks | **Consistency** + **Explorer round glasses** + **Explorer hair** score those house rules on every cut. Do not weaken them. |
| Film-specific lessons (e.g. `PART03_LESSONS.md`) | Extra locks for that minute still apply; these eight ALWAYS checks still run on top. |

## Process

- Bake all eight checks into every Showrunner brief, picture desk QA, and Ben/CoS UAT pass before the next minute.
- Cite this bible + the Cursor rule when failing a cut for consistency, VO-visual miss, missing glasses, lamp flame artifacts, lamp lava drip, blank cards, unfinished Explorer hair, or soft/unfinished late shots.
- Remint / mint / upload only when a separate production brief says so — **not** from encoding this lock.

## Do not

- Treat these as 002-only or Part-04-only
- Soft-pass off-model Explorer, bare/no-glasses Explorer, unfinished Explorer hair / bald crown, flame-spit lamps, lamp lava drip, blank hero cards, scenery-only under specific VO, or soft/ghosted/unfinished late shots
- Remint locked 001 / 002 parents from this note alone
- Drive Flow, Studio, Mini, Orbit, or Oppti while encoding this lock
