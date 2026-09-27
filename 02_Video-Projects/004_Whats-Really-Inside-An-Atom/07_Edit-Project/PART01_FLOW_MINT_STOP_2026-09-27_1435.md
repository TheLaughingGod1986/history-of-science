# HOS 004 Part 01 Flow mint — STOP (auth gate)

**When:** 27 Sep 2026 ~14:40 UK  
**Gate:** Ben — confirm Mini CDP Chrome is `benoats@googlemail.com` with ~3,492 Flow credits before minting.

## Verdict

**STOPPED. No plates minted.**

## CDP Chrome (`~/.hos-chrome-flow-benoats-googlemail-cdp` · `:9222`)

| Check | Result |
|---|---|
| Signed in as `benoats@googlemail.com` | **NO** — signed out |
| Credits ~3,492 | **Unreadable** (marketing /about pricing page) |
| Action | Launched durable tmux Chrome on `:9222`; Flow → `/about`; AccountChooser → blank Sign in |

Artifacts: `_qa_part01_mint_v01/flow_auth_credits_probe.png` · `auth_try_4.png` · `flow_auth_credits_probe_v01.json` · `auth_url_sweep_v01.json`

## Diagnostic only (not used for mint)

`~/.playwright-hos-flow-profile` is logged in as **`benoats86@gmail.com`** (FORBIDDEN for HOS Veo) with **50** daily Flow credits — not Ultra ~3,492. Did not mint from this session.

## Missing plates (still missing)

`08` · `09` · `11` · `14` · `15` · `16` · `17`

## Need from Ben

Re-auth Mini CDP Chrome as **`benoats@googlemail.com`** Ultra so Flow shows ~3,492 credits, then re-run the remint. Or say which profile/session holds the Ultra balance.
