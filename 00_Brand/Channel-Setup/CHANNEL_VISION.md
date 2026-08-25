# History of Science — channel vision (locked direction)

Created: **25 Aug 2026**  
Repo: `history-of-science` (separate from `orbit-with-ben`)

## What this channel is

**History of Science** is a new YouTube channel. Not a rename of Orbit With Ben.
Animated science storytelling — **more cartoon / stylised**, **more upbeat** — built for browse + return viewers.

| | |
|---|---|
| Display name | **History of Science** |
| Handle (target) | **@HistoryOfScience** (confirm availability at create) |
| Feel | Cartoon-forward · upbeat · curious · science-first |
| Not | Orbit With Ben clone · faceless dread essay · shop-read channel |

## Production stack (reuse — locked)

Same tooling as the Orbit ops template; new brand identity on top.

| Layer | Stack | Notes |
|---|---|---|
| **VO / narration** | ElevenLabs — Ben Orbit Narrator (`kDch6ACCIpqgQ0NsU9kk`) | Same British VO. Upbeat scripts; same voice clone. |
| **CG / picture** | Omni / Gemini Veo (`04_Audio/tools/orbit_gemini_veo.py`) | Silent picture only. Mix VO in edit. Tool filenames stay `orbit_*` for now (shared library). |
| **Upload** | YouTube Data API v3 via Content Ops (`07_Content-Ops` · `npm run youtube:package`) | New channel OAuth / Brand Account when created. |
| **Ops** | Content Ops gates, script reviewer ≥90, package manifest | Same pipeline; new listing identity. |

## Visual direction (TBD — first design pass)

- Prefer **cartoon / stylised** animation over photoreal documentary CG.
- Upbeat energy in colour, motion, and edit pace.
- Character system: **new** for this channel (do not ship Orbit orange robot as the History of Science mascot unless Ben explicitly locks that).
- Seed assets under `01_Orbit-Character/` are **legacy template references** until a History of Science character bible exists.

## Do not

- Point uploads, Studio finish, or API calls at the live Orbit With Ben channel.
- Treat historical audit JSON in this repo as live History of Science metrics (they are seed history from the Orbit template).
- Invent a YouTube channel ID — set `CHANNEL_META.json` after create.

## Next ops steps

1. Create Brand Account channel + handle → fill `CHANNEL_META.json` / `CHANNEL_READY.md`.
2. Connect YouTube Data API OAuth for this channel only.
3. Confirm ElevenLabs VO + Omni/Veo keys work in this workspace.
4. Design cartoon character + colour system → replace legacy Orbit identity docs.
5. First episode scaffold under `02_Video-Projects/` with History of Science packaging.
