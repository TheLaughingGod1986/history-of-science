# Part 02 Flow credit / harvest notes (4 Sep 2026)

## Account
- Use `benoats@googlemail.com` on `https://flow.google.com/u/1/` (AI credits fallback).
- `benoats86@gmail.com` is Flow-credit-only and hits usage limits — do not mint there.

## Harvest (Agent UI)
- Agent UI does **not** emit `getMediaUrlRedirect` ids after 100%.
- Working path: play gallery `/asb/` thumb → capture mp4 via `page.expect_response` (googlevideo).
- Do **not** call `resp.body()` on googlevideo in a global response listener (crashes Chrome).
- Do **not** use UI Download on Agent (often closes the page/context).
- Force outputs **x1** before Create (pill often defaults to x2).

## Status
- Plate 01: salvaged chapter card (text QA for Ben).
- Plate 02: salvaged lavoisier-list-like desk plate.
- Remaining plates: remint with harvest fix; stop after Part 02 rough for Ben UAT.
