#!/bin/zsh
# Arm cutaway plates 03/04/05/07 (glows: Quality) and 15 plain skin (Fast) from stills_h frames.
S=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips/part04/refs/v02_vertex_stills
L=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/07_Edit-Project/_logs/p04
M=/tmp/h5/m
NOTEXT="No letters, words, numbers or writing anywhere in the picture."
CUT="The arm stays the same shape and size the whole time: clean translucent skin, glowing lines stay thin and inside the arm. No balloons, bulges, blobs, spheres, eyes, zigzag traces, lightning or helix. No wounds, no blood on skin, no other hands, no people."

$M --part 4 mint 03_hand_pale --still $S/03_hand_pale_v05.jpg --framing try4_cutaway_dim_hand --quality Quality \
  --replace "Same arm: below the band the hand slowly turns pale and cool; above the band a soft pulse throbs under the skin. Arm only, clean skin.=>Same arm as a clean glowing cutaway, the cream band tied tight round the upper arm. Below the band the blue lines in the forearm slowly fade and the hand turns pale grey and cool; above the band a warm red glow gently brightens and dims in a slow, steady rhythm. The camera drifts slowly along the arm from the hand towards the band." \
  --extra "$CUT $NOTEXT" > $L/03_t4.log 2>&1 &
sleep 5
$M --part 4 mint 04_stopped_loosen --still $S/03_hand_pale_v05.jpg --framing try3_red_stops_at_band --quality Quality \
  --replace "Clean glowing cutaway of the same arm: the tight band squeezes every vessel shut and the warm red stream stops dead at the band; then the band eases open just a little.=>Clean glowing cutaway of the same arm: a warm red stream flows down the upper arm and stops dead at the tight cream band, with no red at all below it in the forearm; then the band's knot loosens and the band eases open just a little." \
  --extra "$CUT $NOTEXT" > $L/04_t3.log 2>&1 &
sleep 5
$M --part 4 mint 05_arteries_veins_shut --still $S/05_arteries_veins_shut_v04.jpg --framing try4_deep_red_on --quality Quality \
  --replace "Same glowing cutaway: deep arteries inside the arm push warm red under the loosened band towards the hand, while the blue veins near the skin stay pinched shut under the band and blood piles up below it.=>Same glowing cutaway, the band a little looser: warm red light travels along the deep lines inside the arm, under the band and on down the forearm to the hand, while the thin blue lines near the surface stay dim and still at the band. The camera glides slowly from the band down to the hand." \
  --extra "$CUT $NOTEXT" > $L/05_t4.log 2>&1 &
sleep 5
$M --part 4 mint 07_in_out_doors --still $S/07_in_out_doors_v05.jpg --framing try2_simple_loop --quality Quality \
  --replace "Clean glowing cutaway of the arm: red flows in deep down, blue flows back out near the skin, a simple loop; the camera then glides along a blue vein towards a pair of little doors inside it.=>Clean glowing cutaway of the arm, no band: warm red light travels deep inside the arm down towards the hand, and cool blue light travels back near the surface up towards the elbow, a simple loop. The camera glides slowly along the forearm." \
  --extra "$CUT $NOTEXT" > $L/07_t2.log 2>&1 &
sleep 5
$M --part 4 mint 15_your_hand_glow --still $S/15_your_hand_glow_v03.jpg --framing try4_plain_skin_follow --quality Fast \
  --replace "veins faintly blue under clean skin; a soft warm glow moves along the veins from the hand up the wrist towards the arm, on its way home.=>veins faintly blue under clean skin. The camera glides slowly from the knuckles up over the wrist and along the forearm towards the elbow, following the blue veins home." \
  --extra "The hand stays relaxed and still on the table. No glow, no light effects, no sparks, no lightning, no helix, no shapes; just natural skin with faint blue veins. No other hands, no people. Clean skin, no wounds, no blood on skin. $NOTEXT" > $L/15_t4.log 2>&1 &
wait
echo MINT_H_DONE
