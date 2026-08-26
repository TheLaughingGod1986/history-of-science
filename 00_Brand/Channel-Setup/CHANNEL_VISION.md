# History of Science — channel vision (locked direction)

Created: **25 Aug 2026**  
Repo: `history-of-science` (separate from `orbit-with-ben`)

## What this channel is

**History of Science** is a new YouTube channel. Not a rename of Orbit With Ben.

| | |
|---|---|
| Display name | **History of Science** |
| Handle (target) | **@HistoryOfScience** (confirm availability at create) |
| Feel | **3D cartoon** immersion (Animistry-class) · curious · discovery-first |
| Runtime | **8–9 minutes** per long |
| Titles | Curiosity questions / day-in-the-life / “Did X really…?” — about **science** |
| Inspiration | [Animistry](https://www.youtube.com/@ytAnimistry) — steal form, not topics (`INSPIRATION_ANIMISTRY.md`) |
| Tagline | Discovery. Wonder. Proof. |
| Brand line | How we discovered what we know. |
| Mascot | **the Explorer** — sparse side character (`01_Character/`) |
| Not | Orbit With Ben · continuous mascot · war-history clone · dread essay |

## Picture rules (locked)

1. **Story is the star.** Put the viewer inside the discovery — Animistry immersion, pointed at science.
2. Style: **3D stylised cartoon** (feature-animation polish) — warm cinematic light, period/lab worlds.
3. **Explorer** pops in **every few scenes** (≈ every 3–5): walks through, shows interest, interacts with a prop, reacts — then leaves. (Animistry has no mascot; we keep a light garnish only.)
4. Never continuous Orbit-style presence. Never the whole film’s talking head.
5. Mute test: story still reads without him.
6. Length **8–9 min** — do not default to 15–16 until hold proves out.

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

Launch pack: `SOCIALS_LAUNCH.md` · `SOCIAL_IDENTITY.json`.

1. Confirm `@HistoryOfScience` in the YouTube channel switcher (empty public page already exists) → brand it → fill `CHANNEL_META.json`.
2. Connect YouTube Data API OAuth for this channel only.
3. Deploy Content Ops for HOS; set `APP_BASE_URL` to that origin.
4. Create **new** Meta / Threads / TikTok (`@historyofscienceyt` on IG — exact `@historyofscience` is Wellesley).
5. First episode: story-first 3D cartoon plates + sparse Explorer beats.
