#!/usr/bin/env bash
# Vercel Ignored Build Step for History of Science Content Ops.
# Exit 0 = skip build; exit 1 = proceed with build.
#
# Vercel Root Directory is 07_Content-Ops. Docs-only / non-app commits
# elsewhere in the monorepo must not trigger a failing production build.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
APP_DIR="07_Content-Ops"

PREV="${VERCEL_GIT_PREVIOUS_SHA:-}"
if [[ -z "$PREV" ]]; then
  if git -C "$ROOT" rev-parse --verify --quiet HEAD^ >/dev/null; then
    PREV="$(git -C "$ROOT" rev-parse HEAD^)"
  else
    echo "[vercel-ignore-build] No previous commit — proceeding with build"
    exit 1
  fi
fi

if git -C "$ROOT" diff --quiet "$PREV" HEAD -- "$APP_DIR"; then
  echo "[vercel-ignore-build] No changes under ${APP_DIR} vs ${PREV} — skipping build"
  exit 0
fi

echo "[vercel-ignore-build] ${APP_DIR} changed vs ${PREV} — proceeding with build"
exit 1
