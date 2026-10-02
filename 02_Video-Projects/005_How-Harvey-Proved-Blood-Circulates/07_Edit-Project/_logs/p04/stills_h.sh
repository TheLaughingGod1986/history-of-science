#!/bin/zsh
# Valve plates reuse Part 02's passed 13_little_doors look (ink vein on parchment with paper flaps),
# as in Harvey's own 1628 figures; arm plates stay glowing cutaways, heart style ref only.
S=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips/part04/refs/v02_vertex_stills
D=$S/_p02_13_doors_3s.jpg
HEART=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips/part01/refs/v02_vertex_stills/09_heart_clock_v02.jpg
M="/tmp/h5/m"
st() { $M --part 4 still "$@" --style-ref $HEART }
latest() { ls -t $S/$1_v*.jpg 2>/dev/null | head -1 }
sd() { $M --part 4 still "$@" --style-ref $D }
NOTEXT="No letters, words, numbers, glyphs, plaques or symbols anywhere in the picture."
DOORS="The same parchment and drawing style as this picture: a vein drawn in brown ink as two smooth parallel lines across cream parchment on the oak desk in soft daylight, with small raised 3D paper flaps inside it like little doors. Clean, tidy and readable."
FINGER="Harvey's single fingertip, from a jet-black sleeve with a plain white cuff entering from the top right, rests on the drawn vein. No other hands."
NOHANDS="The patient's arm alone on the oak table, entering from the right edge; no other hands, no sleeves, no people in frame."
CUT="Clean glowing cutaway: smooth translucent skin, warm red arteries deep inside, cool blue veins near the surface, glowing softly. No gore, no wounds, no cut window, no balls, spheres, blobs, doors or plaques in the arm."
A4=$S/04_stopped_loosen_v03.jpg

sd 09_push_stops --seed $D --extra "$DOORS Close framing: the parchment fills the whole frame; no clock, no other objects. $FINGER A short red ink stream sits inside the vein just below a pair of flaps that are shut towards it. $NOTEXT"
sd 10_slides_heart --seed $D --extra "$DOORS Close framing: the parchment fills the whole frame; no clock, no other objects. $FINGER The flaps all lean the same way, open towards the top of the page; a red ink stream sits inside the vein below them. $NOTEXT"
sd 11_two_fingers --seed $D --extra "$DOORS Close framing: the parchment fills the whole frame; no clock, no other objects. Harvey's two fingertips, from a jet-black sleeve with a plain white cuff entering from the top right, rest side by side on the drawn vein, which is filled with red ink. No other hands. $NOTEXT"
sd 12_stays_fills --seed $D --extra "$DOORS Close framing: the parchment fills the whole frame; no clock, no other objects. Harvey's two fingertips, from a jet-black sleeve with a plain white cuff entering from the top right, press the drawn vein a short way apart; the stretch between them is empty and pale, red ink fills the vein on either side. No other hands. $NOTEXT"
sd 13_one_way --seed $D --extra "$DOORS Close framing: the parchment fills the whole frame; no clock, no other objects. A long drawn vein runs diagonally up the page with many pairs of little paper flaps, every pair open the same way, towards the top of the page; a red ink stream flows inside it towards the top. $NOTEXT"
sd 14_steering_home --seed $D --extra "Two sheets of parchment side by side on the oak desk in soft daylight, both in this drawing style: on the left, an older faded drawing of a vein with little flaps; on the right, a fresh drawing of the same vein with little paper flaps and a red ink stream inside it. $NOTEXT"
st 03_hand_pale --seed $A4 --extra "Same arm, table and light. $NOHANDS A cream linen band tied tight round the upper arm. $CUT Above the band the vessels glow warm red; below the band the forearm and hand are dim and cool grey-blue, with no red in them. $NOTEXT"
st 04_stopped_loosen --seed $A4 --extra "Same arm, table and light. $NOHANDS A cream linen band tied tight round the upper arm. $CUT The warm red stream glows brightly above the band and stops dead at it; the forearm and hand below the band are dim, with no red. $NOTEXT"
st 07_in_out_doors --seed $A4 --extra "Same arm, table and light, the band gone. $NOHANDS $CUT Red flows deep towards the hand; blue flows back near the surface towards the elbow. $NOTEXT"
st 05_arteries_veins_shut --seed $(latest 04_stopped_loosen) --extra "Same arm, table and light. $NOHANDS The cream linen band sits a little looser round the upper arm. $CUT Deep red lines pass under the band and run on into the forearm towards the hand; the thin blue lines near the surface stop short at the band. $NOTEXT"
st 15_your_hand_glow --seed $S/15_your_hand_glow_v01.jpg --extra "Same relaxed hand and wrist on the oak table in soft daylight, no face, nobody else. Natural warm skin with faint, soft blue veins just visible under it on the back of the hand and wrist. No glow, no light effects, no lines drawn on the skin, nothing yellow or gold. Clean skin, no wounds, no blood on skin. $NOTEXT"
echo P04_STILLS_H_DONE
