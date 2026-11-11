# Jalankan asas V3.5

Gunakan checkout sedia ada /workspace/visionforce3; jangan cipta worktree tanpa arahan pengguna. Dependencies sedia ada yang berfungsi boleh digunakan semula.

Jika perlu pulih dependency: buat venv projek, pasang `python3 -m pip install -r core/requirements.txt -r tests/requirements.txt` dalam venv, kemudian `npm_config_cache=/workspace/.npm-cache npm --prefix video ci --ignore-scripts --no-audit --no-fund`. Chromium sistem, FFmpeg/FFprobe dengan libx264/AAC dan Node 24 diperlukan; gunakan pengurus pakej distro jika tiada. Jangan disable TLS/checksum. Pakej Python dipin, wheel hash belum dikunci untuk profil deployment baharu.

Ujian: `python3 -m unittest discover -s tests -v`, `npm --prefix video run typecheck`, `python3 -m tests.smoke_pipeline` (render sebenar beberapa saat). Reportlab hanya dependency ujian fixture, bukan syarat parser produksi.

API worker pembangunan: `python3 -m core.server --storage .data/jobs --port 8787`. Bind loopback sahaja. Upload raw PDF: `curl -H 'Content-Type: application/pdf' --data-binary @dokumen.pdf 'http://127.0.0.1:8787/jobs?prompt=Video%20korporat'`. Poll `GET /jobs/<id>`; apabila SUCCEEDED muat turun `/jobs/<id>/video.mp4`, `/captions.srt`, `/coverage.json`, `/manifest.json`.

CLI tanpa servis: `python3 -m core.worker submit dokumen.pdf --prompt 'Bina video'`, kemudian `python3 -m core.worker run-next`. Status/retry: `python3 -m core.worker status <id>` atau `retry <id>`; pastikan worker asal berhenti sebelum retry job RUNNING. Job disimpan pada disk/SQLite, proses mesti dimulakan semula selepas restart mesin.

Prompt belum disambungkan kepada provider AI. Tempoh/dimensi tetap untuk core Fasa 1; chat/provider/editor ialah fasa seterusnya. Untuk preview composition gunakan Studio repo, bukan timeline yang diwajibkan untuk render CLI.
