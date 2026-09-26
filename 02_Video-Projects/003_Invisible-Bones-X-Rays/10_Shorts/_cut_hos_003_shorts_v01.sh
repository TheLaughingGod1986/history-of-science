#!/bin/bash
set -euo pipefail
ROOT="/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/003_Invisible-Bones-X-Rays"
EXP="$ROOT/09_Final-Export"
OUT="$ROOT/10_Shorts"
ICLOUD="/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
VF='scale=1920:1080,crop=608:1080:656:0,scale=1080:1920:flags=lanczos'

cut_one() {
  local id="$1" src="$2" start="$3" dur="$4" title="$5"
  local dest="$OUT/${id}.mp4"
  echo "CUT $id start=$start dur=$dur from $(basename "$src")"
  ffmpeg -y -ss "$start" -i "$src" -t "$dur" \
    -vf "$VF" \
    -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
    -c:a aac -b:a 192k -movflags +faststart \
    "$dest" 2>"$OUT/_log_${id}.txt"
  local sha size seconds
  sha=$(shasum -a 256 "$dest" | awk '{print $1}')
  size=$(stat -f%z "$dest")
  seconds=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "$dest")
  cp -f "$dest" "$ICLOUD/"
  local isha
  isha=$(shasum -a 256 "$ICLOUD/$(basename "$dest")" | awk '{print $1}')
  echo "$id|$dest|$sha|$seconds|$size|$start|$dur|$title|icloud=$isha"
}

# verify sources
P02="$EXP/hos_003_part02_rough_v03.mp4"
P03="$EXP/hos_003_part03_rough_v02.mp4"
P04="$EXP/hos_003_part04_rough_v03.mp4"
test -f "$P02" && test -f "$P03" && test -f "$P04"

REPORT="$OUT/_cut_report.tsv"
: > "$REPORT"
# Windows chosen for beat: skip ~chapter open; land in motion
cut_one hos_003_s1_cardboard_glow_v01 "$P02" 18.0 24.0 "Why Did This Cardboard Glow in the Dark?" | tee -a "$REPORT"
cut_one hos_003_s2_bones_no_knife_v01 "$P03" 22.0 24.0 "How Can You See Bones Without a Knife?" | tee -a "$REPORT"
cut_one hos_003_s3_bertha_ring_v01 "$P04" 14.0 24.0 "Why Is There a Ring on the First X-ray?" | tee -a "$REPORT"
echo DONE_SHORTS
