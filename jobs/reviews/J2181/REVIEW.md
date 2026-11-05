# J2181 — bounded existing-media recipe, 5 November 2026

Codex covering. **Partial repair proposal; NOT BUILD READY.** This producer is delivered for independent review, not KEEP or a film PASS. No cut build, generation, spend, publishing, Buffer writes, production-stage approval or Ben-watch card. J2169 stays blocked at 1/3.

## Exact replacement proposals

Coordinates below are **native source x:y:width:height**, before scaling to 1080×1920. Playback is 1×; no freeze, artificial push, alias, intermediate upscaling or padded duration. Full hashes and absolute original NAS paths are in the complete `Short_B_cuts.json` / `Short_C_cuts.json`, their pools and `SOURCE_INVENTORY.json`. All 14 unique sources match recorded long KEEP hashes; both actual VO files still match canonical locks (`PROVENANCE_CHECK.json`). Prior KEEP does not approve these new crops.

| Short / row | Film interval | Native source / interval | Crop | Disposition |
|---|---|---|---|---|
| B S01 | 0–2.24 | P1 `03_pot_jar_leaf_t1`, 1–3.24 | 700:190:460:818 | Distinct mint opening; isolates mint from willow and water-leaf jars. 2.348× maximum enlargement, near the limit: explicit sharpness review required. |
| B S02 | 2.24–5.62 | P3 `15_quill_vegetable_t1`, 0–3.38 | 0:0:608:1080 | Actual frames show burning candles under a bell jar, no mint. Crop excludes quill/writing/face. Multiple candles and left-edge flame near interval end need reviewer attention; this is a proposal, not asserted perfect continuity. |
| B S04 | 9.40–13.02 | P3 `10_mint_jar_t1`, 0–3.62 | 656:0:608:1080 | Original insertion/waiting source now unique in B body because S01 changed. Inherited framing still needs rendered verification. |
| B S05 | 13.02–16.30 | P3 `11_candle_tall_t1`, 0–3.28 | 656:0:608:1080 | Original post-mint candle source now unique in B body because S02 changed. |
| B S07 | 19.46–23.20 | P3 `01_soil_to_sky_t1`, 0–3.74 | 600:0:608:1080 | Literal green plant instead of a town. An illustrative plant conclusion, **not evidence of another historical experiment**. Native moving source, no made-up insertion or proof. |
| B terminal return | 23.20–24.20 | Same P1 `03_pot_jar_leaf_t1`, 0–1 | Same as B S01 | Exact source preroll leads to opening source at1s; explicitly retained as a loop row. Pending system contract and rendered correspondence checks. |
| C S05 | 12.00–14.96 | P1 `03_pot_jar_leaf_t1`, 0–2.96 | 1120:0:608:1080 | Leaf and bubbles isolated from other jars. Unique in C body. Uses same original file as B's mint crop **across different Shorts**, never a fake new source identity within a Short. |

C's opening remains the genuine `05_bubbles_macro_t1`, now with explicit source1–3.56s and terminal0–1s to retain preroll provenance; both have matching native crop. This is a **proposal**, not a validated seamless loop or an exemption declaration for the old checker. All 17 rows, including both terminal returns, remain in the lists. All spoken lines, row timings, canonical takes and J1004 lawful edits stay untouched. No original BUILD_RULE or uploaded manifest was rewritten. `BUILD_RULE_J2181_REPAIR_PROPOSAL.json` is the explicit proposed delta, not a second production tracker.

## Closed alternative-source pass

`CANDIDATE_BUDGET.json` records the cumulative bounded pass and dispositions: eight unique original sources, at most three in-depth candidates per missing input; conservatively charged at most13 active minutes of the20-minute scope. **This pass is closed; a restart does not reset its budget.** Baseline J2169 footage was not searched again; unchanged rows were decoded to measure the complete proposal honestly.

All four specifically named candidates were present and hash-matched, but actual stills reject them for these uses:

- `07_priestley_t1`: Priestley gathering brewery air beside a vat; no candle. A filename, prompt or old KEEP is not a candle-shot qualification.
- `12_mouse_mint_t1`: mouse beside and overlapping mint. A narrow/top crop cannot truthfully provide a full-height plant/insertion shot at the allowed enlargement without the unrelated animal experiment.
- `15_leaf_turns_sun_t1`: real plant but only1280×720. Full-height portrait requires at least1920/720 =2.6667×, above2.35×.
- `10_only_green_t2`: actual leaf/bubbles, but the same720-high bound fails before any tighter jar crop. The three-jar frame itself is not silently accepted as one experiment.

Additional inspected alternatives: `09_injured_air_t1` already has a dead wick, unsuitable for the burning-candle line; actual `15_quill_vegetable_t1` unexpectedly contains candles rather than its prompted mint; P1 `03_pot_jar_leaf_t1` provides the clean mint and leaf regions; P3 `01_soil_to_sky_t1` provides the literal plant. Selected crop start/mid/end stills were inspected after native-coordinate extraction (`STILLS.json`, durable `_desk/handoff/J2181` paths and hashes). During broad sampling, requests at/past a4s end produced no frame and one6s-source late sample emitted `mmco: unref short failure`; those invalid samples were discarded, never used as still evidence. Every **used** interval decodes without stderr below.

## Machine results and remaining blockers

`verify_recipe.py` reads originals only. All17 proposed intervals fit actual durations; every native crop is in bounds. All used cropped intervals decode successfully, with no decoder stderr, zero identical adjacent decoded frames and unique frame hashes throughout each interval (`MACHINE_CHECKS.json`). This establishes changing pixels, **not natural perceived motion, anatomy, warmth, listening or a seamless rendered loop**. Source stills do not replace Ben's final watch/listen under the4Nov order.

Ran the **unmodified installed** OWB `picture_qa.py` on the complete lists (source-only; no video argument):

- **B FAIL,2/8 rows:** S06 at2.67×; terminal return still fails same-stretch reuse. S01 at2.348× is a sharpness warning for review.
- **C FAIL,4/9 rows:** S01, S07, S08 and terminal return at2.67×; terminal return also fails same-stretch reuse.

The replacements remove all body same-stretch repeats. No failed loop was omitted, relabelled into a different source, or marked reviewed-ok. The inherited baseline used1.7778× on every source, including720p ones; that value is not the real enlargement for a1080×1920 full-height crop. The explicit native recipes measure it honestly (404-wide720-high crops give max2.6733×; even an ideal aspect crop cannot beat2.6667×).

**Exact missing full-portrait inputs now exposed:**

| Row | Duration / picture | Why current source cannot qualify |
|---|---|---|
| B S06 | 3.16s, candle burning brightly in repaired air, same Priestley context | `06_collect_blaze_t3` is1280×720; it is also an Ingenhousz gas-collection setup, so any replacement must avoid implying that different experiment is Priestley's proof. |
| C S01 + terminal | 2.56s open plus1s leading preroll, green leaf underwater visibly releasing silver bubbles at frame0 | `05_bubbles_macro_t1` is1280×720; authentic identity is retained, but source cannot meet2.35× at full height. No fake up-res copy as a new source. |
| C S07 | 2.80s, jar returned to sunshine and bubbles resuming | `12_shutters_open_t1` is1280×720. |
| C S08 | 2.88s, sunlight powering green leaf | `14_leaf_glow_t1` is1280×720. |

Required replacement format: real changing frames at1×, premium HOS3D cartoon, native1920×1080 (or native portrait1080×1920), crop covering each full row, <=2.35×, honest spoken claim, distinct body source, no garbled text, no Explorer at frame0, no new words/VO. Opening also needs1s usable preceding footage and eventual rendered-loop evidence. These inherited issues were exposed by measuring the requested **complete** source recipe; no extra unbounded asset hunt was started.

Queue **one bounded elected-Chief fallback decision** for these four source needs, with a proposal to use existing full-resolution originals if genuinely available, otherwise separately authorise at most four new HOS Flow/Veo clips, at most two takes per clip, at most200 existing Flow credits total (Quality for candle/flame; no generation under this job). The decision must read current route prices, live balance, credit guards and script/VO approval, adjust scope downward to the cap, and create a specific producer/reviewer chain. This is a **request for a later scoped decision**, not credit authority. If it chooses another honest framing, prove the real scale and all channel rules; no waiver, still push, freeze or re-encode workaround. No new search budget without a genuinely new source/approach and bounded scope.

## Review and release chain

Immediate `kind:review` successor must review these exact crops, the new opening at phone size and candle-count/edge continuity, original KEEP provenance, complete cut/pool records, explicit resolution FAILs and budget log. It may retain useful mappings while requiring fixes. It must also read **J2180's FIX on PR512 head`be2c980ffa`**, J2179 corrections and **J2182's subsequent system re-review/merge evidence**; J2180 being done is not checker acceptance. Do not reopen J2169 while any required source or checker condition remains unresolved. Queue the named source producer after the bounded fallback decision; no generic timed retry or capability-only hold.

J2169 remains1/3. After all source/checker/mapping issues are genuinely cleared: build, run every rendered gate (picture, polish, music/SFX, captions, opening/loop, decode), durable hash-verified deliverables, immediate finished-cut review, then Ben UAT. No awaits without the finished passing cut. No long/live stage change. A/retired/superseded exclusions and standaloneS7 planned-only collision hold stay. Watch-pack15Nov18:00Z and B18Nov/C21Nov11:30 remain conditional; long`VbPubYd6Fbs` must read Public and all approvals must hold before any Short release.

Repository validation is recorded separately in `REPO_CHECKS.txt`; it cannot clear any media FAIL above. No media is committed. Evidence is produced from clean worktree `/private/tmp/J2181-wt`, branch`codex/J2181`. Both repos pulled successfully; required NAS scratch offload found nothing old enough to move, around16GB free. Nothing on the NAS was changed or deleted. No background render exists.
