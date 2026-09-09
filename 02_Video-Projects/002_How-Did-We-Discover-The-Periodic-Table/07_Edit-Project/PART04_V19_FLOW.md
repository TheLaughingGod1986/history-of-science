# PART04 v19 — Flow Ultra remint (bible 43d9405)

**Status:** `STOP_TO_COS` · **BLOCKED_AUTH** · do **not** declare PASS · **NO PAINT** · no Ben ping

## Resume (this turn)

Ben: Flow is **NOT blocked** now. Re-verified login on **`benoats@googlemail.com`** (NOT `benoats86@gmail.com` @ ~50 credits).

**Result:** passkey challenge still blocks googlemail (`Verifying it's you…` / `Complete sign-in using your passkey`).

**Action:** **STOP_TO_COS BLOCKED_AUTH only.** Did not paint. Did not temporal-median. Did not brightness-motion. Did not mint on the 50-credit account.

Evidence:
- `07_Edit-Project/_qa_part04_v19_auth/flow_googlemail_passkey_blocker_RESUME.png`
- `07_Edit-Project/_qa_part04_v19_auth/STOP_TO_COS_BLOCKED_AUTH.json`
- Meta: `part04_mint_flow_v19_meta.json` → `status: STOP_TO_COS_BLOCKED_AUTH`

## Why (parent FAIL)

Parent FAIL `hos_002_part04_rough_v18.mp4` sha `05fb0a2b34dba1a8347ab74b2abc987fd406bef356b82b55f1a0e8ddb88cc6b5`.
UAT HARD FAIL bible `43d9405`: PUBLISH continuous playback horizontal ghost/jitter (paint fallback caused it).

Remint required **Flow Ultra real gallery mp4 only** for:

| Plate | Intent |
|---|---|
| `11_publish_gaps` | single-exposure desk · no horizontal ghost |
| `11b_wait_and_hunt` | same · grid holes |
| `06_explorer_leaves_gap` | lamp banding + garbled cards fix · KEEP back-view hair |

KEEP (assemble): plate `10` · CLEAN LIGHT `09`/`09b` · written cards ~40.

## Scaffold ready (reuse when auth clears)

- `_prep_part04_v19_start_frames.py` + starts under `04_Generated-Clips/part04/refs/v19_start_frames/`
- `_mint_part04_flow_v19.py` — Flow I2V + gallery harvest · ghost/MAD reject · **no paint path**
- `_assemble_part04_rough_v19.py` — remint 06/11/11b from `v19_fast` · keep family from v18

## CoS unblock

1. On Mini, approve passkey for `benoats@googlemail.com` until Flow shows googlemail + ~10050 credits (not 50).
2. Re-run:
   ```bash
   HOS_V19_MAX_CREATES=3 python3 02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/07_Edit-Project/_mint_part04_flow_v19.py
   python3 02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/07_Edit-Project/_assemble_part04_rough_v19.py
   ```
3. QA: publish mid-plate ≥5 frames continuous (no ghosts) · explorer ~46–53 lamp/cards clean · scalp blot stays cleared.

## Not delivered (blocked)

- `hos_002_part04_rough_v19.mp4`
- iCloud HOS UAT copy
- Flow job ids / plate sha256 for 06/11/11b

Parts 01–03 LOCKED. Scores → CoS. No Ben ping from this agent.
