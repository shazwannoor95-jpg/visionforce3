#!/usr/bin/env bash
set -euo pipefail
cd /workspace/visionforce3
mkdir -p artifacts
npm --prefix video run typecheck
npm --prefix video run render -- --browser-executable=/usr/bin/chromium
ffprobe -v error -count_frames -show_entries stream=codec_name,width,height,r_frame_rate,nb_read_frames:format=duration,size -of json artifacts/visionforge3-smoke.mp4 > artifacts/ffprobe.json
python3 - <<'PY'
import json
s=json.load(open('artifacts/ffprobe.json'))['streams'][0]
assert (s['width'],s['height'],s['r_frame_rate'],s['nb_read_frames'])==(1920,1080,'30/1','120')
PY
ffmpeg -v error -i artifacts/visionforge3-smoke.mp4 -f null -
npm --prefix modules/browser run smoke
