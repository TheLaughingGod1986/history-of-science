# Ben Orbit Narrator — Voice Model Settings

**Voice name:** Ben Orbit Narrator  
**Voice ID:** `kDch6ACCIpqgQ0NsU9kk`  
**Source:** Instant Voice Clone of Ben’s own voice  
**Project:** Orbit YouTube / 001 Will We Ever Meet Aliens  
**Active profile:** **Documentary v02** (2026-07-27)  
**Status:** Tuned for space-mystery narration · full master still blocked on character quota

---

## Documentary profile v02 (locked defaults)

| Setting | Value | Why |
|---------|-------|-----|
| Model | `eleven_multilingual_v2` | Best long-form quality on Starter |
| Stability | **0.50** | Calm authority; fewer emotional swings |
| Similarity boost | **0.83** | Stay recognisably Ben |
| Style / expressiveness | **0.08** | Quiet mystery — not theatrical |
| Speed | **0.92** | Reflective cosmic pacing |
| Speaker boost | **On** | Clarity under future music beds |

Saved on the ElevenLabs voice via `/voices/{id}/settings/edit`.

Profile card: `ben_orbit_voice_profile_documentary_v02.md`

### Previous generation settings (v01 — used for sections 01–05 + 09)

| Setting | v01 |
|---------|-----|
| Stability | 0.42 |
| Similarity | 0.80 |
| Style | 0.12 |
| Speed | 0.95 |

When quota allows, re-render those sections with **v02** for a consistent master.

---

## Voice description (target)

> Warm, articulate British educational narrator with calm authority, cinematic curiosity and restrained mystery. Designed for accessible science and space documentary storytelling. Quietly dramatic — never theatrical, never trailer-like.

---

## Test generations

| File | Purpose |
|------|---------|
| `ben_orbit_voice_test_educational_v01.wav` | v01 educational |
| `ben_orbit_voice_test_mystery_v01.wav` | v01 mystery |
| `ben_orbit_voice_test_inspiring_v01.wav` | v01 inspiring |
| `ben_orbit_voice_test_style-tune_v02.wav` | **v02 micro probe** (opened in QuickTime) |

---

## Pronunciation notes

| Term | Guidance |
|------|----------|
| Fermi | FAIR-mee |
| exoplanet | EK-so-planet |
| biosignature | BY-oh-signature |
| technosignature | TEK-no-signature |
| Proxima Centauri | PROK-sim-uh sen-TAW-ree |
| Enceladus | en-SELL-uh-dus |
| Europa | yoo-ROH-puh |
| spectroscopy | spek-TROSS-kuh-pee |
| civilisation | British delivery |

---

## Section generation status

| Section | Status |
|---------|--------|
| 01–05 + 09 | ✅ Generated with v01 settings |
| 06–08 | ❌ Quota (~3.4k characters needed) |
| Full master | ❌ Pending 06–08 + optional v02 re-render |

Quota remaining after style probe: check ElevenLabs subscription (was ~90 after v02 probe).

## Safety

- Ben’s own clone only — no third-party imitation.
- Pause before paid upgrade.
- Never overwrite masters; bump `_v02` for regenerations.
