# Part 02 ward v04 — STOP (2026-08-28 HOS Cloud)

## Checkout

- Fresh clone of `https://github.com/TheLaughingGod1986/history-of-science` at `origin/main`
- SHA: `b45d2455f31749f7142201866a89a9fc265427ca` (*Lock HOS first, then compare Omni*)
- New branch from main only: `cursor/hos-001-part02-ward-v04-a06c`
- Did **not** reuse Mini/Pro trees or leftover `cursor/hos-001-part02-*` branches as base

## Job

Remint only `08_ward_vs_lens` → splice 0:53–1:01 of `hos_001_part02_rough_v01.mp4` → `hos_001_part02_rough_v04.mp4`.

## Result: **STOPPED — no Veo API path**

| Check | Status |
|---|---|
| `GEMINI_API_KEY` / `GOOGLE_API_KEY` on this VM | **MISSING** |
| Veo API probe | cannot run without key |
| Prior HOS cloud run (same prepaid pot) | **429 RESOURCE_EXHAUSTED** (prepaid empty) |
| Flow Ultra on this VM | **not used** (cannot keep Flow login) |
| Ken Burns / still-push fake | **not shipped** |
| Splice of rejected `08_ward_vs_lens_v02` / v03 | **not done** |
| `hos_001_part02_rough_v04.mp4` | **not exported** |
| PASS declared | **no** |
| Parts 03–05 / YouTube upload | **no** |

Failed UAT sha named in brief (`e7265b73…`) was **not** on release `hos-001-uat-cuts`. Release v01/v02 digests:

- v01 `c2aac0bda96b1564709d277cd1aa94c0acda6ef00ac0d1e7b7908a5a99f1b8b4`
- v02 `883b581a3f22fcea80f5633b749d35ea66258aca19770d2bfaab4bd561896bef` (REJECT still-push)

## Ready when credits + key land

1. Put `GEMINI_API_KEY` in Cloud Agent secrets (or `07_Edit-Project/.env`).
2. Confirm AI Studio prepaid has balance for `veo-3.1-lite-generate-preview`.
3. `python3 07_Edit-Project/_mint_part02_ward_v04_api.py`
4. Visual QA: nurses / steam / cloth move; camera locked; no neon; no Explorer/Orbit.
5. `python3 07_Edit-Project/_splice_part02_v04_ward.py`
6. Print SIZE + SHA256 of `hos_001_part02_rough_v04.mp4`. STOP for Ben UAT.

Start still seed: `04_Generated-Clips/part02/refs/08_ward_vs_lens_v04.jpg` (tighter mid-stride composition from the v03 still asset).
