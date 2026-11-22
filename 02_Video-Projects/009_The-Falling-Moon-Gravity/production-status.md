# Production status — Gravity (the falling Moon)

| Field | Value |
|---|---|
| Slug | `009_The-Falling-Moon-Gravity` |
| Stage | **Long master v03 (`744f32b7`, J3314) + J2036 technical QA pack ready for J2037 review & Ben final watch** (`ben_ok: todo`; 22 Nov 2026) |
| Script | `moon_script_master_v01.md` · review **91.3** (`gate:episode` PASS; 6 DATA, 6 SCALE, 2 WHO, 8 WHEN, 4 FACT) |
| FACT_NOTES | Sourced from script new-claims; **7/7 hard-checks PASS**. `FACT_NOTES_v01.md` lines 3 & 77 record "Confirmed by Claude, 4 Oct 2026" (desk claim `5982314076`); earlier header read `Claude UNSIGNED` (preserved as provenance note; no new sign-off invented). |
| Neighbour gate | **PASS — 6 education ≥1M; TED-Ed yes** (`evidence_2026-10-04_neighbours.json` + 24 Oct `eyZEqSPeMwg`) |
| Upload package | `PACKAGE_MANIFEST.json` (thumbs A+B wired, `video: null`, `privacy: private`), `moon_long_description_v01.txt` (exact v03 chapters `0:00/1:24/2:56/4:20/6:33`, 8 Sources, honest making-of line), `moon_long_tags_v01.txt`, `PRE_BUILD_VIDIQ_AUDIT.md` (signed by Claude 4 Oct 2026 in §7; vidIQ waived), `lint:package` PASS |
| Picture | **All 90/90 board rows settled** (Tranche 1 57 KEEP J1237 + Tranche 2 Flow/retakes KEEP J2033–J2629 + J2631 & J2632 r4 code graphics KEEP) & composited into v03 (`picture_qa` 0/92 fail, `polish_gate` 0/92 fail, 5 inspected low-detail warnings). Stays `doing` in `status.json` until J2037/Chief closes edit milestone. |
| VO | **LOCKED v01** (Chief KEEP, desk #180 comment 6101629662, 11 Oct; 5 parts, 508.40 s speech). Retime 8:38.4 in `07_Edit-Project/VO_RETIME_v01.json`. |
| Score | **v04_synth ACCEPTED** (`hos_009_score_v04_synth.wav`, `151ba46a…`, J3241; `music_gate` PASS on v03 cut) |
| Thumbnails | **J3262 Acting Chief PASS (21 Nov 2026):** A (`IT MISSES`, `cd44f056…`) & B (`ONE APPLE`, `3d116433…`), Mini↔NAS 7/7 SHA-256 parity |
| Shorts (separate) | `J0862` Shorts VO PASS (PR #423); `J2171` Shorts A & B assembled (PR #718 open, CI green; separate independent review `J3311` held for non-producer Mini reviewer) |

## STOP

- **Not a film PASS and not Ben's watch:** `ben_ok` and `scheduled` remain `todo`. No YouTube upload, schedule, privacy, or Buffer action is authorized until J2037 review and Ben's final watch approval.
- Do not merge or close desk PR #180 from this work.
- Does **not** close #180.

## 24 Oct 2026 — J0909 (`J0899` Change 4): Gravity-apparatus search terms in description lines 1–2 and tags + Shorts VO & `J0383` teach-graphic alternation notes (Gemini covering)

- **Authority:** Chief PASS on `J0899` (`02_Video-Projects/_analytics/HOS_2026-10-24.md` §4 #4) and queue job `J0909`. `£0` spend, no live YouTube changes.
- **Applied to `11_Upload-Package/` and `10_Shorts/SHORTS_SCRIPTS_v02.md`:**
  1. **Gravity-apparatus search terms in description lines 1–2 and tags (`Descriptions/moon_long_description_v01.txt`, `Tags/moon_long_tags_v01.txt`, `PACKAGE_MANIFEST.json`, `PRE_BUILD_VIDIQ_AUDIT.md`):** Wove `"theory of gravity"`, `"how Newton proved gravity"`, and `"Cavendish torsion balance"` (from breakout neighbour `eyZEqSPeMwg`, `1.14M` views in 6.8h on 23–24 Oct, zero channel names) into lines 1–2 of `moon_long_description_v01.txt` (retaining `Moon`, `Newton`, `gravity` in the first 100 chars) and into `moon_long_tags_v01.txt` (8 tags total). Added `eyZEqSPeMwg` to `PACKAGE_MANIFEST.json` `neighbours.videos`.
  2. **Search-titled `v02` Shorts VO & `J0383` teach-graphic alternation (`LAUNCH_PLAN.md`, `10_Shorts/SHORTS_SCRIPTS_v02.md`, `PACKAGE_MANIFEST.json`):** Documented positive-question Shorts VO titles (*What Would Happen If the Moon Stopped Moving?* / *Why Doesn't the Moon Crash Into the Earth?*, *How Did Newton Discover Gravity?*) and alternating every `J0383`-verified parchment teach graphic in `0:00–0:30` and `1:00–2:00` with a moving 3D plate.
- **Package lint (`npm run lint:package -- --film 009`):** `PASS  02_Video-Projects/009_The-Falling-Moon-Gravity/11_Upload-Package/PACKAGE_MANIFEST.json`.

## 29 Oct 2026 — J1192: HOS 009 picture tranche 1 minted and KEEP (57/57 Flow rows of boards v04) (Gemini covering)

- **Authority:** Acting Chief (Claude) price pass J0863 PASS and queue job `J1192`. £0 cash spend, no ElevenLabs, no upload.
- **Live Flow gate & spend:**
  - Start live Flow read: `18,550` credits (`[email redacted]`, after J1191 008 completion), logged via `ai_spend.py`.
  - Minted all **57/57 tranche-1 Flow rows** across Parts 01–05 (`26 Quality + 31 Fast`):
    - **Part 01 (`12/12` KEEP):** `01_moon_falling`, `02_apple_and_moon`, `03_table_three`, `03_table_three_c1`, `03_table_three_c2`, `04_things_fall`, `05_heavens_map`, `06_perfect_circles` (take 2, non-emissive matte brass armillary sphere), `07_night_field`, `08_three_questions`, `09_no_answer`, `10_farmhouse_dawn`.
    - **Part 02 (`10/10` KEEP):** `01_cambridge_closes`, `02_road_north`, `03_christmas_birth`, `04_sundial_pegs`, `05_working_alone`, `06_prism_spectrum`, `07_fluxions_desk`, `08_the_apple`, `11_explorer_apple`, `12_how_far_moon`.
    - **Part 03 (`7/7` KEEP):** `01_really_falling`, `02_cannon_world`, `03_shot_slow` (take 2 reusing `02_cannon_world` parent still), `04_shot_faster` (take 2 reusing `02_cannon_world` parent still), `05_shot_orbit`, `09_moon_curve`, `10_explorer_cannon`.
    - **Part 04 (`13/13` KEEP):** `01_two_numbers`, `02_spray_paint`, `02_spray_paint_c1` (take 2 reusing `02_spray_paint` parent still), `02_spray_paint_c2` (take 2 reusing `02_spray_paint` parent still), `05_minute_second`, `06_pretty_nearly`, `06_pretty_nearly_c1`, `07_put_aside`, `07_put_aside_c1`, `08_halley_visit`, `09_i_have_calculated`, `10_write_it_down`, `10_write_it_down_c1`.
    - **Part 05 (`15/15` KEEP):** `01_one_law`, `01_one_law_c1`, `02_principia_press`, `02_principia_press_c1`, `04_comet_1758`, `05_iss_orbit` (take 2 clean 3D cartoon station silhouette over blue Earth), `06_iss_apple` (take 2 two upright astronauts in station cabin with floating apple), `07_astronaut_float`, `08_cup_and_planets`, `08_cup_and_planets_c1` (take 2 reusing `08_cup_and_planets` parent still), `08_cup_and_planets_c2`, `09_orchard_dusk`, `10_explorer_bench` (closer), `12_clay_handoff`, `12_clay_handoff_c1`.
  - Total tranche-1 Flow spend: **`3,170` credits** (`2,920` first-pass + `250` across 7 targeted UAT retakes) vs `7,354` expected / `7,585` cap.
  - End live Flow balance: **`15,380` credits** (`>= 3,000` buffer; logged via `ai_spend.py`).
- **Evidence & NAS backup:**
  - Ledger: `02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project/FLOW_MINT_LOG_v04_tranche1.json` (all 57/57 `KEEP` with sha256, duration, UAT sheet paths, and balance reads).
  - Local media: `/Users/benjaminoats/YouTube/hos-009-gravity/02_Video-Projects/009_The-Falling-Moon-Gravity/04_Generated-Clips/part01..05/` (silent `.mp4` clips, Nano Banana 2 `.png` start stills, UAT contact sheets).
  - NAS copy (copy-only verified, 57/57 matching sha256): `/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/009_The-Falling-Moon-Gravity/04_Generated-Clips/` and `07_Edit-Project/FLOW_MINT_LOG_v04_tranche1.json`.
- **Next:** Chief J1237 closed tranche 1 PASS (see below). Tranche 2 (`20` Quality rows, `5,180` expected) waits for the ~12 Nov AI Ultra renewal.

## 30 Oct 2026 — J1237: Motion evidence for the 3 flagged windows of J1192 tranche 1 (Gemini covering)

- **Authority:** Acting Chief (Claude) queue job `J1237` (answering desk `#6511102950`). `£0` spend, no new mint, no retake, no upload.
- **Chief ruling (source of truth):** https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6516310345 — **J1237 PASS**; J1192 tranche 1 picture PASS with the locked in/outs below. Docs/records aligned to that ruling (v05 board + mint-log notes); no remint.
- **Exported evidence (`02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project/review_J1192_motion/`):**
  - Full-size (`1280×720`) PNG frames across each `freezedetect=n=-50dB:d=0.8` flagged window `±0.5 s` (`P01_03_table_three/frames/` 50 frames, `P04_07_put_aside/frames/` 34 frames, `P04_10_write_it_down_c1/frames/` 38 frames), full-size PNG strips (`*_strip.png`), 1-row contact sheets (`*_contact_1row.png`), 6-column contact grids (`*_contact_grid.png`), and full-clip frame-difference plots (`*_frame_diff_plot.png` + `frame_diff_metrics.json`).
- **Per-clip Chief-locked in/out (assembly must use these):**
  1. **`P01:03_table_three` (`3.333–4.375 s`, `f080–f105`):** Low-motion beat, not a freeze (`0` duplicate frames, `MAD = 0.137–0.380`, `RMS = 0.552–2.750`; apple rocks/settles, centroid ~10 px). Camera essentially static across `f080–f105` (best-fit scale `1.000`); **no** push-in in that span — push-in only builds after ~`4.5 s`. Locked **`0.000–7.000 s` ONLY** (`use_s = 7.00`). **FORBIDDEN:** `1.000–8.000 s` (starts mid-settle).
  2. **`P04:07_put_aside` (`7.083–8.000 s`, `f170–f191`):** Brisk continuous motion `0.000–7.083 s` (`MAD` median `1.15`, papers slide into drawer + summer→autumn→winter→spring light shift) followed by a `0.917 s` tail settle; board `use_s = 3.76 s` avoids the tail at locked **`0.000–3.760 s`**. Hard limit **`out ≤ 7.042 s`**.
  3. **`P04:10_write_it_down_c1` (`0.000–1.042 s`, `f000–f025`):** Opening `1.042 s` (`MAD = 0.099–0.508`) is a low-motion pre-action hold; locked trimmed in/out **`1.083–6.423 s`** (`use_s = 5.34`). Hard limit **`in ≥ 1.083 s`**. Arm/figure note: **checked by Chief J1237, clean** (green sleeve = second standing figure correctly occluded; no arm-through-body or hand morph). `2.583–7.923 s` alt not required.
- **Next:** Tranche 1 picture PASS (Chief J1237). Tranche 2 (`20` Quality rows, `5,180` expected) waits for the ~12 Nov AI Ultra renewal; future 009 assembly brief carries the locked in/outs above.

## 30 Oct 2026 — J1266: Final Sources and provisional Chapters in `Descriptions/moon_long_description_v01.txt` (Chief h13 on J1261, £0, Gemini covering)

- **Authority:** Chief (Grok) ruling `h13` on `J1261` (30 Oct 2026, HOS `#180` re `6521114044`) and queue job `J1266`. Records only, `£0` spend, no YouTube/Studio change, no upload.
- **Provisional chapters status:** Chapters provisional from VO part timings (this job); the rough-cut and picture-lock jobs must re-time them against the master before upload.
- **Provisional `Chapters` block added to `11_Upload-Package/Descriptions/moon_long_description_v01.txt` from locked VO part takes in `02_Voiceover/VO_TAKES_KEEP.json` and part `.wav` durations (summed in film order, no picture yet):**

| Stamp | Chapter title | VO part (`02_Voiceover/`) | Part duration (`VO_TAKES_KEEP.json` & `.wav` `ffprobe`) | Summed part start (s) | First word in part (`stt_raw.json`) | First word in film order (s / `m:ss.ss`) |
|---|---|---|---:|---:|---|---:|
| `0:00` | `The falling Moon` | `hos_009_part01_the_falling_moon_v01` (`sha256: 81b6c45f…`) | `83.84 s` | `0.00 s` | `"Right"` at `+0.10 s` | `0.10 s` (`0:00.10`) → **`0:00`** |
| `1:24` | `An apple in a plague year` | `hos_009_part02_an_apple_in_a_plague_year_v01` (`sha256: 36855907…`) | `89.84 s` | `83.84 s` | `"In"` at `+0.14 s` | `83.98 s` (`1:23.98`) → **`1:24`** |
| `2:54` | `The cannon on the mountain` | `hos_009_part03_the_cannon_on_the_mountain_v01` (`sha256: 53235ab0…`) | `80.88 s` | `173.68 s` | `"Newton's"` at `+0.12 s` | `173.80 s` (`2:53.80`) → **`2:54`** |
| `4:15` | `The Moon test` | `hos_009_part04_the_moon_test_v01` (`sha256: 2d03f372…`) | `131.20 s` | `254.56 s` | `"Newton"` at `+0.10 s` | `254.66 s` (`4:14.66`) → **`4:15`** |
| `6:26` | `Falling around the world` | `hos_009_part05_falling_around_the_world_v01` (`sha256: 10ebaf45…`) | `122.64 s` | `385.76 s` | `"Newton's"` at `+0.16 s` | `385.92 s` (`6:25.92`) → **`6:26`** |

  - Total summed VO duration (`Parts 01–05`): `83.84 + 89.84 + 80.88 + 131.20 + 122.64 = 508.40 s` (`8:28.40`).
- **Final `Sources` block added under `Chapters` (8 plain citations strictly from `01_Script/FACT_NOTES_v01.md` source column; no URLs; honours row 33 "Do not attribute to Newton" on spray-paint analogy and row 41 "Not a Newton cite" on the 010 Alvarez hand-off):**
  - `Isaac Newton, Philosophiæ Naturalis Principia Mathematica (London, 1687), Book III, Prop. IV`
  - `Isaac Newton, A Treatise of the System of the World (London, 1728)`
  - `Isaac Newton, memorandum (c. 1714–18), Cambridge University Library Add. MS 3968`
  - `William Stukeley, Memoirs of Sir Isaac Newton's Life (1752), entry for 15 April 1726`
  - `John Conduitt, memoranda, Keynes MS 130 (Newton Project)`
  - `Edmond Halley, Synopsis of the Astronomy of Comets (1705)`
  - `Richard S. Westfall, Never at Rest (1980)`
  - `NASA NSSDC, "Moon Fact Sheet", and NASA, "ISS Facts and Figures"`
- **Rest of description (`moon_long_description_v01.txt`) and `PACKAGE_MANIFEST.json`:** opener, bullet list, and sign-off kept byte-identical to `#383`.
- **Repository check output (`00_Brand/Channel-Setup/tools/check_all.sh 02_Video-Projects/009_The-Falling-Moon-Gravity`):**
```text
-- no media: PASS
-- status board in sync: PASS
-- ElevenLabs guard tests: PASS
-- vo_check word tests: PASS
-- contract tests: PASS
-- package-lint: PASS
-- review:script moon_script_master_v01.md: PASS
-- gate:episode: PASS
ALL CHECKS PASS
```
- **Package lint on `main` and against PR `#387` (`origin/gemini/j1259-release-gate-chapters-sources` @ `592eaae7`, `checkChaptersAndSources`):**
```text
> content-ops@0.1.0 lint:package
> tsx scripts/package-lint.ts --film 009

PASS  02_Video-Projects/009_The-Falling-Moon-Gravity/11_Upload-Package/PACKAGE_MANIFEST.json
   warn  [captions] no captionsFile (captions from the script)
```

## 4 Nov 2026 — J2026: funded tranche2 scope and production handoff (Codex acting Chief)

Authority rechecked: Codex elected; Grok/Claude unavailable. HOS has2/4 November complete vs OWB5/4, so HOS priority. Live authenticated Ultra balance15,430; reset displayed12Nov19:13. Live Flow UI Veo3.1 Quality, Frames,16:9,720p,8s,x1 costs100. Default was Omni/x2: worker MUST verify approved model and one output. No generation or credits spent in this scope job.

**Decision:** authorize exact20 remaining v05 Quality rows now, max3 takes/row, hard total6,000, batch<=5 rows/1,500. Preserve3,000 floor after remaining full cap and all other outstanding commitments. 15,430−6,000=9,430, leaving6,430 above floor. Prior7,550/5,605 reservations are fulfilled (J0352/J1191 done), not charged again. No active Flow mint process or new committed Flow production reservation identified; worker repeats reconciliation under writer lock. No money/overage/upgrade/Vertex/Omni. Scope and exact rows/board hashes: `07_Edit-Project/TRANCHE2_SCOPE_J2026.json`. Historical notes below/above retain the old wait as history, superseded here.

**Chain:** J2033 video worker (Cursor, Codex/Gemini fallback) after J2026 -> J2034 elected-Chief picture review -> J2035 no-new-spend versioned assembly -> J2036 technical QA/package plus J1275 actual chapter retiming -> J2037 elected-Chief Ben-watch handoff. All have HOS:009 links in the existing queue. Queued is not claimed: no generation worker pickup observed at this checkpoint. Final-watch card only after real finished-cut gates and durable verified media. Ben's actual finished-film watch/listen applies under4Nov standing order; no worker perception invented.

All57 tranche1 files exist locally and on NAS and match ledger sha256 (`TRANCHE1_INVENTORY_J2026.json`); accepted70/90 and existing completion percentage unchanged. Source facts signature remains historically UNSIGNED despite existing PIPELINE done: no new sign-off inferred. New graphics must composite named newly generated plates where boarded. J2034 must resolve callback P05:11_table_three_again1.20–7.90 against J1237 P01 source0–7 lock before edit; do not silently extend. Other locks: P04:07 0–3.760/hardout<=7.042; P04:10_c1 1.083–6.423/in>=1.083. Long narration stays locked; J0862 Shorts work does not block long picture. No YouTube/Buffer changes.


# J0862 single-take result — 5 Nov 2026

Worker: codex. No final approval. J1894 scope executed once; three accepted v02 takes remain unchanged.

009 B v03: exact review text is 316 characters, 57 whitespace words (review claimed 311). House client, Ben Orbit Narrator, eleven_v3, unchanged settings. Live balance 97,352 / 121,114 before and after (counter lag); 316 submitted characters conservatively logged. No further take authorized or made.

vo_check_py312.sh: PASS, 23.68 s, mean -24.2 dB, peak -4.3 dB, 147 wpm; homophone warning an apple's / and apples requires Ben's final listen. No audio perception claimed.

Hook FAIL: Scribe ends fall at 3.680 s. The scoped 0.150 s trim plus maximum 1.06 speed yields 3.330 s, over 2.850 s. Total with 1 s tail would be 24.680 s. J1894's predicted token timings are not measurements of this new take. No larger gap surgery, second take, script rewrite or timing waiver performed. Chief must scope the next repair.

Media preserved in the HOS checkout, 009/10_Shorts/vo_v02/hos_009_short_B_v03.{mp3,wav}; TAKE and VO_CHECK records accompany this report. All old v02 files preserved. 010 A retains J1004 Option A1. Downstream J2171 remains blocked on this hook; no film stage approved. Nothing uploaded or published.


## J0862 v04 & J2279 audio-capable splice repair — 6 November 2026

Codex covering (`cb18632d` pickup) + Gemini covering (`J2279` direct `audio_input` audition and zero-spend splice/tail-fade repair). `J2195` scoped one opening-only pickup; recorded once with Ben Orbit Narrator, `eleven_v3`, `speed=1.04`. Actual text is 81 characters (brief says 82). Live ElevenLabs balance before: `93,478` remaining / `121,114`; immediate after counter unchanged; guarded spend ledger records 81 characters. No top-up or overage; `0` additional characters generated in `J2279`.

Three retained takes are untouched: `009 A v02`, `010 A v02` (`J1004` Option A1 retained), `010 C v02`. All three rerun word gates PASS; `A` spelling/homophone warnings remain documented. Old `009 B v02/v03` preserved, and `cb18632d`'s initial `v04` composite is backed up at `/Users/benjaminoats/_desk/media/HOS/009_The-Falling-Moon-Gravity/vo_v02_cb18632d_backup/`.

- **Direct `audio_input` audition & splice repair (`J2279`, `gemini`):**
  1. Confirmed **zero spoken repeat** in `hos_009_short_B_v04.{wav,mp3}` or `v03.{wav,mp3}`: `faster-whisper small.en` (`word_timestamps=True`) hallucinated a `0.18 s` duplicate `Seg 8 [24.14->24.32]` (`no_speech_prob=0.986` WAV / `0.988` MP3, `avg_logprob=-0.987` / `-0.966`, 4 zero-duration words with `prob=0.000`) over the `-41.3 dBFS` post-word breath tail (`23.480–23.640 s` in `v03`), which `vo_check.py` mis-indexed to `0:19.74` after `norm()` stripped 9 cardinal numbers.
  2. Caught and repaired an `80 ms` onset clip on `"Isaac"` in `cb18632d`: in `v03.wav`, `"Isaac"` begins at `5.940 s` (`-45.5 dBFS`), whereas Scribe's `6.020 s` marks the `-13.7 dBFS` vowel peak. Keeping full `open_v04.wav` `[0.100:0.900]+[0.960:6.640]` (`6.480 s`, `hook_end_s = 2.820 s <= 2.850 s`, `atempo = 1.00`) + `v03.wav[5.680:23.680]` (`18.000 s`, starting in `-66.0 dBFS` room tone `260 ms` before `"Isaac"` and fading the post-`"moons"` breath tail with `afade=t=out:st=23.480:d=0.060`) maintains the **exact same `+0.800 s` word-timing offset (`6.480 - 5.680 = +0.800 s`), `24.480 s` VO duration (`25.480 s` with `1.000 s` loop tail), and 8 word-boundary cuts (`S01..S08`)**, restores 100% of the `"Isaac"` onset, and passes the unmodified `vo_check_py312.sh` on both encodings with `0` fails and `0` warnings:
     ```text
     PASS  hos_009_short_B_v04.mp3  0:24.48  mean -24.4 dB  peak -4.2 dB  145 wpm
     PASS  hos_009_short_B_v04.wav  0:24.48  mean -24.1 dB  peak -4.0 dB  145 wpm
     ```
- **Media & SHA-256 (`02_Video-Projects/009_The-Falling-Moon-Gravity/10_Shorts/vo_v02/`):**
  - `hos_009_short_B_v04.wav`: `a6666fd27c9a90e781369ea07e4888d87a2d5edb1624a0090ae98fa39504686b`
  - `hos_009_short_B_v04.mp3`: `0c9c4c6ffdb1337dc11acaf57af909f8d8be91d77210bca2e13af80715b87498`
- **Repository gates:** `check_all.sh 009` ALL CHECKS PASS; `check_all.sh 010` ALL CHECKS PASS.
- **Elected Chief PASS (`J2281` / `J0862`, `gemini`, 7 Nov 2026):** Condition for `J0862` verified satisfied (`J2279` complete at `fc1a23f3`; direct `audio_input` audition confirmed clean delivery with 0 spoken repeats and intact `"Isaac Newton"` onset; `vo_check_py312.sh` PASS on `hos_009_short_A_v02.mp3`, `hos_009_short_B_v04.mp3`/`.wav`, `hos_010_short_A_v02.mp3`, and `hos_010_short_C_v02.mp3`; SHA-256 verified on Mini and `studio-live` NAS). `009` and `010` `shorts_vo` marked `done` in `PIPELINE.json`; HOS PR #423 approved and merged; `J0862` and `J2281` closed `done` (unblocking `J2171` for `009` Shorts A/B assembly).

## 7 Nov 2026 — J2171: HOS 009 Shorts A & B GBP0 media inventory, SHA-256 reconciliation & assembly plan v03 (Gemini covering)

- **Authority:** Acting-Chief Codex `J2023` / queue job `J2171`. `£0` / `0` credits. No generation, no credit spend, no upload, no scheduling, no privacy/retitle or Buffer writes.
- **Duplicate & channel check (`05_Analytics/hos/snapshots/2026-11-07.json`, `64` HOS videos):** `0` public, scheduled, or private HOS videos overlap gravity, Newton, the Moon, or orbits. Promoted 009 long (*Why Doesn't the Moon Fall to Earth?*) is not yet uploaded or scheduled on YouTube (planned target `Thu 26 Nov 2026 18:00 UTC`; conditional Shorts targets `Fri 27 Nov` & `Mon 30 Nov 2026 11:30 UK`, watch-ready `Tue 24 Nov 2026 18:00 UTC`, only after long is public).
- **VO & media inventory (`10_Shorts/SHORTS_PICTURE_PLAN_v03.json`, `10_Shorts/J2171/INPUT_INVENTORY.json`, `10_Shorts/J2171/READINESS_REPORT.md`; `SHORTS_PICTURE_PLAN_v02.json` preserved untouched):**
  1. **Short A (`hos_009_short_A_v02`, *What Would Happen If the Moon Stopped Moving?*, `24.32 s` VO / `25.32 s` total, hook `2.800 s <= 2.850 s`):** VO `.mp3` (`c2fd407d…`) & `.wav` (`48847b15…`) Chief `PASS` (`J0862`/`J2281`, directly auditioned via `audio_input`). **`8/9` rows verified on local disk + NAS** (`6` Tranche 1 KEEP Flow plates from `J1192`/`J1237` + `2` `code_graphics_v01` animations `P3:08_km_a_second` & `P3:06_orbit_teach`). **Row `S03` (`5.74–8.98 s`, `P3:07_ball_to_moon`)** is an unminted Tranche 2 Quality parent row owned by `J2033` -> `J2034`.
  2. **Short B (`hos_009_short_B_v04`, *How Did Newton Discover Gravity?*, `24.48 s` VO / `25.48 s` total, hook `2.820 s <= 2.850 s`):** VO `.mp3` (`0c9c4c6f…`) & `.wav` (`a6666fd2…`) Chief `PASS` (`J0862`/`J2195`/`J2279`/`J2281`, directly auditioned via `audio_input`, preserving both `"In one minute"` and `"in one second"` intervals and all `J1004`/`J1894` restrictions). **`9/9` rows verified on local disk + NAS** (`7` Tranche 1 KEEP Flow plates + `2` `code_graphics_v01` animations), with `S05` (`11.44–14.50 s`) mapped to Tranche 1 KEEP moving 3D plate `P4:02_spray_paint` (`8a7b7d90…`) for `J0383` moving-plate alternation between `S04` (`P4:03_sixty_earths`) and `S06` (`P4:04_dots_square`, moving-plate overlay over `02_spray_paint_c2` `0a6279c0…`), and `S07` mapped to `P4:06_pretty_nearly_c1` (`eb3f5d50…`) so all 8 body cuts use distinct clips.
- **Hold / dependency per `J2171` brief (*"If J2034 incomplete do useful inventory only then attach dependency, not claim a ready master"*):** `J2033` (`0/20` Tranche 2 rows minted, blocked on `J2275`/`J2200`) and `J2034` (complete 009 picture acceptance & moving-plate code-graphic composite review) are incomplete, and HOS 009 `05_Music/` score bed is not yet generated (`J2035`). `J2171` attached to `J2034` dependency; no master claimed ready.



### 11 Nov 2026 — J2632 candidate (Codex; not approved)

Falling-Moon continuation rebuilt as a £0 parchment code graphic for 3:03.94–3:09.20, 158 frames at 30 fps, silent. Mini/studio-live SHA-256 matches MANIFEST.json. Row route changed in part-03_plates_v05.json; no splice or KEEP. Gemini timing advisory clear; Grok sheet decision and join review pending. Evidence: 07_Edit-Project/J2632_review/REVIEW.md. Approved-row count unchanged.

Tool outputs: `J2632 geometry, stream, silence and full decode checks passed; review remains pending.` and `ALL CHECKS PASS` (check_all.sh). These are tool results, not final film PASS.


## J2632 revised falling-Moon evidence — 11 Nov 2026

Codex built 179 unique frames at 30 fps, including 21 animated lead-in frames and two open crater rings. Candidate and sheets on PR #543; no KEEP or splice. Parent frames 99–104 and excluded 112/125 are on the boundary sheet. The 24 fps parent loses 0.875 s, while 21 new frames at 30 fps add 0.700 s: 0.175 s remains for Chief timing reconciliation. Original motion mapping and film end 189.20 are preserved in the candidate evidence.

Repository validation output (not film approval):

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
ALL CHECKS PASS
```

## J2632 r4 timing revision — 11 Nov 2026

32-frame head, 190 unique frames at 30 fps; motion pinned to183.94, nominal end189.20. Artwork unchanged. SHA-256 `23c832b09e70f78d8eeece657dac11d6148e2a5f5c701f2ad88b868845b5f3b3`, NAS verified. Evidence: `07_Edit-Project/code_graphics_v01/J2632_r4/REVIEW.md`. Tool output: `J2632 geometry, stream, silence, 190 unique decoded frames and full decode checks passed; r4 timing residual under 10 ms; review pending.` Repo output: `ALL CHECKS PASS`. Gemini advisory: timing contradictions resolved within Chief tolerance; 0.200 s fade and tail snap required at future assembly. Claude sheet read and Chief KEEP pending; splice_authorized=false, PR543 unmerged.


## 18 Nov 2026 — J3047 score disposition

NOT ACCEPTED / NOT GENERATED. J3045 made 0 POSTs and spent 0 credits / GBP0; J3046 audition NOT PERFORMED. No v03 music_gate or listening PASS exists. Prior v01/v02 rejection and J2035/J2171 holds remain. Allowance permanently closed unused. No compliant no-spend score available. 22 Nov readiness at risk; 26 Nov not a release promise. J3050 prepares billing mapping evidence and tests, no generation. Full ruling: `05_Music/SCORE_DECISION_J3047.md`. No film stage marked done.

Record validation (`check_all.sh 009`, isolated J3047 worktree):

```text
ALL CHECKS PASS
```

This is not a score/film PASS; no v03 media exists.


## 20 Nov 2026 — J3233 compliant replacement score route decision (Gemini acting Chief)

Selected **Option (a): compliant £0 non-ElevenLabs own-score route** following completion of the offline billing-guard and disabled-flight hardening chain (`J3139`–`J3174`, merged via PR `#675` `327c220d`, PR `#680` `f13cb7ae`, PR `#681` `3211c7de`). `ACTIVATION_AUTHORIZED` stays literal `False` (`jobs/reviews/J3150/PRICING_EVIDENCE.md` does not establish both `<= 3,000` credits and `£0` cash), `J3043`/`J3045` remains permanently closed unused (`J3047`), and `v01`/`v02` remain rejected (`J2808`).

Following shipped HOS 006 (`trees006_score_bed_v01.mp3`) and HOS 007 (`vaccine_score_bed_v01.mp3`) £0 own-synthesis precedent, `J3234` synthesizes a deterministic pure-Python/NumPy 17th-century D-minor chamber opening (`hos_009_wonder_v03_synth.wav`, `0.00–178.28 s`, Karplus-Strong plucked gut-string lute + warm multi-voice bowed viols, evolving modal harmony, zero silent rests, zero third-party/GPL samples) joined via exact 3.0 s equal-power crossfade (`175.28–178.28 s`) into byte-unchanged `hos_009_teach_v01.mp3` (`4c1f0a17…`), verified by unchanged complete-library `music_gate.py` (`>= 89` comparisons, `0` unreadable, `< 0.80`, no waiver) and continuity telemetry, followed by independent demonstrated-audio review (`J3235`) and separate elected-Chief disposition (`J3236`). `J2035` and `J2171` remain held; £0 cash, 0 credits, no YouTube/Buffer/schedule changes. Full decision & scope: `05_Music/SCORE_DECISION_J3233.md` and `05_Music/SCORE_SCOPE_J3233.json`.


## 20 Nov 2026 — J3236 Chief score disposition on `v03_synth`: NOT ACCEPTED; FINAL bounded £0 full-runtime `v04_synth` authorized (Gemini acting Chief)

- **Verdict:** **NOT ACCEPTED (REFUSED)**. Independently verified `J3234` PR `#697` (merged `03042715` strictly as rejected-attempt audit provenance): deterministic pure Python/NumPy, `19/19` Mini/NAS SHA-256 parity, all `9/9` preserved locks unchanged (`teach_v01` `4c1f0a17…`), unchanged `music_gate.py` (`62b5159f…`) PASS (`94` comparisons across all 9 roots including 15 materialized UAT tracks, `0` unreadable, max `0.3961`/`0.3868`, no waiver), and `0` `silencedetect` dropouts at `-45 dB` (`d=0.25`/`0.50`). However, independent `audio_input` ear review `J3235` (HOS PR `#698`, `EAR_REVIEW_v03_synth.md`) **FAILED** period chamber musicality/warmth (harsh buzzy reed-organ pad + metallic Karplus-Strong MIDI/chiptune pings), `175.28–178.28 s` join quality (jarring timbral cliff into studio-acoustic `teach_v01`), Part 2 `~84.44 s` shift (`+12` semitone octave jump + `+2.2–2.5 dB` RMS bump), and wonder-to-teach cohesion (confirmed by Chief `audio_input` audition of `hos_009_transition_168_186_bed_v03.wav`).
- **Bounded Fallback Invoked (Option i — ONE AND FINAL £0 attempt):** Authorized unified full-runtime (`0.00–535.33 s`) warm D-minor chamber own-synthesis revision `v04_synth` (`05_Music/SCORE_SCOPE_v04_synth.json`), modeled on shipped HOS 006/007 warm low-harmonic pads + clean soft exponential-decay harp with smooth 3.0 s chapter-card transitions (eliminating both the synthetic buzz/pings and the `175.28–178.28 s` timbral cliff). Queued **`J3239` (assembly) -> `J3240` (independent `audio_input` ear review) -> `J3241` (final Chief disposition)**. **No `v05_synth` allowed**: if `v04_synth` fails `music_gate.py` or `J3240` ear review, `J3241` immediately escalates ONE single ElevenLabs `music_v2` billing/pricing confirmation question to Ben (Option ii).
- **Guardrails & Holds:** `£0.00` cash, `0` credits, `0` account GETs, `0` ElevenLabs POSTs, `ACTIVATION_AUTHORIZED = False` preserved, `J3047` closed unused, `v01`/`v02`/`v03_synth` rejected, `teach_v01` untouched, `J2035` (also awaiting `J2632` picture KEEP) and `J2171` remain held (`blocked`), no YouTube/Buffer/schedule changes. Full ruling: `05_Music/SCORE_DISPOSITION_v03_synth.md` and `05_Music/SCORE_DISPOSITION_v03_synth.json`.


## 22 Nov 2026 — J2036: HOS 009 long master v03 technical QA pack & package completion (Gemini worker)

- **Scope & authority:** Worker technical QA pack only (`J2036`), opened to `gemini` by Claude (`2026-11-22T11:16Z`). **Not a film PASS and not a self-merge.** Full moving-picture and audio review remains assigned to Ben's final watch (`ben_ok: todo`, per 4 Nov 2026 standing order). £0.00 cash, 0 Flow credits, 0 ElevenLabs credits; no YouTube, Studio, Buffer, schedule, or privacy changes.
- **Exact master & input hashes (live recomputed Mini + NAS):**
  - `hos009_long_master_v03.mp4`: `744f32b7f2f95e75fabf039a345aee6c7c01ab6f304a932ebe7172bd3b3ede55` (`898,035,226` bytes, `519.000 s`, `1920x1080` h264 30 fps `15568` frames, AAC 48 kHz stereo; byte-identical Mini scratch ↔ NAS `09_Assembly/j2035_v03/`).
  - Prior masters verified untouched on NAS: `v01` `802b5c7eb0dd64a77b938e5f26c2f63104c3b851979dabe61e39e70eaf33a833`, `v02` `9d8731cb49641776027bcbd75a6f4ae5519fc3907c28cb7f422883ebde73ef10`.
  - Locked VO (`VO_TAKES_KEEP.json` `530743c5…` + all 5 MP3s), `v04_synth` score (`151ba46a…`), J2631 (`e35f9a98…`) & J2632 r4 (`23c832b0…`) code graphics, and J3262 thumbnails A (`cd44f056…`) & B (`3d116433…`, 7/7 Mini↔NAS parity) all verified byte-identical.
- **Independent unmodified gate re-runs on v03:**
  - `picture_qa.py`: `picture QA PASS: 0 of 92 cuts fail, 74 to look at`
  - `polish_gate.py`: `polish gate PASS: 0 of 92 rows failed, 5 to look at` (all 5 low-detail warnings — 1:25 card, 3:04 falling-Moon diagram, 4:21 card, 4:54 spray wall, 5:26 split diagram — visually inspected at 1080p, all clean by design)
  - `music_gate.py`: `music gate PASS: hos_009_score_v04_synth.wav, 535.3 s, about 52.2 BPM, brief Pace: 60-68 BPM`
  - `sfx_kit.py level`: `SFX level PASS: VO -20.8 LUFS, SFX -41.4 LUFS, 14 hits`
  - `ffmpeg ebur128 + silencedetect`: Integrated `-20.8 LUFS`, LRA `4.8 LU`, True Peak `-4.0 dBFS`, `0` silences ≥ 1.5 s.
  - `reviewed_ok.json` unchanged (2 entries only: Grok `6792271903` table callback 0.30–7.00 s; Grok `7046684862` wooden-arch split panel on `05_minute_second`).
- **E2 / Teach / Stills:** 8 opening cuts of `3.9925 s` (< 4.5 s), 0:05–0:15 proof stills verified, `26.15–29.75 s` early DATA+SCALE `THOUSANDS OF YEARS` teach card verified, 33 cards (`0` overlaps, `0` chapter bleeds, `0` cross-shot drifts), all 4 v02 findings resolved; all 21 verification stills + 5 low-detail warn frames + Halley WHO + 1758 comet + 66M handoff + thumbs A/B inspected.
- **Package & provenance:** Exact v03 chapter times (`0:00, 1:24, 2:56, 4:20, 6:33`) and all 8 `Sources` preserved in `11_Upload-Package/Descriptions/moon_long_description_v01.txt` (HOS 010 untouched for `J1275`); honest making-of line added (`studio/RULES.md` line 227); `production-status.md` header reconciled with `FACT_NOTES_v01.md` (lines 3 & 77) and `PRE_BUILD_VIDIQ_AUDIT.md` (§7) without inventing a new sign-off; Shorts (`J0862` VO PASS, `J2171` PR #718 open / `J3311` review held) retained separately. Full report: `07_Edit-Project/J2036_V03_QA_2026-11-22.md`.
- **Pasted contract & package lint outputs (`check_all.sh` + `lint:package --film 009`):**
```text
PASS  02_Video-Projects/009_The-Falling-Moon-Gravity/11_Upload-Package/PACKAGE_MANIFEST.json
   warn  [captions] no captionsFile (captions from the script)
ALL CHECKS PASS
```
