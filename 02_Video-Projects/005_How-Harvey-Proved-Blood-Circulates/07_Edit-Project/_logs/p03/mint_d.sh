#!/bin/zsh
S=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips/part03/refs/v02_vertex_stills
L=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/07_Edit-Project/_logs/p03
M=/tmp/h5/m
$M --part 3 mint 03_stove_to_muscle --still $S/03_stove_to_muscle_from_p02_05_last.jpg --framing "push close, fist beats" \
  --replace "cools and turns into a strong, clean cartoon heart muscle that squeezes firmly, again and again=>cools and the stove melts away while the camera pushes in close on the heart alone; then the heart squeezes hard like a clenching fist, shrinking visibly, and springs back, three big slow beats" \
  --extra "Only the heart fills the frame at the end: no lungs, no trace lines, no zigzags. Every beat is a big obvious squeeze of the whole muscle. Clean, no gore. No letters, words, numbers or writing." > $L/03_t3.log 2>&1 &
sleep 3
$M --part 3 mint 07_thousand_beats --still $S/07_thousand_beats_v01.jpg --framing "already written, quill lifts away" \
  --replace "the quill writes '1000' under '2 oz' and '1/8' in large clear brown ink; a brass clock ticks beside the page=>the page already reads '2 oz', '1/8' and '1000'; the quill lifts off the page and moves away out of frame, and the brass pocket watch beside the page ticks as the camera pushes slowly in on the numbers" \
  --extra "Nothing new is written and nothing on the page changes: '2 oz', '1/8' and '1000' stay exactly as they are, clean and sharp. No hands enter the frame." > $L/07_t3.log 2>&1 &
wait
echo MINT_D_DONE
