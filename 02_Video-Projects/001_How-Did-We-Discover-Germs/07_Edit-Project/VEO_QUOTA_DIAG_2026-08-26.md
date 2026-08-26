# Veo 429 diagnosis — 2026-08-26

## Symptom
`veo-3.1-fast-generate-preview` → HTTP **429 RESOURCE_EXHAUSTED**
(“check plan and billing”) even though prepaid credit remains.

## What still works (same API key, same moment)
| Model | Result |
|---|---|
| `gemini-3.6-flash` (text) | OK |
| `gemini-2.5-flash-image` | OK |
| `veo-3.1-lite-generate-preview` | **OK** (full 8s I2V completed) |
| `veo-3.1-generate-preview` | **OK** (full 8s I2V completed) |
| `veo-3.1-fast-generate-preview` | **429** |

## Root cause
Not “out of money.” **Per-model Veo quota** — Fast’s bucket is exhausted / spend-rate limited.
Credit balance ≠ Fast RPM/RPD/spend window. Lite and standard use separate quotas.

## Fix applied
- Default model → `veo-3.1-lite-generate-preview` (`orbit_gemini_veo.py` + `ORBIT_VEO_MODEL` in `.env`)
- Monitor: https://aistudio.google.com/rate-limit (same project as this key)
- Docs: https://ai.google.dev/gemini-api/docs/rate-limits

## Key note
Env key prefix is `AQ.…` (not classic `AIza…`). Flash/Veo lite still auth fine on it.
