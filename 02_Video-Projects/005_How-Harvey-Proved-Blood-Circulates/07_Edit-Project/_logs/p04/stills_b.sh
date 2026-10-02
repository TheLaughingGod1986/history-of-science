#!/bin/zsh
S=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips/part04/refs/v02_vertex_stills
M=/tmp/h5/m
latest() { ls -t $S/$1_v*.jpg 2>/dev/null | head -1 }
NOTEXT="No letters, words, numbers or writing anywhere in the picture."
SLEEVE="Any hands of Harvey's come in jet-black sleeves with plain white linen cuffs, exactly as in this picture; no brown cloth, no buttons, no brass."
ARM="Close on the patient's bare forearm and hand resting palm-up on the same oak table in the same light; no face, nobody else in frame; clean smooth cartoon skin, no wounds, no blood on skin, no cuts, no red marks. $SLEEVE"
CUT="Clean glowing cutaway illustration of the same forearm on the oak table: smooth translucent skin with warm red arteries deep inside and cool blue veins near the surface, glowing softly. No gore, no wounds, no open flesh, no cut window in the skin, no balls, spheres or blobs. $SLEEVE"
A=$S/02_linen_tie_v05crop.jpg

$M --part 4 still 03_hand_pale --seed $A --extra "$ARM The cream linen band is tied tight round the upper arm near the right of frame; Harvey's hands rest on the table beside it. The hand below the band is a natural skin tone. $NOTEXT"
B=$(latest 03_hand_pale)
$M --part 4 still 09_push_stops --seed $B --extra "$ARM Closer on the forearm below the band: a raised soft blue vein with small knots along it under the skin; one fingertip of Harvey's hand rests lightly on the vein. $NOTEXT"
$M --part 4 still 10_slides_heart --seed $B --extra "$ARM Closer on the forearm below the band: the same raised soft blue vein with small knots under the skin; one fingertip of Harvey's hand rests on it, ready to stroke towards the elbow. $NOTEXT"
$M --part 4 still 11_two_fingers --seed $B --extra "$ARM Closer on the forearm below the band: the same raised soft blue vein; two fingertips of Harvey's hand rest side by side on a short stretch of it. $NOTEXT"
$M --part 4 still 12_stays_fills --seed $B --extra "$ARM Closer on the forearm below the band: two fingertips of Harvey's hand press the vein a short way apart and the stretch between them is flat and pale blue. $NOTEXT"
$M --part 4 still 04_stopped_loosen --seed $B --extra "$CUT The cream linen band is tied tight round the upper arm; the warm red stream inside stops at the band; Harvey's fingers rest on the knot. $NOTEXT"
$M --part 4 still 05_arteries_veins_shut --seed $B --extra "$CUT The cream linen band sits a little looser round the upper arm; deep red arteries run under it towards the hand while the thin blue veins near the surface stay flat and pinched at the band. $NOTEXT"
$M --part 4 still 07_in_out_doors --seed $S/13_one_way_v01.jpg --extra "$CUT Red flows deep down the arm towards the hand; blue flows back near the surface towards the elbow; small soft pulses of light travel along each. $NOTEXT"
$M --part 4 still 08_knots_valve --seed $S/13_one_way_v01.jpg --extra "$CUT Closer on one swollen blue vein through the translucent skin: small knots along it, and inside the nearest knot a tiny pair of cup-shaped flaps like little doors. $NOTEXT"
echo P04_STILLS_B_DONE
