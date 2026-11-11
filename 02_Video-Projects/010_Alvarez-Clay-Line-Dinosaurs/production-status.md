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


# J0862 single-take result — 5 Nov 2026

Worker: codex. No final approval. J1894 scope executed once; three accepted v02 takes remain unchanged.

009 B v03: exact review text is 316 characters, 57 whitespace words (review claimed 311). House client, Ben Orbit Narrator, eleven_v3, unchanged settings. Live balance 97,352 / 121,114 before and after (counter lag); 316 submitted characters conservatively logged. No further take authorized or made.

vo_check_py312.sh: PASS, 23.68 s, mean -24.2 dB, peak -4.3 dB, 147 wpm; homophone warning an apple's / and apples requires Ben's final listen. No audio perception claimed.

Hook FAIL: Scribe ends fall at 3.680 s. The scoped 0.150 s trim plus maximum 1.06 speed yields 3.330 s, over 2.850 s. Total with 1 s tail would be 24.680 s. J1894's predicted token timings are not measurements of this new take. No larger gap surgery, second take, script rewrite or timing waiver performed. Chief must scope the next repair.

Media preserved in the HOS checkout, 009/10_Shorts/vo_v02/hos_009_short_B_v03.{mp3,wav}; TAKE and VO_CHECK records accompany this report. All old v02 files preserved. 010 A retains J1004 Option A1. Downstream J2171 remains blocked on this hook; no film stage approved. Nothing uploaded or published.


## J0862 v04 & J2279 audio-capable splice repair — 6 November 2026

Codex covering (`cb18632d` pickup) + Gemini covering (`J2279` direct `audio_input` audition and zero-spend splice/tail-fade repair). `J2195` scoped one opening-only pickup for `009 Short B`; recorded once with Ben Orbit Narrator, `eleven_v3`, `speed=1.04` (`81` actual chars logged; `93,478 / 121,114` ElevenLabs credits remaining; `0` additional chars generated in `J2279`).

Three retained takes are untouched and PASS `vo_check_py312.sh`: `009 A v02`, `010 A v02` (`J1004` Option A1 retained: `hook_end_s = 2.849 s <= 2.850 s`, `23.289 s` total), and `010 C v02` (`hook_end_s = 1.780 s <= 2.850 s`, `23.560 s` total).

In `J2279`, `gemini` (`audio_input` verified) directly auditioned `009 Short B v04` (`hos_009_short_B_v04.{wav,mp3}`), confirmed zero spoken repeat at `19.74 s` or `24.14 s` (Whisper `Seg 8 [24.14->24.32]` was a `no_speech_prob=0.986/0.988` post-word breath hallucination shifted to `0:19.74` by 9 dropped cardinal numbers in `norm()`), and repaired the `cb18632d` splice (`open_v04[0.100:0.900]+[0.960:6.640]` `6.480 s` + `v03[5.680:23.680]` `18.000 s` with `afade=t=out:st=23.480:d=0.060`), restoring the full `5.940–6.020 s` `"Isaac"` onset while keeping identical `+0.800 s` word offsets, `hook_end_s = 2.820 s`, `24.480 s` VO (`25.480 s` with `1.000 s` loop tail), and 8 cuts. Both `hos_009_short_B_v04.mp3` (`0c9c4c6ffdb1337dc11acaf57af909f8d8be91d77210bca2e13af80715b87498`) and `hos_009_short_B_v04.wav` (`a6666fd27c9a90e781369ea07e4888d87a2d5edb1624a0090ae98fa39504686b`) now PASS unmodified `vo_check_py312.sh` with `0` fails and `0` warnings.

`check_all.sh 009`: ALL CHECKS PASS. `check_all.sh 010`: ALL CHECKS PASS.
- **Elected Chief PASS (`J2281` / `J0862`, `gemini`, 7 Nov 2026):** Condition for `J0862` verified satisfied (`J2279` complete at `fc1a23f3`; direct `audio_input` audition and `vo_check_py312.sh` PASS verified across all four `009` + `010` Shorts VO takes; Option A1 retained for `010 Short A` `hos_010_short_A_v02.mp3` `68d88b5b5883f2376bcec29c26d77efea7634d5c7705693f41202ca587b927fb` and `010 Short C` `hos_010_short_C_v02.mp3` `20432ecd645b28e9fdc051578a284cb2845bd09f3040170b192089b256055b87`). `009` and `010` `shorts_vo` marked `done` in `PIPELINE.json`; HOS PR #423 approved and merged; `J0862` and `J2281` closed `done` (`J2172` remains gated on `J2271` 12-plate production/review chain).

## 10 Nov 2026 — J2268: Tested twelve-plate Flow adapter without generation (£0, 0 Flow credits, Gemini covering)

- **Authority & Scope:** Queue job `J2268` (`ref: J2267`, `after: J2200`). Code + offline regression tests only; **£0 and 0 Flow credits spent**, **0 Flow submissions**, **0 Create clicks**, **0 NAS writes**, and `generation_authorized=false` retained in `10_Shorts/TWELVE_PLATE_SCOPE_J2267.json` (`sha256: 5bcfc162af2c87fd6ae9984377d6b54efe76f50e99a493fd8df9f3ae4ecf827f`). `J2033` and `J2200` states/holds preserved. Parked for elected-Chief system PASS before `J2269` preflight; `PIPELINE.json` not advanced (parked review job).
- **Deliverables:**
  1. `07_Edit-Project/_mint_flow_twelve_plates_j2268.py`: dedicated HOS 010 twelve-plate Flow adapter built on the `J2200` shared Flow accounting foundation (`SharedFlowAccounting` in `~/_desk/state/flow/shared`, matching `009`/`013`), consuming **only** `10_Shorts/TWELVE_PLATE_SCOPE_J2267.json` (10 shared long + 2 Shorts-only `Veo 3.1 - Quality` parents across `3` batches `5 + 5 + 2`), never importing or invoking `_mint_flow_tranche1_j0453.py`. Enforces exact 12-row allowlist, SHA-256 verification across scope + `PICTURE_PLAN_v04.json` + `SHORTS_PICTURE_PLAN_v03.json` + `J2267_BUDGET_RECONCILIATION.json` + all 5 part boards + `VO_TAKES_KEEP.json` + accepted Short A/C VOs + `J1004` Option A1 recipe + Explorer reference (`P5:10_explorer_robin` only, never frame 0), studio Ultra account digest check (no email addresses in tracked files), `Veo 3.1 - Quality` `8s` `16:9` `x1` `100`-credit live DOM check (`Nano Banana 2.1` `16:9` `x1` `0` credits for missing start stills, accepting `1376x768`), `3600` total cap, `<= 5` rows / `<= 1500` credits per batch, `3` takes/row max, `3000`-credit headroom floor, anti-double-counting reservation ledger, duplicate-process flock, `cdp_tabs.reuse_page`, `file_state="GENERATED"` / `status="PENDING_REVIEW"` / `keep=False` (never auto-KEEP), and double submit interlock (`HOS010_TWELVE_PLATES_SUBMIT=1` + explicit `J2269` Chief authorization after `J2033` `DONE`).
  2. `tests/test_hos010_twelve_plate_runner.py`: `15` offline regression tests covering wrong account, wrong model / `x2`, stale price, low balance (`< 3000` floor), reservation double-counting, scope/VO/Option A1 drift, exhausted row/batch/scope caps, duplicate process lock, missing/corrupt Explorer & house style references, guarded `5 + 5 + 2` batch advancement, and 10 Nov live DOM capture (`Ran 15 tests — OK`; full repo suite `Ran 139 tests — OK`, 0 submissions, 0 credits).
- **Repository check output (`bash 00_Brand/Channel-Setup/tools/check_all.sh 010`):**
```text
-- durable desk handoffs: PASS
-- no media: PASS
-- status board in sync: PASS
-- ElevenLabs guard tests: PASS
-- vo_check word tests: PASS
-- atempo check tests: PASS
-- voice speed (atempo <= 1.06): PASS
-- contract tests: PASS
-- package-lint: PASS
-- review:script clay_script_master_v01.md: PASS
-- gate:episode: PASS
ALL CHECKS PASS
```

