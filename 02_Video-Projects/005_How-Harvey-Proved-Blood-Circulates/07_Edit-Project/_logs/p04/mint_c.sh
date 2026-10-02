#!/bin/zsh
S=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips/part04/refs/v02_vertex_stills
L=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/07_Edit-Project/_logs/p04
M=/tmp/h5/m
NOTEXT="No letters, words, numbers or writing anywhere in the picture."
NOHANDS="The patient's arm alone; no other hands or sleeves ever enter the frame."
CUT="The glowing cutaway stays smooth and clean: soft light inside translucent cartoon skin, no gore, no wounds, no blood on skin, no cut flesh, no balls, spheres, hearts or blobs."

$M --part 4 mint 03_hand_pale --still $S/03_hand_pale_v04.jpg --framing try3_glide_no_pulse_word --replace "below the band the hand slowly turns pale and cool; above the band a soft pulse throbs under the skin.=>the camera glides slowly from the hand up to the band: below the band the hand fades to a paler, cooler beige skin tone; above the band the skin of the upper arm gently rises and falls in a slow, steady rhythm." --extra "$NOHANDS Plain skin only: no glowing lines, symbols, zigzags or graphics of any kind. Never purple, lilac or white skin. $NOTEXT" > $L/03_t3.log 2>&1 &
sleep 3
$M --part 4 mint 04_stopped_loosen --still $S/04_stopped_loosen_v03.jpg --framing try2_no_hands --extra "$NOHANDS The band loosens a little by itself near the end as the red stream starts to creep under it. $CUT $NOTEXT" > $L/04_t2.log 2>&1 &
sleep 3
$M --part 4 mint 05_arteries_veins_shut --still $S/05_arteries_veins_shut_v03.jpg --framing try2_no_hands --extra "$NOHANDS The blue veins near the surface stay thin and flat at the band; nothing swells outside the arm's outline. $CUT $NOTEXT" > $L/05_t2.log 2>&1 &
sleep 3
$M --part 4 mint 08_knots_valve --still $S/08_knots_valve_v03.jpg --framing try2_translucent_push --extra "$NOHANDS The camera pushes slowly in towards the small pair of flaps inside the blue vein, which open and close gently like little swing doors. The skin stays whole and translucent, never cut open. $CUT $NOTEXT" > $L/08_t2.log 2>&1 &
wait
echo MINT_C_DONE
