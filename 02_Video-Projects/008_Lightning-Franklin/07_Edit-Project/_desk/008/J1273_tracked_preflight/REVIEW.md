# J1273 — tracked rod preflight for Chief review

Codex covering as specialist worker, 30 October 2026. Candidate only; no film/stage approval. J1267 stays held at 2/6. No full master was rendered, no upload, no credit spend.

## Candidate and checks

Durable candidate directory: `/Users/benjaminoats/_desk/j1273-candidate-v08/`.
- `code_graphic_008_p5_10_metal_easy_v08.mov`: 1920×1080 alpha, 42 frames, 24 fps, 1.750 seconds.
- `composite_v08.mp4`: 1920×1080, exactly source frames 109–150 inclusive, in order at 24 fps. Same prescribed grade; no source transformation beyond the pre-existing scale/grade. No freeze, replay, interpolation, alternate plate or master splice.
- `workman_42f_24fps.mp4`; `all_frames_00.jpg`, `all_frames_14.jpg`, `all_frames_28.jpg`: all 42 source/candidate workman crops.
- Full-size `p10_frame05.png`, `p25_frame11.png`, `p50_frame21.png`, `p75_frame32.png`, `p90_frame38.png`.
- `TRACKING.json` gives all per-frame control points; `OFFSETS.json` records actual encoded-alpha centres separately from source rod measurements. `MEDIA_MANIFEST.json` in this evidence folder hashes every retained artifact, including failed v07.

Required sample offsets (rod minus rendered trace, px):

| Sample | Row frame | Source frame | Rod x | Rendered trace x at y282 | Offset |
|---|---:|---:|---:|---:|---:|
| p10 | 5 | 114 | 1187 | 1191.5 | -4.5 |
| p25 | 11 | 120 | 1145.5 | 1156.5 | -11.0 |
| p50 | 21 | 130 | 1178 | 1174.5 | +3.5 |
| p75 | 32 | 141 | 1198 | 1197.5 | +0.5 |
| p90 | 38 | 147 | 1198 | 1196.5 | +1.5 |

All five are within the unchanged 19.2 px (1%) limit. Across all measurable frames the worst tip offset is 14.5 px at row frame 13; exposed lower-shaft samples at y520/650/800/920 have maximum measured offset 6.5 px. Frame 0 has no callout by the locked animation and is reported unavailable, not zero. Early unfinished parts of the callout also remain unavailable. Source and rendered frames use the same exact indices; percentile indices use ceil(42*pct/100). The unchanged `tip_offset` function is loaded from the archived v08 renderer; `trace_x` comes only from decoded alpha pixels at y282, never from `rod_x`. Grayscale is converted from the exact extracted source PNG, so half-pixel medians may differ slightly from the earlier seek-based probes.

Tool outputs, unchanged gate code and thresholds:

```
polish gate PASS: 0 of 1 rows failed, 0 to look at
picture QA PASS: 0 of 1 cuts fail, 1 to look at
WARN: kind of picture: no title in the pool, so nobody can tell what it is
```

This is row-only QA, not full-film QA. The picture warning is retained for Chief; the composite is the approved Flow plate with our own code overlay. All five exact-frame seam checks found no vertical seam. Gate and detector hashes are recorded. No checker was edited.

## Motion and occlusion review

Worker inspected all 42 source/candidate crops and the five full-size samples. No hammer appears in this selected window. The upper rod flexes/moves relative to the lower shaft in the source; the overlay follows that movement rather than translating a single vertical line. The largest adjacent rendered start-point move is 7 px. No large bracket-induced zigzag remains in the revised candidate. Chief should judge the 24 fps strip for residual small tracking jitter and the source prop motion; this note grants no approval.

Hands obscure roughly y270–350 and y420–480; a wall bracket/shadow also contaminates the y380 region. The overlay bridges the exposed y180 and y520 control points, then follows independently measured lower-shaft points. It continues across the hands as the original teaching overlay did; no source pixels are patched and hidden rod positions are not claimed as directly measured. Measurements at visible y520/650/800/920 are provided; the hand/bracket region requires visual judgement.

Timing/art remain: gold callout full at frame 3 (0.125s); trace begins on the first representable frame after 0.30s, frame 8 (0.333s), reaches the foot at frame 36 (1.50s); anchored METAL CONDUCTS full by frame 12 (0.50s), held through frame 41, no fade-out. Decoded label region is byte-identical for frames 12–41. House colours, Didot italic, rings, width and label anchor retained. Original source and locked bb821f40 alpha hashes verified unchanged.

First worker attempt v07 is retained in `/Users/benjaminoats/_desk/j1273-candidate-v07/`; its bracket-shadow control point caused a visible kink and p25 -20.5 px. `FAILED_v07_OFFSETS.json` records that failure. Original failed v06 and all prior assets were left untouched.

## Delivery code safety

`_build_rough_v09.py` no longer removes destination trees. Delivery uses new `rough_v09_delivery` folders and copy-only SHA-256 verification. Identical retries are accepted; conflicting existing files raise without overwriting. Evidence commits require a clean caller worktree and a fresh evidence directory; the automatic forced branch reset was removed. Focused checks exercised a new copy, identical retry, and conflicting destination refusal, confirming the original destination contents survived. No old full-render/delivery entrypoint was executed.

## Reproduction and next step

Use Python with numpy and Pillow (`/opt/homebrew/opt/python@3.14/bin/python3.14` on this Mini). In the edit directory, set `J1273_OUT` to a NEW directory and run `_preflight_j1273.py extract`, then `build`, then `verify`. Extraction requires NAS/source access. Render refuses existing output files. The exact source is pinned in VALIDATION.json; controls and measurements are retained separately.

Chief reviews this prerequisite and its warning/occlusions. Only acceptance permits resuming J1267 at its existing 2/6. Later assembly still must verify exact original PTS, preserve the 157-frame displayed safe-path body plus 29-frame lead-in (186 total), end boundary, 12923 total frames, original pause trim, VO, unchanged rows and h14 frame diffs/full gates. None of those later assembly checks is claimed here. Ben action: none.

Repository validation: `check_all.sh` completed with ALL CHECKS PASS (36 contract/guard/word tests, status sync, no-media check and package lint). Existing package warnings are preserved in `check_all.log`. Python compilation and `git diff --check` succeeded.
