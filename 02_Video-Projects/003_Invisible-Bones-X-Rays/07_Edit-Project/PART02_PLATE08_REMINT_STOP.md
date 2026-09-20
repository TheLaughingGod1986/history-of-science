# HOS 003 Part 02 — plate 08 remint STOP

**From:** Cursor (mac-mini) · 20 Sep 2026 ~23:15 London  
**Ben:** FAIL remint for `08_locks_the_door` (bolt through strike plate).  
**Account lock:** `benoats@googlemail.com` · do **not** use `benoats86@gmail.com`.

## Ben FAIL (confirmed on Mini)

Old fail **kept**: `04_Generated-Clips/part02/08_locks_the_door_v01.mp4`  
- 8.000 s · 2025949 B  
- sha256 `27849d3f946bcb78c99aa314b80911ed58f1a303737bdeceee12170f48816107`

Clearest clip: **~5.5 s** — cylindrical iron bolt shaft passes through the **solid** decorative strike plate on the jamb (mesh intersection). ~2.5 s also shows the latch plate floating over the door-gap glow. HARD FAIL. Do not overwrite v01.

## Flow — STOP (no Create)

This run did **not** mint `08_locks_the_door_v02.mp4`. Assemble v02 was **not** run.

| Probe | Result |
|---|---|
| Playwright `~/.playwright-owb-flow-benoats-googlemail` | Bounced to `flow.google.com/about` — **not logged in** (same as plate 11 probe2) |
| Playwright `~/.playwright-hos-flow-profile` | Earlier plate 11 false-positive reCAPTCHA footer; not this account lock |
| Chrome Default (`--user-data-dir` real Chrome · launched for Batch B) | CDP **9334 not listening**. Visible Chrome tab is Google Account **Recent security activity** (`myaccount.google.com/notifications?origin=3&utm_source=sign_in_no_continue`) |
| Plate 11 same-evening quote | `You're not signed in. Your session ended because there was no activity. Try signing in again.` Account chooser showed `benoats86@gmail.com` Signed out — **did not click** |

No charge-loop. No account switch. No Ken Burns substitute.

## Ready when Flow is re-authed on `benoats@googlemail.com`

1. Remint only (Quality · 8s · 16:9 · Batch B project `95929b6f-…`):  
   `07_Edit-Project/_remint_part02_plate08_locks_the_door.py`  
   `--probe-only` first. Then one Create → `08_locks_the_door_v02.mp4`.  
   QA start/mid/end: bolt must enter the strike-plate **hole**, not through solid metal. If still clips, `--version v03` once, then stop.
2. After plate PASS:  
   `07_Edit-Project/_assemble_part02_rough_v02.py`  
   Same v01 pipeline (VO txt sha `f3454130…`, ward bed 0.34, labels, plates 02/04–07/**08 v02**/09–11). Lands `09_Final-Export/hos_003_part02_rough_v02.mp4` + iCloud `HOS UAT`.

## Do not

- Overwrite `08_locks_the_door_v01.mp4`
- Assemble v02 from clipped v01
- Sign in as `benoats86`
- Ping Ben
