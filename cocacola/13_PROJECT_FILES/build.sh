#!/usr/bin/env bash
# Full rebuild of the Coca-Cola Short. usage: ./build.sh [--skip-3d]
set -euo pipefail
cd "$(dirname "$0")"
python3 master_vo.py
if [[ "${1:-}" != "--skip-3d" ]]; then
  python3 ../07_3D/coke_scenes.py mol_in ../07_3D/renders/mol_in
  python3 ../07_3D/coke_scenes.py mol_out ../07_3D/renders/mol_out
  python3 ../07_3D/coke_scenes.py leaves ../07_3D/renders/leaves --step 2
  python3 ../07_3D/coke_scenes.py apothecary ../07_3D/renders/apothecary --step 2
fi
python3 compose.py ../12_RENDERS/picture.mp4
python3 mix.py
ffmpeg -v error -y -i ../12_RENDERS/picture.mp4 -i ../12_RENDERS/mix.wav -c:v libx264 -preset slow -crf 18 \
  -pix_fmt yuv420p -c:a aac -b:a 256k -shortest -movflags +faststart ../12_RENDERS/FINAL_VIDEO.mp4
echo "wrote 12_RENDERS/FINAL_VIDEO.mp4"
