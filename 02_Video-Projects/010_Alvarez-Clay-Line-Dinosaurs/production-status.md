# Production status — Dinosaurs (Alvarez and the clay line)

| Field | Value |
|---|---|
| Slug | `010_Alvarez-Clay-Line-Dinosaurs` |
| Channel | `@HistoryOfScienceYT` only |
| Topic | **Dinosaurs** — Alvarez and the clay line (iridium / *Science* 1980 → Chicxulub after-act) |
| Stage | **Script PASS on main** (PR #208, review **92.1**). **FACT_NOTES + HARD_CHECKS + upload scaffold** this PR (write lane, desk #180 claim 5982333546). |
| Neighbour gate | **PASS** (4 Oct 2026): 10 education ≥1M; TED-Ed/TED yes. Evidence `11_Upload-Package/evidence_2026-10-04_neighbours.json` |
| Script review | `clay_script_master_v01.md` on main; **92.1 PASS** |
| FACT_NOTES | **this PR** — every new-claims row sourced; hard-checks 7/7 PASS |
| VO | **waits Claude** confirm on FACT_NOTES + HARD_CHECKS (Ben VO listen not required first once Claude PASSes) |
| Picture | **BOARDS v01, no mint** (J0314, 15 Oct). Flow-first price review in `07_Edit-Project/PRICE_REVIEW_v01.md`. Parked for Chief. |
| Runtime target | 7–9 min, 5 parts (house default) |
| Air (proposed) | Thu **3 Dec 2026** 18:00 UK (`2026-12-03T18:00:00.000Z`) — draft in PACKAGE_MANIFEST |
| Shorts | not outlined yet |

## 15 Oct 2026 — plate boards v01 (J0314)

The long VO is locked (Chief KEEP, desk #180 comment 6101773293). Plate boards are timed from that VO and priced Flow-first, the same table as 009 J0261. Flow expected **12,572** credits against **23,740** left (fits on its own). Vertex expected **£146.88** against **£70.02** usable (does not fit). 006–009 still share the Flow pot, so mint order is the Chief's call. Nothing in the boards is generation-authorised.

## STOP

- No Vertex/Veo/Flow minting on this film.
- No ElevenLabs VO until Claude confirms sourced FACT_NOTES + HARD_CHECKS.
- Do not merge or close desk PR #180 from this work.

## 24 Oct 2026 — J0909 (`J0899` Change 5): 2-way Title T&C launch plan, Shorts positive-question title + payoff-past-15s lock & `300× TOO MUCH` / `rumble_low` notes (Gemini covering)

- **Authority:** Chief PASS on `J0899` (`02_Video-Projects/_analytics/HOS_2026-10-24.md` §4 #5) and queue job `J0909`. `£0` spend, no live YouTube changes.
- **Applied to `11_Upload-Package/` and `10_Shorts/SHORTS_SCRIPTS_v02.md`:**
  1. **2-way Title Test & Compare on launch (`PACKAGE_MANIFEST.json` `titleAbc`, `LAUNCH_PLAN.md`, `PRE_BUILD_VIDIQ_AUDIT.md`):** Armed Variant A *What Killed the Dinosaurs Was Hidden in a Line of Clay* vs Variant B *How a 1-Centimetre Line of Clay Solved What Killed the Dinosaurs* (`64` chars, shares neighbour phrase `dinosaurs`).
  2. **Shorts positive-question titles + payoffs held past `15 s` (`10_Shorts/SHORTS_SCRIPTS_v02.md`, `LAUNCH_PLAN.md`, `PACKAGE_MANIFEST.json`):** Locked positive question titles on Short A (*What Killed the Dinosaurs?*, `24.16 s`) and Short C (*Are Birds Really Dinosaurs?*, `23.51 s`) with payoffs explicitly held past `15 s` (`15.0–23.8 s` on Short A and `15.1–23.2 s` on Short C, clear of the `9.0–14.0 s` promoted-long title banner).
  3. **Thumbnail cover text & Part 04 SFX note (`LAUNCH_PLAN.md`, `PRE_BUILD_VIDIQ_AUDIT.md`, `PACKAGE_MANIFEST.json`):** Documented pairing **`300× TOO MUCH`** cover text with `sfx_kit.py` `rumble_low` on the Part 04 crater reveal.
- **Package lint (`npm run lint:package -- --film 010`):** `PASS  02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/11_Upload-Package/PACKAGE_MANIFEST.json`.

## 30 Oct 2026 — J1266: Final Sources and provisional Chapters in `Descriptions/clay_long_description_v01.txt` (Chief h13 on J1261, £0, Gemini covering)

- **Authority:** Chief (Grok) ruling `h13` on `J1261` (30 Oct 2026, HOS `#180` re `6521114044`) and queue job `J1266`. Records only, `£0` spend, no YouTube/Studio change, no upload.
- **Provisional chapters status:** Chapters provisional from VO part timings (this job); the rough-cut and picture-lock jobs must re-time them against the master before upload.
- **Provisional `Chapters` block added to `11_Upload-Package/Descriptions/clay_long_description_v01.txt` from locked VO part takes in `02_Voiceover/VO_TAKES_KEEP.json` and part `.wav` durations (summed in film order, no picture yet):**

| Stamp | Chapter title | VO part (`02_Voiceover/`) | Part duration (`VO_TAKES_KEEP.json` & `.wav` `ffprobe`) | Summed part start (s) | First word in part (`stt_raw.json`) | First word in film order (s / `m:ss.ss`) |
|---|---|---|---:|---:|---|---:|
| `0:00` | `The line in the rock` | `hos_010_part01_the_line_in_the_rock_v01` (`sha256: 1ed2e527…`) | `89.04 s` | `0.00 s` | `"What"` at `+0.10 s` | `0.10 s` (`0:00.10`) → **`0:00`** |
| `1:29` | `The gorge at Gubbio` | `hos_010_part02_the_gorge_at_gubbio_v01` (`sha256: fc34abf3…`) | `79.76 s` | `89.04 s` | `"Walter"` at `+0.14 s` | `89.18 s` (`1:29.18`) → **`1:29`** |
| `2:49` | `A clock made of stardust` | `hos_010_part03_a_clock_made_of_stardust_v01` (`sha256: 9f25fbeb…`) | `81.04 s` | `168.80 s` | `"Walter's"` at `+0.12 s` | `168.92 s` (`2:48.92`) → **`2:49`** |
| `4:10` | `Too much iridium` | `hos_010_part04_too_much_iridium_v01` (`sha256: 245df001…`) | `103.84 s` | `249.84 s` | `"In"` at `+0.12 s` | `249.96 s` (`4:09.96`) → **`4:10`** |
| `5:54` | `The crater and the birds` | `hos_010_part05_the_crater_and_the_birds_v01` (`sha256: 7e3c9c4f…`) | `146.16 s` | `353.68 s` | `"For"` at `+0.10 s` | `353.78 s` (`5:53.78`) → **`5:54`** |

  - Total summed VO duration (`Parts 01–05`): `89.04 + 79.76 + 81.04 + 103.84 + 146.16 = 499.84 s` (`8:19.84`).
- **Final `Sources` block added under `Chapters` (8 plain citations strictly from `01_Script/FACT_NOTES_v01.md` source column; no URLs; honours row 42 "Not a historical claim. | Production note." on the southern England scale card):**
  - `L. W. Alvarez, W. Alvarez, F. Asaro and H. V. Michel, "Extraterrestrial Cause for the Cretaceous-Tertiary Extinction", Science 208 (1980)`
  - `Walter Alvarez, T. rex and the Crater of Doom (1997)`
  - `L. W. Alvarez et al., "Search for Hidden Chambers in the Pyramids", Science 167 (1970)`
  - `Bohor et al., Science 224 (1984)`
  - `Sigurdsson et al., Nature 349 (1991)`
  - `Hildebrand et al., Geology 19 (1991)`
  - `Renne et al., Science 339 (2013)`
  - `Larson et al., Current Biology 26 (2016), and Field et al., Current Biology 28 (2018)`
- **Rest of description (`clay_long_description_v01.txt`) and `PACKAGE_MANIFEST.json`:** opener, bullet list, and sign-off kept byte-identical to `#383`.
- **Repository check output (`00_Brand/Channel-Setup/tools/check_all.sh 02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs`):**
```text
-- no media: PASS
-- status board in sync: PASS
-- ElevenLabs guard tests: PASS
-- vo_check word tests: PASS
-- contract tests: PASS
-- package-lint: PASS
-- review:script clay_script_master_v01.md: PASS
-- gate:episode: PASS
ALL CHECKS PASS
```
- **Package lint on `main` and against PR `#387` (`origin/gemini/j1259-release-gate-chapters-sources` @ `592eaae7`, `checkChaptersAndSources`):**
```text
> content-ops@0.1.0 lint:package
> tsx scripts/package-lint.ts --film 010

PASS  02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/11_Upload-Package/PACKAGE_MANIFEST.json
   warn  [title.length] T&C title: "How a 1-Centimetre Line of Clay Solved What Killed the Dinosaurs" is 64 chars (aim ≤ 60)
   warn  [captions] no captionsFile (captions from the script)
```
