#!/usr/bin/env python3
"""Locked Orbit channel voice — British Ben Orbit Narrator (IVC).

Import these constants in every VO generator. Do not swap voice_id without an
explicit channel-voice change request.
"""
from __future__ import annotations

VOICE_NAME = "Ben Orbit Narrator"
VOICE_ID = "kDch6ACCIpqgQ0NsU9kk"
VOICE_ACCENT = "British (Ben IVC)"
MODEL_ID = "eleven_v3"

# Production lock (V003 / V004)
VOICE_SETTINGS = {
    "stability": 0.34,
    "similarity_boost": 0.78,
    "style": 0.42,
    "speed": 1.04,
    "use_speaker_boost": True,
}

DESCRIPTION = (
    "Warm, articulate British educational narrator with calm authority, "
    "cinematic curiosity and restrained mystery. Quietly dramatic — never "
    "theatrical, never trailer-like."
)
