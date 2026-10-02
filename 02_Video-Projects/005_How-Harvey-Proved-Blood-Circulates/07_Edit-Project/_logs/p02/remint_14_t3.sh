#!/bin/zsh
M=/tmp/h5/m
while pgrep -f stills_c.sh >/dev/null; do sleep 5; done
NOTEXT="Plain pale brown ink line drawing on cream paper. No letters, words, numbers, symbols or glyphs anywhere, nothing written inside any flap."
$M --part 2 still 14_pool_feet --extra "Side-on close-up of the ink drawing of a lower leg and foot: one long vein drawn as two parallel ink lines, and inside it five pairs of small plain curved cup-shaped flaps (like tiny open pockets, Fabricius-style valve drawings), each pair a simple empty U shape. A thin smooth line of red ink runs down inside the vein and stops neatly at the first pair of flaps. Flat ink drawing, no 3D objects. $NOTEXT"
$M --part 2 mint 14_pool_feet --framing "side close-up, cup valves" --extra "The flaps are simple empty curved ink cups that close gently against the thin red ink line and hold it, staying flat ink on the paper. The red stays a thin smooth ink line, never blobs, drips or splashes. $NOTEXT"
echo T3_DONE
