---
description: HOS CG — Flow Veo primary (Orbit parity)
alwaysApply: true
---

# History of Science — CG path (Flow-first)

Locked to match Orbit With Ben production practice.

## Primary

**Google Flow Veo UI** via `04_Audio/tools/orbit_flow_veo_ui.py`

- Burns **Google One → AI Ultra Flow credits** (not Gemini API Fast/Lite buckets)
- Model: **Veo 3.1** only (`Veo 3.1 - Lite` / `Fast` / `Quality`) — never Omni Flash / Nano Banana
- HOS start-frame I2V proven path (2026-08-26):
  1. Upload still → right-click **Animate**
  2. Lock **Veo 3.1 - Fast** · 16:9 · x1
  3. Prompt → Create → **approve credit confirmation**
  4. Wait for finished mp4 (not the start-frame JPEG)
- CLI: `--start-frame <still.jpg> --prompt "…" --out clip.mp4`
- One-time auth: `python3 04_Audio/tools/orbit_flow_veo_ui.py --login`
- Profile: `ORBIT_FLOW_PROFILE` (default Playwright profile path)
- **Daily generation limit** can block even with monthly credits left — wait for reset; do not ship Ken Burns as a substitute

## Fallback (only if Flow UI is broken / not logged in)

1. Gemini API `orbit_gemini_veo.py` — prefer `veo-3.1-lite-generate-preview` or `veo-3.1-generate-preview`
2. Do **not** default to `veo-3.1-fast-generate-preview` (separate API quota; 429s even with prepaid credit)

## VO (unchanged)

ElevenLabs **Ben Orbit Narrator** only (`kDch6ACCIpqgQ0NsU9kk`).

## Why

API Fast/Lite quotas are too thin for episode plate volume. Orbit avoided this by living on Flow Ultra. HOS follows the same pipe.

See: `VEO_QUOTA_DIAG_2026-08-26.md` (Episode 001).
