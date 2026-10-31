# HOS 013 Darwin–Wallace VO — J0807 (31 Oct 2026)

Parked for Chief. Not a lock.

Listen to `hos_013_vo_v02.wav` (512.48 s). `hos_013_vo_v01.wav` is the untouched API take.

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
