#!/usr/bin/env bash
set -euo pipefail
cd /workspace/visionforce3
export npm_config_cache=/workspace/.npm-cache
export KM_HYPERFRAMES_RUNTIME=/workspace/argon-runtime/hyperframes-0.9.4
node .agents/skills/buat-video-motion-grafik-gemini/scripts/setup_hyperframes.mjs --runtime "$KM_HYPERFRAMES_RUNTIME" --browser /usr/bin/chromium --online
