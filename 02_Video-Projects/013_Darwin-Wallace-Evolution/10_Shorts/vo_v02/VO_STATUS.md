# HOS 013 Shorts VO — `hos_013_short_A_v02` and `hos_013_short_B_v02` (J2246, 6 Nov 2026)

This is a take record, not a VO lock. No one has passed these Shorts.

The long stays locked as `02_Voiceover/hos_013_vo_v03a`. These two files are the Test B Shorts only.

Audio is gitignored. It is on the Mini in this worktree and copied to `/Users/benjaminoats/_desk/media/HOS/013_Darwin-Wallace-Evolution/10_Shorts/vo_v02/` (same hashes).

| File | What | Duration | Check |
|---|---|---|---|
| `hos_013_short_A_v02.wav` | *How Did Darwin Discover Evolution?* 60 spoken words. sha256 `9f80fa1c22951b5f7d25b2365fa5d62a58e848898262e6d5365bb2e68047bef8` | 26.64 s | Scribe 95.08%. The only mismatch is `eighteen thirty-five` heard as `1835`. −20.3 LUFS, mean −23.7 dB, peak −3.9 dB. `vo_check` PASS, 0 word diffs. Pace warn 140 wpm. |
| `hos_013_short_B_v02.wav` | *What Is Survival of the Fittest?* 61 spoken words. sha256 `6745bd813bd390bdf5091460bd9b5425eca568e4dbb3cf37f2c0a53f70ad47c0` | 26.00 s | Scribe 95.16%. The only mismatch is `eighteen sixty-four` heard as `1864`. −20.6 LUFS, mean −24.0 dB, peak −4.0 dB. `vo_check` PASS. Pace warn 143 wpm. One sounds-alike warn: Russel / Russell at 0:11.42. |

MP3 sha256: A `ba46ffaa29dab5ef3dfcc3af7f66c31f3550f90dadcc4e7ed305f643d8c384e1`, B `9e1eaa2fb9ae2719dd378895820ed7599d8c8532d94f5f39475edf00635c6631`.

Voice: Ben Orbit Narrator, `eleven_v3`, speed 1.04, through `vo_take.py` / `el_client.py`. Orders on the takes: J2240, J2246. Scripts: `10_Shorts/vo_v02/hos_013_short_A_v02.txt` (356 characters) and `hos_013_short_B_v02.txt` (339 characters).

## Word check

`vo_check_py312.sh` (`faster-whisper small.en`) on each wav, against that Short's txt. JSON: `vo_check/hos_013_short_A_v02.json` and `vo_check/hos_013_short_B_v02.json`.

Scribe word timings: `stt/<stem>/words.json` (start, end, text) and `stt/<stem>/words.srt`.

- Years heard as digits. The checker drops those number words, so both diffs are empty of real missing words.
- Short B: whisper wrote "Russell" where the script says "Russel" (Alfred Russel Wallace) at about 0:11.42. Marked sounds-alike. This session did not play the audio.
- Pace warns are the long-film line (under 145 wpm). Both Shorts are inside 22–27 s as voice alone.

## Length for the later cut

Voice alone is inside 22–27 s (A 26.64 s, B 26.00 s). A later 1.0 s picture tail on A would be 27.64 s and would fail the Short gate. No time-stretch was applied.

## Credits

ElevenLabs before the two takes: 90,171 of 121,114 left (used 30,943). After a fresh read: 89,847 left (used 31,267). Counter delta 324 against 695 spoken characters. The per-take subscription read lagged (A delta 0, B delta 18). Floor 0. Nothing bought.

No picture. No upload.
