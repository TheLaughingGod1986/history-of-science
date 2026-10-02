#!/bin/zsh
S=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips/part04/refs/v02_vertex_stills
HEART=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips/part01/refs/v02_vertex_stills/09_heart_clock_v02.jpg
M="/tmp/h5/m"
st() { $M --part 4 still "$@" --style-ref $HEART }
NOTEXT="No letters, words, numbers, glyphs or symbols anywhere in the picture."
ONE="Exactly one hand of Harvey's, coming from the top right in a jet-black sleeve with a plain white cuff. No other hands, no brown cloth, no buttons."
NOHANDS="The patient's arm alone on the oak table, entering from the right edge; no other hands, no sleeves, no people in frame."
CUT="Clean glowing cutaway illustration of the forearm, as in this picture: smooth translucent skin, one cool glowing blue vein near the surface with small knots along it, warm red arteries faint and deep. No gore, no wounds, no open flesh, no cut window, no balls, spheres, hearts or blobs."
C=$S/08_knots_valve_v03.jpg

st 07_in_out_doors --seed $S/05_arteries_veins_shut_v03.jpg --extra "Same arm, table and light, the band gone. $NOHANDS Clean glowing cutaway: smooth translucent skin, warm red arteries deep inside flowing towards the hand, cool blue veins near the surface flowing back towards the elbow. No gore, no wounds, no cut window, no balls or blobs, nothing printed on the arm. $NOTEXT"
st 09_push_stops --seed $C --extra "Closer on the forearm, same table and light. $CUT $ONE Its fingertip rests lightly on the skin over the glowing blue vein, just above a knot. $NOTEXT"
st 10_slides_heart --seed $C --extra "Closer on the forearm, same table and light. $CUT $ONE Its fingertip rests on the skin over the glowing blue vein, ready to stroke towards the elbow. $NOTEXT"
st 11_two_fingers --seed $C --extra "Closer on the forearm, same table and light. $CUT $ONE Two of its fingertips rest side by side on the skin over a short stretch of the glowing blue vein. $NOTEXT"
st 12_stays_fills --seed $C --extra "Closer on the forearm, same table and light. $CUT $ONE Two of its fingertips press the skin a short way apart; the stretch of vein between them is dark and empty, the rest glows blue. $NOTEXT"
echo P04_STILLS_F_DONE
