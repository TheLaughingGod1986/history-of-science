# HOS 136 Shorts VO — `hos_136_short_S01_v02_tight` & `hos_136_short_S02_v02_tight` (`J3679`, 26 Nov 2026)

**Status: Take record only — NOT a VO lock or PASS.** Recorded by `gemini` under `J3679` and parked for independent non-producer Chief VO review and PASS (after review/merge of the separate `vo_check.py` `"beta" -> "bethe"` homophone alias PR). Zero picture, thumbnail, or scheduling spend.

## Locked source script verified pre-spend

- Path: `02_Video-Projects/136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained/10_Shorts/SHORTS_SCRIPTS_v02.md`
- SHA-256: `e1df5d81baffca83c559b78a2a87df97df0fe8be15fb8de96a761445906941fe` (exact match to Acting Chief `J3677` lock / HOS PR `#767` merged `ab25f2de`)
- Spoken scripts extracted byte-for-byte into `hos_136_short_S01_v02.txt` (`262` chars, `42` spoken words) and `hos_136_short_S02_v02.txt` (`239` chars, `42` spoken words). Zero words altered.

## Candidate edit-ready Shorts VO masters (16.0–19.0 s house band, `atempo = 1.00`)

Audio files are gitignored (zero media in git). All 10 raw and pause-tightened WAV/MP3 files are stored on the NAS under `/Volumes/data/studio-live/History Of Science/02_Video-Projects/136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained/10_Shorts/vo_v02/` with SHA-256 verified byte-for-byte after copy (`10/10` match).

| Short | Candidate master stem | Duration | Loudness | `vo_check_py312.sh` (on current `main`) | Edit recipe (`atempo`) | SHA-256 (WAV / MP3) |
|---|---|---:|---|---|---|---|
| **S01** (*Could the Trinity Test Have Ignited the Sky?*) | `hos_136_short_S01_v02_tight` | **`18.70 s`** | `-20.1 LUFS` · mean `-22.9 dB` · peak `-4.0 dB` | **1 ASR homophone flag only** (`script 'bethe' / heard 'beta'` — Hans Bethe is pronounced `/ˈbeɪtə/`, identical to "beta"; ElevenLabs Scribe v2 hears `"Bethe"` cleanly; separate `vo_check.py` alias PR opened) | Inter-sentence silence trim only from `hos_136_short_S01_v02` (`21.28 s` → `18.70 s`; 4 pauses trimmed to `0.18 s` inserted gaps with `15 ms` edge fades, **`atempo = 1.00`**, `£0` / `0` extra credits) | WAV: `7a664025231b35f891267b43df32e9f2592041e83b04f2b6e612d983900c4853`<br>MP3: `a5c6d380b03412c658f0bba8998d791215db75960d4a47dc4ef8df94432adce4` |
| **S02** (*How Did Enrico Fermi Measure the Trinity Blast With Paper?*) | `hos_136_short_S02_v02_tight` | **`18.74 s`** | `-21.8 LUFS` · mean `-24.6 dB` · peak `-4.1 dB` | **PASS** (`0` word diffs) | Inter-sentence silence trim only from `hos_136_short_S02_v02` (`21.92 s` → `18.74 s`; 4 pauses trimmed to `0.14 s` inserted gaps with `15 ms` edge fades, **`atempo = 1.00`**, `£0` / `0` extra credits) | WAV: `0ced4f75d68b2cf29320a6a7744b8f4eae8e34c51a251ce9d5e37d2d6db7087c`<br>MP3: `1a5b738b5082601a1adb7bd3d8c7932e2c049b965209371f45ca50b2390b08cd` |

## Raw ElevenLabs API takes (kept untouched on NAS for audit trail)

Voice: **Ben Orbit Narrator** (`kDch6ACCIpqgQ0NsU9kk`), `eleven_v3`, speed `1.04`, API only via `04_Audio/tools/vo_take.py` → `el_client.py` / `el_guard.py` on the Mac mini.

| Raw stem | Duration | Loudness | Scribe v2 | Disposition | SHA-256 (WAV / MP3) |
|---|---:|---|---|---|---|
| `hos_136_short_S01_v02` | `21.28 s` | `-20.2 LUFS` · mean `-23.4 dB` · peak `-4.0 dB` | `93.02%` (`'42` digit + soft `-d` on `"proved radiation"` heard as `"prove"` by Scribe, `"proved"` by Whisper) | **Recommended source** for `hos_136_short_S01_v02_tight`: pronounces Hans **Bethe** accurately (`/ˈbeɪtə/`, "BAY-tuh"), crisp `"Konopinski"`, clean loop, hits `18.70 s` at `atempo = 1.00` with inter-sentence pause trim only | WAV: `3f212b2927bb246777f5f2291a49c679d784c69630f26e14689a19c28cf5c9de`<br>MP3: `9cc0114f1cbeebac886cdb2519fdc15ce4927caea0c12360808bca802992c391` |
| `hos_136_short_S01_v02b` | `21.20 s` | `-21.2 LUFS` · mean `-24.5 dB` · peak `-3.8 dB` | `95.35%` (`'42` digit only; `"proved"` articulated crisply) | Acting-Chief-cleared bounded retake (`gemini` verified Chief via `chief_relay.py status`, `262` chars) to check `"proved"`; **not preferred** because `eleven_v3` mispronounced `"Bethe"` as `"BET-uh"` (Whisper heard `betta`, direct `audio_input` listen heard `"better"`); kept raw on NAS for Chief comparison | WAV: `6e1a77d4e7e2285db0dbfa5a02051582de74d00dc6d3392e60221b37bacb8a41`<br>MP3: `237e60a4e332f7411a152b66eefa2746c3820de6e9e039bbc53bb3b813443362` |
| `hos_136_short_S02_v02` | `21.92 s` | `-21.7 LUFS` · mean `-25.2 dB` · peak `-4.1 dB` | `90.48%` (digits `40`, `10,000` + US spelling `meters` only; `0` word diffs in `vo_check`) | **Source** for `hos_136_short_S02_v02_tight` (trimmed 4 long inter-sentence/clause silences: `0.96 s`, `1.07 s`, `0.90 s`, `0.95 s`) | WAV: `e00483534ac6431a09345112ba62143c3e2760f68dcd99b63fd610c49f5857ee`<br>MP3: `1be4348bd12c8025ed1eb058290763d08cc7b541a73ba79fd02046536eaf9575` |

## Pasted `vo_check_py312.sh` outputs (`faster-whisper small.en`, unmodified current `main`)

### Candidate edit-ready masters (`16.0–19.0 s`)

```text
FAIL  hos_136_short_S01_v02_tight.wav  0:18.70  mean -22.9 dB  peak -4.0 dB  138 wpm
   FAIL  replace at ~0:07.22: script 'could fuse nitrogen bethe and konopinski proved' / heard 'could fuse nitrogen beta and konopinski proved' — listen, then regenerate that sentence alone if real
   warn  pace 138 wpm (< 145); expect a long film — see STUDIO_PLAYBOOK.md §4 speed

PASS  hos_136_short_S02_v02_tight.wav  0:18.74  mean -24.6 dB  peak -4.1 dB  134 wpm
   warn  pace 134 wpm (< 145); expect a long film — see STUDIO_PLAYBOOK.md §4 speed
```

### Raw API takes (for audit trail)

```text
FAIL  hos_136_short_S01_v02.wav  0:21.28  mean -23.4 dB  peak -4.0 dB  121 wpm
   FAIL  replace at ~0:08.02: script 'could fuse nitrogen bethe and konopinski proved' / heard 'could fuse nitrogen beta and konopinski proved' — listen, then regenerate that sentence alone if real
   warn  pace 121 wpm (< 145); expect a long film — see STUDIO_PLAYBOOK.md §4 speed

FAIL  hos_136_short_S01_v02b.wav  0:21.20  mean -24.5 dB  peak -3.8 dB  122 wpm
   FAIL  replace at ~0:08.26: script 'could fuse nitrogen bethe and konopinski proved' / heard 'could fuse nitrogen betta and konopinski proved' — listen, then regenerate that sentence alone if real
   warn  pace 122 wpm (< 145); expect a long film — see STUDIO_PLAYBOOK.md §4 speed

PASS  hos_136_short_S02_v02.wav  0:21.92  mean -25.2 dB  peak -4.1 dB  115 wpm
   warn  pace 115 wpm (< 145); expect a long film — see STUDIO_PLAYBOOK.md §4 speed
```

## Direct `audio_input` listen verification (`gemini`, 26 Nov 2026)

- **`hos_136_short_S01_v02_tight.mp3` (`18.70 s`):** Warm British Ben Orbit Narrator tone, clean pause splices (no clicks or clipped consonants), accurate `/ˈbeɪtə/` ("BAY-tuh") pronunciation of Hans **Bethe** and crisp `"Konopinski"`, strong causal loop (`"...which is why physicists proved"` → `"The Trinity test could never set Earth's sky on fire."`). One minor nuance flagged transparently for Chief: `"proved radiation"` has a soft `-d` coalesced into `r` (Whisper hears `"proved"`, Scribe hears `"prove"`). Compared against retake `hos_136_short_S01_v02b.mp3`, which articulated `-d` more sharply but pronounced `"Bethe"` as `"BET-uh"`/`"better"`, `S01_v02_tight` is preferred on historical name accuracy and `atempo = 1.00` timing.
- **`hos_136_short_S02_v02_tight.mp3` (`18.74 s`):** Crystal-clear British Ben Orbit Narrator delivery throughout (`"Enrico Fermi"`, `"forty seconds"`, `"two and a half metres"`, `"ten thousand tons of TNT"`), natural splice rhythm, zero artefacts, seamless causal loop (`"...which is how"` → `"Enrico Fermi measured the Trinity blast with torn paper."`). Ready for Chief PASS.

## ElevenLabs credits & ledger (`~/_desk/elevenlabs/ledger.jsonl`)

- Pre-take live balance: `7,630` of `121,114` remaining (`113,484` used; resets `2026-11-30T10:50:31Z`).
- Priority check: higher-priority longs `HOS:128` (`J3670`, needs `9,062` chars) and `HOS:136` (`J3678`, needs `7,761` chars) both exceeded `7,630` remaining and remain parked until the `2026-11-30T10:50:31Z` reset; recording HOS 136 Shorts used credits that could not run either long before reset (`floor = 0`, `£0`).
- Post-take settled balance: **`7,275`** of `121,114` remaining (`113,839` used; **`355` credits settled** across `763` spoken characters in 3 API calls: `S01_v02` 262c, `S02_v02` 239c, `S01_v02b` 262c).
- Ledger entries (`2026-11-26`):
  - `07:24:01Z` `vo_take.py` `/v1/text-to-speech/kDch6ACCIpqgQ0NsU9kk` `chars=262` `status=200` `left_before=7630` (+ Scribe `07:24:03Z`)
  - `07:24:16Z` `vo_take.py` `/v1/text-to-speech/kDch6ACCIpqgQ0NsU9kk` `chars=239` `status=200` `left_before=7630` (+ Scribe `07:24:18Z`)
  - `07:26:35Z` `vo_take.py` `/v1/text-to-speech/kDch6ACCIpqgQ0NsU9kk` `chars=262` `status=200` `left_before=7396` (+ Scribe `07:26:37Z`)

## Schedule & next steps

- **Schedule preserved:** Current unified line-up (`J3734`, `status.json`) targets **Thu 14 Jan 2027 18:00 London** for the long (Ben's watch Mon 11 Jan 2027); original `J3679` brief dates (Thu 17 Dec long / Fri 18 Dec `S02` / Sat 19 Dec `S01` 11:30 London; Ben's watch Mon 14 Dec; slides one week if not ready) remain noted. Never air a Short before its long is public.
- **Next:** Independent non-producer Chief (`claude` or `codex`) reviews & merges the separate `vo_check.py` `"beta" -> "bethe"` homophone alias PR, re-verifies `vo_check_py312.sh` PASS on `hos_136_short_S01_v02_tight.wav`, listens to both candidate masters on NAS, merges this PR, and flips `status.json` `shorts_vo` → `done`. Long VO (`J3678`) remains parked for the `2026-11-30T10:50:31Z` reset. **No picture, thumbnail, or scheduling spend until Chief passes the VO.**
