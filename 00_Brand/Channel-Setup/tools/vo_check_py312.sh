#!/bin/zsh
# Run HOS/OWB vo_check on the pinned Python 3.12 venv (faster-whisper/av).
# Default python3 on this Mini is 3.14 and can crash word-check (av metadata_errors).
set -euo pipefail
ROOT="/Users/benjaminoats/YouTube/History Of Science"
VENV="$ROOT/.venv_vo_check_py312"
TOOL="$ROOT/00_Brand/Channel-Setup/tools/vo_check.py"
if [[ ! -x "$VENV/bin/python" ]]; then
  echo "Missing venv at $VENV — create with: /opt/homebrew/opt/python@3.12/bin/python3.12 -m venv \"$VENV\" && \"$VENV/bin/pip\" install faster-whisper av" >&2
  exit 2
fi
exec "$VENV/bin/python" "$TOOL" "$@"
