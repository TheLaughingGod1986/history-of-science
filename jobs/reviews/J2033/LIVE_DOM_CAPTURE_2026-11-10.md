# J2033 Live Flow DOM Capture & Preflight Report (10 Nov 2026)

Per acting-Chief reopen instruction on `J2033` (`2026-11-09T21:54Z`):
> *"Run only with the merged runner on HOS main; first make the 2 zero-credit parent stills, then batches of <=5 rows. If the live evidence read fails closed, block with the captured DOM, do not loosen the reader."*

## 1. Summary

- **Runner**: `02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project/_mint_flow_v05_tranche2.py` on HOS `origin/main` (`97e44918`, containing merged PR #439 / #445 `02b57a1b`).
- **Reader modified?**: **No** (`_mint_flow_v05_tranche2.py` untouched).
- **Submissions / Spend**: **`0` submissions**, **`0 / 20` rows generated (`0` KEEP)**, **`0` credits spent** (`14,890 Google Flow credits` before and after; `£0`).
- **Outcome**: Both `read_live_still_evidence` (`STILL_EVIDENCE_JS`) and `read_live_evidence` (`CREATE_EVIDENCE_JS`) **fail closed** against the live configured Flow project DOM on CDP `:9222` (`https://flow.google.com/project/13d84783-a17a-495c-bacd-0cf0e736f6f4`). Full captured DOM is saved in `jobs/reviews/J2033/LIVE_DOM_CAPTURE_2026-11-10.json`.

## 2. Exact Live DOM Mismatches Causing Fail-Closed

1. **Selected model control (`models: []`) & Image model rename (`🍌 Nano Banana 2.1`)**:
   - `STILL_EVIDENCE_JS` and `CREATE_EVIDENCE_JS` only query `[aria-selected="true"],[aria-checked="true"],[aria-pressed="true"],select option:checked`.
   - In the live Flow `Settings trigger` popover, the selected model is rendered on `<button aria-haspopup="menu" aria-label="Select model family">` (with `aria-selected=null`, `aria-checked=null`, `aria-pressed=null`), whose normalized text is:
     - Image mode: `"🍌 Nano Banana 2.1 arrow_drop_down"` (and `"🍌 Nano Banana 2.1 crop_16_9 x1"` on `button[aria-label="Settings trigger"]`; Google Flow renamed `Nano Banana 2` to `🍌 Nano Banana 2.1`).
     - Video mode: `"Veo 3.1 - Quality arrow_drop_down"`.
   - As a result, `models` is always `[]` in both readers, and `REQUIRED_STILL_MODEL = "Nano Banana 2"` also mismatches `"🍌 Nano Banana 2.1"`.

2. **Selected aspect ratio radio text (`aspects: []`)**:
   - In the live `Settings trigger` popover, the selected aspect ratio radio (`<button role="radio" aria-checked="true">`) includes its Material icon ligature in `innerText`, so `text(e)` produces `"crop_16_9 16:9"` (or `"crop_9_16 9:16"`).
   - Both `STILL_EVIDENCE_JS` and `CREATE_EVIDENCE_JS` filter `selected.filter(t => t === '16:9' || t === '9:16')`, returning `aspects: []`.

3. **Credit balance label (`balances: []`) & overlay mutual exclusion**:
   - In the live `Account details` (`ULTRA`) popup, the credit balance line is **`"14,890 Google Flow credits"`** (resets on 12 Nov at 19:13), whereas `STILL_EVIDENCE_JS` and `CREATE_EVIDENCE_JS` regex-match `/(?:^|\n)\s*([\d,]+)\s+AI credits\s*(?=\n|$)/g` (`"AI credits"`), returning `balances: []` even when `Account details` is open.
   - Furthermore, the `Account details` CDK overlay and the `Settings trigger` CDK popover are mutually exclusive overlays (`cdk-overlay-backdrop`), and both `_flow_still_v01.py:select_image_16x9` and `orbit_flow_veo_ui.py` close `Settings trigger` (`Escape`) before attaching references/frames and arming the prompt. When `create_guard(page)` runs at `submit_create`, neither `Account details` nor `Settings trigger` (`"Generating will use 0 credits"` / `"Generating will use 100 credits"`) is open in the DOM, and while a CDK overlay backdrop is open it intercepts pointer events over the prompt bar.

## 3. Additional Preflight Blockers Identified

1. **`_flow_still_v01.py` hardcoded HOS 006 `STYLE_REFS` path**:
   - `live_still_maker` in `_mint_flow_v05_tranche2.py` calls `_flow_still_v01.make_still(page, prompt, dest, timeout_s=300, create_guard=create_guard)`.
   - `02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/_flow_still_v01.py` hardcodes `MEDIA_CLIPS = Path.home() / "YouTube/hos-006-trees/02_Video-Projects/006_Trees-Are-Made-Of-Air/04_Generated-Clips"`, which does not exist on the Mac mini (`attached == 0`, raising `RuntimeError("style refs not attached")`).
   - For HOS 009, the two style reference JPEGs exist locally at `/Users/benjaminoats/YouTube/hos-009-gravity/02_Video-Projects/009_The-Falling-Moon-Gravity/04_Generated-Clips/_style_refs/{04_sunny_window_v01.jpg,10_mint_jar_v01.jpg}`.

2. **Mac mini `/Volumes/data` NFS vnode hang**:
   - `require_archive` requires a writable directory under `/Volumes/...`. Currently `/Volumes/data` (`192.168.1.119:/volume1/data`) and `/Volumes/MiniWork` (disk image backed by `/Volumes/data`) block in `libsystem_kernel.dylib:__open` / `mkdir` on any uncached directory read or file create (including `nas_offload.py` PID `73678`).
