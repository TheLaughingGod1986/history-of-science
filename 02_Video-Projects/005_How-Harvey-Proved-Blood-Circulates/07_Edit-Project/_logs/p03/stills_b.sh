#!/bin/zsh
F=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips
P2=$F/part02/refs/v02_vertex_stills
S=$F/part03/refs/v02_vertex_stills
M=/tmp/h5/m
while [ ! -s $S/13_one_minute_v01.jpg ] && pgrep -f "stills_a.sh" >/dev/null; do sleep 10; done
ROOM="Plain warm dark oak-panelled room behind, softly out of focus: no beds, no chandeliers, no wall lamps, no candles."
$M --part 3 still 02_slow_hearts --extra "Close-up, slightly top-down, on the open notebook alone: brown-ink sketches of a frog's heart and an eel's heart with little arrows. No person, no hands, no live animal, no writing."
$M --part 3 still 04_squeeze_pulse --seed $P2/04_veins_soak_v02.jpg --extra "$ROOM The same translucent glowing outline figure as the earlier cutaways, seated side-on at the oak table with one arm resting on it; the cartoon heart glows in the chest and a warm red artery runs down the arm to the wrist, where two fingertips of the figure's other hand rest. No floating organ."
$M --part 3 still 09_jug_tower --seed $P2/03_eat_to_liver_v02.jpg --extra "$ROOM A standing translucent glowing outline figure (same look as the earlier cutaways) stands beside a tower of tiny red pewter jugs on the floor, already as tall as its waist. Nothing lying down, no outline on the table."
echo STILLS_B_DONE
