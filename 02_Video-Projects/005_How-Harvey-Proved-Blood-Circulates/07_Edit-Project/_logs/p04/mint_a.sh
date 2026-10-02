#!/bin/zsh
S=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips/part04/refs/v02_vertex_stills
L=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/07_Edit-Project/_logs/p04
M=/tmp/h5/m
NOTEXT="No letters, words, numbers or writing anywhere in the picture."
ARM="Arm and hand only, no face. Clean smooth unbroken skin the whole time: no wound, no cut, no blood on the skin, no needle."
CUT="The glowing cutaway stays smooth and clean: soft light inside a translucent cartoon arm, no gore, no wounds, no blood on skin, no cut flesh."

# wave 1
$M --part 4 mint 02_linen_tie --still $S/02_linen_tie_v01.jpg --extra "$ARM $NOTEXT" > $L/02_t1.log 2>&1 &
sleep 3
$M --part 4 mint 03_hand_pale --still $S/03_hand_pale_v01.jpg --extra "$ARM $NOTEXT" > $L/03_t1.log 2>&1 &
sleep 3
$M --part 4 mint 04_stopped_loosen --still $S/04_stopped_loosen_v01.jpg --extra "$CUT $NOTEXT" > $L/04_t1.log 2>&1 &
sleep 3
$M --part 4 mint 05_arteries_veins_shut --still $S/05_arteries_veins_shut_v01.jpg --extra "$CUT $NOTEXT" > $L/05_t1.log 2>&1 &
sleep 3
$M --part 4 mint 06_veins_swell --still $S/06_veins_swell_v01.jpg --extra "$ARM $NOTEXT" > $L/06_t1.log 2>&1 &
sleep 3
$M --part 4 mint 07_in_out_doors --still $S/07_in_out_doors_v01.jpg --extra "$CUT $NOTEXT" > $L/07_t1.log 2>&1 &
sleep 3
$M --part 4 mint 08_knots_valve --still $S/08_knots_valve_v01.jpg --extra "$CUT $NOTEXT" > $L/08_t1.log 2>&1 &
sleep 3
$M --part 4 mint 09_push_stops --still $S/09_push_stops_v01.jpg --extra "$ARM $NOTEXT" > $L/09_t1.log 2>&1 &
sleep 3
$M --part 4 mint 10_slides_heart --still $S/10_slides_heart_v01.jpg --extra "$ARM $NOTEXT" > $L/10_t1.log 2>&1 &
wait
echo WAVE1_DONE

# wave 2
$M --part 4 mint 11_two_fingers --still $S/11_two_fingers_v01.jpg --extra "$ARM $NOTEXT" > $L/11_t1.log 2>&1 &
sleep 3
$M --part 4 mint 12_stays_fills --still $S/12_stays_fills_v01.jpg --extra "$ARM $NOTEXT" > $L/12_t1.log 2>&1 &
sleep 3
$M --part 4 mint 13_one_way --still $S/13_one_way_v01.jpg --extra "$CUT $NOTEXT" > $L/13_t1.log 2>&1 &
sleep 3
$M --part 4 mint 14_steering_home --still $S/14_steering_home_v01.jpg --extra "Ink line drawings and arrows only. $NOTEXT" > $L/14_t1.log 2>&1 &
sleep 3
$M --part 4 mint 15_your_hand_glow --still $S/15_your_hand_glow_v01.jpg --extra "$ARM $NOTEXT" > $L/15_t1.log 2>&1 &
sleep 3
$M --part 4 mint 16_press_book --still $S/16_press_book_v01.jpg --extra "The title page stays plain and blank (the title is added in the edit); the woodcut plates show only line drawings of an arm. $NOTEXT" > $L/16_t1.log 2>&1 &
sleep 3
$M --part 4 mint 17_whispers --still $S/17_whispers_v01.jpg --extra "Harvey keeps walking at a steady pace. No shop signs with lettering. $NOTEXT" > $L/17_t1.log 2>&1 &
sleep 3
$M --part 4 mint 18_aubrey --still $S/18_aubrey_v01.jpg --extra "The notebook page stays soft and out of focus; no readable or garbled writing is visible. $NOTEXT" > $L/18_t1.log 2>&1 &
sleep 3
$M --part 4 mint 19_gap_open --still $S/19_gap_open_v01.jpg --extra "The drawing keeps its red and blue loop with one blank gap; nothing is written on it. $NOTEXT" > $L/19_t1.log 2>&1 &
wait
echo WAVE2_DONE
