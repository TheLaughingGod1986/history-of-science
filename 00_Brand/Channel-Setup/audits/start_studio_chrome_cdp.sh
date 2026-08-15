#!/usr/bin/env bash
# Open logged-in YouTube Studio with CDP :9222 for in-place Replace.
set -euo pipefail
SRC="${HOME}/Library/Application Support/Google/Chrome"
DST="${HOME}/.orbit-chrome-youtube-studio"
PORT=9222

if curl -sf "http://127.0.0.1:${PORT}/json/version" >/dev/null 2>&1; then
  echo "CDP :${PORT} already up"
  curl -s "http://127.0.0.1:${PORT}/json/list" | python3 -c 'import sys,json
for t in json.load(sys.stdin):
  u=t.get("url","")
  if u.startswith("http"): print(u[:160])'
  exit 0
fi

if [[ ! -d "$DST/Default" ]]; then
  echo "Cloning Default Chrome → $DST"
  mkdir -p "$DST"
  rsync -a --exclude 'Singleton*' --exclude 'BrowserMetrics*' --exclude 'Crashpad' \
    --exclude 'ShaderCache' --exclude 'GrShaderCache' --exclude 'GraphiteDawnCache' \
    --exclude 'component_crx_cache' --exclude 'extensions_crx_cache' --exclude 'Safe Browsing' \
    "$SRC/" "$DST/"
fi

rm -f "$DST/SingletonLock" "$DST/SingletonSocket" "$DST/SingletonCookie"
nohup /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port="${PORT}" \
  --remote-allow-origins='*' \
  --user-data-dir="$DST" \
  --profile-directory=Default \
  --no-first-run \
  --no-default-browser-check \
  'https://studio.youtube.com/' \
  >/tmp/orbit-studio-chrome-cdp.log 2>&1 &
echo "Started Studio Chrome pid $! (log /tmp/orbit-studio-chrome-cdp.log)"
echo "Complete any passkey/2FA prompt, then re-run replace."
