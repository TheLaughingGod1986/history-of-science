#!/bin/zsh
S=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips/part02/refs/v02_vertex_stills
L=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/07_Edit-Project/_logs/p02
M=/tmp/h5/m
for p in 03_eat_to_liver 04_veins_soak 05_heart_stove 10_why_believe 13_little_doors; do
  $M --part 2 mint $p --still $S/${p}_v02.jpg > $L/${p}_t1.log 2>&1 &
  sleep 3
done
ROOM="Plain warm dark oak-panelled room behind, softly out of focus: no beds, no chandeliers, no wall lamps, no candles."
$M --part 2 still 06_septum_holes --seed $S/05_heart_stove_v02.jpg --extra "$ROOM Close-up: the glowing cartoon heart shown as a clean simple diagram cut open, its right and left chambers side by side with a thick smooth wall between them; tiny red drops gather at the wall on the right side. No stove in this shot, no gore." > $L/still_06.log 2>&1
$M --part 2 still 14_pool_feet --seed $S/13_little_doors_v02.jpg --extra "Same flat parchment drawing, top-down: a simple brown-ink outline of a human leg and foot, with the opened vein running down the leg and pairs of little doors along it. A drawing on paper; no hands, no 3D object." > $L/still_14.log 2>&1
wait
echo MINT_B_DONE
