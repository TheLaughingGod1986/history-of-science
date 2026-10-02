#!/bin/zsh
S=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips/part04/refs/v02_vertex_stills
L=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/07_Edit-Project/_logs/p04
M=/tmp/h5/m
NOTEXT="No letters, words, numbers or writing anywhere in the picture."

$M --part 4 mint 15_your_hand_glow --still $S/15_your_hand_glow_v02.jpg --framing try2_blue --replace "a soft warm glow moves along the veins=>a soft cool blue glow drifts gently along the veins" --extra "The hand stays relaxed and still on the table and stays in frame; the camera eases slowly along the wrist towards the arm. Smooth soft light, never gold, yellow or lightning-like. Clean skin, no wounds, no blood on skin. $NOTEXT" > $L/15_t2.log 2>&1 &
sleep 3
$M --part 4 mint 18_aubrey --still $S/18_aubrey_v02.jpg --framing try2_plain_door --extra "The door across the street stays a plain wooden door with no sign, plaque or lettering; a couple of patients walk away from it. The notebook page stays soft and out of focus with no readable or garbled writing. $NOTEXT" > $L/18_t2.log 2>&1 &
wait
echo MINT_D_DONE
