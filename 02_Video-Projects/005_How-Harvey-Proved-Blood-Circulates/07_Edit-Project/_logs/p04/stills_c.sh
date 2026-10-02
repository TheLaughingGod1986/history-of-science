#!/bin/zsh
S=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips/part04/refs/v02_vertex_stills
M=/tmp/h5/m
NOTEXT="No letters, words, numbers or writing anywhere in the picture."
SKIN="Warm natural peach cartoon skin, clean and smooth: no wounds, no blood on skin, no cuts, no red marks."
ONE="Exactly one hand of Harvey's in frame, coming from the top right in a jet-black sleeve with a plain white cuff, as in this picture. No other hands, no brown cloth, no buttons."
NOHANDS="The patient's bare arm alone on the oak table, entering from the right edge; no other hands, no sleeves, no people in frame."
CUT="Clean glowing cutaway illustration: smooth translucent skin with warm red arteries deep inside and cool blue veins near the surface, glowing softly. No gore, no wounds, no open flesh, no cut window in the skin, no balls, spheres, hearts or blobs."
A=$S/10_slides_heart_v01.jpg
P=$S/02_linen_tie_v05crop.jpg

$M --part 4 still 03_hand_pale --seed $P --extra "Close on the same arm on the same oak table in the same light. $NOHANDS A cream linen band is tied tight round the upper arm near the right edge. $SKIN $NOTEXT"
$M --part 4 still 09_push_stops --seed $A --extra "Same close framing and table, slightly brighter warm daylight. $ONE Its fingertip rests on a raised soft blue vein with small knots along it under the skin of the forearm. $SKIN $NOTEXT"
$M --part 4 still 10_slides_heart --seed $A --extra "Same close framing and table, slightly brighter warm daylight. $ONE Its fingertip rests on the raised soft blue vein, ready to stroke towards the elbow. $SKIN $NOTEXT"
$M --part 4 still 11_two_fingers --seed $A --extra "Same close framing and table, slightly brighter warm daylight. $ONE Two of its fingertips rest side by side on a short stretch of the raised soft blue vein. $SKIN $NOTEXT"
$M --part 4 still 12_stays_fills --seed $A --extra "Same close framing and table, slightly brighter warm daylight. $ONE Two of its fingertips press the vein a short way apart; the stretch between them lies flat under the skin. $SKIN $NOTEXT"
$M --part 4 still 04_stopped_loosen --seed $P --extra "Close on the same arm on the oak table. $NOHANDS A cream linen band tied tight round the upper arm. $CUT The warm red stream stops at the band. $NOTEXT"
$M --part 4 still 05_arteries_veins_shut --seed $P --extra "Close on the same arm on the oak table. $NOHANDS A cream linen band a little looser round the upper arm. $CUT Deep red lines run under the band to the hand; the thin blue lines near the surface stay flat and pinched at the band. $NOTEXT"
$M --part 4 still 07_in_out_doors --seed $P --extra "Close on the same arm on the oak table. $NOHANDS No band. $CUT Red flows deep towards the hand; blue flows back near the surface towards the elbow. $NOTEXT"
$M --part 4 still 08_knots_valve --seed $P --extra "Very close on the forearm on the oak table. $NOHANDS $CUT One swollen blue vein with small knots along it; inside the nearest knot a tiny pair of cup-shaped flaps like little swing doors. $NOTEXT"
$M --part 4 still 13_one_way --seed $P --extra "Close on the same arm on the oak table. $NOHANDS $CUT One long blue vein up the forearm with many pairs of tiny cup-shaped flaps like little swing doors, every pair open towards the elbow and the heart. $NOTEXT"
echo P04_STILLS_C_DONE
