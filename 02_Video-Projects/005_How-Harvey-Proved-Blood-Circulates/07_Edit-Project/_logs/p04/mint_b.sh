#!/bin/zsh
S=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips/part04/refs/v02_vertex_stills
L=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/07_Edit-Project/_logs/p04
M=/tmp/h5/m
NOTEXT="No letters, words, numbers or writing anywhere in the picture."
ARM="Arm and hand only, no face. Warm natural peach skin, clean, smooth and unbroken the whole time: no wound, no cut, no blood or red marks on the skin, no needle. The vein stays under the skin. Any hand of Harvey's is in a black sleeve with a white cuff."
PUSH="The camera eases in closer on the forearm."

$M --part 4 mint 03_hand_pale --still $S/03_hand_pale_v04.jpg --framing try2_no_hands --extra "No hands but the patient's. The pulse above the band shows only as a gentle rhythmic swelling of the skin, with no glowing lines, symbols or zigzags; the hand below the band fades to a paler, cooler skin tone, never purple or white. $ARM $NOTEXT" > $L/03_t2.log 2>&1 &
sleep 3
$M --part 4 mint 09_push_stops --still $S/09_push_stops_v04.jpg --framing try2_glide --replace "a fingertip presses the vein and pushes the blood towards the hand; it stops dead at the next knot, which bulges.=>Harvey's fingertip glides gently along the soft blue vein towards the patient's hand, and the vein stays full and stops at the next small knot, which rounds up softly." --extra "$PUSH $ARM $NOTEXT" > $L/09_t2.log 2>&1 &
sleep 3
$M --part 4 mint 10_slides_heart --still $S/10_slides_heart_v04.jpg --framing try2_no_red --extra "$PUSH The vein is a soft blue cord under the skin; nothing red appears on the skin, no beads or dots. $ARM $NOTEXT" > $L/10_t2.log 2>&1 &
sleep 3
$M --part 4 mint 11_two_fingers --still $S/11_two_fingers_v04.jpg --framing try2_black_sleeve --extra "$PUSH The emptied stretch of vein goes flat and pale under the skin. $ARM $NOTEXT" > $L/11_t2.log 2>&1 &
wait
echo MINT_B_DONE
