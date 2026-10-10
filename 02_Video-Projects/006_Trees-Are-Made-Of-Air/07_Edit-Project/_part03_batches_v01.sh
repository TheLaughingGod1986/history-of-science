#!/usr/bin/env bash
# 006 Part 03 first takes on the Vertex Free Trial (J0107; Ben 10 Oct 22:50: spend to £0, never onto paid billing).
#   _part03_batches_v01.sh 1|2|3|all
# Batch 1 opens each set without a seed; 2 and 3 seed from batch 1's stills. Credit re-read and
# ai_spend log after every batch. The minter's guard refuses any take that would go under £0.
# P3:06_leeds_brewery waits for Flow (12 Oct refill); P3:16_repair_reuse is a window of P3:14.
set -u
cd "$(dirname "$0")"
PY=~/.venvs/hos-vertex/bin/python
M="$PY _mint_vertex_v01.py --part 3"
S1=../04_Generated-Clips/part01/refs/v01_vertex_stills
S3=../04_Generated-Clips/part03/refs/v01_vertex_stills
OWB=/Users/benjaminoats/YouTube/orbit-with-ben
NOT_PHOTO="Stylised 3D cartoon like a premium animated feature, rounded simplified shapes, NOT a photograph."
HALES="$NOT_PHOTO Same Teddington churchyard garden and the same Stephen Hales as image 2."
ROOM="$NOT_PHOTO Same plain Georgian room, oak table, glass jar in its bowl of water and window daylight as image 2."
TOWN="$NOT_PHOTO Same 1770s English town and morning light as image 2."
mkdir -p _logs

run() {  # run <log> <args…>; one style ref on stills, so the seed is "image 2"
  local log="_logs/p3_$1.log"; shift
  ( $M "$@" --style-ref "$S1/01_willow_air_v02.jpg" 2>&1 | grep --line-buffered -v -e MallocStack -e "poll " > "$log" ) &
  sleep 4
}

after_batch() {  # credit re-read + ai_spend for every finished take/still not logged yet
  wait
  $PY _vertex_credit_v01.py "p03_b$1" 2>&1 | tail -1
  python3 - "$1" <<'EOF'
import json, subprocess, sys
from pathlib import Path
log = json.loads(Path("PART03_MINT_LOG_v01.json").read_text()) if Path("PART03_MINT_LOG_v01.json").exists() else {"takes": [], "stills": []}
seen_p = Path("_logs/p3_ai_spend_logged.json")
seen = set(json.loads(seen_p.read_text())) if seen_p.exists() else set()
owb = "/Users/benjaminoats/YouTube/orbit-with-ben/scripts/ai_spend.py"
items = [(f"still:{s['plate']}:v{s['v']}", s.get("cost_usd", 0), f"P3:{s['plate']} start still v{s['v']:02d} (gemini-2.5-flash-image), J0107") for s in log.get("stills", [])]
items += [(f"take:{t['plate']}:t{t['take']}", t.get("cost_usd", 0), f"P3:{t['plate']} take {t['take']} {t.get('quality')} ({t.get('model')}, {t.get('seconds')} s), J0107")
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
  python3 "$OWB/scripts/ai_spend.py" record --pool vertex --left "$rd" --by cursor --note "J0107 after P3 batch $1 (console lags; minter guard is lag-aware)"
  $M total
}

batch1() {
  run 01_t1 auto 01_soil_to_sky --still-extra "$NOT_PHOTO"
  run 02_t1 auto 02_hales_branch --still-extra "$NOT_PHOTO"
  run 04_t1 auto 04_leaf_mist --still-extra "$NOT_PHOTO"
  run 05_t1 auto 05_guess --still-extra "$NOT_PHOTO Old paper page, no words or letters anywhere."
  run 07_t1 auto 07_priestley --still-extra "$NOT_PHOTO"
  run 08_t1 auto 08_candles_out --still-extra "$NOT_PHOTO A plain Georgian room with an oak table by a daylight window."
  run 13_t1 auto 13_fires_breath --still-extra "$NOT_PHOTO Wide shot, figures small; faces not readable."
  after_batch 1
}

batch2() {
  run 03_t1 auto 03_water_level --seed $S3/02_hales_branch_v01.jpg --still-extra "$HALES Close on the glass tube; no face."
  run 09_t1 auto 09_injured_air --seed $S3/08_candles_out_v01.jpg --still-extra "$ROOM No candle flame anywhere."
  run 10_t1 auto 10_mint_jar --seed $S3/08_candles_out_v01.jpg --still-extra "$ROOM No candle flame anywhere."
  run 11_t1 auto 11_candle_tall --seed $S3/08_candles_out_v01.jpg --still-extra "$ROOM A green mint sprig in a little pot under the jar."
  run 12_t1 auto 12_mouse_mint --seed $S3/08_candles_out_v01.jpg --still-extra "$ROOM No candle flame anywhere."
  after_batch 2
}

batch3() {
  run 14_t1 auto 14_trees_breathe --seed $S3/13_fires_breath_v01.jpg --still-extra "$TOWN Green woods and hedges beyond the town."
  run 15_t1 auto 15_quill_vegetable --seed $S3/08_candles_out_v01.jpg --still-extra "$ROOM No candle flame anywhere; no readable text."
  run 17_t1 auto 17_notebook_tick --seed $S3/08_candles_out_v01.jpg --still-extra "$ROOM No candle flame anywhere; marks only, no readable words."
  run 18_t1 auto 18_dark_window --seed $S3/08_candles_out_v01.jpg --still-extra "$ROOM Evening; no candle, lamp or flame anywhere."
  after_batch 3
}

case "${1:-}" in
1) batch1 ;;
2) batch2 ;;
3) batch3 ;;
all) batch1; batch2; batch3 ;;
*) echo "usage: $0 1|2|3|all"; exit 2 ;;
esac
echo "part 03 batch ${1} done"
