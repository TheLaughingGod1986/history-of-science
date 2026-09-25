#!/usr/bin/env bash
# Drive remaining Part 02 plates one-by-one.
# Create exits immediately on Agent handoff; shell settles + harvests.
# Bash 3.2 compatible (macOS /bin/bash — no mapfile, no process-sub tee).
set -euo pipefail
EDIT="$(cd "$(dirname "$0")" && pwd)"
PROJ="$(cd "$EDIT/.." && pwd)"
RAW="$PROJ/04_Generated-Clips/part02/raw/v01_fast"
PLATES_JSON="$EDIT/parts/part-02_plates_v01.json"
LOG="$EDIT/logs/drive_part02_remaining_v01.log"
NOHUP_LOG="$EDIT/logs/drive_part02_nohup.log"
mkdir -p "$EDIT/logs" "$RAW"

export ORBIT_FLOW_PROFILE="${ORBIT_FLOW_PROFILE:-$HOME/.playwright-hos-flow-profile}"
export ORBIT_FLOW_ACCOUNT="${ORBIT_FLOW_ACCOUNT:-benoats@googlemail.com}"
export ORBIT_FLOW_HOME="${ORBIT_FLOW_HOME:-https://flow.google.com/u/1/}"
export ORBIT_FLOW_FORCE_NEW_PROJECT=0
export ORBIT_FLOW_REUSE_PROJECT=1
export ORBIT_FLOW_HEADED="${ORBIT_FLOW_HEADED:-1}"
export HOS_FLOW_PROJECT_URL="${HOS_FLOW_PROJECT_URL:-https://flow.google.com/u/1/project/30a34afb-8d9c-4eac-83ba-012d97f6b1b5}"
export ORBIT_FLOW_PROJECT_URL="$HOS_FLOW_PROJECT_URL"
export PYTHONUNBUFFERED=1
export PYTHONFAULTHANDLER=1

SETTLE_S="${HOS_FLOW_HARVEST_SETTLE_S:-75}"
WAIT_S="${HOS_FLOW_HARVEST_WAIT_S:-180}"

# Append-only logging without process substitution (bash 3.2 / SIGPIPE safe).
log() { printf '%s\n' "$*" | tee -a "$LOG" >>"$NOHUP_LOG"; }

log "drive Part 02 remaining start $(date -Iseconds)"

NEED_FILE="$(mktemp)"
python3 - <<PY >"$NEED_FILE"
import json
from pathlib import Path
plates = json.loads(Path("$PLATES_JSON").read_text())["plates"]
raw = Path("$RAW")
for p in plates:
    dest = raw / f"{p['id']}_v01.mp4"
    if not (dest.exists() and dest.stat().st_size > 800_000):
        print(p["id"])
PY

NEED=()
while IFS= read -r line || [[ -n "$line" ]]; do
  [[ -z "$line" ]] && continue
  NEED+=("$line")
done <"$NEED_FILE"
rm -f "$NEED_FILE"

log "need ${#NEED[@]} plates: ${NEED[*]:-}"
if [[ ${#NEED[@]} -eq 0 ]]; then
  log "nothing to do"
  exit 0
fi

for pid in "${NEED[@]}"; do
  dest="$RAW/${pid}_v01.mp4"
  log ""
  log "=== CREATE $pid ==="
  # Run create with output tee'd; do not exec-redirect the whole shell.
  python3 -u "$EDIT/_mint_one_plate_create_v01.py" --plate-id "$pid" --out "$dest" \
    2>&1 | tee -a "$LOG" | tee -a "$NOHUP_LOG"
  create_rc=${PIPESTATUS[0]}
  if [[ "$create_rc" -ne 0 ]]; then
    log "CREATE failed rc=$create_rc for $pid"
    exit "$create_rc"
  fi
  log "=== SETTLE ${SETTLE_S}s ==="
  sleep "$SETTLE_S"
  log "=== HARVEST $pid ==="
  python3 -u "$EDIT/_harvest_newest_gallery_v01.py" \
    --out "$dest" \
    --project "$HOS_FLOW_PROJECT_URL" \
    --wait-s "$WAIT_S" \
    2>&1 | tee -a "$LOG" | tee -a "$NOHUP_LOG"
  harvest_rc=${PIPESTATUS[0]}
  if [[ "$harvest_rc" -ne 0 ]]; then
    log "HARVEST failed rc=$harvest_rc for $pid"
    exit "$harvest_rc"
  fi
  dur="$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$dest")"
  size="$(stat -f%z "$dest" 2>/dev/null || stat -c%s "$dest")"
  log "harvested $pid dur=$dur size=$size"
  python3 -c "dur=float('$dur'); size=int('$size'); assert size>=800000 and 5.5<=dur<=12.0, (size,dur); print('PASS gate')" \
    | tee -a "$LOG" | tee -a "$NOHUP_LOG"
done

log "OK drive Part 02 remaining finished $(date -Iseconds)"
