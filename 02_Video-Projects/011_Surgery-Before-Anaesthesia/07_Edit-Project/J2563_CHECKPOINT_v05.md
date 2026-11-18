# J2563 archive recovery checkpoint v05 — 12 November 2026

Codex covering. Continued existing PR #560 from its saved v04 checkpoint. This run recovered two additional approved originals and identified three printed pages. No new row renders, rough, generation, credits, narration edits, uploads, scheduling, film-stage approval or UAT. The existing four-milestone plan remains 1/4.

## Delivered

`ARCHIVE_RECOVERY_v05.json` records six original source hashes, licences, approved URLs and credit strings; the previous four originals are preserved. Newly recovered: Morton inhaler replica L0018234 (4006×2920, CC BY 4.0) and the Southworth & Hawes Google Art Project scan (4147×3280, public domain). The replica is circa 1945, not an 1846 engraving. All source bytes matched existing metadata sizes and decoded dimensions.

Printed-page identification from the cached PDFs:

- Davy: PDF page 584 of 616, printed page 556. The physical-pain/surgical-operations paragraph is present and visually inspected. Source OCR uses historic spelling and is not quote authority.
- Long: PDF page 711 of 780, December 1849 issue heading and the article start. The March 1842 operation reference is on this page. No printed folio is visible on this opening page, so its record deliberately leaves the folio null rather than inferring it from the next page.
- Long: PDF page 712, printed page 706, article continuation. These are source inputs for the composite, not a claim that the article was published in 1842.

Three high-resolution page extracts and their extracted text carry original PDF and output hashes. Source images/page layouts inspected in stills only. No audio or motion review. The Gillray original includes calibration bars that must be cropped before any use; it is an 1802 scene, not the own-drawn 1844 broadside. That composite remains unbuilt.

Media/evidence delivery: `/Volumes/data/studio-live/History Of Science/02_Video-Projects/011_Surgery-Before-Anaesthesia/07_Edit-Project/J2563_archive_recovery_v05/`. `pages/` holds the extracted pages and manifest; `source_cache/` preserves the original cache, recovered files and raw metadata; `COPY_VERIFICATION_v05.json` verifies every copied file. Raw external metadata remains outside git. Local recovery is on the scratch SSD, not only in temporary storage.

## Network and next work

A bounded later-run probe of the approved Morton original returned HTTP 200 without Retry-After. Downloading resumed from the saved source precedence. After recovering Morton and Ether Dome, the Ether Monument request returned HTTP 429; the fetcher stopped immediately and persisted the network hold. No mirrors, replacement sources or further requests were attempted. Missing archive and portrait sources remain missing. A later worker must inspect the saved hold before a separately bounded retry; do not repeatedly retry in the same run.

Continue all 13 archive composites, full overlay reconciliation and the rough. Preliminary graphics in v03/v04 still need their recorded editorial/readability decisions. No re-render or source-plan edit has been made here. P5:16b remains a dependency slate: no actual P1:07b source exists for interval verification; the hypothetical eight-second source would need 11.13 s for disjoint uses and therefore overlaps by 3.13 s.

Remaining assembly exceeds a short run. Released at this clean source checkpoint, not marked done. No request for Ben.

## Mechanical verification

PASS: six cached source hashes match; three identified PDF pages extracted with source hashes, one-based page numbers and visible folios where present. Source recovery only; no film-stage PASS.

PASS: NAS copy — all 27 files matched SHA-256.

Required `check_all.sh`: ALL CHECKS PASS (durable handoffs, no media, status sync, ElevenLabs guards, VO word checks, speed rules, contract tests and package lint). Initial run could not write the shared npm cache; final run used an isolated scratch cache and the installed project dependencies.
