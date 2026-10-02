#!/bin/zsh
F=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips
P2=$F/part02/refs/v02_vertex_stills
S=$F/part03/refs/v02_vertex_stills
M=/tmp/h5/m
ROOM="Plain warm dark oak-panelled room behind, softly out of focus: no beds, no chandeliers, no wall lamps, no candles."
FACELESS="The figure is a smooth faceless translucent mannequin outline: no eyes, no glowing eyes, no mouth, no facial features at all."
$M --part 3 still 02_slow_hearts --seed $S/02_slow_hearts_v02.jpg --extra "Close-up, slightly top-down, on the open notebook alone: two plain anatomical brown-ink sketches of small hearts (heart shapes only, with vessels) and little curved arrows. The hearts have no faces, no eyes, no heads, no animal bodies. No person, no hands, no live animal, no writing."
$M --part 3 still 04_squeeze_pulse --seed $S/04_squeeze_pulse_v02.jpg --extra "$ROOM $FACELESS Seated side-on at the oak table with one arm resting on it; the cartoon heart glows in the chest and a warm red artery runs down the arm to the wrist, where two fingertips of the figure's other hand rest."
$M --part 3 still 09_jug_tower --seed $S/09_jug_tower_v02.jpg --extra "$ROOM $FACELESS A standing plain pale translucent outline figure beside a tower of tiny red pewter jugs on the floor, already as tall as its waist. Soft daylight, nothing glowing, no glowing heart."
$M --part 3 still 13_one_minute --seed $P2/04_veins_soak_v02.jpg --extra "$ROOM $FACELESS A standing glowing translucent figure with a red loop of arteries and blue veins; a large brass clock face lies flat on the oak table in front of it with one brass hand. A single small round RED blood drop glows on the loop. No flame shapes, no candles, no teardrop of fire. No letters, words or numbers; the clock has plain tick marks only."
echo STILLS_C_DONE
