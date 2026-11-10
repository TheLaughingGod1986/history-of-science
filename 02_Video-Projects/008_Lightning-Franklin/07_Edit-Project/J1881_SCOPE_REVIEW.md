# J1881 — correction recipe review: FIX / production held

Codex, elected acting Chief, 4 November 2026. Review target: HOS PR409, exact head `bd5302494c7337058426b2d8714fa4cf4c90efa9`. This is a code/evidence scope decision, not a moving-picture or listening PASS. No replacement render or generation authorized.

## Current request and locks

Live checks API still reports `HOS-008`, `v03`, verdict `change`, original timestamp `2026-11-03T16:08:33.439Z`, J1297, all six original notes unchanged. `handled=true` means tracked, not resolved. Original notes remain in J1868_BEN_REVIEW_v03.json.

Original h22 (desk6533306017) and h35 (desk6537320070) were read directly. Local master rehashed: `cf1561c218bace7bc14ed3d625b0790a457027a90f392262f45ca7172723099b`, 393139693 bytes. ffprobe:24fps,12923 frames, video start0.125s, duration539.500s. h35 records -14.129LUFS/-1.2dBTP and measured zero VO offset; those are historical measurements, not evidence for a future v04.

## Blocking findings

1. **Picture preservation and timing:** `extract_unchanged_range` re-encodes every unchanged interval with libx264 CRF17 and `setpts=N/(24*TB)`. The future output therefore cannot claim unchanged decoded-frame identity and does not preserve source timestamps. 12923/24=538.4583 seconds, versus measured video duration539.500 seconds. Full decoded-frame ffprobe confirmed12923 frames, first PTS0.125, last PTS539.583333 and24 non-24fps gaps (23 gaps of1/12s and one of0.125s). Examples: index744 goes31.083333→31.166667; index5069 goes211.625→211.750. Original start0.125s and nonuniform source timing must be retained, not replaced by a new CFR clock while copying old audio. Restrict re-encoding to declared patch/GOP-boundary windows and verify all unchanged decoded frames.
2. **Dry-run is not verification:** `verify_plan` only asserts file existence and interval arithmetic, then returns `vo_sync_lag_ms:0.0` and `frame_count_delta:0`. It checks no input hashes, decoded timestamps, sync or finished output. Report these as planned/unmeasured. Enforce hashes and exact source availability; fail on short decode, never repeat the last frame or insert a blank one. Refuse overwrite/missing requested retake instead of silently substituting.
3. **Conflicting evidence:** recipe rough-v12 hash02db759e... differs from h22/h35 d032e5fb...; reconcile actual copies without asserting equivalence. Inventory mix -15.32/-1.00 differs from h35 -14.129/-1.2. Earlier and later cut clocks also differ: resolve from actual master PTS and master-derived words.
4. **Teaching design:** proposed bordered pills/banner, simultaneous city/year/distance labels and `3,600 MILES ACROSS THE ATLANTIC` do not establish HOS one-label house compliance or sourced facts. Remove the new unsourced distance; use a single clear animated crossing idea, with sourced location/date only when needed. Do not rewrite locked VO. Note1's long caption should become brief sequential labels if the actual spoken timing supports them.
5. **Missing exact-match assets:** native options for1:49 and7:58 explicitly omit the tube/hair interaction and ship mast respectively. They are not approved substitutes. Preserve the existing three-candidate search budget; do not reset it. Carry bounded Flow/Veo retake proposals back to Chief after recipe repair; fragile spark requires Quality. No generation credit is authorized here.

## Six-note disposition

| Original note time | Decision |
|---|---|
|00:20|Conditional backed house text over original moving plate; repair label count/style and verify phone readability. Candidate frames427–544 require PTS reconciliation.|
|0:30|Conditional removal of four-frame flash; reconcile declared changed744–839 with code663–839, preserve clean frames and sentence pause.|
|1:49|Exact-match native asset missing; reject silent OptionA substitution. Carry Quality Flow retake proposal, maximum3 takes/300 subscription credits, to a separate Chief scope; fresh balance required, no spend now.|
|2:20|Conditional keep3168–3259 and replace3260–3343 using11_jar_crack_t1.mp4 at4.000–7.500s, after PTS/KEEP/reuse checks; preserve next spark and audio.|
|3:31|Redesign one understandable crossing over moving07_slow_news_t1.mp4; replace full4977–5077 slot only after timing reconciliation; no new unsourced distance, no multiple-label UI banner.|
|7:58|Exact-match ship-mast asset missing; reject silent roofs-only OptionA. Carry bounded Flow/Veo proposal with reference/hash and live rate/balance to separate Chief scope, no spend now.|

## Tracked next action and concrete hold

**J2163** is ready now, kind assembly, HOS008 edit, ordinary assembly fallback chain (Cursor/Grok → Cursor Auto → Codex → Gemini). It repairs the recipe/code and evidence, with small synthetic timing/short-decode/hash/overwrite tests only. Its full brief is in the shared queue. It does not render a replacement film, generate assets, spend credits or publish anything.

**J1881 stays held at2/3** on delivery of J2163's corrected six-row recipe, truthful dry-run and tests. Elected Chief resumes scope immediately when that input is ready; the check time is a condition verification, not a production start date. Do not add a second production execution job before the existing recipe is safe. After repair, Chief must explicitly choose missing-asset scope, queue generation if justified, new-version assembly, and dependent capable QA. All original picture/polish/music/SFX/episode/lint gates, VO timing, full-cut and six-window/adjacent-cut review, unchanged-window verification, phone readability, Chief media decision and Ben's finished-film watch remain required.

Capability register inspected: Codex has no demonstrated audio/moving-video input. Gemini's latest entry expired23:25:39Z and says only that read_file supports media; it is not fresh demonstrated perception. J1880's native-perception claims are retained as attributed worker findings, not independently confirmed. A future media reviewer must supply an actual current probe before assignment; no final review is assigned on the expired entry.

J1297 and every historical master/rough remain preserved. All six notes unresolved. J1755's automatic-publication rejection remains separate; no R2, watch-object, YouTube, schedule, listing or privacy changes. No milestone inferred complete from a master. GBP0; no credit spent.

NAS offload prerequisite ran detached and exited0: waits for01:00–06:00 window with8828MB free; nothing moved or deleted. Logs: `~/_desk/logs/j1881-offload.log`; exit marker `~/_desk/logs/j1881-offload.done`.

Validation of review records (not media): `bash 00_Brand/Channel-Setup/tools/check_all.sh` output: **ALL CHECKS PASS**. `git diff --check` passed.
