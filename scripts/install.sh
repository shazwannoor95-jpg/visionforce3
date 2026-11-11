#!/usr/bin/env bash
set -euo pipefail
cd /workspace/visionforce3
export npm_config_cache=/workspace/.npm-cache
npm --prefix video ci --no-audit --no-fund
npm --prefix modules/browser ci --no-audit --no-fund
command -v ffmpeg
command -v ffprobe
command -v chromium
python3 -c 'import pypdf, docx'
