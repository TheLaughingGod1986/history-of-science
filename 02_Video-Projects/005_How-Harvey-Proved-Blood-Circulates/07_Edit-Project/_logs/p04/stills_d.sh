#!/bin/zsh
S=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips/part04/refs/v02_vertex_stills
M=/tmp/h5/m
NOTEXT="No letters, words, numbers or writing anywhere in the picture."

$M --part 4 still 14_steering_home --seed $S/14_steering_home_v01.jpg --extra "Reframe: close top-down view filling the frame with one sheet of cream parchment on the oak desk in soft daylight. A clean, simple ink drawing: one vein drawn as two smooth parallel lines running from bottom to top, with three clear pairs of small V-shaped flaps inside it, all pointing upwards, and a short red ink stream entering at the bottom. Bold, tidy lines; no scribbles, no arm outline, no arrows. $NOTEXT"
$M --part 4 still 15_your_hand_glow --seed $S/15_your_hand_glow_v01.jpg --extra "Same relaxed hand and wrist on the oak table in soft daylight, no face. The veins on the back of the hand show as soft cool blue lines under clean smooth skin with a gentle blue glow; nothing yellow or gold, no lightning. No wounds, no blood on skin. $NOTEXT"
$M --part 4 still 18_aubrey --seed $S/18_aubrey_v01.jpg --extra "Same John Aubrey, room and window. The door across the street is a plain wooden door with no sign, no lettering and no plaque; two patients walk away from it. The notebook page is soft and out of focus with no readable or garbled writing. $NOTEXT"
echo P04_STILLS_D_DONE
