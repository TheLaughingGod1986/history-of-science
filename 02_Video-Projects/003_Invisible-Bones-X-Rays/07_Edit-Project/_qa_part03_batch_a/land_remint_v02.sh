#!/bin/zsh
set -euo pipefail
PLATE="$1"
SRC="$2"   # zip or mp4
PROJ="/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/003_Invisible-Bones-X-Rays"
CLIP="$PROJ/04_Generated-Clips/part03"
QA="$PROJ/07_Edit-Project/_qa_part03_batch_a"
DEST="$CLIP/${PLATE}_v02.mp4"
KEEP01="$CLIP/01_chapter_bones_v01.mp4"
KEEP03="$CLIP/03_soft_fades_v01.mp4"
KEEP07="$CLIP/07_explorer_hand_beam_v01.mp4"
sha_before() { shasum -a 256 "$1" | awk '{print $1}'; }
B01=$(sha_before "$KEEP01"); B03=$(sha_before "$KEEP03"); B07=$(sha_before "$KEEP07")
TMP="$QA/_unzip_remint_${PLATE}"
rm -rf "$TMP"; mkdir -p "$TMP" "$CLIP" "$QA"
if [[ "$SRC" == *.zip ]]; then
  unzip -o "$SRC" -d "$TMP" >/dev/null
  MP4=$(find "$TMP" -type f -iname '*.mp4' | head -1)
else
  MP4="$SRC"
fi
test -n "$MP4"
test -f "$MP4"
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
SHA=$(shasum -a 256 "$DEST" | awk '{print $1}')
BYTES=$(stat -f%z "$DEST")
ffmpeg -y -ss 0.4 -i "$DEST" -frames:v 1 -q:v 3 "$QA/${PLATE}_v02_start.jpg" 2>/dev/null
ffmpeg -y -ss $(python3 -c "print(max(0.5, float('$DUR')/2))") -i "$DEST" -frames:v 1 -q:v 3 "$QA/${PLATE}_v02_mid.jpg" 2>/dev/null
ffmpeg -y -ss $(python3 -c "print(max(0.5, float('$DUR')-0.6))") -i "$DEST" -frames:v 1 -q:v 3 "$QA/${PLATE}_v02_end.jpg" 2>/dev/null
A01=$(sha_before "$KEEP01"); A03=$(sha_before "$KEEP03"); A07=$(sha_before "$KEEP07")
test "$B01" = "$A01" -a "$B03" = "$A03" -a "$B07" = "$A07"
python3 - <<PY
import json
from datetime import datetime, timezone
r={"plate":"$PLATE","version":"v02","path":"$DEST","bytes":int("$BYTES"),"sha256":"$SHA","duration_s":float("$DUR"),"model":"Veo 3.1 - Quality","project":"https://flow.google.com/project/537a3344-5ba3-46c3-b727-4e166601d9d0","account":"benoats@googlemail.com","ts":datetime.now(timezone.utc).isoformat()}
open("$QA/${PLATE}_v02_mint.json","w").write(json.dumps(r,indent=2))
print(json.dumps(r,indent=2))
PY
