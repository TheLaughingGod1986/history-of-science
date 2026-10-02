#!/bin/zsh
S=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/04_Generated-Clips/part03/refs/v02_vertex_stills
L=/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/07_Edit-Project/_logs/p03
M=/tmp/h5/m
NOTEXT="No letters, words, numbers or writing anywhere in the picture."

$M --part 3 mint 02_slow_hearts --still $S/02_slow_hearts_v04.jpg --framing "hold on open pages, no page turn" \
  --replace "brown-ink drawings of the slow hearts of a frog and an eel with little sketch arrows; pages turn gently, and on the last page the ink drawing of the heart slowly squeezes and relaxes on the paper=>two plain brown-ink heart drawings with little sketch arrows; the camera holds close on the open pages, no page turns, and the ink heart on the right page slowly squeezes and relaxes on the paper" \
  --extra "Every drawing is a heart only. The pages stay blank apart from the heart sketches and arrows: no zigzag lines, no traces. The background is a plain dark oak-panelled wall: no candles, no lights. $NOTEXT" > $L/02_t2.log 2>&1 &
sleep 3
$M --part 3 mint 03_stove_to_muscle --still $S/03_stove_to_muscle_from_p02_05_last.jpg --framing "heart alone, big squeeze" \
  --extra "The little stove and its fire fade away completely in the first two seconds, leaving the cartoon heart alone in the chest (no lungs). From then on the heart muscle clearly contracts hard and relaxes about once a second, getting visibly smaller and bigger with every beat, right to the last frame. Clean, no gore. $NOTEXT" > $L/03_t2.log 2>&1 &
sleep 3
$M --part 3 mint 07_thousand_beats --still $S/07_thousand_beats_from_06_last.jpg --framing "from 06 last frame" \
  --extra "The '2 oz' and '1/8' already on the page stay exactly as they are, clean and unchanged. The quill writes '1000' underneath them in the same large clear brown ink. No blots, smudges or other marks; nothing else is written. The pocket watch beside the page ticks; its face has plain tick marks." > $L/07_t2.log 2>&1 &
wait
echo MINT_B_DONE
