# History of Science — channel vision (locked direction)

Created: **25 Aug 2026**  
Repo: `history-of-science` (separate from `orbit-with-ben`)

## What this channel is

**History of Science** is a new YouTube channel. Not a rename of Orbit With Ben.

| | |
|---|---|
| Display name | **History of Science** |
| Handle (target) | **@HistoryOfScience** (confirm availability at create) |
| Feel | **3D cartoon** · upbeat · curious · discovery-first |
| Tagline | Discovery. Wonder. Proof. |
| Brand line | How we discovered what we know. |
| Mascot | **the Explorer** — side character only (`01_Character/`) |
| Not | Orbit With Ben clone · Orbit robot · continuous mascot show · dread essay |

## Picture rules (locked)

1. **Story is the star.** Worlds, discoveries, experiments, and ideas lead every film.
2. Style: almost **3D cartoon** feature animation — stylised, bright, soft cinematic light.
3. **Explorer** pops in **every few scenes** (≈ every 3–5): walks through, shows interest, interacts with a prop (e.g. dusts a library book and reads), reacts thinking / surprised / eureka — then leaves.
4. He is **less intrusive than Orbit** on Orbit With Ben. Never continuous presence. Never the whole film’s talking head.
5. Mute test: story still reads without him.

Canonical sheet: `01_Character/01_Master-References/hos-explorer-character-sheet-v01.jpg`

## Production stack (reuse — locked)

| Layer | Stack | Notes |
|---|---|---|
| **VO / narration** | ElevenLabs — Ben Orbit Narrator (`kDch6ACCIpqgQ0NsU9kk`) | Same British VO. Upbeat scripts. |
| **CG / picture** | Omni / Gemini Veo (`04_Audio/tools/orbit_gemini_veo.py`) | Silent picture. Mix VO in edit. Tool filenames stay `orbit_*` for now. |
| **Upload** | YouTube Data API v3 via Content Ops | New channel OAuth when created. |
| **Ops** | Content Ops gates, script reviewer ≥90 | Same pipeline; new listing identity. |

## Do not

- Point uploads or OAuth at the live Orbit With Ben channel.
- Ship Orbit orange robot in HOS films.
- Park Explorer in every scene.
- Use `orbit-content-ops.vercel.app` as this app’s production host (that belongs to Orbit With Ben).
- Treat historical Orbit audit JSON as live HOS metrics.

## Next ops steps

1. Create Brand Account channel + handle → fill `CHANNEL_META.json`.
2. Connect YouTube Data API OAuth for this channel only.
3. Deploy Content Ops for HOS; set `APP_BASE_URL` to that origin.
4. Create **new** Meta / Threads / TikTok accounts (do not publish to Orbit’s).
5. First episode: story-first 3D cartoon plates + sparse Explorer beats.
