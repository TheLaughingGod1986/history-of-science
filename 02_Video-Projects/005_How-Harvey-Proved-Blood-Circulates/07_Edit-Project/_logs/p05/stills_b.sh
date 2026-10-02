#!/bin/zsh
F=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips
S=$F/part05/refs/v02_vertex_stills
M=/tmp/h5/m
NOTEXT="No letters, words, numbers or writing anywhere in the picture."
CLOSE=$S/_p03_13t3_at4.jpg
CALM="Clean and calm: thin smooth glowing lines; no sparks, lightning, spirals, twisted or ladder shapes, no blobs or balloons, no eyes or face."

$M --part 5 still 07_capillaries_loop --style-ref $S/06_eyepiece_mesh_v01.jpg --extra "Extreme close-up, magnified, filling the whole frame: a fine net of tiny soft red-to-blue vessels, much thinner than hairs, joining one small red artery entering from the left to one small blue vein leaving on the right, on a soft warm pale pink background. One single straight brown human hair lies across the upper part of the frame for scale, clearly thicker than every vessel. No figure, no body, no room, no sand-glass, no other objects. $CALM $NOTEXT"
$M --part 5 still 09_question --seed $CLOSE --extra "Closer on the chest of the same faceless translucent figure in the same dark oak-panelled room: the clean red cartoon heart in the middle with red arteries and blue veins leading out and back. Plain dark panelling behind, softly out of focus: no lamps, lampshades, candles, furniture, ring, circle, sand-glass or clock. $CALM $NOTEXT"
$M --part 5 still 14_cuff_release --seed $S/13_cuff_v01.jpg --extra "The same single bare arm resting on the same white table in the same bright clinic, framed from shoulder to hand; the grey cuff sits loose round the upper arm; the round metal disc of a stethoscope rests at the inside of the elbow, held by one gloved hand entering from the bottom edge. Only that one gloved hand besides the patient's arm; no other hands, no face, no torso. $NOTEXT"
$M --part 5 still 15_band_table --extra "Still life on an old dark oak table in soft warm daylight, shallow depth of field: a plain strip of cream linen lies coiled sharp in the foreground; behind it, an old brown-ink drawing of a vein with small paired paper flaps; at the very back, a sheet of paper lies face down. $NOTEXT No candles, lamps or flames."
$M --part 5 still 16_proved_last_link --seed $F/part01/refs/v02_vertex_stills/09_heart_clock_v02.jpg --extra "Top-down view of the same painted red heart on the cream page on the dark oak table; nothing else on the table: no watch, no clock, no hands, no sparkles, no rings. A thin red painted line leaves the heart and curves round the page, and a thin blue painted line curves back towards it, forming an open loop with a small gap at the far end of the page. Soft warm daylight. $NOTEXT"
echo P05_STILLS_B_DONE
