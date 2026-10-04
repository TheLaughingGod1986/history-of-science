# HOS 006 Short B v03 + word checks — 4 Oct 2026 ~17:51 London

Claude GO: comment 5982220460 on #180. Claim: 5982235004. Grok desk (no Ben ping, no #180 merge, no picture mint).

## Voice lock
- Ben Orbit Narrator · `kDch6ACCIpqgQ0NsU9kk` · `eleven_v3`
- stability 0.34 · similarity_boost 0.78 · style 0.42 · speed 1.04 · use_speaker_boost True
- Auth: api_key via el_auth.load_token

## Short B script (from origin/main after #205 `52b41a0`)
56 words claimed in SHORTS_SCRIPTS_v01.md (wc=57 with punctuation-split). **No spoken title. No gap squeeze.**

> A sprig of mint repaired the air. Joseph Priestley burned a candle in a sealed jar until the flame died, and no new flame would light. He slid in a sprig of mint and waited. Ten days later, a candle burned bright in that same air. Somehow, the little green plant had made the air good again.

## Credits (ElevenLabs `/v1/user`)
| | Value |
|---|---|
| Limit | 209536 |
| Used before B mint | 109976 |
| Remaining before | 99560 |
| Used after (refreshed) | 112420 |
| Remaining after | 97116 |
| Account delta | +2444 |
| B v03 script chars | 291 |

Note: account delta ≫ 291 — concurrent EL spend on this account (a parallel process also wrote a 21.6 s desk overwrite of `t2_mint_fixed_vo_v03.mp3` at 17:50:42; preserved as `t2_mint_fixed_vo_v03_OVERWRITE_21s.mp3`). Canonical take restored from repo copy.

## Results (Py 3.12.15 + faster-whisper; vo_check loudness/silence/words)

| Short | Take | Dur | vo_check (loud/silence) | Word-check | Notes |
|---|---|---|---|---|---|
| A | v02 KEEP | 22.64 s | PASS mean −19.3 / peak −1.0 / no long silence | **FAIL vs body script** (expected): whisper hears spoken title after “two ounces.” | Claude: trim title in edit. Body to “two ounces.” is present. |
| B | **v03 NEW** | **23.20 s** | **PASS** mean −21.0 / peak −1.2 / no silence >1 s | **PASS** 56/56 normed words, no diffs | No title in audio. No squeeze. |
| C | v01 KEEP | 24.16 s | PASS mean −20.0 / peak −1.0 / no long silence | **PASS** (warn: Ingenhousz→Ingenhaus sounds-alike; pace 139 wpm) | **1779** read as year digits in script/align; whisper token `1779` @ 3.58–4.70 s (~1.12 s ≈ “seventeen seventy-nine”) |

## Paths + sha256
| File | sha256 |
|---|---|
| desk+repo `t2_mint_fixed_vo_v03.mp3` | `cb45356fd60363aad92ba97a05b2fb8cbe7b6b61d7b4bb411ded8f4f9aa3f0bf` |
| `t2_mint_fixed_vo_v03_align.json` | `8bd4caa297c3dd1b319e649a388f6e914be592560eb3ff9a07164477ff0a3c49` |
| `t2_mint_fixed_v03.txt` | `9423f337eb254e384ee70e50f423bebaf73a626823bd48161172a359e17ca902` |
| A `t1_willow_air_vo_v02.mp3` | `ccce477426bc7b1db1a9c6bd65aa671e999f3528aee3c51b523d4da6f69c6f03` |
| C `t3_bubbles_sunlight_vo_v01.mp3` | `5b5d84e560d51ed9ad6f9bf5588f458802620f48f008b9409c532f8a1ea4e269` |

Desk: `/Users/benjaminoats/_desk/006/shorts_vo_20261004/vo/`  
Repo: `02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/vo_20261004/`  
Word-check JSON: `/Users/benjaminoats/_desk/006/shorts_vo_20261004/wordcheck_20261004/`  
Generator: `vo/_generate_short_b_v03.py`

## Screenshot
`/Users/benjaminoats/_desk/handoff/hos006_short_b_v03_verify.png`

## Not done
- No #180 merge/close
- No Vertex/Flow picture mint
- No gap squeeze on B
