# HOS 128 — independent draft review (J3547)

Reviewer: `macbook`, 24 November 2026. Advisory recommendation: **FIX before lock**.
Reviewed HOS PR #751 at `7702cc769a44a342d1fad9cfec0ccff8cb46526f`, including its package scoring, long script, FACT_NOTES, SOURCES, Shorts and launch plan. This report changes no spoken script, grants no PASS, and authorises no VO or picture generation. Chief owns the final decision and merges; PR #751 and its included topic PR #725 remain unmerged by this worker.

## Packaging recommendation

Retain proposed title Arm A, **Why Do We Use AC Instead of DC? (Edison vs Tesla)** (49 characters); it clearly states the question answered by the film. Retain the named-rivalry B/C titles (61 characters each) as candidates for Chief selection. The recorded 95/93/91 scores are draft judgements, not measured CTR or independent phone validation. A character limit does not guarantee no mobile truncation. Existing competitor figures were read as dated research, not refreshed as live analytics.

Thumb A's thick/thin wire contrast is useful, but **1 MILE LIMIT** must not imply that DC physically stops at a fixed distance. Short A and the description make that misleading implication explicit. Revise around the economic constraint of Edison's low-voltage system, and avoid a literally red-hot working street cable as historical fact. Thumb B's **22 MILES AWAY** remains on hold until its exact route distance is sourced; the current claimed primary verification is absent. Neither concept is rendered: 168px readability, style_sheet and image quality remain untested. The optional third thumbnail also needs its own review before a three-way test.

## Corrections required before lock

1. **Part 01: Pearl Street is not the first central power plant without qualification.** Rutgers' Edison chronology lists Holborn Viaduct starting on 12 January 1882, before Pearl Street on 4 September. Suggested replacement: “Edison switched on Pearl Street Station, bringing his central-station direct-current system to Lower Manhattan.” Recheck the separate 3pm detail; the attached row-1 quotation does not establish it. Source: [Rutgers Edison Papers, 1882 chronology](https://edison.rutgers.edu/edit-chronology/chronology-details/1881---1890/1882), read 24 November.

2. **Part 02 conflates Stanley's voltage demonstration with street distribution.** The [IEEE milestone](https://ethw.org/Milestones:Alternating_Current_Electrification,_1886), read 24 November, distinguishes a 500→3,000→500 V demonstration with series lamps from building transformers supplying 100 V. The draft instead sends 3,000 V along the entire 4,000-foot line directly to 100 V shops. FACT_NOTES row 7 itself quotes a return to 500 V but marks the incompatible claim OK. Rewrite VO and DATA to reflect the source accurately. Also, 4,000 feet is only about 0.76 mile: this example cannot itself prove that a “one-mile trap” was broken. Suggested bridge: “The transformer principle worked. Scaling it into a wider network was the next challenge.” The football-pitch comparison needs an explicit assumed pitch length or a simpler sourced scale.

3. **Part 06 confuses cycles with reversals.** Use “completing fifty cycles a second … or sixty” and change the SCALE text from “fifty to sixty silent flips” to cycles. A sinusoidal cycle has two direction changes. [US EIA](https://www.eia.gov/electricity/930-content/about.html) describes North American operation in cycles per second. This is a physics correction, not approval of every other grid claim in row 20.

4. **Niagara evidence is not a quotation.** FACT_NOTES row 19 links only the NPS homepage and supplies a paraphrase, without an identifiable document/page or exact quote. That cannot verify the bundled midnight/date, 11,000 V and 22-mile claims. Obtain the actual NPS/IEEE document and separately check every element; otherwise soften/remove unsupported precision from the long, S02, thumbnail B and launch copy. Do not substitute a different mileage without route-specific evidence.

5. **SOURCES misattributes Wikipedia pages as primary institutions.** Entries labelled Smithsonian, IEEE and NPS mostly link to Wikipedia, not those institutions. Replace them with actual institutional pages and findable quotations, or label them honestly as secondary sources. The “21 OK / 0 FLAG” claim is not independently upheld. Row 17's quotation does not establish the exact $399,000 winning bid; row 5 does not establish May unveiling; row 10 does not establish the March presentation or Ferraris's stated reason for not patenting. Quote-check those individually, along with claimed personal motives, physical cable dimensions and the claim that the fair's success “sealed” Niagara. These are unresolved evidence gaps, not a claim that all are false.

6. **Long opening timings are unsupported by the actual speech.** The 16-word opening question takes about 6.4s at 150wpm. The next 38-word answer brings cumulative speech to about 21.6s; the promise then starts after the required 0:15 milestone, despite the visual note placing it at 0:11. Rebuild the opening to deliver the promise by 0:15 and stakes by 0:25; measure from the actual spoken text and later VO, not annotation timestamps. Keep the answer image by 0:05 and question by 0:08. The special seven-shot experiment applies only to 008–010, not 128.

7. **Short A is not the stated 45 words / 17.5s.** Whitespace count of its supplied spoken paragraph is 51 words: about 19.87s at its own 154wpm assumption, before pauses. Its first 12-word sentence is assigned 2.8s (about 257wpm); at 154wpm the surprise arrives much later than 1.5s. Short B has 48 whitespace tokens (47 excluding the standalone em dash), rather than 46, and its 11-word opener is assigned 3s. Both need shorter, immediate subject-and-surprise openings and a fresh read-through. Do not speed up finished VO to fit. Target 16–19s with actual take measurement.

8. **Short teaching and loop clarity need repair.** S01's fixed one-mile “died” claim overstates an economic range; qualify or replace it. Its final “which is exactly why” makes the following DC limitation sound caused by the subsequent adoption of AC: repair the causal loop. S02's Niagara date stamp starts at 4.5s while the narration is still discussing pre-1888 motors, and the 6.5–10s scene overlaps its 9–14s title row. Retiming must leave one overlay, correct historical context and no simultaneous competing labels. Both have house-style moving-frame intentions, title promotion and matching-end-frame instructions; no rendered OPEN/LENGTH/LOOP gate has been run.

## Teach, polish and craft review

The draft contains 7 DATA, 7 SCALE, 6 WHO, 13 WHEN, 4 FACT and 2 Explorer beats, six TEACH blocks, a timeline and five chapter cards. This is a useful structure, not proof that each requirement is met. William Kemmler is named without a WHO card. The Part 04 image dates the confidential report to 1888 while the VO says 1886. The Pearl Street ten-minute-walk SCALE is not spoken; the motor DATA/SCALE is qualitative rather than a number. Schedule multiple markers sequentially, shorten the five-word “82 customers on day one” label, and source all visual claims. Include sourced portraits and year-first human detail as required by Craft.

The six-part escalation and hand-off ending work in outline. Explorer placement is outside the first minute. The final nuclear-test hook needs a source row or a softer hand-off. Script timestamps and launch-plan chapters disagree and must be retimed after VO. A plate board must break long scene descriptions into the standing 4–6s picture changes. SFX levels, music coverage/change, grain, crossfades, actual overlay motion and final picture quality are unverified until media exists; do not mark them passed from script markers.

## Verification and handoff

Fresh local tool outputs on a verbatim export of the reviewed commit:

```text
review:script: Decision PASS · Score 92 / 100
Words: 1292 · Est. min: 8.6 · Chapters: 5
Structure gates 8/8

gate:episode: Decision PASS — VO / Gemini Veo allowed
project_dir OK; prebuild_vidiq OK; script_file OK; script_review OK;
explorer_acts OK; visual_must OK; teach OK; chapters OK;
production_checklist OK
```

Those are mechanical tool messages only. They do not override the independent factual findings or Chief-lock requirement. No production stage was completed, so no film status or production-status PASS was written.

Input SHA-256: long `abc95edaaad66297e104f647f0e107f3c1333670b2ef3a96cee31be90f4641a9`; FACT_NOTES `c6e92d002d9d485f9778e8db5970804102dde651ea559c269e1d968bc4c07998`; SOURCES `d87a6506f0919b0a26286096e08a6f7ed4e0657eb7b85c03d9c1620b1c438548`; Shorts `ff7cb3ae0ce17be5ac0b8e4951dba37ae7f7bf2e944b45ac7f8e977d94d6a53b`.

Next owner: Chief. Route a corrected v02 to the script author, obtain an independent facts pass and direct quotation check against its exact hash, rerun both script checks and actual Shorts timing, then decide package/script lock and VO jobs. Keep J3547 blocked for that protected decision rather than marking the requested lock complete. Preserve the planned 10 December target and existing slip contingency; no scheduling action occurred.

Repository verification: `bash 00_Brand/Channel-Setup/tools/check_all.sh` completed with `ALL CHECKS PASS`; `git diff --check` was clean. Existing package warnings remain warnings.
