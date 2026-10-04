# HOS 006 Shorts VO — 4 Oct 2026 (desk task from Claude #180)

House-voice VO only (no video, no ElevenLabs plan upgrade). Word-check skipped (faster-whisper/PyAV 3.14 incompat); loudness + silence gates applied.

## Voice lock

- Name: Ben Orbit Narrator
- VOICE_ID: `kDch6ACCIpqgQ0NsU9kk`
- MODEL_ID: `eleven_v3`
- Settings: stability 0.34, similarity_boost 0.78, style 0.42, speed 1.04
- Auth: `api_key` via `el_auth.load_token`

## Credits

| | Value |
|---|---|
| Limit | 209536 |
| Used before | 108825 |
| Used after (refreshed) | 109216 |
| Remaining before | 100711 |
| Remaining after | 100320 |
| API used delta | 391 |
| Script chars sent | 888 (T1 315 + T2 268 + T3 305) |

Note: character_count lagged at mint time (showed unchanged); refreshed query gives +391. Prior test-shorts session had used~42191; other work consumed credit between sessions.

## Results

| Short | Take | Duration | vo_check | Path | sha256 |
|---|---|---|---|---|---|
| A (willow air) | v01 (old) | 24.08 s | FAIL peak −0.8 dB | `elevenlabs_test_shorts_20261004/vo/t1_…_v01.mp3` | e74034… |
| A | **v02 KEEP** | **22.64 s** | **PASS** mean −19.3 / peak −1.0 | `shorts_vo_20261004/vo/t1_willow_air_vo_v02.mp3` | ccce477426bc7b1db1a9c6bd65aa671e999f3528aee3c51b523d4da6f69c6f03 |
| B (mint fixed) | v01 (old) | 21.52 s | FAIL silence 2.03 s | old desk | 14abef… |
| B | v02 raw | 20.00 s | FAIL silence 1.73 s @ 16.28 (title gap) | `t2_mint_fixed_vo_v02.mp3` | 5aacd9256d95eeeeefb286c4e5b7fdb75113e9d5d70c145d763afe7c573b7b73 |
| B | **v02b KEEP** (ffmpeg squeeze gap→0.55 s; no new TTS) | **18.82 s** | **PASS** mean −19.7 / peak −1.4 | `t2_mint_fixed_vo_v02b.mp3` | 99eb4c0dd415fd50a1a7a226e3f54f418b21a69802d052e04b7708780a736d39 |
| C (bubbles sunlight) | **v01 KEEP** | **24.16 s** | **PASS** mean −20.0 / peak −1.0 | `t3_bubbles_sunlight_vo_v01.mp3` | 5b5d84e560d51ed9ad6f9bf5588f458802620f48f008b9409c532f8a1ea4e269 |

One TTS retake each for A and B after v01 FAIL; C one take. B's remaining silence FAIL fixed by remaster (title-tagline gap), not a second TTS spend.

## Generator

- `/Users/benjaminoats/_desk/006/shorts_vo_20261004/vo/_generate_shorts_abc_vo_v01.py`
- Meta: `vo/VO_META.json`

## Notes

- No video generated. No picture mint. No plan upgrade.
- Repo copy: `02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/vo_20261004/`
