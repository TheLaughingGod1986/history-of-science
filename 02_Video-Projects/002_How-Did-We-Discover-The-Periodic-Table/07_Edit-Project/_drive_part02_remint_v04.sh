#!/usr/bin/env bash
# Remint Part 02 scenery v04 — finished Flow, no jars, candles OK.
# Bash 3.2 safe. Create → settle → harvest → size gate.
set -euo pipefail
EDIT="$(cd "$(dirname "$0")" && pwd)"
PROJ="$(cd "$EDIT/.." && pwd)"
RAW="$PROJ/04_Generated-Clips/part02/raw/v01_fast"
REJECT="$PROJ/04_Generated-Clips/part02/raw/_rejected_v03_unfinished_local"
PLATES_JSON="$EDIT/parts/part-02_plates_v04.json"
LOG="$EDIT/logs/drive_part02_remint_v04.log"
mkdir -p "$EDIT/logs" "$RAW" "$REJECT" "$EDIT/_qa_part02_v04/scenery"

export ORBIT_FLOW_PROFILE="${ORBIT_FLOW_PROFILE:-$HOME/.playwright-hos-flow-profile}"
export ORBIT_FLOW_ACCOUNT="${ORBIT_FLOW_ACCOUNT:-benoats@googlemail.com}"
export ORBIT_FLOW_HOME="${ORBIT_FLOW_HOME:-https://flow.google.com/u/1/}"
export ORBIT_FLOW_FORCE_NEW_PROJECT=0
export ORBIT_FLOW_REUSE_PROJECT=1
export ORBIT_FLOW_HEADED="${ORBIT_FLOW_HEADED:-1}"
export HOS_FLOW_PROJECT_URL="${HOS_FLOW_PROJECT_URL:-https://flow.google.com/u/1/project/30a34afb-8d9c-4eac-83ba-012d97f6b1b5}"
export ORBIT_FLOW_PROJECT_URL="$HOS_FLOW_PROJECT_URL"
export PYTHONUNBUFFERED=1

SETTLE_S="${HOS_FLOW_HARVEST_SETTLE_S:-95}"
WAIT_S="${HOS_FLOW_HARVEST_WAIT_S:-300}"
PY="${HOS_FLOW_PY:-/private/tmp/hos-flow-venv/bin/python}"
[[ -x "$PY" ]] || PY=python3

log() { printf '%s\n' "$*" | tee -a "$LOG"; }

log "drive Part 02 remint v04 start $(date -Iseconds)"

NEED_FILE="$(mktemp)"
"$PY" - <<PY >"$NEED_FILE"
import json
from pathlib import Path
plates = json.loads(Path(r"$PLATES_JSON").read_text())["plates"]
for p in plates:
    if p.get("kind") == "scenery" and p.get("remint", True):
        print(p["id"])
PY

NEED=()
while IFS= read -r line || [[ -n "$line" ]]; do
  [[ -z "$line" ]] && continue
  NEED+=("$line")
done <"$NEED_FILE"
rm -f "$NEED_FILE"

log "remint ${#NEED[@]} scenery: ${NEED[*]:-}"

for pid in "${NEED[@]}"; do
  dest="$RAW/${pid}_v01.mp4"
  if [[ -f "$dest" ]]; then
    ts="$(date +%Y%m%d_%H%M%S)"
    mv "$dest" "$REJECT/${pid}_v01_pre_v04_${ts}.mp4"
    log "archived old $pid"
  fi
  log ""
  log "=== CREATE $pid ==="
  set +e
  "$PY" -u "$EDIT/_mint_one_plate_create_v01.py" \
    --plate-id "$pid" \
    --out "$dest" \
    --plates-json "$PLATES_JSON" \
    2>&1 | tee -a "$LOG"
  create_rc=${PIPESTATUS[0]}
  set -e
  if [[ "$create_rc" -ne 0 ]]; then
    log "CREATE failed $pid rc=$create_rc"
    continue
  fi
  if [[ -f "$dest" ]]; then
    size="$(stat -f%z "$dest" 2>/dev/null || stat -c%s "$dest")"
    if [[ "$size" -gt 1500000 ]]; then
      log "DIRECT SAVE $pid size=$size"
    else
      log "=== SETTLE ${SETTLE_S}s ==="
      sleep "$SETTLE_S"
      log "=== HARVEST $pid ==="
      set +e
      "$PY" -u "$EDIT/_harvest_newest_gallery_v01.py" \
        --out "$dest" \
        --project "$HOS_FLOW_PROJECT_URL" \
        --wait-s "$WAIT_S" \
        2>&1 | tee -a "$LOG"
      harvest_rc=${PIPESTATUS[0]}
      set -e
      if [[ "$harvest_rc" -ne 0 || ! -f "$dest" ]]; then
        log "HARVEST failed $pid"
        continue
      fi
    fi
  else
    log "=== SETTLE ${SETTLE_S}s ==="
    sleep "$SETTLE_S"
    log "=== HARVEST $pid ==="
    set +e
    "$PY" -u "$EDIT/_harvest_newest_gallery_v01.py" \
      --out "$dest" \
      --project "$HOS_FLOW_PROJECT_URL" \
      --wait-s "$WAIT_S" \
      2>&1 | tee -a "$LOG"
    harvest_rc=${PIPESTATUS[0]}
    set -e
    if [[ "$harvest_rc" -ne 0 || ! -f "$dest" ]]; then
      log "HARVEST failed $pid"
      continue
    fi
  fi
  dur="$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$dest")"
  size="$(stat -f%z "$dest" 2>/dev/null || stat -c%s "$dest")"
  log "got $pid dur=$dur size=$size"
  # finished Flow clips are typically multi-MB; reject tiny placeholder leftovers
  if [[ "$size" -lt 1500000 ]]; then
    log "REJECT tiny/unfinished $pid size=$size"
    mv "$dest" "$REJECT/${pid}_v01_too_small_$(date +%Y%m%d_%H%M%S).mp4"
    continue
  fi
  ffmpeg -y -hide_banner -loglevel error -ss 2 -i "$dest" -frames:v 1 \
    "$EDIT/_qa_part02_v04/scenery/${pid}_t2.png"
  ffmpeg -y -hide_banner -loglevel error -ss 5 -i "$dest" -frames:v 1 \
    "$EDIT/_qa_part02_v04/scenery/${pid}_t5.png"
  log "PASS size gate $pid — manual fire QA on stills next"
done

log "drive Part 02 remint v04 done $(date -Iseconds)"
