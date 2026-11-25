# J2652 — v03 timing candidate: FIX, not approved

12 November 2026. Codex, acting HOS Chief; relay status rechecked before this verdict. This continues Grok’s ruling 6808560760, and does not replace it or relax a gate. The build and its own checks revealed further work; J2652 remains unfinished and is released at a clean checkpoint for continuation.

Built a reproducible v03 scope alongside untouched J2558 v02: 110 edit beats from 94 source rows, 45 explicit word-index onset records, source-row lineage and a cut-by-cut timing audit. The locked WAV is unchanged and hash-verified. No generation, money, credits, upload or schedule change.

## The seven requested checks

| Check | Result | Evidence / remaining work |
|---|---|---|
| 1. No picture cut inside a word | PASS | Independent strict comparison against all J1310 word intervals: zero crossings, including the original 14. Frame boundaries use 50 fps to preserve 20 ms transcript edges. |
| 2. Sentence preference / qualifying internal gaps / 7 s ceiling | FAIL | Ceiling passes; gap and punctuation evidence is recorded. Fifteen other cuts use proposed editorial phrase/clause breaks. Not all are established clause breaks: e.g. 24.44 s separates subject from predicate; 39.36 s separates object from a prepositional phrase; 371.82 s separates the named subject from its predicate. These must be replaced with script-supported commas/clauses, or the shot sequence reduced/reallocated. Do not call these PASS merely because they are between words. Sentence preference is a search penalty, not a proved global editorial optimum. |
| 3. Graphic / overlay rows at most 8 s | PASS (plan timing only) | Every edit beat is at most 7 s. Long graphics are split into distinct planned renders with moving-picture overlay beats between full-frame graphics. Those revised renders are not yet built or accepted. |
| 4. J1310 WAV is source of truth | PASS | Plan and transcript use 837178125a72fb250d255f1039c5cb7f8630bbb313cf23801a1155f257d796e0; source WAV verified before and after rendering. v02 JSON/part hashes unchanged. |
| 5. Callback no longer than 4.20 s; no loop/stretch | PASS (scope only) | 504.30–508.48 s = 4.18 s. Retiming the opener to 3.82 s consumes another 20 ms, so the genuinely unused source interval is now 3.82–8.00 s. Trim to that interval; do not reuse 3.80–3.82. Callback media is still a labelled slate in this rough. |
| 6. Word-level overlay onsets and completed audit | FAIL | All 45 cues have an explicit transcript index, word and onset, including first-mentioned Darwin and Wallace. Seven overlapping cue pairs remain; the two barnacle cues have the same onset. Resolve to one label at a time without arbitrarily shifting a name away from its spoken onset. |
| 7. Three optional code replacements / 390 px acceptance | PASS (not adopted) | Retained all three Quality sources. No approved 390 px render exists for these proposed replacements; no savings, replacement or generation authorisation is claimed. |

## Rough pass bar and independent findings

`clip_check_v03.json`: **passed=true, errors=[], warnings=[]**. This is a technical timing result, not an editorial PASS. Independent audit: zero in-word cuts, max row 7 s, v02 unchanged, all 45 onsets point to their recorded word.

The 515.00 s, 960×540, 50 fps diagnostic rough has locked VO plus selectable planned-cue subtitles. It has **9 verified existing-render beats and 101 labelled slates**: unavailable media, revised split graphics, or a source too short. It has no score or SFX. The NAS master and six 390-pixel-per-frame phone/contact sheets are checksum-verified; exact paths and hashes are in `ROUGH_MANIFEST_v03.json`. The first phone sheet was inspected as a still: the missing-art slates and brief chapter-card treatment cannot qualify as finished-picture acceptance. No listening or moving-video perception is claimed.

Four Quality-source groups exceed their original eight-second source: P2:02 beach 8.70 s; P2:03 bagging 8.06 s; P2:11 island split 8.16 s; P5:02a Linnean reading 10.36 s. Splitting a source into two rows does not create more source footage. Reallocate cuts to usable footage or a separately reviewed free insert; never extend by freeze, loop or stretch.

The five chapter cards now fit the actual word gaps and required breath, but last only **0.32 / 0.28 / 0.56 / 0.32 / 0.28 s**. They are too brief for their titles. Resolve the chapter transition treatment against the locked VO before rendering final cards; do not silently lengthen audio or waive the breath check.

## Exact continuation

1. Replace the unsupported phrase cuts with demonstrable script punctuation / genuine clause boundaries. Permit dropping a redundant planned view rather than inventing a clause to retain every v02 shot. Keep the strict word interval and maximum-hold checks.
2. Solve source duration as a constraint across all beats sharing a source; address the four overruns above, and preserve the unused callback interval.
3. Resolve chapter-title legibility and the seven overlay collisions (see `acceptance_audit_v03.json`); merge the two barnacle cues. Recheck name onsets and one-label-at-a-time.
4. Build the five previously missing free sources and the revised graphic beats at zero credits only, after timing is stable. Optional Quality-to-code replacements remain unadopted unless their own phone sheet passes.
5. Rebuild the rough, inspect its phone sheets and report all seven checks again. Keep PR #551 open as diagnostic evidence; no merge or Ben UAT from this candidate.

## Validation

- Repository `check_all.sh`: **ALL CHECKS PASS** (including contract tests, package lint, status board, VO/atempo tests).
- Both new builders compile; `git diff --check` passes.
- Independent word-interval/duration/onset/no-generation assertions: PASS.
- Media probe: 515.000000 s, video + audio + cue subtitle streams. Full ffmpeg decode completed with exit 0 and no errors.

The rough ran detached as `J2652-rough-final`; log `~/_desk/logs/J2652-rough-final.log`, completion `~/_desk/logs/J2652-rough-final.done` = 0. Earlier attempts failed before producing the master (missing subtitle filter, then a Python environment without Pillow); the successful build uses selectable captions and the installed Pillow-enabled Python. Never restart an already-running render.
