#!/bin/zsh
S=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips/part02/refs/v02_vertex_stills
L=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/07_Edit-Project/_logs/p02
M=/tmp/h5/m
NOTEXT="No letters, words, numbers or writing anywhere in the picture."
$M --part 2 mint 06_septum_holes --still $S/06_septum_holes_v03.jpg --extra "$NOTEXT" > $L/06_septum_holes_t1.log 2>&1 &
sleep 3
$M --part 2 mint 14_pool_feet --still $S/14_pool_feet_v03.jpg --extra "$NOTEXT" > $L/14_pool_feet_t1.log 2>&1 &
sleep 3
$M --part 2 mint 09_vesalius_nothing --still $S/09_vesalius_nothing_v02.jpg --framing close-on-wall --extra "The pages stay blank apart from the drawing. $NOTEXT The magnifier holds still over the wall in the middle of the heart; the red drop presses against the wall and cannot pass." > $L/09_vesalius_nothing_t2.log 2>&1 &
sleep 3
$M --part 2 mint 10_why_believe --still $S/10_why_believe_v03.jpg --framing blank-cover --extra "The book's cover stays plain blank leather. $NOTEXT" > $L/10_why_believe_t2.log 2>&1 &
sleep 3
$M --part 2 mint 11_padua_explorer --still $S/11_padua_explorer_v01.jpg --framing no-lettering --extra "The drawing on his scroll is a pure line drawing of a vein with paired flaps. $NOTEXT" > $L/11_padua_explorer_t2.log 2>&1 &
sleep 3
$M --part 2 mint 15_harvey_ship --still $S/15_harvey_ship_v01.jpg --framing 1602-harbour --extra "Padua's port in 1602: only wooden sailing ships and old stone and timber buildings in the background haze. No modern ships, no steel, no cranes, no smokestacks." > $L/15_harvey_ship_t2.log 2>&1 &
wait
echo MINT_C_DONE
