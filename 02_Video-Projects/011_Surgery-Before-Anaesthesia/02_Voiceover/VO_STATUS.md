# HOS 011 Anesthesia VO — locked `hos_011_vo_v01` (J2475, 10 Nov 2026)

VO **locked**. The J2475 section at the foot is the lock record. The sections above it are the J2245 take record of 6 Nov, unchanged.

Listen file: `02_Voiceover/hos_011_vo_v01.wav` (532.72 s). WAV and MP3 stay on the Mini in this worktree (`/_desk/worktrees/J2245-011-vo`). They are gitignored.

| File | What | Duration | Check |
|---|---|---|---|
| `hos_011_vo_v01.wav` | Full take, five chapters, 0.7 s gaps. sha256 `d873f1d0c9158087fd61ce0b9f53de985055d778cd58b8df70c67c0701300ae2` | 532.72 s | Scribe 96.93% (20 runs, all numerals or UK/US spelling). −19.6 LUFS, mean −23.1 dB, peak −3.6 dB. `vo_check` PASS, 0 fails, 14 warns. |
| `parts/hos_011_vo_v01/ch00.wav` | Open | 86.80 s | PASS. 165 wpm. Question 36.3 s, promise 48.1 s. |
| `parts/hos_011_vo_v01/ch01.wav` | A Gas That Made People Laugh | 88.16 s | PASS. Pace warn 136 wpm. |
| `parts/hos_011_vo_v01/ch02.wav` | This Is No Humbug | 95.52 s | PASS. Pace warn 141 wpm. |
| `parts/hos_011_vo_v01/ch03.wav` | The Fight Over Who Was First | 93.68 s | PASS. Pace warn, plus ether/aether, Letheon/Lethion, anaesthesia/anesthesia (sounds alike). |
| `parts/hos_011_vo_v01/ch04.wav` | Across the Ocean | 165.76 s | **FAIL.** Two silences: 1.52 s at 0:27.87 and 1.55 s at 0:33.47. Same pauses in the full file at 6:34.83 and 6:40.43. They are inside this chapter, not the 0.7 s chapter gaps. |

MP3 sha256 `9fdd84d50ac2f85bcdf8aea0d5ceefd261cae5458dafa1e6865adf2a3053f496` (also in `hos_011_vo_v01_TAKE.json`).

Voice: Ben Orbit Narrator, `eleven_v3`, speed 1.04. Orders stored on the take: J2231, J0224, J2245. Script: `01_Script/surgery_script_master_v02.md` (1,230 spoken words, 6,941 spoken characters).

## Word check

`vo_check.py` on Python 3.12 (`faster-whisper small.en`) ran on each chapter wav and on the full wav. Chapter checks used that chapter's spoken text with a `## PART 01` header so a long pause fails the part. The full file was checked against the locked master with no `--part`, so a pause over 1.5 s is a warning there, not a fail.

Scribe `scribe_v2` on the full take (96.93%) differed from the script only where the checker already normalises:

- years and ordinals heard as digits (`eighteen forty-six` / `1846`, `twenty-first` / `21st`, `ninety thousand` / `90 000`)
- UK spellings heard in US form (`vapour`, `travelling`, `coloured`, `anaesthesia`, `anaesthetic`, `anaesthetist`)
- `wells's` / `wells'`

No Scribe run shows a dropped clause. The whisper warns that are not the two pauses are marked sounds-alike: Humphry/Humphrey, Wells's, Ether Dome, Letheon, anaesthesia/anesthesia, patient/patience, gentlemen/gentleman, an anaesthetist / and anesthetist, asleep/to sleep. Chapter 3 also heard "ether" as "aether" and "monument to ether" the same way. Chapter 4 also heard "turned" as "turn". Those need a listen. This session did not play the audio.

## Credits

ElevenLabs before the take: 93,404 of 121,114 left (used 27,710). After: 90,350 left (used 30,764). Counter delta 3,054 against 6,941 spoken characters. Floor 0. Nothing bought, nothing billed past the balance.

No picture. No upload.

## J2475 — VO locked as `hos_011_vo_v01` (10 Nov 2026)

`J2286` (Gemini, listening review of all five chapters) returned **KEEP**: no pickups, no re-recording; the two 1.5 s pauses in *Across the Ocean* sit inside a held beat and stay. The acting Chief closed `J2245` on 10 Nov and the job brief for `J2475` orders this lock. This section records that decision; the worker who wrote it did not listen to the audio and makes no judgement of its own.

| Item | Value |
|---|---|
| Take | `hos_011_vo_v01.wav` (532.72 s, five chapters, 0.7 s gaps) |
| WAV sha256 | `d873f1d0c9158087fd61ce0b9f53de985055d778cd58b8df70c67c0701300ae2` (from the J2245 take record; the WAV is gitignored and was not re-hashed in J2475) |
| MP3 sha256 | `9fdd84d50ac2f85bcdf8aea0d5ceefd261cae5458dafa1e6865adf2a3053f496` |
| Verdict | `J2286` KEEP; acting Chief closed `J2245`, 10 Nov 2026 |
| Script | `01_Script/surgery_script_master_v02.md` |
| Timings | `stt/hos_011_vo_v01/words.srt` (193 phrase cues) and `stt/hos_011_vo_v01/stt_raw.json` |
| Loudness | −19.6 LUFS, peak −3.6 dB |

Chapter voice starts on the VO clock for the edit: ch01 0:00.00, ch02 1:27.50, ch03 2:56.36, ch04 4:32.58, ch05 6:06.96. Film 8:52.72. The shot list built on these timings is `07_Edit-Project/SHOT_LIST_v01.md`.
