---
description: Next Orbit video kickoff — Growth System v2 gate before VO/picture
alwaysApply: true
---

# Orbit — next video kickoff (Growth System v2)

**Locked next (27 Aug 2026): History of Science 001 Germs** (Veo 3.1 Fast), then one more HOS long, then compare to Orbit Omni before changing Omni. **007 Neutron Star is paused** (script still passed 91.1 under `_archive_orbit/` — do not spend Omni credits; do not copy it back into `02_Video-Projects/`). Do not start 013 Moon. Simulation is 015. See `orbit-next-production.mdc` · `hos-finish-then-compare-omni.mdc`. **Build 1 minute at a time, QA, then check with Ben before the next minute.**

When the user asks to **build / start / plan the next video**, **new episode**, **next long**, or similar — **do this first**. Do not jump to VO, Flow Veo, Seedance, or picture gen.

## Step 0 — gate (blocking)

1. Read `00_Brand/Channel-Setup/YOUTUBE_GROWTH_SYSTEM_V2.md` and `CONTENT_INTELLIGENCE_STRATEGY.md`
2. Topic score (or confirm locked topic) via `templates/TOPIC_OPPORTUNITY_SCORE.md` / `npm run intelligence:score-topics`
2b. Fill `templates/EPISODE_CLUSTER_PLAN_TEMPLATE.md` (experiential angle · 4–8 Shorts · cluster ID)
3. Pre-build vidIQ audit → project `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md` from `PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md`
4. Cold-open outline: curiosity **5s** · stakes **15s** · journey **30s**
5. Chapter outline: **4–6** acts · Orbit **experiences** science · Hook→Question→Escalation→Discovery→Payoff→Bigger question
6. Write/refine script with `[VISUAL MUST]` · `[ORBIT ACTS]` · `[TEACH]`
7. **Script reviewer ≥ 90** before any VO or picture:
   ```bash
   cd 07_Content-Ops && npm run review:script -- --file <script.md>
   ```
   Below 90 = **REJECT** — rewrite. Do not generate audio/video.
8. **Episode gate (blocking CLI)** before VO / Flow Veo:
   ```bash
   cd 07_Content-Ops && npm run gate:episode -- --project ../02_Video-Projects/<NNN_Slug>
   ```
   Must PASS (audit signed · script ≥90 · `[ORBIT ACTS]` / `[VISUAL MUST]` / `[TEACH]` counts).

## New episode scaffold

Copy `02_Video-Projects/_template_NNN_Episode-Slug/` → `02_Video-Projects/NNN_Your-Slug/`, then run the gate.

## Then produce (Omni long-form — locked)

Prefer the **Europa Omni later standard** (`OMNI_LONGFORM_PLAYBOOK.md`):

1. ~1-min parts → Ben Orbit Narrator VO → **Omni Flash** plates (Flow) → assemble (xfade/acrossfade) → part QA → next part  
2. Picture-first open · mid-film chapter cards · soft-join parts · 10s last-picture hold for Studio end screens → broadcast master. No brand intro. No baked like/subscribe outro.  
3. **4–8** punch Shorts (~22–28s) → checklist → YouTube package. Zero `/go/` on Shorts.  

Do **not** use ElevenLabs Image & Video for CG. Do **not** default to `GEMINI_API_KEY` (Flow first; AI Studio / API are fallbacks only). Legacy full-pass Veo beat gen only if explicitly requested.

After shipping, refresh the next brief from Studio metrics:

```bash
cd 07_Content-Ops && npm run brief:next -- --file metrics.json --topic "Next idea"
# writes docs/NEXT_EPISODE_BRIEF.md
```

## Thumbs + social schedule (after YouTube lock)

Once the **YouTube** long (and Shorts cluster) schedule is locked:

1. **Thumbnails:** produce **3** Orbit-on-brand variants (one object · one emotion · one question). Score in VidIQ; use `vidiq_generate_thumbnail` only if house/Gemini thumbs are weak. Longs: start Studio **Thumbnail ABC** (or title+thumb ABC) after upload.
2. **Social mirror:** Meta / Threads from the **same YouTube air times**. **One unique post per Short** on Instagram, Facebook, and Threads — no remake/file/title duplicates (`orbit-social-no-duplicates.mdc`). **TikTok is paused** (account ban) until Ben lifts `TIKTOK_UPLOAD_BLOCK.json`. Never post social Shorts before the YouTube long is public.

## Defaults (documentary + cluster window)

- Runtime **7–9 min NOW** (007 Neutron Star and new longs; ~7–9 one-minute parts, not ~20). Expand to 15–20–30 only later with impressions + hold past ~5 min. Title one promise (no series suffix) · thumb = one question · experiential framing preferred
- **4–8** Shorts: open inside the question · curiosity-gap end · Related→long · same content cluster
- Evidence labels honest (LOW_DATA / EARLY_POSITIVE_SIGNAL) — never overfit one Short
- No dead ends: end screen · cards · pin → another Orbit documentary
- Do **not** redesign the brand

## Kickoff phrases that trigger this

“Build next video” · “Next episode” · “Start V0xx” · “New long-form” · “Growth System v2 first”

Canonical: `YOUTUBE_GROWTH_SYSTEM_V2.md` · `CONTENT_INTELLIGENCE_STRATEGY.md` · `RETENTION_AND_GROWTH_LOCKED.md` · `LONGFORM_STORY_AND_VO_PICTURE_GATE.md` · `docs/GEMINI_VEO_CG.md` (Ultra UI default)
