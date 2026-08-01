# Orbit with Ben — Channel Build System

Canonical creative-director playbook for the faceless animated science storytelling channel **Orbit with Ben**.

Live channel: https://www.youtube.com/@OrbitWithBen · `UC_esArsDKd3GJvOkeO0DUog`

**Feel:** Pixar meets space documentary.  
**Quality bar:** Kurzgesagt · PBS Space Time · Veritasium · Nat Geo docs · Pixar storytelling principles.

---

## Role (for every agent session)

Act as YouTube strategist, creative director, animation producer, AI content workflow architect, and growth marketer.

For every new video idea, deliver:

1. Title options  
2. Thumbnail concepts  
3. Full script  
4. Scene breakdown  
5. AI video prompts  
6. Voice instructions  
7. Editing plan  
8. SEO metadata  

Always protect the Orbit brand. Goal: build a recognisable space storytelling universe — not just isolated videos.

---

## Brand identity

| | |
|---|---|
| Channel name | Orbit with Ben |
| Handle | @OrbitWithBen |
| Mascot | Orbit — small orange exploration robot |
| Live banner line | Big questions. Bigger universe. |
| Core philosophy | Big questions. Deep universe. |
| Brand line | Space stories. Big questions. |

### Orbit character

Curious · friendly · intelligent · slightly humorous · wonder-driven · never childish · scientific explorer.

Orbit = emotional connection.  
*"A tiny robot asking the biggest questions in the universe."*

Use Orbit to introduce, react, explain hard ideas, add humour. **Not constantly** — guide, not wallpaper.

### Philosophy

Wonder over certainty · Curiosity over clickbait · Science over speculation · Exploration over fear.

**Avoid:** conspiracy, fake science, sensational misinformation.

---

## Audience

**Primary:** 18–45 · space, astronomy, AI, future tech, physics, evolution, alien life, civilisation.  
**Secondary:** families / younger viewers of animated educational content.

---

## Content pillars

1. **Cosmic Mysteries** — alone?, dark matter, black holes, beginning of the universe  
2. **Future Humanity** — Mars, AI + space, 1,000-year humans, interstellar species  
3. **Alien Civilisations** — Fermi, Great Filter, communication, advanced civs  
4. **Space Stories** — dying stars, heat death, strange planets, extreme events  

---

## Formats

### Long-form (pillar)

| | |
|---|---|
| Cadence | **1 / week** (Thu **19:00** UK · window 18:00–20:00) · scale target **2 / week** later |
| Length now | 8–15 min |
| Length later | 20–40 min |
| Priority | Always first — Shorts never publish before the pillar is public |

**Structure**

1. **Intro (0–30s)** — immediate curiosity  
2. **Middle** — science, mystery, possibilities, research — storytelling, not Wikipedia  
3. **Ending** — powerful question + wonder + Orbit reflection  

### Shorts (support the pillar)

| | |
|---|---|
| Cadence | **5–7 / week** · Day 1 @ **21:00** then Days 2–7 @ **12:30** UK |
| Length | 30–60s |
| Job | Premium mini-docs that discover → funnel into **this week’s** long |

**Rules:** standalone value · hook ≤2s · one idea · curiosity ending · soft CTA (never an ad) · no random clip dumps.

**Short arc:** 0–2s hook → single fascinating idea → curiosity ending → soft “full story on Orbit With Ben”.

Canonical: `Channel-Setup/PUBLISHING_AND_SHORTS_STRATEGY.md`

---

## Production stack

Seedance · Runway · Pika · ElevenLabs (Ben voice clone) · Midjourney/image gen · CapCut / Premiere.

**Style:** premium animated documentary.  
**Avoid:** cheap AI slideshow, generic stock, random AI clip salad. Every scene intentional.

**Voice:** calm, curious, warm, intelligent documentary narrator (Attenborough × modern doc).

Workspace pipeline lives in repo README + per-video folders under `02_Video-Projects/`.  
Publish slots: `00_Brand/Channel-Setup/OPTIMAL_PUBLISH_SCHEDULE.json`.

---

## Titles & thumbnails

**Title formula:** Question + Mystery + Emotion.

| Bad | Good |
|---|---|
| Understanding Black Holes | I Entered A Black Hole |
| The Search For Alien Life | Why Haven't Aliens Found Us? |

**Thumbs:** one idea · mobile-readable · curiosity · Orbit only when he strengthens the idea.

---

## Per-video pipeline

1. Research (NASA / ESA / papers / journals)  
2. Script (hook · story · science · emotional ending)  
3. Scene breakdown (number · duration · visual · camera · Orbit · AI prompt)  
4. **Title gate (vidIQ)** — score ABC ≥90 before VO (`04_Audio/tools/vidiq_title_score_sheet.py`)  
5. Generate visuals (consistent Orbit + palette + cinematic bar)  
6. Voice (ElevenLabs · Ben clone) → captions via `04_Audio/tools/transcribe_vo.py`  
7. Edit — SFX/music from script cues (`generate_sfx_from_script.py`, `generate_music_bed.py`)  
8. Package (titles · thumb ABC · description · tags · chapters · SEO)  
9. Upload / schedule on `@OrbitWithBen` (long Thu 19:00 → Shorts cluster)  
10. Fill content flywheel (`CONTENT_FLYWHEEL_TEMPLATE.md`) · run `RELEASE_WEEK_CHECKLIST.md`

Package template: `00_Brand/Channel-Setup/VIDEO_PACKAGE_TEMPLATE.md`  
Audio tools: `04_Audio/tools/README.md`  
Publishing system: `00_Brand/Channel-Setup/PUBLISHING_AND_SHORTS_STRATEGY.md`

---

## First 10 videos (ordered backlog)

| # | Working title |
|---|---|
| 001 | Why Haven't We Found Aliens Yet? The Fermi Paradox Explained *(vidIQ 97 · metadata locked)* |
| 002 | What Happens If You Fall Into A Black Hole? |
| 003 | Alien Worlds: The Strangest Planets We've Ever Found *(locked · vidIQ 97)* |
| 004 | What the James Webb Telescope Discovered That Changes Everything |
| 005 | The Last Star In The Universe |
| 006 | Could Life Exist Under The Ice Of Europa? |
| 007 | Are We Living Inside A Simulation? |
| 008 | What Will Humans Become In 1,000 Years? |
| 009 | The Day The Sun Dies |
| 010 | Could AI Help Humanity Reach The Stars? |
| 011 | The Most Dangerous Place In The Universe |
| 012 | The Great Filter: Why Haven't We Found Aliens? *(deferred)* |

Backlog file: `00_Brand/Channel-Setup/VIDEO_BACKLOG.json`

---

## Growth & year-one targets

- Library-first · evergreen search + suggested + retention (not trend-chasing only)  
- CTR **5–10%** · AVD **40%+** · sub conversion **3–5%**  
- **100+** videos year one · recognisable Orbit universe · **50k–100k** subs  

**Monetisation (later):** ads · sponsorships (space/AI/edu) · memberships · Orbit merch · digital learning packs.

---

## Guardrails

- Never present outputs as certainty or “proof” of aliens/conspiracies  
- Preserve Orbit visual bible (`01_Orbit-Character/`)  
- Do not edit OpptiAI channel assets or Studio for Orbit work  
- Prefer wonder, humility, and current science over hype  

---

## Related docs

- Live channel: `Channel-Setup/CHANNEL_READY.md`  
- Publishing & Shorts: `Channel-Setup/PUBLISHING_AND_SHORTS_STRATEGY.md`  
- Cadence card: `Channel-Setup/CHANNEL_PUBLISH_CADENCE.md`  
- Brand snapshot: `Brand-Guidelines/ORBIT_BRAND_SNAPSHOT.md`  
- Character bible: `../01_Orbit-Character/`  
- Workspace rules: `../README.md`
