#!/bin/zsh
S=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips/part03/refs/v02_vertex_stills
L=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/07_Edit-Project/_logs/p03
M=/tmp/h5/m
NOTEXT="No letters, words, numbers or writing anywhere in the picture."
FIG="The translucent figure stays smooth and clean, no gore, no wounds, no blood on skin."

# wave 1
$M --part 3 mint 02_slow_hearts --still $S/02_slow_hearts_v04.jpg --extra "Every drawing is a heart only: no faces, eyes, heads or animals. $NOTEXT" > $L/02_t1.log 2>&1 &
sleep 3
$M --part 3 mint 03_stove_to_muscle --still $S/03_stove_to_muscle_from_p02_05_last.jpg --extra "The little stove and its fire fade away completely in the first two seconds; from then on only the clean cartoon heart muscle squeezes firmly. $FIG" > $L/03_t1.log 2>&1 &
sleep 3
$M --part 3 mint 04_squeeze_pulse --still $S/04_squeeze_pulse_v03.jpg --extra "$FIG" > $L/04_t1.log 2>&1 &
sleep 3
$M --part 3 mint 05_how_much --still $S/05_how_much_v01.jpg --extra "The page stays blank. $NOTEXT" > $L/05_t1.log 2>&1 &
sleep 3
$M --part 3 mint 06_two_ounces_eighth --still $S/06_two_ounces_eighth_v01.jpg --extra "The only writing on the page is '2 oz' and '1/8'. No other letters or scribbles appear." > $L/06_t1.log 2>&1 &
sleep 3
$M --part 3 mint 07_thousand_beats --still $S/07_thousand_beats_v01.jpg --extra "The only writing on the page is '2 oz', '1/8' and '1000'. No other letters or scribbles appear. The clock has plain tick marks, no numerals." > $L/07_t1.log 2>&1 &
sleep 3
$M --part 3 mint 08_explorer_jugs --still $S/08_explorer_jugs_v01.jpg --extra "$NOTEXT" > $L/08_t1.log 2>&1 &
wait
echo WAVE1_DONE

# wave 2
$M --part 3 mint 09_jug_tower --still $S/09_jug_tower_v03.jpg --extra "$NOTEXT" > $L/09_t1.log 2>&1 &
sleep 3
$M --part 3 mint 10_eat_weight --still $S/10_eat_weight_v01.jpg --extra "$NOTEXT" > $L/10_t1.log 2>&1 &
sleep 3
$M --part 3 mint 11_where_go --still $S/11_where_go_v01.jpg --extra "No clock, watch or pocket watch anywhere. $FIG $NOTEXT" > $L/11_t1.log 2>&1 &
sleep 3
$M --part 3 mint 12_glowing_loop --still $S/12_glowing_loop_v01.jpg --extra "$FIG $NOTEXT" > $L/12_t1.log 2>&1 &
sleep 3
$M --part 3 mint 13_one_minute --still $S/13_one_minute_v03.jpg --extra "The clock has plain tick marks only, no numerals; the single red drop runs once round the loop as the brass hand sweeps once round. $FIG" > $L/13_t1.log 2>&1 &
sleep 3
$M --part 3 mint 14_not_proof --still $S/14_not_proof_v01.jpg --extra "The page of sums lies flat and soft out of focus; no readable or garbled writing is visible. $NOTEXT" > $L/14_t1.log 2>&1 &
wait
echo WAVE2_DONE
