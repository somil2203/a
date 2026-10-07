#!/usr/bin/env bash
# Full rebuild of the Nokia Short: 3D shots -> graphics/captions -> audio -> mux.
# usage: ./build.sh RAW.mp4 [--skip-3d]
set -euo pipefail
cd "$(dirname "$0")"
SRC="$1"
export R3D="${R3D:-$PWD/r3d}"
OUT=../output
mkdir -p "$OUT" "$R3D"
if [[ "${2:-}" != "--skip-3d" ]]; then
  python3 blender/scenes.py turntable "$R3D/turntable" --res 600x600 --samples 24
  python3 blender/scenes.py nokia_still "$R3D/nokia_still" --res 600x600 --samples 32
  python3 blender/scenes.py iphone_still "$R3D/iphone_still" --res 600x600 --samples 32
  for s in village battery drop iphone; do
    python3 blender/scenes.py "$s" "$R3D/$s" --res 720x1280 --samples 24
  done
fi
python3 render_video.py "$SRC" /tmp/nokia_silent.mp4
python3 render_audio.py "$SRC" /tmp/nokia_mix.wav
ffmpeg -v error -y -i /tmp/nokia_silent.mp4 -i /tmp/nokia_mix.wav -c:v libx264 -preset slow -crf 22 \
  -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT/nokia_short_3d.mp4"
echo "wrote $OUT/nokia_short_3d.mp4"
