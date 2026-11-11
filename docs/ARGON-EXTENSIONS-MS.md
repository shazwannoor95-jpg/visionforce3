# Argon: preset dan extension

## Dipasang dan diuji pada mesin semasa

- Atlas: 922 preset boleh disenaraikan. Preset CFX15 berjaya dirender selama 2 saat; decode FFmpeg lulus. Ini ujian wakil, bukan semua 922 preset.
- Empat koleksi Bang Motion/Vox/Huashu/Claude Drawing: 175 resipi gaya lulus validator struktur; resipi bukan semua preset render automatik.
- HyperFrames 0.9.4, GSAP 3.15.0, Three.js, React, Remotion 4.0.540 dan Puppeteer-core dipasang dalam `/workspace/argon-runtime/hyperframes-0.9.4` daripada lockfile skill. Runtime ini berasingan daripada Remotion projek video 4.0.542.
- Plugin GSAP DrawSVG, MorphSVG, MotionPath dan SplitText: import lulus. React markup dan matriks Three.js lulus; Chromium DOM launch lulus.
- Demo HTML/GSAP HyperFrames 10 saat berjaya dirender menggunakan Chromium sistem, fallback screenshot/software GPU. Decode penuh FFmpeg lulus.
- Presets sumber, SVG, watak, motion-array, sebahagian payload vlog dan font sedia dalam fail skill seperti laporan pemasangan terdahulu. Kewujudan aset bukan bukti setiap aset sudah digunakan dalam render.

Bukti: argon-hyperframes-preflight.json, argon-render-tests.json. Video: artifacts/argon-cfx15.mp4 dan artifacts/argon-hyperframes.mp4.

## Bundle tidak dipasang

Pek Gemini fonts dan vlog_payload_03 masih gagal hash; semakan ZIP fonts turut menemui ralat header. Jangan memintas pemeriksaan ini. Bundle runtime lama Node 26, HyperFrames 0.8.185/0.9.2, Chrome 152 dan FFmpeg 9 juga gagal padanan hash manifest pada arkib lengkap; lihat argon-runtime-bundles.json. Dua bundle support/browser-libs lulus tetapi tidak diperlukan oleh runtime sistem yang lulus ujian. Versi lama tidak menggantikan runtime semasa.

Model VO/ASR/matting dan wheelhouse bukan preset/extension render yang diuji di sini; belum dipasang atau diuji. Tiada muat turun model tambahan atau servis berbayar dimulakan. Untuk bundle gagal, perlu fail lengkap yang sepadan dengan manifest asal sebelum pemasangan; tiada hash jangkaan diubah.

## Guna semula

`. scripts/activate-argon.sh` menetapkan path runtime untuk shell semasa. Jalankan `bash scripts/setup-argon.sh` hanya jika runtime hilang/tidak sah; ia memasang menggunakan lockfile dan menguji modul/browser. CLI: `node .agents/skills/buat-video-motion-grafik-gemini/scripts/run_hyperframes.mjs --help`. Atlas: `python3 .agents/skills/buat-video-motion-grafik-gemini/scripts/atlas_preset.py list`; semasa render gunakan `--cache /workspace/argon-runtime/atlas-cache` supaya tidak menulis ke home yang read-only.

Source, lockfile, arahan dan laporan disimpan dalam Git; node_modules kekal di luar Git. Snapshot Cloud dan pemulihan runtime dalam task baharu belum disahkan.
