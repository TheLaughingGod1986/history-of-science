---
description: Orbit CG via Gemini Veo API — ElevenLabs is VO-only
alwaysApply: true
---

# Orbit — CG generation = Gemini Veo (locked)

**Picture (CG / motion clips):** native **Google Gemini Veo API**  
**Narration (VO):** **ElevenLabs TTS only** — Ben Orbit Narrator (`kDch6ACCIpqgQ0NsU9kk`)

## Do this

1. Generate CG with `04_Audio/tools/orbit_gemini_veo.py` (or episode wrappers that import it).
2. Auth: `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) in env / `07_Edit-Project/.env`.
3. Always attach Orbit reference as **start frame + ASSET**; append `CG_SILENT_AUDIO_BLOCK` from `orbit_voice.py`.
4. Set `generate_audio=False`; **strip audio** after download (`strip_cg_native_audio.py` / helper in `orbit_gemini_veo.py`).
5. Mix British VO later from ElevenLabs — never use Veo speech.

## Do not

- Use **ElevenLabs Image & Video** (Omni / Veo Fast in the EL UI) for new CG — costly, Explore/Eiffel contamination, American speech.
- Treat Veo/Omni native speech as channel VO.
- Skip the Growth System v2 gate (vidIQ + script ≥90) before spending Gemini Veo credits.

## Legacy

Existing `_generate_omni_*.py` / Playwright EL Image-Video scripts are **legacy**. Prefer Gemini Veo for all new episodes and regenerations.

Canonical helper: `04_Audio/tools/orbit_gemini_veo.py`  
VO lock: `.cursor/rules/orbit-british-vo-lock.mdc` · `04_Audio/tools/orbit_voice.py`
