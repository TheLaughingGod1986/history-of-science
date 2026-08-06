# Orbit CG — Gemini Veo (default)

**Locked:** 2026-08-06  
**CG:** Native Google Gemini Veo API  
**VO:** ElevenLabs TTS — Ben Orbit Narrator only (unchanged)

## Why

ElevenLabs Image & Video (Omni / in-app Veo) was expensive, injected Explore/Eiffel start frames, and baked American speech. Native Gemini Veo keeps Orbit as start+ASSET reference and supports `generate_audio=False`.

## Setup

1. Buy / enable Gemini plan with Veo access.
2. Create an API key: https://aistudio.google.com/apikey
3. Export or put in `07_Edit-Project/.env` / `04_Audio/tools/.env`:

```bash
export GEMINI_API_KEY=...
# optional
# export ORBIT_VEO_MODEL=veo-3.1-fast-generate-preview
```

4. Install client if needed: `pip install google-genai`

## Generate

```bash
# Probe one silent Orbit clip
python3 04_Audio/tools/orbit_gemini_veo.py --probe

# Custom scene action
python3 04_Audio/tools/orbit_gemini_veo.py \
  --prompt "Orbit stands on Europa ice, cream eyes wide, Jupiter huge in sky" \
  --out /tmp/europa_orbit.mp4

# JWST episode wrapper (regen rejects / beats)
cd 02_Video-Projects/004_JWST-Discoveries-That-Change-Everything/07_Edit-Project
python3 _generate_veo_gemini_api_v01.py --probe --dry-run
```

Always strip audio (helper does this). Mix British VO from ElevenLabs in the edit.

## Rules

- `.cursor/rules/orbit-gemini-veo-cg.mdc`
- `.cursor/rules/orbit-british-vo-lock.mdc`
- Growth gate before spend: script ≥90 + pre-build vidIQ

## Legacy

`_generate_omni_*.py` Playwright EL Image-Video scripts — do not use for new episodes.
