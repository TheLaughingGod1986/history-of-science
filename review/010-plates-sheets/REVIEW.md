# J2770 — independent HOS 010 still and tool review

13 November 2026 · reviewer `codex` · producer `gemini` · £0 / zero credits.

**Evidence complete; FIX before assembly.** Two plates have no identified still-subject defect in the tested framing; ten need crop, interval, mapping or overlay repair. These are **still/tool PASS or FIX only**, not motion PASS, KEEP, a finished-cut gate or permission to render. All twelve remain unaccepted under J2271. J2758 is the existing handoff for capability/Chief disposition; no duplicate verification was created.

## Scope and provenance

Read HOS AGENTS.md, studio/RULES.md, character bible, current shot/Short plans, TWELVE_PLATE_SCOPE_J2267.json, GENERATION_AUTHORIZATION_J2269.json and OWB jobs/reviews/J2757/REVIEW.md. Producer evidence and unchanged half-second sheets are from HOS PR538 head `2f0a227f6b30322d20926f7848851ef1c6a4890c`. Every copied producer-sheet hash matches that manifest. INDEX.md records exact parent, archive, start-still and sheet hashes and line mappings. TOOLS.json contains fresh measurements and findings.

The session directly viewed all 12 original full-clip contact sheets, all 12 new portrait sheets, both extra preroll sheets, the Explorer generation reference and the two house-style references. It can perceive still images and text. It has **not** perceived continuous motion or heard audio. Pose changes, ffmpeg, a clean decode and a model name cannot establish native movement, natural timing or absence of inter-frame defects. Claude's desk offer (6840496402) is an offer only; no Claude review is claimed.

## Tool checks

Fresh check output:

```
VERIFIED 12 parents; decode failures 0 hash mismatches 0
```

All 12 working files and all 12 durable archive copies match the expected unique SHA-256 hashes. Full `ffmpeg -v error -xerror -i <source> -f null -` exits 0 with empty error output for every source. All sources are 1280x720, 24 fps, 7.916667 seconds, zero audio streams. This proves source-audio absence, not that a final mix has been heard. All requested individual Short intervals fit the durations; the nominal eight-second source is actually two 24-fps frames shorter than eight seconds. No freeze, stretch or fabricated padding is approved.

No readable baked words, Orbit robot, DNA helix, black bars or flat padding were found in the inspected source samples. This statement is limited to sampled stills, not an all-frame OCR or motion check. References support a dimensional, warmly shaded cartoon look; the robin skeleton is a specific exception needing repair, not a blanket house-style acceptance. Text in sheet headers is review annotation, not source picture.

## Portrait and upscale measurement

Diagnostic samples use a fixed full-height crop `x=437,y=0,w=405,h=720`, exact 9:16 source geometry. Each tile displays at **390x694** (rounded phone height); there is no blurred, mirrored or flat filler. Samples: source 0 s, 1 s, maximum Short-use minus 0.05 s, and 7.85 s. The fixed centre crop is a diagnostic, **not a claimed approved assembly recipe**. Crop defects below apply to this tested framing and need verified replacement framing, not automatic regeneration of every source.

At 1080x1920 delivery, this crop requires **2.666667x**, over the existing 2.35x ceiling: **FIX if that output is used**, on all twelve. Phone downscaling does not waive the master-scale gate. A mathematical alternative is 936x1664 at **2.311111x**, exactly 9:16, already used in the HOS J2175 framing review. It is only an option for the reviewer to adopt if the delivery contract permits; no output dimensions are changed by J2770. If 1080x1920 is mandatory, obtain genuinely higher-resolution source (at least 818 pixels tall for this ceiling; 1080-high preferred), not a pre-upscaled copy. Padding is forbidden by the current HOS Never list.

## Per-plate evidence and repair scope

The PASS column covers sampled subject/framing only; source hash/decode/audio checks pass on every row. Common output-scale and untested motion gates remain open on every row.

| Plate | Still result | Observation | Exact remaining repair |
|---|---|---|---|
| `P1:01_clay_line` | PASS | The thin dark band and pointing fingertip read at phone size at 0, 1 and 2.799 s. Warm shaded rock and stylised hand fit the references. | No still-subject repair. Preserve band and fingertip in the approved crop; resolve common output-scale and loop-contract requirements below. |
| `P2:01_walter_hammer` | FIX | Landscape shows a geologist at an Italian cliff, but the centre portrait at 0 s cuts off his face, hand and hammer; later hand-to-rock contact is outside the crop. | Specify and sample a right-shifted or tracked 405x720 crop through the full 3.340 s, keeping the hand, hammer and thin layer visible. A face-only crop does not demonstrate the centimetre-thick layer. If no crop works, request a separately scoped portrait-safe plate. |
| `P2:03_tiny_shells` | PASS | Dense small rounded/spiral fossil forms below the dark boundary remain recognisable in the phone crop. Magnifier and rock have depth and warm house shading. | No sampled subject repair. Keep the lens and fossil-rich lower layer visible; common delivery-scale requirement still applies. |
| `P2:05_almost_none` | FIX | At 0–2.5 s the magnifier examines the dark band with sparse shells; it reaches the empty upper rock around 3 s, almost at the end of the 3.720 s row. The words already say Above it earlier in this row. | Align a verified source window showing the upper nearly empty rock with Above it, using the accepted word alignment. Candidate later window must be checked throughout for 3.720 s; do not change the VO or assert that the current 0-based window passes. |
| `P3:08_asaro_michel` | FIX | Two laboratory scientists and instruments read in landscape; the centre portrait cuts both faces at opposite edges, leaving equipment between them. No readable baked words seen at sampled size. | Use a verified crop on one scientist with the sample/testing apparatus (the Short does not name either scientist), or obtain a portrait-safe composition of both. Check the entire 3.120 s. Preserve the named long-board identities separately; this is not historical likeness verification. |
| `P4:06_dust_veil` | FIX | Forest under a dark cloud/dust canopy is visible and shaded, but neither an impact nor asteroid is visible. The mapped lines are Something huge had hit the Earth and When the asteroid struck, not a line about darkness. | Return the line-to-picture mapping for reviewer decision: provide existing accepted impact evidence or a separately scoped literal impact/aftermath shot. Do not call an ordinary dark sky proof of an asteroid strike. Preserve both 3.000 s A and 3.320 s C uses. |
| `P5:08_all_at_once` | FIX | Every sampled frame shows a stratified rock cliff; no birds or other living descendants appear. This directly misses Their descendants are all around you now. | Replace the C S04 mapping with a verified 2.500 s scene of living birds, subject to existing reuse limits and separate review. The current cliff may remain a long-form candidate for a geological line; no source deletion or regeneration here. |
| `P5:09_robin` | FIX | Robin is recognisable, but at 0.5–1.5 s the bright skeleton is detached from the bird rather than aligned to it; 0.958/1 s phone samples show the bird beside a standing skeleton. At 1.83 s the robin is partly clipped at the right edge. | Do not use the current opening/skeleton interval. Review a later clean bird window and its preceding 1 s if the approved recipe permits removing the overlay; otherwise scope a corrected plate. Any changed opening, tracked crop, overlay choice and loop must be reviewed; no paint-patching or implied motion acceptance. |
| `P5:10_explorer_robin` | FIX | Explorer matches the reference in sampled faces: young boy, round gold glasses, finished brown hair, teal coat, tan waistcoat and satchel. One Explorer only. In the portrait the robin is clipped at lower left initially and absent by 3.55 s while the line still concerns every bird. | Keep the bird and Explorer interaction in frame across 3.600 s, with the bird still visible when named. Test an earlier/windowed reframing; if impossible use another accepted bird shot for that line or scope a portrait-safe replacement. Never put Explorer at Short frame 0. |
| `P5:12_clay_callback` | FIX | Distinct clay callback shows two people studying rock, not living birds above the viewer. It misses Look up. They never really left. Its different hash and different scene support a separate callback take, not evidence of full-frame duplicate detection. | Replace C S08 mapping with 3.180 s of living birds/sky consistent with the locked line; respect repeat limits. Keep this clay plate as an unaccepted geological long-form candidate. |
| `P5:09a_pigeon_pavement` | FIX | Landscape has the correct pigeon on pavement and robin on a fence. Centre portrait at 0 s clips the pigeon and loses the robin; at 1 s robin is cut at right edge; at 2.59 s both read. | Choose a source offset/crop that shows both named birds at the right word times for all 2.640 s. Their initial horizontal separation is too wide for this tested centre crop. A later window may work but needs full interval evidence and word alignment. |
| `P5:13a_gull_seaside` | FIX | Landscape gull over chalk coast is the correct bird/setting. Centre portrait clips the gull at 1 s and loses it entirely near 2.67 s. | Specify a tracked or later source window keeping the gull visible through 2.720 s; test both wing extremes. Preserve the coast/fence establishing context and the robin-to-gull word boundary. No subject substitution. |

## Loop and rule-8 checks

The current rule-8 opening requirement remains: moving full-bleed subject, subject/surprise in sentence one, no meta-promise. The locked A/C text supplied in the plan contains no meta-promise. A's clay subject is recognisable in sampled frame 0; C's robin is recognisable but its detached skeleton fails the proposed opening. Actual native movement and rendered caption coverage remain unverified. Accepted A/C voice files and J1004 Option A1 are preserved; this review does not re-lock, rewrite, retime or rejudge the accepted spoken hook.

A: opening 2.849 s + terminal tail 1.000 s = 3.849 s source capacity, leaving **4.067667 s** within the measured source. C: 1.880 + 1.000 = 2.880 s, leaving **5.036667 s**. These are capacity calculations only. Source 0..1 s and 1..3.849 s (A), or 0..1 s and 1..2.880 s (C), would be disjoint forward-preroll candidates if separately prescribed. Extra sheets sample 0, 23/24, 1 and the opening-plus-preroll endpoint. A retains the band at these samples; C retains the detached skeleton around the boundary and therefore fails that candidate. Do not claim a seamless loop from those four stills.

The existing terminal-loop checker contract in OWB STUDIO_PLAYBOOK.md instead documents an explicitly prescribed same-source interval return with identical framing, exact hashes/word evidence and rendered pixel checks; it explicitly does not claim seamless motion. Do not silently interchange that permitted replay contract with a forward-preroll recipe. J2172's accepted prescription must resolve which is intended, including offsets, crop, frame rounding and final word alignment. No terminal-loop contract or cut has been generated here. Tail A begins 22.289 s after the plan's final word 22.169 s; C begins 22.560 s after 22.500 s. Both tails are one second and contain no spoken line in the supplied plan. Rendered timing still needs verification.

The separate callback has a different scene and hash from the opening. No full-frame within-run duplicate audit or continuous-motion review is claimed. Generic footage reuse limits, picture QA, full-bleed, polish, captions, music and final cut gates still apply. The two existing code-graphic parents are outside this twelve-parent assignment; they are not accepted by implication.

## Handoff and preserved state

Send this evidence to **existing J2758** for disposition of J2271 under Ben's 4 November final-watch order. Preserve every FIX above. J2271's capability hold is retained; J2172 remains after J2271 at 1/3. No KEEP flags, media, source boards, accepted A/C VO, J1004 Option A1, generation authorization, budgets, schedules or publishing state were changed. Final source acceptance remains J2271; final cut watch remains Ben. Any repair generation needs its own bounded authorization; none is requested or launched by this evidence-only job.

The reusable evidence lives at `review/010-plates-sheets/`, as requested on the desk. No claim that Claude has reviewed it. This task ends at evidence handoff, with no assembly release.

## Repository validation

`bash 00_Brand/Channel-Setup/tools/check_all.sh` completed with `ALL CHECKS PASS`: durable desk handoffs, email ratchet, no media, status board, ElevenLabs guard, VO word checks, atempo tests/speed check, contract tests and package lint. The first attempt lacked worktree Node dependencies and hit npm-cache sandbox permissions; retry used the existing checkout's installed dependencies through a local untracked symlink, with no installation or source change. Existing package warnings are unchanged. These repository checks do not turn any plate FIX into PASS.
