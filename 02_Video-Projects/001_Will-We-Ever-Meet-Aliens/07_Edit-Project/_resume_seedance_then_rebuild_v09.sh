#!/bin/zsh
set -euo pipefail
cd /Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens/07_Edit-Project
# Prefer ElevenLabs Seedance pipeline (fal is exhausted). Falls back message if CDP down.
if curl -sS -m 2 http://127.0.0.1:9223/json/version >/dev/null; then
  ./.venv_orbit/bin/python3 -u _seedance_pipeline_v11.py
else
  echo "Chrome CDP 9223 not up — start ElevenLabs Image&Video Chrome first."
  echo "Attempting fal Seedance (needs balance)..."
  ./.venv_orbit/bin/python3 -u _animate_bold_scenes_seedance_v07.py || true
  ./.venv_orbit/bin/python3 -u _build_bold_explainer_v09_final_polish.py
fi
open ../09_Final-Export/aliens_BOLD_EXPLAINER_v09_FINAL_POLISHED_MASTER.mp4
