# HOS 007 long-film VO v01 — evidence pack (4 Oct 2026)

Desk task for Claude on PR #180. **No picture / Vertex / Flow spend. No #180 merge.**
Ben listen not required before Claude PASS (standing Ben order 4 Oct).

## Voice lock

- Name: Ben Orbit Narrator
- VOICE_ID: `kDch6ACCIpqgQ0NsU9kk`
- MODEL_ID: `eleven_v3`
- Settings: stability 0.34 / similarity_boost 0.78 / style 0.42 / speed 1.04 / use_speaker_boost True
- Auth: `api_key` via `el_auth.load_token(prefer_api_key=True)` + Germs `.env` + `07_Content-Ops/.env`
- Generator: `vo/_generate_hos007_vo_v01.py` (pattern from HOS 005 `_generate_all_vo_v01.py`)

## Script

- Source: `origin/main` → `02_Video-Projects/007_The-First-Vaccine/01_Script/vaccine_script_master_v01.md`
- Desk copy truncated at `---` before New-claims table (prose-only part 05; table would have leaked past `#|[` filter)
- Filter: drop blank / `^\s*(#|\[|<!--)` — same as vo_check
- Phipps line present in part 03: *In his own notes, Jenner described him simply as a healthy boy, about eight years old.*
- Spoken totals: **1197 words / 6733 chars**

## Credits (ElevenLabs Creator)

| | Value |
|---|---|
| Limit | 209536 |
| Used before (first snapshot) | 109367 |
| Remaining before | 100169 |
| Used at TTS start | 109976 |
| Remaining at TTS start | 99560 |
| Used after (refreshed) | 114054 |
| Remaining after | 95482 |
| Script chars sent | 6733 |
| API delta (refreshed − TTS start) | 4078 |

Note: `character_count` lagged mid-mint (same as 006 shorts). Stayed well above ~50k headroom floor. No plan upgrade.

## Per-part results (KEEP takes)

| Part | Slug | Keep | Dur | Mean / Peak | Loudness+silence | vo_check words | sha256 |
|---|---|---|---|---|---|---|---|
| 01 | the_speckled_monster | **v01b** | 105.76s | -22.1 / -2.0 dB | **PASS** | ASR FAIL×1* | `11137318bde9dad3ad122d31f77c54e39f4883d1c315a514b92a4d0a89fc7bac` |
| 02 | the_milkmaids_secret | **v01** | 129.04s | -20.8 / -1.3 dB | **PASS** | ASR FAIL×1* | `a4c4ad87d73b9ffca9dfc9e7530cfc10f1d4a68f27c612054be4669a9a9ae21e` |
| 03 | a_pail_a_lancet_and_a_boy | **v01** | 69.76s | -20.4 / -1.0 dB | **PASS** | ASR FAIL×3* | `afbbe16957cd3f6d33591937b5fc6b5edba02712278c083c260c87f6f03cada0` |
| 04 | the_test | **v01b** | 92.16s | -21.1 / -1.7 dB | **PASS** | ASR FAIL×1* | `090676adfb3c3dc9d4ebe94243483702359b71cfbc9f38ec8bfae8f5f532aa8d` |
| 05 | the_word_that_saved_millions | **v01b** | 102.56s | -21.3 / -1.9 dB | **PASS** | ASR FAIL×1* | `18b725326c0b40e6bba2250be9f25a2581366a2ff76a2121fa889191f727557f` |

\*Word-check: `vo_check` under Python 3.12 + faster-whisper (`small.en`). Remaining word FAILs are **ASR false positives** — ElevenLabs `*_align.json` contains the exact script span for each dispute (e.g. part01 `how did a cow`, part03 Phipps + matter sentence, part04 `first of July`, part02 `Berkeley`). No TTS v02 retake (would not fix ASR; saves credits). Peak hot takes remastered with `ffmpeg volume=-0.8dB` → v01b.

### Part notes

- **Part 01 (the_speckled_monster)**: peak remaster −0.8 dB from v01; EL align confirms script words
  - vo_check: replace at ~0:04.96: script 'so how did a cow end up' / heard 'so how did the cow end up' — listen, then regenerate that sentence alone if real
- **Part 02 (the_milkmaids_secret)**: raw v01; loudness PASS; berkeley→barclay is ASR
  - vo_check: replace at ~1:09.58: script 'little town of berkeley a country doctor' / heard 'little town of barclay a country doctor' — listen, then regenerate that sentence alone if real
- **Part 03 (a_pail_a_lancet_and_a_boy)**: raw v01; loudness PASS; Jenner/matter skips are ASR; Phipps line in align
  - vo_check: replace at ~0:15.86: script 'saw his chance on the of may' / heard 'saw his chance now the of may' — listen, then regenerate that sentence alone if real
  - vo_check: replace at ~0:18.36: script 'the of may he took a little matter from of the spots on sarah's hand' / heard 'the of may he'd on sarah's hand' — listen, then regenerate that sentence alone if real
  - vo_check: delete at ~0:33.54: script 'week james felt a little unwell a' / heard 'week james felt little unwell a' — listen, then regenerate that sentence alone if real
- **Part 04 (the_test)**: peak remaster −0.8 dB; 'first' of July in align (whisper drops ordinal-as-digit)
  - vo_check: delete at ~0:00.32: script 'on the first of july jenner' / heard 'on the of july jenner' — listen, then regenerate that sentence alone if real
- **Part 05 (the_word_that_saved_millions)**: peak remaster −0.8 dB; spelling honour/honor ASR
  - vo_check: replace at ~0:41.38: script 'a disease that had killed of millions' / heard 'a disease that have killed of millions' — listen, then regenerate that sentence alone if real

## Paths

- Desk: `/Users/benjaminoats/_desk/007/vo_20261004`
- Listen (all parts): `/Users/benjaminoats/_desk/007/vo_20261004/hos_007_vo_all_parts_listen_v01.mp3` (499.28s) sha256 `b615b8e8aabbbf8f0d179d83608e2b1affa9873986955cb95f73f62272602f9c`
- Meta: `vo/VO_TAKES_v01.json`, `vo/VO_TAKES_KEEP.json`, `vo/vo_check/partNN_*_vo_check.json`
- Raw v01 mp3 kept alongside v01b remasters

## Constraints honoured

- No picture / Vertex / Flow mint
- No merge/close of #180 (or #204/#205)
- Creator plan only; no upgrade
- Did not dirty `grok/hos-vo-first-20261004` (#204) with VO media; binaries on desk only



## Landed copy (Grok Bot sync)

- Repo/YouTube tree (same inode via symlink): `/Users/benjaminoats/code/history-of-science/02_Video-Projects/007_The-First-Vaccine/02_Voiceover`
- `VO_META.json` written beside KEEP takes
- Script SHA256 `8939f2933d33ffc35094beba320c8f61dfe80abf48bbb85b897ab5860cdee9fc`
- Script introduced/fixed on `afcb26dfd53345c1a9a3635becc4a256997b754b 007 Phipps line fix + 008 Lightning script v01 (#203)`
- Repo HEAD at land: `a99b59cf69c9e88cdd46769dc9967c2d7b36c5a3`
- Live credits after session: used 114372 / rem **95164** of 209536 (Creator)
- Wordcheck (extract vs whisper): parts 02/04/05 **PASS**; 01/03 **FAIL** hard notes (align confirms script; Claude ear for part01 a/the cow + part03 matter sentence)
