#!/usr/bin/env bash
# J0160: spend the Vertex Free Trial to the £0.10 margin on 006 (Ben 12 Oct 14:46; Chief ruling 12 Oct 15:10).
# Budget from the conservative figure min(console £4.93, £16.11 plateau − £11.86 logged = £4.25) − £0.10 ≈ £4.15.
#   A: P3:06 brewery (Fast 8), P4:01 villa (Fast 8), P4:02 Ingenhousz jars (Quality 8)      ≈ £2.65
#   B: P4:03 plunge leaf, P4:04 sunny window (Fast 6 each, seeded from P4:02's still)      ≈ £1.02  (cum ≈ £3.67)
# P4:05 (Quality 8, ≈ £1.31) would pass £4.15, so the run stops there. The minter's own guard still refuses any
# take that would go under the £0.10 floor.
set -u
cd "$(dirname "$0")"
PY=~/.venvs/hos-vertex/bin/python
S1=../04_Generated-Clips/part01/refs/v01_vertex_stills
S4=../04_Generated-Clips/part04/refs/v01_vertex_stills
OWB=/Users/benjaminoats/YouTube/orbit-with-ben
NOT_PHOTO="Stylised 3D cartoon like a premium animated feature, rounded simplified shapes, NOT a photograph."
SILL="$NOT_PHOTO Same sunny Ingenhousz sill, jars of leaves and summer daylight as image 2."
mkdir -p _logs

run() {  # run <part> <log> <args…>
  local part="$1" log="_logs/j0160_p$1_$2.log"; shift 2
  ( $PY _mint_vertex_v01.py --part "$part" "$@" --style-ref "$S1/01_willow_air_v02.jpg" 2>&1 \
      | grep --line-buffered -v -e MallocStack -e "poll " > "$log" ) &
  sleep 4
}

after_batch() {
  wait
  $PY _vertex_credit_v01.py "j0160_$1" 2>&1 | grep -v MallocStack | tail -1
  python3 - <<'EOF'
import json, subprocess
from pathlib import Path
owb = "/Users/benjaminoats/YouTube/orbit-with-ben/scripts/ai_spend.py"
for part in ("03", "04"):
    lp = Path(f"PART{part}_MINT_LOG_v01.json")
    if not lp.exists():
        continue
    log = json.loads(lp.read_text())
    seen_p = Path(f"_logs/p{int(part)}_ai_spend_logged.json")
    seen = set(json.loads(seen_p.read_text())) if seen_p.exists() else set()
    p = f"P{int(part)}"
    items = [(f"still:{s['plate']}:v{s['v']}", s.get("cost_usd", 0), f"{p}:{s['plate']} start still v{s['v']:02d} (gemini-2.5-flash-image), J0160") for s in log.get("stills", [])]
    items += [(f"take:{t['plate']}:t{t['take']}", t.get("cost_usd", 0), f"{p}:{t['plate']} take {t['take']} {t.get('quality')} ({t.get('model')}, {t.get('seconds')} s), J0160")
              for t in log.get("takes", []) if t.get("status") not in ("SUBMITTED",)]
    for key, usd, what in items:
        if key in seen or not usd:
            continue
        subprocess.run(["python3", owb, "spend", "--pool", "vertex", "--amount", f"{usd * 0.8:.3f}",
                        "--film", "HOS:006", "--what", what, "--by", "cursor"], check=True)
        seen.add(key)
    seen_p.write_text(json.dumps(sorted(seen), indent=1) + "\n")
EOF
  rd=$(python3 -c "import json;print(json.load(open('VERTEX_CREDIT_LOG_v01.json'))['readings'][-1]['free_trial_remaining_gbp'])")
  python3 "$OWB/scripts/ai_spend.py" record --pool vertex --left "$rd" --by cursor --note "J0160 after batch $1 (console lags; budget held to Chief's £4.15)"
  $PY _mint_vertex_v01.py --part 4 total 2>&1 | grep -v MallocStack | tail -3
}

batchA() {
  run 3 06_t1 auto 06_leeds_brewery --allow-flow-row --still-extra "$NOT_PHOTO Wide shot, no people close; no readable signs."
  run 4 01_t1 auto 01_villa --still-extra "$NOT_PHOTO No people."
  run 4 02_t1 auto 02_ingenhousz_jars --still-extra "$NOT_PHOTO"
  after_batch A
}

batchB() {
  [ -f "$S4/02_ingenhousz_jars_v01.jpg" ] || { echo "STOP: no P4:02 still to seed batch B"; return 1; }
  run 4 03_t1 auto 03_plunge_leaf --seed "$S4/02_ingenhousz_jars_v01.jpg" --still-extra "$SILL Close on the hands; no face."
  run 4 04_t1 auto 04_sunny_window --seed "$S4/02_ingenhousz_jars_v01.jpg" --still-extra "$SILL No people."
  after_batch B
}

case "${1:-}" in
A) batchA ;;
B) batchB ;;
all) batchA && batchB ;;
*) echo "usage: $0 A|B|all"; exit 2 ;;
esac
echo "j0160 batch ${1} done"
