# Production status — 004 Why Is the Periodic Table in This Order?

| Field | Value |
|---|---|
| Slug | `004_Whats-Really-Inside-An-Atom` |
| Channel | `@HistoryOfScienceYT` only |
| Topic | Ben picked 26 Sep 2026 (the atom; why the periodic table has its order) |
| Title | *Why Is the Periodic Table in This Order?* (main, chosen 26 Sep from the audit); Test & Compare *What's Really Inside an Atom?* and *How Small Can You Cut Gold?*. Folder slug unchanged. |
| Script | `01_Script/atom_script_master_v02.md`. **Ben: KEEP (26 Sep 2026).** Narration locked; v01 kept as `atom_script_v01_ben.md`. |
| Script review | 88.9. **Passed by hand by Ben, 26 Sep 2026** (reviewer counting bug; see note) |
| Pre-build vidIQ audit | **Signed off by Ben, 26 Sep 2026.** vidIQ waived; public search data used (`11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`) |
| Episode gate | **Passed by Ben (manual), 26 Sep 2026.** `gate:episode` still prints REJECT on the reviewer score; that line is overridden. All other checks OK. |
| VO | **READY (27 Sep 2026).** Ben Orbit Narrator · five part masters · see table below. Copied to iCloud for phone listen. |
| Picture | not started (Flow Veo 3.1, plate library) — **do not mint until Ben passes VO** |
| Runtime (recorded) | **536.160 s = 8:56** total VO (script estimate was ~8:25; re-time parts from this VO) |
| Air | Thu 15 Oct 2026 18:00 UK, normal publish (no Premiere). Fallback Thu 22 Oct. `11_Upload-Package/LAUNCH_PLAN.md` |
| Shorts | Fri 16 (gold coin, 004) · Sun 18 (002) · Tue 20 Oct (003), 11:30 UK |

**Reviewer note (26 Sep):** the script reviewer counts at most one escalation word and one science word per script (its two regexes lack the global flag), which caps those two scores. With that fixed, v02 scores 91.8. Ben decides whether the fix goes in; it was not changed to pass this script.

Only one version of the script is live: v02. Showrunner holds its own edits until Ben signs off.

---

## STOP — VO ready, awaiting Ben listen (27 Sep 2026)

**Do not start picture / plate boards / Flow until Ben passes these five VO masters.**

Voice: ElevenLabs **Ben Orbit Narrator** (`kDch6ACCIpqgQ0NsU9kk`) · settings from `04_Audio/tools/orbit_voice.py` · model `eleven_v3`.

Spoken text (locked words from `atom_script_master_v02.md`):

| Part | Text |
|---|---|
| 01 | `02_Voiceover/part01_cold_open_v01.txt` |
| 02 | `02_Voiceover/part02_the_table_that_broke_its_own_rule_v01.txt` |
| 03 | `02_Voiceover/part03_the_crumb_inside_the_atom_v01.txt` |
| 04 | `02_Voiceover/part04_the_shell_that_bounced_back_v01.txt` |
| 05 | `02_Voiceover/part05_counting_with_x_rays_v01.txt` |

Masters (media out of git; record only):

| Part | Duration | Mean dB | WAV sha256 | Path |
|---|---|---|---|---|
| 01 | 75.440 s (1:15) | −23.8 | `32773ed38eed6693ac20a101a968bc34a4197294c88b1ddb0b1f668bc3077034` | `02_Voiceover/05_Master/hos_004_part01_vo_v01.wav` |
| 02 | 95.760 s (1:35) | −21.9 | `7e3c50ef0ef824b9ebb8b3b7af8a69832bd1a4c69baab2b8447a9d70aa61a70f` | `02_Voiceover/05_Master/hos_004_part02_vo_v01.wav` |
| 03 | 88.960 s (1:28) | −23.4 | `3db4205ae7c4df0bc403f087c517f8f4a00e70e07fef67ca39c0b22e35ad3805` | `02_Voiceover/05_Master/hos_004_part03_vo_v01.wav` |
| 04 | 118.880 s (1:58) | −24.8 | `c608a223f4ac6fcf29c3aaf1facc28beb6316be7b63fd6a41564c1eea2f9de23` | `02_Voiceover/05_Master/hos_004_part04_vo_v01.wav` |
| 05 | 157.120 s (2:37) | −24.3 | `8806482c4cbe96cf47d9c0962ac7f409c71040326f4b0ed9ad702b0b33180287` | `02_Voiceover/05_Master/hos_004_part05_vo_v01.wav` |
| **Total** | **536.160 s (8:56)** | — | meta `02_Voiceover/05_Master/VO_MASTERS_v01.json` | — |

**Phone listen (iCloud):**

`iCloud Drive/HOS UAT/004_Whats-Really-Inside-An-Atom/02_Voiceover/`

- Per-part: `05_Master/hos_004_part0N_vo_v01.mp3` (and `.wav`)
- Joined: `05_Master/hos_004_vo_all_parts_listen_v01.mp3`

Absolute (this machine worktree):  
`/Users/benjaminoats/YouTube/history-of-science-hos004-vo-8839/02_Video-Projects/004_Whats-Really-Inside-An-Atom/02_Voiceover/05_Master/`

**Next after Ben PASS:** plate boards → Flow Veo (steps 3+). No picture spend before then.
