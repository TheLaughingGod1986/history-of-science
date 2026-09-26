#!/bin/zsh
set -euo pipefail
PLATE="$1"; VER="$2"; SRC="$3"
PROJ="/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/003_Invisible-Bones-X-Rays"
CLIP="$PROJ/04_Generated-Clips/part03"
QA="$PROJ/07_Edit-Project/_qa_part03_batch_a"
DEST="$CLIP/${PLATE}_${VER}.mp4"
KEEP01="$CLIP/01_chapter_bones_v01.mp4"; KEEP03="$CLIP/03_soft_fades_v01.mp4"; KEEP07="$CLIP/07_explorer_hand_beam_v01.mp4"
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
B01=$(sha "$KEEP01"); B03=$(sha "$KEEP03"); B07=$(sha "$KEEP07")
TMP="$QA/_unzip_remint_${PLATE}_${VER}"
rm -rf "$TMP"; mkdir -p "$TMP" "$CLIP" "$QA"
if [[ "$SRC" == *.zip ]]; then
  unzip -o "$SRC" -d "$TMP" >/dev/null
  MP4=$(find "$TMP" -type f -iname '*.mp4' | head -1)
else MP4="$SRC"; fi
test -n "$MP4"; test -f "$MP4"
if [[ -f "$DEST" ]]; then echo "STOP dest exists $DEST"; exit 2; fi
cp "$MP4" "$DEST"
/Users/benjaminoats/YouTube/History\ Of\ Science/.venv-hos/bin/python - <<PY
from pathlib import Path
import sys
sys.path.insert(0, "/Users/benjaminoats/YouTube/History Of Science/04_Audio/tools")
import orbit_gemini_veo as veo
veo.strip_audio(Path("$DEST"))
PY
DUR=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$DEST")
SHA=$(sha "$DEST"); BYTES=$(stat -f%z "$DEST")
ffmpeg -y -ss 0.4 -i "$DEST" -frames:v 1 -q:v 3 "$QA/${PLATE}_${VER}_start.jpg" 2>/dev/null
ffmpeg -y -ss $(python3 -c "print(max(0.5, float('$DUR')/2))") -i "$DEST" -frames:v 1 -q:v 3 "$QA/${PLATE}_${VER}_mid.jpg" 2>/dev/null
ffmpeg -y -ss $(python3 -c "print(max(0.5, float('$DUR')-0.6))") -i "$DEST" -frames:v 1 -q:v 3 "$QA/${PLATE}_${VER}_end.jpg" 2>/dev/null
test "$(sha "$KEEP01")" = "$B01" -a "$(sha "$KEEP03")" = "$B03" -a "$(sha "$KEEP07")" = "$B07"
MUTE=$(python3 - <<'PY'
notes={
"02_hand_enters_path":"Mute: faceless hand enters green-violet beam path; clean lab; no helix.",
"04_bones_hold":"Mute: bones hold clearer than soft tissue on clean palm; no helix.",
"05_ring_darker":"Mute: denser/darker ring on bone silhouette; no helix.",
"06_living_skeleton_read":"Mute: living skeleton read / NO KNIFE; clean desk; no helix.",
"08_medicine_question":"Mute: cardboard/CRT + empty beam read medicine question; no helix.",
"09_wonder":"Mute: wonder bone silhouette clear; no helix.",
"10_caution_burn":"Mute: caution/burn intensity + soft heat shimmer; no helix.",
"11_hold_beam":"Mute: beam + cardboard hold readable (not neon-only); no helix.",
}
import os; print(notes[os.environ['PLATE']])
PY
)
PLATE="$PLATE" python3 - <<PY
import json,os
from datetime import datetime, timezone
r={"plate":os.environ['PLATE'],"version":"$VER","path":"$DEST","bytes":int("$BYTES"),"sha256":"$SHA","duration_s":float("$DUR"),"model":"Veo 3.1 - Quality","project":"https://flow.google.com/project/537a3344-5ba3-46c3-b727-4e166601d9d0","account":"benoats@googlemail.com","mute_note":"""$MUTE""","ts":datetime.now(timezone.utc).isoformat()}
open("$QA/${PLATE}_${VER}_mint.json","w").write(json.dumps(r,indent=2))
print(json.dumps(r,indent=2))
PY
