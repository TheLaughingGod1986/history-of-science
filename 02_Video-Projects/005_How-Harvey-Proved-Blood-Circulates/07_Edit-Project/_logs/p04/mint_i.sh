#!/bin/zsh
# Retakes: 04/05 from 03 t4's grey-forearm frame (continuity), 12 parchment without drips, 15 knuckles-to-wrist only.
S=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips/part04/refs/v02_vertex_stills
L=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/07_Edit-Project/_logs/p04
M=/tmp/h5/m
F03=$S/_03t4_at3.0.jpg
NOTEXT="No letters, words, numbers or writing anywhere in the picture."
CUT="The arm stays the same shape and size the whole time, resting still on the table. Glowing lines stay thin and inside the arm. The hand stays plain, with no glow, branching, sparks or lightning in it. No balloons, bulges, blobs, spheres, zigzag traces or helix. No wounds, no blood on skin, no other hands, no people."
FLAPS="Every flap keeps exactly its shape and size the whole time: upright paired paper petals, never flattening, never turning into hearts or other shapes. Ink and parchment only, nothing glowing, soft daylight."

$M --part 4 mint 04_stopped_loosen --still $F03 --framing try4_from_03t4_band_eases --quality Quality \
  --replace "Clean glowing cutaway of the same arm: the tight band squeezes every vessel shut and the warm red stream stops dead at the band; then the band eases open just a little.=>Same glowing cutaway: the warm red glow fills the upper arm and stops dead at the tight cream band; the forearm and hand below it stay pale grey with no red at all. Then the band's knot slackens and the band eases a little looser, still wrapped round the arm." \
  --extra "The band never comes off or unwinds; it only loosens slightly. $CUT $NOTEXT" > $L/04_t4.log 2>&1 &
sleep 5
$M --part 4 mint 05_arteries_veins_shut --still $F03 --framing try5_from_03t4_one_deep_line --quality Quality \
  --replace "Same glowing cutaway: deep arteries inside the arm push warm red under the loosened band towards the hand, while the blue veins near the skin stay pinched shut under the band and blood piles up below it.=>Same glowing cutaway, the band a little looser: one smooth deep red line travels from the upper arm under the band and slowly on down the middle of the forearm towards the wrist, while the thin blue lines near the surface stay dim and still. The camera glides slowly along the forearm from the band towards the wrist." \
  --extra "$CUT $NOTEXT" > $L/05_t5.log 2>&1 &
sleep 5
$M --part 4 mint 12_stays_fills --still $S/12_stays_fills_v06.jpg --framing try3_parchment_no_drip --quality Fast \
  --replace "Same stretch of vein stays flat and empty between the two fingertips; then the finger nearer the hand lifts and the stretch refills from below, from the hand side, in one smooth wave. Clean skin.=>Close on a vein drawn in brown ink on cream parchment with small upright pairs of 3D paper flaps along it. The pale empty stretch between Harvey's two fingertips stays empty for a moment; then the left fingertip lifts a little off the page and the red ink already inside the drawn vein on the left slides along it into the pale stretch in one smooth wave, staying between the two drawn lines." \
  --extra "Nothing drips, pours or falls; nothing comes from above; the red only moves inside the drawn vein. The camera stays still and close on the page. Only Harvey's one hand, from a jet-black sleeve with a plain white cuff, the whole time; no other hands, no people. $FLAPS $NOTEXT" > $L/12_t3.log 2>&1 &
sleep 5
$M --part 4 mint 15_your_hand_glow --still $S/15_your_hand_glow_v03.jpg --framing try5_knuckles_to_wrist --quality Fast \
  --replace "veins faintly blue under clean skin; a soft warm glow moves along the veins from the hand up the wrist towards the arm, on its way home.=>veins faintly blue under clean skin. The camera glides slowly from the knuckles over the back of the hand to the wrist, following the faint blue veins towards the arm." \
  --extra "The hand stays relaxed, palm down and still on the table the whole time. The white cuff and black sleeve stay exactly as they are; the camera never goes past the cuff. No glow, no light effects, no sparks, no lightning, no helix, no shapes; just natural skin with faint blue veins. No other hands, no people. Clean skin, no wounds, no blood on skin. $NOTEXT" > $L/15_t5.log 2>&1 &
wait
echo MINT_I_DONE
