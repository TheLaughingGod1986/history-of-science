#!/usr/bin/env bash
# Run every repo check a PR will face, locally, before pushing (5 Oct 2026).
#
#   00_Brand/Channel-Setup/tools/check_all.sh                     # repo-wide checks
#   00_Brand/Channel-Setup/tools/check_all.sh 02_Video-Projects/009_The-Falling-Moon-Gravity
#   00_Brand/Channel-Setup/tools/check_all.sh 009                 # same, by film number
#
# Repo-wide: no media staged, contract tests, package-lint on every manifest,
# status board in sync, ElevenLabs guard tests.
# With a film folder: also review:script and gate:episode on its script master.
# Exits non-zero if anything fails; a PR with a red check here will be red in CI.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
FILM="${1:-}"
fail=0
run() {
  local name="$1"; shift
  printf '\n== %s\n' "$name"
  if "$@"; then printf -- '-- %s: PASS\n' "$name"; else printf -- '-- %s: FAIL\n' "$name"; fail=1; fi
}

cd "$ROOT"

media=$(git diff --cached --name-only --diff-filter=AM; git ls-files --others --exclude-standard) || true
media=$(printf '%s\n' "$media" | grep -iE '\.(mp4|mov|m4v|webm|wav|mp3|aiff?|m4a|flac|ogg)$' || true)
run "no media" test -z "$media"
[ -n "$media" ] && printf '%s\n' "$media"

run "status board in sync" python3 00_Brand/Channel-Setup/tools/status_board.py --check
run "ElevenLabs guard tests" python3 04_Audio/tools/test_el_guard.py

cd "$ROOT/07_Content-Ops"
run "contract tests" npx vitest run tests/hos-contract.test.ts
run "package-lint" npx tsx scripts/package-lint.ts

if [ -n "$FILM" ]; then
  FILM_DIR="$ROOT/${FILM%/}"
  if [ ! -d "$FILM_DIR" ]; then
    # A bare film number ("007") means its folder under 02_Video-Projects.
    match=("$ROOT"/02_Video-Projects/"${FILM%/}"_*/)
    [ ${#match[@]} -eq 1 ] && [ -d "${match[0]}" ] && FILM_DIR="${match[0]%/}"
  fi
  SCRIPT=$(ls "$FILM_DIR"/01_Script/*_script_master_v*.md 2>/dev/null | sort -V | tail -1)
  if [ -z "$SCRIPT" ]; then
    printf '\n== script: no *_script_master_v*.md in %s/01_Script\n' "$FILM"; fail=1
  else
    run "review:script $(basename "$SCRIPT")" npx tsx scripts/review-script.ts --file "$SCRIPT"
    run "gate:episode" npx tsx scripts/gate-episode.ts --project "$FILM_DIR" --script "$SCRIPT"
  fi
fi

printf '\n%s\n' "$([ $fail -eq 0 ] && echo 'ALL CHECKS PASS' || echo 'SOME CHECKS FAILED')"
exit $fail
