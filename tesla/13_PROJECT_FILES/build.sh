#!/usr/bin/env bash
# Full rebuild. Assumes 01_VO/RAW_VO.mp3 and the downloaded assets (04_BROLL, 02_MUSIC, 03_SFX, 05_PHOTOS, 06_ARCHIVE).
# usage: ./build.sh [--skip-3d]
set -euo pipefail
cd "$(dirname "$0")"
python3 master_vo.py
if [[ "${1:-}" != "--skip-3d" ]]; then
  for s in year2003 doorway names; do python3 ../07_3D/tesla_scenes.py $s ../07_3D/renders/$s --res 720x1280 --samples 16; done
  python3 ../07_3D/tesla_scenes.py network ../07_3D/renders/network --res 720x1280 --samples 10
fi
python3 compose.py ../12_RENDERS/picture.mp4
python3 mix.py
ffmpeg -v error -y -i ../12_RENDERS/picture.mp4 -i ../12_RENDERS/mix.wav -c:v libx264 -preset slow -crf 18 \
  -pix_fmt yuv420p -c:a aac -b:a 256k -shortest -movflags +faststart ../12_RENDERS/FINAL_VIDEO.mp4
echo "wrote 12_RENDERS/FINAL_VIDEO.mp4"
