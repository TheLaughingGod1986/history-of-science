#!/bin/zsh
# Part 01's 03_band_tightens style ref carries brown sleeves into every arm frame: heart ref only.
S=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips/part04/refs/v02_vertex_stills
HEART=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips/part01/refs/v02_vertex_stills/09_heart_clock_v02.jpg
M="/tmp/h5/m"
st() { $M --part 4 still "$@" --style-ref $HEART }
latest() { ls -t $S/$1_v*.jpg 2>/dev/null | head -1 }
NOTEXT="No letters, words, numbers or writing anywhere in the picture."
SKIN="Warm natural peach cartoon skin, clean and smooth: no wounds, no blood on skin, no cuts, no red marks or dots."
ONE="Exactly one hand of Harvey's in frame, coming from the top right in a jet-black sleeve with a plain white cuff. No other hands, no brown cloth, no buttons."
NOHANDS="The patient's bare arm alone on the oak table, entering from the right edge; no other hands, no sleeves, no people in frame."
CUT="Clean glowing cutaway illustration: smooth translucent skin with warm red arteries deep inside and cool blue veins near the surface, glowing softly. No gore, no wounds, no open flesh, no cut window in the skin, no balls, spheres, hearts or blobs."
P=$S/02_linen_tie_v05crop.jpg

st 03_hand_pale --seed $P --extra "Close on the patient's arm on the same oak table in the same warm light. $NOHANDS A cream linen band is tied tight round the upper arm near the right edge. $SKIN $NOTEXT"
B=$(latest 03_hand_pale)
st 09_push_stops --seed $B --extra "Same arm, table and light, closer on the forearm below the band. $ONE Its fingertip rests on a raised soft blue vein with small knots along it under the skin. $SKIN $NOTEXT"
st 10_slides_heart --seed $B --extra "Same arm, table and light, closer on the forearm below the band. $ONE Its fingertip rests on the raised soft blue vein, ready to stroke towards the elbow. $SKIN $NOTEXT"
st 11_two_fingers --seed $B --extra "Same arm, table and light, closer on the forearm below the band. $ONE Two of its fingertips rest side by side on a short stretch of the raised soft blue vein. $SKIN $NOTEXT"
st 12_stays_fills --seed $B --extra "Same arm, table and light, closer on the forearm below the band. $ONE Two of its fingertips press the vein a short way apart; the stretch between them lies flat under the skin. $SKIN $NOTEXT"
st 04_stopped_loosen --seed $B --extra "Same arm, table and light. $NOHANDS A cream linen band tied tight round the upper arm. $CUT The warm red stream stops at the band. $NOTEXT"
st 05_arteries_veins_shut --seed $B --extra "Same arm, table and light. $NOHANDS A cream linen band a little looser round the upper arm. $CUT Deep red lines run under the band to the hand; the thin blue lines near the surface stay flat and pinched at the band. $NOTEXT"
st 07_in_out_doors --seed $B --extra "Same arm, table and light, the band gone. $NOHANDS $CUT Red flows deep towards the hand; blue flows back near the surface towards the elbow. $NOTEXT"
st 08_knots_valve --seed $B --extra "Very close on the forearm, same table and light. $NOHANDS $CUT One swollen blue vein with small knots along it; inside the nearest knot a tiny pair of cup-shaped flaps like little swing doors. $NOTEXT"
st 13_one_way --seed $B --extra "Same arm, table and light, the band gone. $NOHANDS $CUT One long blue vein up the forearm with many pairs of tiny cup-shaped flaps like little swing doors, every pair open towards the elbow and the heart. $NOTEXT"
st 14_steering_home --seed $S/14_steering_home_v01.jpg --extra "Reframe: close top-down view filling the frame with one sheet of cream parchment on the oak desk in soft daylight. A clean, simple ink drawing: one vein drawn as two smooth parallel lines running from bottom to top, with three clear pairs of small V-shaped flaps inside it, all pointing upwards, and a short red ink stream entering at the bottom. Bold, tidy lines; no scribbles, no arm outline, no arrows. $NOTEXT"
st 15_your_hand_glow --seed $S/15_your_hand_glow_v01.jpg --extra "Same relaxed hand and wrist on the oak table in soft daylight, no face. The veins on the back of the hand show as soft cool blue lines under clean smooth skin with a gentle blue glow; nothing yellow or gold, no lightning. No wounds, no blood on skin. $NOTEXT"
st 18_aubrey --seed $S/18_aubrey_v01.jpg --extra "Same John Aubrey, room and window. The door across the street is a plain wooden door with no sign, no lettering and no plaque; two patients walk away from it. The notebook page is soft and out of focus with no readable or garbled writing. $NOTEXT"
echo P04_STILLS_E_DONE
