# HOS 013 Darwin–Wallace VO — locked `hos_013_vo_v03a` (J1310, 31 Oct 2026)

VO **locked**. Listen file `02_Voiceover/hos_013_vo_v03a.wav` (512.480 s). WAV and MP3 stay on the Mini; they are gitignored. The J1310 section below is the lock. Earlier sections are the v01–v03 record.

J1301 ran unmodified `vo_check.py` on `hos_013_vo_v03.wav`: checker PASS, 0 fails. SHA-256 `d56ba2a45a76125e29b0d620ab84772a9311399354c07d860ac168938ff05038`. This is the checker result, not a VO lock. `hos_013_vo_v02.wav` is preserved. `hos_013_vo_v01.wav` is the untouched API take.

| File | What | Duration | Check |
|---|---|---|---|
| `hos_013_vo_v01.wav` | Full take, six chapters, 0.7 s gaps. sha256 `d41c910a…b68d4` | 512.70 s | Scribe 94.8% (number and spelling forms). Loudness −19.5 LUFS, mean −22.9 dB, peak −3.6 dB. `vo_check` FAIL, see below. |
| `hos_013_pickup_credit_v01.wav` | One sentence: "So Darwin could simply hide the letter, and keep the credit?" | 3.44 s | Scribe 100%. −19.6 LUFS. |
| `hos_013_vo_v02.wav` | v01 with that sentence spliced in place of "credits?". sha256 `fa100bb9…b47b6` | 512.48 s | Clip re-hear: "keep the credit. Case closed." `vo_check` still FAIL on the same five v01 lines (none of them this sentence). Mean −23.0 dB, peak −3.6 dB, 146 wpm. Cut record: `hos_013_vo_v02_SPLICE.json`. |

Voice: Ben Orbit Narrator, `eleven_v3`, speed 1.04. Orders: J0307, `60d4f8a9`. Script: `01_Script/darwin_script_master_v02.md` (1,227 words, 7,034 spoken characters).

## Word check

`vo_check` on v01 (faster-whisper small.en) reported five fails. Scribe `scribe_v2` on the same take:

- "what was doing the shaping" — Scribe logprob 0. Whisper wrote "was shaping".
- "Charles Lyell" — Scribe, both times. Whisper wrote "Lyle". A clip re-hear also heard Lyell.
- "On the first of July" — Scribe heard "1st", which the checker drops as a numeral, so "first" looks missing.
- "half better beak" — Scribe heard "better". Whisper wrote "bedder".
- "keep the credit" — Scribe and a clip re-hear both heard **credits**. This one is real. The pickup replaces it in v02 (v01 time 330.80–334.20, about 5:31).

`vo_check` also warns: a 1.69 s silence at 0:20, pace 146 wpm, and UK/US or name spellings (unlabelled, islands', Russel, Linnean, Fleeming).

The last line is complete in Scribe: "…how biologists explain the living world today." The final 50 ms of v02 sits at −40.6 dB mean.

## Credits

ElevenLabs before the take: 104,886 of 121,114 left (used 16,228). After v01 and the pickup: 101,592 left (used 19,522). Counter delta 3,294. Nothing bought, nothing billed past the balance.

No picture. No upload.

## J1300 — shaping re-hear and v03 (31 Oct 2026)

Final take for the J1301 check: **v03**. This is a worker repair record, not a VO lock or final sign-off.


Three-model evidence: base.en and small.en hear **doing was shaping**; medium.en hears **doing the shaping**. A tighter clip repeats the disagreement. The envelope shows an energy shoulder but cannot identify the article. One authorized 31-character pickup of the exact locked sentence returned Scribe **100%**; no money spent.

v03 SHA-256 `d56ba2a45a76125e29b0d620ab84772a9311399354c07d860ac168938ff05038`; **512.48 s, −19.5 LUFS**, mean −23.0 dB, peak −3.6 dB. v01/v02 unchanged. [Full transcripts, word timings/probabilities, envelope and repair record](rehear_J1300/REPORT.md). Cut record: `hos_013_vo_v03_SPLICE.json`.

Not a lock at the time of J1300. The J1301 check is recorded below. No picture or upload.

## J1301 — vo_check on v03 (31 Oct 2026)

Checker result: **PASS**, 0 fails. Not a VO lock. Parked for Chief review.

| | |
|---|---|
| Take | `hos_013_vo_v03.wav` |
| SHA-256 | `d56ba2a45a76125e29b0d620ab84772a9311399354c07d860ac168938ff05038` (matches J1300) |
| Duration | 512.48 s (8:32.48) |
| Levels | mean −23.0 dB, peak −3.6 dB, 146 wpm |
| ASR | faster-whisper small.en |
| Script | `01_Script/darwin_script_master_v02.md` |
| Checker | `vo_check.py` on main after J1299 merge `725a6e45` (PR #392). Run with `vo_check_py312.sh` and `--json` only. No local edits. |
| JSON | `vo_check/hos_013_vo_v03.json` |

The five v02 fails are gone: "doing the shaping", both "Lyell" lines, "first of July", and "better beak". Six warns remain, the same kind already on v02: a 1.69 s silence at 0:20.34 (part join) and five sounds-alike spellings (unlabelled, islands', Russel, Linnean, Fleeming).

No regeneration. No picture. No upload.

## J1310 — VO locked as `hos_013_vo_v03a` (31 Oct 2026)

Chief h39 on J1301 passed `hos_013_vo_v03` on words, loudness and length. This build applies Chief's measured chapter-end fades and locks the take. No re-take, no ElevenLabs, no paid STT. Rulings: J1301 h39, and the chain J0807 / J1299 / J1300. v01, v02, v03, both pickups, parts and the earlier stt folders are untouched.

| | |
|---|---|
| Take | `hos_013_vo_v03a.wav` |
| WAV SHA-256 | `837178125a72fb250d255f1039c5cb7f8630bbb313cf23801a1155f257d796e0` |
| MP3 | `hos_013_vo_v03a.mp3` (libmp3lame 128k, 48 kHz stereo) |
| MP3 SHA-256 | `ada7eaa775104ee5dea9e9be98155abfc0b1e9fda010097f42ca9fa25bed7f85` |
| Frames | 24,599,040 (512.480 s, 8:32.48), pcm_s16le 48 kHz stereo |
| Loudness | I −19.5 LUFS, true peak −3.6 dBTP, LRA 5.0 LU |
| Checker | unmodified `vo_check_py312.sh --json` against `01_Script/darwin_script_master_v02.md`. PASS, 0 fails. 146 wpm, mean −23.0 dB, peak −3.6 dB, 1,174 script words, 1,173 heard. |
| JSON | `vo_check/hos_013_vo_v03a.json` |
| Word timings | `stt/hos_013_vo_v03a/words_fw_small_en.json` (faster-whisper small.en, CPU int8, 1,213 words). No Scribe. |
| Builder | `vo_build_h39/fade_v03a.py` and `vo_build_h39/check_v03a.py`, copied from Chief h39 and not edited. |

`check_v03a.py` last 10 ms, every end below −50 dBFS, last sample 0/0. Null vs v03 outside the six windows: max 0.

| Chapter | Window | Last 10 ms |
|---|---|---|
| ch00 "changes." | 74.740–74.800 s (60 ms) | −56.34 dBFS |
| ch01 "shaping?" | 170.250–170.330 s (80 ms) | −53.88 dBFS |
| ch02 "someone?" | 275.540–275.560 s (20 ms) | −64.70 dBFS |
| ch03 "heard?" | 365.580–365.640 s (60 ms) | −55.30 dBFS |
| ch04 "print." | 447.440–447.460 s (20 ms) | −68.92 dBFS |
| ch05 "today." | 512.440–512.480 s (40 ms) | −59.94 dBFS |

Chapter starts on the VO clock for the edit (script card times shift): ch01 1:15.50, ch02 2:51.08, ch03 4:36.26, ch04 6:06.34, ch05 7:28.16. Film 8:32.48.

The 1.69 s beat after "into the open." at 0:20.34 is accepted in the VO. The editor may tighten it to no less than 0.6 s if the hook needs it.

`vo_check` warns, none of them fails: that 1.69 s silence, and the same sounds-alike spellings as v03 (unlabelled, islands', Russel, Linnean, Fleeming). One extra sounds-alike warn at 4:50.50, "this time" heard as "this times". That moment sits outside every fade window, and the samples there match v03.

No mux. No picture. No upload.
