MOTION ATLAS — locked runtime, 922 presets

Use Python/FFmpeg for footage editing; HTML/GSAP for vector/cartoon animation.
python scripts/atlas_preset.py check jobs/T01.json
python scripts/atlas_preset.py render jobs/T01.json --output title.mp4
python scripts/atlas_preset.py import-config configs/T01.json --output custom-job.json
python scripts/atlas_preset.py verify jobs/T01.json --video title.mp4 --report qa.json

Read references/atlas-python-runtime.md. Keep the original renderer and lock together. Do not bypass validation or regenerate baselines to hide mismatches. Only supported parameters may change. Native 16:9; no silent crop/stretch. Footage requires real inputs, cues, alpha/tracking where required. Rendered layers are silent; mix original audio separately.

Current published 922 videos checked at three decoded frames against the pinned renderer; this is sampled verification, not proof of every frame or every custom layout.

Download optional VL/MA/font asset packs only when needed. Cache existing verified files first.
