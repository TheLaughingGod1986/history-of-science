#!/bin/zsh
# 04 and 05 retakes, two variants each. 04: nothing enters the forearm (helix came when red did).
# 05: red stops in the forearm, never reaches the hand (sparks came at the wrist).
S=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips/part04/refs/v02_vertex_stills
L=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/07_Edit-Project/_logs/p04
M=/tmp/h5/m
NOTEXT="No letters, words, numbers or writing anywhere in the picture."
CALM="The arm rests still on the table and keeps its shape. No twisted, spiral or ladder shapes, no sparks, crackles or flashes, no balloons, bulges or blobs. No wounds, no blood on skin, no other hands, no people."
R04="Clean glowing cutaway of the same arm: the tight band squeezes every vessel shut and the warm red stream stops dead at the band; then the band eases open just a little."
R05="Same glowing cutaway: deep arteries inside the arm push warm red under the loosened band towards the hand, while the blue veins near the skin stay pinched shut under the band and blood piles up below it."

$M --part 4 mint 04_stopped_loosen --still $S/_03t4_at3.0.jpg --framing try5_forearm_unchanged --quality Quality \
  --replace "$R04=>Same glowing cutaway: the warm red glow fills the upper arm and stops dead at the tight cream band. Then the band's knot slackens and the band eases a little looser, still wrapped round the arm. The forearm and hand below the band stay exactly as they are the whole time: pale grey with faint thin blue lines, and nothing new appears in them." \
  --extra "The band never comes off or unwinds. $CALM $NOTEXT" > $L/04_t5.log 2>&1 &
sleep 5
$M --part 4 mint 04_stopped_loosen --still $S/_03t4_at4.0.jpg --framing try6_close_band_eases --quality Quality \
  --replace "$R04=>Same glowing cutaway, close on the band: the warm red glow in the upper arm presses up against the tight cream band and stops dead there. Then the band's knot slackens and the band eases a little looser, still wrapped round the arm. The pale grey forearm stays exactly as it is, and nothing new appears in it. The camera stays close on the band." \
  --extra "The band never comes off or unwinds. $CALM $NOTEXT" > $L/04_t6.log 2>&1 &
sleep 5
$M --part 4 mint 05_arteries_veins_shut --still $S/_04t4_at4.4.jpg --framing try6_from_04t4_red_under_band --quality Quality \
  --replace "$R05=>Same glowing cutaway, the band a little looser: a single smooth red line slowly slides from the upper arm, under the band, and a short way on into the forearm, deep in the middle of the arm, while the bright blue lines near the surface stay where they are and stop at the band. The red stays well short of the wrist. The camera stays close and still." \
  --extra "$CALM $NOTEXT" > $L/05_t6.log 2>&1 &
sleep 5
$M --part 4 mint 05_arteries_veins_shut --still $S/_03t4_at3.0.jpg --framing try7_from_03t4_red_midarm --quality Quality \
  --replace "$R05=>Same glowing cutaway, the band a little looser: a single smooth deep red line slowly slides from the upper arm, under the band, and on to the middle of the forearm, where it stops, well short of the wrist; the thin blue lines near the surface stay dim and still. The hand stays pale grey and plain the whole time." \
  --extra "$CALM $NOTEXT" > $L/05_t7.log 2>&1 &
wait
echo MINT_K_DONE
