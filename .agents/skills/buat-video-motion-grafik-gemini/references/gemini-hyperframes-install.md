# Pasang dan jalankan HyperFrames dalam Gemini

## Kandungan

1. Skop dan keperluan
2. Semak cache dan alat asas
3. Pasang runtime terkunci ketika online
4. Salin projek, check dan render
5. Penyediaan offline dan pemulihan
6. Tafsir readiness dengan tepat

## 1. Skop dan keperluan

Gunakan pada Gemini Task/Spark atau VM yang benar-benar menyediakan shell, Node dan akses fail. Chat sahaja tidak membuktikan terminal, rangkaian atau pemasangan tersedia. Arahan `hyperframes skills update` daripada halaman Codex memasang skill untuk Codex; ia bukan arahan wajib atau jaminan auto-install skill dalam Gemini.

Runtime pakej ini dikunci kepada **HyperFrames 0.9.4**, **GSAP 3.15.0** dan lockfile di `assets/hyperframes/package-lock.json`. Tooling browser memerlukan **Node.js 22.12+**, npm, FFmpeg dan ffprobe. Chrome/Chromium headless mesti benar-benar boleh dilancarkan. Browser fallback npm dalam lock ialah Linux x86_64; OS/CPU lain memerlukan browser serasi yang disediakan secara berasingan.

Sumber rasmi: https://hyperframes.heygen.com/guides/with-codex dan https://hyperframes.heygen.com/guides/export-and-share . Pilih pemasangan Node rasmi daripada https://nodejs.org/en/download jika Node sesuai belum tersedia; jangan bergantung pada nama pakej OS tanpa menyemak versi sebenar. Untuk FFmpeg, gunakan package manager OS yang tersedia dan dibenarkan atau binary rasmi/terpercaya yang serasi. Docker, avatar, Kokoro dan MusicGen bukan keperluan render HTML setempat tanpa VO.

## 2. Semak cache dan alat asas

Pulihkan **core sahaja** untuk projek HTML asas melalui manifest semasa dan `gemini_cache.py plan/install/verify`. Preset Atlas memerlukan core + presets; fon/watak/SVG tambahan hanya apabila projek memerlukannya. Resolve folder sebenar dalam VM dan pilih cache yang boleh ditulis serta dipersist; jangan menyalin path `/root/.codex` dari ChatGPT.

Jalankan dari root toolkit yang mengandungi `SKILL.md`, `scripts/` dan `assets/`:

```bash
node --version
npm --version
ffmpeg -version
ffprobe -version
node scripts/setup_hyperframes.mjs --help
node scripts/setup_hyperframes.mjs
```

Default setup ialah **preflight tanpa muat turun** dengan cubaan melancarkan Chrome sebenar. Jika laporan `ready:true`, terus guna runtime itu. Simpan runtime path daripada laporan sebagai `KM_HYPERFRAMES_RUNTIME` jika menggunakan path selain cache default; jangan memasang semula hanya kerana projek baharu.

## 3. Pasang runtime terkunci ketika online

Apabila alat asas sudah tersedia tetapi dependency HTML/browser belum ready, pilih path cache sebenar yang boleh ditulis. Contoh di bawah menggunakan path mutlak yang perlu diganti mengikut VM:

```bash
export KM_HYPERFRAMES_RUNTIME="/absolute/persistent-cache/hyperframes-0.9.4"
node scripts/setup_hyperframes.mjs --runtime "$KM_HYPERFRAMES_RUNTIME" --online
node scripts/setup_hyperframes.mjs --runtime "$KM_HYPERFRAMES_RUNTIME"
```

Mod online menjalankan `npm ci` menggunakan package + lock yang dibundel. Untuk binari Node/Chrome/FFmpeg yang hilang, jalankan `python3 scripts/setup_video_components.py --install` mengikut runtime-lock.json; ulang preflight browser sebenar. Ia bukan `npm install latest`; jangan menukar versi HyperFrames/GSAP secara senyap. Semua empat plugin DrawSVGPlugin, MorphSVGPlugin, MotionPathPlugin dan SplitText mesti hadir. Jangan memanggil pemasang ini pada setiap render.

Jika VM sudah mempunyai Chrome/Chromium yang serasi:

```bash
node scripts/setup_hyperframes.mjs --runtime "$KM_HYPERFRAMES_RUNTIME" --browser /absolute/path/to/chrome
export HYPERFRAMES_BROWSER_PATH="/absolute/path/to/chrome"
```

Apabila preflight read-only digunakan dengan `--browser`, kekalkan `HYPERFRAMES_BROWSER_PATH` pada shell render yang sama. Jika pemasangan online/offline berjaya, helper menyimpan `browser-path.txt` dalam cache. Untuk ralat shared library pada Linux, semak error launch/`ldd` binary sebenar dan pasang hanya library OS yang hilang melalui package manager yang sesuai. Jangan menganggap nama library sama pada semua versi Ubuntu/Debian atau memasang Docker untuk membaiki dependency Chrome.

## 4. Salin projek, check dan render

Jangan sunting starter induk bagi setiap video. Dari root toolkit, salin starter ke direktori projek yang belum wujud:

```bash
cp -a assets/hyperframes /absolute/projects/video-baharu
node scripts/run_hyperframes.mjs doctor --json
node scripts/run_hyperframes.mjs lint /absolute/projects/video-baharu
node scripts/run_hyperframes.mjs check /absolute/projects/video-baharu --json
node scripts/run_hyperframes.mjs snapshot /absolute/projects/video-baharu --at 0,1,3,6,9 --describe false
node scripts/run_hyperframes.mjs render /absolute/projects/video-baharu --fps 30 --workers 1 --quality draft --output /absolute/projects/video-baharu/proof.mp4
```

Starter berdurasi 10 saat; ganti semua teks/artwork/timing dengan brief sebenar dan laras timestamp snapshot. Untuk melihat editor, jalankan `node scripts/run_hyperframes.mjs preview /absolute/projects/video-baharu`; simpan URL/PID/log. Selepas review/proof, gunakan `--quality delivery` untuk master. Pengguna yang sudah meminta video siap tidak memerlukan kelulusan tambahan hanya kerana contoh upstream memintanya.

Gunakan root `data-composition-id`, dimensi, `data-duration` dan timeline berhingga `paused:true`. Untuk 0.9.4, deklarasikan `window.__hf.buildReady[id]` secara sinkron, muatkan font/aset, bina semua tween dan daftar `window.__timelines[id]` pada akhir. Ikut `html-hyperframes-production.md`; jangan menggunakan ticker bebas atau mengubah DOM melalui callback yang tidak berjalan semasa seek.

Semak output sebenar:

```bash
ffprobe -v error -show_streams -show_format -of json /absolute/projects/video-baharu/proof.mp4
ffmpeg -v error -i /absolute/projects/video-baharu/proof.mp4 -f null -
```

Lihat frame/transisi dan playback/audio apabila tersedia. Lint/check atau ffprobe sahaja tidak membuktikan cerita, sebutan atau gerakan cantik. Semak `--help` versi terpasang sebelum menggunakan flag tambahan.

## 5. Penyediaan offline dan pemulihan

Sebelum mod offline, sediakan Node/FFmpeg, `node_modules` lengkap, browser sebenar, OS shared libraries, font, media serta model yang diperlukan pada OS/CPU sasaran. Npm cache tanpa browser dan dependency lengkap tidak mencukupi. Gunakan model/alat audio hanya apabila diperlukan, dengan preflight berasingan.

Jika cache npm lengkap tersedia dan binaan serasi, mod ini tidak menggunakan rangkaian:

```bash
node scripts/setup_hyperframes.mjs --runtime "$KM_HYPERFRAMES_RUNTIME" --install-offline
node scripts/setup_hyperframes.mjs --runtime "$KM_HYPERFRAMES_RUNTIME"
```

Mod itu menjalankan `npm ci --offline`; jangan gunakannya jika runtime sedia ada sudah ready. Apabila memindahkan runtime lengkap, set path cache/browser sebenar dan ulang preflight serta proof pendek. Jangan memasukkan binary/model besar ke ZIP core atau mendakwa runtime daripada mesin lain pasti serasi. Kekalkan cache dan model selepas membuang frame render.

Jika offline dan dependency perlu tiada, laporkan dependency/fail tepat yang hilang. Jangan cuba rangkaian berulang, menyimpan halaman login sebagai ZIP, mencipta folder kosong atau mendakwa pemasangan berjaya. Selepas online tersedia, pulihkan hanya komponen yang kurang.

## 6. Tafsir readiness dengan tepat

Bezakan pek core tersedia, HTML ready, ASR ready dan matting ready. `doctor --json` boleh keluar dengan code 0 tetapi `.ok:false`, termasuk kerana servis pilihan/Docker tiada. Nilai pemeriksaan yang diperlukan oleh projek; sahkan dengan helper setup dan render sebenar. Jangan memasang semua ciri pilihan untuk menghijaukan doktor.

`check` yang tidak menjalankan browser/layout atau melaporkan 0 samples bukan bukti gerakan lulus. Snapshot boleh menghasilkan PNG walaupun stdout JSON kosong; lihat fail sebenar. Simpan perbezaan seek/raster dengan bukti dan laporkan apa yang belum lulus. Ujian Linux setempat di ChatGPT bukan pengesahan dalam akaun Gemini pengguna.
