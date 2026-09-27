# Voiceover — HOS 004

**Engine:** ElevenLabs **Ben Orbit Narrator** only (`kDch6ACCIpqgQ0NsU9kk`). Settings from `04_Audio/tools/orbit_voice.py` (do not edit shared `VOICE_SETTINGS` speed — override per call if needed).

**Spoken text (locked from `01_Script/atom_script_master_v02.md`):** identical `*_v01.txt` / `*_v02.txt`.

| Part | Text | Master (current listen) |
|---|---|---|
| 01 Cold open | `part01_cold_open_v02.txt` | `05_Master/hos_004_part01_vo_v02.wav` |
| 02 The Table That Broke Its Own Rule | `part02_the_table_that_broke_its_own_rule_v02.txt` | `05_Master/hos_004_part02_vo_v02.wav` |
| 03 The Crumb Inside the Atom | `part03_the_crumb_inside_the_atom_v02.txt` | `05_Master/hos_004_part03_vo_v02.wav` |
| 04 The Shell That Bounced Back | `part04_the_shell_that_bounced_back_v02.txt` | `05_Master/hos_004_part04_vo_v02.wav` |
| 05 Counting With X-rays | `part05_counting_with_x_rays_v02.txt` | `05_Master/hos_004_part05_vo_v02.wav` |

**v02 route:** eleven_v3 ignored per-call speed (1.15 / 1.12) → discarded. Built from v01 by capping silences to 0.60 s + 0.35 s beat before “count”. No atempo. Meta: `05_Master/VO_MASTERS_v02.json`. Listen: `hos_004_vo_all_parts_listen_v02.mp3`.

Generators: `_generate_all_vo_v01.py` (original mint) · `_generate_all_vo_v02.py` (speed attempt; fallbacks applied outside).

Media (mp3/wav) stays out of git. Record paths + sha256 in `production-status.md` / `VO_MASTERS_v0N.json`.
