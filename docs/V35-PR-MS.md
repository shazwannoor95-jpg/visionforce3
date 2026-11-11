# Asas V3.5: registry, queue worker CPU dan PDF ke MP4 dengan Source Lock

Sebelum ini repo mempunyai skill dan contoh render, tetapi tiada laluan job PDF berterusan. Perubahan ini menambah registry sumber/skill, pemeriksaan dependency terkunci, parser PDF, queue SQLite dengan atomic claim/retry manual, API pembangunan loopback dan composition Remotion yang menerima petikan sumber sebagai data.

Upload PDF menghasilkan scene beranimasi dengan petikan tepat dan nombor halaman. Output ialah MP4 H.264/AAC 1080p30, SRT, manifest dan coverage termasuk teks yang tidak digunakan. Planner deterministik, bukan integrasi LLM; audio ialah bed sintetik, bukan voice-over AI. Tiada kod daripada dokumen dilaksanakan. API ini belum sesuai untuk pendedahan awam/produksi.

Validasi: 6 ujian unit/integrasi API lulus, TypeScript lulus, dan dua ujian pipeline sebenar HTTP PDF upload -> SQLite -> render -> FFmpeg decode -> download lulus. Fixture menghasilkan 180 frame/6 saat; angka 42 dan petikan dipadankan kepada PDF. Preview diperiksa visual dan checksum frame video berlainan. Bukti dalam artifacts/v35-smoke dan docs/v35-smoke-result.json.

Repo visionforce2 diperiksa READ-ONLY (README sahaja); tidak diubah. Sepuluh sumber Git rasmi boleh dibaca. Semakan lesen komersial/distribusi masih diperlukan, terutama Remotion dan binary FFmpeg GPL. Integrasi provider, browser login/berbayar, chat UI, hybrid, editor dan GPU kekal fasa seterusnya. Tiada merge automatik.
