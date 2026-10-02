#!/bin/zsh
# Part 03 start frames, in seed order; each checked by eye before a take.
F=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips
P1=$F/part01/refs/v02_vertex_stills
P2=$F/part02/refs/v02_vertex_stills
S=$F/part03/refs/v02_vertex_stills
M=/tmp/h5/m
ROOM="Plain warm dark oak-panelled room behind, softly out of focus: no beds, no chandeliers, no wall lamps, no candles."
$M --part 3 still 01_cold_lecture_room
$M --part 3 still 05_how_much
$M --part 3 still 03_stove_to_muscle --seed $P2/05_heart_stove_v02.jpg --extra "$ROOM"
$M --part 3 still 09_jug_tower --extra "Plain warm oak-panelled room; the body outline is a simple pale translucent silhouette; the jugs are small pewter jugs tinted red."
$M --part 3 still 10_eat_weight
$M --part 3 still 11_where_go --seed $P2/04_veins_soak_v02.jpg --extra "$ROOM"
$M --part 3 still 06_two_ounces_eighth --seed $P1/04_sum_band_doors_v02.jpg --extra "Only '2 oz' is written so far, large and correct, the quill just finishing it; the rest of the page is blank."
$M --part 3 still 02_slow_hearts --seed $S/05_how_much_v01.jpg
$M --part 3 still 08_explorer_jugs --seed $S/05_how_much_v01.jpg --extra "Harvey is not in this shot."
$M --part 3 still 14_not_proof --seed $S/05_how_much_v01.jpg
$M --part 3 still 04_squeeze_pulse --seed $S/03_stove_to_muscle_v01.jpg --extra "$ROOM"
$M --part 3 still 07_thousand_beats --seed $S/06_two_ounces_eighth_v01.jpg --extra "The page shows '2 oz' and '1/8' already written; the quill is starting the '1' of 1000 below them."
$M --part 3 still 12_glowing_loop --seed $S/11_where_go_v01.jpg --extra "$ROOM"
$M --part 3 still 13_one_minute --seed $S/12_glowing_loop_v01.jpg --extra "$ROOM"
echo STILLS_DONE
