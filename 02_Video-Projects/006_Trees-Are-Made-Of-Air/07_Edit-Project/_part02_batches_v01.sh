#!/usr/bin/env bash
# 006 Part 02 on Vertex, in batches after 01_furnace_soil KEEP (Claude desk task 5952355788, 3 Oct 2026).
#   _part02_batches_v01.sh 1|2|3
set -u
cd "$(dirname "$0")"
PY=~/.venvs/hos-vertex/bin/python
M="$PY _mint_vertex_v01.py --part 2"
S1=../04_Generated-Clips/part01/refs/v01_vertex_stills
S2=../04_Generated-Clips/part02/refs/v01_vertex_stills
NOT_PHOTO="Stylised 3D cartoon like a premium animated feature, rounded simplified shapes, NOT a photograph."
VH="Same van Helmont as image 2: long dark wavy hair, moustache, small pointed beard, black coat, white falling collar."
GARDEN="$NOT_PHOTO Same Vilvoorde walled garden of red brick and flagstones as image 2, the same big clay pot."
ROOM="$NOT_PHOTO Same Flemish brick workroom as image 2, lit by daylight from a grey window; the furnace is out of frame."

run() {  # run <log> <args…>; one style ref on stills, so the seed is "image 2"
  local log="_logs/p2_$1.log"; shift
  local sr=()
  [ "$1" = auto ] && sr=(--style-ref "$S1/01_willow_air_v02.jpg")
  ( $M "$@" ${sr[@]+"${sr[@]}"} 2>&1 | grep --line-buffered -v -e MallocStack -e "poll " > "$log" ) &
  sleep 4
}

case "${1:-}" in
1)
  run 02_t1 auto 02_balance_200 --seed $S2/01_furnace_soil_v01.jpg --still-extra "$ROOM"
  run 03_t1 auto 03_willow_shoot_scale --seed $S2/01_furnace_soil_v01.jpg --still-extra "$ROOM"
  run 04_t1 auto 04_lid_rain --seed $S2/06_garden_years_v01.jpg --still-extra "$GARDEN"
  run 05_t1 auto 05_pure_water --seed $S2/06_garden_years_v01.jpg --still-extra "$GARDEN"
  run 06_t2 mint 06_garden_years --still $S2/06_garden_years_v01.jpg --framing pot_locked \
    --replace "while the pot never changes=>while the same clay pot stays fixed in the centre of frame the whole time, the willow always rooted in it" \
    --extra "Locked-off camera, no camera move. The same clay pot stays fixed in the centre of frame the whole time; it never disappears, moves, shrinks or changes, and the willow never leaves it. The walls and flagstone path never change." \
    --tag "pot_lock_remint (Claude 5952355788: control lost the pot at 4.8 s; board uses 6.98 s)"
  run 07_t1 auto 07_explorer_snow --seed $S2/06_garden_years_v01.jpg --still-extra "$GARDEN Winter: snow on the walls, flagstones and pot lid; the willow is now tall."
  run 08_t1 auto 08_haul_tree --seed $S2/06_garden_years_v01.jpg --still-extra "$GARDEN Wide shot, figures small; faces not readable."
  run 09_t1 auto 09_weights_169 --seed $S1/10_van_helmont_sack_v01.jpg --still-extra "$NOT_PHOTO Same brass balance and garden as image 2. No people. The ledger page is blank at the start."
  run 10_t1 auto 10_fallen_leaves --seed $S2/06_garden_years_v01.jpg --still-extra "$GARDEN"
  run 13_t1 auto 13_tree_vs_pinch --seed $S1/03_pot_jar_leaf_v01.jpg --still-extra "$NOT_PHOTO Same oak table and room as image 2."
  ;;
2)
  run 12_t1 auto 12_pointer_short --seed $S2/01_furnace_soil_v01.jpg --still-extra "$ROOM Close on the brass balance pointer and its scale."
  run 14_t1 auto 14_why_grown --seed $S2/06_garden_years_v01.jpg --still-extra "$GARDEN The pot is empty now; van Helmont is small in frame, back to camera."
  run 15_t1 auto 15_desk_candle --seed $S1/10_van_helmont_sack_v01.jpg --still-extra "$NOT_PHOTO $VH Indoor study at night lit by one candle, not the garden."
  run 16_t1 auto 16_water_drawing --still-extra "$NOT_PHOTO Old paper page, brown-ink line drawing of a tree, no words or letters anywhere."
  run 17_t1 auto 17_mostly_wrong --seed $S2/06_garden_years_v01.jpg --still-extra "$GARDEN The pot is empty of soil; an open ledger lies on a garden bench."
  run 18_t1 auto 18_charcoal_hearth --seed $S1/10_van_helmont_sack_v01.jpg --still-extra "$NOT_PHOTO $VH Indoor brick hearth room, not the garden."
  run 22_t1 auto 22_shimmer_willow --seed $S2/06_garden_years_v01.jpg --still-extra "$GARDEN The willow is tall. No people."
  ;;
3)
  run 19_t1 auto 19_ash_mound --seed $S2/18_charcoal_hearth_v02.jpg --still-extra "$NOT_PHOTO Same brick hearth as image 2, fire completely out and cold, no glow, no embers; daylight. No people."
  run 20_t1 auto 20_shimmer_coals --seed $S2/18_charcoal_hearth_v02.jpg --still-extra "$NOT_PHOTO Same brick hearth as image 2, fire completely out, grey cold coals, no glow, no embers; daylight. No people."
  run 21_t1 auto 21_gas_window --seed $S2/15_desk_candle_v03.jpg --still-extra "$NOT_PHOTO Same study as image 2 but by day, candle gone, window open; van Helmont small at his desk, back to camera."
  ;;
*) echo "usage: $0 1|2|3"; exit 2 ;;
esac
wait
echo "batch ${1} done"
