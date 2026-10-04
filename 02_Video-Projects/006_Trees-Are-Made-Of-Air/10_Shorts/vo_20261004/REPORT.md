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


---

---

## Follow-up 4 Oct 2026 ~17:52 London — Short B retake after #205 merge

#205 merged (Claude Shorts scripts + closing line). Recorded **one new TTS take** of Short B with the 56-word script including "Somehow, the little green plant had made the air good again." Title not spoken. No silence-gap squeeze (peak trim only).

### Voice lock (unchanged)
- Name: Ben Orbit Narrator
- VOICE_ID: kDch6ACCIpqgQ0NsU9kk
- MODEL_ID: eleven_v3
- Settings: stability 0.34, similarity_boost 0.78, style 0.42, speed 1.04

### Short B v03

| Take | Duration | vo_check | Path | sha256 |
|---|---|---|---|---|
| v03 raw TTS | 21.60 s | FAIL peak −0.8 dB | vo/t2_mint_fixed_vo_v03.mp3 | f11b88bc8919647f3d50fc30f44c83caab088dbb378be0613aa1512085d6a36a |
| **v03b KEEP** (volume −0.3 dB only; no gap squeeze) | **23.20 s** | **PASS** mean −21.3 / peak −1.5; words 56/56 | vo/t2_mint_fixed_vo_v03b.mp3 | 0f1099262037b62ea2b2a003ce86e196458fa983e9ca97877afb5600e97c7479 |

### Word checks (faster-whisper small.en under Py 3.12 .venv312)

| Short | Take | vo_check | Whisper note |
|---|---|---|---|
| A | v02 | **PASS** (mean −19.3 / peak −1.0; words 51/51 vs Short A script) | Matches willow script; no spoken title in check script |
| B | **v03b** | **PASS** | Closing line heard: "Somehow the little green plant had made the air good again." |
| C | v01 | **PASS** (warn: pace 139; sounds-alike Ingenhousz→Ingenhaus) | Keep |

Evidence dir: `_desk/006/shorts_vo_20261004/wordcheck_20261004/` (vo_check_A_v02.json, vo_check_B_v03b.json, vo_check_C_v01.json, *_whisper.json).

No picture spend. 007 long VO not touched (other lane).


## Provenance correction (4 Oct 2026 ~18:02 — one-process)

Earlier table briefly mis-labelled the **21.60 s / f11b88…** race overwrite as “v03 raw”. Live filenames now:

| name | sha | dur | status |
|---|---|---|---|
| `t2_mint_fixed_vo_v03.mp3` | cb45356… | 23.20 s | PASS (also good; not the lock) |
| `t2_mint_fixed_vo_v03b.mp3` | 0f10992… | 23.20 s | **LOCK** PASS peak −1.5 |
| `t2_mint_fixed_vo_v03_OVERWRITE_21s.mp3` | f11b88… | 21.60 s | REJECT peak −0.8 |

See `PROVENANCE_B_ONEPROC_20261004.md`.
