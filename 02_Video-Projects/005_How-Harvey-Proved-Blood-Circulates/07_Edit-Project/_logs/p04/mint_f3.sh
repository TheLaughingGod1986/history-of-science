#!/bin/zsh
# Valve plates 09-13 on Part 02's passed paper-flap parchment look (08 t4 KEEP on Fast).
S=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips/part04/refs/v02_vertex_stills
L=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/07_Edit-Project/_logs/p04
M=/tmp/h5/m
NOTEXT="No letters, words, numbers or writing anywhere in the picture."
FLAPS="Every flap keeps exactly its shape and size the whole time: upright paired paper petals, never flattening, never turning into hearts or other shapes. Ink and parchment only, nothing glowing, soft daylight."
ONEHAND="Only Harvey's one hand, from a jet-black sleeve with a plain white cuff; no other hands, no people."

$M --part 4 resume 09_push_stops 3 > $L/09_t3.log 2>&1 &
sleep 2
$M --part 4 resume 10_slides_heart 3 > $L/10_t3.log 2>&1 &
sleep 2
$M --part 4 resume 14_steering_home 3 > $L/14_t3.log 2>&1 &
sleep 4
$M --part 4 mint 11_two_fingers --still $S/11_two_fingers_v06.jpg --framing try3_parchment_flaps --quality Fast \
  --replace "Two fingertips press a short stretch of the vein and slide apart, emptying it. Clean skin.=>Close on a vein drawn in brown ink on cream parchment, filled with red ink, with small upright pairs of 3D paper flaps along it. Two of Harvey's fingertips press the drawn vein side by side, then slide apart along it; the stretch between them is left empty and pale cream." \
  --extra "$FLAPS $ONEHAND $NOTEXT" > $L/11_t3.log 2>&1 &
sleep 4
$M --part 4 mint 12_stays_fills --still $S/12_stays_fills_v06.jpg --framing try2_parchment_flaps --quality Fast \
  --replace "Same stretch of vein stays flat and empty between the two fingertips; then the finger nearer the hand lifts and the stretch refills from below, from the hand side, in one smooth wave. Clean skin.=>Close on a vein drawn in brown ink on cream parchment with small upright pairs of 3D paper flaps along it. The pale empty stretch between Harvey's two fingertips stays empty; then the left fingertip lifts and red ink flows back into the empty stretch from the left in one smooth wave." \
  --extra "$FLAPS $ONEHAND $NOTEXT" > $L/12_t2.log 2>&1 &
sleep 4
$M --part 4 mint 13_one_way --still $S/13_one_way_v03.jpg --framing try2_parchment_flaps --quality Fast \
  --replace "Clean glowing cutaway: a long vein with many pairs of little doors, all opening the same way towards the heart as the blood flows home.=>A long vein drawn in brown ink on cream parchment runs diagonally up the page with many upright pairs of 3D paper flaps, all opening the same way, towards the top of the page, as a red ink stream flows steadily through them towards the top. The camera glides gently up along the vein." \
  --extra "$FLAPS No hands. $NOTEXT" > $L/13_t2.log 2>&1 &
wait
echo MINT_F_DONE
