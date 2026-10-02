#!/bin/zsh
F=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips
S=$F/part04/refs/v02_vertex_stills
M=/tmp/h5/m
latest() { ls -t $S/$1_v*.jpg 2>/dev/null | head -1 }
NOTEXT="No letters, words, numbers or writing anywhere in the picture."
ARM="A man's bare forearm and hand resting palm-up on a dark oak table in soft window daylight, seen close; no face, no person beyond the arm; clean smooth cartoon skin, no wounds, no blood on skin, no cuts."
CUT="Clean glowing cutaway illustration of a forearm on the oak table, as in the earlier cutaways: translucent skin, warm red arteries deep inside, cool blue veins near the surface. No gore, no wounds, no open flesh."

$M --part 4 still 02_linen_tie --extra "Harvey seen from chest down, only his hands and black sleeves with white cuffs, tying a plain cream linen band round the bare upper arm of a seated man whose face is out of frame. $NOTEXT"
$M --part 4 still 03_hand_pale --seed $(latest 02_linen_tie) --extra "$ARM The cream linen band is tied tight round the upper arm at the top of frame; the hand below is slightly pale. $NOTEXT"
A=$(latest 03_hand_pale)
$M --part 4 still 06_veins_swell --seed $A --extra "$ARM The same arm and band; the veins on the forearm below the band stand out as soft blue cords, the hand pink. $NOTEXT"
$M --part 4 still 09_push_stops --seed $A --extra "$ARM The same arm and band, closer on the forearm: a raised blue vein with small knots along it; one fingertip of another hand rests on the vein. $NOTEXT"
$M --part 4 still 10_slides_heart --seed $A --extra "$ARM The same raised blue vein with knots; one fingertip rests on the vein, ready to stroke towards the elbow. $NOTEXT"
$M --part 4 still 11_two_fingers --seed $A --extra "$ARM The same raised blue vein; two fingertips of another hand press side by side on a short stretch of it. $NOTEXT"
$M --part 4 still 12_stays_fills --seed $A --extra "$ARM The same raised blue vein; two fingertips a short way apart press it, and the stretch between them is flat and empty. $NOTEXT"
C=$F/part03/refs/v02_vertex_stills/04_squeeze_pulse_v03.jpg
$M --part 4 still 04_stopped_loosen --seed $C --extra "$CUT A cream linen band tied tight round the upper arm; the red stream stops at the band. $NOTEXT"
$M --part 4 still 05_arteries_veins_shut --seed $C --extra "$CUT A loosened cream linen band round the upper arm; deep red arteries pass under it, the blue surface veins pinched under it. $NOTEXT"
$M --part 4 still 07_in_out_doors --seed $C --extra "$CUT Red flows deep, blue flows near the skin in a simple loop; inside one blue vein a pair of small cup-shaped valve flaps. $NOTEXT"
$M --part 4 still 08_knots_valve --seed $A --extra "$ARM Close on the swollen blue vein on the forearm with small knots standing out along it. $NOTEXT"
$M --part 4 still 13_one_way --seed $C --extra "$CUT One long blue vein runs up the forearm with many pairs of small cup-shaped valve flaps, all open towards the elbow. $NOTEXT"
$M --part 4 still 14_steering_home --seed $F/part02/refs/v02_vertex_stills/14_pool_feet_v04.jpg --extra "Two ink drawings side by side on an oak desk: on the left an old brown ink drawing of a leg vein with cup valves, on the right a fresh drawing of a vein with cup valves and a thin red ink line running up through them. Plain line drawings. $NOTEXT"
$M --part 4 still 15_your_hand_glow --extra "Close on the back of a relaxed hand and inside of the wrist resting on dark oak in soft daylight; faint blue veins under clean smooth cartoon skin; no face. $NOTEXT"
$M --part 4 still 16_press_book --extra "A wooden hand printing press in a timbered Frankfurt workshop by day; a small printed sheet lies on the press bed, its type shown only as soft grey blocks, nothing readable. Plain blank title page. $NOTEXT"
$M --part 4 still 18_aubrey --extra "John Aubrey, a man with a long brown wig and brown coat, writes in a notebook at a window desk; through the window across the street a plain dark door. The notebook page is seen edge-on. $NOTEXT"
$M --part 4 still 01_college_demo --extra "Harvey at the front of the same panelled lecture room by day, rows of gowned physicians on benches seen from behind; a plain blank linen strip in his hands. $NOTEXT"
$M --part 4 still 17_whispers --extra "A timbered 1620s London street by day; Harvey walks past in his black gown while two people in period clothes lean together and point. No shop signs with lettering. $NOTEXT"
$M --part 4 still 19_gap_open --extra "Harvey at a leaded window in late-afternoon daylight, holding a plain ink drawing of a red and blue loop with one small gap in it. $NOTEXT"
echo P04_STILLS_DONE
