# HOS compilation film: assembly inventory v01 (J0175)

Cursor, 12 Oct 2026, first run on J0175 (assembly). Plan and script locked by Chief (J0173, #293 `126bfec`); VO takes KEEP (J0174, #298 `d9e150b`). This file is the input list for the assembler: what exists, where, in what format, and where each film is cut. No picture is cut yet.

## Masters (the uploaded files, never a YouTube download)

| Order | Film | Master | Where | Length | Format | Plan runtime |
|---|---|---|---|---|---|---|
| 1 | 005 Harvey | `hos_005_master_v01.mp4` (sha256 `84476e06…`, per 005 production-status) | `~/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/09_Final-Export/` (worktree only; not in the main checkout or on the NAS) | 526.53 s (8:46.5) | 1920×1080, 30 fps, AAC 48k stereo | 8:49 (YouTube) |
| 2 | 006 Trees | **not finished** (picture ETA 25 Oct, airs Thu 5 Nov) | n/a | ~8:58 est. | n/a | ~8:58 |
| 3 | 001 Germs | `hos_001_germs_full_v02.mp4` (manifest `video`) | NAS `mac-mini-archive/YouTube/History Of Science/02_Video-Projects/001_How-Did-We-Discover-Germs/09_Final-Export/` | 364.55 s (6:04.6) | **1280×720, 24 fps** | 6:05 |
| 4 | 002 Periodic table | `hos_002_periodic_table_full_v02.mp4` (manifest `video`) | NAS `…/002_How-Did-We-Discover-The-Periodic-Table/09_Final-Export/` | 540.63 s (9:00.6) | 1920×1080, **24 fps** | 9:01 |
| 5 | 003 X-rays | `hos_003_full_polish_v01.mp4` (the only full cut in 09_Final-Export; 003 has no manifest `video` line, so Chief or the assembler confirms it against `frP_YrNShsU` before render) | NAS `…/003_Invisible-Bones-X-Rays/09_Final-Export/` | 425.71 s (7:05.7) | 1920×1080, **24 fps** | 7:06 |
| 6 | 004 Atom | `hos_004_full_v02.mp4` (manifest `video`; `full_v03` has the same length, not used) | main checkout `02_Video-Projects/004_Whats-Really-Inside-An-Atom/09_Final-Export/` | 524.70 s (8:44.7) | 1920×1080, 30 fps | 8:45 |

NAS files are read and copied to render scratch only; nothing on the NAS is touched.

**Normalise to one format before the concat:** 1920×1080, 30 fps (frame-rate conversion by duplication, `fps=30`, no interpolation), yuv420p, AAC 48 kHz stereo. 001 scales 1.5× (720p to 1080p), inside the 2.35× cap. Loudness: measure each master (two-pass `loudnorm`) and bring each to −14 LUFS integrated, −1 dBTP, so no film jumps in level against its neighbour.

## Trim points (Chief, J0173: trim the three end hand-offs)

Times are master time. Each cut sits in a measured VO pause (`silencedetect`, −28 dB, 0.3 s), checked against the film's own captions.

| Film | Keep | Cut at | Dropped | Evidence |
|---|---|---|---|---|
| 005 | 0:00 → 8:09.20 | 489.20 s | "Thirteen years later, a Dutch cloth merchant… That is where the story of germs begins." plus the end card and hold (8:09.2 → 8:46.5, 37.3 s) | caption 134 ends 8:08.533 "before anyone saw the last link."; pause 488.69–489.25 s |
| 006 | TBD | TBD | "…a young student fired tiny particles at gold" hand-off, end card and hold | needs 006's master |
| 004 | 0:00 → 8:11.40 | 491.40 s | "But the nucleus had one more secret… That's the next story." plus end card and hold (8:11.4 → 8:44.7, 33.3 s). The Closing replaces it. | caption 88 ends 8:10.818 "It's a count."; pause 491.06–491.68 s |
| 001, 002, 003 | whole master | none | none (generic end lines stay, per plan risk 2) | |

Each trimmed film gets 0.6 s of picture and bed past the cut point's last word, then the 0.5–1.5 s crossfade into its bridge (edit lock: never clip a line).

**For Chief:** 001, 002 and 003 keep their own end cards and holds, so the compilation shows a house end card three times mid-film. The plan keeps them (only the hand-offs were ruled on). If Chief wants them out, it's three more trims on the cream card's first frame, about 8–10 s each, with no VO touched.

## New material

| Segment | VO | Length | Picture needed |
|---|---|---|---|
| Intro | `hos_comp_intro_vo_v01.wav` | 51.68 s | six moving plates from the films' own passed clips (arm, willow, flask, cards, screen, foil), none from the first 30 s of its film. The willow plate needs 006's clips. |
| Bridge 1 (after 005) | `hos_comp_bridge1_vo_v01.wav` | 17.12 s | 005's last plate crossing to the willow (006); timeline appearance 1 (1628 · HARVEY) |
| Bridge 2 (after 006) | `hos_comp_bridge2_vo_v01.wav` | 17.04 s | leaf, window, candlelit ward (001's plates); no teach graphic. Listen once for the "a"/"the" Scribe note (Chief, J0174). |
| Bridge 3 (after 001) | `hos_comp_bridge3_vo_v01.wav` | 13.84 s | theatre light to element cards (002); timeline appearance 2 (1779, 1860s) |
| Bridge 4 (after 002) | `hos_comp_bridge4_vo_v01.wav` | 13.44 s | glowing vacancy to dark lab and screen (003); no teach graphic |
| Bridge 5 (after 003) | `hos_comp_bridge5_vo_v01.wav` | 14.88 s | screen to gold foil (004); timeline appearance 3 (1869, 1895) |
| Closing (after 004) | `hos_comp_closing_vo_v01.wav` | 30.24 s | cutaway atom, pull back through the six objects; timeline completes (1911); cream end card 3–4 s; hold 2–3 s, fade |
| Chapter cards ×6 | none | ~3 s each | case-file / cream-on-brown inked card, low wooden thud |

VO audio is on the Mini only: main HOS checkout, `docs/STANDALONE_SHORTS_TEST_2026-10/vo_compilation_v01/` (git-ignored).

**Code graphics (`chart` kind, Codex first):** the timeline (one render per appearance: `code_graphic_comp_timeline_b1/_b3/_b5/_close`, markers ink in with the pen-tap tick, at least 0.5 s apart) and six chapter cards (`code_graphic_comp_card_01…06`). Over moving or blurred plates, never a flat slab; must pass polish_gate near-black. Queued as a follow-on job.

**Music:** 004's existing bed `05_Music/hos004-full_score_bed_v01.mp3` (6.25 MB, no spend) under intro, bridges and closing, with 2–4 s crossfades into each film's own bed. `music_gate.py` treats a reused bed as "sounds like another film's bed": Chief rules whether that's an accepted exception for a compilation (the plan proposes it; no new bed before 30 Oct without Chief's OK).

**SFX:** house kit, `python3 scripts/sfx_kit.py make --out-dir <comp>/06_Sound-Effects/kit_v01 --house hos` (OWB checkout), tick and thud only; `sfx_kit.py level` on the new-material stems.

## Running total (five films now, six when 006 lands)

- Films after trims: 005 489.2 + 001 364.6 + 002 540.6 + 003 425.7 + 004 491.4 = **2,311.5 s (38:31.5)**.
- New material: VO 158.2 s + 6 cards × 3 s + breaths, crossfades and holds (~15 s) ≈ **191 s (3:11)**.
- **Five films: ≈ 41:43, short of 45.** With 006 (~8:58 less its hand-off and end card, ~8:20): **≈ 50:00**, inside 45–60.

## Blocks and order of work

1. **006's master** (picture ETA 25 Oct). The cut can't reach 45 min, the intro and Bridge 1 need its willow plate, and its trim point isn't known until it exists. The assembler can be written and run on the five films with a placeholder slot, but the deliverable waits on 006.
2. **Code graphics** (timeline ×4, cards ×6): follow-on `chart` job.
3. **Intro and bridge plates:** pick from each film's passed clips (most now on the NAS); one plate per object, logged in the cut list.
4. **Assembler** `_assemble_hos_compilation_v01.py` in this folder: normalise, trim, crossfade, lay VO, bed and SFX stems, loudness, then `picture_qa.py`, `polish_gate.py`, `music_gate.py`, `sfx_kit.py level`, and a chapters list from the real cut times.

## Run 3 (Cursor, 12 Oct 2026 21:05): assembler prep and plan stages

- `_assemble_hos_compilation_v01.py prep` normalises and trims each available master into `/private/tmp/hos_comp_v01/film_NNN_norm.mp4` (1080p30, yuv420p, two-pass loudnorm −14 LUFS / −1 dBTP, 0.25 s audio fade on the 005 and 004 trims, inside their measured pauses) and records source sha256, loudness in/out and durations in `prep_report.json`. Started detached on the Mini: tmux `J0175-prep`, log `~/_desk/logs/J0175-prep.log`, exit code in `~/_desk/logs/J0175-prep.done`. 006 is skipped until its master exists.
- `_assemble_hos_compilation_v01.py plan` writes `cut_plan_v01.json` (segment order, start times, chapters draft, missing inputs). Dry run on inventory lengths with 006 at ~8:20: **49:58**, inside 45–60. Chapters draft: 0:00 Six discoveries, one question · 0:52 The Hidden Circle · 9:22 Built From Air · 18:03 The Invisible Enemy · 24:25 The Empty Chairs · 33:42 A Light Through Skin · 41:07 Inside the Atom (final times come from the real cut).
- Still missing (17 items in the plan): the 006 master, the ten J0204 graphics, and the intro and bridge plates. The render stage (crossfades, VO, bed and SFX stems, gates) is written once J0204 lands.
