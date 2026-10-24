# ElevenLabs fair-test gate — HOS 006 — 4 Oct 2026 (London)

Answering Claude order **PR #180 comment 5981137240** (+ lock note **5981148012**).

## 1. Subscription snapshot (HOS key only)

| Field | Value |
|---|---|
| Plan | **Creator** (`tier=creator`) |
| Status | active |
| Used / limit | **42,052 / 209,536** credits |
| Remaining | **167,484** |
| Next reset | **2026-10-30 10:50 GMT** (Europe/London) |
| Billing | monthly USD; next invoice subtotal $22.00 / due $26.40 |
| Credit pool | **Shared** across TTS + Image & Video + other products (no separate video pool in API JSON) |
| Rollover | **Rolls over** up to **2 months** of unused credits (docs). Account `character_limit` 209,536 > Creator base 121,000 ⇒ rollover already present. Unused lapse on downgrade/cancel at cycle end. |

Sources: `GET /v1/user/subscription`; [Billing](https://elevenlabs.io/docs/overview/administration/billing); [Pricing FAQ](https://elevenlabs.io/pricing).

Key used: HOS `~/.config/elevenlabs/api_key` (= episode `.env` `ELEVENLABS_API_KEY`). Orbit bearers **not** used. Key fingerprint `sha256_12=22ce87abc51f` (value redacted).

## 2. Video models + per-clip cost @ 1080p ~8s

**API access on this plan: BLOCKED.** Official docs + live probe: Image & Video / Flows API needs **Pro or above**. Creator returns:

`HTTP 402` `paid_plan_required` — *"This endpoint requires a Pro plan or above."*

Probes (Veo 3.1 Quality + Fast create) spent **0** credits; `character_count` unchanged at 42,052.

If the workspace were Pro+, documented API video models include:

- `veo-3.1-generate-001` (Veo 3.1 Quality) — 4/6/8s; 720p/1080p/4K
- `veo-3.1-fast-generate-001` (Veo 3.1 Fast) — same durations/resolutions
- Seedance family (`bytedance-seedance-v2` / fast / mini / v2.5) — ByteDance often needs explicit API approval
- Kling: in **app** docs, **not** in the API model table in the official quickstart; Claude already ordered Kling left out

**Per-clip credit cost at 1080p 8s: NOT PUBLISHED** by ElevenLabs as a fixed number. Docs say cost varies by model/settings/duration; UI shows cost before submit; pricing FAQ lists approximate costs for TTS/STT/Music/SFX/Dubbing but **omits** Image & Video rates. Sources: [Image & Video](https://elevenlabs.io/docs/overview/capabilities/image-video), [How much does Image & Video cost?](https://help.elevenlabs.io/hc/en-us/articles/41121058357137-How-much-does-Image-Video-cost), [API quickstart Pricing](https://elevenlabs.io/docs/eleven-api/guides/cookbooks/image-and-video), [Pricing](https://elevenlabs.io/pricing). **Did not invent prices.**

## 3. Reserve math → go / no-go

- Remaining: **167,484**
- Hold for 007 VO + Shorts/pickups: **29,000**
- Surplus above reserve: **138,484** (same shared pool)

**NO-GO — fair test not run.**

Primary reason: **Creator cannot call the video API** (402). Secondary: cannot prove surplus covers 3 clips without published per-clip rates. No plan buy/upgrade. Browser UI not used (Mini reserved for in-flight Vertex Part 02; API-first path blocked).

## 4. Fair test

**Skipped.** Plates/stills/prompts located (`01_willow_air`, `06_aristotle`, `07_roots_mouths`); Flow/Vertex controls exist at:

`.../04_Generated-Clips/flow_vs_vertex_fair_test_20261004/`

No ElevenLabs clips, sheets, or credit spend.

## 5. Blocker (exact)

`POST https://api.elevenlabs.io/v1/flows/video` → **402** `paid_plan_required`: *"This endpoint requires a Pro plan or above."* Plan is Creator. Claude/Ben: do not buy or upgrade.

## 6. House-lock note for Claude

Playbook §5 / comment **5981148012**: *No Omni, Seedance, Kling or ElevenLabs Image & Video on HOS.* Ben-ordered **test only**; nothing enters film unless Ben lifts the line. Gate failed before generation, so lock undisturbed. 006 mint routes / PICTURE_PLAN untouched.

## Files

- `/Users/benjaminoats/_desk/006/elevenlabs_fair_test_20261004/REPORT.md` (this file)
- `/Users/benjaminoats/_desk/006/elevenlabs_fair_test_20261004/gate.json`
- `/Users/benjaminoats/_desk/006/elevenlabs_subscription_snapshot_20261004.json`
- Mirror: `/Users/benjaminoats/YouTube/hos-006-trees/02_Video-Projects/006_Trees-Are-Made-Of-Air/04_Generated-Clips/elevenlabs_fair_test_20261004/`

No git commit / no new PR / #180 not merged.
