# HOS 128 Shorts VO — `hos_128_short_S01_v03_tight` & `hos_128_short_S02_v03b_tight` (`J3671`, 26 Nov 2026)

**Status: Take record only — NOT a VO lock or PASS.** Recorded by `gemini` under `J3671` and parked for independent non-producer Chief VO review and PASS. Zero picture, thumbnail, or scheduling spend.

## Locked source script verified pre-spend

- Path: `02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC/10_Shorts/SHORTS_SCRIPTS_v03.md`
- SHA-256: `1132ad9f8b44d4e545f699bf702b83894370effb34afe37ce12b25a2080694e7` (exact match to Acting Chief `J3660` lock / HOS PR `#762` merged `84af0f7d05701a5147d7ad7fb30403a0152e80ff`)
- Spoken scripts extracted byte-for-byte into `hos_128_short_S01_v03.txt` (`277` chars, `39` spoken words) and `hos_128_short_S02_v03.txt` (`263` chars, `40` spoken words). Zero words altered.

## Candidate edit-ready Shorts VO masters (16.0–19.0 s house band, `atempo = 1.00`)

Audio files are gitignored (zero media in git). All raw and pause-tightened WAV/MP3 files are stored on the NAS under `/Volumes/data/studio-live/History Of Science/02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC/10_Shorts/vo_v03/` with SHA-256 verified byte-for-byte after copy.

| Short | Candidate master stem | Duration | Loudness | `vo_check_py312.sh` | Edit recipe (`atempo`) | SHA-256 (WAV / MP3) |
|---|---|---:|---|---|---|---|
| **S01** (*Why Couldn't Thomas Edison's DC Power Cross a City?*) | `hos_128_short_S01_v03_tight` | **`18.54 s`** | `-20.1 LUFS` · mean `-22.6 dB` · peak `-4.0 dB` | **PASS** (1 sounds-alike warn: `tenfold` / `fold` — verified clean by direct listen) | Inter-sentence silence trim only from `hos_128_short_S01_v03` (`20.00 s` → `18.54 s`; `0.24 s` gaps, `15 ms` edge fades, **`atempo = 1.00`**, `£0` / `0` extra credits) | WAV: `931718a6429c8559e77adf2bbd02d549d653f18d5dd6fba683b66e203eb98168`<br>MP3: `40606376678a64f1a05a38f65cf58d74c99885ae09253e4a6ad66da70146cec1` |
| **S02** (*How Did Nikola Tesla's AC Beat Edison's DC?*) | `hos_128_short_S02_v03b_tight` | **`18.39 s`** | `-20.3 LUFS` · mean `-23.1 dB` · peak `-3.8 dB` | **PASS** (`0` word diffs) | Inter-sentence silence trim only from Acting-Chief-cleared retake `hos_128_short_S02_v03b` (`19.68 s` → `18.39 s`; `0.24 s` gaps, `15 ms` edge fades, **`atempo = 1.00`**, `£0` / `0` extra credits) | WAV: `cc51cc86810edd72265848b403b90ae26b814058971aedee1a20929b2e4f9106`<br>MP3: `feb068bc83e18b91fdf1e60419a9b49ef4d09a8aa54e79e7d1af143759c6c8da` |

## Raw ElevenLabs API takes (kept untouched on NAS for audit trail)

Voice: **Ben Orbit Narrator** (`kDch6ACCIpqgQ0NsU9kk`), `eleven_v3`, speed `1.04`, API only via `04_Audio/tools/vo_take.py` → `el_client.py` / `el_guard.py` on the Mini.

| Raw stem | Duration | Loudness | Scribe v2 | Disposition | SHA-256 (WAV / MP3) |
|---|---:|---|---|---|---|
| `hos_128_short_S01_v03` | `20.00 s` | `-20.0 LUFS` · mean `-23.0 dB` · peak `-4.0 dB` | `100.0%` (`0` mismatches) | Source for `hos_128_short_S01_v03_tight` (trimmed 3 long inter-sentence gaps: `0.68 s`, `1.10 s`, `0.88 s`) | WAV: `31d2abb8fc6ae7977388938fb04cbae8f60f0a0fae3676c7dbeab0856943b1ba`<br>MP3: `c95e4aa967ef2e1643f9362cf8a65d4489cf8ac946e15201c68e341142cb28ed` |
| `hos_128_short_S02_v03` | `23.84 s` | `-19.2 LUFS` · mean `-22.5 dB` · peak `-3.9 dB` | `87.5%` (digits `1888` & `22` only) | **Rejected on pacing** (`101 wpm`, slow dramatic pauses `1.16 s` & `1.20 s`; could not fit `16–19 s` even after pause trim + `atempo <= 1.06`) | WAV: `fda89c90bd3b1c7f5201e366083d7ab2139fd38adbba56e44934f9f76dd3829a`<br>MP3: `a927aa290d6b1ed6c042557b728ded606e36c55be5d5daaa7e992e4384152a0b` |
| `hos_128_short_S02_v03b` | `19.68 s` | `-20.4 LUFS` · mean `-23.3 dB` · peak `-3.8 dB` | `87.5%` (digits `1888` & `22` only) | Acting-Chief-cleared retake (`gemini` verified Chief via `chief_relay.py status`, `263` chars); source for `hos_128_short_S02_v03b_tight` (trimmed 2 inter-sentence gaps: `0.82 s`, `1.20 s`) | WAV: `5a8f2b251db155ac5375923a144f83e0438d595f7783b2c32152921dec862b4f`<br>MP3: `49fdd2ef613e8e00ed7730842b0a6db3bfe60f03d0dbbb63b30ca3dac4cd2ad1` |

## Pasted `vo_check_py312.sh` outputs (`faster-whisper small.en`)

### Candidate edit-ready masters (16.0–19.0 s)

```text
PASS  hos_128_short_S01_v03_tight.wav  0:18.54  mean -22.6 dB  peak -4.0 dB  126 wpm
   warn  pace 126 wpm (< 145); expect a long film — see STUDIO_PLAYBOOK.md §4 speed
   warn  replace at ~0:12.54: script 'transformers boosted voltage tenfold cutting wire heat' / heard 'transformers boosted voltage fold cutting wire heat' — sounds alike (likely the transcriber); listen

PASS  hos_128_short_S02_v03b_tight.wav  0:18.39  mean -23.1 dB  peak -3.8 dB  131 wpm
   warn  pace 131 wpm (< 145); expect a long film — see STUDIO_PLAYBOOK.md §4 speed
```

### Raw takes

```text
PASS  hos_128_short_S01_v03.wav  0:20.00  mean -23.0 dB  peak -4.0 dB  117 wpm
   warn  pace 117 wpm (< 145); expect a long film — see STUDIO_PLAYBOOK.md §4 speed

PASS  hos_128_short_S02_v03.wav  0:23.84  mean -22.5 dB  peak -3.9 dB  101 wpm
   warn  pace 101 wpm (< 145); expect a long film — see STUDIO_PLAYBOOK.md §4 speed

PASS  hos_128_short_S02_v03b.wav  0:19.68  mean -23.3 dB  peak -3.8 dB  122 wpm
   warn  pace 122 wpm (< 145); expect a long film — see STUDIO_PLAYBOOK.md §4 speed
```

JSON reports: `vo_check/hos_128_short_S01_v03_tight.json`, `vo_check/hos_128_short_S02_v03b_tight.json`, `vo_check/hos_128_short_S01_v03.json`, `vo_check/hos_128_short_S02_v03.json`, `vo_check/hos_128_short_S02_v03b.json`.
Word timings: `stt/<stem>/words.json` and `stt/<stem>/words.srt` (plus raw Scribe `stt_raw.json` on the three raw takes).

## Direct listening & Shorts house-rules check (`audio_input`)

Direct audio inspection (`read_file` on `hos_128_short_S01_v03_tight.mp3` and `hos_128_short_S02_v03b_tight.mp3`, logged via `chief_relay.py capabilities --available audio_input`):
- **S01 (`18.54 s`):** Clear British delivery, zero misreads, clean "tenfold" (`vo_check` warn is faster-whisper writing "10-fold" and `vo_check` dropping cardinal "10"), natural `0.24 s` sentence joins with zero clicks or clipped breaths, open loop inflection on *"That simple physics explains why"* (`18.18–18.46 s`) looping straight into *"Edison's direct current..."* (`0.06 s`). Subject + surprise (`"Edison's direct current couldn't"`) lands at `0.06–1.82 s`.
- **S02 (`18.39 s`):** Clear British delivery ("patented", "1888", "22 miles to Buffalo"), zero misreads, zero `vo_check` word diffs, natural `0.24 s` sentence joins with zero clicks or clipped breaths, open loop inflection on *"proving just how"* (`18.13–18.35 s`) looping straight into *"Tesla's brushless motor..."* (`0.05 s`). Subject + surprise (`"Tesla's brushless motor broke"`) lands at `0.05–1.79 s`.
- **Downstream S02 edit note (overlay boundary):** On measured `hos_128_short_S02_v03b_tight` timings, *"In 1888, Tesla patented..."* spans `8.41–10.79 s` (straddling the `9.0–14.0 s` promoted long title window). Because the single optional Teach overlay must stay strictly clear of `9.0–14.0 s`, the S02 picture/edit job should either place the Teach overlay earlier (e.g., `4.5–8.5 s` over *"Early alternating current lit lamps, yet stalled in factories"*) or omit the optional Teach overlay on S02 so it never competes with the `9.0–14.0 s` long title. S01's `10× VOLTS = 1/100 HEAT` card fits cleanly inside `4.5–8.8 s` (`"Low voltage meant heavy current, wasting energy as heat unless cables grew hugely expensive"`, `3.78–9.64 s`), strictly clear of `9.0–14.0 s`.

## ElevenLabs credit accounting & ledger

- **Pre-take live check (`2026-11-26T06:58Z`):** `8,003` of `121,114` chars remaining (`113,111` used); resets `2026-11-30T10:50:31Z`. `J3670` (long VO, `9,062` chars) cannot fit in `8,003` and was already parked until `2026-11-30T11:00:00Z`; spending expiring pre-reset credits on `J3671` saves December post-reset allowance.
- **Spoken characters sent across 3 API calls:** `277` (`S01_v03`) + `263` (`S02_v03`) + `263` (`S02_v03b`) = `803` chars (plus 3 Scribe `scribe_v2` calls on ~20 s audio).
- **Post-take live check (`2026-11-26T07:04Z`):** `7,630` of `121,114` chars remaining (`113,484` used); settled counter delta **`373` credits**. Floor `0`, `£0` real money, nothing bought or topped up.
- **Mini ledger summary (`~/_desk/elevenlabs/ledger.jsonl`, all HTTP `200`, via `vo_take.py` on the Mini):**
  - `2026-11-26T07:00:24Z` · `/v1/text-to-speech/kDch6ACCIpqgQ0NsU9kk` · `277` chars · `left_before: 8003` · `200`
  - `2026-11-26T07:00:26Z` · `/v1/speech-to-text` · `0` chars · `left_before: 8003` · `200`
  - `2026-11-26T07:00:41Z` · `/v1/text-to-speech/kDch6ACCIpqgQ0NsU9kk` · `263` chars · `left_before: 8003` · `200`
  - `2026-11-26T07:00:44Z` · `/v1/speech-to-text` · `0` chars · `left_before: 8003` · `200`
  - `2026-11-26T07:02:47Z` · `/v1/text-to-speech/kDch6ACCIpqgQ0NsU9kk` · `263` chars · `left_before: 7752` · `200`
  - `2026-11-26T07:02:50Z` · `/v1/speech-to-text` · `0` chars · `left_before: 7752` · `200`

## Schedule & next step

- Unified `J3734` schedule (`HOS PR #786` / `OWB PR #1330`): long target **Thu 7 Jan 2027 18:00 London** (Ben watch **Mon 4 Jan 2027**); Shorts target **Fri 8 Jan** (`S01`) and **Sat 9 Jan 2027** (`S02`, `11:30 London`) — never before the long is public. *(Original `J3671` brief dates Thu 10 Dec / Fri 11 Dec / Sat 12 Dec with Mon 7 Dec → Thu 17 Dec slip contingency were superseded by `J3734`.)*
- **Next:** Independent non-producer Chief VO review (audio listen on NAS + PR merge + `shorts_vo` PASS/KEEP). Long VO (`J3670`) remains parked for the `2026-11-30T10:50:31Z` reset. No picture, thumbnail, or scheduling spend until Chief passes VO.
