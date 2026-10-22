#!/bin/bash
cd ~/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates
G=04_Generated-Clips/part04
PY=~/.venvs/hos-vo/bin/python
( for n in 03_hand_pale_t4 04_stopped_loosen_t5 05_arteries_veins_shut_t7; do
    $PY $G/graded_v04/grade_arm_v04.py $G/raw/v01/$n.mp4 $G/graded_v04/${n}_graded_v04.mp4 < /dev/null
  done; echo RENDER_DONE ) > $G/graded_v04/render.log 2>&1 &
( HF_HUB_OFFLINE=1 $PY ~/YouTube/hos-005-blood/00_Brand/Channel-Setup/tools/vo_check.py 02_Voiceover/part04_the_tied_arm_v02.mp3 --script 01_Script/blood_script_master_v03.md --part 4 < /dev/null; echo EXIT $? ) > ~/YouTube/hos-005-blood/_v02work/vocheck_p04_v02.txt 2>&1 &
wait
