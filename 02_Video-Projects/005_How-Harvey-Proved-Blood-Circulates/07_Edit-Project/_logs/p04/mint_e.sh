#!/bin/zsh
S=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips/part04/refs/v02_vertex_stills
L=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/07_Edit-Project/_logs/p04
M=/tmp/h5/m
NOTEXT="No letters, words, numbers or writing anywhere in the picture."

$M --part 4 mint 15_your_hand_glow --still $S/15_your_hand_glow_v02.jpg --framing try3_no_glow_follow --quality Fast --replace "veins faintly blue under clean skin; a soft warm glow moves along the veins from the hand up the wrist towards the arm, on its way home.=>veins faintly blue under clean skin. The camera glides slowly from the knuckles up over the wrist and along the forearm towards the elbow, following the blue veins home." --extra "The hand stays relaxed and still on the table. No glow, no light effects, no sparks, no lightning, no helix, no shapes rising from the arm; just natural skin with faint blue veins. Clean skin, no wounds, no blood on skin. $NOTEXT" > $L/15_t3.log 2>&1 &
sleep 3
$M --part 4 mint 18_aubrey --still $S/18_aubrey_v02.jpg --framing try2_plain_door --extra "The door across the street stays a plain wooden door with no sign, plaque or lettering; a couple of patients walk away from it. The notebook page stays soft and out of focus with no readable or garbled writing. $NOTEXT" > $L/18_t3.log 2>&1 &
wait
echo MINT_E_DONE
