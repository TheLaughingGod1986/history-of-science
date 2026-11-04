# J1868 — Franklin v03 UAT correction intake

Codex, elected acting Chief, 3 November 2026. **Triage only; all six notes remain unresolved.**

## Original review and evidence

Live `/api/checks` read confirmed HOS-008, v03, verdict `change`, at `2026-11-03T16:08:33.439Z`, original watch job J1297. Exact review saved in `J1868_BEN_REVIEW_v03.json`; no newer review or duplicate correction job was found. No media was reviewed or changed in this triage.

- [Chief h22 picture lock](https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6533306017): rough v12; not a finished-film approval.
- [Chief h35 master approval](https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6537320070): master v03, SHA256 `cf1561c218bace7bc14ed3d625b0790a457027a90f392262f45ca7172723099b`, 393139693 bytes, 539.626 seconds. These historical approvals are preserved; they do not resolve the new notes.
- J1297 completed UAT delivery; HOS PR391 is merged. Main pipeline still carried older picture/edit labels. Undocumented milestones are not made complete from the existence of the master.
- J1755 remains blocked at 2/3: restored UAT hash verified previously, browser playback media returned 403. Automatic approval review rejected replacement watch-object publication under its no-upload brief. PR401 is still open. Its delivery scope and restrictions remain separate from this correction intake. This record supersedes its pending-watch wording for the current six-note review; it does not dispose of PR401 or authorize publication.

## Correction scope

| Ben time (unchanged) | Ben note (verbatim) | Required outcome / acceptance |
|---|---|---|
| 00:20 | text on screen in readable needs maybe background colour | Readable white Didot italic with compliant contrast/background over moving picture, clear of the subject; check at phone size. |
| 0:30 | flash the next scene | Locate the unintended adjacent-scene flash and specify a clean boundary; no clipped spoken word, frozen filler or timing drift. |
| 1:49 | strange behaviour as hair flies out the tube | Locate the hair/tube artefact; select approved native motion supporting the locked line, or identify a missing asset for separately scoped generation. |
| 2:20 | strange behaviour with the silver foil | Locate the foil artefact and specify physically coherent approved motion supporting the line; no misleading composite or still workaround. |
| 3:31 | the diagram/ map is not easy to understand | Simplify our own animated map/diagram to one idea matching the spoken line; sourced geometry/labels and HOS styling, readable without sound. |
| 7:58 | the rods fall down for some reason | Locate the falling-rod artefact; retain believable anchored rods through the full interval and transitions, using approved motion or a separately scoped asset. |

These are Ben’s observations. Exact source rows, intervals, spoken lines and independently reproduced failures are for J1880 to establish; this intake does not invent those findings.

## Actionable handoffs

- **J1880 — assembly capability chain:** Cursor/Grok, Cursor Auto, Codex, Gemini according to availability. Ready now; due 4 Nov 12:00 London (deadline, not a delayed start). Map all six notes to master/cuts/source/VO and prepare an exact new-version edit recipe or code diff plus six acceptance checks. No replacement render, generation or credit spend. Inspect approved alternative native motion first; bound any missing-input search to 20 active minutes / three candidates, shared across retries. Preserve original files and locked VO/music/sync.
- **J1881 — elected Chief, after J1880:** due 4 Nov 14:00 London. Review the concrete recipe and missing-input evidence; queue separately scoped correction assembly and capable media QA jobs, or record a specific input hold. Any generation requires an explicit bounded HOS route/takes/cap and fresh balance checks. No authority to render or publish is conferred by this planning job.
- **J1755 — separate delivery owner:** existing hold and publication rejection stay in force. No R2 upload, YouTube action, schedule change or bypass here.

Intake acknowledgment through the existing checks API may mark the request handled **only as tracked** after these queue jobs and records exist. Retain original version/verdict/notes/timestamp. No note is marked resolved; no media PASS or Ben approval is claimed. Corrected media still requires all original gates, capable review and Ben’s finished-film watch.

## Validation

Record-only change. Repository check output is recorded in production-status.md.
