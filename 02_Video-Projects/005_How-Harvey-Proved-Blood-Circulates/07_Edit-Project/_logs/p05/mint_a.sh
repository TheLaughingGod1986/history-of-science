#!/bin/zsh
# Part 05 first takes, plates 02-18, in waves of six (01 KEEP t5 first, alone).
S=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips/part05/refs/v02_vertex_stills
L=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/07_Edit-Project/_logs/p05
M=/tmp/h5/m
NOTEXT="No letters, words, numbers or writing anywhere in the picture."
CALM="The figure stays still, faceless, and keeps its shape. Thin smooth glowing lines only; no sparks, lightning, spirals, twisted or ladder shapes, no blobs, balloons or tubes."
mint() { local id=$1 still=$2; shift 2; $M --part 5 mint $id --still $S/$still --framing try1 "$@" > $L/${id[1,2]}_t1.log 2>&1 & sleep 4 }

# wave 1
mint 02_tiny_gaps 02_tiny_gaps_v01.jpg --extra "Red slowly seeps out of the artery's fine tips into the soft pink haze and blurs away, uncertain, never clearly reaching the blue vein; the camera drifts gently. Nothing sharp, nothing glowing. No wounds, no blood on skin. $NOTEXT"
mint 03_old_harvey 03_old_harvey_v01.jpg --extra "Old Harvey stays the same man the whole time: white hair, small white pointed beard, black gown, white collar. He looks down at the book and closes it gently. $NOTEXT"
mint 04_malpighi_slide 04_malpighi_slide_v01.jpg --extra "Malpighi keeps the same face, long dark curled wig, brown coat and white cravat; he slides the glass slide onto the microscope stage and turns the focus knob, leaning in. No animals anywhere. $NOTEXT"
mint 05_explorer_scope 05_explorer_scope_v01.jpg --extra "Exactly one Explorer, on model the whole time: round thin gold glasses, messy wavy brown hair, teal coat. He looks into the eyepiece, adjusts his glasses, looks again and pulls back with a gasp of wonder. No flames. $NOTEXT"
mint 06_eyepiece_mesh 06_eyepiece_mesh_v01.jpg --extra "The round eyepiece view stays fixed; red creeps slowly along the fine mesh of tiny vessels from the red artery and comes out into the blue vein. Daylight look, nothing glowing, no shapes with faces. $NOTEXT"
mint 07_capillaries_loop 07_capillaries_loop_v02.jpg --replace "they light up with a soft glow as the blood creeps through, then the camera pulls back and the glowing mesh becomes the missing link in the glowing loop: heart, arteries, capillaries, veins, and the loop closes.=>they light up with a soft glow as red creeps through them from the small artery and comes out blue into the small vein; the single hair stays still across the top for scale while the camera pulls slowly back." --extra "$CALM $NOTEXT"
wait
# wave 2
mint 08_your_blood 08_your_blood_v01.jpg --extra "Soft pulses of red glow travel out from the heart down the arms and legs, cross a fine soft glowing mesh in the hands and feet, and travel back as blue up to the heart, round and round. $CALM $NOTEXT"
mint 09_question 09_question_v02.jpg --extra "The clean cartoon heart squeezes and relaxes in a slow steady rhythm; soft red pulses run out along the arteries and blue returns along the veins. Plain dark panelling behind, no lamps. $CALM $NOTEXT"
mint 10_one_vein 10_one_vein_v01.jpg --extra "A small soft pale-blue glow starts in one vein at the inside of the left elbow, travels up to the heart and then out along every artery to the whole body, until the whole circuit carries a faint blue tint. $CALM $NOTEXT"
mint 11_transfusion 11_transfusion_v01.jpg --extra "The two physicians stay the same; one picks up the slender silver tube and turns it in the light while the other leans in and points at it. Tools only: no animal, no patient, no blood anywhere. $NOTEXT"
mint 12_tools 12_tools_v01.jpg --extra "The camera glides slowly along the silver tube and quills on the linen; the hand writes in the ledger, whose page stays edge-on and soft so nothing can be read. No blood. $NOTEXT"
mint 13_cuff 13_cuff_v01.jpg --extra "The grey cuff slowly inflates and tightens round the upper arm; the arm rests still on the white table; no face, no other hands. Clean skin. $NOTEXT"
wait
# wave 3
mint 14_cuff_release 14_cuff_release_v02.jpg --extra "The grey cuff slowly deflates and eases loose; the round metal stethoscope disc moves to the inside of the elbow and rests there, listening. Only the patient's arm and the one stethoscope; no face, no extra hands. $NOTEXT"
mint 15_band_table 15_band_table_v02.jpg --extra "The camera glides slowly across the still life from the coiled linen band to the vein drawing; nothing moves on the table and nothing is written. No candles or lamps. $NOTEXT"
mint 16_proved_last_link 16_proved_last_link_v02.jpg --replace "Harvey's painted heart chart; a glowing loop draws itself over it and runs round, and at the far end the last link, a fine glowing mesh of tiny vessels, lights up softly to close it.=>Harvey's painted heart chart on the oak table: a soft glowing red and blue loop runs round the heart, and at the far end of the page the gap in the loop fills with a fine net of tiny glowing lines that lights up softly and closes the loop." --extra "No sparkles, glitter, dust, particles or sparks; only smooth thin glowing lines. No hands. The painted heart stays exactly as it is. $NOTEXT"
mint 17_dutch_lens 17_dutch_lens_v01.jpg --extra "The merchant's hand raises the tiny brass lens plate close towards the glass sliver with its drop of pond water, catching the window light. Hand only, no face. No candles. $NOTEXT"
mint 18_pond_life 18_pond_life_v01.jpg --extra "Inside the round bright drop, the tiny faceless rods, spheres and spirals swim, wriggle and drift all the time, alive. No faces, eyes or mouths on anything. $NOTEXT"
wait
echo P05_MINT_A_DONE
