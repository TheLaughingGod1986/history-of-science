# PART04 v19 — Flow Ultra remint (bible 43d9405)

**Status:** STOP_TO_COS — **BLOCKED_AUTH** · do **not** declare PASS · **NO PAINT** · no Ben ping

## Why

Parent FAIL `hos_002_part04_rough_v18.mp4` sha `05fb0a2b34dba1a8347ab74b2abc987fd406bef356b82b55f1a0e8ddb88cc6b5`.
UAT HARD FAIL bible `43d9405`: PUBLISH ~118–127 continuous playback horizontal ghost/jitter (**paint fallback caused it**).

Remint required **Flow Ultra real gallery mp4 only** for:

| Plate | Intent |
|---|---|
| `11_publish_gaps` | single-exposure desk · no horizontal ghost |
| `11b_wait_and_hunt` | same · grid holes |
| `06_explorer_leaves_gap` | lamp banding + garbled cards fix · KEEP back-view hair |

KEEP (assemble): plate `10` family (v18) · CLEAN LIGHT `09`/`09b` · written cards ~40.

## Scaffold landed (this branch)

- `_prep_part04_v19_start_frames.py` — publish starts from clean v18 desks; explorer start = `keep_explorer_back.jpg`
- `_mint_part04_flow_v19.py` — Flow I2V + gallery harvest · ghost/MAD reject · **no paint path**
- `_assemble_part04_rough_v19.py` — remint 06/11/11b from `v19_fast` · keep family from v18
- Refs: `04_Generated-Clips/part04/refs/v19_start_frames/` · `refs/v19_fail_keep/`

## Flow account

| Field | Value |
|---|---|
| Required | `benoats@googlemail.com` |
| Credits (phone proof) | ~**10050** (`flow_credits_benoats_googlemail.png`) |
| Forbidden | `benoats86@gmail.com` |

## Blocker (after real retries)

**BLOCKED_AUTH — passkey / 2FA for `benoats@googlemail.com`.**

1. `orbit_flow_veo_ui.py --login` on `~/.playwright-hos-flow-profile` → passkey “Verifying that it's you…” · timed out (~90s+).
2. “Try another way” → password (unknown) · phone recovery `••••• ••••69` (no agent access).
3. Chrome Default cookie rsync into Playwright profile → still Flow `/about` Sign in (OSCrypt session does not transfer).
4. Playwright MCP was logged in as **`benoats86@gmail.com` with only 50 credits** — wrong account · refused for mint.
5. AccountChooser → selected googlemail → **passkey challenge again**; waited **180s** · no phone approval.
6. Chrome `--profile-directory=Default` Flow open also hit Google sign-in (Default session not usable for Flow mint).

**Did not paint. Did not temporal-median. Did not brightness-motion paint.**
**Did not mint on benoats86 (50 credits / forbidden).**

Meta: `part04_mint_flow_v19_meta.json` → `status: BLOCKED_AUTH_PASSKEY`.

## Not delivered (blocked)

- `hos_002_part04_rough_v19.mp4`
- iCloud HOS UAT copy
- Flow job ids / plate sha256 for 06/11/11b

## CoS unblock

1. On Mini, approve passkey for `benoats@googlemail.com` on the open Google challenge **or** run:
   ```bash
   ORBIT_FLOW_PROFILE="$HOME/.playwright-hos-flow-profile" \
   ORBIT_FLOW_HOME="https://flow.google.com/u/1/" \
   python3 04_Audio/tools/orbit_flow_veo_ui.py --login
   ```
   Complete login until Flow shows googlemail + high credits (not 50).
2. Re-run:
   ```bash
   HOS_V19_MAX_CREATES=3 python3 02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/07_Edit-Project/_mint_part04_flow_v19.py
   python3 02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/07_Edit-Project/_assemble_part04_rough_v19.py
   ```
3. QA: publish contact ~118–126 continuous (no ghosts) · explorer ~50 + ~53 clean.

## Parent keepers

- v18 FAIL cut remains the current landed picture until v19 Flow lands.
- Parts 01–03 LOCKED. Scores → CoS. No Ben ping from this agent.
