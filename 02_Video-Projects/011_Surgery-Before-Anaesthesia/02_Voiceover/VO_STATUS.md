# HOS 011 Anesthesia VO — locked `hos_011_vo_v01` (J2245 / J2286, 10 Nov 2026)

VO **locked**. Listen file `02_Voiceover/hos_011_vo_v01.wav` (532.720 s, 8:52.72). WAV and MP3 stay on the Mini (`/Users/benjaminoats/_desk/media/HOS/011_Surgery-Before-Anaesthesia/02_Voiceover/`); they are gitignored. The J2286 / J2245 section at the foot of this file is the lock. Earlier sections are the v01 recording and checker record.

| File | What | Duration | Check |
|---|---|---|---|
| `hos_011_vo_v01.wav` | Full locked take, five chapters, 0.7 s gaps. sha256 `d873f1d0c9158087fd61ce0b9f53de985055d778cd58b8df70c67c0701300ae2` | 532.72 s | Scribe 96.93% (20 runs, all numerals or UK/US spelling). −19.6 LUFS, mean −23.1 dB, peak −3.6 dB. `vo_check` PASS, 0 fails, 14 warns. J2286 ear review: **KEEP**. |
| `parts/hos_011_vo_v01/ch00.wav` | Open (*The Fastest Knife*) | 86.80 s | PASS. 165 wpm. Question 36.3 s, promise 48.1 s. J2286: **KEEP**. |
| `parts/hos_011_vo_v01/ch01.wav` | A Gas That Made People Laugh | 88.16 s | PASS. Pace warn 136 wpm. J2286: **KEEP**. |
| `parts/hos_011_vo_v01/ch02.wav` | This Is No Humbug | 95.52 s | PASS. Pace warn 141 wpm. J2286: **KEEP**. |
| `parts/hos_011_vo_v01/ch03.wav` | The Fight Over Who Was First | 93.68 s | PASS. Pace warn, plus ether/aether, Letheon/Lethion, anaesthesia/anesthesia (sounds alike). J2286: **KEEP**. |
| `parts/hos_011_vo_v01/ch04.wav` | Across the Ocean | 165.76 s | `vo_check` `--part` warn/fail on two internal dramatic pauses: 1.52 s at 0:27.87 and 1.55 s at 0:33.47 (full file 6:34.83 and 6:40.43). J2286 ear review: **KEEP** (both pauses sit inside the held beat after *"One evening in November 1847, in his dining room in Edinburgh, Simpson and two assistants poured a heavy, sweet-smelling liquid into tumblers..."* and stay; editor may trim each pause by ~0.35–0.45 s at assembly if needed). |

MP3 `hos_011_vo_v01.mp3` sha256 `9fdd84d50ac2f85bcdf8aea0d5ceefd261cae5458dafa1e6865adf2a3053f496` (also in `hos_011_vo_v01_TAKE.json`).

Voice: Ben Orbit Narrator, `eleven_v3`, speed 1.04. Orders stored on the take: J2231, J0224, J2245. Script: `01_Script/surgery_script_master_v02.md` (1,230 spoken words, 6,941 spoken characters).

## Word check

`vo_check.py` on Python 3.12 (`faster-whisper small.en`) ran on each chapter wav and on the full wav. Chapter checks used that chapter's spoken text with a `## PART 01` header so a long pause fails the part. The full file was checked against the locked master with no `--part`, so a pause over 1.5 s is a warning there, not a fail.

Scribe `scribe_v2` on the full take (96.93%) differed from the script only where the checker already normalises:

- years and ordinals heard as digits (`eighteen forty-six` / `1846`, `twenty-first` / `21st`, `ninety thousand` / `90 000`)
- UK spellings heard in US form (`vapour`, `travelling`, `coloured`, `anaesthesia`, `anaesthetic`, `anaesthetist`)
- `wells's` / `wells'`

No Scribe run shows a dropped clause. The whisper warns that are not the two pauses are marked sounds-alike: Humphry/Humphrey, Wells's, Ether Dome, Letheon, anaesthesia/anesthesia, patient/patience, gentlemen/gentleman, an anaesthetist / and anesthetist, asleep/to sleep. Chapter 3 also heard "ether" as "aether" and "monument to ether" the same way. Chapter 4 also heard "turned" as "turn". All were verified clean by ear in `J2286` (below).

## Credits

ElevenLabs before the take: 93,404 of 121,114 left (used 27,710). After: 90,350 left (used 30,764). Counter delta 3,054 against 6,941 spoken characters. Floor 0. Nothing bought, nothing billed past the balance.

## J2286 / J2245 — VO locked as `hos_011_vo_v01` (10 Nov 2026)

Specialist audio listening review (`J2286`, `jobs/reviews/J2286/REVIEW.md`, 6 Nov 2026) listened directly to `hos_011_vo_v01.wav` and all five chapter WAVs (`ch00.wav`–`ch04.wav`) and returned **KEEP** across all five chapters, with **0 pickups** and **0 re-recordings**. Acting Chief accepted the `J2286` `KEEP` verdict, closed `J2245` on 10 Nov 2026 (`jobs/reviews/J2245/REVIEW.md`), and carried the VO artifacts onto `main` in commit `45f0dbd7` (`J2502`, PR #488). `J2475` records this VO lock and times `SHOT_LIST_v01.md` and `PICTURE_PLAN_v01.json` against `stt/hos_011_vo_v01/words.srt`.

| Field | Value |
|---|---|
| Locked take | `02_Voiceover/hos_011_vo_v01.wav` |
| WAV SHA-256 | `d873f1d0c9158087fd61ce0b9f53de985055d778cd58b8df70c67c0701300ae2` |
| MP3 | `02_Voiceover/hos_011_vo_v01.mp3` (libmp3lame 192k, 44.1 kHz mono) |
| MP3 SHA-256 | `9fdd84d50ac2f85bcdf8aea0d5ceefd261cae5458dafa1e6865adf2a3053f496` |
| Duration | `532.720 s` (`8:52.72`), 5 chapters (`ch00`–`ch04`) with `0.70 s` inter-chapter gaps |
| Loudness | `I -19.6 LUFS`, mean `-23.1 dB`, true peak `-3.6 dBTP`, `139 wpm` |
| Checker (`vo_check`) | `vo_check/full.json` (`PASS`, `0` fails, `14` warns: `12` ASR sounds-alike homophones + `2` `ch04` dramatic pauses over `1.50 s`) |
| Scribe (`scribe_v2`) | `96.93%` (`20` numeral/UK-US orthographic diffs; `0` dropped or added words) |
| Word timings | `stt/hos_011_vo_v01/words.srt` and `stt/hos_011_vo_v01/stt_raw.json` (`1,230` words) |
| Listening verdict (`J2286`) | **KEEP** on all 5 chapters (`ch00`–`ch04`). Every Whisper sounds-alike warning (`Humphry`, `Wells's`, `Ether Dome`, `Letheon`, `anaesthesia`, `patient`, `gentlemen`, `an anaesthetist`, `asleep`, `ether`, `monument to ether`, `turned`) is clearly spoken in the audio. |
| Edit notes (`J2286`) | (1) The two pauses in `ch04` (`1.52 s` at `6:34.83` after *"One evening in November 1847,"* and `1.55 s` at `6:40.43` after *"...Simpson and two assistants"*) are clean room-tone silences inside a held dramatic beat; accepted in the locked VO (editor may trim `~0.35–0.45 s` from each at assembly if desired). (2) Apply a `30–50 ms` `qsin` micro-fade to the final `50 ms` of each chapter WAV (`ch00`–`ch04`) at assembly so every chapter tail drops below `-50 dBFS`. |

### Chapter clock on `hos_011_vo_v01` (`532.72 s` VO + `2.58 s` end card = `535.30 s` / `8:55.30`)

| Chapter | Part | Script section | Chapter WAV | VO start (`s`) | VO end (`s`) | VO span (`m:ss`) | Inter-chapter gap (`s`) |
|---|---|---|---|---:|---:|---|---|
| `ch00` | Part 01 | Cold Open — *The Fastest Knife* (no card) | `parts/hos_011_vo_v01/ch00.wav` (`86.80 s`) | `0.00` | `86.80` | `0:00.00–1:26.80` | `86.80–87.50` (`0.70 s`) |
| `ch01` | Part 02 | `[CHAPTER CARD: A Gas That Made People Laugh]` | `parts/hos_011_vo_v01/ch01.wav` (`88.16 s`) | `87.50` | `175.66` | `1:27.50–2:55.66` | `175.66–176.36` (`0.70 s`) |
| `ch02` | Part 03 | `[CHAPTER CARD: "This Is No Humbug"]` | `parts/hos_011_vo_v01/ch02.wav` (`95.52 s`) | `176.36` | `271.88` | `2:56.36–4:31.88` | `271.88–272.58` (`0.70 s`) |
| `ch03` | Part 04 | `[CHAPTER CARD: The Fight Over Who Was First]` | `parts/hos_011_vo_v01/ch03.wav` (`93.68 s`) | `272.58` | `366.26` | `4:32.58–6:06.26` | `366.26–366.96` (`0.70 s`) |
| `ch04` | Part 05 | `[CHAPTER CARD: Across the Ocean]` + Closing | `parts/hos_011_vo_v01/ch04.wav` (`165.76 s`) | `366.96` | `532.72` | `6:06.96–8:52.72` | `532.72–535.30` (`2.58 s` end-card hold) |

No re-take. No ElevenLabs spend. No paid picture minted.

