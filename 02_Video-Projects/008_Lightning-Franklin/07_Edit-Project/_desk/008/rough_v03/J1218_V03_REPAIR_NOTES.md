# J1218 — HOS 008 diagnostic rough v03 (render in progress)

**Worker:** cursor. **No Ben Ready-for-OK.** Park for Chief after gates + evidence pack.

## Status (30 Oct ~02:19 UTC)

- `code_graphics_v02` rendered (£0): J1193 ten-FIX timing/contrast/alpha; P5:11 KEEP.
- Source correction: Bellin coords = UNVERIFIED PROPOSALS (illustrative geography only).
- Assembler `_assemble_rough_v03.py` (PR #379):
  - non-destructive NAS WORK siblings (`*_rNN`)
  - P5:10 cleaned alpha over KEEP `06_rod_fitting` (breaks 09/10/11 full-frame chain)
  - side-label suppress for baked CG headers
  - contact-sheet mid-interval labels (join)
  - part concat+VO mux on local `/tmp` then rsync (NAS ffmpeg write hang)
  - per-part polish/picture deferred; full-film gates on join
- Live: part 01 DONE (105.42 s, sha `3c1d06ec4c52…`); part 02 assembling.

## Detached run (do NOT start a second copy)

- tmux: `j1218-asm-v03`
- log: `~/_desk/logs/j1218-asm-v03.log`
- done: `~/_desk/logs/j1218-asm-v03.done` (missing = still running; then read exit code)
- WORK: `/Volumes/data/mac-mini-archive/tmp-render-scratch/j1218-hos008-rough-v03/`
- branch/PR: `cursor/j1218-hos008-rough-v03` · https://github.com/TheLaughingGod1986/history-of-science/pull/379

## Next run when `.done` present

1. exit 0 → verify master ≤540 s, sha, desk/NAS copy; episode gate; WARN motion notes; production-status + PIPELINE (008-only, no HOS005/J1223); update PR; park for Chief graphics/composite review with eleven-row dispositions.
2. non-zero → read log; fix; restart once.

## Outstanding (not claimed as PASS)

- Music `SKIPPED_NO_BED` (not PASS); SFX unfinished
- Formal J1193/J1218 elected-Chief graphics PASS
- No Ben watch / upload / privacy change
