#!/usr/bin/env bash
# Remint Part 02 plates marked remint=true in part-02_plates_v02.json.
# Bash 3.2 safe. Create handoff → settle → harvest into v01_fast (overwrite).
set -euo pipefail
EDIT="$(cd "$(dirname "$0")" && pwd)"
PROJ="$(cd "$EDIT/.." && pwd)"
RAW="$PROJ/04_Generated-Clips/part02/raw/v01_fast"
REJECT="$PROJ/04_Generated-Clips/part02/raw/_rejected_v01_fire_gibberish"
PLATES_JSON="$EDIT/parts/part-02_plates_v02.json"
LOG="$EDIT/logs/drive_part02_remint_v02.log"
mkdir -p "$EDIT/logs" "$RAW" "$REJECT"

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

log() { printf '%s\n' "$*" | tee -a "$LOG"; }

log "drive Part 02 remint v02 start $(date -Iseconds)"

NEED_FILE="$(mktemp)"
python3 - <<PY >"$NEED_FILE"
import json
from pathlib import Path
plates = json.loads(Path("$PLATES_JSON").read_text())["plates"]
for p in plates:
    if p.get("remint", True):
        print(p["id"])
PY

NEED=()
while IFS= read -r line || [[ -n "$line" ]]; do
  [[ -z "$line" ]] && continue
  NEED+=("$line")
done <"$NEED_FILE"
rm -f "$NEED_FILE"

log "remint ${#NEED[@]} plates: ${NEED[*]:-}"
[[ ${#NEED[@]} -gt 0 ]] || { log "nothing to remint"; exit 0; }

for pid in "${NEED[@]}"; do
  dest="$RAW/${pid}_v01.mp4"
  if [[ -f "$dest" ]]; then
    ts="$(date +%Y%m%d_%H%M%S)"
    mv "$dest" "$REJECT/${pid}_v01_pre_v02_${ts}.mp4"
    log "archived old $pid -> $REJECT"
  fi
  log ""
  log "=== CREATE $pid ==="
  python3 -u "$EDIT/_mint_one_plate_create_v01.py" \
    --plate-id "$pid" \
    --out "$dest" \
    --plates-json "$PLATES_JSON" \
    2>&1 | tee -a "$LOG"
  create_rc=${PIPESTATUS[0]}
  [[ "$create_rc" -eq 0 ]] || { log "CREATE failed rc=$create_rc"; exit "$create_rc"; }
  before="$(rg -o 'gallery-pending:([0-9]+)' -r '$1' "$LOG" | tail -1 || true)"
  log "=== SETTLE ${SETTLE_S}s (before_thumbs=${before:-none}) ==="
  sleep "$SETTLE_S"
  log "=== HARVEST $pid ==="
  harvest_args=(--out "$dest" --project "$HOS_FLOW_PROJECT_URL" --wait-s "$WAIT_S")
  if [[ -n "${before:-}" ]]; then
    harvest_args+=(--before-thumbs "$before")
  fi
  python3 -u "$EDIT/_harvest_newest_gallery_v01.py" "${harvest_args[@]}" \
    2>&1 | tee -a "$LOG"
  harvest_rc=${PIPESTATUS[0]}
  [[ "$harvest_rc" -eq 0 ]] || { log "HARVEST failed rc=$harvest_rc"; exit "$harvest_rc"; }
  dur="$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$dest")"
  size="$(stat -f%z "$dest" 2>/dev/null || stat -c%s "$dest")"
  log "harvested $pid dur=$dur size=$size"
  python3 -c "dur=float('$dur'); size=int('$size'); assert size>=800000 and 5.5<=dur<=12.0, (size,dur); print('PASS gate')" \
    | tee -a "$LOG"
done

log "OK drive Part 02 remint v02 finished $(date -Iseconds)"
