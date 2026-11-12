# J2563 assembly checkpoint — 12 November 2026

Codex covering. Partial work only: input milestone 1/4. No row renders, timing rough, picture/edit PASS, UAT, generation, spend or publishing changes. Original v02/v03 plans and narration remain untouched.

## Saved work

- `ASSEMBLY_SOURCES_v01.json`: all 13 archive rows and 10 portrait sources, corrected under J2659 and Grok ruling 6810336587 before downloading. Includes source-plan/Scribe hashes, live licence identifiers where fetched, byte hashes, and 93 timing rows classified as 26 free builds plus 67 dependency slates. Ten portrait records are additional overlay inputs, not extra free full-frame rows.
- Twelve live Commons metadata records were fetched. Four original files downloaded: Paré instruments L0041135, Davy's Researches PDF, Gillray's 1802 etching and Long's 1849 journal PDF. Download sizes matched API metadata; both images decoded at the recorded dimensions. PDF signatures/bytes are verified; their required printed pages have NOT been located or visually checked. No archive has a finished source/visual PASS.
- `OVERLAY_CANDIDATES_v01.json`: 28 nonoverlapping candidates with exact Scribe word indices, raw Scribe indices and absolute times; 19 items explicitly held; 13 archive credit intervals with collision flags. This is a partial reconciliation artifact, not the required finished cue schedule. Chapter-card/full-frame graphic interactions and all text/layout/credit placement still need verification.
- `prepare_assembly_v01.py` preserves source precedence and supports resumable metadata/download work. It writes the corrected manifest before fetching. The initial fetch exposed two implementation issues: the default interpreter lacked Pillow and query parameters hid PDF extensions. The helper now probes images with ffprobe and parses the URL path. The initial run also continued across the list after HTTP 429; the helper now stops at the first 429 and persists a network hold. No further fetch was run after that correction.
- `overlay_candidates_v01.py` regenerates the partial cue candidates. It does not render held markers or claim listening/motion perception.

## Resume from the actual state

Working checkpoint: `/Volumes/data/studio-live/History Of Science/02_Video-Projects/011_Surgery-Before-Anaesthesia/07_Edit-Project/J2563_checkpoint_v01/`. Local recovery copy: `/Users/benjaminoats/_desk/J2563/checkpoint_v01/`. Raw external metadata stays outside git. Copy verification lists hashes of every saved file.

1. Continue independent code graphics and reconcile held overlays while the archive host is rate-limited. The existing runtime manifest deliberately refuses `--fetch` while `network_hold` is present. Reassess that hold in a later run; respect the host's Retry-After guidance. Do not bypass it through mirrors or silently replace approved sources. The missing archive/portrait files are still missing.
2. Reconcile the visual prose, preserving narration: Liston's first spoken name is **371.48 s**, so the planned 14.28 s WHO card moves to that mention. Snow's name starts **431.099 s**, in the following archive row rather than P5:06b; its portrait credit and archive credit must not collide. Several planned FACT/WHEN details are sourced annotations absent from the spoken words; their reveal times need an explicit decision, not a fabricated word anchor. The stadium evidence continues across the 465.74 s cut. The E2 experiment is not approved for 011.
3. Locate and verify the exact Davy/Long/other printed pages before any page-based render. Complete source/credit checks and portrait credits from actual metadata. Reconcile the Morton replica and Squire-copy wording in assembly only; inherited v03 source descriptions are not authority.
4. Build all 26 free rows, the full word-timed overlay schedule and the 535.30 s internal rough against the locked WAV. Keep all 66 generation rows and P5:16b as labelled slates. No generation is authorized. For P5:16b, 6.61 + 4.52 = 11.13 s required for disjoint use; a hypothetical 8 s file would overlap by 3.13 s. No actual source file or interval was assessed, and the reuse finding remains a dependency.
5. Verify rendered coverage/durations/hashes/word boundaries/overlay timing, then request a reviewer with demonstrated moving-video input and demonstrated audio input for the corresponding assessments. This session demonstrated neither; no film-stage approval or Ben watch copy exists.

## Verification

```text
PASS: mechanical retime validation — 93 contiguous rows, 92 word-safe boundaries; 18 word crossings removed; all 11 long sentences split; maximum 8.00 s; v02 source, VO lock, row identities, budgets and generation locks preserved.
This is a data validation result, not film-stage approval or listening/motion QA.
```

Three focused tests passed: 23-source/93-row precedence and slate counts, stop-on-first-429, and candidate/raw word-index plus nonoverlap consistency. `check_all.sh` passed before the board checkpoint update; rerun after it is recorded in `J2563_CHECKS_v01.txt`. No additional actual-media review is implied.

Nothing needed from Ben. Remaining work exceeds one short worker run; the job is released at this reviewable checkpoint, not marked done.
