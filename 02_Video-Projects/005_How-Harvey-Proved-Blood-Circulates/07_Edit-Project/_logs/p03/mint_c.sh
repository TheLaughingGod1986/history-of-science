#!/bin/zsh
S=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips/part03/refs/v02_vertex_stills
L=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/07_Edit-Project/_logs/p03
M=/tmp/h5/m
NOTEXT="No letters, words, numbers or writing anywhere in the picture."
INSIDE="The red stays inside the vessels the whole time: no sparks, particles, smoke or glow leave the body."

$M --part 3 mint 11_where_go --still $S/04_squeeze_pulse_v03.jpg --framing "figure at table, no watch" \
  --extra "Nothing on the table: no clock, watch or pocket watch. The red glow drains out of the arms and fades to nothing, leaving the figure pale and empty; then a faint red glow seeps back in through the same arm vessels and returns to the heart. No floating ball, no string. Clean, no gore. $NOTEXT" > $L/11_t2.log 2>&1 &
sleep 3
$M --part 3 mint 12_glowing_loop --still $S/12_glowing_loop_v01.jpg --framing "one clear loop" \
  --extra "$INSIDE One simple loop only: red flows from the heart out along the arteries to the hands and feet, and returns along the blue veins to the heart, round and round. Nothing glows in the belly: no coils, spirals or intestines. The camera pulls back slowly. $NOTEXT" > $L/12_t2.log 2>&1 &
sleep 3
$M --part 3 mint 13_one_minute --still $S/13_one_minute_v03.jpg --framing "exactly one hand" \
  --extra "The clock has exactly ONE brass hand and plain tick marks, no numerals; no second or third hand ever appears. The single hand sweeps once round as the single red drop runs once round the loop. $INSIDE" > $L/13_t2.log 2>&1 &
wait
echo MINT_C_DONE
