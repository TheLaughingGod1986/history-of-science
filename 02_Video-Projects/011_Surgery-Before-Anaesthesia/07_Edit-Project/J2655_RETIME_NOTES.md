# J2655 — v03 retime evidence

Draft implementation of Grok’s 11 Nov 22:17Z ruling; Chief retains approval. No listening or motion review was performed. Tracked Scribe intervals are evidence of the proposed cuts, not proof of audible silence. A gap can be only tens of milliseconds. Audio and script bytes remain unchanged.

Inputs: verified Mini WAV SHA-256 `d873f1d0c9158087fd61ce0b9f53de985055d778cd58b8df70c67c0701300ae2`, 532.720 s. J2653 records its restored studio-live copy. Use `stt_raw.json` for individual words: despite its name, `words.srt` groups several words into subtitles and cannot resolve these boundaries. All 92 internal boundaries, including unchanged ones, are in `RETIME_AUDIT_v03.json`.

Selection: move word-crossing cuts to a nearby gap, preferring punctuation/clause joins; preserve already usable gaps. Move tight units together (Europe and America, in Bristol, room full of doubters, country doctor, within weeks, and the December 1846 date). For all eleven >8 s sentences choose the nearest meaningful clause join to the temporal midpoint. Neighbouring cuts move where necessary to keep every row at most 8 s. No rows, sources, budget or generation permissions are added.

Constraint propagation worth reviewing:

- P2:05b moves to 125.76 (stage / and). To avoid its former 9.14 s successor, P2:06a moves to 133.30 (parties / something), P2:07a to 139.52 (and / not), and P2:07b to 147.50 (noticed / In). The 139.52 gap is the constrained compromise before “not feel”; the conjunction remains on the preceding picture. It is not a noun-phrase split.
- Moving P3:06a to 226.68 (1846 / Morton) requires P3:05b at 218.70, P3:05a at 210.70 and P3:04b at 202.74. The last is the nearby wasn’t / enough gap, keeping each neighbour ≤8 s.
- P5:07a moves to 429.63 after “1853,”, the nearest comma/clause join to the midpoint; P5:07b moves to 437.60 after “Leopold.” so the archive row is 7.97 s.
- P5:12a moves to 486.81 before “so”, closer to the midpoint than the earlier breath / and join.
- P5:13b moves back to 497.05 before “Once”; P5:14a is 502.55 (care / and), preventing a split of “patient slept” while retaining the nearest midpoint clause join.

## All moved boundaries

| Next row | v02 s | v03 s | Gap / join at v03 |
|---|---:|---:|---|
| P1:02a | 6.90 | 6.34 | Why? / Because |
| P1:02b | 10.50 | 10.98 | America, / nobody |
| P1:03b | 18.50 | 18.62 | him / with |
| P1:04b_cg_stopwatch_scale | 26.50 | 26.78 | 1846, / all |
| P1:05a | 30.70 | 29.10 | changed. / In |
| P1:07b | 53.60 | 52.89 | doctor, / and |
| P1:09c | 82.60 | 81.68 | centuries, / and |
| P2:02a | 88.90 | 89.77 | Bristol, / a |
| P2:05b | 127.60 | 125.76 | stage, / and |
| P2:06a | 134.90 | 133.30 | parties, / something |
| P2:07a | 141.90 | 139.52 | and / not |
| P2:07b_cg_timeline_42yr | 148.30 | 147.50 | noticed. / In |
| P2:10a | 170.50 | 173.13 | quietly, / who |
| P3:02a | 177.80 | 178.08 | Connecticut, / a |
| P3:04b | 202.50 | 202.74 | wasn't / enough, |
| P3:05a | 209.92 | 210.70 | fake. / But |
| P3:05b | 216.20 | 218.70 | idea. / He |
| P3:06a | 223.80 | 226.68 | 1846, / Morton |
| P3:06b | 231.20 | 231.89 | globe. / A |
| P3:07a | 238.20 | 238.97 | mouth, / and |
| P3:10a | 264.80 | 263.97 | Dome, / and |
| P4:02a | 274.00 | 275.46 | away. / He |
| P4:03a_arch_letheon_patent | 285.80 | 285.86 | stories / that |
| P4:05b | 320.00 | 319.50 | first. / His |
| P4:06a_cg_master_timeline | 326.50 | 326.94 | Wells / said |
| P4:07b | 338.20 | 339.25 | courtrooms, / and |
| P5:02a | 368.40 | 371.03 | London, / Robert |
| P5:03a_arch_squire_inhaler_1846 | 381.20 | 379.84 | woke, / he |
| P5:03b | 388.40 | 387.80 | delighted. / He |
| P5:05b | 416.20 | 415.48 | table, / and |
| P5:07a_arch_snow_chloroform_1858 | 433.80 | 429.63 | 1853, / a |
| P5:07b | 438.72 | 437.60 | Leopold. / If |
| P5:10a | 466.50 | 465.74 | people / all |
| P5:11a | 474.00 | 473.60 | anesthetic. / That's |
| P5:12a_cg_anesthetist_monitor | 485.80 | 486.81 | medicine / so |
| P5:13b | 498.00 | 497.05 | be. / Once |
| P5:14a | 504.20 | 502.55 | care, / and |

## Eleven long sentences

| Sentence interval | Midpoint | v03 split | Join |
|---|---:|---:|---|
| 48.28–58.82 | 53.55 | 52.89 | doctor, / and |
| 78.66–86.78 | 82.72 | 81.68 | centuries, / and |
| 122.12–130.94 | 126.53 | 125.76 | stage, / and |
| 223.50–231.60 | 227.55 | 226.68 | 1846, / Morton |
| 281.36–289.64 | 285.50 | 285.86 | stories / that |
| 305.90–314.16 | 310.03 | 309.20 | pain, / anesthesia, |
| 409.94–419.56 | 414.75 | 415.48 | table, / and |
| 427.08–437.52 | 432.30 | 429.63 | 1853, / a |
| 452.72–461.22 | 456.97 | 458.50 | rare, / about |
| 481.62–490.22 | 485.92 | 486.81 | medicine / so |
| 497.60–506.38 | 501.99 | 502.55 | care, / and |

## Scope and handoff

P4:08a changes “Victorian” to “mid-1840s” only in visual and prompt. Row VO excerpts are rebuilt from unchanged tracked word tokens so they follow the new intervals; these are references, not new spoken lines. v01/v02 files and part boards remain byte-for-byte unchanged. Assemble explicitly from v03; older per-part v01 boards are not retimed copies.

The inherited v02 opening experiment metadata is labelled unapproved rather than copying its PASS into v03. The standing E2 experiment applies only to 008–010. Opening design, text-to-picture fit, name/overlay reveals, archive implementation (J2654), and timing-sensitive visual prose still require the normal picture/Chief review. No word-accurate overlay schedule or finished render is delivered by this job.

The reused P1:07b source remains unmade; its inherited P5:16b slice is not certified unused by this retime. A render must verify available source duration and reuse intervals. No new spend, render, generation permission, film-stage PASS or UAT handoff.

Next: Chief reviews v03 and these mechanical timing choices, then the existing free-row assembly work can use the restored WAV and corrected archive brief.
